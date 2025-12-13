'use client'

import { ReactNode } from 'react'

interface DashboardTileProps {
  title: string
  icon?: string
  children: ReactNode
  className?: string
  onClick?: () => void
  action?: {
    label: string
    onClick: () => void
  }
}

export default function DashboardTile({
  title,
  icon,
  children,
  className = '',
  onClick,
  action,
}: DashboardTileProps) {
  const TileWrapper = onClick ? 'button' : 'div'

  return (
    <TileWrapper
      className={`
        codex-card
        ${onClick ? 'cursor-pointer hover:scale-105 transition-transform' : ''}
        ${className}
      `}
      onClick={onClick}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          {icon && <span className="text-3xl">{icon}</span>}
          <h3 className="text-xl font-serif text-codex-gold">{title}</h3>
        </div>

        {action && (
          <button
            onClick={(e) => {
              e.stopPropagation()
              action.onClick()
            }}
            className="codex-button text-sm"
          >
            {action.label}
          </button>
        )}
      </div>

      {/* Content */}
      <div>{children}</div>
    </TileWrapper>
  )
}

// Convenience variants
export function StatTile({
  label,
  value,
  icon,
  trend,
  trendValue,
}: {
  label: string
  value: string | number
  icon?: string
  trend?: 'up' | 'down' | 'neutral'
  trendValue?: string
}) {
  const getTrendColor = () => {
    switch (trend) {
      case 'up': return 'text-green-400'
      case 'down': return 'text-red-400'
      case 'neutral': return 'text-gray-400'
      default: return 'text-codex-parchment/70'
    }
  }

  const getTrendIcon = () => {
    switch (trend) {
      case 'up': return '📈'
      case 'down': return '📉'
      case 'neutral': return '➡️'
      default: return ''
    }
  }

  return (
    <div className="codex-panel">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs text-codex-parchment/60">{label}</span>
        {icon && <span className="text-2xl">{icon}</span>}
      </div>
      <div className="flex items-end justify-between">
        <span className="text-3xl font-bold text-codex-gold">{value}</span>
        {trend && trendValue && (
          <div className={`flex items-center space-x-1 text-sm ${getTrendColor()}`}>
            <span>{getTrendIcon()}</span>
            <span>{trendValue}</span>
          </div>
        )}
      </div>
    </div>
  )
}

export function ProgressTile({
  label,
  current,
  total,
  percentage,
  color = 'bg-codex-gold',
}: {
  label: string
  current: number
  total: number
  percentage?: number
  color?: string
}) {
  const calculatedPercentage = percentage ?? Math.round((current / total) * 100)

  return (
    <div className="codex-panel">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-semibold">{label}</span>
        <span className="text-lg font-bold text-codex-gold">
          {current}/{total}
        </span>
      </div>
      <div className="w-full bg-codex-navy/50 rounded-full h-3">
        <div
          className={`${color} h-3 rounded-full transition-all duration-500`}
          style={{ width: `${calculatedPercentage}%` }}
        ></div>
      </div>
      <div className="mt-1 text-xs text-right text-codex-parchment/60">
        {calculatedPercentage}%
      </div>
    </div>
  )
}
