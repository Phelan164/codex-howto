# Community Launch Kit

Use this kit to introduce Codex How To to developers who can run, critique,
adapt, or measure it. The goal is useful adoption and feedback—not coordinated
stars or low-context cross-posting.

Start with the
[verified distribution shortlist](distribution-shortlist.md), which ranks
current destinations by audience fit and records their posting constraints.
Use the copy below only after adapting it to the selected destination.

## Launch sequence

| Window | Action | Evidence to collect |
|---|---|---|
| Day 0 | Publish a tagged GitHub release and social preview | Release URL and passing CI |
| Day 1 | Post a short demo on personal LinkedIn, X, or a developer fanpage | Views, repository visits, useful replies |
| Day 2–3 | Submit to Codex GitHub Show and tell, then the OpenAI developer community | Questions, playground attempts, issues |
| Day 4–6 | Submit one entry to Awesome Codex CLI and one skill to Awesome Codex Skills | Referral traffic, installs, accepted PRs |
| Day 7 | Share once in the current r/ChatGPTCoding promotion thread | Clicks, comments, retention |
| Day 8–10 | Publish a complete technical article on DEV or Viblo | Reads, referral traffic, completed demos |
| Day 11–14 | Share results, fixes, and a first community contribution | Repeat visitors, contributors, forks |

Do not publish identical copy everywhere on the same day. Adapt the engineering
angle to the audience, confirm current self-promotion rules, and remain
available to answer questions.

## Repository launch settings

Apply these settings after the launch-readiness pull request is merged:

- **Description:** `Measurable engineering loops for OpenAI Codex: scope,
  implement, test, review, and report evidence.`
- **Topics:** retain `codex`, `codex-cli`, `openai`, `mcp`, `ai-agents`, and
  `developer-tools`; add `software-engineering`, `agentic-workflows`, `testing`,
  `code-review`, `devops`, and `skills`.
- **Social preview:** upload `assets/social-preview.png`.
- **Discussions:** enable only if the maintainer can answer questions and
  moderate the space.
- **Release:** tag `v0.2.0` on the merged main commit and use
  `resources/release-notes-v0.2.0.md` as the release body.

Do not tag the feature branch: the release tag should identify the exact
commit users receive from the default branch.

## One-minute demo outline

1. Show a vague “fix this bug” request.
2. Replace it with the `engineering-loop` playground prompt.
3. Show the failing regression before implementation.
4. Show the small implementation diff and passing checks.
5. End on the evidence report: commands, results, assumptions, and residual
   risk.

Keep the terminal readable. The proof is the loop, not a fast montage of tool
calls.

## OpenAI developer community

**Title**

```text
Codex How To: a measurable engineering loop with 9 reusable skills
```

**Post**

```text
I built Codex How To, an independent engineering-first curriculum for OpenAI
Codex.

The main idea is that generated code is an intermediate result. A task should
move through scope, reproduction, implementation, focused tests, repository
checks, diff review, and an evidence-based handoff.

The repository includes 13 progressive modules, 9 focused skills, a
dependency-free playground, and a paired-run measurement protocol. It covers
frontend, backend, DevOps, testing, security, and bounded multi-agent
orchestration.

I would especially value feedback from developers who try the playground:
which step was unclear, which skill changed the result, and which checks Codex
still missed?

https://github.com/Phelan164/codex-howto
```

## Show HN

Use this only after a new developer can reproduce the five-minute demo from a
clean checkout.

**Title**

```text
Show HN: Codex How To – measurable engineering loops, skills, and orchestration
```

**Body**

```text
I made an open-source, engineering-first guide to Codex. Instead of treating
code generation as completion, it uses a loop: scope → reproduce → implement →
test → review → evidence.

There are 13 modules, 9 installable skills, and a dependency-free practice
repository with seeded defects. I also included a paired-run protocol so teams
can test whether the workflow improves outcomes without claiming a universal
productivity multiplier.

The design choices I would most like challenged are skill routing, when to use
subagents, and how much verification evidence belongs in the final context.

Repository and runnable demo:
https://github.com/Phelan164/codex-howto
```

Do not ask for upvotes. Answer technical questions and disclose that you are
the project author.

## Reddit

Check each subreddit's current rules and use its designated self-promotion,
showcase, or weekly thread. A useful starting set is communities focused on AI
coding, DevOps, GitHub, testing, or the repository's specific engineering
problem.

### AI coding angle

