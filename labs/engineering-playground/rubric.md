# Playground review rubric

Open this only after completing a first pass. It lists seeded high-value issues,
not the only valid findings.

## Backend

- `reserve` accepts zero and negative quantities even though its contract says
  reservations must be positive. A negative quantity increases available stock.
- The initial suite covers valid and insufficient-stock paths but misses this
  boundary. A regression test should fail before the implementation changes.
- A careful solution also decides how `bool` values should behave because Python
  treats them as integers; that decision is secondary to the seeded defect.

## Frontend

- The customer input has no programmatic label; a placeholder is not a label.
- Error and success changes are not exposed as live status to assistive
  technology, and invalid focus handling is absent.
- `innerHTML` combines untrusted customer text with markup, allowing HTML/script
  injection. Construct DOM nodes or use `textContent`.
- Quantity constraints are incomplete in markup even though JavaScript performs
  a partial check.

## Infrastructure

- The image uses the mutable `latest` tag rather than a reviewed immutable
  version or digest.
- The container runs as root and allows privilege escalation.
- Readiness/liveness behavior and CPU/memory requests or limits are absent.
- Rollout, abort, monitoring, rollback, and target-environment details are
  undefined.
- The fixture has no actual image, account, or cluster. A review must not invent
  an apply result or attempt deployment.

## Review quality

A high-quality answer:

- cites exact files and reachable behavior;
- separates correctness, accessibility, security, and operational impact;
- does not inflate style preferences into findings;
- distinguishes verified checks from proposed checks;
- does not claim that orchestration saved tokens without measured evidence;
- stops when the bounded review scope is exhausted.
