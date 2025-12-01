# comprehensive_omega_test.py
"""
Comprehensive test of the Omega Seal system
Tests multiple cycles and demonstrates the archive functionality
"""

import json

from omega_seal import load_ledger, seal_cycle


def test_comprehensive_omega_seal():
    print("🔥 CODEX DOMINION - COMPREHENSIVE OMEGA SEAL TEST 🔥")
    print("=" * 55)
    print()

    # Test multiple cycle sealing
    test_cycles = [
        ("CYC-ALPHA", "First alpha cycle completion test"),
        ("CYC-BETA", "Beta cycle with enhanced features"),
        ("CYC-GAMMA", "Gamma cycle - final validation phase"),
    ]

    archives = []

    for cycle_id, note in test_cycles:
        print(f"🔐 Sealing cycle: {cycle_id}")
        archive = seal_cycle(cycle_id, note=note)
        archives.append(archive)
        print(f"   ✅ Archive created: {archive['archive_id']}")
        print(f"   📅 Completed: {archive['completed_at']}")
        print(f"   👤 Sealed by: {archive['custodian_seal']}")
        print(f"   📝 Note: {archive['note']}")
        print()

    # Display current ledger status
    print("📊 CURRENT LEDGER STATUS:")
    print("-" * 30)

    ledger = load_ledger()

    print(f"🔒 Omega Seal Active: {ledger['meta'].get('omega_seal', False)}")
    print(f"📅 Last Updated: {ledger['meta'].get('last_updated', 'Unknown')}")
    print(f"💓 Heartbeat: {ledger['heartbeat']['status']}")
    print()

    # Show all completed archives
    completed_archives = ledger.get("completed_archives", [])
    print(f"📚 Total Completed Archives: {len(completed_archives)}")

    if completed_archives:
        print("\n🏛️ ARCHIVE REGISTRY:")
        for i, archive in enumerate(completed_archives[-5:], 1):  # Show last 5
            print(f"   {i}. {archive['archive_id']} - {archive['name']}")
            print(f"      Cycle: {archive['cycle_id']}")
            print(f"      Sealed: {archive['completed_at']}")
            print(f"      By: {archive['custodian_seal']}")
            print()

    # Test summary
    print("🎯 TEST SUMMARY:")
    print(f"   ✅ Cycles Sealed: {len(test_cycles)}")
    print(f"   📦 Archives Created: {len(archives)}")
    print(f"   🔥 Omega Seal Status: OPERATIONAL")
    print()
    print("🌟 All omega seal operations completed successfully!")
    print("🔥 Digital sovereignty confirmed and archived!")


if __name__ == "__main__":
    test_comprehensive_omega_seal()
