# Presenting Codex How To

Use this guide to introduce the repository to developers without walking
through every module or skill. Lead with an engineering outcome, prove it with
one small task, and show the catalog only after the demonstration.

## Core message

> Codex becomes more useful when it follows a measurable engineering loop—not
> simply when it generates more code.

`codex-howto` is an engineering-first curriculum and reusable workflow set for
taking Codex from a scoped task through implementation, testing, review, and
evidence.

## Thirty-second pitch

Codex can generate code quickly, but production engineering also requires
clear acceptance criteria, regression proof, repository checks, review, and a
useful handoff. `codex-howto` packages that process into 13 progressive modules,
9 focused skills, copy-ready templates, and a safe dependency-free playground.
It covers frontend, backend, DevOps, testing, security, and orchestration
without recommending that every task load every workflow or agent.

## Fifteen-minute presentation

| Time | Topic | Show |
|---:|---|---|
| 0–2 min | The gap | Generated code is an intermediate result, not completion |
| 2–4 min | The model | Prompt → `AGENTS.md` → skill → tool/agent only when needed |
| 4–10 min | Live demo | One playground defect through reproduce, fix, test, and review |
| 10–12 min | Skill routing | One lifecycle owner plus relevant domain specialists |
| 12–14 min | Efficiency | Focused context, bounded delegation, evidence summaries |
| 14–15 min | Start here | Choose a learning track or repeat the playground |

Do not spend the opening minutes listing modules. The live result should make
the catalog relevant.

## Live-demo setup

Before presenting:

1. Clone the repository and confirm Codex is available.
2. Copy the playground to a disposable directory.
3. Install only `engineering-loop`, `build-backend`, and `test-software` into
   that copy.
4. Run the existing backend tests and confirm the baseline passes.
5. Keep the playground rubric closed until after the review.
6. Confirm the environment has no production connections or credentials.

Setup commands:

```bash
demo_root="$(mktemp -d)"
cp -R labs/engineering-playground "$demo_root/playground"
mkdir -p "$demo_root/playground/.agents/skills"
cp -R skills/engineering-loop skills/build-backend skills/test-software \
  "$demo_root/playground/.agents/skills/"
cd "$demo_root/playground"
git init
git add .
git commit -m "baseline intentionally flawed playground"
python3 -m unittest discover -s backend -p "test_*.py"
```

The baseline tests pass because the seeded boundary behavior is uncovered.

## Live-demo prompt

```text
$engineering-loop $build-backend $test-software Inspect the inventory
reservation contract, reproduce one uncovered input-boundary defect, add the
smallest regression test, implement the fix, run the required checks, and
review the final diff. Work only in this disposable playground.
```

Narrate the evidence rather than every tool call:

1. **Contract:** What behavior and done condition did Codex establish?
2. **Reproduction:** Did a new regression test fail before implementation?
3. **Change:** Is the implementation smaller than the investigation?
4. **Verification:** Which focused and broader commands passed?
5. **Review:** Did Codex inspect the actual diff and resolve verified findings?
6. **Handoff:** Are assumptions, unrun checks, and residual risks explicit?

If the run fails, use the failure as part of the demonstration. Show whether
the loop distinguishes a product defect, test defect, environment problem, or
incorrect assumption instead of retrying blindly.

## Audience-specific emphasis

### Application engineers

Show `engineering-loop`, `build-frontend`, `build-backend`, `test-software`,
and `review-code`. Emphasize regression tests and contract preservation.

### Platform and DevOps engineers

Show sandbox boundaries, `operate-devops`, preview-before-apply behavior,
rollback planning, and the separation between local validation and deployment
authority.

### Tech leads

Show `AGENTS.md`, review lenses, dependency-aware tickets, engineering
handoffs, and measurable acceptance criteria.

### AI platform teams

Show progressive disclosure, explicit-only routing and orchestration,
skill/plugin packaging, context budgets, and the orchestration decision
matrix.

## Measurement

Compare one normal task with one workflow-assisted task. Keep task, repository,
model, and environment as similar as practical.

Record:

- acceptance criteria satisfied;
- unique consequential findings;
- false positives;
- implementation and test retries;
- focused and broader check outcomes;
- elapsed time;
- total tokens, credits, or cost when available;
- amount of raw log content returned to the main context;
- human corrections required before acceptance.

Do not claim that skills or multiple agents are more efficient from one run.
Look for fewer failed loops, better evidence, and more predictable completion
across repeated comparable tasks. Use the
[token-efficiency scorecard](resources/token-efficiency-scorecard.md).

## Copy-ready announcement

> I built `codex-howto`, an engineering-first guide for OpenAI Codex.
>
> It goes beyond installation and prompting: it covers `AGENTS.md`, reusable
> skills, frontend/backend/DevOps workflows, testing, code review, security,
> and disciplined multi-agent orchestration.
>
> The central workflow is a complete engineering loop: reproduce, implement,
> test, review, fix verified findings, and report evidence.
>
> The repository includes 13 progressive modules, 9 focused skills, copy-ready
> templates, and a dependency-free practice project.
>
> https://github.com/Phelan164/codex-howto

## Frequently asked questions

### Is this official OpenAI documentation?

No. It is an independent community curriculum. Product claims link to official
documentation, which remains the source of truth.

### Is this another large prompt collection?

No. Prompts are only one layer. The repository teaches where one-off context,
repository guidance, reusable skills, tools, agents, plugins, and automation
belong.

### Do more agents save tokens?

Usually not. Parallel agents may reduce elapsed time, isolate noisy
investigation, or add specialist coverage, but they commonly increase total
token use.

### Why not install every skill?

Overlapping instructions add discovery and context cost. Start with one
lifecycle owner and add a specialist only when it changes domain decisions.

## Presentation checklist

- The first minute states the engineering problem and observable outcome.
- The demo repository is disposable and disconnected from production.
- The audience sees a failing regression before the fix when practical.
- The final report includes commands and results, not only a success claim.
- No unmeasured productivity multiplier is presented as fact.
- The final slide gives one next action: try the playground or choose a track.
