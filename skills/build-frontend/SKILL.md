---
name: build-frontend
description: Build or modify production frontend interfaces with repository-native components, accessibility, responsive behavior, state handling, and focused verification. Use for UI features, pages, components, design implementation, client-side bugs, forms, and frontend refactors; do not use for backend-only or infrastructure-only work.
---

# Build Frontend

## Workflow

1. Read applicable `AGENTS.md` files and repository documentation.
2. Inspect the framework, component library, design tokens, routing, state patterns, tests, and nearby implementations.
3. Clarify the user journey, supported viewports, loading/empty/error states, accessibility needs, and completion checks.
4. Reuse existing components and tokens before creating new abstractions.
5. Implement the smallest coherent change.
6. Add or update tests at the lowest layer that proves behavior.
7. Run focused tests, then repository-required lint, type, and build checks.
8. Inspect the rendered result when browser or screenshot tooling is available.
9. Review the final diff for accidental style churn, broken states, and unrelated edits.

## Guardrails

- Preserve the project’s framework, styling system, and component conventions.
- Do not invent API response fields or silently change backend contracts.
- Do not replace an established design system with custom one-off styling.
- Keep semantic HTML, keyboard navigation, focus behavior, labels, and contrast in scope.
- Avoid speculative shared abstractions for a single component.
- Treat screenshots and mockups as visual references, not proof of interaction behavior.
- Do not claim visual verification unless the UI was rendered or inspected.

## Verification

Read [references/verification.md](references/verification.md) for UI, accessibility, responsive, and browser verification. Load it when the task changes rendered behavior or interaction.

Prefer:

```text
component test → feature test → type/lint → build → visual/interaction check
```

If a command cannot run, report the exact blocker and what remains unverified.

## Acceptance criteria

- The requested flow works in supported states and viewports.
- The change uses repository-native components and tokens.
- Meaningful behavior is covered by focused tests.
- Accessibility fundamentals are checked.
- Required repository checks pass or blockers are explicit.
- The final report names changed files, verification, and residual risk.
