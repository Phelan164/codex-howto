# Review-first wiki architecture

> Status: decision
> Last verified: 2026-07-31
> Sources: `official-codex-manual`, `karpathy-llm-wiki-gist`, `astro-karpathy-llm-wiki`, `lucas-llmwiki`, `atomicstrata-llm-wiki-compiler`, `codealmanac`, `kw-okf-memory-skill`

## Decision

Maintain a plain-Markdown wiki with a committed source registry,
deterministic linting, and pull-request review. Keep external source bodies in
an ignored cache by default. Do not add a database, embeddings, MCP server, or
web application until measurements show that Markdown search no longer meets
retrieval needs.

## Why

Karpathy's source–wiki–schema pattern gives knowledge a durable compiled layer.
The Astro-Han implementation shows that the core ingest, query, no-material
triage, cascade-update, and lint loop can be packaged as a portable skill.
CodeAlmanac demonstrates engineering-specific capture from changes, incidents,
and agent sessions. The KW-OKF memory skill demonstrates staged writes and
rebuildable indexes. This repository adopts explicit engineering capture and
review but not automatic transcript ingestion.

The lucasastorian and atomicstrata implementations demonstrate valuable future
capabilities such as MCP access, search indexes, citation graphs, review
queues, freshness tracking, and evaluation. Their platform complexity is not
required at this repository's current scale.

Codex receives a compact routing rule through `AGENTS.md`: start at the index
for prior decisions, experiments, or established guidance, then load only
relevant pages. The maintenance skill remains explicit-only because capture,
ingest, archive, and promotion can modify durable shared knowledge.

## Safeguards

- Official OpenAI documentation remains authoritative for Codex behavior.
- Community sources are hypotheses or patterns, not product specifications.
- Query is read-only by default.
- Capture, ingest, archive, and promotion are explicit operations.
- Chat prose and model output are not evidence by themselves.
- Available source revisions and page dependencies are machine-checked.
- CI checks mechanical integrity; humans review semantic claims.
- Scheduled maintenance may report or draft, but not merge.

## Revisit when

- index-first search fails a measured retrieval evaluation;
- the wiki grows beyond what targeted Markdown search can handle;
- multiple maintainers need live remote access rather than Git collaboration;
  or
- citation and freshness errors justify stronger runtime gates.
