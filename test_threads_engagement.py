"""
🔥 THREADS ENGAGEMENT SYSTEM TESTS 👑
Comprehensive testing suite for Threads engagement functionality
"""

import datetime
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import requests

# Add current directory to path for imports
sys.path.insert(0, ".")

try:
    from codex_threads_engagement import (CodexThreadsEngagement,
                                          archive_threads,
                                          get_threads_engagement,
                                          threads_metrics)
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


class TestThreadsEngagement(unittest.TestCase):
    """Test suite for Threads Engagement System"""

    def setUp(self):
        """Set up test environment"""
        self.test_config_file = "test_threads_config.json"
        self.test_archive_file = "test_ledger_threads.jsonl"

        # Create test configuration
        test_config = {
            "threads": {
                "meta_token": "test_token_123",
                "profile_id": "test_profile_456",
                "app_id": "test_app_789",
                "app_secret": "test_secret_abc",
            },
            "engagement_settings": {
                "track_likes": True,
                "track_reposts": True,
                "track_replies": True,
                "auto_archive": True,
            },
        }

        with open(self.test_config_file, "w") as f:
            json.dump(test_config, f)

        # Initialize system with test config
        self.threads_system = CodexThreadsEngagement(config_file=self.test_config_file)
        self.threads_system.archive_file = Path(self.test_archive_file)

    def tearDown(self):
        """Clean up test files"""
        for file_path in [self.test_config_file, self.test_archive_file]:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_config_loading(self):
        """Test configuration file loading"""
        self.assertIsNotNone(self.threads_system.config)
        self.assertEqual(self.threads_system.meta_token, "test_token_123")
        self.assertEqual(self.threads_system.profile_id, "test_profile_456")

    def test_demo_metrics_generation(self):
        """Test demo metrics generation"""
        metrics = self.threads_system._generate_demo_metrics()

        self.assertIn("likes", metrics)
        self.assertIn("reposts", metrics)
        self.assertIn("replies", metrics)
        self.assertIn("reach", metrics)
        self.assertIn("impressions", metrics)
        self.assertTrue(metrics["demo"])

        # Check realistic ranges
        self.assertGreater(metrics["likes"], 0)
        self.assertGreater(metrics["reposts"], 0)
        self.assertGreater(metrics["replies"], 0)

    def test_metrics_enhancement(self):
        """Test metrics enhancement functionality"""
        base_metrics = {
            "likes": 1000,
            "reposts": 50,
            "replies": 100,
            "reach": 5000,
            "impressions": 8000,
            "followers": 2000,
            "threads_count": 10,
        }

        enhanced = self.threads_system._enhance_metrics(base_metrics)

        # Check calculated fields
        self.assertIn("total_engagement", enhanced)
        self.assertIn("engagement_rate", enhanced)
        self.assertIn("performance_score", enhanced)
        self.assertIn("reply_to_like_ratio", enhanced)

        # Verify calculations
        expected_total = 1000 + 50 + 100
        self.assertEqual(enhanced["total_engagement"], expected_total)

        expected_rate = (expected_total / 8000) * 100
        self.assertAlmostEqual(enhanced["engagement_rate"], expected_rate, places=2)

    def test_performance_score_calculation(self):
        """Test performance score calculation"""
        metrics = {
            "likes": 2000,
            "reposts": 100,
            "replies": 200,
            "reach": 10000,
            "impressions": 15000,
        }

        score = self.threads_system._calculate_performance_score(metrics)

        self.assertIsInstance(score, int)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_archive_functionality(self):
        """Test archiving functionality"""
        test_report = {
            "likes": 500,
            "reposts": 25,
            "replies": 50,
            "test_metric": "test_value",
        }

        # Test archiving
        result = self.threads_system.archive_threads(test_report)
        self.assertTrue(result)

        # Verify file was created and contains data
        self.assertTrue(self.threads_system.archive_file.exists())

        # Test reading history
        history = self.threads_system.get_archive_history()
        self.assertEqual(len(history), 1)

        archived_entry = history[0]
        self.assertEqual(archived_entry["likes"], 500)
        self.assertEqual(archived_entry["reposts"], 25)
        self.assertEqual(archived_entry["test_metric"], "test_value")
        self.assertIn("ts", archived_entry)

    def test_community_analysis(self):
        """Test community engagement analysis"""
        metrics = {"likes": 1000, "reposts": 200, "replies": 400}

        analysis = self.threads_system._analyze_community_engagement(metrics)

        self.assertIn("community_type", analysis)
        self.assertIn("engagement_distribution", analysis)
        self.assertIn("engagement_quality_score", analysis)

        # Verify percentages add up to 100
        dist = analysis["engagement_distribution"]
        total_percentage = dist["likes"] + dist["reposts"] + dist["replies"]
        self.assertAlmostEqual(total_percentage, 100, places=1)

    def test_content_insights(self):
        """Test content insights generation"""
        current_metrics = {
            "likes": 1500,
            "reposts": 100,
            "replies": 300,
            "engagement_rate": 3.5,
            "reach_rate": 65,
            "reply_to_like_ratio": 0.2,
            "performance_score": 75,
        }

        insights = self.threads_system._generate_content_insights(current_metrics, [])

        self.assertIn("content_insights", insights)
        self.assertIn("recommendations", insights)
        self.assertIn("optimization_priority", insights)

        self.assertIsInstance(insights["content_insights"], list)
        self.assertIsInstance(insights["recommendations"], list)

    @patch("requests.get")
    def test_api_integration(self, mock_get):
        """Test Meta Graph API integration (mocked)"""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"name": "likes", "values": [{"value": 1000}]},
                {"name": "shares", "values": [{"value": 50}]},
                {"name": "comments", "values": [{"value": 100}]},
            ]
        }
        mock_get.return_value = mock_response

        # Test API call
        metrics = self.threads_system._fetch_threads_insights("test_profile")

        self.assertEqual(metrics["likes"], 1000)
        self.assertEqual(metrics["reposts"], 50)
        self.assertEqual(metrics["replies"], 100)
        self.assertEqual(metrics["source"], "meta_graph_api")

    @patch("requests.get")
    def test_api_error_handling(self, mock_get):
        """Test API error handling"""
        # Mock API error
        mock_get.side_effect = requests.RequestException("Connection failed")

        metrics = self.threads_system._fetch_threads_insights("test_profile")

        # Should return demo data on API error
        self.assertIn("likes", metrics)
        self.assertTrue(metrics.get("demo", False))

    def test_standalone_functions(self):
        """Test standalone backward-compatible functions"""
        # Test threads_metrics function
        metrics = threads_metrics()
        self.assertIn("likes", metrics)
        self.assertIn("reposts", metrics)
        self.assertIn("replies", metrics)

        # Test archive_threads function
        test_data = {"likes": 100, "reposts": 10, "replies": 20}
        result = archive_threads(test_data)
        self.assertTrue(result)

        # Test get_threads_engagement function
        engagement = get_threads_engagement()
        self.assertIn("likes", engagement)

    def test_growth_metrics_calculation(self):
        """Test growth metrics calculation"""
        # Create mock history data
        history_data = []
        for i in range(10):
            entry = {
                "ts": (
                    datetime.datetime.now() - datetime.timedelta(days=i)
                ).isoformat(),
                "likes": 1000 + (i * 10),
                "total_engagement": 1500 + (i * 15),
                "reach": 5000 + (i * 50),
            }
            history_data.append(entry)

        # Mock the get_archive_history method
        with patch.object(
            self.threads_system, "get_archive_history", return_value=history_data
        ):
            growth_metrics = self.threads_system._calculate_growth_metrics()

        self.assertIn("likes_growth", growth_metrics)
        self.assertIn("engagement_growth", growth_metrics)
        self.assertIn("reach_growth", growth_metrics)
        self.assertIn("trend_direction", growth_metrics)

    def test_engagement_summary(self):
        """Test comprehensive engagement summary"""
        summary = self.threads_system.get_engagement_summary()

        # Should contain all key metrics
        expected_keys = [
            "likes",
            "reposts",
            "replies",
            "total_engagement",
            "engagement_rate",
            "performance_score",
            "content_insights",
        ]

        for key in expected_keys:
            self.assertIn(key, summary)

        self.assertIn("summary_generated", summary)


