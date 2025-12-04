# ADR-002: Risk-Tier Governance

**Status:** Proposed
**Date:** 2025-12-03
**Decision Drivers:**
- Autonomy scaling: Balance AI velocity with human oversight
- Sign-off thresholds: Clear approval authority at each risk level
- Operational efficiency: Prevent bottlenecks while maintaining safety
- Caribbean compliance: CARICOM data governance requirements
- Creator margin: Maximize developer productivity with appropriate gates

## Context

### Intent Source
- **Origin:** Council directive for graduated autonomy framework
- **Issue Reference:** #CODEX-2025-009 - Risk-tiered approval system
- **Form:** Governance policy for autonomous coding system (ADR-001 dependency)

### Problem Statement

The autonomous coding system (ADR-001) requires clear risk classification to:
- Scale autonomy appropriately (low-risk changes auto-merge, high-risk require council)
- Prevent bottlenecks (not all changes need full council review)
- Maintain safety and compliance (critical changes must have proper oversight)
- Provide clear approval authority and accountability chain
- Enable fast iteration for low-risk changes while protecting critical systems

### Affected Modules and Data Flows

**Risk Assessment Engine:**
- Intent Gateway classifies incoming requests by risk tier
- Autonomy Orchestrator routes approvals based on tier
- Policy Guards enforce tier-specific validation rules
- Artifact Ledger tracks approval chains with full lineage

**Data Flows:**
```
Change Request → Risk Classification → Approval Routing
       ↓                  ↓                    ↓
Intent Gateway    Risk Tier Engine    Autonomy Orchestrator
       ↓                  ↓                    ↓
Low/Medium/High    Auto/Steward/Council    Sign-off Workflow
```

### Jurisdiction & PII Classification
- **Primary Jurisdiction:** Caribbean (Trinidad & Tobago governance)
- **Compliance Requirements:** CARICOM data governance, SOC 2 change management
- **PII Impact Assessment:** Changes affecting PII require High tier minimum
- **Cross-Border Considerations:** Data flow changes require council multi-sign

## Decision

Implement three-tier risk governance system with autonomy scaling and graduated sign-off requirements.

### Risk Tier Definitions

#### **Low Risk Tier**
**Scope:**
- Documentation updates (README, ADRs, runbooks, comments)
- Test additions/improvements (unit tests, integration tests, E2E tests)
- Performance tweaks (caching, query optimization, bundle size reduction)
- Configuration changes (feature flags OFF, logging levels, metrics)
- Dependency patch updates (security patches, bug fixes)
- Code formatting and linting fixes
- Non-functional refactoring (no behavior change)

**Autonomy Level:** **Full Automation**
- AI can generate, validate, and merge without human pre-approval
- Post-merge review by steward within 24 hours (async)
- Automated rollback if issues detected in canary

**Approval Workflow:**
```
AI Generation → CI Green → Auto-Merge → Deploy Sandbox → Canary 5%
                  ↓                                          ↓
            Policy Guards                           Auto-Rollback (if >1% error)
                  ↓                                          ↓
         Security/License/Tests                    Steward Notification (async)
```

**Sign-off Threshold:** **None (auto-merge after CI green)**
- Steward notified post-merge for awareness
- Steward can revert within 24 hours if concerns arise
- No human gate blocks the merge

**SLO:** <10 minutes from intent → production (via canary)

**Policy Requirements:**
- ✅ All CI checks pass (lint, type check, unit tests)
- ✅ Security scan clean (no new vulnerabilities)
- ✅ License compliance (no new blocked licenses)
- ✅ Code coverage maintained or improved
- ✅ Performance budgets respected (bundle size, latency)

**Examples:**
- Adding unit tests for existing function
- Updating API documentation with new examples
- Optimizing database query with index
- Fixing typo in README
- Updating dependency `lodash` from 4.17.20 → 4.17.21 (patch)

---

#### **Medium Risk Tier**
**Scope:**
- New features (user-facing functionality, API endpoints)
- External integrations (third-party APIs, webhooks, OAuth providers)
- Database schema changes (new tables, columns; backwards-compatible)
- Dependency minor updates (new features, potential breaking changes)
- Configuration changes (feature flags ON, environment variables)
- Infrastructure changes (scaling rules, resource limits)
- UI/UX changes (layout, styling, user flows)
- Error handling improvements (new retry logic, fallbacks)

