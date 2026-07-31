# Wiki efficiency baseline

> Status: experimental
> Last updated: 2026-07-31
> Sources: `local-engineering-loop-measurement`, `karpathy-llm-wiki-gist`

## Question

Does a compiled maintainer wiki improve repeated Codex engineering and
documentation tasks enough to justify its context and maintenance cost?

## Planned comparison

Run the same 15–20 questions or maintenance tasks with:

1. existing repository documentation and no wiki instruction;
2. index-first wiki query; and
3. index-first wiki query plus the maintenance skill where writes are needed.

Hold the model, reasoning effort, repository revision, tools, permissions, and
done conditions constant.

## Measures

- answer correctness and completeness;
- citation precision and unsupported claims;
- relevant files found and affected pages identified;
- input and output tokens when available;
- elapsed time and tool calls;
- stale-claim detection;
- duplicate or contradictory prose introduced; and
- human review time.

## Proposed decision rule

Keep the wiki as a recommended maintainer workflow only if it preserves quality,
improves evidence recall, and reduces repeated context discovery without
creating unreviewed factual drift. Treat a 30% reduction in files or input
tokens on repeated questions as a useful target, not a guaranteed claim.

## Current result

No benchmark result has been recorded yet. The repository must not present the
wiki as proven more efficient until this experiment has representative data.
