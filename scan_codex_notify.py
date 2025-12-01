import os
import requests
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

ERROR_PATTERNS = ["missing dependency", "syntax error", "failed build"]
WARNING_PATTERNS = ["deprecated", "performance issue", "config mismatch"]


def scan_files(directory: str) -> dict:
    issues = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".log", ".txt", ".json", ".yaml")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", errors="ignore") as f:
                        content = f.read().lower()
                        file_issues = []
                        for pattern in ERROR_PATTERNS:
                            if pattern in content:
                                file_issues.append(f"ERROR: {pattern}")
                        for pattern in WARNING_PATTERNS:
                            if pattern in content:
                                file_issues.append(f"WARNING: {pattern}")
                        if file_issues:
                            issues[path] = file_issues
                except Exception as e:
                    print(f"⚠️ Could not read {path}: {e}")
    return issues


def auto_fix() -> None:
    print("🔧 Attempting auto-fix...")
    try:
        if os.path.exists("package.json"):
            subprocess.run(["npm", "install"], check=True)
        if os.path.exists("requirements.txt"):
            subprocess.run([
                "pip", "install", "-r", "requirements.txt"
            ], check=True)
        print("✅ Auto-fix completed!")
    except Exception as e:
        print(f"❌ Auto-fix failed: {e}")


def notify_slack(message: str) -> None:
    if SLACK_WEBHOOK_URL:
        payload = {"text": message}
        try:
            response = requests.post(SLACK_WEBHOOK_URL, json=payload)
            response.raise_for_status()
            print("✅ Slack notification sent!")
        except Exception as e:
            print(f"❌ Slack notification failed: {e}")
    else:
        print("⚠️ Slack webhook URL not configured.")


def main() -> None:
    project_dir = os.getcwd()
    results = scan_files(project_dir)
    if results:
        issue_lines = []
        for file, problems in results.items():
            line = f"{file}: {', '.join(problems)}"
            issue_lines.append(line)
        issue_summary = "\n".join(issue_lines)
        print("\nIssues Found:\n", issue_summary)
        auto_fix()
        summary = (
            "Codex Dominion Scan: Issues detected!\n" + issue_summary[:500]
        )
        notify_slack(summary)
    else:
        print("✅ No issues detected!")
        notify_slack("Codex Dominion Scan: No issues detected!")


if __name__ == "__main__":
    main()
