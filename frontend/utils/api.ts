// utils/api.ts
/**
 * 🔥 CODEX SIGNALS API CLIENT 📊
 * TypeScript utilities for frontend integration
 *
 * The Merritt Method™ - Frontend Portfolio Intelligence
 */

// Types matching the Python API
export type MarketSnapshot = {
  symbol: string;
  price: number;
  vol_30d: number;
  trend_20d: number;
  liquidity_rank: number;
};

export type Position = {
  symbol: string;
  weight: number;
  allowed_max: number;
};

export type Pick = {
  symbol: string;
  tier: string;
  target_weight: number;
  rationale: string;
  risk_factors: string[];
};

export type SignalsSnapshot = {
  generated_at: string;
  banner: string;
  tier_counts: {
    Alpha: number;
    Beta: number;
    Gamma: number;
    Delta: number;
  };
  picks: Pick[];
};

export type BulletinResponse = {
  format: string;
  content: string;
  generated_at: string;
  tier_counts: {
    Alpha: number;
    Beta: number;
    Gamma: number;
    Delta: number;
  };
};

export class CodexSignalsAPI {
  constructor(private baseURL: string) {}

  /**
   * Generate daily signals with market data and positions
   */
  async generateDailySignals(
    market: MarketSnapshot[],
    positions: Position[]
  ): Promise<SignalsSnapshot> {
    const response = await fetch(`${this.baseURL}/signals/daily`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ market, positions }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  }

  /**
   * Get mock signals for testing
   */
  async getMockSignals(): Promise<SignalsSnapshot> {
    const response = await fetch(`${this.baseURL}/signals/mock`);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  }

  /**
   * Generate formatted bulletin
   */
  async generateBulletin(format: 'md' | 'txt' = 'md'): Promise<BulletinResponse> {
    const response = await fetch(`${this.baseURL}/signals/bulletin?format=${format}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  }

  /**
   * Check API health
   */
  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    const response = await fetch(`${this.baseURL}/signals/health`);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  }

  /**
   * Get engine configuration
   */
  async getEngineConfig(): Promise<any> {
    const response = await fetch(`${this.baseURL}/signals/engine/config`);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  }
}

/**
 * Utility functions for frontend
 */
export const SignalsUtils = {
  /**
   * Convert Markdown to HTML (minimal implementation)
   */
  mdToHtml(markdown: string): string {
    return markdown
      .replace(/^# (.*)$/gm, '<h1>$1</h1>')
      .replace(/^## (.*)$/gm, '<h2>$1</h2>')
      .replace(/^> (.*)$/gm, '<blockquote>$1</blockquote>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n- (.*)/g, '<br>• $1')
      .replace(/\n/g, '<br>');
  },

  /**
   * Generate bulletin markdown from snapshot
   */
  generateBulletinMD(snapshot: SignalsSnapshot): string {
    const header = `# Daily Signals — ${snapshot.generated_at}\n\n`;
    const banner = `> ${snapshot.banner}\n\n`;
    const tiers = `- Alpha: ${snapshot.tier_counts.Alpha}\n- Beta: ${snapshot.tier_counts.Beta}\n- Gamma: ${snapshot.tier_counts.Gamma}\n- Delta: ${snapshot.tier_counts.Delta}\n\n`;

    const body = (snapshot.picks || [])
      .map(
        (p) =>
          `**${p.symbol}** — Tier ${p.tier} | target ${(p.target_weight * 100).toFixed(2)}%\n- Rationale: ${p.rationale}\n- Risks: ${p.risk_factors?.join(', ') || 'None'}\n`
      )
      .join('\n');

    return header + banner + tiers + body;
  },

  /**
   * Format weight as percentage
   */
  formatWeight(weight: number): string {
    return `${(weight * 100).toFixed(2)}%`;
  },

  /**
   * Get tier color for UI
   */
  getTierColor(tier: string): string {
    const colors = {
      Alpha: '#10b981',
      Beta: '#3b82f6',
      Gamma: '#f59e0b',
      Delta: '#ef4444',
    };
    return colors[tier as keyof typeof colors] || '#6b7280';
  },

  /**
   * Calculate total allocation
   */
  calculateTotalAllocation(picks: Pick[]): number {
    return picks.reduce((total, pick) => total + pick.target_weight, 0);
  },

  /**
   * Get risk level description
   */
  getRiskDescription(tier: string): string {
    const descriptions = {
      Alpha: 'High conviction positions with strong fundamentals',
      Beta: 'Balanced exposure with measured risk/reward',
      Gamma: 'Elevated risk requiring defensive positioning',
      Delta: 'High turbulence - capital preservation priority',
    };
    return descriptions[tier as keyof typeof descriptions] || 'Unknown risk level';
  },
};

/**
 * React hook for Codex Signals API
 */
export function useCodexSignals(baseURL: string) {
  const api = new CodexSignalsAPI(baseURL);

  return {
    api,
    utils: SignalsUtils,
  };
}
