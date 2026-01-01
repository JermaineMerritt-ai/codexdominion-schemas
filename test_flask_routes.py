"""
Test script to verify Flask routes work correctly
"""
import requests
import json

BASE_URL = "http://localhost:5000"

print("="*60)
print("🧪 Testing Flask Dashboard Routes")
print("="*60)

# Test 1: Homepage
print("\n1️⃣ Testing homepage...")
try:
    response = requests.get(f"{BASE_URL}/", timeout=5)
    print(f"   Status: {response.status_code} ✅" if response.status_code == 200 else f"   Status: {response.status_code} ❌")
except Exception as e:
    print(f"   Error: {e} ❌")

# Test 2: Login page
print("\n2️⃣ Testing login page...")
try:
    response = requests.get(f"{BASE_URL}/login", timeout=5)
    print(f"   Status: {response.status_code} ✅" if response.status_code == 200 else f"   Status: {response.status_code} ❌")
except Exception as e:
    print(f"   Error: {e} ❌")

# Test 3: Login with demo credentials
print("\n3️⃣ Testing login with demo credentials...")
try:
    session = requests.Session()
    response = session.post(
        f"{BASE_URL}/login",
        data={"email": "demo@codex.ai", "password": "demo123"},
        timeout=5,
        allow_redirects=False
    )
    print(f"   Status: {response.status_code} ✅" if response.status_code in [200, 302] else f"   Status: {response.status_code} ❌")
    
    # Test 4: Access team library (should work after login)
    print("\n4️⃣ Testing team library access...")
    response = session.get(f"{BASE_URL}/studio/graphics/team/2", timeout=5)
    print(f"   Status: {response.status_code} ✅" if response.status_code == 200 else f"   Status: {response.status_code} ❌")
    
    # Test 5: Access constellation (should work after login)
    print("\n5️⃣ Testing constellation access...")
    response = session.get(f"{BASE_URL}/studio/graphics/team/2/constellation", timeout=5)
    print(f"   Status: {response.status_code} ✅" if response.status_code == 200 else f"   Status: {response.status_code} ❌")
    
    # Test 6: Access AI prompts (should work after login)
    print("\n6️⃣ Testing AI prompt recommendations...")
    response = session.get(f"{BASE_URL}/studio/graphics/recommendations/2/prompts", timeout=5)
    print(f"   Status: {response.status_code} ✅" if response.status_code == 200 else f"   Status: {response.status_code} ❌")
    
except Exception as e:
    print(f"   Error: {e} ❌")

print("\n" + "="*60)
print("🏁 Test Complete!")
print("="*60)
print("\n📌 Next steps:")
print("   1. Go to http://localhost:5000/login")
print("   2. Login with demo@codex.ai / demo123")
print("   3. Visit http://localhost:5000/studio/graphics/team/2/constellation")
print("\n🌠 Enjoy your Creative Constellation!\n")
