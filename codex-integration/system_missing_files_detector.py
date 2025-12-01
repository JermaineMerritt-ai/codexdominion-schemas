#!/usr/bin/env python3
"""
System-Level Missing Files Detector
Comprehensive analysis to identify missing files based on system requirements
"""

import importlib.util
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Set

import yaml


class SystemMissingFilesDetector:
    """Detects missing files at system level based on references and requirements."""

    def __init__(self):
        self.workspace_root = Path(__file__).parent.parent
        self.missing_files = []
        self.broken_references = []
        self.system_requirements = {}

    def analyze_missing_files(self) -> Dict:
        """Perform comprehensive missing files analysis."""
        print("🔍 SYSTEM-LEVEL MISSING FILES DETECTOR v1.0.0")
        print("=" * 70)
        print("🔬 Analyzing system for missing files and broken references...")

        analysis_results = {
            "python_import_analysis": self.analyze_python_imports(),
            "yaml_reference_analysis": self.analyze_yaml_references(),
            "json_reference_analysis": self.analyze_json_references(),
            "system_expected_files": self.analyze_system_expected_files(),
            "github_actions_dependencies": self.analyze_github_actions_deps(),
            "capsule_dependencies": self.analyze_capsule_dependencies(),
            "template_dependencies": self.analyze_template_dependencies(),
            "infrastructure_files": self.analyze_infrastructure_files(),
            "missing_config_files": self.analyze_missing_configs(),
            "broken_symlinks": self.analyze_broken_symlinks(),
        }

        # Compile comprehensive missing files report
        self.compile_missing_files_report(analysis_results)

        return analysis_results

    def analyze_python_imports(self) -> Dict:
        """Analyze Python files for missing import dependencies."""
        print("\n🐍 ANALYZING PYTHON IMPORT DEPENDENCIES")
        print("-" * 50)

        python_analysis = {
            "files_analyzed": 0,
            "missing_modules": [],
            "missing_local_imports": [],
            "broken_relative_imports": [],
        }

        python_files = list(self.workspace_root.rglob("*.py"))

        for py_file in python_files:
            if ".venv" in str(py_file) or "__pycache__" in str(py_file):
                continue

            python_analysis["files_analyzed"] += 1

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Find import statements
                import_lines = re.findall(
                    r"^(?:from\s+(\S+)\s+)?import\s+(.+)$", content, re.MULTILINE
                )

                for from_module, import_items in import_lines:
                    if from_module:
                        # Check relative imports
                        if from_module.startswith("."):
                            relative_path = self.resolve_relative_import(
                                py_file, from_module
                            )
                            if relative_path and not relative_path.exists():
                                python_analysis["broken_relative_imports"].append(
                                    {
                                        "file": str(py_file),
                                        "import": from_module,
                                        "expected_path": str(relative_path),
                                    }
                                )
                        else:
                            # Check if module exists
                            if not self.check_module_exists(from_module):
                                python_analysis["missing_modules"].append(
                                    {"file": str(py_file), "module": from_module}
                                )

            except Exception as e:
                print(f"⚠️ Error analyzing {py_file.name}: {str(e)}")

        print(f"🐍 Analyzed {python_analysis['files_analyzed']} Python files")
        if python_analysis["missing_modules"]:
            print(f"❌ Found {len(python_analysis['missing_modules'])} missing modules")
        if python_analysis["broken_relative_imports"]:
            print(
                f"❌ Found {len(python_analysis['broken_relative_imports'])} broken relative imports"
            )

        return python_analysis

    def analyze_yaml_references(self) -> Dict:
        """Analyze YAML files for missing file references."""
        print("\n📄 ANALYZING YAML FILE REFERENCES")
        print("-" * 50)

        yaml_analysis = {
            "files_analyzed": 0,
            "missing_referenced_files": [],
            "broken_path_references": [],
        }

        yaml_files = list(self.workspace_root.rglob("*.yaml")) + list(
            self.workspace_root.rglob("*.yml")
        )

        for yaml_file in yaml_files:
            yaml_analysis["files_analyzed"] += 1

            try:
                with open(yaml_file, "r", encoding="utf-8") as f:
                    yaml_content = yaml.safe_load(f)

                # Recursively check for file path references
                self.find_file_references_in_dict(
                    yaml_content, yaml_file, yaml_analysis
                )

            except Exception as e:
                print(f"⚠️ Error analyzing {yaml_file.name}: {str(e)}")

        print(f"📄 Analyzed {yaml_analysis['files_analyzed']} YAML files")
        if yaml_analysis["missing_referenced_files"]:
            print(
                f"❌ Found {len(yaml_analysis['missing_referenced_files'])} missing referenced files"
            )

        return yaml_analysis

    def analyze_json_references(self) -> Dict:
        """Analyze JSON files for missing references."""
        print("\n🗂️ ANALYZING JSON FILE REFERENCES")
        print("-" * 50)

        json_analysis = {
            "files_analyzed": 0,
            "missing_referenced_files": [],
            "required_data_files": [],
        }

        json_files = list(self.workspace_root.rglob("*.json"))

        # Check for expected JSON data files based on system requirements
        expected_json_files = [
            "proclamations.json",
            "cycles.json",
            "ledger.json",
            "heartbeat.json",
        ]

        for expected_file in expected_json_files:
            if not (self.workspace_root / expected_file).exists():
                json_analysis["required_data_files"].append(expected_file)

        for json_file in json_files:
            json_analysis["files_analyzed"] += 1

            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    json_content = json.load(f)

                # Check for file path references
                self.find_file_references_in_dict(
                    json_content, json_file, json_analysis
                )

            except Exception as e:
                print(f"⚠️ Error analyzing {json_file.name}: {str(e)}")

        print(f"🗂️ Analyzed {json_analysis['files_analyzed']} JSON files")
        if json_analysis["required_data_files"]:
            print(
                f"⚠️ Missing {len(json_analysis['required_data_files'])} expected data files"
            )

        return json_analysis

    def analyze_system_expected_files(self) -> Dict:
        """Analyze expected system files based on documentation and scripts."""
        print("\n⚙️ ANALYZING EXPECTED SYSTEM FILES")
        print("-" * 50)

        system_analysis = {
            "expected_files": [],
            "missing_system_files": [],
            "critical_files_missing": [],
        }

        # Expected system files based on documentation and references
        expected_system_files = [
            # Core system files
            "package.json",
            "requirements.txt",
            "pyproject.toml",
            "Dockerfile",
            ".gitignore",
            "README.md",
            "LICENSE",
            # Configuration files
            "config/app.config.json",
            "config/database.json",
            "config/nginx.conf",
            # Infrastructure files
            "infra/nginx.conf",
            "infra/docker-compose.yml",
            "infra/kubernetes.yaml",
            # Environment files
            ".env",
            ".env.example",
            ".env.production",
            ".env.staging",
            # SSL/Security files
            "ssl/certificates/",
            "ssl/private/",
            # Data files expected by scripts
            "proclamations.json",
            "cycles.json",
            "ledger.json",
            "heartbeat.json",
        ]

        for expected_file in expected_system_files:
            expected_path = self.workspace_root / expected_file
            system_analysis["expected_files"].append(expected_file)

            if not expected_path.exists():
                system_analysis["missing_system_files"].append(expected_file)

                # Mark critical files
                if expected_file in ["requirements.txt", ".gitignore", "README.md"]:
                    system_analysis["critical_files_missing"].append(expected_file)

        print(
            f"⚙️ Checked {len(system_analysis['expected_files'])} expected system files"
        )
        print(f"⚠️ Missing {len(system_analysis['missing_system_files'])} system files")
        if system_analysis["critical_files_missing"]:
            print(
                f"❌ Missing {len(system_analysis['critical_files_missing'])} CRITICAL files"
            )

        return system_analysis

    def analyze_github_actions_deps(self) -> Dict:
        """Analyze GitHub Actions for missing dependencies."""
        print("\n🚀 ANALYZING GITHUB ACTIONS DEPENDENCIES")
        print("-" * 50)

        github_analysis = {
            "workflows_analyzed": 0,
            "missing_action_scripts": [],
            "missing_dependencies": [],
        }

        github_workflows_dir = self.workspace_root / ".github" / "workflows"
        if github_workflows_dir.exists():
            workflow_files = list(github_workflows_dir.glob("*.yaml")) + list(
                github_workflows_dir.glob("*.yml")
            )

            for workflow in workflow_files:
                github_analysis["workflows_analyzed"] += 1

                try:
                    with open(workflow, "r", encoding="utf-8") as f:
                        workflow_content = yaml.safe_load(f)

                    # Check for action script references
                    self.check_workflow_dependencies(workflow_content, github_analysis)

                except Exception as e:
                    print(f"⚠️ Error analyzing {workflow.name}: {str(e)}")

        print(f"🚀 Analyzed {github_analysis['workflows_analyzed']} GitHub workflows")
        return github_analysis

    def analyze_capsule_dependencies(self) -> Dict:
        """Analyze capsule system for missing dependencies."""
        print("\n💊 ANALYZING CAPSULE DEPENDENCIES")
        print("-" * 50)

        capsule_analysis = {
            "capsules_analyzed": 0,
            "missing_parent_capsules": [],
            "missing_storage_paths": [],
        }

        capsule_dirs = [
            self.workspace_root / "system_capsules",
            self.workspace_root / "apps",
        ]

        for capsule_dir in capsule_dirs:
            if capsule_dir.exists():
                for capsule_file in capsule_dir.rglob("*capsule*.yaml"):
                    capsule_analysis["capsules_analyzed"] += 1

                    try:
                        with open(capsule_file, "r", encoding="utf-8") as f:
                            capsule_data = yaml.safe_load(f)

                        # Check for parent capsule dependencies
                        if (
                            "lineage" in capsule_data
                            and "parent_capsules" in capsule_data["lineage"]
                        ):
                            for parent in capsule_data["lineage"]["parent_capsules"]:
                                # This would check if parent capsule exists
                                pass

                    except Exception as e:
                        print(
                            f"⚠️ Error analyzing capsule {capsule_file.name}: {str(e)}"
                        )

        print(f"💊 Analyzed {capsule_analysis['capsules_analyzed']} capsules")
        return capsule_analysis

    def analyze_template_dependencies(self) -> Dict:
        """Analyze template dependencies."""
        print("\n📋 ANALYZING TEMPLATE DEPENDENCIES")
        print("-" * 50)

        template_analysis = {"templates_found": 0, "missing_template_assets": []}

        templates_dir = self.workspace_root / "templates"
        if templates_dir.exists():
            template_files = list(templates_dir.rglob("*.json"))
            template_analysis["templates_found"] = len(template_files)

        print(f"📋 Found {template_analysis['templates_found']} template files")
        return template_analysis

    def analyze_infrastructure_files(self) -> Dict:
        """Analyze infrastructure file dependencies."""
        print("\n🏗️ ANALYZING INFRASTRUCTURE FILES")
        print("-" * 50)

        infra_analysis = {
            "config_files_checked": 0,
            "missing_nginx_configs": [],
            "missing_ssl_configs": [],
        }

        # Check for Nginx configurations
        nginx_configs = ["nginx.conf", "default.conf", "ssl.conf"]
        for config in nginx_configs:
            config_path = self.workspace_root / "infra" / config
            infra_analysis["config_files_checked"] += 1
            if not config_path.exists():
                infra_analysis["missing_nginx_configs"].append(config)

        print(
            f"🏗️ Checked {infra_analysis['config_files_checked']} infrastructure configs"
        )
        return infra_analysis

    def analyze_missing_configs(self) -> Dict:
        """Analyze missing configuration files."""
        print("\n⚙️ ANALYZING MISSING CONFIGURATION FILES")
        print("-" * 50)

        config_analysis = {"config_types_checked": 0, "missing_configs": []}

        expected_configs = [
            "config/database.json",
            "config/redis.json",
            "config/logging.yaml",
            "config/monitoring.yaml",
        ]

        for config in expected_configs:
            config_analysis["config_types_checked"] += 1
            config_path = self.workspace_root / config
            if not config_path.exists():
                config_analysis["missing_configs"].append(config)

        print(f"⚙️ Checked {config_analysis['config_types_checked']} config types")
        return config_analysis

    def analyze_broken_symlinks(self) -> Dict:
        """Analyze broken symbolic links."""
        print("\n🔗 ANALYZING BROKEN SYMLINKS")
        print("-" * 50)

        symlink_analysis = {"symlinks_checked": 0, "broken_symlinks": []}

        # Find all symlinks and check if they're broken
        for item in self.workspace_root.rglob("*"):
            if item.is_symlink():
                symlink_analysis["symlinks_checked"] += 1
                if not item.exists():
                    symlink_analysis["broken_symlinks"].append(str(item))

        print(f"🔗 Checked {symlink_analysis['symlinks_checked']} symlinks")
        return symlink_analysis

    def find_file_references_in_dict(self, data, source_file, analysis):
        """Recursively find file path references in dictionary data."""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    # Check if value looks like a file path
                    if self.looks_like_file_path(value):
                        referenced_path = self.resolve_path_reference(
                            value, source_file
                        )
                        if referenced_path and not referenced_path.exists():
                            analysis["missing_referenced_files"].append(
                                {
                                    "source": str(source_file),
                                    "reference": value,
                                    "resolved_path": str(referenced_path),
                                }
                            )
                elif isinstance(value, (dict, list)):
                    self.find_file_references_in_dict(value, source_file, analysis)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    self.find_file_references_in_dict(item, source_file, analysis)

    def looks_like_file_path(self, value: str) -> bool:
        """Check if a string looks like a file path."""
        # Simple heuristics for file paths
        path_indicators = [
            value.endswith((".py", ".yaml", ".yml", ".json", ".txt", ".conf", ".md")),
            "/" in value or "\\" in value,
            value.startswith("./") or value.startswith("../"),
            "path" in value.lower() and len(value) > 5,
        ]
        return any(path_indicators)

    def resolve_path_reference(self, path_ref: str, source_file: Path):
        """Resolve a path reference relative to source file or workspace."""
        try:
            # Try relative to source file directory
            if path_ref.startswith("./") or path_ref.startswith("../"):
                return source_file.parent / path_ref
            # Try relative to workspace root
            return self.workspace_root / path_ref
        except:
            return None

    def resolve_relative_import(self, py_file: Path, import_name: str):
        """Resolve relative import to file path."""
        try:
            base_dir = py_file.parent
            parts = import_name.lstrip(".").split(".")

            # Count leading dots for directory traversal
            dots = len(import_name) - len(import_name.lstrip("."))
            for _ in range(dots - 1):
                base_dir = base_dir.parent

            # Build path
            module_path = base_dir
            for part in parts:
                module_path = module_path / part

            # Try .py file or __init__.py in directory
            if (module_path.with_suffix(".py")).exists():
                return module_path.with_suffix(".py")
            elif (module_path / "__init__.py").exists():
                return module_path / "__init__.py"

        except:
            pass
        return None

    def check_module_exists(self, module_name: str) -> bool:
        """Check if a module can be imported."""
        try:
            spec = importlib.util.find_spec(module_name)
            return spec is not None
        except:
            return False

    def check_workflow_dependencies(self, workflow_data, analysis):
        """Check GitHub workflow for missing dependencies."""
        if isinstance(workflow_data, dict):
            for key, value in workflow_data.items():
                if key == "run" and isinstance(value, str):
                    # Check for script references in run commands
                    if "python" in value and ".py" in value:
                        # Extract potential script names
                        script_matches = re.findall(r"python\s+([^\s]+\.py)", value)
                        for script in script_matches:
                            script_path = self.workspace_root / script
                            if not script_path.exists():
                                analysis["missing_action_scripts"].append(
                                    {
                                        "script": script,
                                        "expected_path": str(script_path),
                                    }
                                )
                elif isinstance(value, (dict, list)):
                    self.check_workflow_dependencies(value, analysis)

    def compile_missing_files_report(self, analysis_results):
        """Compile comprehensive missing files report."""
        print("\n" + "=" * 70)
        print("📋 COMPREHENSIVE MISSING FILES REPORT")
        print("=" * 70)

        total_missing = 0
        critical_missing = 0

        for category, results in analysis_results.items():
            if isinstance(results, dict):
                for key, value in results.items():
                    if "missing" in key and isinstance(value, list):
                        total_missing += len(value)
                        if "critical" in key:
                            critical_missing += len(value)

        print(f"📊 TOTAL MISSING FILES: {total_missing}")
        print(f"🚨 CRITICAL MISSING FILES: {critical_missing}")

        if total_missing == 0:
            print("\n✅ NO MISSING FILES DETECTED!")
            print("🎉 System file integrity is PERFECT!")
        else:
            print(f"\n⚠️ {total_missing} files need attention")

        # Save comprehensive report
        with open(self.workspace_root / "MISSING_FILES_ANALYSIS.json", "w") as f:
            json.dump(analysis_results, f, indent=2)

        print(f"\n📄 Complete analysis saved to: MISSING_FILES_ANALYSIS.json")


def main():
    """Run missing files detection."""
    detector = SystemMissingFilesDetector()
    results = detector.analyze_missing_files()

    return results


if __name__ == "__main__":
    main()
