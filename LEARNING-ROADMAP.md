# Learning Roadmap

Choose the shortest track that produces the capability you need. Completing every file is not a requirement.

## Track A: Safe beginner

1. [Mental model](modules/00-mental-model/README.md)
2. [Sandbox and approvals](modules/01-sandbox-and-approvals/README.md)
3. [CLI and surfaces](modules/02-cli-and-surfaces/README.md)
4. [Prompts and plans](modules/03-prompts-and-plans/README.md)
5. [AGENTS.md](modules/04-agents-md/README.md)

**Exit test:** complete a small change, run the repository’s checks, inspect the diff, and explain every changed file.

## Track B: Application engineer

Complete Track A, then:

1. [Engineering skills](modules/05-engineering-skills/README.md)
2. Run one representative task without a skill, then compare
   `engineering-loop` and one relevant specialist.
3. [Testing and review](modules/07-testing-and-review/README.md)
4. Keep only the specialist skills that improve a measured result.
5. Complete the relevant parts of the
   [engineering playground](labs/engineering-playground/README.md).

**Exit test:** reproduce and fix a defect, add meaningful tests, and perform
findings-first correctness and threat-focused reviews.

## Track C: Platform and DevOps engineer

Complete Track A, then:

1. Install `operate-devops`.
2. [MCP and tools](modules/06-mcp-and-tools/README.md)
3. [Automation, plugins, and hooks](modules/11-automation-plugins-hooks/README.md)
4. [Troubleshooting](modules/12-troubleshooting/README.md)
5. Complete the operational-plan lab in the
   [engineering playground](labs/engineering-playground/README.md).

**Exit test:** automate a read-only CI check, prove failure behavior, and document rollback and permission boundaries.

## Track D: Agent orchestrator

Complete Tracks A and B, then:

1. [Subagents](modules/08-subagents/README.md)
2. [Orchestration](modules/09-orchestration/README.md)
3. [Context and token efficiency](modules/10-context-and-token-efficiency/README.md)
4. Install `orchestrate-engineering`.
5. Run the orchestrated review exercise in [examples/prompts/orchestrated-review.md](examples/prompts/orchestrated-review.md).
6. Compare a single-agent and delegated implementation of the
   [incident-response benchmark](labs/incident-response-benchmark/README.md).

**Exit test:** freeze component contracts, give writers exclusive ownership,
integrate the result, pass one system evaluator, and compare elapsed time,
total tokens, conflicts, rework, and evidence with a single-agent run.

## Track E: Knowledge maintainer

Complete Track A, then:

1. [Living Codex wiki](modules/13-living-codex-wiki/README.md)
2. Inspect the [source registry](knowledge/sources.json) and
   [review-first architecture](knowledge/decisions/review-first-wiki.md).
3. Install `maintain-codex-wiki`.
4. Query one topic without writing files.
5. Ingest one official source on a branch and run deterministic lint.
6. Complete the
   [wiki efficiency baseline](knowledge/experiments/wiki-efficiency-baseline.md).

**Exit test:** prepare a source-grounded wiki update that keeps external
content out of Git, passes lint, preserves uncertainty, and separates evidence
compilation from curriculum promotion.

## Skill progression

| Level | Reusable surface | Use it for |
|---|---|---|
| 1 | Prompt template | A repeated request that still changes frequently |
| 2 | `AGENTS.md` | Durable rules for one repository or subtree |
| 3 | Skill | A repeatable workflow with clear triggers and optional references/scripts |
| 4 | Custom agent | A specialized delegated role with isolated context |
| 5 | Plugin | A distributable package of skills, hooks, apps, or MCP configuration |
| 6 | Automation | A stable workflow that can run unattended with bounded permissions |

Do not skip directly to automation. First make the workflow reliable interactively, then extract it.

## Self-assessment

You are ready for the next stage when you can answer “yes”:

- Can I state the goal, context, constraints, and completion checks?
- Can I identify which instructions belong in the prompt versus `AGENTS.md`?
- Can I explain what the sandbox permits and when approval is required?
- Can I name the exact verification commands Codex should run?
- Can I decide whether a task is sequential or safely parallel?
- Can I keep exploratory logs out of the main decision thread?
- Can I recognize when a reusable workflow should become a skill?
