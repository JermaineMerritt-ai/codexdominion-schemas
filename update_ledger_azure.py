#!/usr/bin/env python3
"""
Record Azure deployment in Codex Ledger
"""

import json
from datetime import datetime, timezone

def update_ledger_with_deployment():
    """Add Azure deployment information to the ledger"""

    # Load current ledger
    with open('codex_ledger.json', 'r', encoding='utf-8') as f:
        ledger = json.load(f)

    # Current timestamp
    now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    # Update meta
    ledger['meta']['last_updated'] = now

    # Add new proclamation for Azure deployment
    azure_proclamation = {
        "id": f"PRC-{len(ledger['proclamations']) + 1:03d}",
        "title": "Azure Cloud Deployment Proclamation",
        "status": "proclaimed",
        "issued_by": "Custodian CUS-001",
        "issued_date": now,
        "content": "Codex Dominion successfully deployed to Azure Cloud Platform. Frontend at www.codexdominion.app, Backend API at api.codexdominion.app with SSL certificates. Production operational at $14.37/month."
    }
    ledger['proclamations'].append(azure_proclamation)

    # Add Azure portal to portals
    azure_portal = {
        "name": "azure-production",
        "manifest": "azure/production.yaml",
        "version": "1.0.0",
        "purpose": "Production deployment on Azure Cloud Platform",
        "artifacts": [
            "frontend: https://www.codexdominion.app",
            "backend: https://api.codexdominion.app",
            "static: https://witty-glacier-0ebbd971e.3.azurestaticapps.net",
            "app-service: https://codexdominion-backend.azurewebsites.net"
        ],
        "dashboards": [
            "resource_group: codexdominion-basic",
            "region: West US 2",
            "monthly_cost: $14.37"
        ],
        "timestamp": now,
        "ssl_certificate": {
            "issuer": "GeoTrust Global TLS RSA4096 SHA256 2022 CA1",
            "expires": "2026-04-14T23:59:59+00:00",
            "thumbprint": "9CF9D2306540876319AE47496D8B7CCE4A77B44A",
            "type": "SNI"
        },
        "deployment_token": "STORED_IN_GITHUB_SECRETS"
    }
    ledger['portals'].append(azure_portal)

    # Save updated ledger
    with open('codex_ledger.json', 'w', encoding='utf-8') as f:
        json.dump(ledger, f, indent=2)

    print("✅ Ledger updated with Azure deployment information")
    print(f"📋 Proclamation: {azure_proclamation['id']}")
    print(f"🌐 Portal: azure-production")
    print(f"🔥 Timestamp: {now}")

if __name__ == "__main__":
    update_ledger_with_deployment()
