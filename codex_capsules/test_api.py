# codex_capsules/test_api.py
"""
Test script for Codex Capsules API
Run with: python test_api.py
"""

import json
from datetime import datetime

import requests

# Base URL - adjust for your deployment
BASE_URL = "http://localhost:8080/api"


def test_capsules_api():
    print("🧪 Testing Codex Capsules API...")

    # Test 1: Register a capsule
    print("\n1. Registering test capsule...")
    capsule_data = {
        "slug": "test-ceremony",
        "title": "Test Ceremonial Operation",
        "kind": "ceremony",
        "mode": "manual",
        "version": "1.0.0",
        "status": "active",
        "entrypoint": "python ceremony_test.py",
        "schedule": "0 9 * * *",
    }

    response = requests.post(f"{BASE_URL}/capsules", json=capsule_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"✅ Capsule registered: {response.json()['slug']}")
    else:
        print(f"❌ Error: {response.text}")
        return

    # Test 2: List capsules
    print("\n2. Listing capsules...")
    response = requests.get(f"{BASE_URL}/capsules")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        capsules = response.json()
        print(f"✅ Found {len(capsules)} capsules")
        for capsule in capsules:
            print(f"   - {capsule['slug']}: {capsule['title']}")

    # Test 3: Record a run
    print("\n3. Recording test run...")
    run_data = {
        "capsule_slug": "test-ceremony",
        "actor": "test-user",
        "status": "success",
        "artifact_uri": "https://storage.googleapis.com/codex-artifacts/test-ceremony-123.tar.gz",
        "checksum": "sha256:abc123...",
    }

    response = requests.post(f"{BASE_URL}/capsules/run", json=run_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"✅ Run recorded: {response.json()['id']}")

    # Test 4: List runs
    print("\n4. Listing runs...")
    response = requests.get(f"{BASE_URL}/capsules/runs")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        runs = response.json()
        print(f"✅ Found {len(runs)} runs")
        for run in runs:
            print(f"   - {run['capsule_slug']}: {run['status']} by {run['actor']}")

    # Test 5: Performance metrics
    print("\n5. Getting performance metrics...")
    response = requests.get(f"{BASE_URL}/capsules/performance")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        performance = response.json()
        print(f"✅ Performance data for {len(performance)} capsules")

    # Test 6: Scheduled capsules
    print("\n6. Getting scheduled capsules...")
    response = requests.get(f"{BASE_URL}/capsules/scheduled")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        scheduled = response.json()
        print(f"✅ Found {len(scheduled)} scheduled capsules")

    print("\n🎉 API tests completed!")


if __name__ == "__main__":
    try:
        test_capsules_api()
    except requests.exceptions.ConnectionError:
        print(
            "❌ Connection error. Make sure the API is running at http://localhost:8080"
        )
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
