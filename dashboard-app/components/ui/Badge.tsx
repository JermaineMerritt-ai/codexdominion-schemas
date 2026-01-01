/**
 * Badge Component - Status and category indicators
 */

import { styles } from "@/lib/design-system";

type BadgeVariant = "gold" | "emerald" | "crimson" | "blue" | "violet" | "slate";

interface BadgeProps {
  children: React.ReactNode;
  variant?: BadgeVariant;
  className?: string;
}

export function Badge({ children, variant = "blue", className = "" }: BadgeProps) {
  const variantClass = variant === "slate" 
    ? "px-2 py-1 rounded-full text-xs font-semibold bg-slate-600 text-white"
    : styles.badge[variant as keyof typeof styles.badge];
  return <span className={`${variantClass} ${className}`}>{children}</span>;
}
