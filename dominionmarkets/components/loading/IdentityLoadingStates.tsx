import React from 'react';
import { Loader2 } from 'lucide-react';

// ============================================================================
// BASE LOADING STATE COMPONENT
// ============================================================================

interface LoadingStateProps {
  message?: string;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

function LoadingState({ 
  message = "Loading…", 
  size = 'md',
  className = "" 
}: LoadingStateProps) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };

  return (
    <div className={`flex flex-col items-center justify-center p-8 text-center ${className}`}>
      <Loader2 className={`${sizeClasses[size]} text-sovereign-gold animate-spin mb-3`} />
      <p className="text-sm text-sovereign-slate-400">{message}</p>
    </div>
  );
}

// ============================================================================
// GLOBAL LOADING STATES
// ============================================================================

/**
 * Global Loading
 * Message: "Loading…"
 */
export function GlobalLoading({ size = 'md' }: { size?: 'sm' | 'md' | 'lg' }) {
  return <LoadingState message="Loading…" size={size} />;
}

// ============================================================================
// IDENTITY-AWARE LOADING STATES
// ============================================================================

type IdentityType = "diaspora" | "youth" | "creator" | "legacy";

interface IdentityLoadingProps {
  identity: IdentityType;
  module?: string;
  size?: 'sm' | 'md' | 'lg';
}

/**
 * Identity-aware loading with context-specific messages
 * 
 * Diaspora: "Loading regional insights…"
 * Youth: "Loading your learning dashboard…"
 * Creator: "Loading creator-economy data…"
 * Legacy: "Loading long-term indicators…"
 */
export function IdentityLoading({ identity, module, size = 'md' }: IdentityLoadingProps) {
  const messages: Record<IdentityType, string> = {
    diaspora: module ? `Loading ${module}…` : "Loading regional insights…",
    youth: module ? `Loading ${module}…` : "Loading your learning dashboard…",
    creator: module ? `Loading ${module}…` : "Loading creator-economy data…",
    legacy: module ? `Loading ${module}…` : "Loading long-term indicators…"
  };

  return <LoadingState message={messages[identity]} size={size} />;
}

// ============================================================================
// MODULE-SPECIFIC LOADING STATES
// ============================================================================

/**
 * Dashboard Loading
 */
export function DashboardLoading({ identity }: { identity?: IdentityType }) {
  if (identity) {
    return <IdentityLoading identity={identity} module="dashboard" />;
  }
  return <LoadingState message="Loading dashboard…" />;
}

/**
 * Markets Loading
 */
export function MarketsLoading({ identity }: { identity?: IdentityType }) {
  const messages: Record<IdentityType, string> = {
    diaspora: "Loading Caribbean markets…",
    youth: "Loading market basics…",
    creator: "Loading creator platforms…",
    legacy: "Loading dividend data…"
  };

  if (identity) {
    return <LoadingState message={messages[identity]} />;
  }
  return <LoadingState message="Loading market data…" />;
}

/**
 * Portfolio Loading
 */
export function PortfolioLoading({ identity }: { identity?: IdentityType }) {
  const messages: Record<IdentityType, string> = {
    diaspora: "Loading diaspora holdings…",
    youth: "Loading your first portfolio…",
    creator: "Loading creator investments…",
    legacy: "Loading retirement portfolio…"
  };

  if (identity) {
    return <LoadingState message={messages[identity]} />;
  }
  return <LoadingState message="Loading your portfolio…" />;
}

/**
 * News Loading
 */
export function NewsLoading() {
  return <LoadingState message="Loading verified news…" />;
}

/**
 * Alerts Loading
 */
export function AlertsLoading() {
  return <LoadingState message="Loading alerts…" />;
}

/**
 * Settings Loading
 */
export function SettingsLoading() {
  return <LoadingState message="Loading settings…" />;
}

/**
 * Stock Detail Loading
 */
export function StockDetailLoading() {
  return <LoadingState message="Loading company data…" />;
}

// ============================================================================
// INLINE LOADING STATE (for buttons and small components)
// ============================================================================

interface InlineLoadingProps {
  message?: string;
  size?: 'sm' | 'md' | 'lg';
}

/**
 * Inline loading spinner for buttons
 */
export function InlineLoading({ message, size = 'sm' }: InlineLoadingProps) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6'
  };

  return (
    <span className="flex items-center gap-2">
      <Loader2 className={`${sizeClasses[size]} animate-spin`} />
      {message && <span className="text-sm">{message}</span>}
    </span>
  );
}

// ============================================================================
// SKELETON LOADING STATES
// ============================================================================

/**
 * Generic skeleton loader
 */
export function SkeletonLoader({ 
  lines = 3, 
  className = "" 
}: { 
  lines?: number; 
  className?: string;
}) {
  return (
    <div className={`space-y-3 ${className}`}>
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className="h-4 bg-sovereign-slate-700 rounded animate-pulse"
          style={{ width: `${100 - i * 10}%` }}
        />
      ))}
    </div>
  );
}

/**
 * Card skeleton (for dashboard widgets)
 */
