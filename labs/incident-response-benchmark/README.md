# Incident-response orchestration benchmark

This is a large, dependency-free implementation benchmark for comparing one
agent with bounded multi-agent orchestration. It combines persistence, input
validation, HTTP behavior, concurrent writes, browser state, accessibility,
responsive presentation, automated checks, integration, and evidence handoff.

Use it to test a hypothesis, not to prove that more agents are automatically
better. Orchestration is useful only if reduced elapsed time or improved
coverage is worth its total token, conflict, and integration cost.

## Create identical starting copies

Run only from disposable copies. The fixture intentionally has no `incident/`
or `web/` implementation, so its supplied tests fail at baseline.

```bash
cd labs/incident-response-benchmark
benchmark_root="$(mktemp -d)"
cp -R AGENTS.md README.md TASK.md test .gitignore "$benchmark_root/"
cd "$benchmark_root"
git init
git add .
git commit -m "baseline incident-response benchmark"
```

Create two fresh copies from the same commit. Do not put `evaluator.py` in a
candidate. Apply it only after both variants stop:

```bash
python3 /path/to/codex-howto/labs/incident-response-benchmark/evaluator.py \
  /path/to/candidate \
  /path/to/codex-howto/labs/incident-response-benchmark
```

The evaluator executes candidate Python and starts its local server. Run it in
the same disposable sandbox and with the same permissions used for the
candidate; do not evaluate untrusted output on a privileged host. Its browser
checks are static contract checks, not a substitute for browser interaction or
assistive-technology testing.

## Frozen component contract

The contract is deliberately complete enough to permit exclusive ownership.
Do not let workers invent incompatible interfaces.

```text
incident/
├── __init__.py
├── server.py       # HTTP adapter and CLI entry point
└── store.py        # validation, transitions, JSON persistence
web/
├── app.js          # browser behavior and API calls
├── index.html
└── styles.css
```

### Store contract

`incident.store` must export `IncidentStore`, `ValidationError`, and
`ConflictError`.

- `IncidentStore(path)` reads and writes a JSON array at `path`; a missing file means no incidents.
- `list_incidents(status=None, severity=None)` returns newest-updated first and supports both filters.
- `create(payload)` requires a non-blank `title` and a severity of `sev1`, `sev2`, or `sev3`.
- New incidents receive a unique string `id`, `status: "open"`, integer `version: 1`, and UTC `created_at` and `updated_at` timestamps.
- `update(id, payload)` requires the caller's current integer `version`. A stale version raises `ConflictError`.
- Updates may change `title`, `severity`, and `status`; status is `open`, `mitigating`, or `resolved`.
- Every successful update increments `version` and refreshes `updated_at` without changing `created_at`.
- Writes are thread-safe and use a temporary file plus `os.replace` in the store directory.
- Returned values are safe copies; callers cannot mutate stored state indirectly.

### HTTP contract

Run the app with:

```bash
python3 -m incident.server --host 127.0.0.1 --port 8080 --data data/incidents.json
```

All JSON responses set `Content-Type: application/json`; invalid JSON or
invalid fields return `400`; unknown incidents return `404`; stale versions
return `409`.

| Method | Path | Success response |
| --- | --- | --- |
| `GET` | `/health` | `200 {"status":"ok"}` |
| `GET` | `/api/incidents?status=&severity=` | `200 {"incidents":[...]}` |
| `POST` | `/api/incidents` | `201 {"incident":{...}}` |
| `PATCH` | `/api/incidents/{id}` | `200 {"incident":{...}}` |

The server also serves `web/index.html` at `/` and the two static assets under
`/web/`. Prevent path traversal; no requested path may escape `web/`.

### Browser contract

- Show a native create form with title and severity controls.
- Render incidents in `#incident-list`; show status and severity, with controls to advance open → mitigating → resolved.
- Filter by status and severity without a page reload.
- Display request, validation, empty, and conflict states in `#message`, which is a live region.
- Use semantic controls, associated labels, visible keyboard focus, and a responsive layout.
- Use the frozen API paths and version field; do not use external libraries, fonts, images, or network services.

## Controlled comparison

Keep these fixed across variants: starting commit, task text, model, reasoning
effort, permissions, tools, time limit, and evaluator. Change only the method:

- `single_agent`: one agent owns implementation, testing, review, and handoff;
- `orchestrated`: one controller may assign backend and frontend to separate
  writers with exclusive paths, then integrates, runs system checks, reviews,
  and writes the handoff.

For the first orchestrated run, use at most two implementation workers. More
workers add coordination cost without creating another independent write
surface. The controller owns `benchmark-final.md`; workers must not edit the
same files.

Record acceptance, elapsed time, total tokens across every agent, worker count,
retries, edit conflicts, integration rework, human corrections, and evidence
completeness. Mark unavailable telemetry as `unavailable`; never estimate it.
Repeat or alternate run order before making a general claim.

The first [smoke run](../../examples/measurements/incident-orchestration-smoke-2026-08-11.md)
qualified the fixture and evaluator but intentionally makes no efficiency
claim because its variants overlapped and token telemetry was unavailable.
