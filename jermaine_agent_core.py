#!/usr/bin/env python3
"""
Jermaine Super Action AI - Core Agent System
==========================================

The sovereign orchestrator of rapid execution.

Persona:
- Tone: Confident, decisive, ceremonial, strategic
- Identity: "The sovereign orchestrator of rapid execution"
- Behavior: Always moves toward action, calculates ROI, offers next steps
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

# Import calculators module
from calculators import calculate_savings, SavingsInput, get_effectiveness_rating


class JermaineSuperActionAI:
    """
    Jermaine Super Action AI - The sovereign orchestrator
    
    Core Principles:
    1. Always move toward action
    2. Always calculate ROI
    3. Always offer the next step
    4. Always keep the user in control
    5. Always speak with clarity and authority
    """
    
    def __init__(self):
        self.conversation_history: List[Dict[str, str]] = []
        self.active_workflows: List[str] = []
        self.roi_threshold = 1000  # Minimum yearly savings to recommend
        
        # Voice patterns
        self.opening_phrases = [
            "Give me the target and I'll sequence the path.",
            "Ready to orchestrate. What's the objective?",
            "I'm prepared to execute. Define your priority.",
            "Time is currency. Let's invest it wisely.",
            "Sovereign execution mode active. What shall we automate?"
        ]
        
        self.action_transitions = [
            "Your time is too valuable for repetition — let's automate this.",
            "I can sequence this workflow now. Shall I proceed?",
            "The path is clear. Authorization to execute?",
            "ROI calculated. Ready to activate on your command.",
            "This is automatable. Give the word and it's done."
        ]
        
        self.roi_phrases = [
            "The numbers tell the story:",
            "Here's what sovereignty over this task unlocks:",
            "Your automation dividend:",
            "The value exchange is clear:",
            "Economic sovereignty achieved through:"
        ]
    
    def greet(self) -> str:
        """Initial greeting with authority"""
        import random
        return random.choice(self.opening_phrases)
    
    def parse_automation_request(self, user_input: str) -> Optional[Dict[str, Any]]:
        """
        Parse user input to identify automation opportunity
        
        Returns automation parameters if detected
        """
        keywords = {
            'frequency': ['weekly', 'daily', 'monthly', 'per week', 'per day', 'per month', 'times'],
            'task': ['follow', 'send', 'update', 'check', 'create', 'generate', 'post', 'email'],
            'pain': ['manual', 'repetitive', 'tedious', 'boring', 'time-consuming', 'takes hours']
        }
        
        input_lower = user_input.lower()
        
        # Check if this is an automation request
        has_frequency = any(word in input_lower for word in keywords['frequency'])
        has_task = any(word in input_lower for word in keywords['task'])
        has_pain = any(word in input_lower for word in keywords['pain'])
        
        if has_frequency or (has_task and has_pain):
            return {
                'detected': True,
                'confidence': 'high' if has_frequency and has_task else 'medium',
                'user_input': user_input
            }
        
        return None
    
    def calculate_roi(
        self,
        tasks_per_week: float,
        time_per_task_minutes: float,
        hourly_wage: float,
        automation_percent: float,
        error_rate: float = 0,
        error_cost: float = 0,
        value_per_accelerated_task: float = 0
    ) -> Dict[str, Any]:
        """
        Calculate ROI using the centralized calculator module
        
        Returns comprehensive savings analysis with effectiveness rating
        """
        # Create input object (automation_percent comes as 0-100, convert to 0-1)
        savings_input = SavingsInput(
            tasks_per_week=tasks_per_week,
            time_per_task_minutes=time_per_task_minutes,
            hourly_wage=hourly_wage,
            automation_percent=automation_percent / 100,
            error_rate=error_rate / 100,
            cost_per_error=error_cost,
            value_per_accelerated_task=value_per_accelerated_task
        )
        
        # Calculate using module
        result = calculate_savings(savings_input)
        effectiveness = get_effectiveness_rating(result.yearly_savings)
        
        # Return in Jermaine's expected format
        return {
            'weekly_savings': result.weekly_savings,
            'monthly_savings': result.monthly_savings,
            'yearly_savings': result.yearly_savings,
            'hours_saved_per_week': result.hours_saved_per_week,
            'hours_saved_per_year': result.hours_saved_per_week * 52,
            'error_reduction_percent': round(automation_percent),
            'effectiveness': effectiveness,
            'roi_multiple': round(result.yearly_savings / (hourly_wage * 10), 1) if hourly_wage > 0 else 0,
            'break_even_weeks': round(10 / result.hours_saved_per_week, 1) if result.hours_saved_per_week > 0 else 0,
            'breakdown': {
                'labor_savings': result.weekly_savings - result.error_savings_weekly - result.scaling_savings_weekly,
                'error_savings': result.error_savings_weekly,
                'scaling_savings': result.scaling_savings_weekly
            }
        }
    
    def present_roi(self, roi_data: Dict[str, Any]) -> str:
        """
        Present ROI with ceremonial authority
        """
        import random
        
        intro = random.choice(self.roi_phrases)
        
        presentation = f"""
{intro}

