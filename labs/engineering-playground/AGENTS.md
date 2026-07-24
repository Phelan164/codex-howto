# Playground guidance

## Scope

This directory is an intentionally flawed, local-only teaching fixture.

## Commands

Run backend tests with:

```bash
python3 -m unittest discover -s backend -p "test_*.py"
```

The frontend is one static HTML file with no build step.

## Safety

- Do not deploy `infra/deployment.yaml`.
- Do not access a cluster, registry, cloud account, or external service.
- Treat all infrastructure commands as examples or local validation only.
- Do not add third-party dependencies; the lab must remain self-contained.
- Preserve a failing regression test before fixing a seeded backend defect.

## Done

Report changed files, exact checks, unverified browser behavior, and residual
risk. Keep unrelated seeded defects intact unless the exercise requests them.
