# GPT-5.6-sol 2048 game seed measurement

> Date: 2026-07-31
> Status: one controlled medium-sized task set; insufficient for a general
> efficiency claim

## Question and hypothesis

Does the repository's `engineering-loop` improve a medium-sized browser-game
implementation with GPT-5.6-sol?

The pre-registered primary measure was acceptance without a human code
correction. The directional hypothesis was that the lean skill would preserve
the full skill's acceptance and evidence quality with fewer tokens or retries.
Elapsed time and token use were secondary until acceptance passed.

## Fixed setup

| Field | Value |
|---|---|
| Fixture revision | `7043dd6e04c2793f5d24e41c4eba67ac660068d5` |
| Codex surface | Codex CLI 0.143.0, ephemeral `exec` |
| Model | `gpt-5.6-sol` |
| Reasoning effort | `medium` |
| Sandbox | `workspace-write` |
| Task | Implement the dependency-free 2048 benchmark |
| Variants | no repository skill; `engineering-loop` v0.2.0; `engineering-loop` v0.4.0 |
| Run order | full skill, lean skill, no repository skill |

Each variant began at the same clean Git commit and received the same task,
repository instructions, tools, dependencies, sandbox, model, and acceptance
criteria. The two skill variants explicitly invoked their installed
`engineering-loop`; the control did not install or name a repository skill.
Global personal skills remained visible to every run. The control selected
`onboarding` and `coding-workflow`, so this measures incremental repository-skill
value over a realistic configured Codex—not an instruction-free model.

Before any measured run, a reference implementation passed the ten supplied
tests and the post-run evaluator. Two incorrect score expectations discovered
during that benchmark preflight were corrected before the common baseline
commit; no variant saw a different test.

## Results

| Variant | Accepted | Evidence complete | Required checks | Retries | Elapsed | Total reported tokens |
|---|---:|---:|---:|---:|---:|---:|
| No repository skill | yes | yes | passed | 1 | 350 s | 828,446 |
| Full skill v0.2.0 | yes | yes | passed | 1 | 257 s | 553,179 |
| Lean skill v0.4.0 | yes | yes | passed | 0 | 247 s | 380,767 |

`total reported tokens` is CLI `input_tokens + output_tokens`. Cached input is
already included in input tokens and is not added twice.

| Variant | Input tokens | Cached input | Output tokens | Reasoning output |
|---|---:|---:|---:|---:|
| No repository skill | 815,286 | 754,944 | 13,160 | 3,089 |
| Full skill v0.2.0 | 543,191 | 491,520 | 9,988 | 2,773 |
| Lean skill v0.4.0 | 373,301 | 330,752 | 7,466 | 2,075 |

Reasoning output is reported separately by the CLI and is not added again.

All variants:

- implemented all four required browser-game files;
- passed all 10 supplied engine tests without modifying them;
- passed JavaScript syntax checks and every post-run evaluator check;
- kept the implementation dependency-free and free of network calls;
- reviewed the final added files; and
- distinguished verified checks from browser behavior that remained unverified.

No run completed a browser interaction. The sandbox denied loopback server
binding and Chromium startup. The lean run stopped after establishing that
browser execution was unavailable. The other variants explored additional
launch routes; retries count only a repeated attempt that added no new evidence,
not the first command that established a distinct environmental limitation.

## Directional interpretation

This task shows no quality difference: every variant passed the same public and
post-run gates with no human code correction.

The lean skill used about 31.2% fewer reported tokens than v0.2.0 and 54.0%
fewer than the no-repository-skill control. It was about 3.9% faster than v0.2.0
and 29.4% faster than the control. On this task, the lean workflow earned its
context cost relative to the older skill and did not add overhead over the
configured control.

That is a task-local observation, not proof that skills generally save tokens.
The smaller backend seed produced a different result: the control used the
fewest tokens. Together, the two runs suggest a useful boundary to test:
lifecycle guidance may be redundant for small, strongly specified fixes but
helpful when a task has multiple implementation and verification surfaces.

## Limitations

- This is one seeded game task, not an independent community replication.
- The public test and evaluator emphasize deterministic engine behavior; live
  browser behavior and visual quality were not verified.
- All runs could see the same personal global skill catalog, and the control
  auto-selected two global workflow skills.
- The evaluator knew each variant after execution.
- Run order was not randomized. Rotate it for the next task.
- The CLI repeatedly emitted a model-cache schema warning that did not fail a
  run.
- Elapsed time uses the run event-log creation and completion timestamps,
  rounded to the nearest second.
- Cost and context-noise-line measurements were unavailable and not estimated.

## Next evidence

Repeat the three variants on the existing frontend and infrastructure tasks,
then use representative external repository work. Keep quality gates primary,
rotate run order, and use successful browser interaction where the environment
allows it.
