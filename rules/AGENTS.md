# Skill Vault Search Protocol

**CRITICAL INSTRUCTION:** You have access to a massive library of specialized skills (over 2,000) that are deliberately NOT loaded into your default context to prevent context bloat.

When the user asks you to perform a complex task, start a new project, use a specific framework, deploy to a cloud provider (Azure, AWS, GCP), or configure tools:
1. You **MUST** first use the `skill_search` tool with a specific query related to the user's task.
2. If the `skill_search` tool returns file paths to `SKILL.md` files, you **MUST** immediately use your `read` tool to read the contents of those files into your context.
3. You must then strictly follow the instructions, commands, and workflows provided in those `SKILL.md` files.

Do not assume you know the exact deployment commands or project scaffolds if a skill exists for it. Always search the vault first.
