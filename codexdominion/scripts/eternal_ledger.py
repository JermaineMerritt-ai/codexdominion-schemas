#!/usr/bin/env python3
"""
Eternal Ledger - Immutable Artifact Storage System

Provides cryptographic integrity verification and cycle replay
for all Codex Dominion artifacts with blockchain-style ledger.
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class EternalLedger:
    """Immutable ledger for artifact storage and integrity verification"""

    def __init__(self, ledger_path: str = "manifests/eternal_ledger.json"):
        self.ledger_path = Path(ledger_path)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_ledger()

    def _initialize_ledger(self) -> None:
        """Initialize the eternal ledger if it doesn't exist"""
        if not self.ledger_path.exists():
            initial_ledger = {
                "ledger_version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "genesis_hash": self._calculate_genesis_hash(),
                "artifacts": [],
                "cycles": []
            }
            self._write_ledger(initial_ledger)

    def _calculate_genesis_hash(self) -> str:
        """Calculate the genesis block hash"""
        genesis_data = {
            "ledger_name": "Codex Dominion Eternal Ledger",
            "timestamp": datetime.now().isoformat(),
            "sovereign": "Jermaine Merritt"
        }
        return hashlib.sha256(
            json.dumps(genesis_data, sort_keys=True).encode()
        ).hexdigest()

    def _read_ledger(self) -> Dict[str, Any]:
        """Read the current ledger state"""
        with open(self.ledger_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_ledger(self, ledger: Dict[str, Any]) -> None:
        """Write ledger state to disk"""
        with open(self.ledger_path, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2)

    def _calculate_artifact_hash(
        self, artifact_id: str, metadata: Dict, content_hash: str
    ) -> str:
        """Calculate the immutable hash for an artifact entry"""
        entry_data = {
            "artifact_id": artifact_id,
            "metadata": metadata,
            "content_hash": content_hash,
            "timestamp": datetime.now().isoformat()
        }
        return hashlib.sha256(
            json.dumps(entry_data, sort_keys=True).encode()
        ).hexdigest()

    def _get_previous_hash(self, ledger: Dict[str, Any]) -> str:
        """Get the hash of the previous entry (blockchain-style linking)"""
        if ledger["artifacts"]:
            return ledger["artifacts"][-1]["ledger_hash"]
        return ledger["genesis_hash"]

    def store_artifact(
        self,
        artifact_id: str,
        metadata: Dict[str, Any],
        content_hash: str
    ) -> Dict[str, Any]:
        """
        Store an artifact in the eternal ledger with cryptographic integrity

        Args:
            artifact_id: Unique identifier for the artifact
            metadata: Artifact metadata (title, version, authors, etc.)
            content_hash: SHA256 hash of the artifact content

        Returns:
            Dictionary containing the ledger entry with immutable hash
        """
        print(f"📝 STORING ARTIFACT: {artifact_id}")
        print("=" * 60)

        ledger = self._read_ledger()

        # Check if artifact already exists
        existing = next(
            (a for a in ledger["artifacts"] if a["artifact_id"] == artifact_id),
            None
        )
        if existing:
            print(f"⚠️  Artifact already exists: {artifact_id}")
            print(f"   Existing hash: {existing['ledger_hash']}")
            return existing

        # Create immutable ledger entry
        previous_hash = self._get_previous_hash(ledger)
        ledger_hash = self._calculate_artifact_hash(
            artifact_id, metadata, content_hash
        )

        entry = {
            "artifact_id": artifact_id,
            "metadata": metadata,
            "content_hash": content_hash,
            "ledger_hash": ledger_hash,
            "previous_hash": previous_hash,
            "stored_at": datetime.now().isoformat(),
            "block_number": len(ledger["artifacts"]) + 1
        }

        # Append to ledger
        ledger["artifacts"].append(entry)
        self._write_ledger(ledger)

        print(f"✅ Artifact stored in eternal ledger")
        print(f"   Block: #{entry['block_number']}")
        print(f"   Content Hash: {content_hash[:16]}...")
        print(f"   Ledger Hash: {ledger_hash[:16]}...")
        print(f"   Previous Hash: {previous_hash[:16]}...")
        print()

        return entry

    def verify_integrity(self, artifact_id: str) -> bool:
        """
        Verify the cryptographic integrity of an artifact

        Args:
            artifact_id: Unique identifier for the artifact

        Returns:
            True if integrity is verified, False otherwise
        """
        print(f"🔍 VERIFYING INTEGRITY: {artifact_id}")
        print("=" * 60)

        ledger = self._read_ledger()

        # Find artifact in ledger
        artifact = next(
            (a for a in ledger["artifacts"] if a["artifact_id"] == artifact_id),
            None
        )

        if not artifact:
            print(f"❌ Artifact not found in ledger: {artifact_id}")
            return False

        # Recalculate hash
        calculated_hash = self._calculate_artifact_hash(
            artifact["artifact_id"],
            artifact["metadata"],
            artifact["content_hash"]
        )

        # Verify hash matches
        if calculated_hash != artifact["ledger_hash"]:
            print(f"❌ INTEGRITY VIOLATION DETECTED!")
            print(f"   Expected: {artifact['ledger_hash']}")
            print(f"   Calculated: {calculated_hash}")
            return False

        # Verify chain integrity (previous hash)
        artifact_index = ledger["artifacts"].index(artifact)
        if artifact_index > 0:
            previous_artifact = ledger["artifacts"][artifact_index - 1]
            if artifact["previous_hash"] != previous_artifact["ledger_hash"]:
                print(f"❌ CHAIN INTEGRITY VIOLATION!")
                print(f"   Previous hash mismatch")
                return False
        else:
            # First artifact should link to genesis
            if artifact["previous_hash"] != ledger["genesis_hash"]:
                print(f"❌ GENESIS LINK VIOLATION!")
                return False

        print(f"✅ Integrity verified")
        print(f"   Block: #{artifact['block_number']}")
        print(f"   Hash: {artifact['ledger_hash'][:32]}...")
        print(f"   Stored: {artifact['stored_at']}")
        print()

        return True

    def replay_cycle(self, cycle_id: str) -> List[Dict[str, Any]]:
        """
        Replay all artifacts from a specific cycle

        Args:
            cycle_id: Cycle identifier (ISO timestamp or cycle number)

        Returns:
            List of artifacts from the specified cycle
        """
        print(f"🔄 REPLAYING CYCLE: {cycle_id}")
        print("=" * 60)

        ledger = self._read_ledger()

        # Find artifacts matching cycle
        cycle_artifacts = []
        for artifact in ledger["artifacts"]:
            metadata = artifact["metadata"]
            if metadata.get("cycle") == cycle_id:
                cycle_artifacts.append(artifact)

        if not cycle_artifacts:
            print(f"⚠️  No artifacts found for cycle: {cycle_id}")
            return []

        print(f"📋 Found {len(cycle_artifacts)} artifacts in cycle")
        print()

        # Verify and display each artifact
        for artifact in cycle_artifacts:
            print(f"🔹 {artifact['artifact_id']}")
            print(f"   Title: {artifact['metadata'].get('title', 'N/A')}")
            print(f"   Block: #{artifact['block_number']}")
            print(f"   Hash: {artifact['ledger_hash'][:32]}...")

            # Verify integrity during replay
            is_valid = self.verify_integrity(artifact["artifact_id"])
            if not is_valid:
                print(f"   ⚠️  INTEGRITY CHECK FAILED")
            print()

        # Record cycle replay in ledger
        cycle_entry = {
            "cycle_id": cycle_id,
            "replayed_at": datetime.now().isoformat(),
            "artifact_count": len(cycle_artifacts),
            "artifacts": [a["artifact_id"] for a in cycle_artifacts]
        }
        ledger["cycles"].append(cycle_entry)
        self._write_ledger(ledger)

        print(f"✅ Cycle replay complete")
        print(f"   Artifacts: {len(cycle_artifacts)}")
        print()

        return cycle_artifacts

    def get_ledger_stats(self) -> Dict[str, Any]:
        """Get statistics about the eternal ledger"""
        ledger = self._read_ledger()

        return {
            "total_artifacts": len(ledger["artifacts"]),
            "total_cycles": len(ledger["cycles"]),
            "genesis_hash": ledger["genesis_hash"],
            "created_at": ledger["created_at"],
            "latest_block": (
                ledger["artifacts"][-1]["block_number"]
                if ledger["artifacts"] else 0
            ),
            "latest_artifact": (
                ledger["artifacts"][-1]["artifact_id"]
                if ledger["artifacts"] else None
            )
        }

    def verify_full_chain(self) -> bool:
        """Verify the integrity of the entire ledger chain"""
        print("🔗 VERIFYING FULL CHAIN INTEGRITY")
        print("=" * 60)

        ledger = self._read_ledger()

        if not ledger["artifacts"]:
            print("✅ Empty ledger (valid)")
            return True

        # Verify each artifact
        for i, artifact in enumerate(ledger["artifacts"]):
            artifact_id = artifact["artifact_id"]
            print(f"Verifying block #{i + 1}: {artifact_id}...", end=" ")

            if not self.verify_integrity(artifact_id):
                print("❌ FAILED")
                return False

            print("✅")

        print()
        print("✅ FULL CHAIN INTEGRITY VERIFIED")
        print(f"   Total blocks: {len(ledger['artifacts'])}")
        print()

        return True


def main() -> None:
    """Main execution for testing"""
    print("🔥 ETERNAL LEDGER SYSTEM")
    print("=" * 60)
    print()

    ledger = EternalLedger()

    # Display stats
    stats = ledger.get_ledger_stats()
    print("📊 LEDGER STATISTICS")
    print(f"   Total Artifacts: {stats['total_artifacts']}")
    print(f"   Total Cycles: {stats['total_cycles']}")
    print(f"   Genesis Hash: {stats['genesis_hash'][:32]}...")
    print(f"   Latest Block: #{stats['latest_block']}")
    print()

    # Verify full chain
    ledger.verify_full_chain()


if __name__ == "__main__":
    main()
