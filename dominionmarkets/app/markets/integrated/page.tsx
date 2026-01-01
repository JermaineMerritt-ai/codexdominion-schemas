'use client';

import { useState, useEffect } from 'react';
import { 
  HeatmapError,
  MoversError,
  EarningsCalendarError
} from '@/components/errors/ModuleErrorStates';
import { 
  NoMoversEmpty,
  NoEarningsEmpty 
} from '@/components/empty/GlobalEmptyStates';
import { MarketsLoading } from '@/components/loading/IdentityLoadingStates';
import { TableSkeleton } from '@/components/loading/IdentityLoadingStates';

type IdentityType = "diaspora" | "youth" | "creator" | "legacy";
type TabType = "heatmap" | "movers" | "earnings";

interface Mover {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
}

interface EarningsEvent {
  symbol: string;
  name: string;
  date: string;
  time: string;
  estimate: number;
}

export default function MarketsPage() {
  const [identity, setIdentity] = useState<IdentityType>('diaspora');
  const [activeTab, setActiveTab] = useState<TabType>('movers');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<any>(null);
  const [gainers, setGainers] = useState<Mover[]>([]);
  const [losers, setLosers] = useState<Mover[]>([]);
  const [earnings, setEarnings] = useState<EarningsEvent[]>([]);

  useEffect(() => {
    fetchMarketsData();
  }, [activeTab]);

  const fetchMarketsData = async () => {
    setLoading(true);
    setError(null);

    try {
      const endpoint = 
        activeTab === 'movers' ? '/api/markets/movers' :
        activeTab === 'earnings' ? '/api/markets/earnings' :
        '/api/markets/heatmap';

      const response = await fetch(endpoint);
      
      if (!response.ok) {
        throw {
          status: response.status,
          message: response.statusText,
          type: response.status >= 500 ? 'server' : 'generic'
        };
      }

      const result = await response.json();
      
      if (activeTab === 'movers') {
        setGainers(result.gainers || []);
        setLosers(result.losers || []);
      } else if (activeTab === 'earnings') {
        setEarnings(result.events || []);
      }
    } catch (err: any) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-sovereign-obsidian">
      {/* Header */}
      <header className="border-b border-sovereign-slate-700 bg-sovereign-obsidian/50 backdrop-blur-sm sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white">Markets</h1>
              <p className="text-sm text-sovereign-slate-400">Real-time market data</p>
            </div>
            
            {/* Identity Selector */}
            <select
              value={identity}
              onChange={(e) => setIdentity(e.target.value as IdentityType)}
              className="px-3 py-1.5 bg-sovereign-slate-700 text-white rounded-lg text-sm"
            >
              <option value="diaspora">Diaspora</option>
              <option value="youth">Youth</option>
              <option value="creator">Creator</option>
              <option value="legacy">Legacy-Builder</option>
            </select>
          </div>

          {/* Tabs */}
          <div className="flex gap-4 mt-4">
            <button
              onClick={() => setActiveTab('movers')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                activeTab === 'movers'
                  ? 'bg-sovereign-gold text-sovereign-obsidian'
                  : 'bg-sovereign-slate-700 text-white hover:bg-sovereign-slate-600'
              }`}
            >
              Movers
            </button>
            <button
              onClick={() => setActiveTab('heatmap')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                activeTab === 'heatmap'
                  ? 'bg-sovereign-gold text-sovereign-obsidian'
                  : 'bg-sovereign-slate-700 text-white hover:bg-sovereign-slate-600'
              }`}
            >
              Heatmap
            </button>
            <button
              onClick={() => setActiveTab('earnings')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                activeTab === 'earnings'
                  ? 'bg-sovereign-gold text-sovereign-obsidian'
                  : 'bg-sovereign-slate-700 text-white hover:bg-sovereign-slate-600'
              }`}
            >
              Earnings
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {activeTab === 'movers' && (
          <MoversTab 
            loading={loading}
            error={error}
            gainers={gainers}
            losers={losers}
            identity={identity}
            onRetry={fetchMarketsData}
          />
        )}

        {activeTab === 'heatmap' && (
          <HeatmapTab 
            loading={loading}
            error={error}
            onRetry={fetchMarketsData}
          />
        )}

        {activeTab === 'earnings' && (
          <EarningsTab 
            loading={loading}
            error={error}
            earnings={earnings}
            onRetry={fetchMarketsData}
          />
        )}
      </main>
    </div>
  );
}

// ============================================================================
// TAB COMPONENTS
// ============================================================================

function MoversTab({ 
  loading, 
  error, 
  gainers, 
  losers,
  identity,
  onRetry 
}: { 
  loading: boolean;
  error: any;
  gainers: Mover[];
  losers: Mover[];
  identity: IdentityType;
  onRetry: () => void;
}) {
  // Show loading state
  if (loading) {
    return (
      <div className="space-y-6">
        <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
          <h2 className="text-lg font-medium text-white mb-4">Top Gainers</h2>
          <TableSkeleton rows={5} columns={5} />
        </div>
        <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
          <h2 className="text-lg font-medium text-white mb-4">Top Losers</h2>
          <TableSkeleton rows={5} columns={5} />
        </div>
      </div>
    );
  }

  // Show error state
  if (error) {
    return <MoversError onRetry={onRetry} />;
  }

  // Show empty state
  if (!gainers.length && !losers.length) {
    return <NoMoversEmpty />;
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Gainers */}
      <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
        <h2 className="text-lg font-medium text-white mb-4">Top Gainers</h2>
        
        {!gainers.length ? (
          <p className="text-sm text-sovereign-slate-400">No significant gains today.</p>
        ) : (
          <div className="space-y-3">
            {gainers.map((stock) => (
              <div key={stock.symbol} className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-white">{stock.symbol}</p>
                  <p className="text-xs text-sovereign-slate-400">{stock.name}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium text-green-400">
                    +{stock.changePercent.toFixed(2)}%
                  </p>
                  <p className="text-xs text-sovereign-slate-400">
                    ${stock.price.toFixed(2)}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Losers */}
      <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
        <h2 className="text-lg font-medium text-white mb-4">Top Losers</h2>
        
        {!losers.length ? (
          <p className="text-sm text-sovereign-slate-400">No significant losses today.</p>
        ) : (
          <div className="space-y-3">
            {losers.map((stock) => (
              <div key={stock.symbol} className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-white">{stock.symbol}</p>
                  <p className="text-xs text-sovereign-slate-400">{stock.name}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium text-red-400">
                    {stock.changePercent.toFixed(2)}%
                  </p>
                  <p className="text-xs text-sovereign-slate-400">
                    ${stock.price.toFixed(2)}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function HeatmapTab({ loading, error, onRetry }: { loading: boolean; error: any; onRetry: () => void }) {
  if (loading) {
    return (
      <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
        <h2 className="text-lg font-medium text-white mb-4">Market Heatmap</h2>
        <div className="h-96 flex items-center justify-center">
          <MarketsLoading />
        </div>
      </div>
    );
  }

  if (error) {
    return <HeatmapError onRetry={onRetry} />;
  }

  return (
    <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
      <h2 className="text-lg font-medium text-white mb-4">Market Heatmap</h2>
      <div className="h-96 flex items-center justify-center text-sovereign-slate-400">
        Heatmap visualization would render here
      </div>
    </div>
  );
}

function EarningsTab({ 
  loading, 
  error, 
  earnings,
  onRetry 
}: { 
  loading: boolean;
  error: any;
  earnings: EarningsEvent[];
  onRetry: () => void;
}) {
  if (loading) {
    return (
      <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
        <h2 className="text-lg font-medium text-white mb-4">Earnings Calendar</h2>
        <TableSkeleton rows={8} columns={4} />
      </div>
    );
  }

  if (error) {
    return <EarningsCalendarError onRetry={onRetry} />;
  }

  if (!earnings.length) {
    return (
      <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
        <h2 className="text-lg font-medium text-white mb-4">Earnings Calendar</h2>
        <NoEarningsEmpty />
      </div>
    );
  }

  return (
    <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
      <h2 className="text-lg font-medium text-white mb-4">Earnings Calendar</h2>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-sovereign-slate-700">
              <th className="text-left text-xs font-medium text-sovereign-slate-400 pb-3">Symbol</th>
              <th className="text-left text-xs font-medium text-sovereign-slate-400 pb-3">Company</th>
              <th className="text-left text-xs font-medium text-sovereign-slate-400 pb-3">Date</th>
              <th className="text-left text-xs font-medium text-sovereign-slate-400 pb-3">Time</th>
              <th className="text-right text-xs font-medium text-sovereign-slate-400 pb-3">Estimate</th>
            </tr>
          </thead>
          <tbody>
            {earnings.map((event) => (
              <tr key={`${event.symbol}-${event.date}`} className="border-b border-sovereign-slate-700 last:border-0">
                <td className="py-3 text-sm font-medium text-white">{event.symbol}</td>
                <td className="py-3 text-sm text-sovereign-slate-300">{event.name}</td>
                <td className="py-3 text-sm text-sovereign-slate-300">{event.date}</td>
                <td className="py-3 text-sm text-sovereign-slate-300">{event.time}</td>
                <td className="py-3 text-sm text-right text-sovereign-slate-300">${event.estimate.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
