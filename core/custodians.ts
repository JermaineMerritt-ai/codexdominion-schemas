/**
 * 🛡️ CUSTODIANS - Infrastructure & Shared Services Layer
 *
 * Custodian packages provide shared libraries, utilities, and infrastructure services.
 * Maintains code quality, manages dependencies, ensures consistency across sovereigns.
 */

import { randomUUID } from 'crypto';
import { councilSeal } from './councilSeal';

export interface Custodian {
  name: string;
  focus: "finance" | "security" | "innovation" | "community";
  responsibilities: string[];
}

export interface CustodianConfig extends Custodian {
  id: string;
  type: 'LIBRARY' | 'SERVICE' | 'UTILITY' | 'FRAMEWORK' | 'SCHEMA';
  version: string;
  status: 'ACTIVE' | 'DEPRECATED' | 'UPDATING' | 'INACTIVE';
  dependencies?: string[];
  exports?: any;
  metrics: {
    performance?: number;
    reliability?: number;
    coverage?: number;
    lastUpdated: Date;
    usageCount: number;
    issues?: number;
  };
}

export class CustodianService {
  private custodians: Map<string, CustodianConfig> = new Map();

  constructor() {
    this.initializeCustodians();
  }

  /**
   * Initialize all custodian packages
   */
  private initializeCustodians(): void {
    const custodianPackages: CustodianConfig[] = [
      {
        id: 'custodian-ui',
        name: 'UI Component Library',
        focus: 'innovation',
        responsibilities: ['ui-components', 'design-system', 'theming'],
        type: 'LIBRARY',
        status: 'ACTIVE',
        version: '2.0.0',
        dependencies: ['react@18.2.0', 'tailwindcss@3.4.0', 'framer-motion@11.0.0'],
        exports: {
          components: ['Button', 'Card', 'Modal', 'Form', 'Table', 'Chart', 'Avatar', 'Badge', 'Toast'],
          hooks: ['useTheme', 'useAuth', 'useModal', 'useToast', 'useForm'],
          utils: ['cn', 'formatDate', 'formatCurrency']
        },
        metrics: {
          usageCount: 4, // Used by all 4 sovereigns
          lastUpdated: new Date('2025-11-15'),
          performance: 98,
          issues: 0
        }
      },
      {
        id: 'custodian-utils',
        name: 'Common Utilities',
        focus: 'innovation',
        responsibilities: ['shared-utilities', 'helper-functions', 'validation'],
        type: 'UTILITY',
        status: 'ACTIVE',
        version: '2.0.0',
        dependencies: ['lodash@4.17.21', 'dayjs@1.11.10', 'zod@3.22.4'],
        exports: {
          functions: [
            'generateId',
            'validateEmail',
            'validatePhone',
            'sanitizeInput',
            'debounce',
            'throttle',
            'retry',
            'timeout',
            'parseJWT',
            'encryptData',
            'decryptData',
            'hashPassword',
            'comparePassword'
          ],
          constants: ['API_ENDPOINTS', 'ERROR_CODES', 'STATUS_CODES', 'REGEX_PATTERNS'],
          types: ['Result', 'Option', 'AsyncResult', 'ValidationError']
        },
        metrics: {
          usageCount: 4,
          lastUpdated: new Date('2025-11-20'),
          performance: 99,
          issues: 0
        }
      },
      {
        id: 'custodian-schemas',
        name: 'Data Schemas & Validation',
        focus: 'security',
        responsibilities: ['data-validation', 'schema-management', 'type-safety'],
        type: 'SCHEMA',
        status: 'ACTIVE',
        version: '2.0.0',
        dependencies: ['zod@3.22.4', 'ajv@8.12.0'],
        exports: {
          schemas: [
            'UserSchema',
            'ProductSchema',
            'OrderSchema',
            'PaymentSchema',
            'AuditLogSchema',
            'MetricSchema',
            'AlertSchema',
            'ConfigSchema'
          ],
          validators: [
            'validateUser',
            'validateProduct',
            'validateOrder',
            'validatePayment',
            'validateConfig'
          ],
          types: ['User', 'Product', 'Order', 'Payment', 'Config']
        },
        metrics: {
          usageCount: 4,
          lastUpdated: new Date('2025-11-25'),
          performance: 100,
          issues: 0
        }
      },
      {
        id: 'custodian-healing',
        name: 'Self-Healing Infrastructure',
        focus: 'security',
        responsibilities: ['health-monitoring', 'auto-recovery', 'resilience'],
        type: 'SERVICE',
        status: 'ACTIVE',
        version: '2.0.0',
        dependencies: ['@opentelemetry/api@1.7.0', 'prom-client@15.1.0'],
        exports: {
          services: [
            'HealthCheckService',
            'AutoScalingService',
            'CircuitBreakerService',
            'RetryService',
            'CacheInvalidationService'
          ],
          monitors: [
            'PerformanceMonitor',
            'ErrorMonitor',
            'ResourceMonitor',
            'DependencyMonitor'
          ],
          healers: [
            'RestartHealer',
            'ScaleHealer',
            'CacheHealer',
            'ConfigHealer'
          ]
        },
        metrics: {
          usageCount: 3,
          lastUpdated: new Date('2025-11-28'),
          performance: 97,
          issues: 0
        }
      }
    ];

    custodianPackages.forEach(custodian => {
      this.custodians.set(custodian.id, custodian);
    });

    console.log(`✅ Initialized ${custodianPackages.length} Custodian packages`);
  }

