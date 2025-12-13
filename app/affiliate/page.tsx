import AffiliateProgramList from './components/AffiliateProgramList'
import LinkPerformance from './components/LinkPerformance'
import MarketContentPanel from './components/MarketContentPanel'

export default function AffiliatePage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-serif text-ceremonial mb-2">
          🤝 Affiliate Network
        </h1>
        <p className="text-proclamation">
          Affiliate Program Management, Link Tracking & Revenue Analytics
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <AffiliateProgramList />
          <LinkPerformance />
        </div>

        <div>
          <MarketContentPanel />
        </div>
      </div>
    </div>
  )
}
