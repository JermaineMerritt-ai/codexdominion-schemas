import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import {
  IntelligenceItem,
  IntelligenceAudience,
} from './intelligence.types';
import {
  IntelligenceRules,
  IntelligenceRuleContext,
} from './rules/rule-definitions';

interface GetIntelligenceOptions {
  domain?: string;
  regionId?: string;
  userId?: string;
  roles?: string[];
}

@Injectable()
export class IntelligenceService {
  private ctx: IntelligenceRuleContext;

  constructor(private readonly prisma: PrismaService) {
    this.ctx = { prisma: this.prisma };
  }

  private filterByAudience(
    items: IntelligenceItem[],
    roles: string[] | undefined
  ): IntelligenceItem[] {
    if (!roles || roles.length === 0) return items;

    // Map roles to audiences
    const audienceFromRoles: IntelligenceAudience[] = [];
    if (roles.includes('ADMIN') || roles.includes('COUNCIL')) audienceFromRoles.push('admin');
    if (roles.includes('REGIONAL_DIRECTOR')) audienceFromRoles.push('director');
    if (roles.includes('AMBASSADOR')) audienceFromRoles.push('ambassador');
    if (roles.includes('YOUTH_CAPTAIN')) audienceFromRoles.push('captain');
    if (roles.includes('CREATOR')) audienceFromRoles.push('creator');
    if (roles.includes('YOUTH')) audienceFromRoles.push('youth');

    return items.filter((item) =>
      item.audience.some((a) => audienceFromRoles.includes(a))
    );
  }

  async getAlerts(options: GetIntelligenceOptions): Promise<IntelligenceItem[]> {
    const all = await this.evaluateAllRules(options);
    return all.filter((i) => i.type === 'alert');
  }

  async getRecommendations(options: GetIntelligenceOptions): Promise<IntelligenceItem[]> {
    const all = await this.evaluateAllRules(options);
    return all.filter((i) => i.type === 'recommendation');
  }

  async getForecasts(options: GetIntelligenceOptions): Promise<IntelligenceItem[]> {
    const all = await this.evaluateAllRules(options);
    return all.filter((i) => i.type === 'forecast');
  }

  async getOpportunities(options: GetIntelligenceOptions): Promise<IntelligenceItem[]> {
    const all = await this.evaluateAllRules(options);
    return all.filter((i) => i.type === 'opportunity');
  }

  async getInsights(options: GetIntelligenceOptions): Promise<{
    alerts: IntelligenceItem[];
    recommendations: IntelligenceItem[];
    forecasts: IntelligenceItem[];
    opportunities: IntelligenceItem[];
  }> {
    const all = await this.evaluateAllRules(options);

    return {
      alerts: all.filter((i) => i.type === 'alert'),
      recommendations: all.filter((i) => i.type === 'recommendation'),
      forecasts: all.filter((i) => i.type === 'forecast'),
      opportunities: all.filter((i) => i.type === 'opportunity'),
    };
  }

  private async evaluateAllRules(options: GetIntelligenceOptions): Promise<IntelligenceItem[]> {
    const results: IntelligenceItem[] = [];

    for (const rule of IntelligenceRules) {
      // domain filter
      if (options.domain && rule.domain !== options.domain) continue;

      const items = await rule.evaluator(this.ctx, {
        regionId: options.regionId,
        userId: options.userId,
        roles: options.roles,
      });

      // tag with ruleId if not set inside evaluator
      for (const item of items) {
        if (!item.ruleId) {
          item.ruleId = rule.id;
        }
        if (!item.timestamp) {
          item.timestamp = new Date().toISOString();
        }
      }

      results.push(...items);
    }

    return this.filterByAudience(results, options.roles);
  }
}
