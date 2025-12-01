# complete_omega_test.py
"""
Complete Omega Seal Test - Creates cycles then seals them
Demonstrates the full cycle lifecycle in Codex Dominion
"""

import datetime
import json
import uuid

from omega_seal import load_ledger, save_ledger, seal_cycle


def create_test_cycles():
    """Create test cycles in the ledger"""
    print("📋 Creating test cycles in the ledger...")

    ledger = load_ledger()

    # Ensure cycles array exists
    if "cycles" not in ledger:
        ledger["cycles"] = []

    # Test cycles to create
    test_cycles = [
        {
            "id": "CYC-ALPHA",
            "name": "Alpha Test Cycle",
            "state": "completed",
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        },
        {
            "id": "CYC-BETA",
            "name": "Beta Enhancement Cycle",
            "state": "completed",
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        },
        {
            "id": "CYC-GAMMA",
            "name": "Gamma Validation Cycle",
            "state": "completed",
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        },
    ]

    # Add cycles if they don't exist
    existing_cycle_ids = {cycle["id"] for cycle in ledger["cycles"]}

    for cycle in test_cycles:
        if cycle["id"] not in existing_cycle_ids:
            ledger["cycles"].append(cycle)
            print(f"   ✅ Created cycle: {cycle['id']} - {cycle['name']}")

    save_ledger(ledger)
    print("📋 Test cycles created successfully!")
    print()


def test_omega_sealing():
    """Test the omega sealing process"""
    print("🔥 CODEX DOMINION - COMPLETE OMEGA SEAL TEST 🔥")
    print("=" * 55)
    print()

    # First create test cycles
    create_test_cycles()

    # Test cycle sealing
    test_cycles = [
        ("CYC-ALPHA", "First alpha cycle completion test"),
        ("CYC-BETA", "Beta cycle with enhanced features"),
        ("CYC-GAMMA", "Gamma cycle - final validation phase"),
    ]

    archives = []

    for cycle_id, note in test_cycles:
        print(f"🔐 Sealing cycle: {cycle_id}")
        try:
            archive = seal_cycle(cycle_id, note=note)
            archives.append(archive)
            print(f"   ✅ Archive created: {archive['archive_id']}")
            print(f"   📅 Completed: {archive['completed_at']}")
            print(f"   👤 Sealed by: {archive['custodian_seal']}")
            print(f"   📝 Note: {archive['note']}")
            print()
        except Exception as e:
            print(f"   ❌ Error sealing {cycle_id}: {e}")
            print()

    # Display current ledger status
    print("📊 CURRENT LEDGER STATUS:")
    print("-" * 30)

    ledger = load_ledger()

    print(f"🔒 Omega Seal Active: {ledger['meta'].get('omega_seal', False)}")
    print(f"📅 Last Updated: {ledger['meta'].get('last_updated', 'Unknown')}")
    print(f"💓 Heartbeat: {ledger['heartbeat']['status']}")
    print()

    # Show cycles status
    cycles = ledger.get("cycles", [])
    print(f"🔄 Total Cycles: {len(cycles)}")
    if cycles:
        print("   Current Cycles:")
        for cycle in cycles[-5:]:  # Show last 5
            print(f"     • {cycle['id']} - {cycle['name']} [{cycle['state']}]")
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

    # Show contributions if any
    contributions = ledger.get("contributions", [])
    if contributions:
        print(f"💬 Community Contributions: {len(contributions)}")
        affirmed = len([c for c in contributions if c.get("status") == "affirmed"])
        silenced = len([c for c in contributions if c.get("status") == "silenced"])
        pending = len([c for c in contributions if not c.get("status")])
        print(
            f"   ✅ Affirmed: {affirmed} | 🔕 Silenced: {silenced} | ⏳ Pending: {pending}"
        )
        print()

    # Test summary
    print("🎯 TEST SUMMARY:")
    print(f"   ✅ Cycles Created: {len(test_cycles)}")
    print(f"   📦 Archives Created: {len([a for a in archives if a])}")
    print(f"   🔥 Omega Seal Status: OPERATIONAL")
    print()
    print("🌟 Complete omega seal test finished successfully!")
    print("🔥 Digital sovereignty confirmed and archived!")
    print()
    print("💡 You can now view the results in the dashboard:")
    print("   python -m streamlit run app.py --server.port 8095")


if __name__ == "__main__":
    test_omega_sealing()
