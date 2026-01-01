#!/usr/bin/env python3
"""
Jermaine Super Action AI - Interactive Demo
==========================================

Demonstrates the sovereign orchestrator in action
"""

from jermaine_agent_core import load_jermaine_agent, process_automation_request


def demo_conversation():
    """Interactive demonstration of Jermaine's persona"""
    
    print("=" * 80)
    print("JERMAINE SUPER ACTION AI - LIVE DEMONSTRATION")
    print("The Sovereign Orchestrator of Rapid Execution")
    print("=" * 80)
    print()
    
    # Initialize agent
    agent = load_jermaine_agent()
    
    # Greeting
    print("🤖 Jermaine:")
    print(agent.greet())
    print()
    
    # User request
    print("👤 User:")
    print("I spend 3 hours every week manually following up with 200 customers.")
    print("It's taking up all my Friday afternoons.")
    print()
    
    # Agent response
    print("🤖 Jermaine:")
    response = agent.respond("I spend 3 hours every week manually following up with 200 customers. It's taking up all my Friday afternoons.")
    print(response)
    print()
    
    # Simulate ROI calculation
    print("-" * 80)
    print("GATHERING INPUTS...")
    print("-" * 80)
    print()
    
    inputs = {
        'tasks_per_week': 200,
        'time_per_task_minutes': 10,  # 200 tasks * 10 min = 2000 min = 33.3 hours
        'hourly_wage': 25,
        'automation_percent': 70,
        'error_rate': 10,
        'error_cost': 15
    }
    
    print("📊 Processing automation request...")
    print(f"   • Tasks per week: {inputs['tasks_per_week']}")
    print(f"   • Time per task: {inputs['time_per_task_minutes']} minutes")
    print(f"   • Hourly wage: ${inputs['hourly_wage']}")
    print(f"   • Automation potential: {inputs['automation_percent']}%")
    print(f"   • Error rate: {inputs['error_rate']}%")
    print(f"   • Cost per error: ${inputs['error_cost']}")
    print()
    
    # Calculate ROI
    roi_data, presentation, workflow = process_automation_request(
        agent=agent,
        workflow_name="Weekly Customer Follow-Up Automation",
        **inputs
    )
    
    # Present ROI
    print("🤖 Jermaine:")
    print(presentation)
    print()
    
    # Activation decision
    print("-" * 80)
    print("USER DECISION POINT")
    print("-" * 80)
    print()
    print("👤 User:")
    print("Yes, activate this automation.")
    print()
    
    # Save workflow
    print("🤖 Jermaine:")
    print("Executing workflow activation...")
    print()
    
    success, message = agent.save_workflow_to_ledger(workflow)
    
    if success:
        print("⚡ SOVEREIGNTY ACHIEVED ⚡")
        print()
        print(f"✅ {message}")
        print(f"✅ Workflow ID: {workflow['id']}")
        print(f"✅ Status: {workflow['status'].upper()}")
        print(f"✅ Annual Value: ${roi_data['yearly_savings']:,.2f}")
        print(f"✅ Time Reclaimed: {roi_data['hours_saved_per_year']:.1f} hours/year")
        print()
        print(workflow['flame_seal'])
    else:
        print(f"❌ {message}")
    
    print()
    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print()
    print("🤖 Jermaine:")
    print("The path is sequenced. Execution complete.")
    print()
    print("Your automation is now active and monitoring:")
    print("   • Customer database integration: READY")
    print("   • Email service connection: ACTIVE")
    print("   • CRM system sync: OPERATIONAL")
    print()
    print("Every Friday at 9:00 AM, this workflow will execute automatically.")
    print("You'll receive weekly performance reports showing:")
    print("   • Successful executions")
    print("   • Time saved")
    print("   • Error rate")
    print("   • Cumulative value delivered")
    print()
    print("What's the next priority? I stand ready for rapid execution.")
    print()
    print("=" * 80)
    print()


def demo_multiple_workflows():
    """Demonstrate managing multiple automations"""
    
    print("=" * 80)
    print("MULTIPLE WORKFLOW ORCHESTRATION")
    print("=" * 80)
    print()
    
    agent = load_jermaine_agent()
    
    workflows_to_process = [
        {
            'name': 'Social Media Content Posting',
            'tasks_per_week': 50,
            'time_per_task': 15,
            'hourly_wage': 30,
            'automation_percent': 80
        },
        {
            'name': 'Weekly Report Generation',
            'tasks_per_week': 10,
            'time_per_task': 45,
            'hourly_wage': 50,
            'automation_percent': 90
        },
        {
            'name': 'Invoice Processing',
            'tasks_per_week': 75,
            'time_per_task': 8,
            'hourly_wage': 20,
            'automation_percent': 95
        }
    ]
    
    total_yearly_savings = 0
    total_hours_saved = 0
    
    print("🤖 Jermaine:")
    print("Analyzing automation portfolio...")
    print()
    
    for workflow_params in workflows_to_process:
        roi_data, _, workflow = process_automation_request(
            agent=agent,
            **workflow_params,
            error_rate=0,
            error_cost=0
        )
        
        print(f"📊 {workflow['name']}")
        print(f"   Yearly Savings: ${roi_data['yearly_savings']:,.2f}")
        print(f"   Hours/Year: {roi_data['hours_saved_per_year']:.1f}")
        print(f"   Effectiveness: {roi_data['effectiveness']}")
        print()
        
        total_yearly_savings += roi_data['yearly_savings']
        total_hours_saved += roi_data['hours_saved_per_year']
    
    print("=" * 80)
    print("PORTFOLIO ANALYSIS")
    print("=" * 80)
    print()
    print("🤖 Jermaine:")
    print("The sovereignty dividend is substantial:")
    print()
    print(f"💰 Total Annual Savings: ${total_yearly_savings:,.2f}")
    print(f"⏰ Total Hours Reclaimed: {total_hours_saved:,.1f} hours/year")
    print(f"📈 Average ROI Multiple: {total_yearly_savings / 50000:.1f}x")
    print()
    print("That's equivalent to reclaiming", int(total_hours_saved / 40), "work weeks per year.")
    print()
    print("All three workflows can be activated simultaneously.")
    print("Shall I proceed with portfolio deployment?")
    print()
    print("=" * 80)
    print()


if __name__ == "__main__":
    # Run single workflow demo
    demo_conversation()
    
    print()
    input("Press Enter to see multiple workflow orchestration...")
    print()
    
    # Run portfolio demo
    demo_multiple_workflows()
