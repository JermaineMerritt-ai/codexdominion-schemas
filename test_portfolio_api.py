"""Test script for Portfolio API"""
import requests
import json

BASE_URL = "http://localhost:8095"

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    print("🏥 Health Check:")
    print(json.dumps(response.json(), indent=2))
    print()

def test_register():
    data = {
        "email": "user@example.com",
        "password": "mypassword",
        "risk_profile": "moderate"
    }
    response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
    print("✅ Register User:")
    print(json.dumps(response.json(), indent=2))
    print()

def test_create_portfolio():
    data = {
        "user_id": 42,
        "name": "Aggressive Growth",
        "risk_profile": "aggressive"
    }
    response = requests.post(f"{BASE_URL}/api/portfolios", json=data)
    print("📁 Create Portfolio:")
    print(json.dumps(response.json(), indent=2))
    print()
    return response.json()["id"]

def test_get_portfolios():
    response = requests.get(f"{BASE_URL}/api/portfolios")
    print("📊 Get All Portfolios:")
    print(json.dumps(response.json(), indent=2))
    print()

def test_risk_profiles():
    response = requests.get(f"{BASE_URL}/api/risk-profiles")
    print("⚠️  Risk Profiles:")
    print(json.dumps(response.json(), indent=2))
    print()

if __name__ == "__main__":
    print("🔥 Codex Portfolio API - Test Suite 👑\n")

    try:
        test_health()
        test_register()
        test_risk_profiles()
        portfolio_id = test_create_portfolio()
        test_get_portfolios()
        print("\n✅ All tests passed! 🔥")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
