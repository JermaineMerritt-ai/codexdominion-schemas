"""
🔥 THREADS ENGAGEMENT SYSTEM SETUP GUIDE 👑

Complete setup instructions for the Codex Threads Engagement System
"""

import json
import os
from pathlib import Path

import requests


class ThreadsSetupGuide:
    """Setup guide for Threads Engagement System"""

    def __init__(self):
        self.config_file = Path("threads_config.json")

    def check_setup(self):
        """Check current setup status"""
        print("🔥 THREADS ENGAGEMENT SYSTEM SETUP CHECK 👑")
        print("=" * 50)

        # Check config file
        if self.config_file.exists():
            print("✅ Configuration file found: threads_config.json")
            with open(self.config_file, "r") as f:
                config = json.load(f)

            # Check credentials
            meta_token = config.get("threads", {}).get("meta_token")
            profile_id = config.get("threads", {}).get("profile_id")

            if meta_token and meta_token != "YOUR_META_TOKEN_HERE":
                print("✅ Meta token configured")
            else:
                print("⚠️  Meta token needs configuration")

            if profile_id and profile_id != "YOUR_THREADS_PROFILE_ID_HERE":
                print("✅ Profile ID configured")
            else:
                print("⚠️  Profile ID needs configuration")
        else:
            print("⚠️  Configuration file not found - will be created on first run")

        # Check environment variables
        env_token = os.getenv("META_TOKEN")
        env_profile = os.getenv("THREADS_PROFILE_ID")

        if env_token:
            print("✅ META_TOKEN environment variable set")
        else:
            print("⚠️  META_TOKEN environment variable not set")

        if env_profile:
            print("✅ THREADS_PROFILE_ID environment variable set")
        else:
            print("⚠️  THREADS_PROFILE_ID environment variable not set")

        print("\n" + "=" * 50)

    def setup_instructions(self):
        """Print detailed setup instructions"""
        print("\n🔥 THREADS ENGAGEMENT SETUP INSTRUCTIONS 👑")
        print("=" * 55)

        print("\n1. META DEVELOPER SETUP:")
        print("   • Visit: https://developers.facebook.com/")
        print("   • Create a new app or use existing app")
        print("   • Add 'Instagram Basic Display' product")
        print("   • Note: Threads uses Instagram's infrastructure")

        print("\n2. GET ACCESS TOKEN:")
        print("   • Go to your Meta App Dashboard")
        print("   • Navigate to Instagram Basic Display > Basic Display")
        print("   • Generate Access Token")
        print("   • Copy the long-lived access token")

        print("\n3. GET PROFILE ID:")
        print(
            "   • Use Graph API Explorer: https://developers.facebook.com/tools/explorer/"
        )
        print("   • Query: /me?fields=id,username")
        print("   • Copy the 'id' field value")

        print("\n4. CONFIGURATION OPTIONS:")
        print("   Option A - Environment Variables (Recommended):")
        print("   • Set META_TOKEN in your environment")
        print("   • Set THREADS_PROFILE_ID in your environment")

        print("\n   Option B - Configuration File:")
        print("   • Edit threads_config.json")
        print("   • Replace YOUR_META_TOKEN_HERE with your token")
        print("   • Replace YOUR_THREADS_PROFILE_ID_HERE with your ID")

        print("\n5. TEST CONNECTION:")
        print("   • Run: python codex_threads_engagement.py")
        print("   • Check for successful connection test")

        print("\n6. DASHBOARD INTEGRATION:")
        print("   • The system auto-integrates with codex_simple_dashboard.py")
        print("   • Run dashboard to see Threads Engagement tab")

        print("=" * 55)

    def test_meta_api(self, token: str = None, profile_id: str = None):
        """Test Meta Graph API connection"""
        if not token:
            token = os.getenv("META_TOKEN")
        if not profile_id:
            profile_id = os.getenv("THREADS_PROFILE_ID")

        if not token:
            print("❌ No Meta token provided for testing")
            return False

        try:
            print("\n🔥 TESTING META GRAPH API CONNECTION 👑")

            headers = {"Authorization": f"Bearer {token}"}

            # Test basic API access
            print("Testing basic API access...")
            response = requests.get(
                "https://graph.facebook.com/v19.0/me", headers=headers, timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                print(f"✅ API Connection successful!")
                print(f"   User ID: {data.get('id')}")
                print(f"   Name: {data.get('name', 'Not available')}")
            else:
                print(f"❌ API Test failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False

            # Test profile access if provided
            if profile_id:
                print(f"\nTesting profile access for ID: {profile_id}")
                profile_response = requests.get(
                    f"https://graph.facebook.com/v19.0/{profile_id}",
                    headers=headers,
                    timeout=10,
                )

                if profile_response.status_code == 200:
                    profile_data = profile_response.json()
                    print(f"✅ Profile access successful!")
                    print(f"   Profile ID: {profile_data.get('id')}")
                else:
                    print(f"⚠️  Profile access limited: {profile_response.status_code}")

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
            "threads": {
                "meta_token": "YOUR_META_TOKEN_HERE",
                "profile_id": "YOUR_THREADS_PROFILE_ID_HERE",
                "app_id": "YOUR_META_APP_ID",
                "app_secret": "YOUR_META_APP_SECRET",
            },
            "engagement_settings": {
                "track_likes": True,
                "track_reposts": True,
                "track_replies": True,
                "track_mentions": True,
                "track_hashtags": True,
                "auto_archive": True,
                "sentiment_analysis": False,
            },
            "analytics_settings": {
                "track_growth": True,
                "track_reach": True,
                "track_impressions": True,
                "competitor_analysis": False,
                "export_format": "json",
                "alert_thresholds": {
                    "engagement_spike": 500,
                    "follower_milestone": 1000,
                    "viral_threshold": 10000,
                    "engagement_drop": 0.1,
                },
            },
            "content_settings": {
                "auto_tag_engagement": True,
                "track_viral_threads": True,
                "content_categories": ["tech", "business", "lifestyle", "news"],
                "optimal_posting_times": ["09:00", "12:00", "15:00", "18:00"],
            },
        }

        with open(self.config_file, "w") as f:
            json.dump(sample_config, f, indent=2)

        print(f"✅ Sample configuration created: {self.config_file}")


if __name__ == "__main__":
    guide = ThreadsSetupGuide()
    guide.check_setup()
    guide.setup_instructions()

    # Test if we have credentials
    if os.getenv("META_TOKEN"):
        guide.test_meta_api()
    else:
        print("\n💡 Set META_TOKEN environment variable to test API connection")

    if not guide.config_file.exists():
        guide.create_sample_config()
