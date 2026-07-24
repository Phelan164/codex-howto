# 11 · Automation, plugins, and hooks

## Outcome

Promote stable workflows into enforceable or distributable Codex extensions.

## Promotion path

```text
prompt → AGENTS.md → skill → plugin → automation
                    ↘ hook for mechanical enforcement
```

Use:

- a **skill** for the reusable procedure;
- a **plugin** to distribute skills and optionally bundle hooks, apps, or MCP configuration;
- a **hook** for deterministic lifecycle checks;
- an **automation** for stable recurring or unattended work;
- `codex exec` for non-interactive CI or scripting.

## When a workflow is automation-ready

- Inputs and outputs are explicit.
- Failure behavior is understood.
- Permissions are bounded.
- The workflow succeeds repeatedly in interactive use.
- Verification is machine-observable.
- A human review point exists for consequential writes.

## Hooks

Hooks should enforce a narrow mechanical invariant, such as running a formatter or rejecting a prohibited file pattern. Keep hook scripts deterministic, fast, and safe to rerun.

Do not hide a complex agent workflow inside a hook. Do not execute untrusted text as shell code.

## Plugins

A plugin has a required `.codex-plugin/plugin.json` and can include skills, hooks, an MCP-backed app, configuration, and assets. Build a plugin when a workflow is stable enough to share beyond one repository.

## CI pattern

1. Start with a read-only analysis.
2. Use a dedicated least-privilege token.
3. Set an explicit timeout or budget.
4. Emit reviewable output.
5. Fail closed when new approval would be required.
6. Keep merge or deployment decisions under repository policy.

## Lab A: package and install a local plugin

The repository includes a minimal marketplace and plugin:

```text
examples/plugin-marketplace/
├── .agents/plugins/marketplace.json
└── plugins/engineering-review/
    ├── .codex-plugin/plugin.json
    └── skills/evidence-review/SKILL.md
```

From the repository root:

```bash
codex plugin marketplace add ./examples/plugin-marketplace
codex plugin marketplace list
codex plugin list --marketplace codex-howto-lab --available --json
codex plugin add engineering-review@codex-howto-lab
```

Start a new task and invoke `$evidence-review` on a small local diff. Then remove the lab installation:

```bash
codex plugin remove engineering-review@codex-howto-lab
codex plugin marketplace remove codex-howto-lab
```

Inspect the manifest before installation. A real plugin needs stable versioning, publisher metadata, tests, and an upgrade policy before distribution.

## Lab B: configure and trust a hook

Work in a disposable clone with no existing `.codex/hooks.json`. Copy the bundled validation hook:

```bash
mkdir -p .codex
cp examples/hooks/validate-on-stop/hooks.json .codex/hooks.json
```

Start Codex, open `/hooks`, inspect the exact command and source, and trust it only after confirming that it runs this repository’s read-only `scripts/validate_repo.py`. Complete a documentation-only task and verify that the Stop hook reports validation.

Change one harmless character in the copied hook, restart Codex, and confirm the changed hash requires review again. Restore or remove the copied hook after the lab. Never overwrite or merge an existing hook configuration without reviewing every handler.

## Lab C: schedule a read-only automation

Run [the documentation-drift prompt](../../examples/prompts/scheduled-docs-drift.md) manually first. In the Codex app, create a temporary recurring automation with that prompt and repository, using a short test schedule.

Inspect the first run:

- it remains read-only;
- every reported drift item has a local location and official source;
- unavailable documentation is reported rather than guessed;
- “no verified drift” is concise.

Disable or delete the temporary automation after the test. Add write actions only after repeated read-only runs are reliable and a human approval point is defined.

## Lab D: non-interactive CI

Turn one manual review checklist into:

1. a skill invoked explicitly in local Codex;
2. a read-only `codex exec` check in a test branch;
3. a documented rollback that removes the CI step.

Do not add automatic fixes until the read-only results are reliable.

## Verify

- The workflow fails safely without credentials.
- CI cannot modify production or protected branches.
- The local plugin installs, invokes, and removes cleanly.
- The hook command and trust hash are inspected before execution.
- The scheduled task is proven read-only and removed after the lab.
- Hook, plugin, automation, and CI removal are documented and reversible.
- Human reviewers can inspect the produced evidence.

## Official sources

- [Build plugins](https://developers.openai.com/codex/plugins/build)
- [Hooks](https://developers.openai.com/codex/hooks)
- [Automations](https://developers.openai.com/codex/app/automations)
- [Non-interactive mode](https://developers.openai.com/codex/noninteractive)

Last verified: 2026-07-24.
