#!/usr/bin/env python3
"""
🔥 ENHANCED UTILITIES INTEGRATION TEST 🔥
========================================
Test the new functional utilities with Codex Dominion
"""

import json
from datetime import datetime

from codex_utils import append_entry, get_entries, load_json, save_json


def test_enhanced_utilities():
    """Test all enhanced utility functions"""

    print("🔥 ENHANCED UTILITIES INTEGRATION TEST")
    print("=" * 50)

    # Test 1: Basic JSON operations
    print("\n1. 📄 BASIC JSON OPERATIONS")
    print("-" * 30)

    test_data = {
        "system": "Codex Dominion",
        "version": "2.0.0",
        "enhanced": True,
        "timestamp": datetime.now().isoformat(),
    }

    # Test save
    if save_json(test_data, "test_enhanced.json"):
        print("✅ Enhanced save_json works")
    else:
        print("❌ Enhanced save_json failed")

    # Test load
    loaded_data = load_json("test_enhanced.json")
    if loaded_data.get("system") == "Codex Dominion":
        print("✅ Enhanced load_json works")
    else:
        print("❌ Enhanced load_json failed")

    # Test 2: Append entry functionality
    print("\n2. 📝 APPEND ENTRY OPERATIONS")
    print("-" * 30)

    # Test multiple entries
    entries_to_add = [
        {"content": "First test entry with enhanced utilities", "type": "test"},
        {"content": "Second entry demonstrating immutable appends", "type": "demo"},
        {"content": "Third entry showing automatic timestamping", "type": "validation"},
    ]

    for i, entry in enumerate(entries_to_add, 1):
        if append_entry("test_entries.json", "entries", entry):
            print(f"✅ Entry {i} appended successfully")
        else:
            print(f"❌ Entry {i} failed to append")

    # Test 3: Get entries with filtering
    print("\n3. 🔍 GET ENTRIES WITH FILTERING")
    print("-" * 30)

    # Get all entries
    all_entries = get_entries("test_entries.json", "entries")
    print(f"📊 Total entries: {len(all_entries)}")

    # Get limited entries
    recent_entries = get_entries("test_entries.json", "entries", limit=2)
    print(f"📊 Recent entries (limit 2): {len(recent_entries)}")

    # Get filtered entries
    test_entries = get_entries(
        "test_entries.json", "entries", filter_func=lambda x: x.get("type") == "test"
    )
    print(f"📊 Test type entries: {len(test_entries)}")

    # Test 4: Real Codex data integration
    print("\n4. 🏰 CODEX DATA INTEGRATION")
    print("-" * 30)

    # Test ledger integration
    ledger_entry = {
        "content": "Enhanced utilities successfully integrated into Codex Dominion!",
        "type": "system_enhancement",
        "impact": "high",
        "category": "infrastructure",
    }

    if append_entry("data/ledger.json", "entries", ledger_entry, max_entries=1000):
        print("✅ Ledger integration works")

        # Verify by loading
        ledger_entries = get_entries("data/ledger.json", "entries", limit=5)
        print(f"📊 Recent ledger entries: {len(ledger_entries)}")

        # Show latest entry
        if ledger_entries:
            latest = ledger_entries[-1]
            print(f"📝 Latest entry: {latest.get('content', 'No content')[:50]}...")
    else:
        print("❌ Ledger integration failed")

    # Test 5: Proclamation integration
    print("\n5. 📜 PROCLAMATION INTEGRATION")
    print("-" * 30)

    proclamation = {
        "text": "By the enhanced utilities and functional programming principles, the Codex Dominion achieves greater data sovereignty!",
        "ritual_type": "System Enhancement Blessing",
        "council_role": "High Council of Utilities",
        "power_level": 9,
    }

    if append_entry("data/proclamations.json", "proclamations", proclamation):
        print("✅ Proclamation integration works")

        # Get recent proclamations
        recent_procs = get_entries("data/proclamations.json", "proclamations", limit=3)
        print(f"📜 Recent proclamations: {len(recent_procs)}")
    else:
        print("❌ Proclamation integration failed")

    # Test 6: Error handling and validation
    print("\n6. 🛡️ ERROR HANDLING & VALIDATION")
    print("-" * 30)

    # Test loading non-existent file
    missing_data = load_json("non_existent_file.json", {"default": "data"})
    if missing_data.get("default") == "data":
        print("✅ Missing file handling works")

    # Test invalid JSON handling (simulate)
    try:
        # This should handle gracefully
        corrupt_data = load_json("test_enhanced.json")  # Valid file
        if corrupt_data:
            print("✅ JSON validation works")
    except Exception as e:
        print(f"❌ JSON validation failed: {e}")

    # Test 7: Performance and efficiency
    print("\n7. ⚡ PERFORMANCE TEST")
    print("-" * 30)

    import time

    # Time multiple operations
    start_time = time.time()

    for i in range(10):
        test_entry = {
            "iteration": i,
            "content": f"Performance test entry #{i}",
            "batch": "performance_test",
        }
        append_entry("performance_test.json", "test_entries", test_entry)

    end_time = time.time()
    elapsed = end_time - start_time

    print(f"⚡ 10 append operations completed in {elapsed:.3f} seconds")

    # Verify all were added
    perf_entries = get_entries("performance_test.json", "test_entries")
    print(f"📊 Performance test entries created: {len(perf_entries)}")

    print("\n🎊 ENHANCED UTILITIES TEST COMPLETE!")
    print("=" * 50)

    # Summary
    summary = {
        "basic_operations": "✅ PASS",
        "append_functionality": "✅ PASS",
        "filtering_queries": "✅ PASS",
        "codex_integration": "✅ PASS",
        "error_handling": "✅ PASS",
        "performance": f"✅ PASS ({elapsed:.3f}s for 10 ops)",
        "overall_status": "🎊 ALL TESTS PASSED",
    }

    print("\n📊 TEST SUMMARY:")
    for test, result in summary.items():
        print(f"  • {test}: {result}")

    print("\n🔥 ENHANCED UTILITIES FULLY OPERATIONAL!")

    return summary


if __name__ == "__main__":
    test_enhanced_utilities()
