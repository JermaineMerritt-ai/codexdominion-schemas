#!/usr/bin/env python3
"""
Codex Market Dominion API - Test Suite
Comprehensive testing of all API endpoints
"""

import requests
import json
import time
from datetime import datetime, date

class CodexAPITester:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def test_endpoint(self, method, endpoint, data=None, expected_status=200):
        """Test an API endpoint"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, timeout=10)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            success = response.status_code == expected_status
            
            print(f"{'✅' if success else '❌'} {method.upper():>4} {endpoint}")
            print(f"    Status: {response.status_code}")
            
            if success and response.headers.get('content-type', '').startswith('application/json'):
                try:
                    data = response.json()
                    if isinstance(data, dict):
                        # Show a few key fields
                        for key in list(data.keys())[:3]:
                            value = data[key]
                            if isinstance(value, (str, int, float)):
                                print(f"    {key}: {value}")
                            else:
                                print(f"    {key}: {type(value).__name__}")
                    elif isinstance(data, list):
                        print(f"    Items: {len(data)}")
                except:
                    print("    Response: [Non-JSON data]")
            
            print()
            return success, response
            
        except Exception as e:
            print(f"❌ {method.upper():>4} {endpoint}")
            print(f"    Error: {e}")
            print()
            return False, None

    def run_comprehensive_test(self):
        """Run comprehensive API test suite"""
        print("🧪 CODEX MARKET DOMINION API - TEST SUITE")
        print("=" * 60)
        print(f"🎯 Testing API at: {self.base_url}")
        print(f"⏰ Started at: {datetime.now().isoformat()}")
        print()
        
        tests_passed = 0
        total_tests = 0
        
        # Test basic endpoints
        basic_tests = [
            ("GET", "/"),
            ("GET", "/health"),
            ("GET", "/market/quote/AAPL"),
            ("GET", "/market/quote/MSFT"),
            ("GET", "/market/trending"),
            ("GET", "/analytics/summary")
        ]
        
        print("📊 BASIC ENDPOINT TESTS")
        print("-" * 30)
        
        for method, endpoint in basic_tests:
            success, _ = self.test_endpoint(method, endpoint)
            total_tests += 1
            if success:
                tests_passed += 1
        
        # Test portfolio endpoints (mock data)
        print("💼 PORTFOLIO ENDPOINT TESTS")
        print("-" * 30)
        
        portfolio_tests = [
            ("GET", "/portfolio/test-portfolio-123/positions"),
            ("GET", "/portfolio/test-portfolio-123/performance?days=7")
        ]
        
        for method, endpoint in portfolio_tests:
            success, _ = self.test_endpoint(method, endpoint)
            total_tests += 1
            if success:
                tests_passed += 1
        
        # Test trading picks
        print("📈 TRADING PICKS TESTS")
        print("-" * 30)
        
        pick_data = {
            "user_id": "test_user_001",
            "symbols": ["AAPL", "MSFT", "GOOGL"],
            "trade_date": date.today().isoformat()
        }
        
        success, _ = self.test_endpoint("POST", "/picks", data=pick_data)
        total_tests += 1
        if success:
            tests_passed += 1
        
        # Test affiliate endpoints
        print("🤝 AFFILIATE ENDPOINT TESTS") 
        print("-" * 30)
        
        success, _ = self.test_endpoint("GET", "/affiliate/stats")
        total_tests += 1
        if success:
            tests_passed += 1
        
        # Test AMM endpoints
        print("🔄 AMM/DEFI ENDPOINT TESTS")
        print("-" * 30)
        
        success, _ = self.test_endpoint("GET", "/amm/pools")
        total_tests += 1
        if success:
            tests_passed += 1
        
        swap_data = {
            "pool_id": "pool-001",
            "from_asset": "USDC",
            "to_asset": "ETH",
            "amount": 1000.0
        }
        
        success, _ = self.test_endpoint("POST", "/amm/swap", data=swap_data)
        total_tests += 1
        if success:
            tests_passed += 1
        
        # Test results summary
        print("🎯 TEST RESULTS SUMMARY")
        print("=" * 40)
        print(f"✅ Tests Passed: {tests_passed}/{total_tests}")
        print(f"📊 Success Rate: {tests_passed/total_tests*100:.1f}%")
        
        if tests_passed == total_tests:
            print("🏆 ALL TESTS PASSED! API is fully operational!")
        elif tests_passed >= total_tests * 0.8:
            print("👍 Most tests passed - API is largely functional")
        else:
            print("⚠️ Several tests failed - API may have issues")
        
        print(f"⏰ Completed at: {datetime.now().isoformat()}")

def main():
    """Main test runner"""
    # Check if API is running
    tester = CodexAPITester()
    
    print("🔍 Checking if API is running...")
    try:
        response = requests.get(f"{tester.base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is running! Starting comprehensive tests...")
            print()
            tester.run_comprehensive_test()
        else:
            print(f"❌ API returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ API is not running. Please start the API first:")
        print("   python codex_system_launcher.py")
        print("   OR")
        print("   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"❌ Error connecting to API: {e}")

if __name__ == "__main__":
    main()