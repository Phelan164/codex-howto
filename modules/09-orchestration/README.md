# 09 · Orchestration

## Outcome

Coordinate multi-agent engineering work with explicit dependencies, ownership, and merge gates.

## Orchestrator responsibilities

The main agent should retain:

- requirements and acceptance criteria;
- the dependency graph;
- file or subsystem ownership;
- decisions that affect multiple workers;
- integration, conflict resolution, and final verification.

Workers should receive bounded tasks and return compact evidence.

## Three useful patterns

### Fan-out / fan-in

Run independent read-heavy analyses in parallel, then consolidate:

```text
security review ─┐
test-gap review ─┼─> deduplicate → prioritize → report
API contract ────┘
```

### Pipeline

Use sequential stages when outputs are dependencies:

```text
explore → plan → implement → test → review
```

### Partitioned implementation

Parallelize writes only when ownership is exclusive:

```text
worker A: packages/contracts/**
worker B: services/api/**
worker C: apps/web/**
```

Freeze shared interfaces first. If workers need the same file, run sequentially.

## Orchestration protocol

1. Define acceptance criteria.
2. Map dependencies.
3. Choose single-agent, pipeline, or fan-out.
4. Assign exclusive scopes and permission levels.
5. Require evidence summaries.
6. Wait at explicit merge gates.
7. Integrate in dependency order.
8. Run system-level checks.
9. Review the combined diff.

## Failure controls

- Stop a worker that expands scope.
- Re-plan when a dependency assumption changes.
- Do not let one worker’s unverified claim become another’s requirement.
- Prefer read-only workers for disputed or high-risk areas.
- Record unresolved decisions in the main thread.

## Exercise

Install [`orchestrate-engineering`](../../skills/orchestrate-engineering/SKILL.md), use it to run [the orchestrated review prompt](../../examples/prompts/orchestrated-review.md), then compare the result with one `/review` pass.

```bash
mkdir -p .agents/skills
cp -R /path/to/codex-howto/skills/orchestrate-engineering .agents/skills/
```

Measure:

- unique high-value findings;
- duplicates;
- false positives;
- elapsed time;
- total agent count;
- total tokens, credits, or cost when the surface exposes them;
- whether the main context stayed readable.

## Verify

- The chosen topology matches real dependencies.
- Each write owner is exclusive.
- Final validation covers cross-module behavior.
- The integrated result satisfies the original acceptance criteria.
- Any efficiency claim is tied to measured quality, elapsed time, context
  clarity, retries, or total cost.

## Official sources

- [Multi-agent workflows](https://developers.openai.com/codex/multi-agent)
- [Subagents](https://developers.openai.com/codex/subagents)

Last verified: 2026-07-24.
