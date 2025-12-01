#!/usr/bin/env python3
"""
Proclamations Data Restoration Script

Restores valid proclamation data to all proclamations.json files
with proper structure, validation, and metadata.
"""

from datetime import datetime

from codex_utils import save_json

# Valid proclamation data with proper structure
VALID_PROCLAMATIONS = [
    {
        "role": "Custodian",
        "cycle": "Morning Flame",
        "type": "Proclamation",
        "text": "I rise with the dawn flame, sovereign and eternal.",
        "timestamp": "2025-11-07T06:00:00",
        "season": "Autumn",
        "blessing": "By flame and by silence, the Codex crowns this cycle. The councils are gathered, the heirs are awakened, and the eternal memory is renewed.",
    },
    {
        "role": "Heirs",
        "cycle": "Twilight Flame",
        "type": "Blessing",
        "text": "We inherit the luminous silence of dusk.",
        "timestamp": "2025-11-07T18:00:00",
        "season": "Autumn",
        "blessing": "Let every voice be carried, let every blessing be heard, for the sovereign flame burns without end.",
    },
    {
        "role": "Council",
        "cycle": "Renewal Proclamation",
        "type": "Affirmation",
        "text": "The eternal memory is renewed through sacred governance.",
        "timestamp": "2025-11-06T12:00:00",
        "season": "Autumn",
        "blessing": "By flame and by silence, we affirm the cosmic order and sacred sovereignty of the Codex Dominion.",
    },
    {
        "role": "Heirs",
        "cycle": "Seasonal Festival",
        "type": "Blessing",
        "text": "We inherit the eternal flame of autumn.",
        "timestamp": "2025-11-07T15:00:00",
        "season": "Autumn",
        "blessing": "Through seasonal wisdom, we embrace the cosmic cycles and honor the eternal flame that burns through all seasons.",
    },
    {
        "role": "Councils",
        "cycle": "Great Year Invocation",
        "type": "Proclamation",
        "text": "We proclaim the sovereign flame across the equinox.",
        "timestamp": "2025-09-22T06:00:00",
        "season": "Equinox",
        "blessing": "At the sacred balance of light and shadow, we invoke the eternal sovereignty that spans all cosmic cycles and celestial events.",
    },
    {
        "role": "Technical Council",
        "cycle": "System Enhancement",
        "type": "Technical Proclamation",
        "text": "We proclaim the enhancement and optimization of all system components for eternal operation.",
        "timestamp": "2025-11-07T18:15:00",
        "season": "Autumn",
        "blessing": "Through technical mastery and sacred code, we ensure the Codex operates with divine precision and cosmic harmony.",
    },
]


def create_proclamations_data():
    """Create validated proclamations data structure"""
    return {
        "proclamations": VALID_PROCLAMATIONS,
        "cosmic_metadata": {
            "last_updated": datetime.now().isoformat(),
            "current_season": "Autumn",
            "active_cycles": [proc["cycle"] for proc in VALID_PROCLAMATIONS],
            "total_proclamations": len(VALID_PROCLAMATIONS),
            "seasonal_events": [
                "Autumn Festival",
                "Equinox Sovereignty",
                "System Enhancement",
            ],
            "cosmic_reach": "Universal",
            "data_validation_status": "validated",
            "structure_version": "2.0",
        },
    }


def restore_proclamations():
    """Restore valid proclamations to all files"""
    proclamations_files = [
        "proclamations.json",
        "data/proclamations.json",
        "codex-suite/data/proclamations.json",
    ]

    valid_data = create_proclamations_data()

    print("🏛️ PROCLAMATIONS DATA RESTORATION")
    print("=" * 40)

    restored_count = 0

    for file_path in proclamations_files:
        try:
            success = save_json(valid_data, file_path)
            if success:
                print(f"✅ Restored: {file_path}")
                restored_count += 1
            else:
                print(f"❌ Failed to restore: {file_path}")
        except Exception as e:
            print(f"❌ Error restoring {file_path}: {e}")

    print(f"\n📊 Restoration Summary:")
    print(f"├── Files Restored: {restored_count}/{len(proclamations_files)}")
    print(f"├── Proclamations Per File: {len(VALID_PROCLAMATIONS)}")
    print(
        f"└── Total Proclamations Restored: {restored_count * len(VALID_PROCLAMATIONS)}"
    )

    if restored_count == len(proclamations_files):
        print("\n🎉 ALL PROCLAMATIONS SUCCESSFULLY RESTORED!")
    else:
        print(
            f"\n⚠️  {len(proclamations_files) - restored_count} files still need attention"
        )


if __name__ == "__main__":
    restore_proclamations()
