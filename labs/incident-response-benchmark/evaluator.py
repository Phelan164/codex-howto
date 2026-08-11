#!/usr/bin/env python3
import ast
import json
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path


IMMUTABLE_FIXTURE_FILES = (
    ".gitignore",
    "AGENTS.md",
    "README.md",
    "TASK.md",
    "test/test_store.py",
)
ALLOWED_CANDIDATE_FILES = set(IMMUTABLE_FIXTURE_FILES) | {
    "benchmark-final.md",
    "incident/__init__.py",
    "incident/server.py",
    "incident/store.py",
    "web/app.js",
    "web/index.html",
    "web/styles.css",
}


def assert_fixture_integrity(candidate, fixture):
    for relative in IMMUTABLE_FIXTURE_FILES:
        if (candidate / relative).read_bytes() != (fixture / relative).read_bytes():
            fail(f"fixture file changed: {relative}")


def assert_candidate_scope(candidate):
    actual = set()
    for path in candidate.rglob("*"):
        relative = path.relative_to(candidate)
        if path.is_symlink():
            fail(f"candidate symlink is not allowed: {relative.as_posix()}")
        if path.is_dir() or ".git" in relative.parts or "__pycache__" in relative.parts:
            continue
        if relative.parts[0] == "data" or path.suffix == ".pyc":
            continue
        actual.add(relative.as_posix())
    unexpected = sorted(actual - ALLOWED_CANDIDATE_FILES)
    missing = sorted(ALLOWED_CANDIDATE_FILES - actual)
    if unexpected:
        fail(f"unexpected candidate files: {', '.join(unexpected)}")
    if missing:
        fail(f"missing candidate files: {', '.join(missing)}")


def assert_atomic_replace(source):
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if (
            node.func.attr == "replace"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "os"
        ):
            return
    fail("store must call os.replace for atomic persistence")


def fail(message):
    raise AssertionError(message)


def check(name, operation, failures):
    try:
        operation()
        print(f"PASS {name}")
    except Exception as error:  # evaluator must report all independent failures
        failures.append(f"{name}: {error}")
        print(f"FAIL {name}: {error}", file=sys.stderr)


