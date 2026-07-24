---
name: review-code
description: Review code changes for correctness defects, regressions, security risks, data-integrity problems, concurrency hazards, and missing meaningful tests. Use for pull requests, branches, commits, patches, or working-tree reviews; do not use for implementation unless the user separately requests fixes.
---

# Review Code

## Workflow

1. Establish the review target and comparison base.
2. Read applicable `AGENTS.md`, architecture, and review guidance.
3. Inspect the diff, then trace changed behavior through callers, contracts, persistence, and tests.
4. Inspect the target, isolation, fixtures, and side effects before running a
   narrow check that materially confirms a suspected issue.
5. Rank findings by impact and confidence.
6. Remove duplicates and unsupported speculation.
7. Return findings first, followed by open questions and a short change summary.

## Finding standard

Each finding must include:

- severity;
- precise file and line or symbol;
- the failing scenario or invariant;
- user or system impact;
- evidence or a reproduction path;
- a concise fix direction when clear.

Do not report style preferences, theoretical risks without a reachable path, or issues outside the change unless the diff materially exposes them.

## Guardrails

- Review in read-only mode by default.
- Do not assume a test is read-only: it may write snapshots, databases, queues,
  browsers, or external services.
- Do not run production-integrated, shared-environment, or destructive tests
  without explicit authorization and verified isolation.
- Do not modify, comment, approve, or request changes on a remote PR unless asked.
- Do not equate passing tests with correctness.
- Do not treat generated code or lockfile churn as a defect without understanding its source.
- Respect repository-specific compatibility and risk rules.
- State when a claim was not reproduced.

## Checklist

Read [references/review-checklist.md](references/review-checklist.md) when the change touches APIs, data, authorization, concurrency, infrastructure, or tests.

## Output

If there are no actionable findings, say so directly and name residual unverified areas. Keep the summary shorter than the findings.

## Acceptance criteria

- Every finding is actionable and evidenced.
- Severity reflects realistic impact.
- Line ranges are tight.
- Missing tests are tied to a concrete risk.
- Unverified assumptions and unrun checks are explicit.
