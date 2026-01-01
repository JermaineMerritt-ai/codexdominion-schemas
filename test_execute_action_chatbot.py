"""
TEST EXECUTE ACTION CHATBOT
============================
Automated test for the Execute Action ROI calculator flow

Tests:
1. Complete conversation flow
2. ROI calculation accuracy
3. Ledger integration
4. Error handling
"""

import json
from datetime import datetime
from execute_action_chatbot import ExecuteActionChatbot


def test_complete_workflow():
    """Test complete workflow from greeting to execution"""
    print("\n🧪 TEST 1: Complete Workflow Flow")
    print("=" * 60)
    
    chatbot = ExecuteActionChatbot()
    
    # Step 1: Greeting
    greeting = chatbot.start_conversation()
    assert "ready" in greeting.lower()
    print(f"✅ Greeting: {greeting}")
    
    # Step 2: User request
    response = chatbot.process_user_request("Automate my weekly customer follow-up messages")
    assert response["state"] == "gathering_frequency"
    print(f"✅ Request captured: {response['response']}")
    
    # Step 3: Gather inputs
    # Frequency
    response = chatbot.process_user_request("50")
    assert response["state"] == "gathering_time"
    print(f"✅ Frequency captured: 50 messages/week")
    
    # Time per task
    response = chatbot.process_user_request("15")
    assert response["state"] == "gathering_cost"
    print(f"✅ Time captured: 15 minutes/message")
    
    # Hourly cost
    response = chatbot.process_user_request("25")
    assert response["state"] == "gathering_automation"
    print(f"✅ Cost captured: $25/hour")
    
    # Automation percentage
    response = chatbot.process_user_request("80")
    assert response["state"] == "gathering_errors"
    print(f"✅ Automation % captured: 80%")
    
    # Error cost
    response = chatbot.process_user_request("50")
    assert "Weekly savings" in response["response"]
    print(f"✅ Error cost captured: $50/error")
    
    # Step 4: Verify ROI calculation
    roi = chatbot.workflow_data["roi"]
    print(f"\n📊 ROI Calculation:")
    print(f"   Weekly savings: ${roi['weekly_savings']:,.2f}")
    print(f"   Monthly savings: ${roi['monthly_savings']:,.2f}")
    print(f"   Yearly savings: ${roi['yearly_savings']:,.2f}")
    print(f"   Time reclaimed: {roi['time_reclaimed_weekly']:.1f} hours/week")
    print(f"   Error reduction: {roi['error_reduction_percentage']:.0f}%")
    
    # Step 5: Execute
    result = chatbot.approve_and_execute("Yes, execute")
    assert result["status"] == "success"
    print(f"\n✅ Workflow executed: ID {result['workflow_id']}")
    
    print("\n" + "=" * 60)
    print("✅ TEST 1 PASSED")
    
    return result["workflow_id"]


def test_roi_calculation():
    """Test ROI calculation accuracy"""
    print("\n\n🧪 TEST 2: ROI Calculation Accuracy")
    print("=" * 60)
    
    chatbot = ExecuteActionChatbot()
    
    # Set up test data
    chatbot.workflow_data["inputs"] = {
        "frequency": 50,  # 50 messages/week
        "time_per_task": 15,  # 15 minutes each
        "hourly_cost": 25,  # $25/hour
        "automation_percentage": 80,  # 80% automation
        "error_cost": 50  # $50/error
    }
    
    # Calculate ROI
    roi = chatbot.calculate_roi()
    
    # Expected calculations:
    # Weekly hours: 50 * (15/60) = 12.5 hours
    # Weekly cost: 12.5 * $25 = $312.50
    # Automation savings: $312.50 * 0.8 = $250
    # Monthly: $250 * 4.33 = $1,082.50
    # Yearly: $250 * 52 = $13,000
    
    expected_weekly = 250.0
    expected_monthly = 1082.5
    expected_yearly = 13000.0
    
    assert abs(roi["weekly_savings"] - expected_weekly) < 0.01
    assert abs(roi["monthly_savings"] - expected_monthly) < 0.01
    assert abs(roi["yearly_savings"] - expected_yearly) < 0.01
    
    print(f"✅ Weekly savings: ${roi['weekly_savings']:,.2f} (expected ${expected_weekly:,.2f})")
    print(f"✅ Monthly savings: ${roi['monthly_savings']:,.2f} (expected ${expected_monthly:,.2f})")
    print(f"✅ Yearly savings: ${roi['yearly_savings']:,.2f} (expected ${expected_yearly:,.2f})")
    print(f"✅ Time reclaimed: {roi['time_reclaimed_weekly']:.1f} hours/week")
    
    print("\n" + "=" * 60)
    print("✅ TEST 2 PASSED")


