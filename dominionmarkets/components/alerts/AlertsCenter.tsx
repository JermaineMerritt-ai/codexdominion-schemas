/**
 * Alerts Center - Main Dashboard
 * ===============================
 * Personal signal hub for market alerts
 */

"use client"

import { useState, useEffect } from 'react'
import { Bell, Plus, TrendingUp, Newspaper, DollarSign, Calendar, RefreshCw } from 'lucide-react'
import AlertCard from '@/components/alerts/AlertCard'
import CreateAlertModal from '@/components/alerts/CreateAlertModal'
import { AlertsEmptyState, AlertsLoadError } from '@/components/alerts/AlertErrorStates'

interface Alert {
  id: string
  alert_type: string
  symbol: string | null
  condition_type: string
  target_value: number | null
  alert_name: string | null
  status: string
  trigger_count: number
  last_triggered_at: string | null
  notification_push: boolean
  notification_email: boolean
  created_at: string
}

interface RecentTrigger {
  id: string
  triggered_at: string
  trigger_value: number | null
  trigger_data: any
  alert: {
    id: string
    alert_type: string
    symbol: string | null
    alert_name: string | null
  }
}

interface Summary {
  active_count: number
  triggered_today: number
  counts_by_type: Record<string, number>
  limits_by_type: Record<string, number>
  user_tier: string
}

interface AlertsCenterProps {
  userTier: string
  identityType: string
}

