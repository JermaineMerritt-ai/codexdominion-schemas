"""
Test Withdrawal/Payout System

Tests:
1. Create user and product, make purchase to generate earnings
2. Check user balance
3. Request withdrawal
4. Update withdrawal status (processing → completed)
5. Verify balance updated after withdrawal
6. Test insufficient funds
7. Test withdrawal history
8. Test failed withdrawal
"""

import requests
import time
import sys
import io

# Fix Windows Unicode issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://localhost:5000/api"


def test_withdrawals():
    """Run complete withdrawal system tests"""
    
    print("="*80)
    print("  🧪 WITHDRAWAL/PAYOUT SYSTEM TEST")
    print("="*80 + "\n")
    
    # Step 1: Create user (creator)
    print("1. Setting up creator user...")
    user_data = {
        "name": "Creator User",
        "email": f"creator_{int(time.time())}@example.com",
        "password": "CreatorPass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    if response.status_code != 201:
        print(f"❌ Creator registration failed: {response.status_code}")
        return False
    
    creator_id = response.json().get('user', {}).get('id')
    creator_token = response.json().get('token')
    print(f"✅ Creator registered: {creator_id}")
    
    # Step 2: Create product
    print("\n2. Creating product...")
    product_data = {
        "title": "Test Ebook for Withdrawal Test",
        "description": "A digital product to test the withdrawal system",
        "category": "ebook",
        "price": 100.00,
        "fileUrl": "https://example.com/test-ebook.pdf",
        "creatorId": creator_id
    }
    
    response = requests.post(
        f"{BASE_URL}/products",
        json=product_data,
        headers={"Authorization": f"Bearer {creator_token}"}
    )
    if response.status_code != 201:
        print(f"❌ Product creation failed: {response.status_code}")
        print(response.json())
        return False
    
    product_id = response.json().get('product', {}).get('id')
    print(f"✅ Product created: {product_id}")
    
    # Step 3: Publish product
    print("\n3. Publishing product...")
    response = requests.patch(
        f"{BASE_URL}/products/{product_id}/status",
        json={"status": "published"},
        headers={"Authorization": f"Bearer {creator_token}"}
    )
    if response.status_code != 200:
        print(f"❌ Product publish failed: {response.status_code}")
        return False
    
    print("✅ Product published")
    
    # Step 4: Create referrer user
    print("\n4. Creating referrer user...")
    referrer_data = {
        "name": "Referrer User",
        "email": f"referrer_{int(time.time())}@example.com",
        "password": "ReferrerPass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=referrer_data)
    if response.status_code != 201:
        print(f"❌ Referrer registration failed: {response.status_code}")
        return False
    
    referrer_id = response.json().get('user', {}).get('id')
    print(f"✅ Referrer created: {referrer_id}")
    
    # Step 5: Record purchase with referrer (generates earnings)
    print("\n5. Recording purchase with referrer...")
    purchase_data = {
        "productId": product_id,
        "buyerId": None,
        "referrerId": referrer_id,
        "paymentMethod": "stripe",
        "orderId": "WITHDRAW-TEST-001",
        "status": "paid"
    }
    
    response = requests.post(f"{BASE_URL}/products/purchases", json=purchase_data)
    if response.status_code != 201:
        print(f"❌ Purchase failed: {response.status_code}")
        print(response.json())
        return False
    
    purchase = response.json().get('purchase', {})
    print(f"✅ Purchase recorded:")
    print(f"   Creator Earning: ${purchase.get('creatorEarning')} (should be $80)")
    print(f"   Referrer Earning: ${purchase.get('referrerEarning')} (should be $20)")
    
    # Step 6: Check creator balance
    print("\n6. Checking creator balance...")
    response = requests.get(f"{BASE_URL}/products/users/{creator_id}/balance")
    if response.status_code != 200:
        print(f"❌ Get balance failed: {response.status_code}")
        print(response.json() if response.headers.get('content-type') == 'application/json' else response.text)
        return False
    
    balance = response.json().get('balance', {})
    print(f"✅ Creator balance:")
    print(f"   Available: ${balance.get('availableBalance')}")
    print(f"   Total Earnings: ${balance.get('totalEarnings')}")
    print(f"   Creator Earnings: ${balance.get('creatorEarnings')}")
    print(f"   Referrer Earnings: ${balance.get('referrerEarnings')}")
    
    if balance.get('creatorEarnings') != 80.0:
        print(f"❌ Creator earnings mismatch! Expected $80, got ${balance.get('creatorEarnings')}")
        return False
    
    # Step 7: Check referrer balance
    print("\n7. Checking referrer balance...")
    response = requests.get(f"{BASE_URL}/products/users/{referrer_id}/balance")
    if response.status_code != 200:
        print(f"❌ Get balance failed: {response.status_code}")
        return False
    
    balance = response.json().get('balance', {})
    print(f"✅ Referrer balance:")
    print(f"   Available: ${balance.get('availableBalance')}")
    print(f"   Referrer Earnings: ${balance.get('referrerEarnings')}")
    
    if balance.get('referrerEarnings') != 20.0:
        print(f"❌ Referrer earnings mismatch! Expected $20, got ${balance.get('referrerEarnings')}")
        return False
    
    # Step 8: Test insufficient funds withdrawal
    print("\n8. Testing insufficient funds withdrawal...")
    withdrawal_data = {
        "userId": creator_id,
        "amount": 1000.00,  # More than available
        "destination": "paypal",
        "destinationDetails": {"email": "creator@paypal.com"}
    }
    
    response = requests.post(f"{BASE_URL}/products/withdrawals", json=withdrawal_data)
    if response.status_code != 400:
        print(f"❌ Should have rejected insufficient funds!")
        return False
    
    print(f"✅ Insufficient funds properly rejected:")
    print(f"   {response.json().get('error')}")
    
    # Step 9: Request valid withdrawal (creator - $50)
    print("\n9. Requesting creator withdrawal ($50)...")
    withdrawal_data = {
        "userId": creator_id,
        "amount": 50.00,
        "destination": "paypal",
        "destinationDetails": {"email": "creator@paypal.com"}
    }
    
    response = requests.post(f"{BASE_URL}/products/withdrawals", json=withdrawal_data)
    if response.status_code != 201:
        print(f"❌ Withdrawal request failed: {response.status_code}")
        print(response.json())
        return False
    
    withdrawal1 = response.json().get('withdrawal', {})
    withdrawal1_id = withdrawal1.get('id')
    print(f"✅ Withdrawal requested:")
    print(f"   ID: {withdrawal1_id}")
    print(f"   Amount: ${withdrawal1.get('amount')}")
    print(f"   Status: {withdrawal1.get('status')}")
    print(f"   Remaining Balance: ${response.json().get('availableBalance')}")
    
    if withdrawal1.get('status') != 'pending':
        print(f"❌ Status should be 'pending', got '{withdrawal1.get('status')}'")
        return False
    
    # Step 10: Request referrer withdrawal ($15)
    print("\n10. Requesting referrer withdrawal ($15)...")
    withdrawal_data = {
        "userId": referrer_id,
        "amount": 15.00,
        "destination": "stripe",
        "destinationDetails": {"accountId": "acct_123456"}
    }
    
    response = requests.post(f"{BASE_URL}/products/withdrawals", json=withdrawal_data)
    if response.status_code != 201:
        print(f"❌ Withdrawal request failed: {response.status_code}")
        return False
    
    withdrawal2 = response.json().get('withdrawal', {})
    withdrawal2_id = withdrawal2.get('id')
    print(f"✅ Withdrawal requested:")
    print(f"   ID: {withdrawal2_id}")
    print(f"   Amount: ${withdrawal2.get('amount')}")
    
    # Step 11: Update withdrawal status to processing
    print("\n11. Updating withdrawal to 'processing'...")
    response = requests.patch(
        f"{BASE_URL}/products/withdrawals/{withdrawal1_id}",
        json={"status": "processing"}
    )
    if response.status_code != 200:
        print(f"❌ Status update failed: {response.status_code}")
        return False
    
    withdrawal = response.json().get('withdrawal', {})
    print(f"✅ Status updated to: {withdrawal.get('status')}")
    
    # Step 12: Update withdrawal status to completed
    print("\n12. Updating withdrawal to 'completed'...")
    response = requests.patch(
        f"{BASE_URL}/products/withdrawals/{withdrawal1_id}",
        json={"status": "completed"}
    )
    if response.status_code != 200:
        print(f"❌ Status update failed: {response.status_code}")
        return False
    
    withdrawal = response.json().get('withdrawal', {})
    print(f"✅ Status updated to: {withdrawal.get('status')}")
    print(f"   Processed At: {withdrawal.get('processedAt')}")
    
    # Step 13: Verify balance updated
    print("\n13. Verifying updated balance...")
    response = requests.get(f"{BASE_URL}/products/users/{creator_id}/balance")
    if response.status_code != 200:
        print(f"❌ Get balance failed: {response.status_code}")
        return False
    
    balance = response.json().get('balance', {})
    print(f"✅ Updated creator balance:")
    print(f"   Available: ${balance.get('availableBalance')} (should be $30 = $80 - $50)")
    print(f"   Total Withdrawn: ${balance.get('totalWithdrawn')}")
    print(f"   Pending: ${balance.get('pendingWithdrawals')}")
    
    expected_available = 80.0 - 50.0  # $30
    if abs(balance.get('availableBalance') - expected_available) > 0.01:
        print(f"❌ Balance mismatch! Expected ${expected_available}, got ${balance.get('availableBalance')}")
        return False
    
    # Step 14: Test failed withdrawal
    print("\n14. Testing failed withdrawal...")
    response = requests.patch(
        f"{BASE_URL}/products/withdrawals/{withdrawal2_id}",
        json={"status": "failed", "failureReason": "Invalid payment account"}
    )
    if response.status_code != 200:
        print(f"❌ Status update failed: {response.status_code}")
        return False
    
    withdrawal = response.json().get('withdrawal', {})
    print(f"✅ Withdrawal marked as failed:")
    print(f"   Status: {withdrawal.get('status')}")
    print(f"   Reason: {withdrawal.get('failureReason')}")
    
    # Step 15: Get withdrawal history
    print("\n15. Getting creator withdrawal history...")
    response = requests.get(f"{BASE_URL}/products/users/{creator_id}/withdrawals")
    if response.status_code != 200:
        print(f"❌ Get history failed: {response.status_code}")
        return False
    
    withdrawals = response.json().get('withdrawals', [])
    total = response.json().get('pagination', {}).get('total')
    print(f"✅ Withdrawal history retrieved:")
    print(f"   Total Withdrawals: {total}")
    for w in withdrawals:
        print(f"   - {w.get('id')}: ${w.get('amount')} ({w.get('status')})")
    
    # Step 16: Filter by status
    print("\n16. Filtering by completed status...")
    response = requests.get(f"{BASE_URL}/products/users/{creator_id}/withdrawals?status=completed")
    if response.status_code != 200:
        print(f"❌ Get history failed: {response.status_code}")
        return False
    
    withdrawals = response.json().get('withdrawals', [])
    print(f"✅ Completed withdrawals: {len(withdrawals)}")
    
    print("\n" + "="*80)
    print("  ✅ ALL WITHDRAWAL TESTS PASSED!")
    print("="*80)
    
    return True


if __name__ == '__main__':
    try:
        success = test_withdrawals()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
