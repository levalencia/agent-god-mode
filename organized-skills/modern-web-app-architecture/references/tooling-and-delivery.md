# Tooling, Delivery, and Production Readiness

## Build Tooling (Pick the Simplest That Fits)

### SPA Builds
- Vite is a strong default for CSR SPAs (fast dev server, modern bundling).
- Ensure code splitting is aligned to your router and large feature boundaries.

### Hybrid/SSR Builds
- Use a framework when SSR/SSG/ISR/RSC is a requirement (routing, loaders, caching, streaming are hard to hand-roll).
- Decide whether rendering happens on origin servers vs edge runtime.

## Module Boundaries That Scale

Prefer **feature/domain folders** with stable public APIs:
- `features/<domain>/components|hooks|services|routes`
- `shared/<components|hooks|utils>`
- Avoid “god” `utils/` dumping grounds; create small, owned libraries.

## Environments and Configuration

Make config explicit:
- Build-time values (public) vs runtime values (server-only).
- Don’t ship secrets to the browser.
- Prefer a single config module that validates required variables at startup.

## Deployment Basics

### Static Assets
- Content-hashed filenames + long-lived caching (`immutable`).
- HTML should revalidate frequently (or be cached with strategy per route).

### Rollouts
- Use canaries/feature flags for risky launches.
- Have fast rollback (previous artifact still deployable).

## Observability (You’ll Want This Later)

Baseline:
- Error monitoring (e.g., Sentry) with release tagging and sourcemaps
- Product analytics events for key funnels (privacy-aware)
- Web Vitals/RUM collection (LCP/INP/CLS) by route and device class

## Feature Flags and Experiments

Use flags when:
- You need safe incremental rollout
- You want A/B testing
- You’re migrating legacy to new routes/components

Rules:
- Flags must have owners and cleanup dates
- Don’t let flags leak into every component; centralize decision points

## Delivery Checklist

- [ ] Source maps uploaded to error monitoring
- [ ] Cache headers correct for hashed assets
- [ ] Runtime config validated (no “undefined” at runtime)
- [ ] CI gates enforced (tests + budgets)
- [ ] Rollback plan documented

