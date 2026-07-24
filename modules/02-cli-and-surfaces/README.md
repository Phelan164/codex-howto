# 02 · CLI and surfaces

## Outcome

Start Codex safely, understand the current working context, and complete a reversible first task.

## Install and authenticate

Use the [official quickstart](https://developers.openai.com/codex/quickstart). Prefer official installers or documented package-manager options over copied third-party commands.

After installation:

```bash
codex --version
codex
```

Sign in with the account method appropriate to your organization. API-key authentication and ChatGPT-plan authentication are different billing and access paths.

## First-session checklist

Before asking Codex to edit:

1. Confirm the current directory.
2. Confirm the repository and active branch.
3. Inspect `git status`.
4. Read applicable `AGENTS.md`.
5. Identify the expected test and lint commands.
6. Start with the default permission mode.

## Learn with reversible tasks

Good first tasks:

- explain a module;
- add a focused unit test;
- improve a small documentation section;
- fix a reproduced, low-risk bug;
- review uncommitted changes.

Avoid using your first session for credential rotation, production infrastructure, data deletion, or an unbounded repository rewrite.

## Core interactive tools

- `/init` scaffolds a starter `AGENTS.md`.
- `/plan` enters planning mode for complex work.
- `/permissions` inspects or changes the permission mode.
- `/review` performs a focused code review.
- `/agent` inspects agent threads in supported CLI workflows.

These commands evolve. Confirm current availability in the [CLI reference](https://developers.openai.com/codex/cli).

## Exercise: one verified edit

```text
Goal: improve one misleading comment or documentation paragraph.
Context: inspect the implementation before editing the text.
Constraints: change one file only; do not change runtime behavior.
Done when: the wording matches the implementation and the repository's
documentation checks pass.
```

Inspect the diff before accepting the result.

## Verify

- You can explain the authentication mode you used.
- You know the active sandbox and approval behavior.
- The diff contains only the intended documentation change.
- The relevant check passes.

## Official sources

- [Codex quickstart](https://developers.openai.com/codex/quickstart)
- [Codex CLI](https://developers.openai.com/codex/cli)

Last verified: 2026-07-24.
