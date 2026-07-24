# 12 · Troubleshooting

## Outcome

Diagnose Codex failures by layer instead of changing random settings.

## Diagnostic layers

### 1. Task

- Is the goal observable?
- Is important context missing?
- Are constraints contradictory?
- Does “done” name a command or behavior?

### 2. Repository

- Are you in the intended directory and branch?
- Are there uncommitted user changes?
- Which `AGENTS.md` files apply?
- Are dependencies and tool versions available?

### 3. Permission boundary

- Did the sandbox block a path, command, or network request?
- Is approval interactive in this surface?
- Can the task succeed with narrower access?

### 4. Extension

- Is the skill in a discovered location?
- Does its description match the request?
- Is the plugin installed and enabled?
- Is the MCP server configured and authenticated?
- Does a restart or new session load the change?

### 5. External system

- Is the credential valid and least-privileged?
- Is the service available?
- Did an API or CLI version change?
- Is a proxy or organization policy blocking access?

### 6. Codex defect

Capture:

- Codex version and surface;
- operating system;
- minimal reproduction;
- expected and actual behavior;
- sanitized logs;
- relevant configuration without secrets.

Then search or report against [openai/codex](https://github.com/openai/codex).

## Stop conditions

Stop retrying when:

- the same permission request is denied repeatedly;
- the task requires credentials you do not have;
- the target is ambiguous or destructive;
- product documentation does not establish a claimed capability;
- external state must change before progress is possible.

## Exercise

Temporarily move a test skill out of `.agents/skills`, observe that it is unavailable, then restore it and confirm discovery. Do not change global configuration.

## Verify

- You identified the failing layer.
- The fix is narrower than “give full access.”
- Logs contain no secrets.
- The final note records cause, resolution, and prevention.

## Official sources

- [Configuration](https://developers.openai.com/codex/config-basic)
- [Security](https://developers.openai.com/codex/security)
- [Official Codex repository](https://github.com/openai/codex)

Last verified: 2026-07-24.
