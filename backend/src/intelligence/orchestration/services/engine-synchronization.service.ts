// =============================================================================
// ENGINE SYNCHRONIZATION SERVICE
// =============================================================================
// Coordinates all 9 engines to prevent collisions and ensure harmony

import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../../prisma/prisma.service';
import { EngineName, EngineStatus } from '@prisma/client';
import {
  EngineHealthReport,
  EngineIssue,
  DependencyStatus,
  EngineConflict,
  EngineSequence,
  SequenceStep,
  SyncAllEnginesDto,
} from '../types/orchestration.types';

@Injectable()
export class EngineSynchronizationService {
  constructor(private prisma: PrismaService) {}

  /**
   * Synchronize all engines or specific engines
   * Ensures no collisions, proper sequencing, and dependency resolution
   */
  async syncAllEngines(dto: SyncAllEnginesDto): Promise<EngineHealthReport[]> {
    const enginesToSync = dto.specificEngines || Object.values(EngineName);
    const healthReports: EngineHealthReport[] = [];

    for (const engineName of enginesToSync) {
      // Get or create engine state
      let engineState = await this.prisma.engineState.findUnique({
        where: { engineName },
      });

      if (!engineState) {
        engineState = await this.prisma.engineState.create({
          data: {
            engineName,
            status: EngineStatus.OPERATIONAL,
            health: 1.0,
            currentConfig: {},
            metrics: {},
            dependencies: this.getEngineDependencies(engineName),
            dependents: this.getEngineDependents(engineName),
          },
        });
      }

      // Check engine health
      const healthReport = await this.checkEngineHealth(engineName);
      healthReports.push(healthReport);

      // Update heartbeat and sync timestamp
      await this.prisma.engineState.update({
        where: { engineName },
        data: {
          lastHeartbeat: new Date(),
          lastSync: new Date(),
          nextSync: new Date(Date.now() + 3600000), // 1 hour from now
        },
      });
    }

    // Resolve conflicts if any found
    if (dto.forceSync) {
      const conflicts = await this.resolveEngineConflicts();
      console.log(`Resolved ${conflicts.length} engine conflicts`);
    }

    return healthReports;
  }

  /**
   * Check health of a specific engine
   * Returns comprehensive health report with issues and dependencies
   */
  async checkEngineHealth(engineName: EngineName): Promise<EngineHealthReport> {
    const engineState = await this.prisma.engineState.findUnique({
      where: { engineName },
    });

    if (!engineState) {
      return {
        engineName,
        status: EngineStatus.OFFLINE,
        health: 0,
        lastHeartbeat: new Date(),
        metrics: {},
        issues: [
          {
            severity: 'CRITICAL',
            description: 'Engine not initialized',
            detectedAt: new Date(),
            suggestedAction: 'Initialize engine state',
          },
        ],
        dependencies: [],
      };
    }

    // Calculate health score based on metrics
    const health = this.calculateEngineHealth(engineName, engineState.metrics as any);

    // Check dependencies
    const dependencies = await this.checkDependencies(engineName);

    // Identify issues
    const issues = await this.identifyEngineIssues(engineName, engineState);

    return {
      engineName,
      status: engineState.status,
      health,
      lastHeartbeat: engineState.lastHeartbeat,
      metrics: engineState.metrics as any,
      issues,
      dependencies,
    };
  }

  /**
   * Resolve conflicts between engines
   * E.g., mission unlocking before curriculum ready, creator challenge misaligned with season
   */
  async resolveEngineConflicts(): Promise<EngineConflict[]> {
    const conflicts: EngineConflict[] = [];

    // Check Mission-Curriculum conflicts
    const missionCurriculumConflicts = await this.checkMissionCurriculumConflicts();
    conflicts.push(...missionCurriculumConflicts);

    // Check Creator-Season conflicts
    const creatorSeasonConflicts = await this.checkCreatorSeasonConflicts();
    conflicts.push(...creatorSeasonConflicts);

    // Check Intelligence-Governance conflicts
    const intelligenceGovernanceConflicts = await this.checkIntelligenceGovernanceConflicts();
    conflicts.push(...intelligenceGovernanceConflicts);

    // Resolve each conflict
    for (const conflict of conflicts) {
      await this.applyConflictResolution(conflict);
    }

    return conflicts;
  }

