'use client'

interface StatusBadgeProps {
  status: 'active' | 'inactive' | 'pending' | 'success' | 'error' | 'warning' | 'info'
  label?: string
  size?: 'sm' | 'md' | 'lg'
  dot?: boolean
  pulse?: boolean
  className?: string
}

export default function StatusBadge({
  status,
  label,
  size = 'md',
  dot = false,
  pulse = false,
  className = '',
}: StatusBadgeProps) {
  const getStatusConfig = () => {
    switch (status) {
      case 'active':
      case 'success':
        return {
          color: 'bg-green-500/20 text-green-400 border-green-500/30',
          dotColor: 'bg-green-500',
          icon: '✓',
        }
      case 'inactive':
        return {
          color: 'bg-gray-500/20 text-gray-400 border-gray-500/30',
          dotColor: 'bg-gray-500',
          icon: '○',
        }
      case 'pending':
        return {
          color: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
          dotColor: 'bg-yellow-500',
          icon: '⏳',
        }
      case 'error':
        return {
          color: 'bg-red-500/20 text-red-400 border-red-500/30',
          dotColor: 'bg-red-500',
          icon: '✕',
        }
      case 'warning':
        return {
          color: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
          dotColor: 'bg-orange-500',
          icon: '⚠',
        }
      case 'info':
        return {
          color: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
          dotColor: 'bg-blue-500',
          icon: 'ℹ',
        }
      default:
        return {
          color: 'bg-gray-500/20 text-gray-400 border-gray-500/30',
          dotColor: 'bg-gray-500',
          icon: '○',
        }
    }
  }

  const getSizeClasses = () => {
    switch (size) {
      case 'sm':
        return {
          badge: 'px-2 py-0.5 text-xs',
          dot: 'w-1.5 h-1.5',
        }
      case 'md':
        return {
          badge: 'px-2.5 py-1 text-sm',
          dot: 'w-2 h-2',
        }
      case 'lg':
        return {
          badge: 'px-3 py-1.5 text-base',
          dot: 'w-2.5 h-2.5',
        }
    }
  }

  const config = getStatusConfig()
  const sizeClasses = getSizeClasses()
  const displayLabel = label || status.charAt(0).toUpperCase() + status.slice(1)

  if (dot) {
    return (
      <div className={`flex items-center space-x-2 ${className}`}>
        <div
          className={`
            ${sizeClasses.dot} rounded-full ${config.dotColor}
            ${pulse ? 'animate-pulse' : ''}
          `}
        />
        {label && (
          <span className={`${size === 'sm' ? 'text-xs' : size === 'lg' ? 'text-base' : 'text-sm'}`}>
            {displayLabel}
          </span>
        )}
      </div>
    )
  }

  return (
    <span
      className={`
        inline-flex items-center space-x-1
        ${sizeClasses.badge}
        ${config.color}
        border rounded-full font-semibold
        ${className}
      `}
    >
      <span>{config.icon}</span>
      <span>{displayLabel}</span>
    </span>
  )
}

// Status indicator for system health
export function HealthIndicator({
  health,
  size = 'md',
  showLabel = true,
}: {
  health: 'excellent' | 'good' | 'fair' | 'poor' | 'critical'
  size?: 'sm' | 'md' | 'lg'
  showLabel?: boolean
}) {
  const getHealthConfig = () => {
    switch (health) {
      case 'excellent':
        return { emoji: '✅', label: 'EXCELLENT', color: 'text-green-500' }
      case 'good':
        return { emoji: '🟢', label: 'GOOD', color: 'text-green-400' }
      case 'fair':
        return { emoji: '🟡', label: 'FAIR', color: 'text-yellow-400' }
      case 'poor':
        return { emoji: '🟠', label: 'POOR', color: 'text-orange-400' }
      case 'critical':
        return { emoji: '🔴', label: 'CRITICAL', color: 'text-red-500' }
      default:
        return { emoji: '❓', label: 'UNKNOWN', color: 'text-gray-400' }
    }
  }

  const config = getHealthConfig()
  const emojiSize = size === 'sm' ? 'text-lg' : size === 'lg' ? 'text-4xl' : 'text-2xl'
  const labelSize = size === 'sm' ? 'text-xs' : size === 'lg' ? 'text-xl' : 'text-base'

  return (
    <div className="flex items-center space-x-2">
      <span className={emojiSize}>{config.emoji}</span>
      {showLabel && (
        <span className={`${labelSize} font-semibold ${config.color}`}>
          {config.label}
        </span>
      )}
    </div>
  )
}

// Status list for multiple items
export function StatusList({
  items,
}: {
  items: Array<{
    label: string
    status: 'active' | 'inactive' | 'pending' | 'success' | 'error' | 'warning' | 'info'
    detail?: string
  }>
}) {
  return (
    <div className="space-y-2">
      {items.map((item, idx) => (
        <div key={idx} className="flex items-center justify-between codex-panel">
          <div className="flex-1">
            <div className="font-semibold text-sm">{item.label}</div>
            {item.detail && (
              <div className="text-xs text-codex-parchment/60">{item.detail}</div>
            )}
          </div>
          <StatusBadge status={item.status} size="sm" />
        </div>
      ))}
    </div>
  )
}
