# Codex How To v0.5.0

Codex How To now includes controlled GPT-5.6-sol measurements for deciding
when an engineering skill earns its context cost, plus a reproducible
medium-sized implementation benchmark and a distributable Codex plugin bundle.

## Highlights

- **Measured skill value:** six controlled runs compare no repository skill,
  the v0.2.0 full `engineering-loop`, and the v0.4.0 lean skill across a small
  backend fix and a medium browser-game implementation.
- **Balanced result:** every variant passed. The control used the fewest
  reported tokens on the small fix; the lean skill used 31.2% fewer reported
  tokens than v0.2.0 and 54.0% fewer than the control on the game task.
- **Reproducible game benchmark:** a dependency-free 2048 fixture exercises
  deterministic state transitions, browser input, accessibility, responsive
  UI, automated checks, review, and evidence handoff.
- **Plugin distribution:** the repository includes marketplace-ready metadata,
  install guidance, and automated plugin-bundle scanning.
- **Safer evidence identity:** Living Wiki sources can pin immutable revisions,
  declare affected pages, preserve source paths, and validate supersession
  relationships.
- **Actionable participation:** maintainers can contribute anonymized
  measurements, stack adaptations, translations, and evidence-backed wiki
  improvements.

## What the measurements mean

The release does not claim that skills always save tokens. It shows why
measurement must keep quality gates primary:

| Task | Quality result | Most token-efficient variant |
|---|---|---|
| Small backend boundary fix | All variants passed | No repository skill |
| Medium 2048 browser game | All variants passed | Lean skill v0.4.0 |

Two seeded tasks are not a general productivity study. Repeat the three-way
ablation on representative work before standardizing or removing a skill.

## Try the engineering loop

Install the current skill into Codex:

```bash
npx skills add Phelan164/codex-howto --skill engineering-loop -g -a codex -y
```

Run the dependency-free backend playground:

```bash
demo_root="$(mktemp -d)"
cp -R labs/engineering-playground "$demo_root/playground"
cd "$demo_root/playground"
git init
```

For the medium task, follow
[`labs/2048-game-benchmark/README.md`](../labs/2048-game-benchmark/README.md).
Inspect every skill before use; it runs with the permissions available to the
invoking agent.

## Verification

The release gate covers:

- repository structure and all relative Markdown links;
- 42 measurement and Living Wiki utility tests;
- both dependency-free backend playground tests;
- all 10 public game-engine tests plus post-run evaluator checks for each
  measured candidate;
- six seeded wiki pages with zero lint warnings;
- Python compilation and JavaScript evaluator syntax;
- GitHub Actions repository validation; and
- automated plugin-bundle scanning.

Live browser interaction for the seed game runs was blocked by the managed
sandbox and is recorded as unverified. The evaluator checks engine behavior and
the static browser contract; it does not replace visual, interaction, or
assistive-technology testing.

## Feedback wanted

The highest-value contribution is an independent replication:

1. choose a representative task;
2. run no repository skill, v0.2.0, and the current lean skill from identical
   starting conditions;
3. keep acceptance and evidence quality primary; and
4. submit anonymized measurements, including results that show no advantage.

Codex How To is an independent community project. Official OpenAI
documentation remains authoritative for current product behavior.
