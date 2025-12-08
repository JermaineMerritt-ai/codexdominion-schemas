"""
Digital Seal Service - Cryptographic signing for Codex Dominion exports
Implements SHA-256 + RSA/ECC signatures bound to Custodian and Council keys
"""

import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding, ec
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
import base64


class CouncilSeal:
    """Represents a Council member's digital seal (certificate)"""

    def __init__(
        self,
        member_id: str,
        member_name: str,
        role: str,
        public_key: bytes,
        private_key: Optional[bytes] = None,
        seal_type: str = "RSA-2048"
    ):
        self.member_id = member_id
        self.member_name = member_name
        self.role = role
        self.public_key = public_key
        self.private_key = private_key
        self.seal_type = seal_type
        self.created_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Export seal metadata (without private key)"""
        return {
            "member_id": self.member_id,
            "member_name": self.member_name,
            "role": self.role,
            "seal_type": self.seal_type,
            "public_key": base64.b64encode(self.public_key).decode('utf-8'),
            "created_at": self.created_at
        }


class DigitalSealService:
    """
    Cryptographic signing service for Codex Dominion exports

    Features:
    - SHA-256 content hashing
    - RSA-2048 or ECC P-256 signatures
    - Multi-signature covenant support
    - Custodian master key
    - Council member seals
    - Immutable ledger integration
    """

    def __init__(self, custodian_name: str = "Jermaine Merritt"):
        self.custodian_name = custodian_name
        self.custodian_key = None
        self.custodian_public_key = None
        self.council_seals: Dict[str, CouncilSeal] = {}
        self.signature_ledger: List[Dict[str, Any]] = []

        # Initialize custodian master key
        self._initialize_custodian_key()

    def _initialize_custodian_key(self):
        """Generate or load custodian RSA key pair"""
        # In production, load from secure key storage (HSM, Azure Key Vault, etc.)
        # For now, generate ephemeral key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.custodian_key = private_key
        self.custodian_public_key = private_key.public_key()

    def register_council_seal(
        self,
        member_id: str,
        member_name: str,
        role: str,
        seal_type: str = "RSA-2048"
    ) -> CouncilSeal:
        """
        Register a new council member seal

        Args:
            member_id: Unique identifier for council member
            member_name: Full name of council member
            role: Council role (e.g., "Senior Council", "Council Observer")
            seal_type: Cryptographic algorithm ("RSA-2048", "ECC-P256")

        Returns:
            CouncilSeal object with generated key pair
        """
        if seal_type == "RSA-2048":
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            public_key = private_key.public_key()

            # Serialize keys
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

        elif seal_type == "ECC-P256":
            private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
            public_key = private_key.public_key()

            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        else:
            raise ValueError(f"Unsupported seal type: {seal_type}")

        seal = CouncilSeal(
            member_id=member_id,
            member_name=member_name,
            role=role,
            public_key=public_pem,
            private_key=private_pem,
            seal_type=seal_type
        )

        self.council_seals[member_id] = seal
        return seal

    def _compute_content_hash(self, content: str | bytes) -> str:
        """Compute SHA-256 hash of content"""
        if isinstance(content, str):
            content = content.encode('utf-8')
        return hashlib.sha256(content).hexdigest()

    def _sign_with_rsa(self, content_hash: str, private_key) -> str:
        """Sign content hash with RSA private key"""
        signature = private_key.sign(
            content_hash.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode('utf-8')

    def _sign_with_ecc(self, content_hash: str, private_key) -> str:
        """Sign content hash with ECC private key"""
        signature = private_key.sign(
            content_hash.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )
        return base64.b64encode(signature).decode('utf-8')

    def sign_export(
        self,
        content: str | bytes,
        export_format: str,
        metadata: Optional[Dict[str, Any]] = None,
        include_custodian: bool = True
    ) -> Dict[str, Any]:
        """
        Sign an export with custodian seal

        Args:
            content: Export content (PDF bytes, Markdown text, YAML text)
            export_format: Format type ("pdf", "markdown", "yaml")
            metadata: Additional metadata (cycle, engine, role filters)
            include_custodian: Whether to include custodian signature

        Returns:
            Seal package with content hash, signature, and metadata
        """
        # Compute content hash
        content_hash = self._compute_content_hash(content)

        # Timestamp
        timestamp = datetime.now(timezone.utc).isoformat()

        # Build seal package
        seal_package = {
            "content_hash": content_hash,
            "hash_algorithm": "SHA-256",
            "export_format": export_format,
            "timestamp": timestamp,
            "metadata": metadata or {},
            "signatures": []
        }

        # Custodian signature
        if include_custodian:
            custodian_signature = self._sign_with_rsa(content_hash, self.custodian_key)
            seal_package["signatures"].append({
                "signer": "custodian",
                "name": self.custodian_name,
                "role": "Sovereign Custodian",
                "signature": custodian_signature,
                "algorithm": "RSA-2048-PSS-SHA256",
                "timestamp": timestamp
            })

        # Record in ledger
        self._record_to_ledger(seal_package)

        return seal_package

    def add_council_signature(
        self,
        seal_package: Dict[str, Any],
        member_id: str
    ) -> Dict[str, Any]:
        """
        Add a council member's signature to an existing seal package

        Args:
            seal_package: Existing seal package from sign_export()
            member_id: Council member ID to sign with

        Returns:
            Updated seal package with additional signature
        """
        if member_id not in self.council_seals:
            raise ValueError(f"Council member {member_id} not registered")

        seal = self.council_seals[member_id]
        content_hash = seal_package["content_hash"]

        # Load private key from PEM
        if seal.seal_type == "RSA-2048":
            private_key = serialization.load_pem_private_key(
                seal.private_key,
                password=None,
                backend=default_backend()
            )
            signature = self._sign_with_rsa(content_hash, private_key)
            algorithm = "RSA-2048-PSS-SHA256"

        elif seal.seal_type == "ECC-P256":
            private_key = serialization.load_pem_private_key(
                seal.private_key,
                password=None,
                backend=default_backend()
            )
            signature = self._sign_with_ecc(content_hash, private_key)
            algorithm = "ECDSA-P256-SHA256"
        else:
            raise ValueError(f"Unsupported seal type: {seal.seal_type}")

        # Add signature
        timestamp = datetime.now(timezone.utc).isoformat()
        seal_package["signatures"].append({
            "signer": "council",
            "member_id": member_id,
            "name": seal.member_name,
            "role": seal.role,
            "signature": signature,
            "algorithm": algorithm,
            "timestamp": timestamp
        })

        # Update ledger
        self._update_ledger(seal_package)

        return seal_package

    def create_multi_signature_covenant(
        self,
        content: str | bytes,
        export_format: str,
        council_member_ids: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a multi-signature covenant with custodian + council seals

        Args:
            content: Export content
            export_format: Format type
            council_member_ids: List of council member IDs to sign
            metadata: Additional metadata

        Returns:
            Seal package with multiple signatures
        """
        # Initial custodian seal
        seal_package = self.sign_export(content, export_format, metadata)

        # Add each council signature
        for member_id in council_member_ids:
            seal_package = self.add_council_signature(seal_package, member_id)

        seal_package["covenant_type"] = "multi-signature"
        seal_package["required_signatures"] = len(council_member_ids) + 1  # Custodian + council
        seal_package["signature_count"] = len(seal_package["signatures"])

        return seal_package

    def verify_signature(
        self,
        seal_package: Dict[str, Any],
        content: str | bytes,
        signer_index: int = 0
    ) -> bool:
        """
        Verify a specific signature in a seal package

        Args:
            seal_package: Seal package with signatures
            content: Original content
            signer_index: Index of signature to verify

        Returns:
            True if signature is valid
        """
        # Compute content hash
        content_hash = self._compute_content_hash(content)

        # Check hash matches
        if content_hash != seal_package["content_hash"]:
            return False

        signature_info = seal_package["signatures"][signer_index]
        signature_bytes = base64.b64decode(signature_info["signature"])

        try:
            if signature_info["signer"] == "custodian":
                # Verify with custodian public key
                self.custodian_public_key.verify(
                    signature_bytes,
                    content_hash.encode('utf-8'),
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                return True

            elif signature_info["signer"] == "council":
                # Verify with council member public key
                member_id = signature_info["member_id"]
                if member_id not in self.council_seals:
                    return False

                seal = self.council_seals[member_id]
                public_key = serialization.load_pem_public_key(
                    seal.public_key,
                    backend=default_backend()
                )

                if seal.seal_type == "RSA-2048":
                    public_key.verify(
                        signature_bytes,
                        content_hash.encode('utf-8'),
                        padding.PSS(
                            mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                        hashes.SHA256()
                    )
                elif seal.seal_type == "ECC-P256":
                    public_key.verify(
                        signature_bytes,
                        content_hash.encode('utf-8'),
                        ec.ECDSA(hashes.SHA256())
                    )

                return True

        except InvalidSignature:
            return False
        except Exception as e:
            print(f"Verification error: {e}")
            return False

        return False

    def verify_all_signatures(
        self,
        seal_package: Dict[str, Any],
        content: str | bytes
    ) -> Dict[str, bool]:
        """
        Verify all signatures in a seal package

        Returns:
            Dictionary mapping signer names to verification status
        """
        results = {}
        for i, sig in enumerate(seal_package["signatures"]):
            signer_name = sig["name"]
            results[signer_name] = self.verify_signature(seal_package, content, i)
        return results

    def _record_to_ledger(self, seal_package: Dict[str, Any]):
        """Record seal package to immutable ledger"""
        ledger_entry = {
            "entry_id": len(self.signature_ledger) + 1,
            "content_hash": seal_package["content_hash"],
            "export_format": seal_package["export_format"],
            "timestamp": seal_package["timestamp"],
            "signature_count": len(seal_package["signatures"]),
            "signers": [sig["name"] for sig in seal_package["signatures"]],
            "metadata": seal_package.get("metadata", {})
        }
        self.signature_ledger.append(ledger_entry)

    def _update_ledger(self, seal_package: Dict[str, Any]):
        """Update existing ledger entry with new signature"""
        content_hash = seal_package["content_hash"]

        # Find existing entry
        for entry in self.signature_ledger:
            if entry["content_hash"] == content_hash:
                entry["signature_count"] = len(seal_package["signatures"])
                entry["signers"] = [sig["name"] for sig in seal_package["signatures"]]
                entry["last_updated"] = datetime.now(timezone.utc).isoformat()
                break

    def get_ledger(self) -> List[Dict[str, Any]]:
        """Get complete signature ledger"""
        return self.signature_ledger

    def export_ledger_to_json(self) -> str:
        """Export ledger to JSON format"""
        return json.dumps(self.signature_ledger, indent=2)

    def get_council_seals(self) -> List[Dict[str, Any]]:
        """Get all registered council seals (public keys only)"""
        return [seal.to_dict() for seal in self.council_seals.values()]

    def export_seal_package_for_storage(self, seal_package: Dict[str, Any]) -> str:
        """
        Format seal package for storage in Replay Capsule Archive

        Returns JSON string with complete seal information
        """
        storage_package = {
            "codex_dominion_seal": {
                "version": "1.0.0",
                "content_hash": seal_package["content_hash"],
                "hash_algorithm": seal_package["hash_algorithm"],
                "export_format": seal_package["export_format"],
                "timestamp": seal_package["timestamp"],
                "covenant_type": seal_package.get("covenant_type", "single-signature"),
                "metadata": seal_package.get("metadata", {}),
                "signatures": seal_package["signatures"],
                "verification_url": f"https://codexdominion.app/api/verify/{seal_package['content_hash']}",
                "sealed_by": "Codex Dominion Digital Seal Service",
                "immutable": True
            }
        }
        return json.dumps(storage_package, indent=2)


# Singleton instance
_seal_service_instance: Optional[DigitalSealService] = None

def get_seal_service(custodian_name: str = "Jermaine Merritt") -> DigitalSealService:
    """Get or create singleton seal service instance"""
    global _seal_service_instance
    if _seal_service_instance is None:
        _seal_service_instance = DigitalSealService(custodian_name)
    return _seal_service_instance
