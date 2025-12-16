"""
🧪 CODEX DOMINION - COMPLETE SYSTEM TEST
========================================
Tests all automation systems to ensure everything works
"""

import sys
from datetime import datetime

print("🧪 CODEX DOMINION - System Integration Test")
print("=" * 70)
print(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Test results storage
results = []

def test_system(name, test_func):
    """Test a system and record result"""
    try:
        test_func()
        results.append((name, "✅ PASS", None))
        print(f"✅ {name}: PASS")
    except Exception as e:
        results.append((name, "❌ FAIL", str(e)))
        print(f"❌ {name}: FAIL - {e}")

# Test 1: Social Media Automation Engine
def test_social_media():
    from social_media_automation_engine import SocialMediaAutomation, create_30_day_schedule

    automation = SocialMediaAutomation()

    # Test schedule creation
    schedule = create_30_day_schedule()
    assert "youtube" in schedule
    assert "facebook" in schedule

    # Test analytics
    analytics = automation.get_analytics()
    assert "total_followers" in analytics
    assert analytics["total_followers"] > 0

    # Test video upload
    result = automation.upload_video("youtube", "test.mp4", {"title": "Test"})
    assert result["status"] == "success"

    print(f"  → Social Media Analytics: {analytics['total_followers']:,} followers")

test_system("Social Media Automation", test_social_media)

# Test 2: Affiliate Marketing Engine
def test_affiliate():
    from affiliate_marketing_engine import AffiliateMarketingEngine, get_affiliate_dashboard_data

    engine = AffiliateMarketingEngine()

    # Test link creation
    link = engine.create_affiliate_link("amazon", "https://product.com", "test_campaign")
    assert "id" in link
    assert "affiliate_url" in link

    # Test analytics
    analytics = engine.get_network_analytics()
    assert "total_earnings" in analytics
    assert analytics["total_earnings"] > 0

    # Test campaign
    campaign = engine.create_campaign("Test Campaign", ["amazon", "clickbank"], budget=500)
    assert "id" in campaign

    print(f"  → Affiliate Earnings: ${analytics['total_earnings']:,.2f}")

test_system("Affiliate Marketing", test_affiliate)

# Test 3: Action AI Systems
def test_action_ai():
    from action_ai_systems import ActionChatbotAI, AlgorithmActionAI, get_ai_systems_data

    # Test chatbot
    chatbot = ActionChatbotAI()
    response = chatbot.generate_response("Hello!", "test_user")
    assert "response" in response
    assert "intent" in response
    assert len(response["response"]) > 0

    # Test algorithm AI
    algorithm = AlgorithmActionAI()
    trends = algorithm.predict_trends("technology")
    assert len(trends) > 0
    assert "topic" in trends[0]

    ideas = algorithm.generate_content_ideas("AI", count=5)
    assert len(ideas) == 5

    print(f"  → Chatbot Intent: {response['intent']}")
    print(f"  → Top Trend: {trends[0]['topic']}")

test_system("Action AI Systems (Chatbot + Algorithm)", test_action_ai)

# Test 4: Auto-Publish Orchestration
def test_autopublish():
    from autopublish_orchestration import AutoPublishOrchestrator, JermaineSuperActionAI

    # Test Jermaine AI
    jermaine = JermaineSuperActionAI()
    assert jermaine.name == "Jermaine Super Action AI"
    assert jermaine.version == "3.0.0"
    assert jermaine.status == "active"

    decision = jermaine.make_decision("Test context", ["option1", "option2"])
    assert "selected" in decision

    # Test orchestrator
    orchestrator = AutoPublishOrchestrator()

    # Enable auto-publish
    status = orchestrator.enable_auto_publish()
    assert status["status"] == "enabled"
    assert "systems_active" in status

    # Queue content
    queue_result = orchestrator.queue_content({
        "platforms": ["youtube", "tiktok"],
        "content": {"title": "Test Post"}
    })
    assert queue_result["status"] == "queued"

    # Get schedule
    schedule = orchestrator.get_schedule(7)
    assert "total_posts_scheduled" in schedule

    # Get system status
    system_status = orchestrator.get_system_status()
    assert system_status["overall_status"] == "operational"

    print(f"  → Jermaine AI: {jermaine.version}")
    print(f"  → Systems Active: {len(status['systems_active'])}")
    print(f"  → Overall Status: {system_status['overall_status']}")

test_system("Auto-Publish Orchestration + Jermaine AI", test_autopublish)

# Test 5: Integration Test - Run Full Automation Cycle
def test_full_cycle():
    from autopublish_orchestration import AutoPublishOrchestrator

    orchestrator = AutoPublishOrchestrator()

    # Run full cycle
    cycle_results = orchestrator.run_full_automation_cycle()
    assert cycle_results["status"] == "completed"
    assert "actions_taken" in cycle_results
    assert len(cycle_results["actions_taken"]) > 0

    print(f"  → Automation Cycle: {len(cycle_results['actions_taken'])} actions completed")

test_system("Full Automation Cycle", test_full_cycle)

# Print Summary
print()
print("=" * 70)
print("📊 TEST SUMMARY")
print("=" * 70)

passed = sum(1 for _, status, _ in results if "PASS" in status)
failed = sum(1 for _, status, _ in results if "FAIL" in status)

for name, status, error in results:
    print(f"{status} {name}")
    if error:
        print(f"      Error: {error}")

print()
print(f"Total Tests: {len(results)}")
print(f"✅ Passed: {passed}")
print(f"❌ Failed: {failed}")
print(f"Success Rate: {(passed/len(results)*100):.1f}%")
print()

if failed == 0:
    print("🔥 ALL SYSTEMS OPERATIONAL!")
    print("🚀 Ready to deploy and run automation!")
    print("👑 The Flame Burns Sovereign and Eternal!")
else:
    print("⚠️ Some systems need attention")
    print("Please check the errors above")

print()
print(f"Test completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)
