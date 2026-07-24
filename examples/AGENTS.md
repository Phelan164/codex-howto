# Example repository guidance

Adapt this file to the repository. Remove any command or rule that you have not verified.

## Layout

- `apps/web/`: customer-facing web application
- `services/api/`: public API and background jobs
- `packages/contracts/`: shared schemas and generated client sources
- `infra/`: infrastructure as code and deployment configuration
- `docs/`: architecture and operational documentation

## Commands

Run from the repository root:

```bash
pnpm install --frozen-lockfile
pnpm lint
pnpm typecheck
pnpm test
pnpm build
```

Use package-level focused tests before running the full suite.

## Engineering rules

- Inspect existing patterns before introducing a dependency or abstraction.
- Change shared API shapes in `packages/contracts/` before updating consumers.
- Add a migration for persisted schema changes; do not edit production data manually.
- Preserve backward compatibility unless the task explicitly changes a public contract.
- Keep secrets out of source files, logs, fixtures, and command output.
- Do not edit generated files directly.

## Frontend

- Reuse the shared component library and design tokens.
- Include loading, empty, error, and keyboard behavior for interactive features.
- Run the relevant component or browser test after rendered changes.

## Backend

- Validate input and enforce resource-level authorization.
- Cover success, failure, and denied cases.
- Design retryable side effects to be idempotent.

## Infrastructure

- Run format, validate, and plan/render steps before proposing an apply.
- Never change production resources without explicit approval and a recovery plan.

## Definition of done

- Focused tests pass.
- Required lint, type, and build checks pass.
- The final diff contains no unrelated changes.
- The final response lists changed files, commands run, unverified checks, and residual risks.
