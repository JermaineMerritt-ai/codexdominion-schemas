#!/usr/bin/env python3
"""
Codex Suite Launcher
====================

Unified launcher for all Codex Dominion Suite applications.
"""

import os
import subprocess
import sys
from pathlib import Path


def main():
    print("👑 CODEX DOMINION SUITE LAUNCHER")
    print("=" * 50)
    print()

    # Get suite root directory
    suite_root = Path(__file__).parent

    print("Available Applications:")
    print()
    print("1. 🏛️  Dashboard - Unified control interface")
    print("2. 🌐  API Server - REST API interface")
    print("3. 🔧  Settings - Configuration management")
    print("4. ✨  Spark Studio - AI content generation")
    print("5. 📊  System Status - Health check")
    print("6. 🚪  Exit")
    print()

    while True:
        try:
            choice = input("Select application (1-6): ").strip()

            if choice == "1":
                print("🚀 Launching Codex Dashboard...")
                dashboard_path = suite_root / "apps" / "dashboard"
                os.chdir(dashboard_path)
                subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "streamlit",
                        "run",
                        "codex_dashboard.py",
                        "--server.port",
                        "8530",
                    ]
                )

            elif choice == "2":
                print("🚀 Launching API Server...")
                api_path = suite_root / "apps" / "api"
                os.chdir(api_path)
                subprocess.run([sys.executable, "main.py"])

            elif choice == "3":
                print("🔧 Loading Configuration Settings...")
                os.chdir(suite_root)
                subprocess.run([sys.executable, "core/settings.py"])

            elif choice == "4":
                print("✨ Testing Spark Studio...")
                os.chdir(suite_root)
                subprocess.run(
                    [
                        sys.executable,
                        "-c",
                        "from modules.spark_studio import spark_studio; "
                        "result = spark_studio.generate_content('documentation', 'Test content generation'); "
                        "print('Generated:', result['content'][:200] + '...')",
                    ]
                )

            elif choice == "5":
                print("📊 System Status Check...")
                os.chdir(suite_root)
                subprocess.run(
                    [
                        sys.executable,
                        "-c",
                        "from core.settings import CODEX_CONFIG; "
                        "from core.ledger import codex_ledger; "
                        "from core.memory import codex_memory; "
                        "print('✅ System:', CODEX_CONFIG['system']['name']); "
                        "print('✅ Version:', CODEX_CONFIG['system']['version']); "
                        "stats = codex_ledger.get_statistics(); "
                        "analytics = codex_memory.get_memory_analytics(); "
                        "print(f'✅ Ledger Entries: {stats[\"total_entries\"]}'); "
                        "print(f'✅ Memories: {analytics[\"total_memories\"]}');",
                    ]
                )

            elif choice == "6":
                print("👑 May the Codex flame guide your digital sovereignty!")
                break

            else:
                print("❌ Invalid choice. Please select 1-6.")

            print("\n" + "=" * 50 + "\n")

        except KeyboardInterrupt:
            print("\n\n👑 Codex Suite Launcher terminated.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