class TestThreadsIntegration(unittest.TestCase):
    """Integration tests for Threads system"""

    def test_config_creation(self):
        """Test automatic config file creation"""
        config_file = "auto_test_config.json"

        # Remove file if exists
        if os.path.exists(config_file):
            os.remove(config_file)

        # Initialize system - should create config
        system = CodexThreadsEngagement(config_file=config_file)

        # Verify config was created
        self.assertTrue(os.path.exists(config_file))

        # Verify config structure
        with open(config_file, "r") as f:
            config = json.load(f)

        self.assertIn("threads", config)
        self.assertIn("engagement_settings", config)
        self.assertIn("analytics_settings", config)

        # Cleanup
        os.remove(config_file)

    def test_environment_variable_override(self):
        """Test environment variable configuration override"""
        # Set test environment variables
        os.environ["META_TOKEN"] = "env_token_test"
        os.environ["THREADS_PROFILE_ID"] = "env_profile_test"

        try:
            system = CodexThreadsEngagement()

            # Should use environment variables
            self.assertEqual(system.meta_token, "env_token_test")
            self.assertEqual(system.profile_id, "env_profile_test")

        finally:
            # Cleanup environment variables
            del os.environ["META_TOKEN"]
            del os.environ["THREADS_PROFILE_ID"]


def run_tests():
    """Run all tests with detailed output"""
    print("🔥 RUNNING THREADS ENGAGEMENT SYSTEM TESTS 👑")
    print("=" * 55)

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestThreadsEngagement))
    test_suite.addTest(unittest.makeSuite(TestThreadsIntegration))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Summary
    print("\n" + "=" * 55)
    if result.wasSuccessful():
        print("🎉 ALL TESTS PASSED! System ready for production. 👑")
    else:
        print(f"⚠️  {len(result.failures)} failures, {len(result.errors)} errors")
        print("Check output above for details.")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
