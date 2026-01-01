import React, { useEffect, useState } from 'react';
import { WifiOff, RefreshCw, Database } from 'lucide-react';

// ============================================================================
// OFFLINE STATE COMPONENT
// ============================================================================

interface OfflineStateProps {
  onRetry?: () => void;
  hasCachedData?: boolean;
  onViewCached?: () => void;
  className?: string;
}

/**
 * Offline State
 * Message: "You're offline — reconnect to continue."
 * Actions: Retry, View cached data (if available)
 */
export function OfflineState({ 
  onRetry, 
  hasCachedData = false,
  onViewCached,
  className = "" 
}: OfflineStateProps) {
  return (
    <div className={`flex flex-col items-center justify-center p-8 text-center ${className}`}>
      <div className="mb-4 text-sovereign-slate-400">
        <WifiOff className="w-12 h-12" />
      </div>
      
      <p className="text-base text-sovereign-slate-300 mb-6 max-w-md">
        You're offline — reconnect to continue.
      </p>
      
      <div className="flex gap-3">
        {onRetry && (
          <button
            onClick={onRetry}
            className="px-4 py-2 bg-sovereign-gold text-sovereign-obsidian rounded-lg hover:bg-sovereign-gold-hover transition-colors font-medium flex items-center gap-2"
          >
            <RefreshCw className="w-4 h-4" />
            Retry
          </button>
        )}
        
        {hasCachedData && onViewCached && (
          <button
            onClick={onViewCached}
            className="px-4 py-2 bg-sovereign-slate-700 text-white rounded-lg hover:bg-sovereign-slate-600 transition-colors font-medium flex items-center gap-2"
          >
            <Database className="w-4 h-4" />
            View Cached Data
          </button>
        )}
      </div>
    </div>
  );
}

// ============================================================================
// FULL-SCREEN OFFLINE OVERLAY
// ============================================================================

interface OfflineOverlayProps {
  hasCachedData?: boolean;
  onViewCached?: () => void;
  lastSyncTime?: Date;
}

/**
 * Full-screen offline overlay that appears when connection is lost
 * Auto-dismisses when online
 */
