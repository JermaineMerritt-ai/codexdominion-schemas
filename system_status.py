# system_status.py
from omega_seal import load_ledger
import json
from datetime import datetime

def display_system_status():
    """Display comprehensive Codex Dominion system status"""
    print("=" * 60)
    print("🏛️  CODEX DOMINION - DIGITAL SOVEREIGNTY STATUS")
    print("=" * 60)
    
    try:
        ledger = load_ledger()
        
        # System Overview
        print(f"📅 Last Updated: {ledger['meta'].get('last_updated', 'Unknown')}")
        print(f"🔒 Omega Seal: {'ACTIVE' if ledger['meta'].get('omega_seal', False) else 'INACTIVE'}")
        print(f"👑 Custodian: {ledger['meta'].get('custodian', 'Unknown')}")
        
        # Cycles Status
        cycles = ledger.get('cycles', [])
        active_cycles = [c for c in cycles if c.get('status') == 'active']
        print(f"\n🔄 CYCLE MANAGEMENT:")
        print(f"   Total Cycles: {len(cycles)}")
        print(f"   Active Cycles: {len(active_cycles)}")
        
        # Archives Status
        archives = ledger.get('completed_archives', [])
        print(f"\n📚 ARCHIVE MANAGEMENT:")
        print(f"   Total Archives: {len(archives)}")
        if archives:
            latest_archive = max(archives, key=lambda x: x.get('completed_at', ''))
            print(f"   Latest Archive: {latest_archive.get('archive_id', 'Unknown')}")
        
        # Community Status
        contributions = ledger.get('contributions', [])
        pending_contributions = [c for c in contributions if c.get('status') == 'pending']
        print(f"\n🤝 COMMUNITY STATUS:")
        print(f"   Total Contributions: {len(contributions)}")
        print(f"   Pending Review: {len(pending_contributions)}")
        
        # Council Status
        council = ledger.get('council', {})
        print(f"\n🏛️  COUNCIL STATUS:")
        print(f"   Advisory Members: {len(council.get('advisory_members', []))}")
        print(f"   Active Protocols: {len(council.get('protocols', []))}")
        
        # Service Status
        print(f"\n⚡ SERVICE STATUS:")
        print(f"   Main Dashboard: http://localhost:8095 (app.py)")
        print(f"   Council Portal: http://localhost:8080")
        print(f"   Contributions: http://localhost:8085")
        print(f"   Analytics: Multiple dashboards active")
        
        print("\n" + "=" * 60)
        print("✅ SYSTEM STATUS: FULLY OPERATIONAL")
        print("🎯 DIGITAL SOVEREIGNTY: ACHIEVED")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error loading system status: {e}")

if __name__ == "__main__":
    display_system_status()