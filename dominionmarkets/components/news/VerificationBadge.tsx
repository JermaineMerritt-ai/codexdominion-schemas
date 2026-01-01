/**
 * Verification Badge
 * ==================
 * Visual verification score display with color coding
 */

"use client"

import { CheckCircle2, AlertCircle, XCircle, HelpCircle } from 'lucide-react'

interface VerificationBadgeProps {
  score: number
  badge: {
    emoji: string
    label: string
    color: string
  }
  sourceCount?: number
  size?: 'small' | 'medium' | 'large'
  showLabel?: boolean
  onClick?: () => void
}

export default function VerificationBadge({ 
  score, 
  badge, 
  sourceCount = 0,
  size = 'medium',
  showLabel = true,
  onClick
}: VerificationBadgeProps) {
  // Get verification level based on source count
  const getVerificationLevel = () => {
    if (sourceCount >= 3) return 'Verified'
    if (sourceCount >= 1) return 'Partially Verified'
    return 'Unverified'
  }
  
  const verificationLevel = getVerificationLevel()
  const displayLabel = showLabel && size !== 'small' ? verificationLevel : ''
  const sizeClasses = {
    small: 'text-xs px-2 py-1',
    medium: 'text-sm px-3 py-1.5',
    large: 'text-base px-4 py-2'
  }

  const iconSizes = {
    small: 'h-3 w-3',
    medium: 'h-4 w-4',
    large: 'h-5 w-5'
  }

  const colorClasses = {
    emerald: 'bg-emerald-50 border-emerald-200 text-emerald-800',
    green: 'bg-green-50 border-green-200 text-green-800',
    yellow: 'bg-yellow-50 border-yellow-200 text-yellow-800',
    red: 'bg-red-50 border-red-200 text-red-800'
  }

  const Icon = getIcon(score)
  const colorClass = colorClasses[badge.color as keyof typeof colorClasses] || colorClasses.green

  return (
    <button
      onClick={onClick}
      disabled={!onClick}
      className={`inline-flex items-center border rounded-lg font-semibold ${sizeClasses[size]} ${colorClass} ${
        onClick ? 'cursor-pointer hover:opacity-80 transition-opacity' : 'cursor-default'
      }`}
      title={`${verificationLevel} • ${sourceCount} source${sourceCount !== 1 ? 's' : ''} • Tap for details`}
    >
      <Icon className={`${iconSizes[size]} mr-1.5`} />
      <span className="font-mono">{score}/100</span>
      {displayLabel && (
        <span className="ml-2 font-normal">{displayLabel}</span>
      )}
    </button>
  )
}

function getIcon(score: number) {
  if (score >= 90) return CheckCircle2
  if (score >= 75) return CheckCircle2
  if (score >= 60) return AlertCircle
  if (score >= 1) return XCircle
  return HelpCircle
}
