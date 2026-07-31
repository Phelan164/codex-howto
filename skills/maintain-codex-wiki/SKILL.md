---
name: maintain-codex-wiki
description: Maintain a review-first Markdown knowledge base for Codex practices with source provenance, engineering capture, citation-aware queries, explicit archive and promotion, and deterministic linting. Use when asked to capture a durable engineering lesson, ingest Codex research, query or archive what the repository knows, check wiki health, reconcile conflicting guidance, or promote verified knowledge.
---

# Maintain Codex Wiki

Treat the wiki as compiled maintainer knowledge, not as an automatic source of
truth. Keep official documentation authoritative and require human review
before shared knowledge or curriculum changes land.

## Choose one operation

- **Query**: read `knowledge/index.md`, search candidate pages, and answer with
  links. Do not write unless the user explicitly asks.
- **Capture**: preserve a durable lesson from repository evidence such as a
  merged change, incident, review finding, or measured run.
- **Ingest**: register one source, update affected wiki pages, run lint, and
  prepare a reviewable diff.
- **Archive**: save a requested query result as an experimental, cited page.
- **Lint**: run the bundled deterministic checker, then review semantic drift
  that a script cannot prove.
- **Promote**: move a verified conclusion into the appropriate module, skill,
  or repository rule through a separate, reviewable change.

Read [source-policy.md](references/source-policy.md) before Capture, Ingest,
Archive, or Promote.
Read [article-template.md](references/article-template.md) when creating a page.

## Query

1. Read `knowledge/index.md`.
2. Search `knowledge/` for the subject and its common synonyms.
3. Before reading any wiki page, index, registry, log, or registered
   repository `path`, require a normalized project-relative path, reject
   absolute paths and `..` components, resolve symlinks, require a regular
   file, and verify the target remains inside the project root.
4. Read only the relevant pages and their registered sources.
5. Distinguish verified guidance, community practice, experiment results, and
   unresolved claims.
6. Answer with links to wiki pages. State when the wiki has no evidence.

Do not use model memory to silently fill a gap in the repository wiki.

## Capture

1. Require an explicit request to preserve the lesson.
2. Identify a durable repository or experiment artifact. Do not treat chat
   prose, an unmerged proposal, or model output as evidence by itself.
3. Search the index and full wiki before creating a page.
4. Register or reuse the evidence source, including a stable revision when
   available and the pages it affects.
5. Update the smallest existing page, or create an `experimental` page when
   the conclusion is not stable enough for another status.
6. Update the index and log, run lint, and leave promotion for a separate
   decision.

No material change is a valid result. Do not force every task, PR, or incident
into durable knowledge.

## Ingest

1. Require an explicit request to ingest before changing the registry, pages,
   index, or log. A general research request remains read-only.
2. Inspect `knowledge/sources.json` and reuse an existing source ID when it
   identifies the same material.
3. For external material, store metadata in the registry and use
   `.wiki-cache/` for temporary fetched content. Do not commit a full external
   source unless its license and repository policy permit redistribution.
4. Classify the source as `official`, `community`, `repository`, or
   `experiment`.
5. Search existing pages before creating a new page.
6. Update every materially affected page. Preserve disagreements explicitly;
   do not rewrite a disputed claim as consensus.
7. Update `knowledge/index.md` and append a concise event to
   `knowledge/log.md`.
8. Run:

   ```bash
   python3 <skill-dir>/scripts/wiki_lint.py <project-root>
   ```

9. Review the diff and report unverified claims. Never push directly to a
   protected branch.

Compile sources sequentially because the registry, index, and log are shared
state. Parallel research is acceptable only when workers do not edit them.

## Archive

Archive only when the user explicitly asks to save a query result:

1. Preserve the source IDs used by the answer.
2. Create a compact `experimental` page in the most relevant knowledge
   directory; do not merge model-only conclusions into verified guidance.
3. Link related pages instead of copying their prose.
4. Update the index and log, then run lint.

Archive is not promotion. A later evidence review may revise, promote, or
remove the page.

## Lint

Run the bundled checker first. It verifies:

- registry schema, source IDs, dates, URLs, and local source paths;
- source revisions, supersession references, and affected-page declarations;
- required page metadata and registered source references;
- duplicate page titles;
- index coverage; and
- local links inside `knowledge/`.

Then inspect what deterministic lint cannot establish:

- whether a claim is actually supported by its cited source;
- whether newer official guidance supersedes a page;
- whether two sources materially disagree;
- whether a conclusion deserves promotion; and
- whether a page duplicates existing curriculum instead of mapping evidence.

Treat lint as read-only unless the user explicitly authorizes fixes. With that
authorization, auto-fix only mechanical link or index errors. Otherwise report
the proposed edits. Always propose factual changes for review.

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
