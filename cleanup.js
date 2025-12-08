// cleanup.js
// Ceremonial Sovereign Companion Cleanup Protocol
// Purpose: Move or rename template files so TypeScript ignores them

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const TEMPLATE_DIR = path.join(__dirname, "templates");
const ARCHIVE_DIR = path.join(__dirname, "templates-archived");

// Ensure archive directory exists
if (!fs.existsSync(ARCHIVE_DIR)) {
  fs.mkdirSync(ARCHIVE_DIR, { recursive: true });
}

// Recursively process directory
function processDirectory(dir, archiveBase) {
  if (!fs.existsSync(dir)) {
    console.log(`Directory not found: ${dir}`);
    return;
  }

  const entries = fs.readdirSync(dir, { withFileTypes: true });

  entries.forEach(entry => {
    const sourcePath = path.join(dir, entry.name);
    const relativePath = path.relative(TEMPLATE_DIR, sourcePath);

    if (entry.isDirectory()) {
      // Recursively process subdirectories
      const subArchiveDir = path.join(archiveBase, entry.name);
      if (!fs.existsSync(subArchiveDir)) {
        fs.mkdirSync(subArchiveDir, { recursive: true });
      }
      processDirectory(sourcePath, subArchiveDir);
    } else if (entry.name.endsWith(".ts") || entry.name.endsWith(".tsx")) {
      // Rename .ts/.tsx files to .tpl
      const newName = entry.name.replace(/\.tsx?$/, ".tpl");
      const targetPath = path.join(archiveBase, newName);

      fs.renameSync(sourcePath, targetPath);
      console.log(`✅ Archived: ${relativePath} → templates-archived/${path.relative(ARCHIVE_DIR, targetPath)}`);
    }
  });
}

console.log("🔥 Codex Dominion Template Cleanup Protocol");
console.log("=" .repeat(60));

// Process templates directory
const archiveCodeDir = path.join(ARCHIVE_DIR, "code");
if (!fs.existsSync(archiveCodeDir)) {
  fs.mkdirSync(archiveCodeDir, { recursive: true });
}

processDirectory(TEMPLATE_DIR, ARCHIVE_DIR);

console.log("=" .repeat(60));
console.log("✨ Cleanup complete. TypeScript errors should be resolved.");
