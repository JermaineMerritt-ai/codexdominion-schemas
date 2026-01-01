"""
Test suite for Council helper functions
Tests domain lookup and combined permission checking.
"""

import sys
from council_engine import council_engine, get_council_by_domain, council_allows_action

def test_get_council_by_domain_engine():
    """Test: Get first council by domain using engine method"""
    print("\n🧪 TEST: Get council by domain (engine method)")
    
    council = council_engine.get_council_by_domain("policy")
    
    assert council is not None, "Should find council with 'policy' domain"
    assert council.name == "Governance Council"
    assert "policy" in council.domains
    
    print(f"✅ SUCCESS: Found {council.name} for domain 'policy'")
    print(f"   Domains: {', '.join(council.domains)}")

def test_get_council_by_domain_utility():
    """Test: Get council by domain using utility function"""
    print("\n🧪 TEST: Get council by domain (utility function)")
    
    council_dict = get_council_by_domain("safety")
    
    assert council_dict is not None, "Should find council with 'safety' domain"
    assert council_dict["name"] == "Governance Council"
    assert "safety" in council_dict["domains"]
    
    print(f"✅ SUCCESS: Found {council_dict['name']} for domain 'safety'")
    print(f"   ID: {council_dict['id']}")

def test_council_allows_action_blocked():
    """Test: Check blocked action using engine method"""
    print("\n🧪 TEST: Council allows action - BLOCKED")
    
    # Action blocked by oversight
    allowed = council_engine.council_allows_action(
        "council_governance",
        "delete_user_data",
        None
    )
    
    assert allowed is False, "delete_user_data should be blocked"
    
    print(f"✅ SUCCESS: Action 'delete_user_data' correctly blocked")

def test_council_allows_action_allowed():
    """Test: Check allowed action using engine method"""
    print("\n🧪 TEST: Council allows action - ALLOWED")
    
    # Action not blocked, low savings (no review needed)
    allowed = council_engine.council_allows_action(
        "council_governance",
        "create_workflow",
        {"weekly_savings": 1000}
    )
    
    assert allowed is True, "create_workflow with $1000 should be allowed"
    
    print(f"✅ SUCCESS: Action 'create_workflow' correctly allowed")

def test_council_allows_action_review_required():
    """Test: Check action requiring review using engine method"""
    print("\n🧪 TEST: Council allows action - REVIEW REQUIRED")
    
    # Action not blocked, but high savings (requires review)
    allowed = council_engine.council_allows_action(
        "council_governance",
        "create_workflow",
        {"weekly_savings": 10000}
    )
    
    assert allowed is False, "High savings ($10k) should require review"
    
    print(f"✅ SUCCESS: Action correctly flagged for review (weekly savings: $10,000)")

def test_council_allows_action_utility_blocked():
    """Test: Check blocked action using utility function"""
    print("\n🧪 TEST: Council allows action (utility) - BLOCKED")
    
    council_dict = get_council_by_domain("safety")
    
    allowed = council_allows_action(
        council_dict,
        "delete_user_data",
        None
    )
    
    assert allowed is False, "delete_user_data should be blocked"
    
    print(f"✅ SUCCESS: Utility function correctly blocks action")

def test_council_allows_action_utility_threshold():
    """Test: Check review threshold using utility function"""
    print("\n🧪 TEST: Council allows action (utility) - THRESHOLD")
    
    council_dict = get_council_by_domain("policy")
    
    # Below threshold
    allowed_low = council_allows_action(
        council_dict,
        "update_policy",
        {"weekly_savings": 3000}
    )
    
    # Above threshold
    allowed_high = council_allows_action(
        council_dict,
        "update_policy",
        {"weekly_savings": 15000}
    )
    
    assert allowed_low is True, "$3k should be allowed (below $5k threshold)"
    assert allowed_high is False, "$15k should require review (above $5k threshold)"
    
    print(f"✅ SUCCESS: Threshold checking works correctly")
    print(f"   $3,000 → allowed: {allowed_low}")
    print(f"   $15,000 → requires review: {not allowed_high}")

def test_council_allows_action_total_weekly_savings():
    """Test: Check action using total_weekly_savings field"""
    print("\n🧪 TEST: Council allows action - total_weekly_savings field")
    
    # Test with alternative field name
    allowed = council_engine.council_allows_action(
        "council_governance",
        "create_workflow",
        {"total_weekly_savings": 8000}
    )
    
    assert allowed is False, "Should use total_weekly_savings for threshold check"
    
    print(f"✅ SUCCESS: Alternative savings field 'total_weekly_savings' works")

def test_nonexistent_domain():
    """Test: Get council by nonexistent domain"""
    print("\n🧪 TEST: Get council by nonexistent domain")
    
    # Engine method
    council = council_engine.get_council_by_domain("nonexistent_domain")
    assert council is None
    
    # Utility function
    council_dict = get_council_by_domain("nonexistent_domain")
    assert council_dict is None
    
    print(f"✅ SUCCESS: Returns None for nonexistent domain")

def test_nonexistent_council():
    """Test: Check action for nonexistent council"""
    print("\n🧪 TEST: Check action for nonexistent council")
    
    # Should default to allow if council not found
    allowed = council_engine.council_allows_action(
        "council_nonexistent",
        "any_action",
        {"weekly_savings": 10000}
    )
    
    assert allowed is True, "Should default to allow if council not found"
    
    print(f"✅ SUCCESS: Defaults to allow for nonexistent council")

def run_all_tests():
    """Run all council helper tests"""
    print("\n" + "="*60)
    print("🔥 COUNCIL HELPER FUNCTIONS TEST SUITE 🔥")
    print("="*60)
    
    try:
        # Test domain lookup
        test_get_council_by_domain_engine()
        test_get_council_by_domain_utility()
        
        # Test permission checking (engine methods)
        test_council_allows_action_blocked()
        test_council_allows_action_allowed()
        test_council_allows_action_review_required()
        test_council_allows_action_total_weekly_savings()
        
        # Test permission checking (utility functions)
        test_council_allows_action_utility_blocked()
        test_council_allows_action_utility_threshold()
        
        # Test edge cases
        test_nonexistent_domain()
        test_nonexistent_council()
        
        print("\n" + "="*60)
        print("✅ ALL COUNCIL HELPER TESTS PASSED!")
        print("="*60)
        print("\n📊 Test Coverage:")
        print("   ✅ Domain lookup (engine + utility)")
        print("   ✅ Blocked action detection")
        print("   ✅ Review threshold enforcement")
        print("   ✅ Alternative field names (total_weekly_savings)")
        print("   ✅ Edge cases (nonexistent domains/councils)")
        print("\n🔥 THE FLAME BURNS SOVEREIGN AND ETERNAL! 👑\n")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()
