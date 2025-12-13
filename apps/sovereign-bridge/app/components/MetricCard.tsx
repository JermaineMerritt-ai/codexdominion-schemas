'use client'

import { ReactNode } from 'react'

interface MetricCardProps {
  label: string
  value: string | number
  icon?: string
  trend?: 'up' | 'down' | 'neutral'
  trendValue?: string
  subtitle?: string
  color?: 'gold' | 'green' | 'blue' | 'purple' | 'red'
  size?: 'sm' | 'md' | 'lg'
  className?: string
  onClick?: () => void
}

export default function MetricCard({
  label,
  value,
  icon,
  trend,
  trendValue,
  subtitle,
  color = 'gold',
  size = 'md',
  className = '',
  onClick,
}: MetricCardProps) {
  const getColorClass = () => {
    switch (color) {
      case 'gold': return 'text-codex-gold'
      case 'green': return 'text-green-400'
      case 'blue': return 'text-blue-400'
      case 'purple': return 'text-purple-400'
      case 'red': return 'text-red-400'
      default: return 'text-codex-gold'
    }
  }

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
      case 'up': return '↗'
      case 'down': return '↘'
      case 'neutral': return '→'
      default: return ''
    }
  }

  const getSizeClasses = () => {
    switch (size) {
      case 'sm':
        return {
          value: 'text-xl',
          label: 'text-xs',
          icon: 'text-2xl',
        }
      case 'md':
        return {
          value: 'text-3xl',
          label: 'text-sm',
          icon: 'text-3xl',
        }
      case 'lg':
        return {
          value: 'text-4xl',
          label: 'text-base',
          icon: 'text-4xl',
        }
    }
  }

  const sizeClasses = getSizeClasses()
  const Wrapper = onClick ? 'button' : 'div'

  return (
    <Wrapper
      onClick={onClick}
      className={`
        codex-panel
        ${onClick ? 'cursor-pointer hover:bg-codex-gold/10 transition-all' : ''}
        ${className}
      `}
    >
      <div className="flex items-start justify-between mb-2">
        <span className={`${sizeClasses.label} text-codex-parchment/60 uppercase font-semibold`}>
          {label}
        </span>
        {icon && <span className={sizeClasses.icon}>{icon}</span>}
      </div>

      <div className="flex items-end justify-between">
        <div className="flex-1">
          <div className={`${sizeClasses.value} font-bold ${getColorClass()} leading-none mb-1`}>
            {value}
          </div>
          {subtitle && (
            <div className="text-xs text-codex-parchment/50">{subtitle}</div>
          )}
        </div>

        {trend && trendValue && (
          <div className={`flex items-center space-x-1 ${getTrendColor()} ml-2`}>
            <span className="text-lg font-semibold">{getTrendIcon()}</span>
            <span className="text-sm font-semibold">{trendValue}</span>
          </div>
        )}
      </div>
    </Wrapper>
  )
}

// Grid variant for displaying multiple metrics
export function MetricCardGrid({
  children,
  columns = 4,
}: {
  children: ReactNode
  columns?: 2 | 3 | 4 | 6
}) {
  const gridClass = {
    2: 'grid-cols-1 md:grid-cols-2',
    3: 'grid-cols-1 md:grid-cols-3',
    4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4',
    6: 'grid-cols-2 md:grid-cols-3 lg:grid-cols-6',
  }[columns]

  return <div className={`grid ${gridClass} gap-4`}>{children}</div>
}

// Compact inline variant
export function InlineMetric({
  label,
  value,
  color = 'gold',
}: {
  label: string
  value: string | number
  color?: 'gold' | 'green' | 'blue' | 'purple' | 'red'
}) {
  const getColorClass = () => {
    switch (color) {
      case 'gold': return 'text-codex-gold'
      case 'green': return 'text-green-400'
      case 'blue': return 'text-blue-400'
      case 'purple': return 'text-purple-400'
      case 'red': return 'text-red-400'
      default: return 'text-codex-gold'
    }
  }

  return (
    <div className="flex items-center justify-between text-sm">
      <span className="text-codex-parchment/70">{label}</span>
      <span className={`font-bold ${getColorClass()}`}>{value}</span>
    </div>
  )
}
