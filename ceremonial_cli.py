#!/usr/bin/env python3
"""
🕯️ Ceremonial CLI - Sacred Inscription Interface
===============================================

Command-line interface for inscribing ceremonial entries into the eternal bulletin.
Three sacred kinds available: proclamation, silence, blessing.

Usage Examples:
  python ceremonial_cli.py proclamation "The eternal flame burns bright"
  python ceremonial_cli.py silence "In memory of all who came before"
  python ceremonial_cli.py blessing "May wisdom guide our path"
  python ceremonial_cli.py --list-recent 10
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from codex_ceremonial_inscriber import (CodexCeremonialInscriber,
                                        inscribe_ceremony)


def main():
    """Main CLI interface for ceremonial inscriptions."""
    parser = argparse.ArgumentParser(
        description="🕯️ Ceremonial CLI - Sacred Inscription Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Sacred Ceremonial Kinds:
  proclamation    Bold declarations and announcements (📢)
  silence         Moments of reflection and remembrance (🤫)
  blessing        Sacred invocations and well-wishes (🙏)

Examples:
  %(prog)s proclamation "The Codex Dominion stands eternal"
  %(prog)s silence "In honor of all who built this platform"
  %(prog)s blessing "May this system serve all who use it"
  %(prog)s --list-recent 5
  %(prog)s --list-kind blessing
        """,
    )

    # Ceremonial inscription commands
    parser.add_argument(
        "kind",
        nargs="?",
        choices=["proclamation", "silence", "blessing"],
        help="Type of ceremonial inscription",
    )
    parser.add_argument("message", nargs="?", help="Sacred message to inscribe")

    # Information commands
    parser.add_argument(
        "--list-recent",
        type=int,
        metavar="N",
        help="List N most recent ceremonial inscriptions",
    )
    parser.add_argument(
        "--list-kind",
        choices=["proclamation", "silence", "blessing"],
        help="List inscriptions of specific kind",
    )
    parser.add_argument(
        "--show-status", action="store_true", help="Show ceremonial system status"
    )

    args = parser.parse_args()

    # Initialize ceremonial inscriber
    inscriber = CodexCeremonialInscriber()

    try:
        # Handle different command types
        if args.kind and args.message:
            print(f"🕯️ Inscribing sacred {args.kind}...")
            entry = inscribe_ceremony(args.kind, args.message)

            print(f"SUCCESS: {args.kind.title()} inscribed successfully!")
            print(f"Cycle ID: {entry['cycle_id']}")
            print(f"Timestamp: {entry['timestamp']}")
            print(f"Rite: {entry['rite']}")
            print(f"Sacred Checksum: {entry['sacred_checksum']}")
            print()

            # Show the formatted proclamation
            if "proclamation" in entry:
                print("Formatted Proclamation:")
                print("-" * 40)
                print(entry["proclamation"])

        elif args.list_recent:
            print(
                f"📚 Retrieving {args.list_recent} most recent ceremonial inscriptions..."
            )

            # Check local ceremonial file
            ceremonial_file = Path("ceremonial_inscriptions_backup.json")
            if ceremonial_file.exists():
                with open(ceremonial_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                cycles = data.get("cycles", [])
                recent_cycles = cycles[-args.list_recent :] if cycles else []

                if recent_cycles:
                    print(
                        f"\n🕯️ Found {len(recent_cycles)} recent ceremonial inscriptions:"
                    )
                    print("=" * 60)

                    for cycle in recent_cycles:
                        kind_icon = {
                            "proclamation": "📢",
                            "silence": "🤫",
                            "blessing": "🙏",
                        }.get(cycle.get("kind", ""), "🕯️")

                        print(
                            f"{kind_icon} {cycle.get('cycle_id', 'unknown')}: {cycle.get('kind', 'unknown').upper()}"
                        )
                        print(f"   Time: {cycle.get('timestamp', 'unknown')[:19]}")
                        print(f"   Rite: {cycle.get('rite', 'unknown')}")
                        print(f"   Message: {cycle.get('message', 'unknown')}")
                        print(f"   Checksum: {cycle.get('sacred_checksum', 'unknown')}")
                        print("-" * 40)
                else:
                    print("📭 No ceremonial inscriptions found")
            else:
                print("📭 No ceremonial inscriptions file found")

        elif args.list_kind:
            print(f"🔍 Listing all {args.list_kind} inscriptions...")

            ceremonial_file = Path("ceremonial_inscriptions_backup.json")
            if ceremonial_file.exists():
                with open(ceremonial_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                cycles = data.get("cycles", [])
                kind_cycles = [c for c in cycles if c.get("kind") == args.list_kind]

                if kind_cycles:
                    kind_icon = {
                        "proclamation": "📢",
                        "silence": "🤫",
                        "blessing": "🙏",
                    }.get(args.list_kind, "🕯️")
                    print(
                        f"\n{kind_icon} Found {len(kind_cycles)} {args.list_kind} inscriptions:"
                    )
                    print("=" * 60)

                    for cycle in kind_cycles:
                        print(
                            f"   {cycle.get('cycle_id', 'unknown')}: {cycle.get('timestamp', 'unknown')[:19]}"
                        )
                        print(f"   Message: {cycle.get('message', 'unknown')}")
                        print("-" * 30)
                else:
                    print(f"📭 No {args.list_kind} inscriptions found")
            else:
                print("📭 No ceremonial inscriptions file found")

        elif args.show_status:
            print("🕯️ Ceremonial System Status")
            print("=" * 40)

            # Check ceremonial inscriptions file
            ceremonial_file = Path("ceremonial_inscriptions_backup.json")
            if ceremonial_file.exists():
                try:
                    with open(ceremonial_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    print(f"📂 Status: {data.get('codex_festival_status', 'UNKNOWN')}")
                    print(f"📊 Total Inscriptions: {data.get('total_ceremonies', 0)}")
                    print(f"📅 Last Inscription: {data.get('last_ceremony', 'Never')}")
                    print(f"🕐 Last Updated: {data.get('last_updated', 'Unknown')}")

                    # Count by kind
                    if data.get("cycles"):
                        kinds = {}
                        for cycle in data["cycles"]:
                            kind = cycle.get("kind", "unknown")
                            kinds[kind] = kinds.get(kind, 0) + 1

                        print("\n🎭 Inscriptions by Kind:")
                        for kind, count in kinds.items():
                            kind_icon = {
                                "proclamation": "📢",
                                "silence": "🤫",
                                "blessing": "🙏",
                            }.get(kind, "🕯️")
                            print(f"   {kind_icon} {kind}: {count}")

                except Exception as e:
                    print(f"❌ Error reading ceremonial status: {e}")
            else:
                print("📭 No ceremonial inscriptions found")

            # Check cloud connectivity
            try:
                test_inscriptions = inscriber.get_ceremonial_inscriptions(limit=1)
                if test_inscriptions:
                    print("☁️ Cloud Status: Connected")
                else:
                    print("🏠 Cloud Status: Using local backup")
            except Exception:
                print("🏠 Cloud Status: Using local backup")

        else:
            print("❓ No command specified or invalid arguments.")
            print("\nUsage:")
            print(f"  {sys.argv[0]} proclamation 'Your sacred declaration'")
            print(f"  {sys.argv[0]} silence 'Your moment of reflection'")
            print(f"  {sys.argv[0]} blessing 'Your sacred blessing'")
            print(f"  {sys.argv[0]} --list-recent 10")
            print(f"  {sys.argv[0]} --show-status")

    except Exception as e:
        print(f"❌ Error executing ceremonial command: {e}")
        sys.exit(1)

    print("\n🕯️ May the sacred inscriptions illuminate your path 🕯️")


if __name__ == "__main__":
    main()
