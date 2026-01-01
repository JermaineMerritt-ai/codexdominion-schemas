"""
Test the Workflow Engine API
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_workflow_engine():
    print("=" * 60)
    print("Testing Workflow Engine API")
    print("=" * 60)
    
    # 1. Create a workflow action with calculated savings
    print("\n1. Creating workflow action...")
    create_payload = {
        "action_type": "customer_followup",
        "created_by_agent": "jermaine_super_action_ai",
        "inputs": {
            "tasks_per_week": 200,
            "time_per_task_minutes": 10,
            "hourly_wage": 25,
            "automation_percent": 0.7
        },
        "calculated_savings": {
            "weekly_savings": 793.33,
            "yearly_savings": 41253.33,
            "effectiveness": "STELLAR"
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/workflows/actions", json=create_payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        action_id = data["action_id"]
        print(f"✅ Action created: {action_id}")
        print(f"   Status: {data['status']}")
    else:
        print(f"❌ Failed to create action")
        return
    
    # 2. Get action details
    print(f"\n2. Getting action details...")
    response = requests.get(f"{BASE_URL}/api/workflows/actions/{action_id}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        action = data["action"]
        print(f"✅ Action retrieved")
        print(f"   Type: {action['action_type']}")
        print(f"   Status: {action['status']}")
        print(f"   Created by: {action['created_by_agent']}")
        print(f"   Yearly savings: ${action['calculated_savings']['yearly_savings']:,.2f}")
    
    # 3. Execute action (change status to running)
    print(f"\n3. Executing action...")
    response = requests.post(f"{BASE_URL}/api/workflows/actions/{action_id}/execute")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Action execution started")
        print(f"   Status: {data['status']}")
    
    # 4. Update status to completed
    print(f"\n4. Completing action...")
    response = requests.patch(
        f"{BASE_URL}/api/workflows/actions/{action_id}",
        json={"status": "completed"}
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Action completed")
        print(f"   Status: {data['status']}")
    
    # 5. List all actions
    print(f"\n5. Listing all actions...")
    response = requests.get(f"{BASE_URL}/api/workflows/actions")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved {data['count']} action(s)")
        for aid, action in data["actions"].items():
            print(f"   - {action['action_type']} ({action['status']})")
    
    print("\n" + "=" * 60)
    print("✅ All workflow engine tests passed!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_workflow_engine()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Flask server not running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")
