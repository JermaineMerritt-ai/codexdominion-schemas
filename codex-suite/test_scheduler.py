#!/usr/bin/env python3
"""Test Great Year Scheduler"""

import sys
sys.path.append('.')

from core.scheduler import check_great_year, GREAT_YEAR_DATES
from datetime import datetime

print("🌌 Great Year Scheduler Test")
print("=" * 40)

now = datetime.now()
print(f"Current date/time: {now.month}/{now.day} at {now.hour}:{now.minute:02d}")
print(f"Great Year dates: {GREAT_YEAR_DATES}")

# Check current conditions
is_great_year = (now.month, now.day) in GREAT_YEAR_DATES
is_dawn = now.hour == 6 and now.minute == 0

print(f"Is Great Year date: {is_great_year}")
print(f"Is dawn hour (6:00): {is_dawn}")

if is_great_year and is_dawn:
    print("🔥 TRIGGERING Great Year Invocation!")
else:
    print("⏰ Not triggering (conditions not met)")

# Test the actual function
print("\nTesting check_great_year() function...")
check_great_year()
print("✅ Great Year scheduler test completed")

# Show what dates would trigger
print(f"\nGreat Year Invocations occur on these dates at 6:00 AM:")
for month, day in GREAT_YEAR_DATES:
    season = ["Spring Equinox", "Summer Solstice", "Autumn Equinox", "Winter Solstice"]
    season_name = season[GREAT_YEAR_DATES.index((month, day))]
    print(f"  - {month}/{day} ({season_name})")