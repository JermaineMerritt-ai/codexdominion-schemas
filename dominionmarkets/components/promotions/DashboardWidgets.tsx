/**
 * Cross-Promotion Engine - React Components
 * Dashboard widgets and contextual links for ecosystem products
 */

import React, { useEffect, useState } from 'react';
import { 
  ExternalLink, X, ShoppingBag, Wrench, GraduationCap, 
  Globe, TrendingUp, FileText, DollarSign, Sparkles,
  ChevronRight
} from 'lucide-react';

// ============================================================================
// TYPES
// ============================================================================

interface Promotion {
  id: string;
  product_id: string;
  name: string;
  description: string;
  long_description?: string;
  price: number | null;
  currency: string;
  original_price?: number | null;
  category: 'template' | 'tool' | 'service' | 'education';
  identity_fit: 'diaspora' | 'youth' | 'creator' | 'legacy' | 'all';
  icon: string;
  image_url?: string;
  cta_text: string;
  cta_link: string;
  widget_type: 'product_card' | 'free_tool' | 'service_promotion' | 'inline_link';
}

interface PromotionWidgetProps {
  location: 'dashboard' | 'portfolio' | 'markets' | 'news' | 'alerts';
  userIdentity: 'diaspora' | 'youth' | 'creator' | 'legacy';
  userTier: 'free' | 'premium' | 'pro';
  context?: Record<string, any>;
  maxWidgets?: number;
}

// ============================================================================
// ICON MAPPING
// ============================================================================

const getIconComponent = (iconName: string) => {
  const icons: Record<string, React.FC<{ className?: string }>> = {
    'globe': Globe,
    'trending-up': TrendingUp,
    'file-text': FileText,
    'dollar-sign': DollarSign,
    'graduation-cap': GraduationCap,
    'wrench': Wrench,
    'shopping-bag': ShoppingBag,
    'sparkles': Sparkles,
  };
  return icons[iconName] || FileText;
};

// ============================================================================
// IDENTITY THEME COLORS
// ============================================================================

const getIdentityTheme = (identity: string) => {
  const themes: Record<string, { border: string; bg: string; text: string; badge: string }> = {
    diaspora: {
      border: 'border-emerald-600',
      bg: 'bg-emerald-50',
      text: 'text-emerald-700',
      badge: 'bg-emerald-100 text-emerald-800'
    },
    youth: {
      border: 'border-blue-600',
      bg: 'bg-blue-50',
      text: 'text-blue-700',
      badge: 'bg-blue-100 text-blue-800'
    },
    creator: {
      border: 'border-purple-600',
      bg: 'bg-purple-50',
      text: 'text-purple-700',
      badge: 'bg-purple-100 text-purple-800'
    },
    legacy: {
      border: 'border-amber-600',
      bg: 'bg-amber-50',
      text: 'text-amber-700',
      badge: 'bg-amber-100 text-amber-800'
    },
    all: {
      border: 'border-gray-600',
      bg: 'bg-gray-50',
      text: 'text-gray-700',
      badge: 'bg-gray-100 text-gray-800'
    }
  };
  return themes[identity] || themes.all;
};

const getIdentityLabel = (identity: string) => {
  const labels: Record<string, string> = {
    diaspora: 'For Diaspora Investors',
    youth: 'For Beginners',
    creator: 'For Creators & Entrepreneurs',
    legacy: 'For Legacy-Builders',
    all: 'For All Investors'
  };
  return labels[identity] || '';
};

// ============================================================================
// MAIN WIDGET CONTAINER
// ============================================================================

