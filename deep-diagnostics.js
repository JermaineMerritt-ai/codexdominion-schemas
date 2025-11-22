#!/usr/bin/env node

import chalk from 'chalk';
import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs';
import path from 'path';

const execAsync = promisify(exec);

console.log(chalk.bold.magenta('🔬 CODEX DOMINION DEEP DIAGNOSTICS 🔬\n'));

class EmpireDiagnostics {
  constructor() {
    this.results = {
      critical: [],
      warnings: [],
      info: [],
      success: []
    };
  }

  log(level, message) {
    this.results[level].push(message);
    const colors = {
      critical: chalk.red,
      warnings: chalk.yellow,
      info: chalk.blue,
      success: chalk.green
    };
    const icons = {
      critical: '🚨',
      warnings: '⚠️',
      info: 'ℹ️',
      success: '✅'
    };
    console.log(`${icons[level]} ${colors[level](message)}`);
  }

  async checkFile(filePath, description) {
    try {
      const fullPath = path.resolve(filePath);
      const stats = fs.statSync(fullPath);
      this.log('success', `${description}: Found (${stats.size} bytes)`);
      return true;
    } catch (error) {
      this.log('critical', `${description}: Missing or inaccessible`);
      return false;
    }
  }

  async checkDirectory(dirPath, description) {
    try {
      const fullPath = path.resolve(dirPath);
      const stats = fs.statSync(fullPath);
      if (stats.isDirectory()) {
        const contents = fs.readdirSync(fullPath);
        this.log('success', `${description}: Found (${contents.length} items)`);
        return true;
      } else {
        this.log('warnings', `${description}: Exists but not a directory`);
        return false;
      }
    } catch (error) {
      this.log('critical', `${description}: Missing`);
      return false;
    }
  }

  async checkCommand(command, description) {
    try {
      const { stdout } = await execAsync(command);
      this.log('success', `${description}: Available`);
      return true;
    } catch (error) {
      this.log('warnings', `${description}: Not available or error`);
      return false;
    }
  }