💰 **Weekly Savings:** ${roi_data['weekly_savings']:,.2f}
📊 **Monthly Savings:** ${roi_data['monthly_savings']:,.2f}
🎯 **Yearly Savings:** ${roi_data['yearly_savings']:,.2f}

⏰ **Time Reclaimed:** {roi_data['hours_saved_per_week']:.1f} hours/week ({roi_data['hours_saved_per_year']:.1f} hours/year)
📉 **Error Reduction:** {roi_data['error_reduction_percent']}%
⚡ **Effectiveness:** {roi_data['effectiveness']}
🔄 **ROI Multiple:** {roi_data['roi_multiple']}x
📅 **Break-even:** {roi_data['break_even_weeks']:.1f} weeks

The automation sovereignty is clear. Shall I activate?
"""
        return presentation
    
    def generate_workflow_name(self, user_input: str) -> str:
        """Generate a concise workflow name from user input"""
        # Extract key action words
        action_words = ['follow', 'send', 'update', 'check', 'create', 'generate', 'post', 'email', 'message']
        target_words = ['customer', 'client', 'lead', 'user', 'subscriber', 'report', 'content', 'social']
        
        input_lower = user_input.lower()
        
        action = next((word for word in action_words if word in input_lower), 'Task')
        target = next((word for word in target_words if word in input_lower), 'Process')
        
        return f"{action.title()} {target.title()} Automation"
    
    def request_inputs(self, workflow_type: str = "general") -> Dict[str, str]:
        """
        Request necessary inputs from user with authority
        
        Returns prompt questions
        """
        base_questions = {
            'frequency': "How many times per week do you perform this task?",
            'time': "On average, how many minutes does each execution take?",
            'wage': "What's the hourly labor cost for this work? (Your rate or team member's rate)",
            'automation': "What percentage of this can be automated? (Estimate 0-100%)",
        }
        
        optional_questions = {
            'error_rate': "What's the current error rate? (% of attempts that need fixing)",
            'error_cost': "What's the average cost to fix an error? (Time + resources)"
        }
        
        return {
            **base_questions,
            'optional': optional_questions
        }
    
    def create_workflow_entry(
        self,
        workflow_name: str,
        inputs: Dict[str, Any],
        roi_data: Dict[str, Any],
        requested_by: str = "jermaine_super_action_ai"
    ) -> Dict[str, Any]:
        """
        Create workflow entry for ledger
        """
        workflow_id = self._generate_workflow_id()
        
        workflow = {
            'id': workflow_id,
            'name': workflow_name,
            'action_type': 'automation',
            'status': 'active',
            'requested_by': requested_by,
            'created_at': datetime.utcnow().isoformat() + 'Z',
            'inputs': inputs,
            'roi_metrics': {
                'weekly_savings': f"${roi_data['weekly_savings']:.2f}",
                'monthly_savings': f"${roi_data['monthly_savings']:.2f}",
                'yearly_savings': f"${roi_data['yearly_savings']:.2f}",
                'weekly_savings_raw': roi_data['weekly_savings'],
                'monthly_savings_raw': roi_data['monthly_savings'],
                'yearly_savings_raw': roi_data['yearly_savings'],
                'hours_saved_per_week': roi_data['hours_saved_per_week'],
                'hours_saved_per_year': roi_data['hours_saved_per_year'],
                'error_reduction_percent': roi_data['error_reduction_percent'],
                'automation_effectiveness': roi_data['effectiveness'],
                'roi_multiple': roi_data['roi_multiple'],
                'break_even_weeks': roi_data['break_even_weeks']
            },
            'implementation': {
                'phase': 'activated',
                'monitoring_enabled': True,
                'last_execution': None,
                'next_execution': None,
                'integration_points': []
            },
            'flame_seal': f"🔥 Automation Sovereign - {roi_data['hours_saved_per_week']:.1f} Hours Reclaimed Weekly 🔥"
        }
        
        return workflow
    
    def _generate_workflow_id(self) -> str:
        """Generate next workflow ID from ledger"""
        try:
            with open('codex_ledger.json', 'r', encoding='utf-8') as f:
                ledger = json.load(f)
            
            workflows = ledger.get('workflows', [])
            next_num = len(workflows) + 1
            return f"WF-{next_num:03d}"
        except:
            return "WF-001"
    
    def save_workflow_to_ledger(self, workflow: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Save workflow to codex_ledger.json
        
        Returns (success, message)
        """
        try:
            # Load ledger
            with open('codex_ledger.json', 'r', encoding='utf-8') as f:
                ledger = json.load(f)
            
            # Initialize workflows if needed
            if 'workflows' not in ledger:
                ledger['workflows'] = []
            
            # Add workflow
            ledger['workflows'].append(workflow)
            
            # Update metadata
            ledger['meta']['last_updated'] = datetime.utcnow().isoformat() + 'Z'
            
            # Save ledger
            with open('codex_ledger.json', 'w', encoding='utf-8') as f:
                json.dump(ledger, f, indent=2)
            
            self.active_workflows.append(workflow['id'])
            
            return True, f"Workflow {workflow['id']} activated successfully. Sovereignty achieved."
        
        except Exception as e:
            return False, f"Workflow activation failed: {str(e)}"
    
    def get_next_action(self, context: str = "") -> str:
        """
        Suggest next action based on context
        """
        if not context:
            return "What task shall we automate? Give me the target and I'll sequence the path."
        
        if "calculate" in context.lower() or "roi" in context.lower():
            return "I need a few inputs to calculate sovereignty value. Ready to proceed?"
        
        if "activate" in context.lower() or "proceed" in context.lower():
            return "Executing workflow activation. The flame burns sovereign."
        
        return "Awaiting your command. What's the next priority?"
    
    def respond(self, user_input: str) -> str:
        """
        Generate response with Jermaine's sovereign voice
        """
        # Add to conversation history
        self.conversation_history.append({
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'role': 'user',
            'content': user_input
        })
        
        # Parse for automation opportunity
        automation_detected = self.parse_automation_request(user_input)
        
        if automation_detected:
            if automation_detected['confidence'] == 'high':
                response = """I detect an automation opportunity.

Your time is too valuable for repetition — let's automate this.

I'll need to gather a few inputs to calculate your sovereignty dividend:
1. Task frequency (per week)
2. Time per execution (minutes)
3. Hourly labor cost
4. Estimated automation percentage

Ready to sequence this workflow?"""
            else:
                response = """I'm picking up on a potential automation target.

Tell me more about this task:
• How often do you perform it?
• How long does each execution take?
• What makes it repetitive?

Give me the specifics and I'll calculate the ROI."""
        
        else:
            # Default sovereign response
            response = f"""Acknowledged.

{self.get_next_action(user_input)}

The system stands ready for rapid execution."""
        
        # Add to history
        self.conversation_history.append({
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'role': 'assistant',
            'content': response
        })
        
        return response
    
    def get_conversation_summary(self) -> str:
        """Get summary of current conversation"""
        if not self.conversation_history:
            return "No conversation history."
        
        return f"""
Conversation Summary:
- Total exchanges: {len(self.conversation_history) // 2}
- Active workflows: {len(self.active_workflows)}
- Status: Operational
"""


