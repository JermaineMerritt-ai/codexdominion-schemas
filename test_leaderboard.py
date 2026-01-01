"""
Test Leaderboard System

Tests:
1. Create multiple users
2. Create products and make purchases
3. Generate varied earnings for different users
4. Test weekly leaderboard
5. Test monthly leaderboard
6. Test current user ranking
7. Test badges system
8. Test limit parameter
"""

import requests
import time
import sys
import io

# Fix Windows Unicode issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://localhost:5000/api"


def create_user_and_product(user_number):
    """Helper: Create a user with a product"""
    user_data = {
        "name": f"User {user_number}",
        "email": f"user{user_number}_{int(time.time())}@example.com",
        "password": "UserPass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    if response.status_code != 201:
        print(f"❌ User {user_number} registration failed: {response.status_code}")
        return None, None, None
    
    user_id = response.json().get('user', {}).get('id')
    token = response.json().get('token')
    
    # Create product
    product_data = {
        "title": f"Product from User {user_number}",
        "description": f"Test product #{user_number}",
        "category": "ebook",
        "price": 100.00,
        "fileUrl": f"https://example.com/product{user_number}.pdf",
        "creatorId": user_id
    }
    
    response = requests.post(
        f"{BASE_URL}/products",
        json=product_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code != 201:
        print(f"❌ Product creation failed for user {user_number}")
        return user_id, token, None
    
    product_id = response.json().get('product', {}).get('id')
    
    # Publish product
    response = requests.patch(
        f"{BASE_URL}/products/{product_id}/status",
        json={"status": "published"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    return user_id, token, product_id


def make_purchase(product_id, referrer_id=None):
    """Helper: Record a purchase"""
    purchase_data = {
        "productId": product_id,
        "buyerId": None,
        "referrerId": referrer_id,
        "paymentMethod": "stripe",
        "orderId": f"LEADERBOARD-{int(time.time() * 1000)}",
        "status": "paid"
    }
    
    response = requests.post(f"{BASE_URL}/products/purchases", json=purchase_data)
    return response.status_code == 201


def test_leaderboard():
    """Run complete leaderboard system tests"""
    
    print("="*80)
    print("  🏆 LEADERBOARD SYSTEM TEST")
    print("="*80 + "\n")
    
    # Step 1: Create 5 users with products
    print("1. Setting up 5 users with products...")
    users = []
    for i in range(1, 6):
        user_id, token, product_id = create_user_and_product(i)
        if user_id and product_id:
            users.append({
                'id': user_id,
                'token': token,
                'product_id': product_id,
                'number': i
            })
            print(f"   ✅ User {i} created: {user_id}")
    
    if len(users) < 5:
        print(f"❌ Failed to create all users. Only {len(users)} created.")
        return False
    
    # Step 2: Generate purchases to create varied earnings
    print("\n2. Generating purchases for leaderboard data...")
    
    # User 1: 5 sales as creator (5 * $80 = $400)
    print("   - User 1: 5 sales as creator...")
    for _ in range(5):
        make_purchase(users[0]['product_id'])
    
    # User 2: 3 sales as creator + 2 referrals (3 * $80 + 2 * $20 = $280)
    print("   - User 2: 3 sales as creator + 2 referrals...")
    for _ in range(3):
        make_purchase(users[1]['product_id'])
    make_purchase(users[0]['product_id'], users[1]['id'])
    make_purchase(users[0]['product_id'], users[1]['id'])
    
    # User 3: 10 referrals (10 * $20 = $200) - Top Referrer!
    print("   - User 3: 10 referrals (Top Referrer)...")
    for _ in range(10):
        make_purchase(users[0]['product_id'], users[2]['id'])
    
    # User 4: 1 sale as creator ($80)
    print("   - User 4: 1 sale as creator...")
    make_purchase(users[3]['product_id'])
    
    # User 5: No sales ($0) - Not in leaderboard
    print("   - User 5: No sales...")
    
    print("   ✅ All purchases generated")
    
    # Step 3: Test weekly leaderboard
    print("\n3. Testing weekly leaderboard...")
    response = requests.get(f"{BASE_URL}/products/leaderboard?period=week")
    if response.status_code != 200:
        print(f"❌ Leaderboard request failed: {response.status_code}")
        print(response.json())
        return False
    
    data = response.json()
    entries = data.get('entries', [])
    
    print(f"✅ Leaderboard retrieved ({len(entries)} users):")
    for entry in entries:
        badges_str = ', '.join(entry.get('badges', []))
        print(f"   #{entry.get('rank')}: {entry.get('username')} - ${entry.get('earnings')} [{badges_str}]")
    
    # Verify rankings
    if len(entries) < 4:
        print(f"❌ Expected at least 4 users in leaderboard, got {len(entries)}")
        return False
    
    # Find our test users in the leaderboard
    user1_entry = next((e for e in entries if e['userId'] == users[0]['id']), None)
    user2_entry = next((e for e in entries if e['userId'] == users[1]['id']), None)
    user3_entry = next((e for e in entries if e['userId'] == users[2]['id']), None)
    user4_entry = next((e for e in entries if e['userId'] == users[3]['id']), None)
    
    if not user1_entry or not user2_entry or not user3_entry or not user4_entry:
        print(f"❌ Not all test users found in leaderboard")
        return False
    
    # User 1 should have highest earnings of our test users
    if user1_entry['earnings'] < user2_entry['earnings']:
        print(f"❌ User 1 should have more earnings than User 2")
        return False
    
    # Check User 1 has earned at least $400 from this test
    if user1_entry['earnings'] < 400.0:
        print(f"❌ User 1 should have at least $400, got ${user1_entry['earnings']}")
        return False
    
    print(f"   ✅ User 1 ranked #{user1_entry['rank']} with ${user1_entry['earnings']}")
    
    # Check badges are present
    if 'first-sale' not in user1_entry['badges']:
        print(f"❌ User 1 missing 'first-sale' badge")
        return False
    
    if 'top-10' not in user1_entry['badges']:
        print(f"❌ User 1 missing 'top-10' badge")
        return False
    
    print("   ✅ User 1 has correct badges (top-10, first-sale)")
    
    # User 2 should have earned at least $280
    if user2_entry['earnings'] < 280.0:
        print(f"❌ User 2 should have at least $280, got ${user2_entry['earnings']}")
        return False
    
    print(f"   ✅ User 2 ranked #{user2_entry['rank']} with ${user2_entry['earnings']}")
    
    # User 3 should have earned at least $200 (all from referrals)
    if user3_entry['earnings'] < 200.0:
        print(f"❌ User 3 should have at least $200, got ${user3_entry['earnings']}")
        return False
    
    print(f"   ✅ User 3 ranked #{user3_entry['rank']} with ${user3_entry['earnings']}")
    
    # Step 4: Test currentUser parameter
    print("\n4. Testing currentUser parameter...")
    response = requests.get(
        f"{BASE_URL}/products/leaderboard?period=week&currentUserId={users[3]['id']}"
    )
    if response.status_code != 200:
        print(f"❌ Leaderboard request failed: {response.status_code}")
        return False
    
    data = response.json()
    current_user = data.get('currentUser')
    
    if not current_user:
        print(f"❌ currentUser not found in response")
        return False
    
    print(f"✅ Current user tracking:")
    print(f"   User: {current_user.get('username')}")
    print(f"   Rank: #{current_user.get('rank')}")
    print(f"   Earnings: ${current_user.get('earnings')}")
    print(f"   Badges: {', '.join(current_user.get('badges', []))}")
    
    if current_user['userId'] != users[3]['id']:
        print(f"❌ Current user ID mismatch")
        return False
    
    # User 4 should have at least $100 from this test
    if current_user['earnings'] < 100.0:
        print(f"❌ User 4 should have at least $100, got ${current_user['earnings']}")
        return False
    
    # Step 5: Test badges
    print("\n5. Testing badge system...")
    
    # Our test users should have 'first-sale' badge
    test_user_entries = [user1_entry, user2_entry, user3_entry, user4_entry]
    for entry in test_user_entries:
        if 'first-sale' not in entry['badges']:
            print(f"❌ User {entry['username']} missing 'first-sale' badge")
            return False
    
    print("   ✅ All test users have 'first-sale' badge")
    
    # Users in top 10 should have 'top-10' badge
    for entry in entries[:min(10, len(entries))]:
        if 'top-10' not in entry['badges']:
            print(f"❌ User {entry['username']} in top 10 missing 'top-10' badge")
            return False
    
    print("   ✅ All top 10 users have 'top-10' badge")
    
    # Step 6: Test limit parameter
    print("\n6. Testing limit parameter...")
    response = requests.get(f"{BASE_URL}/products/leaderboard?period=week&limit=2")
    if response.status_code != 200:
        print(f"❌ Leaderboard request failed: {response.status_code}")
        return False
    
    data = response.json()
    entries = data.get('entries', [])
    
    if len(entries) != 2:
        print(f"❌ Expected 2 entries with limit=2, got {len(entries)}")
        return False
    
    print(f"✅ Limit parameter working (returned {len(entries)} entries)")
    
    # Step 7: Test monthly period
    print("\n7. Testing monthly period...")
    response = requests.get(f"{BASE_URL}/products/leaderboard?period=month")
    if response.status_code != 200:
        print(f"❌ Monthly leaderboard request failed: {response.status_code}")
        return False
    
    data = response.json()
    
    if data.get('period') != 'month':
        print(f"❌ Period should be 'month', got '{data.get('period')}'")
        return False
    
    print(f"✅ Monthly leaderboard working")
    
    # Step 8: Test invalid period
    print("\n8. Testing invalid period validation...")
    response = requests.get(f"{BASE_URL}/products/leaderboard?period=year")
    if response.status_code != 400:
        print(f"❌ Should reject invalid period with 400")
        return False
    
    print(f"✅ Invalid period properly rejected")
    
    # Step 9: Test totalUsers count
    print("\n9. Testing totalUsers count...")
    response = requests.get(f"{BASE_URL}/products/leaderboard?period=week")
    data = response.json()
    
    total_users = data.get('totalUsers')
    if total_users < 4:  # Should have at least our 4 test users
        print(f"❌ Expected at least 4 total users, got {total_users}")
        return False
    
    print(f"✅ Total users count: {total_users} (includes historical data)")
    
    print("\n" + "="*80)
    print("  ✅ ALL LEADERBOARD TESTS PASSED!")
    print("="*80)
    
    return True


if __name__ == '__main__':
    try:
        success = test_leaderboard()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
