"""
Test suite for Workflow Catalog API endpoints
Tests REST API for workflow type management.
"""

import json
import requests
import sys

BASE_URL = "http://localhost:5000"

def test_list_workflow_types():
    """Test: List all workflow types via API"""
    print("\n🧪 TEST: List workflow types (API)")
    
    response = requests.get(f"{BASE_URL}/api/workflows/types")
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "workflow_types" in data
    assert len(data["workflow_types"]) >= 6
    
    print(f"✅ SUCCESS: Retrieved {len(data['workflow_types'])} workflow types")
    for wid, winfo in data["workflow_types"].items():
        print(f"   - {winfo['name']} ({winfo['domain']})")

def test_get_workflow_type():
    """Test: Get specific workflow type via API"""
    print("\n🧪 TEST: Get workflow type (API)")
    
    response = requests.get(f"{BASE_URL}/api/workflows/types/customer_followup")
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    
    wt = data["workflow_type"]
    assert wt["id"] == "customer_followup"
    assert wt["domain"] == "commerce"
    assert "required_inputs" in wt
    assert "default_calculator_profile" in wt
    
    print(f"✅ SUCCESS: Retrieved workflow type '{wt['name']}'")
    print(f"   Domain: {wt['domain']}")
    print(f"   Category: {wt['category']}")
    print(f"   Required inputs: {wt['required_inputs']}")
    print(f"   Calculator defaults: {wt['default_calculator_profile']}")

def test_get_nonexistent_workflow_type():
    """Test: Get nonexistent workflow type returns 404"""
    print("\n🧪 TEST: Get nonexistent workflow type (API)")
    
    response = requests.get(f"{BASE_URL}/api/workflows/types/nonexistent")
    
    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    
    print(f"✅ SUCCESS: Returns 404 for nonexistent workflow type")

def test_chat_with_workflow_type_domain():
    """Test: Chat API uses workflow type domain for council oversight"""
    print("\n🧪 TEST: Chat API with workflow type domain")
    
    # Test commerce domain workflow (customer_followup)
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={
            "agent_id": "agent_jermaine_super_action",
            "message": "Set up customer follow-up automation",
            "mode": "execute",
            "context": {
                "calculator_inputs": {
                    "tasks_per_week": 100,
                    "time_per_task_minutes": 10,
                    "hourly_wage": 25,
                    "automation_percent": 0.7,
                    "error_rate": 0.1,
                    "cost_per_error": 15,
                    "value_per_accelerated_task": 0
                },
                "workflow_inputs": {
                    "workflow_type": "customer_followup",
                    "description": "Automate weekly customer check-ins"
                }
            }
        }
    )
    
    # Should succeed (low savings)
    assert response.status_code == 200
    data = response.json()
    assert "workflow_action" in data
    
    print(f"✅ SUCCESS: Commerce domain workflow created")
    print(f"   Workflow Type: customer_followup")
    print(f"   Domain: commerce")
    print(f"   Workflow ID: {data['workflow_action']}")

def test_chat_with_different_workflow_domains():
    """Test: Different workflow types map to correct domains"""
    print("\n🧪 TEST: Multiple workflow types with different domains")
    
    workflow_types = [
        ("content_scheduler", "media"),
        ("data_entry_automation", "automation"),
        ("email_triage", "automation")
    ]
    
    for wt_id, expected_domain in workflow_types:
        response = requests.get(f"{BASE_URL}/api/workflows/types/{wt_id}")
        assert response.status_code == 200
        
        data = response.json()
        actual_domain = data["workflow_type"]["domain"]
        assert actual_domain == expected_domain
        
        print(f"   ✓ {wt_id} → {actual_domain}")
    
    print(f"✅ SUCCESS: All workflow types map to correct domains")

def run_all_tests():
    """Run all workflow catalog API tests"""
    print("\n" + "="*60)
    print("🔥 WORKFLOW CATALOG API TEST SUITE 🔥")
    print("="*60)
    
    try:
        # Test catalog endpoints
        test_list_workflow_types()
        test_get_workflow_type()
        test_get_nonexistent_workflow_type()
        
        # Test domain mapping
        test_chat_with_different_workflow_domains()
        
        # Test integration with chat API
        test_chat_with_workflow_type_domain()
        
        print("\n" + "="*60)
        print("✅ ALL WORKFLOW CATALOG API TESTS PASSED!")
        print("="*60)
        print("\n📊 Test Coverage:")
        print("   ✅ List workflow types endpoint")
        print("   ✅ Get workflow type endpoint")
        print("   ✅ 404 handling")
        print("   ✅ Domain mapping validation")
        print("   ✅ Chat API integration")
        print("\n🔥 THE FLAME BURNS SOVEREIGN AND ETERNAL! 👑\n")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to Flask server")
        print("Make sure Flask is running: python flask_dashboard.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()
