# 10 · Context and token efficiency

## Outcome

Spend context on decisions and evidence instead of repeated instructions, broad scans, and raw logs.

## First principle

Multi-agent work usually consumes more total tokens than a comparable single-agent run. Use it to reduce elapsed time, isolate noisy investigation, or improve specialist coverage—not as a token-saving shortcut.

## The context hierarchy

1. **Prompt:** current objective and constraints.
2. **`AGENTS.md`:** durable repository facts.
3. **Skill metadata:** compact workflow discovery.
4. **`SKILL.md`:** selected procedure.
5. **References:** optional detail loaded only when needed.
6. **Subagent thread:** isolated noisy work.
7. **Summary:** distilled evidence returned to the main thread.

Put information at the lowest-cost durable layer that still reaches the task.

## Efficiency techniques

### Route before reading

Provide entry points, failing commands, and likely owners. Ask Codex to follow call paths rather than scan every file.

### Use progressive disclosure

Keep skill bodies small. Put framework variants, checklists, and schemas in direct references.

### Prefer focused verification

Run the smallest reproducing test first, then required broader checks. Do not stream a full monorepo test log into the main thread when a worker can return the failing cases.

### Summarize with evidence

A useful worker summary contains:

- conclusion;
- file or command evidence;
- uncertainty;
- recommended next action.

### Compact at phase boundaries

After exploration or debugging, restate confirmed facts and discard superseded theories before implementation.

### Avoid repeated retries

When a command fails twice for the same reason, stop and diagnose the environment, permissions, or assumption instead of rerunning it blindly.

## Anti-patterns

- installing dozens of overlapping skills;
- copying framework manuals into `AGENTS.md`;
- asking every worker to read the entire repository;
- returning raw logs instead of conclusions;
- using high reasoning for mechanical edits;
- running parallel agents on one file;
- keeping obsolete requirements in the active thread.

## Exercise

Complete the [token-efficiency scorecard](../../resources/token-efficiency-scorecard.md) for one real task. Rewrite the prompt and routing instructions, then compare retries and context noise—not only raw token counts.

## Verify

- Main-thread context contains requirements, decisions, and results.
- Reusable instructions are not repeated in prompts.
- Each delegated result is smaller than its working context.
- Extra agents have a measurable reason to exist.

## Official sources

- [Codex best practices](https://developers.openai.com/codex/learn/best-practices)
- [Subagents](https://developers.openai.com/codex/subagents)

Last verified: 2026-07-24.