```text
I wanted Codex to behave less like a one-shot code generator and more like an
engineering loop, so I packaged the workflow into an open-source guide and 9
skills.

The interesting part is not the prompt. The loop requires a baseline or
reproduction, the smallest coherent change, focused and required checks, diff
review, and an evidence report. There is a tiny dependency-free playground if
you want to test it without pointing an agent at a production repository.

I am looking for critical feedback on where the loop adds useful discipline
and where it adds unnecessary overhead:
https://github.com/Phelan164/codex-howto
```

### DevOps angle

```text
I published a Codex engineering guide that treats infrastructure work as a
change-safety problem: inspect first, validate locally, preview before apply,
define rollback, and stop at authority boundaries.

It includes an operate-devops skill, a safe playground deployment example,
testing/review workflows, and guidance on when multi-agent orchestration is
actually worth the extra tokens.

Feedback from platform engineers would be valuable, especially on missing
failure modes or unsafe defaults:
https://github.com/Phelan164/codex-howto
```

### GitHub/open-source angle

```text
I turned my Codex learning notes into a structured open-source curriculum:
13 modules, 9 reusable skills, copy-ready repository guidance, CI validation,
and a small practice project.

The repository is designed to be forked into stack-specific, team-specific,
or translated editions while keeping the core reproduce–implement–test–review
loop measurable.

If you maintain developer documentation, I would appreciate feedback on the
five-minute start and contribution paths:
https://github.com/Phelan164/codex-howto
```

## LinkedIn or developer fanpage

```text
Code generation is not the same as engineering completion.

I built Codex How To around a stricter loop:
scope → reproduce → implement → test → review → evidence.

It is an open-source learning package with:
• 13 modules from safe fundamentals to orchestration
• 9 focused skills for frontend, backend, DevOps, testing, and review
• a dependency-free practice project
• a protocol for measuring results instead of claiming “10x”

Try the five-minute playground, adapt a fork for your stack, or tell me where
the workflow breaks:
https://github.com/Phelan164/codex-howto
```

Attach the one-minute demo or the repository social preview. On Facebook or a
fanpage, add one short question such as “Which step does your coding agent skip
most often?” to start a technical discussion.

## Vietnamese developer communities

For Viblo or a Vietnamese developer group, lead with a local-language problem
statement and keep technical terms precise:

```text
Codex sinh code nhanh, nhưng một engineering task chỉ hoàn thành khi có bằng
chứng: reproduce được lỗi, thay đổi nhỏ và đúng scope, test pass, review diff,
và handoff rõ phần chưa kiểm chứng.

Mình xây dựng Codex How To như một learning path open source gồm 13 modules,
9 skills cho frontend/backend/DevOps/testing/review, một playground không cần
dependency, và cách đo hiệu quả qua paired runs.

Mình muốn nhận feedback thực tế: bước nào hữu ích, bước nào tạo overhead, và
workflow còn thiếu case nào trong dự án của bạn?

https://github.com/Phelan164/codex-howto
```

Ask a moderator before posting in groups that do not publish clear promotion
rules.

## Technical article outline

**Working title:** “Code generation is an intermediate result: building a
measurable engineering loop for Codex”

1. The failure mode: a plausible patch without reproducible evidence.
2. The loop contract: scope, reproduce, implement, test, review, evidence.
3. Why one lifecycle owner is usually better than loading every skill.
4. When a bounded subagent saves elapsed time and when it wastes tokens.
5. A complete playground example.
6. Paired-run measurement and limitations.
7. How teams can fork the guide for their stack.

Publish the useful explanation in the article itself. Do not make the article
an empty teaser that requires a GitHub click.

## Calls to action

Choose one primary action per post:

- **Try:** complete the five-minute playground.
- **Critique:** open an issue with one reproducible gap.
- **Measure:** contribute anonymized paired-run results.
- **Adapt:** create a tested stack, team, or translation fork.
- **Follow:** star the project only if it is useful and worth revisiting.

## Distribution tracker

Record data after 24 hours, 7 days, and 30 days:

| Date | Channel | Post URL | Format | Views | Repo visits | Stars | Forks | Issues/PRs | Demo completions | Notes |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| YYYY-MM-DD | Example | URL | Demo | 0 | 0 | 0 | 0 | 0 | 0 | Audience questions |

Use GitHub traffic and referral data while available. Compare channels by
meaningful actions—completed demos, useful issues, repeat visitors, and
maintained forks—not by impressions alone.

## Launch checklist

- [ ] Main branch CI passes.
- [ ] The five-minute demo works from a clean checkout.
- [ ] The repository has a social preview and clear description.
- [ ] A versioned release explains what is stable and what is experimental.
- [ ] Issue templates make feedback easy to classify.
- [ ] Each post matches the destination community and its current rules.
- [ ] The author can answer questions after publishing.
- [ ] Results are recorded without inflating or purchasing engagement.
