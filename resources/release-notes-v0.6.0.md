# Codex How To v0.6.0

Codex How To now includes a dependency-free incident-response benchmark for
comparing one agent with bounded backend/frontend orchestration under the same
task contract and external acceptance evaluator.

The first smoke run is deliberately a harness result, not an efficiency claim:
both candidates passed all six evaluator groups, while elapsed time was
non-comparable and aggregate token telemetry was unavailable.

## Highlights

- **Large-task benchmark:** implement thread-safe JSON persistence, an HTTP API,
  a responsive browser client, accessibility behavior, and evidence handoff.
- **Bounded orchestration:** the controller may assign only the two genuine
  implementation surfaces—`incident/**` and `web/**`—to separate writers.
- **Shared external evaluator:** both variants face the same fixture-integrity,
  scope, store, live HTTP, traversal, static-browser, and handoff-topic gates.
- **Timeout and scope safeguards:** store probes run outside the evaluator
  process with time limits; fixture mutation, symlinks, unexpected files, and
  dependency or network additions are rejected.
- **Auditable receipts:** the run template records model, permissions, worker
  ownership, acceptance, elapsed time, total tokens, retries, conflicts,
  rework, corrections, browser evidence, and residual risk.
- **Honest negative boundary:** the repository does not infer speed or token
  savings from overlapping runs or missing aggregate telemetry.

## Smoke result

| Measure | Single agent | Orchestrated |
| --- | ---: | ---: |
| Accepted after review | Yes | Yes |
| Supplied tests | 4/4 | 4/4 |
| External evaluator groups | 6/6 | 6/6 |
| Implementation workers | 0 | 2 |
| Edit conflicts | 0 | 0 |
| Integration rework | 0 | 0 |
| Browser interaction exercised by candidate | No | Yes |
| Aggregate tokens | Unavailable | Unavailable |
| Comparable elapsed time | No | No |

Read the complete
[smoke receipt](../examples/measurements/incident-orchestration-smoke-2026-08-11.md)
before interpreting the table. The orchestrated candidate added browser
evidence, but one run cannot establish that orchestration caused better
coverage or would justify its extra agents on another task.

## Run the benchmark

Create two disposable copies from the same fixture commit and keep model,
reasoning effort, permissions, tools, time limit, and evaluator fixed. Change
only the execution method:

```bash
python3 labs/incident-response-benchmark/evaluator.py \
  /path/to/candidate \
  labs/incident-response-benchmark
```

Follow the
[benchmark contract](../labs/incident-response-benchmark/README.md) and record
each candidate with the
[orchestration receipt](../examples/templates/orchestration-run-receipt.md).
Run generated candidates and the evaluator only inside the same disposable,
least-privileged environment.

## What would support an efficiency claim

Run at least three fresh sequential pairs and alternate method order. Preserve
every attempted candidate, including failures. Compare acceptance and evidence
quality first, then elapsed time, aggregate controller-plus-worker tokens,
conflicts, integration rework, retries, and human corrections.

If aggregate token totals remain unavailable, report them as unavailable. Do
not substitute controller-only tokens or estimates.

## Verification

The release gate covers:

- repository structure and relative Markdown links;
- 51 CI Python tests: 49 measurement, wiki, and evaluator-guard tests plus two
  dependency-free playground tests;
- Python compilation for the benchmark and evaluator machinery;
- seven evaluator guard tests for candidate scope, fixture integrity, symlinks,
  dependency manifests, missing files, and strict atomic-write detection;
- both retained smoke implementations passing all six hardened evaluator
  groups, including store edge cases, live HTTP behavior, traversal safety,
  static browser requirements, and handoff topics; and
- automated plugin-bundle scanning.

Static browser checks are not a substitute for real interaction or assistive-
technology testing. The orchestrated smoke candidate received a live browser
pass; the single-agent candidate's browser behavior was exercised only later
by the external controller.

## Feedback wanted

The highest-value contribution is a controlled replication on a task with two
real ownership surfaces. Negative and neutral results are welcome. Fork the
repository only when the fork adds a reproducible task, evaluator, stack
edition, translation, correction, or measurement.

Codex How To is an independent community project. Official OpenAI
documentation remains authoritative for current product behavior.
