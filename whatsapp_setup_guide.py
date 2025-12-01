"""
🔥 WHATSAPP BUSINESS SYSTEM SETUP GUIDE 👑

Complete setup instructions for the Codex WhatsApp Business System
"""

import json
import os
from pathlib import Path

import requests


class WhatsAppSetupGuide:
    """Setup guide for WhatsApp Business System"""

    def __init__(self):
        self.config_file = Path("whatsapp_config.json")

    def check_setup(self):
        """Check current setup status"""
        print("🔥 WHATSAPP BUSINESS SYSTEM SETUP CHECK 👑")
        print("=" * 55)

        # Check config file
        if self.config_file.exists():
            print("✅ Configuration file found: whatsapp_config.json")
            with open(self.config_file, "r") as f:
                config = json.load(f)

            # Check credentials
            whatsapp_token = config.get("whatsapp", {}).get("token")
            phone_id = config.get("whatsapp", {}).get("phone_id")
            business_id = config.get("whatsapp", {}).get("business_id")

            if whatsapp_token and whatsapp_token != "YOUR_WHATSAPP_TOKEN_HERE":
                print("✅ WhatsApp token configured")
            else:
                print("⚠️  WhatsApp token needs configuration")

            if phone_id and phone_id != "YOUR_WHATSAPP_PHONE_ID_HERE":
                print("✅ Phone ID configured")
            else:
                print("⚠️  Phone ID needs configuration")

            if business_id and business_id != "YOUR_WHATSAPP_BUSINESS_ID_HERE":
                print("✅ Business ID configured")
            else:
                print("⚠️  Business ID needs configuration")
        else:
            print("⚠️  Configuration file not found - will be created on first run")

        # Check environment variables
        env_token = os.getenv("WHATSAPP_TOKEN")
        env_phone = os.getenv("WHATSAPP_PHONE_ID")
        env_business = os.getenv("WHATSAPP_BUSINESS_ID")

        if env_token:
            print("✅ WHATSAPP_TOKEN environment variable set")
        else:
            print("⚠️  WHATSAPP_TOKEN environment variable not set")

        if env_phone:
            print("✅ WHATSAPP_PHONE_ID environment variable set")
        else:
            print("⚠️  WHATSAPP_PHONE_ID environment variable not set")

        if env_business:
            print("✅ WHATSAPP_BUSINESS_ID environment variable set")
        else:
            print("⚠️  WHATSAPP_BUSINESS_ID environment variable not set")

        print("\n" + "=" * 55)

    def setup_instructions(self):
        """Print detailed setup instructions"""
        print("\n🔥 WHATSAPP BUSINESS SETUP INSTRUCTIONS 👑")
        print("=" * 60)

        print("\n1. META BUSINESS SETUP:")
        print("   • Visit: https://business.facebook.com/")
        print("   • Create a Business Account or use existing")
        print("   • Add WhatsApp Business Platform product")
        print("   • Verify your business phone number")

        print("\n2. WHATSAPP BUSINESS API SETUP:")
        print("   • Go to Meta for Developers: https://developers.facebook.com/")
        print("   • Create a new app or use existing app")
        print("   • Add 'WhatsApp Business Platform' product")
        print("   • Complete phone number verification process")

        print("\n3. GET API CREDENTIALS:")
        print("   • Navigate to WhatsApp > API Setup")
        print("   • Copy the Phone Number ID")
        print("   • Generate Access Token (temporary or permanent)")
        print("   • Note the Business Account ID")

        print("\n4. PHONE NUMBER VERIFICATION:")
        print("   • Use WhatsApp Business app on your phone")
        print("   • Verify with SMS or voice call")
        print("   • Complete two-factor authentication setup")

        print("\n5. CONFIGURATION OPTIONS:")
        print("   Option A - Environment Variables (Recommended):")
        print("   • Set WHATSAPP_TOKEN in your environment")
        print("   • Set WHATSAPP_PHONE_ID in your environment")
        print("   • Set WHATSAPP_BUSINESS_ID in your environment")

        print("\n   Option B - Configuration File:")
        print("   • Edit whatsapp_config.json")
        print("   • Replace YOUR_WHATSAPP_TOKEN_HERE with your token")
        print("   • Replace YOUR_WHATSAPP_PHONE_ID_HERE with your phone ID")
        print("   • Replace YOUR_WHATSAPP_BUSINESS_ID_HERE with your business ID")

        print("\n6. WEBHOOK SETUP (Optional but Recommended):")
        print("   • Configure webhook URL for message delivery status")
        print("   • Set webhook fields: messages, message_deliveries, message_reads")
        print("   • Verify webhook token for security")

        print("\n7. MESSAGE TEMPLATES:")
        print("   • Create message templates in Meta Business Manager")
        print("   • Get templates approved for broadcast messaging")
        print("   • Use templates for marketing and notifications")

        print("\n8. TEST CONNECTION:")
        print("   • Run: python codex_whatsapp_business.py")
        print("   • Check for successful connection test")

        print("\n9. DASHBOARD INTEGRATION:")
        print("   • The system auto-integrates with codex_simple_dashboard.py")
        print("   • Run dashboard to see WhatsApp Business tab")

        print("=" * 60)

    def test_whatsapp_api(self, token: str = None, phone_id: str = None):
        """Test WhatsApp Business API connection"""
        if not token:
            token = os.getenv("WHATSAPP_TOKEN")
        if not phone_id:
            phone_id = os.getenv("WHATSAPP_PHONE_ID")

        if not token:
            print("❌ No WhatsApp token provided for testing")
            return False

        if not phone_id:
            print("❌ No Phone ID provided for testing")
            return False

        try:
            print("\n🔥 TESTING WHATSAPP BUSINESS API CONNECTION 👑")

            headers = {"Authorization": f"Bearer {token}"}

            # Test phone number access
            print("Testing phone number access...")
            response = requests.get(
                f"https://graph.facebook.com/v19.0/{phone_id}",
                headers=headers,
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                print(f"✅ Phone API Connection successful!")
                print(
                    f"   Phone Number: {data.get('display_phone_number', 'Not available')}"
                )
                print(f"   Verified Name: {data.get('verified_name', 'Not available')}")
                print(
                    f"   Quality Rating: {data.get('quality_rating', 'Not available')}"
                )
            else:
                print(f"❌ Phone API Test failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False

            # Test message capabilities
            print(f"\nTesting message capabilities...")
            capabilities_response = requests.get(
                f"https://graph.facebook.com/v19.0/{phone_id}/message_templates",
                headers=headers,
                timeout=10,
            )

            if capabilities_response.status_code == 200:
                templates_data = capabilities_response.json()
                templates = templates_data.get("data", [])
                print(f"✅ Message capabilities accessible!")
                print(f"   Available Templates: {len(templates)}")

                if templates:
                    print("   Template Names:")
                    for template in templates[:3]:  # Show first 3 templates
                        print(
                            f"     • {template.get('name', 'Unknown')} ({template.get('status', 'Unknown')})"
                        )
            else:
                print(
                    f"⚠️  Template access limited: {capabilities_response.status_code}"
                )

            return True

        except requests.RequestException as e:
            print(f"❌ Connection error: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return False

    def create_sample_config(self):
        """Create sample configuration with instructions"""
        sample_config = {
            "whatsapp": {
                "token": "YOUR_WHATSAPP_TOKEN_HERE",
                "phone_id": "YOUR_WHATSAPP_PHONE_ID_HERE",
                "business_id": "YOUR_WHATSAPP_BUSINESS_ID_HERE",
                "app_id": "YOUR_META_APP_ID",
                "app_secret": "YOUR_META_APP_SECRET",
            },
            "messaging_settings": {
                "track_conversations": True,
                "track_leads": True,
                "track_costs": True,
                "track_templates": True,
                "auto_archive": True,
                "enable_broadcasts": True,
                "rate_limiting": True,
            },
            "analytics_settings": {
                "track_delivery_rates": True,
                "track_read_rates": True,
                "track_conversion_rates": True,
                "cost_monitoring": True,
                "export_format": "json",
                "alert_thresholds": {
                    "high_cost_alert": 100.0,
                    "low_delivery_rate": 0.8,
                    "conversation_spike": 1000,
                    "daily_budget_limit": 500.0,
                },
            },
            "broadcast_settings": {
                "max_recipients_per_batch": 100,
                "batch_delay_seconds": 1,
                "template_categories": ["marketing", "utility", "authentication"],
                "default_language": "en",
                "track_campaign_performance": True,
            },
            "business_settings": {
                "business_name": "Your Business Name",
                "industry": "Technology",
                "timezone": "UTC",
                "currency": "USD",
                "contact_list_management": True,
            },
        }

        with open(self.config_file, "w") as f:
            json.dump(sample_config, f, indent=2)

        print(f"✅ Sample configuration created: {self.config_file}")

    def pricing_info(self):
        """Display WhatsApp Business API pricing information"""
        print("\n💰 WHATSAPP BUSINESS API PRICING INFORMATION")
        print("=" * 50)

        print("\nConversation-Based Pricing (per 24-hour session):")
        print("• Marketing Conversations: $0.025 - $0.300 (varies by country)")
        print("• Utility Conversations: $0.010 - $0.150 (varies by country)")
        print("• Authentication Conversations: $0.005 - $0.075 (varies by country)")
        print("• Service Conversations: Free for first 1,000/month")

        print("\nMessage Templates:")
        print("• Template approval required for broadcast messages")
        print("• Marketing templates have higher pricing")
        print("• Utility templates for order updates, etc. cost less")

        print("\nRate Limits:")
        print("• Start with 250 conversations/24 hours")
        print("• Can scale to unlimited with good quality rating")
        print("• Quality rating affects pricing and limits")

        print("\n💡 Cost Optimization Tips:")
        print("• Use utility templates when possible")
        print("• Maintain high quality rating")
        print("• Group messages into conversations")
        print("• Monitor delivery and read rates")

        print("=" * 50)


if __name__ == "__main__":
    guide = WhatsAppSetupGuide()
    guide.check_setup()
    guide.setup_instructions()
    guide.pricing_info()

    # Test if we have credentials
    if os.getenv("WHATSAPP_TOKEN") and os.getenv("WHATSAPP_PHONE_ID"):
        guide.test_whatsapp_api()
    else:
        print(
            "\n💡 Set WHATSAPP_TOKEN and WHATSAPP_PHONE_ID environment variables to test API connection"
        )

    if not guide.config_file.exists():
        guide.create_sample_config()
