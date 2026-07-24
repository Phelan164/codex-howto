# Orchestrated review prompt

```text
Review this branch against main using bounded parallel agents.

Preflight:
- Read applicable AGENTS.md and repository review guidance.
- Resolve the actual diff and list affected subsystems.
- Keep all workers read-only.
- Decide whether parallel review is justified. If the diff is small or tightly
  coupled, use one reviewer and explain why.

If delegation is justified, choose the smallest relevant subset of these
independent roles:
- explorer: map changed execution paths and public contracts when ownership or
  impact is unclear;
- reviewer-security: inspect authentication, authorization, trust boundaries,
  untrusted input, secrets, or permission changes when the diff touches them;
- reviewer-tests: identify changed behavior lacking meaningful regression,
  failure-path, or contract coverage;
- reviewer-reliability: inspect transactions, concurrency, retries, timeouts,
  cleanup, and degraded dependency behavior when those risks are present.

Worker output contract:
- Return at most five candidate findings.
- Include file/symbol evidence, failing scenario, impact, confidence, and
  uncertainty.
- Do not return raw logs or style-only feedback.
- Do not modify files or post comments.
- Stop after the assigned risk surface has been traced through changed code,
  direct callers/contracts, and relevant tests; do not broaden into unrelated
  subsystems.

Wait for every selected worker. Then:
- validate candidate findings against the code;
- deduplicate overlapping findings;
- discard unsupported speculation;
- rank remaining findings by realistic impact;
- return findings first with tight file references;
- list unverified areas and checks not run;
- provide a short change summary last.

Do not spawn additional agents unless a worker exposes a genuinely independent,
material question that cannot be answered from its existing scope.

In the final response, state which roles were selected or skipped and why.
Do not claim token savings unless the surface exposed measurements.
```
