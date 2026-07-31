# Codex Living Wiki

This directory is the repository's review-first maintainer knowledge layer. It
compiles evidence about Codex workflows into small, interlinked Markdown pages
without replacing the human-reviewed curriculum.

## Boundaries

- Official OpenAI documentation remains authoritative for Codex behavior.
- `modules/` and `resources/` remain the published learning package.
- `skills/` contain reusable procedures, not a copy of the wiki.
- `AGENTS.md` contains rules that must apply on every repository task.
- `knowledge/` records current understanding, evidence, uncertainty, decisions,
  and experiments that may later be promoted.

External source bodies belong in the ignored `.wiki-cache/` directory unless
their license and repository policy permit redistribution. The committed
[`sources.json`](sources.json) file stores stable identifiers and provenance.

## Operations

Install or explicitly invoke
[`maintain-codex-wiki`](../skills/maintain-codex-wiki/SKILL.md):

```text
$maintain-codex-wiki Query what this repository knows about model-adaptive
skills. Cite the wiki pages and do not modify files.
```

```text
$maintain-codex-wiki Ingest this official Codex documentation update. Prepare
a reviewable wiki diff, run lint, and do not promote it into a module yet.
```

Run deterministic validation directly:

```bash
python3 skills/maintain-codex-wiki/scripts/wiki_lint.py .
```

## Review model

1. Register or reuse a source.
2. Update the smallest set of affected wiki pages.
3. Run deterministic lint and inspect semantic evidence.
4. Review the diff through a pull request.
5. Promote stable conclusions into modules, skills, rules, or checks only when
   explicitly requested.

Scheduled maintenance may report drift or prepare a draft PR. It must not push
directly to a protected branch or silently turn community practice into
official guidance.
