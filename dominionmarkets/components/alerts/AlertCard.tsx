/**
 * Alert Card Component
 * ====================
 * Individual alert display with actions
 */

"use client"

import { TrendingUp, Newspaper, DollarSign, Calendar, MoreVertical, Pause, Play, Trash2, Edit } from 'lucide-react'
import { useState } from 'react'

interface AlertCardProps {
  alert: {
    id: string
    alert_type: string
    symbol: string | null
    condition_type: string
    target_value: number | null
    alert_name: string | null
    status: string
    trigger_count: number
    last_triggered_at: string | null
    created_at: string
  }
  onDelete: (id: string) => void
  onPause: (id: string, isPaused: boolean) => void
}

export default function AlertCard({ alert, onDelete, onPause }: AlertCardProps) {
  const [showMenu, setShowMenu] = useState(false)
  
  const isPaused = alert.status === 'paused'
  const isTriggered = alert.status === 'triggered'
  
  const getAlertIcon = () => {
    switch (alert.alert_type) {
      case 'price': return TrendingUp
      case 'news': return Newspaper
      case 'earnings': return DollarSign
      case 'dividend': return Calendar
      default: return TrendingUp
    }
  }

  const getAlertColor = () => {
    switch (alert.alert_type) {
      case 'price': return 'text-green-600 bg-green-100'
      case 'news': return 'text-blue-600 bg-blue-100'
      case 'earnings': return 'text-purple-600 bg-purple-100'
      case 'dividend': return 'text-emerald-600 bg-emerald-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getConditionLabel = () => {
    const type = alert.condition_type
    const value = alert.target_value
    
    if (type === 'above') return `↑ Above $${value}`
    if (type === 'below') return `↓ Below $${value}`
    if (type === 'percent_up') return `↑ +${value}%`
    if (type === 'percent_down') return `↓ -${value}%`
    if (type === 'any_news') return `📰 Any verified news`
    if (type === 'earnings_upcoming_7d') return `📅 7 days before earnings`
    if (type === 'earnings_upcoming_1d') return `📅 1 day before earnings`
    if (type === 'earnings_released') return `📊 Earnings released`
    if (type === 'ex_date_approaching') return `💰 Ex-date approaching`
    
    return type
  }

  const getStatusBadge = () => {
    if (isPaused) {
      return (
        <span className="inline-flex items-center px-2 py-1 rounded text-xs font-semibold bg-gray-200 text-gray-700">
          ⏸️ Paused
        </span>
      )
    }
    if (isTriggered) {
      return (
        <span className="inline-flex items-center px-2 py-1 rounded text-xs font-semibold bg-red-100 text-red-800">
          🔔 Triggered
        </span>
      )
    }
    return (
      <span className="inline-flex items-center px-2 py-1 rounded text-xs font-semibold bg-green-100 text-green-800">
        🟢 Active
      </span>
    )
  }

  const Icon = getAlertIcon()

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-5 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          {/* Header */}
          <div className="flex items-center gap-3 mb-3">
            <div className={`p-2 rounded-lg ${getAlertColor()}`}>
              <Icon className="h-5 w-5" />
            </div>
            
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <span className="px-2 py-0.5 bg-gray-100 text-gray-700 text-xs font-semibold rounded uppercase">
                  {alert.alert_type}
                </span>
                {alert.symbol && (
                  <span className="font-mono font-bold text-gray-900">
                    {alert.symbol}
                  </span>
                )}
                {getStatusBadge()}
              </div>
              
              <h3 className="font-semibold text-gray-900">
                {alert.alert_name || getConditionLabel()}
              </h3>
            </div>
          </div>

          {/* Details */}
          <div className="ml-14 space-y-2">
            <div className="flex items-center gap-4 text-sm text-gray-600">
              <span>Condition: {getConditionLabel()}</span>
              <span>•</span>
              <span>Created: {new Date(alert.created_at).toLocaleDateString()}</span>
            </div>

            {alert.trigger_count > 0 && (
              <div className="text-sm text-gray-600">
                Triggered {alert.trigger_count} time{alert.trigger_count !== 1 ? 's' : ''}
                {alert.last_triggered_at && (
                  <span className="text-dominion-gold font-medium ml-1">
                    • Last: {new Date(alert.last_triggered_at).toLocaleString('en-US', {
                      month: 'short',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </span>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Actions Menu */}
        <div className="relative">
          <button
            onClick={() => setShowMenu(!showMenu)}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <MoreVertical className="h-5 w-5 text-gray-600" />
          </button>

          {showMenu && (
            <>
              <div
                className="fixed inset-0 z-10"
                onClick={() => setShowMenu(false)}
              />
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-20">
                <button
                  onClick={() => {
                    // TODO: Implement edit
                    setShowMenu(false)
                  }}
                  className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 flex items-center"
                >
                  <Edit className="h-4 w-4 mr-2" />
                  Edit Alert
                </button>
                
                <button
                  onClick={() => {
                    onPause(alert.id, isPaused)
                    setShowMenu(false)
                  }}
                  className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 flex items-center"
                >
                  {isPaused ? (
                    <>
                      <Play className="h-4 w-4 mr-2" />
                      Resume Alert
                    </>
                  ) : (
                    <>
                      <Pause className="h-4 w-4 mr-2" />
                      Pause Alert
                    </>
                  )}
                </button>
                
                <div className="border-t border-gray-200 my-1" />
                
                <button
                  onClick={() => {
                    onDelete(alert.id)
                    setShowMenu(false)
                  }}
                  className="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50 flex items-center"
                >
                  <Trash2 className="h-4 w-4 mr-2" />
                  Delete Alert
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
