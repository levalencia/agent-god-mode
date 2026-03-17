import skillTool from './tools/skill_search';

async function runTest() {
  console.log("Testing skill_search tool with query: 'postgres query optimization'");
  try {
    const result = await skillTool.execute(
      { query: "postgres query optimization" },
      { worktree: process.cwd() }
    );
    console.log("\n--- RESULT ---");
    console.log(result);
    console.log("--------------\n");
  } catch (e) {
    console.error("Test failed:", e);
  }
}

runTest();
