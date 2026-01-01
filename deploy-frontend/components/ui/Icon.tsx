/**
 * Icon Component - Unified icon system using Lucide React
 * Install: npm install lucide-react
 */

import {
  Crown,
  Shield,
  Zap,
  Layers,
  Brain,
  Users,
  BarChart3,
  ClipboardCheck,
  Workflow,
  Coins,
  Check,
  X,
  Star,
  Flame,
  ChevronRight,
  Home,
  Settings,
  Menu,
  Search,
  Plus,
  Minus,
  Edit,
  Trash2,
  Download,
  Upload,
  Eye,
  EyeOff,
  AlertCircle,
  Info,
  CheckCircle,
  XCircle,
  Clock,
  ArrowRight,
  Activity,
  Bug,
  List,
  RefreshCw,
  LucideIcon,
} from "lucide-react";

export const icons = {
  crown: Crown,
  shield: Shield,
  spark: Zap,
  zap: Zap,
  layers: Layers,
  brain: Brain,
  users: Users,
  chart: BarChart3,
  clipboard: ClipboardCheck,
  workflow: Workflow,
  coins: Coins,
  check: Check,
  cross: X,
  star: Star,
  fire: Flame,
  chevronRight: ChevronRight,
  home: Home,
  settings: Settings,
  menu: Menu,
  search: Search,
  plus: Plus,
  minus: Minus,
  edit: Edit,
  trash: Trash2,
  download: Download,
  upload: Upload,
  eye: Eye,
  eyeOff: EyeOff,
  alert: AlertCircle,
  info: Info,
  checkCircle: CheckCircle,
  xCircle: XCircle,
  clock: Clock,
  arrowRight: ArrowRight,
  activity: Activity,
  bug: Bug,
  list: List,
  refresh: RefreshCw,
} as const;

export type IconName = keyof typeof icons;

interface IconProps {
  name: IconName;
  className?: string;
  size?: number;
  strokeWidth?: number;
  color?: string;
}

export function Icon({
  name,
  className = "",
  size = 20,
  strokeWidth = 1.5,
  color,
}: IconProps) {
  const IconComponent = icons[name] as LucideIcon;
  
  return (
    <IconComponent
      className={className}
      size={size}
      strokeWidth={strokeWidth}
      color={color}
    />
  );
}
