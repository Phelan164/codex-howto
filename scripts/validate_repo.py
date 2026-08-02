#!/usr/bin/env python3
"""Validate the repository structure, local links, and starter skill metadata."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
UI_FIELD_RE = re.compile(r'^  ([a-z_]+):\s+("(?:[^"\\]|\\.)*")\s*$')
REQUIRED_ROOT = {
    ".github/pull_request_template.md",
    ".github/workflows/benchmark-site.yml",
    ".github/workflows/validate.yml",
    ".codex-plugin/plugin.json",
    "README.md",
    "LEARNING-ROADMAP.md",
    "CATALOG.md",
    "CHANGELOG.md",
    "COMMUNITY.md",
    "QUICK_REFERENCE.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "site/README.md",
    "AGENTS.md",
    "LICENSE",
    "assets/social-preview.png",
    "assets/social-preview.svg",
    "resources/community-launch-kit.md",
    "resources/articles/do-codex-skills-save-tokens.md",
    "resources/distribution-shortlist.md",
    "resources/model-adaptive-skills.md",
    "resources/release-notes-v0.5.0.md",
    "resources/release-notes-v0.4.0.md",
    "resources/release-notes-v0.3.0.md",
    "resources/release-notes-v0.2.0.md",
    "examples/skills/choose-engineering-flow/SKILL.md",
    "examples/skills/choose-engineering-flow/agents/openai.yaml",
    "knowledge/README.md",
    "knowledge/index.md",
    "knowledge/log.md",
    "knowledge/sources.json",
    "knowledge/decisions/review-first-wiki.md",
    "knowledge/experiments/wiki-efficiency-baseline.md",
}
REQUIRED_MODULES = {
    "00-mental-model",
    "01-sandbox-and-approvals",
    "02-cli-and-surfaces",
    "03-prompts-and-plans",
    "04-agents-md",
    "05-engineering-skills",
    "06-mcp-and-tools",
    "07-testing-and-review",
    "08-subagents",
    "09-orchestration",
    "10-context-and-token-efficiency",
    "11-automation-plugins-hooks",
    "12-troubleshooting",
    "13-living-codex-wiki",
}
REQUIRED_SKILLS = {
    "engineering-loop",
    "build-frontend",
    "build-backend",
    "operate-devops",
    "review-code",
    "test-software",
    "review-security",
    "orchestrate-engineering",
    "maintain-codex-wiki",
}
EXPLICIT_ONLY_SKILLS = {
    "choose-engineering-flow",
    "maintain-codex-wiki",
    "orchestrate-engineering",
}
REQUIRED_LAB_FILES = {
    "labs/engineering-playground/README.md",
    "labs/engineering-playground/AGENTS.md",
    "labs/engineering-playground/backend/inventory.py",
    "labs/engineering-playground/backend/test_inventory.py",
    "labs/engineering-playground/frontend/checkout.html",
    "labs/engineering-playground/infra/deployment.yaml",
    "labs/engineering-playground/rubric.md",
}
REQUIRED_MEASUREMENT_FILES = {
    "examples/measurements/engineering-loop-runs.csv",
    "examples/measurements/gpt-5.6-sol-2048-game-2026-07-31.md",
    "labs/2048-game-benchmark/AGENTS.md",
    "labs/2048-game-benchmark/README.md",
    "labs/2048-game-benchmark/TASK.md",
    "labs/2048-game-benchmark/evaluator.mjs",
    "labs/2048-game-benchmark/test/engine.test.mjs",
    "resources/engineering-loop-measurement.md",
    "scripts/summarize_engineering_loop.py",
    "scripts/tests/test_summarize_engineering_loop.py",
}
REQUIRED_JSON = {
    ".codex-plugin/plugin.json",
    "examples/hooks/validate-on-stop/hooks.json",
    "examples/plugin-marketplace/.agents/plugins/marketplace.json",
    "examples/plugin-marketplace/plugins/engineering-review/.codex-plugin/plugin.json",
    "knowledge/sources.json",
}
IGNORED_PATH_PARTS = {
    ".git",
    ".next",
    ".wrangler",
    "dist",
    "node_modules",
}


def repository_files(pattern: str) -> list[Path]:
    """Return repository source files while excluding generated/vendor trees."""
    return [
        path
        for path in ROOT.rglob(pattern)
        if not IGNORED_PATH_PARTS.intersection(path.relative_to(ROOT).parts)
    ]


def check_required(errors: list[str]) -> None:
    for name in sorted(REQUIRED_ROOT):
        if not (ROOT / name).is_file():
            errors.append(f"missing required root file: {name}")
    for name in sorted(REQUIRED_LAB_FILES):
        if not (ROOT / name).is_file():
            errors.append(f"missing required engineering lab file: {name}")
    for name in sorted(REQUIRED_MEASUREMENT_FILES):
        if not (ROOT / name).is_file():
            errors.append(f"missing required measurement artifact: {name}")


def check_json_examples(errors: list[str]) -> None:
    for name in sorted(REQUIRED_JSON):
        path = ROOT / name
        if not path.is_file():
            errors.append(f"missing required JSON example: {name}")
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON example {name}: {exc}")


def check_links(errors: list[str]) -> None:
    for path in repository_files("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            target = target.strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue

            local, separator, fragment = target.partition("#")
            resolved = path if not local else (path.parent / unquote(local)).resolve()
            if not resolved.exists():
                errors.append(
                    f"broken local link: {path.relative_to(ROOT)} -> {target}"
                )
                continue

            if separator and fragment:
                markdown_path = resolved
                if resolved.is_dir():
                    markdown_path = resolved / "README.md"
                if markdown_path.suffix.lower() != ".md" or not markdown_path.is_file():
                    errors.append(
                        f"anchor targets a non-Markdown file: "
                        f"{path.relative_to(ROOT)} -> {target}"
                    )
                    continue
                anchors = markdown_anchors(markdown_path)
                if unquote(fragment).lower() not in anchors:
                    errors.append(
                        f"broken local anchor: {path.relative_to(ROOT)} -> {target}"
                    )


def markdown_anchors(path: Path) -> set[str]:
    """Return GitHub-style heading IDs for the subset used in this repository."""
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = HEADING_RE.match(line)
        if not match:
            continue
        heading = html.unescape(match.group(1))
        heading = re.sub(r"<[^>]+>", "", heading)
        heading = re.sub(r"[`*_~]", "", heading).strip().lower()
        base = re.sub(r"[^\w\- ]", "", heading, flags=re.UNICODE)
        base = re.sub(r"\s+", "-", base)
        count = counts.get(base, 0)
        anchor = base if count == 0 else f"{base}-{count}"
        counts[base] = count + 1
        anchors.add(anchor)
    return anchors


def parse_frontmatter(path: Path, errors: list[str]) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        errors.append(f"missing YAML frontmatter: {path.relative_to(ROOT)}")
        return {}

    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"invalid frontmatter line in {path.relative_to(ROOT)}")
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip()

    if set(values) != {"name", "description"}:
        errors.append(
            f"frontmatter must contain only name and description: "
            f"{path.relative_to(ROOT)}"
        )
    return values


def check_skills(errors: list[str]) -> None:
    skills_dir = ROOT / "skills"
    skill_dirs = sorted(path for path in skills_dir.iterdir() if path.is_dir())
    if not skill_dirs:
        errors.append("no skills found")
        return
    actual_names = {path.name for path in skill_dirs}
    for name in sorted(REQUIRED_SKILLS - actual_names):
        errors.append(f"missing required engineering skill: {name}")

    for skill_dir in skill_dirs:
        check_skill_dir(skill_dir, errors)

    example_skill = ROOT / "examples" / "skills" / "choose-engineering-flow"
    if example_skill.is_dir():
        check_skill_dir(example_skill, errors)


def check_skill_dir(skill_dir: Path, errors: list[str]) -> None:
    skill_file = skill_dir / "SKILL.md"
    ui_file = skill_dir / "agents" / "openai.yaml"
    if not skill_file.is_file():
        errors.append(f"missing SKILL.md: {skill_dir.relative_to(ROOT)}")
        return
    if not ui_file.is_file():
        errors.append(
            f"missing agents/openai.yaml: {skill_dir.relative_to(ROOT)}"
        )

    values = parse_frontmatter(skill_file, errors)
    name = values.get("name", "")
    description = values.get("description", "")
    if name != skill_dir.name:
        errors.append(f"skill name/folder mismatch: {skill_dir.name} vs {name}")
    if len(description) < 80:
        errors.append(f"skill description is too short: {skill_dir.name}")

    if ui_file.is_file():
        check_ui_metadata(ui_file, skill_dir.name, errors)


def check_ui_metadata(path: Path, skill_name: str, errors: list[str]) -> None:
    """Validate the strict YAML subset generated for starter skill UI metadata."""
    lines = [
        line for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not lines or lines[0] != "interface:":
        errors.append(f"invalid UI metadata root: {path.relative_to(ROOT)}")
        return

    policy_index = lines.index("policy:") if "policy:" in lines else len(lines)
    values: dict[str, str] = {}
    for line in lines[1:policy_index]:
        match = UI_FIELD_RE.fullmatch(line)
        if not match:
            errors.append(f"invalid UI metadata YAML: {path.relative_to(ROOT)}")
            return
        key, encoded_value = match.groups()
        if key in values:
            errors.append(
                f"duplicate UI metadata field {key}: {path.relative_to(ROOT)}"
            )
            return
        values[key] = json.loads(encoded_value)

    expected = {"display_name", "short_description", "default_prompt"}
    if set(values) != expected:
        errors.append(
            f"UI metadata fields must be {sorted(expected)}: {path.relative_to(ROOT)}"
        )
        return
    if not 25 <= len(values["short_description"]) <= 64:
        errors.append(f"invalid short_description length: {path.relative_to(ROOT)}")
    if f"${skill_name}" not in values["default_prompt"]:
        errors.append(
            f"default_prompt must mention ${skill_name}: {path.relative_to(ROOT)}"
        )

    policy_lines = lines[policy_index:]
    expected_policy = ["policy:", "  allow_implicit_invocation: false"]
    if policy_lines and policy_lines != expected_policy:
        errors.append(f"invalid invocation policy: {path.relative_to(ROOT)}")
    if skill_name in EXPLICIT_ONLY_SKILLS and policy_lines != expected_policy:
        errors.append(
            f"{skill_name} must disable implicit invocation: "
            f"{path.relative_to(ROOT)}"
        )


def check_modules(errors: list[str]) -> None:
    modules = sorted((ROOT / "modules").glob("*/README.md"))
    actual_names = {
        path.name for path in (ROOT / "modules").iterdir() if path.is_dir()
    }
    for name in sorted(REQUIRED_MODULES - actual_names):
        errors.append(f"missing required learning module: {name}")
    for name in sorted(actual_names - REQUIRED_MODULES):
        errors.append(f"unexpected or stale learning module: {name}")
    for path in modules:
        text = path.read_text(encoding="utf-8")
        for heading in ("## Outcome", "## Verify"):
            if heading not in text:
                errors.append(f"{path.relative_to(ROOT)} missing {heading}")


def check_placeholders(errors: list[str]) -> None:
    for path in repository_files("*.md") + repository_files("*.yaml"):
        text = path.read_text(encoding="utf-8")
        if "[TODO" in text or "TODO]" in text:
            errors.append(f"unfinished TODO placeholder: {path.relative_to(ROOT)}")


def check_wiki(errors: list[str]) -> None:
    script = ROOT / "skills" / "maintain-codex-wiki" / "scripts" / "wiki_lint.py"
    if not script.is_file():
        errors.append("missing living-wiki lint script")
        return
    result = subprocess.run(
        [sys.executable, str(script), str(ROOT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        details = (result.stderr or result.stdout).strip()
        errors.append(f"living-wiki lint failed: {details}")


def main() -> int:
    errors: list[str] = []
    check_required(errors)
    check_links(errors)
    check_json_examples(errors)
    check_skills(errors)
    check_modules(errors)
    check_placeholders(errors)
    check_wiki(errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    module_count = len(list((ROOT / "modules").glob("*/README.md")))
    skill_count = len([path for path in (ROOT / "skills").iterdir() if path.is_dir()])
    print(
        "Validation passed: "
        f"{module_count} modules, {skill_count} skills, "
        "all required goal artifacts present."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
