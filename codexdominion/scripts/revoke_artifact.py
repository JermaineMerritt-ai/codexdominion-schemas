#!/usr/bin/env python3
"""
Codex Dominion Artifact Revocation System

Implements sovereign control over artifact distribution.
Allows revocation by Sovereign Avatar with immutable ledger entry.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class ArtifactRevocationEngine:
    """Manage artifact revocation with sovereign control"""

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.revocation_ledger = (
            self.root_dir / "manifests" / "revocations.json"
        )
        self._ensure_ledger()

    def _ensure_ledger(self) -> None:
        """Ensure revocation ledger exists"""
        if not self.revocation_ledger.exists():
            self.revocation_ledger.parent.mkdir(parents=True, exist_ok=True)
            initial_ledger = {
                "ledger_version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "revocations": []
            }
            with open(self.revocation_ledger, "w", encoding="utf-8") as f:
                json.dump(initial_ledger, f, indent=2)

    def revoke_artifact(
        self,
        artifact_id: str,
        by: str,
        reason: str,
        replacement_artifact_id: Optional[str] = None
    ) -> Dict:
        """Revoke an artifact with sovereign authority"""
        print(f"🔐 REVOKING ARTIFACT: {artifact_id}")
        print("=" * 60)

        # Load current ledger
        with open(self.revocation_ledger, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        # Create revocation entry
        revocation = {
            "artifactId": artifact_id,
            "revoked": True,
            "revocation": {
                "by": by,
                "at": datetime.now().isoformat(),
                "reason": reason
            }
        }

        if replacement_artifact_id:
            revocation["revocation"]["replacementArtifactId"] = (
                replacement_artifact_id
            )

        # Add to ledger
        ledger["revocations"].append(revocation)

        # Write updated ledger
        with open(self.revocation_ledger, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2)

        print("✅ Revocation recorded in immutable ledger")
        print(f"   By: {by}")
        print(f"   Reason: {reason}")
        if replacement_artifact_id:
            print(f"   Replacement: {replacement_artifact_id}")

        # Update artifact metadata
        self._mark_artifact_revoked(artifact_id, revocation)

        return revocation

    def _mark_artifact_revoked(
        self, artifact_id: str, revocation: Dict
    ) -> None:
        """Mark artifact as revoked in its metadata"""
        # Find artifact.json file
        capsules_dir = self.root_dir / "capsules"

        for capsule_dir in capsules_dir.iterdir():
            if capsule_dir.is_dir():
                artifact_file = capsule_dir / "artifact.json"

                if artifact_file.exists():
                    with open(artifact_file, "r", encoding="utf-8") as f:
                        artifact = json.load(f)

                    if artifact.get("artifactId") == artifact_id:
                        # Add revocation to artifact
                        artifact["revoked"] = True
                        artifact["revocation"] = revocation["revocation"]

                        # Write updated artifact
                        with open(artifact_file, "w", encoding="utf-8") as f:
                            json.dump(artifact, f, indent=2)

                        print(f"   Updated: {artifact_file}")
                        return

        print(f"   ⚠️  Artifact metadata not found: {artifact_id}")

    def check_revocation(self, artifact_id: str) -> Optional[Dict[str, Any]]:
        """Check if an artifact has been revoked"""
        with open(self.revocation_ledger, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        for revocation in ledger["revocations"]:
            if revocation["artifactId"] == artifact_id:
                return revocation

        return None

    def list_revocations(self) -> None:
        """List all revoked artifacts"""
        print("\n📋 REVOCATION LEDGER")
        print("=" * 60)

        with open(self.revocation_ledger, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        if not ledger["revocations"]:
            print("No revocations recorded")
            return

        for rev in ledger["revocations"]:
            print(f"\n🔒 {rev['artifactId']}")
            print(f"   By: {rev['revocation']['by']}")
            print(f"   At: {rev['revocation']['at']}")
            print(f"   Reason: {rev['revocation']['reason']}")
            if "replacementArtifactId" in rev["revocation"]:
                print(
                    f"   Replacement: "
                    f"{rev['revocation']['replacementArtifactId']}"
                )


def main() -> None:
    """Main execution"""
    print("🔥 CODEX DOMINION ARTIFACT REVOCATION SYSTEM")
    print("=" * 60)
    print()

    engine = ArtifactRevocationEngine()

    # Example: Revoke eternal-ledger-001
    revocation = engine.revoke_artifact(
        artifact_id="eternal-ledger-001",
        by="Sovereign Avatar",
        reason="Superseded by v1.0.1",
        replacement_artifact_id="eternal-ledger-101"
    )

    print("\n" + "=" * 60)
    print("✅ SOVEREIGN REVOCATION COMPLETE")
    print("=" * 60)
    print()
    print("📋 Revocation Details:")
    print(json.dumps(revocation, indent=2))
    print()
    print("🔐 Immutable ledger entry created")
    print("✨ Distribution consent revoked")
    print()


if __name__ == "__main__":
    main()
