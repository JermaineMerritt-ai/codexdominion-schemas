import FlowList from './components/FlowList'
import FlowEditor from './components/FlowEditor'
import RitualScheduler from './components/RitualScheduler'
import TriggerPanel from './components/TriggerPanel'

export default function AutomationsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-ceremonial">⚡ Automation & Rituals</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <FlowList />
          <FlowEditor />
        </div>

        <div className="space-y-6">
          <RitualScheduler />
          <TriggerPanel />
        </div>
      </div>
    </div>
  )
}
