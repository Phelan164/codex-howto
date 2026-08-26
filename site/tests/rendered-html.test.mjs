import assert from "node:assert/strict";
import test from "node:test";

async function render(path = "/") {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);

  return worker.fetch(
    new Request(`http://localhost${path}`, {
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
  assert.match(
    html,
    /<link rel="canonical" href="https:\/\/codex-howto-benchmark\.nguyenvantamdk2\.chatgpt\.site\/?"\/>/i,
  );
  assert.match(html, /<meta name="robots" content="index, follow"\/>/i);
  assert.match(html, /application\/ld\+json/i);
  assert.match(html, /https:\/\/github\.com\/Phelan164\/codex-howto/);
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

test("publishes crawler discovery routes", async () => {
  const robotsResponse = await render("/robots.txt");
  assert.equal(robotsResponse.status, 200);
  const robots = await robotsResponse.text();
  assert.match(robots, /User-Agent: \*/i);
  assert.match(robots, /Allow: \//i);
  assert.match(
    robots,
    /Sitemap: https:\/\/codex-howto-benchmark\.nguyenvantamdk2\.chatgpt\.site\/sitemap\.xml/i,
  );

  const sitemapResponse = await render("/sitemap.xml");
  assert.equal(sitemapResponse.status, 200);
  const sitemap = await sitemapResponse.text();
  assert.match(
    sitemap,
    /<loc>https:\/\/codex-howto-benchmark\.nguyenvantamdk2\.chatgpt\.site<\/loc>/i,
  );
});
