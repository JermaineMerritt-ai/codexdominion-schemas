#!/usr/bin/env python3
"""
Codex Dominion Comprehensive System Check

Performs a complete health assessment of all system components:
1. Core system files and directories
2. Data integrity and validation
3. Dashboard and application status
4. GitHub Actions and automation
5. Dependencies and environment
6. Performance and operational metrics
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple


class CodexSystemChecker:
    def __init__(self):
        self.root_path = Path(".")
        self.issues = []
        self.successes = []
        self.warnings = []
        self.metrics = {}

    def check_core_structure(self) -> Dict[str, Any]:
        """Check core directory and file structure"""
        print("🏛️ Checking Core System Structure...")

        critical_paths = {
            # Core directories
            "codex-suite": "codex-suite/",
            "data_directory": "data/",
            "github_actions": ".github/",
            "config_directory": "config/",
            # Core files
            "codex_models": "codex_models.py",
            "codex_utils": "codex_utils.py",
            "requirements": "requirements.txt",
            "readme": "README.md",
            # Dashboard files
            "unified_dashboard": "codex-suite/apps/dashboard/codex_unified.py",
            "council_access": "codex-suite/apps/dashboard/council_access.py",
            # Data files
            "proclamations": "proclamations.json",
            "ledger": "ledger.json",
            "cycles": "cycles.json",
        }

        structure_status = {}
        missing_critical = []

        for name, path in critical_paths.items():
            full_path = self.root_path / path
            exists = full_path.exists()
            structure_status[name] = {
                "path": str(path),
                "exists": exists,
                "type": "directory" if full_path.is_dir() else "file",
            }

            if exists:
                self.successes.append(f"✅ {name}: {path}")
                print(f"   ✅ {name}: {path}")
            else:
                missing_critical.append(path)
                self.issues.append(f"❌ Missing critical: {path}")
                print(f"   ❌ Missing: {path}")

        return {
            "status": "healthy" if not missing_critical else "degraded",
            "missing_count": len(missing_critical),
            "total_checked": len(critical_paths),
            "structure": structure_status,
            "missing_files": missing_critical,
        }

    def check_data_integrity(self) -> Dict[str, Any]:
        """Check data file integrity and validation"""
        print("\n📊 Checking Data Integrity...")

        data_files = [
            "proclamations.json",
            "data/proclamations.json",
            "codex-suite/data/proclamations.json",
            "ledger.json",
            "cycles.json",
            "demo_verification.json",
        ]

        integrity_status = {}
        valid_files = 0

        for data_file in data_files:
            file_path = self.root_path / data_file
            file_status = {
                "exists": file_path.exists(),
                "valid_json": False,
                "size_bytes": 0,
                "last_modified": None,
            }

            if file_path.exists():
                try:
                    file_status["size_bytes"] = file_path.stat().st_size
                    file_status["last_modified"] = datetime.fromtimestamp(
                        file_path.stat().st_mtime
                    ).isoformat()

                    with open(file_path, "r", encoding="utf-8") as f:
                        json.load(f)
                    file_status["valid_json"] = True
                    valid_files += 1
                    self.successes.append(f"✅ Valid JSON: {data_file}")
                    print(
                        f"   ✅ {data_file}: Valid JSON ({file_status['size_bytes']} bytes)"
                    )

                except json.JSONDecodeError as e:
                    self.issues.append(f"❌ Invalid JSON: {data_file} - {e}")
                    print(f"   ❌ {data_file}: Invalid JSON - {e}")
                except Exception as e:
                    self.issues.append(f"❌ Error reading: {data_file} - {e}")
                    print(f"   ❌ {data_file}: Error - {e}")
            else:
                self.warnings.append(f"⚠️ Missing data file: {data_file}")
                print(f"   ⚠️ Missing: {data_file}")

            integrity_status[data_file] = file_status

        return {
            "status": "healthy" if valid_files >= len(data_files) * 0.8 else "degraded",
            "valid_files": valid_files,
            "total_files": len(data_files),
            "integrity_rate": (valid_files / len(data_files)) * 100,
            "files": integrity_status,
        }

    def check_python_environment(self) -> Dict[str, Any]:
        """Check Python environment and dependencies"""
        print("\n🐍 Checking Python Environment...")

        env_status = {
            "python_version": sys.version,
            "python_executable": sys.executable,
            "virtual_env": None,
            "installed_packages": [],
            "missing_packages": [],
        }

        # Check virtual environment
        if hasattr(sys, "real_prefix") or (
            hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
        ):
            env_status["virtual_env"] = "active"
            self.successes.append("✅ Virtual environment: Active")
            print("   ✅ Virtual environment: Active")
        else:
            env_status["virtual_env"] = "none"
            self.warnings.append("⚠️ No virtual environment detected")
            print("   ⚠️ No virtual environment detected")

        # Check critical packages
        critical_packages = [
            "streamlit",
            "pydantic",
            "requests",
            "pathlib",
            "datetime",
            "json",
            "os",
            "sys",
        ]

        for package in critical_packages:
            try:
                __import__(package)
                env_status["installed_packages"].append(package)
                self.successes.append(f"✅ Package available: {package}")
                print(f"   ✅ {package}: Available")
            except ImportError:
                env_status["missing_packages"].append(package)
                self.issues.append(f"❌ Missing package: {package}")
                print(f"   ❌ {package}: Missing")

        # Check requirements.txt
        req_file = self.root_path / "requirements.txt"
        if req_file.exists():
            try:
                with open(req_file, "r") as f:
                    requirements = f.read().strip().split("\n")
                env_status["requirements_count"] = len(
                    [r for r in requirements if r.strip()]
                )
                self.successes.append(
                    f"✅ Requirements file: {env_status['requirements_count']} packages"
                )
                print(
                    f"   ✅ requirements.txt: {env_status['requirements_count']} packages"
                )
            except Exception as e:
                self.issues.append(f"❌ Error reading requirements.txt: {e}")
                print(f"   ❌ requirements.txt error: {e}")

        return env_status

    def check_github_actions(self) -> Dict[str, Any]:
        """Check GitHub Actions configuration"""
        print("\n⚙️ Checking GitHub Actions...")

        github_dir = self.root_path / ".github"
        workflows_dir = github_dir / "workflows"
        actions_dir = github_dir / "actions"

        github_status = {
            "workflows_count": 0,
            "actions_count": 0,
            "valid_workflows": 0,
            "templates_exist": False,
            "dependabot_configured": False,
        }

        if not workflows_dir.exists():
            self.issues.append("❌ No .github/workflows directory")
            print("   ❌ No workflows directory found")
            return github_status

        # Check workflows
        workflow_files = list(workflows_dir.glob("*.yml")) + list(
            workflows_dir.glob("*.yaml")
        )
        github_status["workflows_count"] = len(workflow_files)

        valid_workflows = 0
        for workflow in workflow_files:
            try:
                import yaml

                with open(workflow, "r") as f:
                    yaml.safe_load(f)
                valid_workflows += 1
                self.successes.append(f"✅ Valid workflow: {workflow.name}")
                print(f"   ✅ Workflow: {workflow.name}")
            except Exception as e:
                self.issues.append(f"❌ Invalid workflow: {workflow.name} - {e}")
                print(f"   ❌ Workflow error: {workflow.name}")

        github_status["valid_workflows"] = valid_workflows

        # Check for custom actions
        if actions_dir.exists():
            action_dirs = [d for d in actions_dir.iterdir() if d.is_dir()]
            github_status["actions_count"] = len(action_dirs)
            for action in action_dirs:
                self.successes.append(f"✅ Custom action: {action.name}")
                print(f"   ✅ Action: {action.name}")

        # Check for templates
        pr_template = github_dir / "pull_request_template.md"
        issue_templates = github_dir / "ISSUE_TEMPLATE"

        if pr_template.exists() and issue_templates.exists():
            github_status["templates_exist"] = True
            self.successes.append("✅ GitHub templates configured")
            print("   ✅ Templates: Configured")

        # Check Dependabot
        dependabot_file = github_dir / "dependabot.yml"
        if dependabot_file.exists():
            github_status["dependabot_configured"] = True
            self.successes.append("✅ Dependabot configured")
            print("   ✅ Dependabot: Configured")

        return github_status

    def check_dashboard_status(self) -> Dict[str, Any]:
        """Check dashboard and application status"""
        print("\n📊 Checking Dashboard Applications...")

        dashboard_files = [
            "codex-suite/apps/dashboard/codex_unified.py",
            "codex-suite/apps/dashboard/council_access.py",
            "codex-suite/apps/dashboard/heir_avatar.py",
            "codex-suite/apps/dashboard/command_crown.py",
            "ai_development_studio_lite.py",
        ]

        dashboard_status = {
            "total_dashboards": len(dashboard_files),
            "available_dashboards": 0,
            "syntax_valid": 0,
            "dashboards": {},
        }

        for dashboard in dashboard_files:
            dashboard_path = self.root_path / dashboard
            status = {
                "exists": dashboard_path.exists(),
                "syntax_valid": False,
                "size_bytes": 0,
            }

            if dashboard_path.exists():
                dashboard_status["available_dashboards"] += 1
                status["size_bytes"] = dashboard_path.stat().st_size

                # Check Python syntax
                try:
                    with open(dashboard_path, "r", encoding="utf-8") as f:
                        compile(f.read(), dashboard, "exec")
                    status["syntax_valid"] = True
                    dashboard_status["syntax_valid"] += 1
                    self.successes.append(f"✅ Dashboard valid: {dashboard}")
                    print(
                        f"   ✅ {Path(dashboard).name}: Valid syntax ({status['size_bytes']} bytes)"
                    )
                except SyntaxError as e:
                    self.issues.append(f"❌ Syntax error in {dashboard}: {e}")
                    print(f"   ❌ {Path(dashboard).name}: Syntax error")
                except Exception as e:
                    self.warnings.append(f"⚠️ Could not validate {dashboard}: {e}")
                    print(f"   ⚠️ {Path(dashboard).name}: Validation error")
            else:
                self.issues.append(f"❌ Missing dashboard: {dashboard}")
                print(f"   ❌ Missing: {Path(dashboard).name}")

            dashboard_status["dashboards"][dashboard] = status

        return dashboard_status

    def check_system_performance(self) -> Dict[str, Any]:
        """Check system performance metrics"""
        print("\n🚀 Checking System Performance...")

        perf_metrics = {
            "disk_usage": {},
            "file_counts": {},
            "largest_files": [],
            "python_files": 0,
            "json_files": 0,
            "total_files": 0,
        }

        try:
            # Get directory sizes and file counts
            for item in self.root_path.iterdir():
                if item.is_dir():
                    try:
                        file_count = len(list(item.rglob("*")))
                        perf_metrics["file_counts"][item.name] = file_count
                        print(f"   📁 {item.name}: {file_count} files")
                    except Exception:
                        perf_metrics["file_counts"][item.name] = 0

            # Count file types
            python_files = list(self.root_path.rglob("*.py"))
            json_files = list(self.root_path.rglob("*.json"))

            perf_metrics["python_files"] = len(python_files)
            perf_metrics["json_files"] = len(json_files)
            perf_metrics["total_files"] = len(list(self.root_path.rglob("*")))

            print(f"   🐍 Python files: {perf_metrics['python_files']}")
            print(f"   📋 JSON files: {perf_metrics['json_files']}")
            print(f"   📄 Total files: {perf_metrics['total_files']}")

            # Find largest files
            large_files = []
            for file_path in self.root_path.rglob("*"):
                if file_path.is_file():
                    try:
                        size = file_path.stat().st_size
                        if size > 1024 * 1024:  # > 1MB
                            large_files.append(
                                {
                                    "path": str(file_path.relative_to(self.root_path)),
                                    "size_mb": round(size / (1024 * 1024), 2),
                                }
                            )
                    except Exception:
                        pass

            large_files.sort(key=lambda x: x["size_mb"], reverse=True)
            perf_metrics["largest_files"] = large_files[:10]

            for large_file in perf_metrics["largest_files"]:
                print(
                    f"   💾 Large file: {large_file['path']} ({large_file['size_mb']} MB)"
                )

        except Exception as e:
            self.warnings.append(f"⚠️ Performance check error: {e}")
            print(f"   ⚠️ Performance check error: {e}")

        return perf_metrics

    def generate_system_report(self) -> Dict[str, Any]:
        """Generate comprehensive system report"""

        print(f"\n🏛️ CODEX DOMINION COMPREHENSIVE SYSTEM CHECK")
        print("=" * 60)

        # Run all checks
        structure_check = self.check_core_structure()
        data_check = self.check_data_integrity()
        env_check = self.check_python_environment()
        github_check = self.check_github_actions()
        dashboard_check = self.check_dashboard_status()
        performance_check = self.check_system_performance()

        # Calculate overall health score
        total_checks = 6
        healthy_systems = sum(
            [
                1 if structure_check["status"] == "healthy" else 0,
                1 if data_check["status"] == "healthy" else 0,
                1 if len(env_check["missing_packages"]) == 0 else 0,
                1 if github_check["valid_workflows"] > 0 else 0,
                (
                    1
                    if dashboard_check["syntax_valid"]
                    >= dashboard_check["available_dashboards"] * 0.8
                    else 0
                ),
                1 if performance_check["python_files"] > 0 else 0,
            ]
        )

        health_score = (healthy_systems / total_checks) * 100

        # Determine overall status
        if health_score >= 90:
            overall_status = "OPTIMAL"
            status_icon = "🎉"
        elif health_score >= 70:
            overall_status = "HEALTHY"
            status_icon = "✅"
        elif health_score >= 50:
            overall_status = "DEGRADED"
            status_icon = "⚠️"
        else:
            overall_status = "CRITICAL"
            status_icon = "❌"

        # Generate report
        report = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": overall_status,
            "health_score": round(health_score, 1),
            "summary": {
                "total_issues": len(self.issues),
                "total_successes": len(self.successes),
                "total_warnings": len(self.warnings),
            },
            "checks": {
                "core_structure": structure_check,
                "data_integrity": data_check,
                "python_environment": env_check,
                "github_actions": github_check,
                "dashboard_status": dashboard_check,
                "system_performance": performance_check,
            },
            "issues": self.issues,
            "successes": self.successes,
            "warnings": self.warnings,
            "recommendations": [],
        }

        # Generate recommendations
        if len(self.issues) > 0:
            report["recommendations"].append(
                "🔧 Address critical issues listed in the issues section"
            )
        if data_check["integrity_rate"] < 100:
            report["recommendations"].append(
                "📊 Restore or validate damaged data files"
            )
        if env_check["virtual_env"] == "none":
            report["recommendations"].append(
                "🐍 Set up Python virtual environment for better dependency management"
            )
        if github_check["workflows_count"] == 0:
            report["recommendations"].append(
                "⚙️ Configure GitHub Actions workflows for automation"
            )
        if dashboard_check["syntax_valid"] < dashboard_check["available_dashboards"]:
            report["recommendations"].append(
                "📊 Fix syntax errors in dashboard applications"
            )

        # Save report
        with open("SYSTEM_CHECK_REPORT.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, default=str)

        # Display summary
        print(f"\n{status_icon} SYSTEM STATUS SUMMARY")
        print("=" * 40)
        print(f"🎯 Overall Status: {overall_status}")
        print(f"📊 Health Score: {health_score:.1f}%")
        print(f"✅ Successes: {len(self.successes)}")
        print(f"⚠️ Warnings: {len(self.warnings)}")
        print(f"❌ Issues: {len(self.issues)}")

        if self.issues:
            print(f"\n❌ CRITICAL ISSUES:")
            for issue in self.issues[:5]:  # Show top 5 issues
                print(f"   {issue}")
            if len(self.issues) > 5:
                print(f"   ... and {len(self.issues) - 5} more issues")

        if report["recommendations"]:
            print(f"\n🔧 RECOMMENDATIONS:")
            for rec in report["recommendations"]:
                print(f"   {rec}")

        print(f"\n🏛️ SACRED DOMINION STATUS: {overall_status}")
        if overall_status == "OPTIMAL":
            print(
                "🔥 Sacred flames burn bright! The dominion operates with divine precision! 🔥"
            )
        elif overall_status == "HEALTHY":
            print("✅ The dominion operates well with minor optimizations needed.")
        elif overall_status == "DEGRADED":
            print("⚠️ The dominion requires attention to maintain eternal operation.")
        else:
            print("❌ Critical intervention required to restore dominion stability.")

        return report


def main():
    """Run comprehensive system check"""
    checker = CodexSystemChecker()
    report = checker.generate_system_report()

    # Return appropriate exit code
    return 0 if report["overall_status"] in ["OPTIMAL", "HEALTHY"] else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