**Autonomy Level:** **Assisted Automation**
- AI generates code and runs validation
- Human steward reviews and approves before merge
- Steward can request changes or approve as-is

**Approval Workflow:**
```
AI Generation → CI Green → Steward Review → Sign-off → Merge
                  ↓              ↓             ↓
            Policy Guards   Code Review   Approval Logged
                  ↓              ↓             ↓
         Security/Tests   Functionality   Artifact Ledger
                                ↓
                    Deploy Sandbox → Canary 5% → Production
```

**Sign-off Threshold:** **Steward approval required**
- **Steward Roles:** Lead Engineer, Senior Developer, Tech Lead
- **Review SLA:** <2 hours during business hours, <8 hours off-hours
- **Approval Criteria:**
  - Code quality meets standards
  - Tests cover new functionality
  - No obvious security issues
  - Aligns with architecture patterns

**SLO:** <4 hours from intent → production (including review time)

**Policy Requirements:**
- ✅ All Low Risk policies pass
- ✅ Integration tests pass (if external dependencies)
- ✅ Feature flag exists for rollback control
- ✅ Monitoring/alerting configured for new functionality
- ✅ Documentation updated (API docs, user guides)
- ✅ Database migrations reversible (if schema changes)

**Examples:**
- Adding new API endpoint `/api/v1/analytics`
- Integrating Stripe payment processing
- Adding new React component for dashboard widget
- Updating Next.js from 14.0.0 → 14.1.0 (minor)
- Creating new database table `user_preferences`
- Enabling feature flag for beta users (10% rollout)

---

#### **High Risk Tier**
**Scope:**
- Avatars and AI systems (autonomous agents, AI model changes)
- Compliance-critical features (GDPR, CARICOM, consent management)
- Data flows (PII processing, cross-border transfers, data retention)
- Authentication and authorization (login flows, RBAC, permissions)
- Cryptography and secrets (encryption changes, key rotation)
- Database breaking changes (table drops, column renames, data migrations)
- Architecture changes (service boundaries, API contracts, data models)
- Infrastructure core changes (networking, security groups, IAM policies)
- Payment processing (billing logic, transaction handling)
- Dependency major updates (potential breaking changes, new APIs)

**Autonomy Level:** **Human-Supervised**
- AI generates design + code for review
- Council multi-sign required before merge
- Extended validation in sandbox (48+ hours)
- Conservative canary rollout (1% initial traffic)

**Approval Workflow:**
```
AI Generation → CI Green → Steward Review → Council Multi-Sign → Merge
                  ↓              ↓                 ↓              ↓
            Policy Guards   Tech Review    Legal/Security   Approval Logged
                  ↓              ↓                 ↓              ↓
         Security/Tests   Architecture   Compliance Check  Artifact Ledger
                                                   ↓
                    Deploy Sandbox (48hr) → Canary 1% (manual gate) → Production
```

**Sign-off Threshold:** **Council multi-sign required (minimum 2 of 3)**
- **Council Roles:**
  - **Engineering Manager:** Technical feasibility and architecture alignment
  - **Security Lead:** Security posture and vulnerability assessment
  - **Compliance Officer:** Regulatory compliance (GDPR, CARICOM, SOC 2)
- **Review SLA:** <24 hours for first review, <7 days for final approval
- **Approval Criteria:**
  - Architecture Decision Record (ADR) created and approved
  - Security audit completed (threat model, penetration test if needed)
  - Compliance checklist signed off (data privacy impact assessment)
  - Rollback plan documented and tested in sandbox
  - Incident response plan updated

**SLO:** <7 days from intent → production (including extended validation)

**Policy Requirements:**
- ✅ All Medium Risk policies pass
- ✅ ADR created and linked in artifact ledger
- ✅ Security audit completed (SAST, DAST, manual review)
- ✅ Compliance impact assessment documented
- ✅ Data Privacy Impact Assessment (DPIA) if PII affected
- ✅ Extended sandbox testing (48+ hours, full test suite)
- ✅ Rollback tested and verified in sandbox
- ✅ Monitoring dashboards and alerts configured
- ✅ Incident response runbook created/updated
- ✅ Deployment plan with manual gates approved

**Examples:**
- Implementing new AI avatar system with autonomous decision-making
- Adding GDPR "right to erasure" data deletion workflow
- Changing authentication from JWT to OAuth 2.0 + OIDC
- Migrating PII data to new encryption scheme (AES-256-GCM)
- Implementing cross-border data transfer to EU region
- Upgrading React from 17.x → 18.x (major version, concurrent rendering)
- Creating new microservice for payment processing
- Modifying database schema to drop `legacy_users` table
- Changing RBAC model from role-based to attribute-based (ABAC)

