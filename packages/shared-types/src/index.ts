/**
 * 🏛️ Council Seal - Supreme Governance Authority
 * 
 * The Council Seal represents the highest authority in the Codex Dominion
 * architecture. It oversees all system operations, enforces policies,
 * and maintains the integrity of the entire digital empire.
 */

export interface CouncilSeal {
  id: string;
  authority: 'SUPREME';
  status: 'ACTIVE' | 'SEALED' | 'EMERGENCY';
  permissions: CouncilPermissions;
  policies: GovernancePolicy[];
  monitoring: SystemMonitoring;
}

export interface CouncilPermissions {
  canApproveChanges: boolean;
  canOverrideSecurity: boolean;
  canAccessAllSystems: boolean;
  canModifyPolicies: boolean;
  canInitiateEmergency: boolean;
}

export interface GovernancePolicy {
  id: string;
  name: string;
  type: 'SECURITY' | 'COMPLIANCE' | 'OPERATIONAL' | 'STRATEGIC';
  rules: PolicyRule[];
  enforcementLevel: 'STRICT' | 'MODERATE' | 'ADVISORY';
  createdAt: Date;
  lastUpdated: Date;
}

export interface PolicyRule {
  id: string;
  description: string;
  condition: string;
  action: 'ALLOW' | 'DENY' | 'REVIEW' | 'ESCALATE';
  parameters: Record<string, any>;
}

export interface SystemMonitoring {
  health: SystemHealth;
  metrics: SystemMetrics;
  alerts: Alert[];
  auditLog: AuditEntry[];
}

export interface SystemHealth {
  overall: 'HEALTHY' | 'DEGRADED' | 'CRITICAL';
  sovereigns: ComponentHealth;
  custodians: ComponentHealth;
  agents: ComponentHealth;
  customers: ComponentHealth;
}

export interface ComponentHealth {
  status: 'OPERATIONAL' | 'DEGRADED' | 'DOWN';
  uptime: number;
  lastCheck: Date;
  issues: string[];
}

export interface SystemMetrics {
  requestsPerSecond: number;
  averageResponseTime: number;
  errorRate: number;
  activeUsers: number;
  resourceUtilization: ResourceUtilization;
}

export interface ResourceUtilization {
  cpu: number;
  memory: number;
  disk: number;
  network: number;
}

export interface Alert {
  id: string;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'INFO';
  type: 'SECURITY' | 'PERFORMANCE' | 'AVAILABILITY' | 'COMPLIANCE';
  message: string;
  timestamp: Date;
  acknowledged: boolean;
  resolvedAt?: Date;
}

export interface AuditEntry {
  id: string;
  timestamp: Date;
  actor: string;
  action: string;
  resource: string;
  result: 'SUCCESS' | 'FAILURE' | 'DENIED';
  metadata: Record<string, any>;
}

/**
 * Sovereign (Application Layer) Types
 */
export interface Sovereign {
  id: string;
  name: string;
  type: 'FRONTEND' | 'API' | 'DASHBOARD' | 'EXECUTOR';
  status: 'ACTIVE' | 'INACTIVE' | 'MAINTENANCE';
  dependencies: string[];
  endpoints: Endpoint[];
  configuration: SovereignConfig;
}

export interface SovereignConfig {
  port: number;
  environment: 'development' | 'staging' | 'production';
  features: Record<string, boolean>;
  secrets: Record<string, string>;
}

export interface Endpoint {
  path: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  handler: string;
  authentication: boolean;
  rateLimit?: RateLimit;
}

export interface RateLimit {
  requests: number;
  window: number; // seconds
  burst: number;
}

/**
 * Custodian (Infrastructure Layer) Types
 */
export interface Custodian {
  id: string;
  name: string;
  type: 'LIBRARY' | 'UTILITY' | 'CLIENT' | 'SERVICE';
  version: string;
  exports: string[];
  dependencies: Dependency[];
}

export interface Dependency {
  name: string;
  version: string;
  type: 'production' | 'development';
  optional: boolean;
}

/**
 * Industry Agent Types
 */
