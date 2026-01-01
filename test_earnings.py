"""
Test earnings tracking features
"""

import requests
import json
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://localhost:5000/api"

def test_earnings():
    print("=" * 80)
    print("  🧪 EARNINGS TRACKING TEST")
    print("=" * 80)
    print()
    
    # Register and login
    print("1. Setting up test user...")
    user_data = {
        "name": "Earnings Tester",
        "email": f"earnings_test_{int(__import__('time').time())}@example.com",
        "password": "TestPassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    if response.status_code != 201:
        print(f"❌ Registration failed: {response.status_code}")
        return False
    
    token = response.json().get('token')
    print(f"✅ User registered")
    
    # Create product
    print("\n2. Creating test product...")
    product_data = {
        "title": "Earnings Test Product",
        "description": "Testing earnings splits",
        "category": "ebook",
        "price": 100.00,
        "fileUrl": "https://example.com/test.pdf"
    }
    
    response = requests.post(
        f"{BASE_URL}/products",
        headers={"Authorization": f"Bearer {token}"},
        json=product_data
    )
    
    if response.status_code != 201:
        print(f"❌ Product creation failed: {response.status_code}")
        return False
    
    product_id = response.json().get('product', {}).get('id')
    print(f"✅ Product created: {product_id}")
    
    # Publish product
    print("\n3. Publishing product...")
    response = requests.patch(
        f"{BASE_URL}/products/{product_id}/status",
        headers={"Authorization": f"Bearer {token}"},
        json={"status": "published"}
    )
    
    if response.status_code != 200:
        print(f"❌ Publishing failed: {response.status_code}")
        return False
    
    print("✅ Product published")
    
    # Test 1: Purchase WITHOUT referrer (creator gets 100%)
    print("\n4. Testing purchase WITHOUT referrer...")
    purchase1 = {
        "productId": product_id,
        "buyerId": None,
        "referrerId": None,
        "paymentMethod": "stripe",
        "orderId": "ORDER-001",
        "status": "paid"
    }
    
    response = requests.post(f"{BASE_URL}/products/purchases", json=purchase1)
    if response.status_code != 201:
        print(f"❌ Purchase 1 failed: {response.status_code}")
        print(response.json())
        return False
    
    data = response.json().get('purchase', {})
    print("✅ Purchase recorded:")
    print(f"   Order ID: {data.get('orderId')}")
    print(f"   Amount: ${data.get('amount')}")
    print(f"   Creator Earning: ${data.get('creatorEarning')} (should be $100)")
    print(f"   Referrer Earning: ${data.get('referrerEarning')} (should be $0)")
    print(f"   Status: {data.get('status')}")
    
    # Verify earnings
    if data.get('creatorEarning') != 100.0:
        print(f"❌ Creator earning incorrect: {data.get('creatorEarning')}")
        return False
    if data.get('referrerEarning') != 0:
        print(f"❌ Referrer earning should be 0: {data.get('referrerEarning')}")
        return False
    
    # Create a second user to be referrer
    print("\n5. Creating referrer user...")
    referrer_data = {
        "name": "Referrer User",
        "email": f"referrer_{int(__import__('time').time())}@example.com",
        "password": "RefPassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=referrer_data)
    if response.status_code != 201:
        print(f"❌ Referrer registration failed: {response.status_code}")
        return False
    
    referrer_id = response.json().get('user', {}).get('id')
    print(f"✅ Referrer created: {referrer_id}")
    
    # Test 2: Purchase WITH referrer (80/20 split)
    print("\n6. Testing purchase WITH referrer...")
    purchase2 = {
        "productId": product_id,
        "buyerId": None,
        "referrerId": referrer_id,
        "paymentMethod": "paypal",
        "orderId": "ORDER-002",
        "status": "paid"
    }
    
    response = requests.post(f"{BASE_URL}/products/purchases", json=purchase2)
    if response.status_code != 201:
        print(f"❌ Purchase 2 failed: {response.status_code}")
        print(response.json())
        return False
    
    data = response.json().get('purchase', {})
    print("✅ Purchase recorded:")
    print(f"   Order ID: {data.get('orderId')}")
    print(f"   Amount: ${data.get('amount')}")
    print(f"   Creator Earning: ${data.get('creatorEarning')} (should be $80)")
    print(f"   Referrer Earning: ${data.get('referrerEarning')} (should be $20)")
    print(f"   Status: {data.get('status')}")
    
    # Verify 80/20 split
    if data.get('creatorEarning') != 80.0:
        print(f"❌ Creator earning incorrect: {data.get('creatorEarning')}, expected 80.0")
        return False
    if data.get('referrerEarning') != 20.0:
        print(f"❌ Referrer earning incorrect: {data.get('referrerEarning')}, expected 20.0")
        return False
    
    # Test analytics
    print("\n7. Testing analytics with earnings breakdown...")
    response = requests.get(f"{BASE_URL}/products/purchases/analytics")
    if response.status_code != 200:
        print(f"❌ Analytics failed: {response.status_code}")
        return False
    
    analytics = response.json().get('analytics', {})
    print("✅ Analytics retrieved:")
    print(f"   Total Revenue: ${analytics.get('totalRevenue')}")
    print(f"   Total Creator Earnings: ${analytics.get('totalCreatorEarnings')}")
    print(f"   Total Referrer Earnings: ${analytics.get('totalReferrerEarnings')}")
    print(f"   Total Purchases: {analytics.get('totalPurchases')}")
    
    referral_stats = analytics.get('referralStats', {})
    print(f"   Referrer Commission: ${referral_stats.get('totalReferrerEarnings', 0)}")
    
    print()
    print("=" * 80)
    print("  ✅ ALL EARNINGS TESTS PASSED!")
    print("=" * 80)
    
    return True


if __name__ == "__main__":
    try:
        success = test_earnings()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