---

### Risk Classification Algorithm

**Automatic Classification (Intent Gateway):**

```javascript
function classifyRisk(intent) {
  // High Risk indicators (any match → High)
  const highRiskKeywords = [
    'avatar', 'AI model', 'autonomous agent',
    'GDPR', 'compliance', 'consent', 'PII', 'cross-border',
    'authentication', 'authorization', 'RBAC', 'permissions',
    'encryption', 'secrets', 'cryptography',
    'data migration', 'schema breaking', 'drop table',
    'architecture', 'microservice', 'API contract',
    'payment', 'billing', 'transaction'
  ];

  // Medium Risk indicators
  const mediumRiskKeywords = [
    'feature', 'integration', 'API endpoint',
    'database schema', 'new table', 'migration',
    'feature flag', 'configuration',
    'UI change', 'user flow'
  ];

  // Low Risk indicators
  const lowRiskKeywords = [
    'documentation', 'README', 'comment',
    'test', 'unit test', 'integration test',
    'performance', 'optimization', 'caching',
    'refactor', 'formatting', 'linting'
  ];

  // Check High Risk first
  if (highRiskKeywords.some(kw => intent.includes(kw))) {
    return 'HIGH';
  }

  // Check Medium Risk
  if (mediumRiskKeywords.some(kw => intent.includes(kw))) {
    return 'MEDIUM';
  }

  // Default to Low Risk
  return 'LOW';
}
```

**Manual Override:**
- Stewards can escalate Low → Medium
- Council can escalate Medium → High
- De-escalation requires council approval (audit trail required)

### Autonomy Scaling Matrix

| Risk Tier | AI Autonomy | Human Gate | Approval SLA | Canary Traffic | Rollback Threshold |
|-----------|-------------|------------|--------------|----------------|-------------------|
| **Low**   | Full auto-merge | None (post-review) | <10 min | 5% standard | >1% error rate |
| **Medium** | Assisted (AI generates) | Steward sign-off | <4 hours | 5% standard | >0.5% error rate |
| **High**  | Supervised (AI assists) | Council multi-sign | <7 days | 1% conservative | >0.1% error rate |

### Escalation Paths

**Low → Medium Escalation:**
- Triggered by: Steward review flags concern, policy violation detected post-merge
- Process: Steward creates escalation ticket, routes to council for re-classification
- Timeline: <2 hours for decision

**Medium → High Escalation:**
- Triggered by: Security concern identified, compliance impact discovered, architectural risk
- Process: Steward flags for council review, multi-sign required before proceeding
- Timeline: <24 hours for initial review, <7 days for final decision

**Emergency De-escalation (High → Medium):**
- Triggered by: Production incident requiring urgent fix, security patch critical
- Process: Council emergency session, 2 of 3 sign-off required, temporary de-escalation with audit
- Timeline: <1 hour for critical incidents
- Post-incident: Full High Risk review within 7 days, resealing if needed

## Alternatives Considered

### Alternative 1: Single Approval Tier (All Changes Require Council)
- **Pros:** Maximum oversight, clear accountability, risk-averse
- **Cons:** Severe bottleneck, council overwhelmed, slow velocity (weeks per change)
- **Trade-off:** Safety vs. velocity - **rejected due to unacceptable bottleneck**

### Alternative 2: Two-Tier System (Auto vs. Manual)
- **Pros:** Simpler to implement, clear binary decision
- **Cons:** Medium-risk changes either too slow (manual) or too risky (auto)
- **Trade-off:** Simplicity vs. granularity - **rejected due to lack of nuance**

### Alternative 3: Three-Tier System with Autonomy Scaling (SELECTED)
- **Pros:** Balanced velocity + safety, graduated oversight, clear escalation paths
- **Cons:** More complex to implement, requires risk classification engine
- **Trade-off:** Complexity vs. optimal governance - **selected for flexibility**

## Consequences

### Positive

- ✅ **Velocity:** Low-risk changes deploy in <10 minutes (vs. days with manual review)
- ✅ **Safety:** High-risk changes get proper council oversight and extended validation
- ✅ **Efficiency:** Stewards focus on Medium/High changes, not doc updates
- ✅ **Transparency:** Clear approval chains in artifact ledger
- ✅ **Compliance:** High-risk tier enforces GDPR/CARICOM requirements
- ✅ **Creator Margin:** Developers spend less time waiting for approvals

