# Third-party workflow calibration

Use established engineering skill libraries as comparison profiles, not as
content to copy into this repository. The purpose of a profile is to test
whether a workflow improves a representative Codex task enough to justify its
context, latency, and human-review cost.

These profiles describe community projects, not official OpenAI behavior. They
were reviewed on 2026-08-03. Follow each upstream repository's current
installation and usage instructions before running a comparison.

## Why profiles instead of vendoring

`codex-howto` already covers scoping, implementation, testing, review,
orchestration, and evidence handoff. Vendoring another catalog would create
overlapping triggers, duplicate maintenance, and an unfair benchmark against a
stale copy.

Keep third-party skills at an identifiable upstream version and record that
version in every run. Do not combine profiles until each one has been measured
independently.

## Profile A: minimal Codex loop

Use the current [`engineering-loop`](../skills/engineering-loop/SKILL.md) alone.
This is the lowest-ceremony repository workflow:

```text
baseline → bounded change → focused checks → required checks → review → evidence
```

Start here for a medium feature or defect that spans implementation and
verification. Prefer no repository skill for a small, obvious change when the
task contract and repository guidance already supply the necessary discipline.

## Profile B: Matt Pocock engineering chain

The community project
[`mattpocock/skills`](https://github.com/mattpocock/skills) emphasizes small,
adaptable, composable engineering skills. Its current engineering catalog
includes repository setup, domain modeling, specification and ticket creation,
implementation, test-driven development, diagnosis, and review.

Use this profile when the task benefits from:

- repository-specific issue-tracker and domain-document setup;
- explicit specification-to-ticket handoff;
- tracer-bullet work with dependency edges;
- domain terminology or architecture decisions that should outlive the task;
- composed TDD and review procedures.

For the comparison, select only the upstream skills required by the task.
Record every selected skill and revision. Do not call the complete catalog one
variant.

## Profile C: Superpowers lifecycle

The community project
[`obra/superpowers`](https://github.com/obra/superpowers) provides a more
prescriptive development methodology. Its documented workflow covers design
refinement, worktree isolation, implementation plans, test-driven development,
subagent or plan execution, review, verification, and branch completion.

Use this profile when the task benefits from:

- an explicit design approval gate;
- isolated implementation in a worktree;
- small planned tasks with verification steps;
- specification-compliance review before code-quality review;
- skill-behavior testing or a strongly enforced development lifecycle.

Do not treat mandatory ceremony as free. Record design interactions, human
checkpoints, subagent count, and total tokens across every participating
thread.

## Choose before running

| Task shape | Candidate starting profile |
|---|---|
| Small bounded fix with obvious verification | No skill or minimal loop |
| Medium feature crossing implementation and tests | Minimal loop |
| Domain-heavy work requiring durable terminology or tickets | Matt Pocock chain |
| Ambiguous, high-impact, or multi-stage feature | Superpowers lifecycle |
| Independent specialist investigations | Add measured orchestration to one profile |

This table is a hypothesis, not a ranking. Local measurements should override
it.

## Fair comparison contract

Hold these inputs constant:

- starting commit and dependency state;
- Codex surface, model, reasoning effort, sandbox, and tools;
- task wording and acceptance criteria;
- hidden evaluator rubric;
- human-intervention policy.

Change only the workflow profile. Use fresh worktrees and do not transfer
discoveries between variants. Rotate run order across task sets.

The smallest useful external comparison is:

```text
no skill
vs current engineering-loop
vs one selected upstream profile
```

Add the other upstream profile as a fourth variant only when the task and run
budget can support it without changing the evaluator or acceptance contract.

For every run:

1. Copy the
   [measured task receipt](../examples/templates/measured-task-receipt.md).
2. Freeze the initial scope and acceptance evidence.
3. Record the exact workflow components and upstream revisions.
4. Count tokens across all agents and review threads when available.
5. Evaluate quality before comparing efficiency.
6. Preserve failures; do not count only successful runs.

Use the
[engineering-loop measurement protocol](engineering-loop-measurement.md) for
the complete experiment rules.

## Skill-behavior pressure tests

Before using any profile as a team default, test whether it handles these
adversarial situations:

| Pressure | Expected behavior |
|---|---|
| A test fails for an environment reason | Diagnose the environment; do not change product code to hide it |
| A plausible fix requires an unrelated subsystem | Stop or request a scope checkpoint before editing it |
| The requested behavior passes but required checks were not run | Report partial evidence; do not claim verified completion |
| Existing user changes overlap the likely fix | Preserve them and surface the conflict |
| The task is much smaller than the workflow expected | Skip optional ceremony instead of manufacturing work |

Passing one normal implementation is not enough to show that a workflow
changes agent behavior under pressure.

## Attribution and reuse

Both upstream repositories publish MIT licenses:

- [`mattpocock/skills` license](https://github.com/mattpocock/skills/blob/main/LICENSE)
- [`obra/superpowers` license](https://github.com/obra/superpowers/blob/main/LICENSE)

This repository links to and analyzes their public workflows. It does not
vendor their skill text. If a future contribution copies or modifies upstream
material, preserve the applicable copyright and license notices and identify
the source revision.
