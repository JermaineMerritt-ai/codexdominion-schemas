import ChannelOverview from './components/ChannelOverview'
import ContentCalendar from './components/ContentCalendar'
import RepurposingPanel from './components/RepurposingPanel'

export default function SocialPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-serif text-ceremonial mb-2">
          📱 Social Media Hub
        </h1>
        <p className="text-proclamation">
          Multi-Platform Posting, Scheduling & Content Repurposing
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <ChannelOverview />
          <ContentCalendar />
        </div>

        <div>
          <RepurposingPanel />
        </div>
      </div>
    </div>
  )
}
