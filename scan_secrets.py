import os
import re

# 🔍 Directories to scan
TARGET_DIRS = [
    ".github/workflows",   # GitHub Actions workflows
    "scripts",             # Python or automation scripts
    "src",                 # Source code if secrets referenced
]

# 🧬 Regex patterns to catch secret references
PATTERNS = [
    r"\${{\s*secrets\.([A-Za-z0-9_\-]+)\s*}}",   # GitHub Actions secrets
    r"os\.getenv\([\"']([A-Za-z0-9_\-]+)[\"']\)", # Python getenv calls
]

def scan_file(filepath: str) -> list[str]:
    found: list[str] = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                content = f.read()
            except UnicodeDecodeError:
                print(f"⚠️ Skipping binary or non-UTF8 file: {filepath}")
                return found
            for pattern in PATTERNS:
                matches = re.findall(pattern, content)
                if matches:
                    found.extend(matches)
    except Exception as e:
        print(f"⚠️ Could not read {filepath}: {e}")
    return found

def main() -> None:
    all_found = {}
    scanned_files = 0
    skipped_dirs = []
    for target_dir in TARGET_DIRS:
        if not os.path.exists(target_dir):
            print(f"⚠️ Skipped missing directory: {target_dir}")
            skipped_dirs.append(target_dir)
            continue
        for root, _, files in os.walk(target_dir):
            for file in files:
                filepath = os.path.join(root, file)
                secrets = scan_file(filepath)
                scanned_files += 1
                if secrets:
                    all_found[filepath] = secrets

    print("\n🔍 Secret references found:")
    if all_found:
        for filepath, secrets in all_found.items():
            print(f"📂 {filepath}")
            for secret in secrets:
                print(f"   ➡️ {secret}")
        total_refs = sum(len(secrets) for secrets in all_found.values())
        print(f"\n📊 Found {total_refs} secret references in {len(all_found)} files.")
    else:
        print("✅ No secret references found.")

    print(f"\n📊 Scanned {scanned_files} files.")
    if skipped_dirs:
        skipped_str = ', '.join(skipped_dirs)
        print(
            f"⚠️ Skipped {len(skipped_dirs)} missing directories: {skipped_str}"
        )

    

if __name__ == "__main__":
    main()
