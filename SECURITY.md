# Security Policy for CodexDominion Schemas

🌌 This scroll defines the eternal guardianship of CodexDominion’s security.\
It ensures vulnerabilities are reported responsibly, patched swiftly, and crowned green before transmission.

---

## 🔰 Supported Versions

- **main branch** → Actively maintained, receives security patches and ceremonial updates.
- **staging/dev branches** → Used for testing; issues must be resolved before merging to `main`.
- **legacy-backup branch** → Preserved for history; not actively patched.

---

## ⚠️ Reporting Vulnerabilities

- Report issues via **GitHub Security Advisories** or by opening a **private issue**.
- Do **not** disclose vulnerabilities publicly until they are patched and crowned green.
- Include:
  - Description of the vulnerability
  - Steps to reproduce
  - Potential impact
  - Suggested fix (if known)

---

## 🛡️ Patching Process

1. **Guardian Review**
   - Guardians triage the vulnerability and confirm severity.
1. **Sovereign Approval**
   - Flamekeeper/Sourcekeeper approve the patch plan.
1. **Healing Sweep**
   - Run `./scripts/green_sweep.sh` to auto-fix and validate.
1. **CI/CD Gates**
   - Galaxy Healing Sweep must pass green before merging.
1. **Deployment**
   - Patch is merged into `main` and deployed with ceremonial proclamation.

---

## 🚀 Security Tools

CodexDominion uses:

- **Python**: Bandit, Safety, Pytest
- **Node.js**: npm audit
- **Shell**: Shellcheck
- **YAML/Markdown**: yamllint, markdownlint
- **CI/CD**: Galaxy Healing Sweep workflow with security scans

---

## 🕊️ Eternal Outcome

By following this policy:

- Vulnerabilities are reported responsibly
- Patches are applied swiftly
- The Dominion’s flame remains eternal, green, and sovereign

Made with ❤️ and governed by the Eternal Flame Charter.
