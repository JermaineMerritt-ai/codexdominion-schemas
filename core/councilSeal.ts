/**
 * 👑 COUNCIL SEAL - Supreme Governance Authority
 * 
 * The highest authority in the Codex Dominion architecture.
 * Manages strategic direction, policy enforcement, and system-wide oversight.
 */

import { CouncilSeal, Policy, AuditLog, Alert, SystemStatus } from '../packages/shared-types/src';

export class CouncilSealAuthority {
  private static instance: CouncilSealAuthority;
  private config: CouncilSeal;
  private auditLogs: AuditLog[] = [];
  private alerts: Alert[] = [];
  private emergencyMode: boolean = false;

  private constructor() {
    this.config = {
      id: 'council-seal-supreme',
      name: 'Council Seal Supreme Authority',
      authority: 'SUPREME',
      permissions: [
        'APPROVE_DEPLOYMENT',
        'MODIFY_POLICY',
        'ACCESS_ALL_DATA',
        'EMERGENCY_SHUTDOWN',
        'AUDIT_ALL',
        'ALLOCATE_RESOURCES',
        'OVERRIDE_ALL'
      ],
      policies: [
        {
          id: 'security-policy-001',
          name: 'Data Security & Privacy',
          rules: [
            { condition: 'data.classification === "sensitive"', action: 'ENCRYPT', severity: 'critical' },
            { condition: 'access.unauthorized === true', action: 'DENY', severity: 'critical' },
            { condition: 'audit.enabled === false', action: 'ALERT', severity: 'high' }
          ],
          enforcement: 'STRICT',
          scope: 'GLOBAL',
          active: true
        },
        {
          id: 'compliance-policy-002',
          name: 'Regulatory Compliance',
          rules: [
            { condition: 'data.pii === true', action: 'AUDIT', severity: 'high' },
            { condition: 'deployment.environment === "production"', action: 'REQUIRE_APPROVAL', severity: 'high' },
            { condition: 'change.breaking === true', action: 'REQUIRE_REVIEW', severity: 'medium' }
          ],
          enforcement: 'STRICT',
          scope: 'GLOBAL',
          active: true
        },
        {
          id: 'operational-policy-003',
          name: 'Operational Excellence',
          rules: [
            { condition: 'performance.threshold > 90', action: 'ALERT', severity: 'medium' },
            { condition: 'cost.budget > allocated', action: 'NOTIFY', severity: 'medium' },
            { condition: 'availability < 99.9', action: 'ESCALATE', severity: 'high' }
          ],
          enforcement: 'ADVISORY',
          scope: 'GLOBAL',
          active: true
        }
      ],
      monitoring: {
        enabled: true,
        interval: 60000, // 1 minute
        metrics: ['performance', 'security', 'compliance', 'cost', 'availability'],
        alertThresholds: {
          critical: 95,
          high: 80,
          medium: 60,
          low: 40
        }
      }
    };
  }

  /**
   * Get singleton instance of Council Seal Authority
   */
  public static getInstance(): CouncilSealAuthority {
    if (!CouncilSealAuthority.instance) {
      CouncilSealAuthority.instance = new CouncilSealAuthority();
    }
    return CouncilSealAuthority.instance;
  }

  /**
   * Enforce a policy across the system
   */
  public enforcePolicy(policyId: string, context: Record<string, any>): {
    allowed: boolean;
    actions: string[];
    violations: string[];
  } {
    const policy = this.config.policies.find(p => p.id === policyId);
    
    if (!policy || !policy.active) {
      return { allowed: true, actions: [], violations: [] };
    }

    const actions: string[] = [];
    const violations: string[] = [];
    let allowed = true;

    for (const rule of policy.rules) {
      if (this.evaluateRule(rule.condition, context)) {
        actions.push(rule.action);
        
        if (rule.action === 'DENY' || rule.action === 'BLOCK') {
          allowed = false;
          violations.push(`Policy ${policy.name}: ${rule.condition}`);
        }

        // Log enforcement action
        this.audit({
          timestamp: new Date(),
          actor: 'CouncilSeal',
          action: `POLICY_ENFORCEMENT: ${rule.action}`,
          resource: policyId,
          status: 'SUCCESS',
          severity: rule.severity,
          metadata: context
        });
      }
    }

    return { allowed, actions, violations };
  }

  /**
   * Evaluate a rule condition against context
   */
  private evaluateRule(condition: string, context: Record<string, any>): boolean {
    try {
      // Simple evaluation - in production, use a proper rule engine
      const func = new Function('data', 'access', 'audit', 'performance', 'cost', 'availability', 'deployment', 'change', 
        `return ${condition};`);
      return func(
        context.data,
        context.access,
        context.audit,
        context.performance,
        context.cost,
        context.availability,
        context.deployment,
        context.change
      );
    } catch (error) {
      console.error('Rule evaluation error:', error);
      return false;
    }
  }

  /**
   * Create audit log entry
   */
  public audit(log: AuditLog): void {
    this.auditLogs.push(log);

    // Maintain audit log size
    if (this.auditLogs.length > 10000) {
      this.auditLogs = this.auditLogs.slice(-10000);
    }

    // Create alert for high-severity events
    if (log.severity === 'critical' || log.severity === 'high') {
      this.createAlert({
        id: `alert-${Date.now()}`,
        timestamp: new Date(),
        severity: log.severity,
        message: `${log.action} on ${log.resource}`,
        source: log.actor,
        resolved: false
      });
    }
  }

  /**
   * Create system alert
   */
  private createAlert(alert: Alert): void {
    this.alerts.push(alert);
    
    // Auto-escalate critical alerts
    if (alert.severity === 'critical') {
      console.error('🚨 CRITICAL ALERT:', alert.message);
      // In production: send to monitoring system, page on-call
    }
  }

