"""
PRODUCTS API TESTS
======================
Comprehensive tests for product CRUD operations
"""

import requests
import json
import time
import sys
import io

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://localhost:5000/api"
AUTH_URL = f"{BASE_URL}/auth"
PRODUCTS_URL = f"{BASE_URL}/products"

# Test user credentials
TEST_USER = {
    "name": "Product Creator",
    "email": f"creator_{int(time.time())}@example.com",
    "password": "Creator123"
}

# Global token storage
auth_token = None
test_product_id = None


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def print_subheader(text):
    """Print formatted subheader"""
    print(f"\nℹ️  {text}")


def print_success(text):
    """Print success message"""
    print(f"✅ {text}")


def print_error(text):
    """Print error message"""
    print(f"❌ {text}")


def test_setup_authentication():
    """Setup: Register and login user"""
    global auth_token
    
    print_subheader("Setting up authentication...")
    
    # Register user
    response = requests.post(f"{AUTH_URL}/register", json=TEST_USER)
    if response.status_code != 201:
        print_error(f"Registration failed: {response.status_code}")
        return False
    
    data = response.json()
    auth_token = data.get('token')
    
    if not auth_token:
        print_error("No token received")
        return False
    
    print_success(f"Authenticated as {TEST_USER['name']}")
    print(f"   Token: {auth_token[:50]}...")
    return True


