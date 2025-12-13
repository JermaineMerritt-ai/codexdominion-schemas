'use client'

export default function DeploymentStatus() {
  const deployments = [
    { platform: 'Azure', status: 'success', time: '2h ago' },
    { platform: 'GCP', status: 'success', time: '5h ago' },
    { platform: 'IONOS', status: 'success', time: '1d ago' },
  ]

  return (
    <div className="codex-card">
      <h2 className="text-xl font-serif text-codex-gold mb-4">
        🚀 Recent Deployments
      </h2>

      <div className="space-y-3">
        {deployments.map((deploy, idx) => (
          <div key={idx} className="codex-panel border-l-2 border-green-500">
            <div className="flex items-center justify-between">
              <span className="font-semibold text-sm">{deploy.platform}</span>
              <span className="codex-badge-success">{deploy.status}</span>
            </div>
            <p className="text-xs text-codex-parchment/60 mt-1">{deploy.time}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
