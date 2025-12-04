# License Compliance Policy
# OPA Rego Policy for dependency license validation

package codex.license

import future.keywords

# Default deny unknown licenses
default allow = false

# Allowed Licenses
allowed_licenses := {
    "MIT",
    "Apache-2.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "ISC",
    "0BSD",
    "CC0-1.0"
}

# Conditionally Allowed (requires review)
conditional_licenses := {
    "GPL-3.0",
    "LGPL-3.0",
    "MPL-2.0",
    "EPL-2.0"
}

# Blocked Licenses
blocked_licenses := {
    "AGPL-3.0",
    "SSPL",
    "Commons Clause",
    "Proprietary"
}

# Allow if license is in allowed list
allow if {
    some license in input.dependencies[_].licenses
    allowed_licenses[license]
}

# Conditional approval with manual review flag
allow if {
    some license in input.dependencies[_].licenses
    conditional_licenses[license]
    input.manual_review == true
}

# Deny reasons
deny_reasons contains msg if {
    some dep in input.dependencies
    some license in dep.licenses
    blocked_licenses[license]
    msg := sprintf("Blocked license %s in package %s", [license, dep.name])
}

deny_reasons contains msg if {
    some dep in input.dependencies
    some license in dep.licenses
    conditional_licenses[license]
    not input.manual_review
    msg := sprintf("License %s in package %s requires manual review", [license, dep.name])
}

deny_reasons contains msg if {
    some dep in input.dependencies
    count(dep.licenses) == 0
    msg := sprintf("Package %s has no license information", [dep.name])
}

# License compatibility check
compatible_with_mit if {
    every dep in input.dependencies {
        some license in dep.licenses
        allowed_licenses[license]
    }
}

# Generate license report
license_report := {
    "allowed": [dep |
        some dep in input.dependencies
        some license in dep.licenses
        allowed_licenses[license]
    ],
    "conditional": [dep |
        some dep in input.dependencies
        some license in dep.licenses
        conditional_licenses[license]
    ],
    "blocked": [dep |
        some dep in input.dependencies
        some license in dep.licenses
        blocked_licenses[license]
    ],
    "unknown": [dep |
        some dep in input.dependencies
        count(dep.licenses) == 0
    ]
}
