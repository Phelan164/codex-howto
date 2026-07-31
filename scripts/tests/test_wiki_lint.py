import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


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
                    "revision": "0000000000000000000000000000000000000000",
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
        subprocess.run(
            ["git", "init", "-q", str(self.root)],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(self.root), "add", "."],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "-c",
                "user.name=Wiki Lint Tests",
                "-c",
                "user.email=wiki-lint@example.invalid",
                "commit",
                "-qm",
                "fixture",
            ],
            check=True,
        )
        revision = subprocess.run(
            ["git", "-C", str(self.root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "update-ref",
                "refs/remotes/origin/main",
                revision,
            ],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "symbolic-ref",
                "refs/remotes/origin/HEAD",
                "refs/remotes/origin/main",
            ],
            check=True,
        )
        registry = json.loads(
            (self.root / "knowledge" / "sources.json").read_text(encoding="utf-8")
        )
        registry["sources"][0]["revision"] = revision
        (self.root / "knowledge" / "sources.json").write_text(
            json.dumps(registry), encoding="utf-8"
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

    def test_git_commands_disable_lazy_fetching(self):
        with patch.object(WIKI_LINT.subprocess, "run") as run:
            run.return_value = subprocess.CompletedProcess(
                args=["git", "rev-parse", "--show-object-format"],
                returncode=0,
                stdout="sha1\n",
            )

            WIKI_LINT.git_object_id_length(self.root)

        env = run.call_args.kwargs["env"]
        self.assertEqual("1", env["GIT_NO_LAZY_FETCH"])

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

    def test_missing_worktree_source_is_valid_when_pinned_blob_exists(self):
        (self.root / "evidence.md").unlink()
        errors, _ = self.validate()
        self.assertEqual([], errors)

    def test_source_absent_from_recorded_tree_is_rejected(self):
        untracked = self.root / "untracked.md"
        untracked.write_text("# Untracked\n", encoding="utf-8")
        revision = subprocess.run(
            ["git", "-C", str(self.root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.write_registry(
            [
                {
                    "id": "untracked-evidence",
                    "title": "Untracked evidence",
                    "kind": "repository",
                    "path": "untracked.md",
                    "last_verified": "2026-07-31",
                    "revision": revision,
                }
            ]
        )
        errors, _ = self.validate()
        self.assertTrue(
            any(
                "repository evidence does not exist at revision" in error
                for error in errors
            )
        )

    def test_historical_source_survives_later_committed_rename(self):
        registry = json.loads(
            (self.root / "knowledge" / "sources.json").read_text(encoding="utf-8")
        )
        recorded_revision = registry["sources"][0]["revision"]
        (self.root / "evidence.md").rename(self.root / "renamed-evidence.md")
        subprocess.run(
            ["git", "-C", str(self.root), "add", "-A"],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "-c",
                "user.name=Wiki Lint Tests",
                "-c",
                "user.email=wiki-lint@example.invalid",
                "commit",
                "-qm",
                "rename evidence",
            ],
            check=True,
        )
        current_revision = subprocess.run(
            ["git", "-C", str(self.root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "update-ref",
                "refs/remotes/origin/main",
                current_revision,
            ],
            check=True,
        )
        errors, _ = self.validate()
        self.assertEqual([], errors)
        self.assertEqual(
            ("100644", "blob"),
            WIKI_LINT.git_tree_entry(
                self.root, recorded_revision, "evidence.md"
            ),
        )

    def test_symlink_at_recorded_revision_is_rejected(self):
        target = self.root / "target.md"
        target.write_text("# Target\n", encoding="utf-8")
        linked = self.root / "linked-evidence.md"
        linked.symlink_to(target.name)
        subprocess.run(
            ["git", "-C", str(self.root), "add", "target.md", "linked-evidence.md"],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "-c",
                "user.name=Wiki Lint Tests",
                "-c",
                "user.email=wiki-lint@example.invalid",
                "commit",
                "-qm",
                "add linked evidence",
            ],
            check=True,
        )
        revision = subprocess.run(
            ["git", "-C", str(self.root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "update-ref",
                "refs/remotes/origin/main",
                revision,
            ],
            check=True,
        )
        self.write_registry(
            [
                {
                    "id": "linked-evidence",
                    "title": "Linked evidence",
                    "kind": "repository",
                    "path": "linked-evidence.md",
                    "last_verified": "2026-07-31",
                    "revision": revision,
                }
            ]
        )
        errors, _ = self.validate()
        self.assertTrue(
            any(
                "repository evidence must be a regular file at revision" in error
                for error in errors
            )
        )

    def test_sensitive_repository_source_is_rejected(self):
        sensitive = self.root / ".env.production"
        sensitive.write_text("TOKEN=not-a-real-secret\n", encoding="utf-8")
        subprocess.run(
            ["git", "-C", str(self.root), "add", "-f", ".env.production"],
            check=True,
        )
        self.write_registry(
            [
                {
                    "id": "sensitive-evidence",
                    "title": "Sensitive evidence",
                    "kind": "repository",
                    "path": ".env.production",
                    "last_verified": "2026-07-31",
                }
            ]
        )
        errors, _ = self.validate()
        self.assertTrue(
            any("sensitive repository path is not allowed" in error for error in errors)
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
        self.assertTrue(any("Sources must contain" in error for error in errors))

    def test_experimental_page_requires_last_updated_not_last_verified(self):
        self.page.write_text(
            self.page.read_text(encoding="utf-8").replace(
                "> Status: verified", "> Status: experimental"
            ),
            encoding="utf-8",
        )
        errors, _ = self.validate()
        self.assertTrue(
            any(
                "Last verified is only valid for verified pages" in error
                for error in errors
            )
        )
        self.assertTrue(any("missing Last updated" in error for error in errors))

        self.page.write_text(
            self.page.read_text(encoding="utf-8").replace(
                "> Last verified: 2026-07-31", "> Last updated: 2026-07-31"
            ),
            encoding="utf-8",
        )
        errors, _ = self.validate()
        self.assertEqual([], errors)

    def test_verified_page_requires_last_verified(self):
        self.page.write_text(
            self.page.read_text(encoding="utf-8").replace(
                "> Last verified: 2026-07-31", "> Last updated: 2026-07-31"
            ),
            encoding="utf-8",
        )
        errors, _ = self.validate()
        self.assertTrue(any("missing Last verified" in error for error in errors))

    def test_wiki_page_symlink_cannot_escape_project_root(self):
        outside = Path(self.temp.name).parent / "outside-wiki-page.md"
        outside.write_text("# Private\n", encoding="utf-8")
        try:
            self.page.unlink()
            self.page.symlink_to(outside)
            errors, _ = self.validate()
            self.assertTrue(
                any(
                    "knowledge/topics/example.md: file escapes the project root"
                    in error
                    for error in errors
                )
            )
        finally:
            outside.unlink(missing_ok=True)

    def test_index_symlink_cannot_escape_project_root(self):
        outside = Path(self.temp.name).parent / "outside-wiki-index.md"
        outside.write_text("# Private\n", encoding="utf-8")
        index = self.root / "knowledge" / "index.md"
        try:
            index.unlink()
            index.symlink_to(outside)
            errors, _ = self.validate()
            self.assertTrue(
                any(
                    "knowledge/index.md: file escapes the project root" in error
                    for error in errors
                )
            )
        finally:
            outside.unlink(missing_ok=True)

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

    def test_repository_source_requires_full_object_id(self):
        self.write_registry(
            [
                {
                    "id": "local-evidence",
                    "title": "Local evidence",
                    "kind": "repository",
                    "path": "evidence.md",
                    "last_verified": "2026-07-31",
                    "revision": "abc123",
                }
            ]
        )
        errors, _ = self.validate()
        self.assertTrue(
            any(
                "repository evidence requires a full 40-character Git revision"
                in error
                for error in errors
            )
        )

    def test_sha256_repository_uses_64_character_object_ids(self):
        sha256_root = self.root / "sha256-repository"
        completed = subprocess.run(
            ["git", "init", "-q", "--object-format=sha256", str(sha256_root)],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            self.skipTest("installed Git does not support SHA-256 repositories")
        self.assertEqual(64, WIKI_LINT.git_object_id_length(sha256_root))

    def test_repository_source_must_exist_at_revision(self):
        self.write_registry(
            [
                {
                    "id": "local-evidence",
                    "title": "Local evidence",
                    "kind": "repository",
                    "path": "evidence.md",
                    "last_verified": "2026-07-31",
                    "revision": "f" * 40,
                }
            ]
        )
        errors, _ = self.validate()
        self.assertTrue(
            any(
                "repository evidence does not exist at revision" in error
                for error in errors
            )
        )

    def test_repository_revision_must_be_reachable_from_trusted_ref(self):
        detached = subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "commit-tree",
                subprocess.run(
                    ["git", "-C", str(self.root), "write-tree"],
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.strip(),
                "-m",
                "untrusted evidence",
            ],
            check=True,
            capture_output=True,
            text=True,
            env={
                **os.environ,
                "GIT_AUTHOR_NAME": "Wiki Lint Tests",
                "GIT_AUTHOR_EMAIL": "wiki-lint@example.invalid",
                "GIT_COMMITTER_NAME": "Wiki Lint Tests",
                "GIT_COMMITTER_EMAIL": "wiki-lint@example.invalid",
            },
        ).stdout.strip()
        self.write_registry(
            [
                {
                    "id": "local-evidence",
                    "title": "Local evidence",
                    "kind": "repository",
                    "path": "evidence.md",
                    "last_verified": "2026-07-31",
                    "revision": detached,
                }
            ]
        )
        errors, _ = self.validate()
        self.assertTrue(
            any(
                "repository revision is not reachable from trusted refs" in error
                for error in errors
            )
        )

    def test_repository_source_requires_configured_trusted_ref(self):
        subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "symbolic-ref",
                "--delete",
                "refs/remotes/origin/HEAD",
            ],
            check=True,
        )
        errors, _ = self.validate()
        self.assertTrue(
            any(
                "repository trusted refs are not configured" in error
                for error in errors
            )
        )

    def test_repository_tag_cannot_be_configured_as_trusted_history(self):
        revision = subprocess.run(
            ["git", "-C", str(self.root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        subprocess.run(
            ["git", "-C", str(self.root), "tag", "evidence-release", revision],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "symbolic-ref",
                "--delete",
                "refs/remotes/origin/HEAD",
            ],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "config",
                "--add",
                "codex.wikiTrustedRef",
                "refs/tags/evidence-release",
            ],
            check=True,
        )
        errors, _ = self.validate()
        self.assertTrue(
            any(
                "repository trusted refs are not configured" in error
                for error in errors
            )
        )

    def test_shallow_history_reports_incomplete_checkout_for_missing_revision(self):
        current_revision = subprocess.run(
            ["git", "-C", str(self.root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        (self.root / ".git" / "shallow").write_text(
            f"{current_revision}\n", encoding="ascii"
        )
        registry = json.loads(
            (self.root / "knowledge" / "sources.json").read_text(encoding="utf-8")
        )
        registry["sources"][0]["revision"] = "f" * 40
        (self.root / "knowledge" / "sources.json").write_text(
            json.dumps(registry), encoding="utf-8"
        )

        errors, _ = self.validate()

        self.assertTrue(
            any(
                "shallow repository history cannot verify revision" in error
                for error in errors
            )
        )
        self.assertFalse(
            any(
                "repository revision is not reachable from trusted refs" in error
                or "repository evidence does not exist at revision" in error
                for error in errors
            )
        )

    def test_shallow_history_accepts_available_trusted_revision(self):
        current_revision = subprocess.run(
            ["git", "-C", str(self.root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        (self.root / ".git" / "shallow").write_text(
            f"{current_revision}\n", encoding="ascii"
        )

        errors, _ = self.validate()

        self.assertEqual([], errors)

    def test_partial_clone_reports_incomplete_checkout_for_missing_revision(self):
        subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "config",
                "remote.origin.promisor",
                "true",
            ],
            check=True,
        )
        registry = json.loads(
            (self.root / "knowledge" / "sources.json").read_text(encoding="utf-8")
        )
        registry["sources"][0]["revision"] = "f" * 40
        (self.root / "knowledge" / "sources.json").write_text(
            json.dumps(registry), encoding="utf-8"
        )

        errors, _ = self.validate()

        self.assertTrue(
            any(
                "partial clone is missing objects required to verify revision"
                in error
                for error in errors
            )
        )
        self.assertFalse(
            any(
                "repository revision is not reachable from trusted refs" in error
                or "repository evidence does not exist at revision" in error
                for error in errors
            )
        )

    def test_partial_clone_reports_missing_evidence_blob_without_lazy_fetch(self):
        subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "config",
                "remote.origin.promisor",
                "true",
            ],
            check=True,
        )
        blob = subprocess.run(
            ["git", "-C", str(self.root), "rev-parse", "HEAD:evidence.md"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        (self.root / ".git" / "objects" / blob[:2] / blob[2:]).unlink()

        errors, _ = self.validate()

        self.assertTrue(
            any(
                "partial clone is missing the repository evidence blob" in error
                for error in errors
            )
        )
        self.assertFalse(
            any("repository evidence does not exist at revision" in error for error in errors)
        )

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
> Last updated: 2026-07-31
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
