import fs from 'fs';
import path from 'path';
import os from 'os';

function cosineSimilarity(vecA: number[], vecB: number[]) {
  let dotProduct = 0;
  let normA = 0;
  let normB = 0;
  for (let i = 0; i < vecA.length; i++) {
    dotProduct += vecA[i] * vecB[i];
    normA += vecA[i] ** 2;
    normB += vecB[i] ** 2;
  }
  if (normA === 0 || normB === 0) return 0;
  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

// Tier 1 lifecycle keywords for fast matching against skills in skills/
const LIFECYCLE_TRIGGERS: Record<string, string[]> = {
  'spec-driven-development': ['spec', 'specification', 'requirements', 'prd', 'plan feature', 'new project', 'new feature', 'design spec', 'write spec', 'architecture'],
  'planning-and-task-breakdown': ['plan', 'breakdown', 'tasks', 'roadmap', 'milestone', 'schedule', 'organize', 'structure work', 'task list', 'project plan'],
  'incremental-implementation': ['implement', 'build feature', 'add feature', 'development', 'coding', 'write code', 'create', 'slice', 'vertical slice'],
  'test-driven-development': ['test', 'tdd', 'testing', 'unit test', 'integration test', 'jest', 'vitest', 'pytest', 'mocha', 'coverage'],
  'debugging-and-error-recovery': ['debug', 'bug', 'error', 'fix', 'crash', 'failure', 'exception', 'broken', 'not working', 'troubleshoot'],
  'code-review-and-quality': ['review', 'pr review', 'code review', 'refactor', 'quality', 'lint', 'smell', 'improve code', 'peer review'],
  'code-simplification': ['simplify', 'cleanup', 'clean up', 'reduce complexity', 'delete code', 'remove dead code', 'streamline'],
  'security-and-hardening': ['security', 'secure', 'auth', 'authentication', 'authorization', 'owasp', 'sanitize', 'injection', 'vulnerability', 'xss', 'csrf'],
  'performance-optimization': ['performance', 'optimize', 'speed', 'fast', 'slow', 'latency', 'memory leak', 'profiling', 'benchmark', 'bundle size'],
  'frontend-ui-engineering': ['frontend', 'ui', 'react', 'vue', 'angular', 'html', 'css', 'component', 'design system', 'tailwind', 'responsive', 'accessibility'],
  'api-and-interface-design': ['api', 'rest', 'graphql', 'endpoint', 'swagger', 'openapi', 'contract', 'interface', 'dto', 'schema'],
  'source-driven-development': ['documentation', 'docs', 'official docs', 'framework version', 'verify source', 'cite', 'reference'],
  'context-engineering': ['context', 'prompt engineering', 'mcp', 'system prompt', 'custom instructions', 'rules file', 'context packing'],
  'browser-testing-with-devtools': ['devtools', 'chrome', 'browser', 'e2e', 'playwright', 'cypress', 'selenium', 'dom', 'console', 'network tab'],
  'git-workflow-and-versioning': ['git', 'commit', 'branch', 'merge', 'rebase', 'workflow', 'semantic version', 'changelog', 'release'],
  'ci-cd-and-automation': ['ci', 'cd', 'pipeline', 'github actions', 'gitlab ci', 'jenkins', 'deploy', 'docker', 'kubernetes', 'automation'],
  'shipping-and-launch': ['ship', 'launch', 'production', 'prod', 'release', 'deploy to prod', 'go live', 'rollout', 'rollback', 'feature flag'],
  'deprecation-and-migration': ['deprecate', 'migration', 'sunset', 'remove', 'legacy', 'upgrade', 'migrate', 'breaking change'],
  'documentation-and-adrs': ['adr', 'architecture decision', 'design doc', 'runbook', 'readme', 'api doc', 'inline doc', 'comment'],
  'idea-refine': ['ideate', 'brainstorm', 'idea', 'concept', 'refine', 'explore', 'discover', 'prototype'],
};

function detectLifecycleMatches(query: string): string[] {
  const lower = query.toLowerCase();
  const matches: string[] = [];
  for (const [skill, triggers] of Object.entries(LIFECYCLE_TRIGGERS)) {
    for (const trigger of triggers) {
      if (lower.includes(trigger)) {
        matches.push(skill);
        break;
      }
    }
  }
  return [...new Set(matches)];
}

async function search(query: string, vaultDir: string) {
  const indexPath = '/Users/luisvalencia/Documents/ClaudeCodeRepos/index.json';
  const logPath = path.join(os.homedir(), '.config', 'opencode', 'skill_vault.log');
  const timestamp = new Date().toISOString();

  try { fs.appendFileSync(logPath, `[${timestamp}] 🔍 WORKER QUERY: "${query}"\n`); } catch(e) {}

  if (!fs.existsSync(indexPath)) {
    console.error(JSON.stringify({ error: `Index not found at ${indexPath}` }));
    process.exit(1);
  }

  const indexData = JSON.parse(fs.readFileSync(indexPath, 'utf-8'));
  const results: { tag: string; path: string; name: string; score: number }[] = [];

  // Pass 1: Lifecycle detection
  const lifecycleMatches = detectLifecycleMatches(query);
  for (const skillName of lifecycleMatches) {
    const entry = indexData.find((s: any) => s.name === skillName && s.path.startsWith('skills/'));
    if (entry) {
      results.push({ tag: 'LIFECYCLE', path: path.join('/Users/luisvalencia/Documents/ClaudeCodeRepos', entry.path), name: entry.name, score: 1.0 });
    }
  }

  // Pass 2: Domain RAG
  try {
    const { pipeline } = await import('@xenova/transformers');
    const extractor = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');
    const output = await extractor(query, { pooling: 'mean', normalize: true });
    const queryEmbedding = Array.from(output.data as Float32Array);

    const scored = indexData
      .filter((s: any) => s.embedding && s.embedding.length > 0)
      .map((s: any) => ({ ...s, score: cosineSimilarity(queryEmbedding, s.embedding) }));

    scored.sort((a: any, b: any) => b.score - a.score);
    const already = new Set(results.map(r => r.name));
    for (const s of scored) {
      if (s.score < 0.2) break;
      if (already.has(s.name)) continue;
      results.push({ tag: 'DOMAIN', path: path.join('/Users/luisvalencia/Documents/ClaudeCodeRepos', s.path), name: s.name, score: s.score });
      if (results.filter(r => r.tag === 'DOMAIN').length >= 3) break;
    }
  } catch (err: any) {
    try { fs.appendFileSync(logPath, `[${timestamp}] ⚠️ WORKER EMBEDDING ERROR: ${err.message}\n`); } catch(e) {}
  }

  try { fs.appendFileSync(logPath, `[${timestamp}] ✅ WORKER RESULTS: ${results.length} matches\n\n`); } catch(e) {}
  return results;
}

// CLI entry point
const query = process.argv[2];
const vaultDir = process.argv[3] || process.cwd();

if (!query) {
  console.error(JSON.stringify({ error: 'Usage: node skill_search_worker.mjs "<query>" [vaultDir]' }));
  process.exit(1);
}

search(query, vaultDir).then(results => {
  console.log(JSON.stringify(results));
}).catch(err => {
  console.error(JSON.stringify({ error: err.message }));
  process.exit(1);
});
