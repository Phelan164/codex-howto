# Scheduled documentation-drift check

Use this prompt only in a recurring Codex automation that has read access to the repository:

```text
Inspect README.md, CATALOG.md, modules/, and the current official Codex manual.

Goal:
Identify version-sensitive Codex claims or official links that are stale.

Constraints:
- Work read-only.
- Do not edit files, open issues, post messages, or install dependencies.
- Treat official OpenAI documentation as authoritative.
- Report only claims that can be verified or contradicted.

Done when:
- each finding cites the local file and official source;
- unchanged checks produce a short "no verified drift" result;
- unavailable sources are reported as unavailable, not guessed.
```

Run it manually once before scheduling it. Review the first scheduled result before deciding whether any write action should be added.
