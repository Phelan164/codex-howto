# 08 · Subagents

## Outcome

Delegate narrow work to isolated agent threads without losing control of scope or evidence.

## Good delegation candidates

- codebase exploration;
- independent documentation research;
- test or log analysis;
- security, test-gap, and maintainability review passes;
- independent modules with exclusive ownership.

Poor candidates:

- two agents editing the same files;
- tightly ordered work where every step depends on the last;
- a tiny task where coordination costs more than execution;
- vague “build the whole feature” delegation.

## Delegation contract

Every worker should receive:

```text
Objective:
Bounded scope:
Allowed actions:
Required evidence:
Output format:
Stop condition:
```

Ask workers to return distilled evidence rather than raw logs. The main agent owns integration and final verification.

## Custom agents

Project agents live in `.codex/agents/*.toml`; personal agents live in `~/.codex/agents/*.toml`.

The required fields are `name`, `description`, and `developer_instructions`. Settings such as `sandbox_mode`, `model`, and reasoning effort are optional overrides; omitted values inherit through Codex configuration.

This example adds an optional read-only override:

```toml
name = "reviewer"
description = "Read-only reviewer for correctness and regression risks."
sandbox_mode = "read-only"
developer_instructions = """
Lead with consequential findings.
Cite files and explain impact.
Do not modify code.
"""
```

Omitting a model lets the agent inherit defaults. Pin a model or reasoning level only when you have measured a reason to do so.

## Exercise

Use the bundled [explorer](../../examples/agents/explorer.toml) and [reviewer](../../examples/agents/reviewer.toml):

```text
Use explorer to map the affected execution path, then use reviewer to inspect
the current diff using that evidence. Keep both agents read-only. Return only
verified findings with file references.
```

## Verify

- Each worker had one clear responsibility.
- Workers did not edit overlapping files.
- Summaries include evidence and uncertainty.
- The main agent inspected the combined result.
- Delegation improved quality or elapsed time enough to justify its token cost.

## Official source

- [Subagents](https://developers.openai.com/codex/subagents)

Last verified: 2026-07-24.
