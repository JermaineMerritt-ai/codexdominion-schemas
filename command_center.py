#!/usr/bin/env python3
"""
👑 CODEX DOMINION COMMAND CENTER
Interactive dashboard for monitoring and controlling the Digital Empire
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path


class CodexCommandCenter:
    """Command center for the Digital Empire."""

    def __init__(self):
        self.workspace_root = Path(__file__).parent
        self.load_empire_data()

    def load_empire_data(self):
        """Load empire data from configuration files."""
        try:
            # Load app configuration
            app_config_path = self.workspace_root / "config" / "app.config.json"
            if app_config_path.exists():
                with open(app_config_path, "r") as f:
                    self.app_config = json.load(f)
            else:
                self.app_config = {
                    "app": {"name": "Codex Dominion", "version": "1.0.0"}
                }

            # Load cycles data
            cycles_path = self.workspace_root / "cycles.json"
            if cycles_path.exists():
                with open(cycles_path, "r") as f:
                    self.cycles_data = json.load(f)
            else:
                self.cycles_data = []

            # Load ledger data
            ledger_path = self.workspace_root / "ledger.json"
            if ledger_path.exists():
                with open(ledger_path, "r") as f:
                    self.ledger_data = json.load(f)
            else:
                self.ledger_data = []

            # Load heartbeat data
            heartbeat_path = self.workspace_root / "heartbeat.json"
            if heartbeat_path.exists():
                with open(heartbeat_path, "r") as f:
                    heartbeat_raw = json.load(f)
                    # Handle both array and object formats
                    if isinstance(heartbeat_raw, list) and heartbeat_raw:
                        self.heartbeat_data = heartbeat_raw[0]  # Get latest heartbeat
                    elif isinstance(heartbeat_raw, dict):
                        self.heartbeat_data = heartbeat_raw
                    else:
                        self.heartbeat_data = {
                            "status": "SUPREME",
                            "timestamp": datetime.now().isoformat(),
                        }
            else:
                self.heartbeat_data = {
                    "status": "SUPREME",
                    "timestamp": datetime.now().isoformat(),
                }

        except Exception as e:
            print(f"⚠️ Warning: Could not load some empire data: {e}")

    def display_header(self):
        """Display dashboard header."""
        print("=" * 80)
        print("👑 CODEX DOMINION - DIGITAL EMPIRE COMMAND CENTER")
        print("=" * 80)
        print(
            f"🏛️ Empire: {self.app_config.get('app', {}).get('name', 'Codex Dominion')}"
        )
        print(f"📦 Version: {self.app_config.get('app', {}).get('version', '1.0.0')}")
        print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⚡ Status: {self.heartbeat_data.get('status', 'SUPREME')}")
        print("=" * 80)

    def display_empire_overview(self):
        """Display empire overview."""
        print("\n🌟 EMPIRE OVERVIEW")
        print("-" * 40)

        features = self.app_config.get("features", {})
        active_count = sum(1 for v in features.values() if v)

        print(
            f"🎬 Video Studio Omega: {'✅ ACTIVE' if features.get('video_studio_omega') else '❌ INACTIVE'}"
        )
        print(
            f"🚀 Lovable Destroyer: {'✅ ACTIVE' if features.get('lovable_destroyer') else '❌ INACTIVE'}"
        )
        print(
            f"🔄 Codex Flow Engine: {'✅ ACTIVE' if features.get('codex_flow_engine') else '❌ INACTIVE'}"
        )
        print(
            f"🌐 IONOS Dominion: {'✅ ACTIVE' if features.get('ionos_dominion_manager') else '❌ INACTIVE'}"
        )
        print(
            f"🍌 Nano Banana Destroyer: {'✅ ACTIVE' if features.get('nano_banana_destroyer') else '❌ INACTIVE'}"
        )
        print(
            f"💾 NotebookLLM Destroyer: {'✅ ACTIVE' if features.get('notebookllm_destroyer') else '❌ INACTIVE'}"
        )

        print(f"\n📊 Total Active Systems: {active_count}/{len(features)}")

        if active_count == len(features):
            print("🏆 SUPREME EMPIRE STATUS: ALL SYSTEMS OPERATIONAL!")
        elif active_count >= len(features) * 0.8:
            print("🔥 DOMINANT EMPIRE STATUS: NEARLY COMPLETE!")
        else:
            print("⚡ GROWING EMPIRE STATUS: SYSTEMS ACTIVATING!")

    def display_recent_achievements(self):
        """Display recent empire achievements."""
        print("\n📖 RECENT ACHIEVEMENTS")
        print("-" * 40)

        if self.ledger_data:
            # Show last 5 achievements
            recent = (
                self.ledger_data[-5:] if len(self.ledger_data) > 5 else self.ledger_data
            )

            for i, achievement in enumerate(reversed(recent), 1):
                print(f"{i}. {achievement.get('entry', 'Unknown achievement')}")
                print(
                    f"   📅 {achievement.get('date', 'Unknown date')} | 👤 {achievement.get('custodian', 'Unknown custodian')}"
                )
                print()
        else:
            print(
                "📋 No achievements recorded yet. Start deploying systems to see achievements!"
            )

    def display_system_cycles(self):
        """Display system cycles information."""
        print("\n🔄 SYSTEM CYCLES")
        print("-" * 40)

        if self.cycles_data:
            current_date = datetime.now().strftime("%Y-%m-%d")
            current_cycle = None

            # Find current cycle
            for cycle in self.cycles_data:
                if cycle["date"] <= current_date:
                    current_cycle = cycle

            if current_cycle:
                print(f"🌟 Current Cycle: {current_cycle['cycle']}")
                print(f"🌸 Season: {current_cycle['season']}")
                print(f"📅 Date: {current_cycle['date']}")

            print("\nAll Cycles:")
            for cycle in self.cycles_data:
                marker = "👑" if cycle == current_cycle else "📅"
                print(
                    f"{marker} {cycle['season']} - {cycle['cycle']} ({cycle['date']})"
                )
        else:
            print("🔄 No cycle data found.")

    def display_quick_actions(self):
        """Display available quick actions."""
        print("\n⚡ QUICK ACTIONS")
        print("-" * 40)
        print("1. 🎬 Launch Video Studio Omega")
        print("2. 🚀 Deploy Lovable Destroyer")
        print("3. 🔄 Activate Flow Engine")
        print("4. 🌐 Manage IONOS Empire")
        print("5. 📊 Generate Empire Report")
        print("6. 🔐 Check SSL Status")
        print("7. 📋 View System Files Status")
        print("8. 🖥️ Launch Streamlit Dashboard")
        print("9. 🌀 Launch Codex Eternum Omega Dashboard")
        print("10. 🔄 Refresh Data")
        print("0. 🚪 Exit")

    def execute_action(self, action: str):
        """Execute selected action."""
        if action == "1":
            print("🎬 Launching Video Studio Omega...")
            os.system("python codex-integration\\video_studio_omega.py")

        elif action == "2":
            print("🚀 Deploying Lovable Destroyer...")
            os.system("python codex-integration\\lovable_destroyer.py")

        elif action == "3":
            print("🔄 Activating Codex Flow Engine...")
            os.system("python codex-integration\\codex_flow_engine.py")

        elif action == "4":
            print("🌐 Managing IONOS Empire...")
            os.system("python codex-integration\\ionos_dominion_manager.py")

        elif action == "5":
            print("📊 Generating Empire Report...")
            os.system("python EMPIRE_STATUS_REPORT.py")

        elif action == "6":
            print("🔐 Checking SSL Status...")
            os.system("python codex-integration\\ssl_flame_check.py")

        elif action == "7":
            print("📋 Viewing System Files Status...")
            os.system("python codex-integration\\system_files_status_report.py")

        elif action == "8":
            print("🖥️ Launching Streamlit Dashboard...")
            print("📦 Installing dashboard dependencies if needed...")
            os.system("python launch_dashboard.py")

        elif action == "9":
            print("🌀 Launching Codex Eternum Omega Dashboard...")
            print("🔱 Activating Sovereign Control Interface...")
            os.system("python launch_omega_dashboard.py")

        elif action == "10":
            print("🔄 Refreshing empire data...")
            self.load_empire_data()
            print("✅ Empire data refreshed!")

        else:
            print("❌ Invalid action. Please try again.")

    def run_interactive_mode(self):
        """Run interactive command center."""
        while True:
            self.display_header()
            self.display_empire_overview()
            self.display_recent_achievements()
            self.display_system_cycles()
            self.display_quick_actions()

            print("\n" + "=" * 80)
            action = input("🎯 Select action (0-10): ").strip()

            if action == "0":
                print("\n👑 Exiting Command Center. Empire remains supreme!")
                break

            print("\n" + "=" * 80)
            self.execute_action(action)

            input("\n⏸️ Press Enter to continue...")
            print("\n" * 2)  # Clear screen space

    def run_status_mode(self):
        """Run one-time status display."""
        self.display_header()
        self.display_empire_overview()
        self.display_recent_achievements()
        self.display_system_cycles()
        print("\n" + "=" * 80)
        print(
            "👑 Empire status displayed. For interactive mode, run without arguments."
        )


def main():
    """Main command center function."""
    command_center = CodexCommandCenter()

    # Check if running in status-only mode
    if len(sys.argv) > 1 and sys.argv[1] == "--status":
        command_center.run_status_mode()
    else:
        command_center.run_interactive_mode()


if __name__ == "__main__":
    main()
