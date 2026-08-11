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
| Day 0 | Publish a tagged release, verify `npx skills`, and confirm skills.sh plus independent audit pages | Release URL, passing CI, install result, audit URLs |
| Day 1 | Publish one short measurement result on a personal developer channel | Views, repository visits, useful disagreement |
| Day 2–3 | Update the existing Codex GitHub Show and tell and project announcement | Questions, playground attempts, issues |
| Day 4–6 | Submit one guide listing and one flagship skill listing | Referral traffic, installs, accepted PRs |
| Day 7 | Share the mixed benchmark result once in an allowed Codex showcase or promotion thread | Clicks, technical replies, replications |
| Day 8–10 | Publish a complete measurement article on DEV or Viblo | Reads, referral traffic, completed demos |
| Day 11–14 | Share corrections, independent results, and the fork-edition starter | Repeat visitors, contributors, maintained forks |

Do not publish identical copy everywhere on the same day. Adapt the engineering
angle to the audience, confirm current self-promotion rules, and remain
available to answer questions.

## Repository launch settings

Verify these settings before each release:

- **Description:** state the module count, installable skills, measurement
  surface, and engineering audience without claiming a productivity multiplier.
- **Topics:** keep the available topic slots focused on Codex, agent skills,
  software engineering, testing, review, DevOps, orchestration, and knowledge
  maintenance.
- **Social preview:** upload `assets/social-preview.png`.
- **Discussions:** keep the evergreen welcome post aligned with the current
  release and replication request.
