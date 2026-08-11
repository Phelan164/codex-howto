import importlib.util
import tempfile
import unittest
from pathlib import Path


EVALUATOR_PATH = (
    Path(__file__).resolve().parents[2]
    / "labs"
    / "incident-response-benchmark"
    / "evaluator.py"
)
SPEC = importlib.util.spec_from_file_location("incident_evaluator", EVALUATOR_PATH)
evaluator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(evaluator)


class IncidentEvaluatorGuardTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        root = Path(self.temporary.name)
        self.fixture = root / "fixture"
        self.candidate = root / "candidate"
        for directory in (self.fixture, self.candidate):
            directory.mkdir()
        for relative in evaluator.IMMUTABLE_FIXTURE_FILES:
            for directory in (self.fixture, self.candidate):
                path = directory / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"fixture:{relative}\n")
        for relative in evaluator.ALLOWED_CANDIDATE_FILES:
            path = self.candidate / relative
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"candidate:{relative}\n")

    def test_accepts_exact_fixture_and_scope(self):
        evaluator.assert_fixture_integrity(self.candidate, self.fixture)
        evaluator.assert_candidate_scope(self.candidate)

    def test_rejects_changed_task(self):
        (self.candidate / "TASK.md").write_text("changed\n")
        with self.assertRaisesRegex(AssertionError, "fixture file changed: TASK.md"):
            evaluator.assert_fixture_integrity(self.candidate, self.fixture)

    def test_rejects_unexpected_dependency_manifest(self):
        (self.candidate / "package.json").write_text("{}\n")
        with self.assertRaisesRegex(AssertionError, "unexpected candidate files: package.json"):
            evaluator.assert_candidate_scope(self.candidate)

    def test_rejects_missing_required_file(self):
        (self.candidate / "web/app.js").unlink()
        with self.assertRaisesRegex(AssertionError, "missing candidate files: web/app.js"):
            evaluator.assert_candidate_scope(self.candidate)

    def test_rejects_candidate_symlink(self):
        target = self.candidate / "web/app.js"
        target.unlink()
        target.symlink_to(self.candidate / "TASK.md")
        with self.assertRaisesRegex(AssertionError, "candidate symlink is not allowed"):
            evaluator.assert_candidate_scope(self.candidate)

    def test_accepts_os_replace_for_atomic_persistence(self):
        evaluator.assert_atomic_replace("import os\nos.replace('tmp', 'store')\n")

    def test_rejects_decoy_string_replace(self):
        with self.assertRaisesRegex(AssertionError, "must call os.replace"):
            evaluator.assert_atomic_replace("timestamp.replace('+00:00', 'Z')\n")


if __name__ == "__main__":
    unittest.main()
