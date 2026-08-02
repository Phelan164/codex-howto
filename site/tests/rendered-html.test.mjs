import assert from "node:assert/strict";
import test from "node:test";

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);

  return worker.fetch(
    new Request("http://localhost/", {
      headers: { accept: "text/html" },
    }),
    {
      ASSETS: {
        fetch: async () => new Response("Not found", { status: 404 }),
      },
    },
    {
      waitUntil() {},
      passThroughOnException() {},
    },
  );
}

test("server-renders the benchmark explorer", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);

  const html = await response.text();
  assert.match(html, /<title>Codex Skill Benchmark — Codex How To<\/title>/i);
  assert.match(html, /Do Codex skills/);
  assert.match(html, /It depends/);
  assert.match(html, /Six controlled GPT-5\.6-sol runs/);
  assert.match(html, /Dependency-free 2048/);
  assert.match(html, /828,446/);
  assert.match(html, /380,767/);
  assert.match(html, /This is a boundary to test, not a universal claim/);
  assert.match(html, /Phelan164\/codex-howto/);
  assert.doesNotMatch(html, /codex-preview/);
  assert.doesNotMatch(html, /react-loading-skeleton/);
});
