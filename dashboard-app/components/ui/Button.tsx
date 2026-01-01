/**
 * Button Component - Sovereign-styled actions
 */

import { ReactNode } from "react";
import { styles } from "@/lib/design-system";
import { Icon, IconName } from "./Icon";

type ButtonVariant = "primary" | "secondary" | "danger" | "ghost";

interface ButtonProps {
  children: ReactNode;
  variant?: ButtonVariant;
  icon?: IconName;
  className?: string;
  onClick?: () => void;
  disabled?: boolean;
  type?: "button" | "submit" | "reset";
}

export function Button({
  children,
  variant = "primary",
  icon,
  className = "",
  onClick,
  disabled = false,
  type = "button",
}: ButtonProps) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${styles.button[variant]} ${className} flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed`}
    >
      {icon && <Icon name={icon} size={18} />}
      {children}
    </button>
  );
}