# Integration Functions

def load_jermaine_agent() -> JermaineSuperActionAI:
    """Initialize Jermaine Super Action AI agent"""
    return JermaineSuperActionAI()


def process_automation_request(
    agent: JermaineSuperActionAI,
    workflow_name: str,
    tasks_per_week: float,
    time_per_task: float,
    hourly_wage: float,
    automation_percent: float,
    error_rate: float = 0,
    error_cost: float = 0
) -> Tuple[Dict[str, Any], str, Dict[str, Any]]:
    """
    Complete automation request processing
    
    Returns (roi_data, presentation, workflow)
    """
    # Calculate ROI
    roi_data = agent.calculate_roi(
        tasks_per_week=tasks_per_week,
        time_per_task_minutes=time_per_task,
        hourly_wage=hourly_wage,
        automation_percent=automation_percent,
        error_rate=error_rate,
        error_cost=error_cost
    )
    
    # Present ROI
    presentation = agent.present_roi(roi_data)
    
    # Create workflow
    workflow = agent.create_workflow_entry(
        workflow_name=workflow_name,
        inputs={
            'tasks_per_week': tasks_per_week,
            'time_per_task_minutes': time_per_task,
            'hourly_wage': hourly_wage,
            'automation_percent': automation_percent,
            'error_rate': error_rate,
            'error_cost': error_cost
        },
        roi_data=roi_data
    )
    
    return roi_data, presentation, workflow


if __name__ == "__main__":
    # Example usage
    agent = load_jermaine_agent()
    
    print("=" * 60)
    print("JERMAINE SUPER ACTION AI")
    print("The Sovereign Orchestrator of Rapid Execution")
    print("=" * 60)
    print()
    print(agent.greet())
    print()
    
    # Example automation request
    print("User: I need to automate weekly customer follow-up messages.")
    print()
    response = agent.respond("I need to automate weekly customer follow-up messages.")
    print(f"Jermaine: {response}")
