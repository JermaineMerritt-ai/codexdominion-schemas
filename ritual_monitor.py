"""
Sovereign Bridge - Active Rituals Monitor
Orchestration & Automation Engine
Checks all automated processes, workflows, and scheduled tasks
"""

import json
import subprocess
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
import sys

class RitualMonitor:
    """Monitor all active rituals (automated processes) in Codex Dominion"""

    def __init__(self):
        self.timestamp = datetime.utcnow().isoformat() + "Z"
        self.root_dir = Path.cwd()
        self.results = {
            "timestamp": self.timestamp,
            "realm": "Sovereign-Bridge",
            "engines": ["orchestration", "automation"],
            "rituals": {},
            "failures": [],
            "warnings": [],
            "summary": {}
        }

    def check_all_rituals(self) -> Dict[str, Any]:
        """Check all ritual categories"""

        print("\n" + "="*70)
        print("🔮 SOVEREIGN BRIDGE - ACTIVE RITUALS MONITOR")
        print("="*70 + "\n")

        # 1. GitHub Actions Workflows
        print("📋 Checking GitHub Actions Workflows...")
        self.check_github_workflows()

        # 2. Systemd Services (if on Linux)
        print("\n🔧 Checking System Services...")
        self.check_system_services()

        # 3. Docker Containers
        print("\n🐋 Checking Docker Containers...")
        self.check_docker_containers()

        # 4. Scheduled Capsules
        print("\n🎯 Checking Scheduled Capsules...")
        self.check_scheduled_capsules()

        # 5. Ledger Integrity
        print("\n📖 Checking Ledger Integrity...")
        self.check_ledger_integrity()

        # 6. Background Processes
        print("\n⚙️  Checking Background Processes...")
        self.check_background_processes()

        # 7. Cron Jobs / Task Scheduler
        print("\n⏰ Checking Scheduled Tasks...")
        self.check_scheduled_tasks()

        # Generate summary
        self.generate_summary()

        return self.results

    def check_github_workflows(self):
        """Check GitHub Actions workflow status"""

        workflows_dir = self.root_dir / ".github" / "workflows"

        if not workflows_dir.exists():
            self.add_warning("GitHub workflows directory not found")
            return

        workflow_files = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))

        ritual = {
            "name": "GitHub Actions Workflows",
            "type": "CI/CD",
            "status": "active",
            "total_workflows": len(workflow_files),
            "workflows": []
        }

        critical_workflows = [
            "deploy-complete-frontend.yml",
            "deploy-backend.yml",
            "backend-deploy.yml",
            "frontend-deploy.yml",
            "ci-cd.yml"
        ]

        for workflow_file in workflow_files:
            workflow_name = workflow_file.name
            is_critical = workflow_name in critical_workflows

            # Check if workflow has run recently (would need GitHub API for real status)
            workflow_info = {
                "name": workflow_name,
                "path": str(workflow_file.relative_to(self.root_dir)),
                "critical": is_critical,
                "size_kb": round(workflow_file.stat().st_size / 1024, 2)
            }

            ritual["workflows"].append(workflow_info)

        # Check for common issues
        if len(workflow_files) > 40:
            self.add_warning(f"Large number of workflows detected ({len(workflow_files)}). Consider consolidation.")

        self.results["rituals"]["github_workflows"] = ritual
        print(f"   ✓ Found {len(workflow_files)} workflow files")

    def check_system_services(self):
        """Check systemd services and timers"""

        ritual = {
            "name": "System Services",
            "type": "Daemon",
            "status": "checking",
            "services": []
        }

        # List of expected Codex services
        expected_services = [
            "codex-dashboard",
            "codex-dashboard-production",
            "codexdominion-api",
            "festival-transmission",
            "festival-scroll"
        ]

        # Check for .service files in repo
        service_files = list(self.root_dir.glob("*.service"))
        timer_files = list(self.root_dir.glob("*.timer"))

        for service_file in service_files:
            service_name = service_file.stem
            service_info = {
                "name": service_name,
                "file": str(service_file.relative_to(self.root_dir)),
                "type": "service",
                "status": "defined"
            }

            # Try to check if service is running (Linux only)
            if sys.platform == "linux":
                try:
                    result = subprocess.run(
                        ["systemctl", "is-active", service_name],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    service_info["status"] = result.stdout.strip()

                    if result.returncode != 0:
                        self.add_failure(f"Service '{service_name}' is not active")
                except Exception as e:
                    service_info["status"] = "unknown"
            else:
                service_info["platform_note"] = "systemctl check skipped (not Linux)"

            ritual["services"].append(service_info)

        for timer_file in timer_files:
            timer_name = timer_file.stem
            timer_info = {
                "name": timer_name,
                "file": str(timer_file.relative_to(self.root_dir)),
                "type": "timer",
                "status": "defined"
            }
            ritual["services"].append(timer_info)

        ritual["status"] = "active" if not any(s.get("status") == "inactive" for s in ritual["services"]) else "degraded"

        self.results["rituals"]["system_services"] = ritual
        print(f"   ✓ Found {len(service_files)} services, {len(timer_files)} timers")

    def check_docker_containers(self):
        """Check Docker container health"""

        ritual = {
            "name": "Docker Containers",
            "type": "Containerized Services",
            "status": "checking",
            "containers": []
        }

        try:
            # Check if Docker is available
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}\t{{.Status}}\t{{.State}}"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")

                for line in lines:
                    if line:
                        parts = line.split("\t")
                        if len(parts) >= 3:
                            container_info = {
                                "name": parts[0],
                                "status": parts[1],
                                "state": parts[2]
                            }

                            if parts[2] != "running":
                                self.add_failure(f"Container '{parts[0]}' is not running (state: {parts[2]})")

                            ritual["containers"].append(container_info)

                ritual["status"] = "active" if all(c["state"] == "running" for c in ritual["containers"]) else "degraded"
                print(f"   ✓ Found {len(ritual['containers'])} containers")
            else:
                ritual["status"] = "docker_unavailable"
                self.add_warning("Docker is not running or not accessible")
                print(f"   ⚠ Docker not accessible")

        except FileNotFoundError:
            ritual["status"] = "not_installed"
            self.add_warning("Docker command not found")
            print(f"   ⚠ Docker not installed")
        except Exception as e:
            ritual["status"] = "error"
            ritual["error"] = str(e)
            self.add_warning(f"Error checking Docker: {e}")
            print(f"   ⚠ Error: {e}")

        self.results["rituals"]["docker_containers"] = ritual

    def check_scheduled_capsules(self):
        """Check system_capsules and their schedules"""

        capsules_dir = self.root_dir / "system_capsules"

        ritual = {
            "name": "Scheduled Capsules",
            "type": "Autonomous Agents",
            "status": "active",
            "capsules": []
        }

        if not capsules_dir.exists():
            self.add_warning("system_capsules directory not found")
            self.results["rituals"]["scheduled_capsules"] = ritual
            return

        expected_capsules = [
            "signals-daily",
            "dawn-dispatch",
            "treasury-audit",
            "sovereignty-bulletin",
            "education-matrix"
        ]

        for capsule_name in expected_capsules:
            capsule_path = capsules_dir / capsule_name

            capsule_info = {
                "name": capsule_name,
                "status": "exists" if capsule_path.exists() else "missing"
            }

            if capsule_path.exists():
                # Check for config file
                config_file = capsule_path / "config.json"
                if config_file.exists():
                    try:
                        with open(config_file) as f:
                            config = json.load(f)
                            capsule_info["schedule"] = config.get("schedule", "not_defined")
                            capsule_info["enabled"] = config.get("enabled", False)
                    except Exception as e:
                        capsule_info["config_error"] = str(e)
            else:
                self.add_warning(f"Expected capsule '{capsule_name}' not found")

            ritual["capsules"].append(capsule_info)

        ritual["status"] = "active" if all(c["status"] == "exists" for c in ritual["capsules"]) else "degraded"

        self.results["rituals"]["scheduled_capsules"] = ritual
        print(f"   ✓ Checked {len(expected_capsules)} expected capsules")

    def check_ledger_integrity(self):
        """Check ledger files for corruption or issues"""

        ritual = {
            "name": "Ledger Integrity",
            "type": "Data Integrity",
            "status": "checking",
            "ledgers": []
        }

        ledger_files = [
            "codex_ledger.json",
            "proclamations.json",
            "cycles.json",
            "accounts.json",
            "completed_archives.json"
        ]

        for ledger_name in ledger_files:
            ledger_path = self.root_dir / ledger_name

            ledger_info = {
                "name": ledger_name,
                "exists": ledger_path.exists()
            }

            if ledger_path.exists():
                try:
                    with open(ledger_path) as f:
                        data = json.load(f)

                    ledger_info["status"] = "valid"
                    ledger_info["size_kb"] = round(ledger_path.stat().st_size / 1024, 2)

                    # Check last_updated timestamp
                    if isinstance(data, dict) and "meta" in data:
                        last_updated = data["meta"].get("last_updated")
                        if last_updated:
                            ledger_info["last_updated"] = last_updated

                            # Check if stale (no updates in 7 days)
                            try:
                                update_time = datetime.fromisoformat(last_updated.replace("Z", "+00:00"))
                                age_days = (datetime.now(update_time.tzinfo) - update_time).days

                                if age_days > 7:
                                    self.add_warning(f"Ledger '{ledger_name}' hasn't been updated in {age_days} days")

                                ledger_info["age_days"] = age_days
                            except:
                                pass

                except json.JSONDecodeError as e:
                    ledger_info["status"] = "corrupted"
                    ledger_info["error"] = str(e)
                    self.add_failure(f"Ledger '{ledger_name}' is corrupted: {e}")
                except Exception as e:
                    ledger_info["status"] = "error"
                    ledger_info["error"] = str(e)
            else:
                ledger_info["status"] = "missing"
                if ledger_name == "codex_ledger.json":
                    self.add_failure(f"Critical ledger '{ledger_name}' is missing")
                else:
                    self.add_warning(f"Ledger '{ledger_name}' is missing")

            ritual["ledgers"].append(ledger_info)

        ritual["status"] = "healthy" if all(l.get("status") == "valid" for l in ritual["ledgers"] if l["exists"]) else "degraded"

        self.results["rituals"]["ledger_integrity"] = ritual
        print(f"   ✓ Checked {len(ledger_files)} ledger files")

    def check_background_processes(self):
        """Check for running Python/Node background processes"""

        ritual = {
            "name": "Background Processes",
            "type": "Runtime Processes",
            "status": "checking",
            "processes": []
        }

        try:
            if sys.platform == "win32":
                # Windows
                result = subprocess.run(
                    ["powershell", "-Command",
                     "Get-Process | Where-Object {$_.ProcessName -match 'python|node|streamlit|uvicorn'} | Select-Object ProcessName,Id,CPU | ConvertTo-Json"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode == 0 and result.stdout.strip():
                    try:
                        processes = json.loads(result.stdout)
                        if not isinstance(processes, list):
                            processes = [processes]

                        ritual["processes"] = [
                            {
                                "name": p.get("ProcessName"),
                                "pid": p.get("Id"),
                                "cpu": p.get("CPU")
                            }
                            for p in processes
                        ]
                    except:
                        pass
            else:
                # Linux/Mac
                result = subprocess.run(
                    ["ps", "aux"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode == 0:
                    for line in result.stdout.split("\n"):
                        if any(proc in line.lower() for proc in ["python", "node", "streamlit", "uvicorn", "fastapi"]):
                            ritual["processes"].append({"cmdline": line.strip()})

            ritual["status"] = "active"
            print(f"   ✓ Found {len(ritual['processes'])} relevant background processes")

        except Exception as e:
            ritual["status"] = "error"
            ritual["error"] = str(e)
            self.add_warning(f"Error checking background processes: {e}")
            print(f"   ⚠ Error: {e}")

        self.results["rituals"]["background_processes"] = ritual

    def check_scheduled_tasks(self):
        """Check Windows Task Scheduler or cron jobs"""

        ritual = {
            "name": "Scheduled Tasks",
            "type": "Task Scheduler",
            "status": "checking",
            "tasks": []
        }

        try:
            if sys.platform == "win32":
                # Check Task Scheduler
                result = subprocess.run(
                    ["powershell", "-Command",
                     "Get-ScheduledTask | Where-Object {$_.TaskName -match 'codex|dawn|festival'} | Select-Object TaskName,State | ConvertTo-Json"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode == 0 and result.stdout.strip():
                    try:
                        tasks = json.loads(result.stdout)
                        if not isinstance(tasks, list):
                            tasks = [tasks]

                        for task in tasks:
                            task_info = {
                                "name": task.get("TaskName"),
                                "state": task.get("State")
                            }

                            if task.get("State") != "Ready" and task.get("State") != "Running":
                                self.add_warning(f"Scheduled task '{task.get('TaskName')}' is in state: {task.get('State')}")

                            ritual["tasks"].append(task_info)
                    except Exception as e:
                        ritual["parse_error"] = str(e)

                print(f"   ✓ Found {len(ritual['tasks'])} Codex-related scheduled tasks")
            else:
                # Check crontab
                result = subprocess.run(
                    ["crontab", "-l"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                if result.returncode == 0:
                    cron_lines = [line for line in result.stdout.split("\n")
                                 if line.strip() and not line.strip().startswith("#")]

                    ritual["tasks"] = [{"cron_entry": line} for line in cron_lines]
                    print(f"   ✓ Found {len(cron_lines)} cron jobs")

            ritual["status"] = "active"

        except Exception as e:
            ritual["status"] = "error"
            ritual["error"] = str(e)
            print(f"   ⚠ Error: {e}")

        self.results["rituals"]["scheduled_tasks"] = ritual

    def add_failure(self, message: str):
        """Add a failure to the report"""
        self.results["failures"].append({
            "message": message,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "severity": "critical"
        })

    def add_warning(self, message: str):
        """Add a warning to the report"""
        self.results["warnings"].append({
            "message": message,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "severity": "warning"
        })

    def generate_summary(self):
        """Generate executive summary"""

        total_rituals = len(self.results["rituals"])
        active_rituals = sum(1 for r in self.results["rituals"].values()
                            if r.get("status") in ["active", "healthy"])
        degraded_rituals = sum(1 for r in self.results["rituals"].values()
                              if r.get("status") in ["degraded", "error"])

        self.results["summary"] = {
            "total_ritual_categories": total_rituals,
            "active": active_rituals,
            "degraded": degraded_rituals,
            "total_failures": len(self.results["failures"]),
            "total_warnings": len(self.results["warnings"]),
            "overall_health": self._calculate_health_score(),
            "needs_attention": len(self.results["failures"]) > 0 or len(self.results["warnings"]) > 3
        }

    def _calculate_health_score(self) -> str:
        """Calculate overall system health"""

        failures = len(self.results["failures"])
        warnings = len(self.results["warnings"])

        if failures == 0 and warnings == 0:
            return "EXCELLENT"
        elif failures == 0 and warnings <= 3:
            return "GOOD"
        elif failures <= 2 and warnings <= 5:
            return "FAIR"
        else:
            return "NEEDS_ATTENTION"

    def print_report(self):
        """Print formatted report to console"""

        print("\n" + "="*70)
        print("📊 RITUAL STATUS REPORT")
        print("="*70 + "\n")

        summary = self.results["summary"]

        # Overall Health
        health_emoji = {
            "EXCELLENT": "✅",
            "GOOD": "🟢",
            "FAIR": "🟡",
            "NEEDS_ATTENTION": "🔴"
        }

        print(f"Overall Health: {health_emoji.get(summary['overall_health'], '❓')} {summary['overall_health']}")
        print(f"Active Rituals: {summary['active']}/{summary['total_ritual_categories']}")
        print(f"Failures: {summary['total_failures']}")
        print(f"Warnings: {summary['total_warnings']}\n")

        # Failures
        if self.results["failures"]:
            print("🔴 CRITICAL FAILURES:")
            print("-" * 70)
            for i, failure in enumerate(self.results["failures"], 1):
                print(f"{i}. {failure['message']}")
            print()

        # Warnings
        if self.results["warnings"]:
            print("⚠️  WARNINGS:")
            print("-" * 70)
            for i, warning in enumerate(self.results["warnings"], 1):
                print(f"{i}. {warning['message']}")
            print()

        # Ritual Details
        print("📋 RITUAL CATEGORIES:")
        print("-" * 70)
        for category, ritual in self.results["rituals"].items():
            status_emoji = {
                "active": "✅",
                "healthy": "✅",
                "degraded": "⚠️",
                "error": "🔴",
                "checking": "🔍",
                "not_installed": "❌",
                "docker_unavailable": "⚠️"
            }

            emoji = status_emoji.get(ritual["status"], "❓")
            print(f"{emoji} {ritual['name']}: {ritual['status'].upper()}")

            # Additional details
            if "total_workflows" in ritual:
                print(f"   └─ {ritual['total_workflows']} workflows defined")
            if "services" in ritual:
                print(f"   └─ {len(ritual['services'])} services/timers defined")
            if "containers" in ritual:
                running = sum(1 for c in ritual["containers"] if c.get("state") == "running")
                print(f"   └─ {running}/{len(ritual['containers'])} containers running")
            if "capsules" in ritual:
                existing = sum(1 for c in ritual["capsules"] if c.get("status") == "exists")
                print(f"   └─ {existing}/{len(ritual['capsules'])} capsules found")
            if "ledgers" in ritual:
                valid = sum(1 for l in ritual["ledgers"] if l.get("status") == "valid")
                print(f"   └─ {valid}/{len(ritual['ledgers'])} ledgers valid")
            if "processes" in ritual:
                print(f"   └─ {len(ritual['processes'])} background processes")
            if "tasks" in ritual:
                print(f"   └─ {len(ritual['tasks'])} scheduled tasks")

        print("\n" + "="*70)
        print(f"Report generated: {self.results['timestamp']}")
        print("="*70 + "\n")

    def save_report(self, output_path: str = "ritual_status_report.json"):
        """Save report to JSON file"""

        with open(output_path, "w") as f:
            json.dump(self.results, f, indent=2)

        print(f"💾 Report saved: {output_path}")


def main():
    """Run ritual monitor"""

    monitor = RitualMonitor()
    results = monitor.check_all_rituals()

    # Print formatted report
    monitor.print_report()

    # Save to file
    monitor.save_report()

    # Exit with appropriate code
    if results["summary"]["total_failures"] > 0:
        print("⚠️  Exiting with failure code (failures detected)")
        sys.exit(1)
    elif results["summary"]["overall_health"] == "NEEDS_ATTENTION":
        print("⚠️  Exiting with warning code (attention needed)")
        sys.exit(2)
    else:
        print("✅ All rituals healthy!")
        sys.exit(0)


if __name__ == "__main__":
    main()
