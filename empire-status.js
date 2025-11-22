#!/usr/bin/env node

import chalk from 'chalk';
import ora from 'ora';
import fs from 'fs';
import path from 'path';

const spinner = ora('Checking Codex Dominion Empire Status').start();

// Empire Status Check
class EmpireStatus {
  constructor() {
    this.components = {
      'Package Configuration': false,
      'Frontend Application': false,
      'Backend Services': false,
      'Dashboard System': false,
      'Council Interface': false,
      'Proxy Services': false,
      'Sacred Seals': false,
      'Proclamations Archive': false
    };
  }

  async checkComponent(name, checkFunction) {
    try {
      const result = await checkFunction();
      this.components[name] = result;
      return result;
    } catch (error) {
      this.components[name] = false;
      return false;
    }
  }

  async runDiagnostics() {
    spinner.text = 'Analyzing Empire Components...';

    // Check package.json
    await this.checkComponent('Package Configuration', () => {
      return fs.existsSync('package.json') && fs.existsSync('frontend/package.json');
    });

    // Check frontend
    await this.checkComponent('Frontend Application', () => {
      return fs.existsSync('frontend') && fs.existsSync('frontend/package.json');
    });

    // Check backend services
    await this.checkComponent('Backend Services', () => {
      return fs.existsSync('server.js') || fs.existsSync('app.py');
    });

    // Check dashboard
    await this.checkComponent('Dashboard System', () => {
      return fs.existsSync('codex-suite') || fs.existsSync('advanced_intelligence_computation_dashboard.py');
    });

    // Check council
    await this.checkComponent('Council Interface', () => {
      return fs.existsSync('ceremonial_council_archival.py');
    });

    // Check proxy
    await this.checkComponent('Proxy Services', () => {
      return fs.existsSync('aistorelab-proxy.js');
    });

    // Check seals
    await this.checkComponent('Sacred Seals', () => {
      const sealFiles = fs.readdirSync('.').filter(file => file.includes('seal') && file.endsWith('.json'));
      return sealFiles.length > 0;
    });

    // Check proclamations
    await this.checkComponent('Proclamations Archive', () => {
      const proclamationFiles = fs.readdirSync('.').filter(file => 
        file.includes('PROCLAMATION') && file.endsWith('.md')
      );
      return proclamationFiles.length > 0;
    });

    spinner.succeed('Empire Analysis Complete');
    this.displayResults();
  }

  displayResults() {
    console.log('\n' + chalk.bold.yellow('='.repeat(60)));
    console.log(chalk.bold.yellow('           CODEX DOMINION EMPIRE STATUS           '));
    console.log(chalk.bold.yellow('='.repeat(60)));

    Object.entries(this.components).forEach(([component, status]) => {
      const icon = status ? chalk.green('✓') : chalk.red('✗');
      const statusText = status ? chalk.green('OPERATIONAL') : chalk.red('NEEDS ATTENTION');
      console.log(`${icon} ${chalk.bold(component.padEnd(25))} ${statusText}`);
    });

    const operationalCount = Object.values(this.components).filter(Boolean).length;
    const totalCount = Object.keys(this.components).length;
    const percentage = Math.round((operationalCount / totalCount) * 100);

    console.log('\n' + chalk.bold.cyan('='.repeat(60)));
    console.log(chalk.bold.cyan(`Empire Operational Level: ${percentage}% (${operationalCount}/${totalCount})`));
    
    if (percentage === 100) {
      console.log(chalk.bold.green('🏰 EMPIRE STATUS: FULLY OPERATIONAL'));
      console.log(chalk.bold.green('🔥 FLAME STATUS: ETERNAL'));
      console.log(chalk.bold.green('👑 SOVEREIGNTY: SUPREME'));
    } else if (percentage >= 75) {
      console.log(chalk.bold.yellow('🏰 EMPIRE STATUS: MOSTLY OPERATIONAL'));
      console.log(chalk.bold.yellow('🔥 FLAME STATUS: STABLE'));
      console.log(chalk.bold.yellow('👑 SOVEREIGNTY: HIGH'));
    } else {
      console.log(chalk.bold.red('🏰 EMPIRE STATUS: NEEDS MAINTENANCE'));
      console.log(chalk.bold.red('🔥 FLAME STATUS: REQUIRES ATTENTION'));
      console.log(chalk.bold.red('👑 SOVEREIGNTY: REBUILDING'));
    }

    console.log(chalk.bold.cyan('='.repeat(60)));
  }
}

// Execute Status Check
const empire = new EmpireStatus();
empire.runDiagnostics().catch(error => {
  spinner.fail('Empire Status Check Failed');
  console.error(chalk.red('Error:'), error.message);
  process.exit(1);
});