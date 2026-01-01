import React from 'react';
import { 
  Inbox, 
  PlusCircle, 
  Eye, 
  Bell, 
  Newspaper,
  Search,
  TrendingUp
} from 'lucide-react';

// ============================================================================
// BASE EMPTY STATE COMPONENT
// ============================================================================

interface EmptyStateProps {
  message: string;
  icon: React.ReactNode;
  actionLabel?: string;
  onAction?: () => void;
  secondaryLabel?: string;
  onSecondary?: () => void;
  className?: string;
}

function EmptyState({ 
  message, 
  icon, 
  actionLabel,
  onAction,
  secondaryLabel,
  onSecondary,
  className = "" 
}: EmptyStateProps) {
  return (
    <div className={`flex flex-col items-center justify-center p-8 text-center ${className}`}>
      <div className="mb-4 text-sovereign-slate-400">
        {icon}
      </div>
      <p className="text-base text-sovereign-slate-300 mb-6 max-w-md">
        {message}
      </p>
      <div className="flex gap-3">
        {onAction && (
          <button
            onClick={onAction}
            className="px-4 py-2 bg-sovereign-gold text-sovereign-obsidian rounded-lg hover:bg-sovereign-gold-hover transition-colors font-medium"
          >
            {actionLabel}
          </button>
        )}
        {onSecondary && (
          <button
            onClick={onSecondary}
            className="px-4 py-2 bg-sovereign-slate-700 text-white rounded-lg hover:bg-sovereign-slate-600 transition-colors font-medium"
          >
            {secondaryLabel}
          </button>
        )}
      </div>
    </div>
  );
}

// ============================================================================
// DASHBOARD EMPTY STATES
// ============================================================================

type IdentityType = "diaspora" | "youth" | "creator" | "legacy";

interface IdentityEmptyStateProps {
  identity: IdentityType;
  onAction?: () => void;
}

/**
 * No Portfolio
 * Message: Identity-aware "No holdings yet — add your first stock."
 */
export function NoPortfolioEmpty({ identity, onAction }: IdentityEmptyStateProps) {
  const messages: Record<IdentityType, string> = {
    diaspora: "No holdings yet — add your first Caribbean or international stock.",
    youth: "No holdings yet — add your first stock and start learning.",
    creator: "No holdings yet — add your first creator-economy stock.",
    legacy: "No holdings yet — add your first dividend stock."
  };

  return (
    <EmptyState
      message={messages[identity]}
      icon={<PlusCircle className="w-12 h-12" />}
      actionLabel="Add Stock"
      onAction={onAction}
    />
  );
}

/**
 * No Watchlist
 * Message: "Your watchlist is empty — search for a company to add."
 */
export function NoWatchlistEmpty({ onAction }: { onAction?: () => void }) {
  return (
    <EmptyState
      message="Your watchlist is empty — search for a company to add."
      icon={<Eye className="w-12 h-12" />}
      actionLabel="Search Companies"
      onAction={onAction}
    />
  );
}

/**
 * No Alerts
 * Message: Identity-aware "No alerts yet — create your first alert."
 */
export function NoAlertsEmpty({ identity, onAction }: IdentityEmptyStateProps) {
  const messages: Record<IdentityType, string> = {
    diaspora: "No alerts yet — track Caribbean market movements.",
    youth: "No alerts yet — get notified when your stocks move.",
    creator: "No alerts yet — track creator-economy earnings.",
    legacy: "No alerts yet — monitor dividend announcements."
  };

  return (
    <EmptyState
      message={messages[identity]}
      icon={<Bell className="w-12 h-12" />}
      actionLabel="Create Alert"
      onAction={onAction}
    />
  );
}

/**
 * No News
 * Message: "No news available — check back later."
 */
export function NoNewsEmpty() {
  return (
    <EmptyState
      message="No news available — check back later."
      icon={<Newspaper className="w-12 h-12" />}
    />
  );
}

// ============================================================================
// MARKETS EMPTY STATES
// ============================================================================

/**
 * No Movers
 * Message: "No significant movement at the moment."
 */
export function NoMoversEmpty() {
  return (
    <EmptyState
      message="No significant movement at the moment."
      icon={<TrendingUp className="w-12 h-12" />}
    />
  );
}

/**
 * No Earnings Today
 * Message: "No companies reporting earnings today."
 */
export function NoEarningsEmpty() {
  return (
    <EmptyState
      message="No companies reporting earnings today."
      icon={<Inbox className="w-12 h-12" />}
    />
  );
}

// ============================================================================
// STOCK DETAIL EMPTY STATES
// ============================================================================

/**
 * No News (Stock Detail)
 * Message: "No recent news for this company."
 */
export function NoStockNewsEmpty() {
  return (
    <EmptyState
      message="No recent news for this company."
      icon={<Newspaper className="w-12 h-12" />}
    />
  );
}

// ============================================================================
// PORTFOLIO EMPTY STATES
// ============================================================================

/**
 * No Holdings
 * Message: Identity-aware "No holdings yet — add your first stock."
 */
