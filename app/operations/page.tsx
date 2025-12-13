export default function OperationsPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-serif text-ceremonial mb-2">
          ⚙️ Operations Center
        </h1>
        <p className="text-proclamation">
          System Operations, Deployment Pipelines & Infrastructure Management
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Deployment Status */}
        <div className="codex-card">
          <h2 className="text-xl font-serif text-codex-gold mb-4">
            🚀 Deployment Status
          </h2>
          <div className="space-y-3">
            <div className="codex-panel border-l-2 border-green-500">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-sm">Azure Static Web App</span>
                <span className="codex-badge-success">LIVE</span>
              </div>
              <p className="text-xs text-codex-parchment/60 mt-1">Last deploy: 2 hours ago</p>
            </div>
            <div className="codex-panel border-l-2 border-green-500">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-sm">GCP Cloud Run</span>
                <span className="codex-badge-success">LIVE</span>
              </div>
              <p className="text-xs text-codex-parchment/60 mt-1">Last deploy: 5 hours ago</p>
            </div>
            <div className="codex-panel border-l-2 border-green-500">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-sm">IONOS VPS</span>
                <span className="codex-badge-success">LIVE</span>
              </div>
              <p className="text-xs text-codex-parchment/60 mt-1">Last deploy: 1 day ago</p>
            </div>
          </div>
        </div>

        {/* Infrastructure Health */}
        <div className="codex-card">
          <h2 className="text-xl font-serif text-codex-gold mb-4">
            🏗️ Infrastructure Health
          </h2>
          <div className="space-y-3">
            <div className="codex-panel">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm">Docker Containers</span>
                <span className="font-bold text-green-400">3/3</span>
              </div>
              <div className="w-full bg-codex-navy/50 rounded-full h-2">
                <div className="bg-green-500 h-2 rounded-full" style={{ width: '100%' }}></div>
              </div>
            </div>
            <div className="codex-panel">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm">GitHub Workflows</span>
                <span className="font-bold text-green-400">41 active</span>
              </div>
              <div className="w-full bg-codex-navy/50 rounded-full h-2">
                <div className="bg-green-500 h-2 rounded-full" style={{ width: '100%' }}></div>
              </div>
            </div>
            <div className="codex-panel">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm">System Services</span>
                <span className="font-bold text-green-400">7/7</span>
              </div>
              <div className="w-full bg-codex-navy/50 rounded-full h-2">
                <div className="bg-green-500 h-2 rounded-full" style={{ width: '100%' }}></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="codex-card mt-6">
        <h2 className="text-xl font-serif text-codex-gold mb-4">
          ⚡ Quick Operations
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button className="codex-button">🚀 Deploy Frontend</button>
          <button className="codex-button">📦 Deploy Backend</button>
          <button className="codex-button">🔄 Restart Services</button>
          <button className="codex-button">📊 View Logs</button>
        </div>
      </div>
    </div>
  )
}
