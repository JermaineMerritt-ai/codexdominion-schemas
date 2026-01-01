// Intelligence Core Engine Types
// Defines the structure for the 12 intelligence engines in CodexDominion

export interface IntelligenceEngine {
  id: string
  name: string
  description: string
  role: string
  capabilities: string[]
  primary_capsules: string[]
  operational_mode: "off" | "assist" | "hybrid" | "auto"
  status: "planned" | "active" | "in_progress" | "deprecated"
  lifecycle: "concept" | "prototype" | "beta" | "active" | "refine" | "legacy"
  governance: {
    risk_level: "low" | "medium" | "high" | "critical"
    approval_required: "automated" | "user" | "domain_expert" | "cultural_expert" | "council"
    audit_frequency: "continuous" | "daily" | "weekly" | "monthly" | "quarterly"
    owner_role: string
    owner_entity: string
    review_cadence: string
    kill_switch: boolean
    feedback_channels: string[]
    guardrails: string[]
    feedback_loops: string[]
    ethics_profile: {
      prioritizes_privacy: boolean
      prioritizes_safety: boolean
      bias_mitigation: string
      youth_protection: string
    }
    audit_trail: {
      log_all_operations: boolean
      retention_days: number
      sensitive_data_encryption: boolean
    }
  }
  overlays: {
    stewardship: boolean
    wellbeing: boolean
    planetary: boolean
    intergenerational: boolean
  }
}

export type EngineStatus = IntelligenceEngine["status"]
export type EngineLifecycle = IntelligenceEngine["lifecycle"]
export type OperationalMode = IntelligenceEngine["operational_mode"]
export type RiskLevel = IntelligenceEngine["governance"]["risk_level"]
export type ApprovalLevel = IntelligenceEngine["governance"]["approval_required"]
export type AuditFrequency = IntelligenceEngine["governance"]["audit_frequency"]

export interface EngineOverlays {
  stewardship: boolean
  wellbeing: boolean
  planetary: boolean
  intergenerational: boolean
}

export interface EngineGovernance {
  risk_level: RiskLevel
  approval_required: ApprovalLevel
  audit_frequency: AuditFrequency
  owner_role: string
  owner_entity: string
  review_cadence: string
  kill_switch: boolean
  feedback_channels: string[]
  guardrails: string[]
  feedback_loops: string[]
  ethics_profile: {
    prioritizes_privacy: boolean
    prioritizes_safety: boolean
    bias_mitigation: string
    youth_protection: string
  }
  audit_trail: {
    log_all_operations: boolean
    retention_days: number
    sensitive_data_encryption: boolean
  }
}
