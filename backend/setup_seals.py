"""
Setup script for Digital Seal Service
Registers sample council members with cryptographic seals
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.digital_seal_service import get_seal_service

def setup_council_seals():
    """Register sample council members"""
    seal_service = get_seal_service("Jermaine Merritt")

    print("🔐 Initializing Digital Seal Service...")
    print(f"👑 Custodian: {seal_service.custodian_name}")
    print()

    # Register council members
    council_members = [
        {
            "member_id": "council_001",
            "member_name": "Elena Rodriguez",
            "role": "Senior Council",
            "seal_type": "ECC-P256"
        },
        {
            "member_id": "council_002",
            "member_name": "Marcus Chen",
            "role": "Council Observer",
            "seal_type": "RSA-2048"
        },
        {
            "member_id": "council_003",
            "member_name": "Aisha Patel",
            "role": "Technical Council",
            "seal_type": "ECC-P256"
        },
        {
            "member_id": "council_004",
            "member_name": "Dmitri Volkov",
            "role": "Commerce Council",
            "seal_type": "RSA-2048"
        },
        {
            "member_id": "council_005",
            "member_name": "Sofia Ramirez",
            "role": "Marketing Council",
            "seal_type": "ECC-P256"
        }
    ]

    print("📝 Registering Council Seals:")
    print()

    for member in council_members:
        seal = seal_service.register_council_seal(
            member_id=member["member_id"],
            member_name=member["member_name"],
            role=member["role"],
            seal_type=member["seal_type"]
        )

        print(f"✅ {member['member_name']}")
        print(f"   ID: {member['member_id']}")
        print(f"   Role: {member['role']}")
        print(f"   Algorithm: {seal.seal_type}")
        print(f"   Created: {seal.created_at}")
        print()

    print(f"🎉 Seal Service Ready!")
    print(f"   Total Council Members: {len(council_members)}")
    print(f"   Signature Algorithms: RSA-2048, ECC-P256")
    print()

    # Test multi-signature covenant
    print("🧪 Testing Multi-Signature Covenant...")
    test_content = "# Test Export\n\nThis is a test ceremonial scroll."

    seal_package = seal_service.create_multi_signature_covenant(
        content=test_content,
        export_format="markdown",
        council_member_ids=["council_001", "council_002"],
        metadata={"test": True}
    )

    print(f"   Content Hash: {seal_package['content_hash'][:32]}...")
    print(f"   Signatures: {seal_package['signature_count']}")
    print(f"   Signers: {', '.join([s['name'] for s in seal_package['signatures']])}")
    print()

    # Verify signatures
    print("🔍 Verifying Signatures...")
    results = seal_service.verify_all_signatures(seal_package, test_content)

    for signer, valid in results.items():
        status = "✅ Valid" if valid else "❌ Invalid"
        print(f"   {signer}: {status}")

    print()
    print("🏁 Setup Complete!")
    print()
    print("API Endpoints:")
    print("   GET  /api/seal/ledger - View signature ledger")
    print("   GET  /api/seal/council-seals - List council members")
    print("   POST /api/seal/verify - Verify seal package")
    print("   POST /api/seal/register-council - Add council member")
    print()
    print("Export with Council Signatures:")
    print("   /api/annotations/export?format=markdown&include_council=true&council_members=council_001,council_002")
    print()


if __name__ == "__main__":
    setup_council_seals()