export function NoHoldingsEmpty({ identity, onAction }: IdentityEmptyStateProps) {
  const messages: Record<IdentityType, string> = {
    diaspora: "No holdings yet — add your first Caribbean or international stock.",
    youth: "No holdings yet — add your first stock and start learning.",
    creator: "No holdings yet — add your first creator-economy stock.",
    legacy: "No holdings yet — add your first dividend stock."
  };

  return (
    <EmptyState
      message={messages[identity]}
      icon={<PlusCircle className="w-12 h-12" />}
      actionLabel="Add Stock"
      onAction={onAction}
    />
  );
}

/**
 * No Allocation Data
 * Message: "Add holdings to see your allocation."
 */
export function NoAllocationEmpty({ onAction }: { onAction?: () => void }) {
  return (
    <EmptyState
      message="Add holdings to see your allocation."
      icon={<Inbox className="w-12 h-12" />}
      actionLabel="Add Stock"
      onAction={onAction}
    />
  );
}

// ============================================================================
// NEWS VERIFICATION EMPTY STATES
// ============================================================================

/**
 * No Sources
 * Message: "No sources available for this story."
 */
export function NoSourcesEmpty() {
  return (
    <EmptyState
      message="No sources available for this story."
      icon={<Inbox className="w-12 h-12" />}
    />
  );
}

/**
 * No Related Companies
 * Message: "No related companies found."
 */
export function NoRelatedCompaniesEmpty() {
  return (
    <EmptyState
      message="No related companies found."
      icon={<Search className="w-12 h-12" />}
    />
  );
}

// ============================================================================
// SETTINGS EMPTY STATES
// ============================================================================

/**
 * No Billing History
 * Message: "No billing history available."
 */
export function NoBillingHistoryEmpty() {
  return (
    <EmptyState
      message="No billing history available."
      icon={<Inbox className="w-12 h-12" />}
    />
  );
}

/**
 * No Connected Devices
 * Message: "No devices connected."
 */
export function NoConnectedDevicesEmpty() {
  return (
    <EmptyState
      message="No devices connected."
      icon={<Inbox className="w-12 h-12" />}
    />
  );
}

// ============================================================================
// COMPACT EMPTY STATE (for small widgets)
// ============================================================================

interface CompactEmptyProps {
  message: string;
  actionLabel?: string;
  onAction?: () => void;
}

/**
 * Smaller empty state for widget-sized components
 */
export function CompactEmpty({ message, actionLabel, onAction }: CompactEmptyProps) {
  return (
    <div className="flex flex-col items-center justify-center p-6 text-center">
      <Inbox className="w-8 h-8 text-sovereign-slate-400 mb-2" />
      <p className="text-sm text-sovereign-slate-300 mb-3">{message}</p>
      {onAction && (
        <button
          onClick={onAction}
          className="text-xs text-sovereign-gold hover:text-sovereign-gold-hover font-medium"
        >
          {actionLabel}
        </button>
      )}
    </div>
  );
}

// ============================================================================
// GENERIC EMPTY STATE (fallback)
// ============================================================================

interface GenericEmptyProps {
  title?: string;
  message: string;
  actionLabel?: string;
  onAction?: () => void;
}

/**
 * Generic empty state with optional title
 */
export function GenericEmpty({ 
  title, 
  message, 
  actionLabel, 
  onAction 
}: GenericEmptyProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center">
      <Inbox className="w-12 h-12 text-sovereign-slate-400 mb-4" />
      {title && (
        <h3 className="text-lg font-medium text-white mb-2">{title}</h3>
      )}
      <p className="text-base text-sovereign-slate-300 mb-6 max-w-md">{message}</p>
      {onAction && (
        <button
          onClick={onAction}
          className="px-4 py-2 bg-sovereign-gold text-sovereign-obsidian rounded-lg hover:bg-sovereign-gold-hover transition-colors font-medium"
        >
          {actionLabel}
        </button>
      )}
    </div>
  );
}

// ============================================================================
// USAGE EXAMPLES
// ============================================================================

/**
 * Example: Dashboard portfolio widget
 * 
 * function PortfolioWidget({ identity }: { identity: IdentityType }) {
 *   const { data, loading } = useQuery('/api/portfolio');
 *   
 *   if (!data?.holdings?.length) {
 *     return (
 *       <NoPortfolioEmpty 
 *         identity={identity} 
 *         onAction={() => router.push('/portfolio')} 
 *       />
 *     );
 *   }
 *   
 *   return <div>{data.holdings.map(h => ...)}</div>;
 * }
 */

/**
 * Example: Alerts module with identity awareness
 * 
 * function AlertsModule({ identity }: { identity: IdentityType }) {
 *   const { data } = useQuery('/api/alerts');
 *   
 *   if (!data?.alerts?.length) {
 *     return (
 *       <NoAlertsEmpty 
 *         identity={identity}
 *         onAction={() => openCreateModal()} 
 *       />
 *     );
 *   }
 *   
 *   return <AlertsList alerts={data.alerts} />;
 * }
 */

/**
 * Example: Compact empty state in small widget
 * 
 * function WatchlistWidget() {
 *   const { data } = useQuery('/api/watchlist');
 *   
 *   if (!data?.symbols?.length) {
 *     return (
 *       <CompactEmpty
 *         message="Watchlist empty"
 *         actionLabel="Add Stock"
 *         onAction={() => openSearch()}
 *       />
 *     );
 *   }
 *   
 *   return <div>{data.symbols.map(s => ...)}</div>;
 * }
 */
