#!/usr/bin/env node

import chalk from 'chalk';
import fs from 'fs';
import path from 'path';

console.log(chalk.bold.magenta('🏰 CODEX DOMINION EMPIRE VALIDATOR 🏰\n'));

class EmpireValidator {
  constructor() {
    this.errors = [];
    this.warnings = [];
    this.fixes = [];
  }

  validatePackageJson() {
    console.log(chalk.blue('📋 Validating Package Configuration...'));

    if (!fs.existsSync('package.json')) {
      this.errors.push('Missing package.json');
      return;
    }

    const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));

    // Check required fields
    const required = ['name', 'version', 'description', 'scripts', 'dependencies'];
    required.forEach((field) => {
      if (!pkg[field]) {
        this.errors.push(`Missing ${field} in package.json`);
      }
    });

    // Check Codex Dominion configuration
    if (!pkg.codexDominion) {
      this.warnings.push('Missing codexDominion configuration');
    }

    console.log(chalk.green('✓ Package validation complete\n'));
  }

  validateFrontend() {
    console.log(chalk.blue('🎨 Validating Frontend...'));

    if (!fs.existsSync('frontend')) {
      this.errors.push('Missing frontend directory');
      return;
    }

    if (!fs.existsSync('frontend/package.json')) {
      this.errors.push('Missing frontend/package.json');
    }

    // Check for essential frontend files
    const frontendFiles = ['next.config.js', 'tsconfig.json'];
    frontendFiles.forEach((file) => {
      if (!fs.existsSync(path.join('frontend', file))) {
        this.warnings.push(`Missing frontend/${file}`);
      }
    });

    console.log(chalk.green('✓ Frontend validation complete\n'));
  }

  validateBackend() {
    console.log(chalk.blue('⚙️ Validating Backend Services...'));

    const backendFiles = ['server.js', 'app.py'];
    const hasBackend = backendFiles.some((file) => fs.existsSync(file));

    if (!hasBackend) {
      this.warnings.push('No backend entry point found (server.js or app.py)');
    }

    console.log(chalk.green('✓ Backend validation complete\n'));
  }

  validateEmpireStructure() {
    console.log(chalk.blue('🏛️ Validating Empire Structure...'));

    const essentialDirs = ['frontend', 'codex-suite'];
    essentialDirs.forEach((dir) => {
      if (!fs.existsSync(dir)) {
        this.warnings.push(`Missing ${dir} directory`);
      }
    });

    // Check for proclamation files
    const files = fs.readdirSync('.');
    const proclamations = files.filter(
      (file) => file.includes('PROCLAMATION') && file.endsWith('.md')
    );

    if (proclamations.length === 0) {
      this.warnings.push('No proclamation files found');
    }

    console.log(chalk.green('✓ Empire structure validation complete\n'));
  }

  generateFixes() {
    console.log(chalk.blue('🔧 Generating Auto-Fixes...\n'));

    // Auto-fix suggestions
    if (this.errors.includes('Missing package.json')) {
      this.fixes.push('Run: npm init -y to create package.json');
    }

    if (this.warnings.includes('Missing frontend/next.config.js')) {
      this.fixes.push('Create frontend/next.config.js for Next.js configuration');
    }

    if (this.warnings.includes('Missing frontend/tsconfig.json')) {
      this.fixes.push('Create frontend/tsconfig.json for TypeScript configuration');
    }
  }

  displayResults() {
    console.log(chalk.bold.yellow('='.repeat(60)));
    console.log(chalk.bold.yellow('           VALIDATION RESULTS           '));
    console.log(chalk.bold.yellow('='.repeat(60)));

    if (this.errors.length > 0) {
      console.log(chalk.bold.red('\n❌ CRITICAL ERRORS:'));
      this.errors.forEach((error) => {
        console.log(chalk.red(`  • ${error}`));
      });
    }

    if (this.warnings.length > 0) {
      console.log(chalk.bold.yellow('\n⚠️  WARNINGS:'));
      this.warnings.forEach((warning) => {
        console.log(chalk.yellow(`  • ${warning}`));
      });
    }

    if (this.fixes.length > 0) {
      console.log(chalk.bold.cyan('\n🔧 SUGGESTED FIXES:'));
      this.fixes.forEach((fix) => {
        console.log(chalk.cyan(`  • ${fix}`));
      });
    }

    if (this.errors.length === 0 && this.warnings.length === 0) {
      console.log(chalk.bold.green('\n🏆 EMPIRE VALIDATION: PERFECT'));
      console.log(chalk.bold.green('👑 All systems operational and compliant'));
    } else if (this.errors.length === 0) {
      console.log(chalk.bold.yellow('\n✅ EMPIRE VALIDATION: GOOD'));
      console.log(chalk.bold.yellow('🔧 Minor improvements recommended'));
    } else {
      console.log(chalk.bold.red('\n❌ EMPIRE VALIDATION: NEEDS ATTENTION'));
      console.log(chalk.bold.red('🚨 Critical issues require immediate fixing'));
    }

    console.log(chalk.bold.yellow('\n' + '='.repeat(60)));
  }

  async validate() {
    this.validatePackageJson();
    this.validateFrontend();
    this.validateBackend();
    this.validateEmpireStructure();
    this.generateFixes();
    this.displayResults();

    return {
      errors: this.errors.length,
      warnings: this.warnings.length,
      fixes: this.fixes.length,
    };
  }
}

// Execute Validation
const validator = new EmpireValidator();
validator
  .validate()
  .then((results) => {
    process.exit(results.errors > 0 ? 1 : 0);
  })
  .catch((error) => {
    console.error(chalk.red('Validation failed:'), error.message);
    process.exit(1);
  });
