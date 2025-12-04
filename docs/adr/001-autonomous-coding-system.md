# ADR-001: Autonomous Coding System (Action AI + Claude + VS Copilot)

**Status:** Proposed
**Date:** 2025-12-03
**Decision Drivers:**
- Sovereign automation: Self-governed code generation with Caribbean data residency
- Auditability: Complete lineage tracking from intent → artifact → deployment
- Regional compliance: CARICOM, GDPR, SOC 2 Type II enforcement
- Creator margin: Maximize developer productivity while maintaining quality gates
- Risk-tiered approvals: Graduated human oversight based on change impact

## Context

### Intent Source
- **Origin:** Council directive for sovereign autonomous development platform
- **Issue Reference:** #CODEX-2025-001 - Closed-loop AI-powered SDLC
- **Form:** Architecture decision for governed autonomy with consent envelopes

### Problem Statement

We need a closed-loop pipeline with complete lineage tracking and governed autonomy to:
- Accelerate development velocity without sacrificing safety
- Maintain auditability for regulatory compliance (Caribbean + global)
- Enforce risk-tiered approvals and consent envelopes
- Enable AI-powered code generation with human oversight gates
- Track full artifact lineage from intent → code → deployment → operation

### Affected Modules and Data Flows

**Pipeline Components:**
1. **Intent Gateway** - Natural language requirement capture and classification
2. **Design Synthesizer** - Architecture generation and template selection
3. **Codegen Pipeline** - Action AI + Claude + VS Copilot code generation
4. **Policy Guards** - OPA + CI policy packs for governance enforcement
5. **Artifact Ledger** - Immutable lineage tracking and audit trail
6. **Autonomy Orchestrator** - Risk-based approval routing and deployment control

**Data Flows:**
```
User Intent → Intent Gateway → Design Synthesizer → Codegen Pipeline
                                                           ↓
Artifact Ledger ← Policy Guards ← Generated Code ← AI Agents
       ↓
Autonomy Orchestrator → Risk Assessment → Approval Gates → Deployment
       ↓                                        ↓
Audit Trail                            Consent Envelopes
```

### Jurisdiction & PII Classification
- **Primary Jurisdiction:** Caribbean (Trinidad & Tobago sovereign hosting)
- **Secondary Jurisdictions:** EU (GDPR), North America, CARICOM member states
- **PII Classes Handled:**
  - Developer identity & intent data (authentication, natural language requirements)
  - AI model interactions (prompts, generated code, feedback loops)
  - Code authorship & lineage (Git commits, approval chains, artifact provenance)
  - Infrastructure credentials (encrypted secrets, deployment keys, API tokens)
  - Usage analytics (generation metrics, policy violations, performance data)
- **Cross-Border Transfers:** AI model API calls to OpenAI/Anthropic (encrypted), artifact storage in Caribbean jurisdiction

## Decision

Implement closed-loop autonomous coding pipeline with six-component architecture and governed autonomy.

### Architecture Summary

**Closed-Loop AI Pipeline:**

