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

- [GPT-6 Astra prompting and migration guidance](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices)
- [Build focused skills](https://learn.chatgpt.com/docs/build-skills)

Last verified: 2026-09-08. The latest-model URL described GPT-6 Astra on this date.

## GPT-6 Astra compatibility review

OpenAI documents stronger instruction following, possible unnecessary
clarification pauses, less delegation than a workflow may want, and excessive
verification for small changes. Audit both `SKILL.md` and conditional
references alongside applicable `AGENTS.md` files: contradictory guidance in a
rarely loaded reference can still change execution.

Our engineering-loop adaptation is a community practice informed by that
guidance, not a measured Astra efficiency improvement:

- Carry existing authorization forward and distinguish an implementation-plan
  change from expanded task scope. Resolve routine gaps using repository
  evidence; surface material unanswered decisions.
- When a skill causes a pause, identify the exact instruction and check whether
  the user has already supplied the required authority.
- Finish after acceptance evidence and required checks pass. Additional checks
  need a new change, failure, or unresolved concern to justify them.
- Start with one agent. Use authorized delegation for independent subtasks
  when expected time savings or coverage justify the coordination cost.
- Preserve regression evidence, review, explicit budgets, and accurate handoff.
  Avoid duplicating model-host instructions unless a workflow-specific decision
  needs clarification.

Before claiming an improvement, compare three conditions on GPT-6 Astra:
no engineering-loop, the pre-adaptation skill, and the revised skill. Record
the exact commit for each skill; use the same starting task state, reasoning
effort, tools, permissions, and acceptance checks in fresh sessions. Disable
engineering-loop in the control, since omission from the prompt does not
prevent automatic selection. Keep other available skills constant.

Record unnecessary approval pauses, human corrections, checks repeated without
new evidence, acceptance outcomes, elapsed time, and reported tokens across all
participating agents. Include unsuccessful runs. Repeat paired comparisons
and alternate run order; a single successful run proves neither efficiency nor
generality. Use the existing measurement protocol and receipt, with additional
observations in the evidence notes.

Retain historical GPT-5.6 results with their original model and skill revisions.
They do not establish Astra performance. This documentation update does not
change model defaults or enable new runtime capabilities.