  /**
   * Get custodian by ID
   */
  public getCustodian(id: string): CustodianConfig | undefined {
    return this.custodians.get(id);
  }

  /**
   * Get all custodians
   */
  public getAllCustodians(): CustodianConfig[] {
    return Array.from(this.custodians.values());
  }

  /**
   * Get custodians by type
   */
  public getCustodiansByType(type: 'LIBRARY' | 'UTILITY' | 'SERVICE' | 'FRAMEWORK'): CustodianConfig[] {
    return Array.from(this.custodians.values()).filter(c => c.type === type);
  }

  /**
   * Update custodian package
   */
  public async updateCustodian(
    custodianId: string,
    newVersion: string,
    changelog: string
  ): Promise<{ success: boolean; message: string }> {
    const custodian = this.custodians.get(custodianId);

    if (!custodian) {
      return { success: false, message: 'Custodian not found' };
    }

    // Check for breaking changes
    const isBreaking = this.isBreakingChange(custodian.version, newVersion);

    // Request approval from Council Seal
    const approval = councilSeal.approveChange({
      id: `update-${custodianId}-${newVersion}`,
      type: 'DEPLOYMENT',
      description: `Update ${custodian.name} from ${custodian.version} to ${newVersion}`,
      requestor: custodianId,
      context: {
        environment: 'production',
        breaking: isBreaking
      }
    });

    if (!approval.approved) {
      return {
        success: false,
        message: `Update denied by Council Seal: ${approval.reason}`
      };
    }

    // Update custodian
    custodian.version = newVersion;
    custodian.metrics.lastUpdated = new Date();
    custodian.status = 'UPDATING';
    this.custodians.set(custodianId, custodian);

    // Log update
    councilSeal.audit({
      id: randomUUID(),
      timestamp: new Date(),
      actor: 'CustodianService',
      action: 'UPDATE_PACKAGE',
      resource: custodianId,
      status: 'SUCCESS',
      severity: isBreaking ? 'HIGH' : 'MEDIUM',
      metadata: { oldVersion: custodian.version, newVersion, changelog }
    });

    // Simulate update completion
    setTimeout(() => {
      custodian.status = 'ACTIVE';
      this.custodians.set(custodianId, custodian);
    }, 1000);

    return {
      success: true,
      message: `Successfully updated ${custodian.name} to version ${newVersion}`
    };
  }

  /**
   * Check if version change is breaking
   */
  private isBreakingChange(oldVersion: string, newVersion: string): boolean {
    const [oldMajor] = oldVersion.split('.').map(Number);
    const [newMajor] = newVersion.split('.').map(Number);
    return newMajor > oldMajor;
  }

