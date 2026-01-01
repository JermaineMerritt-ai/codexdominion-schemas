/**
 * Alert Detail View
 * =================
 * Full configuration and history of an alert
 */

"use client"

import { useState, useEffect } from 'react'
import { TrendingUp, Newspaper, DollarSign, Calendar, Briefcase, Volume2, Sparkles, Edit, Trash2, Clock, Bell, Globe, Sprout, Lightbulb, Crown as LegacyIcon, X } from 'lucide-react'

interface Alert {
  id: string
  alert_type: string
  symbol: string | null
  condition_type: string
  target_value: number | null
  alert_name: string | null
  min_verification_score: number | null
  status: string
  trigger_count: number
  last_triggered_at: string | null
  notification_push: boolean
  notification_email: boolean
  notification_sms: boolean
  created_at: string
}

interface Trigger {
  id: string
  triggered_at: string
  trigger_value: number | null
  trigger_data: any
}

interface RelatedCompany {
  symbol: string
  name: string
  correlation: number
}

interface AlertDetailViewProps {
  alertId: string
  identityType: string
  onClose: () => void
  onEdit: (alert: Alert) => void
  onDelete: (id: string) => void
}

export default function AlertDetailView({ alertId, identityType, onClose, onEdit, onDelete }: AlertDetailViewProps) {
  const [alert, setAlert] = useState<Alert | null>(null)
  const [triggers, setTriggers] = useState<Trigger[]>([])
  const [relatedCompanies, setRelatedCompanies] = useState<RelatedCompany[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadAlertDetail()
  }, [alertId])

  const loadAlertDetail = async () => {
    try {
      setLoading(true)
      setError(null)

      // Load alert
      const alertRes = await fetch(`/api/alerts/${alertId}`)
      if (!alertRes.ok) throw new Error('Failed to load alert')
      const alertData = await alertRes.json()
      setAlert(alertData)

      // Load trigger history
      const triggersRes = await fetch(`/api/alerts/${alertId}/triggers?limit=10`)
      if (triggersRes.ok) {
        const triggersData = await triggersRes.json()
        setTriggers(triggersData.triggers || [])
      }

      // Load related companies (if symbol exists)
      if (alertData.symbol) {
        // Mock data - in production, fetch from API
        setRelatedCompanies([
          { symbol: 'VOO', name: 'Vanguard S&P 500 ETF', correlation: 0.89 },
          { symbol: 'SPY', name: 'SPDR S&P 500 ETF', correlation: 0.87 },
          { symbol: 'QQQ', name: 'Invesco QQQ Trust', correlation: 0.72 }
        ])
      }
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'price': return TrendingUp
      case 'news': return Newspaper
      case 'earnings': return DollarSign
      case 'dividend': return Calendar
      case 'portfolio': return Briefcase
      case 'volume': return Volume2
      case 'cultural_alpha': return Sparkles
      default: return Bell
    }
  }

  const getIdentityTag = () => {
    switch (identityType) {
      case 'diaspora':
        return {
          icon: Globe,
          label: 'Global Opportunity',
          color: 'bg-blue-100 text-blue-800'
        }
      case 'youth':
        return {
          icon: Sprout,
          label: 'Learning Pick',
          color: 'bg-green-100 text-green-800'
        }
      case 'creator':
        return {
          icon: Lightbulb,
          label: 'Business Signal',
          color: 'bg-purple-100 text-purple-800'
        }
      case 'legacy':
        return {
          icon: LegacyIcon,
          label: 'Dividend Watch',
          color: 'bg-amber-100 text-amber-800'
        }
      default:
        return null
    }
  }

  const getConditionLabel = () => {
    if (!alert) return ''
    
    const type = alert.condition_type
    const value = alert.target_value
    
    if (type === 'above') return `↑ Above $${value}`
    if (type === 'below') return `↓ Below $${value}`
    if (type === 'percent_up') return `↑ +${value}%`
    if (type === 'percent_down') return `↓ -${value}%`
    if (type === 'any_news') return `📰 Any verified news`
    if (type === 'multi_source') return `📰 Multi-source confirmation`
    if (type === 'volume_above') return `📊 Volume above ${value?.toLocaleString()}`
    if (type === 'volume_spike') return `📊 Volume spike ${value}%`
    if (type === 'earnings_upcoming_7d') return `📅 7 days before earnings`
    if (type === 'earnings_upcoming_1d') return `📅 1 day before earnings`
    if (type === 'earnings_released') return `📊 Earnings released`
    if (type === 'ex_date_approaching') return `💰 Ex-date approaching`
    
    return type
  }

  const handleDelete = async () => {
    if (!alert) return
    if (!confirm('Are you sure you want to delete this alert?')) return

    try {
      const response = await fetch(`/api/alerts/${alert.id}`, {
        method: 'DELETE'
      })

      if (!response.ok) throw new Error('Failed to delete alert')

      onDelete(alert.id)
      onClose()
    } catch (err: any) {
      alert(err.message)
    }
  }

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-dominion-gold mx-auto"></div>
          <p className="text-center text-gray-600 mt-4">Loading alert details...</p>
        </div>
      </div>
    )
  }

  if (error || !alert) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg p-8 max-w-md">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Unable to load alert</h3>
          <p className="text-gray-600 mb-6">{error || 'Alert not found'}</p>
          <button
            onClick={onClose}
            className="w-full px-6 py-3 bg-gray-200 text-gray-700 font-semibold rounded-lg hover:bg-gray-300 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    )
  }

  const Icon = getAlertIcon(alert.alert_type)
  const identityTag = getIdentityTag()

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 overflow-y-auto">
      <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full my-8">
        {/* Header */}
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-start justify-between">
            <div className="flex items-start gap-4">
              <div className="p-3 rounded-lg bg-blue-100">
                <Icon className="h-8 w-8 text-blue-600" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-1">
                  {alert.alert_name || getConditionLabel()}
                </h2>
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs font-semibold rounded uppercase">
                    {alert.alert_type}
                  </span>
                  {alert.symbol && (
                    <span className="font-mono font-bold text-gray-900">
                      {alert.symbol}
                    </span>
                  )}
                  <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-semibold ${
                    alert.status === 'active' ? 'bg-green-100 text-green-800' :
                    alert.status === 'paused' ? 'bg-gray-200 text-gray-700' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {alert.status === 'active' ? '🟢 Active' :
                     alert.status === 'paused' ? '⏸️ Paused' :
                     '🔔 Triggered'}
                  </span>
                  {identityTag && (
                    <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-semibold ${identityTag.color}`}>
                      <identityTag.icon className="h-3 w-3 mr-1" />
                      {identityTag.label}
                    </span>
                  )}
                </div>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <X className="h-5 w-5 text-gray-600" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Configuration */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Alert Configuration</h3>
            <div className="bg-gray-50 rounded-lg p-4 space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Condition:</span>
                <span className="font-semibold text-gray-900">{getConditionLabel()}</span>
              </div>
              {alert.min_verification_score !== null && (
                <div className="flex justify-between">
                  <span className="text-gray-600">Min Verification:</span>
                  <span className="font-semibold text-gray-900">{alert.min_verification_score}/100</span>
                </div>
              )}
              <div className="flex justify-between">
                <span className="text-gray-600">Created:</span>
                <span className="font-semibold text-gray-900">
                  {new Date(alert.created_at).toLocaleDateString('en-US', {
                    month: 'long',
                    day: 'numeric',
                    year: 'numeric'
                  })}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Notifications:</span>
                <div className="flex gap-2">
                  {alert.notification_push && <span className="text-sm">📱 Push</span>}
                  {alert.notification_email && <span className="text-sm">✉️ Email</span>}
                  {alert.notification_sms && <span className="text-sm">💬 SMS</span>}
                </div>
              </div>
            </div>
          </div>

          {/* Trigger History */}
          {triggers.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Recent Triggers ({alert.trigger_count} total)
              </h3>
              <div className="space-y-3">
                {triggers.map((trigger) => (
                  <div key={trigger.id} className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex items-start gap-3">
                        <Clock className="h-5 w-5 text-yellow-600 mt-0.5" />
                        <div>
                          <p className="font-medium text-gray-900">
                            {new Date(trigger.triggered_at).toLocaleString('en-US', {
                              month: 'short',
                              day: 'numeric',
                              hour: '2-digit',
                              minute: '2-digit'
                            })}
                          </p>
                          {trigger.trigger_value !== null && (
                            <p className="text-sm text-gray-600 mt-1">
                              Value: ${trigger.trigger_value.toFixed(2)}
                            </p>
                          )}
                        </div>
                      </div>
                      <Bell className="h-5 w-5 text-yellow-600" />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Related Companies */}
          {relatedCompanies.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Related Companies</h3>
              <div className="grid gap-3">
                {relatedCompanies.map((company) => (
                  <div key={company.symbol} className="bg-gray-50 rounded-lg p-4 flex items-center justify-between hover:bg-gray-100 transition-colors cursor-pointer">
                    <div>
                      <p className="font-mono font-bold text-gray-900">{company.symbol}</p>
                      <p className="text-sm text-gray-600">{company.name}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-600">Correlation</p>
                      <p className="font-semibold text-gray-900">{(company.correlation * 100).toFixed(0)}%</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Last Triggered */}
          {alert.last_triggered_at && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <p className="text-sm font-medium text-blue-900 mb-1">Last Triggered</p>
              <p className="text-blue-700">
                {new Date(alert.last_triggered_at).toLocaleString('en-US', {
                  month: 'long',
                  day: 'numeric',
                  year: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </p>
            </div>
          )}
        </div>

        {/* Footer Actions */}
        <div className="flex items-center justify-between p-6 border-t border-gray-200 bg-gray-50">
          <button
            onClick={handleDelete}
            className="px-5 py-2.5 text-red-600 font-medium hover:bg-red-50 rounded-lg transition-colors flex items-center gap-2"
          >
            <Trash2 className="h-4 w-4" />
            Delete
          </button>
          
          <div className="flex gap-3">
            <button
              onClick={onClose}
              className="px-5 py-2.5 text-gray-700 font-medium hover:bg-gray-200 rounded-lg transition-colors"
            >
              Close
            </button>
            <button
              onClick={() => {
                onEdit(alert)
                onClose()
              }}
              className="px-6 py-2.5 bg-dominion-gold text-dominion-obsidian font-semibold rounded-lg hover:bg-yellow-500 transition-colors flex items-center gap-2"
            >
              <Edit className="h-4 w-4" />
              Edit Alert
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
