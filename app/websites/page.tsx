import SiteCard from './components/SiteCard'
import DeploymentStatus from './components/DeploymentStatus'

export default function WebsitesPage() {
  const sites = [
    { id: '1', name: 'CodexDominion.app', status: 'live', visitors: 12847 },
    { id: '2', name: 'FaithEmpire.com', status: 'live', visitors: 8932 },
    { id: '3', name: 'Advent2025.com', status: 'building', visitors: 0 },
  ]

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-serif text-ceremonial mb-2">
          🌐 Website Factory
        </h1>
        <p className="text-proclamation">
          Rapid Website Generation, Deployment & Management
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="codex-card">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-serif text-codex-gold">
                Active Websites
              </h2>
              <button className="codex-button">
                ➕ Create Website
              </button>
            </div>

            <div className="space-y-4">
              {sites.map((site) => (
                <SiteCard key={site.id} site={site} />
              ))}
            </div>
          </div>
        </div>

        <div>
          <DeploymentStatus />
        </div>
      </div>
    </div>
  )
}