  async checkPackageJson(filePath, description) {
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      const pkg = JSON.parse(content);
      
      this.log('success', `${description}: Valid JSON`);
      
      if (pkg.dependencies) {
        this.log('info', `  - Dependencies: ${Object.keys(pkg.dependencies).length} packages`);
      }
      if (pkg.devDependencies) {
        this.log('info', `  - DevDependencies: ${Object.keys(pkg.devDependencies).length} packages`);
      }
      if (pkg.scripts) {
        this.log('info', `  - Scripts: ${Object.keys(pkg.scripts).length} commands`);
      }
      
      return true;
    } catch (error) {
      this.log('critical', `${description}: Invalid or missing (${error.message})`);
      return false;
    }
  }

  async checkNodeModules(dirPath, description) {
    try {
      const fullPath = path.resolve(dirPath, 'node_modules');
      const stats = fs.statSync(fullPath);
      if (stats.isDirectory()) {
        const modules = fs.readdirSync(fullPath);
        const moduleCount = modules.filter(m => !m.startsWith('.')).length;
        this.log('success', `${description}: ${moduleCount} modules installed`);
        return true;
      }
    } catch (error) {
      this.log('warnings', `${description}: No modules installed`);
      return false;
    }
  }

  async systemCheck() {
    console.log(chalk.bold.cyan('🔧 System Prerequisites\n'));
    
    await this.checkCommand('node --version', 'Node.js');
    await this.checkCommand('npm --version', 'NPM');
    await this.checkCommand('python --version', 'Python');
    await this.checkCommand('git --version', 'Git');
  }

  async coreFilesCheck() {
    console.log(chalk.bold.cyan('\n📁 Core Files Structure\n'));
    
    await this.checkPackageJson('package.json', 'Root Package.json');
    await this.checkFile('server.js', 'Server Entry Point');
    await this.checkFile('empire-status.js', 'Empire Status Tool');
    await this.checkFile('validate-empire.js', 'Empire Validator');
    await this.checkFile('auto-fix-empire.js', 'Auto-Fix System');
  }

  async frontendCheck() {
    console.log(chalk.bold.cyan('\n🎨 Frontend Structure\n'));
    
    await this.checkDirectory('frontend', 'Frontend Directory');
    await this.checkPackageJson('frontend/package.json', 'Frontend Package.json');
    await this.checkFile('frontend/next.config.js', 'Next.js Config');
    await this.checkFile('frontend/tsconfig.json', 'TypeScript Config');
    await this.checkNodeModules('frontend', 'Frontend Dependencies');
  }

  async dependenciesCheck() {
    console.log(chalk.bold.cyan('\n📦 Dependencies Status\n'));
    
    await this.checkNodeModules('.', 'Root Dependencies');
    
    try {
      const { stdout } = await execAsync('npm outdated --json');
      const outdated = JSON.parse(stdout || '{}');
      const outdatedCount = Object.keys(outdated).length;
      if (outdatedCount > 0) {
        this.log('warnings', `${outdatedCount} packages have updates available`);
      } else {
        this.log('success', 'All packages are up to date');
      }
    } catch (error) {
      this.log('info', 'Could not check for outdated packages');
    }
  }

  async securityCheck() {
    console.log(chalk.bold.cyan('\n🛡️ Security Audit\n'));
    
    try {
      const { stdout } = await execAsync('npm audit --json');
      const audit = JSON.parse(stdout);
      
      if (audit.metadata.vulnerabilities.total === 0) {
        this.log('success', 'No security vulnerabilities found');
      } else {
        const { high, critical, moderate, low } = audit.metadata.vulnerabilities;
        if (critical > 0) this.log('critical', `${critical} critical vulnerabilities`);
        if (high > 0) this.log('critical', `${high} high vulnerabilities`);
        if (moderate > 0) this.log('warnings', `${moderate} moderate vulnerabilities`);
        if (low > 0) this.log('info', `${low} low vulnerabilities`);
      }
    } catch (error) {
      this.log('warnings', 'Could not perform security audit');
    }
  }

  async performanceCheck() {
    console.log(chalk.bold.cyan('\n⚡ Performance Metrics\n'));
    
    try {
      const startTime = Date.now();
      await this.checkCommand('node -e "console.log(process.versions)"', 'Node.js Performance');
      const endTime = Date.now();
      this.log('info', `Command execution time: ${endTime - startTime}ms`);
    } catch (error) {
      this.log('warnings', 'Performance check failed');
    }
  }

  displaySummary() {
    console.log(chalk.bold.yellow('\n' + '='.repeat(60)));
    console.log(chalk.bold.yellow('           DEEP DIAGNOSTICS SUMMARY           '));
    console.log(chalk.bold.yellow('='.repeat(60)));

    const counts = {
      critical: this.results.critical.length,
      warnings: this.results.warnings.length,
      info: this.results.info.length,
      success: this.results.success.length
    };

    console.log(chalk.red(`🚨 Critical Issues: ${counts.critical}`));
    console.log(chalk.yellow(`⚠️ Warnings: ${counts.warnings}`));
    console.log(chalk.blue(`ℹ️ Information: ${counts.info}`));
    console.log(chalk.green(`✅ Success: ${counts.success}`));

    const totalChecks = counts.critical + counts.warnings + counts.info + counts.success;
    const healthScore = Math.round(((counts.success + counts.info * 0.5) / totalChecks) * 100);

    console.log(chalk.bold.cyan(`\n🏥 Empire Health Score: ${healthScore}%`));

    if (healthScore >= 90) {
      console.log(chalk.bold.green('\n🏆 EMPIRE STATUS: EXCELLENT'));
      console.log(chalk.bold.green('🔥 All systems operating at peak performance'));
    } else if (healthScore >= 75) {
      console.log(chalk.bold.yellow('\n✅ EMPIRE STATUS: GOOD'));
      console.log(chalk.bold.yellow('🔧 Minor optimizations recommended'));
    } else if (healthScore >= 50) {
      console.log(chalk.bold.orange('\n⚠️ EMPIRE STATUS: FAIR'));
      console.log(chalk.bold.orange('🛠️ Several issues need attention'));
    } else {
      console.log(chalk.bold.red('\n🚨 EMPIRE STATUS: CRITICAL'));
      console.log(chalk.bold.red('🆘 Immediate intervention required'));
    }

    if (counts.critical > 0) {
      console.log(chalk.bold.red('\n🔧 RECOMMENDED ACTION: Run auto-fix system'));
      console.log(chalk.bold.red('   Command: npm run auto-fix'));
    }

    console.log(chalk.bold.yellow('\n' + '='.repeat(60)));
  }

  async diagnose() {
    console.log(chalk.bold.green('🚀 Starting Deep Empire Diagnostics...\n'));
    
    await this.systemCheck();
    await this.coreFilesCheck();
    await this.frontendCheck();
    await this.dependenciesCheck();
    await this.securityCheck();
    await this.performanceCheck();
    
    this.displaySummary();
    
    return this.results;
  }
}

// Execute Diagnostics
const diagnostics = new EmpireDiagnostics();
diagnostics.diagnose().then(results => {
  console.log(chalk.bold.magenta('\n🔬 Deep Diagnostics Complete 🔬'));
  const hasCritical = results.critical.length > 0;
  process.exit(hasCritical ? 1 : 0);
}).catch(error => {
  console.error(chalk.red('Diagnostics failed:'), error.message);
  process.exit(1);
});