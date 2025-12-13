import { NextRequest, NextResponse } from 'next/server'
import type { AgentCommand } from '@codex/shared-types'

/**
 * POST /api/agent-commands
 * Process AI agent commands
 * Deployed to Azure Static Web Apps
 */
export async function POST(request: NextRequest) {
  try {
    const command = await request.json() as AgentCommand

    // Validate command
    if (!command.agent || !command.mode || !command.prompt) {
      return NextResponse.json(
        { success: false, message: 'Invalid command format' },
        { status: 400 }
      )
    }

    // Extract command details
    const { agent, mode, prompt, targets, context } = command
    const realm = targets.find((t) => t.startsWith('realm:'))?.replace('realm:', '') || 'default'
    const documents = context.documentIds || []

    // Generate IDs
    const projectId = `video_${Date.now()}`
    const taskId = `task_${Date.now()}`

    // Mock response - in real implementation, this would create DB records
    const response = {
      success: true,
      taskId,
      projectId,
      message: `Video project created successfully. Task ${taskId} is processing.`,
      data: {
        project: {
          id: projectId,
          type: 'video',
          title: documents[0]?.replace(/_/g, ' ') || 'New Video Project',
          status: 'pending',
          realm,
        },
        task: {
          id: taskId,
          type: 'doc_creation',
          engineId: 'narrative_engine',
          status: 'pending',
          progress: 0,
          aiAgentId: agent,
        },
      },
    }

    return NextResponse.json(response)
  } catch (error) {
    console.error('Agent command error:', error)
    return NextResponse.json(
      {
        success: false,
        message: error instanceof Error ? error.message : 'Internal server error',
      },
      { status: 500 }
    )
  }
}

/**
 * GET /api/agent-commands
 * Get command status or list recent commands
 */
export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const taskId = searchParams.get('taskId')

  if (taskId) {
    return NextResponse.json({
      success: true,
      task: {
        id: taskId,
        status: 'active',
        progress: 60,
        message: 'Processing...',
      },
    })
  }

  return NextResponse.json({
    success: true,
    commands: [],
  })
}
