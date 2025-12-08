#!/usr/bin/env node
/**
 * CODEX DOMINION - System Efficiency Optimizer
 *
 * Automates performance optimization tasks:
 * - Cleans build caches
 * - Optimizes node_modules
 * - Analyzes bundle sizes
 * - Generates performance reports
 */

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const colors = {
  reset: '\x1b[0m',
  cyan: '\x1b[36m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  gray: '\x1b[90m',
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function exec(command, options = {}) {
  try {
    return execSync(command, { stdio: 'inherit', ...options });
  } catch (error) {
    log(`⚠️  Command failed: ${command}`, 'yellow');
    return null;
  }
}

function formatBytes(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function getDirSize(dirPath) {
  if (!fs.existsSync(dirPath)) return 0;

  let size = 0;
  const files = fs.readdirSync(dirPath, { withFileTypes: true });

  for (const file of files) {
    const filePath = path.join(dirPath, file.name);
    if (file.isDirectory()) {
      size += getDirSize(filePath);
    } else {
      size += fs.statSync(filePath).size;
    }
  }

  return size;
}

function cleanDirectory(dirPath, name) {
  if (fs.existsSync(dirPath)) {
    const sizeBefore = getDirSize(dirPath);
    log(`  Cleaning ${name}... (${formatBytes(sizeBefore)})`, 'gray');
    fs.rmSync(dirPath, { recursive: true, force: true });
    log(`  ✓ Removed ${name}`, 'green');
    return sizeBefore;
  }
  return 0;
}

async function main() {
  log('\n═══════════════════════════════════════', 'cyan');
  log('  CODEX DOMINION - System Optimizer', 'cyan');
  log('═══════════════════════════════════════\n', 'cyan');

  const startTime = Date.now();
  let totalCleaned = 0;

  // 1. Clean build caches
  log('📦 Step 1: Cleaning Build Caches', 'cyan');
  const cacheDirs = [
    { path: 'node_modules/.cache', name: 'Node cache' },
    { path: '.next', name: 'Next.js build' },
    { path: 'frontend/.next', name: 'Frontend build' },
    { path: 'dist', name: 'TypeScript output' },
    { path: 'build', name: 'Build artifacts' },
    { path: 'coverage', name: 'Test coverage' },
    { path: '.turbo', name: 'Turbo cache' },
    { path: '__pycache__', name: 'Python cache' },
    { path: '.mypy_cache', name: 'MyPy cache' },
    { path: '.pytest_cache', name: 'Pytest cache' },
  ];

  for (const dir of cacheDirs) {
    totalCleaned += cleanDirectory(dir.path, dir.name);
  }

  log(`\n  Total cleaned: ${formatBytes(totalCleaned)}\n`, 'green');

  // 2. Optimize node_modules
  log('📦 Step 2: Optimizing Dependencies', 'cyan');
  log('  Running npm dedupe...', 'gray');
  exec('npm dedupe');

  log('  Pruning unused packages...', 'gray');
  exec('npm prune');

  log('  ✓ Dependencies optimized\n', 'green');

  // 3. Analyze bundle sizes
  log('📊 Step 3: Analyzing Bundle Sizes', 'cyan');

  const frontendPath = path.join(process.cwd(), 'frontend');
  if (fs.existsSync(frontendPath)) {
    log('  Building Next.js production bundle...', 'gray');
    exec('npm run build', { cwd: frontendPath });

    const buildPath = path.join(frontendPath, '.next');
    if (fs.existsSync(buildPath)) {
      const buildSize = getDirSize(buildPath);
      log(`  Build size: ${formatBytes(buildSize)}`, 'yellow');
    }
  }

  log('  ✓ Bundle analysis complete\n', 'green');

  // 4. Update validation report
  log('📝 Step 4: Generating Optimization Report', 'cyan');

  const report = {
    timestamp: new Date().toISOString(),
    optimization: {
      cachesCleaned: formatBytes(totalCleaned),
      duration: `${((Date.now() - startTime) / 1000).toFixed(2)}s`,
    },
    recommendations: [
      'Consider enabling Redis caching for production',
      'Enable compression in production environment',
      'Monitor bundle sizes to stay under 500KB budget',
      'Run this optimizer weekly for optimal performance',
    ],
  };

  const reportPath = 'optimization_report.json';
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
  log(`  Report saved to ${reportPath}`, 'gray');
  log('  ✓ Report generated\n', 'green');

  // Summary
  log('═══════════════════════════════════════', 'cyan');
  log('  ✅ Optimization Complete!', 'green');
  log('═══════════════════════════════════════\n', 'cyan');

  log('📊 Summary:', 'cyan');
  log(`  • Caches cleaned: ${formatBytes(totalCleaned)}`, 'green');
  log(`  • Time elapsed: ${((Date.now() - startTime) / 1000).toFixed(2)}s`, 'green');
  log(`  • Report: ${reportPath}`, 'green');

  log('\n💡 Next Steps:', 'yellow');
  log('  • Run validation: npm run validate', 'gray');
  log('  • Run tests: npm run test', 'gray');
  log('  • Check pre-commit: npm run precommit\n', 'gray');
}

// Run optimizer
main().catch((error) => {
  log(`\n❌ Optimization failed: ${error.message}`, 'red');
  process.exit(1);
});
