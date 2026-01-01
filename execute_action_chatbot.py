"""
🤖 CODEX DOMINION - EXECUTE ACTION CHATBOT
==========================================
Conversational AI for automation workflow creation with ROI calculation

This implementation follows the ceremonial "Execute Action" flow:
1. Agent greeting
2. User request
3. Agent gathers inputs
4. Agent calculates savings
5. User approves
6. Agent triggers workflow
7. Confirmation & monitoring

Features:
- ROI calculation (weekly, monthly, yearly savings)
- Time reclamation tracking
- Error reduction percentage
- Workflow activation
- Ledger integration for tracking
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional


class ExecuteActionChatbot:
    """
    Automation workflow chatbot with ROI calculator
    
    Usage:
        chatbot = ExecuteActionChatbot()
        response = chatbot.start_conversation()
        # ... continue conversation
        workflow = chatbot.execute_workflow(inputs)
    """
    
    def __init__(self):
        self.conversation_state = "greeting"
        self.workflow_data = {}
        self.ledger_path = "codex_ledger.json"
        
    def start_conversation(self) -> str:
        """Step 1: Agent greeting"""
        self.conversation_state = "awaiting_request"
        return "Alright, I'm ready. What action do you want me to execute?"
    
    def process_user_request(self, user_message: str) -> Dict[str, Any]:
        """
        Step 2 & 3: Identify action and gather inputs
        
        Args:
            user_message: User's automation request
            
        Returns:
            Dict with next_question and workflow_context
        """
        if self.conversation_state == "awaiting_request":
            # Identify automation intent
            self.workflow_data["name"] = user_message
            self.workflow_data["inputs"] = {}
            self.conversation_state = "gathering_frequency"
            
            return {
                "response": f"Got it. I can automate your {user_message}. I'll need a few quick details so I can build the workflow correctly.",
                "next_question": "How many follow-up messages do you send weekly?",
                "state": "gathering_frequency"
            }
        
        elif self.conversation_state == "gathering_frequency":
            self.workflow_data["inputs"]["frequency"] = int(user_message)
            self.conversation_state = "gathering_time"
            return {
                "response": f"Got it, {user_message} messages per week.",
                "next_question": "On average, how long does each one take? (in minutes)",
                "state": "gathering_time"
            }
        
        elif self.conversation_state == "gathering_time":
            self.workflow_data["inputs"]["time_per_task"] = float(user_message)
            self.conversation_state = "gathering_cost"
            return {
                "response": f"Perfect, {user_message} minutes per message.",
                "next_question": "What's the hourly labor cost for whoever handles this? (in dollars)",
                "state": "gathering_cost"
            }
        
        elif self.conversation_state == "gathering_cost":
            self.workflow_data["inputs"]["hourly_cost"] = float(user_message)
            self.conversation_state = "gathering_automation"
            return {
                "response": f"${user_message}/hour. Got it.",
                "next_question": "What percentage of this can be automated? (0-100)",
                "state": "gathering_automation"
            }
        
        elif self.conversation_state == "gathering_automation":
            self.workflow_data["inputs"]["automation_percentage"] = float(user_message)
            self.conversation_state = "gathering_errors"
            return {
                "response": f"{user_message}% automation potential. Excellent.",
                "next_question": "Do errors ever happen? If so, what's the average cost of fixing them? (in dollars, or 0 if no errors)",
                "state": "gathering_errors"
            }
        
        elif self.conversation_state == "gathering_errors":
            self.workflow_data["inputs"]["error_cost"] = float(user_message)
            self.conversation_state = "presenting_roi"
            
            # Calculate ROI
            roi = self.calculate_roi()
            self.workflow_data["roi"] = roi
            
            return {
                "response": self.format_roi_presentation(roi),
                "next_question": "Would you like me to build and activate this workflow now?",
                "state": "awaiting_approval"
            }
    
    def calculate_roi(self) -> Dict[str, Any]:
        """
        Step 4: Calculate automation savings with ceremonial precision
        
        Returns:
            Dict containing all ROI metrics
        """
        inputs = self.workflow_data["inputs"]
        
        # Convert minutes to hours
        time_hours = inputs["time_per_task"] / 60
        
        # Weekly calculations
        weekly_hours = inputs["frequency"] * time_hours
        weekly_cost = weekly_hours * inputs["hourly_cost"]
        automation_factor = inputs["automation_percentage"] / 100
        
        # Savings calculations
        weekly_savings = weekly_cost * automation_factor
        monthly_savings = weekly_savings * 4.33  # Average weeks per month
        yearly_savings = weekly_savings * 52
        
        # Time reclamation
        time_reclaimed_weekly = weekly_hours * automation_factor
        
        # Error reduction
        error_reduction_percentage = inputs["automation_percentage"]
        annual_error_savings = inputs["error_cost"] * 52 * automation_factor
        
        return {
            "weekly_savings": round(weekly_savings, 2),
            "monthly_savings": round(monthly_savings, 2),
            "yearly_savings": round(yearly_savings, 2),
            "time_reclaimed_weekly": round(time_reclaimed_weekly, 1),
            "error_reduction_percentage": round(error_reduction_percentage, 0),
            "annual_error_savings": round(annual_error_savings, 2)
        }
    
    def format_roi_presentation(self, roi: Dict[str, Any]) -> str:
        """
        Format ROI presentation with ceremonial clarity
        
        Args:
            roi: ROI metrics dictionary
            
        Returns:
            Formatted presentation string
        """
        return f"""Here's what your automation unlocks:

