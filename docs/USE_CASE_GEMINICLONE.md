# Use Case: Planning GeminiClone with Agent God Mode

## Overview

This case study documents how **Agent God Mode's two-tier skill system** was used to plan and architect **GeminiClone** — a self-hosted, multi-provider AI chat application with deep research, multimodal generation, and social media research capabilities.

**Context:** The author wanted to stop paying for Gemini subscriptions while giving their wife (a PhD researcher) access to deep research with full control over models, data, and research breadth. The project needed to support any LLM provider, web search with anti-blocking, image/video generation via Azure Foundry, and social media research channels.

---

## Phase 1: Starting the Conversation (Tier 1 — Lifecycle Skills)

### Initial Prompt

> "I want to create a Gemini clone. I love OpenDesign because it uses opencode backend to select any provider and model. How difficult would it be to do something similar? I want to stop paying for Gemini. My wife uses deep research a lot. I want high reasoning loops, web searching, and fetching data. I also generate images and videos via Azure Foundry. Make sure to plan this properly."

### Skills Triggered Automatically

```
[LIFECYCLE] idea-refine           (100%)
[LIFECYCLE] spec-driven-development (100%)
[LIFECYCLE] planning-and-task-breakdown (100%)
```

### What Happened

The agent **did not start coding**. Instead, it followed `spec-driven-development` rigorously:

1. **Listed assumptions immediately:**
   - "This is a web application (not mobile)"
   - "Authentication uses email/password (not OAuth initially)"
   - "Backend is Node.js with TypeScript"
   - "SQLite for persistence, scalable later"

2. **Asked clarifying questions:**
   - Real-time vs. batched reasoning visibility?
   - Full autonomy or user confirmation at each step?
   - Max iteration depth for deep research?
   - Which search provider / anti-blocking approach?
   - Local use only or cloud deployment?

3. **Surfaced implicit requirements:**
   - The wife is a PhD researcher → social media research (Twitter, Reddit, LinkedIn) is critical
   - Azure Foundry already has image/video models → integration should be endpoint-configurable
   - Multi-user needed → authentication + per-user chat history

---

## Phase 2: Finding Domain Knowledge (Tier 2 — RAG Search)

As the conversation progressed, the agent searched the vault for specific technical domains:

### Search Query 1: "planning task breakdown Next.js LLM frontend architecture multimodal"

**Results:**
```
[DOMAIN] nextjs-app-router      (94%)
[DOMAIN] nextjs-authentication   (87%)
[DOMAIN] azure-container-apps    (82%)
```

**Impact:** The agent recommended Next.js 16 + React 18 for the frontend, and considered Azure Container Apps for deployment from day one.

### Search Query 2: "agentic reasoning loop deep research web search browsing multimodal"

**Results:**
```
[DOMAIN] webscraping-ai-automation (88%)
[DOMAIN] researching-web-skill     (85%)
[DOMAIN] azure-foundry             (91%)
```

**Impact:** The agent pulled in web scraping patterns and understood anti-blocking is a solved problem (Firecrawl, Jina AI, etc.). It also confirmed Azure Foundry patterns for multimodal generation.

### Search Query 3: "test driven development incremental implementation security hardening api interface design typescript express"

**Results:**
```
[LIFECYCLE] test-driven-development    (100%)
[LIFECYCLE] incremental-implementation (100%)
[LIFECYCLE] security-and-hardening     (100%)
[LIFECYCLE] api-and-interface-design   (100%)
```

**Impact:** The development approach was locked in:
- Tests FIRST (vitest, supertest)
- Thin vertical slices (one route → one service → one repository)
- Security from day one (bcrypt, helmet, rate limiting, JWT httpOnly cookies)
- Contract-first API design (Zod schemas, shared types package)

---

## Phase 3: Iteration & Refinement (Spec Alive)

The agent treated the spec as a **living document**. Key iterations:

| Iteration | Trigger | Change |
|---|---|---|
| 1 | User said "not Apple auth, just email/password" | Auth strategy simplified to bcrypt + JWT |
| 2 | User said "I don't have a domain" | Deployment target changed from custom domain → Azure Container Apps with auto-generated URL |
| 3 | User asked about Onyx Danswer | Deep research algorithm studied from Onyx (MIT license) and ported to TypeScript/Node.js |
| 4 | User mentioned Agent-Reach | Phase 4 added for social media research channels (Twitter, Reddit, LinkedIn) |
| 5 | User emphasized "SOLID principles, OOP, design patterns, TDD" | Architecture reinforced: Strategy Pattern for providers, Repository Pattern for data, Dependency Injection throughout |

---

## Phase 4: The Final Plan (5 Phases, Backwards from Goal)

The `planning-and-task-breakdown` skill decomposed the project into **5 vertical phases** with acceptance criteria for each task.

### Architecture Diagram

