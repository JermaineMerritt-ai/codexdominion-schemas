package codex.compliance

# Default deny-all policy
default allow = false

# Extract input context
risk_tier := input.change.risk_tier
jurisdiction := input.change.jurisdiction
licenses := input.scan.licenses
pii_classes := input.scan.pii
signoffs := input.change.signoffs
ci_status := input.ci
controls := input.controls

# ============================================================================
# RISK-TIER APPROVAL GATES (per ADR-002)
# ============================================================================

# LOW RISK: Auto-approve after CI green
allow {
  risk_tier == "low"
  ci_all_green
  not violates_licenses
  not violates_pii
  not violates_security
  not violates_performance
}

# MEDIUM RISK: Requires steward sign-off
allow {
  risk_tier == "medium"
  ci_all_green
  has_steward_signoff
  not violates_licenses
  not violates_pii
  not violates_security
  not violates_performance
}

# HIGH RISK: Requires council multi-sign (2 of 3)
allow {
  risk_tier == "high"
  ci_all_green
  has_council_quorum
  valid_jurisdiction
  not violates_licenses
  not violates_pii
  not violates_security
  not violates_performance
  has_adr_approval
}

# ============================================================================
# CI/CD VALIDATION
# ============================================================================

ci_all_green {
  ci_status.all_green == true
  ci_status.lint == "passed"
  ci_status.tests == "passed"
  ci_status.security_scan == "passed"
  ci_status.coverage >= 80
}

# ============================================================================
# APPROVAL VALIDATION
# ============================================================================

has_steward_signoff {
  signoffs.steward == true
  signoffs.steward_role in {"lead-engineer", "senior-developer", "tech-lead"}
}

has_council_quorum {
  signoffs.council >= 2
  has_required_council_roles
}

has_required_council_roles {
  count([role |
    role := signoffs.council_roles[_]
    role in {"engineering-manager", "security-lead", "compliance-officer"}
  ]) >= 2
}

has_adr_approval {
  input.change.adr_id != ""
  input.change.adr_status == "approved"
}

# ============================================================================
# JURISDICTION VALIDATION
# ============================================================================

valid_jurisdiction {
  jurisdiction in {"caribbean", "trinidad-tobago", "global"}
  caribbean_compliant
}

caribbean_compliant {
  # CARICOM data protection requirements
  input.controls.data_residency == "caribbean"
  input.controls.cross_border_encryption == true
  input.controls.sovereign_hosting == true
}

# ============================================================================
# LICENSE COMPLIANCE (per policies/licensing.rego)
# ============================================================================

violates_licenses {
  some l
  l := licenses[_]
  not allowed_licenses[l]
  not conditional_licenses[l]
}

allowed_licenses := {
  "MIT",
  "Apache-2.0",
  "BSD-2-Clause",
  "BSD-3-Clause",
  "ISC",
  "CC0-1.0"
}

conditional_licenses := {
  "GPL-3.0",
  "LGPL-3.0",
  "MPL-2.0"
}

blocked_licenses := {
  "AGPL-3.0",
  "SSPL",
  "Commons-Clause",
  "Proprietary",
  "UNLICENSED"
}

# Check for explicitly blocked licenses
violates_licenses {
  some l
  l := licenses[_]
  blocked_licenses[l]
}

# ============================================================================
# PII & DATA PRIVACY (GDPR, CARICOM)
# ============================================================================

violates_pii {
  count(pii_classes) > 0
  not has_pii_controls
}

has_pii_controls {
  controls.pii_redaction_enabled == true
  controls.pii_encryption_at_rest == true
  controls.pii_encryption_in_transit == true
  has_consent_envelopes
  has_retention_policy
}

has_consent_envelopes {
  # GDPR Article 6/7: Lawful basis and explicit consent
  input.controls.consent_management_enabled == true
  input.controls.consent_envelopes != []

  # Validate each PII class has consent envelope
  count([class |
    class := pii_classes[_]
    has_consent_for_class(class)
  ]) == count(pii_classes)
}

has_consent_for_class(class) {
  some envelope
  envelope := input.controls.consent_envelopes[_]
  class in envelope.data_categories
  envelope.granted == true
  not is_expired(envelope)
}

