"""
Quick Action Script - Resolve Ritual Issues
Automated fixes for common ritual failures
"""

import json
import subprocess
from pathlib import Path
from typing import List

class RitualHealer:
    """Automatically resolve common ritual issues"""

    def __init__(self):
        self.root_dir = Path.cwd()
        self.fixes_applied = []

    def heal_all(self):
        """Apply all available fixes"""

        print("\n" + "="*70)
        print("🔧 RITUAL HEALER - AUTOMATIC ISSUE RESOLUTION")
        print("="*70 + "\n")

        # 1. Create missing capsules directory structure
        self.create_capsules_structure()

        # 2. Fix scheduled task states
        self.check_scheduled_tasks()

        # 3. Validate ledgers
        self.validate_ledgers()

        # Summary
        self.print_summary()

    def create_capsules_structure(self):
        """Create system_capsules directory with placeholders"""

        print("📦 Creating system_capsules structure...")

        capsules_dir = self.root_dir / "system_capsules"
        capsules_dir.mkdir(exist_ok=True)

        expected_capsules = {
            "signals-daily": {
                "description": "Daily market signals and analytics",
                "schedule": "0 6 * * *",  # 6 AM daily
                "enabled": True
            },
            "dawn-dispatch": {
                "description": "Dawn dispatch notifications and updates",
                "schedule": "0 5 * * *",  # 5 AM daily
                "enabled": True
            },
            "treasury-audit": {
                "description": "Treasury and financial audit checks",
                "schedule": "0 8 * * MON",  # 8 AM Mondays
                "enabled": True
            },
            "sovereignty-bulletin": {
                "description": "Sovereignty status bulletin generator",
                "schedule": "0 9 * * *",  # 9 AM daily
                "enabled": True
            },
            "education-matrix": {
                "description": "Educational content matrix updates",
                "schedule": "0 10 * * TUE,THU",  # 10 AM Tue/Thu
                "enabled": True
            }
        }

        for capsule_name, config in expected_capsules.items():
            capsule_dir = capsules_dir / capsule_name
            capsule_dir.mkdir(exist_ok=True)

            # Create config.json
            config_file = capsule_dir / "config.json"
            if not config_file.exists():
                with open(config_file, "w") as f:
                    json.dump(config, f, indent=2)
                print(f"   ✓ Created {capsule_name}/config.json")
                self.fixes_applied.append(f"Created capsule: {capsule_name}")

            # Create __init__.py
            init_file = capsule_dir / "__init__.py"
            if not init_file.exists():
                init_file.write_text(f'"""{config["description"]}"""')
                print(f"   ✓ Created {capsule_name}/__init__.py")

            # Create main.py placeholder
            main_file = capsule_dir / "main.py"
            if not main_file.exists():
                template = f'''"""
{config["description"]}
Capsule: {capsule_name}
Schedule: {config["schedule"]}
"""

import json
from pathlib import Path
from datetime import datetime

def execute():
    """Main capsule execution function"""
    print(f"Executing {capsule_name} capsule...")

    # TODO: Implement capsule logic here

    result = {{
        "capsule": "{capsule_name}",
        "executed_at": datetime.utcnow().isoformat() + "Z",
        "status": "success",
        "message": "Capsule executed successfully (placeholder)"
    }}

    return result

if __name__ == "__main__":
    result = execute()
    print(json.dumps(result, indent=2))
'''
                main_file.write_text(template)
                print(f"   ✓ Created {capsule_name}/main.py")

        print(f"\n✅ System capsules structure created!\n")

    def check_scheduled_tasks(self):
        """Check and provide guidance on scheduled task issues"""

        print("⏰ Checking scheduled tasks...")

        try:
            result = subprocess.run(
                ["powershell", "-Command",
                 "Get-ScheduledTask | Where-Object {$_.TaskName -match 'Codex'} | Select-Object TaskName,State,LastRunTime | Format-Table -AutoSize"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                print("\n" + result.stdout)

                print("💡 Task State 3 = Disabled")
                print("   To re-enable tasks:")
                print("   1. Open Task Scheduler (taskschd.msc)")
                print("   2. Find Codex-Flame tasks")
                print("   3. Right-click → Enable")
                print("   OR run: Enable-ScheduledTask -TaskName 'Codex-Flame-*'\n")
            else:
                print("   ⚠ Could not query scheduled tasks\n")

        except Exception as e:
            print(f"   ⚠ Error checking tasks: {e}\n")

    def validate_ledgers(self):
        """Validate all ledger files"""

        print("📖 Validating ledgers...")

        ledger_files = [
            "codex_ledger.json",
            "proclamations.json",
            "cycles.json",
            "accounts.json",
            "completed_archives.json"
        ]

        for ledger_name in ledger_files:
            ledger_path = self.root_dir / ledger_name

            if ledger_path.exists():
                try:
                    with open(ledger_path) as f:
                        data = json.load(f)
                    print(f"   ✓ {ledger_name} - Valid")
                except json.JSONDecodeError as e:
                    print(f"   ❌ {ledger_name} - CORRUPTED: {e}")
                    self.fixes_applied.append(f"ERROR: {ledger_name} needs manual repair")
            else:
                print(f"   ⚠ {ledger_name} - Missing")

        print()

    def print_summary(self):
        """Print fix summary"""

        print("="*70)
        print("📊 HEALING SUMMARY")
        print("="*70 + "\n")

        if self.fixes_applied:
            print(f"✅ Applied {len(self.fixes_applied)} fixes:\n")
            for i, fix in enumerate(self.fixes_applied, 1):
                print(f"{i}. {fix}")
        else:
            print("ℹ️  No automatic fixes applied")

        print("\n💡 NEXT STEPS:")
        print("   1. Run ritual_monitor.py again to verify fixes")
        print("   2. Re-enable disabled scheduled tasks in Task Scheduler")
        print("   3. Implement capsule logic in system_capsules/*/main.py")
        print("   4. Test capsule execution manually")
        print("   5. Configure GitHub Actions secrets if workflows fail")

        print("\n" + "="*70 + "\n")


def main():
    """Run ritual healer"""
    healer = RitualHealer()
    healer.heal_all()


if __name__ == "__main__":
    main()
