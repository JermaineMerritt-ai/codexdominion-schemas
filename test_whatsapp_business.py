"""
🔥 WHATSAPP BUSINESS SYSTEM TESTS 👑
Comprehensive testing suite for WhatsApp Business functionality
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
    from codex_whatsapp_business import (CodexWhatsAppBusiness,
                                         archive_whatsapp,
                                         get_whatsapp_business_summary,
                                         whatsapp_broadcast, whatsapp_metrics)
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


class TestWhatsAppBusiness(unittest.TestCase):
    """Test suite for WhatsApp Business System"""

    def setUp(self):
        """Set up test environment"""
        self.test_config_file = "test_whatsapp_config.json"
        self.test_archive_file = "test_ledger_whatsapp.jsonl"

        # Create test configuration
        test_config = {
            "whatsapp": {
                "token": "test_token_123",
                "phone_id": "test_phone_456",
                "business_id": "test_business_789",
                "app_id": "test_app_abc",
                "app_secret": "test_secret_def",
            },
            "messaging_settings": {
                "track_conversations": True,
                "track_leads": True,
                "track_costs": True,
                "auto_archive": True,
            },
            "broadcast_settings": {
                "max_recipients_per_batch": 10,
                "batch_delay_seconds": 0.1,
            },
        }

        with open(self.test_config_file, "w") as f:
            json.dump(test_config, f)

        # Initialize system with test config
        self.whatsapp_system = CodexWhatsAppBusiness(config_file=self.test_config_file)
        self.whatsapp_system.archive_file = Path(self.test_archive_file)

    def tearDown(self):
        """Clean up test files"""
        for file_path in [self.test_config_file, self.test_archive_file]:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_config_loading(self):
        """Test configuration file loading"""
        self.assertIsNotNone(self.whatsapp_system.config)
        self.assertEqual(self.whatsapp_system.whatsapp_token, "test_token_123")
        self.assertEqual(self.whatsapp_system.phone_id, "test_phone_456")
        self.assertEqual(self.whatsapp_system.business_id, "test_business_789")

    def test_demo_metrics_generation(self):
        """Test demo metrics generation"""
        metrics = self.whatsapp_system._generate_demo_metrics()

        self.assertIn("conversations", metrics)
        self.assertIn("leads", metrics)
        self.assertIn("messaging_cost_usd", metrics)
        self.assertIn("messages_sent", metrics)
        self.assertIn("messages_delivered", metrics)
        self.assertIn("messages_read", metrics)
        self.assertIn("delivery_rate", metrics)
        self.assertIn("read_rate", metrics)
        self.assertTrue(metrics["demo"])

        # Check realistic ranges
        self.assertGreater(metrics["conversations"], 0)
        self.assertGreater(metrics["messages_sent"], 0)
        self.assertGreaterEqual(metrics["delivery_rate"], 0)
        self.assertLessEqual(metrics["delivery_rate"], 1)
        self.assertGreaterEqual(metrics["read_rate"], 0)
        self.assertLessEqual(metrics["read_rate"], 1)

    def test_metrics_enhancement(self):
        """Test metrics enhancement functionality"""
        base_metrics = {
            "conversations": 100,
            "leads": 15,
            "messaging_cost_usd": 25.50,
            "messages_sent": 300,
            "messages_delivered": 285,
            "messages_read": 200,
            "delivery_rate": 0.95,
            "read_rate": 0.70,
        }

        enhanced = self.whatsapp_system._enhance_metrics(base_metrics)

        # Check calculated fields
        self.assertIn("lead_conversion_rate", enhanced)
        self.assertIn("cost_per_conversation", enhanced)
        self.assertIn("cost_per_lead", enhanced)
        self.assertIn("messages_per_conversation", enhanced)
        self.assertIn("engagement_score", enhanced)
        self.assertIn("roi_percentage", enhanced)

        # Verify calculations
        expected_conversion_rate = (15 / 100) * 100
        self.assertEqual(enhanced["lead_conversion_rate"], expected_conversion_rate)

        expected_cost_per_conversation = 25.50 / 100
        self.assertAlmostEqual(
            enhanced["cost_per_conversation"], expected_cost_per_conversation, places=3
        )

    def test_archive_functionality(self):
        """Test archiving functionality"""
        test_report = {
            "conversations": 50,
            "leads": 8,
            "messaging_cost_usd": 12.75,
            "test_field": "test_value",
        }

        # Test archiving
        result = self.whatsapp_system.archive_whatsapp(test_report)
        self.assertTrue(result)

        # Verify file was created and contains data
        self.assertTrue(self.whatsapp_system.archive_file.exists())

        # Test reading history
        history = self.whatsapp_system.get_archive_history()
        self.assertEqual(len(history), 1)

        archived_entry = history[0]
        self.assertEqual(archived_entry["conversations"], 50)
        self.assertEqual(archived_entry["leads"], 8)
        self.assertEqual(archived_entry["test_field"], "test_value")
        self.assertIn("ts", archived_entry)

    def test_broadcast_simulation(self):
        """Test broadcast simulation functionality"""
        message = "Test broadcast message"
        recipients = ["+1234567890", "+0987654321", "+1111222333"]

        result = self.whatsapp_system._simulate_broadcast(message, recipients)

        self.assertIn("campaign_id", result)
        self.assertIn("total_recipients", result)
        self.assertIn("successful_sends", result)
        self.assertIn("failed_sends", result)
        self.assertIn("success_rate", result)
        self.assertIn("estimated_cost", result)
        self.assertTrue(result.get("demo", False))

        # Verify totals
        total = result["successful_sends"] + result["failed_sends"]
        self.assertEqual(total, len(recipients))
        self.assertEqual(result["total_recipients"], len(recipients))

    def test_business_performance_analysis(self):
        """Test business performance analysis"""
        current_metrics = {
            "conversations": 200,
            "leads": 30,
            "delivery_rate": 0.92,
            "read_rate": 0.75,
            "lead_conversion_rate": 15.0,
        }

        analysis = self.whatsapp_system._analyze_business_performance(
            current_metrics, []
        )

        self.assertIn("business_performance_score", analysis)
        self.assertIn("performance_trend", analysis)
        self.assertIn("delivery_quality", analysis)
        self.assertIn("engagement_quality", analysis)

        # Check score is reasonable
        score = analysis["business_performance_score"]
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_cost_efficiency_analysis(self):
        """Test cost efficiency analysis"""
        current_metrics = {
            "conversations": 100,
            "leads": 15,
            "messaging_cost_usd": 20.0,
            "cost_per_conversation": 0.20,
            "cost_per_lead": 1.33,
            "roi_percentage": 25.5,
        }

        analysis = self.whatsapp_system._analyze_cost_efficiency(current_metrics, [])

        self.assertIn("cost_efficiency_rating", analysis)
        self.assertIn("avg_daily_cost", analysis)
        self.assertIn("monthly_cost_projection", analysis)
        self.assertIn("roi_status", analysis)

        # Check ROI status logic
        self.assertEqual(analysis["roi_status"], "profitable")

    def test_campaign_performance_analysis(self):
        """Test campaign performance analysis"""
        # Create mock campaign history
        campaign_history = [
            {
                "type": "broadcast_campaign",
                "successful_sends": 90,
                "failed_sends": 10,
                "success_rate": 90.0,
                "ts": "2024-01-01T12:00:00",
            },
            {
                "type": "broadcast_campaign",
                "successful_sends": 85,
                "failed_sends": 15,
                "success_rate": 85.0,
                "ts": "2024-01-02T12:00:00",
            },
        ]

        analysis = self.whatsapp_system._analyze_campaign_performance(campaign_history)

        self.assertIn("total_campaigns", analysis)
        self.assertIn("avg_success_rate", analysis)
        self.assertIn("total_messages_sent", analysis)
        self.assertIn("campaign_performance", analysis)

        # Verify calculations
        self.assertEqual(analysis["total_campaigns"], 2)
        self.assertEqual(analysis["avg_success_rate"], 87.5)
        self.assertEqual(analysis["total_messages_sent"], 175)

    @patch("requests.get")
    def test_api_integration(self, mock_get):
        """Test WhatsApp Business API integration (mocked)"""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "analytics": [
                {"name": "conversations", "values": [{"value": 150}]},
                {"name": "messages_sent", "values": [{"value": 400}]},
                {"name": "messages_delivered", "values": [{"value": 380}]},
            ],
            "cost_breakdown": {
                "marketing_conversations": {"amount": 35.0},
                "utility_conversations": {"amount": 15.0},
            },
        }
        mock_get.return_value = mock_response

        # Test API call
        metrics = self.whatsapp_system._fetch_whatsapp_analytics("test_phone")

        self.assertEqual(metrics["conversations"], 150)
        self.assertEqual(metrics["messages_sent"], 400)
        self.assertEqual(metrics["messages_delivered"], 380)
        self.assertEqual(metrics["messaging_cost_usd"], 50.0)
        self.assertEqual(metrics["source"], "whatsapp_business_api")

    @patch("requests.get")
    def test_api_error_handling(self, mock_get):
        """Test API error handling"""
        # Mock API error
        mock_get.side_effect = requests.RequestException("Connection failed")

        metrics = self.whatsapp_system._fetch_whatsapp_analytics("test_phone")

        # Should return demo data on API error
        self.assertIn("conversations", metrics)
        self.assertTrue(metrics.get("demo", False))

    @patch("requests.post")
    def test_broadcast_integration(self, mock_post):
        """Test broadcast integration (mocked)"""
        # Mock successful broadcast response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"messages": [{"id": "msg_123"}]}
        mock_post.return_value = mock_response

        # Test broadcast
        message = "Test broadcast"
        recipients = ["+1234567890", "+0987654321"]

        result = self.whatsapp_system.whatsapp_broadcast(message, recipients)

        self.assertIn("campaign_id", result)
        self.assertEqual(result["total_recipients"], 2)
        self.assertIn("successful_sends", result)
        self.assertIn("message_ids", result)

    def test_standalone_functions(self):
        """Test standalone backward-compatible functions"""
        # Test whatsapp_metrics function
        metrics = whatsapp_metrics()
        self.assertIn("conversations", metrics)
        self.assertIn("leads", metrics)
        self.assertIn("messaging_cost_usd", metrics)

        # Test archive_whatsapp function
        test_data = {"conversations": 50, "leads": 8, "messaging_cost_usd": 12.0}
        result = archive_whatsapp(test_data)
        self.assertTrue(result)

        # Test whatsapp_broadcast function
        broadcast_result = whatsapp_broadcast("Test message", ["+1234567890"])
        self.assertIn("successful_sends", broadcast_result)

        # Test get_whatsapp_business_summary function
        summary = get_whatsapp_business_summary()
        self.assertIn("conversations", summary)

    def test_growth_metrics_calculation(self):
        """Test growth metrics calculation"""
        # Create mock history data
        history_data = []
        for i in range(10):
            entry = {
                "ts": (
                    datetime.datetime.now() - datetime.timedelta(days=i)
                ).isoformat(),
                "conversations": 100 + (i * 5),
                "leads": 15 + i,
                "messaging_cost_usd": 20.0 + (i * 2),
            }
            history_data.append(entry)

        # Mock the get_archive_history method
        with patch.object(
            self.whatsapp_system, "get_archive_history", return_value=history_data
        ):
            growth_metrics = self.whatsapp_system._calculate_growth_metrics()

        self.assertIn("conversation_growth", growth_metrics)
        self.assertIn("lead_growth", growth_metrics)
        self.assertIn("cost_growth", growth_metrics)
        self.assertIn("trend_direction", growth_metrics)

    def test_business_summary(self):
        """Test comprehensive business summary"""
        summary = self.whatsapp_system.get_business_summary()

        # Should contain all key metrics
        expected_keys = [
            "conversations",
            "leads",
            "messaging_cost_usd",
            "lead_conversion_rate",
            "cost_per_conversation",
            "business_performance_score",
            "cost_efficiency_rating",
        ]

        for key in expected_keys:
            self.assertIn(key, summary)

        self.assertIn("summary_generated", summary)


class TestWhatsAppIntegration(unittest.TestCase):
    """Integration tests for WhatsApp Business system"""

    def test_config_creation(self):
        """Test automatic config file creation"""
        config_file = "auto_test_whatsapp_config.json"

        # Remove file if exists
        if os.path.exists(config_file):
            os.remove(config_file)

        # Initialize system - should create config
        system = CodexWhatsAppBusiness(config_file=config_file)

        # Verify config was created
        self.assertTrue(os.path.exists(config_file))

        # Verify config structure
        with open(config_file, "r") as f:
            config = json.load(f)

        self.assertIn("whatsapp", config)
        self.assertIn("messaging_settings", config)
        self.assertIn("analytics_settings", config)
        self.assertIn("broadcast_settings", config)

        # Cleanup
        os.remove(config_file)

    def test_environment_variable_override(self):
        """Test environment variable configuration override"""
        # Set test environment variables
        os.environ["WHATSAPP_TOKEN"] = "env_token_test"
        os.environ["WHATSAPP_PHONE_ID"] = "env_phone_test"
        os.environ["WHATSAPP_BUSINESS_ID"] = "env_business_test"

        try:
            system = CodexWhatsAppBusiness()

            # Should use environment variables
            self.assertEqual(system.whatsapp_token, "env_token_test")
            self.assertEqual(system.phone_id, "env_phone_test")
            self.assertEqual(system.business_id, "env_business_test")

        finally:
            # Cleanup environment variables
            del os.environ["WHATSAPP_TOKEN"]
            del os.environ["WHATSAPP_PHONE_ID"]
            del os.environ["WHATSAPP_BUSINESS_ID"]


def run_tests():
    """Run all tests with detailed output"""
    print("🔥 RUNNING WHATSAPP BUSINESS SYSTEM TESTS 👑")
    print("=" * 60)

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestWhatsAppBusiness))
    test_suite.addTest(unittest.makeSuite(TestWhatsAppIntegration))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Summary
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("🎉 ALL TESTS PASSED! WhatsApp Business system ready for production. 👑")
    else:
        print(f"⚠️  {len(result.failures)} failures, {len(result.errors)} errors")
        print("Check output above for details.")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
