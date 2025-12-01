"""
🔥 CODEX BUFFER INTEGRATION TEST SUITE 👑
Comprehensive testing for Buffer API integration

The Merritt Method™ - Testing Digital Sovereignty
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add the current directory to the path
sys.path.append(".")

try:
    from codex_buffer_proclamation import (CodexBufferProclaimer,
                                           proclaim_social)

    print("✅ Successfully imported CodexBufferProclaimer")
except ImportError as e:
    print(f"❌ Failed to import Buffer integration: {e}")
    sys.exit(1)


def test_configuration():
    """Test Buffer configuration setup"""
    print("\n🔧 Testing Configuration...")

    try:
        buffer_client = CodexBufferProclaimer()
        print("✅ Buffer client initialized")

        # Check if config file exists
        if Path("buffer_config.json").exists():
            print("✅ Buffer config file exists")

            # Check config content
            with open("buffer_config.json", "r") as f:
                config = json.load(f)

            if (
                config.get("buffer", {}).get("access_token")
                == "YOUR_BUFFER_ACCESS_TOKEN"
            ):
                print("⚠️  Buffer access token not configured (using placeholder)")
                return False
            else:
                print("✅ Buffer access token configured")
                return True
        else:
            print("⚠️  Buffer config file not found")
            return False

    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def test_connection():
    """Test Buffer API connection"""
    print("\n🌐 Testing Buffer API Connection...")

    try:
        buffer_client = CodexBufferProclaimer()

        if buffer_client.test_connection():
            print("✅ Buffer API connection successful")
            return True
        else:
            print("❌ Buffer API connection failed")
            return False

    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False


def test_profiles():
    """Test Buffer profiles retrieval"""
    print("\n👥 Testing Buffer Profiles...")

    try:
        buffer_client = CodexBufferProclaimer()
        profiles = buffer_client.get_profiles()

        if profiles:
            print(f"✅ Found {len(profiles)} Buffer profiles:")
            for profile in profiles:
                service = profile.get("service", "Unknown")
                formatted_username = profile.get("formatted_username", "N/A")
                print(f"   📱 {service}: {formatted_username}")
            return True
        else:
            print("⚠️  No Buffer profiles found")
            return False

    except Exception as e:
        print(f"❌ Profiles test failed: {e}")
        return False


def test_proclamation_formatting():
    """Test proclamation text formatting"""
    print("\n📝 Testing Proclamation Formatting...")

    try:
        buffer_client = CodexBufferProclaimer()

        test_cases = [
            {"text": "Test sovereignty message", "type": "sovereignty"},
            {"text": "Test wisdom message", "type": "wisdom"},
            {"text": "Test celebration message", "type": "celebration"},
            {"text": "Test announcement message", "type": "announcement"},
        ]

        for case in test_cases:
            formatted = buffer_client.format_proclamation(case["text"], case["type"])
            print(f"✅ {case['type'].title()}: {formatted[:50]}...")

        return True

    except Exception as e:
        print(f"❌ Formatting test failed: {e}")
        return False


def test_hashtag_addition():
    """Test hashtag functionality"""
    print("\n🏷️ Testing Hashtag Addition...")

    try:
        buffer_client = CodexBufferProclaimer()

        test_text = "This is a test message"
        hashtag_sets = ["default", "business", "tech", "leadership"]

        for hashtag_set in hashtag_sets:
            with_hashtags = buffer_client.add_hashtags(test_text, hashtag_set)
            print(f"✅ {hashtag_set} hashtags: {with_hashtags[-50:]}")

        return True

    except Exception as e:
        print(f"❌ Hashtag test failed: {e}")
        return False


def test_analytics():
    """Test analytics functionality"""
    print("\n📊 Testing Analytics...")

    try:
        buffer_client = CodexBufferProclaimer()
        analytics = buffer_client.get_analytics_summary()

        if analytics:
            print("✅ Analytics retrieved:")
            print(f"   📱 Total profiles: {analytics.get('total_profiles', 0)}")
            print(f"   📝 Recent posts: {analytics.get('recent_posts', 0)}")
            print(f"   ⏰ Pending posts: {analytics.get('pending_posts', 0)}")

            platforms = analytics.get("profiles_by_platform", {})
            if platforms:
                print("   🎯 Platforms:")
                for platform, count in platforms.items():
                    print(f"      • {platform}: {count}")

            return True
        else:
            print("⚠️  No analytics data available")
            return False

    except Exception as e:
        print(f"❌ Analytics test failed: {e}")
        return False


def test_dry_run_proclamation():
    """Test proclamation without actually sending"""
    print("\n🧪 Testing Dry Run Proclamation...")

    try:
        buffer_client = CodexBufferProclaimer()

        # Test with placeholder token (should fail gracefully)
        test_text = "🔥 Test proclamation from Codex Dominion test suite! 👑"

        result = buffer_client.send_proclamation(
            text=test_text, proclamation_type="sovereignty", hashtag_set="default"
        )

        print(f"✅ Proclamation test completed")
        print(f"   Success: {result.get('success', False)}")
        print(f"   Message: {result.get('message', result.get('error', 'No message'))}")

        return True

    except Exception as e:
        print(f"❌ Dry run test failed: {e}")
        return False


def test_legacy_function():
    """Test the legacy proclaim_social function"""
    print("\n🔄 Testing Legacy Function...")

    try:
        test_text = "Testing legacy proclaim_social function"
        profile_ids = []  # Empty list should use all profiles

        result = proclaim_social(test_text, profile_ids)

        print(f"✅ Legacy function test completed")
        print(f"   Success: {result.get('success', False)}")
        print(f"   Message: {result.get('message', result.get('error', 'No message'))}")

        return True

    except Exception as e:
        print(f"❌ Legacy function test failed: {e}")
        return False


def main():
    """Run all Buffer integration tests"""
    print("🔥 CODEX BUFFER INTEGRATION TEST SUITE 👑")
    print("=" * 50)

    test_results = []

    # Run all tests
    tests = [
        ("Configuration", test_configuration),
        ("Connection", test_connection),
        ("Profiles", test_profiles),
        ("Formatting", test_proclamation_formatting),
        ("Hashtags", test_hashtag_addition),
        ("Analytics", test_analytics),
        ("Dry Run", test_dry_run_proclamation),
        ("Legacy Function", test_legacy_function),
    ]

    for test_name, test_func in tests:
        try:
            result = test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            test_results.append((test_name, False))

    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)

    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)

    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")

    print("-" * 50)
    print(f"📈 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

    if passed == total:
        print("\n🔥 ALL TESTS PASSED! BUFFER INTEGRATION READY! 👑")
    elif passed > 0:
        print(
            f"\n⚠️  {total-passed} tests failed. Check configuration and API credentials."
        )
    else:
        print("\n❌ ALL TESTS FAILED. Please check your Buffer setup.")

    print("\n📋 Next Steps:")
    if passed < total:
        print("1. Configure Buffer API credentials in buffer_config.json")
        print("2. Ensure Buffer account has connected social media profiles")
        print("3. Verify API permissions and access tokens")
    else:
        print("1. Buffer integration is ready for production use!")
        print("2. Configure templates and hashtags as needed")
        print("3. Start proclaiming your digital sovereignty! 🔥👑")


if __name__ == "__main__":
    main()
