# Measured task receipt

Create one receipt for every measured agent run. Define the contract and
budgets before starting, then complete the outcome from observed evidence.
Leave unavailable optional values blank instead of estimating them.

```yaml
task:
  id:
  class:
  starting_commit:
  goal:
  in_scope: []
  out_of_scope: []
  planned_paths: []
  acceptance_checks: []

run:
  profile:
  workflow_components: []
  workflow_revisions: []
  codex_surface:
  model:
  reasoning_effort:
  sandbox:
  tool_profile:

budgets:
  elapsed_seconds:
  total_tokens:
  retries:
  scope_expansions:
  human_checkpoints:

outcome:
  accepted:
  evidence_complete:
  regression_before_fix:
  focused_checks_passed:
  required_checks_passed:
  files_read:
  files_changed:
  unexpected_files_changed:
  scope_expansions:
  retries:
  human_corrections:
  human_checkpoints:
  elapsed_seconds:
  total_tokens:
  total_cost_usd:

evidence:
  baseline:
  focused_checks: []
  required_checks: []
  review:
  unverified: []

decision:
  verdict: # keep, simplify, specialize, remove, or unresolved
  reason:
  repeat_on: []
```

## Counting rules

- `unexpected_files_changed` counts changed files outside the approved scope,
  excluding repository-generated files explicitly named in the task contract.
- `scope_expansions` counts approved changes to the original in-scope paths,
  subsystems, acceptance criteria, or external systems.
- `retries` counts repeated attempts that add no new evidence.
- `human_corrections` counts interventions that change code, tests,
  requirements, or the next technical action.
- `human_checkpoints` includes required design, scope, permission, and
  integration approvals.
- `total_tokens` includes all participating agents and review threads when the
  surface exposes them.

Record the counting policy before comparing runs. A receipt is an auditable
run record, not a universal productivity score.
