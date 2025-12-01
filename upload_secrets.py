

import sys
import os
import requests
import base64
import json
from nacl import encoding, public
import re
from typing import Optional, Dict, List, Tuple
import logging

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


GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN environment variable not set.")

REPOS: List[str] = [
    "jerameelart/codededominion-schema",
    "JermaineMerritt1/codedimension-schemas",
    "jermaine-merritt/codex-dominion"
]

SECRETS: Dict[str, str] = {
    "CODE_DEPEND_ON_SCHEMAS": os.getenv("CODE_DEPEND_ON_SCHEMAS", "true"),
    "SLACK_WEBHOOK_URL": os.getenv(
        "SLACK_WEBHOOK_URL",
        "https://hooks.slack.com/services/your/webhook/url"
    ),
    "Codex_Dominion_Schemas": os.getenv("CODEX_DOMINION_SCHEMAS", "true"),
    "Schemas_Dispacth_Webhook": os.getenv(
        "SCHEMAS_DISPATCH_WEBHOOK",
        "https://hooks.slack.com/services/your/dispatch/url"
    )
}

PATTERNS: List[str] = [
    r"\${{\s*secrets\.([A-Za-z0-9_\-]+)\s*}}",   # GitHub Actions secrets
    r"os\.getenv\([\"']([A-Za-z0-9_\-]+)[\"']\)",  # Python getenv calls
]

headers: Dict[str, str] = {"Authorization": f"token {GITHUB_TOKEN}"}


def get_public_key(repo: str) -> Tuple[Optional[str], Optional[str]]:
    key_url = f"https://api.github.com/repos/{repo}/actions/secrets/public-key"
    try:
        response = requests.get(key_url, headers=headers)
        response.raise_for_status()
        key_data = response.json()
        return key_data["key_id"], key_data["key"]
    except requests.RequestException as e:
        logging.error(f"Failed to get public key for {repo}: {e}")
        print(f"❌ Failed to get public key for {repo}: {e}")
        return None, None


def encrypt_secret(public_key: str, secret_value: str) -> str:
    pk = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder)
    sealed_box = public.SealedBox(pk)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")


def upload_secret(
    repo: str,
    key_id: str,
    public_key: str,
    secret_name: str,
    secret_value: str
) -> None:
    encrypted_value = encrypt_secret(public_key, secret_value)
    put_url = (
        f"https://api.github.com/repos/{repo}/actions/secrets/"
        f"{secret_name}"
    )
    payload = {"encrypted_value": encrypted_value, "key_id": key_id}
    try:
        put_response = requests.put(
            put_url,
            headers=headers,
            data=json.dumps(payload)
        )
        if put_response.status_code in [201, 204]:
            print(f"✅ Secret '{secret_name}' uploaded to {repo}")
        else:
            logging.error(
                f"Failed to upload '{secret_name}' to {repo}: "
                f"{put_response.text}"
            )
            print(
                f"❌ Failed to upload '{secret_name}' to {repo}: "
                f"{put_response.text}"
            )
    except requests.RequestException as e:
        logging.error(f"Exception uploading '{secret_name}' to {repo}: {e}")
        print(f"❌ Exception uploading '{secret_name}' to {repo}: {e}")


def verify_secrets(repo: str) -> None:
    verify_url = f"https://api.github.com/repos/{repo}/actions/secrets"
    try:
        verify_response = requests.get(verify_url, headers=headers)
        verify_response.raise_for_status()
        repo_secrets = [
            s["name"] for s in verify_response.json().get("secrets", [])
        ]
        for secret in SECRETS.keys():
            if secret in repo_secrets:
                print(f"✅ Verified: '{secret}' present in {repo}")
            else:
                print(f"⚠️ Missing: '{secret}' in {repo}")
    except requests.RequestException as e:
        logging.error(f"Failed to verify secrets for {repo}: {e}")
        print(f"❌ Failed to verify secrets for {repo}: {e}")


def scan_file(filepath: str) -> List[str]:
    found: List[str] = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            for pattern in PATTERNS:
                matches = re.findall(pattern, content)
                if matches:
                    found.extend(matches)
    except UnicodeDecodeError:
        logging.warning(f"Skipping binary or non-UTF8 file: {filepath}")
        print(f"⚠️ Skipping binary or non-UTF8 file: {filepath}")
    except Exception as e:
        logging.error(f"Could not read {filepath}: {e}")
        print(f"⚠️ Could not read {filepath}: {e}")
    return found


def scan_repo() -> Dict[str, List[str]]:
    print("\n🔍 Scanning repo for secret references...")
    TARGET_DIRS: List[str] = [".github/workflows", "scripts", "src"]
    all_found: Dict[str, List[str]] = {}
    scanned_files: int = 0
    for target_dir in TARGET_DIRS:
        if not os.path.exists(target_dir):
            logging.warning(f"Skipped missing directory: {target_dir}")
            print(f"⚠️ Skipped missing directory: {target_dir}")
            continue
        for root, _, files in os.walk(target_dir):
            for file in files:
                filepath = os.path.join(root, file)
                secrets = scan_file(filepath)
                scanned_files += 1
                if secrets:
                    all_found[filepath] = secrets
    print("\n🔍 Secret references found:")
    for filepath, secrets in all_found.items():
        print(f"📂 {filepath}")
        for secret in secrets:
            print(f"   ➡️ {secret}")
    if not all_found:
        print("✅ No secret references found.")
    print(f"\n📊 Scanned {scanned_files} files.")
    return all_found


def upload_and_verify(repo: str) -> None:
    print(f"\n🔐 Processing {repo}...")
    key_id, public_key = get_public_key(repo)
    if not key_id or not public_key:
        return
    for name, value in SECRETS.items():
        upload_secret(repo, key_id, public_key, name, value)
    verify_secrets(repo)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )
    scan_repo()
    for repo in REPOS:
        upload_and_verify(repo)
    # Enhanced error/warning scan and output formatting
    if len(sys.argv) > 1:
        project_dir = sys.argv[1]
        results = scan_files(project_dir)
        format_issues(results)
