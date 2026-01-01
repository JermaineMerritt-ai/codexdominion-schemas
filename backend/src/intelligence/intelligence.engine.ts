import { Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import {
  IntelligenceRules,
  IntelligenceRuleDefinition,
  IntelligenceRuleContext,
  RuleTrigger,
} from './rules/rule-definitions';
import { IntelligenceItem } from './intelligence.types';

@Injectable()
export class IntelligenceEngine {
  private readonly logger = new Logger(IntelligenceEngine.name);
  private readonly context: IntelligenceRuleContext;

  constructor(private readonly prisma: PrismaService) {
    this.context = { prisma };
  }

  async runWeeklyRules(options?: {
    regionId?: string;
    userId?: string;
    roles?: string[];
  }): Promise<IntelligenceItem[]> {
    return this.runRulesByTrigger('weekly', options);
  }

  async runDailyRules(options?: {
    regionId?: string;
    userId?: string;
    roles?: string[];
  }): Promise<IntelligenceItem[]> {
    return this.runRulesByTrigger('daily', options);
  }

  async runOnDemandRules(options?: {
    regionId?: string;
    userId?: string;
    roles?: string[];
  }): Promise<IntelligenceItem[]> {
    return this.runRulesByTrigger('on_demand', options);
  }

  private async runRulesByTrigger(
    trigger: RuleTrigger,
    options?: { regionId?: string; userId?: string; roles?: string[] },
  ): Promise<IntelligenceItem[]> {
    this.logger.log(`Running ${trigger} intelligence rules...`);
    const results: IntelligenceItem[] = [];

    const rules = IntelligenceRules.filter((r) => r.trigger === trigger);

    for (const rule of rules) {
      try {
        const items = await rule.evaluator(this.context, options);
        results.push(...items);
        this.logger.log(
          `Rule ${rule.id} evaluated: ${items.length} items generated`,
        );
      } catch (error) {
        this.logger.error(`Error evaluating rule ${rule.id}:`, error);
      }
    }

    this.logger.log(
      `${trigger} rules complete: ${results.length} total items`,
    );
    return results;
  }

  async runAllRules(options?: {
    regionId?: string;
    userId?: string;
    roles?: string[];
  }): Promise<IntelligenceItem[]> {
    this.logger.log('Running all intelligence rules...');
    const results: IntelligenceItem[] = [];

    for (const rule of IntelligenceRules) {
      try {
        const items = await rule.evaluator(this.context, options);
        results.push(...items);
      } catch (error) {
        this.logger.error(`Error evaluating rule ${rule.id}:`, error);
      }
    }

    return results;
  }

  async runRule(
    ruleId: string,
    options?: { regionId?: string; userId?: string; roles?: string[] },
  ): Promise<IntelligenceItem[]> {
    const rule = IntelligenceRules.find((r) => r.id === ruleId);

    if (!rule) {
      throw new Error(`Rule ${ruleId} not found`);
    }

    this.logger.log(`Running rule ${ruleId}...`);

    try {
      const items = await rule.evaluator(this.context, options);
      this.logger.log(
        `Rule ${ruleId} evaluated: ${items.length} items generated`,
      );
      return items;
    } catch (error) {
      this.logger.error(`Error evaluating rule ${ruleId}:`, error);
      throw error;
    }
  }

  getRules(): IntelligenceRuleDefinition[] {
    return IntelligenceRules.map((rule) => ({
      id: rule.id,
      name: rule.name,
      trigger: rule.trigger,
      domain: rule.domain,
      evaluator: rule.evaluator,
    }));
  }

  getRulesByTrigger(trigger: RuleTrigger): IntelligenceRuleDefinition[] {
    return IntelligenceRules.filter((r) => r.trigger === trigger);
  }
}
