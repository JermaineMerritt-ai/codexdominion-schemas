# Security Policy - Authentication & Authorization
# OPA Rego Policy for Codex Dominion Autonomous System

package codex.security

import future.keywords

# Default deny
default allow = false

# Authentication Rules
allow if {
    input.method == "GET"
    public_endpoints[input.path]
}

allow if {
    authenticated_user
    authorized_action
}

# Helper: Check if user is authenticated
authenticated_user if {
    input.user
    input.user.id
    valid_token
}

# Helper: Validate JWT token
valid_token if {
    token := input.headers.authorization
    startswith(token, "Bearer ")
    jwt_valid(trim_prefix(token, "Bearer "))
}

# Helper: Check authorization for action
authorized_action if {
    user_has_permission(input.user, input.action, input.resource)
}

# Role-Based Access Control
user_has_permission(user, action, resource) if {
    role := user_roles[user.id][_]
    permission := role_permissions[role][_]
    permission.action == action
    permission.resource == resource
}

# User Roles Mapping
user_roles := {
    "admin": ["admin", "developer", "operator"],
    "developer": ["developer"],
    "operator": ["operator"],
    "viewer": ["viewer"]
}

# Role Permissions
role_permissions := {
    "admin": [
        {"action": "*", "resource": "*"}
    ],
    "developer": [
        {"action": "read", "resource": "*"},
        {"action": "write", "resource": "code"},
        {"action": "deploy", "resource": "sandbox"},
        {"action": "deploy", "resource": "canary"}
    ],
    "operator": [
        {"action": "read", "resource": "*"},
        {"action": "deploy", "resource": "*"},
        {"action": "rollback", "resource": "*"}
    ],
    "viewer": [
        {"action": "read", "resource": "*"}
    ]
}

# Public Endpoints (no auth required)
public_endpoints := {
    "/health",
    "/api/status",
    "/api/version"
}

# Security Constraints
deny_reasons contains msg if {
    not authenticated_user
    not public_endpoints[input.path]
    msg := "authentication required"
}

deny_reasons contains msg if {
    authenticated_user
    not authorized_action
    msg := "insufficient permissions"
}

deny_reasons contains msg if {
    rate_limit_exceeded
    msg := "rate limit exceeded"
}

# Rate Limiting
rate_limit_exceeded if {
    count(user_requests_last_hour) > 1000
}

# Audit Logging
audit_log := {
    "timestamp": time.now_ns(),
    "user": input.user.id,
    "action": input.action,
    "resource": input.resource,
    "result": allow,
    "deny_reasons": deny_reasons
}
