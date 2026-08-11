# Incident benchmark guidance

## Scope

Build the requested dependency-free incident dashboard only in a disposable
copy of this directory.

## Required command

```bash
python3 -m unittest discover -s test -v
```

## Constraints

- Use only the Python standard library and browser-native HTML, CSS, and JavaScript.
- Do not add dependencies, generated assets, build steps, or network calls.
- Do not weaken, remove, skip, or rewrite the supplied tests.
- Preserve the HTTP and file ownership contracts in `README.md`.
- Persist through atomic replacement so an interrupted write cannot truncate the store.

## Done

Report changed files, exact checks, browser behavior actually exercised,
unverified behavior, integration rework, and residual risk. Review the final
diff before handoff.
