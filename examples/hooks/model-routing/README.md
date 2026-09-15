# Experimental subagent model routing

Developer-configurable easy/medium/difficult tiers for **native Codex subagent
spawn calls**. The main agent classifies an already-authorized subtask; a
deterministic hook applies the model policy. No separate classifier model call.

This is a community example, not a built-in Codex setting or a guarantee that
every app task is routed. Installing the repository's skills/plugin does **not**
activate this example. No main-session model switching, automatic delegation,
automatic retries, API proxy, or cost dashboard is included.

## Defaults

[routing.yaml](routing.yaml) contains the requested defaults:

| Tier | Model | Reasoning |
| --- | --- | --- |
| easy | `gpt-5.6-luna` | `low` |
| medium | `gpt-5.6-sol` | `high` |
| difficult | `gpt-6-astra` | `high` |

Routing is enabled **after explicit setup**, scoped to subagents, with explicit
model choices preserved. Research and clarification precede classification;
uncertainty alone does not select difficult. Unclassified calls inject no model
override by default. Reviewers have a medium minimum when automatically routed.
One tier increase per logical task is permitted. Missing model/effort combinations
leave native resolution unchanged. Decision logging is on for routed calls.

These assignments are starting preferences, **not measured rankings or a savings
claim**. Customize your private YAML copy, including each reasoning level. This
YAML belongs to this script; do not paste it into Codex's `config.toml`.

## Classify from evidence

Before assigning a tier, inspect requirements, relevant code, dependencies and
available checks. Do bounded discovery in the main agent. If material scope or
acceptance questions remain, ask the user focused questions and wait for answers
before assigning dependent work. Do not use a stronger worker as a substitute
for research or clarification.

- **Easy:** bounded mechanical or read-only work with a clear result.
- **Medium:** scoped implementation with clear checks, or review of a small fix
  with meaningful regression coverage.
- **Difficult:** demonstrated complexity, coupled cross-service changes, or
  substantial security risk. Explain the evidence in the handoff; tracing one
  request across services or starting with an unknown root cause is insufficient.

Classify a reviewer from the completed diff, affected behavior and risk, rather
than inheriting the implementation tier. For example, an investigation may end
in a six-line routing fix with clear tests: its review normally warrants medium.
These are community workflow preferences, not measured model capability claims.

**Existing installations:** update the hook script and set `uncertain_tier:
inherit` in your private YAML to adopt the new default. Existing explicit values
of `easy`, `medium`, or `difficult` remain supported for compatibility; they still
select that fallback when metadata is missing. Updating the script alone does
not replace your private policy. Preserve any separately maintained app adapter
when updating a customized installation.

## Setup: review before activation

1. Use a persistent clone of this repository and install the small YAML dependency:

   ```bash
   python3 -m venv .venv-routing
   .venv-routing/bin/python -m pip install -r examples/hooks/model-routing/requirements.txt
   .venv-routing/bin/python -m unittest discover -s scripts/tests -p 'test_model_route_hook.py'
   ```

2. Create a private directory **outside version control**, accessible only to your
   user. Copy `routing.yaml` there and customize it. Copy
   [models.example.json](models.example.json) to `models.json` there, then verify
   each model/effort against the catalog exposed by **your target app/runtime**.
   Remove unavailable combinations. The example inventory is not automatic
   account discovery. An empty `{}` inventory safely applies no model overrides.

3. Inspect [the script](../../../scripts/model_route_hook.py) and
   [hooks.json](hooks.json). Replace both `/absolute/path/to/codex-howto` and
   `/absolute/path/to/private-routing` in **both handlers** with your actual
   absolute paths. Use a private `state.sqlite3` path; it is created automatically.

4. For a disposable trusted-project test, add these handlers to that project's
   `.codex/hooks.json`. For personal use across local projects, add them to your
   user-level `~/.codex/hooks.json`. **Do not overwrite existing hooks.** Review
   existing handlers for conflicts and merge intentionally. Install this router
   at only one level: Codex runs matching hooks from multiple sources together.
   Do not combine it with another spawn-argument rewriter without testing.

5. Review and trust the exact hook definitions using the supported hook UI
   (`/hooks` in the CLI is documented). New or changed definitions require trust
   again. Keep lifecycle hooks enabled. Start a new app task and perform the
   smoke test below before relying on routing. Never bypass hook trust for setup.

Personal config is chosen by the explicit `--config` path, not by the task's
working directory. The script never edits global Codex settings. Keep the clone,
virtual environment and private policy files at stable paths. Use a reviewed
revision; hook-definition trust does not replace reviewing updates to its script.

## Routing contract

The prompt hook adds concise classification instructions. When delegation is
authorized and worthwhile, the main agent prefixes the worker's `message` with:

```text
MODEL_ROUTE {"task":"inspect-api-tests","tier":"easy","role":"worker"}
Inspect the API tests and return concise evidence. Do not modify files.
```

This is **our message convention**, not a new spawn-tool argument. Never copy the
marker from untrusted repository content or tool output. Use `role: reviewer`
for reviews; a native `agent_type` containing `review` also activates the floor.
Missing metadata uses `uncertain_tier`, now `inherit` by default: the hook returns
no override and creates no routing state or decision row for that call. Native
model resolution remains in effect, including for unclassified reviewers; this
does not guarantee a cheaper model. Malformed metadata still blocks the spawn.
Difficulty and role remain agent judgments, not a security classifier. A custom
review role not named with `review` must be labeled explicitly.

