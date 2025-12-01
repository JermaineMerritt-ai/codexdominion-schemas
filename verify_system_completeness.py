#!/usr/bin/env python3
"""
System Completeness Verification - Post-Addition Check
====================================================

Verifies all missing files have been added and the system is complete.
"""

import json
from datetime import datetime
from pathlib import Path


def main():
    print("🔍 SYSTEM COMPLETENESS VERIFICATION")
    print("=" * 50)

    base_path = Path(".")
    verification_results = {
        "timestamp": datetime.now().isoformat(),
        "verification_status": "COMPLETE",
        "files_checked": 0,
        "files_found": 0,
        "files_missing": 0,
        "critical_issues": [],
        "system_health": "OPERATIONAL",
    }

    # Check all the files we just created
    required_files = [
        "flows.json",
        "dispatch_log.json",
        "events.json",
        "concords.json",
        "revenue_streams.json",
        "package.json",
        "modules/spark_studio.py",
    ]

    print("📋 REQUIRED FILES CHECK:")
    print("-" * 30)

    for file in required_files:
        verification_results["files_checked"] += 1
        file_path = base_path / file

        if file_path.exists():
            verification_results["files_found"] += 1
            print(f"✅ {file}")

            # Validate JSON files
            if file.endswith(".json"):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        json.load(f)
                    print(f"   📄 Valid JSON structure")
                except json.JSONDecodeError:
                    print(f"   ⚠️ Invalid JSON format")
                    verification_results["critical_issues"].append(
                        f"Invalid JSON: {file}"
                    )
        else:
            verification_results["files_missing"] += 1
            verification_results["critical_issues"].append(f"Missing file: {file}")
            print(f"❌ {file}")

    # Check existing critical files
    existing_critical = [
        "codex_models.py",
        "codex_utils.py",
        "ledger.json",
        "cycles.json",
        "proclamations.json",
        "requirements.txt",
        ".env",
    ]

    print(f"\n📋 EXISTING CRITICAL FILES:")
    print("-" * 30)

    for file in existing_critical:
        verification_results["files_checked"] += 1
        file_path = base_path / file

        if file_path.exists():
            verification_results["files_found"] += 1
            print(f"✅ {file}")
        else:
            print(f"⚠️ {file}")

    # Check dashboard availability
    print(f"\n🎯 DASHBOARD AVAILABILITY:")
    print("-" * 30)

    dashboard_files = [
        "codex-suite/apps/dashboard/codex_unified.py",
        "codex-suite/apps/dashboard/council_access.py",
        "codex-suite/apps/dashboard/heir_avatar.py",
    ]

    for dashboard in dashboard_files:
        verification_results["files_checked"] += 1
        dashboard_path = base_path / dashboard

        if dashboard_path.exists():
            verification_results["files_found"] += 1
            print(f"✅ {dashboard}")
        else:
            print(f"❌ {dashboard}")
            verification_results["critical_issues"].append(
                f"Missing dashboard: {dashboard}"
            )

    # Calculate completion percentage
    completion_percentage = (
        verification_results["files_found"] / verification_results["files_checked"]
    ) * 100

    print(f"\n📊 SYSTEM STATUS SUMMARY:")
    print("-" * 30)
    print(f"📁 Files Checked: {verification_results['files_checked']}")
    print(f"✅ Files Found: {verification_results['files_found']}")
    print(f"❌ Files Missing: {verification_results['files_missing']}")
    print(f"📈 Completion: {completion_percentage:.1f}%")

    if verification_results["critical_issues"]:
        print(f"\n⚠️ CRITICAL ISSUES ({len(verification_results['critical_issues'])}):")
        for issue in verification_results["critical_issues"]:
            print(f"   - {issue}")
        verification_results["system_health"] = "ISSUES_DETECTED"
    else:
        print(f"\n🎉 NO CRITICAL ISSUES DETECTED!")
        verification_results["system_health"] = "FULLY_OPERATIONAL"

    # Test Spark Studio
    print(f"\n🎯 SPARK STUDIO TEST:")
    print("-" * 30)

    try:
        import sys

        sys.path.append("modules")
        from spark_studio import SparkStudioEngine, quick_spark

        # Quick test
        test_spark = quick_spark("System Verification", "tech_leaders", "professional")
        print(f"✅ Spark Studio operational")
        print(f"   📝 Generated spark: {test_spark['content']['title']}")
        print(f"   📊 Quality score: {test_spark['metadata']['quality_score']}/10")

        verification_results["spark_studio_status"] = "OPERATIONAL"

    except Exception as e:
        print(f"❌ Spark Studio error: {e}")
        verification_results["spark_studio_status"] = "ERROR"
        verification_results["critical_issues"].append(f"Spark Studio error: {e}")

    # Overall system assessment
    if completion_percentage >= 95 and not verification_results["critical_issues"]:
        verification_results["verification_status"] = "SYSTEM_COMPLETE"
        final_status = "🔥 SYSTEM FULLY OPERATIONAL - ALL COMPONENTS ADDED! 🔥"
    elif completion_percentage >= 90:
        verification_results["verification_status"] = "MOSTLY_COMPLETE"
        final_status = "⚡ SYSTEM MOSTLY COMPLETE - MINOR ISSUES DETECTED"
    else:
        verification_results["verification_status"] = "INCOMPLETE"
        final_status = "⚠️ SYSTEM INCOMPLETE - MAJOR COMPONENTS MISSING"

    print(f"\n{final_status}")
    print("=" * len(final_status))

    # Save verification report
    with open("SYSTEM_COMPLETENESS_REPORT.json", "w") as f:
        json.dump(verification_results, f, indent=2)

    print(f"\n📄 Verification report saved: SYSTEM_COMPLETENESS_REPORT.json")

    return verification_results["verification_status"] == "SYSTEM_COMPLETE"


if __name__ == "__main__":
    main()
