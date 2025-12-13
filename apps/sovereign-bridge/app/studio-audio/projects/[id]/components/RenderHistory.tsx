'use client'

import { DashboardTile, Table, StatusBadge } from '@/components'

interface RenderRecord {
  id: string
  timestamp: string
  format: string
  duration: string
  status: 'success' | 'error'
  size: string
}

interface RenderHistoryProps {
  projectId: string
}

export default function RenderHistory({ projectId }: RenderHistoryProps) {
  const renders: RenderRecord[] = [
    { id: '1', timestamp: '1 hour ago', format: 'MP3 320kbps', duration: '3:45', status: 'success', size: '8.5 MB' },
    { id: '2', timestamp: '5 hours ago', format: 'WAV 48kHz', duration: '3:42', status: 'success', size: '42.3 MB' },
    { id: '3', timestamp: '1 day ago', format: 'MP3 192kbps', duration: '3:40', status: 'success', size: '5.2 MB' },
    { id: '4', timestamp: '2 days ago', format: 'AAC 256kbps', duration: '3:38', status: 'error', size: '-' },
  ]

  return (
    <DashboardTile title="Render History" icon="🎧">
      <Table
        columns={[
          { key: 'timestamp', header: 'Time' },
          { key: 'format', header: 'Format' },
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
