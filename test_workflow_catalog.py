"""
Test suite for Workflow Catalog
Tests workflow type definitions and catalog API endpoints.
"""

import sys
from workflow_catalog import (
    get_workflow_type, 
    list_workflow_types, 
    get_workflow_domain,
    get_calculator_defaults,
    merge_calculator_inputs
)

def test_get_workflow_type():
    """Test: Get workflow type by ID"""
    print("\n🧪 TEST: Get workflow type")
    
    wt = get_workflow_type("customer_followup")
    
    assert wt is not None
    assert wt.id == "customer_followup"
    assert wt.name == "Customer Follow-up Automation"
    assert wt.domain == "commerce"
    assert "tasks_per_week" in wt.required_inputs
    
    print(f"✅ SUCCESS: Retrieved workflow type '{wt.name}'")
    print(f"   Domain: {wt.domain}")
    print(f"   Category: {wt.category}")
    print(f"   Required inputs: {len(wt.required_inputs)}")

def test_list_workflow_types():
    """Test: List all workflow types"""
    print("\n🧪 TEST: List all workflow types")
    
    types = list_workflow_types()
    
    assert len(types) >= 6, "Should have at least 6 workflow types"
    assert "customer_followup" in types
    assert "invoice_reminders" in types
    assert "content_scheduler" in types
    
    print(f"✅ SUCCESS: Found {len(types)} workflow types")
    for wid, winfo in types.items():
        print(f"   - {winfo['name']} ({winfo['domain']})")

def test_get_workflow_domain():
    """Test: Get domain for workflow type"""
    print("\n🧪 TEST: Get workflow domain")
    
    domain = get_workflow_domain("customer_followup")
    assert domain == "commerce"
    
    domain = get_workflow_domain("data_entry_automation")
    assert domain == "automation"
    
    domain = get_workflow_domain("nonexistent")
    assert domain is None
    
    print(f"✅ SUCCESS: Domain mapping works correctly")
    print(f"   customer_followup → commerce")
    print(f"   data_entry_automation → automation")

def test_get_calculator_defaults():
    """Test: Get calculator defaults"""
    print("\n🧪 TEST: Get calculator defaults")
    
    defaults = get_calculator_defaults("invoice_reminders")
    
    assert defaults["error_rate"] == 0.05
    assert defaults["cost_per_error"] == 25
    assert defaults["value_per_accelerated_task"] == 15
    
    print(f"✅ SUCCESS: Retrieved calculator defaults")
    print(f"   error_rate: {defaults['error_rate']}")
    print(f"   cost_per_error: ${defaults['cost_per_error']}")

def test_merge_calculator_inputs():
    """Test: Merge user inputs with defaults"""
    print("\n🧪 TEST: Merge calculator inputs")
    
    user_inputs = {
        "tasks_per_week": 200,
        "time_per_task_minutes": 10,
        "hourly_wage": 25
    }
    
    merged = merge_calculator_inputs("customer_followup", user_inputs)
    
    # Should have user inputs
    assert merged["tasks_per_week"] == 200
    assert merged["hourly_wage"] == 25
    
    # Should have defaults
    assert merged["value_per_accelerated_task"] == 0
    
    print(f"✅ SUCCESS: Merged inputs correctly")
    print(f"   User inputs: {len(user_inputs)}")
    print(f"   Merged result: {len(merged)}")

def test_workflow_categories():
    """Test: Workflow categorization"""
    print("\n🧪 TEST: Workflow categories")
    
    types = list_workflow_types()
    categories = set(winfo["category"] for winfo in types.values())
    
    assert "crm" in categories
    assert "finance" in categories
    assert "marketing" in categories
    
    print(f"✅ SUCCESS: Found {len(categories)} categories")
    print(f"   Categories: {', '.join(sorted(categories))}")

def test_workflow_domains():
    """Test: Workflow domains"""
    print("\n🧪 TEST: Workflow domains")
    
    types = list_workflow_types()
    domains = set(winfo["domain"] for winfo in types.values())
    
    assert "commerce" in domains
    assert "automation" in domains
    assert "media" in domains
    
    print(f"✅ SUCCESS: Found {len(domains)} domains")
    print(f"   Domains: {', '.join(sorted(domains))}")

def run_all_tests():
    """Run all workflow catalog tests"""
    print("\n" + "="*60)
    print("🔥 WORKFLOW CATALOG TEST SUITE 🔥")
    print("="*60)
    
    try:
        # Test basic operations
        test_get_workflow_type()
        test_list_workflow_types()
        
        # Test domain mapping
        test_get_workflow_domain()
        
        # Test calculator integration
        test_get_calculator_defaults()
        test_merge_calculator_inputs()
        
        # Test categorization
        test_workflow_categories()
        test_workflow_domains()
        
        print("\n" + "="*60)
        print("✅ ALL WORKFLOW CATALOG TESTS PASSED!")
        print("="*60)
        print("\n📊 Test Coverage:")
        print("   ✅ Workflow type retrieval")
        print("   ✅ Catalog listing")
        print("   ✅ Domain mapping")
        print("   ✅ Calculator defaults")
        print("   ✅ Input merging")
        print("   ✅ Categorization")
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
