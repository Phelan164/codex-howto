# Source policy

Use this policy for every ingest and promotion.

## Source classes

| Kind | Meaning | Typical use |
|---|---|---|
| `official` | Current first-party product documentation | Product behavior and supported configuration |
| `repository` | Versioned evidence already in this repository | Experiments, decisions, and local workflows |
| `community` | External implementation, article, discussion, or practice | Inspiration and hypotheses that need verification |
| `experiment` | A reproducible local or published evaluation | Measured claims with recorded setup and limitations |

## Registry

Add one object to `knowledge/sources.json`:

```json
{
  "id": "short-stable-id",
  "title": "Human-readable title",
  "kind": "official",
  "url": "https://example.com/source",
  "last_verified": "YYYY-MM-DD"
}
```

Use `path` instead of `url` for repository evidence. Paths are relative to the
project root. Use exactly one of `url` or `path`.

Source IDs are permanent. If a URL moves, update the record without changing
the ID. `last_verified` records when a maintainer checked the source, not when
the source was published.

## External content

- Put temporary downloads and extracted text in `.wiki-cache/`.
- Do not commit full external articles, documentation, transcripts, or images
  without redistribution permission.
- Prefer a metadata record, a direct link, and a compact synthesis.
- Keep quotations short and only when wording is materially important.
- Never place credentials, private conversations, or personal data in the
  public wiki.

## Claims

- Cite every load-bearing product, measurement, or historical claim.
- Mark inference as inference.
- Keep conflicting evidence visible until it is resolved.
- Use official sources for current Codex behavior.
- Treat community sources as patterns to test, not product specifications.
- Record experimental setup and limitations next to results.

## Review

- Query is read-only by default.
- Ingest and promotion require an explicit request.
- Generated factual changes require PR review.
- Scheduled maintenance may report drift or prepare a draft PR; it must not
  merge or push directly to a protected branch.
