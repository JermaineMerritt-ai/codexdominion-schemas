---
name: Drift Detected
about: Automated drift detection alert
title: '[DRIFT] Fact re-verification required'
labels: drift, fact-check, urgent
assignees: ''
---

## 🚨 Drift Detection Alert

**Automated drift monitoring has detected potential discrepancies in verified facts.**

### Details

- **Detection Time**: {{ env.GITHUB_RUN_TIMESTAMP }}
- **Workflow Run**: {{ env.GITHUB_RUN_ID }}
- **Branch**: {{ env.GITHUB_REF }}

### Action Required

The drift monitor has flagged facts that may need re-verification. Please review the workflow logs and take appropriate action.

### Next Steps

1. Review the drift monitor logs
2. Re-verify flagged facts using updated sources
3. Update fact database if needed
4. Close this issue once verified

### Links

- [Workflow Run]({{ env.GITHUB_SERVER_URL }}/{{ env.GITHUB_REPOSITORY }}/actions/runs/{{ env.GITHUB_RUN_ID }})
- [Drift Monitor Documentation](../docs/drift-monitoring.md)

---

**This is an automated issue created by the Codex Dominion drift monitoring system.**
