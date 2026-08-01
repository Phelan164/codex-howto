# Game benchmark guidance

## Scope

Build the requested dependency-free browser game only in a disposable copy of
this directory.

## Required command

```bash
node --test
```

## Constraints

- Use browser-native HTML, CSS, and JavaScript modules.
- Do not add dependencies, a build step, generated assets, or network calls.
- Do not weaken, remove, skip, or rewrite the provided tests.
- Keep game rules in `game/engine.mjs` and browser behavior in `game/app.mjs`.
- Preserve deterministic random injection in the engine API.

## Done

Report changed files, exact checks, browser behavior actually verified,
unverified behavior, and residual risk. Review the final diff before handoff.
