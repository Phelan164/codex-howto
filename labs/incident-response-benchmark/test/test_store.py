import json
import tempfile
import unittest
from pathlib import Path

from incident.store import ConflictError, IncidentStore, ValidationError


class IncidentStoreTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "nested" / "incidents.json"
        self.store = IncidentStore(self.path)

    def tearDown(self):
        self.temp.cleanup()

    def test_create_persists_normalized_incident(self):
        incident = self.store.create({"title": "  Database latency  ", "severity": "sev1"})

        self.assertEqual(incident["title"], "Database latency")
        self.assertEqual(incident["severity"], "sev1")
        self.assertEqual(incident["status"], "open")
        self.assertEqual(incident["version"], 1)
        self.assertTrue(incident["id"])
        self.assertEqual(incident["created_at"], incident["updated_at"])
        self.assertEqual(json.loads(self.path.read_text()), [incident])

    def test_create_rejects_missing_title_and_unknown_severity(self):
        for payload in ({"severity": "sev1"}, {"title": " ", "severity": "sev1"}, {"title": "x", "severity": "sev0"}):
            with self.subTest(payload=payload), self.assertRaises(ValidationError):
                self.store.create(payload)

    def test_update_requires_version_and_preserves_creation_time(self):
        created = self.store.create({"title": "API down", "severity": "sev1"})
        updated = self.store.update(created["id"], {"version": 1, "status": "mitigating"})

        self.assertEqual(updated["status"], "mitigating")
        self.assertEqual(updated["version"], 2)
        self.assertEqual(updated["created_at"], created["created_at"])
        with self.assertRaises(ConflictError):
            self.store.update(created["id"], {"version": 1, "status": "resolved"})

    def test_filters_and_returns_safe_copies(self):
        first = self.store.create({"title": "A", "severity": "sev1"})
        second = self.store.create({"title": "B", "severity": "sev2"})
        self.store.update(first["id"], {"version": 1, "status": "resolved"})

        self.assertEqual([item["id"] for item in self.store.list_incidents(severity="sev2")], [second["id"]])
        self.assertEqual([item["id"] for item in self.store.list_incidents(status="resolved")], [first["id"]])
        result = self.store.list_incidents()
        result[0]["title"] = "mutated"
        self.assertNotEqual(self.store.list_incidents()[0]["title"], "mutated")


if __name__ == "__main__":
    unittest.main()