export const DashboardWidgets: React.FC<PromotionWidgetProps> = ({
  location,
  userIdentity,
  userTier,
  context = {},
  maxWidgets = 2
}) => {
  const [promotions, setPromotions] = useState<Promotion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadPromotions();
  }, [location, userIdentity, userTier]);

  const loadPromotions = async () => {
    try {
      setLoading(true);
      setError(null);

      const contextParam = encodeURIComponent(JSON.stringify(context));
      const response = await fetch(
        `/api/promotions?location=${location}&identity=${userIdentity}&tier=${userTier}&context=${contextParam}`
      );

      if (!response.ok) {
        throw new Error('Failed to load promotions');
      }

      const data = await response.json();
      setPromotions(data.promotions.slice(0, maxWidgets));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      console.error('Error loading promotions:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleImpression = async (promotionId: string) => {
    try {
      await fetch('/api/promotions/impression', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          promotion_id: promotionId,
          location,
          identity: userIdentity,
          tier: userTier,
          context
        })
      });
    } catch (err) {
      console.error('Error tracking impression:', err);
    }
  };

  const handleClick = async (promotionId: string, action: string) => {
    try {
      await fetch('/api/promotions/click', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          promotion_id: promotionId,
          location,
          identity: userIdentity,
          tier: userTier,
          action
        })
      });
    } catch (err) {
      console.error('Error tracking click:', err);
    }
  };

  const handleDismiss = async (promotionId: string, reason: string = 'other') => {
    try {
      await fetch('/api/promotions/dismiss', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          promotion_id: promotionId,
          location,
          identity: userIdentity,
          tier: userTier,
          reason,
          hide_duration_days: 7
        })
      });

      // Remove from UI
      setPromotions(prev => prev.filter(p => p.id !== promotionId));
    } catch (err) {
      console.error('Error dismissing promotion:', err);
    }
  };

  useEffect(() => {
    // Track impressions when promotions load
    promotions.forEach(promo => {
      handleImpression(promo.id);
    });
  }, [promotions]);

  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(maxWidgets)].map((_, i) => (
          <div key={i} className="border border-slate-200 rounded-lg p-4 animate-pulse">
            <div className="h-4 bg-slate-200 rounded w-1/2 mb-2"></div>
            <div className="h-3 bg-slate-200 rounded w-full mb-2"></div>
            <div className="h-3 bg-slate-200 rounded w-3/4"></div>
          </div>
        ))}
      </div>
    );
  }

  if (error) {
    return null; // Fail silently
  }

  if (promotions.length === 0) {
    return null; // No promotions available
  }

  return (
    <div className="space-y-4">
      {promotions.map(promo => {
        switch (promo.widget_type) {
          case 'product_card':
            return (
              <ProductCard
                key={promo.id}
                promotion={promo}
                onDismiss={handleDismiss}
                onClick={handleClick}
              />
            );
          case 'free_tool':
            return (
              <FreeToolCard
                key={promo.id}
                promotion={promo}
                onDismiss={handleDismiss}
                onClick={handleClick}
              />
            );
          case 'service_promotion':
            return (
              <ServicePromotionCard
                key={promo.id}
                promotion={promo}
                onDismiss={handleDismiss}
                onClick={handleClick}
              />
            );
          default:
            return null;
        }
      })}
    </div>
  );
};

// ============================================================================
// PRODUCT CARD (PAID PRODUCTS)
// ============================================================================

interface CardProps {
  promotion: Promotion;
  onDismiss: (id: string, reason: string) => void;
  onClick: (id: string, action: string) => void;
}

export const ProductCard: React.FC<CardProps> = ({ promotion, onDismiss, onClick }) => {
  const theme = getIdentityTheme(promotion.identity_fit);
  const Icon = getIconComponent(promotion.icon);

  const handleCtaClick = () => {
    onClick(promotion.id, 'learn_more');
    window.open(promotion.cta_link, '_blank');
  };

  return (
    <div className={`border ${theme.border} rounded-lg p-4 bg-white shadow-sm hover:shadow-md transition-shadow`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <span className={`text-xs px-2 py-1 rounded-full ${theme.badge} font-medium`}>
          {getIdentityLabel(promotion.identity_fit)}
        </span>
        <button
          onClick={() => onDismiss(promotion.id, 'not_interested')}
          className="text-slate-400 hover:text-slate-600 transition-colors"
          aria-label="Dismiss"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Icon & Title */}
      <div className="flex items-start gap-3 mb-3">
        <div className={`p-2 ${theme.bg} rounded-lg`}>
          <Icon className={`w-5 h-5 ${theme.text}`} />
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-slate-900 text-sm mb-1 line-clamp-1">
            {promotion.name}
          </h3>
          <p className="text-xs text-slate-600 line-clamp-2">
            {promotion.description}
          </p>
        </div>
      </div>

      {/* Price & CTA */}
      <div className="flex items-center justify-between mt-4 pt-3 border-t border-slate-100">
        {promotion.price ? (
          <div className="flex items-center gap-2">
            <span className="text-lg font-bold text-slate-900">
              ${promotion.price}
            </span>
            {promotion.original_price && (
              <span className="text-sm text-slate-400 line-through">
                ${promotion.original_price}
              </span>
            )}
          </div>
        ) : (
          <span className="text-sm font-medium text-emerald-600">Free</span>
        )}

        <button
          onClick={handleCtaClick}
          className={`flex items-center gap-1 text-sm font-medium ${theme.text} hover:underline`}
        >
          {promotion.cta_text}
          <ExternalLink className="w-3 h-3" />
        </button>
      </div>

      {/* Dismiss Link */}
      <button
        onClick={() => onDismiss(promotion.id, 'not_interested')}
        className="text-xs text-slate-400 hover:text-slate-600 mt-2 underline"
      >
        Not interested
      </button>
    </div>
  );
};

// ============================================================================
// FREE TOOL CARD
// ============================================================================

