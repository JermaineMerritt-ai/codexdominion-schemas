/**
 * Create Alert Modal
 * ==================
 * Wizard for creating new alerts
 */

"use client"

import { useState } from 'react'
import { X, TrendingUp, Newspaper, DollarSign, Calendar, Briefcase, Volume2, Sparkles, Lock } from 'lucide-react'

interface CreateAlertModalProps {
  userTier: string
  identityType: string
  onClose: () => void
  onSuccess: () => void
}

export default function CreateAlertModal({ userTier, identityType, onClose, onSuccess }: CreateAlertModalProps) {
  const [step, setStep] = useState<'type' | 'configure'>('type')
  const [selectedType, setSelectedType] = useState<string | null>(null)
  
  // Form state
  const [symbol, setSymbol] = useState('')
  const [conditionType, setConditionType] = useState('above')
  const [targetValue, setTargetValue] = useState('')
  const [alertName, setAlertName] = useState('')
  const [minScore, setMinScore] = useState(75)
  const [notifPush, setNotifPush] = useState(true)
  const [notifEmail, setNotifEmail] = useState(false)
  const [notifSMS, setNotifSMS] = useState(false)
  const [creating, setCreating] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const alertTypes = [
    {
      value: 'price',
      label: 'Price Alert',
      icon: TrendingUp,
      description: 'Get notified when price crosses threshold',
      limits: { free: 5, premium: 50, pro: 999999 },
      premium: false
    },
    {
      value: 'news',
      label: 'News Alert',
      icon: Newspaper,
      description: 'Get notified about verified news',
      limits: { free: 3, premium: 20, pro: 999999 },
      premium: false
    },
    {
      value: 'earnings',
      label: 'Earnings Alert',
      icon: DollarSign,
      description: 'Get notified about earnings events',
      limits: { free: 10, premium: 100, pro: 999999 },
      premium: false
    },
    {
      value: 'dividend',
      label: 'Dividend Alert',
      icon: Calendar,
      description: 'Get notified about dividend events',
      limits: { free: 5, premium: 30, pro: 999999 },
      premium: false
    },
    {
      value: 'portfolio',
      label: 'Portfolio Alert',
      icon: Briefcase,
      description: 'Get notified about portfolio changes',
      limits: { free: 3, premium: 15, pro: 999999 },
      premium: false
    },
    {
      value: 'volume',
      label: 'Volume Alert',
      icon: Volume2,
      description: 'Unusual trading activity',
      limits: { free: 0, premium: 10, pro: 50 },
      premium: true
    },
    {
      value: 'cultural_alpha',
      label: 'Cultural Alpha',
      icon: Sparkles,
      description: 'Identity-specific opportunities',
      limits: { free: 2, premium: 10, pro: 999999 },
      premium: true
    }
  ]

  const handleSelectType = (type: string) => {
    const alertType = alertTypes.find(t => t.value === type)
    if (!alertType) return

    // Check if requires premium
    if (alertType.premium && userTier === 'free') {
      alert('This alert type requires Premium or Pro subscription')
      return
    }

    setSelectedType(type)
    setStep('configure')
  }

  const handleCreate = async () => {
    setCreating(true)
    setError(null)

    try {
      const payload: any = {
        alert_type: selectedType,
        condition_type: conditionType,
        alert_name: alertName || null,
        notification_push: notifPush,
        notification_email: notifEmail,
        notification_sms: notifSMS
      }

      if (selectedType === 'price') {
        if (!symbol) throw new Error('Stock symbol is required')
        if (!targetValue) throw new Error('Target value is required')
        
        payload.symbol = symbol.toUpperCase()
        payload.target_value = parseFloat(targetValue)
      }

      if (selectedType === 'news') {
        if (!symbol) throw new Error('Stock symbol is required')
        
        payload.symbol = symbol.toUpperCase()
        payload.min_verification_score = minScore
        payload.condition_type = 'any_news'
      }

      if (selectedType === 'earnings') {
        if (!symbol) throw new Error('Stock symbol is required')
        
        payload.symbol = symbol.toUpperCase()
      }

      if (selectedType === 'dividend') {
        if (!symbol) throw new Error('Stock symbol is required')
        
        payload.symbol = symbol.toUpperCase()
      }

      if (selectedType === 'volume') {
        if (!symbol) throw new Error('Stock symbol is required')
        if (!targetValue) throw new Error('Volume value is required')
        
        payload.symbol = symbol.toUpperCase()
        payload.target_value = parseFloat(targetValue)
      }

      const response = await fetch('/api/alerts/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })

      const data = await response.json()

      if (!response.ok) {
        if (data.upgrade_required) {
          throw new Error(`Alert limit reached (${data.current_count}/${data.limit}). Upgrade to ${data.tier === 'free' ? 'Premium' : 'Pro'} for more alerts.`)
        }
        throw new Error(data.error || 'Failed to create alert')
      }

      onSuccess()
      onClose()
    } catch (err: any) {
      setError(err.message)
    } finally {
      setCreating(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900">
            {step === 'type' ? 'Create New Alert' : `Configure ${selectedType?.charAt(0).toUpperCase()}${selectedType?.slice(1)} Alert`}
          </h2>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <X className="h-5 w-5 text-gray-600" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {step === 'type' && (
            <div className="space-y-6">
              {/* Identity-Based Suggestions */}
              <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4 border border-blue-200">
                <h3 className="font-semibold text-gray-900 mb-2 flex items-center">
                  <Sparkles className="h-5 w-5 mr-2 text-dominion-gold" />
                  Suggested for {identityType.charAt(0).toUpperCase() + identityType.slice(1)}
                </h3>
                <div className="space-y-2 text-sm">
                  {identityType === 'diaspora' && (
                    <>
                      <p className="text-gray-700">• Caribbean-linked companies (e.g., Grace Kennedy)</p>
                      <p className="text-gray-700">• Regional economic indicators</p>
                      <p className="text-gray-700">• Diaspora-relevant news alerts</p>
                    </>
                  )}
                  {identityType === 'youth' && (
                    <>
                      <p className="text-gray-700">• Beginner-friendly companies (e.g., VOO, SPY)</p>
                      <p className="text-gray-700">• Learning-focused news</p>
                      <p className="text-gray-700">• Mock portfolio alerts</p>
                    </>
                  )}
                  {identityType === 'creator' && (
                    <>
                      <p className="text-gray-700">• Creator-economy companies (e.g., Shopify)</p>
                      <p className="text-gray-700">• AI-tool companies (e.g., NVIDIA)</p>
                      <p className="text-gray-700">• Digital-product platforms</p>
                    </>
                  )}
                  {identityType === 'legacy' && (
                    <>
                      <p className="text-gray-700">• Dividend announcements</p>
                      <p className="text-gray-700">• Long-term stability indicators</p>
                      <p className="text-gray-700">• Low-volatility companies (e.g., JNJ, KO)</p>
                    </>
                  )}
                </div>
              </div>
              
              <div className="space-y-3">
              <p className="text-gray-600">Select alert type to get started</p>
              
              {alertTypes.map(type => {
                const Icon = type.icon
                const limit = type.limits[userTier as keyof typeof type.limits]
                const isLocked = type.premium && userTier === 'free'

                return (
                  <button
                    key={type.value}
                    onClick={() => handleSelectType(type.value)}
                    disabled={isLocked}
                    className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                      isLocked
                        ? 'border-gray-200 bg-gray-50 cursor-not-allowed opacity-60'
                        : 'border-gray-200 hover:border-dominion-gold hover:bg-yellow-50'
                    }`}
                  >
                    <div className="flex items-start">
                      <div className={`p-2 rounded-lg mr-4 ${
                        isLocked ? 'bg-gray-200' : 'bg-blue-100'
                      }`}>
                        <Icon className={`h-6 w-6 ${isLocked ? 'text-gray-400' : 'text-blue-600'}`} />
                      </div>
                      
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-1">
                          <h3 className="font-semibold text-gray-900 flex items-center">
                            {type.label}
                            {isLocked && <Lock className="h-4 w-4 ml-2 text-gray-400" />}
                          </h3>
                          <span className="text-xs text-gray-500">
                            {limit === 999999 ? 'Unlimited' : `${limit} alerts`}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600">{type.description}</p>
                        {isLocked && (
                          <p className="text-xs text-dominion-gold mt-1 font-medium">
                            Premium required
                          </p>
                        )}
                      </div>
                    </div>
                  </button>
                )
              })}
            </div>
          )}

          {step === 'configure' && selectedType === 'price' && (
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
                    onClick={() => setConditionType('percent_up')}
                    className={`px-4 py-3 rounded-lg border-2 font-medium transition-colors ${
                      conditionType === 'percent_up'
                        ? 'border-dominion-gold bg-yellow-50 text-gray-900'
                        : 'border-gray-200 text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    ↑ % Up
                  </button>
                  <button
                    onClick={() => setConditionType('percent_down')}
                    className={`px-4 py-3 rounded-lg border-2 font-medium transition-colors ${
                      conditionType === 'percent_down'
                        ? 'border-dominion-gold bg-yellow-50 text-gray-900'
                        : 'border-gray-200 text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    ↓ % Down
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

              {/* Alert Name (Optional) */}
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

              {/* Notification Preferences */}
              <div>
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
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-sm text-red-800">
                  {error}
                </div>
              )}
            </div>
          )}

          {step === 'configure' && selectedType === 'news' && (
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
                  min="60"
                  max="100"
                  step="5"
                  value={minScore}
                  onChange={(e) => setMinScore(parseInt(e.target.value))}
                  className="w-full"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Higher score = more sources required
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Alert Name (Optional)
                </label>
                <input
                  type="text"
                  value={alertName}
                  onChange={(e) => setAlertName(e.target.value)}
                  placeholder="NVDA News Alert"
                  maxLength={100}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-dominion-gold focus:border-transparent"
                />
              </div>

              {/* Notification Preferences */}
              <div>
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
                </div>
              </div>

              {error && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-sm text-red-800">
                  {error}
                </div>
              )}
            </div>
          )}

          {step === 'configure' && selectedType === 'volume' && (
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
                  Condition Type *
                </label>
                <div className="space-y-3">
                  <button
                    onClick={() => setConditionType('volume_above')}
                    className={`w-full text-left px-4 py-3 rounded-lg border-2 font-medium transition-colors ${
                      conditionType === 'volume_above'
                        ? 'border-dominion-gold bg-yellow-50 text-gray-900'
                        : 'border-gray-200 text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <span>📊 Volume Above Threshold</span>
                      <span className="text-xs text-gray-500">Free</span>
                    </div>
                  </button>
                  <button
                    onClick={() => {
                      if (userTier === 'free') {
                        alert('Volume spike alerts require Premium')
                        return
                      }
                      setConditionType('volume_spike')
                    }}
                    disabled={userTier === 'free'}
                    className={`w-full text-left px-4 py-3 rounded-lg border-2 font-medium transition-colors ${
                      conditionType === 'volume_spike'
                        ? 'border-dominion-gold bg-yellow-50 text-gray-900'
                        : 'border-gray-200 text-gray-700 hover:border-gray-300'
                    } ${userTier === 'free' ? 'opacity-50 cursor-not-allowed' : ''}`}
                  >
                    <div className="flex justify-between items-center">
                      <span>📈 Volume Spike % {userTier === 'free' && '🔒'}</span>
                      <span className="text-xs text-dominion-gold">Premium</span>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">
                      Alert when volume exceeds historical average by X%
                    </p>
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {conditionType === 'volume_spike' ? 'Spike Percentage (%)' : 'Volume Threshold'} *
                </label>
                <input
                  type="number"
                  value={targetValue}
                  onChange={(e) => setTargetValue(e.target.value)}
                  placeholder={conditionType === 'volume_spike' ? '50' : '1000000'}
                  step={conditionType === 'volume_spike' ? '10' : '100000'}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-dominion-gold focus:border-transparent"
                />
                <p className="text-xs text-gray-500 mt-1">
                  {conditionType === 'volume_spike' 
                    ? 'Alert when volume is X% above 30-day average'
                    : 'Alert when daily volume exceeds this number'}
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Alert Name (Optional)
                </label>
                <input
                  type="text"
                  value={alertName}
                  onChange={(e) => setAlertName(e.target.value)}
                  placeholder="TSLA High Volume"
                  maxLength={100}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-dominion-gold focus:border-transparent"
                />
              </div>

              {/* Notification Preferences */}
              <div>
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

              {error && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-sm text-red-800">
                  {error}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        {step === 'configure' && (
          <div className="flex items-center justify-between p-6 border-t border-gray-200">
            <button
              onClick={() => setStep('type')}
              className="px-6 py-2 text-gray-700 hover:bg-gray-100 rounded-lg font-medium transition-colors"
            >
              ← Back
            </button>
            <button
              onClick={handleCreate}
              disabled={creating}
              className="px-8 py-3 bg-dominion-gold text-gray-900 rounded-lg font-semibold hover:bg-yellow-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {creating ? 'Creating...' : 'Create Alert'}
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
