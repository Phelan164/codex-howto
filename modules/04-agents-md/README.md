# 04 · `AGENTS.md`

## Outcome

Encode durable repository knowledge without filling every prompt with repeated instructions.

## What belongs in `AGENTS.md`

- repository layout and important boundaries;
- build, test, lint, format, and type-check commands;
- language and framework conventions that are not enforced automatically;
- required validation and review expectations;
- dangerous or prohibited operations;
- links to deeper architecture or review documents.

Avoid biographies, broad coding advice, copied framework manuals, and rules that a formatter or linter already enforces.

## Scope and precedence

Use:

- `~/.codex/AGENTS.md` for personal defaults;
- a root `AGENTS.md` for shared repository guidance;
- nested `AGENTS.md` files for subtree-specific rules.

Guidance closer to the working directory takes precedence. Keep local rules near the code they govern.

## Start small

Run `/init`, then replace guesses with verified facts. A useful root file can be under one page:

```markdown
# Repository guidance

## Layout
- `apps/web`: browser application
- `services/api`: public API
- `packages/contracts`: shared schemas

## Commands
- `pnpm lint`
- `pnpm typecheck`
- `pnpm test`

## Rules
- Change shared API shapes in `packages/contracts` first.
- Add a migration for persisted schema changes.
- Do not edit generated clients manually.

## Done
- Focused tests and required repository checks pass.
- The final response lists changed files and remaining risks.
```

## Feedback loop

When Codex repeats a mistake:

1. identify whether the cause is missing durable context;
2. add the smallest rule at the closest applicable directory;
3. prefer a verification command over prose when possible;
4. remove obsolete guidance when the repository changes.

## Exercise

Adapt [the starter example](../../examples/AGENTS.md) to a real repository. Ask Codex to verify every command before saving it.

## Verify

- Commands exist and run in the documented directory.
- Nested rules do not contradict root rules accidentally.
- The file contains no credentials or machine-specific paths.
- Another engineer can understand “done” without asking you.

## Official source

- [Custom instructions with `AGENTS.md`](https://developers.openai.com/codex/guides/agents-md)

Last verified: 2026-07-24.