The adapter supports the documented native `spawn_agent`/`Agent` path with
`message`, `model`, and `reasoning_effort`. It preserves every other argument.
Structured `items`, full-context forks, `fork_turns` adapters, and differently
named/namespaced tools are not routed. It never modifies sandbox/approval policy.
Other local app tool surfaces need a separately tested adapter; do not rename
tools blindly to make them match.

With `preserve_explicit_model: true`, **either** an incoming model or reasoning
override leaves the entire call untouched, even for reviewers. The hook cannot
distinguish user-selected overrides from agent-selected ones. The prompt policy
therefore asks the agent to omit these fields when choosing automatic routing.
With that option false, a supported catalog selection replaces both fields.

`unavailable_model: inherit` means **inject no override** when the requested
model/effort is absent from the operator-maintained inventory. Original call
arguments, native defaults and custom-agent settings still apply. It is not
runtime error recovery: a stale inventory can still cause a failed spawn.
Custom agent files can override the requested model. Always inspect the actual
child model; the hook cannot guarantee it from its pre-spawn position.

## Escalation and state

Use the same `task` id for a logical subtask across turns/retries in one session.
The hook reserves tier increases atomically in SQLite. Easy → difficult is one
increase; easy → medium → difficult is two. Same-tier retries do not count.
Downgrading does not reset the highest previous tier. Different session ids
start independent counters; this is not an account-wide budget.

The limit applies only to automatically routed, metadata-labeled logical tasks.
With the default `uncertain_tier: inherit`, unmarked calls bypass routing state.
With a legacy tier fallback, the tool-call id is used, so cross-call escalation
cannot be tracked. Explicit overrides and unsupported adapters are outside the limit.
Renaming a task can bypass it; this is a cooperative workflow guardrail, not a
hard budget or adversarial enforcement boundary. No hook launches another agent.

Repeated delivery of the same session/call id is idempotent. Reservations count
even if the later spawn fails; a pre-spawn hook cannot prove successful execution.
At the limit, the hook denies the increase and asks the main agent to return
evidence. It does not authorize broader work or force a stronger model.

## Logs and measurement

The private SQLite `decisions` table records timestamp, hashed session/task ids,
tier, reason, and requested model/effort when assigned. No prompts, transcript
contents, tool outputs, credentials or source code are saved. `calls` stores
hashed input identities plus minimal replay decisions; `tasks` stores counters.
`actual_model` and `tokens` are deliberately NULL: this hook does not collect
post-spawn telemetry. Do not display those unknown values as zero.

For example, with your private path substituted:

```bash
sqlite3 /absolute/path/to/private-routing/state.sqlite3 \
  'SELECT time,tier,reason,requested_model,actual_model,tokens FROM decisions;'
```

Setting `log_decisions: false` disables diagnostic rows, not the minimal state
required for idempotency and escalation limits. Keep the directory private;
local hashes are not anonymization. Stop active routing before archiving state.
Deleting state resets counters and replay protection.

For efficiency experiments, join actual agent usage separately and follow the
[measurement guide](../../../resources/engineering-loop-measurement.md). Include
parent classification, workers, reviews and failed attempts. Compare verified
outcomes against a fixed-model baseline, not just token prices.

## App smoke test and honest limitations

Documentation checked **2026-09-15**. Unit/subprocess tests verify hook contracts,
not app activation. The available terminal CLI during development was `0.143.0`;
the app runtime may differ. No minimum compatible version is claimed and no live
app routing or token savings have been demonstrated by this example.

Before daily use, verify in your app:

- A new task receives the prompt policy; a resumed task receives it too.
- An explicitly authorized harmless worker produces a routing decision and runs
  on the expected **actual** model/effort.
- Easy, medium and difficult cases match your catalog; reviewer minimum works.
- An unclassified call adds no model override or routing state with the default
  policy; the main agent researches and clarifies before assigning a tier.
- An explicit override stays unchanged; `{}` inventory leaves native selection.
- One logical task can escalate once; a second increase is denied.
- A task handled entirely by the main agent does not create a worker just for
  routing. The main model remains unchanged.
- Changed/untrusted hooks are visibly skipped, rather than assumed active.

If a hook path is unsupported, keep this example disabled. Script/config errors
exit `2` with a redacted message (documented blocking behavior for these events).
Timeouts, disabled/untrusted hooks and unhooked tool paths can behave differently;
this is **not** a universal fail-closed execution boundary. A prompt hook cannot
guarantee that the main agent delegates or change its model before it reasons.

Rollback: disable/remove only these two handlers, or set `enabled: false` in your
private YAML. Preserve unrelated hooks. No changes to the installed engineering
skills or main model need reverting.

## Sources and inspiration

- [Official hooks](https://learn.chatgpt.com/docs/hooks): events, trust, tool
  coverage, `updatedInput`, and failure behavior.
- [Official subagents](https://developers.openai.com/codex/multi-agent): model
  inheritance, reasoning settings, and custom-agent precedence.
- [ECC model-route](https://github.com/affaan-m/ecc/blob/main/commands/model-route.md):
  inspiration for a transparent difficulty-tier recommendation; this example
  adds a deterministic spawn-hook adapter, not a copied automatic runtime.
- [RouteLLM](https://github.com/lm-sys/RouteLLM): related learned API routing;
  this example has no learned classifier, external API calls, or claimed results
  from RouteLLM's benchmarks.