  /**
   * Get package dependencies
   */
  public getDependencies(custodianId: string): {
    direct: string[];
    dependents: string[];
  } {
    const custodian = this.custodians.get(custodianId);

    if (!custodian) {
      return { direct: [], dependents: [] };
    }

    // Get direct dependencies
    const direct = custodian.dependencies || [];

    // Get dependents (other custodians that depend on this one)
    const dependents = Array.from(this.custodians.values())
      .filter(c => c.dependencies?.some(dep => dep.startsWith(custodianId)))
      .map(c => c.id);

    return { direct, dependents };
  }

  /**
   * Run health check on custodian
   */
  public runHealthCheck(custodianId: string): {
    healthy: boolean;
    issues: string[];
    performance: number;
  } {
    const custodian = this.custodians.get(custodianId);

    if (!custodian) {
      return { healthy: false, issues: ['Custodian not found'], performance: 0 };
    }

    const issues: string[] = [];

    // Check status
    if (custodian.status !== 'ACTIVE') {
      issues.push(`Status is ${custodian.status}, expected ACTIVE`);
    }

    // Check performance
    if ((custodian.metrics.performance ?? 100) < 80) {
      issues.push(`Performance is ${custodian.metrics.performance}%, below threshold`);
    }

    // Check for unresolved issues
    if ((custodian.metrics.issues ?? 0) > 0) {
      issues.push(`${custodian.metrics.issues} unresolved issues`);
    }

    // Check last update (warn if > 90 days)
    const daysSinceUpdate = Math.floor(
      (Date.now() - custodian.metrics.lastUpdated.getTime()) / (1000 * 60 * 60 * 24)
    );
    if (daysSinceUpdate > 90) {
      issues.push(`Last updated ${daysSinceUpdate} days ago`);
    }

    return {
      healthy: issues.length === 0,
      issues,
      performance: custodian.metrics.performance ?? 100
    };
  }

  /**
   * Get usage statistics
   */
  public getUsageStats(): {
    mostUsed: Custodian;
    leastUsed: Custodian;
    averagePerformance: number;
    totalIssues: number;
  } {
    const custodians = Array.from(this.custodians.values());

    const sorted = [...custodians].sort((a, b) => b.metrics.usageCount - a.metrics.usageCount);

    return {
      mostUsed: sorted[0],
      leastUsed: sorted[sorted.length - 1],
      averagePerformance: custodians.reduce((sum, c) => sum + (c.metrics.performance || 0), 0) / custodians.length,
      totalIssues: custodians.reduce((sum, c) => sum + (c.metrics.issues || 0), 0)
    };
  }

  /**
   * Export custodian for use by sovereigns/agents
   */
  public exportCustodian(custodianId: string): {
    success: boolean;
    exports?: Record<string, any>;
    message: string;
  } {
    const custodian = this.custodians.get(custodianId);

    if (!custodian) {
      return { success: false, message: 'Custodian not found' };
    }

    if (custodian.status !== 'ACTIVE') {
      return { success: false, message: `Custodian is ${custodian.status}, not ACTIVE` };
    }

    // Log export
    councilSeal.audit({
      id: randomUUID(),
      timestamp: new Date(),
      actor: 'CustodianService',
      action: 'EXPORT_PACKAGE',
      resource: custodianId,
      status: 'SUCCESS',
      severity: 'LOW',
      metadata: {}
    });

    return {
      success: true,
      exports: custodian.exports,
      message: `Successfully exported ${custodian.name}`
    };
  }

  /**
   * Get system-wide package health
   */
  public getSystemHealth(): {
    healthy: number;
    degraded: number;
    unhealthy: number;
    averagePerformance: number;
  } {
    const custodians = Array.from(this.custodians.values());

    const healthChecks = custodians.map(c => this.runHealthCheck(c.id));

    return {
      healthy: healthChecks.filter(h => h.healthy).length,
      degraded: healthChecks.filter(h => !h.healthy && h.performance > 50).length,
      unhealthy: healthChecks.filter(h => !h.healthy && h.performance <= 50).length,
      averagePerformance: healthChecks.reduce((sum, h) => sum + h.performance, 0) / healthChecks.length
    };
  }
}

// Export singleton instance
export const custodianService = new CustodianService();