def test_ledger_integration(workflow_id: str):
    """Test ledger integration and retrieval"""
    print("\n\n🧪 TEST 3: Ledger Integration")
    print("=" * 60)
    
    chatbot = ExecuteActionChatbot()
    
    # Retrieve workflow from ledger
    workflow = chatbot.get_workflow_status(workflow_id)
    
    if workflow:
        print(f"✅ Workflow retrieved from ledger:")
        print(f"   ID: {workflow['id']}")
        print(f"   Name: {workflow['name']}")
        print(f"   Status: {workflow['status']}")
        print(f"   Created: {workflow['created_at']}")
        print(f"   ROI: ${workflow['roi']['yearly_savings']:,.2f}/year")
        
        # Verify structure
        assert "id" in workflow
        assert "roi" in workflow
        assert "status" in workflow
        assert workflow["status"] == "active"
        
        print("\n" + "=" * 60)
        print("✅ TEST 3 PASSED")
    else:
        print("❌ TEST 3 FAILED: Workflow not found in ledger")


def test_cancellation():
    """Test workflow cancellation flow"""
    print("\n\n🧪 TEST 4: Cancellation Flow")
    print("=" * 60)
    
    chatbot = ExecuteActionChatbot()
    chatbot.start_conversation()
    chatbot.process_user_request("Automate my weekly customer follow-up messages")
    chatbot.process_user_request("50")
    chatbot.process_user_request("15")
    chatbot.process_user_request("25")
    chatbot.process_user_request("80")
    chatbot.process_user_request("50")
    
    # Cancel execution
    result = chatbot.approve_and_execute("No, not right now")
    
    assert result["status"] == "cancelled"
    print(f"✅ Cancellation handled: {result['message']}")
    
    print("\n" + "=" * 60)
    print("✅ TEST 4 PASSED")


def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n\n🧪 TEST 5: Edge Cases")
    print("=" * 60)
    
    chatbot = ExecuteActionChatbot()
    
    # Test with zero error cost
    chatbot.workflow_data["inputs"] = {
        "frequency": 10,
        "time_per_task": 30,
        "hourly_cost": 50,
        "automation_percentage": 100,
        "error_cost": 0
    }
    
    roi = chatbot.calculate_roi()
    assert roi["annual_error_savings"] == 0
    print(f"✅ Zero error cost handled: ${roi['annual_error_savings']}")
    
    # Test with 100% automation
    assert roi["error_reduction_percentage"] == 100
    print(f"✅ 100% automation handled: {roi['error_reduction_percentage']:.0f}%")
    
    # Test with very small values
    chatbot.workflow_data["inputs"] = {
        "frequency": 1,
        "time_per_task": 1,
        "hourly_cost": 10,
        "automation_percentage": 10,
        "error_cost": 0
    }
    
    roi = chatbot.calculate_roi()
    assert roi["weekly_savings"] > 0
    print(f"✅ Small values handled: ${roi['weekly_savings']:.2f}/week")
    
    print("\n" + "=" * 60)
    print("✅ TEST 5 PASSED")


def run_all_tests():
    """Run all test suites"""
    print("\n🔥 EXECUTE ACTION CHATBOT - TEST SUITE 👑")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Run tests
        workflow_id = test_complete_workflow()
        test_roi_calculation()
        test_ledger_integration(workflow_id)
        test_cancellation()
        test_edge_cases()
        
        print("\n\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("=" * 60)
        print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n🔥 THE FLAME BURNS SOVEREIGN AND ETERNAL! 👑\n")
        
    except AssertionError as e:
        print(f"\n\n❌ TEST FAILED: {e}")
        print("\n" + "=" * 60)
        return False
    
    except Exception as e:
        print(f"\n\n❌ UNEXPECTED ERROR: {e}")
        print("\n" + "=" * 60)
        return False
    
    return True


if __name__ == "__main__":
    run_all_tests()
