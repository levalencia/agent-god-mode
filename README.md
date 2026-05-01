# ⚡️ Agent God Mode

> **Turn your AI coding assistant into an Omni-Agent. Give OpenCode & Claude Code 2,300+ domain skills + 20 production-grade engineering workflows without nuking your context window or bankrupting your API costs.**

Imagine giving your AI coding agent a Ph.D. in Quantum Computing, an MBA in Product Marketing, and a Senior Staff DevOps certification—all at the same time. 

Normally, loading thousands of custom prompt "skills" into an agent causes catastrophic **Context Bloat**: it consumes tens of thousands of tokens, skyrockets your API costs, and makes the AI confused and sluggish.

**Agent God Mode solves this.** 

We built a **100% Local Retrieval-Augmented Generation (RAG) architecture** that completely bypasses the native skill-discovery limits. Using an isolated background worker and local AI embeddings, your agent can now dynamically search, discover, and inject exactly the knowledge it needs, *precisely when it needs it*.

---

## 🛑 The Problem: Death by a Thousand Skills

Both [OpenCode](https://opencode.ai) and [Claude Code](https://github.com/anthropics/claude-code) support custom "Skills" (instructions and workflows) placed in global directories (`~/.agents/skills/`). 

However, their native implementation dynamically reads the `name` and `description` of **every single skill** into the LLM's system prompt on every turn. If you have 5 skills, this is fine. If you have **2,000+ skills**:
1. 📉 **Token Bankruptcy:** It consumes 30,000+ tokens before you even type "Hello".
2. 💸 **Skyrocketing Costs:** You pay for those tokens on every single message.
3. 🧠 **LLM Confusion:** The agent gets overwhelmed by thousands of irrelevant instructions.

## 📖 Day-to-Day Usage

New to Agent God Mode? Start here: **[docs/USAGE.md](docs/USAGE.md)** — a complete guide mapping real work scenarios (building features, fixing bugs, code reviews, shipping, learning new tech) to the right skills and personas.

## 💡 The Solution: Two-Tier Hybrid Architecture

This repository combines two powerful systems into a single, zero-bloat skill architecture:

### Tier 1 — Lifecycle Skills (`skills/`)
20 production-grade engineering skills from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) that enforce *how* software is built. These cover the entire SDLC:
- **DEFINE** → `spec-driven-development`
- **PLAN** → `planning-and-task-breakdown`
- **BUILD** → `incremental-implementation`, `test-driven-development`
- **VERIFY** → `debugging-and-error-recovery`
- **REVIEW** → `code-review-and-quality`
- **SHIP** → `shipping-and-launch`

### Tier 2 — Domain Skills (`organized-skills/`)
2,300+ specialized skills covering *what* to build in specific contexts: Azure, AWS, Kubernetes, Qiskit, marketing, design, security, and thousands more.

### How It Works
1. **Total Isolation:** Both tiers are kept outside the agent's default prompt to prevent context bloat.
2. **Free, Local Embeddings:** A setup script uses `@xenova/transformers` to generate lightweight, private vectors on your CPU. No OpenAI/Anthropic API keys required.
3. **Two-Pass Search:** The agent first checks for lifecycle intent (specs, testing, shipping), then runs a RAG embedding search for domain knowledge.
4. **Sandbox-Bypassing Worker:** A background Node.js worker (`skill_search_worker.mjs`) safely calculates cosine similarity outside the sandbox.
5. **Just-In-Time Injection:** The agent receives exactly the skills it needs — process skills *and* domain skills — precisely when it needs them.

---

## 🚀 Setup & Installation

