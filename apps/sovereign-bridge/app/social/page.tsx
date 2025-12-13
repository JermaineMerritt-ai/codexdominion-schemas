'use client'

import { useState } from 'react'
import ChannelOverview from './components/ChannelOverview'
import ContentCalendar from './components/ContentCalendar'
import RepurposingPanel from './components/RepurposingPanel'
import NewCampaignModal from './components/NewCampaignModal'

export default function SocialPage() {
  const [showNewCampaignModal, setShowNewCampaignModal] = useState(false)

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-ceremonial">📱 Social Media Hub</h1>
        <button
          onClick={() => setShowNewCampaignModal(true)}
          className="codex-button"
        >
          ✨ New Campaign
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <ChannelOverview />
          <ContentCalendar />
        </div>

        <div className="space-y-6">
          <RepurposingPanel />
        </div>
      </div>

      <NewCampaignModal
        isOpen={showNewCampaignModal}
        onClose={() => setShowNewCampaignModal(false)}
      />
    </div>
  )
}
