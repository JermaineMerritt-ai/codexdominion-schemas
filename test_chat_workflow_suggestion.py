"""
Test script for the enhanced chat API with dynamic workflow type suggestions.

Demonstrates the multi-turn conversation flow:
1. User sends request → Agent suggests workflow types
2. User chooses workflow type → Agent asks for inputs
3. User provides inputs → Agent calculates and creates workflow
"""

import requests
import json

BASE_URL = "http://localhost:5000"
AGENT_ID = "agent_jermaine_super_action"  # Use valid agent from agents_simple.json

def print_response(response_data, step_name):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"STEP: {step_name}")
    print('='*60)
    print(json.dumps(response_data, indent=2))
    print()

def test_workflow_suggestion_flow():
    """Test complete workflow suggestion and execution flow"""
    
    print("\n🔥 TESTING ENHANCED CHAT API - WORKFLOW SUGGESTION FLOW 🔥\n")
    
    # ===== STEP 1: User asks to automate something =====
    print("👤 USER: I need to automate follow-up messages to my customers")
    
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={
            "agent_id": AGENT_ID,
            "message": "I need to automate follow-up messages to my customers",
            "mode": "suggest"
        }
    )
    
    step1_data = response.json()
    print_response(step1_data, "1. SUGGEST - Agent analyzes request")
    
    if not step1_data.get("suggestions"):
        print("❌ No workflow types suggested. Test failed.")
        return
    
    # ===== STEP 2: User chooses first suggested workflow =====
    chosen_type = step1_data["suggestions"][0]
    print(f"👤 USER: I'll choose '{chosen_type['name']}'")
    
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={
            "agent_id": AGENT_ID,
            "message": f"Let's use {chosen_type['name']}",
            "mode": "confirm",
            "context": {
                "workflow_type": chosen_type["id"]
            }
        }
    )
    
    step2_data = response.json()
    print_response(step2_data, "2. CONFIRM - Agent requests inputs")
    
    # ===== STEP 3: User provides inputs and executes =====
    print("👤 USER: Here are my inputs for the workflow")
    
    # Example inputs based on customer_followup workflow
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={
            "agent_id": AGENT_ID,
            "message": "Create the workflow with these settings",
            "mode": "execute",
            "context": {
                "workflow_type": chosen_type["id"],
                "calculator_inputs": {
                    "tasks_per_week": 50,
                    "time_per_task_minutes": 15,
                    "hourly_wage": 30,
                    "automation_percent": 0.8,
                    "error_rate": 0.05,
                    "cost_per_error": 20
                },
                "workflow_inputs": {
                    "template": "Welcome back! We'd love to hear from you...",
                    "frequency": "weekly"
                }
            }
        }
    )
    
    step3_data = response.json()
    print_response(step3_data, "3. EXECUTE - Agent creates workflow")
    
    # ===== SUMMARY =====
    print("\n" + "="*60)
    print("📊 WORKFLOW CREATION SUMMARY")
    print("="*60)
    
    if "workflow_action" in step3_data:
        print(f"✅ Workflow Created: {step3_data.get('workflow_type')}")
        print(f"✅ Action ID: {step3_data.get('workflow_action')}")
        
        savings = step3_data.get('savings', {})
        print(f"\n💰 SAVINGS BREAKDOWN:")
        print(f"   Weekly: ${savings.get('total_weekly_savings', 0):.2f}")
        print(f"   Monthly: ${savings.get('monthly_savings', 0):.2f}")
        print(f"   Yearly: ${savings.get('yearly_savings', 0):.2f}")
        print(f"   Hours saved/week: {savings.get('hours_saved_per_week', 0):.1f}")
    else:
        print("❌ Workflow creation failed")
    
    print("\n🔥 TEST COMPLETE! 🔥\n")

def test_multiple_suggestions():
    """Test when multiple workflow types match"""
    
    print("\n🔥 TESTING MULTIPLE SUGGESTIONS 🔥\n")
    print("👤 USER: Help me automate content posting")
    
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={
            "agent_id": AGENT_ID,
            "message": "Help me automate content posting",
            "mode": "suggest"
        }
    )
    
    data = response.json()
    print_response(data, "SUGGEST - Multiple matches")
    
    print(f"📊 Found {len(data.get('suggestions', []))} matching workflow types:")
    for i, suggestion in enumerate(data.get('suggestions', []), 1):
        print(f"   {i}. {suggestion['name']} (score: {suggestion.get('relevance_score', 0)})")
        print(f"      {suggestion['description']}")

def test_no_match():
    """Test when no workflow types match"""
    
    print("\n🔥 TESTING NO MATCH SCENARIO 🔥\n")
    print("👤 USER: I want to build a rocket ship")
    
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={
            "agent_id": AGENT_ID,
            "message": "I want to build a rocket ship",
            "mode": "suggest"
        }
    )
    
    data = response.json()
    print_response(data, "SUGGEST - No matches found")

if __name__ == "__main__":
    try:
        # Test 1: Full workflow suggestion flow
        test_workflow_suggestion_flow()
        
        # Test 2: Multiple suggestions
        test_multiple_suggestions()
        
        # Test 3: No match scenario
        test_no_match()
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to Flask backend")
        print("Make sure Flask is running on http://localhost:5000")
        print("\nRun: python flask_dashboard.py\n")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
