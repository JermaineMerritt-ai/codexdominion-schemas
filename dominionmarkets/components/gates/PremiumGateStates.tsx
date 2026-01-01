import React from 'react';
import { Lock, Crown, X, ArrowRight } from 'lucide-react';

// ============================================================================
// BASE PREMIUM GATE COMPONENT
// ============================================================================

interface PremiumGateProps {
  tier: 'premium' | 'pro';
  message: string;
  features?: string[];
  onUpgrade?: () => void;
  onClose?: () => void;
  className?: string;
}

function PremiumGate({ 
  tier, 
  message, 
  features,
  onUpgrade, 
  onClose,
  className = "" 
}: PremiumGateProps) {
  const Icon = tier === 'pro' ? Crown : Lock;
  const tierColor = tier === 'pro' ? 'text-purple-400' : 'text-sovereign-gold';
  const buttonColor = tier === 'pro' 
    ? 'bg-purple-500 hover:bg-purple-600 text-white' 
    : 'bg-sovereign-gold hover:bg-sovereign-gold-hover text-sovereign-obsidian';

  return (
    <div className={`relative p-6 bg-sovereign-obsidian/80 backdrop-blur-sm rounded-lg border border-sovereign-slate-700 ${className}`}>
      {/* Close button (optional) */}
      {onClose && (
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-sovereign-slate-400 hover:text-white transition-colors"
          aria-label="Close"
        >
          <X className="w-5 h-5" />
        </button>
      )}

      <div className="flex flex-col items-center text-center">
        {/* Icon */}
        <div className={`mb-4 ${tierColor}`}>
          <Icon className="w-12 h-12" />
        </div>

        {/* Message */}
        <p className="text-base text-sovereign-slate-200 mb-4 max-w-md">
          {message}
        </p>

        {/* Features (optional) */}
        {features && features.length > 0 && (
          <ul className="mb-6 space-y-2 text-sm text-sovereign-slate-300 text-left">
            {features.map((feature, i) => (
              <li key={i} className="flex items-start gap-2">
                <ArrowRight className="w-4 h-4 mt-0.5 text-sovereign-gold flex-shrink-0" />
                <span>{feature}</span>
              </li>
            ))}
          </ul>
        )}

        {/* Actions */}
        <div className="flex gap-3">
          {onUpgrade && (
            <button
              onClick={onUpgrade}
              className={`px-6 py-2 rounded-lg font-medium transition-colors ${buttonColor}`}
            >
              Upgrade to {tier === 'pro' ? 'Pro' : 'Premium'}
            </button>
          )}
          {onClose && (
            <button
              onClick={onClose}
              className="px-6 py-2 bg-sovereign-slate-700 text-white rounded-lg hover:bg-sovereign-slate-600 transition-colors font-medium"
            >
              Close
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

// ============================================================================
// PREMIUM TIER GATES
// ============================================================================

interface GateProps {
  onUpgrade?: () => void;
  onClose?: () => void;
}

/**
 * Generic Premium Gate
 * Message: "Upgrade to Premium to unlock this feature."
 */
export function PremiumGateGeneric({ onUpgrade, onClose }: GateProps) {
  return (
    <PremiumGate
      tier="premium"
      message="Upgrade to Premium to unlock this feature."
      onUpgrade={onUpgrade}
      onClose={onClose}
    />
  );
}

/**
 * CSV Export Gate
 * Message: "Upgrade to Premium to export portfolios as CSV."
 */
export function PremiumGateCSVExport({ onUpgrade, onClose }: GateProps) {
  return (
    <PremiumGate
      tier="premium"
      message="Upgrade to Premium to export portfolios as CSV."
      features={[
        "Export holdings to Excel/CSV",
        "Schedule automatic exports",
        "Historical portfolio snapshots"
      ]}
      onUpgrade={onUpgrade}
      onClose={onClose}
    />
  );
}

/**
 * Advanced Charts Gate
 * Message: "Upgrade to Premium for technical indicators."
 */
export function PremiumGateAdvancedCharts({ onUpgrade, onClose }: GateProps) {
  return (
    <PremiumGate
      tier="premium"
      message="Upgrade to Premium for technical indicators."
      features={[
        "RSI, MACD, Bollinger Bands",
        "Custom timeframes",
        "Comparison charts"
      ]}
      onUpgrade={onUpgrade}
      onClose={onClose}
    />
  );
}

/**
 * Multi-Portfolio Gate
 * Message: "Upgrade to Premium for unlimited portfolios."
 */
export function PremiumGateMultiPortfolio({ onUpgrade, onClose }: GateProps) {
  return (
    <PremiumGate
      tier="premium"
      message="Upgrade to Premium for unlimited portfolios."
      features={[
        "Create unlimited portfolios",
        "Track retirement, trading, long-term separately",
        "Compare performance across portfolios"
      ]}
      onUpgrade={onUpgrade}
      onClose={onClose}
    />
  );
}

/**
 * AI Insights Gate
 * Message: "Upgrade to Premium to unlock AI-powered insights."
 */
export function PremiumGateAIInsights({ onUpgrade, onClose }: GateProps) {
  return (
    <PremiumGate
      tier="premium"
      message="Upgrade to Premium to unlock AI-powered insights."
      features={[
        "AI-generated stock summaries",
        "Sentiment analysis on news",
        "Portfolio optimization suggestions"
      ]}
      onUpgrade={onUpgrade}
      onClose={onClose}
    />
  );
}

/**
 * Earnings Alerts Gate
 * Message: "Upgrade to Premium to unlock earnings alerts."
 */
export function PremiumGateEarningsAlerts({ onUpgrade, onClose }: GateProps) {
  return (
    <PremiumGate
      tier="premium"
      message="Upgrade to Premium to unlock earnings alerts."
      features={[
        "Get notified before earnings",
        "Track analyst estimates",
        "Historical earnings data"
      ]}
      onUpgrade={onUpgrade}
      onClose={onClose}
    />
  );
}

/**
 * Portfolio Analytics Gate
 * Message: "Upgrade to Premium to unlock analytics."
 */
export function PremiumGateAnalytics({ onUpgrade, onClose }: GateProps) {
  return (
    <PremiumGate
      tier="premium"
      message="Upgrade to Premium to unlock analytics."
      features={[
        "Sector allocation breakdown",
        "Risk metrics (beta, volatility)",
        "Performance attribution"
      ]}
      onUpgrade={onUpgrade}
      onClose={onClose}
    />
  );
}

// ============================================================================
// PRO TIER GATES
// ============================================================================

/**
 * Generic Pro Gate
 * Message: "Upgrade to Pro for advanced tools."
 */
export function ProGateGeneric({ onUpgrade, onClose }: GateProps) {
  return (
    <PremiumGate
      tier="pro"
      message="Upgrade to Pro for advanced tools."
      onUpgrade={onUpgrade}
      onClose={onClose}
    />
  );
}

/**
 * API Access Gate
 * Message: "Upgrade to Pro for API access."
 */
export function ProGateAPIAccess({ onUpgrade, onClose }: GateProps) {
  return (
    <PremiumGate
      tier="pro"
      message="Upgrade to Pro for API access."
      features={[
        "RESTful API for portfolio data",
        "10,000 API calls per month",
        "Real-time webhooks"
      ]}
      onUpgrade={onUpgrade}
      onClose={onClose}
    />
  );
}

/**
 * Institutional Tools Gate
 * Message: "Upgrade to Pro for institutional analytics."
 */
export function ProGateInstitutional({ onUpgrade, onClose }: GateProps) {
  return (
    <PremiumGate
      tier="pro"
      message="Upgrade to Pro for institutional analytics."
      features={[
        "Advanced risk modeling",
        "Factor analysis",
        "Multi-asset class support"
      ]}
      onUpgrade={onUpgrade}
      onClose={onClose}
    />
  );
}

/**
 * White-Label Gate
 * Message: "Upgrade to Pro for white-label branding."
 */
export function ProGateWhiteLabel({ onUpgrade, onClose }: GateProps) {
  return (
    <PremiumGate
      tier="pro"
      message="Upgrade to Pro for white-label branding."
      features={[
        "Remove DominionMarkets branding",
        "Custom domain support",
        "Team collaboration tools"
      ]}
      onUpgrade={onUpgrade}
      onClose={onClose}
    />
  );
}

// ============================================================================
// INLINE PREMIUM BADGE (for feature labels)
// ============================================================================

interface PremiumBadgeProps {
  tier: 'premium' | 'pro';
  size?: 'sm' | 'md';
}

/**
 * Small badge to show feature requires Premium/Pro
 */
export function PremiumBadge({ tier, size = 'sm' }: PremiumBadgeProps) {
  const Icon = tier === 'pro' ? Crown : Lock;
  const bgColor = tier === 'pro' ? 'bg-purple-500/20' : 'bg-sovereign-gold/20';
  const textColor = tier === 'pro' ? 'text-purple-400' : 'text-sovereign-gold';
  const sizeClasses = size === 'sm' ? 'text-xs px-2 py-0.5' : 'text-sm px-3 py-1';

  return (
    <span className={`inline-flex items-center gap-1 ${bgColor} ${textColor} rounded-full ${sizeClasses} font-medium`}>
      <Icon className="w-3 h-3" />
      {tier === 'pro' ? 'Pro' : 'Premium'}
    </span>
  );
}

// ============================================================================
// OVERLAY PREMIUM GATE (full-screen modal)
// ============================================================================

interface OverlayGateProps {
  tier: 'premium' | 'pro';
  message: string;
  features?: string[];
  onUpgrade?: () => void;
  onClose?: () => void;
}

/**
 * Full-screen premium gate modal
 */
export function OverlayPremiumGate({ 
  tier, 
  message, 
  features,
  onUpgrade, 
  onClose 
}: OverlayGateProps) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="max-w-lg w-full mx-4">
        <PremiumGate
          tier={tier}
          message={message}
          features={features}
          onUpgrade={onUpgrade}
          onClose={onClose}
        />
      </div>
    </div>
  );
}

// ============================================================================
// COMPACT PREMIUM GATE (for small widgets)
// ============================================================================

interface CompactGateProps {
  tier: 'premium' | 'pro';
  message: string;
  onUpgrade?: () => void;
}

/**
 * Smaller premium gate for widget-sized components
 */
export function CompactPremiumGate({ tier, message, onUpgrade }: CompactGateProps) {
  const Icon = tier === 'pro' ? Crown : Lock;
  const iconColor = tier === 'pro' ? 'text-purple-400' : 'text-sovereign-gold';
  const buttonColor = tier === 'pro' 
    ? 'text-purple-400 hover:text-purple-300' 
    : 'text-sovereign-gold hover:text-sovereign-gold-hover';

  return (
    <div className="flex items-center justify-between p-4 bg-sovereign-obsidian/50 rounded-lg border border-sovereign-slate-700">
      <div className="flex items-center gap-3">
        <Icon className={`w-5 h-5 ${iconColor}`} />
        <span className="text-sm text-sovereign-slate-300">{message}</span>
      </div>
      {onUpgrade && (
        <button
          onClick={onUpgrade}
          className={`text-xs font-medium ${buttonColor}`}
        >
          Upgrade
        </button>
      )}
    </div>
  );
}

// ============================================================================
// USAGE EXAMPLES
// ============================================================================

/**
 * Example: Feature locked behind Premium
 * 
 * function CSVExportButton({ userTier }: { userTier: string }) {
 *   const [showGate, setShowGate] = useState(false);
 *   
 *   const handleExport = () => {
 *     if (userTier === 'free') {
 *       setShowGate(true);
 *     } else {
 *       exportToCSV();
 *     }
 *   };
 *   
 *   return (
 *     <>
 *       <button onClick={handleExport}>
 *         Export CSV <PremiumBadge tier="premium" />
 *       </button>
 *       
 *       {showGate && (
 *         <OverlayPremiumGate
 *           tier="premium"
 *           message="Upgrade to Premium to export portfolios as CSV."
 *           features={['Export to Excel', 'Scheduled exports', 'Historical snapshots']}
 *           onUpgrade={() => router.push('/pricing')}
 *           onClose={() => setShowGate(false)}
 *         />
 *       )}
 *     </>
 *   );
 * }
 */

/**
 * Example: Inline premium badge
 * 
 * function FeatureList() {
 *   return (
 *     <ul>
 *       <li>Basic charts</li>
 *       <li>Advanced indicators <PremiumBadge tier="premium" /></li>
 *       <li>API access <PremiumBadge tier="pro" /></li>
 *     </ul>
 *   );
 * }
 */

/**
 * Example: Compact gate in small widget
 * 
 * function AnalyticsWidget({ userTier }: { userTier: string }) {
 *   if (userTier === 'free') {
 *     return (
 *       <CompactPremiumGate
 *         tier="premium"
 *         message="Upgrade to unlock analytics"
 *         onUpgrade={() => router.push('/pricing')}
 *       />
 *     );
 *   }
 *   
 *   return <AnalyticsDashboard />;
 * }
 */
