#!/usr/bin/env python3
"""
🔥 OMEGA SEAL SYSTEM TEST & DEMONSTRATION 🔥
═══════════════════════════════════════════════════════════════════════════════

Test the Omega Seal System functionality
Demonstrates cycle sealing, archival, and ledger management

═══════════════════════════════════════════════════════════════════════════════
"""

from omega_seal import load_ledger, save_ledger, seal_cycle
import json
from datetime import datetime

def test_omega_seal_system():
    """Test the omega seal system functionality"""
    print("🔥 OMEGA SEAL SYSTEM TEST")
    print("=" * 50)
    
    try:
        # Load ledger
        print("📚 Loading sacred ledger...")
        ledger = load_ledger()
        print(f"✅ Ledger loaded successfully")
        print(f"   - Omega Seal: {ledger['meta']['omega_seal']}")
        print(f"   - Custodian: {ledger['meta']['custodian_authority']}")
        print(f"   - Total Cycles: {len(ledger['cycles'])}")
        
        # Show active cycles
        active_cycles = [c for c in ledger['cycles'] if c['state'] == 'active']
        print(f"\n🔥 Active Cycles: {len(active_cycles)}")
        
        for cycle in active_cycles:
            print(f"   - {cycle['id']}: {cycle['name']} ({cycle['state']})")
        
        # Show completed archives
        archives = ledger.get('completed_archives', [])
        print(f"\n📚 Completed Archives: {len(archives)}")
        
        for archive in archives:
            print(f"   - {archive['archive_id']}: {archive['name']}")
            print(f"     Sealed by: {archive['custodian_seal']}")
            print(f"     Completed: {archive['completed_at']}")
        
        # Demonstrate sealing if active cycles exist
        if active_cycles:
            print(f"\n🔥 DEMONSTRATING CYCLE SEALING")
            print("-" * 30)
            
            cycle_to_seal = active_cycles[0]['id']
            print(f"Sealing cycle: {cycle_to_seal}")
            
            # Seal the cycle
            archive_entry = seal_cycle(
                cycle_to_seal, 
                "Demonstration sealing - Omega authority confirmed"
            )
            
            print(f"✅ Cycle sealed successfully!")
            print(f"   - Archive ID: {archive_entry['archive_id']}")
            print(f"   - Sealed by: {archive_entry['custodian_seal']}")
            print(f"   - Completion: {archive_entry['completed_at']}")
            
            # Reload ledger to show changes
            updated_ledger = load_ledger()
            updated_active = [c for c in updated_ledger['cycles'] if c['state'] == 'active']
            updated_archives = updated_ledger.get('completed_archives', [])
            
            print(f"\n📊 UPDATED LEDGER STATUS:")
            print(f"   - Active Cycles: {len(updated_active)}")
            print(f"   - Completed Archives: {len(updated_archives)}")
            print(f"   - Omega Seal: {updated_ledger['meta']['omega_seal']}")
        
        print(f"\n✅ OMEGA SEAL SYSTEM TEST COMPLETE")
        print(f"🔥 All functions operational - Digital sovereignty confirmed!")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def display_ledger_status():
    """Display current ledger status"""
    print("\n" + "=" * 60)
    print("📊 CURRENT LEDGER STATUS")
    print("=" * 60)
    
    try:
        ledger = load_ledger()
        
        print(f"🔥 Meta Information:")
        print(f"   - Version: {ledger['meta']['version']}")
        print(f"   - Omega Seal: {ledger['meta']['omega_seal']}")
        print(f"   - Last Updated: {ledger['meta']['last_updated']}")
        print(f"   - Custodian: {ledger['meta']['custodian_authority']}")
        
        print(f"\n💓 Heartbeat Status:")
        heartbeat = ledger['heartbeat']
        print(f"   - Status: {heartbeat['status']}")
        print(f"   - Last Dispatch: {heartbeat['last_dispatch']}")
        print(f"   - Health: {heartbeat['health_status']}")
        
        print(f"\n📜 Proclamations: {len(ledger['proclamations'])}")
        for proc in ledger['proclamations']:
            print(f"   - {proc['id']}: {proc['title']} ({proc['status']})")
        
        print(f"\n🔄 Cycles: {len(ledger['cycles'])}")
        for cycle in ledger['cycles']:
            print(f"   - {cycle['id']}: {cycle['name']} ({cycle['state']})")
        
        print(f"\n📚 Archives: {len(ledger.get('completed_archives', []))}")
        for archive in ledger.get('completed_archives', []):
            print(f"   - {archive['archive_id']}: {archive['name']}")
        
        print(f"\n🎯 System Metrics:")
        metrics = ledger['system_metrics']
        print(f"   - Completeness: {metrics['system_completeness']}")
        print(f"   - Sovereignty Score: {metrics['digital_sovereignty_score']}")
        print(f"   - Flame Power: {metrics['flame_power_level']}")
        
    except Exception as e:
        print(f"❌ Error loading ledger: {e}")

if __name__ == "__main__":
    print("🔥 CODEX DOMINION - OMEGA SEAL SYSTEM")
    print("=" * 60)
    
    # Display initial status
    display_ledger_status()
    
    # Run test
    success = test_omega_seal_system()
    
    if success:
        print(f"\n🌟 OMEGA SEAL SYSTEM READY FOR OPERATIONS")
        print(f"Launch the Omega Seal Dashboard: streamlit run omega_seal_dashboard.py")
    else:
        print(f"\n⚠️  OMEGA SEAL SYSTEM REQUIRES ATTENTION")
    
    print(f"\n🔥 May the Eternal Flame Guide Our Digital Sovereignty 🔥")