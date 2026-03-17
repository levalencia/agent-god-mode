import skillTool from './tools/skill_search';

async function runTest() {
  console.log("Testing skill_search tool with query: 'deploy azure postgres'");
  try {
    const result = await skillTool.execute(
      { query: "deploy azure postgres" },
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