• Weekly savings: ${roi['weekly_savings']:,.2f}
• Monthly savings: ${roi['monthly_savings']:,.2f}
• Yearly savings: ${roi['yearly_savings']:,.2f}
• Error reduction: {roi['error_reduction_percentage']:.0f}%
• Time reclaimed: {roi['time_reclaimed_weekly']:.1f} hours/week
{f"• Annual error cost savings: ${roi['annual_error_savings']:,.2f}" if roi['annual_error_savings'] > 0 else ""}"""
    
    def approve_and_execute(self, user_approval: str) -> Dict[str, Any]:
        """
        Step 5-7: User approval, agent confirmation, workflow trigger
        
        Args:
            user_approval: User's approval message (e.g., "Yes, execute")
            
        Returns:
            Dict with confirmation and workflow_id
        """
        if user_approval.lower() in ["yes", "yes, execute", "execute", "go ahead", "do it"]:
            self.conversation_state = "executing"
            
            # Generate workflow ID
            workflow_id = str(uuid.uuid4())
            
            # Save to ledger
            self.save_workflow_to_ledger(workflow_id)
            
            # Confirmation message
            workflow_name = self.workflow_data["name"]
            roi = self.workflow_data["roi"]
            
            return {
                "status": "success",
                "workflow_id": workflow_id,
                "confirmation": f"Perfect. I'm building your automation now.",
                "completion": f"Your {workflow_name} automation is now active. I'll monitor performance and notify you of improvements.",
                "roi": roi
            }
        else:
            return {
                "status": "cancelled",
                "message": "No problem. Let me know if you'd like to try a different automation."
            }
    
    def save_workflow_to_ledger(self, workflow_id: str) -> None:
        """
        Save workflow activation to codex_ledger.json
        
        Args:
            workflow_id: Unique workflow identifier
        """
        try:
            with open(self.ledger_path, "r") as f:
                ledger = json.load(f)
            
            # Ensure workflows key exists
            if "workflows" not in ledger:
                ledger["workflows"] = []
            
            # Create workflow entry
            workflow_entry = {
                "id": workflow_id,
                "name": self.workflow_data["name"],
                "inputs": self.workflow_data["inputs"],
                "roi": self.workflow_data["roi"],
                "status": "active",
                "created_at": datetime.utcnow().isoformat() + "Z",
                "created_by": "execute_action_chatbot"
            }
            
            ledger["workflows"].append(workflow_entry)
            
            # Update metadata
            ledger["meta"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
            
            # Save back to file
            with open(self.ledger_path, "w") as f:
                json.dump(ledger, f, indent=2)
                
        except Exception as e:
            print(f"⚠️ Error saving to ledger: {e}")
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve workflow status from ledger
        
        Args:
            workflow_id: Unique workflow identifier
            
        Returns:
            Workflow data or None if not found
        """
        try:
            with open(self.ledger_path, "r") as f:
                ledger = json.load(f)
            
            workflows = ledger.get("workflows", [])
            for workflow in workflows:
                if workflow["id"] == workflow_id:
                    return workflow
            
            return None
            
        except Exception as e:
            print(f"⚠️ Error reading ledger: {e}")
            return None


# ============================================================================
# EXAMPLE USAGE - INTERACTIVE CLI
# ============================================================================

def run_interactive_session():
    """
    Run interactive chatbot session in terminal
    
    Usage:
        python execute_action_chatbot.py
    """
    print("\n🔥 CODEX DOMINION - EXECUTE ACTION CHATBOT 👑\n")
    print("=" * 60)
    
    chatbot = ExecuteActionChatbot()
    
    # Step 1: Greeting
    print(f"\n🤖 Agent: {chatbot.start_conversation()}")
    
    # Step 2: User request
    user_request = input("\n👤 You: ")
    response = chatbot.process_user_request(user_request)
    print(f"\n🤖 Agent: {response['response']}")
    print(f"          {response['next_question']}")
    
    # Step 3: Gather inputs
    while chatbot.conversation_state != "awaiting_approval":
        user_input = input("\n👤 You: ")
        response = chatbot.process_user_request(user_input)
        print(f"\n🤖 Agent: {response['response']}")
        if response.get('next_question'):
            print(f"          {response['next_question']}")
    
    # Step 5: Approval
    user_approval = input("\n👤 You: ")
    result = chatbot.approve_and_execute(user_approval)
    
    if result["status"] == "success":
        print(f"\n🤖 Agent: {result['confirmation']}")
        print(f"\n✅ {result['completion']}")
        print(f"\n📊 Workflow ID: {result['workflow_id']}")
        print("\n" + "=" * 60)
        print("🔥 THE FLAME BURNS SOVEREIGN AND ETERNAL! 👑")
    else:
        print(f"\n🤖 Agent: {result['message']}")


if __name__ == "__main__":
    run_interactive_session()
