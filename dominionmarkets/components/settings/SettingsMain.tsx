/**
 * Settings Main Screen
 * ====================
 * Control center for DominionMarkets
 */

"use client"

import { useState } from 'react'
import { User, Bell, CreditCard, Shield, Database, Sliders, HelpCircle, ChevronRight } from 'lucide-react'

interface SettingsMainProps {
  userTier: string
  identityType: string
}

export default function SettingsMain({ userTier, identityType }: SettingsMainProps) {
  const [activeCategory, setActiveCategory] = useState<string | null>(null)

  const categories = [
    {
      id: 'profile',
      label: 'Profile & Identity',
      description: 'Manage personal information and identity type',
      icon: User,
      color: 'text-blue-600 bg-blue-100'
    },
    {
      id: 'notifications',
      label: 'Notifications',
      description: 'Control alerts and app notifications',
      icon: Bell,
      color: 'text-yellow-600 bg-yellow-100'
    },
    {
      id: 'billing',
      label: 'Billing & Subscription',
      description: 'Manage Premium and Pro subscriptions',
      icon: CreditCard,
      color: 'text-green-600 bg-green-100'
    },
    {
      id: 'security',
      label: 'Security & Login',
      description: 'Manage account security',
      icon: Shield,
      color: 'text-red-600 bg-red-100'
    },
    {
      id: 'privacy',
      label: 'Data & Privacy',
      description: 'Control your data and privacy settings',
      icon: Database,
      color: 'text-purple-600 bg-purple-100'
    },
    {
      id: 'preferences',
      label: 'App Preferences',
      description: 'Customize the app experience',
      icon: Sliders,
      color: 'text-indigo-600 bg-indigo-100'
    },
    {
      id: 'support',
      label: 'Help & Support',
      description: 'Get help and contact support',
      icon: HelpCircle,
      color: 'text-gray-600 bg-gray-100'
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Settings</h1>
          <p className="text-gray-600">
            Manage your account, preferences, and subscription
          </p>
        </div>

        {/* User Info Bar */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-dominion-gold bg-opacity-20 flex items-center justify-center">
                <User className="h-6 w-6 text-dominion-gold" />
              </div>
              <div>
                <p className="font-semibold text-gray-900">Your Account</p>
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-gray-600">
                    {identityType.charAt(0).toUpperCase() + identityType.slice(1)}
                  </span>
                  <span className="text-gray-400">•</span>
                  <span className="px-2 py-0.5 bg-dominion-gold bg-opacity-20 text-dominion-gold text-xs font-semibold rounded">
                    {userTier === 'free' ? 'Free' : userTier === 'premium' ? 'Premium' : 'Pro'}
                  </span>
                </div>
              </div>
            </div>
            {userTier === 'free' && (
              <button className="px-4 py-2 bg-dominion-gold text-dominion-obsidian font-semibold rounded-lg hover:bg-yellow-500 transition-colors text-sm">
                Upgrade
              </button>
            )}
          </div>
        </div>

        {/* Categories Grid */}
        <div className="space-y-3">
          {categories.map((category) => {
            const Icon = category.icon
            return (
              <button
                key={category.id}
                onClick={() => setActiveCategory(category.id)}
                className="w-full bg-white rounded-lg shadow-sm border border-gray-200 p-5 hover:shadow-md transition-all text-left group"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4 flex-1">
                    <div className={`p-3 rounded-lg ${category.color}`}>
                      <Icon className="h-6 w-6" />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900 mb-1">
                        {category.label}
                      </h3>
                      <p className="text-sm text-gray-600">
                        {category.description}
                      </p>
                    </div>
                  </div>
                  <ChevronRight className="h-5 w-5 text-gray-400 group-hover:text-gray-600 transition-colors" />
                </div>
              </button>
            )
          })}
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>DominionMarkets v1.0.0</p>
          <p className="mt-1">
            <a href="/terms" className="hover:text-dominion-gold transition-colors">Terms</a>
            {' • '}
            <a href="/privacy" className="hover:text-dominion-gold transition-colors">Privacy</a>
            {' • '}
            <a href="/docs" className="hover:text-dominion-gold transition-colors">Documentation</a>
          </p>
        </div>
      </div>
    </div>
  )
}
