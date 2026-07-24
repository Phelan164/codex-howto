# Catalog

## Tutorials

| Module | Core artifact |
|---|---|
| [00 · Mental model](modules/00-mental-model/README.md) | Surface and task selection |
| [01 · Sandbox and approvals](modules/01-sandbox-and-approvals/README.md) | Risk-based permission profiles |
| [02 · CLI and surfaces](modules/02-cli-and-surfaces/README.md) | Safe first-session checklist |
| [03 · Prompts and plans](modules/03-prompts-and-plans/README.md) | Four-part prompt contract |
| [04 · AGENTS.md](modules/04-agents-md/README.md) | Root and nested instruction strategy |
| [05 · Engineering skills](modules/05-engineering-skills/README.md) | Skill anatomy and installation |
| [06 · MCP and tools](modules/06-mcp-and-tools/README.md) | Tool selection and safety review |
| [07 · Testing and review](modules/07-testing-and-review/README.md) | Verify-and-review loop |
| [08 · Subagents](modules/08-subagents/README.md) | Bounded delegation |
| [09 · Orchestration](modules/09-orchestration/README.md) | Parallel work protocol |
| [10 · Context efficiency](modules/10-context-and-token-efficiency/README.md) | Context budget and summary contracts |
| [11 · Automation and plugins](modules/11-automation-plugins-hooks/README.md) | Promotion path from prompt to automation |
| [12 · Troubleshooting](modules/12-troubleshooting/README.md) | Layer-by-layer diagnosis |

## Installable skills

| Skill | Bundled reference |
|---|---|
| [engineering-loop](skills/engineering-loop/SKILL.md) | `references/loop-contract.md` |
| [build-frontend](skills/build-frontend/SKILL.md) | `references/verification.md` |
| [build-backend](skills/build-backend/SKILL.md) | `references/contracts-and-data.md` |
| [operate-devops](skills/operate-devops/SKILL.md) | `references/change-safety.md` |
| [review-code](skills/review-code/SKILL.md) | `references/review-checklist.md` |
| [test-software](skills/test-software/SKILL.md) | `references/test-strategy.md` |
| [review-security](skills/review-security/SKILL.md) | `references/threat-checklist.md` |
| [orchestrate-engineering](skills/orchestrate-engineering/SKILL.md) | `references/context-budget.md` |

## Copy-ready examples

- [Starter `AGENTS.md`](examples/AGENTS.md)
- [Conservative project configuration](examples/config/config.toml)
- [Explorer agent](examples/agents/explorer.toml)
- [Reviewer agent](examples/agents/reviewer.toml)
- [Test runner agent](examples/agents/test-runner.toml)
- [General task prompt](examples/prompts/task-template.md)
- [Orchestrated review prompt](examples/prompts/orchestrated-review.md)
- [Scheduled documentation-drift prompt](examples/prompts/scheduled-docs-drift.md)
- [Local plugin marketplace](examples/plugin-marketplace/.agents/plugins/marketplace.json)
- [Stop-hook example](examples/hooks/validate-on-stop/hooks.json)
- [Orchestration decision matrix](resources/orchestration-decision-matrix.md)
- [Token-efficiency scorecard](resources/token-efficiency-scorecard.md)

## Hands-on lab

- [Engineering playground](labs/engineering-playground/README.md) — a
  dependency-free frontend, backend, and deployment fixture with seeded defects
  for all seven bundled skills.

## Official references

- [Codex documentation](https://developers.openai.com/codex)
- [Quickstart](https://developers.openai.com/codex/quickstart)
- [`AGENTS.md` guide](https://developers.openai.com/codex/guides/agents-md)
- [Skills](https://developers.openai.com/codex/skills)
- [Subagents and multi-agent workflows](https://developers.openai.com/codex/subagents)
- [MCP](https://developers.openai.com/codex/mcp)
- [Security and sandboxing](https://developers.openai.com/codex/security)
- [Configuration reference](https://developers.openai.com/codex/config-reference)
- [Hooks](https://developers.openai.com/codex/config-advanced#hooks)
- [Non-interactive mode](https://developers.openai.com/codex/noninteractive)
- [Best practices](https://developers.openai.com/codex/learn/best-practices)
