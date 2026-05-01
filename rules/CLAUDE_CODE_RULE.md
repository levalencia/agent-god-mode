# Skill Vault Search Protocol (Claude Code)

**CRITICAL INSTRUCTION:** You have access to a massive two-tier skill system.

- **Tier 1 (`skills/`)**: 20 production-grade lifecycle skills (specs, testing, reviews, shipping) from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills).
- **Tier 2 (`organized-skills/`)**: 2,300+ domain skills (Azure, quantum, marketing, etc.) discovered on-demand via local embeddings.

When the user asks you to perform a complex task, start a new project, use a specific framework, deploy to a cloud provider (Azure, AWS, GCP), or configure tools:

1. You **MUST** use your native `Bash` tool to execute the background search worker:
   `node /ABSOLUTE/PATH/TO/agent-god-mode/tools/skill_search_worker.mjs "<YOUR_SEARCH_QUERY_HERE>" /ABSOLUTE/PATH/TO/agent-god-mode`
2. The worker returns a JSON list of file paths to relevant `SKILL.md` files, tagged as `[LIFECYCLE]` or `[DOMAIN]`.
3. You **MUST** immediately use your `Read` tool to read the contents of those specific `SKILL.md` files into your context.
4. Follow Tier 1 (lifecycle) skills exactly. Integrate Tier 2 (domain) skills for specialized knowledge.
5. For pure engineering tasks, always check `skills/` first via the worker before acting.

Do not assume you know the exact deployment commands or project scaffolds if a skill exists for it. Always run the search first.
