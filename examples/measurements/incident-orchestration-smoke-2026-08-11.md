# Incident orchestration benchmark smoke run

Date: 2026-08-11<br>
Status: harness qualification, not an efficiency result

This smoke run tested whether the
[incident-response benchmark](../../labs/incident-response-benchmark/README.md)
is solvable by both supported methods and whether its external evaluator can
apply the same store, HTTP, static-browser, scope, and handoff-topic checks.

## Raw outcome

| Measure | Single agent | Orchestrated |
| --- | ---: | ---: |
| Hardened evaluator accepted post-review copy | Yes | Yes |
| Implementation workers | 0 | 2 |
| Total agents, including controller | 1 | 3 |
| Supplied tests | 4/4 passed | 4/4 passed |
| External evaluator groups | 6/6 passed | 6/6 passed |
| Edit conflicts | 0 | 0 |
| Integration rework events | 0 | 0 |
| Internal review corrections | 1 | 0 |
| Browser interaction exercised by candidate | No | Yes |
| Total tokens | unavailable | unavailable |
| Observed wall time | recorded but non-comparable | recorded but non-comparable |

## Run receipts

| Field | Single agent | Orchestrated |
| --- | --- | --- |
| Run ID | `incident-single-smoke-20260811` | `incident-orchestrated-smoke-20260811` |
| Starting fixture commit | `e297b97cb2ef9412d471070866765d0f7106c18b` | same |
| Model | `gpt-5.6-sol` | `gpt-5.6-sol` |
| Reasoning effort | task default; not surfaced in run telemetry | same |
| Permissions and tools | workspace-write, local shell; localhost unavailable to candidate | workspace-write, local shell and browser |
| Explicit time limit | none | none |
| Worker ownership | one agent owned all files | `incident/**` and `web/**`; controller owned evaluation and handoff |
| Observed elapsed seconds | approximately 239 after authorized restart | approximately 282 |
| Retries | 0 candidate retries; 1 pre-run directory relocation | 0 candidate retries; 1 evaluator permission rerun |
| Human corrections | 0 | 0 |
| Candidate artifact | retained locally; not published to avoid shipping the solution | retained locally; not published to avoid shipping the solution |

Exact supplied check:

```bash
python3 -m unittest discover -s test -v
```

Exact external check, run once per post-review evaluation copy from the guide
repository:

```bash
python3 labs/incident-response-benchmark/evaluator.py \
  /path/to/candidate labs/incident-response-benchmark
```

Both hardened evaluator runs reported the same six passes: fixture/scope,
supplied tests, store edge cases, live HTTP/static serving, static browser
contract, and handoff topics. These were not reruns of the original working
directories: after independent review changed the evaluator guidance, two
post-review evaluation copies received the current immutable fixture
documentation. Their implementations and handoffs remained byte-for-byte
unchanged. The original run README SHA-256 was
`b9de52fda7cf00584733e3de178e296c35dc9990172b0639ea0ee5909249f57e`;
the hardened evaluation-copy README SHA-256 was
`667e99d34cd8bd1035743b6a86c0a3c8f1e75355a9ceb680fb32b0cd54516f44`.
Therefore the 6/6 result qualifies the hardened harness against the produced
implementations; it is not a claim that the untouched original directories
pass the later fixture-integrity hash.

The orchestrated controller froze the contract, assigned `incident/**` and
`web/**` to separate writers, and retained system evaluation and handoff
ownership. Its browser pass covered create, filter, state transitions,
validation feedback, console errors, and a mobile viewport. The single agent
found and fixed one conflict-message behavior during final review; runtime HTTP
and browser interaction were unavailable inside that candidate's sandbox, but
the external controller later exercised its live HTTP implementation.

## Why this is not an efficiency comparison

- The variants overlapped in wall-clock time, so they competed for local resources.
- The first single-agent disposable directory was rejected by a safety guard;
  the unchanged fixture was restarted inside the authorized workspace.
- The execution surface did not expose per-agent token totals.
- This was one run per method, with no alternated run order.

The observed times are therefore intentionally omitted from the comparison
table. Neither “faster” nor “more token-efficient” follows from this run.

## What the smoke run established

- The task has two real, exclusive write surfaces and integrates without
  inventing worker-specific interfaces.
- The supplied tests establish a useful baseline but do not replace the hidden
  concurrent-store, HTTP, traversal, static-browser-contract, scope, and
  handoff-topic checks.
- Both methods can satisfy the same external acceptance bar.
- Specialist ownership can add independently reported browser evidence without
  creating edit conflicts in this fixture.

## Next valid experiment

Run at least three fresh sequential pairs. Alternate method order, keep model,
reasoning, permissions, time limit, and machine load fixed, and capture total
tokens for the controller plus every worker. Publish every attempted candidate,
including failures. Compare acceptance first, then evidence completeness,
elapsed time, total tokens, conflicts, rework, and human corrections.