export function OfflineOverlay({ 
  hasCachedData = false,
  onViewCached,
  lastSyncTime
}: OfflineOverlayProps) {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Don't show overlay if online
  if (isOnline) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm">
      <div className="max-w-lg w-full mx-4 p-8 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700 text-center">
        <div className="mb-6 text-sovereign-slate-400">
          <WifiOff className="w-16 h-16 mx-auto" />
        </div>
        
        <h2 className="text-xl font-medium text-white mb-2">
          You're Offline
        </h2>
        
        <p className="text-base text-sovereign-slate-300 mb-6">
          Please check your internet connection to continue using DominionMarkets.
        </p>
        
        {lastSyncTime && (
          <p className="text-sm text-sovereign-slate-400 mb-6">
            Last synced: {lastSyncTime.toLocaleTimeString()}
          </p>
        )}
        
        <div className="flex flex-col gap-3">
          <button
            onClick={() => window.location.reload()}
            className="w-full px-4 py-2 bg-sovereign-gold text-sovereign-obsidian rounded-lg hover:bg-sovereign-gold-hover transition-colors font-medium flex items-center justify-center gap-2"
          >
            <RefreshCw className="w-4 h-4" />
            Check Connection
          </button>
          
          {hasCachedData && onViewCached && (
            <button
              onClick={onViewCached}
              className="w-full px-4 py-2 bg-sovereign-slate-700 text-white rounded-lg hover:bg-sovereign-slate-600 transition-colors font-medium flex items-center justify-center gap-2"
            >
              <Database className="w-4 h-4" />
              View Cached Data
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

// ============================================================================
// COMPACT OFFLINE INDICATOR (for nav bar)
// ============================================================================

/**
 * Small offline indicator for navigation bar
 */
export function CompactOfflineIndicator() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  if (isOnline) {
    return null;
  }

  return (
    <div className="flex items-center gap-2 px-3 py-1 bg-red-500/20 border border-red-500/50 rounded-full">
      <WifiOff className="w-4 h-4 text-red-400" />
      <span className="text-xs text-red-400 font-medium">Offline</span>
    </div>
  );
}

// ============================================================================
// RECONNECTING INDICATOR
// ============================================================================

interface ReconnectingProps {
  attemptNumber?: number;
}

/**
 * Shows when app is attempting to reconnect
 */
export function ReconnectingIndicator({ attemptNumber = 1 }: ReconnectingProps) {
  return (
    <div className="flex items-center gap-3 px-4 py-3 bg-sovereign-obsidian/90 border border-sovereign-slate-700 rounded-lg">
      <RefreshCw className="w-5 h-5 text-sovereign-gold animate-spin" />
      <div>
        <p className="text-sm text-white font-medium">Reconnecting…</p>
        <p className="text-xs text-sovereign-slate-400">
          Attempt {attemptNumber}
        </p>
      </div>
    </div>
  );
}

// ============================================================================
// CACHED DATA INDICATOR
// ============================================================================

interface CachedDataIndicatorProps {
  lastSyncTime: Date;
  onRefresh?: () => void;
}

/**
 * Shows when viewing cached data while offline
 */
export function CachedDataIndicator({ lastSyncTime, onRefresh }: CachedDataIndicatorProps) {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Only show if offline
  if (isOnline) {
    return null;
  }

  return (
    <div className="flex items-center justify-between px-4 py-3 bg-blue-500/10 border border-blue-500/30 rounded-lg mb-4">
      <div className="flex items-center gap-3">
        <Database className="w-5 h-5 text-blue-400" />
        <div>
          <p className="text-sm text-white font-medium">Viewing Cached Data</p>
          <p className="text-xs text-sovereign-slate-400">
            Last synced: {lastSyncTime.toLocaleTimeString()}
          </p>
        </div>
      </div>
      
      {onRefresh && isOnline && (
        <button
          onClick={onRefresh}
          className="text-xs text-blue-400 hover:text-blue-300 font-medium"
        >
          Refresh
        </button>
      )}
    </div>
  );
}

// ============================================================================
// MODULE-SPECIFIC CACHED DATA AVAILABILITY
// ============================================================================

/**
 * Determines which modules have cached data available
 */
export interface CachedDataStatus {
  portfolio: boolean;
  markets: boolean;
  news: boolean;
  alerts: boolean;
  settings: boolean;
}

/**
 * Hook to check cached data availability
 */
export function useCachedDataStatus(): CachedDataStatus {
  const [status, setStatus] = useState<CachedDataStatus>({
    portfolio: false,
    markets: false,
    news: false,
    alerts: false,
    settings: false
  });

  useEffect(() => {
    // Check localStorage for cached data
    const portfolioCached = localStorage.getItem('cached_portfolio') !== null;
    const newsCached = localStorage.getItem('cached_news') !== null;
    const alertsCached = localStorage.getItem('cached_alerts') !== null;
    const settingsCached = localStorage.getItem('cached_settings') !== null;

    setStatus({
      portfolio: portfolioCached,
      markets: false, // Markets require real-time data
      news: newsCached,
      alerts: alertsCached,
      settings: settingsCached
    });
  }, []);

  return status;
}

// ============================================================================
// OFFLINE-AWARE FETCH WRAPPER
// ============================================================================

interface OfflineFetchOptions {
  cacheKey?: string;
  maxCacheAge?: number; // milliseconds
}

/**
 * Fetch wrapper that handles offline scenarios with caching
 */
export async function offlineFetch<T>(
  url: string, 
  options?: RequestInit & OfflineFetchOptions
): Promise<{ data: T | null; fromCache: boolean; error?: string }> {
  const { cacheKey, maxCacheAge = 3600000, ...fetchOptions } = options || {};

  try {
    const response = await fetch(url, fetchOptions);
    const data = await response.json();

    // Cache successful response
    if (cacheKey) {
      localStorage.setItem(cacheKey, JSON.stringify({
        data,
        timestamp: Date.now()
      }));
    }

    return { data, fromCache: false };
  } catch (error) {
    // If offline, try to return cached data
    if (cacheKey) {
      const cached = localStorage.getItem(cacheKey);
      if (cached) {
        const { data, timestamp } = JSON.parse(cached);
        const age = Date.now() - timestamp;

        if (age < maxCacheAge) {
          return { data, fromCache: true };
        }
      }
    }

    return { 
      data: null, 
      fromCache: false, 
      error: 'Unable to fetch data and no valid cache available' 
    };
  }
}

// ============================================================================
// USAGE EXAMPLES
// ============================================================================

/**
 * Example: Full-screen offline overlay in root layout
 * 
 * function RootLayout({ children }) {
 *   return (
 *     <div>
 *       <OfflineOverlay
 *         hasCachedData={true}
 *         onViewCached={() => router.push('/portfolio?cached=true')}
 *         lastSyncTime={new Date()}
 *       />
 *       {children}
 *     </div>
 *   );
 * }
 */

/**
 * Example: Compact offline indicator in nav bar
 * 
 * function NavigationBar() {
 *   return (
 *     <nav className="flex items-center gap-4">
 *       <Logo />
 *       <CompactOfflineIndicator />
 *     </nav>
 *   );
 * }
 */

/**
 * Example: Fetch with offline support
 * 
 * async function fetchPortfolio() {
 *   const { data, fromCache, error } = await offlineFetch('/api/portfolio', {
 *     cacheKey: 'cached_portfolio',
 *     maxCacheAge: 3600000 // 1 hour
 *   });
 *   
 *   if (fromCache) {
 *     console.log('Showing cached portfolio data');
 *   }
 *   
 *   return data;
 * }
 */

/**
 * Example: Module with cached data indicator
 * 
 * function PortfolioModule() {
 *   const [isFromCache, setIsFromCache] = useState(false);
 *   const [lastSync, setLastSync] = useState(new Date());
 *   
 *   return (
 *     <div>
 *       {isFromCache && (
 *         <CachedDataIndicator
 *           lastSyncTime={lastSync}
 *           onRefresh={() => refetchData()}
 *         />
 *       )}
 *       <PortfolioContent />
 *     </div>
 *   );
 * }
 */
