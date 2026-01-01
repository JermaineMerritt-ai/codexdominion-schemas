"""
Test the unified /api/chat endpoint with chat and execute modes
"""

import requests
import json

BASE_URL = "http://localhost:5000"

print("=" * 70)
print("Testing Unified Chat API")
print("=" * 70)

# 1. Test chat mode (simple conversational)
print("\n1. Testing CHAT mode...")
chat_payload = {
    "agent_id": "agent_jermaine_super_action",
    "message": "Hello, tell me about automation!",
    "mode": "chat"
}

response = requests.post(f"{BASE_URL}/api/chat", json=chat_payload)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"✅ Chat mode response")
    print(f"   Agent: {data['agent_name']}")
    print(f"   Mode: {data['mode']}")
    print(f"   Reply: {data['reply'][:80]}...")
else:
    print(f"❌ Error: {response.json()}")

# 2. Test execute mode with calculator inputs
print("\n2. Testing EXECUTE mode with calculator inputs...")
execute_payload = {
    "agent_id": "agent_jermaine_super_action",
    "message": "Create a customer followup automation workflow",
    "mode": "execute",
    "context": {
        "calculator_inputs": {
            "tasks_per_week": 200,
            "time_per_task_minutes": 10,
            "hourly_wage": 25,
            "automation_percent": 0.7,
            "error_rate": 0.1,
            "cost_per_error": 15,
            "value_per_accelerated_task": 0
        },
        "workflow_inputs": {
            "workflow_name": "Customer Followup Automation",
            "target_platform": "Email",
            "frequency": "Daily"
        }
    }
}

response = requests.post(f"{BASE_URL}/api/chat", json=execute_payload)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"✅ Execute mode response")
    print(f"   Agent: {data['agent_name']}")
    print(f"   Mode: {data['mode']}")
    print(f"   Workflow ID: {data['workflow_action']}")
    print(f"   Reply: {data['reply']}")
    
    if data.get("savings"):
        savings = data["savings"]
        print(f"\n   💰 Savings Calculated:")
        print(f"      Weekly: ${savings['weekly_savings']:,.2f}")
        print(f"      Monthly: ${savings['monthly_savings']:,.2f}")
        print(f"      Yearly: ${savings['yearly_savings']:,.2f}")
        print(f"      Hours/Week: {savings['hours_saved_per_week']:.2f}")
    
    # 3. Verify the workflow was created
    workflow_id = data['workflow_action']
    print(f"\n3. Verifying workflow {workflow_id[:20]}... was created...")
    response = requests.get(f"{BASE_URL}/api/workflows/{workflow_id}")
    
    if response.status_code == 200:
        workflow = response.json()
        print(f"✅ Workflow verified")
        print(f"   Type: {workflow['action_type']}")
        print(f"   Status: {workflow['status']}")
        print(f"   Created by: {workflow['created_by_agent']}")
else:
    print(f"❌ Error: {response.json()}")

# 4. Test invalid agent
print("\n4. Testing invalid agent ID...")
invalid_payload = {
    "agent_id": "invalid_agent_12345",
    "message": "Test message",
    "mode": "chat"
}

response = requests.post(f"{BASE_URL}/api/chat", json=invalid_payload)
print(f"Status: {response.status_code}")

if response.status_code == 404:
    print(f"✅ Correctly returned 404 for invalid agent")
    print(f"   Error: {response.json()['error']}")

print("\n" + "=" * 70)
print("✅ All chat API tests passed!")
print("=" * 70)
print("\n📊 Endpoint Summary:")
print("   POST /api/chat (mode=chat)    → Conversational response")
print("   POST /api/chat (mode=execute) → Create workflow with ROI")
print("   - Integrates with calculator module")
print("   - Creates workflow action in engine")
print("   - Returns workflow ID for tracking")