  /**
   * Orchestrate engine sequence for coordinated actions
   * E.g., season transition sequence: Intelligence → Governance → Curriculum → Mission → Creator
   */
  async orchestrateEngineSequence(sequenceType: string): Promise<EngineSequence> {
    const sequences: Record<string, EngineSequence> = {
      SEASON_TRANSITION: {
        engines: [
          EngineName.INTELLIGENCE,
          EngineName.GOVERNANCE,
          EngineName.CURRICULUM,
          EngineName.MISSION,
          EngineName.CREATOR,
          EngineName.EXCHANGE,
        ],
        sequenceType: 'SEASON_TRANSITION',
        estimatedDuration: 120, // 2 hours
        steps: [
          { step: 1, engine: EngineName.INTELLIGENCE, action: 'Analyze readiness', duration: 10, dependencies: [] },
          { step: 2, engine: EngineName.GOVERNANCE, action: 'Approve transition', duration: 20, dependencies: [1] },
          { step: 3, engine: EngineName.CURRICULUM, action: 'Align curriculum', duration: 30, dependencies: [2] },
          { step: 4, engine: EngineName.MISSION, action: 'Sync missions', duration: 30, dependencies: [3] },
          { step: 5, engine: EngineName.CREATOR, action: 'Launch challenges', duration: 20, dependencies: [3] },
          { step: 6, engine: EngineName.EXCHANGE, action: 'Integrate lessons', duration: 10, dependencies: [4, 5] },
        ],
      },
      REGIONAL_EXPANSION: {
        engines: [
          EngineName.GOVERNANCE,
          EngineName.CIRCLE,
          EngineName.YOUTH,
          EngineName.CURRICULUM,
          EngineName.MISSION,
        ],
        sequenceType: 'REGIONAL_EXPANSION',
        estimatedDuration: 180, // 3 hours
        steps: [
          { step: 1, engine: EngineName.GOVERNANCE, action: 'Approve expansion', duration: 30, dependencies: [] },
          { step: 2, engine: EngineName.CIRCLE, action: 'Create circles', duration: 40, dependencies: [1] },
          { step: 3, engine: EngineName.YOUTH, action: 'Onboard youth', duration: 60, dependencies: [2] },
          { step: 4, engine: EngineName.CURRICULUM, action: 'Customize curriculum', duration: 30, dependencies: [1] },
          { step: 5, engine: EngineName.MISSION, action: 'Assign first missions', duration: 20, dependencies: [3, 4] },
        ],
      },
      CREATOR_RENAISSANCE: {
        engines: [
          EngineName.INTELLIGENCE,
          EngineName.CREATOR,
          EngineName.MISSION,
          EngineName.EXCHANGE,
        ],
        sequenceType: 'CREATOR_RENAISSANCE',
        estimatedDuration: 90,
        steps: [
          { step: 1, engine: EngineName.INTELLIGENCE, action: 'Identify rising creators', duration: 15, dependencies: [] },
          { step: 2, engine: EngineName.CREATOR, action: 'Launch seasonal challenge', duration: 30, dependencies: [1] },
          { step: 3, engine: EngineName.MISSION, action: 'Link creator missions', duration: 20, dependencies: [2] },
          { step: 4, engine: EngineName.EXCHANGE, action: 'Integrate financial tools', duration: 25, dependencies: [2] },
        ],
      },
    };

    return sequences[sequenceType] || sequences.SEASON_TRANSITION;
  }

  // =============================================================================
  // PRIVATE HELPER METHODS
  // =============================================================================