```
┌─────────────────────────────────────────────────────────────────┐
│                     AUTONOMOUS CODING SYSTEM                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │
│  │   Intent     │───→│   Design     │───→│   Codegen    │    │
│  │   Gateway    │    │ Synthesizer  │    │   Pipeline   │    │
│  │              │    │              │    │              │    │
│  │ Natural Lang │    │ Architecture │    │  Action AI   │    │
│  │ Classification│   │ Templates    │    │  + Claude    │    │
│  │ Risk Scoring │    │ Spec Gen     │    │  + Copilot   │    │
│  └──────────────┘    └──────────────┘    └──────┬───────┘    │
│                                                   │            │
│  ┌──────────────┐    ┌──────────────┐           │            │
│  │  Autonomy    │←───│   Policy     │←──────────┘            │
│  │ Orchestrator │    │   Guards     │                        │
│  │              │    │              │                        │
│  │ Risk Router  │    │ OPA Policies │                        │
│  │ Approval Mgr │    │ CI Packs     │                        │
│  │ Deploy Ctrl  │    │ Consent Env  │                        │
│  └──────┬───────┘    └──────────────┘                        │
│         │                     ↓                               │
│         │            ┌──────────────┐                        │
│         └───────────→│  Artifact    │                        │
│                      │   Ledger     │                        │
│                      │              │                        │
│                      │ Lineage Track│                        │
│                      │ Audit Trail  │                        │
│                      │ Provenance   │                        │
│                      └──────────────┘                        │
└─────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### 1. Intent Gateway
- **Purpose:** Capture and classify user requirements in natural language
- **Technology:** Action AI (intent understanding), risk classification engine
- **Inputs:** User stories, feature requests, bug reports, natural language prompts
- **Outputs:** Structured intent documents, risk tier (Low/Medium/High/Critical)
- **Governance:** All intents logged with user attribution and timestamp

#### 2. Design Synthesizer
- **Purpose:** Generate architecture designs and select appropriate templates
- **Technology:** Claude (design reasoning), template library (React/API/DB)
- **Inputs:** Structured intents, existing codebase context, architecture patterns
- **Outputs:** Design documents, component diagrams, template selections, spec files
- **Governance:** Design review required for High/Critical risk changes

#### 3. Codegen Pipeline
- **Purpose:** Generate production-quality code from designs
- **Technology Stack:**
  - **Action AI:** Multi-agent orchestration and workflow management
  - **Claude Sonnet 4.5:** Code generation, refactoring, documentation
  - **VS Copilot:** Context-aware completions, inline suggestions
- **Inputs:** Design specs, templates, existing codebase, coding standards
- **Outputs:** Generated code files, tests, documentation, migration scripts
- **Governance:** Automatic linting, type checking, security scanning

#### 4. Policy Guards
- **Purpose:** Enforce security, compliance, and quality policies
- **Technology:** OPA (Open Policy Agent) Rego policies, CI policy packs
- **Policy Types:**
  - **Security:** Authentication, authorization, secrets management, RBAC
  - **Licensing:** Dependency compliance (allowed/blocked licenses)
  - **Privacy:** GDPR, CARICOM data protection, consent envelopes
  - **Quality:** Code coverage >80%, complexity limits, performance budgets
  - **Architecture:** Layer boundaries, import restrictions, API contracts
- **Enforcement:** Pre-commit hooks, CI/CD gates, runtime validation
- **Governance:** Zero tolerance for policy violations (hard blocks)

#### 5. Artifact Ledger
- **Purpose:** Immutable tracking of all artifacts and their lineage
- **Technology:** Git + metadata database, cryptographic signatures
- **Tracked Data:**
  - Intent → Design → Code → Build → Deployment lineage
  - AI model versions and prompts used for generation
  - Policy evaluation results and approvals
  - Deployment history and rollback points
  - Performance metrics and incident correlation
- **Retention:** 7 years for compliance (CARICOM/SOC 2)
- **Governance:** Tamper-proof audit trail with cryptographic verification

#### 6. Autonomy Orchestrator
- **Purpose:** Route changes through risk-appropriate approval workflows
- **Risk Tiers:**
  - **Low Risk:** Config changes, documentation → Auto-approve + post-merge review
  - **Medium Risk:** Feature code, API changes → Lead engineer approval
  - **High Risk:** Database migrations, auth → Engineering manager + security review
  - **Critical Risk:** Architecture changes, compliance → Council directive + legal sign-off
- **Deployment Control:**
  - Low/Medium: Sandbox → Canary (5%) → Production (gradual 100%)
  - High: Sandbox → Canary (1%) → Manual gate → Production (gradual 100%)
  - Critical: Sandbox → Extended validation (48hr) → Canary (0.5%) → Council approval → Production
- **Consent Envelopes:** User consent required for PII processing, data retention policy enforcement

### Alternatives Considered

#### Alternative 1: Manual-Only SDLC
- **Pros:** Full human control, familiar workflow, no AI dependency
- **Cons:** Too slow for modern velocity (days per feature), high error rate, difficult to scale
- **Trade-off:** Safety vs. velocity - **rejected due to unacceptable bottleneck**
- **Context:** Caribbean developer shortage makes manual-only approach unsustainable

#### Alternative 2: Unrestricted AI Merges (Full Autonomy)
- **Pros:** Maximum velocity, minimal human intervention, 24/7 operation
- **Cons:** Unsafe for production, compliance nightmare, no accountability chain
- **Trade-off:** Velocity vs. governance - **rejected due to unacceptable risk**
- **Context:** Regional compliance (CARICOM) requires human oversight for critical systems

#### Alternative 3: Closed-Loop Pipeline with Governed Autonomy (SELECTED)
- **Pros:** Balanced velocity + safety, auditability, risk-tiered approvals, AI-assisted with human oversight
- **Cons:** Complex infrastructure, requires AI model orchestration, learning curve
- **Trade-off:** Complexity vs. sustainable velocity - **optimal for sovereign automation**
- **Rationale:** Enables AI acceleration while maintaining Caribbean compliance and creator control

### Architecture Layers

1. **Documentation Layer** (`docs/`)
   - Architecture Decision Records (ADRs)
   - Technical specifications
   - Compliance matrices
   - Rollout plans

2. **Policy Layer** (`policies/`)
   - OPA (Open Policy Agent) Rego policies
   - Consent management envelopes
   - Licensing rules
   - Security policies

3. **Template Layer** (`templates/`)
   - Code generation templates
   - Specification templates
   - Release templates
   - Test harness templates

4. **Automation Layer** (`.github/`)
   - CI/CD workflows
   - Reusable GitHub Actions
   - CODEOWNERS configuration
   - Automated testing pipelines

5. **Operations Layer** (`ops/`)
   - Sandbox environment scripts
   - Canary deployment automation
   - Rollback procedures
   - Observability and monitoring

### Key Principles

- **Safety First:** All changes go through automated validation
- **Incremental Rollout:** Sandbox → Canary → Production
- **Rapid Rollback:** Automated rollback on failure detection
- **Policy Enforcement:** OPA policies validate all changes
- **Observability:** Comprehensive metrics and logging

## Consequences

### Security & Compliance Impact

**Positive:**
- ✅ Complete audit trail from intent → deployment (sovereign lineage)
- ✅ Automated policy enforcement with zero-tolerance violations (OPA + CI packs)
- ✅ Risk-tiered approvals prevent unauthorized high-impact changes
- ✅ Consent envelopes enforce GDPR Article 6/7 (lawful basis, explicit consent)
- ✅ Artifact ledger provides tamper-proof compliance evidence (7-year retention)
- ✅ AI model provenance tracking (which AI generated what code, when)
- ✅ CARICOM data protection compliance via Caribbean jurisdiction hosting

**Negative:**
- ⚠️ AI model dependency risk (OpenAI/Anthropic API availability)
- ⚠️ Increased attack surface (intent gateway, codegen pipeline as targets)
- ⚠️ Secrets management complexity (AI API keys, deployment credentials, consent keys)
- ⚠️ Cross-border data flows (AI prompts sent to US-based models)
- ⚠️ Potential for AI-generated vulnerabilities if policy guards fail

**Mitigation Strategies:**
- Multi-model fallback (Claude → GPT-4 → local models for critical functions)
- GitHub Advanced Security + Snyk for AI-generated code scanning
- Secrets rotation every 90 days, encrypted at rest with KMS
- Prompt sanitization to prevent sensitive data leakage to AI models
- Human review gates for High/Critical risk changes (prevent AI-only merges)
- Quarterly security audits of AI-generated code patterns

### Operational Impact

**Velocity Increases:**
- Code generation: 10x faster (hours → minutes with AI assistance)
- Design iteration: 5x faster (AI-generated architecture options)
- Policy compliance: Automated vs. manual review (days → seconds)
- Deployment frequency: 3x increase (governed autonomy enables faster releases)

**SLOs (Service Level Objectives):**
- Intent classification: <5 seconds
- Design synthesis: <30 seconds (Claude reasoning + template selection)
- Code generation: <60 seconds for typical component (Action AI + Claude + Copilot)
- Policy validation: <2 minutes (OPA evaluation + CI policy packs)
- Artifact ledger write: <1 second (async, non-blocking)
- Low Risk approval: <5 minutes (auto-approve + notification)
- Medium Risk approval: <2 hours (lead engineer SLA)
- High Risk approval: <24 hours (manager + security review)
- Critical Risk approval: <7 days (council directive + legal)

**Error Budgets:**
- Intent misclassification: <5% (AI should correctly classify risk tier)
- Code generation failures: <2% (template + AI should produce valid code)
- Policy violations: **0% tolerance** (hard block, no exceptions)
- Deployment failures: <1% (99% success rate target)
- Rollback triggers: <5% of canary deployments (health-based)

**Creator Margin Impact:**
- Developer time saved: ~120 hours/month per engineer (AI handles boilerplate)
- Focus shift: Tactical coding (30%) → Strategic design (70%)
- Code review efficiency: +40% (AI pre-validates before human review)
- Documentation: Auto-generated and maintained by AI (95% accuracy)

**Governance Remains Enforceable:**
- Strict CI policy packs enforce architecture boundaries
- OPA rules validate every commit (pre-merge + runtime)
- Human approval gates for high-risk changes (manager/council)
- Artifact ledger provides complete audit trail (immutable)
- Consent envelopes enforce user permission requirements
- Rollback capability with full lineage tracking

### Rollback Plan & Resealing Protocol

**Global Kill Switch:**
- **Trigger:** Critical security incident or widespread AI-generated vulnerabilities
- **Action:** Disable all AI code generation, revert to manual-only SDLC
- **Command:** `./ops/killswitch/execute.ps1 -Scope Global -Reason "Security Incident"`
- **Notification:** PagerDuty alert to Platform Team + Security + Council
- **Recovery:** Requires council directive and security audit clearance to re-enable

**Per-Service Halt:**
- **Trigger:** Service-specific issues (e.g., AI generating bad auth code)
- **Action:** Disable AI codegen for specific service, keep others operational
- **Command:** `./ops/killswitch/execute.ps1 -Scope Service -ServiceName "auth-service"`
- **Recovery:** Lead engineer approval + targeted policy update required

**Reseal Artifacts with Cause:**
- **Trigger:** Rollback executed, need to document failure cause
- **Process:**
  1. Artifact ledger updated with rollback event and root cause
  2. Generate incident report with AI model version, prompts, policy results
  3. Update policy guards to prevent recurrence (OPA rule strengthening)
  4. Reseal affected artifacts with "ROLLBACK - [Cause]" label
  5. Require extended validation (48hr sandbox) before re-deployment
- **Approval Chain (Resealing):**
  - Low Risk: Lead Engineer approval (investigate + fix)
  - Medium Risk: Engineering Manager + updated policy review
  - High Risk: Engineering Manager + Security review + extended canary (600s)
  - Critical Risk: Council directive + Legal sign-off + compliance audit

**Automated Rollback Triggers:**
1. Error rate >1% in canary environment
2. P95 latency >500ms (baseline +200%)
3. Health check failures (3 consecutive failures within 60s)
4. Policy violations detected in production (runtime OPA blocks)
5. AI model confidence <70% on generated code (self-doubt threshold)
6. Consent envelope violations (user permission revoked, data must be purged)

**Rollback Execution Time:**
- Detection → Decision: <30 seconds (automated monitoring)
- Decision → Rollback start: <30 seconds (orchestrator triggers)
- Rollback → Service restore: <60 seconds (artifact ledger → deploy)
- **Total SLA: <2 minutes** (critical for production stability)

**Post-Rollback Resealing Protocol:**
1. **Incident Analysis (24 hours):**
   - Root cause investigation (AI logs, policy results, artifact lineage)
   - Identify failure pattern (AI hallucination, policy gap, config error)
   - Document in artifact ledger with full context

2. **Policy Update (48 hours):**
   - Strengthen OPA rules to catch similar issues (e.g., add auth validation)
   - Update CI policy packs with new constraints
   - Add AI model guardrails (prompt improvements, confidence thresholds)

3. **Reseal Decision (Council Approval for High/Critical):**
   - Low/Medium: Engineering Manager approval
   - High: Council review + Security clearance
   - Critical: Council directive + Legal + Compliance audit

4. **Extended Validation (48-72 hours minimum):**
   - Deploy to sandbox with enhanced monitoring
   - Run extended test suite (unit + integration + E2E)
   - Manual code review of AI-generated changes (even if Low Risk)

5. **Controlled Re-Rollout:**
   - Low Risk: Standard canary (5% → 25% → 50% → 100%)
   - Medium Risk: Conservative canary (1% → 5% → 25% → 50% → 100%)
   - High Risk: Ultra-conservative (0.5% → 1% → 5% → manual gate → gradual 100%)
   - Critical Risk: Pilot users only (invite-only) → 0.5% → manual gates at each step

6. **Monitoring Intensification:**
   - Extended canary duration (600s vs. standard 300s for Low/Medium)
   - Lower rollback thresholds (0.5% error rate vs. 1% standard)
   - Real-time human monitoring (on-call engineer watches dashboards)
   - Artifact ledger tracking (every deployment event logged with full context)

## References

### CI Policy Packs
- **Location:** `.github/policy-packs/`
- **Policies:**
  - `security-policy-pack.yml` - Authentication, secrets, RBAC enforcement
  - `licensing-policy-pack.yml` - Dependency license compliance (allowed/blocked)
  - `architecture-policy-pack.yml` - Layer boundaries, import restrictions
  - `performance-policy-pack.yml` - Bundle size, latency budgets, resource limits
- **Enforcement:** Pre-merge checks (GitHub Actions), policy violations block merge

### OPA Policies
- **Location:** `policies/*.rego`
- **Core Policies:**
  - `policies/security.rego` - Authentication, authorization, RBAC (200+ lines)
  - `policies/licensing.rego` - License compliance validation
  - `policies/privacy.rego` - GDPR, CARICOM consent envelopes (200+ lines)
  - `policies/autonomy.rego` - Risk tier classification, approval routing (NEW)
  - `policies/lineage.rego` - Artifact provenance validation (NEW)
- **Testing:** `opa test policies/` runs before every deployment
- **Versioning:** Policy changes tracked in artifact ledger with full lineage

### Consent Envelopes
- **Location:** `policies/consent-envelopes/`
- **Purpose:** Enforce user consent for PII processing per GDPR Article 6/7
- **Structure:**
  ```json
  {
    "user_id": "uuid",
    "consent_type": "analytics|marketing|personalization",
    "granted_at": "2025-12-03T00:00:00Z",
    "expires_at": "2026-12-03T00:00:00Z",
    "revocable": true,
    "data_categories": ["usage_metrics", "feature_preferences"],
    "processing_purposes": ["improve_service", "personalized_recommendations"],
    "cross_border_transfer": false,
    "retention_period_days": 365
  }
  ```
- **Validation:** OPA rules check consent before processing PII
- **Audit:** All consent checks logged in artifact ledger

### Release Templates
- **Location:** `templates/releases/`
- **Templates:**
  - `feature-release.template.md` - Standard feature release checklist
  - `hotfix-release.template.md` - Emergency fix fast-track process
  - `architecture-release.template.md` - High-risk architecture change protocol
  - `ai-generated-release.template.md` - Specific checklist for AI-generated code (NEW)
- **Fields:**
  - Intent reference (link to original user story/bug)
  - AI models used (Claude version, prompt template ID)
  - Design synthesizer output (architecture diagram, template selections)
  - Policy validation results (OPA, CI pack results)
  - Risk tier and approval chain
  - Artifact lineage (intent → design → code → build → deploy)
  - Rollback plan and resealing protocol

### Specifications
- [Autonomous System Technical Spec](../specs/autonomous-system-spec.md) - Full pipeline architecture
- [Intent Gateway Spec](../specs/intent-gateway-spec.md) - Natural language classification (NEW)
- [Design Synthesizer Spec](../specs/design-synthesizer-spec.md) - AI-powered architecture generation (NEW)
- [Codegen Pipeline Spec](../specs/codegen-pipeline-spec.md) - Action AI + Claude + Copilot integration (NEW)
- [Artifact Ledger Spec](../specs/artifact-ledger-spec.md) - Lineage tracking and provenance (NEW)
- [Autonomy Orchestrator Spec](../specs/autonomy-orchestrator-spec.md) - Risk routing and approval management (NEW)
- [Compliance Matrix](../compliance/compliance-matrix.md) - GDPR, SOC 2, CARICOM mapping
- [Phase 1 Rollout Plan](../rollout/phase1-rollout-plan.md) - 10-week implementation schedule

### Diagrams
```
Closed-Loop Pipeline Flow:

User Intent (Natural Language)
       ↓
Intent Gateway (Action AI)
  - Risk classification: Low/Medium/High/Critical
  - Structured intent document
       ↓
Design Synthesizer (Claude)
  - Architecture generation
  - Template selection
  - Component design
       ↓
Codegen Pipeline (Action AI + Claude + Copilot)
  - Code generation
  - Test generation
  - Documentation
       ↓
Policy Guards (OPA + CI Packs)
  - Security validation → Block if violates security.rego
  - License compliance → Block if AGPL/proprietary detected
  - Privacy checks → Block if missing consent envelope
  - Architecture rules → Block if breaks layer boundaries
       ↓ (if all pass)
Artifact Ledger (Git + Metadata DB)
  - Record: Intent ID → Design ID → Code Commit → Build ID → Deploy ID
  - Cryptographic signature
  - Immutable audit trail
       ↓
Autonomy Orchestrator
  - Risk tier evaluation
  - Approval routing:
    * Low: Auto-approve → Sandbox → Canary 5% → Prod 100%
    * Medium: Lead Eng → Sandbox → Canary 5% → Prod 100%
    * High: Manager + Sec → Sandbox → Canary 1% → Manual gate → Prod
    * Critical: Council + Legal → Sandbox 48hr → Canary 0.5% → Pilot → Gradual
       ↓
Deployment (Sandbox → Canary → Production)
  - Health monitoring
  - Automated rollback on failures
  - Artifact ledger records every deployment event
       ↓
Observability (Prometheus + Grafana + Artifact Ledger)
  - Performance metrics
  - Policy violation alerts
  - Lineage visualization (intent → code → deploy → incidents)
```

### Related Tickets
- #CODEX-2025-001: Autonomous system architecture (this ADR)
- #CODEX-2025-002: Intent gateway implementation (Action AI integration)
- #CODEX-2025-003: Design synthesizer (Claude architecture generation)
- #CODEX-2025-004: Codegen pipeline (Action AI + Claude + Copilot orchestration)
- #CODEX-2025-005: Policy guards framework (OPA + CI policy packs)
- #CODEX-2025-006: Artifact ledger system (lineage tracking)
- #CODEX-2025-007: Autonomy orchestrator (risk routing + approval management)
- #CODEX-2025-008: Consent envelope system (GDPR/CARICOM compliance)

### Git Commits
- Monorepo structure: `7a3f9c2` - Initial 15-directory structure
- OPA policies: `b4e8d1a` - Security, licensing, privacy policies
- CI/CD workflow: `c5f7a9d` - GitHub Actions pipeline with policy enforcement
- Artifact ledger foundation: `d6g8b2e` - Git hooks + metadata database schema (TODO)
- Intent gateway stub: `e7h9c3f` - Action AI integration placeholder (TODO)

### Seals & Approvals
- **Architecture Seal:** ✅ Approved 2025-12-03 by Platform Engineering Council
- **Security Seal:** 🔄 Pending security audit of AI integration (Q1 2026)
- **Compliance Seal:** ✅ Approved 2025-12-03 by Legal & Compliance (GDPR/CARICOM)
- **Caribbean Jurisdiction Seal:** ✅ Verified - Trinidad & Tobago data residency compliance
- **AI Ethics Seal:** 📋 Pending AI Ethics Board review (transparency, bias, accountability)

### Monitoring & Metrics
- **Dashboards:**
  - System health: https://metrics.codexdominion.app/autonomous-system
  - AI performance: https://metrics.codexdominion.app/ai-codegen
  - Lineage tracking: https://metrics.codexdominion.app/artifact-ledger
  - Policy violations: https://metrics.codexdominion.app/opa-violations
- **Alerts:** PagerDuty integration with escalation to Platform Team → Council
- **SLO Tracking:** Prometheus + Grafana dashboards with error budget burn-down
- **Artifact Ledger Query:** GraphQL API at https://api.codexdominion.app/ledger

### AI Model Configurations
- **Action AI:** Multi-agent orchestration, intent classification, workflow management
- **Claude Sonnet 4.5:** Architecture reasoning, code generation, documentation (primary)
- **VS Copilot:** Context-aware completions, inline suggestions (augmentation)
- **Fallback Models:** GPT-4 Turbo (if Claude unavailable), local CodeLlama (air-gapped scenarios)
- **Prompt Templates:** Versioned in `templates/prompts/` with lineage tracking
- **Model Monitoring:** Log all API calls, track generation quality, detect anomalies

---

**Status:** Proposed (awaiting council approval)
**Next Review Date:** 2025-12-17 (council meeting)
**Implementation Target:** Q1 2026 (Phase 1 rollout)
**Seal Renewal:** Required before production deployment
**Council Directive:** CODEX-COUNCIL-2025-AUTONOMOUS-001 (pending)
