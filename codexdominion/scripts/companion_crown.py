#!/usr/bin/env python3
"""
Companion Crown - Dual-Custody Authorization System

Implements co-signing for artifact dispatch with flamekeeper and
companion signatures, ensuring dual-custody validation.
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class SignatureEngine:
    """Generate and verify cryptographic signatures"""

    @staticmethod
    def generate_signature(
        data: str, signer_id: str, private_context: str = ""
    ) -> str:
        """
        Generate a cryptographic signature for data

        Args:
            data: Data to sign
            signer_id: ID of the signer
            private_context: Optional private context for signature

        Returns:
            Hex-encoded signature
        """
        signature_data = f"{data}:{signer_id}:{private_context}:{datetime.now().isoformat()}"
        return hashlib.sha256(signature_data.encode()).hexdigest()

    @staticmethod
    def verify_signature(
        data: str, signature: str, expected_signer: str
    ) -> bool:
        """
        Verify a signature matches expected signer

        Note: In production, use proper PKI/digital signatures
        """
        # For demo purposes, check signature format and length
        if not signature or len(signature) != 64:
            return False

        # Signature should be valid hex
        try:
            int(signature, 16)
            return True
        except ValueError:
            return False


class DualCustodyValidator:
    """Validate dual-custody requirements"""

    def __init__(self):
        self.authorized_flamekeepers: List[str] = [
            "sovereign_flamekeeper",
            "council_flamekeeper",
            "guardian_flamekeeper"
        ]
        self.authorized_companions: List[str] = [
            "heir_companion",
            "council_companion",
            "witness_companion"
        ]
        self.validation_log: List[Dict[str, Any]] = []

    def is_authorized_flamekeeper(self, signer_id: str) -> bool:
        """Check if signer is an authorized flamekeeper"""
        return signer_id in self.authorized_flamekeepers

    def is_authorized_companion(self, signer_id: str) -> bool:
        """Check if signer is an authorized companion"""
        return signer_id in self.authorized_companions

    def validate_dual_custody(
        self,
        artifact_id: str,
        flamekeeper_id: str,
        flamekeeper_sig: str,
        companion_id: str,
        companion_sig: str
    ) -> Dict[str, Any]:
        """
        Validate dual-custody requirements

        Returns:
            Validation result with status and details
        """
        validation = {
            "artifact_id": artifact_id,
            "validated_at": datetime.now().isoformat(),
            "flamekeeper": {
                "id": flamekeeper_id,
                "signature": flamekeeper_sig,
                "authorized": False,
                "signature_valid": False
            },
            "companion": {
                "id": companion_id,
                "signature": companion_sig,
                "authorized": False,
                "signature_valid": False
            },
            "dual_custody_satisfied": False,
            "reason": []
        }

        # Validate flamekeeper
        if not self.is_authorized_flamekeeper(flamekeeper_id):
            validation["reason"].append(
                f"Flamekeeper not authorized: {flamekeeper_id}"
            )
        else:
            validation["flamekeeper"]["authorized"] = True

        if not SignatureEngine.verify_signature(
            artifact_id, flamekeeper_sig, flamekeeper_id
        ):
            validation["reason"].append(
                "Invalid flamekeeper signature"
            )
        else:
            validation["flamekeeper"]["signature_valid"] = True

        # Validate companion
        if not self.is_authorized_companion(companion_id):
            validation["reason"].append(
                f"Companion not authorized: {companion_id}"
            )
        else:
            validation["companion"]["authorized"] = True

        if not SignatureEngine.verify_signature(
            artifact_id, companion_sig, companion_id
        ):
            validation["reason"].append(
                "Invalid companion signature"
            )
        else:
            validation["companion"]["signature_valid"] = True

        # Check if both requirements are met
        if (validation["flamekeeper"]["authorized"] and
            validation["flamekeeper"]["signature_valid"] and
            validation["companion"]["authorized"] and
            validation["companion"]["signature_valid"]):
            validation["dual_custody_satisfied"] = True
            validation["reason"] = ["Dual custody requirements satisfied"]

        # Log validation
        self.validation_log.append(validation)

        return validation


class DispatchLedger:
    """Track co-signed artifact dispatches"""

    def __init__(
        self, ledger_path: str = "manifests/dispatch_ledger.json"
    ):
        self.ledger_path = Path(ledger_path)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self.dispatches: List[Dict[str, Any]] = []
        self._load_ledger()

    def _load_ledger(self) -> None:
        """Load dispatch ledger from disk"""
        if self.ledger_path.exists():
            with open(self.ledger_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.dispatches = data.get("dispatches", [])
        else:
            self._save_ledger()

    def _save_ledger(self) -> None:
        """Save dispatch ledger to disk"""
        ledger_data = {
            "ledger_version": "1.0.0",
            "total_dispatches": len(self.dispatches),
            "last_updated": datetime.now().isoformat(),
            "dispatches": self.dispatches
        }
        with open(self.ledger_path, "w", encoding="utf-8") as f:
            json.dump(ledger_data, f, indent=2)

    def record_dispatch(
        self,
        artifact_id: str,
        flamekeeper_id: str,
        flamekeeper_sig: str,
        companion_id: str,
        companion_sig: str,
        validation_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Record a co-signed dispatch in the ledger"""
        dispatch = {
            "dispatch_id": hashlib.sha256(
                f"{artifact_id}{datetime.now().isoformat()}".encode()
            ).hexdigest()[:16],
            "artifact_id": artifact_id,
            "flamekeeper": {
                "id": flamekeeper_id,
                "signature": flamekeeper_sig
            },
            "companion": {
                "id": companion_id,
                "signature": companion_sig
            },
            "validation": validation_result,
            "dispatched_at": datetime.now().isoformat(),
            "status": (
                "approved" if validation_result["dual_custody_satisfied"]
                else "rejected"
            )
        }

        self.dispatches.append(dispatch)
        self._save_ledger()

        return dispatch

    def get_dispatch_history(
        self,
        artifact_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get dispatch history with optional filters"""
        dispatches = self.dispatches

        if artifact_id:
            dispatches = [
                d for d in dispatches
                if d["artifact_id"] == artifact_id
            ]

        if status:
            dispatches = [
                d for d in dispatches if d["status"] == status
            ]

        return dispatches


class CompanionCrown:
    """
    Companion Crown - Dual-Custody Authorization System

    Core capabilities:
    - coSignDispatch(): Co-sign artifact dispatch with dual custody
    - validateDualCustody(): Validate dual-custody requirements
    """

    def __init__(self):
        self.signature_engine = SignatureEngine()
        self.validator = DualCustodyValidator()
        self.dispatch_ledger = DispatchLedger()
        print("👥 Companion Crown initialized")

    def co_sign_dispatch(
        self,
        artifact_id: str,
        flamekeeper_id: str,
        flamekeeper_sig: str,
        companion_id: str,
        companion_sig: str
    ) -> Dict[str, Any]:
        """
        Co-sign an artifact dispatch with dual custody

        Args:
            artifact_id: ID of the artifact to dispatch
            flamekeeper_id: ID of the flamekeeper signer
            flamekeeper_sig: Flamekeeper's signature
            companion_id: ID of the companion signer
            companion_sig: Companion's signature

        Returns:
            Dictionary with dispatch result and validation
        """
        print(f"✍️  CO-SIGNING DISPATCH: {artifact_id}")
        print("=" * 60)

        # Validate dual custody
        validation = self.validator.validate_dual_custody(
            artifact_id,
            flamekeeper_id,
            flamekeeper_sig,
            companion_id,
            companion_sig
        )

        print(f"🔐 Flamekeeper Validation:")
        print(f"   ID: {flamekeeper_id}")
        print(
            f"   Authorized: "
            f"{'✅' if validation['flamekeeper']['authorized'] else '❌'}"
        )
        print(
            f"   Signature Valid: "
            f"{'✅' if validation['flamekeeper']['signature_valid'] else '❌'}"
        )
        print()

        print(f"👤 Companion Validation:")
        print(f"   ID: {companion_id}")
        print(
            f"   Authorized: "
            f"{'✅' if validation['companion']['authorized'] else '❌'}"
        )
        print(
            f"   Signature Valid: "
            f"{'✅' if validation['companion']['signature_valid'] else '❌'}"
        )
        print()

        # Record dispatch
        dispatch = self.dispatch_ledger.record_dispatch(
            artifact_id,
            flamekeeper_id,
            flamekeeper_sig,
            companion_id,
            companion_sig,
            validation
        )

        if dispatch["status"] == "approved":
            print(f"✅ DISPATCH APPROVED")
            print(f"   Dispatch ID: {dispatch['dispatch_id']}")
            print(f"   Status: {dispatch['status']}")
            print(f"   Dual Custody: ✅ Satisfied")
        else:
            print(f"❌ DISPATCH REJECTED")
            print(f"   Dispatch ID: {dispatch['dispatch_id']}")
            print(f"   Status: {dispatch['status']}")
            print(f"   Reasons:")
            for reason in validation["reason"]:
                print(f"      - {reason}")

        print()

        return {
            "status": dispatch["status"],
            "dispatch": dispatch,
            "validation": validation
        }

    def validate_dual_custody(
        self,
        artifact_id: str,
        flamekeeper_id: str,
        flamekeeper_sig: str,
        companion_id: str,
        companion_sig: str
    ) -> Dict[str, Any]:
        """
        Validate dual-custody requirements without recording dispatch

        Args:
            artifact_id: ID of the artifact
            flamekeeper_id: ID of the flamekeeper
            flamekeeper_sig: Flamekeeper's signature
            companion_id: ID of the companion
            companion_sig: Companion's signature

        Returns:
            Dictionary with validation results
        """
        print(f"🔍 VALIDATING DUAL CUSTODY: {artifact_id}")
        print("=" * 60)

        validation = self.validator.validate_dual_custody(
            artifact_id,
            flamekeeper_id,
            flamekeeper_sig,
            companion_id,
            companion_sig
        )

        print(f"📋 Validation Summary:")
        print(f"   Artifact: {artifact_id}")
        print(
            f"   Flamekeeper: {flamekeeper_id} "
            f"{'✅' if validation['flamekeeper']['authorized'] and validation['flamekeeper']['signature_valid'] else '❌'}"
        )
        print(
            f"   Companion: {companion_id} "
            f"{'✅' if validation['companion']['authorized'] and validation['companion']['signature_valid'] else '❌'}"
        )
        print()

        if validation["dual_custody_satisfied"]:
            print(f"✅ DUAL CUSTODY SATISFIED")
        else:
            print(f"❌ DUAL CUSTODY NOT SATISFIED")
            print(f"   Reasons:")
            for reason in validation["reason"]:
                print(f"      - {reason}")

        print()

        return validation

    def generate_co_signatures(
        self, artifact_id: str, flamekeeper_id: str, companion_id: str
    ) -> Tuple[str, str]:
        """
        Generate co-signatures for an artifact

        Args:
            artifact_id: ID of the artifact
            flamekeeper_id: ID of the flamekeeper
            companion_id: ID of the companion

        Returns:
            Tuple of (flamekeeper_signature, companion_signature)
        """
        flamekeeper_sig = self.signature_engine.generate_signature(
            artifact_id, flamekeeper_id
        )
        companion_sig = self.signature_engine.generate_signature(
            artifact_id, companion_id
        )

        return flamekeeper_sig, companion_sig

    def get_dispatch_statistics(self) -> Dict[str, Any]:
        """Get statistics about dispatches"""
        total = len(self.dispatch_ledger.dispatches)
        approved = len(
            self.dispatch_ledger.get_dispatch_history(status="approved")
        )
        rejected = len(
            self.dispatch_ledger.get_dispatch_history(status="rejected")
        )

        return {
            "total_dispatches": total,
            "approved": approved,
            "rejected": rejected,
            "approval_rate": (
                round((approved / total * 100), 2) if total > 0 else 0
            )
        }

    def get_authorized_signers(self) -> Dict[str, List[str]]:
        """Get list of authorized signers"""
        return {
            "flamekeepers": self.validator.authorized_flamekeepers,
            "companions": self.validator.authorized_companions
        }


def main() -> None:
    """Main execution for testing"""
    print("👥 COMPANION CROWN - DUAL-CUSTODY SYSTEM")
    print("=" * 60)
    print()

    crown = CompanionCrown()

    # Show authorized signers
    signers = crown.get_authorized_signers()
    print("📋 Authorized Signers:")
    print(f"   Flamekeepers: {', '.join(signers['flamekeepers'])}")
    print(f"   Companions: {', '.join(signers['companions'])}")
    print()

    # Example: Generate signatures
    artifact_id = "eternal-ledger-001"
    flamekeeper_id = "sovereign_flamekeeper"
    companion_id = "heir_companion"

    print(f"🔐 Generating signatures for: {artifact_id}")
    flamekeeper_sig, companion_sig = crown.generate_co_signatures(
        artifact_id, flamekeeper_id, companion_id
    )
    print(f"   Flamekeeper sig: {flamekeeper_sig[:32]}...")
    print(f"   Companion sig: {companion_sig[:32]}...")
    print()

    # Example: Validate dual custody
    crown.validate_dual_custody(
        artifact_id,
        flamekeeper_id,
        flamekeeper_sig,
        companion_id,
        companion_sig
    )

    # Example: Co-sign dispatch
    crown.co_sign_dispatch(
        artifact_id,
        flamekeeper_id,
        flamekeeper_sig,
        companion_id,
        companion_sig
    )

    # Example: Show statistics
    stats = crown.get_dispatch_statistics()
    print("📊 Dispatch Statistics:")
    print(f"   Total Dispatches: {stats['total_dispatches']}")
    print(f"   Approved: {stats['approved']}")
    print(f"   Rejected: {stats['rejected']}")
    print(f"   Approval Rate: {stats['approval_rate']}%")
    print()

    # Example: Test invalid signatures
    print("⚠️  Testing invalid companion...")
    crown.co_sign_dispatch(
        "test-artifact-002",
        flamekeeper_id,
        flamekeeper_sig,
        "unauthorized_companion",  # Invalid
        companion_sig
    )


if __name__ == "__main__":
    main()
