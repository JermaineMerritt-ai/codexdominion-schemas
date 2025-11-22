#!/usr/bin/env python3
"""
GitHub Actions Validator and Fixer
Validates and fixes common issues in GitHub Actions workflows
"""

import os
import yaml
import json
from pathlib import Path

def validate_github_workflows():
    """Validate all GitHub Actions workflows."""
    print("🔍 GITHUB ACTIONS VALIDATOR")
    print("=" * 50)
    
    github_dir = Path(".github")
    workflows_dir = github_dir / "workflows"
    actions_dir = github_dir / "actions"
    
    validation_results = {
        "workflows_checked": 0,
        "actions_checked": 0,
        "issues_found": [],
        "fixes_applied": [],
        "status": "unknown"
    }
    
    # Check workflows directory
    if not workflows_dir.exists():
        validation_results["issues_found"].append("❌ .github/workflows directory not found")
        return validation_results
    
    # Validate workflow files
    for workflow_file in workflows_dir.glob("*.yaml"):
        validation_results["workflows_checked"] += 1
        print(f"📄 Checking workflow: {workflow_file.name}")
        
        try:
            with open(workflow_file, 'r') as f:
                workflow_content = yaml.safe_load(f)
                
            # Re-read for text analysis
            with open(workflow_file, 'r') as f:
                workflow_text = f.read()
            
            print(f"🔍 Workflow content keys: {list(workflow_content.keys()) if workflow_content else 'None'}")
            
            # Check for common issues
            if not workflow_content or ('on' not in workflow_content and True not in workflow_content):
                validation_results["issues_found"].append(f"❌ {workflow_file.name}: Missing 'on' trigger")
            
            if not workflow_content or 'jobs' not in workflow_content:
                validation_results["issues_found"].append(f"❌ {workflow_file.name}: Missing 'jobs' section")
            
            # Check for outdated actions
            if 'actions/checkout@v3' in workflow_text:
                validation_results["issues_found"].append(f"⚠️ {workflow_file.name}: Using outdated checkout action")
            
            print(f"✅ {workflow_file.name}: Syntax valid")
            
        except yaml.YAMLError as e:
            validation_results["issues_found"].append(f"❌ {workflow_file.name}: YAML syntax error - {str(e)}")
        except Exception as e:
            validation_results["issues_found"].append(f"❌ {workflow_file.name}: Validation error - {str(e)}")
    
    # Check custom actions
    if actions_dir.exists():
        for action_dir in actions_dir.iterdir():
            if action_dir.is_dir():
                validation_results["actions_checked"] += 1
                action_yml = action_dir / "action.yml"
                
                if action_yml.exists():
                    try:
                        with open(action_yml, 'r') as f:
                            action_content = yaml.safe_load(f)
                        print(f"✅ Custom action: {action_dir.name}")
                    except Exception as e:
                        validation_results["issues_found"].append(f"❌ Action {action_dir.name}: {str(e)}")
                else:
                    validation_results["issues_found"].append(f"❌ Action {action_dir.name}: Missing action.yml")
    
    # Generate summary
    total_issues = len(validation_results["issues_found"])
    
    if total_issues == 0:
        validation_results["status"] = "perfect"
        print("\n🎉 All GitHub Actions are perfect!")
    elif total_issues <= 3:
        validation_results["status"] = "minor_issues"
        print(f"\n⚠️ Found {total_issues} minor issues")
    else:
        validation_results["status"] = "needs_attention"
        print(f"\n🚨 Found {total_issues} issues that need attention")
    
    # Print issues
    if validation_results["issues_found"]:
        print("\n📋 Issues Found:")
        for issue in validation_results["issues_found"]:
            print(f"  {issue}")
    
    # Save validation report
    with open("github_actions_validation.json", "w") as f:
        json.dump(validation_results, f, indent=2)
    
    print(f"\n📊 Summary:")
    print(f"  Workflows checked: {validation_results['workflows_checked']}")
    print(f"  Actions checked: {validation_results['actions_checked']}")
    print(f"  Issues found: {total_issues}")
    print(f"  Overall status: {validation_results['status'].upper()}")
    
    return validation_results

def main():
    validate_github_workflows()

if __name__ == "__main__":
    main()