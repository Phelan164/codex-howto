# Repository guidance

## Purpose

Maintain an accurate, engineering-first learning guide for OpenAI Codex.

## Editing rules

- Keep product behavior aligned with official OpenAI documentation.
- Label community practices and opinions clearly.
- Do not add credentials, destructive examples, or full-access defaults.
- Keep modules progressive: outcome, concepts, exercise, verification, sources.
- Keep skill bodies concise; put optional detail in direct `references/`.
- Preserve attribution to `luongnv89/claude-howto` as inspiration.

## Validation

Run:

```bash
python3 scripts/validate_repo.py
```

For each changed skill, also run:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py skills/<skill-name>
```

## Definition of done

- All relative Markdown links resolve.
- Every skill has valid frontmatter and UI metadata.
- Examples are safe and contain no placeholder secrets.
- Version-sensitive claims include an official source or verification note.
