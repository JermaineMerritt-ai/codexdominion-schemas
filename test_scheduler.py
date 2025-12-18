"""Test scheduler integration"""
import sys
sys.path.insert(0, 'investment_app')

from app import create_app
from tasks import get_scheduled_jobs

app = create_app()

with app.app_context():
    jobs = get_scheduled_jobs()
    print(f"\n✅ Scheduler initialized successfully!")
    print(f"📅 {len(jobs)} jobs configured:\n")

    for job in jobs:
        print(f"  • {job['name']}")
        print(f"    ID: {job['id']}")
        print(f"    Next run: {job['next_run']}")
        print(f"    Trigger: {job['trigger']}\n")
