/**
 * 🔄 FLOWS - Data & Communication Flow Orchestration
 *
 * Manages data flow patterns and communication between layers:
 * - Primary Flow: Council Seal → Sovereigns → Custodians → Agents → Customers
 * - Feedback Loop: Customers → Agents → Custodians → Sovereigns → Council Seal
 */

import { randomUUID } from 'crypto';
import { Message, Event } from '../packages/shared-types/src';
import { councilSeal } from './councilSeal';
import { sovereignService } from './sovereigns';
import { custodianService } from './custodians';

export type FlowDirection = 'DOWNSTREAM' | 'UPSTREAM' | 'LATERAL';
export type FlowType = 'REQUEST' | 'RESPONSE' | 'EVENT' | 'COMMAND' | 'NOTIFICATION';

export interface Flow {
  id: string;
  type: FlowType;
  direction: FlowDirection;
  source: string;
  target: string;
  payload: any;
  timestamp: Date;
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'FAILED';
  metadata?: Record<string, any>;
}

export class FlowOrchestrator {
  private flows: Map<string, Flow> = new Map();
  private flowHistory: Flow[] = [];

  /**
   * Initialize a new flow
   */
  public initiateFlow(
    type: FlowType,
    source: string,
    target: string,
    payload: any,
    metadata?: Record<string, any>
  ): Flow {
    const direction = this.determineDirection(source, target);

    const flow: Flow = {
      id: `flow-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      type,
      direction,
      source,
      target,
      payload,
      timestamp: new Date(),
      status: 'PENDING',
      metadata
    };

    this.flows.set(flow.id, flow);

    // Log flow initiation
    councilSeal.audit({
      id: randomUUID(),
      timestamp: new Date(),
      actor: source,
      action: 'FLOW_INITIATED',
      resource: target,
      status: 'SUCCESS',
      severity: 'LOW',
      metadata: { flowId: flow.id, type, direction }
    });

    return flow;
  }

  /**
   * Determine flow direction based on source and target
   */
  private determineDirection(source: string, target: string): FlowDirection {
    const hierarchy = ['council', 'sovereign', 'custodian', 'agent', 'customer'];

    const sourceLevel = hierarchy.findIndex(level => source.toLowerCase().includes(level));
    const targetLevel = hierarchy.findIndex(level => target.toLowerCase().includes(level));

    if (sourceLevel < targetLevel) return 'DOWNSTREAM';
    if (sourceLevel > targetLevel) return 'UPSTREAM';
    return 'LATERAL';
  }

  /**
   * Execute a flow
   */
  public async executeFlow(flowId: string): Promise<{
    success: boolean;
    result?: any;
    error?: string;
  }> {
    const flow = this.flows.get(flowId);

    if (!flow) {
      return { success: false, error: 'Flow not found' };
    }

    flow.status = 'IN_PROGRESS';
    this.flows.set(flowId, flow);

    try {
      let result: any;

      // Route flow based on direction and type
      switch (flow.direction) {
        case 'DOWNSTREAM':
          result = await this.executeDownstreamFlow(flow);
          break;
        case 'UPSTREAM':
          result = await this.executeUpstreamFlow(flow);
          break;
        case 'LATERAL':
          result = await this.executeLateralFlow(flow);
          break;
      }

      flow.status = 'COMPLETED';
      this.flows.set(flowId, flow);
      this.flowHistory.push({ ...flow });

      return { success: true, result };
    } catch (error) {
      flow.status = 'FAILED';
      this.flows.set(flowId, flow);

      councilSeal.audit({
        id: randomUUID(),
        timestamp: new Date(),
        actor: flow.source,
        action: 'FLOW_FAILED',
        resource: flow.target,
        status: 'FAILURE',
        severity: 'HIGH',
        metadata: { flowId, error: (error as Error).message }
      });

      return { success: false, error: (error as Error).message };
    }
  }

  /**
   * Execute downstream flow (top-down: Council → Sovereign → Custodian → Agent → Customer)
   */
  private async executeDownstreamFlow(flow: Flow): Promise<any> {
    switch (flow.type) {
      case 'COMMAND':
        return this.executeCommand(flow);
      case 'REQUEST':
        return this.executeRequest(flow);
      case 'EVENT':
        return this.broadcastEvent(flow);
      default:
        throw new Error(`Unsupported downstream flow type: ${flow.type}`);
    }
  }

  /**
   * Execute upstream flow (bottom-up: Customer → Agent → Custodian → Sovereign → Council)
   */
  private async executeUpstreamFlow(flow: Flow): Promise<any> {
    switch (flow.type) {
      case 'RESPONSE':
        return this.deliverResponse(flow);
      case 'NOTIFICATION':
        return this.escalateNotification(flow);
      case 'EVENT':
        return this.bubbleEvent(flow);
      default:
        throw new Error(`Unsupported upstream flow type: ${flow.type}`);
    }
  }

  /**
   * Execute lateral flow (peer-to-peer: Sovereign ↔ Sovereign, Agent ↔ Agent)
   */
  private async executeLateralFlow(flow: Flow): Promise<any> {
    // Lateral flows typically require coordination
    if (flow.source.includes('sovereign')) {
      return this.coordinateSovereigns(flow);
    } else if (flow.source.includes('agent')) {
      return this.coordinateAgents(flow);
    }

    throw new Error('Unsupported lateral flow');
  }

  /**
   * Execute command (Council Seal directive)
   */
  private async executeCommand(flow: Flow): Promise<any> {
    const { command, parameters } = flow.payload;

    // Commands must come from Council Seal
    if (!flow.source.includes('council')) {
      throw new Error('Commands can only originate from Council Seal');
    }

    councilSeal.audit({
      id: randomUUID(),
      timestamp: new Date(),
      actor: flow.source,
      action: `COMMAND_EXECUTED: ${command}`,
      resource: flow.target,
      status: 'SUCCESS',
      severity: 'HIGH',
      metadata: parameters
    });

    return { command, status: 'executed', target: flow.target };
  }

  /**
   * Execute request
   */
  private async executeRequest(flow: Flow): Promise<any> {
    // Simulate request processing
    await this.delay(100);

    return {
      requestId: flow.id,
      status: 'processed',
      data: flow.payload,
      timestamp: new Date()
    };
  }

  /**
   * Broadcast event downstream
   */
  private async broadcastEvent(flow: Flow): Promise<any> {
    const event: any = {
      id: flow.id,
      type: (flow.payload.type as any) || 'CUSTOM',
      timestamp: new Date(),
      source: flow.source,
      target: flow.target,
      data: flow.payload,
      priority: flow.metadata?.priority || 'medium'
    };

    // Broadcast to all relevant components
    if (flow.target === 'ALL_SOVEREIGNS') {
      sovereignService.getAllSovereigns().forEach(sovereign => {
        sovereignService.handleEvent(event);
      });
    }

    return { broadcast: true, recipients: flow.target };
  }

  /**
   * Deliver response upstream
   */
  private async deliverResponse(flow: Flow): Promise<any> {
    return {
      responseId: flow.id,
      delivered: true,
      target: flow.target,
      timestamp: new Date()
    };
  }

  /**
   * Escalate notification upstream
   */
  private async escalateNotification(flow: Flow): Promise<any> {
    const { severity, message } = flow.payload;

    // High severity notifications go to Council Seal
    if (severity === 'critical' || severity === 'high') {
      councilSeal.audit({
        id: randomUUID(),
        timestamp: new Date(),
        actor: flow.source,
        action: 'ESCALATION',
        resource: flow.target,
        status: 'SUCCESS',
        severity: (severity === 'critical' ? 'CRITICAL' : 'HIGH') as 'CRITICAL' | 'HIGH',
        metadata: { message }
      });
    }

    return { escalated: true, severity, target: flow.target };
  }

  /**
   * Bubble event upstream
   */
  private async bubbleEvent(flow: Flow): Promise<any> {
    // Events bubble up through the hierarchy
    return {
      eventId: flow.id,
      bubbled: true,
      source: flow.source,
      target: flow.target
    };
  }

  /**
   * Coordinate between sovereigns
   */
  private async coordinateSovereigns(flow: Flow): Promise<any> {
    const message: any = {
      id: flow.id,
      from: flow.source,
      to: flow.target,
      type: 'COORDINATION',
      content: flow.payload,
      timestamp: new Date(),
      priority: flow.metadata?.priority || 'medium'
    };

    return sovereignService.sendMessage(message);
  }

  /**
   * Coordinate between agents
   */
  private async coordinateAgents(flow: Flow): Promise<any> {
    // Agent coordination logic
    return {
      coordinated: true,
      agents: [flow.source, flow.target]
    };
  }

  /**
   * Get flow status
   */
  public getFlow(flowId: string): Flow | undefined {
    return this.flows.get(flowId);
  }

  /**
   * Get recent flows
   */
  public getRecentFlows(limit: number = 50): Flow[] {
    return this.flowHistory.slice(-limit);
  }

  /**
   * Get flows by type
   */
  public getFlowsByType(type: FlowType): Flow[] {
    return this.flowHistory.filter(f => f.type === type);
  }

  /**
   * Get flows by direction
   */
  public getFlowsByDirection(direction: FlowDirection): Flow[] {
    return this.flowHistory.filter(f => f.direction === direction);
  }

  /**
   * Get flow metrics
   */
  public getFlowMetrics(): {
    total: number;
    completed: number;
    failed: number;
    pending: number;
    averageDuration: number;
    byType: Record<FlowType, number>;
    byDirection: Record<FlowDirection, number>;
  } {
    const flows = Array.from(this.flows.values());

    const byType = flows.reduce((acc, flow) => {
      acc[flow.type] = (acc[flow.type] || 0) + 1;
      return acc;
    }, {} as Record<FlowType, number>);

    const byDirection = flows.reduce((acc, flow) => {
      acc[flow.direction] = (acc[flow.direction] || 0) + 1;
      return acc;
    }, {} as Record<FlowDirection, number>);

    return {
      total: flows.length,
      completed: flows.filter(f => f.status === 'COMPLETED').length,
      failed: flows.filter(f => f.status === 'FAILED').length,
      pending: flows.filter(f => f.status === 'PENDING').length,
      averageDuration: 0, // Would calculate from timestamps
      byType,
      byDirection
    };
  }

  /**
   * Clear completed flows (housekeeping)
   */
  public clearCompletedFlows(): number {
    const before = this.flows.size;

    Array.from(this.flows.entries()).forEach(([id, flow]) => {
      if (flow.status === 'COMPLETED') {
        this.flows.delete(id);
      }
    });

    return before - this.flows.size;
  }

  /**
   * Utility: delay
   */
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Export singleton instance
export const flowOrchestrator = new FlowOrchestrator();

/**
 * Convenience functions for common flow patterns
 */
export const FlowPatterns = {
  /**
   * Council Seal issues command to Sovereign
   */
  councilToSovereign: (command: string, sovereignId: string, parameters: any) => {
    const flow = flowOrchestrator.initiateFlow(
      'COMMAND',
      'council-seal-supreme',
      sovereignId,
      { command, parameters }
    );
    return flowOrchestrator.executeFlow(flow.id);
  },

  /**
   * Customer sends request through Agent to Sovereign
   */
  customerRequest: (customerId: string, agentId: string, request: any) => {
    const flow = flowOrchestrator.initiateFlow(
      'REQUEST',
      customerId,
      agentId,
      request
    );
    return flowOrchestrator.executeFlow(flow.id);
  },

  /**
   * Agent escalates issue to Sovereign
   */
  escalateToSovereign: (agentId: string, sovereignId: string, issue: any) => {
    const flow = flowOrchestrator.initiateFlow(
      'NOTIFICATION',
      agentId,
      sovereignId,
      { severity: 'high', ...issue }
    );
    return flowOrchestrator.executeFlow(flow.id);
  },

  /**
   * Broadcast system-wide event
   */
  systemBroadcast: (eventType: string, payload: any) => {
    const flow = flowOrchestrator.initiateFlow(
      'EVENT',
      'council-seal-supreme',
      'ALL_SOVEREIGNS',
      { type: eventType, ...payload }
    );
    return flowOrchestrator.executeFlow(flow.id);
  }
};
