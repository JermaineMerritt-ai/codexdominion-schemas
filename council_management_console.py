#!/usr/bin/env python3
# 🏛️⚡🎯 INTERACTIVE CEREMONIAL COUNCIL MANAGEMENT 🎯⚡🏛️
# Real-time Council Entry & Chronicle Management for Codex Dominion
# Date: November 9, 2025

import os
import sys
from pathlib import Path

# Add the current directory to the path to import the archival system
sys.path.append(str(Path(__file__).parent))

try:
    from ceremonial_council_archival import (COUNCIL_FILE,
                                             append_council_entry,
                                             display_council_chronicle,
                                             get_council_entries,
                                             load_sacred_archive)
except ImportError:
    print("❌ Error: Could not import ceremonial_council_archival module")
    print("   Ensure ceremonial_council_archival.py is in the same directory")
    sys.exit(1)


def display_menu():
    """Display the ceremonial council management menu"""
    print("\n🏛️📜✨ CEREMONIAL COUNCIL MANAGEMENT CONSOLE ✨📜🏛️")
    print("=" * 60)
    print("1. 📋 Add New Council Entry")
    print("2. 📜 Display Full Chronicle")
    print("3. 🔍 Search Council Entries")
    print("4. 📊 Council Statistics")
    print("5. 🎯 Quick Proclamation")
    print("6. 🌟 Quick Blessing")
    print("7. ⚡ Quick Affirmation")
    print("8. 🔄 Recent Entries (Last 5)")
    print("9. 🚪 Exit")
    print("=" * 60)


def add_council_entry_interactive():
    """Interactive council entry creation"""
    print("\n📋 CREATING NEW CEREMONIAL COUNCIL ENTRY")
    print("-" * 45)

    # Entry type selection
    print("📜 Available Entry Types:")
    entry_types = [
        "Proclamation",
        "Affirmation",
        "Blessing",
        "Silence",
        "Inscription",
        "Declaration",
    ]
    for i, etype in enumerate(entry_types, 1):
        print(f"   {i}. {etype}")

    while True:
        try:
            type_choice = int(input("\nSelect entry type (1-6): "))
            if 1 <= type_choice <= len(entry_types):
                entry_type = entry_types[type_choice - 1]
                break
            else:
                print("❌ Invalid choice. Please select 1-6.")
        except ValueError:
            print("❌ Please enter a valid number.")

    # Author selection/input
    print("\n👑 Council Authorities:")
    councils = [
        "Council of Radiance",
        "Cosmic Council",
        "Succession Council",
        "Operational Council",
        "Ceremonial Council",
        "Custom Council",
    ]

    for i, council in enumerate(councils, 1):
        print(f"   {i}. {council}")

    while True:
        try:
            author_choice = int(input("\nSelect council authority (1-6): "))
            if 1 <= author_choice <= len(councils):
                if author_choice == len(councils):  # Custom Council
                    author = input("Enter custom council name: ").strip()
                    if not author:
                        print("❌ Council name cannot be empty.")
                        continue
                else:
                    author = councils[author_choice - 1]
                break
            else:
                print("❌ Invalid choice. Please select 1-6.")
        except ValueError:
            print("❌ Please enter a valid number.")

    # Message input
    print(f"\n💬 Enter {entry_type} message:")
    message = input("Message: ").strip()
    if not message:
        print("❌ Message cannot be empty.")
        return

    # Optional ceremonial metadata
    print("\n✨ Add ceremonial metadata? (y/n): ", end="")
    add_metadata = input().lower().startswith("y")

    ceremonial_metadata = {}
    if add_metadata:
        ceremony_type = input("Ceremony type (optional): ").strip()
        if ceremony_type:
            ceremonial_metadata["ceremony_type"] = ceremony_type.upper().replace(
                " ", "_"
            )

        cosmic_scope = input("Cosmic scope (optional): ").strip()
        if cosmic_scope:
            ceremonial_metadata["cosmic_scope"] = cosmic_scope.upper().replace(" ", "_")

    # Create the entry
    try:
        entry = append_council_entry(
            entry_type,
            author,
            message,
            ceremonial_metadata if ceremonial_metadata else None,
        )
        print(f"\n✅ Council entry created successfully!")
        print(f"   🆔 Archive ID: {entry['ceremonial_metadata']['archive_id']}")
    except Exception as e:
        print(f"\n❌ Error creating council entry: {e}")


