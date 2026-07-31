# Model-adaptive skills

> Status: verified
> Last verified: 2026-07-31
> Sources: `official-codex-manual`, `local-model-adaptive-skills`

## Current understanding

A capable current model already knows generic engineering practice. A skill
earns its context and maintenance cost when it supplies a measured workflow
gap, repository or domain knowledge, a safety boundary, an evidence contract,
or a deterministic reusable resource.

Progressive disclosure makes a focused skill efficient: metadata is visible
for discovery, the main instructions load only when selected, and references
or scripts load only when needed.

## Evidence

- OpenAI's skill guidance recommends focused workflows, concise descriptions,
  progressive disclosure, and testing trigger behavior.
- The repository's
  [model-adaptive guide](../../resources/model-adaptive-skills.md) applies that
  guidance to GPT-5.6-era engineering workflows and requires a no-skill
  baseline.

## Implications

Do not add a skill simply because a workflow can be written down. Compare it
with the same task and model without the skill, then retain only instructions
that improve a measured result or enforce a necessary boundary.

## Promotion status

Promoted into module
[05 · Engineering skills](../../modules/05-engineering-skills/README.md) and the
current lean skill catalog.
