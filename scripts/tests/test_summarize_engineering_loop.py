from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from summarize_engineering_loop import FIELDS, load_rows, summarize


class SummarizeEngineeringLoopTest(unittest.TestCase):
    def write_csv(self, rows: list[list[str]]) -> Path:
        temporary = tempfile.NamedTemporaryFile(
            mode="w", newline="", encoding="utf-8", delete=False
        )
        self.addCleanup(Path(temporary.name).unlink, missing_ok=True)
        temporary.write(",".join(FIELDS) + "\n")
        for row in rows:
            temporary.write(",".join(row) + "\n")
        temporary.close()
        return Path(temporary.name)

    def test_summarizes_three_way_quality_and_efficiency(self) -> None:
        rows = [
            [
                "backend",
                "no_skill",
                "baseline-1",
                "gpt-5.6-sol",
                "medium",
                "abc123",
                "local-default",
                "none",
                "false",
                "false",
                "false",
                "true",
                "true",
                "0",
                "1",
                "2",
                "1",
                "120",
                "1000",
                "0.10",
                "20",
                "",
            ],
            [
                "backend",
                "full_skill",
                "full-1",
                "gpt-5.6-sol",
                "medium",
                "abc123",
                "local-default",
                "v0.2.0",
                "true",
                "true",
                "true",
                "true",
                "true",
                "1",
                "0",
                "1",
                "0",
                "160",
                "1500",
                "0.15",
                "8",
                "",
            ],
            [
                "backend",
                "lean_skill",
                "lean-1",
                "gpt-5.6-sol",
                "medium",
                "abc123",
                "local-default",
                "v0.3.0",
                "true",
                "true",
                "true",
                "true",
                "true",
                "1",
                "0",
                "0",
                "0",
                "150",
                "1200",
                "0.12",
                "4",
                "",
            ],
        ]
        output = summarize(load_rows(self.write_csv(rows)))
        self.assertIn("| no_skill | 1 | 0/1 (0%)", output)
        self.assertIn("| full_skill | 1 | 1/1 (100%)", output)
        self.assertIn("| lean_skill | 1 | 1/1 (100%)", output)
        self.assertIn("- Complete three-way tasks: 1/1", output)

    def test_rejects_unknown_variant(self) -> None:
        row = [
            "backend",
            "unknown",
            "run-1",
            "gpt-5.6-sol",
            "medium",
            "abc123",
            "local-default",
            "none",
            "true",
            "true",
            "",
            "true",
            "true",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        with self.assertRaisesRegex(ValueError, "variant must be one of"):
            load_rows(self.write_csv([row]))

    def test_empty_template_is_valid(self) -> None:
        path = self.write_csv([])
        self.assertEqual(load_rows(path), [])
        self.assertEqual(summarize([]), "No measurement rows found.\n")

    def test_requires_model_reasoning_and_skill_version(self) -> None:
        row = [
            "backend",
            "no_skill",
            "run-1",
            "",
            "medium",
            "abc123",
            "local-default",
            "none",
            "true",
            "true",
            "",
            "true",
            "true",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        with self.assertRaisesRegex(ValueError, "model.*required"):
            load_rows(self.write_csv([row]))

    def test_rejects_mismatched_controlled_fields(self) -> None:
        rows = [
            self.valid_row("no_skill", "baseline-1"),
            self.valid_row(
                "lean_skill", "lean-1", model="gpt-5.5", reasoning_effort="high"
            ),
        ]
        with self.assertRaisesRegex(ValueError, "controlled fields must match"):
            load_rows(self.write_csv(rows))

    def test_rejects_duplicate_variant_for_task(self) -> None:
        rows = [
            self.valid_row("no_skill", "baseline-1"),
            self.valid_row("no_skill", "baseline-2"),
        ]
        with self.assertRaisesRegex(ValueError, "duplicate variant"):
            load_rows(self.write_csv(rows))

    def valid_row(
        self,
        variant: str,
        run_id: str,
        *,
        model: str = "gpt-5.6-sol",
        reasoning_effort: str = "medium",
    ) -> list[str]:
        return [
            "backend",
            variant,
            run_id,
            model,
            reasoning_effort,
            "abc123",
            "local-default",
            "none" if variant == "no_skill" else "v0.3.0",
            "true",
            "true",
            "",
            "true",
            "true",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]

    def test_rejects_wrong_column_count(self) -> None:
        with self.assertRaisesRegex(ValueError, "column count"):
            load_rows(self.write_csv([["backend", "no_skill"]]))


if __name__ == "__main__":
    unittest.main()
