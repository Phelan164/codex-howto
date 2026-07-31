# Codex How To v0.3.0

Codex How To now includes a review-first Living Wiki and a model-adaptive
engineering skill system.

## Highlights

- **Living Codex Wiki:** compile repeated research into small, interlinked
  Markdown evidence pages instead of reconstructing the same context for every
  question.
- **Review-first maintenance:** register source authority, preserve conflicts
  and uncertainty, lint deterministic structure, and promote stable knowledge
  through reviewed changes.
- **Four wiki operations:** query, ingest, lint, and explicitly promote
  verified conclusions into modules, skills, repository rules, or checks.
- **Model-adaptive skills:** keep nine installable workflows focused on
  decisions, evidence contracts, and failure boundaries that a stronger model
  should not guess.
- **Three-way measurement:** compare no-skill, v0.2 full-skill, and current
  lean-skill runs while holding the model, reasoning effort, repository
  revision, tools, prompt, and done conditions constant.
- **Clearer presentation:** a readable engineering-loop diagram, refreshed
  social preview, and tracked community-distribution experiments.

## Try the Living Wiki

Ask a read-only question before adding infrastructure:

```text
$maintain-codex-wiki What does this repository know about orchestration
efficiency? Cite wiki pages, separate evidence from recommendation, and do not
modify files.
```

Run its deterministic health check:

```bash
python3 skills/maintain-codex-wiki/scripts/wiki_lint.py .
```

The initial implementation deliberately uses Markdown, repository search, and
Git review. It does not add a database, vector index, MCP server, or autonomous
merge path without evidence that those layers are needed.

## Verification

The release gate covers:

- repository structure and local-link validation;
- all 14 measurement and wiki utility tests;
- both dependency-free engineering playground tests;
- six seeded wiki pages and their registered sources;
- wiki metadata, index coverage, and local links; and
- Python compilation for the bundled scripts.

## Feedback wanted

Useful contributions include:

- a source that contradicts an existing wiki conclusion;
- a query the index routes poorly;
- an anonymized no-skill/full-skill/lean-skill measurement;
- a workflow step that adds cost without improving quality; or
- a maintained stack, team, or translation fork.

Codex How To is an independent community project. Official OpenAI
documentation remains authoritative for current product behavior.
