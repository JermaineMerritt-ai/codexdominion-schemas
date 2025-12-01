#!/usr/bin/env python3
"""
🎭 Codex Festival CLI - Sacred Ceremony Interface
================================================

Command-line interface for recording sacred proclamations and ceremonial rites.
Every command etches a new cycle into the eternal festival log.

Usage Examples:
  python festival_cli.py --proclaim "The flame burns bright" --rite "Daily Affirmation"
  python festival_cli.py --crown-flame
  python festival_cli.py --daily-dispatch "Markets show strength, sovereignty grows"
  python festival_cli.py --list-recent 5
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from codex_festival_proclamation import CodexFestivalKeeper


def main():
    """Main CLI interface for festival proclamations."""
    parser = argparse.ArgumentParser(
        description="🎭 Codex Festival CLI - Sacred Ceremony Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --proclaim "The flame burns eternal" --rite "Morning Affirmation"
  %(prog)s --crown-flame
  %(prog)s --daily-dispatch "Market signals are strong today"
  %(prog)s --capsule-complete signals-daily 3
  %(prog)s --list-recent 10
        """,
    )

    # Proclamation commands
    parser.add_argument("--proclaim", help="Sacred proclamation text")
    parser.add_argument("--rite", help="Ceremonial rite name")
    parser.add_argument(
        "--ceremony-type", default="sacred_cycle", help="Type of ceremony"
    )

    # Special ceremonies
    parser.add_argument(
        "--crown-flame", action="store_true", help="Perform flame crowning ceremony"
    )
    parser.add_argument("--daily-dispatch", help="Record daily dispatch proclamation")
    parser.add_argument(
        "--capsule-complete",
        nargs=2,
        metavar=("CAPSULE", "ARTIFACTS"),
        help="Record capsule completion (capsule_name artifact_count)",
    )

    # Information commands
    parser.add_argument(
        "--list-recent",
        type=int,
        metavar="N",
        help="List N most recent festival cycles",
    )
    parser.add_argument(
        "--show-status", action="store_true", help="Show festival system status"
    )

    args = parser.parse_args()

    # Initialize festival keeper
    keeper = CodexFestivalKeeper()

    try:
        # Handle different command types
        if args.crown_flame:
            print("🔥 Performing Sacred Flame Crowning Ceremony...")
            cycle = keeper.proclaim_flame_crowning()
            print(f"👑 Crowning recorded: {cycle['cycle_id']}")
            print(f"📅 Timestamp: {cycle['timestamp']}")

        elif args.daily_dispatch:
            print("📰 Recording Daily Dispatch...")
            cycle = keeper.proclaim_daily_dispatch(args.daily_dispatch)
            print(f"📋 Dispatch recorded: {cycle['cycle_id']}")
            print(f"📅 Timestamp: {cycle['timestamp']}")

        elif args.capsule_complete:
            capsule_name, artifact_count = args.capsule_complete
            print(f"⚡ Recording Capsule Completion: {capsule_name}")
            cycle = keeper.proclaim_capsule_completion(
                capsule_name, int(artifact_count)
            )
            print(f"🎯 Completion recorded: {cycle['cycle_id']}")
            print(f"📅 Timestamp: {cycle['timestamp']}")

        elif args.proclaim and args.rite:
            print("🎭 Recording Sacred Proclamation...")
            cycle = keeper.append_festival_proclamation(
                args.proclaim, args.rite, args.ceremony_type
            )
            print(f"📜 Proclamation recorded: {cycle['cycle_id']}")
            print(f"📅 Timestamp: {cycle['timestamp']}")
            print(f"🔒 Sacred checksum: {cycle['sacred_checksum']}")

        elif args.list_recent:
            print(f"📚 Retrieving {args.list_recent} most recent festival cycles...")
            cycles = keeper.get_recent_festivals(args.list_recent)

            if cycles:
                print(f"\n🎊 Found {len(cycles)} recent cycles:")
                print("=" * 60)

                for cycle in cycles:
                    print(f"🆔 Cycle: {cycle.get('cycle_id', 'unknown')}")
                    print(f"📅 Time: {cycle.get('timestamp', 'unknown')}")
                    print(f"🎭 Type: {cycle.get('ceremony_type', 'unknown')}")
                    print(f"🔥 Status: {cycle.get('flame_status', 'unknown')}")
                    print(f"📝 Rite: {cycle.get('rite', 'unknown')}")

                    # Show first 100 chars of proclamation
                    proclamation = cycle.get("proclamation", "")
                    if len(proclamation) > 100:
                        print(f"📜 Proclamation: {proclamation[:100]}...")
                    else:
                        print(f"📜 Proclamation: {proclamation}")

                    print("-" * 40)
            else:
                print("📭 No recent cycles found")

        elif args.show_status:
            print("🎭 Festival System Status")
            print("=" * 40)

            # Check local backup file
            local_file = Path("festival_local_backup.json")
            if local_file.exists():
                try:
                    with open(local_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    print(
                        f"📂 Local Status: {data.get('codex_festival_status', 'UNKNOWN')}"
                    )
                    print(f"📊 Total Ceremonies: {data.get('total_ceremonies', 0)}")
                    print(f"📅 Last Ceremony: {data.get('last_ceremony', 'Never')}")
                    print(f"🕐 Last Updated: {data.get('last_updated', 'Unknown')}")

                    if data.get("cycles"):
                        latest = data["cycles"][-1]
                        print(f"🎯 Latest Cycle: {latest.get('cycle_id', 'unknown')}")
                        print(
                            f"🎭 Latest Type: {latest.get('ceremony_type', 'unknown')}"
                        )

                except Exception as e:
                    print(f"❌ Error reading local status: {e}")
            else:
                print("📭 No local festival data found")

            # Check cloud connectivity
            try:
                recent = keeper.get_recent_festivals(1)
                print("☁️ Cloud Status: Connected")
            except Exception:
                print("🏠 Cloud Status: Using local backup")

        else:
            print("❓ No command specified. Use --help for usage information.")
            parser.print_help()

    except Exception as e:
        print(f"❌ Error executing command: {e}")
        sys.exit(1)

    print("\n🌟 May the eternal flame guide your path 🌟")


if __name__ == "__main__":
    main()
