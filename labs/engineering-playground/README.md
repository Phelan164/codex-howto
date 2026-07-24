# Engineering playground

Practice the bundled engineering skills against a small, intentionally flawed
inventory checkout example. The lab uses only Python's standard library and a
static HTML page. Nothing connects to a cloud account, package registry, or
production service.

## Files

```text
engineering-playground/
├── AGENTS.md
├── backend/
│   ├── inventory.py
│   └── test_inventory.py
├── frontend/checkout.html
├── infra/deployment.yaml
└── rubric.md
```

The fixtures contain seeded correctness, accessibility, security, and
operational defects. Do not read [the rubric](rubric.md) until after your first
review.

## Setup

Copy the playground to a disposable, version-controlled directory:

```bash
cp -R labs/engineering-playground /tmp/codex-howto-playground
cd /tmp/codex-howto-playground
git init
git add .
git commit -m "baseline intentionally flawed playground"
```

If Git identity is not configured, the commit is optional; keep a clean copy so
you can inspect the final diff.

Run the dependency-free backend tests:

```bash
python3 -m unittest discover -s backend -p "test_*.py"
```

They pass initially. That is intentional: the suite does not yet cover the
seeded boundary defect.

## Lab 1: backend regression

Install `test-software` and `build-backend` as described in
[Module 05](../../modules/05-engineering-skills/README.md), then ask:

```text
$test-software Inspect the inventory reservation contract. Add the smallest
regression test for an uncovered input boundary. Prove it fails for the current
implementation. Work only in this disposable playground.
```

After observing the failing test:

```text
$build-backend Fix the reproduced inventory boundary bug without changing the
valid reservation behavior. Run the focused suite and inspect the diff.
```

## Lab 2: frontend behavior and accessibility

Open `frontend/checkout.html` in a browser, use the form with several names and
quantities, and then ask:

```text
$build-frontend Review and repair the checkout page's accessible form semantics,
status/error announcements, and unsafe result rendering. Preserve the simple
dependency-free design. Verify keyboard behavior and explain any browser checks
you could not run.
```

Do not accept a visual-only check as proof that keyboard, announcements, and
untrusted text handling work.

## Lab 3: operational plan

Ask for a plan before allowing edits:

```text
$operate-devops Review infra/deployment.yaml as a local teaching fixture. Do not
apply or deploy anything. Produce the filled change-safety template, identify
runtime and rollout risks, and propose the smallest hardened manifest change
with validation and rollback commands.
```

If you choose to implement the local YAML edits, keep all apply/deploy commands
explicitly out of scope.

## Lab 4: independent reviews

Run both review skills against your final diff:

```text
$review-code Review the playground diff against the baseline commit. Return
findings first and name any checks that were unsafe or unavailable.
```

```text
$review-security Threat-review the playground diff and remaining fixtures.
Trace attacker-controlled input, runtime privilege, and supply-chain assumptions.
Do not exploit anything or access external systems.
```

Compare the reports: correctness findings and security findings can overlap,
but each should explain its own impact and evidence.

## Lab 5: orchestration comparison

First complete one single-agent review and record its elapsed time, total token
usage if the surface exposes it, finding quality, and retry count. Then invoke:

```text
$orchestrate-engineering Decide whether this playground review benefits from
delegation. If it does, use the smallest set of read-only specialists, give each
exclusive scope and a stop condition, then deduplicate and validate their
findings. If it does not, explain why and keep one agent.
```

Use the [token-efficiency scorecard](../../resources/token-efficiency-scorecard.md)
to compare the runs. Parallel work is not a token-saving claim; measure total
cost and useful evidence.

## Completion check

- A new test fails before the backend fix and passes afterward.
- Frontend verification covers keyboard use, labels, announcements, and safe
  rendering—not appearance alone.
- The infrastructure output separates plan, apply, verify, and rollback.
- Code and security reviews contain evidence-backed findings or explicitly say
  none were verified.
- The orchestration decision names selected and skipped roles.
- No command targeted a real environment or external service.
