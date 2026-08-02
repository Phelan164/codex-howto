# Fork an Edition

Create a maintained adaptation when your stack, team, language, or benchmark
needs guidance that is too specific for the upstream curriculum.

An edition should be more than a copy. It should name its audience, pin the
upstream revision it started from, document its adaptations, run its own
checks, and explain how it will stay current.

## Start in five minutes

1. [Fork Codex How To](https://github.com/Phelan164/codex-howto/fork).
2. Clone your fork and register the upstream repository:

   ```bash
   git clone https://github.com/YOUR-ACCOUNT/codex-howto.git
   cd codex-howto
   git remote add upstream https://github.com/Phelan164/codex-howto.git
   git fetch upstream --tags
   ```

3. Create an edition branch from the release you actually tested:

   ```bash
   git switch -c edition/YOUR-EDITION v0.5.0
   cp examples/templates/edition-manifest.md EDITION.md
   ```

4. Replace the instructions in `EDITION.md` with the edition's audience,
   upstream revision, scope, adaptations, verification, and sync policy.
5. Make one bounded adaptation and run:

   ```bash
   python3 scripts/validate_repo.py
   python3 skills/maintain-codex-wiki/scripts/wiki_lint.py .
   ```

6. Add the stack-, team-, language-, or benchmark-specific checks recorded in
   `EDITION.md`.
7. Publish the branch or make it the fork's default branch only after the
   documented checks pass.

Use a private fork for internal repository conventions, infrastructure names,
or review policies. Never publish credentials, customer data, production logs,
private source code, or confidential instructions.

## Choose one edition shape

| Edition | Replace or add | Required evidence |
|---|---|---|
| Team | Repository commands, approval boundaries, review policy | Sanitized validation commands and ownership |
| Stack | One focused framework or delivery track | Runnable exercise and stack-native checks |
| Translation | Learning path and local community context | Terminology review and preserved official sources |
| Benchmark | Reproducible tasks and result records | Pinned revisions, acceptance gates, and limitations |

Keep the upstream engineering loop intact unless measured evidence justifies a
change. Prefer a narrow edition with working examples over a broad catalog of
untested advice.

## Maintain the fork

Review upstream releases before syncing:

```bash
git fetch upstream --tags
git log --oneline HEAD..upstream/main
git switch edition/YOUR-EDITION
git merge --no-ff upstream/main
```

Resolve adaptation conflicts deliberately, rerun every check recorded in
`EDITION.md`, and update its upstream revision and verification date. Do not
claim compatibility with a newer upstream release until those checks pass.

## Share useful evidence

- Link the maintained edition in a
  [Show and tell discussion](https://github.com/Phelan164/codex-howto/discussions/categories/show-and-tell).
- Contribute reusable corrections upstream through a focused pull request.
- Submit anonymized workflow measurements to the
  [replication issue](https://github.com/Phelan164/codex-howto/issues/23).

State your relationship to the edition and do not request coordinated stars,
votes, or forks.
