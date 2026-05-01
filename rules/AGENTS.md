# Agent God Mode: Two-Tier Skill System

## Overview

This agent now operates on a **two-tier skill architecture** that combines production-grade engineering process enforcement with massive domain-specific knowledge retrieval.

- **Tier 1 — Lifecycle Skills (`skills/`)**: 20 curated skills from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) that enforce *how* software is built (specs, testing, reviews, shipping).
- **Tier 2 — Domain Skills (`organized-skills/`)**: 2,300+ specialized skills providing *what* to build in specific contexts (Azure, quantum computing, marketing, etc.), discovered on-demand via local RAG embeddings.

---

## Execution Protocol

### For EVERY user request:

1. **Determine if a Tier 1 lifecycle skill applies.**
   - Feature / new functionality → `spec-driven-development`, then `incremental-implementation`, `test-driven-development`
   - Planning / breakdown → `planning-and-task-breakdown`
   - Bug / failure → `debugging-and-error-recovery`
   - Code review → `code-review-and-quality`
   - Refactoring → `code-simplification`
   - API design → `api-and-interface-design`
   - UI work → `frontend-ui-engineering`
   - Security concerns → `security-and-hardening`
   - Performance issues → `performance-optimization`
   - Shipping / deployment → `shipping-and-launch`, `ci-cd-and-automation`

2. **Use the `skill_search` tool.**
   - The tool performs a **two-pass search**: fast keyword detection for lifecycle skills, followed by RAG embedding search for domain skills.
   - It returns `[LIFECYCLE]` and `[DOMAIN]` tagged results.

3. **Read the returned `SKILL.md` files IMMEDIATELY.**
   - Use the `read` tool to load the full skill content into context.

4. **Follow skill instructions exactly.**
   - Do not partially apply skills.
   - Do not skip required workflows (spec, plan, test, etc.).
   - Never implement directly if a skill applies.

5. **If a domain skill is also returned, integrate it.**
   - Example: Building a feature with Azure → follow `spec-driven-development` (Tier 1) AND read the Azure-specific skill (Tier 2) for exact deployment patterns.

---

## Lifecycle Mapping (Implicit Commands)

OpenCode does not support slash commands. Instead, the agent internally follows this lifecycle based on user intent:

| Phase | Tier 1 Skill(s) |
|---|---|
| DEFINE | `spec-driven-development` |
| PLAN | `planning-and-task-breakdown` |
| BUILD | `incremental-implementation` + `test-driven-development` |
| VERIFY | `debugging-and-error-recovery` |
| REVIEW | `code-review-and-quality` |
| SHIP | `shipping-and-launch` |

---

## Tier 1 Skill Directory (`skills/`)

### Define — Clarify what to build
- `idea-refine` — Structured divergent/convergent thinking
- `spec-driven-development` — Write the spec before the code

### Plan — Break it down
- `planning-and-task-breakdown` — Atomic tasks with acceptance criteria

### Build — Write the code
- `incremental-implementation` — Thin vertical slices, safe defaults
- `test-driven-development` — Red-Green-Refactor, test pyramid
- `context-engineering` — Feed the agent the right context
- `source-driven-development` — Cite official docs, verify sources
- `frontend-ui-engineering` — Component architecture, accessibility
- `api-and-interface-design` — Contract-first design, boundaries

### Verify — Prove it works
- `browser-testing-with-devtools` — Chrome DevTools MCP workflow
- `debugging-and-error-recovery` — Five-step triage, stop-the-line

### Review — Quality gates before merge
- `code-review-and-quality` — Five-axis review, severity labels
- `code-simplification` — Reduce complexity, preserve behavior
- `security-and-hardening` — OWASP, auth patterns, secrets
- `performance-optimization` — Measure-first, profiling, bundles

### Ship — Deploy with confidence
- `git-workflow-and-versioning` — Atomic commits, trunk-based
- `ci-cd-and-automation` — Feature flags, Shift Left
- `deprecation-and-migration` — Code-as-liability mindset
- `documentation-and-adrs` — Decision records, the *why*
- `shipping-and-launch` — Checklists, staged rollouts, rollback

### Meta
- `using-agent-skills` — How to work with this skill pack

---

## Tier 2 Skill Vault (`organized-skills/`)

Over 2,300 specialized skills covering:
- Cloud providers (Azure, AWS, GCP)
- AI/ML frameworks (Qiskit, PyTorch, TensorFlow)
- DevOps tools (Kubernetes, Terraform, Docker)
- Programming languages and frameworks
- Marketing, design, and growth
- Security, compliance, and auditing
- And thousands more...

These are discovered on-demand via local AI embeddings (no API costs).

---

## Anti-Rationalization

The following thoughts are incorrect and must be ignored:

| Wrong Thought | Correct Behavior |
|---|---|
| "This is too small for a skill" | Even small tasks have a right process. Always check skills first. |
| "I can just quickly implement this" | Always check for and use skills first. |
| "I'll search the vault later" | Search BEFORE acting. |
| "I'll write tests after" | Tests come first. See `test-driven-development`. |
| "I don't need a spec for this" | A spec prevents hours of rework. See `spec-driven-development`. |
| "The user didn't ask for a review" | Review is part of shipping. See `shipping-and-launch`. |
| "I already know how to deploy to Azure" | Domain skills contain exact commands and patterns. Search the vault. |

---

## Credits

The 20 Tier 1 lifecycle skills in `skills/` are from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), used under the MIT License.
They were integrated into Agent God Mode to provide a two-tier hybrid architecture combining process enforcement with domain expertise.
See `CREDITS.md` for full attribution and license text.