### Prerequisites
- Node.js & npm
- [OpenCode](https://opencode.ai) OR [Claude Code](https://github.com/anthropics/claude-code) installed.

### 1. Clone & Build the Index (All Platforms)
```bash
git clone https://github.com/levalencia/agent-god-mode.git
cd agent-god-mode
npm install
```

Run the indexer. This downloads a tiny (~22MB) embedding model directly to your machine and processes all ~2,323 skills (20 lifecycle + 2,300+ domain) into a local vector database.
```bash
npm run build-index
```
*(This generates an `index.json` file in the project root).*

---

### 2. Configure Your Agent

**OpenCode** natively supports custom `.ts` tools, so we install the tool directly into its configuration directory. **Claude Code** does not natively support `.ts` tools, but we can teach it to use its native `bash` capability to run our background worker directly!

Choose your setup below:

#### ⚡️ OpenCode (Mac/Linux)
1. Install the tool and worker script:
   ```bash
   mkdir -p ~/.config/opencode/tools
   cp tools/skill_search.ts ~/.config/opencode/tools/
   cp tools/skill_search_worker.mjs ~/.config/opencode/tools/
   ```
2. **Update Absolute Paths:** Open `~/.config/opencode/tools/skill_search.ts` and `~/.config/opencode/tools/skill_search_worker.mjs` and update `const VAULT_DIR = ...` to point to the exact absolute path where you cloned this repository.
3. Install dependencies globally for the worker:
   ```bash
   cd ~/.config/opencode
   npm install @xenova/transformers
   ```
4. Enforce the rule:
   ```bash
   cat rules/AGENTS.md >> ~/.config/opencode/AGENTS.md
   ```

#### ⚡️ OpenCode (Windows PowerShell)
1. Install the tool and worker script:
   ```powershell
   New-Item -Path $env:USERPROFILE\.config\opencode\tools -ItemType Directory -Force
   Copy-Item tools\* -Destination $env:USERPROFILE\.config\opencode\tools\
   ```
2. **Update Absolute Paths:** Open `%USERPROFILE%\.config\opencode\tools\skill_search.ts` and `%USERPROFILE%\.config\opencode\tools\skill_search_worker.mjs` and update `const VAULT_DIR = ...` to point to the exact absolute path where you cloned this repository (e.g., `C:\\Users\\Name\\Projects\\agent-god-mode`).
3. Install dependencies globally for the worker:
   ```powershell
   cd $env:USERPROFILE\.config\opencode
   npm install @xenova/transformers
   ```
4. Enforce the rule:
   ```powershell
   Get-Content rules\AGENTS.md | Add-Content -Path $env:USERPROFILE\.config\opencode\AGENTS.md
   ```

#### ⚡️ Claude Code (Mac/Linux)
1. Open the `.clauderules` file (or your global `claude.json` custom prompt).
2. Append the contents of `rules/CLAUDE_CODE_RULE.md` to your prompt.
   *Note: Make sure to update the absolute path to `skill_search_worker.mjs` inside that rule before applying it!*
3. Install the required dependency in your project or globally:
   ```bash
   npm install -g @xenova/transformers
   ```

#### ⚡️ Claude Code (Windows)
1. Open your project's `.clauderules` file.
2. Append the contents of `rules/CLAUDE_CODE_RULE.md` to your prompt.
   *Note: Update the absolute path to point to `node C:\\path\\to\\agent-god-mode\\skill_search_worker.mjs`.*
3. Install the required dependency:
   ```powershell
   npm install -g @xenova/transformers
   ```

---

## 🧪 Testing & Proving It Works

Because AI agents run in the background, you might wonder: *"Is it actually using the vault?"*

We built **file-based logging** so you can watch the agent "think" in real-time. 

### Step 1: Tail the Logs
Open a separate terminal window and run this command. Leave it open.
* **Mac/Linux:** `tail -f ~/.config/opencode/skill_vault.log`
* **Windows (PowerShell):** `Get-Content $env:USERPROFILE\.config\opencode\skill_vault.log -Wait`

### Step 2: Trigger the Agent
In your main terminal, open your agent (`opencode` or `claude`) and paste a complex prompt. Watch the log window instantly light up with vector search results!

---

## 🔥 Complex Examples (The Proof)

Here are three massive, cross-disciplinary prompts that prove the agent is dynamically loading highly-specialized skills on demand.

### Example 1: The Full-Stack Feature Build (Two-Tier in Action)
**You Ask:**
> "Build a new authentication feature for my Azure Container Apps project. Use best practices."

**What Happens in the Logs:**
```text
[2026-04-30T10:15:08.690Z] 🔍 QUERY RECEIVED: "Build a new authentication feature for my Azure Container Apps project"
[2026-04-30T10:15:08.690Z] ✅ MATCHES FOUND:
    [LIFECYCLE] spec-driven-development (100.0%)
    [LIFECYCLE] test-driven-development (100.0%)
    [LIFECYCLE] incremental-implementation (100.0%)
    [DOMAIN] azure-container-apps (91.2%)
    [DOMAIN] security-and-hardening (87.5%)
```
**The Result:** The agent doesn't just start coding. It follows `spec-driven-development` to write a PRD first, uses `test-driven-development` to write failing tests, and references the `azure-container-apps` + `security-and-hardening` skills for the exact Bicep/Terraform and auth patterns. Two-tier architecture ensures process *and* domain expertise.

### Example 2: The Enterprise DevOps Architect
**You Ask:**
> "I need to configure Azure API Management as an AI Gateway for my MCP tools with semantic caching."

**What Happens in the Logs:**
```text
[2026-04-30T07:45:08.690Z] 🔍 QUERY RECEIVED: "configure Azure API Management AI Gateway MCP tools semantic caching"
[2026-04-30T07:45:08.690Z] ✅ MATCHES FOUND:
    [DOMAIN] azure-aigateway (94.3%)
    [DOMAIN] azure-devops (43.5%)
    [DOMAIN] az-aks-agent (39.3%)
```
**The Result:** The agent bypasses generic advice, reads the specific Azure DevOps guidelines, and outputs the exact XML policy configurations for semantic caching.

### Example 3: The Quantum Scientist
**You Ask:**
> "I need to build a quantum circuit using Qiskit that implements Grover's algorithm to search an unstructured database."

**What Happens in the Logs:**
```text
[2026-04-30T08:12:14.221Z] 🔍 QUERY RECEIVED: "Qiskit quantum circuit Grover's algorithm unstructured database"
[2026-04-30T08:12:14.221Z] ✅ MATCHES FOUND:
    [DOMAIN] qiskit (74.2%)
    [DOMAIN] scientific-brainstorming (41.1%)
    [DOMAIN] python-data-science (38.5%)
```
**The Result:** The agent dynamically loads the `qiskit` skill, pulling in the precise mathematical formulations and Python syntax required to initialize the superposition and amplitude amplification steps.

### Example 4: The Growth Marketer
**You Ask:**
> "We are starting a new marketing project and need to establish our tone of voice, visual identity, and typography rules. How should we set up our brand guidelines document?"

**What Happens in the Logs:**
```text
[2026-04-30T08:15:33.901Z] 🔍 QUERY RECEIVED: "tone of voice visual identity typography brand guidelines marketing"
[2026-04-30T08:15:33.901Z] ✅ MATCHES FOUND:
    [DOMAIN] brand-guidelines (68.9%)
    [DOMAIN] campaign-brief-generator (55.4%)
    [DOMAIN] ux-design-patterns (49.2%)
```
**The Result:** The agent abandons "coding mode" entirely, adopting the persona of an expert Brand Strategist to structure your brand pillars, tone matrix, and hex color constraints.

---

## 🛠️ Uninstallation & Rollback
If you ever want to remove this tool and return your agent to its default behavior:

```bash
# 1. Remove the custom tools
rm ~/.config/opencode/tools/skill_search.ts
rm ~/.config/opencode/tools/skill_search_worker.mjs

# 2. Remove the rule (manually delete the "Skill Vault Search Protocol" section from your AGENTS.md)
nano ~/.config/opencode/AGENTS.md

# 3. Clean up the log file
rm ~/.config/opencode/skill_vault.log
```

---

## 🌍 Contributing (Add Your Own Skills!)

**Agent God Mode is 100% Open Source and community-driven.** 
We want to build the largest, most powerful library of AI agent skills on the internet. Have a highly specialized workflow, custom system prompt, or framework? Add it to the vault!

### How to Contribute a Skill
1. **Fork the repo** and clone it locally.
2. **Decide which tier your skill belongs to:**
   - **Tier 1 (`skills/`)**: Only for broad, software engineering lifecycle skills (specs, testing, reviews, shipping). These must follow the format of [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills).
   - **Tier 2 (`organized-skills/`)**: For domain-specific, framework, or tool-specific skills (Azure, Qiskit, marketing, etc.).
3. **Create a new folder** inside the appropriate directory. Name it descriptively (e.g., `kubernetes-expert-troubleshooter`).
4. **Add your `SKILL.md` file** inside that folder. This file should contain the actual instructions, rules, and workflows you want the agent to adopt. *(Feel free to include reference files, templates, or code snippets in the same folder!)*
5. **Test it locally (Optional):** Run `npm run build-index` to rebuild the vector database and ensure your skill gets embedded correctly.
6. **Commit, Push, and PR:**
   ```bash
   git checkout -b feature/add-awesome-skill
   git add .
   git commit -m "Add [Skill Name] to the vault"
   git push origin feature/add-awesome-skill
   ```
7. **Open a Pull Request!** We will review your skill and merge it into the global vault for everyone to use.

---

## 🤝 Credits & Origins

This repository is an **aggregation, curation, and optimization effort**. The skills within were not all written from scratch by the authors of this repository.

### Tier 1: Lifecycle Skills
The 20 production-grade engineering skills in `skills/`, `agents/`, `references/`, and `hooks/` are from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) by Addy Osmani, used under the MIT License. They were integrated to provide structured software engineering lifecycle enforcement.

