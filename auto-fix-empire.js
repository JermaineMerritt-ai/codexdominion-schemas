#!/usr/bin/env node

import chalk from 'chalk';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

console.log(chalk.bold.magenta('🏰 CODEX DOMINION AUTO-FIX SYSTEM 🏰\n'));

class EmpireFixer {
  constructor() {
    this.fixes = [];
    this.errors = [];
  }

  async runCommand(command, description) {
    console.log(chalk.blue(`🔧 ${description}...`));
    try {
      const { stdout, stderr } = await execAsync(command);
      if (stderr && !stderr.includes('warn')) {
        console.log(chalk.yellow(`⚠️  ${stderr}`));
      }
      if (stdout) {
        console.log(chalk.green(`✓ ${description} completed`));
      }
      this.fixes.push(description);
      return true;
    } catch (error) {
      console.log(chalk.red(`❌ ${description} failed: ${error.message}`));
      this.errors.push({ description, error: error.message });
      return false;
    }
  }

  async installDependencies() {
    console.log(chalk.bold.cyan('\n📦 Installing Dependencies...\n'));

    await this.runCommand('npm install', 'Installing root dependencies');
    await this.runCommand('cd frontend && npm install', 'Installing frontend dependencies');
  }

  async auditAndFix() {
    console.log(chalk.bold.cyan('\n🔍 Security Audit and Auto-Fix...\n'));

    await this.runCommand('npm audit fix', 'Fixing root security issues');
    await this.runCommand('cd frontend && npm audit fix', 'Fixing frontend security issues');
  }

  async updateDependencies() {
    console.log(chalk.bold.cyan('\n⬆️ Updating Dependencies...\n'));

    await this.runCommand('npm update', 'Updating root dependencies');
    await this.runCommand('cd frontend && npm update', 'Updating frontend dependencies');
  }

  async runTests() {
    console.log(chalk.bold.cyan('\n🧪 Running Tests...\n'));

    await this.runCommand('npm run validate', 'Validating empire configuration');
    await this.runCommand('npm run status', 'Checking empire status');
  }

  displayResults() {
    console.log(chalk.bold.yellow('\n' + '='.repeat(60)));
    console.log(chalk.bold.yellow('           AUTO-FIX RESULTS           '));
    console.log(chalk.bold.yellow('='.repeat(60)));

    if (this.fixes.length > 0) {
      console.log(chalk.bold.green('\n✅ SUCCESSFUL FIXES:'));
      this.fixes.forEach((fix) => {
        console.log(chalk.green(`  ✓ ${fix}`));
      });
    }

    if (this.errors.length > 0) {
      console.log(chalk.bold.red('\n❌ FAILED FIXES:'));
      this.errors.forEach(({ description, error }) => {
        console.log(chalk.red(`  ✗ ${description}: ${error}`));
      });
    }

    const successRate = Math.round(
      (this.fixes.length / (this.fixes.length + this.errors.length)) * 100
    );

    console.log(chalk.bold.cyan(`\n📊 Fix Success Rate: ${successRate}%`));

    if (successRate === 100) {
      console.log(chalk.bold.green('\n🏆 EMPIRE AUTO-FIX: COMPLETE SUCCESS'));
      console.log(chalk.bold.green('🔥 All systems optimized and operational'));
    } else if (successRate >= 80) {
      console.log(chalk.bold.yellow('\n✅ EMPIRE AUTO-FIX: MOSTLY SUCCESSFUL'));
      console.log(chalk.bold.yellow('🔧 Minor issues may require manual attention'));
    } else {
      console.log(chalk.bold.red('\n⚠️ EMPIRE AUTO-FIX: PARTIAL SUCCESS'));
      console.log(chalk.bold.red('🚨 Some issues require manual intervention'));
    }

    console.log(chalk.bold.yellow('\n' + '='.repeat(60)));
  }

  async fix() {
    console.log(chalk.bold.green('🚀 Starting Empire Auto-Fix Sequence...\n'));

    await this.installDependencies();
    await this.auditAndFix();
    await this.updateDependencies();
    await this.runTests();

    this.displayResults();

    return {
      fixes: this.fixes.length,
      errors: this.errors.length,
      successRate: Math.round((this.fixes.length / (this.fixes.length + this.errors.length)) * 100),
    };
  }
}

// Execute Auto-Fix
const fixer = new EmpireFixer();
fixer
  .fix()
  .then((results) => {
    console.log(chalk.bold.magenta('\n🏰 Empire Auto-Fix Complete 🏰'));
    process.exit(results.errors > 0 ? 1 : 0);
  })
  .catch((error) => {
    console.error(chalk.red('Auto-fix failed:'), error.message);
    process.exit(1);
  });
