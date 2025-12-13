// AI Orchestration System Types

export type TaskStatus = 'pending' | 'active' | 'success' | 'failed' | 'cancelled'
export type EngineCategory = 'core' | 'specialized'
export type ProjectType = 'video' | 'audio' | 'document' | 'image'
export type AgentMode = 'build' | 'analyze' | 'optimize' | 'monitor'

// Engine Definition
export interface Engine {
  id: string
  name: string
  category: EngineCategory
  status: 'active' | 'inactive' | 'pending'
  description: string
  metrics: {
    requests24h: number
    errorRate: number
    avgLatencyMs: number
  }
  lastHeartbeatAt: string
  createdAt: string
  updatedAt: string
}

// Task Definition
export interface Task {
  id: string
  type: string
  engineId: string
  status: TaskStatus
  progress: number
  aiAgentId: string
  realm: string
  input: Record<string, any>
  output: any | null
  error: string | null
  createdAt: string
  startedAt: string | null
  finishedAt: string | null
}

// Project Definition
export interface Project {
  id: string
  type: ProjectType
  title: string
  status: TaskStatus
  description: string
  ownerId: string
  realm: string
  data: Record<string, any>
  createdAt: string
  updatedAt: string
}

// Agent Command
export interface AgentCommand {
  agent: string
  mode: AgentMode
  prompt: string
  targets: string[]
  context: {
    documentIds?: string[]
    taskId?: string | null
    projectId?: string | null
    [key: string]: any
  }
}

// Action Definition
export interface Action {
  type: string
  target: string
  title?: string
  description?: string
  requires?: string[]
  sourceDocument?: string
  [key: string]: any
}

// Action Batch
export interface ActionBatch {
  actions: Action[]
}

// Command Response
export interface CommandResponse {
  success: boolean
  taskId?: string
  projectId?: string
  message: string
  data?: any
}
