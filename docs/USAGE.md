# Agent God Mode — Day-to-Day Usage Guide

You now have **2,382 skills** at your fingertips, but the real question is: *how do you actually use them every day?*

This guide maps **real work scenarios** to the right skills, personas, and references — no memorization required.

---

## The Golden Rule

> **Just ask normally.** The two-tier search system handles the rest.

When you type a task, the agent automatically:
1. Scans for **Tier 1 lifecycle intent** (build, test, review, ship, debug)
2. Runs a **Tier 2 domain search** (Azure, React, Kubernetes, etc.)
3. Loads and follows the relevant skills

You don't need to remember skill names. **Natural language is the interface.**

---

## Daily Workflow Scenarios

### 1. Starting Your Day / Sprint Planning

**You ask:**
> "What should I focus on this sprint?"

**Skills triggered:**
- `idea-refine` — Clarify goals, surface assumptions
- `planning-and-task-breakdown` — Decompose into atomic, verifiable tasks

**What happens:** The agent asks clarifying questions, then produces a structured task list with acceptance criteria and dependency ordering.

---

### 2. Building a New Feature

**You ask:**
> "Build a new authentication feature for this project."

**Skills triggered:**
- `spec-driven-development` → Writes a PRD before any code
- `test-driven-development` → Writes failing tests first
- `incremental-implementation` → Thin vertical slices, one at a time
- `api-and-interface-design` — If building REST/GraphQL endpoints
- `frontend-ui-engineering` — If building UI components

**What happens:** The agent does NOT start coding immediately. It:
1. Asks clarifying questions to surface assumptions
2. Writes a spec (Objective, Tech Stack, Commands, Structure, Testing Strategy, Boundaries)
3. Breaks it into tasks
4. Writes failing tests
5. Implements the minimal code to make tests pass
6. Refactors
7. Asks you to review the spec/plan before proceeding

**Pro tip:** If your feature involves a specific platform (Azure, AWS, Kubernetes), the agent will also pull in domain skills automatically.

---

### 3. Fixing a Bug

**You ask:**
> "This endpoint is returning 500 errors."
> "The login flow is broken."

**Skills triggered:**
- `debugging-and-error-recovery` — Five-step triage: reproduce → localize → reduce → fix → guard
- `test-driven-development` — Write a reproduction test first (the Prove-It Pattern)

**What happens:** The agent:
1. Asks for error logs / reproduction steps
2. Spawns a subagent to investigate (if configured)
3. Writes a test that reproduces the bug
4. Confirms the test fails
5. Implements the fix
6. Confirms the test passes
7. Runs the full test suite to check for regressions

**Anti-pattern the agent avoids:** "I'll just fix it quickly" → No. It follows the triage workflow every time.

---

### 4. Code Review (Before Merge)

**You ask:**
> "Review this PR."
> "Is this code ready to merge?"

**Skills triggered:**
- `code-review-and-quality` — Five-axis review (correctness, readability, architecture, security, performance)

**Persona option (for deeper review):**
> "Review this PR as the code-reviewer persona."

The agent reads `agents/code-reviewer.md` and adopts a **Senior Staff Engineer** perspective.

**What happens:** The agent evaluates across:
1. **Correctness** — Does it do what the spec says? Edge cases? Race conditions?
2. **Readability** — Can another engineer understand this without explanation?
3. **Architecture** — Follows existing patterns? Appropriate abstraction level?
4. **Security** — Input validation? Secrets exposure? OWASP risks?
5. **Performance** — N+1 queries? Unnecessary renders? Memory leaks?

**Severity labels:** Nit → Optional → FYI → Must Fix

---

### 5. Security Audit

**You ask:**
> "Are there security issues in auth.ts?"
> "Audit this codebase for vulnerabilities."

**Skills triggered:**
- `security-and-hardening` — OWASP Top 10 prevention, auth patterns, secrets management

**Persona option (for deeper audit):**
> "Audit this as the security-auditor persona."

The agent reads `agents/security-auditor.md` and adopts a **Security Engineer** perspective.

**What happens:** The agent checks:
- Input validation and sanitization
- Authentication / authorization gaps
- Secrets in code or logs
- Dependency vulnerabilities
- CORS and security headers
- Error handling that leaks information

**References used:** `references/security-checklist.md`

---

### 6. Adding Tests

**You ask:**
> "Write tests for this feature."
> "What tests are missing for the checkout flow?"

**Skills triggered:**
- `test-driven-development` — Red-Green-Refactor, test pyramid, Beyonce Rule
- `browser-testing-with-devtools` — If browser-based (e2e, DOM, console, network)

