#!/usr/bin/env python3
"""
Festival Ceremony Script - SSL Flame Checker
Checks Codex flames (production + staging) and proclaims seasonal blessing.
"""

import datetime
import requests

def check_flame(url):
    try:
        r = requests.get(url, timeout=5)
        return r.status_code == 200
    except Exception:
        return False

def seasonal_blessing():
    month = datetime.datetime.now().month
    if month in [3,4,5]:
        return "🌸 The Codex blossoms anew; the flame is crowned in Spring's renewal."
    elif month in [6,7,8]:
        return "☀️ The Codex burns bright; the flame is crowned in Summer's radiance."
    elif month in [9,10,11]:
        return "🍂 The Codex gathers memory; the flame is crowned in Autumn's harvest."
    else:
        return "❄️ The Codex endures; the flame is crowned in Winter's vigil."

def main():
    print("🔥 Festival Ceremony begins...")
    prod_alive = check_flame("https://aistorelab.com")
    stag_alive = check_flame("https://staging.aistorelab.com")

    if prod_alive and stag_alive:
        print(seasonal_blessing())
    else:
        print("⚠️ One or more flames are resting. Summon a custodian.")

    print("🕯️ Ceremony closes.")

if __name__ == "__main__":
    main()