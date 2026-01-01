/**
 * Edit Alert Modal
 * =================
 * Modify existing alert configuration
 */

"use client"

import { useState, useEffect } from 'react'
import { X, TrendingUp, Newspaper, DollarSign, Calendar, Briefcase, Volume2, Sparkles, AlertCircle, Crown } from 'lucide-react'

interface Alert {
  id: string
  alert_type: string
  symbol: string | null
  condition_type: string
  target_value: number | null
  alert_name: string | null
  min_verification_score: number | null
  notification_push: boolean
  notification_email: boolean
  notification_sms: boolean
  status: string
}

interface EditAlertModalProps {
  alert: Alert
  userTier: string
  onClose: () => void
  onSuccess: () => void
  onDelete: (id: string) => void
}

export default function EditAlertModal({ alert, userTier, onClose, onSuccess, onDelete }: EditAlertModalProps) {
  // Form state - initialize with existing values
  const [symbol, setSymbol] = useState(alert.symbol || '')
  const [conditionType, setConditionType] = useState(alert.condition_type)
  const [targetValue, setTargetValue] = useState(alert.target_value?.toString() || '')
  const [alertName, setAlertName] = useState(alert.alert_name || '')
  const [minScore, setMinScore] = useState(alert.min_verification_score || 75)
  const [notifPush, setNotifPush] = useState(alert.notification_push)
  const [notifEmail, setNotifEmail] = useState(alert.notification_email)
  const [notifSMS, setNotifSMS] = useState(alert.notification_sms)
  const [saving, setSaving] = useState(false)
  const [deleting, setDeleting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showPremiumGate, setShowPremiumGate] = useState(false)

  // Check if this is a premium alert being edited by free user
  const isPremiumAlert = ['earnings', 'volume', 'cultural_alpha'].includes(alert.alert_type)
  const isPremiumCondition = ['percent_up', 'percent_down', 'volume_spike'].includes(conditionType)
  const shouldShowPremiumGate = userTier === 'free' && (isPremiumAlert || isPremiumCondition)

  useEffect(() => {
    if (shouldShowPremiumGate) {
      setShowPremiumGate(true)
    }
  }, [shouldShowPremiumGate])

  const getAlertIcon = () => {
    switch (alert.alert_type) {
      case 'price': return TrendingUp
      case 'news': return Newspaper
      case 'earnings': return DollarSign
      case 'dividend': return Calendar
      case 'portfolio': return Briefcase
      case 'volume': return Volume2
      case 'cultural_alpha': return Sparkles
      default: return TrendingUp
    }
  }

  const handleSave = async () => {
    setSaving(true)
    setError(null)

    try {
      const payload: any = {
        condition_type: conditionType,
        alert_name: alertName || null,
        notification_push: notifPush,
        notification_email: notifEmail,
        notification_sms: notifSMS
      }

      if (alert.alert_type === 'price') {
        if (!symbol) throw new Error('Stock symbol is required')
        if (!targetValue) throw new Error('Target value is required')
        
        payload.symbol = symbol.toUpperCase()
        payload.target_value = parseFloat(targetValue)
      }

      if (alert.alert_type === 'news') {
        if (!symbol) throw new Error('Stock symbol is required')
        
        payload.symbol = symbol.toUpperCase()
        payload.min_verification_score = minScore
      }

      if (['earnings', 'dividend', 'volume'].includes(alert.alert_type)) {
        if (!symbol) throw new Error('Stock symbol is required')
        payload.symbol = symbol.toUpperCase()
      }

      const response = await fetch(`/api/alerts/${alert.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Unable to update alert')
      }

      onSuccess()
      onClose()
    } catch (err: any) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this alert?')) return

    setDeleting(true)
    setError(null)

    try {
      const response = await fetch(`/api/alerts/${alert.id}`, {
        method: 'DELETE'
      })

      if (!response.ok) {
        throw new Error('Unable to delete alert')
      }

      onDelete(alert.id)
      onClose()
    } catch (err: any) {
      setError(err.message)
    } finally {
      setDeleting(false)
    }
  }

  const Icon = getAlertIcon()

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Premium Gate Overlay */}
        {showPremiumGate && (
          <div className="absolute inset-0 bg-white bg-opacity-95 z-10 rounded-lg flex items-center justify-center p-8">
            <div className="text-center max-w-md">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-dominion-gold bg-opacity-20 mb-4">
                <Crown className="h-8 w-8 text-dominion-gold" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">
                Premium Alert
              </h3>
              <p className="text-gray-600 mb-6">
                This alert type requires a Premium or Pro subscription. Upgrade to edit and unlock unlimited alert customization.
              </p>
              <div className="flex gap-3 justify-center">
                <button
                  onClick={() => window.location.href = '/pricing'}
                  className="px-6 py-3 bg-dominion-gold text-dominion-obsidian font-semibold rounded-lg hover:bg-yellow-500 transition-colors"
                >
                  Upgrade Now
                </button>
                <button
                  onClick={onClose}
                  className="px-6 py-3 bg-gray-200 text-gray-700 font-semibold rounded-lg hover:bg-gray-300 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-blue-100">
              <Icon className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Edit Alert</h2>
              <p className="text-sm text-gray-600">
                {alert.alert_type.charAt(0).toUpperCase() + alert.alert_type.slice(1)} Alert
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <X className="h-5 w-5 text-gray-600" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {/* Price Alert Configuration */}
          {alert.alert_type === 'price' && (
            <div className="space-y-6">
              {/* Stock Symbol */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Stock Symbol *
                </label>
                <input
                  type="text"
                  value={symbol}
                  onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                  placeholder="AAPL"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-dominion-gold focus:border-transparent"
                />
              </div>

              {/* Condition */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Condition *
                </label>
                <div className="grid grid-cols-2 gap-3">
                  <button
                    onClick={() => setConditionType('above')}
                    className={`px-4 py-3 rounded-lg border-2 font-medium transition-colors ${
                      conditionType === 'above'
                        ? 'border-dominion-gold bg-yellow-50 text-gray-900'
                        : 'border-gray-200 text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    ↑ Above
                  </button>
                  <button
                    onClick={() => setConditionType('below')}
                    className={`px-4 py-3 rounded-lg border-2 font-medium transition-colors ${
                      conditionType === 'below'
                        ? 'border-dominion-gold bg-yellow-50 text-gray-900'
                        : 'border-gray-200 text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    ↓ Below
                  </button>
                  <button
                    onClick={() => {
                      if (userTier === 'free') {
                        alert('% change conditions require Premium')
                        return
                      }
                      setConditionType('percent_up')
                    }}
                    disabled={userTier === 'free'}
                    className={`px-4 py-3 rounded-lg border-2 font-medium transition-colors ${
                      conditionType === 'percent_up'
                        ? 'border-dominion-gold bg-yellow-50 text-gray-900'
                        : 'border-gray-200 text-gray-700 hover:border-gray-300'
                    } ${userTier === 'free' ? 'opacity-50 cursor-not-allowed' : ''}`}
                  >
                    ↑ % Up {userTier === 'free' && '🔒'}
                  </button>
                  <button
                    onClick={() => {
                      if (userTier === 'free') {
                        alert('% change conditions require Premium')
                        return
                      }
                      setConditionType('percent_down')
                    }}
                    disabled={userTier === 'free'}
                    className={`px-4 py-3 rounded-lg border-2 font-medium transition-colors ${
                      conditionType === 'percent_down'
                        ? 'border-dominion-gold bg-yellow-50 text-gray-900'
                        : 'border-gray-200 text-gray-700 hover:border-gray-300'
                    } ${userTier === 'free' ? 'opacity-50 cursor-not-allowed' : ''}`}
                  >
                    ↓ % Down {userTier === 'free' && '🔒'}
                  </button>
                </div>
              </div>

              {/* Target Value */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Target {conditionType.includes('percent') ? '(%)' : '($)'} *
                </label>
                <input
                  type="number"
                  value={targetValue}
                  onChange={(e) => setTargetValue(e.target.value)}
                  placeholder={conditionType.includes('percent') ? '5' : '185.00'}
                  step={conditionType.includes('percent') ? '0.1' : '0.01'}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-dominion-gold focus:border-transparent"
                />
              </div>

              {/* Alert Name */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Alert Name (Optional)
                </label>
                <input
                  type="text"
                  value={alertName}
                  onChange={(e) => setAlertName(e.target.value)}
                  placeholder="AAPL Above $185"
                  maxLength={100}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-dominion-gold focus:border-transparent"
                />
              </div>
            </div>
          )}

          {/* News Alert Configuration */}
          {alert.alert_type === 'news' && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Stock Symbol *
                </label>
                <input
                  type="text"
                  value={symbol}
                  onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                  placeholder="NVDA"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-dominion-gold focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Minimum Verification Score: {minScore}
                </label>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={minScore}
                  onChange={(e) => setMinScore(parseInt(e.target.value))}
                  className="w-full"
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>Any News</span>
                  <span>Verified Only</span>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Alert Name (Optional)
                </label>
                <input
                  type="text"
                  value={alertName}
                  onChange={(e) => setAlertName(e.target.value)}
                  placeholder="NVDA Verified News"
                  maxLength={100}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-dominion-gold focus:border-transparent"
                />
              </div>
            </div>
          )}

          {/* Earnings/Dividend/Volume Alerts */}
          {['earnings', 'dividend', 'volume'].includes(alert.alert_type) && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Stock Symbol *
                </label>
                <input
                  type="text"
                  value={symbol}
                  onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                  placeholder="TSLA"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-dominion-gold focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Alert Name (Optional)
                </label>
                <input
                  type="text"
                  value={alertName}
                  onChange={(e) => setAlertName(e.target.value)}
                  placeholder={`${symbol} ${alert.alert_type} alert`}
                  maxLength={100}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-dominion-gold focus:border-transparent"
                />
              </div>
            </div>
          )}

          {/* Notification Preferences */}
          <div className="mt-6">
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Notification Preferences
            </label>
            <div className="space-y-2">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={notifPush}
                  onChange={(e) => setNotifPush(e.target.checked)}
                  className="w-4 h-4 text-dominion-gold focus:ring-dominion-gold rounded"
                />
                <span className="ml-3 text-sm text-gray-700">Push notification</span>
              </label>
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={notifEmail}
                  onChange={(e) => setNotifEmail(e.target.checked)}
                  className="w-4 h-4 text-dominion-gold focus:ring-dominion-gold rounded"
                />
                <span className="ml-3 text-sm text-gray-700">Email</span>
              </label>
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={notifSMS}
                  onChange={(e) => setNotifSMS(e.target.checked)}
                  disabled={userTier !== 'pro'}
                  className="w-4 h-4 text-dominion-gold focus:ring-dominion-gold rounded disabled:opacity-50"
                />
                <span className="ml-3 text-sm text-gray-700">
                  SMS {userTier !== 'pro' && <span className="text-dominion-gold">(Pro only)</span>}
                </span>
              </label>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start">
              <AlertCircle className="h-5 w-5 text-red-600 mr-3 flex-shrink-0 mt-0.5" />
              <div className="text-sm text-red-800">{error}</div>
            </div>
          )}
        </div>

        {/* Footer Actions */}
        <div className="flex items-center justify-between p-6 border-t border-gray-200 bg-gray-50">
          <button
            onClick={handleDelete}
            disabled={deleting || saving}
            className="px-5 py-2.5 text-red-600 font-medium hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50"
          >
            {deleting ? 'Deleting...' : 'Delete Alert'}
          </button>
          
          <div className="flex gap-3">
            <button
              onClick={onClose}
              disabled={saving || deleting}
              className="px-5 py-2.5 text-gray-700 font-medium hover:bg-gray-200 rounded-lg transition-colors disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              disabled={saving || deleting || showPremiumGate}
              className="px-6 py-2.5 bg-dominion-gold text-dominion-obsidian font-semibold rounded-lg hover:bg-yellow-500 transition-colors disabled:opacity-50"
            >
              {saving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