def test_create_product():
    """Test creating a new product"""
    global test_product_id
    
    print_subheader("Testing product creation...")
    
    product_data = {
        "title": "Amazing Ebook - Test Product",
        "description": "This is a comprehensive ebook about building digital products and growing your online business. Perfect for creators!",
        "category": "ebook",
        "price": 29.99,
        "fileUrl": "https://example.com/files/amazing-ebook.pdf"
    }
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(PRODUCTS_URL, json=product_data, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 201 and data.get('success'):
            test_product_id = data['product']['id']
            print_success("Product created successfully!")
            print(f"   Product ID: {test_product_id}")
            print(f"   Title: {data['product']['title']}")
            print(f"   Price: ${data['product']['price']}")
            return True
        else:
            print_error(f"Creation failed: {data.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_list_products():
    """Test listing all products"""
    print_subheader("Testing product listing...")
    
    response = requests.get(PRODUCTS_URL)
    
    print(f"Status Code: {response.status_code}")
    
    try:
        data = response.json()
        
        if response.status_code == 200 and data.get('success'):
            products = data['products']
            pagination = data['pagination']
            
            print(f"Response: Found {len(products)} products")
            print(f"Pagination: Page {pagination['page']} of {pagination['pages']}, Total: {pagination['total']}")
            
            if products:
                print("\nFirst Product:")
                print(f"   {json.dumps(products[0], indent=2)}")
            
            print_success("Product listing successful!")
            return True
        else:
            print_error(f"Listing failed: {data.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_get_product():
    """Test getting a single product"""
    print_subheader("Testing get single product...")
    
    if not test_product_id:
        print_error("No test product ID available")
        return False
    
    response = requests.get(f"{PRODUCTS_URL}/{test_product_id}")
    
    print(f"Status Code: {response.status_code}")
    
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200 and data.get('success'):
            print_success("Get product successful!")
            print(f"   Title: {data['product']['title']}")
            print(f"   Category: {data['product']['category']}")
            return True
        else:
            print_error(f"Get product failed: {data.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_update_product():
    """Test updating a product"""
    print_subheader("Testing product update...")
    
    if not test_product_id:
        print_error("No test product ID available")
        return False
    
    update_data = {
        "title": "Amazing Ebook - UPDATED",
        "price": 34.99
    }
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.put(f"{PRODUCTS_URL}/{test_product_id}", json=update_data, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200 and data.get('success'):
            print_success("Product updated successfully!")
            print(f"   New Title: {data['product']['title']}")
            print(f"   New Price: ${data['product']['price']}")
            return True
        else:
            print_error(f"Update failed: {data.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_filter_by_category():
    """Test filtering products by category"""
    print_subheader("Testing category filter...")
    
    response = requests.get(f"{PRODUCTS_URL}?category=ebook&limit=5")
    
    print(f"Status Code: {response.status_code}")
    
    try:
        data = response.json()
        
        if response.status_code == 200 and data.get('success'):
            products = data['products']
            print(f"Found {len(products)} ebooks")
            
            # Verify all are ebooks
            all_ebooks = all(p['category'] == 'ebook' for p in products)
            if all_ebooks:
                print_success("Category filter working correctly!")
                return True
            else:
                print_error("Some products have wrong category")
                return False
        else:
            print_error(f"Filter failed: {data.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_unauthorized_update():
    """Test updating product without authentication"""
    print_subheader("Testing unauthorized update (should fail)...")
    
    if not test_product_id:
        print_error("No test product ID available")
        return False
    
    update_data = {"title": "Hacked Title"}
    response = requests.put(f"{PRODUCTS_URL}/{test_product_id}", json=update_data)
    
    print(f"Status Code: {response.status_code}")
    
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 401:
            print_success("Unauthorized update correctly rejected!")
            return True
        else:
            print_error("Security issue: Unauthorized update was allowed!")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_validation_errors():
    """Test validation errors"""
    print_subheader("Testing validation errors...")
    
    # Test with invalid data
    invalid_product = {
        "title": "AB",  # Too short
        "description": "Short",  # Too short
        "category": "invalid",  # Invalid category
        "price": -10,  # Negative price
        "fileUrl": "bad"  # Invalid URL
    }
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(PRODUCTS_URL, json=invalid_product, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 400:
            print_success("Validation errors correctly detected!")
            print(f"   Error: {data.get('error')}")
            return True
        else:
            print_error("Validation should have failed!")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_update_product_status():
    """Test updating product status"""
    print_subheader("Testing product status update...")
    
    if not test_product_id:
        print_error("No test product ID available")
        return False
    
    # First, create a new product for status testing
    product_data = {
        "title": "Status Test Product",
        "description": "This product is for testing status updates",
        "category": "template",
        "price": 19.99,
        "fileUrl": "https://example.com/files/template.zip"
    }
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    create_response = requests.post(PRODUCTS_URL, json=product_data, headers=headers)
    
    if create_response.status_code != 201:
        print_error("Failed to create test product")
        return False
    
    new_product_id = create_response.json()['product']['id']
    print(f"Created test product: {new_product_id}")
    
    # Update status to published
    status_data = {
        "productId": new_product_id,
        "status": "published"
    }
    
    response = requests.patch(f"{PRODUCTS_URL}/{new_product_id}/status", json=status_data, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200 and data.get('success'):
            if data['product']['status'] == 'published':
                print_success("Product status updated to published!")
                print(f"   Previous: {data.get('previousStatus', 'pending')}")
                print(f"   Current: {data['product']['status']}")
                
                # Clean up - delete test product
                requests.delete(f"{PRODUCTS_URL}/{new_product_id}", headers=headers)
                return True
            else:
                print_error("Status not updated correctly")
                return False
        else:
            print_error(f"Status update failed: {data.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_invalid_status():
    """Test updating with invalid status"""
    print_subheader("Testing invalid status value (should fail)...")
    
    if not test_product_id:
        print_error("No test product ID available")
        return False
    
    status_data = {
        "productId": test_product_id,
        "status": "invalid_status"
    }
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.patch(f"{PRODUCTS_URL}/{test_product_id}/status", json=status_data, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 400:
            print_success("Invalid status correctly rejected!")
            print(f"   Error: {data.get('error')}")
            return True
        else:
            print_error("Invalid status should have been rejected!")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_track_product_share():
    """Test tracking product share"""
    print_subheader("Testing product share tracking...")
    
    if not test_product_id:
        print_error("No test product ID available")
        return False
    
    # Track share on WhatsApp
    share_data = {
        "userId": "user_test",
        "productId": test_product_id,
        "channel": "whatsapp"
    }
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{PRODUCTS_URL}/{test_product_id}/share", json=share_data, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 201 and data.get('success'):
            print_success("Share tracked successfully!")
            print(f"   Share ID: {data['share']['id']}")
            print(f"   Channel: {data['share']['channel']}")
            
            # Track another share on Instagram
            share_data2 = {
                "userId": "user_test",
                "productId": test_product_id,
                "channel": "instagram"
            }
            requests.post(f"{PRODUCTS_URL}/{test_product_id}/share", json=share_data2, headers=headers)
            
            # Track share on TikTok
            share_data3 = {
                "userId": "user_test",
                "productId": test_product_id,
                "channel": "tiktok"
            }
            requests.post(f"{PRODUCTS_URL}/{test_product_id}/share", json=share_data3, headers=headers)
            
            return True
        else:
            print_error(f"Share tracking failed: {data.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_product_analytics():
    """Test getting product analytics"""
    print_subheader("Testing product analytics...")
    
    if not test_product_id:
        print_error("No test product ID available")
        return False
    
    response = requests.get(f"{PRODUCTS_URL}/{test_product_id}/analytics")
    
    print(f"Status Code: {response.status_code}")
    
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200 and data.get('success'):
            analytics = data['analytics']
            print_success("Analytics retrieved successfully!")
            print(f"   Total Shares: {analytics['totalShares']}")
            print(f"   Unique Sharers: {analytics['uniqueSharers']}")
            print(f"   WhatsApp: {analytics['channelBreakdown']['whatsapp']}")
            print(f"   Instagram: {analytics['channelBreakdown']['instagram']}")
            print(f"   TikTok: {analytics['channelBreakdown']['tiktok']}")
            
            # Verify we have the shares we tracked
            if analytics['totalShares'] >= 3:
                print_success("All shares recorded correctly!")
                return True
            else:
                print_error(f"Expected at least 3 shares, got {analytics['totalShares']}")
                return False
        else:
            print_error(f"Analytics retrieval failed: {data.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_invalid_share_channel():
    """Test tracking share with invalid channel"""
    print_subheader("Testing invalid share channel (should fail)...")
    
    if not test_product_id:
        print_error("No test product ID available")
        return False
    
    share_data = {
        "userId": "user_test",
        "productId": test_product_id,
        "channel": "invalid_channel"
    }
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{PRODUCTS_URL}/{test_product_id}/share", json=share_data, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 400:
            print_success("Invalid channel correctly rejected!")
            print(f"   Error: {data.get('error')}")
            return True
        else:
            print_error("Invalid channel should have been rejected!")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_delete_product():
    """Test deleting a product"""
    print_subheader("Testing product deletion...")
    
    if not test_product_id:
        print_error("No test product ID available")
        return False
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.delete(f"{PRODUCTS_URL}/{test_product_id}", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200 and data.get('success'):
            print_success("Product deleted successfully!")
            
            # Verify it's gone
            verify_response = requests.get(f"{PRODUCTS_URL}/{test_product_id}")
            if verify_response.status_code == 404:
                print_success("Verified: Product no longer exists")
                return True
            else:
                print_error("Product still exists after deletion")
                return False
        else:
            print_error(f"Deletion failed: {data.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def run_all_tests():
    """Run all product API tests"""
    print_header("🔥 CODEX DOMINION - PRODUCTS API TESTS")
    print(f"\nℹ️  Testing against: {PRODUCTS_URL}")
    print(f"ℹ️  Test User: {TEST_USER['name']} ({TEST_USER['email']})")
    
    tests = [
        ("Setup Authentication", test_setup_authentication),
        ("Create Product", test_create_product),
        ("List Products", test_list_products),
        ("Get Single Product", test_get_product),
        ("Update Product", test_update_product),
        ("Update Product Status", test_update_product_status),
        ("Invalid Status Value", test_invalid_status),
        ("Track Product Share", test_track_product_share),
        ("Product Analytics", test_product_analytics),
        ("Invalid Share Channel", test_invalid_share_channel),
        ("Filter by Category", test_filter_by_category),
        ("Unauthorized Update", test_unauthorized_update),
        ("Validation Errors", test_validation_errors),
        ("Delete Product", test_delete_product),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"{name} crashed: {str(e)}")
            results.append((name, False))
    
    # Summary
    print_header("📊 TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    failed = len(results) - passed
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\n✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"\nTotal: {len(results)} tests")
    
    if failed == 0:
        print("\n✅ 🎉 All tests passed! Products API is working correctly.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Review output above for details.")


def test_record_purchase():
    """Test recording a product purchase"""
    global test_product_id
    
    print_subheader("Testing purchase recording...")
    
    # Create a new product specifically for purchase testing
    product_data = {
        "title": "Purchase Test Product",
        "description": "Product created for testing purchase tracking",
        "category": "ebook",
        "price": 49.99,
        "fileUrl": "https://example.com/purchase-test.pdf"
    }
    
    response = requests.post(
        PRODUCTS_URL,
        headers={"Authorization": f"Bearer {auth_token}"},
        json=product_data
    )
    
    if response.status_code != 201:
        print_error(f"Failed to create test product: {response.status_code}")
        return False
    
    purchase_test_product_id = response.json().get('product', {}).get('id')
    
    # Publish the product
    response = requests.patch(
        f"{PRODUCTS_URL}/{purchase_test_product_id}/status",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"status": "published"}
    )
    
    if response.status_code != 200:
        print_error(f"Failed to publish product: {response.status_code}")
        return False
    
    # Test 1: Record purchase with buyer and referrer
    purchase_data = {
        "productId": purchase_test_product_id,
        "buyerId": TEST_USER.get("userId"),  # We'll use the creator as buyer for testing
        "referrerId": None,
        "paymentMethod": "stripe"
    }
    
    response = requests.post(f"{PRODUCTS_URL}/purchases", json=purchase_data)
    
    if response.status_code != 201:
        print_error(f"Purchase recording failed: {response.status_code}")
        print(response.json())
        return False
    
    data = response.json()
    if not data.get('success'):
        print_error(f"Purchase recording unsuccessful: {data.get('error')}")
        return False
    
    purchase = data.get('purchase')
    if not purchase:
        print_error("No purchase data returned")
        return False
    
    print_success(f"Purchase recorded: {purchase.get('id')}")
    print(f"   Product: {purchase.get('productId')}")
    print(f"   Amount: ${purchase.get('amount')}")
    print(f"   Payment Method: {purchase.get('paymentMethod')}")
    
    # Test 2: Record guest purchase (no buyer ID)
    guest_purchase_data = {
        "productId": purchase_test_product_id,
        "buyerId": None,
        "referrerId": None,
        "paymentMethod": "paypal"
    }
    
    response = requests.post(f"{PRODUCTS_URL}/purchases", json=guest_purchase_data)
    
    if response.status_code != 201:
        print_error(f"Guest purchase failed: {response.status_code}")
        return False
    
    data = response.json()
    if not data.get('success'):
        print_error(f"Guest purchase unsuccessful: {data.get('error')}")
        return False
    
    print_success("Guest purchase recorded successfully")
    
    return True


def test_purchase_analytics():
    """Test purchase analytics endpoint"""
    print_subheader("Testing purchase analytics...")
    
    # Get overall analytics
    response = requests.get(f"{PRODUCTS_URL}/purchases/analytics")
    
    if response.status_code != 200:
        print_error(f"Analytics request failed: {response.status_code}")
        return False
    
    data = response.json()
    if not data.get('success'):
        print_error(f"Analytics unsuccessful: {data.get('error')}")
        return False
    
    analytics = data.get('analytics')
    if not analytics:
        print_error("No analytics data returned")
        return False
    
    print_success("Analytics retrieved successfully")
    print(f"   Total Revenue: ${analytics.get('totalRevenue', 0)}")
    print(f"   Total Purchases: {analytics.get('totalPurchases', 0)}")
    print(f"   Average Order Value: ${analytics.get('averageOrderValue', 0)}")
    
    # Check revenue by payment method
    revenue_by_method = analytics.get('revenueByPaymentMethod', {})
    if revenue_by_method:
        print("   Revenue by Payment Method:")
        for method, stats in revenue_by_method.items():
            print(f"      {method}: ${stats.get('revenue', 0)} ({stats.get('count', 0)} purchases)")
    
    # Check referral stats
    referral_stats = analytics.get('referralStats', {})
    if referral_stats:
        print("   Referral Stats:")
        print(f"      Referred Purchases: {referral_stats.get('totalReferredPurchases', 0)}")
        print(f"      Referral Revenue: ${referral_stats.get('totalReferralRevenue', 0)}")
        print(f"      Non-Referred Purchases: {referral_stats.get('nonReferredPurchases', 0)}")
    
    return True


def test_product_purchases():
    """Test getting purchases for a specific product"""
    global test_product_id
    
    print_subheader("Testing product-specific purchases...")
    
    # Create a product with purchases for testing
    product_data = {
        "title": "Product Purchases Test",
        "description": "Product for testing purchase retrieval",
        "category": "template",
        "price": 19.99,
        "fileUrl": "https://example.com/template-test.zip"
    }
    
    response = requests.post(
        PRODUCTS_URL,
        headers={"Authorization": f"Bearer {auth_token}"},
        json=product_data
    )
    
    if response.status_code != 201:
        print_error(f"Failed to create test product: {response.status_code}")
        return False
    
    test_purchase_product_id = response.json().get('product', {}).get('id')
    
    # Publish it
    requests.patch(
        f"{PRODUCTS_URL}/{test_purchase_product_id}/status",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"status": "published"}
    )
    
    # Add a purchase
    requests.post(f"{PRODUCTS_URL}/purchases", json={
        "productId": test_purchase_product_id,
        "buyerId": None,
        "paymentMethod": "stripe"
    })
    
    # Get purchases for product (requires auth)
    response = requests.get(
        f"{PRODUCTS_URL}/{test_purchase_product_id}/purchases",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    if response.status_code != 200:
        print_error(f"Product purchases request failed: {response.status_code}")
        return False
    
    data = response.json()
    if not data.get('success'):
        print_error(f"Product purchases unsuccessful: {data.get('error')}")
        return False
    
    print_success("Product purchases retrieved")
    print(f"   Total Purchases: {data.get('totalPurchases', 0)}")
    print(f"   Total Revenue: ${data.get('totalRevenue', 0)}")
    
    purchases = data.get('purchases', [])
    if purchases:
        print(f"   Recent Purchases: {len(purchases)}")
        for purchase in purchases[:3]:  # Show first 3
            print(f"      - ${purchase.get('amount')} via {purchase.get('paymentMethod')}")
    
    return True


def test_invalid_purchase():
    """Test error handling for invalid purchase attempts"""
    print_subheader("Testing invalid purchase scenarios...")
    
    # Test 1: Missing product ID
    response = requests.post(f"{PRODUCTS_URL}/purchases", json={
        "paymentMethod": "stripe"
    })
    
    if response.status_code != 400:
        print_error(f"Missing productId should return 400, got {response.status_code}")
        return False
    
    print_success("Missing productId rejected correctly")
    
    # Test 2: Missing payment method
    response = requests.post(f"{PRODUCTS_URL}/purchases", json={
        "productId": test_product_id
    })
    
    if response.status_code != 400:
        print_error(f"Missing paymentMethod should return 400, got {response.status_code}")
        return False
    
    print_success("Missing paymentMethod rejected correctly")
    
    # Test 3: Invalid product ID
    response = requests.post(f"{PRODUCTS_URL}/purchases", json={
        "productId": "invalid_product_123",
        "paymentMethod": "stripe"
    })
    
    if response.status_code != 404:
        print_error(f"Invalid productId should return 404, got {response.status_code}")
        return False
    
    print_success("Invalid productId rejected correctly")
    
    return True


def test_purchase_date_filtering():
    """Test analytics with date filtering"""
    print_subheader("Testing purchase analytics date filtering...")
    
    from datetime import datetime, timedelta
    
    # Get analytics for last 7 days
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    
    response = requests.get(
        f"{PRODUCTS_URL}/purchases/analytics",
        params={
            "startDate": start_date.isoformat() + "Z",
            "endDate": end_date.isoformat() + "Z"
        }
    )
    
    if response.status_code != 200:
        print_error(f"Date filtering failed: {response.status_code}")
        return False
    
    data = response.json()
    if not data.get('success'):
        print_error(f"Date filtering unsuccessful: {data.get('error')}")
        return False
    
    analytics = data.get('analytics')
    print_success("Date filtering working")
    print(f"   Purchases in last 7 days: {analytics.get('totalPurchases', 0)}")
    print(f"   Revenue in last 7 days: ${analytics.get('totalRevenue', 0)}")
    
    return True


def run_purchase_tests():
    """Run all purchase-related tests"""
    print_header("🧪 PURCHASE TRACKING TESTS")
    
    tests = [
        ("Record Purchase", test_record_purchase),
        ("Purchase Analytics", test_purchase_analytics),
        ("Product Purchases", test_product_purchases),
        ("Invalid Purchase", test_invalid_purchase),
        ("Date Filtering", test_purchase_date_filtering),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"{name} crashed: {str(e)}")
            results.append((name, False))
    
    # Summary
    print_header("📊 PURCHASE TESTS SUMMARY")
    passed = sum(1 for _, result in results if result)
    failed = len(results) - passed
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\n✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"\nTotal: {len(results)} purchase tests")
    
    return failed == 0


if __name__ == "__main__":
    # First run original tests
    run_all_tests()
    
    # Then run purchase tests
    time.sleep(2)  # Brief pause between test suites
    purchase_success = run_purchase_tests()
    
    if purchase_success:
        print("\n🎉 All tests (products + purchases) passed!")
    else:
        print("\n⚠️  Some purchase tests failed. Review output above.")
