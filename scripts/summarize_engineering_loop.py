#!/usr/bin/env python3
"""Validate and summarize engineering-loop skill-ablation records."""

from __future__ import annotations

import argparse
import csv
import statistics
import sys
from collections import defaultdict
from pathlib import Path


VARIANTS = ("no_skill", "full_skill", "lean_skill")
REQUIRED_BOOLEAN_FIELDS = (
    "accepted",
    "evidence_complete",
)
OPTIONAL_BOOLEAN_FIELDS = (
    "regression_before_fix",
    "focused_checks_passed",
    "required_checks_passed",
)
INTEGER_FIELDS = (
    "actionable_findings",
    "false_positives",
    "retries",
    "human_corrections",
    "total_tokens",
    "context_noise_lines",
)
FLOAT_FIELDS = ("elapsed_seconds", "total_cost_usd")
FIELDS = (
    "task_id",
    "variant",
    "run_id",
    "model",
    "reasoning_effort",
    "starting_commit",
    "tool_profile",
    "skill_version",
    "accepted",
    "evidence_complete",
    "regression_before_fix",
    "focused_checks_passed",
    "required_checks_passed",
    "actionable_findings",
    "false_positives",
    "retries",
    "human_corrections",
    "elapsed_seconds",
    "total_tokens",
    "total_cost_usd",
    "context_noise_lines",
    "notes",
)


def parse_boolean(value: str, field: str, row_number: int) -> bool:
    normalized = value.strip().lower()
    if normalized not in {"true", "false"}:
        raise ValueError(
            f"row {row_number}: {field} must be true or false, got {value!r}"
        )
    return normalized == "true"


def parse_nonnegative(
    value: str, field: str, row_number: int, number_type: type[int] | type[float]
) -> int | float | None:
    if not value.strip():
        return None
    try:
        parsed = number_type(value)
    except ValueError as exc:
        raise ValueError(
            f"row {row_number}: {field} must be a number, got {value!r}"
        ) from exc
    if parsed < 0:
        raise ValueError(f"row {row_number}: {field} must be nonnegative")
    return parsed


def load_rows(path: Path) -> list[dict[str, object]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError(
                "CSV header does not match the measurement template; "
                f"expected {','.join(FIELDS)}"
            )

        rows: list[dict[str, object]] = []
        seen_run_ids: set[str] = set()
        for row_number, raw in enumerate(reader, start=2):
            if None in raw or any(raw.get(field) is None for field in FIELDS):
                raise ValueError(
                    f"row {row_number}: column count does not match the CSV header"
                )
            task_id = raw["task_id"].strip()
            run_id = raw["run_id"].strip()
            variant = raw["variant"].strip()
            model = raw["model"].strip()
            reasoning_effort = raw["reasoning_effort"].strip()
            starting_commit = raw["starting_commit"].strip()
            tool_profile = raw["tool_profile"].strip()
            skill_version = raw["skill_version"].strip()
            if not all(
                (
                    task_id,
                    run_id,
                    model,
                    reasoning_effort,
                    starting_commit,
                    tool_profile,
                    skill_version,
                )
            ):
                raise ValueError(
                    f"row {row_number}: task_id, run_id, model, "
                    "reasoning_effort, starting_commit, tool_profile, and "
                    "skill_version are required"
                )
            if run_id in seen_run_ids:
                raise ValueError(f"row {row_number}: duplicate run_id {run_id!r}")
            if variant not in VARIANTS:
                raise ValueError(
                    f"row {row_number}: variant must be one of {VARIANTS}, "
                    f"got {variant!r}"
                )
            seen_run_ids.add(run_id)

            parsed: dict[str, object] = {
                "task_id": task_id,
                "run_id": run_id,
                "variant": variant,
                "model": model,
                "reasoning_effort": reasoning_effort,
                "starting_commit": starting_commit,
                "tool_profile": tool_profile,
                "skill_version": skill_version,
                "notes": raw["notes"].strip(),
            }
            for field in REQUIRED_BOOLEAN_FIELDS:
                parsed[field] = parse_boolean(raw[field], field, row_number)
            for field in OPTIONAL_BOOLEAN_FIELDS:
                parsed[field] = (
                    parse_boolean(raw[field], field, row_number)
                    if raw[field].strip()
                    else None
                )
            for field in INTEGER_FIELDS:
                parsed[field] = parse_nonnegative(
                    raw[field], field, row_number, int
                )
            for field in FLOAT_FIELDS:
                parsed[field] = parse_nonnegative(
                    raw[field], field, row_number, float
                )
            rows.append(parsed)
    validate_task_sets(rows)
    return rows


def validate_task_sets(rows: list[dict[str, object]]) -> None:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["task_id"])].append(row)

    controlled_fields = (
        "model",
        "reasoning_effort",
        "starting_commit",
        "tool_profile",
    )
    for task_id, task_rows in grouped.items():
        variants = [str(row["variant"]) for row in task_rows]
        if len(variants) != len(set(variants)):
            raise ValueError(f"task {task_id!r}: duplicate variant")

        controls = {
            tuple(str(row[field]) for field in controlled_fields)
            for row in task_rows
        }
        if len(controls) > 1:
            raise ValueError(
                f"task {task_id!r}: controlled fields must match across variants"
            )


