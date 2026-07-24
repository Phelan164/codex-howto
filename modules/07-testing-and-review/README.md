# 07 · Testing and review

## Outcome

Make Codex prove a change works and review it for consequential defects.

## The engineering loop

```text
reproduce → implement → focused test → required checks → inspect diff → review → report
```

Do not accept “implemented” as completion. Define the commands and behaviors that prove the requested outcome.

## Test by risk

Prioritize:

1. the user-visible behavior being changed;
2. boundary and failure cases;
3. authorization and data-integrity invariants;
4. integration contracts;
5. broad regression suites.

Avoid tests that only mirror implementation details.

## Review findings first

A useful review asks for:

- correctness and regression risks;
- security and authorization issues;
- data-loss or migration problems;
- concurrency and failure-path issues;
- missing meaningful tests.

Each finding should include a location, impact, evidence or reproduction path, and the smallest safe direction for a fix. Style-only preferences should not crowd out real defects.

## Separate author and reviewer context

For higher-risk changes, use a fresh review pass or a read-only reviewer agent. The reviewer should inspect the actual diff and repository rules, not merely the author’s summary.

## Exercise

Use the seeded backend defect in the
[engineering playground](../../labs/engineering-playground/README.md), or an
equivalent disposable fixture:

1. Install `test-software`, the relevant build skill, `review-code`, and
   `review-security`.
2. Use `$test-software` to write a failing regression test.
3. Use the relevant build skill to fix it.
4. Run focused and required broader checks.
5. Use `$review-code` on the resulting diff.
6. Use `$review-security` to trace trust boundaries and attacker-controlled
   input independently.
7. Reconcile overlaps without merging distinct correctness and security impact.

## Verify

- The test fails for the original behavior.
- The test passes after the fix.
- Required lint/type/build checks pass.
- Review findings are resolved or explicitly accepted.
- Security findings have a reachable attack path or are labeled as
  defense-in-depth.
- The final report distinguishes verified results from unrun checks.

## Official source

- [Codex best practices: testing and review](https://developers.openai.com/codex/learn/best-practices)

Last verified: 2026-07-24.
