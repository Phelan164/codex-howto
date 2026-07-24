# Orchestration decision matrix

| Situation | Topology | Reason |
|---|---|---|
| Small, well-scoped edit | One agent | Coordination would cost more than execution |
| Unknown code path before a change | Explorer → implementer | Exploration output is a dependency |
| Security, tests, and reliability review | Parallel read-only fan-out | Independent lenses over one immutable diff |
| Frontend and backend share an unsettled contract | Sequential contract-first pipeline | Workers otherwise encode conflicting assumptions |
| Independent modules with frozen interfaces | Partitioned parallel implementation | Exclusive ownership limits conflicts |
| Two tasks edit the same central file | Sequential | Merge and reasoning conflicts dominate |
| Large failing test log | Test worker → concise summary | Isolates noise from the main thread |
| Production deployment | Human-controlled staged procedure | Consequence and external state require explicit gates |

## Decision questions

1. Can one agent complete the task within a clear context?
2. Are subtasks independent or merely different stages?
3. Are workers read-heavy or write-heavy?
4. Can each write worker own an exclusive path?
5. Is the interface between workers already stable?
6. Will each worker return a concise evidence summary?
7. What integration check catches cross-worker failure?

If answers 2, 4, or 5 are unclear, prefer a sequential plan.
