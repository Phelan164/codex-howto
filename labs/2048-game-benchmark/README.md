# Dependency-free 2048 benchmark

This is a medium-sized implementation benchmark for the
[engineering-loop measurement protocol](../../resources/engineering-loop-measurement.md).
It is deliberately larger than the backend boundary exercise: success requires
state transitions, deterministic randomness, browser input, accessibility,
responsive presentation, automated checks, review, and an evidence handoff.

Run it only from a disposable copy. The starting fixture intentionally has no
`game/` implementation, so its supplied test suite fails at baseline.

```bash
cd labs/2048-game-benchmark
benchmark_root="$(mktemp -d)"
cp -R AGENTS.md README.md TASK.md test .gitignore "$benchmark_root/"
cd "$benchmark_root"
git init
git add .
git commit -m "baseline 2048 benchmark"
```

Create three fresh copies from that same commit and follow the measurement
protocol. Do not copy `evaluator.mjs` into a candidate. Apply it only after all
variants finish:

```bash
node /path/to/codex-howto/labs/2048-game-benchmark/evaluator.mjs \
  /path/to/candidate \
  /path/to/codex-howto/labs/2048-game-benchmark
```

The first published three-way result is
[GPT-5.6-sol 2048 game seed measurement](../../examples/measurements/gpt-5.6-sol-2048-game-2026-07-31.md).

## Required files

```text
game/
├── app.mjs
├── engine.mjs
├── index.html
└── styles.css
```

## Engine contract

`game/engine.mjs` must export:

- `SIZE`, equal to `4`;
- `createGame({ random } = {})`;
- `move(state, direction, { random } = {})`;
- `spawnTile(board, random)`;
- `canMove(board)`.

State contains a 16-value `board`, numeric `score`, and `status` of `playing`,
`won`, or `lost`.

- A new game contains exactly two spawned tiles.
- A spawn chooses an empty cell with injected randomness and adds `2` 90% of
  the time or `4` 10% of the time.
- `move` accepts `left`, `right`, `up`, or `down` without mutating its input.
- Equal adjacent tiles merge once per move and add their result to the score.
- A changed move spawns one tile; a no-op does not spawn.
- Reaching 2048 wins; a board without a legal move loses.
- Terminal states reject additional moves.

## Browser contract

- Load `app.mjs` from `index.html` as a module.
- Render the game in `#board`, score in `#score`, and announcements in
  `#status`.
- Provide a native button at `#restart`.
- Support Arrow keys and WASD, prevent scrolling for handled keys, and ignore
  unrelated keys.
- Give the board understandable semantics and make status changes a live
  region.
- Use a responsive layout without external fonts, images, or libraries.

## Acceptance

- The supplied tests remain byte-for-byte unchanged and `node --test` passes.
- The post-run evaluator passes.
- The final diff contains only the implementation and requested handoff.
- The handoff distinguishes automated evidence, exercised browser behavior,
  unverified behavior, and residual risk.

The evaluator checks deterministic engine edge cases and the static browser
contract. It does not replace interaction, visual, or assistive-technology
testing.
