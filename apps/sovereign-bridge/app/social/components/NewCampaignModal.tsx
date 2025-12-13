'use client'

import { useState } from 'react'
import { Modal } from '@/components'

interface NewCampaignModalProps {
  isOpen: boolean
  onClose: () => void
}

export default function NewCampaignModal({ isOpen, onClose }: NewCampaignModalProps) {
  const [campaignName, setCampaignName] = useState('')
  const [campaignType, setCampaignType] = useState('product-launch')
  const [platforms, setPlatforms] = useState<string[]>([])
  const [duration, setDuration] = useState(7)

  const handleCreate = () => {
    console.log('Creating campaign:', { campaignName, campaignType, platforms, duration })
    onClose()
  }

  const availablePlatforms = [
    { id: 'instagram', name: 'Instagram', icon: '📸' },
    { id: 'facebook', name: 'Facebook', icon: '👥' },
    { id: 'pinterest', name: 'Pinterest', icon: '📌' },
    { id: 'youtube', name: 'YouTube', icon: '🎥' },
    { id: 'tiktok', name: 'TikTok', icon: '🎵' },
    { id: 'twitter', name: 'Twitter', icon: '🐦' },
  ]

  const togglePlatform = (platformId: string) => {
    setPlatforms(prev =>
      prev.includes(platformId)
        ? prev.filter(p => p !== platformId)
        : [...prev, platformId]
    )
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Create New Campaign">
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-codex-parchment mb-2">
            Campaign Name
          </label>
          <input
            type="text"
            value={campaignName}
            onChange={(e) => setCampaignName(e.target.value)}
            placeholder="Enter campaign name..."
            className="w-full px-3 py-2 bg-codex-navy/30 border border-codex-gold/30 rounded text-codex-parchment"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-codex-parchment mb-2">
            Campaign Type
          </label>
          <select
            value={campaignType}
            onChange={(e) => setCampaignType(e.target.value)}
            className="w-full px-3 py-2 bg-codex-navy/30 border border-codex-gold/30 rounded text-codex-parchment"
          >
            <option value="product-launch">Product Launch</option>
            <option value="seasonal">Seasonal Promotion</option>
            <option value="brand-awareness">Brand Awareness</option>
            <option value="engagement">Engagement Campaign</option>
            <option value="educational">Educational Series</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-codex-parchment mb-2">
            Select Platforms
          </label>
          <div className="grid grid-cols-3 gap-2">
            {availablePlatforms.map((platform) => (
              <button
                key={platform.id}
                onClick={() => togglePlatform(platform.id)}
                className={`p-3 rounded border transition-colors ${
                  platforms.includes(platform.id)
                    ? 'bg-codex-gold/20 border-codex-gold'
                    : 'bg-codex-navy/30 border-codex-gold/30'
                }`}
              >
                <div className="text-2xl mb-1">{platform.icon}</div>
                <div className="text-xs text-codex-parchment">{platform.name}</div>
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-codex-parchment mb-2">
            Campaign Duration (days)
          </label>
          <input
            type="number"
            value={duration}
            onChange={(e) => setDuration(parseInt(e.target.value))}
            min="1"
            max="90"
            className="w-full px-3 py-2 bg-codex-navy/30 border border-codex-gold/30 rounded text-codex-parchment"
          />
        </div>
      </div>

      <div className="flex gap-3 mt-6">
        <button onClick={onClose} className="codex-button flex-1">
          Cancel
        </button>
        <button onClick={handleCreate} className="codex-button flex-1 bg-codex-gold text-codex-navy">
          Create Campaign
        </button>
      </div>
    </Modal>
  )
}
