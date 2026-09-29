# Experimental JEV Router pilot

Goal: finish coding tasks faster with less wasted usage, without lowering the
acceptance bar. This is an **opt-in community integration**, not a required
dependency, an official OpenAI feature, or a demonstrated efficiency win.

Source review: 2026-09-29, JEV Router version `0.3.0`, commit
[`38da6b84ea01241bfc41fbddc0928d0f40a703f0`](https://github.com/gargpratyush/jev-router/tree/38da6b84ea01241bfc41fbddc0928d0f40a703f0).
No live routed coding experiment has been run for this guide. Pin and recheck
the implementation before use; upstream and Codex compatibility can change.

## Choose the right layer

| Option | What chooses the model | Scope | Tradeoff |
| --- | --- | --- | --- |
| Native model selection | Developer or native agent configuration | Main session or configured subagents | No extra routing service |
| [Our routing hook](../examples/hooks/model-routing/README.md) | Agent-supplied tier plus local policy | Eligible subagent spawns | Does not switch the main app model |
| JEV `jev-codex` | External classifier plus proxy policy | Fresh user turns through its CLI wrapper | Prompt sharing, network delay, proxy compatibility |

JEV is not a general skill selector. Its bundled explanation skill displays
the routing decision; engineering-loop still owns implementation and verification.
Do not combine JEV and our subagent hook in the first experiment: isolate the
effect of one router before introducing interacting policies.

Native configuration reference: [OpenAI subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents).
The JEV launcher starts the Codex **CLI**, not the desktop app. Starting the app
normally does not activate this wrapper. Desktop integration is unverified.

## What the inspected code does

- Starts a loopback proxy and launches the installed Codex CLI with a temporary
  custom Responses provider; forwards authentication headers to upstream.
- Sends the extracted current user prompt, current model, approximate context
  size, and available model IDs to TypeSafe's System One service.
- Selects a model for a fresh user turn; keeps tool continuations pinned.
- Passes concrete model selections through instead of routing them.
- Uses confidence and context-size rules to limit switching; routing-service
  failure normally keeps the current model. This does not guarantee recovery
  from every proxy, protocol, or provider failure.
- Preserves supported reasoning effort; replaces unsupported effort with the
  catalog default. This is not our explicit model-plus-effort tier policy.

The classifier does not receive the complete conversation in its routing
request. Test follow-ups such as “implement that plan” and “yes, continue”:
their difficulty may depend on context absent from the classifier.

Sources: [router request](https://github.com/gargpratyush/jev-router/blob/38da6b84ea01241bfc41fbddc0928d0f40a703f0/src/router.mjs),
[Codex proxy](https://github.com/gargpratyush/jev-router/blob/38da6b84ea01241bfc41fbddc0928d0f40a703f0/src/codex-proxy.mjs),
[policy](https://github.com/gargpratyush/jev-router/blob/38da6b84ea01241bfc41fbddc0928d0f40a703f0/src/policy.mjs),
[launcher](https://github.com/gargpratyush/jev-router/blob/38da6b84ea01241bfc41fbddc0928d0f40a703f0/src/codex-cli.mjs).

## Privacy and compatibility gate

Before enabling it:

1. Approve TypeSafe as a recipient of the pilot prompts. Use public or synthetic
   tasks only; do not submit proprietary code, credentials, or customer data.
   Review the service's current retention, pricing, and account terms separately.
2. Treat the proxy and its SDK as trusted software: they handle request bodies
   and forwarded authentication headers. This source inspection is not a full
   security audit or an endorsement of the service.
3. Leave `JEV_DEBUG` and `JEV_DUMP` unset. Normal routing already retains up to
   20 prompt-bearing exchanges per CLI session in temporary files. Upstream
   uses restrictive Unix permissions and stale-file cleanup, not encryption;
   full request dumps have separate handling and should remain disabled.
4. Note that startup installs/overwrites an explanation skill at
   `~/.agents/skills/jev-router-explain/SKILL.md`. Preserve any existing custom
   file first. Exiting the wrapper does not uninstall this skill.
5. Verify the exact CLI version, account model catalog, reasoning levels,
   authentication path, tool execution, and permissions on a disposable task.
   The launcher disables WebSockets; enterprise-specific backend origins are
   a documented compatibility limitation. Do not assume native-path latency parity.

Sources: [status storage](https://github.com/gargpratyush/jev-router/blob/38da6b84ea01241bfc41fbddc0928d0f40a703f0/src/status.mjs),
[launcher](https://github.com/gargpratyush/jev-router/blob/38da6b84ea01241bfc41fbddc0928d0f40a703f0/src/codex-cli.mjs),
[upstream compatibility notes](https://github.com/gargpratyush/jev-router/blob/38da6b84ea01241bfc41fbddc0928d0f40a703f0/README.md#compatibility-notes).

## Optional setup, after that gate

Prefer a disposable environment with Node.js 20.12+ and an already authenticated
Codex CLI. Inspect the pinned source and dependency lock before installation.
Do not install globally or modify the user's normal Codex configuration for
this pilot.

```bash
git clone https://github.com/gargpratyush/jev-router.git jev-router-pilot
cd jev-router-pilot
git checkout --detach 38da6b84ea01241bfc41fbddc0928d0f40a703f0
npm ci --ignore-scripts
npm test
```

Provision `JEV_API_KEY` through your secret manager or a protected local
environment, outside the repository. Never paste the key into a task, receipt,
shell command history, or PR. Launch from the disposable target project:

```bash
node /absolute/path/to/jev-router-pilot/bin/jev-codex.mjs
```

The absolute path above is a placeholder; replace it with your checkout path.
Inspect the native catalog and recorded selected model before trusting a run.
The inspected defaults include older GPT-5.6 models. `JEV_CODEX_FAST_MODEL`,
`JEV_CODEX_BALANCED_MODEL`, `JEV_CODEX_STRONG_MODEL`, and `JEV_CODEX_LONG_MODEL`
configure fallback mappings, but the fetched catalog can supply other exact
models: these variables are **not a strict allowlist**. Astra maps to the
opt-in long tier by default, controlled by `JEV_ALLOW_FABLE`. Do not enable it
without an explicit usage budget. Do not claim our Sol-medium/Astra-low/high
policy is enforced by this setup.

Select a concrete model to pause routing. To return to the ordinary execution
path, exit the wrapper and launch plain `codex`; no permanent provider edit is
required by the inspected launcher. Handle retained prompt files and the
installed explanation skill separately under your local retention policy.

## Quality-first experiment

Use the controls in our [measurement protocol](engineering-loop-measurement.md),
but keep this **routing experiment separate from the published skill ablation**.
Freeze skills, tools, permissions, task prompts, acceptance checks, and starting
commit; only model-routing policy varies. Record the intended effort and the
actual model/effort for every turn where surfaced.

Compare three arms on fresh copies:

1. Native CLI with a fixed everyday model and effort.
2. Native CLI with a fixed stronger model and effort.
3. JEV CLI with the same skills and a recorded routing configuration.

Use at least three task classes, repeating each arm and rotating run order:
bounded bug fix with a regression; new small app/game with interaction checks;
and a multi-step change containing context-dependent follow-ups. Use the same
predefined follow-ups across arms. Do not transfer discoveries between runs.

Before spending usage, set per-run elapsed-time and usage budgets plus a
stop condition for router/protocol failures. Agree the acceptable quality
threshold and minimum worthwhile speed/cost improvement in advance. Keep
failed, stopped, and abandoned runs in the denominator.

Record one sanitized receipt per run:

```text
Task, variant, repeat, starting commit:
Codex version; JEV commit; skill revision:
Configured policy; actual models and efforts; switches:
Accepted; defects; human corrections; check evidence:
Total elapsed time; time to first useful output:
Routing latency and fallback count, if observable:
Input/cached/output/reasoning tokens, where separately surfaced:
Provider cost or subscription credits; TypeSafe charges, if available:
Reviewer usage; retries; human correction time:
Missing measurements; stop reason:
```

Do not double-count reasoning tokens if included in output usage. Do not equate
API-dollar estimates with subscription bills. Leave unavailable values unknown;
do not store raw prompt exchanges in public receipts. Compare acceptance and
defects first, then median/tail completion time and total usage per accepted
task, including unsuccessful attempts and router overhead.

A cheaper model can cost less while using more tokens. Routing adds a network
round trip and switching may affect cache reuse. Upstream timing comments are
not this repository's measurements. No benefit is established until a pilot
passes the quality gate and improves a predeclared efficiency metric.

Known pinned-version limitation: `test/live-routing.mjs` passes `available`,
but `askJev` requires `models` and returns early without it. Do not treat that
script as working end-to-end evidence. Resolve the mismatch in a reviewed
upstream revision or isolated pilot patch, recording the exact diff first.
Sources: [live smoke script](https://github.com/gargpratyush/jev-router/blob/38da6b84ea01241bfc41fbddc0928d0f40a703f0/test/live-routing.mjs),
[router](https://github.com/gargpratyush/jev-router/blob/38da6b84ea01241bfc41fbddc0928d0f40a703f0/src/router.mjs).

## Promotion decision

Keep this opt-in unless repeated representative runs retain quality and improve
total time or usage. Stop adoption for unacceptable prompt-sharing policy,
unverifiable model selection, protocol regressions, or excess corrections.
Only then evaluate combining it with subagent routing. Skill selection remains
a separate experiment; this recipe does not install a skill-selection router.
