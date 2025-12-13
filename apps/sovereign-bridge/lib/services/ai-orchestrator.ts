import type { AgentCommand, CommandResponse, Task, Project } from '@/types/ai-orchestration'

export class AIOrchestrator {
  /**
   * Process an agent command and create appropriate tasks/projects
   */
  async processCommand(command: AgentCommand): Promise<CommandResponse> {
    try {
      // Extract command details
      const { agent, mode, prompt, targets, context } = command

      // Parse targets
      const realm = this.extractRealm(targets)
      const documents = context.documentIds || []

      // Determine action based on prompt
      if (prompt.toLowerCase().includes('create') && prompt.toLowerCase().includes('video')) {
        return await this.createVideoProject(prompt, documents, realm, agent)
      }

      // Default response for unknown commands
      return {
        success: false,
        message: 'Unknown command type',
      }
    } catch (error) {
      return {
        success: false,
        message: error instanceof Error ? error.message : 'Command processing failed',
      }
    }
  }

  /**
   * Create a video project from documents
   */
  private async createVideoProject(
    prompt: string,
    documentIds: string[],
    realm: string,
    agentId: string
  ): Promise<CommandResponse> {
    // Generate project ID
    const projectId = `video_${Date.now()}`
    const taskId = `task_${Date.now()}`

    // Create project (in real implementation, save to database)
    const project: Partial<Project> = {
      id: projectId,
      type: 'video',
      title: this.extractTitle(prompt, documentIds),
      status: 'pending',
      description: `Generated from: ${documentIds.join(', ')}`,
      ownerId: 'system',
      realm: realm || 'video_studio',
      data: {
        sourceDocuments: documentIds,
        script: null,
        scenes: [],
        settings: {
          aspectRatio: '16:9',
          platform: 'YouTube',
        },
      },
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    }

    // Create task for script generation
    const task: Partial<Task> = {
      id: taskId,
      type: 'doc_creation',
      engineId: 'narrative_engine',
      status: 'pending',
      progress: 0,
      aiAgentId: agentId,
      realm: realm || 'video_studio',
      input: {
        projectId,
        documentIds,
        outputFormat: 'script',
      },
      output: null,
      error: null,
      createdAt: new Date().toISOString(),
      startedAt: null,
      finishedAt: null,
    }

    // In real implementation, save to database and trigger background processing
    console.log('Created project:', project)
    console.log('Created task:', task)

    return {
      success: true,
      taskId,
      projectId,
      message: `Video project created successfully. Task ${taskId} is processing.`,
      data: { project, task },
    }
  }

  /**
   * Extract realm from targets array
   */
  private extractRealm(targets: string[]): string {
    const realmTarget = targets.find((t) => t.startsWith('realm:'))
    return realmTarget?.replace('realm:', '') || 'default'
  }

  /**
   * Extract title from prompt and documents
   */
  private extractTitle(prompt: string, documentIds: string[]): string {
    // Try to extract from document ID
    if (documentIds.length > 0) {
      const docName = documentIds[0]
        .replace(/_/g, ' ')
        .replace(/\b\w/g, (l) => l.toUpperCase())
      return `${docName} – Episode 1`
    }

    // Fallback to generic title
    return 'New Video Project'
  }
}

// Singleton instance
export const aiOrchestrator = new AIOrchestrator()
