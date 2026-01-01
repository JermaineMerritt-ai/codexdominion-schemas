# 🏛️ DominionMarkets Governance, Compliance & Audit Framework

> **Extracted from copilot-instructions.md - Sections 30-34**
> **Last Updated:** December 25, 2025
> **Status:** Production Guidelines

## 🎯 Core Governance Principles

DominionMarkets follows **five core governance principles** that guide all development decisions:

### 1. Transparency
Users understand what the platform does and why.
- All data collection purposes must be clearly documented
- System behavior must be explainable and auditable
- Privacy policies and terms must be accessible and clear
- Dashboard interfaces show what data is used and how

### 2. Accountability
Every system has an owner and audit trail.
- All workflows track `created_by_agent` and timestamps
- Database models include audit fields: `created_at`, `updated_at`, `created_by`
- Changes to critical systems require council review (see `workflow_engine.py` COUNCIL_RULES)
- Audit logs captured in `AuditLog` model (models.py)

### 3. Safety
No predictions, no recommendations, no sensitive profiling.
- **NEVER** implement predictive algorithms for user behavior
- **NEVER** create recommendation engines that profile users
- **NEVER** collect or store sensitive personal data without explicit consent
- AI agents provide tools and insights, NOT decisions or predictions

### 4. Compliance
All systems align with relevant laws and best practices.
- GDPR compliance for EU users (data minimization, right to deletion)
- CCPA compliance for California users (data transparency)
- Financial regulations for treasury operations (SOX, PCI-DSS where applicable)
- Accessibility standards (WCAG 2.1 AA minimum)
- Security best practices (OWASP Top 10, CSP headers, input validation)

### 5. Stewardship
Data is handled with care, respect, and minimalism.
- Collect only what is needed (principle of data minimization)
- Store data securely (encryption at rest and in transit)
- Delete data when no longer needed (automated retention policies)
- User privacy is paramount (no data selling, no third-party tracking)
- Graceful degradation when data is unavailable

## 📋 Pre-Deployment Governance Checklist

Before deploying any feature:
- [ ] **Data Minimization**: Only necessary data collected?
- [ ] **Audit Logging**: Critical actions logged in `AuditLog`?
- [ ] **No Predictions**: Feature avoids predictive algorithms?
- [ ] **No Profiling**: No sensitive user profiling or categorization?
- [ ] **Error Handling**: Graceful failure without exposing sensitive data?
- [ ] **Documentation**: Changes documented in relevant docs?
- [ ] **Testing**: Unit tests and integration tests pass?
- [ ] **Security**: Input validation, SQL injection prevention, XSS protection?
- [ ] **Accessibility**: UI follows WCAG 2.1 AA standards?
- [ ] **Council Review**: High-impact changes approved by relevant council?

## 🔐 Security Best Practices

### Input Validation Pattern
```python
from flask import request, jsonify
import re

@app.route('/api/store/<store_id>')
def get_store(store_id):
    # Validate input format
    if not re.match(r'^[a-zA-Z0-9_-]+$', store_id):
        return jsonify({"error": "Invalid store ID"}), 400
    
    # Use parameterized queries (prevents SQL injection)
    session = SessionLocal()
    try:
        store = session.query(Store).filter_by(id=store_id).first()
        if not store:
            return jsonify({"error": "Store not found"}), 404
        return jsonify(store.to_dict())
    finally:
        session.close()
```

### Secrets Management Pattern
```python
# ✅ GOOD: Environment variables
import os
api_key = os.getenv("STRIPE_SECRET_KEY")

# ❌ BAD: Hardcoded secrets
api_key = "sk_live_abc123..."  # NEVER do this

# ✅ GOOD: Config file pattern
from config import config
database_url = config.DATABASE_URL  # Loaded from .env
```

## 📊 Data Governance

### Data Classification Schema
```python
class DataClassification(enum.Enum):
    PUBLIC = "public"              # Public information
    INTERNAL = "internal"          # Internal business data
    CONFIDENTIAL = "confidential"  # User data, financial records
    RESTRICTED = "restricted"      # Authentication, payment info
```

### Data Retention Policies
```python
DATA_RETENTION_POLICIES = {
    "audit_logs": timedelta(days=365 * 7),  # 7 years (SOX compliance)
    "user_sessions": timedelta(days=30),
    "workflow_history": timedelta(days=365 * 2),  # 2 years
    "analytics_data": timedelta(days=90),
    "temporary_uploads": timedelta(days=7)
}
```

