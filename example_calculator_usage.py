"""
Complete Python example for Calculator API
"""
import requests

# Make API request
response = requests.post(
    "http://localhost:5000/api/calculators/savings",
    json={
        "tasks_per_week": 200,
        "time_per_task_minutes": 10,
        "hourly_wage": 25,
        "automation_percent": 0.7,
        "error_rate": 0.1,
        "cost_per_error": 15,
        "value_per_accelerated_task": 0
    }
)

# Print results
print(f"\nStatus Code: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    print(f"\n💰 Savings Breakdown:")
    print(f"   Weekly:  ${result['weekly_savings']:,.2f}")
    print(f"   Monthly: ${result['monthly_savings']:,.2f}")
    print(f"   Yearly:  ${result['yearly_savings']:,.2f}")
    print(f"\n⏰ Time Saved: {result['hours_saved_per_week']} hours/week")
    print(f"\n📊 Effectiveness: {result['effectiveness']}")
    print(f"\n✅ Success: {result['success']}\n")
else:
    print(f"❌ Error: {response.text}\n")
