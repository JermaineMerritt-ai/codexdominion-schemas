/**
 * CodexDominion Sovereign Design System
 * Unified colors, styles, and component utilities
 */

// ═══════════════════════════════════════════════════════════════════════════
// COLOR PALETTE
// ═══════════════════════════════════════════════════════════════════════════

export const colors = {
  // Primary Colors
  imperialGold: "#F5C542",
  dominionBlue: "#3B82F6",
  councilEmerald: "#10B981",
  
  // Secondary Colors
  obsidianBlack: "#0F172A",
  slateSteel: "#1E293B",
  violetPulse: "#7C3AED",
  crimsonReview: "#DC2626",
  
  // Backgrounds
  bg: {
    primary: "#0F172A",
    secondary: "#1E293B",
    elevated: "#020617",
  },
  
  // Borders
  border: {
    primary: "#1E293B",
    secondary: "#334155",
  },
} as const;

// ═══════════════════════════════════════════════════════════════════════════
// COMPONENT STYLES
// ═══════════════════════════════════════════════════════════════════════════

export const styles = {
  // Cards
  card: "rounded-lg border border-sovereign-slate bg-sovereign-obsidian shadow-sm hover:shadow-md transition-shadow",
  cardHeader: "px-4 py-3 border-b border-sovereign-slate",
  cardBody: "p-4",
  
  // Buttons
  button: {
    primary: "px-4 py-2 rounded-md bg-sovereign-gold text-sovereign-obsidian font-semibold hover:bg-yellow-400 transition-colors",
    secondary: "px-4 py-2 rounded-md bg-sovereign-slate text-white font-semibold hover:bg-slate-600 transition-colors",
    danger: "px-4 py-2 rounded-md bg-sovereign-crimson text-white font-semibold hover:bg-red-700 transition-colors",
    ghost: "px-4 py-2 rounded-md hover:bg-sovereign-slate transition-colors",
  },
  
  // Badges
  badge: {
    gold: "px-2 py-1 rounded-full text-xs font-semibold bg-sovereign-gold text-sovereign-obsidian",
    emerald: "px-2 py-1 rounded-full text-xs font-semibold bg-sovereign-emerald text-white",
    crimson: "px-2 py-1 rounded-full text-xs font-semibold bg-sovereign-crimson text-white",
    blue: "px-2 py-1 rounded-full text-xs font-semibold bg-sovereign-blue text-white",
    violet: "px-2 py-1 rounded-full text-xs font-semibold bg-sovereign-violet text-white",
  },
  
  // Tables
  table: {
    wrapper: "rounded-lg border border-sovereign-slate overflow-hidden",
    header: "bg-[#020617] text-sm font-semibold",
    row: "border-b border-sovereign-slate hover:bg-sovereign-slate transition-colors",
    cell: "px-4 py-3",
  },
  
  // Text
  text: {
    heading: "text-2xl font-bold text-white",
    subheading: "text-lg font-semibold text-white",
    body: "text-sm text-slate-300",
    muted: "text-xs text-slate-400",
    accent: "text-sovereign-gold",
  },
} as const;

// ═══════════════════════════════════════════════════════════════════════════
// AVATAR COLORS BY DOMAIN
// ═══════════════════════════════════════════════════════════════════════════

export const avatarColors = {
  commerce: "#F5C542", // Gold
  governance: "#10B981", // Emerald
  media: "#7C3AED", // Violet
  youth: "#3B82F6", // Blue
  research: "#64748B", // Slate
  creator: "#EC4899", // Pink
  default: "#6B7280", // Gray
} as const;

export type AvatarDomain = keyof typeof avatarColors;

// ═══════════════════════════════════════════════════════════════════════════
// ICON DEFINITIONS
// ═══════════════════════════════════════════════════════════════════════════

export const iconMap = {
  crown: "👑",
  shield: "🛡️",
  spark: "⚡",
  layers: "📚",
  brain: "🧠",
  users: "👥",
  chart: "📊",
  clipboard: "📋",
  workflow: "🔄",
  coins: "💰",
  check: "✓",
  cross: "✗",
  star: "★",
  fire: "🔥",
} as const;

