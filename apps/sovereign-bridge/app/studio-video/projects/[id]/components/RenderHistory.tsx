'use client'

import { DashboardTile, Table, StatusBadge } from '@/components'

interface RenderRecord {
  id: string
  timestamp: string
  resolution: string
  duration: string
  status: 'success' | 'error'
  size: string
}

interface RenderHistoryProps {
  projectId: string
}

export default function RenderHistory({ projectId }: RenderHistoryProps) {
  const renders: RenderRecord[] = [
    { id: '1', timestamp: '2 hours ago', resolution: '1080p', duration: '45s', status: 'success', size: '12.3 MB' },
    { id: '2', timestamp: '1 day ago', resolution: '1080p', duration: '45s', status: 'success', size: '11.8 MB' },
    { id: '3', timestamp: '2 days ago', resolution: '720p', duration: '42s', status: 'success', size: '7.2 MB' },
    { id: '4', timestamp: '3 days ago', resolution: '1080p', duration: '40s', status: 'error', size: '-' },
  ]

  return (
    <DashboardTile title="Render History" icon="🎬">
      <Table
        columns={[
          { key: 'timestamp', header: 'Time' },
          { key: 'resolution', header: 'Resolution' },
          { key: 'duration', header: 'Duration' },
          {
            key: 'status',
            header: 'Status',
            render: (record) => <StatusBadge status={record?.status || 'pending'} />
          },
          { key: 'size', header: 'Size' },
        ]}
        data={renders}
      />
    </DashboardTile>
  )
}
