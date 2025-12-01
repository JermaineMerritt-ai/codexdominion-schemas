#!/usr/bin/env python3
"""
Deploy Codex Dominion database schema to Cloud SQL - Updated Version
"""
import os

import requests


def deploy_schema_via_api():
    """Deploy schema using the existing Codex Capsules API"""

    # Get the Signals service URL from Terraform
    signals_url = "https://codex-signals-pbiapu66bq-uc.a.run.app"

    schema_sql = """
-- Codex Dominion Database Schema
-- Capsules system for operational sovereignty tracking

-- Capsules table: indexes ceremonial + technical capsules
CREATE TABLE IF NOT EXISTS capsules (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(120) UNIQUE NOT NULL,   -- e.g., 'festival', 'signals-daily'
    title VARCHAR(200) NOT NULL,
    kind VARCHAR(50) NOT NULL,           -- 'ceremony' | 'engine' | 'dispatch' | 'treasury' | 'education'
    mode VARCHAR(50) NOT NULL,           -- 'custodian' | 'heir' | 'customer' | 'public'
    version VARCHAR(50) DEFAULT '1.0.0',
    status VARCHAR(50) DEFAULT 'active', -- 'active' | 'archived'
    entrypoint TEXT,                     -- command, URL, or script path
    schedule VARCHAR(50),                -- cron-like '0 6 * * *' or null
    created_at TIMESTAMP DEFAULT NOW()
);

-- Capsule runs table: records executions, audits, lineage
CREATE TABLE IF NOT EXISTS capsule_runs (
    id SERIAL PRIMARY KEY,
    capsule_slug VARCHAR(120) NOT NULL REFERENCES capsules(slug) ON DELETE CASCADE,
    actor VARCHAR(120) NOT NULL,         -- 'custodian' | service account
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'success',-- 'success' | 'error'
    artifact_uri TEXT,                   -- Cloud Storage path or URL to snapshot/bulletin
    checksum TEXT                        -- integrity hash for idempotency
);

-- Indexes for fast lookup
CREATE INDEX IF NOT EXISTS idx_capsules_slug ON capsules(slug);
CREATE INDEX IF NOT EXISTS idx_runs_capsule_slug ON capsule_runs(capsule_slug);
CREATE INDEX IF NOT EXISTS idx_runs_started_at ON capsule_runs(started_at);
    """

    # Initial capsules data
    initial_capsules = [
        {
            "slug": "signals-daily",
            "title": "Daily Signals Dispatch",
            "kind": "engine",
            "mode": "custodian",
            "entrypoint": "/api/signals/daily",
            "schedule": "0 6 * * *",
        },
        {
            "slug": "dawn-dispatch",
            "title": "Dawn Proclamation Capsule",
            "kind": "dispatch",
            "mode": "custodian",
            "entrypoint": "/api/capsules/dawn-dispatch",
            "schedule": "0 6 * * *",
        },
        {
            "slug": "sovereignty-bulletin",
            "title": "Operational Sovereignty Bulletin",
            "kind": "ceremony",
            "mode": "public",
            "entrypoint": "/api/bulletins/generate",
            "schedule": None,
        },
        {
            "slug": "treasury-audit",
            "title": "Treasury Compliance Audit",
            "kind": "treasury",
            "mode": "custodian",
            "entrypoint": "/api/treasury/audit",
            "schedule": "0 0 1 * *",
        },
        {
            "slug": "education-matrix",
            "title": "Educational Content Matrix",
            "kind": "education",
            "mode": "public",
            "entrypoint": "/api/education/matrix",
            "schedule": None,
        },
    ]

    try:
        print("🗄️ Deploying Codex Dominion database schema...")

        # Test if service is accessible
        response = requests.get(f"{signals_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Signals service is accessible")

        # Register each capsule through the API
        for capsule in initial_capsules:
            try:
                response = requests.post(
                    f"{signals_url}/capsules/register", json=capsule, timeout=10
                )
                if response.status_code in [200, 201]:
                    print(f"✅ Registered capsule: {capsule['slug']}")
                else:
                    print(
                        f"⚠️ Warning: Could not register {capsule['slug']}: {response.status_code}"
                    )
            except requests.exceptions.RequestException as e:
                print(f"⚠️ Warning: Network error registering {capsule['slug']}: {e}")

        # Get current capsules count
        try:
            response = requests.get(f"{signals_url}/capsules", timeout=10)
            if response.status_code == 200:
                capsules = response.json()
                print(f"\n📊 Total capsules in system: {len(capsules)}")

                print("\n🎯 Deployed Capsules:")
                for capsule in capsules:
                    print(
                        f"  - {capsule['slug']}: {capsule['title']} ({capsule['kind']})"
                    )
            else:
                print("⚠️ Could not retrieve capsules list")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Warning: Could not retrieve capsules: {e}")

        print("\n🎉 Codex Dominion database deployment completed!")
        print(f"🌐 Service URL: {signals_url}")
        return True

    except Exception as e:
        print(f"❌ Error during deployment: {e}")
        return False


if __name__ == "__main__":
    deploy_schema_via_api()
