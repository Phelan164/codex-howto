# 06 · MCP and tools

## Outcome

Connect Codex to external systems while keeping capability, trust, and permissions explicit.

## Use MCP for live external capability

MCP servers can provide:

- tools that perform actions;
- resources that expose readable context;
- reusable prompts.

Examples include documentation, issue trackers, source hosting, databases, design systems, and internal knowledge.

Do not paste large external manuals into `AGENTS.md`. Use a documentation MCP server when Codex needs current, queryable information.

## Tool selection

Prefer the narrowest source:

1. local repository files for codebase facts;
2. a purpose-built connector or MCP server for authorized private data;
3. official documentation for product and API behavior;
4. web search for public current information.

## Safety review

Before enabling an MCP server, answer:

- Who operates it?
- What data can it read?
- What actions can it perform?
- Which credentials does it receive?
- Are write and destructive tools accurately labeled?
- Can it start read-only?
- Is output treated as untrusted input?

Use least-privilege credentials and never commit tokens.

## Pair MCP with skills

MCP supplies capability; a skill supplies a repeatable procedure. A code-review skill might ask a GitHub connector for PR metadata, then inspect the local diff and return findings in a stable format.

## Add and inspect a server

The CLI manages configured servers with:

```bash
codex mcp list
codex mcp get <name>
codex mcp add <name> --url <streamable-http-url>
codex mcp remove <name>
```

For a local stdio server, put the executable and its arguments after `--`:

```bash
codex mcp add <name> -- <command> <args>
```

Use `codex mcp login <name>` and `codex mcp logout <name>` when a configured server uses supported OAuth. For bearer-token authentication, configure the environment-variable name with `--bearer-token-env-var`; do not put the token itself in committed configuration or shell history.

Use `~/.codex/config.toml` for personal servers. Put team-approved, repository-specific configuration in the trusted project’s `.codex/config.toml`, and document ownership and required authentication.

## Lab: official documentation server

This lab changes personal MCP configuration, then removes the change:

```bash
codex mcp add openaiDeveloperDocs --url https://developers.openai.com/mcp
codex mcp list
codex mcp get openaiDeveloperDocs
```

Start a new Codex task and ask:

```text
Use the OpenAI developer documentation source to verify where repo-scoped
skills are discovered. Return the official source and do not change files.
```

Inspect which MCP tool or resource was selected and confirm the response cites an official document. Then clean up:

```bash
codex mcp remove openaiDeveloperDocs
codex mcp list
```

If your organization already manages this server, do not replace its configuration; inspect the existing entry and perform only the read-only query.

For any other server, repeat the safety review before installation and start with a read-only query.

## Verify

- The server is configured in the expected scope.
- No credential was written to version control.
- The configured transport and authentication method are understood.
- Tool/resource selection is visible in the task evidence.
- The answer cites the authoritative document.
- The server can be removed cleanly.
- After removal, Codex reports that the source is unavailable rather than silently claiming it used the source.

## Official source

- [Model Context Protocol in Codex](https://developers.openai.com/codex/mcp)

Last verified: 2026-07-24.
