---
name: test-software
description: Design, implement, and evaluate risk-based software tests across unit, integration, contract, end-to-end, and regression layers. Use when adding tests, reproducing bugs, improving coverage, diagnosing flaky tests, or defining a test strategy; do not use to change production behavior unless the user also requests implementation.
---

# Test Software

## Workflow

1. Read repository testing guidance and identify the existing test stack.
2. Confirm the test target, environment, fixtures, external services, and write
   side effects before executing commands.
3. Define the behavior, invariant, or defect the tests must prove.
4. List risks and select the lowest test layer that observes each risk reliably.
5. Reproduce defects before fixing them when practical.
6. Build deterministic fixtures around public behavior.
7. Implement the smallest high-value test set.
8. Run focused tests repeatedly, then required broader checks.
9. Inspect failures for product defects, test defects, and environment defects separately.

## Guardrails

- Test behavior rather than private implementation details.
- Avoid snapshots that hide meaningful assertions.
- Do not mock the component whose integration contract is under test.
- Control time, randomness, concurrency, and external dependencies explicitly.
- Keep fixtures minimal and readable.
- Do not “fix” flaky tests by adding blind retries or sleeps.
- Do not claim a regression test without proving it fails against the broken behavior when feasible.
- Treat tests as potentially state-changing: they may write databases, queues,
  files, snapshots, browsers, or external sandboxes.
- Do not run tests against production, shared customer data, or external
  services without explicit authorization and a verified isolation strategy.
- Stop when the configured test target or cleanup behavior is ambiguous.

## Strategy

Read [references/test-strategy.md](references/test-strategy.md) when choosing
test layers or specialized methods, investigating flakes, or planning
cross-service coverage.

## Output

For a strategy request, return:

1. risks in priority order;
2. proposed test layer for each risk;
3. fixtures and dependencies;
4. commands to run;
5. coverage intentionally deferred.

For implementation, report focused and broader checks separately.

## Acceptance criteria

- Each test maps to a meaningful behavior or invariant.
- Failure messages make diagnosis possible.
- Fixtures are deterministic and isolated.
- The focused suite passes repeatedly.
- The test would detect the intended regression.
- Uncovered risks and unrun suites are explicit.
