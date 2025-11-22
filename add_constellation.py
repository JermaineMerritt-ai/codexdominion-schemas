#!/usr/bin/env python3
"""
Constellation Data Integration
=============================
Add constellation revenue data to the Codex Dominion ledger system
"""

import json
import os
from datetime import datetime
from pathlib import Path

def ensure_data_dir():
    """Ensure data directory exists"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    return data_dir

def save_json_simple(filename, data):
    """Simple JSON save function"""
    filepath = ensure_data_dir() / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return filepath

def load_json_simple(filename, default=None):
    """Simple JSON load function"""
    filepath = ensure_data_dir() / filename
    if filepath.exists():
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return default or {}

def append_entry_simple(filename, key, entry):
    """Simple entry append function"""
    data = load_json_simple(filename, {})
    if key not in data:
        data[key] = []
    
    # Add timestamp and ID
    entry['timestamp'] = datetime.now().isoformat()
    entry['id'] = len(data[key]) + 1
    
    data[key].append(entry)
    save_json_simple(filename, data)
    return entry

def main():
    """Main constellation data integration"""
    
    print("🌟 ADDING CONSTELLATION DATA TO CODEX LEDGER")
    print("=" * 50)
    
    # Constellation data provided
    constellation_data = {
        "constellation": [
            {
                "stream": "Store",
                "cycle": "Morning Flame",
                "amount": 300,
                "star": "Golden Dawn",
                "timestamp": "2025-11-07T06:00:00"
            },
            {
                "stream": "Social",
                "cycle": "Twilight Flame",
                "amount": 150,
                "star": "Evening Concord",
                "timestamp": "2025-11-07T18:00:00"
            },
            {
                "stream": "Website",
                "cycle": "Seasonal Festival",
                "amount": 200,
                "star": "Festival Radiance",
                "timestamp": "2025-11-07T15:00:00"
            }
        ]
    }
    
    # Create enhanced constellation entry for the ledger
    constellation_entry = {
        "type": "constellation_revenue",
        "description": "Revenue Constellation - Multi-Stream Earnings",
        "authority": "Revenue Crown",
        "data": constellation_data,
        "total_amount": sum(item["amount"] for item in constellation_data["constellation"]),
        "stream_count": len(constellation_data["constellation"]),
        "cycles": list(set(item["cycle"] for item in constellation_data["constellation"])),
        "stars": list(set(item["star"] for item in constellation_data["constellation"]))
    }
    
    # Add to main ledger
    result = append_entry_simple("ledger.json", "entries", constellation_entry)
    print(f"✅ Added constellation to main ledger: {result.get('timestamp')}")
    
    # Save constellation data to dedicated file
    constellation_file_data = {
        "constellations": [constellation_data],
        "metadata": {
            "total_revenue": constellation_entry["total_amount"],
            "last_updated": datetime.now().isoformat(),
            "stream_types": ["Store", "Social", "Website"],
            "active_cycles": constellation_entry["cycles"],
            "active_stars": constellation_entry["stars"]
        }
    }
    
    save_json_simple("constellations.json", constellation_file_data)
    print("✅ Saved constellation data to constellations.json")
    
    # Add individual entries for each stream
    for stream_data in constellation_data["constellation"]:
        stream_entry = {
            "type": "revenue_stream",
            "description": f"{stream_data['stream']} revenue from {stream_data['star']}",
            "authority": "Revenue Crown",
            "stream": stream_data["stream"],
            "cycle": stream_data["cycle"],
            "amount": stream_data["amount"],
            "star": stream_data["star"],
            "revenue_timestamp": stream_data["timestamp"]
        }
        
        stream_result = append_entry_simple("revenue_streams.json", "streams", stream_entry)
        print(f"✅ Added {stream_data['stream']} stream: ${stream_data['amount']}")
    
    print(f"\n🏆 CONSTELLATION DATA INTEGRATION COMPLETE!")
    print(f"💰 Total Revenue: ${constellation_entry['total_amount']}")
    print(f"⭐ Revenue Streams: {constellation_entry['stream_count']}")
    print(f"🔥 Active Cycles: {', '.join(constellation_entry['cycles'])}")
    print(f"✨ Stellar Sources: {', '.join(constellation_entry['stars'])}")
    
    # Verify data was saved correctly
    saved_data = load_json_simple("constellations.json", {})
    print(f"\n📊 Verification: Loaded {len(saved_data.get('constellations', []))} constellation(s)")
    print("🌟 Constellation data is ready for Revenue Crown dashboard!")
    
    # Create revenue summary for dashboard
    revenue_summary = {
        "total_revenue": constellation_entry["total_amount"],
        "streams": {
            "Store": 300,
            "Social": 150, 
            "Website": 200
        },
        "cycles": {
            "Morning Flame": 300,
            "Twilight Flame": 150,
            "Seasonal Festival": 200
        },
        "stars": {
            "Golden Dawn": 300,
            "Evening Concord": 150,
            "Festival Radiance": 200
        },
        "last_updated": datetime.now().isoformat(),
        "period": "2025-11-07"
    }
    
    save_json_simple("revenue_summary.json", revenue_summary)
    print("✅ Created revenue summary for dashboard display")

if __name__ == "__main__":
    main()