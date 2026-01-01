'use client';

import { useState, useEffect } from 'react';
import { 
  SmartErrorBoundary,
  DashboardLoading,
  NoPortfolioEmpty,
  NoWatchlistEmpty,
  NoAlertsEmpty
} from '@/components/errors/GlobalErrorStates';
import { MarketTickerError, PortfolioSnapshotError, DashboardNewsError } from '@/components/errors/ModuleErrorStates';
import { CompactOfflineIndicator } from '@/components/offline/OfflineState';

type IdentityType = "diaspora" | "youth" | "creator" | "legacy";

interface DashboardData {
  portfolio: {
    value: number;
    holdings: any[];
  };
  watchlist: any[];
  alerts: any[];
  news: any[];
  marketTicker: any;
}

export default function DashboardPage() {
  const [identity, setIdentity] = useState<IdentityType>('diaspora');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<any>(null);
  const [data, setData] = useState<DashboardData | null>(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/dashboard');
      
      if (!response.ok) {
        throw {
          status: response.status,
          message: response.statusText,
          type: response.status === 401 ? 'auth' : 
                response.status >= 500 ? 'server' : 'generic'
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

  // Show identity-aware loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-sovereign-obsidian p-6">
        <DashboardLoading identity={identity} />
      </div>
    );
  }

  // Show error state with smart detection
  if (error) {
    return (
      <div className="min-h-screen bg-sovereign-obsidian p-6">
        <SmartErrorBoundary 
          error={error} 
          onRetry={fetchDashboardData}
          onLogin={() => window.location.href = '/login'}
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-sovereign-obsidian">
      {/* Header with offline indicator */}
      <header className="border-b border-sovereign-slate-700 bg-sovereign-obsidian/50 backdrop-blur-sm sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">DominionMarkets</h1>
            <p className="text-sm text-sovereign-slate-400">Dashboard</p>
          </div>
          
          {/* Identity Selector */}
          <div className="flex items-center gap-4">
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
            
            <CompactOfflineIndicator />
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column: Portfolio & Watchlist */}
          <div className="lg:col-span-2 space-y-6">
            {/* Market Ticker Widget */}
            <MarketTickerWidget data={data?.marketTicker} onRetry={fetchDashboardData} />

            {/* Portfolio Widget */}
            <PortfolioWidget 
              data={data?.portfolio} 
              identity={identity}
              onRetry={fetchDashboardData}
            />

            {/* News Widget */}
            <NewsWidget 
              data={data?.news}
              onRetry={fetchDashboardData}
            />
          </div>

          {/* Right Column: Alerts & Watchlist */}
          <div className="space-y-6">
            {/* Watchlist Widget */}
            <WatchlistWidget 
              data={data?.watchlist}
              onRetry={fetchDashboardData}
            />

            {/* Alerts Widget */}
            <AlertsWidget 
              data={data?.alerts}
              identity={identity}
              onRetry={fetchDashboardData}
            />
          </div>
        </div>
      </main>
    </div>
  );
}

// ============================================================================
// WIDGETS WITH ERROR HANDLING
// ============================================================================

function MarketTickerWidget({ data, onRetry }: { data: any; onRetry: () => void }) {
  if (!data) {
    return (
      <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
        <MarketTickerError onRetry={onRetry} />
      </div>
    );
  }

  return (
    <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
      <h2 className="text-lg font-medium text-white mb-4">Market Overview</h2>
      <div className="grid grid-cols-3 gap-4">
        <div>
          <p className="text-xs text-sovereign-slate-400">S&P 500</p>
          <p className="text-lg font-medium text-green-400">+0.45%</p>
        </div>
        <div>
          <p className="text-xs text-sovereign-slate-400">NASDAQ</p>
          <p className="text-lg font-medium text-green-400">+0.72%</p>
        </div>
        <div>
          <p className="text-xs text-sovereign-slate-400">DOW</p>
          <p className="text-lg font-medium text-red-400">-0.12%</p>
        </div>
      </div>
    </div>
  );
}

function PortfolioWidget({ 
  data, 
  identity,
  onRetry 
}: { 
  data: any; 
  identity: IdentityType;
  onRetry: () => void;
}) {
  if (!data) {
    return (
      <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
        <PortfolioSnapshotError onRetry={onRetry} />
      </div>
    );
  }

  if (!data.holdings?.length) {
    return (
      <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
        <NoPortfolioEmpty 
          identity={identity}
          onAction={() => window.location.href = '/portfolio'}
        />
      </div>
    );
  }

  return (
    <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
      <h2 className="text-lg font-medium text-white mb-4">Portfolio</h2>
      <div className="space-y-3">
        <div className="flex justify-between items-center">
          <span className="text-sovereign-slate-400">Total Value</span>
          <span className="text-xl font-medium text-white">${data.value.toLocaleString()}</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-sovereign-slate-400">Holdings</span>
          <span className="text-sovereign-slate-300">{data.holdings.length} stocks</span>
        </div>
      </div>
    </div>
  );
}

function NewsWidget({ data, onRetry }: { data: any; onRetry: () => void }) {
  if (!data) {
    return (
      <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
        <DashboardNewsError onRetry={onRetry} />
      </div>
    );
  }

  if (!data.length) {
    return (
      <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
        <h2 className="text-lg font-medium text-white mb-4">Latest News</h2>
        <p className="text-sm text-sovereign-slate-400">No news available — check back later.</p>
      </div>
    );
  }

  return (
    <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
      <h2 className="text-lg font-medium text-white mb-4">Latest News</h2>
      <div className="space-y-3">
        {data.slice(0, 5).map((article: any, i: number) => (
          <div key={i} className="border-b border-sovereign-slate-700 pb-3 last:border-0">
            <p className="text-sm text-white">{article.title}</p>
            <p className="text-xs text-sovereign-slate-400 mt-1">{article.source}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function WatchlistWidget({ data, onRetry }: { data: any; onRetry: () => void }) {
  if (!data?.length) {
    return (
      <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
        <NoWatchlistEmpty onAction={() => window.location.href = '/markets'} />
      </div>
    );
  }

  return (
    <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
      <h2 className="text-lg font-medium text-white mb-4">Watchlist</h2>
      <div className="space-y-2">
        {data.map((stock: any, i: number) => (
          <div key={i} className="flex justify-between items-center">
            <span className="text-sm text-white">{stock.symbol}</span>
            <span className="text-sm text-green-400">+{stock.change}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function AlertsWidget({ 
  data, 
  identity,
  onRetry 
}: { 
  data: any; 
  identity: IdentityType;
  onRetry: () => void;
}) {
  if (!data?.length) {
    return (
      <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
        <NoAlertsEmpty 
          identity={identity}
          onAction={() => window.location.href = '/alerts'}
        />
      </div>
    );
  }

  return (
    <div className="p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700">
      <h2 className="text-lg font-medium text-white mb-4">Active Alerts</h2>
      <div className="space-y-2">
        {data.map((alert: any, i: number) => (
          <div key={i} className="text-sm text-sovereign-slate-300">
            {alert.title}
          </div>
        ))}
      </div>
    </div>
  );
}
