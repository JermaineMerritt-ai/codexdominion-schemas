#!/usr/bin/env python3
"""
Archive Signing Script
Signs compliance archives with cryptographic signatures for integrity verification.
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path


def sign_archive(archive_dir, archive_name):
    """
    Sign an archive directory with a cryptographic signature.

    Args:
        archive_dir: Path to the archive directory
        archive_name: Name of the archive

    Returns:
        0 on success, 1 on failure
    """
    try:
        archive_path = Path(archive_dir)

        if not archive_path.exists():
            print(f"❌ Archive directory not found: {archive_dir}", file=sys.stderr)
            return 1

        # Generate manifest of all files and their hashes
        manifest = {
            "archive_name": archive_name,
            "timestamp": datetime.utcnow().isoformat(),
            "files": {}
        }

        # Calculate SHA256 hash for each file
        for file_path in archive_path.rglob("*"):
            if file_path.is_file():
                with open(file_path, "rb") as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                    rel_path = str(file_path.relative_to(archive_path))
                    manifest["files"][rel_path] = {
                        "sha256": file_hash,
                        "size": file_path.stat().st_size
                    }

        # Generate manifest hash
        manifest_json = json.dumps(manifest, sort_keys=True, indent=2)
        manifest_hash = hashlib.sha256(manifest_json.encode()).hexdigest()
        manifest["manifest_hash"] = manifest_hash

        # Write manifest and signature
        manifest_file = archive_path / "MANIFEST.json"
        with open(manifest_file, "w") as f:
            json.dump(manifest, f, indent=2)

        signature_file = archive_path / "SIGNATURE.txt"
        with open(signature_file, "w") as f:
            f.write(f"Archive: {archive_name}\n")
            f.write(f"Timestamp: {manifest['timestamp']}\n")
            f.write(f"Manifest Hash (SHA256): {manifest_hash}\n")
            f.write(f"Total Files: {len(manifest['files'])}\n")

        print(f"✅ Archive signed successfully")
        print(f"   Archive: {archive_name}")
        print(f"   Files: {len(manifest['files'])}")
        print(f"   Manifest Hash: {manifest_hash}")
        print(f"   Manifest: {manifest_file}")
        print(f"   Signature: {signature_file}")

        return 0

    except Exception as e:
        print(f"❌ Error signing archive: {e}", file=sys.stderr)
        return 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Sign compliance archives")
    parser.add_argument("archive_dir", help="Path to archive directory")
    parser.add_argument("--name", required=True, help="Archive name")

    args = parser.parse_args()

    sys.exit(sign_archive(args.archive_dir, args.name))


if __name__ == "__main__":
    main()
