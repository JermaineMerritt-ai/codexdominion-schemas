import PolicyDashboard from './components/PolicyDashboard'
import SafetyDashboard from './components/SafetyDashboard'
import AuditLog from './components/AuditLog'
import IncidentPanel from './components/IncidentPanel'

export default function GovernancePage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-ceremonial">👁️ Governance & Oversight</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <PolicyDashboard />
          <AuditLog />
        </div>

        <div className="space-y-6">
          <SafetyDashboard />
          <IncidentPanel />
        </div>
      </div>
    </div>
  )
}
