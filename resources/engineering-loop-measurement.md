# Engineering-loop measurement protocol

Use this protocol to compare an ordinary Codex run with the repository's
engineering loop. The goal is not to prove that one prompt wins once. The goal
is to learn whether the workflow improves repeatable, quality-gated completion
for your tasks.

## Hypothesis

Write the hypothesis before running either variant:

```text
For [task class], the engineering-loop variant will improve [primary quality
measure] without an unacceptable increase in [time, tokens, cost, or human
corrections].
```

Choose one primary quality measure. Treat speed, tokens, and cost as secondary
until both variants satisfy the same acceptance criteria.

## Variants

Use two fresh copies of the same starting commit:

- `ad_hoc`: give Codex the task contract without naming a repository skill or
  prescribing the engineering-loop stages;
- `engineering_loop`: give Codex the same task contract and explicitly invoke
  `$engineering-loop` plus only the relevant specialist skills.

Keep the model, reasoning setting, Codex surface, sandbox, available tools,
repository instructions, dependency state, and acceptance criteria fixed.
Record any difference you cannot control.

Do not reuse the first run's modified worktree or paste its discoveries into
the second run. Alternate which variant runs first across tasks to reduce order
and operator-learning effects.

## Minimum experiment

Run at least three paired tasks before drawing a local directional conclusion.
The playground supports three useful task classes:

1. backend boundary defect;
2. frontend behavior, accessibility, and unsafe rendering;
3. infrastructure review and hardening plan.

Create one `ad_hoc` and one `engineering_loop` run for each `task_id`. Keep the
[playground rubric](../labs/engineering-playground/rubric.md) hidden until both
runs for that task finish. When practical, review anonymized diffs and reports
without knowing the variant.

Three pairs are enough to exercise the protocol, not to establish a general
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

The summary reports quality rates first, medians second, and paired-task
coverage. It does not collapse the result into one score.

## Decision rule

Interpret the engineering loop as useful for the measured task class only when:

1. acceptance and evidence completeness improve or remain at an agreed
   acceptable level;
2. regressions, focused checks, and required checks provide at least equivalent
   proof;
3. any increase in elapsed time, tokens, or cost is justified by fewer retries,
   fewer human corrections, or better defect coverage; and
4. the result repeats across representative paired tasks.

Report tradeoffs directly. “Higher quality but slower,” “faster but less
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
