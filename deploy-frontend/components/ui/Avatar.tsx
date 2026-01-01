/**
 * Avatar Component - Sovereign-styled agent avatars
 */

import { getAvatarColor, type AvatarDomain } from "@/lib/design-system";
import { Icon, IconName } from "./Icon";

interface AvatarProps {
  domain: AvatarDomain | string;
  icon?: IconName;
  size?: "sm" | "md" | "lg" | "xl";
  className?: string;
}

const sizeMap = {
  sm: { wrapper: "w-8 h-8", icon: 16 },
  md: { wrapper: "w-12 h-12", icon: 20 },
  lg: { wrapper: "w-16 h-16", icon: 28 },
  xl: { wrapper: "w-24 h-24", icon: 40 },
};

export function Avatar({ domain, icon = "brain", size = "md", className = "" }: AvatarProps) {
  const color = getAvatarColor(domain);
  const { wrapper, icon: iconSize } = sizeMap[size];

  return (
    <div
      className={`${wrapper} rounded-full flex items-center justify-center ${className}`}
      style={{
        background: `linear-gradient(135deg, ${color}dd, ${color}88)`,
      }}
    >
      <Icon name={icon} size={iconSize} color="white" strokeWidth={2} />
    </div>
  );
}
