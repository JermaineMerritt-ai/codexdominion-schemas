import os
import re

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


def format_issues(issues: dict) -> None:
    if not issues:
        print("✅ No issues detected!")
        return
    print("\nIssues Found:")
    for file, problems in issues.items():
        print(f"\n📄 {file}:")
        for problem in problems:
            if problem.startswith("ERROR"):
                print(f"  ❌ {problem}")
            elif problem.startswith("WARNING"):
                print(f"  ⚠️ {problem}")
            else:
                print(f"  - {problem}")
    print("\n✅ Suggested Fixes:")
    print("- Run dependency installer (npm install / pip install)")
    print("- Check config files for missing values")
    print("- Update deprecated code")


def main():
    project_dir = os.getcwd()
    results = scan_files(project_dir)
    format_issues(results)


if __name__ == "__main__":
    main()
