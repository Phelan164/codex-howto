#!/usr/bin/env python3
"""Validate a review-first Codex knowledge wiki using only the standard library."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlparse


SOURCE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SOURCE_REF_RE = re.compile(r"`([a-z0-9]+(?:-[a-z0-9]+)*)`")
STATUS_RE = re.compile(r"^>\s*Status:\s*(\S+)\s*$", re.IGNORECASE)
VERIFIED_RE = re.compile(
    r"^>\s*Last verified:\s*(\d{4}-\d{2}-\d{2})\s*$", re.IGNORECASE
)
SOURCES_RE = re.compile(r"^>\s*Sources:\s*(.+?)\s*$", re.IGNORECASE)
ALLOWED_KINDS = {"official", "repository", "community", "experiment"}
ALLOWED_STATUSES = {"verified", "community", "experimental", "decision"}
PAGE_DIRS = ("topics", "decisions", "experiments")


def parse_date(value: str, label: str, errors: list[str]) -> None:
    try:
        date.fromisoformat(value)
    except ValueError:
        errors.append(f"{label}: expected ISO date YYYY-MM-DD, got {value!r}")


def load_sources(root: Path, errors: list[str]) -> dict[str, dict[str, str]]:
    path = root / "knowledge" / "sources.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append("missing knowledge/sources.json")
        return {}
    except json.JSONDecodeError as exc:
        errors.append(f"invalid knowledge/sources.json: {exc}")
        return {}

    if payload.get("schema_version") != 1:
        errors.append("knowledge/sources.json: schema_version must be 1")
    items = payload.get("sources")
    if not isinstance(items, list):
        errors.append("knowledge/sources.json: sources must be a list")
        return {}

    sources: dict[str, dict[str, str]] = {}
    for position, item in enumerate(items, start=1):
        label = f"knowledge/sources.json source #{position}"
        if not isinstance(item, dict):
            errors.append(f"{label}: expected an object")
            continue
        source_id = item.get("id")
        if not isinstance(source_id, str) or not SOURCE_ID_RE.fullmatch(source_id):
            errors.append(f"{label}: invalid id {source_id!r}")
            continue
        if source_id in sources:
            errors.append(f"{label}: duplicate id {source_id!r}")
            continue
        sources[source_id] = item

        if not isinstance(item.get("title"), str) or not item["title"].strip():
            errors.append(f"{label}: title is required")
        if item.get("kind") not in ALLOWED_KINDS:
            errors.append(
                f"{label}: kind must be one of {', '.join(sorted(ALLOWED_KINDS))}"
            )
        verified = item.get("last_verified")
        if not isinstance(verified, str):
            errors.append(f"{label}: last_verified is required")
        else:
            parse_date(verified, f"{label} last_verified", errors)

        has_url = "url" in item
        has_path = "path" in item
        if has_url == has_path:
            errors.append(f"{label}: define exactly one of url or path")
        elif has_url:
            url = item["url"]
            parsed = urlparse(url) if isinstance(url, str) else None
            if not parsed or parsed.scheme != "https" or not parsed.netloc:
                errors.append(f"{label}: url must be an absolute HTTPS URL")
        else:
            local = item["path"]
            if not isinstance(local, str) or not local:
                errors.append(f"{label}: path must be a non-empty string")
                continue
            target = (root / local).resolve()
            if not target.is_relative_to(root.resolve()):
                errors.append(f"{label}: path escapes the project root")
            elif not target.is_file():
                errors.append(f"{label}: local source does not exist: {local}")
    return sources


def wiki_pages(root: Path) -> list[Path]:
    knowledge = root / "knowledge"
    pages: list[Path] = []
    for name in PAGE_DIRS:
        directory = knowledge / name
        if directory.is_dir():
            pages.extend(directory.rglob("*.md"))
    return sorted(pages)


def page_metadata(
    path: Path, root: Path, known_sources: set[str], errors: list[str]
) -> set[str]:
    relative = path.relative_to(root).as_posix()
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or not lines[0].startswith("# "):
        errors.append(f"{relative}: first line must be an H1")

    status = None
    verified = None
    source_ids: set[str] = set()
    for line in lines[1:12]:
        if match := STATUS_RE.match(line):
            status = match.group(1).lower()
        elif match := VERIFIED_RE.match(line):
            verified = match.group(1)
        elif match := SOURCES_RE.match(line):
            source_ids = set(SOURCE_REF_RE.findall(match.group(1)))

    if status not in ALLOWED_STATUSES:
        errors.append(
            f"{relative}: Status must be one of "
            f"{', '.join(sorted(ALLOWED_STATUSES))}"
        )
    if verified is None:
        errors.append(f"{relative}: missing Last verified metadata")
    else:
        parse_date(verified, f"{relative} Last verified", errors)
    if not source_ids:
        errors.append(f"{relative}: Sources must contain at least one backticked ID")
    for source_id in sorted(source_ids - known_sources):
        errors.append(f"{relative}: unknown source ID {source_id!r}")
    return source_ids


def check_index(root: Path, pages: list[Path], errors: list[str]) -> None:
    index = root / "knowledge" / "index.md"
    try:
        text = index.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append("missing knowledge/index.md")
        return

    indexed: set[Path] = set()
    for target in LINK_RE.findall(text):
        local = target.partition("#")[0]
        if not local or local.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (index.parent / unquote(local)).resolve()
        if any(resolved.is_relative_to((root / "knowledge" / name).resolve()) for name in PAGE_DIRS):
            indexed.add(resolved)

    for page in pages:
        if page.resolve() not in indexed:
            errors.append(
                f"knowledge/index.md: missing page "
                f"{page.relative_to(root / 'knowledge').as_posix()}"
            )


def check_local_links(root: Path, errors: list[str]) -> None:
    knowledge = root / "knowledge"
    if not knowledge.is_dir():
        errors.append("missing knowledge/ directory")
        return
    for path in sorted(knowledge.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            local = target.partition("#")[0]
            if not local or local.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / unquote(local)).resolve()
            if not resolved.is_relative_to(root.resolve()):
                errors.append(
                    f"{path.relative_to(root)}: link escapes project root: {target}"
                )
            elif not resolved.exists():
                errors.append(
                    f"{path.relative_to(root)}: broken local link: {target}"
                )


def validate(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    sources = load_sources(root, errors)
    pages = wiki_pages(root)
    if not pages:
        errors.append("knowledge/: no topic, decision, or experiment pages found")

    referenced: set[str] = set()
    for page in pages:
        referenced.update(page_metadata(page, root, set(sources), errors))
    for source_id in sorted(set(sources) - referenced):
        warnings.append(f"unreferenced source: {source_id}")

    check_index(root, pages, errors)
    check_local_links(root, errors)
    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "project_root",
        nargs="?",
        default=".",
        help="repository containing knowledge/ (default: current directory)",
    )
    args = parser.parse_args(argv)
    root = Path(args.project_root).resolve()
    errors, warnings = validate(root)

    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    if errors:
        print(
            f"Wiki lint failed: {len(errors)} error(s), {len(warnings)} warning(s).",
            file=sys.stderr,
        )
        return 1
    print(f"Wiki lint passed: {len(wiki_pages(root))} pages, {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
