# 05 · Engineering skills

## Outcome

Turn a proven engineering workflow into a discoverable, token-efficient Codex skill.

## Why skills

A skill packages instructions plus optional references, scripts, and assets. Codex sees compact metadata first, loads `SKILL.md` when the skill is selected, and reads bundled resources only when needed. This progressive disclosure keeps reusable depth available without loading all of it into every task.

## Anatomy

```text
skill-name/
├── SKILL.md
├── agents/openai.yaml
├── references/     # optional, read only when relevant
├── scripts/        # optional, deterministic repeated operations
└── assets/         # optional, copied or used in outputs
```

`SKILL.md` requires:

```markdown
---
name: review-code
description: Review code changes for correctness, regressions, security risks, and missing tests. Use for PR, branch, commit, or working-tree reviews.
---

Imperative workflow...
```

The description is the trigger. Put both capability and usage context there.

## Installation

- Repository skill: `.agents/skills/<skill-name>/`
- Personal skill: `~/.agents/skills/<skill-name>/`

Invoke explicitly with `$skill-name`, or let Codex match the description.

Example repository installation:

```bash
mkdir -p .agents/skills
cp -R /path/to/codex-howto/skills/review-code .agents/skills/
```

Then start a new task:

```text
$review-code Review this branch against main. Lead with consequential findings
and list checks you could not run.
```

## Extract a workflow

Create a skill only after you can answer:

1. What user requests should trigger it?
2. What sequence is stable across projects?
3. Which decisions remain project-specific?
4. What evidence proves the workflow completed correctly?
5. Which details should live in optional references?

Avoid a single “software-engineer” skill that tries to cover every technology. Narrow skills trigger more reliably and are easier to maintain.

## Lab A: install and inspect an existing skill

1. Pick one bundled skill.
2. Read its `SKILL.md` and reference.
3. Copy it into `.agents/skills/`.
4. Invoke it on a small task.
5. Record where it lacked repository-specific knowledge.
6. Put repository facts in `AGENTS.md`, not in the reusable skill.

## Lab B: author a skill from scratch

Create a narrow `summarize-test-failure` skill with the built-in creator:

```text
$skill-creator Create a repo-scoped skill named summarize-test-failure.

Trigger it when a user asks to analyze failing test output or CI test logs.
It must return the failing command, failing cases, concise root-cause evidence,
environment uncertainty, and the next diagnostic action. It must not modify
production code or return full logs. Keep the main SKILL.md concise and place
the output template in one direct reference.
```

Review the generated `.agents/skills/summarize-test-failure/` folder:

- `SKILL.md` frontmatter contains only `name` and `description`;
- the description includes intended triggers and boundaries;
- instructions are imperative and define acceptance criteria;
- `agents/openai.yaml` has quoted UI strings and a default prompt containing
  `$summarize-test-failure`;
- the reference is linked directly from `SKILL.md`.

Ask `$skill-creator` to validate the folder. Then test both sides of discovery:

```text
$summarize-test-failure Analyze this failing test output: [sanitized output]
```

```text
Implement this unrelated frontend layout change.
```

The first request should use the skill. The unrelated request should not select it implicitly. If a new or updated skill is not visible in `/skills`, restart Codex and inspect its discovery location.

## Lab C: use the engineering skill set

Copy the [engineering playground](../../labs/engineering-playground/README.md)
to a disposable directory. Its staged exercises use every bundled skill across
backend, frontend, infrastructure, testing, code review, security review, and
orchestration. Start with one relevant skill; add orchestration only for the
final comparison.

## Verify

- The skill triggers for intended requests and not adjacent requests.
- A newly authored skill passes metadata validation.
- The body is concise and imperative.
- Optional details are one reference hop away.
- Acceptance criteria produce observable evidence.
- The skill contains no environment-specific secret or destructive default.

## Official source

- [Build and use skills](https://developers.openai.com/codex/skills)

Last verified: 2026-07-24.
