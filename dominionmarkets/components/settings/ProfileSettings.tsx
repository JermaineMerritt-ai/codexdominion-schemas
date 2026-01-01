/**
 * Profile & Identity Settings
 * ===========================
 * Category 1: Manage personal information and identity type
 */

"use client"

import { useState } from 'react'
import { User, Mail, Globe, Sprout, Lightbulb, Crown as LegacyIcon, Camera, Link, Save, AlertCircle } from 'lucide-react'

interface ProfileSettingsProps {
  initialData: {
    name: string
    email: string
    identityType: string
    profilePhoto?: string
    codexDominionConnected: boolean
  }
  onSave: (data: any) => Promise<void>
  onBack: () => void
}

export default function ProfileSettings({ initialData, onSave, onBack }: ProfileSettingsProps) {
  const [name, setName] = useState(initialData.name)
  const [email, setEmail] = useState(initialData.email)
  const [identityType, setIdentityType] = useState(initialData.identityType)
  const [profilePhoto, setProfilePhoto] = useState(initialData.profilePhoto || '')
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  const [showIdentityConfirm, setShowIdentityConfirm] = useState(false)
  const [pendingIdentity, setPendingIdentity] = useState<string | null>(null)

  const identities = [
    {
      value: 'diaspora',
      label: 'Diaspora',
      icon: Globe,
      description: 'Global investor perspective with regional insights',
      color: 'text-blue-600 bg-blue-50'
    },
    {
      value: 'youth',
      label: 'Youth',
      icon: Sprout,
      description: 'Learning-focused with beginner-friendly content',
      color: 'text-green-600 bg-green-50'
    },
    {
      value: 'creator',
      label: 'Creator',
      icon: Lightbulb,
      description: 'Business-focused with creator economy insights',
      color: 'text-purple-600 bg-purple-50'
    },
    {
      value: 'legacy',
      label: 'Legacy-Builder',
      icon: LegacyIcon,
      description: 'Long-term wealth with dividend focus',
      color: 'text-amber-600 bg-amber-50'
    }
  ]

  const handleIdentityChange = (newIdentity: string) => {
    if (newIdentity === identityType) return
    
    setPendingIdentity(newIdentity)
    setShowIdentityConfirm(true)
  }

  const confirmIdentityChange = () => {
    if (pendingIdentity) {
      setIdentityType(pendingIdentity)
      setShowIdentityConfirm(false)
      setPendingIdentity(null)
    }
  }

  const handleSave = async () => {
    setSaving(true)
    setError(null)
    setSuccess(false)

    try {
      // Validation
      if (!name.trim()) throw new Error('Name is required')
      if (!email.trim()) throw new Error('Email is required')
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) throw new Error('Invalid email format')

      await onSave({
        name: name.trim(),
        email: email.trim(),
        identityType,
        profilePhoto
      })

      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
    } catch (err: any) {
      setError(err.message || 'Unable to save changes — try again.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-3xl mx-auto px-4">
        {/* Header */}
        <div className="mb-6">
          <button
            onClick={onBack}
            className="text-gray-600 hover:text-gray-900 mb-4 flex items-center gap-2"
          >
            ← Back to Settings
          </button>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Profile & Identity</h1>
          <p className="text-gray-600">Manage your personal information and identity type</p>
        </div>

        {/* Success Message */}
        {success && (
          <div className="mb-6 bg-green-50 border border-green-200 rounded-lg p-4 flex items-center">
            <div className="flex-1 text-green-800">✅ Changes saved successfully</div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start">
            <AlertCircle className="h-5 w-5 text-red-600 mr-3 flex-shrink-0 mt-0.5" />
            <div className="flex-1 text-red-800">{error}</div>
          </div>
        )}

        {/* Profile Photo */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Profile Photo</h2>
          <div className="flex items-center gap-6">
            <div className="relative">
              {profilePhoto ? (
                <img src={profilePhoto} alt="Profile" className="w-24 h-24 rounded-full object-cover" />
              ) : (
                <div className="w-24 h-24 rounded-full bg-dominion-gold bg-opacity-20 flex items-center justify-center">
                  <User className="h-12 w-12 text-dominion-gold" />
                </div>
              )}
              <button className="absolute bottom-0 right-0 p-2 bg-white border border-gray-300 rounded-full shadow-sm hover:bg-gray-50 transition-colors">
                <Camera className="h-4 w-4 text-gray-600" />
              </button>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-2">Upload a profile photo (optional)</p>
              <button className="text-sm text-dominion-gold hover:text-yellow-600 font-medium">
                Choose File
              </button>
            </div>
          </div>
        </div>

        {/* Personal Information */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Personal Information</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Name *
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-dominion-gold focus:border-transparent"
                placeholder="Your full name"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email *
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-dominion-gold focus:border-transparent"
                placeholder="your.email@example.com"
              />
            </div>
          </div>
        </div>

        {/* Identity Type */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">Identity Type</h2>
          <p className="text-sm text-gray-600 mb-4">
            Your identity personalizes insights, news filters, and dashboard widgets
          </p>
          <div className="grid gap-3">
            {identities.map((identity) => {
              const Icon = identity.icon
              const isSelected = identityType === identity.value
              return (
                <button
                  key={identity.value}
                  onClick={() => handleIdentityChange(identity.value)}
                  className={`text-left p-4 rounded-lg border-2 transition-all ${
                    isSelected
                      ? 'border-dominion-gold bg-yellow-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <div className={`p-2 rounded-lg ${identity.color}`}>
                      <Icon className="h-5 w-5" />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900">{identity.label}</h3>
                      <p className="text-sm text-gray-600 mt-1">{identity.description}</p>
                    </div>
                    {isSelected && (
                      <div className="text-dominion-gold text-xl">✓</div>
                    )}
                  </div>
                </button>
              )
            })}
          </div>
        </div>

        {/* CodexDominion Connection */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">CodexDominion Account</h2>
          <p className="text-sm text-gray-600 mb-4">
            Connect your CodexDominion account for seamless access across the ecosystem
          </p>
          {initialData.codexDominionConnected ? (
            <div className="flex items-center justify-between p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-center gap-3">
                <Link className="h-5 w-5 text-green-600" />
                <span className="font-medium text-green-900">Connected to CodexDominion</span>
              </div>
              <button className="text-sm text-red-600 hover:text-red-700 font-medium">
                Disconnect
              </button>
            </div>
          ) : (
            <button className="w-full px-6 py-3 bg-dominion-obsidian text-white font-semibold rounded-lg hover:bg-gray-800 transition-colors flex items-center justify-center gap-2">
              <Link className="h-5 w-5" />
              Connect CodexDominion Account
            </button>
          )}
        </div>

        {/* Save Button */}
        <div className="flex justify-end gap-3">
          <button
            onClick={onBack}
            className="px-6 py-3 border border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            disabled={saving}
            className="px-8 py-3 bg-dominion-gold text-dominion-obsidian font-semibold rounded-lg hover:bg-yellow-500 transition-colors disabled:opacity-50 flex items-center gap-2"
          >
            <Save className="h-5 w-5" />
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </div>

      {/* Identity Confirmation Modal */}
      {showIdentityConfirm && pendingIdentity && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-3">Confirm Identity Change</h3>
            <p className="text-gray-600 mb-6">
              Switching to <span className="font-semibold">{identities.find(i => i.value === pendingIdentity)?.label}</span> will update:
            </p>
            <ul className="space-y-2 mb-6 text-sm text-gray-700">
              <li>• Dashboard widgets and layout</li>
              <li>• News filters and recommendations</li>
              <li>• Insights and cross-promotions</li>
              <li>• Alert suggestions</li>
            </ul>
            <div className="flex gap-3">
              <button
                onClick={() => {
                  setShowIdentityConfirm(false)
                  setPendingIdentity(null)
                }}
                className="flex-1 px-6 py-3 border border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={confirmIdentityChange}
                className="flex-1 px-6 py-3 bg-dominion-gold text-dominion-obsidian font-semibold rounded-lg hover:bg-yellow-500 transition-colors"
              >
                Confirm
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
