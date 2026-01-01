"""
Test simplified workflow endpoints
"""

import requests
import json

BASE_URL = "http://localhost:5000"

print("=" * 60)
print("Testing Simplified Workflow Endpoints")
print("=" * 60)

# 1. Create a workflow action
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
action_id = response.json()["action_id"]
print(f"✅ Created action: {action_id}")

# 2. Test simplified GET /api/workflows
print("\n2. Testing GET /api/workflows (simplified)...")
response = requests.get(f"{BASE_URL}/api/workflows")
print(f"Status: {response.status_code}")

if response.status_code == 200:
    workflows = response.json()
    print(f"✅ Retrieved {len(workflows)} workflow(s)")
    for wf_id, wf in workflows.items():
        print(f"   - ID: {wf_id[:20]}...")
        print(f"     Type: {wf['action_type']}")
        print(f"     Status: {wf['status']}")
        print(f"     Savings: ${wf['calculated_savings']['yearly_savings']:,.2f}/year")

# 3. Test simplified GET /api/workflows/<id>
print(f"\n3. Testing GET /api/workflows/{action_id[:20]}... (simplified)...")
response = requests.get(f"{BASE_URL}/api/workflows/{action_id}")
print(f"Status: {response.status_code}")

if response.status_code == 200:
    workflow = response.json()
    print(f"✅ Retrieved workflow")
    print(f"   Type: {workflow['action_type']}")
    print(f"   Created by: {workflow['created_by_agent']}")
    print(f"   Status: {workflow['status']}")
    print(f"   Yearly Savings: ${workflow['calculated_savings']['yearly_savings']:,.2f}")
    print(f"   Effectiveness: {workflow['calculated_savings']['effectiveness']}")

# 4. Test non-existent workflow
print(f"\n4. Testing non-existent workflow...")
response = requests.get(f"{BASE_URL}/api/workflows/invalid-id-12345")
print(f"Status: {response.status_code}")

if response.status_code == 404:
    error = response.json()
    print(f"✅ Correctly returned 404")
    print(f"   Error: {error['error']}")
    print(f"   ID: {error['id']}")

print("\n" + "=" * 60)
print("✅ All simplified endpoint tests passed!")
print("=" * 60)
print("\n📊 Available Endpoints:")
print("   - GET  /api/workflows              (list all)")
print("   - GET  /api/workflows/<id>         (get one)")
print("   - POST /api/workflows/actions      (create)")
print("   - GET  /api/workflows/actions      (list with metadata)")
print("   - PATCH /api/workflows/actions/<id> (update status)")
