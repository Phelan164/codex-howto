# 00 · Mental model

## Outcome

Choose the smallest Codex surface and instruction mechanism that fits the task.

## Codex is an agent, not autocomplete

A useful task loop is:

```text
understand → inspect → plan when needed → change → verify → review → report
```

Your prompt defines the current job. Repository instructions and configuration define the environment in which that job happens. Tests, linters, and review criteria make completion observable.

## Choose a surface

| Surface | Best fit |
|---|---|
| CLI | Terminal-first local repository work and scripting |
| IDE extension | Editor-attached implementation and navigation |
| Desktop app | Planning, task management, visual review, and connected workflows |
| Cloud/web | Hosted, parallel, or offloaded repository work |

Do not optimize for a single “best” surface. Choose based on where the code, context, review, and permissions already live.

## Choose a durable mechanism

| Requirement | Use |
|---|---|
| One-time constraint | Prompt |
| Repository convention | `AGENTS.md` |
| Repeated multi-step workflow | Skill |
| Specialized delegated role | Custom agent |
| External data or action | MCP/app connector |
| Lifecycle enforcement | Hook |
| Shareable bundle | Plugin |
| Stable recurring run | Automation |

## Exercise: repository orientation

Run Codex in a small repository with read-only permissions:

```text
Map this repository for a new contributor.

Return:
1. the runtime and package manager;
2. the main entry points;
3. the build, test, lint, and type-check commands;
4. the three most important architecture boundaries;
5. the files that support each conclusion.

Do not change files or install dependencies.
```

## Verify

- Every command is backed by a repository file.
- The response distinguishes facts from inference.
- No file changed.
- You know which surface would be best for the next implementation task.

## Official sources

- [Codex documentation](https://developers.openai.com/codex)
- [Codex best practices](https://developers.openai.com/codex/learn/best-practices)

Last verified: 2026-07-24.
