---
name: engineering-loop
description: "Drive a repository change through a complete local engineering loop: establish a baseline, reproduce behavior, plan, implement minimally, add tests, run focused and required checks, inspect the diff, review findings, fix verified issues, and report evidence. Use when asked to implement or fix a feature end to end, work autonomously until tests pass, follow a Devin-style develop-test-review loop, or keep iterating until explicit acceptance criteria are met; do not use for explanation-only, review-only, or unauthorized production work."
---

# Engineering Loop

Own the change from a verified starting point to a reviewed result. Keep one
main agent by default and load only the domain guidance the task needs.

## Establish the contract

1. Read applicable `AGENTS.md` files and repository documentation.
2. State the requested behavior, scope, constraints, and observable acceptance
   criteria.
3. Inspect the branch, working tree, and existing changes. Preserve user-owned
   work and avoid unrelated cleanup.
4. Identify the repository-native build, test, lint, type-check, and review
   commands.
5. Confirm the local test target, fixtures, external dependencies, and possible
   side effects before running commands.
6. Run the smallest safe baseline that distinguishes a pre-existing failure
   from a regression introduced by the task.

For a long, cross-stack, or high-risk change, use the templates and failure
rules in [references/loop-contract.md](references/loop-contract.md).

## Route only relevant guidance

When the specialist skill is installed and applicable:

- Use `$build-frontend` for rendered UI, interaction, accessibility, or
  client-state work.
- Use `$build-backend` for APIs, services, jobs, persistence, and integrations.
- Use `$operate-devops` for infrastructure, CI/CD, containers, deployment, or
  operational configuration.
- Use `$test-software` when test strategy, regression design, flakes, or
  specialized testing is material.
- Use `$review-code` for the final correctness and regression pass.
- Use `$review-security` when trust boundaries, authorization, untrusted input,
  secrets, dependencies, or permissions are affected.
- Use `$orchestrate-engineering` only when independent workstreams justify
  delegation.

Do not load every skill by default. This skill owns the loop and integration;
specialist skills supply domain-specific decisions.

## Run the loop

1. Reproduce the defect, or capture the current behavior for a feature.
2. Plan the smallest coherent change and name the evidence that will prove it.
3. Add a failing regression test first when the behavior is testable and doing
   so is practical. Record when test-first is not appropriate.
4. Implement one bounded change without speculative refactoring.
5. Run the narrowest relevant check.
6. Classify failures as product, test, environment, or assumption failures.
7. Fix the cause, not the symptom, and rerun the affected check.
8. After focused checks pass, run repository-required broader checks.
9. Inspect the complete diff for accidental churn, contract drift, unsafe
   behavior, and missing coverage.
10. Perform a fresh findings-first review. Fix verified findings, then rerun
    every check affected by those fixes.

Keep a compact ledger of confirmed facts, changed files, commands, outcomes,
and the next decision. Return concise diagnostics instead of full logs.

## Control iteration

- Continue while a new code or test change has a clear evidence-producing next
  step.
- If the same command fails twice for the same reason, stop retrying and
  re-check the environment, target, permissions, and underlying assumption.
- Stop and report a blocker when progress requires missing authority, secrets,
  unavailable infrastructure, destructive action, or a product decision.
- Never make a failing check pass by weakening assertions, deleting coverage,
  hiding errors, or silently changing acceptance criteria.
- Do not broaden sandbox, network, or external-system permissions merely to
  keep the loop moving.
- Do not query production, deploy, migrate, merge, or publish unless the user
  explicitly authorizes that action.

## Finish with evidence

Report:

1. behavior implemented or defect fixed;
2. changed files and important design decisions;
3. regression proof or acceptance evidence;
4. focused and broader commands with outcomes;
5. review findings fixed or explicitly unresolved;
6. unrun checks, residual risks, and blockers.

## Acceptance criteria

- The original acceptance criteria are satisfied by observable evidence.
- A defect is reproduced before the fix when practical.
- Focused and repository-required checks pass, or exact blockers are reported.
- The final diff contains no unrelated or user-owned changes.
- Consequential review findings are fixed or clearly handed back.
- The final report distinguishes verified facts from assumptions.
