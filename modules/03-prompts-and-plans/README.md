# 03 · Prompts and plans

## Outcome

Turn a vague request into a scoped engineering contract.

## The four-part prompt

```text
Goal: the observable change.
Context: relevant files, errors, designs, or tickets.
Constraints: architecture, safety, compatibility, and scope limits.
Done when: commands and behaviors that prove completion.
```

Example:

```text
Goal: reject expired password-reset tokens with the existing API error format.
Context: start at src/auth/reset.ts and its route tests.
Constraints: preserve public response fields; do not add a dependency.
Done when: an expired-token test fails before the change, passes afterward,
and the focused auth suite plus type checking pass.
```

## When to plan first

Use planning mode when:

- requirements are ambiguous;
- multiple subsystems are involved;
- a migration or compatibility boundary exists;
- the change is difficult to reverse;
- you cannot yet state the verification commands.

Ask the plan to include assumptions, affected interfaces, implementation stages, validation, and rollback.

Do not turn a small, well-understood edit into a ceremony. Planning has value when it reduces wrong work.

## Context routing

Point Codex to likely entry points instead of attaching the entire repository. Ask it to expand context only when imports, callers, tests, or contracts require it.

Useful routing information:

- the failing test or stack trace;
- the owning module;
- a similar implementation;
- a public contract or schema;
- the command that reproduces the problem.

## Exercise: interview before implementation

Give Codex a deliberately incomplete feature idea:

```text
I want to add organization-level API keys. Do not implement yet.
Interview me until permissions, lifecycle, storage, audit, compatibility,
and acceptance criteria are concrete. Then produce a staged plan with risks
and verification commands.
```

## Verify

- The plan separates confirmed requirements from assumptions.
- Each stage has a proof of completion.
- The plan identifies security and migration risks.
- The plan is small enough to review before coding.

## Official sources

- [Prompting](https://developers.openai.com/codex/prompting)
- [Best practices](https://developers.openai.com/codex/learn/best-practices)

Last verified: 2026-07-24.
