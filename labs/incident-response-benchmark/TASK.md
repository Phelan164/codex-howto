# Benchmark task

Implement the dependency-free incident-response dashboard specified in
`README.md` and follow `AGENTS.md`.

Requirements:

1. Preserve the supplied tests byte-for-byte.
2. Implement the store, HTTP API, and browser client with the smallest coherent design.
3. Run the required checks and inspect the final diff.
4. Do not add dependencies, generated assets, build steps, or network calls.
5. Write `benchmark-final.md` containing:
   - changed files;
   - exact checks and results;
   - browser interactions actually exercised;
   - integration rework or ownership conflicts;
   - anything unverified;
   - residual risks.

Completion requires the supplied tests and the post-run evaluator to pass. Do
not claim browser verification unless a browser interaction was actually
performed.