export function CardSkeleton({ className = "" }: { className?: string }) {
  return (
    <div className={`p-6 bg-sovereign-obsidian rounded-lg border border-sovereign-slate-700 ${className}`}>
      <div className="h-5 w-32 bg-sovereign-slate-700 rounded mb-4 animate-pulse" />
      <div className="space-y-3">
        <div className="h-4 w-full bg-sovereign-slate-700 rounded animate-pulse" />
        <div className="h-4 w-4/5 bg-sovereign-slate-700 rounded animate-pulse" />
        <div className="h-4 w-3/5 bg-sovereign-slate-700 rounded animate-pulse" />
      </div>
    </div>
  );
}

/**
 * Table skeleton (for data tables)
 */
export function TableSkeleton({ 
  rows = 5, 
  columns = 4,
  className = "" 
}: { 
  rows?: number; 
  columns?: number;
  className?: string;
}) {
  return (
    <div className={`space-y-3 ${className}`}>
      {/* Header */}
      <div className="flex gap-4 pb-3 border-b border-sovereign-slate-700">
        {Array.from({ length: columns }).map((_, i) => (
          <div key={i} className="h-4 flex-1 bg-sovereign-slate-700 rounded animate-pulse" />
        ))}
      </div>
      {/* Rows */}
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex gap-4">
          {Array.from({ length: columns }).map((_, j) => (
            <div key={j} className="h-4 flex-1 bg-sovereign-slate-700 rounded animate-pulse" />
          ))}
        </div>
      ))}
    </div>
  );
}

/**
 * Chart skeleton (for data visualizations)
 */
export function ChartSkeleton({ className = "" }: { className?: string }) {
  return (
    <div className={`flex items-end gap-2 h-48 ${className}`}>
      {Array.from({ length: 12 }).map((_, i) => {
        const height = Math.random() * 80 + 20; // Random height 20-100%
        return (
          <div
            key={i}
            className="flex-1 bg-sovereign-slate-700 rounded-t animate-pulse"
            style={{ height: `${height}%` }}
          />
        );
      })}
    </div>
  );
}

// ============================================================================
// IDENTITY-AWARE MODULE LOADING VARIATIONS
// ============================================================================

/**
 * Dashboard loading with identity-specific messages
 */
export function IdentityDashboardLoading({ identity }: { identity: IdentityType }) {
  const messages: Record<IdentityType, string> = {
    diaspora: "Loading regional insights…",
    youth: "Loading your learning dashboard…",
    creator: "Loading creator-economy data…",
    legacy: "Loading long-term indicators…"
  };

  return <LoadingState message={messages[identity]} />;
}

/**
 * Portfolio insights loading with identity context
 */
export function IdentityInsightsLoading({ identity }: { identity: IdentityType }) {
  const messages: Record<IdentityType, string> = {
    diaspora: "Loading diaspora market analysis…",
    youth: "Loading beginner-friendly insights…",
    creator: "Loading creator platform metrics…",
    legacy: "Loading dividend aristocrat data…"
  };

  return <LoadingState message={messages[identity]} />;
}

// ============================================================================
// LOADING STATE WITH TIMEOUT WARNING
// ============================================================================

interface LoadingWithTimeoutProps {
  message: string;
  timeoutMs?: number;
  onTimeout?: () => void;
}

/**
 * Shows loading state, then warning if it takes too long
 */
export function LoadingWithTimeout({ 
  message, 
  timeoutMs = 10000,
  onTimeout 
}: LoadingWithTimeoutProps) {
  const [showWarning, setShowWarning] = React.useState(false);

  React.useEffect(() => {
    const timer = setTimeout(() => {
      setShowWarning(true);
      onTimeout?.();
    }, timeoutMs);

    return () => clearTimeout(timer);
  }, [timeoutMs, onTimeout]);

  if (showWarning) {
    return (
      <div className="flex flex-col items-center justify-center p-8 text-center">
        <Loader2 className="w-8 h-8 text-sovereign-gold animate-spin mb-3" />
        <p className="text-sm text-sovereign-slate-400 mb-2">{message}</p>
        <p className="text-xs text-sovereign-slate-500">
          This is taking longer than expected…
        </p>
      </div>
    );
  }

  return <LoadingState message={message} />;
}

// ============================================================================
// USAGE EXAMPLES
// ============================================================================

/**
 * Example: Identity-aware dashboard loading
 * 
 * function Dashboard({ identity }: { identity: IdentityType }) {
 *   const { data, loading } = useQuery('/api/dashboard');
 *   
 *   if (loading) {
 *     return <IdentityDashboardLoading identity={identity} />;
 *   }
 *   
 *   return <div>{data.widgets}</div>;
 * }
 */

/**
 * Example: Button with inline loading
 * 
 * function SaveButton({ loading }: { loading: boolean }) {
 *   return (
 *     <button disabled={loading}>
 *       {loading ? <InlineLoading message="Saving…" /> : 'Save Changes'}
 *     </button>
 *   );
 * }
 */

/**
 * Example: Table with skeleton loader
 * 
 * function PortfolioTable() {
 *   const { data, loading } = useQuery('/api/portfolio');
 *   
 *   if (loading) {
 *     return <TableSkeleton rows={10} columns={5} />;
 *   }
 *   
 *   return <table>{data.holdings.map(...)}</table>;
 * }
 */

/**
 * Example: Loading with timeout warning
 * 
 * function MarketData() {
 *   return (
 *     <LoadingWithTimeout
 *       message="Loading market data…"
 *       timeoutMs={8000}
 *       onTimeout={() => console.log('Taking too long')}
 *     />
 *   );
 * }
 */
