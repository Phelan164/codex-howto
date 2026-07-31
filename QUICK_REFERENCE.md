# Quick Reference

## Prompt contract

```text
Goal:
Context:
Constraints:
Done when:
```

## Where instructions belong

| Need | Surface |
|---|---|
| Only for this task | Prompt |
| Durable repository convention | `AGENTS.md` |
| Repeatable workflow | Skill |
| Specialized delegated role | Custom agent |
| Live external data or action | MCP/app connector |
| Mechanical lifecycle enforcement | Hook |
| Distributable bundle | Plugin |
| Scheduled or unattended task | Automation |

## Before editing

- Start without a skill for a new task class.
- Invoke `$engineering-loop` only when its complete lifecycle changes a
  measured result.
- Confirm the repository and active branch.
- Inspect applicable `AGENTS.md` files.
- Check the working tree for user changes.
- Find the commands that define “done.”
- Decide whether planning is necessary.

When evaluating a reusable skill, compare no-skill, previous full-skill, and
current lean-skill runs with the same model and reasoning effort.

## Before delegating

- Invoke `$orchestrate-engineering` explicitly for a complex task with
  independent workstreams.
- Is the task genuinely independent?
- Does the worker have a bounded input and output?
- Can it stay read-only?
- Will its summary be smaller than its working context?
- Could simultaneous edits conflict?

## Before accepting a result

- Inspect the diff.
- Run focused tests first.
- Run repository-required checks.
- Review failure paths and rollback.
- Confirm no secrets or generated artifacts were added.
- Ask for remaining assumptions and unverified claims.

## Useful commands

```text
/init          Create a starter AGENTS.md
/plan          Enter planning mode
/review        Review a branch, commit, or working tree
/permissions   Inspect or change the current permission mode
/agent         Inspect agent threads in the CLI
```

Commands and availability can change. Verify them in the [official CLI documentation](https://developers.openai.com/codex/cli).
