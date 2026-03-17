# Testing & Quality Strategy for Web Apps

## Guiding Principles

- Prefer tests that validate **user-visible behavior**, not implementation details.
- Put tests at the **lowest level that proves the behavior** (fast feedback).
- Make “quality” measurable with **CI gates** (types, lint, tests, budgets).

## Test Layers (Practical Pyramid)

1. **Static checks (fastest)**
   - Typecheck (TypeScript)
   - Lint (ESLint)
   - Formatting (Prettier)
2. **Unit tests**
   - Pure functions (formatters, reducers, domain logic)
3. **Component tests**
   - Render components with Testing Library
   - Mock network with MSW
4. **Integration tests**
   - Real router + data layer + key flows
5. **E2E tests (few, high value)**
   - Critical flows: auth, purchase, onboarding, permissions

## Tooling (Common Choices)

- Unit/component: Vitest or Jest + Testing Library
- Network mocking: MSW
- E2E: Playwright (preferred) or Cypress
- a11y: axe-core (component/E2E checks), Lighthouse CI (budgets)
- Visual regression (optional): Storybook + Chromatic or Playwright snapshots

## CI Quality Gates (Good Defaults)

- `typecheck` must pass
- `lint` must pass
- unit/component tests must pass
- E2E smoke suite on main branch and before deploy
- Bundle size budgets (fail build if exceeded)
- Lighthouse CI thresholds for key routes (especially public/SEO routes)

## Test Data & Determinism

- Use factories/fixtures for consistent data.
- Avoid time-dependent tests (freeze time).
- Avoid relying on real networks or shared environments in CI.

## Contract Testing (When Frontend/Backend Move Independently)

Use contract tests when you have:
- multiple teams changing API + UI in parallel
- frequent API evolution
- BFF/GraphQL schema changes

Approaches:
- Schema-driven (OpenAPI/GraphQL schema validation)
- Consumer-driven contracts (Pact-style)

## “Definition of Done” (Frontend)

- [ ] Loading, empty, and error states implemented
- [ ] Accessibility checked for critical flows
- [ ] Error boundary strategy exists (no white-screens)
- [ ] Performance budget not regressed
- [ ] Observability hooks in place (errors + key events)