## 🛡️ Compliance Framework

### Required Compliance Standards
- **GDPR**: EU General Data Protection Regulation (data protection)
- **CCPA**: California Consumer Privacy Act (consumer rights)
- **SOX**: Sarbanes-Oxley (financial reporting)
- **PCI-DSS**: Payment Card Industry (payment security)
- **WCAG**: Web Content Accessibility Guidelines (accessibility)

### Data Subject Rights Implementation
```python
DATA_SUBJECT_RIGHTS = [
    "right_to_access",       # Export all data
    "right_to_rectify",      # Correct inaccurate data
    "right_to_erasure",      # Delete all data
    "right_to_restrict",     # Limit data processing
    "right_to_portability",  # Transfer data to another service
    "right_to_object"        # Opt-out of specific processing
]
```

## 📝 Audit Framework

### Mandatory Audit Events
```python
MANDATORY_AUDIT_EVENTS = [
    # Authentication & Authorization
    "user_login", "user_logout", "login_failed",
    "password_changed", "mfa_enabled", "mfa_disabled",
    
    # Data Operations
    "data_accessed", "data_modified", "data_deleted",
    "data_exported", "data_imported",
    
    # Financial Operations
    "transaction_created", "payment_processed",
    "refund_issued", "budget_allocated",
    
    # System Configuration
    "config_changed", "feature_flag_toggled",
    "secret_rotated", "integration_added",
    
    # Compliance Events
    "gdpr_request", "ccpa_request", "data_breach_detected",
    "compliance_check_failed"
]
```

### Audit Log Pattern
```python
def create_audit_log_enhanced(
    action: str,
    user_id: str,
    details: dict,
    severity: str = "info"
):
    """Create audit log with governance metadata"""
    session = SessionLocal()
    try:
        # Verify action is mandatory
        if action in MANDATORY_AUDIT_EVENTS:
            details["mandatory_event"] = True
        
        # Add contextual information
        details.update({
            "ip_address": request.remote_addr if request else None,
            "user_agent": request.headers.get("User-Agent") if request else None,
            "session_id": session.get("session_id"),
            "severity": severity
        })
        
        audit = AuditLog(
            user_id=user_id,
            action=action,
            details=details,
            timestamp=datetime.utcnow()
        )
        session.add(audit)
        session.commit()
        
        # Alert on high-severity events
        if severity in ["critical", "high"]:
            notify_council("council_security", {
                "type": "audit_alert",
                "action": action,
                "user_id": user_id,
                "severity": severity
            })
    finally:
        session.close()
```

## 🔄 Incident Response

### Incident Categories
- **Security**: Auth failures, unauthorized access attempts
- **Data**: Data corruption, integrity violations
- **Performance**: Slow queries, timeouts, resource exhaustion
- **Provider outage**: Third-party API failures
- **Billing**: Payment processing errors

### Incident Workflow
1. **Detection**: Automated monitoring or user report
2. **Containment**: Isolate affected systems
3. **Resolution**: Fix root cause
4. **User notification**: Inform affected users (if needed)
5. **Post-incident review**: Document lessons learned

## 📈 Security Review Cadence

- **Monthly**: Vulnerability scans (automated)
- **Quarterly**: Penetration tests (external security firm)
- **Annual**: Full security audit (comprehensive review)

## 🎯 Council Responsibilities

### Council Types
- **Council Security**: Security policies, incident response
- **Council Finance**: Treasury operations, budget allocation
- **Council Product**: Feature approval, UX consistency
- **Council Compliance**: Regulatory oversight, audit trails

### High-Impact Workflows Requiring Council Review
```python
high_impact_workflows = [
    "budget_allocation",      # Financial impact
    "user_data_export",       # Privacy impact
    "system_configuration",   # Security impact
    "pricing_change",         # Revenue impact
]
```

---

**For implementation details, see:**
- Main copilot instructions: `.github/copilot-instructions.md`
- Architecture patterns: `ARCHITECTURE_PATTERNS.md`
- Deployment guide: `DEPLOYMENT_GUIDE.md`

🔥 **The Flame Burns Sovereign and Eternal!** 👑
