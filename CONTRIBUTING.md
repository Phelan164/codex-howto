# Contributing

Thank you for improving Codex How To.

## Before you start

- Search existing issues and pull requests for overlapping work.
- Keep changes focused on one learning outcome or reusable workflow.
- Open an issue first for major curriculum changes or new product surfaces.
- Never include private repository content, credentials, or production data.

## Ways to contribute

- Fix an unclear instruction, broken example, or outdated official source.
- Add one missing engineering case with a runnable exercise and verification.
- Report sanitized workflow evidence, including negative or inconclusive
  results.
- Adapt a focused stack or translation edition in a fork, then contribute
  generally useful improvements upstream.

Large stack-specific or organization-specific variants usually belong in a
fork. Keep the upstream guide focused on reusable engineering decisions.

## Local validation

The repository validator uses only the Python standard library:

```bash
python3 scripts/validate_repo.py
python3 -m unittest discover \
  -s labs/engineering-playground/backend \
  -p "test_*.py"
python3 -m unittest discover \
  -s scripts/tests \
  -p "test_*.py"
python3 scripts/summarize_engineering_loop.py \
  examples/measurements/engineering-loop-runs.csv
python3 -m compileall -q scripts labs/engineering-playground/backend
```

For a changed skill, also run the official `quick_validate.py` bundled with the
Codex skill creator.

## Content standard

Every tutorial contribution must include:

1. a concrete learner outcome;
2. prerequisites;
3. an exercise that avoids production credentials and destructive actions;
4. a verification step;
5. links to authoritative sources for product behavior;
6. a “last verified” date for version-sensitive claims.

Prefer runnable examples over broad advice. Label community conventions as opinions rather than product guarantees.

## Skill standard

Each skill must:

- use a lowercase, hyphenated folder name;
- contain `SKILL.md` with only `name` and `description` in frontmatter;
- use an imperative workflow;
- define workflow boundaries and observable output;
- keep detailed variants in one-level-deep `references/`;
- avoid embedded secrets, credentials, or destructive defaults;
- pass the repository validator and the official skill validator.
- demonstrate a measured workflow, safety, domain-knowledge, output-contract,
  or deterministic-tool advantage over a no-skill baseline.

Do not add a README inside a skill folder.

## Pull request checklist

- [ ] Product claims are linked to official documentation.
- [ ] Examples are safe to copy into a test repository.
- [ ] New links are relative where possible.
- [ ] `python3 scripts/validate_repo.py` passes.
- [ ] Playground and measurement tests pass.
- [ ] Changed skills pass `quick_validate.py`.
- [ ] The change is described in plain language.
- [ ] The final diff contains no generated caches or unrelated edits.

## Style

- Use short paragraphs and descriptive headings.
- Explain why a workflow exists before showing configuration.
- Separate stable principles from version-sensitive commands.
- Use “Codex can” only when supported by official documentation.
- Avoid unverified productivity multipliers.

By contributing, you agree that your contribution is licensed under this
repository's [MIT License](LICENSE).
