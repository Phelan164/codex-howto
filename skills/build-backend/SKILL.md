---
name: build-backend
description: Build or modify backend APIs, services, jobs, persistence, and integrations with explicit contracts, authorization, data integrity, and verification. Use for server-side features, API routes, database changes, background processing, backend bugs, and service refactors; do not use for frontend-only or infrastructure-only changes.
---

# Build Backend

## Workflow

1. Read applicable `AGENTS.md` files and identify the service’s build and test commands.
2. Trace the entry point through validation, authorization, domain logic, persistence, side effects, and response mapping.
3. Define the externally observable contract before editing.
4. Identify compatibility, migration, concurrency, retry, and failure-path risks.
5. Implement the smallest change at the owning layer.
6. Add focused tests for success, invalid input, authorization, and relevant failure behavior.
7. Run focused tests, then required type, lint, integration, and build checks.
8. Review the diff for contract drift, partial failure, secret logging, and unrelated edits.

## Guardrails

- Preserve published contracts unless the request explicitly changes them.
- Enforce authorization at a trustworthy server-side boundary.
- Validate untrusted input before domain or persistence operations.
- Keep multi-write operations atomic where partial state would violate invariants.
- Design external calls for timeouts, retries, idempotency, and duplicate delivery where applicable.
- Do not query or mutate production data without explicit authorization.
- Do not fabricate migration, framework, or API behavior; verify version-sensitive details.
- Avoid broad service abstractions that are used once.

## Contracts and data

Read [references/contracts-and-data.md](references/contracts-and-data.md) when the task changes a public API, schema, transaction, job, or integration.

## Verification

Prefer:

```text
reproducing/focused test → contract/integration test → type/lint → build
```

For migrations, validate forward behavior and document rollback or roll-forward strategy.

## Acceptance criteria

- The public contract and compatibility decision are explicit.
- Authorization and validation are enforced at the correct boundary.
- Persistence and side effects preserve invariants under failure.
- High-value behavior is covered by tests.
- Required repository checks pass or blockers are explicit.
- The final report lists migration, operational, and compatibility risks.