export interface IndustryAgent {
  id: string;
  name: string;
  type: 'CAPSULE' | 'AVATAR' | 'ORCHESTRATOR';
  status: 'IDLE' | 'RUNNING' | 'PAUSED' | 'FAILED';
  schedule?: CronSchedule;
  execution: ExecutionConfig;
  capabilities: Capability[];
}

export interface CronSchedule {
  expression: string; // e.g., "0 6 * * *"
  timezone: string;
  enabled: boolean;
}

export interface ExecutionConfig {
  timeout: number; // seconds
  retries: number;
  retryDelay: number; // seconds
  resources: ResourceRequirements;
}

export interface ResourceRequirements {
  cpu: string; // e.g., "500m"
  memory: string; // e.g., "512Mi"
  storage: string; // e.g., "1Gi"
}

export interface Capability {
  name: string;
  description: string;
  parameters: CapabilityParameter[];
  outputs: string[];
}

export interface CapabilityParameter {
  name: string;
  type: 'string' | 'number' | 'boolean' | 'object' | 'array';
  required: boolean;
  default?: any;
  validation?: string;
}

/**
 * Avatar Types
 */
export interface Avatar {
  id: string;
  name: string;
  role: 'SUPPORT' | 'SALES' | 'ANALYST' | 'ORCHESTRATOR';
  personality: AvatarPersonality;
  capabilities: string[];
  interactions: Interaction[];
}

export interface AvatarPersonality {
  tone: 'PROFESSIONAL' | 'FRIENDLY' | 'CASUAL' | 'FORMAL';
  language: string;
  responseStyle: 'CONCISE' | 'DETAILED' | 'BALANCED';
  empathy: number; // 0-100
}

export interface Interaction {
  id: string;
  customerId: string;
  timestamp: Date;
  channel: 'CHAT' | 'EMAIL' | 'VOICE' | 'API';
  message: string;
  response: string;
  sentiment: number; // -1 to 1
  resolved: boolean;
}

/**
 * Customer Types
 */
export interface Customer {
  id: string;
  email: string;
  name: string;
  tier: 'FREE' | 'PREMIUM' | 'ENTERPRISE';
  status: 'ACTIVE' | 'INACTIVE' | 'SUSPENDED';
  createdAt: Date;
  lastActivity: Date;
  preferences: CustomerPreferences;
  usage: UsageMetrics;
}

export interface CustomerPreferences {
  notifications: boolean;
  newsletter: boolean;
  dataSharing: boolean;
  theme: 'LIGHT' | 'DARK' | 'AUTO';
  language: string;
}

export interface UsageMetrics {
  totalRequests: number;
  successfulRequests: number;
  failedRequests: number;
  averageResponseTime: number;
  lastRequest: Date;
  quotaUsed: number;
  quotaLimit: number;
}

/**
 * Communication Types
 */
export interface Message<T = any> {
  id: string;
  type: string;
  source: string;
  destination: string;
  timestamp: Date;
  payload: T;
  metadata: MessageMetadata;
}

export interface MessageMetadata {
  correlationId?: string;
  causationId?: string;
  userId?: string;
  traceId?: string;
  priority: 'LOW' | 'NORMAL' | 'HIGH' | 'CRITICAL';
}

export interface Event<T = any> {
  id: string;
  name: string;
  timestamp: Date;
  data: T;
  source: string;
  version: string;
}

/**
 * Error Types
 */
export class CouncilError extends Error {
  constructor(
    message: string,
    public code: string,
    public severity: Alert['severity'],
    public metadata?: Record<string, any>
  ) {
    super(message);
    this.name = 'CouncilError';
  }
}

export class SovereignError extends Error {
  constructor(
    message: string,
    public sovereignId: string,
    public operation: string
  ) {
    super(message);
    this.name = 'SovereignError';
  }
}

export class CustodianError extends Error {
  constructor(
    message: string,
    public custodianId: string,
    public package: string
  ) {
    super(message);
    this.name = 'CustodianError';
  }
}

export class AgentError extends Error {
  constructor(
    message: string,
    public agentId: string,
    public execution: string
  ) {
    super(message);
    this.name = 'AgentError';
  }
}
