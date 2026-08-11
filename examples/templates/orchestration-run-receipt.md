# Orchestration run receipt

Use one receipt per candidate. Record observed values only; write
`unavailable` when the environment does not expose a metric.

| Field | Value |
| --- | --- |
| Run ID | |
| Variant | `single_agent` / `orchestrated` |
| Starting commit | |
| Model and reasoning effort | |
| Permissions and tools | |
| Time limit | |
| Worker count, excluding controller | |
| Worker ownership | |
| Accepted by evaluator | |
| Elapsed seconds | |
| Total tokens across all agents | |
| Retries | |
| Edit conflicts | |
| Integration rework events | |
| Human corrections | |
| Supplied checks | |
| Hidden evaluator checks | |
| Browser behavior exercised | |
| Unverified behavior | |
| Residual risk | |

For a comparison, report the raw receipts before interpreting them. Do not
call orchestration more efficient from one run, from elapsed time alone, or
when failed candidates are excluded.