def main():
    if len(sys.argv) != 3:
        print("usage: evaluator.py <candidate-dir> <fixture-dir>", file=sys.stderr)
        return 2
    candidate, fixture = map(lambda value: Path(value).resolve(), sys.argv[1:])
    failures = []

    def fixture_and_scope():
        assert_candidate_scope(candidate)
        assert_fixture_integrity(candidate, fixture)

    def public_tests():
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "test", "-v"],
            cwd=candidate, text=True, capture_output=True, timeout=30,
        )
        if result.returncode:
            fail((result.stdout + result.stderr).strip())

    def store_edges():
        store_source = (candidate / "incident/store.py").read_text()
        assert_atomic_replace(store_source)
        helper = fixture / "checks/store_probe.py"
        try:
            result = subprocess.run(
                [sys.executable, str(helper), str(candidate)],
                text=True,
                capture_output=True,
                timeout=10,
            )
        except subprocess.TimeoutExpired:
            fail("store probe timed out; candidate may deadlock")
        if result.returncode:
            fail((result.stdout + result.stderr).strip())

    def server_contract():
        source = (candidate / "incident/server.py").read_text()
        tree = ast.parse(source)
        if not any(isinstance(node, ast.Call) and getattr(node.func, "id", "") == "main" for node in ast.walk(tree)):
            fail("server module has no main entry point call")
        with socket.socket() as reservation:
            reservation.bind(("127.0.0.1", 0))
            port = reservation.getsockname()[1]
        with tempfile.TemporaryDirectory() as directory:
            process = subprocess.Popen(
                [sys.executable, "-m", "incident.server", "--host", "127.0.0.1", "--port", str(port), "--data", str(Path(directory) / "incidents.json")],
                cwd=candidate, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            base = f"http://127.0.0.1:{port}"

            def request(path, method="GET", body=None):
                payload = None if body is None else json.dumps(body).encode()
                req = urllib.request.Request(base + path, data=payload, method=method)
                if payload is not None:
                    req.add_header("Content-Type", "application/json")
                with urllib.request.urlopen(req, timeout=3) as response:
                    content_type = response.headers.get_content_type()
                    raw = response.read()
                    return response.status, content_type, raw

            try:
                deadline = time.monotonic() + 5
                while True:
                    if process.poll() is not None:
                        stdout, stderr = process.communicate()
                        fail(f"server exited early: {stdout}\n{stderr}".strip())
                    try:
                        status, content_type, raw = request("/health")
                        break
                    except (OSError, urllib.error.URLError):
                        if time.monotonic() >= deadline:
                            fail("server did not become ready")
                        time.sleep(0.05)
                if (status, content_type, json.loads(raw)) != (200, "application/json", {"status": "ok"}):
                    fail("health response does not match contract")
                status, content_type, raw = request("/api/incidents", "POST", {"title": "Queue stalled", "severity": "sev2"})
                created = json.loads(raw)["incident"]
                if status != 201 or content_type != "application/json" or created["version"] != 1:
                    fail("create response does not match contract")
                status, _, raw = request("/api/incidents?severity=sev2")
                if status != 200 or json.loads(raw)["incidents"][0]["id"] != created["id"]:
                    fail("filtered list response does not match contract")
                status, _, raw = request(f"/api/incidents/{created['id']}", "PATCH", {"version": 1, "status": "mitigating"})
                if status != 200 or json.loads(raw)["incident"]["version"] != 2:
                    fail("update response does not match contract")
                try:
                    request(f"/api/incidents/{created['id']}", "PATCH", {"version": 1, "status": "resolved"})
                    fail("stale update did not return an error")
                except urllib.error.HTTPError as error:
                    if error.code != 409 or error.headers.get_content_type() != "application/json":
                        fail("stale update did not return JSON 409")
                for path, method, body, expected in (
                    ("/api/incidents", "POST", {"title": "", "severity": "sev2"}, 400),
                    ("/api/incidents/missing", "PATCH", {"version": 1, "status": "resolved"}, 404),
                ):
                    try:
                        request(path, method, body)
                        fail(f"{method} {path} did not return an error")
                    except urllib.error.HTTPError as error:
                        if error.code != expected or error.headers.get_content_type() != "application/json":
                            fail(f"{method} {path} did not return JSON {expected}")
                invalid = urllib.request.Request(
                    base + "/api/incidents",
                    data=b"{invalid",
                    method="POST",
                    headers={"Content-Type": "application/json"},
                )
                try:
                    urllib.request.urlopen(invalid, timeout=3)
                    fail("invalid JSON did not return an error")
                except urllib.error.HTTPError as error:
                    if error.code != 400 or error.headers.get_content_type() != "application/json":
                        fail("invalid JSON did not return JSON 400")
                status, content_type, raw = request("/")
                if status != 200 or content_type != "text/html" or b"incident-list" not in raw:
                    fail("root page was not served")
                try:
                    request("/web/%2e%2e/TASK.md")
                    fail("encoded path traversal was served")
                except urllib.error.HTTPError as error:
                    if error.code < 400:
                        fail("encoded path traversal was not rejected")
            finally:
                process.terminate()
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=3)

    def browser_contract():
        html = (candidate / "web/index.html").read_text()
        app = (candidate / "web/app.js").read_text()
        css = (candidate / "web/styles.css").read_text()
        combined = "\n".join((html, app, css)).lower()
        for token in ('id="incident-list"', 'id="message"', "aria-live", "<form", "<label"):
            if token not in html.lower():
                fail(f"index.html missing {token}")
        for token in ("/api/incidents", "fetch(", "version", "409"):
            if token.lower() not in app.lower():
                fail(f"app.js missing {token}")
        if "@media" not in css or ":focus" not in css:
            fail("styles lack responsive or visible-focus rules")
        if "http://" in combined or "https://" in combined:
            fail("external URL found")

    def handoff_contract():
        handoff = (candidate / "benchmark-final.md").read_text().lower()
        for term in ("changed", "check", "browser", "unverified", "risk", "integration"):
            if term not in handoff:
                fail(f"handoff does not address {term}")

    for name, operation in (
        ("fixture integrity and candidate scope pass", fixture_and_scope),
        ("supplied test suite passes", public_tests),
        ("concurrent and validation store edges pass", store_edges),
        ("integrated HTTP and static-server contract passes", server_contract),
        ("static browser contract is present", browser_contract),
        ("handoff topics are present", handoff_contract),
    ):
        check(name, operation, failures)

    if failures:
        print(f"\n{len(failures)} acceptance check(s) failed.", file=sys.stderr)
        return 1
    print("\nAll post-run acceptance checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