**Persona option (for test strategy):**
> "Review test coverage as the test-engineer persona."

The agent reads `agents/test-engineer.md` and adopts a **QA Engineer** perspective.

**What happens:** The agent:
1. Identifies what's testable (pure logic → unit; boundary crossing → integration; critical flow → e2e)
2. Writes Arrange-Act-Assert tests
3. Names them descriptively (`it('rejects empty titles')` not `it('works')`)
4. Follows DAMP over DRY in tests
5. Prioritizes real implementations over mocks

**References used:** `references/testing-patterns.md`

---

### 7. Refactoring / Simplifying Code

**You ask:**
> "This code works but is hard to maintain. Simplify it."
> "Refactor this module."

**Skills triggered:**
- `code-simplification` — Chesterton's Fence, Rule of 500, reduce complexity while preserving behavior

**What happens:** The agent:
1. Documents current behavior (so it knows what to preserve)
2. Identifies complexity (nesting, duplication, mixed concerns)
3. Simplifies incrementally
4. Verifies tests still pass after each change
5. Never removes code without understanding why it exists

---

### 8. Performance Optimization

**You ask:**
> "The dashboard is slow. Optimize it."
> "Why is this API taking 3 seconds?"

**Skills triggered:**
- `performance-optimization` — Measure-first, profiling, bundle analysis
- `browser-testing-with-devtools` — Chrome DevTools MCP for runtime data

**What happens:** The agent:
1. Measures before optimizing (no guessing)
2. Profiles the bottleneck (network, database, render, compute)
3. Implements targeted fix
4. Verifies improvement with before/after metrics
5. References `references/performance-checklist.md`

---

### 9. Shipping to Production

**You ask:**
> "Deploy this to production."
> "Ship it."

**Skills triggered:**
- `shipping-and-launch` — Pre-launch checklists, feature flags, staged rollouts, rollback
- `ci-cd-and-automation` — Pipeline validation, Shift Left, quality gates
- `git-workflow-and-versioning` — Atomic commits, trunk-based development

**Persona orchestration (for high-stakes releases):**
> "Ship this. Run a full review first."

The agent fans out to:
- `code-reviewer` → review report
- `security-auditor` → audit report
- `test-engineer` → coverage report
- Main agent synthesizes → go/no-go decision + rollback plan

**What happens:** The agent:
1. Validates all tests pass
2. Checks CI/CD pipeline status
3. Verifies feature flags are configured
4. Plans staged rollout (canary → 10% → 50% → 100%)
5. Documents rollback procedure
6. Only then proceeds with deployment

---

### 10. Learning a New Framework / Technology

**You ask:**
> "How do I set up Playwright in this React project?"
> "I need to configure Azure API Management as an AI Gateway."

**Skills triggered:**
- Tier 2 domain skills (Playwright, Azure, Qiskit, Kubernetes, etc.)
- `source-driven-development` — Cite official docs, verify source, flag unverified claims

**What happens:** The agent:
1. Searches the vault for the exact domain skill
2. Reads `SKILL.md` and any included scripts/templates
3. Follows the official documentation steps
4. Provides exact commands, not generic advice

---

## Personas: When and How to Use Them

### What Personas Are

Personas (`agents/`) are **perspective shifts**. They don't add new workflows — they change *who* is doing the review.

| Persona | Perspective | Best For |
|---------|------------|----------|
| `code-reviewer` | Senior Staff Engineer | Thorough pre-merge review |
| `security-auditor` | Security Engineer | Vulnerability detection, OWASP audit |
| `test-engineer` | QA Engineer | Test strategy, coverage analysis, Prove-It pattern |

### How to Invoke Them

**Option 1 — Direct persona load (recommended for OpenCode):**
```
Review this PR as the code-reviewer persona.
```
The agent reads `agents/code-reviewer.md` and adopts that perspective for the current task.

**Option 2 — Load persona + skill together:**
```
Audit auth.ts for security issues as the security-auditor persona, following the security-and-hardening skill.
```

**Option 3 — Parallel review (manual orchestration):**
```
I need a full review before shipping:
1. Code review as code-reviewer
2. Security audit as security-auditor
3. Test coverage review as test-engineer
```
Run them sequentially in one session, or open multiple agent sessions.

> **Note:** Claude Code supports native subagent spawning (`/ship` command). OpenCode does not. In OpenCode, personas are loaded as context, not spawned as independent agents.

---

