'use client'

import { DashboardTile, StatusBadge } from '@/components'

interface Task {
  id: string
  type: string
  engineId: string
  status: 'pending' | 'active' | 'success'
  progress: number
  aiAgent: string
  realm: string
  createdAt: string
}

export default function TaskQueue() {
  const tasks: Task[] = [
    {
      id: 'task_123',
      type: 'doc_creation',
      engineId: 'narrative_engine',
      status: 'active',
      progress: 60,
      aiAgent: 'super_action_ai',
      realm: 'video_studio',
      createdAt: '2 min ago'
    },
    {
      id: 'task_124',
      type: 'script_generation',
      engineId: 'narrative_engine',
      status: 'active',
      progress: 85,
      aiAgent: 'super_action_ai',
      realm: 'video_studio',
      createdAt: '5 min ago'
    },
    {
      id: 'task_125',
      type: 'visual_prompt',
      engineId: 'visual_engine',
      status: 'pending',
      progress: 0,
      aiAgent: 'visual_ai',
      realm: 'video_studio',
      createdAt: '1 min ago'
    },
    {
      id: 'task_126',
      type: 'audio_processing',
      engineId: 'audio_engine',
      status: 'success',
      progress: 100,
      aiAgent: 'audio_ai',
      realm: 'audio_studio',
      createdAt: '8 min ago'
    },
  ] as const

  const getStatusColor = (progress: number) => {
    if (progress === 100) return 'bg-green-500'
    if (progress > 50) return 'bg-blue-500'
    if (progress > 0) return 'bg-yellow-500'
    return 'bg-gray-500'
  }

  return (
    <DashboardTile title="Task Queue" icon="📋" action={{ label: "📊 All Tasks", onClick: () => {} }}>
      <div className="space-y-3">
        {tasks.map((task) => (
          <div key={task.id} className="codex-panel hover:bg-codex-gold/10 cursor-pointer">
            <div className="flex items-start justify-between mb-2">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold text-sm text-codex-parchment">{task.type}</span>
                  <StatusBadge status={task.status} />
                </div>
                <p className="text-xs text-codex-parchment/60">
                  {task.aiAgent} • {task.realm} • {task.createdAt}
                </p>
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="text-codex-parchment/70">Progress</span>
                <span className="font-bold text-codex-gold">{task.progress}%</span>
              </div>
              <div className="w-full bg-codex-navy/50 rounded-full h-1.5">
                <div
                  className={`h-1.5 rounded-full transition-all ${getStatusColor(task.progress)}`}
                  style={{ width: `${task.progress}%` }}
                />
              </div>
            </div>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
