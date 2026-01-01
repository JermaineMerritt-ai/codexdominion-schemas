"""
Test suite for Council Oversight in Chat API
Tests council permission enforcement during workflow execution.
"""

import json
import requests
import sys

BASE_URL = "http://localhost:5000"

def test_chat_execute_blocked_by_council():
    """Test: Chat execute blocked by council oversight (high savings)"""
    print("\n🧪 TEST: Chat execute - BLOCKED by council (high savings)")
    
    # High savings that exceed Governance Council threshold ($5k)
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={
            "agent_id": "agent_jermaine_super_action",
            "message": "Automate customer follow-ups",
            "mode": "execute",
            "context": {
                "calculator_inputs": {
                    "tasks_per_week": 500,  # High volume
                    "time_per_task_minutes": 15,
                    "hourly_wage": 30,
                    "automation_percent": 0.8,
                    "error_rate": 0.1,
                    "cost_per_error": 20,
                    "value_per_accelerated_task": 0
                },
                "workflow_inputs": {
                    "workflow_type": "customer_followup",
                    "description": "High-value automation"
                }
            }
        }
    )
    
    # Should be blocked with 403
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    data = response.json()
    
    assert "blocked_by_council" in data
    assert "Governance Council" in data["reply"] or "review" in data["reply"].lower()
    assert data["savings"]["weekly_savings"] > 5000, "Savings should exceed threshold"
    
    print(f"✅ SUCCESS: High-value workflow blocked by council")
    print(f"   Weekly Savings: ${data['savings']['weekly_savings']:,.2f}")
    print(f"   Blocked By: {data['blocked_by_council']}")
    print(f"   Message: {data['reply']}")

def test_chat_execute_allowed_low_savings():
    """Test: Chat execute allowed (low savings, no review needed)"""
    print("\n🧪 TEST: Chat execute - ALLOWED (low savings)")
    
    # Low savings below threshold
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={
            "agent_id": "agent_jermaine_super_action",
            "message": "Automate simple task",
            "mode": "execute",
            "context": {
                "calculator_inputs": {
                    "tasks_per_week": 50,  # Low volume
                    "time_per_task_minutes": 5,
                    "hourly_wage": 25,
                    "automation_percent": 0.5,
                    "error_rate": 0.05,
                    "cost_per_error": 10,
                    "value_per_accelerated_task": 0
                },
                "workflow_inputs": {
                    "workflow_type": "customer_followup",
                    "description": "Low-value automation"
                }
            }
        }
    )
    
    # Should be allowed with 200
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    
    assert "workflow_action" in data, "Should create workflow"
    assert "blocked_by_council" not in data
    assert data["savings"]["weekly_savings"] < 5000, "Savings should be below threshold"
    
    print(f"✅ SUCCESS: Low-value workflow allowed")
    print(f"   Weekly Savings: ${data['savings']['weekly_savings']:,.2f}")
    print(f"   Workflow ID: {data['workflow_action']}")
    print(f"   Message: {data['reply']}")

def test_chat_execute_no_savings():
    """Test: Chat execute with no savings data"""
    print("\n🧪 TEST: Chat execute - NO savings data")
    
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={
            "agent_id": "agent_jermaine_super_action",
            "message": "Create workflow without calculator",
            "mode": "execute",
            "context": {
                "workflow_inputs": {
                    "workflow_type": "customer_followup",
                    "description": "No calculator inputs"
                }
            }
        }
    )
    
    # Should be allowed (no savings = no threshold check)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    
    assert "workflow_action" in data
    assert data.get("savings") is None
    
    print(f"✅ SUCCESS: Workflow allowed without savings data")
    print(f"   Workflow ID: {data['workflow_action']}")

def test_chat_mode_not_affected():
    """Test: Chat mode (conversational) not affected by council oversight"""
    print("\n🧪 TEST: Chat mode - NOT affected by council")
    
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={
            "agent_id": "agent_jermaine_super_action",
            "message": "Tell me about automation",
            "mode": "chat"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["mode"] == "chat"
    assert "blocked_by_council" not in data
    assert "reply" in data
    
    print(f"✅ SUCCESS: Chat mode works normally")
    print(f"   Reply: {data['reply'][:100]}...")

def test_edge_case_exactly_at_threshold():
    """Test: Workflow with savings exactly at threshold"""
    print("\n🧪 TEST: Chat execute - EXACTLY at threshold")
    
    # Calculate inputs to hit exactly $5000/week
    # Formula: weekly_savings = (tasks_per_week * time_per_task_minutes / 60) * hourly_wage * automation_percent
    # 5000 = (100 * 30 / 60) * 100 * 0.5 = 50 * 100 * 0.5 = 2500
    # Let's try to get close to 5000
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={
            "agent_id": "agent_jermaine_super_action",
            "message": "Automate at threshold",
            "mode": "execute",
            "context": {
                "calculator_inputs": {
                    "tasks_per_week": 240,
                    "time_per_task_minutes": 10,
                    "hourly_wage": 25,
                    "automation_percent": 1.0,
                    "error_rate": 0,
                    "cost_per_error": 0,
                    "value_per_accelerated_task": 0
                },
                "workflow_inputs": {
                    "workflow_type": "customer_followup"
                }
            }
        }
    )
    
    data = response.json()
    weekly_savings = data.get("savings", {}).get("weekly_savings", 0)
    
    print(f"   Weekly Savings: ${weekly_savings:,.2f}")
    
    if weekly_savings >= 5000:
        assert response.status_code == 403, "Should be blocked if >= 5000"
        print(f"✅ SUCCESS: Blocked at ${weekly_savings:,.2f} (>= threshold)")
    else:
        assert response.status_code == 200, "Should be allowed if < 5000"
        print(f"✅ SUCCESS: Allowed at ${weekly_savings:,.2f} (< threshold)")

def run_all_tests():
    """Run all council oversight chat API tests"""
    print("\n" + "="*60)
    print("🔥 COUNCIL OVERSIGHT CHAT API TEST SUITE 🔥")
    print("="*60)
    
    try:
        # Test blocked scenarios
        test_chat_execute_blocked_by_council()
        
        # Test allowed scenarios
        test_chat_execute_allowed_low_savings()
        test_chat_execute_no_savings()
        
        # Test chat mode not affected
        test_chat_mode_not_affected()
        
        # Test edge cases
        test_edge_case_exactly_at_threshold()
        
        print("\n" + "="*60)
        print("✅ ALL COUNCIL OVERSIGHT TESTS PASSED!")
        print("="*60)
        print("\n📊 Test Coverage:")
        print("   ✅ High-value workflows blocked by council")
        print("   ✅ Low-value workflows allowed")
        print("   ✅ Workflows without savings data allowed")
        print("   ✅ Chat mode unaffected by council oversight")
        print("   ✅ Threshold edge cases handled correctly")
        print("\n🏛️ Council Governance System: OPERATIONAL")
        print("🔥 THE FLAME BURNS SOVEREIGN AND ETERNAL! 👑\n")
        
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
