/**
 * StatusBadge - Smart status indicator with color coding
 */

import { getStatusColor } from "@/lib/design-system";

interface StatusBadgeProps {
  status: string;
  className?: string;
}

export function StatusBadge({ status, className = "" }: StatusBadgeProps) {
  const color = getStatusColor(status);
  const displayText = status.replace(/_/g, " ").toUpperCase();

  return (
    <span
      className={`px-2 py-1 rounded-full text-xs font-semibold ${className}`}
      style={{
        backgroundColor: `${color}22`,
        color: color,
        border: `1px solid ${color}44`,
      }}
    >
      {displayText}
    </span>
  );
}
