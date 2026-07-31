# Engineering-loop measurement protocol

Use this protocol to decide whether an engineering skill earns its context
cost. Compare the model alone, the v0.2 full skill, and the current lean skill.
The goal is not to prove that one prompt wins once; it is to detect whether
workflow instructions improve repeatable, quality-gated completion.

## Hypothesis

Write the hypothesis before running either variant:

```text
For [task class], [skill variant] will improve [primary quality measure]
without an unacceptable increase in [time, tokens, cost, or human corrections].
```

Choose one primary quality measure. Treat speed, tokens, and cost as secondary
until all variants satisfy the same acceptance criteria.

## Three variants

Use three fresh copies of the same starting commit:

- `no_skill`: give Codex the task contract without naming or installing a
  repository skill;
- `full_skill`: install `engineering-loop` from the `v0.2.0` tag and invoke it;
- `lean_skill`: install the current `engineering-loop` and invoke it.

Keep the model, reasoning setting, starting commit, Codex surface, sandbox,
available tools, repository instructions, dependency state, and acceptance
criteria fixed. Record the exact model, reasoning effort, starting commit,
tool-profile label, and skill version for every run.
Use `none` as the `skill_version` for `no_skill`, `v0.2.0` for the full
baseline, and a release, commit SHA, or branch label for the lean candidate.

Do not reuse a modified worktree or paste discoveries between runs. Rotate the
variant order across tasks to reduce order and operator-learning effects.

## Minimum experiment

Run at least three paired tasks before drawing a local directional conclusion.
The playground supports three useful task classes:

1. backend boundary defect;
2. frontend behavior, accessibility, and unsafe rendering;
3. infrastructure review and hardening plan.

Create one run of every variant for each `task_id`. Keep the
[playground rubric](../labs/engineering-playground/rubric.md) hidden until all
three runs finish. When practical, review anonymized diffs and reports without
knowing the variant.

Three task sets are enough to exercise the protocol, not to establish a general
productivity claim. Repeat on representative real tasks before changing team
policy.

## Measures

Record quality before efficiency:

| Measure | Definition |
|---|---|
| `accepted` | The result satisfies the task's acceptance criteria without a human code correction |
| `evidence_complete` | The report distinguishes verified results, unrun checks, assumptions, and residual risk |
| `regression_before_fix` | For a reproducible defect, a relevant check fails before implementation and passes afterward |
| `focused_checks_passed` | The narrow checks relevant to the changed behavior pass |
| `required_checks_passed` | All repository-required applicable checks pass |
| `actionable_findings` | Unique consequential issues found during final review |
| `false_positives` | Reported findings rejected by the evaluator as unsupported or non-actionable |
| `retries` | Repeated attempts that did not add new evidence |
| `human_corrections` | Human interventions that changed code, tests, requirements, or the next technical action |
| `elapsed_seconds` | Wall-clock time from submitted prompt to final report, including tool execution and human waits |
| `total_tokens` | Total input plus output tokens when the surface exposes them |
| `total_cost_usd` | Total run cost when the surface exposes it |
| `context_noise_lines` | Raw log or diagnostic lines returned to the main decision context but not used in the final evidence |

Define acceptance criteria and counting rules before the run. Leave unavailable
optional measurements blank; do not estimate hidden token or cost data.

## Record and summarize

Copy [the CSV run record](../examples/measurements/engineering-loop-runs.csv)
and add one row per run. Preserve the header and use `true` or `false` for
observed boolean fields. `accepted` and `evidence_complete` are required. Leave
other unavailable or non-applicable measures blank, and quote notes containing
commas as normal CSV.

Generate a Markdown summary:

```bash
python3 scripts/summarize_engineering_loop.py \
  examples/measurements/engineering-loop-runs.csv
```

The summary reports quality rates first, medians second, and complete
three-variant coverage. It does not collapse the result into one score.

## Decision rule

Retain the skill for the measured task class only when:

1. it improves correctness, safety, evidence quality, or rework; or
2. it supplies a repeatable team output or domain rule not available from the
   task and repository context;
3. any increase in elapsed time, tokens, or cost is justified by that gain; and
4. the result repeats across representative task sets.

Prefer the lean skill when it preserves the full skill's quality with lower
token use, latency, or retries. Prefer no skill when quality is unchanged and
both skill variants add overhead. “Higher quality but slower,” “faster but less
reliable,” and “no observed difference” are valid outcomes.

## Threats to validity

- task leakage between variants;
- different starting commits or dependency state;
- different models, reasoning settings, permissions, or tools;
- evaluator knowledge of the variant;
- prompts with unequal acceptance criteria;
- counting unsuccessful runs only for one variant;
- using token savings as a proxy for correctness;
- generalizing from the seeded playground to production work.

Keep raw run records so another developer can audit the conclusion.

## Model-adaptive interpretation

Do not hard-code a permanent conclusion for one model generation. Re-run the
ablation after a material model, reasoning-default, tool, or Codex-runtime
change. See [Model-adaptive skills](model-adaptive-skills.md) for the design
rules behind this protocol.
