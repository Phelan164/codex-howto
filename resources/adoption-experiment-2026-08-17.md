# Weekly adoption experiment: 2026-08-17 to 2026-08-23

## Question

Can clearer first-visit routing and one visible replication request turn
existing discovery into useful developer participation?

This is a one-week operational experiment, not evidence that README changes
cause stars, forks, or benchmark participation. GitHub traffic is aggregated,
rolling, and may include automated activity.

## Baseline

Captured from the GitHub API on 2026-08-17 in the repository owner's account:

| Signal | 14-day value |
|---|---:|
| Views | 287 |
| Unique viewers | 70 |
| Clones | 382 |
| Unique cloners | 123 |
| Stars | 2 |
| Forks | 1 |
| Subscribers | 0 |
| Open issues and pull requests | 3 |

The repository overview received 82 views from 55 unique visitors. The skills
directory received 12 views from 8 unique visitors. Leading referrers were
GitHub (56 views, 28 unique), the OpenAI Developer Community (53 views, 6
unique), and the hosted benchmark (50 views, 16 unique).

The clone-to-star difference indicates that discovery and cloning exist, but it
does not identify user intent or prove a conversion problem. Automated registry
and security-scanner activity may contribute to clone counts.

## Actions

1. Add a top-of-README decision table that routes developers to the minimum
   useful workflow: direct testing/review guidance, the engineering loop,
   bounded orchestration, or the Living Wiki.
2. Pin [issue #23](https://github.com/Phelan164/codex-howto/issues/23) and add a
   v0.6.0 replication recipe. Do not create a duplicate benchmark issue.
3. Send one maintainer-ready follow-up to the green
   [ECC contribution](https://github.com/affaan-m/ECC/pull/2761). Do not add
   promotional comments to unrelated issues.
4. Do not open more directory-listing pull requests this week. Existing
   submissions already cover the relevant catalogs.
5. Capture the same API snapshot on 2026-08-24 and record the result, including
   neutral or negative outcomes.

## Execution log

| Date | Action | Evidence |
|---|---|---|
| 2026-08-17 | Published the README routing and baseline as a draft change | [PR #39](https://github.com/Phelan164/codex-howto/pull/39); repository validation, wiki lint, and plugin scanning passed |
| 2026-08-17 | Pinned the existing replication request and added the v0.6.0 large-task recipe | [Issue #23 update](https://github.com/Phelan164/codex-howto/issues/23#issuecomment-5311881984) |
| 2026-08-17 | Sent one maintainer-ready status summary for the green ECC contribution | [ECC PR #2761 update](https://github.com/affaan-m/ECC/pull/2761#issuecomment-5311884726) |
| 2026-08-17 | Reviewed existing directory submissions | No new directory PR opened and no repeated follow-up posted |

## Decision criteria

Primary evidence is one independent benchmark replication, a substantive issue
or pull-request comment, or a maintained fork that contributes a tested edition.
Stars and forks are secondary discovery signals, not proof of engineering value.

Continue the routing experiment only if the week produces a meaningful action
or exposes a specific onboarding failure. Otherwise keep the clearer README,
stop additional promotion, and prioritize a fresh measured engineering task.

## Reproduction commands

```bash
gh api repos/Phelan164/codex-howto/traffic/views
gh api repos/Phelan164/codex-howto/traffic/clones
gh api repos/Phelan164/codex-howto/traffic/popular/referrers
gh api repos/Phelan164/codex-howto/traffic/popular/paths
gh api repos/Phelan164/codex-howto \
  --jq '{stars:.stargazers_count,forks:.forks_count,subscribers:.subscribers_count,open_issues:.open_issues_count}'
```
