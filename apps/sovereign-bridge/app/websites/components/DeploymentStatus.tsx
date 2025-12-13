'use client'

import { DashboardTile, StatusBadge } from '@/components'

export default function DeploymentStatus() {
  const deployments = [
    { platform: 'Azure', status: 'success' as const, time: '2h ago' },
    { platform: 'GCP', status: 'success' as const, time: '5h ago' },
    { platform: 'IONOS', status: 'success' as const, time: '1d ago' },
  ]

  return (
    <DashboardTile title="Recent Deployments" icon="🚀">
      <div className="space-y-3">
        {deployments.map((deploy, idx) => (
          <div key={idx} className="codex-panel flex items-center justify-between">
            <div className="flex-1">
              <div className="text-sm font-medium text-codex-parchment">{deploy.platform}</div>
              <div className="text-xs text-codex-parchment/60 mt-1">{deploy.time}</div>
            </div>
            <StatusBadge status={deploy.status} />
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
