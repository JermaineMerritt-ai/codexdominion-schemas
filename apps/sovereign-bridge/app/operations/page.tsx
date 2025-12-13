import EngineMonitor from './components/EngineMonitor'
import TaskQueue from './components/TaskQueue'
import ProjectList from './components/ProjectList'
import SystemMetrics from './components/SystemMetrics'

export default function OperationsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-ceremonial">⚙️ Operations Center</h1>
      </div>

      <SystemMetrics />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <EngineMonitor />
          <TaskQueue />
        </div>

        <div className="space-y-6">
          <ProjectList />
        </div>
      </div>
    </div>
  )
}