  /**
   * Approve a change request (deployment, policy change, etc.)
   */
  public approveChange(changeRequest: {
    id: string;
    type: 'DEPLOYMENT' | 'POLICY' | 'CONFIGURATION' | 'EMERGENCY';
    description: string;
    requestor: string;
    context: Record<string, any>;
  }): { approved: boolean; reason: string } {
    // Check if emergency mode
    if (this.emergencyMode && changeRequest.type !== 'EMERGENCY') {
      return {
        approved: false,
        reason: 'System in emergency mode - only emergency changes allowed'
      };
    }

    // Enforce policies
    const policyCheck = this.enforcePolicy('compliance-policy-002', {
      deployment: { environment: changeRequest.context.environment },
      change: { breaking: changeRequest.context.breaking || false }
    });

    if (!policyCheck.allowed) {
      return {
        approved: false,
        reason: `Policy violations: ${policyCheck.violations.join(', ')}`
      };
    }

    // Log approval
    this.audit({
      timestamp: new Date(),
      actor: 'CouncilSeal',
      action: 'APPROVE_CHANGE',
      resource: changeRequest.id,
      status: 'SUCCESS',
      severity: changeRequest.type === 'EMERGENCY' ? 'critical' : 'medium',
      metadata: changeRequest
    });

    return {
      approved: true,
      reason: 'Change approved by Council Seal'
    };
  }

  /**
   * Initiate emergency mode
   */
  public initiateEmergency(reason: string): void {
    this.emergencyMode = true;
    
    this.audit({
      timestamp: new Date(),
      actor: 'CouncilSeal',
      action: 'EMERGENCY_MODE_ACTIVATED',
      resource: 'SYSTEM',
      status: 'SUCCESS',
      severity: 'critical',
      metadata: { reason }
    });

    this.createAlert({
      id: `emergency-${Date.now()}`,
      timestamp: new Date(),
      severity: 'critical',
      message: `Emergency mode activated: ${reason}`,
      source: 'CouncilSeal',
      resolved: false
    });
  }

  /**
   * Deactivate emergency mode
   */
  public deactivateEmergency(): void {
    this.emergencyMode = false;
    
    this.audit({
      timestamp: new Date(),
      actor: 'CouncilSeal',
      action: 'EMERGENCY_MODE_DEACTIVATED',
      resource: 'SYSTEM',
      status: 'SUCCESS',
      severity: 'high',
      metadata: {}
    });
  }

  /**
   * Get system status
   */
  public getSystemStatus(): SystemStatus {
    const recentLogs = this.auditLogs.slice(-100);
    const unresolvedAlerts = this.alerts.filter(a => !a.resolved);

    return {
      healthy: !this.emergencyMode && unresolvedAlerts.filter(a => a.severity === 'critical').length === 0,
      lastCheck: new Date(),
      services: {
        councilSeal: 'OPERATIONAL',
        sovereigns: 'OPERATIONAL',
        custodians: 'OPERATIONAL',
        agents: 'OPERATIONAL'
      },
      metrics: {
        totalAuditLogs: this.auditLogs.length,
        recentErrors: recentLogs.filter(l => l.status === 'FAILURE').length,
        activeAlerts: unresolvedAlerts.length,
        criticalAlerts: unresolvedAlerts.filter(a => a.severity === 'critical').length,
        emergencyMode: this.emergencyMode
      },
      alerts: unresolvedAlerts.slice(0, 10) // Most recent 10
    };
  }

  /**
   * Get audit logs (filtered)
   */
  public getAuditLogs(filter?: {
    actor?: string;
    action?: string;
    severity?: 'low' | 'medium' | 'high' | 'critical';
    limit?: number;
  }): AuditLog[] {
    let logs = [...this.auditLogs];

    if (filter?.actor) {
      logs = logs.filter(l => l.actor === filter.actor);
    }
    if (filter?.action) {
      logs = logs.filter(l => l.action.includes(filter.action));
    }
    if (filter?.severity) {
      logs = logs.filter(l => l.severity === filter.severity);
    }

    return logs.slice(-(filter?.limit || 100));
  }

  /**
   * Get Council Seal configuration
   */
  public getConfig(): CouncilSeal {
    return { ...this.config };
  }

  /**
   * Update policy
   */
  public updatePolicy(policyId: string, updates: Partial<Policy>): { success: boolean; message: string } {
    const policyIndex = this.config.policies.findIndex(p => p.id === policyId);
    
    if (policyIndex === -1) {
      return { success: false, message: 'Policy not found' };
    }

    this.config.policies[policyIndex] = {
      ...this.config.policies[policyIndex],
      ...updates
    };

    this.audit({
      timestamp: new Date(),
      actor: 'CouncilSeal',
      action: 'POLICY_UPDATED',
      resource: policyId,
      status: 'SUCCESS',
      severity: 'high',
      metadata: updates
    });

    return { success: true, message: 'Policy updated successfully' };
  }

  /**
   * Allocate resources to sovereigns/custodians
   */
  public allocateResources(allocation: {
    target: string;
    type: 'COMPUTE' | 'STORAGE' | 'NETWORK' | 'BUDGET';
    amount: number;
    reason: string;
  }): { approved: boolean; message: string } {
    // In production: check availability, budget, policies
    this.audit({
      timestamp: new Date(),
      actor: 'CouncilSeal',
      action: 'RESOURCE_ALLOCATION',
      resource: allocation.target,
      status: 'SUCCESS',
      severity: 'medium',
      metadata: allocation
    });

    return {
      approved: true,
      message: `Allocated ${allocation.amount} ${allocation.type} to ${allocation.target}`
    };
  }
}

// Export singleton instance
export const councilSeal = CouncilSealAuthority.getInstance();
