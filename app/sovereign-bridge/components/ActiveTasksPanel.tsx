'use client'

import { useEffect, useState } from 'react'

interface Task {
  id: string
  name: string
  status: 'running' | 'queued' | 'completed' | 'failed'
  progress: number
  startedAt: string
}

export default function ActiveTasksPanel() {
  const [tasks, setTasks] = useState<Task[]>([])

  useEffect(() => {
    // Mock active tasks
    const mockTasks: Task[] = [
      { id: '1', name: 'Advent Devotional Generation', status: 'completed', progress: 100, startedAt: '2 min ago' },
      { id: '2', name: 'Ritual Health Monitor', status: 'completed', progress: 100, startedAt: '5 min ago' },
      { id: '3', name: 'Dawn Dispatch Preparation', status: 'queued', progress: 0, startedAt: 'Scheduled for 5:00 AM' },
      { id: '4', name: 'Treasury Audit', status: 'queued', progress: 0, startedAt: 'Scheduled for Monday 8:00 AM' },
    ]
    setTasks(mockTasks)
  }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'bg-blue-500/20 text-blue-400 border-blue-500/30'
      case 'queued': return 'bg-gray-500/20 text-gray-400 border-gray-500/30'
      case 'completed': return 'bg-green-500/20 text-green-400 border-green-500/30'
      case 'failed': return 'bg-red-500/20 text-red-400 border-red-500/30'
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/30'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running': return '⚙️'
      case 'queued': return '⏳'
      case 'completed': return '✅'
      case 'failed': return '❌'
      default: return '❓'
    }
  }

  return (
    <div className="codex-card">
      <h2 className="text-2xl font-serif text-codex-gold mb-6">
        Active Tasks & Executions
      </h2>

      <div className="space-y-4">
        {tasks.map((task) => (
          <div key={task.id} className="codex-panel hover:bg-codex-navy/90 transition-all">
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center space-x-3">
                <span className="text-2xl">{getStatusIcon(task.status)}</span>
                <div>
                  <h3 className="font-semibold">{task.name}</h3>
                  <p className="text-xs text-codex-parchment/60">{task.startedAt}</p>
                </div>
              </div>
              <span className={`codex-badge ${getStatusColor(task.status)}`}>
                {task.status.toUpperCase()}
              </span>
            </div>

            {task.status === 'running' && (
              <div className="w-full bg-codex-navy/50 rounded-full h-2">
                <div
                  className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${task.progress}%` }}
                ></div>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="mt-6 pt-6 border-t border-codex-gold/20 flex justify-between items-center">
        <span className="text-sm text-codex-parchment/70">Total Tasks Today</span>
        <span className="text-lg font-semibold text-codex-gold">{tasks.length}</span>
      </div>
    </div>
  )
}
