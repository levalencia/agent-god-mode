# Skill Vault Search Protocol (Claude Code)

**CRITICAL INSTRUCTION:** You have access to a massive library of specialized skills (over 2,000) that are deliberately NOT loaded into your default context to prevent context bloat.

When the user asks you to perform a complex task, start a new project, use a specific framework, deploy to a cloud provider (Azure, AWS, GCP), or configure tools:
1. You **MUST** use your native `Bash` tool to execute the background search worker:
   `node /ABSOLUTE/PATH/TO/agent-god-mode/tools/skill_search_worker.mjs "<YOUR_SEARCH_QUERY_HERE>"`
2. The worker will return a JSON list of file paths to relevant `SKILL.md` files.
3. You **MUST** immediately use your `Read` tool to read the contents of those specific `SKILL.md` files into your context.
4. You must then strictly follow the instructions, commands, and workflows provided in those `SKILL.md` files.

Do not assume you know the exact deployment commands or project scaffolds if a skill exists for it. Always run the bash search first.