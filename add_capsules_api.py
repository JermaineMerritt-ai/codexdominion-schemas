"""
Add production capsules via backend API
"""
import requests
import json

API_BASE = "http://codex-api-eastus.eastus.azurecontainer.io:8000"

# Production capsules
capsules = [
    {
        "slug": "daily-signal-001",
        "title": "Daily Sovereign Signal",
        "kind": "dispatch",
        "mode": "recurring",
        "engine": "gpt-4o-mini",
        "user_role": "heir",
        "content": "Dawn breaks. Sovereignty restored. Continue the watch."
    },
    {
        "slug": "sovereignty-bulletin",
        "title": "Sovereignty Council Bulletin",
        "kind": "decree",
        "mode": "scheduled",
        "engine": "gpt-4o",
        "user_role": "council",
        "content": "Council convenes. Decisions sealed. Eternal flame burns."
    },
    {
        "slug": "treasury-report",
        "title": "Treasury Audit Report",
        "kind": "analysis",
        "mode": "periodic",
        "engine": "gpt-4",
        "user_role": "custodian",
        "content": "Financial review complete. All accounts balanced."
    },
    {
        "slug": "dawn-dispatch",
        "title": "Dawn Dispatch Capsule",
        "kind": "notification",
        "mode": "recurring",
        "engine": "gpt-4o-mini",
        "user_role": "heir",
        "content": "Morning briefing: All systems operational. Archive integrity confirmed."
    },
    {
        "slug": "education-matrix",
        "title": "Educational Matrix Capsule",
        "kind": "knowledge",
        "mode": "scheduled",
        "engine": "gpt-4o",
        "user_role": "observer",
        "content": "Knowledge compilation: Historical data indexed and cross-referenced."
    }
]

print("📦 Adding capsules via backend API...\n")

for capsule in capsules:
    try:
        # For now, just verify API is accessible
        # Backend needs a POST endpoint to create capsules
        print(f"• {capsule['slug']}: Prepared")
    except Exception as e:
        print(f"✗ Error: {e}")

print(f"\n✓ {len(capsules)} capsules prepared")
print("\nNote: Backend needs POST /api/capsules endpoint to insert via API")
print("Database service exists but not exposed via API endpoint yet")
