'use client';

import { useState, useEffect } from 'react';
import { 
  PortfolioLoadError,
  AnalyticsError 
} from '@/components/errors/ModuleErrorStates';
import { 
  NoHoldingsEmpty,
  NoAllocationEmpty 
} from '@/components/empty/GlobalEmptyStates';
import { PortfolioLoading } from '@/components/loading/IdentityLoadingStates';
import { 
  PremiumGateAnalytics,
  PremiumGateCSVExport,
  PremiumGateMultiPortfolio,
  PremiumBadge
} from '@/components/gates/PremiumGateStates';

type UserTier = "free" | "premium" | "pro";
type IdentityType = "diaspora" | "youth" | "creator" | "legacy";

interface Holding {
  symbol: string;
  shares: number;
  avgCost: number;
  currentPrice: number;
  value: number;
  gainLoss: number;
  gainLossPercent: number;
}

interface PortfolioData {
  holdings: Holding[];
  totalValue: number;
  totalGainLoss: number;
  totalGainLossPercent: number;
  allocation: Record<string, number>;
}

export default function PortfolioPage() {
  const [userTier, setUserTier] = useState<UserTier>('free');
  const [identity, setIdentity] = useState<IdentityType>('diaspora');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<any>(null);
  const [data, setData] = useState<PortfolioData | null>(null);
  const [showAnalyticsGate, setShowAnalyticsGate] = useState(false);
  const [showCSVGate, setShowCSVGate] = useState(false);

  useEffect(() => {
    fetchPortfolio();
  }, []);

  const fetchPortfolio = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/portfolio');
      
      if (!response.ok) {
        throw {
          status: response.status,
          message: response.statusText,
          type: response.status >= 500 ? 'server' : 'generic'
        };
      }

      const result = await response.json();
      setData(result);
    } catch (err: any) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  const handleExportCSV = () => {
    if (userTier === 'free') {
      setShowCSVGate(true);
    } else {
      // Export logic here
      console.log('Exporting CSV...');
    }
  };

  const handleViewAnalytics = () => {
    if (userTier === 'free') {
      setShowAnalyticsGate(true);
    } else {
      // Show analytics
      console.log('Showing analytics...');
    }
  };

  // Show identity-aware loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-sovereign-obsidian p-6">
        <PortfolioLoading identity={identity} />
      </div>
    );
  }

  // Show error state
  if (error) {
    return (
      <div className="min-h-screen bg-sovereign-obsidian p-6">
        <PortfolioLoadError onRetry={fetchPortfolio} />
      </div>
    );
  }

  // Show empty state if no holdings
  if (!data?.holdings?.length) {
    return (
      <div className="min-h-screen bg-sovereign-obsidian p-6">
        <NoHoldingsEmpty 
          identity={identity}
          onAction={() => window.location.href = '/markets'}
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-sovereign-obsidian">
      {/* Header */}
      <header className="border-b border-sovereign-slate-700 bg-sovereign-obsidian/50 backdrop-blur-sm sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white">Portfolio</h1>
              <p className="text-sm text-sovereign-slate-400">
                {data.holdings.length} holdings • ${data.totalValue.toLocaleString()}
              </p>
            </div>
            
            {/* Actions */}
            <div className="flex items-center gap-3">
              {/* User Tier Selector (Demo) */}
              <select
                value={userTier}
                onChange={(e) => setUserTier(e.target.value as UserTier)}
                className="px-3 py-1.5 bg-sovereign-slate-700 text-white rounded-lg text-sm"
              >
                <option value="free">Free Tier</option>
                <option value="premium">Premium Tier</option>
                <option value="pro">Pro Tier</option>
              </select>

              <button
                onClick={handleExportCSV}
                className="px-4 py-2 bg-sovereign-slate-700 text-white rounded-lg hover:bg-sovereign-slate-600 transition-colors text-sm font-medium flex items-center gap-2"
              >
                Export CSV
                {userTier === 'free' && <PremiumBadge tier="premium" size="sm" />}
              </button>

              <button
                onClick={handleViewAnalytics}
                className="px-4 py-2 bg-sovereign-gold text-sovereign-obsidian rounded-lg hover:bg-sovereign-gold-hover transition-colors text-sm font-medium flex items-center gap-2"
              >
                Analytics
                {userTier === 'free' && <PremiumBadge tier="premium" size="sm" />}
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column: Holdings Table */}
          <div className="lg:col-span-2">
            <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
              <h2 className="text-lg font-medium text-white mb-4">Holdings</h2>
              
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-sovereign-slate-700">
                      <th className="text-left text-xs font-medium text-sovereign-slate-400 pb-3">Symbol</th>
                      <th className="text-right text-xs font-medium text-sovereign-slate-400 pb-3">Shares</th>
                      <th className="text-right text-xs font-medium text-sovereign-slate-400 pb-3">Avg Cost</th>
                      <th className="text-right text-xs font-medium text-sovereign-slate-400 pb-3">Current</th>
                      <th className="text-right text-xs font-medium text-sovereign-slate-400 pb-3">Value</th>
                      <th className="text-right text-xs font-medium text-sovereign-slate-400 pb-3">Gain/Loss</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.holdings.map((holding) => (
                      <tr key={holding.symbol} className="border-b border-sovereign-slate-700 last:border-0">
                        <td className="py-3 text-sm font-medium text-white">{holding.symbol}</td>
                        <td className="py-3 text-sm text-right text-sovereign-slate-300">{holding.shares}</td>
                        <td className="py-3 text-sm text-right text-sovereign-slate-300">${holding.avgCost.toFixed(2)}</td>
                        <td className="py-3 text-sm text-right text-sovereign-slate-300">${holding.currentPrice.toFixed(2)}</td>
                        <td className="py-3 text-sm text-right text-white">${holding.value.toLocaleString()}</td>
                        <td className={`py-3 text-sm text-right font-medium ${holding.gainLoss >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                          {holding.gainLoss >= 0 ? '+' : ''}{holding.gainLossPercent.toFixed(2)}%
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Right Column: Summary & Allocation */}
          <div className="space-y-6">
            {/* Summary Card */}
            <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
              <h2 className="text-lg font-medium text-white mb-4">Summary</h2>
              
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-sovereign-slate-400">Total Value</span>
                  <span className="text-lg font-medium text-white">
                    ${data.totalValue.toLocaleString()}
                  </span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm text-sovereign-slate-400">Total Gain/Loss</span>
                  <span className={`text-lg font-medium ${data.totalGainLoss >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                    {data.totalGainLoss >= 0 ? '+' : ''}${Math.abs(data.totalGainLoss).toLocaleString()}
                  </span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm text-sovereign-slate-400">Return</span>
                  <span className={`text-lg font-medium ${data.totalGainLossPercent >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                    {data.totalGainLossPercent >= 0 ? '+' : ''}{data.totalGainLossPercent.toFixed(2)}%
                  </span>
                </div>
              </div>
            </div>

            {/* Allocation Card */}
            <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
              <h2 className="text-lg font-medium text-white mb-4">Allocation</h2>
              
              {data.allocation && Object.keys(data.allocation).length > 0 ? (
                <div className="space-y-2">
                  {Object.entries(data.allocation).map(([sector, percent]) => (
                    <div key={sector}>
                      <div className="flex justify-between items-center mb-1">
                        <span className="text-xs text-sovereign-slate-400 capitalize">{sector}</span>
                        <span className="text-xs text-sovereign-slate-300">{percent}%</span>
                      </div>
                      <div className="h-2 bg-sovereign-slate-700 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-sovereign-gold"
                          style={{ width: `${percent}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <NoAllocationEmpty onAction={() => window.location.href = '/portfolio'} />
              )}
            </div>
          </div>
        </div>
      </main>

      {/* Premium Gates */}
      {showAnalyticsGate && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
          <div className="max-w-lg w-full mx-4">
            <PremiumGateAnalytics 
              onUpgrade={() => window.location.href = '/pricing'}
              onClose={() => setShowAnalyticsGate(false)}
            />
          </div>
        </div>
      )}

      {showCSVGate && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
          <div className="max-w-lg w-full mx-4">
            <PremiumGateCSVExport 
              onUpgrade={() => window.location.href = '/pricing'}
              onClose={() => setShowCSVGate(false)}
            />
          </div>
        </div>
      )}
    </div>
  );
}
