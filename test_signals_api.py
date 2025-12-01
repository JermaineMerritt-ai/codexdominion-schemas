"""
🔥 CODEX SIGNALS API TEST SUITE 📊
Comprehensive testing for FastAPI REST service

The Merritt Method™ - API Validation & Testing
"""

import json
import time
from datetime import datetime

import requests


class SignalsAPITester:
    """Test suite for Codex Signals API"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []

    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.test_results.append(result)

        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")

    def test_health_check(self):
        """Test health check endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/health")

            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    self.log_test(
                        "Health Check",
                        True,
                        f"Engine status: {data.get('engine_status')}",
                    )
                else:
                    self.log_test(
                        "Health Check", False, f"Unhealthy status: {data.get('status')}"
                    )
            else:
                self.log_test(
                    "Health Check", False, f"Status code: {response.status_code}"
                )

        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")

    def test_daily_signals(self):
        """Test daily signals endpoint with sample data"""
        try:
            # Sample request data
            request_data = {
                "market": [
                    {
                        "symbol": "MSFT",
                        "price": 420.1,
                        "vol_30d": 0.22,
                        "trend_20d": 0.48,
                        "liquidity_rank": 5,
                    },
                    {
                        "symbol": "ETH-USD",
                        "price": 3500.0,
                        "vol_30d": 0.40,
                        "trend_20d": 0.30,
                        "liquidity_rank": 15,
                    },
                ],
                "positions": [{"symbol": "MSFT", "weight": 0.04, "allowed_max": 0.08}],
            }

            response = self.session.post(
                f"{self.base_url}/signals/daily",
                json=request_data,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 200:
                data = response.json()
                execution_time = data.get("execution_time_ms", 0)
                picks_count = len(data.get("picks", []))
                self.log_test(
                    "Daily Signals", True, f"{picks_count} picks in {execution_time}ms"
                )
            else:
                self.log_test(
                    "Daily Signals", False, f"Status code: {response.status_code}"
                )

        except Exception as e:
            self.log_test("Daily Signals", False, f"Error: {str(e)}")

    def run_all_tests(self):
        """Run complete test suite"""
        print("🔥 CODEX SIGNALS API TEST SUITE 📊")
        print("=" * 50)
        print("Testing FastAPI REST service...")
        print("")

        # Wait for service to be ready
        print("Waiting for API service to be ready...")
        max_retries = 5
        for i in range(max_retries):
            try:
                response = requests.get(f"{self.base_url}/health", timeout=2)
                if response.status_code == 200:
                    print("✅ API service is ready!")
                    break
            except:
                if i == max_retries - 1:
                    print(
                        "❌ API service not available. Please start the service with:"
                    )
                    print("   .\\launch_signals_api.ps1")
                    return False
                time.sleep(1)

        print("")

        # Run tests
        self.test_health_check()
        self.test_daily_signals()

        # Summary
        print("\n" + "=" * 50)
        print("🎯 TEST SUMMARY")
        print("=" * 50)

        passed = sum(1 for r in self.test_results if r["success"])
        total = len(self.test_results)
        success_rate = (passed / total) * 100 if total > 0 else 0

        print(f"Tests Passed: {passed}/{total} ({success_rate:.1f}%)")

        if passed == total:
            print("🔥 ALL TESTS PASSED! API is ready for production! 👑")
        else:
            print("⚠️ Some tests failed. Check the details above.")

        return passed == total


def main():
    """Run API tests"""
    tester = SignalsAPITester()
    success = tester.run_all_tests()

    if success:
        print("\n🌟 Your FastAPI Codex Signals service is fully operational!")
        print("📊 Access interactive documentation at: http://localhost:8000/docs")
        print("🔥 Ready for integration with Cloud Run deployment!")
    else:
        print("\n🔧 Please fix failing tests before deploying to production.")

    return success


if __name__ == "__main__":
    main()
