# Data Privacy & GDPR Compliance Policy
# OPA Rego Policy for data handling

package codex.privacy

import future.keywords

# Default deny data processing
default allow = false

# Personal Data Categories
personal_data_categories := {
    "identity": ["name", "email", "phone", "address"],
    "financial": ["credit_card", "bank_account", "payment_info"],
    "health": ["medical_records", "health_data"],
    "biometric": ["fingerprint", "face_scan", "voice"],
    "location": ["gps_coordinates", "ip_address"],
    "online": ["cookies", "browsing_history", "device_id"]
}

# Consent Requirements
allow if {
    input.data_category == "non_personal"
}

allow if {
    input.data_category != "non_personal"
    valid_consent
    lawful_basis
    purpose_limitation
}

# Valid Consent Check
valid_consent if {
    input.consent.given == true
    input.consent.timestamp
    input.consent.version == current_consent_version
    not input.consent.withdrawn
}

# Lawful Basis (GDPR Article 6)
lawful_basis if {
    input.legal_basis in {
        "consent",
        "contract",
        "legal_obligation",
        "vital_interests",
        "public_task",
        "legitimate_interests"
    }
}

# Purpose Limitation (GDPR Article 5)
purpose_limitation if {
    input.purpose in allowed_purposes
    input.purpose == input.consent.purpose
}

allowed_purposes := {
    "service_provision",
    "analytics",
    "marketing",
    "security",
    "compliance"
}

# Data Minimization
data_minimization_violated if {
    count(input.fields_collected) > count(input.fields_required)
}

# Storage Limitation
retention_exceeded if {
    retention_period := data_retention_periods[input.data_category]
    current_time := time.now_ns()
    data_age := current_time - input.data_created
    data_age > retention_period
}

# Data retention periods (in nanoseconds)
data_retention_periods := {
    "identity": 63072000000000000,      # 2 years
    "financial": 94608000000000000,     # 3 years
    "analytics": 2592000000000000,      # 30 days
    "marketing": 31536000000000000      # 1 year
}

# Right to Access
allow_access if {
    input.action == "data_access"
    input.user.id == input.data_subject_id
}

# Right to Erasure (Right to be Forgotten)
allow_erasure if {
    input.action == "data_erasure"
    input.user.id == input.data_subject_id
    erasure_conditions_met
}

erasure_conditions_met if {
    input.consent.withdrawn == true
}

erasure_conditions_met if {
    retention_exceeded
}

# Data Portability
allow_export if {
    input.action == "data_export"
    input.user.id == input.data_subject_id
    input.format in {"json", "csv", "xml"}
}

# Cross-Border Transfer
allow_transfer if {
    input.action == "cross_border_transfer"
    destination_adequate
    appropriate_safeguards
}

destination_adequate if {
    input.destination_country in adequate_countries
}

adequate_countries := {
    "EU", "EEA", "UK", "Switzerland", "Canada",
    "Japan", "South Korea", "New Zealand"
}

appropriate_safeguards if {
    input.safeguards.standard_contractual_clauses == true
}

appropriate_safeguards if {
    input.safeguards.binding_corporate_rules == true
}

# Security Measures Required
required_security_measures := {
    "encryption_at_rest",
    "encryption_in_transit",
    "access_control",
    "audit_logging",
    "pseudonymization"
}

security_compliant if {
    every measure in required_security_measures {
        input.security_measures[measure] == true
    }
}

# Deny Reasons
deny_reasons contains msg if {
    not valid_consent
    msg := "Valid consent required"
}

deny_reasons contains msg if {
    data_minimization_violated
    msg := "Data minimization principle violated"
}

deny_reasons contains msg if {
    retention_exceeded
    msg := "Data retention period exceeded"
}

deny_reasons contains msg if {
    not security_compliant
    msg := "Required security measures not implemented"
}

# Privacy Impact Assessment Required
pia_required if {
    input.data_category in {"health", "biometric", "financial"}
}

pia_required if {
    input.processing_type == "automated_decision_making"
}

pia_required if {
    input.data_subjects_count > 10000
}

# Compliance Report
compliance_report := {
    "gdpr_compliant": allow,
    "consent_valid": valid_consent,
    "lawful_basis": lawful_basis,
    "purpose_limitation": purpose_limitation,
    "data_minimization": not data_minimization_violated,
    "storage_limitation": not retention_exceeded,
    "security_compliant": security_compliant,
    "pia_required": pia_required,
    "deny_reasons": deny_reasons
}

# Current consent version
current_consent_version := "2.0.0"
