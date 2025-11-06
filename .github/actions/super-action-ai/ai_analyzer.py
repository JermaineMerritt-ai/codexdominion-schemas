#!/usr/bin/env python3
"""
Super Action AI - AI Analyzer
Performs intelligent code analysis for Codex deployments.
"""

import os
import json
import subprocess
from datetime import datetime

def analyze_codebase():
    """Perform AI-powered analysis of the codebase."""
    print("🤖 Super Action AI Analyzer starting...")
    
    analysis = {
        "timestamp": datetime.now().isoformat(),
        "status": "analyzing",
        "findings": [],
        "recommendations": [],
        "score": 0
    }
    
    # Check for common issues
    try:
        # Check for Python syntax errors
        result = subprocess.run(['python', '-m', 'py_compile', 'codex-integration/'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            analysis["findings"].append("✅ Python syntax validation passed")
            analysis["score"] += 25
        else:
            analysis["findings"].append("❌ Python syntax errors detected")
            
    except Exception as e:
        analysis["findings"].append(f"⚠️ Analysis error: {str(e)}")
    
    # Check for security patterns
    security_patterns = [
        "password", "secret", "key", "token", "api_key"
    ]
    
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(('.py', '.yaml', '.yml')):
                try:
                    with open(os.path.join(root, file), 'r') as f:
                        content = f.read().lower()
                        for pattern in security_patterns:
                            if pattern in content and "secret" in content:
                                analysis["findings"].append(f"🔒 Potential secret in {file}")
                except:
                    pass
    
    # Generate recommendations
    if analysis["score"] >= 80:
        analysis["recommendations"].append("🎉 Codebase ready for deployment")
    elif analysis["score"] >= 60:
        analysis["recommendations"].append("⚠️ Minor issues detected, proceed with caution")
    else:
        analysis["recommendations"].append("🚫 Major issues detected, review required")
    
    analysis["status"] = "complete"
    
    # Save analysis results
    with open("ai_analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)
    
    print(f"📊 Analysis complete. Score: {analysis['score']}/100")
    return analysis

def main():
    analysis = analyze_codebase()
    
    # Set GitHub Actions outputs
    if os.getenv("GITHUB_ACTIONS"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"ai_recommendations={json.dumps(analysis['recommendations'])}\n")
            f.write(f"analysis_score={analysis['score']}\n")

if __name__ == "__main__":
    main()