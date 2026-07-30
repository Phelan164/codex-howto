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

    def test_summarizes_paired_quality_and_efficiency(self) -> None:
        rows = [
            [
                "backend",
                "ad_hoc",
                "baseline-1",
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
                "engineering_loop",
                "loop-1",
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
        self.assertIn("| ad_hoc | 1 | 0/1 (0%)", output)
        self.assertIn("| engineering_loop | 1 | 1/1 (100%)", output)
        self.assertIn("- Paired tasks: 1/1", output)

    def test_rejects_unknown_variant(self) -> None:
        row = [
            "backend",
            "unknown",
            "run-1",
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

    def test_rejects_wrong_column_count(self) -> None:
        with self.assertRaisesRegex(ValueError, "column count"):
            load_rows(self.write_csv([["backend", "ad_hoc"]]))


if __name__ == "__main__":
    unittest.main()