export default function AlertsCenter({ userTier, identityType }: AlertsCenterProps) {
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [recentTriggers, setRecentTriggers] = useState<RecentTrigger[]>([])
  const [summary, setSummary] = useState<Summary | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [filterType, setFilterType] = useState<string | null>(null)

  useEffect(() => {
    loadData()
  }, [filterType])

  const loadData = async () => {
    try {
      setLoading(true)
      setError(null)

      // Load summary
      const summaryRes = await fetch('/api/alerts/summary')
      const summaryData = await summaryRes.json()
      setSummary(summaryData)

      // Load alerts
      const params = new URLSearchParams({ status: 'active' })
      if (filterType) params.append('alert_type', filterType)
      
      const alertsRes = await fetch(`/api/alerts?${params}`)
      const alertsData = await alertsRes.json()
      setAlerts(alertsData.alerts)

      // Load recent triggers
      const triggersRes = await fetch('/api/alerts/triggers/recent?hours=24')
      const triggersData = await triggersRes.json()
      setRecentTriggers(triggersData.triggers)

    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateAlert = () => {
    loadData() // Refresh after creating
  }

  const handleDeleteAlert = async (alertId: string) => {
    if (!confirm('Delete this alert? This cannot be undone.')) return

    try {
      await fetch(`/api/alerts/${alertId}`, { method: 'DELETE' })
      loadData()
    } catch (err) {
      alert('Failed to delete alert')
    }
  }

  const handlePauseAlert = async (alertId: string, isPaused: boolean) => {
    try {
      const endpoint = isPaused ? 'resume' : 'pause'
      await fetch(`/api/alerts/${alertId}/${endpoint}`, { method: 'POST' })
      loadData()
    } catch (err) {
      alert('Failed to update alert')
    }
  }

  const alertTypes = [
    { value: 'price', label: 'Price', icon: TrendingUp, color: 'text-green-600' },
    { value: 'news', label: 'News', icon: Newspaper, color: 'text-blue-600' },
    { value: 'earnings', label: 'Earnings', icon: DollarSign, color: 'text-purple-600' },
    { value: 'dividend', label: 'Dividend', icon: Calendar, color: 'text-emerald-600' }
  ]

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-6xl mx-auto px-4">
          <div className="animate-pulse space-y-6">
            <div className="h-12 bg-gray-200 rounded w-1/3"></div>
            <div className="h-32 bg-gray-200 rounded"></div>
            <div className="space-y-4">
              {[1, 2, 3].map(i => (
                <div key={i} className="h-24 bg-gray-200 rounded"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return <AlertsLoadError onRetry={loadData} />
  }

  if (alerts.length === 0 && !filterType) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-6xl mx-auto px-4">
          <AlertsEmptyState onCreate={() => setShowCreateModal(true)} />
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 flex items-center">
              <Bell className="h-8 w-8 mr-3 text-dominion-gold" />
              Alerts Center
            </h1>
            <p className="text-gray-600 mt-1">Your personal market signal hub</p>
          </div>
          
          <button
            onClick={() => setShowCreateModal(true)}
            className="flex items-center px-6 py-3 bg-dominion-gold text-gray-900 rounded-lg font-semibold hover:bg-yellow-500 transition-colors"
          >
            <Plus className="h-5 w-5 mr-2" />
            Create Alert
          </button>
        </div>

        {/* Summary Bar */}
        {summary && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div>
                <div className="text-3xl font-bold text-gray-900">{summary.active_count}</div>
                <div className="text-sm text-gray-600">Active Alerts</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-dominion-gold">{summary.triggered_today}</div>
                <div className="text-sm text-gray-600">Triggered Today</div>
              </div>
              <div>
                <div className="text-sm font-medium text-gray-700 mb-2">Usage by Type</div>
                <div className="space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-gray-600">Price:</span>
                    <span className="font-semibold">
                      {summary.counts_by_type.price || 0} / {summary.limits_by_type.price}
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-gray-600">News:</span>
                    <span className="font-semibold">
                      {summary.counts_by_type.news || 0} / {summary.limits_by_type.news}
                    </span>
                  </div>
                </div>
              </div>
              <div>
                <div className="inline-flex items-center px-3 py-1 rounded-full bg-blue-100 text-blue-800 text-sm font-semibold mb-2">
                  {summary.user_tier.toUpperCase()} Tier
                </div>
                {summary.user_tier === 'free' && (
                  <button className="text-xs text-dominion-gold hover:underline">
                    Upgrade for more alerts →
                  </button>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Alert Type Filters */}
        <div className="flex gap-2 mb-6 overflow-x-auto">
          <button
            onClick={() => setFilterType(null)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors whitespace-nowrap ${
              filterType === null
                ? 'bg-dominion-gold text-gray-900'
                : 'bg-white text-gray-700 border border-gray-200 hover:bg-gray-50'
            }`}
          >
            All Alerts
          </button>
          {alertTypes.map(type => {
            const Icon = type.icon
            return (
              <button
                key={type.value}
                onClick={() => setFilterType(type.value)}
                className={`flex items-center px-4 py-2 rounded-lg font-medium transition-colors whitespace-nowrap ${
                  filterType === type.value
                    ? 'bg-dominion-gold text-gray-900'
                    : 'bg-white text-gray-700 border border-gray-200 hover:bg-gray-50'
                }`}
              >
                <Icon className={`h-4 w-4 mr-2 ${type.color}`} />
                {type.label}
              </button>
            )
          })}
        </div>

        {/* Recent Triggers */}
        {recentTriggers.length > 0 && (
          <div className="mb-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <span className="text-2xl mr-2">🔴</span>
              Recent Triggers (Last 24 Hours)
            </h2>
            <div className="space-y-3">
              {recentTriggers.slice(0, 5).map(trigger => (
                <div
                  key={trigger.id}
                  className="bg-white rounded-lg shadow-sm border border-red-200 p-4 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="px-2 py-1 bg-red-100 text-red-800 text-xs font-semibold rounded">
                          {trigger.alert.alert_type.toUpperCase()}
                        </span>
                        {trigger.alert.symbol && (
                          <span className="font-mono font-semibold text-gray-900">
                            {trigger.alert.symbol}
                          </span>
                        )}
                      </div>
                      <p className="text-gray-900 font-medium">
                        {trigger.alert.alert_name || getAlertDescription(trigger)}
                      </p>
                      {trigger.trigger_value && (
                        <p className="text-sm text-gray-600 mt-1">
                          Triggered at: ${trigger.trigger_value}
                        </p>
                      )}
                    </div>
                    <div className="text-sm text-gray-500 text-right">
                      {new Date(trigger.triggered_at).toLocaleString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Active Alerts */}
        <div>
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center justify-between">
            <span className="flex items-center">
              <span className="text-2xl mr-2">⚡</span>
              {filterType ? `${filterType.charAt(0).toUpperCase() + filterType.slice(1)} Alerts` : 'Active Alerts'} ({alerts.length})
            </span>
            <button
              onClick={loadData}
              className="text-sm text-gray-600 hover:text-dominion-gold flex items-center"
            >
              <RefreshCw className="h-4 w-4 mr-1" />
              Refresh
            </button>
          </h2>

          {alerts.length === 0 ? (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
              <p className="text-gray-600 mb-4">
                No {filterType || 'active'} alerts found
              </p>
              <button
                onClick={() => setShowCreateModal(true)}
                className="text-dominion-gold hover:underline font-semibold"
              >
                Create your first {filterType || ''} alert →
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {alerts.map(alert => (
                <AlertCard
                  key={alert.id}
                  alert={alert}
                  onDelete={handleDeleteAlert}
                  onPause={handlePauseAlert}
                />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Create Alert Modal */}
      {showCreateModal && (
        <CreateAlertModal
          userTier={userTier}
          identityType={identityType}
          onClose={() => setShowCreateModal(false)}
          onSuccess={handleCreateAlert}
        />
      )}
    </div>
  )
}

function getAlertDescription(trigger: RecentTrigger): string {
  const { alert_type } = trigger.alert
  
  if (alert_type === 'price') return 'Price target reached'
  if (alert_type === 'news') return `${trigger.trigger_data?.article_count || 0} new articles`
  if (alert_type === 'earnings') return 'Earnings event'
  if (alert_type === 'dividend') return 'Dividend event'
  
  return 'Alert triggered'
}
