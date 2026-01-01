import React from 'react';
import { 
  TrendingUp, 
  Briefcase, 
  Newspaper, 
  User,
  Grid,
  BarChart3,
  Calendar,
  Building2,
  LineChart,
  Lightbulb,
  ShieldAlert,
  Link,
  Clock,
  Bell,
  AlertCircle,
  Save,
  CreditCard,
  Download,
  RefreshCw
} from 'lucide-react';

// ============================================================================
// BASE MODULE ERROR COMPONENT
// ============================================================================

interface ModuleErrorProps {
  message: string;
  icon: React.ReactNode;
  onRetry?: () => void;
  className?: string;
}

function ModuleError({ message, icon, onRetry, className = "" }: ModuleErrorProps) {
  return (
    <div className={`flex flex-col items-center justify-center p-6 text-center ${className}`}>
      <div className="mb-3 text-sovereign-slate-400">
        {icon}
      </div>
      <p className="text-sm text-sovereign-slate-300 mb-4">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-3 py-1.5 bg-sovereign-gold text-sovereign-obsidian rounded text-sm hover:bg-sovereign-gold-hover transition-colors font-medium flex items-center gap-2"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          Retry
        </button>
      )}
    </div>
  );
}

// ============================================================================
// DASHBOARD MODULE ERRORS
// ============================================================================

export function MarketTickerError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Market data unavailable — retry."
      icon={<TrendingUp className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

export function PortfolioSnapshotError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Unable to load your portfolio."
      icon={<Briefcase className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

export function DashboardNewsError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="News temporarily unavailable."
      icon={<Newspaper className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

export function IdentityWidgetError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Unable to load identity insights."
      icon={<User className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

// ============================================================================
// MARKETS MODULE ERRORS
// ============================================================================

export function HeatmapError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Unable to load heatmap."
      icon={<Grid className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

export function MoversError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Unable to load market movers."
      icon={<TrendingUp className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

export function VolumeSpikesError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Unable to load volume data."
      icon={<BarChart3 className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

export function EarningsCalendarError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Earnings data temporarily unavailable."
      icon={<Calendar className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

// ============================================================================
// STOCK DETAIL MODULE ERRORS
// ============================================================================

export function StockOverviewError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Unable to load company data."
      icon={<Building2 className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

export function StockChartError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Chart data unavailable."
      icon={<LineChart className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

export function StockNewsError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="No verified news available."
      icon={<Newspaper className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

export function StockInsightsError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Unable to load insights."
      icon={<Lightbulb className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

// ============================================================================
// PORTFOLIO MODULE ERRORS
// ============================================================================

export function PortfolioLoadError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Unable to load your portfolio."
      icon={<Briefcase className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

export function HoldingUpdateError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Unable to update holding."
      icon={<AlertCircle className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

export function AnalyticsError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Analytics temporarily unavailable."
      icon={<BarChart3 className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

// ============================================================================
// NEWS VERIFICATION MODULE ERRORS
// ============================================================================

export function VerificationError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Unable to verify this story."
      icon={<ShieldAlert className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

export function SourceLoadError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Unable to load sources."
      icon={<Link className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

export function TimelineError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Timeline unavailable."
      icon={<Clock className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

// ============================================================================
// ALERTS MODULE ERRORS
// ============================================================================

export function AlertCreationError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Unable to create alert."
      icon={<Bell className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

export function AlertUpdateError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Unable to update alert."
      icon={<AlertCircle className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

export function AlertLoadError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Unable to load alerts."
      icon={<Bell className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

// ============================================================================
// SETTINGS MODULE ERRORS
// ============================================================================

export function SettingsSaveError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Unable to save changes."
      icon={<Save className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

export function BillingError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Payment method could not be updated."
      icon={<CreditCard className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

export function IdentitySwitchError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Unable to update identity."
      icon={<User className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

export function DataExportError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ModuleError
      message="Export unavailable — try again later."
      icon={<Download className="w-10 h-10" />}
      onRetry={onRetry}
    />
  );
}

// ============================================================================
// USAGE EXAMPLES
// ============================================================================

/**
 * Example: Dashboard widget with specific error
 * 
 * function MarketTickerWidget() {
 *   const { data, error, refetch } = useQuery('/api/markets/ticker');
 *   
 *   if (error) {
 *     return <MarketTickerError onRetry={refetch} />;
 *   }
 *   
 *   return <div>{data.ticker}</div>;
 * }
 */

/**
 * Example: Portfolio module with error handling
 * 
 * function PortfolioModule() {
 *   const { data, error, refetch } = useQuery('/api/portfolio');
 *   
 *   if (error) {
 *     return <PortfolioLoadError onRetry={refetch} />;
 *   }
 *   
 *   return <PortfolioTable data={data} />;
 * }
 */

/**
 * Example: Settings save with error state
 * 
 * function SettingsForm() {
 *   const [saveError, setSaveError] = useState(false);
 *   
 *   const handleSave = async () => {
 *     try {
 *       await saveSettings();
 *     } catch (error) {
 *       setSaveError(true);
 *     }
 *   };
 *   
 *   if (saveError) {
 *     return <SettingsSaveError onRetry={handleSave} />;
 *   }
 *   
 *   return <form onSubmit={handleSave}>...</form>;
 * }
 */
