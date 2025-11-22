"""
🔥 DAWN MONETIZATION SCROLL - SIMPLE INTEGRATION 📜
Exact implementation for seamless integration into existing systems

The Merritt Method™ - Revenue Analytics Sovereignty
"""

import os
import datetime
import json
from pathlib import Path

def dawn_monetization_scroll():
    """
    🔥 Dawn Monetization Scroll - Simple Implementation
    Read last entries from JSONL ledgers and produce a single report
    
    This is the exact function requested for integration.
    """
    
    def tail(path, n=1):
        """Read the last n entries from a JSONL file"""
        try:
            file_path = Path(path)
            if not file_path.exists():
                return []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return [json.loads(l) for l in lines[-n:]] if lines else []
        except Exception:
            return []
    
    # Read last entries from JSONL ledgers and produce a single report
    report = {
        "youtube": tail("ledger_youtube.jsonl"),
        "tiktok": tail("ledger_tiktok.jsonl"),
        "threads": tail("ledger_threads.jsonl"),
        "whatsapp": tail("ledger_whatsapp.jsonl"),
        "pinterest": tail("ledger_pinterest.jsonl"),
        "affiliate": tail("ledger_affiliate.jsonl"),
    }
    
    # Archive the monetization report
    with open("completed_archives.jsonl", "a", encoding='utf-8') as f:
        f.write(json.dumps({"ts": datetime.datetime.utcnow().isoformat(), "monetization": report}) + "\n")
    
    return report

# Example usage and testing
if __name__ == "__main__":
    print("🔥 Testing Simple Dawn Monetization Scroll...")
    
    report = dawn_monetization_scroll()
    
    print("📜 Monetization Report Generated:")
    for platform, data in report.items():
        status = "✅ Data Available" if data else "❌ No Data"
        print(f"  {platform.upper()}: {status}")
    
    print("💾 Report archived to completed_archives.jsonl")
    print("🔥 Dawn Monetization Scroll completed!")