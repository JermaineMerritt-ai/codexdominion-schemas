#!/usr/bin/env python3
"""
🔥 CODEX SIGNALS CONTAINER TEST 📊
Test the containerized API locally

The Merritt Method™ - Container Verification
"""

import json
import sys
import time

import requests


def test_container():
    """Test the locally running container"""
    base_url = "http://localhost:8000"

    print("🔥 CODEX SIGNALS CONTAINER TEST 📊")
    print("=" * 40)

    # Wait for container to start
    print("⏳ Waiting for container to start...")
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{base_url}/", timeout=2)
            if response.status_code == 200:
                print("✅ Container is responding")
                break
        except requests.exceptions.RequestException:
            pass

        time.sleep(1)
        if attempt == max_attempts - 1:
            print("❌ Container failed to start within 30 seconds")
            return False

    # Test endpoints
    endpoints = [
        ("/", "Root endpoint"),
        ("/health", "Health check"),
        ("/docs", "API documentation"),
        ("/signals/mock", "Mock signals"),
    ]

    print("\n📊 Testing endpoints...")
    success_count = 0

    for endpoint, description in endpoints:
        try:
            if endpoint == "/bulletin":
                response = requests.post(f"{base_url}{endpoint}?format=md", timeout=10)
            else:
                response = requests.get(f"{base_url}{endpoint}", timeout=10)

            if response.status_code == 200:
                print(f"✅ {description}: {response.status_code}")
                success_count += 1
            else:
                print(f"❌ {description}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {description}: Connection error - {e}")

    # Test bulletin endpoint specifically
    print("\n📝 Testing bulletin generation...")
    try:
        response = requests.post(f"{base_url}/bulletin?format=md", timeout=15)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Bulletin generated: {data['format']} format")
            print(f"   Tier counts: {data['tier_counts']}")
            print(f"   Content length: {len(data['content'])} characters")
            success_count += 1
        else:
            print(f"❌ Bulletin generation failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Bulletin test failed: {e}")

    print("\n" + "=" * 40)
    print(f"🎯 Test Results: {success_count}/{len(endpoints)+1} endpoints working")

    if success_count >= len(endpoints):
        print("✅ Container test PASSED")
        print("\n🌐 API available at: http://localhost:8000")
        print("📚 Documentation: http://localhost:8000/docs")
        return True
    else:
        print("❌ Container test FAILED")
        return False


if __name__ == "__main__":
    success = test_container()
    sys.exit(0 if success else 1)
