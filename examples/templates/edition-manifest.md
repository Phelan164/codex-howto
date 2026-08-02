# Edition Manifest

Replace the instructional text below before publishing an edition.

## Identity

- **Edition name:** Replace with a short, specific name.
- **Audience:** Replace with the developers or teams this edition serves.
- **Maintainer:** Replace with a GitHub account or team.
- **Status:** Choose `experimental`, `maintained`, or `archived`.
- **Upstream repository:** `https://github.com/Phelan164/codex-howto`
- **Upstream revision:** Replace with a release tag and immutable commit.
- **Last verified:** Replace with a `YYYY-MM-DD` date.

## Scope

Describe whether this is a team, stack, translation, or benchmark edition.
Name what the edition intentionally changes and what remains inherited from
upstream.

## Adaptations

| Area | Edition change | Evidence |
|---|---|---|
| Replace with a module, skill, example, or policy | Describe the bounded adaptation | Link a runnable check, exercise, or measurement |

## Verification

Record commands that a maintainer can run from a clean checkout:

```bash
python3 scripts/validate_repo.py
python3 skills/maintain-codex-wiki/scripts/wiki_lint.py .
```

Add edition-specific tests, builds, linters, type checks, or review gates.
Document any check that remains unverified and why.

## Safety and authority

Document sandbox expectations, approval boundaries, secret handling, and
operations that require a human decision. Keep private material in a private
fork.

## Upstream sync policy

State how often maintainers review upstream releases, who owns conflict
resolution, and which checks must pass before claiming compatibility with a
new upstream revision.

## Upstream contributions

List generally useful fixes proposed or contributed back to Codex How To.
