#!/usr/bin/env python3
"""Run hidden store checks in a process the evaluator can time out."""

import json
import sys
import tempfile
import threading
from pathlib import Path


def main():
    candidate = Path(sys.argv[1]).resolve()
    sys.path.insert(0, str(candidate))
    from incident.store import ConflictError, IncidentStore, ValidationError

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "nested" / "store.json"
        store = IncidentStore(path)
        created = []
        errors = []

        def create(index):
            try:
                created.append(
                    store.create({"title": f"Incident {index}", "severity": "sev3"})
                )
            except Exception as error:  # surfaced after all threads stop
                errors.append(error)

        threads = [threading.Thread(target=create, args=(index,)) for index in range(12)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        assert not errors, errors
        assert len(store.list_incidents()) == 12
        assert len({item["id"] for item in created}) == 12
        json.loads(path.read_text())
        assert not list(path.parent.glob("*.tmp"))

        target = created[0]
        before = store.list_incidents()
        before[0]["title"] = "mutated outside the store"
        assert all(item["title"] != "mutated outside the store" for item in store.list_incidents())

        updated = store.update(
            target["id"],
            {"version": target["version"], "status": "mitigating"},
        )
        assert updated["created_at"] == target["created_at"]
        assert updated["updated_at"] > target["updated_at"]
        assert updated["version"] == target["version"] + 1
        assert store.list_incidents()[0]["id"] == target["id"]

        for payload in (
            {"status": "resolved"},
            {"version": updated["version"], "status": "unknown"},
            {"version": updated["version"], "severity": "sev0"},
        ):
            try:
                store.update(target["id"], payload)
            except (ValidationError, ConflictError):
                pass
            else:
                raise AssertionError(f"invalid update accepted: {payload}")

        try:
            store.update(target["id"], {"version": target["version"], "status": "resolved"})
        except ConflictError:
            pass
        else:
            raise AssertionError("stale update accepted")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
