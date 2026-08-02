# Codex Skill Benchmark

Interactive evidence explorer for the controlled GPT-5.6-sol measurements in
[Phelan164/codex-howto](https://github.com/Phelan164/codex-howto).

The page compares no repository skill, `engineering-loop` v0.2.0, and the lean
v0.4.0 loop across a small backend fix and a medium dependency-free 2048 build.
It keeps acceptance gates primary and presents token use, elapsed time, retries,
method controls, and limitations without claiming that skills always improve
efficiency.

## Local development

Requires Node.js `>=22.13.0`.

```bash
npm install
npm run dev
```

Open the local URL printed by the development server.

## Verification

```bash
npm run build
npm run lint
npm test
```

`npm test` builds the production worker and verifies that the server-rendered
page contains the benchmark evidence, source link, and limitations while
excluding starter-preview artifacts.

## Sources

- [Backend boundary measurement](https://github.com/Phelan164/codex-howto/blob/main/examples/measurements/gpt-5.6-sol-backend-boundary-2026-07-31.md)
- [2048 measurement](https://github.com/Phelan164/codex-howto/blob/main/examples/measurements/gpt-5.6-sol-2048-game-2026-07-31.md)
- [Replication request](https://github.com/Phelan164/codex-howto/issues/23)

The site is an evidence viewer, not an independent replication.
