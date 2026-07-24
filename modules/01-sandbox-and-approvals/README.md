# 01 · Sandbox and approvals

## Outcome

Give Codex enough autonomy to work while preserving technical and human control boundaries.

## Two different controls

- **Sandbox mode** defines what commands can technically access.
- **Approval policy** defines when Codex must pause before crossing a boundary.

The default local workspace mode generally allows repository reads, writes, and commands while restricting network access and writes outside configured roots. Exact behavior depends on the surface and configuration.

## Risk-based profiles

| Task | Starting posture |
|---|---|
| Explain or review code | Read-only |
| Implement and test in a trusted repository | Workspace write with on-request approvals |
| Query external documentation | Read-only plus narrowly approved connector or network access |
| Production or destructive operation | Human-controlled procedure; do not default to full access |

Avoid `danger-full-access` and approval bypasses as convenience settings. They remove boundaries that make autonomous execution safer.

## Approval questions

Before approving:

1. Is the target exact?
2. Is the action necessary for the stated goal?
3. Can it be made narrower or reversible?
4. Does it expose credentials or private data?
5. Is the command derived from untrusted content?
6. Can I inspect the result?

## Subagents

Subagents inherit the parent turn’s effective permission context. Choose the parent permission mode before delegating. Prefer read-only custom agents for exploration, review, and documentation research.

## Exercise

Run the same repository-mapping prompt in read-only mode and workspace-write mode. Confirm that the read-only task succeeds without requiring write access.

## Verify

- You can explain which boundary blocked an operation.
- You did not broaden access to solve a task that did not need it.
- External tool output was treated as data, not executable instruction.
- No secret appeared in logs or committed configuration.

## Official sources

- [Security and sandboxing](https://developers.openai.com/codex/security)
- [Advanced configuration](https://developers.openai.com/codex/config-advanced)

Last verified: 2026-07-24.