def rate(rows: list[dict[str, object]], field: str) -> tuple[int, int, float]:
    observed = [row[field] for row in rows if row[field] is not None]
    positive = sum(value is True for value in observed)
    total = len(observed)
    percentage = (positive / total * 100) if total else 0.0
    return positive, total, percentage


def median(rows: list[dict[str, object]], field: str) -> float | None:
    observed = [float(row[field]) for row in rows if row[field] is not None]
    return statistics.median(observed) if observed else None


def format_median(value: float | None) -> str:
    return "n/a" if value is None else f"{value:g}"


def summarize(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "No measurement rows found.\n"

    grouped = {
        variant: [row for row in rows if row["variant"] == variant]
        for variant in VARIANTS
    }
    lines = [
        "# Engineering-loop skill-ablation summary",
        "",
        "## Quality gates",
        "",
        "| Variant | Runs | Accepted | Evidence complete | Regression before fix | Focused checks passed | Required checks passed |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for variant, variant_rows in grouped.items():
        rate_cells = []
        for field in (
            "accepted",
            "evidence_complete",
            "regression_before_fix",
            "focused_checks_passed",
            "required_checks_passed",
        ):
            positive, total, percentage = rate(variant_rows, field)
            rate_cells.append(
                "n/a" if total == 0 else f"{positive}/{total} ({percentage:.0f}%)"
            )
        lines.append(
            f"| {variant} | {len(variant_rows)} | " + " | ".join(rate_cells) + " |"
        )

    lines.extend(
        [
            "",
            "## Efficiency and review medians",
            "",
            "| Variant | Actionable findings | False positives | Retries | Human corrections | Elapsed seconds | Total tokens | Cost USD | Context-noise lines |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    median_fields = (
        "actionable_findings",
        "false_positives",
        "retries",
        "human_corrections",
        "elapsed_seconds",
        "total_tokens",
        "total_cost_usd",
        "context_noise_lines",
    )
    for variant, variant_rows in grouped.items():
        cells = [format_median(median(variant_rows, field)) for field in median_fields]
        lines.append(f"| {variant} | " + " | ".join(cells) + " |")

    task_variants: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        task_variants[str(row["task_id"])].add(str(row["variant"]))
    complete = sum(
        set(VARIANTS).issubset(variants) for variants in task_variants.values()
    )
    lines.extend(
        [
            "",
            "## Coverage",
            "",
            f"- Complete three-way tasks: {complete}/{len(task_variants)}",
            f"- Total runs: {len(rows)}",
            "",
            "Interpret quality gates before speed, token, or cost differences.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and summarize engineering-loop ablation CSV data."
    )
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()
    try:
        rows = load_rows(args.csv_path)
    except (OSError, ValueError) as exc:
        print(f"Measurement data error: {exc}", file=sys.stderr)
        return 1
    print(summarize(rows), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
