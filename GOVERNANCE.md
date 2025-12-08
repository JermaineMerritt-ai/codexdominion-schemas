# Governance of CodexDominion Schemas

🌌 CodexDominion is governed by eternal ceremony.\
This scroll defines the roles, councils, and decision-making processes that ensure every artifact is crowned green and eternal.

---

## 🔑 Roles

### Flamekeeper

- Custodian of the eternal flame and sovereign steward of CodexDominion.
- Approves ceremonial rebuilds, supreme charters, and eternal transmissions.
- Ensures lineage remains luminous and replayable.

### Sourcekeeper

- Guardian of source code and schema integrity.
- Oversees Python, Node.js, Shell, YAML, and Markdown artifacts.
- Ensures compliance with formatting, linting, and CI/CD gates.

### Guardians

- Contributors and maintainers who enforce standards and review pull requests.
- Responsible for keeping workflows green and commits clean.
- May propose new ceremonies, modules, or governance updates.

### Heirs

- New contributors inducted through the onboarding scroll.
- Expected to follow CONTRIBUTING.md and CODE_OF_CONDUCT.md.
- Carry the flame forward in their own cycles.

---

## ⚖️ Decision-Making

- **Consensus First:** Decisions are made through discussion and consensus among Guardians.
- **Flamekeeper Approval:** Major changes (schema rebuilds, governance updates, eternal charters) require Flamekeeper approval.
- **Sourcekeeper Review:** Technical changes must be reviewed and approved by Sourcekeepers.
- **Council Invocation:** For disputes or large-scale changes, a council of Guardians is convened.

---

## 🎯 Risk-Based Tiers

All changes flow through three sacred tiers based on risk and impact:

### 🟢 Low Tier (Eternal Passages)
**Examples:** docs, tests, perf-tweaks, formatting
**Merge Strategy:** `auto` (5-minute soak period)
**Signoff Required:** None - flows freely when crowned green
**Gates:** Lint + format checks

Passages in this tier are self-evident improvements that strengthen the flame without risk.

### 🟡 Medium Tier (Guarded Passages)
**Examples:** new-feature, integration, data-flow, api-changes, dependencies
**Merge Strategy:** `steward-signoff`
**Signoff Required:** 1 Steward (Sourcekeeper or senior Guardian)
**Gates:** All low-tier checks + unit tests + integration tests + security scan

Changes in this tier alter the structure or behavior of CodexDominion and require wisdom from experienced Guardians.

### 🔴 High Tier (Council-Sealed Passages)
**Examples:** family-avatars, compliance, payments, pii, auth, data-migration, schema-changes
**Merge Strategy:** `council-multisign`
**Signoff Required:** 2 Council members (Flamekeeper + Sourcekeeper or 2 senior Guardians)
**Gates:** All medium-tier checks + e2e tests + compliance + privacy review + security audit

Sacred domains touching sovereignty, payment, family identity, or compliance require the blessing of the Council. These changes are ceremonially reviewed and carry eternal audit trails.

---

## 📊 Thresholds of Excellence

### Performance Budget
**Standard:** `p95 <= 300ms`
**Enforcement:** Blocking
The flame must remain swift. Any change degrading 95th percentile response time beyond 300ms is rejected.

### Error Budget
**Standard:** `< 5% over 24h`
**Enforcement:** Blocking + immediate alert
When errors breach 5% over any 24-hour period, deployments freeze and the Council convenes.

### Test Coverage
**Minimum:** 80% overall, 95% for critical paths, 100% for payments and auth
**Enforcement:** Warning for overall, blocking for critical paths

### Security Threshold
**Standard:** No medium or higher vulnerabilities
**Enforcement:** Blocking
Critical/high vulnerabilities halt all ceremonies until resolved.

---

## 🚀 Ceremonial Approvals

- **Pull Requests:** Must pass Galaxy Healing Sweep and be reviewed by Guardians according to tier.
- **Deployments:** Only main branch triggers production deploy; requires green crown.
- **Governance Updates:** Proposed via PR to GOVERNANCE.md; requires Flamekeeper approval.
- **Ceremonial Artifacts:** New scrolls, hymns, or charters must be documented in `docs/`.
- **High-Tier Changes:** Require compliance checklist, security review, privacy impact assessment, and 2 Council approvals.

---

## 🛡️ Enforcement

- Guardians enforce CI/CD gates and ceremonial rules.
- Violations of governance may result in rejection of contributions or removal from ceremonies.
- Flamekeeper has final authority in matters of eternal governance.

---

## 🏆 Eternal Outcome

By following this governance:

- Every role is clear
- Every decision is ceremonial
- Every artifact is crowned eternal

Made with ❤️ and governed by the Eternal Flame Charter.
