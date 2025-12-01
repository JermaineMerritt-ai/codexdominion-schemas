import requests
import base64
import json
from nacl import encoding, public

# 🔐 Your GitHub Personal Access Token
GITHUB_TOKEN = "ghp_your_actual_token_here"

# 🧭 Repositories to target
REPOS = [
    "jerameelart/codededominion-schema",
    "JermaineMerritt1/codedimension-schemas",
    "jermaine-merritt/codex-dominion"
]

# 🧬 Secrets to upload
SECRETS = {
    "Codex_Dominion_Schemas": "true",
    "Schemas_Dispacth_Webhook": "https://hooks.slack.com/services/your/webhook/url"
}

def encrypt(public_key: str, secret_value: str) -> str:
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")

# 🔁 Upload loop
for repo in REPOS:
    print(f"🔐 Uploading secrets to {repo}...")

    # Get public key for encryption
    key_url = f"https://api.github.com/repos/{repo}/actions/secrets/public-key"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(key_url, headers=headers)
    key_data = response.json()

    if "key" not in key_data:
        print(f"❌ Failed to get public key for {repo}")
        continue

    key_id = key_data["key_id"]
    public_key = key_data["key"]

    for name, value in SECRETS.items():
        encrypted_value = encrypt(public_key, value)

        # Upload secret
        put_url = f"https://api.github.com/repos/{repo}/actions/secrets/{name}"
        payload = {
            "encrypted_value": encrypted_value,
            "key_id": key_id
        }
        put_response = requests.put(put_url, headers=headers, data=json.dumps(payload))

        if put_response.status_code in (201, 204):
            print(f"✅ Secret '{name}' uploaded to {repo}")
        else:
            print(f"❌ Failed to upload '{name}' to {repo}: {put_response.text}")