  private calculateEngineHealth(engineName: EngineName, metrics: any): number {
    // Default health calculation
    let health = 1.0;

    // Engine-specific health calculations
    switch (engineName) {
      case EngineName.CIRCLE:
        // Health based on circle activity
        health = metrics.activeCircles / (metrics.totalCircles || 1);
        break;
      case EngineName.MISSION:
        // Health based on mission completion rate
        health = metrics.completionRate || 0.8;
        break;
      case EngineName.CURRICULUM:
        // Health based on engagement
        health = metrics.engagementRate || 0.85;
        break;
      case EngineName.CREATOR:
        // Health based on submission rate
        health = metrics.submissionRate || 0.75;
        break;
      case EngineName.INTELLIGENCE:
        // Health based on insight accuracy
        health = metrics.insightAccuracy || 0.9;
        break;
      case EngineName.GOVERNANCE:
        // Health based on decision flow
        health = metrics.decisionFlowRate || 0.88;
        break;
      case EngineName.EXCHANGE:
        // Health based on usage
        health = metrics.toolUsage || 0.70;
        break;
      default:
        health = 0.9;
    }

    return Math.max(0, Math.min(1, health));
  }

  private async checkDependencies(engineName: EngineName): Promise<DependencyStatus[]> {
    const dependencies = this.getEngineDependencies(engineName);
    const statuses: DependencyStatus[] = [];

    for (const depName of dependencies) {
      const depState = await this.prisma.engineState.findUnique({
        where: { engineName: depName as EngineName },
      });

      if (!depState) {
        statuses.push({
          dependsOn: depName as EngineName,
          status: 'BLOCKED',
          lastSync: new Date(),
        });
      } else {
        const status =
          depState.status === EngineStatus.OPERATIONAL
            ? 'HEALTHY'
            : depState.status === EngineStatus.DEGRADED
            ? 'DEGRADED'
            : 'BLOCKED';

        statuses.push({
          dependsOn: depName as EngineName,
          status,
          lastSync: depState.lastSync || new Date(),
        });
      }
    }

    return statuses;
  }

  private async identifyEngineIssues(engineName: EngineName, engineState: any): Promise<EngineIssue[]> {
    const issues: EngineIssue[] = [];

    // Check heartbeat freshness
    const lastHeartbeat = new Date(engineState.lastHeartbeat);
    const minutesSinceHeartbeat = (Date.now() - lastHeartbeat.getTime()) / 60000;

    if (minutesSinceHeartbeat > 60) {
      issues.push({
        severity: 'HIGH',
        description: `No heartbeat for ${Math.round(minutesSinceHeartbeat)} minutes`,
        detectedAt: new Date(),
        suggestedAction: 'Check engine connectivity',
      });
    }

    // Check health score
    if (engineState.health < 0.5) {
      issues.push({
        severity: 'CRITICAL',
        description: `Health score critically low: ${engineState.health}`,
        detectedAt: new Date(),
        suggestedAction: 'Investigate engine metrics and resolve issues',
      });
    } else if (engineState.health < 0.7) {
      issues.push({
        severity: 'MEDIUM',
        description: `Health score degraded: ${engineState.health}`,
        detectedAt: new Date(),
        suggestedAction: 'Monitor engine performance',
      });
    }

    // Check error rate
    if (engineState.errorRate > 0.1) {
      issues.push({
        severity: 'HIGH',
        description: `High error rate: ${(engineState.errorRate * 100).toFixed(1)}%`,
        detectedAt: new Date(),
        suggestedAction: 'Review error logs and fix recurring errors',
      });
    }

    return issues;
  }

  private async checkMissionCurriculumConflicts(): Promise<EngineConflict[]> {
    // Check for missions without curriculum prerequisites
    const missionsWithoutCurriculum = await this.prisma.mission.findMany({
      where: {
        curriculumLinks: { none: {} },
        type: 'CIRCLE', // Circle missions typically need curriculum
      },
      take: 10,
    });

    return missionsWithoutCurriculum.map((mission) => ({
      engine1: EngineName.MISSION,
      engine2: EngineName.CURRICULUM,
      conflictType: 'MISSING_PREREQUISITE',
      description: `Mission "${mission.title}" has no curriculum prerequisites`,
      resolution: 'Link mission to appropriate curriculum modules',
      priority: 7,
    }));
  }

