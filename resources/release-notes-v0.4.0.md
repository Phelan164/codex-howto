# Codex How To v0.4.0

Codex How To now routes prior engineering knowledge through a review-first
Living Wiki and exposes its flagship workflows through the open agent skills
ecosystem.

## Highlights

- **Index-first knowledge routing:** `AGENTS.md` directs work involving prior
  decisions, experiments, or established guidance through
  `knowledge/index.md` before broad repository search.
- **Engineering capture:** `maintain-codex-wiki` can preserve an explicitly
  requested lesson from a merged change, incident, review finding, or measured
  run. No material change remains a valid result.
- **Explicit archive:** useful query synthesis can be saved as experimental,
  cited knowledge without silently becoming verified guidance.
- **Stronger provenance:** source records can pin revisions, identify
  superseded evidence, and declare the wiki pages they affect.
- **Deterministic integrity:** wiki lint now catches invalid source
  relationships, affected pages that do not cite their source, duplicate page
  titles, malformed metadata, broken links, and missing index entries.
- **Open skill installation:** `engineering-loop` and
  `maintain-codex-wiki` are indexed at
  [skills.sh](https://skills.sh/phelan164/codex-howto).

## Install a flagship workflow

Install the complete engineering loop into Codex:

```bash
npx skills add Phelan164/codex-howto --skill engineering-loop -g -a codex -y
```

Install review-first knowledge maintenance:

```bash
npx skills add Phelan164/codex-howto --skill maintain-codex-wiki -g -a codex -y
```

List all nine repository skills without installing:

```bash
npx skills add Phelan164/codex-howto --list
```

Inspect every skill before use. Skills run with the permissions available to
the agent that invokes them.

## Knowledge safety model

The Living Wiki remains plain Markdown under Git review:

- queries are read-only by default;
- capture, ingest, archive, and promotion require explicit intent;
- chat prose and model output are not evidence by themselves;
- official OpenAI documentation remains authoritative for current Codex
  behavior;
- generated factual changes require semantic review; and
- scheduled maintenance may report drift or prepare a draft but cannot merge
  factual changes automatically.

The release does not add a database, vector index, MCP server, copied external
corpus, automatic transcript ingestion, or autonomous merge path.

## Verification

The release gate covers:

- repository structure and every relative Markdown link;
- 26 measurement and Living Wiki utility tests;
- both dependency-free engineering playground tests;
- six seeded wiki pages with zero lint warnings;
- source revisions, supersession relationships, affected-page citations, and
  duplicate-title detection;
- official skill validation for `maintain-codex-wiki`;
- isolated `npx skills` listing and Codex installation smoke tests; and
- GitHub Actions validation on the release pull request.

## Feedback wanted

Useful contributions include:

- an engineering lesson that should produce no durable wiki change;
- a source revision that should mark a dependent page stale;
- a query that reads too many files or misses relevant evidence;
- an anonymized no-skill/full-skill/lean-skill measurement; or
- a maintained stack, team, language, or translation fork.

Codex How To is an independent community project. Official OpenAI
documentation remains authoritative for current product behavior.