export const FreeToolCard: React.FC<CardProps> = ({ promotion, onDismiss, onClick }) => {
  const Icon = getIconComponent(promotion.icon);

  const handleCtaClick = () => {
    onClick(promotion.id, 'try_now');
    window.open(promotion.cta_link, '_blank');
  };

  return (
    <div className="border-2 border-emerald-500 rounded-lg p-4 bg-gradient-to-br from-emerald-50 to-white shadow-sm hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <span className="flex items-center gap-1 text-xs px-2 py-1 rounded-full bg-emerald-100 text-emerald-800 font-medium">
          <Sparkles className="w-3 h-3" />
          Free Tool
        </span>
        <button
          onClick={() => onDismiss(promotion.id, 'other')}
          className="text-slate-400 hover:text-slate-600 transition-colors"
          aria-label="Dismiss"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Icon & Title */}
      <div className="flex items-start gap-3 mb-3">
        <div className="p-2 bg-emerald-100 rounded-lg">
          <Icon className="w-5 h-5 text-emerald-700" />
        </div>
        <div className="flex-1">
          <h3 className="font-semibold text-slate-900 text-sm mb-1">
            {promotion.name}
          </h3>
          <p className="text-xs text-slate-600 line-clamp-2">
            {promotion.description}
          </p>
        </div>
      </div>

      {/* CTA Button */}
      <button
        onClick={handleCtaClick}
        className="w-full bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-medium py-2 px-4 rounded-lg transition-colors flex items-center justify-center gap-2 mt-3"
      >
        {promotion.cta_text}
        <ChevronRight className="w-4 h-4" />
      </button>
    </div>
  );
};

// ============================================================================
// SERVICE PROMOTION CARD
// ============================================================================

export const ServicePromotionCard: React.FC<CardProps> = ({ promotion, onDismiss, onClick }) => {
  const Icon = getIconComponent(promotion.icon);

  const handleCtaClick = () => {
    onClick(promotion.id, 'explore');
    window.open(promotion.cta_link, '_blank');
  };

  return (
    <div className="border border-slate-300 rounded-lg p-4 bg-gradient-to-br from-slate-50 to-white shadow-sm hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs px-2 py-1 rounded-full bg-amber-100 text-amber-800 font-medium">
          🔥 From CodexDominion
        </span>
        <button
          onClick={() => onDismiss(promotion.id, 'not_interested')}
          className="text-slate-400 hover:text-slate-600 transition-colors"
          aria-label="Dismiss"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Icon & Title */}
      <div className="flex items-start gap-3 mb-3">
        <div className="p-2 bg-amber-100 rounded-lg">
          <Icon className="w-5 h-5 text-amber-700" />
        </div>
        <div className="flex-1">
          <h3 className="font-semibold text-slate-900 text-sm mb-1">
            {promotion.name}
          </h3>
          <p className="text-xs text-slate-600 line-clamp-3">
            {promotion.description}
          </p>
        </div>
      </div>

      {/* CTA & Dismiss */}
      <div className="flex items-center justify-between mt-4 pt-3 border-t border-slate-100">
        <button
          onClick={handleCtaClick}
          className="text-sm font-medium text-amber-700 hover:text-amber-800 hover:underline flex items-center gap-1"
        >
          {promotion.cta_text}
          <ExternalLink className="w-3 h-3" />
        </button>

        <button
          onClick={() => onDismiss(promotion.id, 'not_interested')}
          className="text-xs text-slate-400 hover:text-slate-600 underline"
        >
          Not Interested
        </button>
      </div>
    </div>
  );
};

// ============================================================================
// INLINE PROMOTION (CONTEXTUAL LINK)
// ============================================================================

interface InlinePromotionProps {
  promotion: Promotion;
  onDismiss: (id: string) => void;
  onClick: (id: string, action: string) => void;
}

export const InlinePromotion: React.FC<InlinePromotionProps> = ({ promotion, onDismiss, onClick }) => {
  const theme = getIdentityTheme(promotion.identity_fit);

  const handleClick = () => {
    onClick(promotion.id, 'inline_click');
    window.open(promotion.cta_link, '_blank');
  };

  return (
    <div className={`border ${theme.border} rounded-lg p-3 bg-white shadow-sm my-4`}>
      <div className="flex items-center justify-between gap-3">
        <div className="flex-1">
          <p className="text-sm text-slate-700">
            <span className="font-medium">{promotion.name}</span>
            {' — '}
            {promotion.description}
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleClick}
            className={`text-sm font-medium ${theme.text} hover:underline whitespace-nowrap flex items-center gap-1`}
          >
            {promotion.cta_text}
            <ExternalLink className="w-3 h-3" />
          </button>
          <button
            onClick={() => onDismiss(promotion.id)}
            className="text-slate-400 hover:text-slate-600"
            aria-label="Dismiss"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default DashboardWidgets;
