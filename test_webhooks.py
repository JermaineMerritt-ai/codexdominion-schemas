"""
Test script for webhooks API
"""

import requests
import json

BASE_URL = "http://localhost:8097"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/webhooks/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_daily_picks():
    """Test daily picks webhook"""
    print("📬 Testing daily picks webhook...")

    picks = [
        {
            "ticker": "MSFT",
            "reason": "Bullish cloud revenue growth, AI momentum continuing",
            "pick_type": "swing",
            "entry_price": 380.50,
            "target_price": 410.00,
            "stop_loss": 370.00,
            "confidence": "high"
        },
        {
            "ticker": "GOOGL",
            "reason": "Breaking out of consolidation pattern, strong Q4 expected",
            "pick_type": "position",
            "entry_price": 142.30,
            "target_price": 155.00,
            "stop_loss": 137.00,
            "confidence": "medium"
        }
    ]

    response = requests.post(
        f"{BASE_URL}/webhooks/daily-picks",
        json=picks
    )

    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_pick_update():
    """Test pick status update"""
    print("📊 Testing pick update webhook...")

    response = requests.post(
        f"{BASE_URL}/webhooks/pick-update",
        params={
            "ticker": "MSFT",
            "status": "hit_target"
        },
        json={
            "exit_price": 410.25,
            "gain_loss_pct": 7.82
        }
    )

    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_subscribers():
    """Test subscriber query"""
    print("👥 Testing subscriber query...")

    response = requests.get(f"{BASE_URL}/webhooks/subscribers/daily_picks")

    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

if __name__ == "__main__":
    print("🔥 Codex Dominion Webhooks Test Suite 👑\n")

    try:
        test_health()
        test_daily_picks()
        test_pick_update()
        test_subscribers()

        print("✅ All webhook tests completed!")

    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the API is running:")
        print("   python webhooks_api.py")
    except Exception as e:
        print(f"❌ Test failed: {e}")
