import AffiliateProgramList from './components/AffiliateProgramList'
import LinkPerformance from './components/LinkPerformance'
import MarketContentPanel from './components/MarketContentPanel'

export default function AffiliatePage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-ceremonial">🤝 Affiliate Network</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <AffiliateProgramList />
          <LinkPerformance />
        </div>

        <div className="space-y-6">
          <MarketContentPanel />
        </div>
      </div>
    </div>
  )
}