- **Release:** tag the merged `main` commit and use the matching file under
  `resources/release-notes-v*.md`. The current release is
  [`v0.5.0`](https://github.com/Phelan164/codex-howto/releases/tag/v0.5.0).
- **Trust evidence:** verify the public SkillStore audit links and badge
  endpoints before displaying them.

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
Codex How To: engineering loops and a review-first living wiki
```

**Post**

```text
I built Codex How To, an independent engineering-first curriculum for OpenAI
Codex.

The main idea is that generated code is an intermediate result. A task should
move through scope, reproduction, implementation, focused tests, repository
checks, diff review, and an evidence-based handoff.

The repository includes 14 progressive modules, 9 installable skills, a
review-first Codex Living Wiki, a dependency-free playground, and a
reproducible three-way skill-ablation protocol.

Six controlled GPT-5.6-sol runs produced a mixed result. Every variant passed.
No repository skill used the fewest reported tokens on a small backend fix.
The lean engineering loop used 31.2% fewer reported tokens than v0.2.0 and
54.0% fewer than the no-skill control on a medium 2048 implementation.

I would especially value independent results that disagree with this boundary:
which task did you run, what passed, where did the skill help, and where did it
add ceremony?

https://github.com/Phelan164/codex-howto
```

## Hacker News

Do not submit the documentation repository by itself. The
[Show HN guidelines](https://news.ycombinator.com/showhn.html) exclude reading
material and lists. The interactive benchmark creates an eligible tool only
after every gate below passes:

- PR #27 is merged and its CI is green on `main`;
- `https://codex-howto-benchmark.nguyenvantamdk2.chatgpt.site` is public;
- an anonymous visitor receives the explorer without sign-in;
- both task toggles work and the source-measurement links resolve; and
- the maintainer can remain available for technical questions.

The merge, public-access, anonymous-response, and CI gates passed on
2026-08-02. Run one final interaction and outbound-link smoke test immediately
before submitting.

**Title**

```text
Show HN: Do Codex skills save tokens? A six-run task-size benchmark
```

**Body**

```text
I built an interactive explorer for a small controlled experiment with
GPT-5.6-sol.

Six runs compared no repository skill, engineering-loop v0.2.0, and a lean
v0.4.0 skill across two task sizes. Every variant passed its acceptance gates.
The result reversed with task size: no repository skill used the fewest
reported tokens on a bounded backend fix, while the lean skill used 54.0% fewer
than the control on a medium dependency-free 2048 implementation.

The useful claim is not that skills save tokens. It is that a workflow skill
has to earn its context cost for the task class.

The explorer shows the exact token, time, retry, and acceptance results; links
to both source measurements; and keeps the limitations visible. I would value
replications that disagree, especially on real frontend, infrastructure,
ambiguous-debugging, or security-sensitive work.

Interactive benchmark:
https://codex-howto-benchmark.nguyenvantamdk2.chatgpt.site

Source and replication protocol:
https://github.com/Phelan164/codex-howto
```

Do not ask for votes, coordinate comments, or submit before anonymous access is
verified. Answer questions with the source measurements rather than expanding
the two-task result into a general performance claim.

## Reddit

Check each subreddit's current rules and use its designated self-promotion,
showcase, or weekly thread. A useful starting set is communities focused on AI
coding, DevOps, GitHub, testing, or the repository's specific engineering
problem.

### AI coding angle

```text
Maintainer disclosure: I built Codex How To, an open-source engineering guide
and skill package for Codex.

I tested whether an engineering workflow skill actually reduces reported token
use. Six controlled GPT-5.6-sol runs compared no repository skill,
engineering-loop v0.2.0, and the current lean skill across two task sizes.

Every variant passed. The no-skill control was cheapest on a small backend fix.
On a medium dependency-free 2048 implementation, the lean skill used 31.2%
fewer reported tokens than v0.2.0 and 54.0% fewer than the control.

My tentative conclusion is not “skills save tokens.” A skill has to earn its
context cost for the task class. I am looking for independent results,
including neutral and negative ones:
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
14 modules, 9 installable skills, a source-grounded living wiki, copy-ready
repository guidance, CI validation, and a small skill-ablation practice
project.

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
• 14 modules from safe fundamentals to living knowledge maintenance
• 9 installable skills for engineering, review, and wiki maintenance
• a source-grounded Codex Living Wiki with deterministic lint
• a dependency-free practice project
• six controlled GPT-5.6-sol seed runs with mixed results

The small task favored no skill. The medium implementation favored the lean
engineering loop. That is a more useful boundary than claiming skills always
save tokens.

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

Mình chạy sáu lượt đo GPT-5.6-sol với ba variant: no-skill, engineering-loop
v0.2.0, và bản lean hiện tại. Cả ba đều pass. Task backend nhỏ dùng no-skill ít
reported token nhất; task 2048 cỡ vừa dùng bản lean ít hơn 31.2% so với v0.2.0
và 54.0% so với control.

Mình muốn nhận feedback thực tế: bước nào hữu ích, bước nào tạo overhead, và
workflow còn thiếu case nào trong dự án của bạn?

https://github.com/Phelan164/codex-howto
```

Ask a moderator before posting in groups that do not publish clear promotion
rules.

## Technical article

Use the complete, publication-ready
[measurement article](articles/do-codex-skills-save-tokens.md). It includes the
controlled setup, both result tables, the task-size hypothesis, limitations,
and the replication protocol.

For Viblo or another Vietnamese developer publication, start from the complete
[Vietnamese edition](articles/do-codex-skills-save-tokens.vi.md). Keep the
measurements, disclosure, limitations, and canonical-English link intact.

Publish the useful explanation in the destination itself. Do not turn it into
an empty teaser that requires a GitHub click. Update only channel-specific
frontmatter, the cover-image URL, and the public interactive-benchmark link;
keep the measurements and limitations unchanged.

## Calls to action

Choose one primary action per post:

- **Try:** complete the five-minute playground.
- **Critique:** open an issue with one reproducible gap.
- **Measure:** contribute anonymized three-way ablation results.
- **Adapt:** create a tested stack, team, translation, or benchmark edition.
- **Follow:** star the project only if it is useful and worth revisiting.

## Distribution tracker

Record data after 24 hours, 7 days, and 30 days:

| Date | Channel | Post URL | Format | Views | Repo visits | Stars | Forks | Issues/PRs | Demo completions | Notes |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| YYYY-MM-DD | Example | URL | Demo | 0 | 0 | 0 | 0 | 0 | 0 | Audience questions |
| 2026-07-31 | GitHub Traffic | [Repository](https://github.com/Phelan164/codex-howto) | 14-day baseline | 39 | 2 | 1 | 0 | — | — | 23 clones from 17 unique cloners; GitHub was the only reported referrer |
| 2026-07-31 | GitHub Releases | [v0.3.0](https://github.com/Phelan164/codex-howto/releases/tag/v0.3.0) | Release | — | — | 1 | 0 | 0 | — | Living Wiki and model-adaptive skills released from validated `main` |
| 2026-07-31 | skills.sh | [Codex How To catalog](https://skills.sh/phelan164/codex-howto) | Skill registry | 0 installs | — | 1 | 0 | — | 1 smoke install | `engineering-loop` and `maintain-codex-wiki` indexed; CLI detected all 9 skills |
| 2026-07-31 | OpenAI Codex GitHub Discussions | [Discussion #36262](https://github.com/openai/codex/discussions/36262) and [benchmark update](https://github.com/openai/codex/discussions/36262#discussioncomment-17850277) | Show and tell | — | — | 1 | 0 | 0 | — | Existing post updated with the verified skills.sh install path |
| 2026-07-31 | Awesome Codex CLI | [PR #172](https://github.com/RoggeOhta/awesome-codex-cli/pull/172) | Directory PR | — | — | 1 | 0 | 1 | — | Existing PR updated with the verified skills.sh install path |
| 2026-07-31 | Awesome Codex Skills | [PR #198](https://github.com/composio-community/awesome-codex-skills/pull/198) | Skill directory PR | — | — | 1 | 0 | 1 | — | Open and mergeable; canonical `engineering-loop` catalog link verified |
| 2026-07-31 | Awesome Codex Guide | [PR #3](https://github.com/geekjourneyx/awesome-codex-guide/pull/3) | Resource directory PR | — | — | 1 | 0 | 1 | — | English and Chinese discovery metadata plus the install path; one scope-check follow-up posted on 2026-08-11 after eleven days without maintainer response |
| 2026-07-31 | GitHub contributors | [Issue #8](https://github.com/Phelan164/codex-howto/issues/8) | Community benchmark | — | — | 1 | 0 | 1 | — | Invites sanitized three-way measurements and reproducible forks |
| 2026-08-01 | GitHub Releases | [v0.5.0](https://github.com/Phelan164/codex-howto/releases/tag/v0.5.0) | Release | — | — | 1 | 0 | 0 | — | Six GPT-5.6-sol runs, 2048 benchmark, plugin distribution, and replication request |
| 2026-08-02 | GitHub Traffic | [Repository](https://github.com/Phelan164/codex-howto) | 14-day baseline | 114 | 11 | 1 | 0 | — | — | 223 clones from 104 unique cloners; likely includes automated registry and scanner traffic |
| 2026-08-02 | SkillStore | [Engineering Loop](https://skillstore.io/skills/phelan164-engineering-loop) | Independent audit | 0 | — | 1 | 0 | — | 3 downloads | Approved, audit complete, signed artifact available, quality score 75 |
| 2026-08-02 | HOL Codex Plugin Marketplace | [PR #341](https://github.com/hashgraph-online/awesome-codex-plugins/pull/341) | Plugin marketplace PR | — | — | 1 | 0 | 1 | — | One alphabetized Development & Workflow entry; source scanner CI passes the required ≥80/no-high gate |
| 2026-08-11 | GitHub Traffic | [Repository](https://github.com/Phelan164/codex-howto) | Pre-orchestration-update baseline | — | — | 2 | 1 | 4 open | — | Public GitHub API baseline immediately before distribution; target remains 1,000 stars and 200 forks |
| 2026-08-11 | OpenAI Codex GitHub Discussions | [Orchestration benchmark update](https://github.com/openai/codex/discussions/36262#discussioncomment-17970755) | Technical replication request | — | — | 2 | 1 | [PR #36](https://github.com/Phelan164/codex-howto/pull/36) | — | Existing Show-and-tell updated without duplicating a new post; asks for evaluator critique and paired replications, not votes |
| 2026-08-11 | Everything Claude Code | [PR #2761](https://github.com/affaan-m/ECC/pull/2761) | Native evaluator contribution | — | — | 2 | 1 | 1 upstream PR | — | Adds an orchestration-efficiency evidence scenario with pinned attribution; contribution-first discovery rather than a directory listing or vote request |
| 2026-08-11 | Matt Pocock Skills | [Issue #826 response](https://github.com/mattpocock/skills/issues/826#issuecomment-5248892813) | Technical support and measurement guidance | — | — | 2 | 1 | 1 community response | — | Diagnoses a reported 1.5M-token fan-out, distinguishes current `/to-tickets` behavior from orchestration-layer expansion, and links the bounded smoke receipt with an explicit no-efficiency-claim caveat |
| 2026-08-11 | GitHub Traffic | [Repository](https://github.com/Phelan164/codex-howto) | Pre-Show-HN 14-day baseline | 328 | 65 unique | 2 | 1 | 4 open | — | 487 clones from 174 unique cloners; top unique referrers were GitHub 30, the benchmark site 16, OpenAI Community 7, Google 2, and ChatGPT 1; no HN referrer yet |
| 2026-08-11 | Hacker News | [Show HN item 49253301](https://news.ycombinator.com/item?id=49253301) | Interactive mixed benchmark and replication request | 1 initial point; flagged | — | 2 | 1 | — | — | The submission was immediately flagged and is not counted as a successful distribution result; do not delete and repost, solicit votes, or infer the flag's cause without moderator evidence |

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
