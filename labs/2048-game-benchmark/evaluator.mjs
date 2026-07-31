import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFile } from "node:fs/promises";
import { pathToFileURL } from "node:url";
import path from "node:path";

const [candidateArg, fixtureArg] = process.argv.slice(2);
if (!candidateArg || !fixtureArg) {
  console.error("usage: node evaluator.mjs <candidate-dir> <fixture-dir>");
  process.exit(2);
}

const candidate = path.resolve(candidateArg);
const fixture = path.resolve(fixtureArg);
const failures = [];
const check = async (name, operation) => {
  try {
    await operation();
    console.log(`PASS ${name}`);
  } catch (error) {
    failures.push(`${name}: ${error.message}`);
    console.error(`FAIL ${name}: ${error.message}`);
  }
};

await check("provided tests are unchanged", async () => {
  const expected = await readFile(path.join(fixture, "test/engine.test.mjs"));
  const actual = await readFile(path.join(candidate, "test/engine.test.mjs"));
  assert.deepEqual(actual, expected);
});

await check("provided test suite passes", async () => {
  const result = spawnSync(process.execPath, ["--test"], {
    cwd: candidate,
    encoding: "utf8",
  });
  assert.equal(result.status, 0, `${result.stdout}\n${result.stderr}`.trim());
});

let engine;
await check("engine module imports", async () => {
  const url = pathToFileURL(path.join(candidate, "game/engine.mjs"));
  url.searchParams.set("evaluation", Date.now().toString());
  engine = await import(url.href);
  for (const name of ["SIZE", "createGame", "move", "spawnTile", "canMove"]) {
    assert.notEqual(engine[name], undefined, `missing export ${name}`);
  }
});

await check("additional merge and score cases pass", async () => {
  assert.ok(engine, "engine did not import");
  const state = {
    board: [
      2, 2, 4, 4,
      8, 0, 8, 8,
      16, 16, 32, 32,
      64, 128, 256, 512,
    ],
    score: 3,
    status: "playing",
  };
  const original = structuredClone(state);
  const values = [0, 0];
  const result = engine.move(state, "right", {
    random: () => values.shift() ?? 0,
  });

  assert.deepEqual(result.board.slice(0, 4), [2, 0, 4, 8]);
  assert.deepEqual(result.board.slice(4, 8), [0, 0, 8, 16]);
  assert.deepEqual(result.board.slice(8, 12), [0, 0, 32, 64]);
  assert.equal(result.score, 3 + 4 + 8 + 16 + 32 + 64);
  assert.deepEqual(state, original);
});

await check("spawn threshold uses ten percent fours", async () => {
  assert.ok(engine, "engine did not import");
  const empty = Array(16).fill(0);
  const twoValues = [0, 0.899999];
  const fourValues = [0, 0.9];
  const two = engine.spawnTile(empty, () => twoValues.shift());
  const four = engine.spawnTile(empty, () => fourValues.shift());
  assert.equal(two[0], 2);
  assert.equal(four[0], 4);
});

await check("browser contract is present", async () => {
  const html = await readFile(path.join(candidate, "game/index.html"), "utf8");
  const app = await readFile(path.join(candidate, "game/app.mjs"), "utf8");
  const css = await readFile(path.join(candidate, "game/styles.css"), "utf8");

  assert.match(html, /id=["']board["']/i);
  assert.match(html, /id=["']score["']/i);
  assert.match(html, /id=["']status["']/i);
  assert.match(html, /aria-live=["'](?:polite|assertive)["']/i);
  assert.match(html, /<button[^>]*id=["']restart["']/i);
  assert.match(
    html,
    /<script(?=[^>]*type=["']module["'])(?=[^>]*src=["'][^"']*app\.mjs["'])[^>]*>/i,
  );
  assert.match(app, /preventDefault\s*\(/);
  for (const key of ["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown"]) {
    assert.match(app, new RegExp(key));
  }
  assert.doesNotMatch(`${html}\n${app}\n${css}`, /https?:\/\//i);
});

if (failures.length) {
  console.error(`\n${failures.length} acceptance check(s) failed.`);
  process.exit(1);
}

console.log("\nAll post-run acceptance checks passed.");
