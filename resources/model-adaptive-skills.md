# Model-adaptive skills

Treat a skill as an evaluated workflow contract, not a permanent patch for
model weakness.

## Start with the model

Run a representative task without a skill first. Add a skill only when it
contributes at least one non-generic capability:

- a stable sequence whose omission causes measured failures;
- repository, organization, policy, schema, or tool knowledge;
- safety or authorization boundaries specific to the workflow;
- a required output or evidence contract;
- a deterministic script, template, or validation resource.

Do not use a skill merely to tell a capable coding model to inspect, plan,
implement carefully, run tests, or be concise.

## Keep the loaded body lean

State each instruction once. Keep the essential decision sequence in
`SKILL.md`; move detailed checklists, variants, and policies into direct
references that are loaded only when relevant. Remove examples that do not
encode a product requirement or correct a measured failure.

Descriptions should identify the task and its boundaries. Do not use a router
skill to compensate for overlapping descriptions; fix the descriptions first.
Keep coordination workflows explicit-only when accidental activation would add
agents, latency, or context.

## Evaluate by ablation

Compare:

1. `no_skill` — the task contract and repository context only;
2. `full_skill` — the previous stable skill;
3. `lean_skill` — the reduced candidate.

Hold the model, reasoning effort, starting commit, tools, permissions, and done
conditions constant. Judge quality and safety before tokens or speed. Use the
[engineering-loop measurement protocol](engineering-loop-measurement.md) and
record the exact model and skill version.

## Decide

- Keep the lean skill when it preserves or improves quality with less overhead.
- Keep the full skill only when removed instructions prevent a repeatable
  failure.
- Use no skill when quality is unchanged and the skill adds context, turns, or
  latency.
- Re-run the comparison after a material model or runtime change.

Do not generalize from one seeded task. Publish the task class, measurement
limits, and negative results.

## Official sources

- [GPT-5.6 prompting best practices](https://developers.openai.com/api/docs/guides/model-guidance?model=gpt-5.6#prompting-best-practices)
- [Build focused skills](https://developers.openai.com/plugins/build/skills#define-the-workflow-boundary)

Last verified: 2026-07-31.