def search_council_entries():
    """Search and filter council entries"""
    print("\n🔍 SEARCH COUNCIL ENTRIES")
    print("-" * 30)

    print("Search options:")
    print("1. By Entry Type")
    print("2. By Author/Council")
    print("3. By Date")
    print("4. Show All Entries")

    choice = input("Select search option (1-4): ").strip()

    try:
        if choice == "1":
            entry_type = input(
                "Enter entry type (Proclamation, Affirmation, etc.): "
            ).strip()
            entries = get_council_entries(entry_type=entry_type)
        elif choice == "2":
            author = input("Enter council/author name: ").strip()
            entries = get_council_entries(author=author)
        elif choice == "3":
            date = input("Enter date (YYYY-MM-DD): ").strip()
            entries = get_council_entries(date=date)
        elif choice == "4":
            entries = get_council_entries()
        else:
            print("❌ Invalid choice.")
            return

        if entries:
            print(f"\n📜 Found {len(entries)} entries:")
            print("-" * 40)
            for i, entry in enumerate(entries, 1):
                print(f"Entry {i}:")
                print(f"  📜 Type: {entry.get('type')}")
                print(f"  👑 Author: {entry.get('author')}")
                print(f"  📅 Date: {entry.get('date')}")
                print(f"  💬 Message: {entry.get('message')[:100]}...")
                print("-" * 40)
        else:
            print("📭 No entries found matching your criteria.")

    except Exception as e:
        print(f"❌ Search error: {e}")


def show_council_statistics():
    """Display council entry statistics"""
    print("\n📊 COUNCIL STATISTICS")
    print("-" * 25)

    try:
        entries = get_council_entries()

        if not entries:
            print("📭 No council entries found.")
            return

        # Basic stats
        total_entries = len(entries)
        print(f"📋 Total Entries: {total_entries}")

        # Entry type breakdown
        type_counts = {}
        author_counts = {}

        for entry in entries:
            entry_type = entry.get("type", "Unknown")
            author = entry.get("author", "Unknown")

            type_counts[entry_type] = type_counts.get(entry_type, 0) + 1
            author_counts[author] = author_counts.get(author, 0) + 1

        print("\n📜 Entry Types:")
        for entry_type, count in type_counts.items():
            print(f"   {entry_type}: {count}")

        print("\n👑 Council Authorities:")
        for author, count in author_counts.items():
            print(f"   {author}: {count}")

        # Recent activity
        recent_entries = entries[-3:] if len(entries) >= 3 else entries
        print(f"\n⏰ Recent Activity ({len(recent_entries)} entries):")
        for entry in recent_entries:
            print(
                f"   📅 {entry.get('date')} - {entry.get('type')} by {entry.get('author')}"
            )

    except Exception as e:
        print(f"❌ Statistics error: {e}")


def quick_entry(entry_type, default_author):
    """Create a quick entry with minimal input"""
    print(f"\n⚡ QUICK {entry_type.upper()}")
    print("-" * (len(entry_type) + 10))

    message = input(f"Enter {entry_type.lower()} message: ").strip()
    if not message:
        print("❌ Message cannot be empty.")
        return

    try:
        entry = append_council_entry(entry_type, default_author, message)
        print(f"✅ {entry_type} created successfully!")
        print(f"   🆔 Archive ID: {entry['ceremonial_metadata']['archive_id']}")
    except Exception as e:
        print(f"❌ Error creating {entry_type.lower()}: {e}")


def show_recent_entries():
    """Show the last 5 council entries"""
    print("\n🔄 RECENT COUNCIL ENTRIES (Last 5)")
    print("-" * 35)

    try:
        entries = get_council_entries()
        recent_entries = entries[-5:] if len(entries) >= 5 else entries

        if not recent_entries:
            print("📭 No recent entries found.")
            return

        for i, entry in enumerate(reversed(recent_entries), 1):
            print(f"📋 Entry {i}:")
            print(f"   📜 Type: {entry.get('type')}")
            print(f"   👑 Author: {entry.get('author')}")
            print(f"   📅 Date: {entry.get('date')}")
            print(f"   💬 Message: {entry.get('message')}")
            print("-" * 30)

    except Exception as e:
        print(f"❌ Error loading recent entries: {e}")


def main():
    """Main interactive console loop"""
    print("🏛️✨ CEREMONIAL COUNCIL MANAGEMENT CONSOLE ✨🏛️")
    print("Sacred Council Entry Management System Activated")

    while True:
        display_menu()
        choice = input("Select option (1-9): ").strip()

        try:
            if choice == "1":
                add_council_entry_interactive()
            elif choice == "2":
                display_council_chronicle()
            elif choice == "3":
                search_council_entries()
            elif choice == "4":
                show_council_statistics()
            elif choice == "5":
                quick_entry("Proclamation", "Council of Radiance")
            elif choice == "6":
                quick_entry("Blessing", "Succession Council")
            elif choice == "7":
                quick_entry("Affirmation", "Cosmic Council")
            elif choice == "8":
                show_recent_entries()
            elif choice == "9":
                print("\n🏛️✨ May the eternal flame guide your path! ✨🏛️")
                print("Sacred council management console closed.")
                break
            else:
                print("❌ Invalid choice. Please select 1-9.")

        except KeyboardInterrupt:
            print("\n\n🏛️✨ Sacred council session interrupted. Farewell! ✨🏛️")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