### Tier 2: Domain Skills
The 2,300+ skills in `organized-skills/` were carefully collected, standardized, and organized from various incredible open-source communities, prompt libraries, and the official baseline skill repositories from projects like Claude Code and OpenCode.

### Original Repositories
We extend our deepest gratitude to the creators of the following repositories, whose work forms the foundation of this vault:
- [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
- [BehiSecc/awesome-claude-skills](https://github.com/BehiSecc/awesome-claude-skills)
- [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice)
- [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)
- [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)
- [twostraws/Swift-Agent-Skills](https://github.com/twostraws/Swift-Agent-Skills)
- [miles990/claude-software-skills](https://github.com/miles990/claude-software-skills)
- [giuseppe-trisciuoglio/developer-kit-claude-code](https://github.com/giuseppe-trisciuoglio/developer-kit-claude-code)
- [glebis/claude-skills](https://github.com/glebis/claude-skills)
- [julianobarbosa/claude-code-skills](https://github.com/julianobarbosa/claude-code-skills)
- [levnikolaevich/claude-code-skills](https://github.com/levnikolaevich/claude-code-skills)
- [ratacat/claude-skills](https://github.com/ratacat/claude-skills)
- [deanpeters/Product-Manager-Skills](https://github.com/deanpeters/Product-Manager-Skills)
- [athina-ai/goose-skills](https://github.com/athina-ai/goose-skills)
- [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills)
- [product-on-purpose/pm-skills](https://github.com/product-on-purpose/pm-skills)
- [ZeroLu/Ultimate-AI-Media-Generator-Skill](https://github.com/ZeroLu/Ultimate-AI-Media-Generator-Skill)
- [digitalsamba/claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit)
- [guinacio/claude-image-gen](https://github.com/guinacio/claude-image-gen)
- [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit)
- [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills)
- [trailofbits/skills](https://github.com/trailofbits/skills)
- [karanb192/awesome-claude-skills](https://github.com/karanb192/awesome-claude-skills)
- [mhylle/claude-skills-collection](https://github.com/mhylle/claude-skills-collection)
- [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills)
- [marketcalls/vectorbt-backtesting-skills](https://github.com/marketcalls/vectorbt-backtesting-skills)
- [ajeeshworkspace/indian-trading-skills](https://github.com/ajeeshworkspace/indian-trading-skills)

By grouping these open-source resources into a scalable RAG architecture, our goal is to amplify their usefulness for the developer community. If you recognize a skill you authored and would like explicit attribution on the file or wish for it to be removed, please open an issue!

---
*Built to make AI coding agents truly unstoppable. 100% Local. 100% Free.* 🚀
