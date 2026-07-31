# Codex knowledge surfaces

> Status: verified
> Last verified: 2026-07-31
> Sources: `official-codex-manual`, `karpathy-llm-wiki-gist`

## Current understanding

Codex benefits from several durable surfaces, but they serve different scopes.
Use the prompt for one task, `AGENTS.md` for required repository conventions, a
skill for a reusable procedure, an MCP connector for live external data, and
automation for a proven recurring workflow. Local memories can help recall
prior work but should not be the only copy of required team guidance.

A living wiki adds a separate evidence layer: it stores synthesized
understanding, uncertainty, experiments, and promotion decisions without
injecting the entire knowledge base into every task.

## Evidence

- OpenAI documents `AGENTS.md`, skills, plugins, MCP, memories, and scheduled
  tasks as separate customization surfaces.
- Karpathy's pattern separates immutable sources, a compiled wiki, and the
  schema that teaches the agent how to maintain it.

## Implications

Keep mandatory rules compact in [`AGENTS.md`](../../AGENTS.md). Load wiki pages
only for tasks that need their evidence, and promote stable procedures into
focused skills rather than asking Codex to reread the full wiki.

## Promotion status

The surface-selection guidance is already represented in modules
[04](../../modules/04-agents-md/README.md),
[05](../../modules/05-engineering-skills/README.md), and
[11](../../modules/11-automation-plugins-hooks/README.md). This page remains an
evidence map for maintainers.