is_expired(envelope) {
  expires_at := time.parse_rfc3339_ns(envelope.expires_at)
  now := time.now_ns()
  now > expires_at
}

has_retention_policy {
  input.controls.retention_policy_defined == true
  input.controls.retention_period_days <= max_retention_days
}

max_retention_days := 2555  # 7 years for compliance

# ============================================================================
# SECURITY CONTROLS
# ============================================================================

violates_security {
  has_critical_vulnerabilities
}

violates_security {
  has_high_vulnerabilities
  risk_tier == "high"
}

violates_security {
  exposes_secrets
}

violates_security {
  missing_auth_controls
  requires_auth
}

has_critical_vulnerabilities {
  input.scan.vulnerabilities.critical > 0
}

has_high_vulnerabilities {
  input.scan.vulnerabilities.high > 0
}

exposes_secrets {
  input.scan.secrets_detected == true
}

missing_auth_controls {
  not input.controls.authentication_enabled
  not input.controls.authorization_enabled
}

requires_auth {
  # Changes affecting auth, payment, or PII require auth controls
  input.change.affects_auth == true
}

requires_auth {
  input.change.affects_payment == true
}

requires_auth {
  count(pii_classes) > 0
}

# ============================================================================
# PERFORMANCE BUDGETS
# ============================================================================

violates_performance {
  exceeds_bundle_size
}

violates_performance {
  exceeds_latency_budget
}

exceeds_bundle_size {
  input.scan.bundle_size_kb > max_bundle_size_kb
}

max_bundle_size_kb := 500

exceeds_latency_budget {
  input.scan.latency_p95_ms > max_latency_ms
}

max_latency_ms := 500

# ============================================================================
# COMPLIANCE REPORTING
# ============================================================================

# Generate compliance report for audit trail
compliance_report := {
  "timestamp": time.now_ns(),
  "risk_tier": risk_tier,
  "jurisdiction": jurisdiction,
  "approved": allow,
  "violations": violations,
  "signoffs": signoff_summary,
  "controls": control_summary,
  "recommendations": recommendations
}

violations := [v |
  v := violation_checks[_]
  v.violated == true
]

violation_checks := [
  {"type": "licenses", "violated": violates_licenses},
  {"type": "pii", "violated": violates_pii},
  {"type": "security", "violated": violates_security},
  {"type": "performance", "violated": violates_performance}
]

signoff_summary := {
  "steward": has_steward_signoff,
  "council_quorum": has_council_quorum,
  "council_count": signoffs.council,
  "adr_approved": has_adr_approval
}

control_summary := {
  "pii_controls": has_pii_controls,
  "consent_envelopes": has_consent_envelopes,
  "auth_controls": not missing_auth_controls,
  "caribbean_compliant": caribbean_compliant,
  "ci_passed": ci_all_green
}

recommendations := [r |
  recommendation_checks[_].condition == true
  r := recommendation_checks[_].message
]

recommendation_checks := [
  {
    "condition": risk_tier == "medium" and not has_feature_flag,
    "message": "Consider adding feature flag for safer rollback"
  },
  {
    "condition": count(pii_classes) > 0 and not has_dpia,
    "message": "Data Privacy Impact Assessment (DPIA) recommended for PII changes"
  },
  {
    "condition": risk_tier == "high" and not has_extended_sandbox,
    "message": "Extended sandbox testing (48+ hours) required for HIGH risk"
  },
  {
    "condition": has_conditional_licenses,
    "message": "Conditional licenses detected - manual legal review required"
  }
]

has_feature_flag {
  input.change.feature_flag_enabled == true
}

has_dpia {
  input.change.dpia_completed == true
}

has_extended_sandbox {
  input.change.sandbox_duration_hours >= 48
}

has_conditional_licenses {
  some l
  l := licenses[_]
  conditional_licenses[l]
}

# ============================================================================
# EMERGENCY OVERRIDE (Council-only)
# ============================================================================

# Emergency production incident requiring urgent fix
allow {
  input.change.emergency_override == true
  signoffs.council == 3  # All council members must approve
  input.change.emergency_reason != ""
  input.change.post_incident_review_scheduled == true
  ci_all_green
}
