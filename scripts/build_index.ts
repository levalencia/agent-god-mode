const fs = require('fs');
const path = require('path');
const { globSync } = require('glob');
const matter = require('gray-matter');

const SKILLS_DIRS = [
  path.join(__dirname, '../skills'),
  path.join(__dirname, '../organized-skills'),
];
const OUTPUT_FILE = path.join(__dirname, '../index.json');

async function buildIndex() {
  const { pipeline } = await import('@xenova/transformers');
  
  console.log(`Loading local embedding model (Xenova/all-MiniLM-L6-v2)...`);
  console.log(`This may take a minute on the first run as it downloads the model (approx 22MB).`);
  
  const extractor = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');

  const allFiles: string[] = [];
  for (const dir of SKILLS_DIRS) {
    const files = globSync(`${dir}/**/SKILL.md`);
    allFiles.push(...files);
    console.log(`Found ${files.length} SKILL.md files in ${dir}`);
  }

  console.log(`Total: ${allFiles.length} skills. Parsing frontmatter...`);

  const skills = [];

  for (const file of allFiles) {
    try {
      const content = fs.readFileSync(file, 'utf-8');
      const parsed = matter(content);
      const name = parsed.data.name || path.basename(path.dirname(file));
      const description = parsed.data.description || '';

      if (!description) {
        continue;
      }

      skills.push({
        name,
        description,
        path: path.relative(path.join(__dirname, '..'), file),
      });
    } catch (e) {
      console.error(`Error parsing ${file}:`, e);
    }
  }

  console.log(`Successfully parsed ${skills.length} skills.`);
  console.log(`Generating local embeddings... this might take a moment depending on your CPU.`);
  
  for (let i = 0; i < skills.length; i++) {
    const skill = skills[i];
    if (i % 100 === 0) {
       console.log(`Processing ${i} / ${skills.length}...`);
    }
    
    try {
      const output = await extractor(`Name: ${skill.name}\nDescription: ${skill.description}`, {
        pooling: 'mean',
        normalize: true,
      });
      skill.embedding = Array.from(output.data);
    } catch (error) {
      console.error(`Error generating embedding for ${skill.name}:`, error);
    }
  }

  console.log(`Saving index to ${OUTPUT_FILE}...`);
  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(skills, null, 2));
  console.log('Done!');
}

buildIndex().catch(console.error);
