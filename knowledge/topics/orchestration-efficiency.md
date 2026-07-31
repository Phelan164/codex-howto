# Orchestration efficiency

> Status: experimental
> Last updated: 2026-07-31
> Sources: `official-codex-manual`, `local-orchestration-matrix`

## Current understanding

Multi-agent orchestration normally increases total token use. Its defensible
benefits are reduced elapsed time, isolated noisy investigation, and broader
specialist coverage when work can be divided into independent, bounded parts.

## Evidence

The repository's
[decision matrix](../../resources/orchestration-decision-matrix.md) routes
small or coupled tasks to one agent and reserves delegation for work with clear
ownership, independent evidence, and concise return contracts. Official Codex
guidance similarly treats multi-agent work as coordination that needs explicit
scope and integration.

## Implications

Do not advertise subagents as a token-saving feature. Measure total tokens,
elapsed time, coverage, duplicate work, conflicts, and integration failures.

## Promotion status

Promoted into modules
[08 · Subagents](../../modules/08-subagents/README.md),
[09 · Orchestration](../../modules/09-orchestration/README.md), and
[10 · Context efficiency](../../modules/10-context-and-token-efficiency/README.md).
