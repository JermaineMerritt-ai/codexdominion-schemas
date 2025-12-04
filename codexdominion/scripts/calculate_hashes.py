#!/usr/bin/env python3
"""
Codex Dominion Artifact Hash Calculator

Calculates SHA256 hashes for artifact files and updates artifact.json metadata.
Ensures immutable audit trail for all syndicated artifacts.
"""

import hashlib
import json
from pathlib import Path
from typing import Dict, List


class ArtifactHasher:
    """Calculate and update artifact hashes"""

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.capsules_dir = self.root_dir / "capsules"

    def calculate_sha256(self, file_path: Path) -> str:
        """Calculate SHA256 hash of a file"""
        sha256_hash = hashlib.sha256()

        if not file_path.exists():
            return "FILE_NOT_FOUND"

        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        return sha256_hash.hexdigest()

    def get_file_size(self, file_path: Path) -> int:
        """Get file size in bytes"""
        if not file_path.exists():
            return 0
        return file_path.stat().st_size

    def update_artifact_metadata(self, artifact_json_path: Path) -> bool:
        """Update artifact.json with file hashes and sizes"""
        if not artifact_json_path.exists():
            print(f"⚠️  Artifact metadata not found: {artifact_json_path}")
            return False

        with open(artifact_json_path, "r", encoding="utf-8") as f:
            artifact = json.load(f)

        print(f"\n🔍 Processing: {artifact['title']}")

        updated = False
        for file_entry in artifact.get("files", []):
            file_path = self.root_dir / file_entry["path"]

            # Calculate hash
            sha256 = self.calculate_sha256(file_path)
            file_size = self.get_file_size(file_path)

            if sha256 != "FILE_NOT_FOUND":
                print(f"  ✅ {file_path.name}")
                print(f"     SHA256: {sha256[:16]}...{sha256[-16:]}")
                print(f"     Size: {file_size:,} bytes")

                file_entry["sha256"] = sha256
                file_entry["bytes"] = file_size
                updated = True
            else:
                print(f"  ⚠️  {file_path.name} - Not found")
                file_entry["sha256"] = "FILE_NOT_FOUND"
                file_entry["bytes"] = 0

        # Calculate immutable hash for entire artifact
        artifact_string = json.dumps(artifact, sort_keys=True)
        immutable_hash = hashlib.sha256(
            artifact_string.encode()
        ).hexdigest()

        artifact["audit"]["immutableHash"] = immutable_hash
        hash_short = f"{immutable_hash[:16]}...{immutable_hash[-16:]}"
        print(f"  🔐 Artifact Hash: {hash_short}")

        # Write updated artifact.json
        if updated:
            with open(artifact_json_path, "w", encoding="utf-8") as f:
                json.dump(artifact, f, indent=2)
            print(f"  💾 Updated: {artifact_json_path.name}")

        return updated

    def hash_all_artifacts(self) -> List[Dict]:
        """Process all artifact.json files in capsules"""
        print("🔥 CODEX DOMINION ARTIFACT HASHER")
        print("=" * 60)

        artifact_files = list(self.capsules_dir.glob("*/artifact.json"))

        if not artifact_files:
            print("⚠️  No artifact.json files found in capsules/")
            return []

        print(f"📋 Found {len(artifact_files)} artifacts")

        results = []
        for artifact_json in artifact_files:
            success = self.update_artifact_metadata(artifact_json)
            results.append({
                "path": artifact_json,
                "success": success
            })

        successful = sum(1 for r in results if r["success"])
        print(f"\n✅ Processed: {successful}/{len(results)} artifacts")

        return results


def main():
    """Main execution"""
    hasher = ArtifactHasher()

    try:
        results = hasher.hash_all_artifacts()

        print("\n🔐 HASH CALCULATION COMPLETE")
        print("-" * 60)
        print("All artifact metadata updated with:")
        print("  • SHA256 file hashes")
        print("  • File sizes in bytes")
        print("  • Immutable artifact hashes")
        print("\n✨ Artifacts ready for secure syndication!")

    except Exception as e:
        print(f"\n❌ Hash calculation failed: {e}")
        raise


if __name__ == "__main__":
    main()
