"""
🧪 AUTHENTICATION API TESTS
============================
Quick tests for user registration, login, and authentication endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000/api/auth"

# Test colors
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_success(message):
    print(f"{GREEN}✅ {message}{RESET}")

def print_error(message):
    print(f"{RED}❌ {message}{RESET}")

def print_info(message):
    print(f"{BLUE}ℹ️  {message}{RESET}")

# Test data
test_user = {
    "name": "Test User",
    "email": f"test_{int(time.time())}@example.com",  # Unique email
    "password": "TestPass123"
}

import time

def test_registration():
    """Test user registration"""
    print_info("Testing registration...")
    
    # Update email to be unique
    test_user["email"] = f"test_{int(time.time())}@example.com"
    
    response = requests.post(
        f"{BASE_URL}/register",
        json=test_user,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        data = response.json()
        if data["success"]:
            print_success("Registration successful!")
            print_info(f"User ID: {data['user']['id']}")
            print_info(f"Token: {data['token'][:50]}...")
            return data["token"]
        else:
            print_error(f"Registration failed: {data['error']}")
            return None
    else:
        print_error(f"Registration failed with status {response.status_code}")
        return None

def test_login():
    """Test user login"""
    print_info("\nTesting login...")
    
    response = requests.post(
        f"{BASE_URL}/login",
        json={
            "email": test_user["email"],
            "password": test_user["password"]
        },
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            print_success("Login successful!")
            return data["token"]
        else:
            print_error(f"Login failed: {data['error']}")
            return None
    else:
        print_error(f"Login failed with status {response.status_code}")
        return None

def test_verify_token(token):
    """Test token verification"""
    print_info("\nTesting token verification...")
    
    response = requests.get(
        f"{BASE_URL}/verify",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            print_success("Token verification successful!")
            return True
        else:
            print_error(f"Token verification failed: {data['error']}")
            return False
    else:
        print_error(f"Token verification failed with status {response.status_code}")
        return False

def test_get_profile(token):
    """Test get user profile"""
    print_info("\nTesting get profile...")
    
    response = requests.get(
        f"{BASE_URL}/profile",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            print_success("Get profile successful!")
            print_info(f"User: {data['user']['name']} ({data['user']['email']})")
            return True
        else:
            print_error(f"Get profile failed: {data['error']}")
            return False
    else:
        print_error(f"Get profile failed with status {response.status_code}")
        return False

def test_invalid_login():
    """Test login with invalid credentials"""
    print_info("\nTesting invalid login...")
    
    response = requests.post(
        f"{BASE_URL}/login",
        json={
            "email": test_user["email"],
            "password": "WrongPassword123"
        },
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 401:
        print_success("Invalid login correctly rejected!")
        return True
    else:
        print_error("Invalid login should return 401")
        return False

def test_duplicate_registration():
    """Test registering with existing email"""
    print_info("\nTesting duplicate registration...")
    
    response = requests.post(
        f"{BASE_URL}/register",
        json=test_user,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 409:
        print_success("Duplicate registration correctly rejected!")
        return True
    else:
        print_error("Duplicate registration should return 409")
        return False

def test_invalid_token():
    """Test with invalid token"""
    print_info("\nTesting invalid token...")
    
    response = requests.get(
        f"{BASE_URL}/verify",
        headers={"Authorization": "Bearer invalid_token_here"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 401:
        print_success("Invalid token correctly rejected!")
        return True
    else:
        print_error("Invalid token should return 401")
        return False

def test_onboarding(token):
    """Test user onboarding with role selection"""
    print_info("\nTesting onboarding...")
    
    # First get user ID from token verification
    verify_response = requests.get(
        f"{BASE_URL}/verify",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if verify_response.status_code != 200:
        print_error("Cannot get user ID for onboarding test")
        return False
    
    user_id = verify_response.json()["user"]["id"]
    
    # Test onboarding with 'creator' role
    response = requests.post(
        f"{BASE_URL}/onboarding",
        json={
            "userId": user_id,
            "role": "creator",
            "token": token
        },
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        if data["success"] and data["user"]["user_type"] == "creator":
            print_success("Onboarding successful!")
            print_info(f"User Type: {data['user']['user_type']}")
            print_info(f"Next Steps: {len(data['next_steps'])} items")
            return True
        else:
            print_error(f"Onboarding failed: {data.get('error', 'Unknown error')}")
            return False
    else:
        print_error(f"Onboarding failed with status {response.status_code}")
        return False

def run_all_tests():
    """Run all authentication tests"""
    print(f"\n{'='*60}")
    print("🔥 CODEX DOMINION - AUTHENTICATION API TESTS")
    print(f"{'='*60}\n")
    
    print_info(f"Testing against: {BASE_URL}")
    print_info(f"Test User: {test_user['name']} ({test_user['email']})\n")
    
    results = {
        "passed": 0,
        "failed": 0
    }
    
    # Test 1: Registration
    token = test_registration()
    if token:
        results["passed"] += 1
    else:
        results["failed"] += 1
        print_error("Cannot continue tests without valid token")
        return
    
    # Test 2: Login
    login_token = test_login()
    if login_token:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 3: Verify Token
    if test_verify_token(token):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 4: Get Profile
    if test_get_profile(token):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 5: Invalid Login
    if test_invalid_login():
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 6: Duplicate Registration
    if test_duplicate_registration():
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 7: Invalid Token
    if test_invalid_token():
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 8: Onboarding
    if test_onboarding(token):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}\n")
    print_success(f"Passed: {results['passed']}")
    print_error(f"Failed: {results['failed']}")
    print(f"\nTotal: {results['passed'] + results['failed']} tests\n")
    
    if results["failed"] == 0:
        print_success("🎉 All tests passed! Authentication API is working correctly.")
    else:
        print_error("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print_error("\n⚠️  Cannot connect to Flask server!")
        print_info("Make sure Flask is running: python flask_dashboard.py")
        print_info(f"Expected URL: {BASE_URL}\n")
    except Exception as e:
        print_error(f"\n⚠️  Unexpected error: {str(e)}\n")
