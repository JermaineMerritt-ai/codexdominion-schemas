#!/usr/bin/env python3.11
import argparse
import base64
import datetime
import hashlib
import json
import os
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def write_checksums(root, out_path):
    entries = []
    for p in sorted(Path(root).rglob("*")):
        if p.is_file() and p.name not in ("CHECKSUMS.txt", "SIGNATURE.txt"):
            entries.append(f"{sha256_file(p)}  {p.relative_to(root).as_posix()}")
    Path(out_path).write_text("\n".join(entries) + "\n", encoding="utf-8")
    return entries

def write_manifest(root, out_path, entries):
    files = []
    for line in entries:
        digest, rel = line.split("  ", 1)
        full = Path(root) / rel
        files.append({"path": rel, "size_bytes": full.stat().st_size, "sha256": digest})
    manifest = {
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "file_count": len(files),
        "files": files,
    }
    Path(out_path).write_text(json.dumps(manifest, indent=2), encoding="utf-8")

def sign_checksums(checksums_path, key_path, out_sig, armor=True):
    private_key = serialization.load_pem_private_key(
        Path(key_path).read_bytes(), password=os.environ.get("COMPLIANCE_KEY_PASS", "").encode() or None
    )
    data = Path(checksums_path).read_bytes()
    signature = private_key.sign(
        data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    if armor:
        armored = "-----BEGIN SIGNATURE-----\n" + base64.b64encode(signature).decode() + "\n-----END SIGNATURE-----\n"
        Path(out_sig).write_text(armored, encoding="utf-8")
    else:
        Path(out_sig).write_bytes(signature)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive-root", required=True, help="Path to archive directory")
    ap.add_argument("--key", required=True, help="PEM private key path")
    ap.add_argument("--out-checksums", default="CHECKSUMS.txt")
    ap.add_argument("--out-manifest", default="MANIFEST.json")
    ap.add_argument("--out-signature", default="SIGNATURE.txt")
    args = ap.parse_args()

    root = Path(args.archive_root)
    entries = write_checksums(root, root / args.out_checksums)
    write_manifest(root, root / args.out_manifest, entries)
    sign_checksums(root / args.out_checksums, args.key, root / args.out_signature)
    print(f"Archive sealed: {root}")
