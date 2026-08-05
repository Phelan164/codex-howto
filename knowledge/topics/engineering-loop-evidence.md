# Engineering-loop evidence

> Status: experimental
> Last updated: 2026-08-05
> Sources: `local-engineering-loop-measurement`, `ecc-loop-controls`

## Current understanding

The engineering loop defines useful completion evidence: baseline or
reproduction, a coherent change, focused checks, required checks, final diff
review, and a handoff that records uncertainty. The repository does not treat
the existence of that workflow as proof that its skill is more efficient.

## Evidence

The
[measurement protocol](../../resources/engineering-loop-measurement.md) compares
three variants with the model, reasoning effort, repository state, and done
conditions held constant:

1. no skill;
2. the earlier full skill; and
3. the current lean skill.

It records quality gates, retries, context noise, elapsed time, and tokens when
available.

## Implications

Examples and demos establish that the workflow is runnable, not that it
generalizes. Team recommendations require repeated measurements on
representative work.

## Promotion status

The workflow is published, while its efficiency claim remains experimental.
Future run data should update this page before changing the recommendation.

For repeated autonomous tasks, the loop now defines an optional judge,
iteration and retry budgets, stop-loss rules, and a resumable checkpoint.
Measurements should include stopped runs, first-judge pass rate, and iterations
to green so one eventual success is not mistaken for reliable control.