## References: Deep-Dive When Needed

### What References Are

References (`references/`) are **supplementary checklists and pattern libraries**. They are NOT loaded automatically. Skills mention them when relevant.

| Reference | Used By | Covers |
|-----------|---------|--------|
| `testing-patterns.md` | `test-driven-development` | Test structure, mocking, React/API/E2E examples |
| `security-checklist.md` | `security-and-hardening` | Pre-commit checks, auth, input validation, OWASP Top 10 |
| `performance-checklist.md` | `performance-optimization` | Core Web Vitals, frontend/backend checklists |
| `accessibility-checklist.md` | `frontend-ui-engineering` | Keyboard nav, screen readers, ARIA, WCAG |
| `orchestration-patterns.md` | `shipping-and-launch` | Persona composition, parallel fan-out, anti-patterns |

### How to Use Them

When a skill says *"See references/testing-patterns.md for examples,"* you can explicitly ask:
```
Read the testing-patterns reference and apply those patterns to this test suite.
```

Or ask the agent directly:
```
What does the security checklist say about input validation?
```

---

## What Doesn't Apply to OpenCode

| Feature | Status | Why |
|---------|--------|-----|
| `hooks/` (session-start, etc.) | **Not applicable** | Designed for Claude Code plugin lifecycle |
| `/.claude/commands/` | **Not applicable** | Claude Code slash commands; OpenCode uses natural language intent mapping |
| Subagent spawning | **Not applicable** | OpenCode doesn't support native subagents; load personas as context instead |

These are kept in the repo for Claude Code users but are ignored by OpenCode.

---

## Quick Reference Card

| Your Intent | Just Say... | What Gets Triggered |
|---|---|---|
| Build something | "Build a new feature for X" | `spec-driven-development` → `incremental-implementation` → `test-driven-development` |
| Fix a bug | "This is broken" or "Fix this error" | `debugging-and-error-recovery` + `test-driven-development` |
| Review code | "Review this PR" | `code-review-and-quality` |
| Security audit | "Audit for vulnerabilities" | `security-and-hardening` |
| Optimize performance | "This is slow" | `performance-optimization` |
| Refactor | "Simplify this code" | `code-simplification` |
| Ship to prod | "Deploy this" or "Ship it" | `shipping-and-launch` + `ci-cd-and-automation` + `git-workflow-and-versioning` |
| Learn a tool | "How do I set up X?" | Tier 2 domain skill (Azure, Playwright, Kubernetes, etc.) |
| Plan sprint | "What should I work on?" | `idea-refine` + `planning-and-task-breakdown` |

---

## Pro Tips for Maximum Effectiveness

### 1. Start Simple
Don't overthink it. The system is designed to intercept natural language. Just describe what you want.

### 2. Let the Agent Ask Questions
When `spec-driven-development` triggers, the agent will list assumptions and ask you to confirm them. **This is the feature, not a bug.** It prevents building the wrong thing.

### 3. Correct Assumptions Early
If the agent assumes PostgreSQL and you're using MongoDB, correct it immediately. The spec is a living document.

### 4. Use Personas for High-Stakes Tasks
For critical PRs or security-sensitive code, explicitly invoke the persona. It changes the rigor level.

### 5. Check the Logs
```bash
tail -f ~/.config/opencode/skill_vault.log
```
Watch `[LIFECYCLE]` and `[DOMAIN]` matches in real time. It helps you understand what's happening under the hood.

### 6. Add Your Own Skills
If you find yourself repeating the same instructions, create a skill:
```bash
mkdir organized-skills/my-custom-pattern
echo "# My Custom Pattern" > organized-skills/my-custom-pattern/SKILL.md
npm run build-index
```
It will be immediately searchable.

---

## Summary

Agent God Mode is designed to be **invisible infrastructure**. You don't think about skills. You think about your work. The agent figures out the rest.

| Layer | What You Do | What the Agent Does |
|---|---|---|
| **Tier 1** | Describe your task in natural language | Maps intent to lifecycle skills (specs, tests, reviews) |
| **Tier 2** | Mention a technology or domain | Searches the vault for exact domain knowledge |
| **Personas** | Say "as the code-reviewer persona" | Adopts a senior perspective from `agents/` |
| **References** | Ask for deeper patterns | Pulls checklists from `references/` on demand |

**The goal:** Every engineering task follows senior-level process, with instant access to specialized knowledge, at zero context cost.

---

*See also: [README.md](README.md) for setup and installation, [CREDITS.md](CREDITS.md) for attribution.*
