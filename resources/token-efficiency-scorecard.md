# Context and token-efficiency scorecard

Score each item from 0 (no) to 2 (consistently).

| Practice | Score |
|---|---:|
| The prompt states goal, routed context, constraints, and observable completion | |
| Durable repository facts live in `AGENTS.md`, not repeated prompts | |
| Skills are narrow and use progressive disclosure | |
| Exploration starts from named entry points rather than a repository-wide scan | |
| Focused tests run before broad suites | |
| Raw logs stay out of the main decision thread | |
| Worker summaries contain evidence, uncertainty, and a next action | |
| Parallel agents have independent work and a measurable reason to exist | |
| Write workers have exclusive ownership | |
| Obsolete assumptions are removed at phase boundaries | |
| Repeated failures trigger diagnosis rather than blind retry | |
| Final output separates verified results from unrun checks | |

## Interpretation

- **20–24:** context is intentionally managed.
- **14–19:** workable, with identifiable waste.
- **8–13:** likely suffering from broad reading, repeated prompts, or noisy output.
- **0–7:** simplify the workflow before adding agents or automation.

Track retries, elapsed time, duplicate work, and accepted defects alongside token use. A cheaper run that produces the wrong change is not efficient.

For a controlled baseline-vs-workflow comparison, use the
[engineering-loop measurement protocol](engineering-loop-measurement.md) and
its structured run record. This scorecard evaluates practices; it does not by
itself demonstrate that the engineering loop caused a better outcome.
