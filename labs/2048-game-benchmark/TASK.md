# Benchmark task

Implement the dependency-free 2048-style browser game specified in `README.md`
and follow `AGENTS.md`.

Requirements:

1. Preserve the provided tests byte-for-byte.
2. Implement the engine and browser files with the smallest coherent design.
3. Run the required checks and inspect the final diff.
4. Do not add dependencies, generated assets, or network calls.
5. Write `benchmark-final.md` containing:
   - changed files;
   - exact checks and results;
   - browser interactions actually exercised;
   - anything unverified;
   - residual risks.

Completion requires `node --test` to pass. Do not claim browser verification
unless a browser interaction was actually performed.
