'use client'

import { Table, StatusBadge } from '@/components'

interface Task {
  id: string
  name: string
  status: 'active' | 'pending' | 'success' | 'error'
  started: string
  duration: string
}

interface EngineTasksProps {
  engineId?: string
}

export default function EngineTasks({ engineId }: EngineTasksProps) {
  const tasks: Task[] = [
    { id: '1', name: 'Process Content', status: 'active', started: '2 min ago', duration: '2m 15s' },
    { id: '2', name: 'Generate Output', status: 'success', started: '5 min ago', duration: '1m 30s' },
    { id: '3', name: 'Validate Data', status: 'success', started: '8 min ago', duration: '45s' },
    { id: '4', name: 'Sync State', status: 'pending', started: 'Scheduled', duration: '-' },
    { id: '5', name: 'Cleanup Cache', status: 'success', started: '15 min ago', duration: '30s' },
  ]

  return (
    <Table
      columns={[
        { key: 'name', header: 'Task Name', sortable: true },
        {
          key: 'status',
          header: 'Status',
          render: (task) => <StatusBadge status={task.status} pulse={task.status === 'active'} />
        },
        { key: 'started', header: 'Started' },
        { key: 'duration', header: 'Duration' },
      ]}
      data={tasks}
      onRowClick={(task) => console.log('Task clicked:', task.name)}
    />
  )
}
