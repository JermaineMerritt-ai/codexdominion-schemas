import SystemHealthConstellation from './components/SystemHealthConstellation'
import ActiveTasksPanel from './components/ActiveTasksPanel'
import RitualsPanel from './components/RitualsPanel'
import RevenueImpactPanel from './components/RevenueImpactPanel'
import QuickActionsDock from './components/QuickActionsDock'
import LiveEventsStrip from './components/LiveEventsStrip'

export default function SovereignBridgePage() {
  return (
    <div className="container mx-auto px-4 py-8 space-y-6">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-serif text-ceremonial mb-2">
          ⚡ Sovereign Bridge
        </h1>
        <p className="text-proclamation">
          Council Seal Command Center • Real-time Orchestration & System Overview
        </p>
      </div>

      {/* Live Events Strip */}
      <LiveEventsStrip />

      {/* Main Dashboard Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - System Health */}
        <div className="lg:col-span-2 space-y-6">
          <SystemHealthConstellation />
          <ActiveTasksPanel />
        </div>

        {/* Right Column - Rituals & Revenue */}
        <div className="space-y-6">
          <RitualsPanel />
          <RevenueImpactPanel />
        </div>
      </div>

      {/* Quick Actions Dock */}
      <QuickActionsDock />
    </div>
  )
}
