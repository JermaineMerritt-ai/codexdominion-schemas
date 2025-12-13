import FlowList from './components/FlowList'
import RitualScheduler from './components/RitualScheduler'

export default function AutomationsPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-serif text-ceremonial mb-2">
          ⚡ Automation & Rituals
        </h1>
        <p className="text-proclamation">
          Workflow Orchestration, Scheduled Tasks & System Rituals
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <FlowList />
        </div>

        <div>
          <RitualScheduler />
        </div>
      </div>
    </div>
  )
}