// ═══════════════════════════════════════════════════════════════════════════
// UTILITY FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════

export function getAvatarColor(domain: string | AvatarDomain): string {
  const normalized = domain.toLowerCase() as AvatarDomain;
  return avatarColors[normalized] || avatarColors.default;
}

export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

export function formatPercentage(value: number): string {
  return `${(value * 100).toFixed(0)}%`;
}

export function getStatusColor(status: string): string {
  const statusMap: Record<string, string> = {
    completed: colors.councilEmerald,
    approved: colors.councilEmerald,
    success: colors.councilEmerald,
    pending: colors.dominionBlue,
    in_progress: colors.dominionBlue,
    processing: colors.dominionBlue,
    failed: colors.crimsonReview,
    rejected: colors.crimsonReview,
    denied: colors.crimsonReview,
    error: colors.crimsonReview,
  };
  return statusMap[status.toLowerCase()] || colors.slateSteel;
}

// ═══════════════════════════════════════════════════════════════════════════
// COUNCIL THEMING
// ═══════════════════════════════════════════════════════════════════════════

export const councilTheme: Record<
  string,
  { icon: string; color: string }
> = {
  council_governance: { icon: "shield-check", color: "#10B981" },
  council_policy: { icon: "scale", color: "#10B981" },
  council_compliance: { icon: "badge-check", color: "#14B8A6" },
  council_identity_safety: { icon: "lock-closed", color: "#0EA5E9" },

  council_commerce: { icon: "banknotes", color: "#F59E0B" },
  council_marketplace: { icon: "shopping-bag", color: "#F97316" },
  council_pricing: { icon: "currency-dollar", color: "#FACC15" },
  council_finance_risk: { icon: "shield-exclamation", color: "#F97316" },

  council_media: { icon: "play-circle", color: "#6366F1" },
  council_content_integrity: { icon: "document-check", color: "#4F46E5" },
  council_creator: { icon: "sparkles", color: "#EC4899" },
  council_distribution: { icon: "paper-airplane", color: "#22C55E" },

  council_youth: { icon: "user-group", color: "#38BDF8" },
  council_education: { icon: "academic-cap", color: "#22C55E" },
  council_training_skills: { icon: "light-bulb", color: "#EAB308" },
  council_mentorship: { icon: "hand-raised", color: "#F97316" },

  council_research: { icon: "beaker", color: "#0EA5E9" },
  council_data: { icon: "database", color: "#22C55E" },
  council_analytics: { icon: "chart-bar", color: "#F97316" },
  council_ai_ethics: { icon: "scale", color: "#EC4899" },

  council_security: { icon: "shield-exclamation", color: "#EF4444" },
  council_threat_response: { icon: "fire", color: "#F97316" },
  council_infrastructure: { icon: "server-stack", color: "#6366F1" },
  council_privacy: { icon: "eye-slash", color: "#0EA5E9" },

  council_community: { icon: "chat-bubble-left-right", color: "#22C55E" },
  council_support: { icon: "lifebuoy", color: "#0EA5E9" },
  council_engagement: { icon: "bolt", color: "#F59E0B" },
  council_reputation: { icon: "trophy", color: "#FACC15" },

  council_operations: { icon: "cog-6-tooth", color: "#22C55E" },
  council_workflow: { icon: "arrow-path", color: "#6366F1" },
  council_automation: { icon: "cpu-chip", color: "#F97316" },
  council_quality_assurance: { icon: "check-badge", color: "#22C55E" },

  council_culture: { icon: "sparkles", color: "#A855F7" },
  council_experience: { icon: "cursor-arrow-rays", color: "#22C55E" },
  council_accessibility: { icon: "eye", color: "#0EA5E9" },
  council_inclusivity: { icon: "users", color: "#EC4899" }
};

/**
 * Get themed icon and color for a council
 */
export function getCouncilTheme(councilId: string): { icon: string; color: string } {
  return councilTheme[councilId] || { icon: "shield", color: colors.slateSteel };
}