### Negative

- ⚠️ **Complexity:** Risk classification algorithm requires tuning and maintenance
- ⚠️ **Misclassification Risk:** AI might incorrectly classify High as Medium (needs manual override)
- ⚠️ **Council Bottleneck:** High-risk changes still require <7 days (acceptable trade-off)
- ⚠️ **Learning Curve:** Teams must understand tier definitions and workflows

### Mitigation

- Quarterly review of risk classification accuracy (target >95% correct classification)
- Steward training on escalation procedures and override authority
- Council capacity planning (dedicated review slots for High-risk changes)
- Artifact ledger analytics to identify classification patterns and improve algorithm

## Rollback Plan

**Per-Tier Rollback:**
- **Low Risk:** Automated rollback via canary monitoring (>1% error → instant rollback)
- **Medium Risk:** Steward-triggered rollback (<2 hour response time)
- **High Risk:** Council-approved rollback with incident analysis

**Resealing After Rollback:**
- Low Risk: Escalate to Medium (steward review required for retry)
- Medium Risk: Escalate to High (council review required for retry)
- High Risk: Remains High with extended validation (96+ hours sandbox testing)

## References

### Related ADRs
- [ADR-001: Autonomous Coding System](./001-autonomous-coding-system.md) - Parent architecture decision

### OPA Policies
- **Location:** `policies/risk-tier.rego` (NEW - to be created)
- **Purpose:** Enforce risk tier validation and approval requirements
- **Rules:**
  - Validate approval chain matches risk tier
  - Block merge if insufficient sign-offs
  - Enforce canary traffic allocation by tier
  - Validate rollback thresholds by tier

### Approval Workflows
- **Location:** `.github/workflows/approval-routing.yml` (NEW - to be created)
- **Purpose:** Route changes to appropriate approvers based on risk tier
- **Steps:**
  1. Risk classification via Intent Gateway
  2. Route to auto-merge (Low), steward (Medium), or council (High)
  3. Enforce approval thresholds (0, 1, or 2+ sign-offs)
  4. Log approval chain in artifact ledger
  5. Proceed to deployment pipeline

### Risk Classification Rules
- **Location:** `policies/risk-classification.json` (NEW - to be created)
- **Purpose:** Keyword mapping and override rules for risk tier assignment
- **Format:**
  ```json
  {
    "high_risk_keywords": ["avatar", "GDPR", "auth", "encryption", ...],
    "medium_risk_keywords": ["feature", "integration", "schema", ...],
    "low_risk_keywords": ["docs", "test", "performance", ...],
    "manual_overrides": [
      {"pattern": "hotfix/*", "tier": "MEDIUM"},
      {"pattern": "security/*", "tier": "HIGH"}
    ]
  }
  ```

### Council Composition
- **Engineering Manager:** Technical architecture and feasibility
- **Security Lead:** Security posture and vulnerability management
- **Compliance Officer:** Regulatory compliance (GDPR, CARICOM, SOC 2)
- **Quorum:** 2 of 3 required for High Risk approval
- **Emergency Powers:** Any single council member can escalate Low/Medium → High

### Metrics & SLOs
- **Dashboard:** https://metrics.codexdominion.app/risk-governance
- **Tracked Metrics:**
  - Risk classification accuracy (target >95%)
  - Approval SLA adherence (Low <10min, Medium <4hr, High <7d)
  - Misclassification rate (target <5%)
  - Council review capacity utilization (target <80% to prevent bottleneck)
  - Escalation frequency (Low→Medium, Medium→High)
  - Rollback frequency by tier

### Related Tickets
- #CODEX-2025-009: Risk-tier governance framework (this ADR)
- #CODEX-2025-010: Risk classification engine implementation
- #CODEX-2025-011: Approval routing workflows (GitHub Actions)
- #CODEX-2025-012: Council review dashboard
- #CODEX-2025-013: OPA risk-tier policy creation

---

**Status:** Proposed (awaiting council approval)
**Dependencies:** ADR-001 (Autonomous Coding System)
**Next Review Date:** 2025-12-17 (council meeting)
**Implementation Target:** Q1 2026 (Phase 1 rollout)
**Council Directive:** CODEX-COUNCIL-2025-RISK-GOVERNANCE-002 (pending)
