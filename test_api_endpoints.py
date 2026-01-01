"""
API Endpoint Testing Script
============================
Tests all Phase 1 Intelligence Core API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_endpoint(method, endpoint, description):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {description}")
            print(f"   {method} {endpoint}")
            if isinstance(data, dict):
                print(f"   Keys: {list(data.keys())[:5]}")
            elif isinstance(data, list):
                print(f"   Count: {len(data)} items")
            return True
        else:
            print(f"❌ {description}")
            print(f"   {method} {endpoint}")
            print(f"   Status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {description}")
        print(f"   {method} {endpoint}")
        print(f"   Error: Connection refused - Is Flask running?")
        return False
    except Exception as e:
        print(f"❌ {description}")
        print(f"   {method} {endpoint}")
        print(f"   Error: {e}")
        return False

print("\n" + "="*70)
print("  INTELLIGENCE CORE - API ENDPOINT TESTING")
print("="*70)
print(f"\nBase URL: {BASE_URL}")
print("Testing all Phase 1 endpoints...\n")

tests = [
    ("GET", "/api/industries", "All Industries"),
    ("GET", "/api/industries/faith_education", "Faith Education Industry"),
    ("GET", "/api/industries/stock_trading", "Stock Trading Industry"),
    ("GET", "/api/niches", "All Niches"),
    ("GET", "/api/niches/industry/faith_education", "Niches by Industry"),
    ("GET", "/api/domain-packs", "All Domain Packs"),
    ("GET", "/api/domain-packs/faith_education_pack", "Faith Education Pack"),
    ("GET", "/api/domain-packs/ecommerce_automation_pack", "E-Commerce Pack"),
    ("GET", "/api/phase-1-status", "Phase 1 Status"),
    ("GET", "/api/cross-reference/faith_education", "Cross-Reference: Faith Education"),
]

passed = 0
failed = 0

for method, endpoint, description in tests:
    if test_endpoint(method, endpoint, description):
        passed += 1
    else:
        failed += 1
    print()

print("="*70)
print(f"Results: {passed} passed, {failed} failed out of {len(tests)} tests")
print("="*70)

if failed == 0:
    print("\n🔥 ALL API ENDPOINTS OPERATIONAL! 👑\n")
else:
    print("\n⚠️  Some endpoints failed. Check Flask server status.\n")
    print("To restart Flask:")
    print("  python flask_dashboard.py\n")