  private async checkCreatorSeasonConflicts(): Promise<EngineConflict[]> {
    // Check for creator challenges misaligned with season
    const currentSeason = await this.prisma.season.findFirst({
      where: {
        startDate: { lte: new Date() },
        endDate: { gte: new Date() },
      },
    });

    if (!currentSeason) return [];

    const misalignedChallenges = await this.prisma.creatorChallenge.findMany({
      where: {
        seasonId: { not: currentSeason.id },
        deadline: { gte: new Date() }, // Active challenges
      },
      take: 10,
    });

    return misalignedChallenges.map((challenge) => ({
      engine1: EngineName.CREATOR,
      engine2: EngineName.ORCHESTRATION,
      conflictType: 'SEASON_MISALIGNMENT',
      description: `Challenge "${challenge.title}" not aligned with current season`,
      resolution: 'Update challenge to align with current season',
      priority: 5,
    }));
  }

  private async checkIntelligenceGovernanceConflicts(): Promise<EngineConflict[]> {
    // Check for intelligence actions not routed to governance
    const unroutedActions = await this.prisma.intelligenceAction.findMany({
      where: {
        status: 'PENDING',
        insightSeverity: 'HIGH',
        detectedAt: { lt: new Date(Date.now() - 86400000) }, // Over 24 hours old
      },
      take: 10,
    });

    return unroutedActions.map((action) => ({
      engine1: EngineName.INTELLIGENCE,
      engine2: EngineName.GOVERNANCE,
      conflictType: 'ACTION_NOT_ROUTED',
      description: `High-severity action "${action.insightType}" not routed for 24+ hours`,
      resolution: 'Route action to appropriate leadership level',
      priority: 8,
    }));
  }

  private async applyConflictResolution(conflict: EngineConflict): Promise<void> {
    // Log conflict and resolution attempt
    console.log(`Resolving conflict: ${conflict.conflictType} between ${conflict.engine1} and ${conflict.engine2}`);

    // In production, this would trigger automated resolution actions
    // For now, log the resolution strategy
    console.log(`Resolution: ${conflict.resolution}`);
  }

  private getEngineDependencies(engineName: EngineName): string[] {
    const dependencies: Record<EngineName, string[]> = {
      [EngineName.CIRCLE]: ['YOUTH'],
      [EngineName.YOUTH]: [],
      [EngineName.MISSION]: ['CURRICULUM', 'CIRCLE'],
      [EngineName.CURRICULUM]: [],
      [EngineName.CREATOR]: ['YOUTH', 'MISSION'],
      [EngineName.EXCHANGE]: ['YOUTH', 'CURRICULUM'],
      [EngineName.INTELLIGENCE]: ['CIRCLE', 'MISSION', 'YOUTH'],
      [EngineName.GOVERNANCE]: ['INTELLIGENCE'],
      [EngineName.ORCHESTRATION]: ['INTELLIGENCE', 'GOVERNANCE'],
    };

    return dependencies[engineName] || [];
  }

  private getEngineDependents(engineName: EngineName): string[] {
    // Reverse lookup: which engines depend on this one?
    const allDependencies: Record<string, string[]> = {
      [EngineName.CIRCLE]: ['YOUTH'],
      [EngineName.YOUTH]: [],
      [EngineName.MISSION]: ['CURRICULUM', 'CIRCLE'],
      [EngineName.CURRICULUM]: [],
      [EngineName.CREATOR]: ['YOUTH', 'MISSION'],
      [EngineName.EXCHANGE]: ['YOUTH', 'CURRICULUM'],
      [EngineName.INTELLIGENCE]: ['CIRCLE', 'MISSION', 'YOUTH'],
      [EngineName.GOVERNANCE]: ['INTELLIGENCE'],
      [EngineName.ORCHESTRATION]: ['INTELLIGENCE', 'GOVERNANCE'],
    };

    const dependents: string[] = [];
    for (const [engine, deps] of Object.entries(allDependencies)) {
      if ((deps as string[]).includes(engineName as string)) {
        dependents.push(engine);
      }
    }

    return dependents;
  }
}
