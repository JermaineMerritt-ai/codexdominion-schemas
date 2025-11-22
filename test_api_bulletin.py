#!/usr/bin/env python3
"""
Test the FastAPI bulletin endpoint
"""

import requests
import json

def test_bulletin_api():
    """Test the /bulletin endpoint"""
    base_url = "http://127.0.0.1:8001"
    
    print("🔥 TESTING FASTAPI BULLETIN ENDPOINT 📊")
    print("=" * 40)
    
    # Test markdown format
    print("\n📝 Testing Markdown format...")
    try:
        response = requests.post(f"{base_url}/bulletin?format=md")
        if response.status_code == 200:
            data = response.json()
            print("✅ Markdown bulletin generated successfully!")
            print(f"Generated at: {data['generated_at']}")
            print(f"Format: {data['format']}")
            print(f"Tier counts: {data['tier_counts']}")
            print("\nFirst 300 characters of content:")
            print(data['content'][:300] + "...")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    # Test text format
    print("\n📝 Testing Text format...")
    try:
        response = requests.post(f"{base_url}/bulletin?format=txt")
        if response.status_code == 200:
            data = response.json()
            print("✅ Text bulletin generated successfully!")
            print(f"Generated at: {data['generated_at']}")
            print(f"Format: {data['format']}")
            print(f"Tier counts: {data['tier_counts']}")
            print("\nFirst 300 characters of content:")
            print(data['content'][:300] + "...")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    # Test health endpoint
    print("\n🏥 Testing Health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed!")
            print(f"Status: {data['status']}")
            print(f"Engine: {data['engine_status']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    test_bulletin_api()