# Distribution Shortlist

This shortlist favors communities where Codex How To answers an existing
developer need and where project sharing is explicitly supported. Policies and
activity were checked on 2026-07-31; recheck them immediately before posting.

## Priority 1: exact audience fit

### skills.sh — open agent skills ecosystem

- **Destination:** [Codex How To catalog](https://skills.sh/phelan164/codex-howto)
- **Why it fits:** developers can inspect and install the repository's skills
  directly into Codex through the public `npx skills` workflow.
- **Verified:** the CLI detects all nine skills; `engineering-loop` and
  `maintain-codex-wiki` have canonical catalog pages and passed an isolated
  Codex installation smoke test.
- **Install:** `npx skills add Phelan164/codex-howto --skill engineering-loop
  -g -a codex -y`
- **Measure:** catalog installs, repository referrals, and whether installers
  complete the playground or provide benchmark evidence.

### OpenAI Codex GitHub Discussions — Show and tell

- **Destination:** [Show and tell](https://github.com/openai/codex/discussions/categories/show-and-tell)
- **Why it fits:** the official Codex community explicitly routes Codex-related
  projects to this category.
- **Share:** the runnable playground, the engineering-loop contract, and one
  measured result.
- **Ask:** which verification step or specialist skill is missing?
- **Timing:** first public submission after `v0.2.0` is released.

Suggested title:

```text
Codex How To: engineering loops and a review-first living wiki
```

Suggested opening:

```text
I built an independent, engineering-first Codex curriculum around one claim:
generated code is an intermediate result. The included playground takes a task
through scope, reproduction, implementation, tests, diff review, and an
evidence-based handoff. I would value feedback from people who run the
five-minute exercise, especially where the loop adds overhead or misses a
real engineering check.
```

### OpenAI Developer Community — Codex

- **Destination:** [Codex category](https://community.openai.com/c/codex/24)
- **Why it fits:** developers already share Codex projects, case studies, and
  agent workflows there.
- **Share:** a short case study, not a bare repository link.
- **Ask:** invite playground attempts and sanitized workflow evidence.
- **Timing:** two or three days after the GitHub Show and tell post; answer
  every substantive question.

### Awesome Codex CLI

- **Destination:** [RoggeOhta/awesome-codex-cli](https://github.com/RoggeOhta/awesome-codex-cli)
- **Rules:** its
  [contribution guide](https://github.com/RoggeOhta/awesome-codex-cli/blob/main/CONTRIBUTING.md)
  accepts Codex-specific, actively maintained resources with a clear
  value-oriented description and star badge.
- **Why it fits:** the list has dedicated tutorials, skills, plugins, and
  community sections.
- **Share:** submit one entry under **Tutorials & Articles** after the release;
  do not request several entries for the same repository.

Proposed entry:

```markdown
- [Codex How To](https://github.com/Phelan164/codex-howto) — Engineering-first Codex curriculum with 14 modules, 9 installable skills, a review-first living wiki, a runnable playground, and measured workflow experiments. ![GitHub stars](https://img.shields.io/github/stars/Phelan164/codex-howto?style=flat-square)
```

### Awesome Codex Skills

- **Destination:** [composio-community/awesome-codex-skills](https://github.com/composio-community/awesome-codex-skills)
- **Rules:** the project welcomes real reusable skills with precise trigger
  descriptions, scripts, and references.
- **Why it fits:** `engineering-loop` is a concrete lifecycle skill rather than
  a generic prompt collection.
- **Share:** propose only `skills/engineering-loop`, with its loop contract and
  hard-debugging reference. Do not copy the full skill catalog into the list.
- **Gate:** complete—the released skill passes the official validator and an
  isolated `npx skills` Codex installation.

### HOL Codex Plugin Marketplace

- **Destination:** [hashgraph-online/awesome-codex-plugins](https://github.com/hashgraph-online/awesome-codex-plugins)
- **Rules:** submit one repository-root README entry, sorted alphabetically,
  after the source plugin passes the required HOL scanner workflow.
- **Why it fits:** the marketplace mirrors installable plugin bundles instead
  of treating the project as a generic reading list.
- **Verified:** the repository has a valid manifest and icon, `SECURITY.md`,
  an MIT license, and a passing SHA-pinned scanner workflow configured with
  `min_score: 80` and `fail_on_severity: high`.
- **Submission:** [PR #341](https://github.com/hashgraph-online/awesome-codex-plugins/pull/341)
  adds one entry under **Development & Workflow**.

### SkillStore

- **Destination:** [Engineering Loop](https://skillstore.io/skills/phelan164-engineering-loop)
  and [Maintain Codex Wiki](https://skillstore.io/skills/phelan164-maintain-codex-wiki).
- **Why it fits:** the pages provide independent discovery, security status,
  quality scoring, and install/download signals for the flagship skills.
- **Status:** both skills are already listed; do not submit duplicate forms.
- **Measure:** page views, downloads, favorites, and whether audit visibility
  improves repository conversion.

## Priority 2: rule-approved discovery

### r/ChatGPTCoding self-promotion thread

- **Destination:** use the newest recurring **Self Promotion Thread** in
  [r/ChatGPTCoding](https://www.reddit.com/r/ChatGPTCoding/).
- **Current rule pattern:** promote a project only once; use the designated
  thread. Low-karma accounts may be removed automatically.
- **Angle:** a disciplined alternative to one-shot AI coding, with the
  dependency-free demo.
- **Avoid:** a separate promotional post or repeated comments in later threads.

Suggested comment:

```text
Disclosure: I maintain this project.

I built Codex How To because generated code kept being treated as the finish
line. The repository packages a stricter loop—scope, reproduce, implement,
test, review, and evidence—into 9 installable skills, a review-first living
wiki, and a dependency-free playground with no-skill/full-skill/lean-skill
comparison.

I am looking for critical feedback from people who run the five-minute demo:
which step catches a real problem, and which step adds overhead without value?

https://github.com/Phelan164/codex-howto
```

### r/devops weekly self-promotion thread

- **Destination:** use the newest
  [r/devops weekly self-promotion thread](https://www.reddit.com/r/devops/search/?q=%22Weekly%20Self%20Promotion%20Thread%22&restrict_sr=1&sort=new).
- **Current rule pattern:** projects and repositories are welcome inside the
  weekly thread.
- **Angle:** safe authority boundaries, preview-before-apply behavior,
  rollback-aware validation, and the `operate-devops` skill.
- **Ask:** where platform engineers require human approval in an agent loop.

### r/github self-promotion megathread

- **Destination:** the
  [project-promotion megathread](https://www.reddit.com/r/github/comments/1jy8rea/promote_your_projects_here_selfpromotion/).
- **Current rule pattern:** include a short description, repository link,
  main features, and context for involvement.
- **Angle:** a forkable open-source curriculum with clear stack, translation,
  and measurement contribution paths.
- **Expected value:** contributor discovery rather than deep Codex feedback.

## Priority 3: durable technical content

### DEV Community

- **Destination:** [DEV Community](https://dev.to/)
- **Format:** publish the complete technical article, not a teaser whose only
  purpose is an outbound click.
- **Angle:** “Code generation is an intermediate result: building a measurable
  engineering loop for Codex.”
- **Tags:** use four accurate tags such as `codex`, `ai`, `testing`, and
  `softwareengineering`.
- **Why:** existing Codex and skills articles show an active audience, while
  DEV moderation favors information over promotion.

### Viblo

- **Destination:** [Viblo](https://viblo.asia/)
- **Format:** a Vietnamese technical article with the runnable example and
  limitations included in the article.
- **Why it fits:** Viblo explicitly supports development, infrastructure, QA,
  and project-management knowledge in Vietnamese, English, and Japanese.
- **Angle:** `Từ code generation đến engineering evidence với OpenAI Codex`.
- **Avoid:** a short announcement or repository-only post; Viblo flags thin or
  spam-like content.

### daily.dev

- **Destination:** [daily.dev](https://daily.dev/)
- **Format:** distribute the substantive DEV or personal-blog article through
  an appropriate public Squad or publication source.
- **Why:** daily.dev is suited to developer articles, not a naked repository
  submission.
- **Timing:** after the article has demonstrated useful reading and discussion.

## Conditional opportunities

### Show HN

[Show HN rules](https://news.ycombinator.com/showhn.html) require something
people can try and identify lists or pure reading material as off-topic. Codex
How To is eligible only if the post leads with the runnable playground and
installable skills—not merely the curriculum.

Use it after several clean-checkout demo runs prove that a stranger can try the
project without signup. Never ask friends for upvotes or coordinated comments.

### console.dev

[console.dev](https://console.dev/selection-criteria) reviews developer tools
that are self-service, high-quality, maintained, documented, and part of a
regular development workflow. The guide alone is a weak fit; the installable
plugin and skills may qualify after a stable release and real usage evidence.

If those gates are met, email `hello@console.dev` with a concise description,
demo instructions, release link, and maintenance evidence. Do not purchase a
sponsorship as a substitute for product fit.

## Do not prioritize yet

- **Product Hunt:** the current artifact is primarily a curriculum and workflow
  package, not a polished standalone product launch.
- **Generic startup directories:** their visitors are less likely to run Codex
  engineering workflows or maintain useful forks.
- **Unmoderated Facebook-group cross-posting:** use one group only when its
  rules and audience are known; ask a moderator when unclear.
- **Paid stars, follow exchanges, or vote groups:** these create misleading
  metrics and can violate platform rules without producing users.

## Recommended order

1. Keep the `v0.6.0` release, skills.sh catalog, and SkillStore audit pages
   healthy.
2. Answer feedback on the existing OpenAI Codex Show and tell.
3. Maintain the pending Awesome Codex CLI, Awesome Codex Skills, and HOL
   marketplace submissions without duplicating them.
4. Share the mixed benchmark result once in a current rule-approved promotion
   thread.
5. Publish the complete measurement article on DEV; adapt it into Vietnamese
   for Viblo.
6. Invite independent benchmark runs and maintained fork editions.
7. Use r/devops only with the platform-safety angle.
8. Reconsider Show HN only after there is a hosted, directly usable tool.

Record each result in the
[distribution tracker](community-launch-kit.md#distribution-tracker) after 24
hours, 7 days, and 30 days.
