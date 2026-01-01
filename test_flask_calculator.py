"""Test the Flask calculator API"""
import requests
import json

url = "http://localhost:5000/api/calculators/savings"
data = {
    "tasks_per_week": 200,
    "time_per_task_minutes": 10,
    "hourly_wage": 25,
    "automation_percent": 0.7,
    "error_rate": 0.1,
    "cost_per_error": 15,
    "value_per_accelerated_task": 0
}

print("\n" + "="*60)
print("Testing Flask Calculator API")
print("="*60)
print(f"URL: {url}\n")

response = requests.post(url, json=data)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    print(f"\n✅ SUCCESS!\n")
    print(f"Weekly: ${result['weekly_savings']}")
    print(f"Yearly: ${result['yearly_savings']}")
    print(f"Hours/Week: {result['hours_saved_per_week']}")
    print(f"Effectiveness: {result['effectiveness']}\n")
else:
    print(f"❌ Error: {response.text}\n")

print("="*60 + "\n")
