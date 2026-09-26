# 10 practical Codex tips

Pick the problem you have today. Copy one prompt, replace the example details,
and inspect the result. These are community workflow recipes, not guaranteed
token savings. No skill installation is needed for these prompts.

## 1. Define the finish line

**Problem:** the change looks finished but the behavior is unverified.

```text
Fix the empty-cart checkout bug. Done means the reproduction passes,
the relevant regression test passes, and the repository's required checks
pass. Report any check you could not run and why.
```

**Useful when:** handing off a feature or bug fix.
**Limit:** passing checks prove only the behavior they cover.
[More: prompt contracts](../modules/03-prompts-and-plans/README.md).

## 2. Give a starting point

**Problem:** exploration consumes time before reaching the relevant code.

```text
Start with src/cart/checkout.ts and its callers. The failing behavior is
an empty cart reaching payment. Expand the search when dependencies require
it; preserve the public API.
```

**Useful when:** you know a failing command, file, or entry point.
**Limit:** a suspected file is a lead; allow evidence to redirect the search.
[More: context efficiency](../modules/10-context-and-token-efficiency/README.md).

## 3. Turn a bug report into a reproduction

**Problem:** a plausible patch addresses the wrong cause.

```text
Reproduce the reported failure first. Show the smallest failing case,
then fix the cause and rerun that case. If reproduction is blocked,
explain the missing prerequisite before claiming the bug is fixed.
```

**Useful when:** the report is specific enough to reproduce.
**Limit:** intermittent failures may need instrumentation rather than another
test rerun. [More: testing](../modules/07-testing-and-review/README.md).

## 4. Ask for a decision before a large implementation

**Problem:** implementation starts while an architectural choice is unresolved.

```text
Inspect our current authentication flow. Compare two ways to add organization
API keys, including compatibility and verification. Recommend one and ask
only questions whose answers would change the design. Do not implement yet.
```

**Useful when:** alternatives have meaningful tradeoffs.
**Limit:** routine edits rarely need a design exercise.
[More: engineering specification](../examples/templates/engineering-spec.md).

## 5. Correct direction while work is running

**Problem:** a missing constraint becomes apparent mid-task.

```text
Keep the existing response schema. Continue the fix within that constraint;
adjust the planned tests accordingly.
```

**Useful when:** steering the current task. In the CLI, Enter steers and Tab
queues a follow-up while Codex is working.
**Limit:** queue unrelated follow-ups so they do not change the current goal.
[Official behavior: steering and queuing](https://learn.chatgpt.com/docs/prompting#improve-the-result-with-follow-up-messages).

## 6. Review a fixed candidate

**Problem:** review findings refer to code that changed during review.

```text
Before completion, record the candidate commit or diff. Use a fresh reviewer
context to inspect it for consequential defects. Validate findings, fix
confirmed issues, rerun affected checks, and identify the final reviewed revision.
```

**Useful when:** a change warrants an independent review and your environment
supports delegation.
**Limit:** another reviewer consumes time and tokens and can miss defects.
[More: independent review](../skills/engineering-loop/references/independent-review.md).

## 7. Delegate an independent question

**Problem:** workers edit overlapping files or repeat the same investigation.

```text
Delegate a read-only inspection of the API contract tests. Return missing
cases with file references. Keep implementation ownership with the main agent.
Do not create additional workers unless another independent task justifies it.
```

**Useful when:** inspection can proceed alongside implementation.
**Limit:** parallel work can reduce elapsed time while increasing total usage.
[More: orchestration choices](orchestration-decision-matrix.md).

## 8. Stop an unchanged retry loop

**Problem:** the same command keeps failing for the same reason.

```text
This failure has repeated. Identify whether it comes from code, environment,
permissions, or an incorrect assumption. Choose a next step that produces new
evidence; report the blocker if progress requires something unavailable.
```

**Useful when:** progress has stalled.
**Limit:** a running job with a live handle may simply need observation;
restarting it can duplicate work.
[More: troubleshooting](../modules/12-troubleshooting/README.md).

## 9. Carry evidence into the next session

**Problem:** the next session repeats discovery or revives rejected approaches.

```text
Prepare a short handoff: objective, branch and revision, relevant files,
confirmed decisions, checks and outcomes, failed approaches, remaining risks,
and the next action. Exclude secrets and unrelated conversation.
```

**Useful when:** switching sessions or handing work to another engineer.
**Limit:** the next session should verify that repository state still matches.
[Copy the handoff template](../examples/templates/engineering-handoff.md).

## 10. Measure before adding more process

**Problem:** a skill, stronger model, or additional reviewer feels better but
has no recorded benefit.

```text
For this task, record the model and reasoning effort if observable, acceptance
results, elapsed time, retries, review defects, and available token usage.
Mark missing measurements unknown. Include worker and review usage when available.
```

**Useful when:** deciding whether to keep a workflow change.
**Limit:** one successful task cannot establish general savings. Compare similar
tasks and quality before cost; token counts alone are not a bill.
[More: measurement protocol](engineering-loop-measurement.md).

## Try one, then contribute evidence

Run one tip in the [five-minute playground](../labs/engineering-playground/README.md).
If it helps or fails, share a sanitized reproduction and what changed through
[the contribution guide](../CONTRIBUTING.md). A tested correction is more useful
than another list of untested prompts.

Product-specific prompting and CLI steering guidance checked **2026-09-26**
against [official prompting documentation](https://learn.chatgpt.com/docs/prompting).
The engineering recipes above are repository practices; their linked modules
provide the deeper contracts and limitations.
