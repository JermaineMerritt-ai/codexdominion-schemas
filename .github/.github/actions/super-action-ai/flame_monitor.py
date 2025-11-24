#!/usr/bin/env python3
"""
Super Action AI - Flame Monitor
Monitors Codex flame status and provides intelligent alerts.
"""

import os
import json
import requests
from datetime import datetime

def check_flame_detailed(url, name):
    """Check flame status with detailed reporting."""
    try:
        response = requests.get(url, timeout=10)
        status = {
            "name": name,
            "url": url,
            "status_code": response.status_code,
            "response_time": response.elapsed.total_seconds(),
            "alive": response.status_code == 200,
            "timestamp": datetime.now().isoformat()
        }
        return status
    except Exception as e:
        return {
            "name": name,
            "url": url,
            "status_code": None,
            "response_time": None,
            "alive": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def monitor_flames():
    """Monitor all Codex flames and generate report."""
    print("🔥 Super Action AI Flame Monitor starting...")
    
    flames = [
        ("Production", "https://aistorelab.com"),
        ("Staging", "https://staging.aistorelab.com")
    ]
    
    monitoring_report = {
        "timestamp": datetime.now().isoformat(),
        "flames": [],
        "overall_status": "checking",
        "alerts": []
    }
    
    all_alive = True
    
    for name, url in flames:
        print(f"🔍 Checking {name} flame ({url})...")
        flame_status = check_flame_detailed(url, name)
        monitoring_report["flames"].append(flame_status)
        
        if flame_status["alive"]:
            print(f"✅ {name} flame: ALIVE (Status: {flame_status['status_code']})")
        else:
            print(f"❌ {name} flame: DOWN")
            all_alive = False
            monitoring_report["alerts"].append(f"{name} flame is not responding")
    
    # Generate overall status
    if all_alive:
        monitoring_report["overall_status"] = "all_flames_alive"
        print("🎉 All Codex flames are burning bright!")
    else:
        monitoring_report["overall_status"] = "flames_need_attention"
        print("⚠️ Some Codex flames need attention!")
    
    # Save monitoring report
    with open("flame_monitoring_report.json", "w") as f:
        json.dump(monitoring_report, f, indent=2)
    
    return monitoring_report

def main():
    report = monitor_flames()
    
    # Set GitHub Actions outputs
    if os.getenv("GITHUB_ACTIONS"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"flame_status={report['overall_status']}\n")
            f.write(f"alerts={json.dumps(report['alerts'])}\n")
            f.write(f"flame_count={len(report['flames'])}\n")

if __name__ == "__main__":
    main()