```
┌────────────── Browser (Next.js + Tailwind) ─────────────┐
│  Chat UI → Reasoning Panel → History Sidebar            │
│  Settings Panel → Provider Picker → Auth Panel          │
└───────────────────┬─────────────────────────────────────┘
                    │ SSE / REST
                    ▼
┌────────────── API Server (Express + TypeScript) ────────┐
│  Auth Middleware (JWT + bcrypt)                         │
│  Chat Controller → Chat Service → Conversation Repo     │
│  Provider Router (Strategy Pattern, OpenAI SDK universal)│
│  Deep Research Loop (Orchestrator + Research Agents)    │
│  Firecrawl Client → SQLite (better-sqlite3 WAL)         │
└─────────────────────────────────────────────────────────┘
```

### Phase Breakdown

| Phase | Scope | Key Skills Used |
|---|---|---|
| **Phase 1: Foundation** | Auth, chat, provider picker, basic streaming | `incremental-implementation`, `test-driven-development`, `api-and-interface-design` |
| **Phase 2: Deep Research** | Firecrawl, reasoning loop, citations, 10-iteration autonomy | `source-driven-development` (studied Onyx), `browser-testing-with-devtools` |
| **Phase 3: Multimodal** | Azure Foundry image/video gen, Blob Storage | Domain: `azure-foundry` |
| **Phase 4: Social Media** | Agent-Reach channels (Twitter, Reddit, LinkedIn) | Domain: `webscraping-ai-automation` |
| **Phase 5: Deployment** | Docker, Azure Container Apps | Domain: `azure-container-apps` |

---

## Key Design Decisions (Informed by Skills)

### 1. Provider Router — Strategy Pattern
**Skill:** `api-and-interface-design`

Instead of hardcoding providers, a universal config object:
```typescript
interface ProviderConfig {
  id: string;
  baseUrl: string;
  apiKey: string;
  model: string;
}
```
The `openai` SDK handles all providers via custom `baseURL` — same pattern OpenDesign uses.

### 2. Deep Research — Two-Loop Architecture
**Skill:** `source-driven-development` (studied Onyx MIT implementation)

- **Orchestrator Loop:** Breaks query into sub-tasks, delegates to parallel Research Agents (max 3), max 8 cycles.
- **Research Agent Loop:** Each agent searches → fetches → thinks → generates report, max 8 cycles.
- **Final Synthesis:** Collapses all reports into a comprehensive answer with citations.

### 3. Security — Zero Hardcoded Secrets
**Skill:** `security-and-hardening`

- JWT in httpOnly cookies (not localStorage)
- bcrypt for password hashing
- Helmet for security headers
- Rate limiting on all routes
- No secrets in code — everything via `.env` or admin UI

### 4. TDD — Every Module Tested First
**Skill:** `test-driven-development`

```
Auth:      2 tests (register, login)
Chat:      1 test (streaming)
Providers: 1 test (CRUD)
Research:  1 test (orchestrator loop)
Encryption: 1 test (round-trip)
```

---

## What the User Learned

| Lesson | Source Skill |
|---|---|
| "Don't start coding until the spec is validated" | `spec-driven-development` |
| "List assumptions before writing any spec content" | `spec-driven-development` |
| "Break into thin vertical slices" | `incremental-implementation` |
| "Write tests first, make them fail, then implement" | `test-driven-development` |
| "The user (or a slash command) is the orchestrator" | `agents/README.md` |
| "Skills are mandatory hops inside a persona's workflow" | `agents/README.md` |

---

## Result

**From vague idea to fully-specified, 5-phase plan:**
- ✅ Monorepo scaffolded (pnpm workspaces)
- ✅ SQLite schema defined
- ✅ Auth system specced (email/password, JWT)
- ✅ Provider router designed (Strategy Pattern, universal client)
- ✅ Deep research algorithm ported from Onyx
- ✅ 5 API test files written (failing first, then passing)
- ✅ Frontend components planned (AppShell, ChatView, ReasoningPanel, SettingsPanel, Sidebar)
- ✅ Deployment path defined (Docker → Azure Container Apps)

**All without writing a single line of production code first.**

---

## How You Can Use This Pattern

1. **Start with natural language.** "I want to build X."
2. **Let the agent ask questions.** The spec surfaces misunderstandings before code.
3. **Validate the spec.** Read it and say "yes" or "no, change Y."
4. **Watch the two-tier search.** `[LIFECYCLE]` for process, `[DOMAIN]` for knowledge.
5. **Follow the phases.** Don't implement Phase 3 before Phase 1 is done.
6. **Add your own skills.** If you repeat instructions, make a skill.

---

*This case study demonstrates how Agent God Mode's two-tier hybrid system combines software engineering lifecycle enforcement (specs, tests, architecture) with on-demand domain expertise (Next.js, Azure, web scraping, research algorithms) to turn vague ideas into production-ready plans.*
