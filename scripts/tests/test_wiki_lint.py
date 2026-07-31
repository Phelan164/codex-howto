import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills" / "maintain-codex-wiki" / "scripts" / "wiki_lint.py"
SPEC = importlib.util.spec_from_file_location("wiki_lint", SCRIPT)
assert SPEC and SPEC.loader
WIKI_LINT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(WIKI_LINT)


class WikiLintTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "evidence.md").write_text("# Evidence\n", encoding="utf-8")
        (self.root / "knowledge" / "topics").mkdir(parents=True)
        (self.root / "knowledge" / "decisions").mkdir()
        (self.root / "knowledge" / "experiments").mkdir()
        self.write_registry(
            [
                {
                    "id": "local-evidence",
                    "title": "Local evidence",
                    "kind": "repository",
                    "path": "evidence.md",
                    "last_verified": "2026-07-31",
                    "revision": "abc123",
                    "affected_pages": ["knowledge/topics/example.md"],
                }
            ]
        )
        self.page = self.root / "knowledge" / "topics" / "example.md"
        self.page.write_text(
            """# Example

> Status: verified
> Last verified: 2026-07-31
> Sources: `local-evidence`

See the [index](../index.md).
""",
            encoding="utf-8",
        )
        (self.root / "knowledge" / "index.md").write_text(
            "# Index\n\n- [Example](topics/example.md)\n", encoding="utf-8"
        )
        (self.root / "knowledge" / "README.md").write_text(
            "# Knowledge\n", encoding="utf-8"
        )
        (self.root / "knowledge" / "log.md").write_text(
            "# Log\n", encoding="utf-8"
        )

    def tearDown(self):
        self.temp.cleanup()

    def write_registry(self, sources):
        (self.root / "knowledge" / "sources.json").write_text(
            json.dumps({"schema_version": 1, "sources": sources}),
            encoding="utf-8",
        )

    def validate(self):
        return WIKI_LINT.validate(self.root)

    def test_valid_wiki_passes(self):
        errors, warnings = self.validate()
        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_unknown_source_is_rejected(self):
        self.page.write_text(
            self.page.read_text(encoding="utf-8").replace(
                "`local-evidence`", "`missing-source`"
            ),
            encoding="utf-8",
        )
        errors, warnings = self.validate()
        self.assertTrue(any("unknown source ID" in error for error in errors))
        self.assertEqual(["unreferenced source: local-evidence"], warnings)

    def test_page_missing_from_index_is_rejected(self):
        (self.root / "knowledge" / "index.md").write_text(
            "# Index\n", encoding="utf-8"
        )
        errors, _ = self.validate()
        self.assertTrue(any("missing page topics/example.md" in error for error in errors))

    def test_missing_local_source_is_rejected(self):
        (self.root / "evidence.md").unlink()
        errors, _ = self.validate()
        self.assertTrue(
            any("local source does not exist: evidence.md" in error for error in errors)
        )

    def test_broken_local_link_is_rejected(self):
        self.page.write_text(
            self.page.read_text(encoding="utf-8").replace(
                "../index.md", "../missing.md"
            ),
            encoding="utf-8",
        )
        errors, _ = self.validate()
        self.assertTrue(any("broken local link" in error for error in errors))

    def test_duplicate_source_id_is_rejected(self):
        source = {
            "id": "local-evidence",
            "title": "Local evidence",
            "kind": "repository",
            "path": "evidence.md",
            "last_verified": "2026-07-31",
        }
        self.write_registry([source, source])
        errors, _ = self.validate()
        self.assertTrue(any("duplicate id" in error for error in errors))

    def test_page_metadata_is_required(self):
        self.page.write_text("# Example\n", encoding="utf-8")
        errors, _ = self.validate()
        self.assertTrue(any("Status must be one of" in error for error in errors))
        self.assertTrue(any("missing Last verified" in error for error in errors))
        self.assertTrue(any("Sources must contain" in error for error in errors))

    def test_empty_page_reports_errors_without_crashing(self):
        self.page.write_text("", encoding="utf-8")
        errors, _ = self.validate()
        self.assertTrue(any("first line must be an H1" in error for error in errors))

    def test_empty_source_revision_is_rejected(self):
        self.write_registry(
            [
                {
                    "id": "local-evidence",
                    "title": "Local evidence",
                    "kind": "repository",
                    "path": "evidence.md",
                    "last_verified": "2026-07-31",
                    "revision": "",
                }
            ]
        )
        errors, _ = self.validate()
        self.assertTrue(any("revision must be a non-empty string" in e for e in errors))

    def test_unknown_superseded_source_is_rejected(self):
        self.write_registry(
            [
                {
                    "id": "local-evidence",
                    "title": "Local evidence",
                    "kind": "repository",
                    "path": "evidence.md",
                    "last_verified": "2026-07-31",
                    "supersedes": ["missing-source"],
                }
            ]
        )
        errors, _ = self.validate()
        self.assertTrue(any("unknown superseded source" in error for error in errors))

    def test_supersession_cycle_is_rejected(self):
        other = self.root / "other.md"
        other.write_text("# Other\n", encoding="utf-8")
        self.write_registry(
            [
                {
                    "id": "local-evidence",
                    "title": "Local evidence",
                    "kind": "repository",
                    "path": "evidence.md",
                    "last_verified": "2026-07-31",
                    "supersedes": ["other-evidence"],
                },
                {
                    "id": "other-evidence",
                    "title": "Other evidence",
                    "kind": "repository",
                    "path": "other.md",
                    "last_verified": "2026-07-31",
                    "supersedes": ["local-evidence"],
                },
            ]
        )
        errors, _ = self.validate()
        self.assertTrue(any("source supersession cycle" in error for error in errors))

    def test_affected_page_must_cite_source(self):
        other = self.root / "other.md"
        other.write_text("# Other\n", encoding="utf-8")
        self.write_registry(
            [
                {
                    "id": "local-evidence",
                    "title": "Local evidence",
                    "kind": "repository",
                    "path": "evidence.md",
                    "last_verified": "2026-07-31",
                },
                {
                    "id": "other-evidence",
                    "title": "Other evidence",
                    "kind": "repository",
                    "path": "other.md",
                    "last_verified": "2026-07-31",
                    "affected_pages": ["knowledge/topics/example.md"],
                },
            ]
        )
        errors, _ = self.validate()
        self.assertTrue(any("affected page does not cite" in error for error in errors))

    def test_duplicate_page_title_is_rejected(self):
        duplicate = self.root / "knowledge" / "decisions" / "duplicate.md"
        duplicate.write_text(
            """# example

> Status: decision
> Last verified: 2026-07-31
> Sources: `local-evidence`
""",
            encoding="utf-8",
        )
        (self.root / "knowledge" / "index.md").write_text(
            "# Index\n\n- [Example](topics/example.md)\n"
            "- [Duplicate](decisions/duplicate.md)\n",
            encoding="utf-8",
        )
        errors, _ = self.validate()
        self.assertTrue(any("duplicate page title" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
