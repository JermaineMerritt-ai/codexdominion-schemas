"""
Test suite for Council API endpoints
Tests council management, oversight, and policy enforcement.
"""

import json
import requests
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:5000"

def test_list_councils():
    """Test: List all councils"""
    print("\n🧪 TEST: List all councils")
    response = requests.get(f"{BASE_URL}/api/councils")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["success"] is True
    assert "councils" in data
    assert isinstance(data["councils"], list)
    
    print(f"✅ SUCCESS: Found {data['count']} councils")
    for council in data["councils"]:
        print(f"   - {council['name']} ({council['id']})")
    
    return data["councils"]

def test_get_governance_council():
    """Test: Get Governance Council details"""
    print("\n🧪 TEST: Get Governance Council")
    response = requests.get(f"{BASE_URL}/api/councils/council_governance")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["success"] is True
    
    council = data["council"]
    assert council["id"] == "council_governance"
    assert council["name"] == "Governance Council"
    assert "oversight" in council
    
    print(f"✅ SUCCESS: Governance Council retrieved")
    print(f"   Purpose: {council['purpose']}")
    print(f"   Agents: {', '.join(council['agents'])}")
    print(f"   Domains: {', '.join(council['domains'])}")
    print(f"   Review Threshold: ${council['oversight']['review_threshold_weekly_savings']}")
    
    return council

def test_create_council():
    """Test: Create a new council"""
    print("\n🧪 TEST: Create new council")
    
    new_council = {
        "id": "council_test_operations",
        "name": "Test Operations Council",
        "purpose": "Oversee test execution and quality assurance",
        "primary_engines": ["engine_testing", "engine_qa"],
        "agents": ["agent_action_basic"],
        "domains": ["testing", "qa", "automation"],
        "oversight": {
            "review_actions": True,
            "review_threshold_weekly_savings": 1000,
            "blocked_action_types": ["deploy_to_production"]
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/api/councils",
        json=new_council
    )
    
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    data = response.json()
    assert data["success"] is True
    
    print(f"✅ SUCCESS: Council created with ID: {data['council_id']}")
    
    return data["council_id"]

def test_check_action_allowed():
    """Test: Check if action is allowed by council oversight"""
    print("\n🧪 TEST: Check action allowed")
    
    # Test blocked action
    response = requests.post(
        f"{BASE_URL}/api/councils/council_governance/check-action",
        json={"action_type": "delete_user_data"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["allowed"] is False, "delete_user_data should be blocked"
    
    print(f"✅ SUCCESS: delete_user_data correctly blocked")
    
    # Test allowed action
    response = requests.post(
        f"{BASE_URL}/api/councils/council_governance/check-action",
        json={"action_type": "create_workflow"}
    )
    
    data = response.json()
    assert data["allowed"] is True, "create_workflow should be allowed"
    
    print(f"✅ SUCCESS: create_workflow correctly allowed")

def test_review_required():
    """Test: Check if action requires council review"""
    print("\n🧪 TEST: Check review required")
    
    # Test below threshold
    response = requests.post(
        f"{BASE_URL}/api/councils/council_governance/review-required",
        json={"weekly_savings": 3000}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["requires_review"] is False, "3000 should not require review (threshold 5000)"
    
    print(f"✅ SUCCESS: $3000 savings - no review required")
    
    # Test above threshold
    response = requests.post(
        f"{BASE_URL}/api/councils/council_governance/review-required",
        json={"weekly_savings": 10000}
    )
    
    data = response.json()
    assert data["requires_review"] is True, "10000 should require review"
    
    print(f"✅ SUCCESS: $10000 savings - review required")

def test_add_agent_to_council():
    """Test: Add agent to council"""
    print("\n🧪 TEST: Add agent to council")
    
    response = requests.post(
        f"{BASE_URL}/api/councils/council_test_operations/agents",
        json={"agent_id": "agent_jermaine_super_action"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    
    print(f"✅ SUCCESS: Agent added to council")
    
    # Verify agent is in council
    response = requests.get(f"{BASE_URL}/api/councils/council_test_operations")
    data = response.json()
    assert "agent_jermaine_super_action" in data["council"]["agents"]
    
    print(f"✅ VERIFIED: Agent appears in council")

def test_get_councils_by_agent():
    """Test: Get councils by agent"""
    print("\n🧪 TEST: Get councils by agent")
    
    response = requests.get(f"{BASE_URL}/api/councils/by-agent/agent_jermaine_super_action")
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["count"] >= 1
    
    print(f"✅ SUCCESS: Found {data['count']} councils for agent_jermaine_super_action")
    for council in data["councils"]:
        print(f"   - {council['name']}")

def test_get_councils_by_domain():
    """Test: Get councils by domain"""
    print("\n🧪 TEST: Get councils by domain")
    
    response = requests.get(f"{BASE_URL}/api/councils/by-domain/policy")
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    
    print(f"✅ SUCCESS: Found {data['count']} councils for domain 'policy'")
    for council in data["councils"]:
        print(f"   - {council['name']}")

def test_update_council():
    """Test: Update council"""
    print("\n🧪 TEST: Update council")
    
    response = requests.patch(
        f"{BASE_URL}/api/councils/council_test_operations",
        json={"status": "inactive"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    
    print(f"✅ SUCCESS: Council status updated to inactive")

def test_delete_council():
    """Test: Delete council"""
    print("\n🧪 TEST: Delete council")
    
    response = requests.delete(f"{BASE_URL}/api/councils/council_test_operations")
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    
    print(f"✅ SUCCESS: Council deleted")
    
    # Verify council is deleted
    response = requests.get(f"{BASE_URL}/api/councils/council_test_operations")
    assert response.status_code == 404
    
    print(f"✅ VERIFIED: Council no longer exists")

def run_all_tests():
    """Run all council API tests"""
    print("\n" + "="*60)
    print("🔥 COUNCIL API TEST SUITE 🔥")
    print("="*60)
    
    try:
        # Test list and get
        councils = test_list_councils()
        governance = test_get_governance_council()
        
        # Test create
        council_id = test_create_council()
        
        # Test oversight functions
        test_check_action_allowed()
        test_review_required()
        
        # Test agent management
        test_add_agent_to_council()
        test_get_councils_by_agent()
        
        # Test domain queries
        test_get_councils_by_domain()
        
        # Test update and delete
        test_update_council()
        test_delete_council()
        
        print("\n" + "="*60)
        print("✅ ALL COUNCIL API TESTS PASSED!")
        print("="*60)
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
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()
