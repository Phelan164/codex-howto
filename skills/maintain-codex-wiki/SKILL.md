---
name: maintain-codex-wiki
description: Maintain a review-first Markdown knowledge base for Codex practices with source provenance, explicit ingest and promotion, citation-aware queries, and deterministic linting. Use when asked to ingest Codex research, query what the repository knows, check wiki health, reconcile conflicting guidance, or promote verified knowledge into learning modules.
---

# Maintain Codex Wiki

Treat the wiki as compiled maintainer knowledge, not as an automatic source of
truth. Keep official documentation authoritative and require human review
before shared knowledge or curriculum changes land.

## Choose one operation

- **Query**: read `knowledge/index.md`, search candidate pages, and answer with
  links. Do not write unless the user explicitly asks.
- **Ingest**: register one source, update affected wiki pages, run lint, and
  prepare a reviewable diff.
- **Lint**: run the bundled deterministic checker, then review semantic drift
  that a script cannot prove.
- **Promote**: move a verified conclusion into the appropriate module, skill,
  or repository rule through a separate, reviewable change.

Read [source-policy.md](references/source-policy.md) before Ingest or Promote.
Read [article-template.md](references/article-template.md) when creating a page.

## Query

1. Read `knowledge/index.md`.
2. Search `knowledge/` for the subject and its common synonyms.
3. Read only the relevant pages and their registered sources.
4. Distinguish verified guidance, community practice, experiment results, and
   unresolved claims.
5. Answer with links to wiki pages. State when the wiki has no evidence.

Do not use model memory to silently fill a gap in the repository wiki.

## Ingest

1. Inspect `knowledge/sources.json` and reuse an existing source ID when it
   identifies the same material.
2. For external material, store metadata in the registry and use
   `.wiki-cache/` for temporary fetched content. Do not commit a full external
   source unless its license and repository policy permit redistribution.
3. Classify the source as `official`, `community`, `repository`, or
   `experiment`.
4. Search existing pages before creating a new page.
5. Update every materially affected page. Preserve disagreements explicitly;
   do not rewrite a disputed claim as consensus.
6. Update `knowledge/index.md` and append a concise event to
   `knowledge/log.md`.
7. Run:

   ```bash
   python3 <skill-dir>/scripts/wiki_lint.py <project-root>
   ```

8. Review the diff and report unverified claims. Never push directly to a
   protected branch.

Compile sources sequentially because the registry, index, and log are shared
state. Parallel research is acceptable only when workers do not edit them.

## Lint

Run the bundled checker first. It verifies:

- registry schema, source IDs, dates, URLs, and local source paths;
- required page metadata and registered source references;
- index coverage; and
- local links inside `knowledge/`.

Then inspect what deterministic lint cannot establish:

- whether a claim is actually supported by its cited source;
- whether newer official guidance supersedes a page;
- whether two sources materially disagree;
- whether a conclusion deserves promotion; and
- whether a page duplicates existing curriculum instead of mapping evidence.

Auto-fix only mechanical link or index errors. Propose factual changes for
review.

## Promote

Promote knowledge only when the user explicitly requests it and evidence is
strong enough for the destination:

- durable repository requirements → `AGENTS.md`;
- reusable procedure with a measured gap → a focused skill;
- stable learning content → a module or resource;
- mechanical enforcement → a script, CI check, or hook;
- unresolved or early evidence → keep it in `knowledge/`.

Link the destination back to the evidence page when that helps future
maintenance. Keep the wiki page as a compact evidence map instead of copying
the published prose.

## Completion

Return:

- operation performed;
- pages and source records changed;
- lint command and result;
- conflicts or freshness uncertainty;
- promotion performed or deferred; and
- review or approval still required.
