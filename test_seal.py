# test_seal.py
from omega_seal import seal_cycle, load_ledger
import json

def test_simple_omega_seal():
    """Simple test of omega seal functionality"""
    print("🔥 Testing Omega Seal Functionality...")
    
    try:
        # Test sealing an existing cycle
        archive = seal_cycle("CYC-001", note="Omega completion confirmed.")
        print("✅ Archive created successfully!")
        print("📦 Archived:", json.dumps(archive, indent=2))
        
        # Show current ledger status
        ledger = load_ledger()
        print(f"\n🔒 Omega Seal Active: {ledger['meta'].get('omega_seal', False)}")
        print(f"📚 Total Archives: {len(ledger.get('completed_archives', []))}")
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("💡 Tip: Run 'python complete_omega_test.py' to create test cycles first")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_simple_omega_seal()