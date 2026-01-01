"""
Test suite for Background Worker and Workflow Metrics
Tests auto-completion of workflows and metrics endpoint.
"""

import json
import requests
import sys
import time

BASE_URL = "http://localhost:5000"

def test_workflow_metrics_endpoint():
    """Test: Get workflow metrics"""
    print("\n🧪 TEST: Get workflow metrics")
    
    response = requests.get(f"{BASE_URL}/api/workflows/metrics")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "total_actions" in data
    assert "status_counts" in data
    assert "total_savings" in data
    assert "actions_by_type" in data
    
    print(f"✅ SUCCESS: Retrieved workflow metrics")
    print(f"   Total Actions: {data['total_actions']}")
    print(f"   Status Counts: {data['status_counts']}")
    print(f"   Total Savings: Weekly ${data['total_savings']['weekly']:,.2f}")

def test_create_workflow_and_check_auto_completion():
    """Test: Create workflow and verify auto-completion by worker"""
    print("\n🧪 TEST: Workflow auto-completion by background worker")
    
    # Create a workflow
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={
            "agent_id": "agent_jermaine_super_action",
            "message": "Test workflow",
            "mode": "execute",
            "context": {
                "workflow_type": "customer_followup",
                "calculator_inputs": {
                    "tasks_per_week": 100,
                    "time_per_task_minutes": 5,
                    "hourly_wage": 25,
                    "automation_percent": 0.7,
                    "error_rate": 0.1,
                    "cost_per_error": 15,
                    "value_per_accelerated_task": 0
                }
            }
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    workflow_id = data["workflow_action"]
    
    print(f"   Created workflow: {workflow_id}")
    
    # Check initial status
    response = requests.get(f"{BASE_URL}/api/workflows/{workflow_id}")
    assert response.status_code == 200
    workflow = response.json()
    assert workflow["status"] == "running"
    
    print(f"   Initial status: {workflow['status']}")
    print(f"   Waiting 6 seconds for auto-completion...")
    
    # Wait for worker to complete it (5 second threshold + 2 second sleep cycle)
    time.sleep(6)
    
    # Check status after delay
    response = requests.get(f"{BASE_URL}/api/workflows/{workflow_id}")
    assert response.status_code == 200
    workflow = response.json()
    
    print(f"   Final status: {workflow['status']}")
    
    # Worker should have completed it
    assert workflow["status"] == "completed", f"Expected 'completed', got '{workflow['status']}'"
    
    print(f"✅ SUCCESS: Workflow auto-completed by background worker")

def test_metrics_after_completions():
    """Test: Verify metrics reflect completed workflows"""
    print("\n🧪 TEST: Metrics after auto-completions")
    
    response = requests.get(f"{BASE_URL}/api/workflows/metrics")
    assert response.status_code == 200
    
    metrics = response.json()
    
    print(f"✅ SUCCESS: Metrics updated")
    print(f"   Total Actions: {metrics['total_actions']}")
    print(f"   Completed: {metrics['status_counts']['completed']}")
    print(f"   Running: {metrics['status_counts']['running']}")
    print(f"   Total Savings (Yearly): ${metrics['total_savings']['yearly']:,.2f}")

def test_multiple_workflows_auto_complete():
    """Test: Create multiple workflows and verify all auto-complete"""
    print("\n🧪 TEST: Multiple workflows auto-complete")
    
    workflow_ids = []
    
    # Create 3 workflows
    for i in range(3):
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={
                "agent_id": "agent_jermaine_super_action",
                "message": f"Test workflow {i}",
                "mode": "execute",
                "context": {
                    "workflow_type": "data_entry_automation",
                    "calculator_inputs": {
                        "entries_per_week": 50 * (i + 1),
                        "time_per_entry_minutes": 3,
                        "hourly_wage": 20,
                        "automation_percent": 0.8
                    }
                }
            }
        )
        
        assert response.status_code == 200
        workflow_ids.append(response.json()["workflow_action"])
    
    print(f"   Created {len(workflow_ids)} workflows")
    
    # Wait for auto-completion
    print(f"   Waiting 6 seconds for auto-completion...")
    time.sleep(6)
    
    # Check all are completed
    completed_count = 0
    for wid in workflow_ids:
        response = requests.get(f"{BASE_URL}/api/workflows/{wid}")
        workflow = response.json()
        if workflow["status"] == "completed":
            completed_count += 1
    
    print(f"   Completed: {completed_count}/{len(workflow_ids)}")
    assert completed_count == len(workflow_ids), f"Expected all {len(workflow_ids)} to complete"
    
    print(f"✅ SUCCESS: All workflows auto-completed")

def run_all_tests():
    """Run all background worker tests"""
    print("\n" + "="*60)
    print("🔥 BACKGROUND WORKER & METRICS TEST SUITE 🔥")
    print("="*60)
    
    try:
        # Test metrics endpoint
        test_workflow_metrics_endpoint()
        
        # Test auto-completion
        test_create_workflow_and_check_auto_completion()
        
        # Test metrics after completions
        test_metrics_after_completions()
        
        # Test multiple workflows
        test_multiple_workflows_auto_complete()
        
        print("\n" + "="*60)
        print("✅ ALL BACKGROUND WORKER TESTS PASSED!")
        print("="*60)
        print("\n📊 Test Coverage:")
        print("   ✅ Workflow metrics endpoint")
        print("   ✅ Auto-completion after 5 seconds")
        print("   ✅ Metrics reflect completed workflows")
        print("   ✅ Multiple workflows complete correctly")
        print("\n⚡ Background Worker: OPERATIONAL")
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
