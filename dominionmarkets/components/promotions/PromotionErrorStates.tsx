/**
 * Cross-Promotion Engine - Error States
 * Error and empty state components for promotion loading failures
 */

import React from 'react';
import { 
  AlertCircle, XCircle, Wifi, RefreshCw, X,
  ShoppingBag
} from 'lucide-react';

// ============================================================================
// PROMOTION LOAD ERROR
// ============================================================================

interface PromotionLoadErrorProps {
  onRetry?: () => void;
  onDismiss?: () => void;
}

export const PromotionLoadError: React.FC<PromotionLoadErrorProps> = ({ 
  onRetry, 
  onDismiss 
}) => {
  return (
    <div className="border border-red-200 rounded-lg p-4 bg-red-50">
      <div className="flex items-start gap-3">
        <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
        <div className="flex-1 min-w-0">
          <h3 className="text-sm font-semibold text-red-900 mb-1">
            Unable to Load Recommendations
          </h3>
          <p className="text-xs text-red-700 mb-3">
            We couldn't load personalized recommendations. Check your connection and try again.
          </p>
          
          <div className="flex items-center gap-2">
            {onRetry && (
              <button
                onClick={onRetry}
                className="text-xs font-medium text-red-700 hover:text-red-800 underline flex items-center gap-1"
              >
                <RefreshCw className="w-3 h-3" />
                Retry
              </button>
            )}
            {onDismiss && (
              <button
                onClick={onDismiss}
                className="text-xs font-medium text-red-600 hover:text-red-700 underline"
              >
                Dismiss
              </button>
            )}
          </div>
        </div>
        
        {onDismiss && (
          <button
            onClick={onDismiss}
            className="text-red-400 hover:text-red-600 flex-shrink-0"
            aria-label="Close"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>
    </div>
  );
};

// ============================================================================
// NETWORK TIMEOUT ERROR
// ============================================================================

interface NetworkTimeoutErrorProps {
  onRetry?: () => void;
}

export const NetworkTimeoutError: React.FC<NetworkTimeoutErrorProps> = ({ onRetry }) => {
  return (
    <div className="border border-orange-200 rounded-lg p-3 bg-orange-50">
      <div className="flex items-center gap-3">
        <Wifi className="w-5 h-5 text-orange-600 flex-shrink-0" />
        <div className="flex-1">
          <p className="text-xs text-orange-700">
            Connection timeout. Please check your network.
          </p>
        </div>
        {onRetry && (
          <button
            onClick={onRetry}
            className="text-xs font-medium text-orange-700 hover:text-orange-800 underline whitespace-nowrap"
          >
            Try Again
          </button>
        )}
      </div>
    </div>
  );
};

// ============================================================================
// NO PROMOTIONS AVAILABLE
// ============================================================================

export const NoPromotionsAvailable: React.FC = () => {
  // This component renders nothing (silent empty state)
  // Used when user has dismissed all promotions or preferences disable them
  return null;
};

// ============================================================================
// PROMOTIONS DISABLED STATE
// ============================================================================

interface PromotionsDisabledProps {
  onEnable?: () => void;
}

export const PromotionsDisabled: React.FC<PromotionsDisabledProps> = ({ onEnable }) => {
  return (
    <div className="border border-slate-200 rounded-lg p-4 bg-slate-50">
      <div className="flex items-start gap-3">
        <ShoppingBag className="w-5 h-5 text-slate-400 flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <h3 className="text-sm font-medium text-slate-700 mb-1">
            Ecosystem Recommendations Disabled
          </h3>
          <p className="text-xs text-slate-600 mb-2">
            You've turned off product recommendations. You can re-enable them in Settings.
          </p>
          {onEnable && (
            <button
              onClick={onEnable}
              className="text-xs font-medium text-slate-700 hover:text-slate-900 underline"
            >
              Enable Recommendations
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

// ============================================================================
// IMPRESSION LIMIT REACHED
// ============================================================================

export const ImpressionLimitReached: React.FC = () => {
  return (
    <div className="border border-blue-200 rounded-lg p-3 bg-blue-50">
      <div className="flex items-center gap-3">
        <AlertCircle className="w-5 h-5 text-blue-600 flex-shrink-0" />
        <div className="flex-1">
          <p className="text-xs text-blue-700">
            You've seen all available recommendations for now. Check back tomorrow for new suggestions!
          </p>
        </div>
      </div>
    </div>
  );
};

// ============================================================================
// GENERIC ERROR FALLBACK
// ============================================================================

interface GenericErrorProps {
  message?: string;
  onDismiss?: () => void;
}

export const GenericPromotionError: React.FC<GenericErrorProps> = ({ 
  message = 'Something went wrong loading recommendations.',
  onDismiss 
}) => {
  return (
    <div className="border border-slate-200 rounded-lg p-3 bg-slate-50">
      <div className="flex items-start gap-3">
        <XCircle className="w-5 h-5 text-slate-400 flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <p className="text-xs text-slate-600">
            {message}
          </p>
        </div>
        {onDismiss && (
          <button
            onClick={onDismiss}
            className="text-slate-400 hover:text-slate-600 flex-shrink-0"
            aria-label="Close"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>
    </div>
  );
};

// ============================================================================
// LOADING SKELETON
// ============================================================================

interface PromotionLoadingSkeletonProps {
  count?: number;
}

export const PromotionLoadingSkeleton: React.FC<PromotionLoadingSkeletonProps> = ({ 
  count = 2 
}) => {
  return (
    <div className="space-y-4">
      {[...Array(count)].map((_, i) => (
        <div 
          key={i} 
          className="border border-slate-200 rounded-lg p-4 bg-white animate-pulse"
        >
          {/* Header */}
          <div className="flex items-center justify-between mb-3">
            <div className="h-5 bg-slate-200 rounded-full w-24"></div>
            <div className="h-4 w-4 bg-slate-200 rounded"></div>
          </div>

          {/* Icon & Title */}
          <div className="flex items-start gap-3 mb-3">
            <div className="h-9 w-9 bg-slate-200 rounded-lg flex-shrink-0"></div>
            <div className="flex-1 space-y-2">
              <div className="h-4 bg-slate-200 rounded w-3/4"></div>
              <div className="h-3 bg-slate-200 rounded w-full"></div>
              <div className="h-3 bg-slate-200 rounded w-5/6"></div>
            </div>
          </div>

          {/* Footer */}
          <div className="flex items-center justify-between mt-4 pt-3 border-t border-slate-100">
            <div className="h-6 bg-slate-200 rounded w-16"></div>
            <div className="h-4 bg-slate-200 rounded w-20"></div>
          </div>
        </div>
      ))}
    </div>
  );
};

// ============================================================================
// ALL PROMOTIONS DISMISSED
// ============================================================================

interface AllDismissedProps {
  onViewDismissed?: () => void;
}

export const AllPromotionsDismissed: React.FC<AllDismissedProps> = ({ onViewDismissed }) => {
  return (
    <div className="border border-slate-200 rounded-lg p-4 bg-slate-50 text-center">
      <ShoppingBag className="w-8 h-8 text-slate-300 mx-auto mb-2" />
      <h3 className="text-sm font-medium text-slate-700 mb-1">
        No Recommendations Right Now
      </h3>
      <p className="text-xs text-slate-600 mb-3">
        You've dismissed all current suggestions. They'll return in a few days, or you can restore them now.
      </p>
      {onViewDismissed && (
        <button
          onClick={onViewDismissed}
          className="text-xs font-medium text-slate-700 hover:text-slate-900 underline"
        >
          View Dismissed Products
        </button>
      )}
    </div>
  );
};

// ============================================================================
// DISMISSED PRODUCTS LIST (FOR SETTINGS)
// ============================================================================

interface DismissedProduct {
  promotion_id: string;
  promotion_name: string;
  dismissed_at: string;
  hide_until: string;
  reason: string | null;
}

interface DismissedListProps {
  dismissed: DismissedProduct[];
  onRestore: (promotionId: string) => void;
  loading?: boolean;
}

export const DismissedProductsList: React.FC<DismissedListProps> = ({ 
  dismissed, 
  onRestore,
  loading 
}) => {
  if (loading) {
    return (
      <div className="space-y-2">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="border border-slate-200 rounded p-3 animate-pulse">
            <div className="h-4 bg-slate-200 rounded w-2/3 mb-2"></div>
            <div className="h-3 bg-slate-200 rounded w-1/2"></div>
          </div>
        ))}
      </div>
    );
  }

  if (dismissed.length === 0) {
    return (
      <div className="text-center py-6">
        <p className="text-sm text-slate-600">
          You haven't dismissed any products yet.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {dismissed.map(item => {
        const hideUntilDate = new Date(item.hide_until);
        const daysRemaining = Math.ceil((hideUntilDate.getTime() - Date.now()) / (1000 * 60 * 60 * 24));

        return (
          <div 
            key={item.promotion_id} 
            className="border border-slate-200 rounded-lg p-3 bg-white hover:bg-slate-50 transition-colors"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex-1 min-w-0">
                <h4 className="text-sm font-medium text-slate-900 mb-1">
                  {item.promotion_name}
                </h4>
                <p className="text-xs text-slate-600">
                  Hidden for {daysRemaining} more {daysRemaining === 1 ? 'day' : 'days'}
                  {item.reason && ` • ${item.reason.replace('_', ' ')}`}
                </p>
              </div>
              <button
                onClick={() => onRestore(item.promotion_id)}
                className="text-xs font-medium text-blue-600 hover:text-blue-700 underline whitespace-nowrap"
              >
                Restore
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default {
  PromotionLoadError,
  NetworkTimeoutError,
  NoPromotionsAvailable,
  PromotionsDisabled,
  ImpressionLimitReached,
  GenericPromotionError,
  PromotionLoadingSkeleton,
  AllPromotionsDismissed,
  DismissedProductsList
};
