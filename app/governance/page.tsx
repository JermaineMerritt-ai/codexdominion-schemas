import PolicyDashboard from './components/PolicyDashboard'
import SafetyDashboard from './components/SafetyDashboard'
import AuditLog from './components/AuditLog'

export default function GovernancePage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-serif text-ceremonial mb-2">
          👁️ Governance & Oversight
        </h1>
        <p className="text-proclamation">
          Council Seal Authority • Policy Management, Safety & Compliance
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <PolicyDashboard />
          <AuditLog />
        </div>

        <div>
          <SafetyDashboard />
        </div>
      </div>
    </div>
  )
}
