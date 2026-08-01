import test from "node:test";
import assert from "node:assert/strict";

import {
  SIZE,
  canMove,
  createGame,
  move,
  spawnTile,
} from "../game/engine.mjs";

const board = (...rows) => rows.flat();
const fixedRandom = (...values) => {
  let index = 0;
  return () => values[Math.min(index++, values.length - 1)];
};

test("exports a four-by-four engine and creates two deterministic tiles", () => {
  assert.equal(SIZE, 4);
  const game = createGame({ random: fixedRandom(0, 0, 0, 0.95) });

  assert.equal(game.board.length, 16);
  assert.deepEqual(game.board.slice(0, 2), [2, 4]);
  assert.equal(game.board.filter(Boolean).length, 2);
  assert.equal(game.score, 0);
  assert.equal(game.status, "playing");
});

test("spawnTile is immutable and respects cell and value randomness", () => {
  const input = Array(16).fill(0);
  const result = spawnTile(input, fixedRandom(0.999, 0.95));

  assert.notEqual(result, input);
  assert.deepEqual(input, Array(16).fill(0));
  assert.equal(result[15], 4);
});

test("left movement compresses and merges each tile at most once", () => {
  const state = {
    board: board(
      [2, 2, 2, 2],
      [4, 4, 8, 0],
      [2, 0, 2, 2],
      [0, 0, 0, 0],
    ),
    score: 7,
    status: "playing",
  };

  const result = move(state, "left", { random: fixedRandom(0, 0) });

  assert.deepEqual(result.board.slice(0, 12), [
    4, 4, 2, 0,
    8, 8, 0, 0,
    4, 2, 0, 0,
  ]);
  assert.equal(result.score, 7 + 4 + 4 + 8 + 4);
  assert.deepEqual(state.board.slice(0, 4), [2, 2, 2, 2]);
});

test("right movement mirrors left movement", () => {
  const state = {
    board: board(
      [2, 2, 2, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0],
    ),
    score: 0,
    status: "playing",
  };

  const result = move(state, "right", { random: fixedRandom(0, 0) });
  assert.deepEqual(result.board.slice(0, 4), [2, 0, 2, 4]);
  assert.equal(result.score, 4);
});

test("vertical movement uses the same merge rules", () => {
  const state = {
    board: board(
      [2, 0, 4, 0],
      [2, 0, 4, 0],
      [4, 0, 4, 0],
      [4, 0, 4, 0],
    ),
    score: 0,
    status: "playing",
  };

  const up = move(state, "up", { random: fixedRandom(0.999, 0) });
  assert.deepEqual(
    [up.board[0], up.board[4], up.board[8], up.board[12]],
    [4, 8, 0, 0],
  );
  assert.deepEqual(
    [up.board[2], up.board[6], up.board[10], up.board[14]],
    [8, 8, 0, 0],
  );
  assert.equal(up.score, 4 + 8 + 8 + 8);
});

test("a no-op move neither spawns nor mutates", () => {
  const state = {
    board: board(
      [2, 4, 8, 16],
      [0, 0, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0],
    ),
    score: 12,
    status: "playing",
  };
  let calls = 0;

  const result = move(state, "left", {
    random: () => {
      calls += 1;
      return 0;
    },
  });

  assert.deepEqual(result, state);
  assert.notEqual(result, state);
  assert.equal(calls, 0);
});

test("a 2048 merge wins and terminal states reject further moves", () => {
  const state = {
    board: board(
      [1024, 1024, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0],
    ),
    score: 10,
    status: "playing",
  };

  const won = move(state, "left", { random: fixedRandom(0, 0) });
  assert.equal(won.status, "won");
  assert.equal(won.score, 2058);

  const after = move(won, "right", { random: fixedRandom(0, 0) });
  assert.deepEqual(after, won);
  assert.notEqual(after, won);
});

test("a full board without adjacent equals is lost", () => {
  const locked = board(
    [2, 4, 2, 4],
    [4, 2, 4, 2],
    [2, 4, 2, 4],
    [4, 2, 4, 2],
  );
  assert.equal(canMove(locked), false);

  const state = { board: locked, score: 99, status: "playing" };
  const result = move(state, "left", { random: fixedRandom(0, 0) });
  assert.equal(result.status, "lost");
  assert.deepEqual(result.board, locked);
});

test("a full board with an available merge can still move", () => {
  const playable = board(
    [2, 2, 4, 8],
    [4, 8, 16, 32],
    [8, 16, 32, 64],
    [16, 32, 64, 128],
  );
  assert.equal(canMove(playable), true);
});

test("invalid directions fail without changing state", () => {
  const state = {
    board: Array(16).fill(0),
    score: 0,
    status: "playing",
  };

  assert.throws(() => move(state, "diagonal"), /direction/i);
  assert.deepEqual(state.board, Array(16).fill(0));
});
