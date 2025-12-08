"""
Seal Verification API - Verify cryptographic seals on exports
"""

from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
from pydantic import BaseModel
import json

from services.digital_seal_service import get_seal_service

router = APIRouter(prefix="/api/seal", tags=["seal-verification"])


class VerificationRequest(BaseModel):
    """Request to verify a seal package"""
    seal_package: Dict[str, Any]
    content: str
    content_encoding: str = "utf-8"  # or "base64" for binary content


class SignatureRequest(BaseModel):
    """Request to add council signature"""
    seal_package: Dict[str, Any]
    member_id: str


class MultiSignatureRequest(BaseModel):
    """Request to create multi-signature covenant"""
    content: str
    export_format: str
    council_member_ids: list[str]
    metadata: Optional[Dict[str, Any]] = None
    content_encoding: str = "utf-8"


@router.get("/ledger")
async def get_signature_ledger():
    """
    Get the complete immutable signature ledger

    Returns all recorded seal operations with timestamps and signers
    """
    seal_service = get_seal_service()
    ledger = seal_service.get_ledger()

    return JSONResponse(content={
        "ledger": ledger,
        "total_entries": len(ledger),
        "custodian": seal_service.custodian_name
    })


@router.get("/ledger/export")
async def export_ledger():
    """
    Export signature ledger as JSON file

    Provides downloadable JSON of all seal operations for archival
    """
    seal_service = get_seal_service()
    ledger_json = seal_service.export_ledger_to_json()

    from fastapi.responses import Response
    return Response(
        content=ledger_json,
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename=codex-dominion-seal-ledger.json"
        }
    )


@router.get("/council-seals")
async def get_council_seals():
    """
    Get all registered council member seals

    Returns public keys and metadata for all council members
    """
    seal_service = get_seal_service()
    seals = seal_service.get_council_seals()

    return JSONResponse(content={
        "council_seals": seals,
        "total_members": len(seals)
    })


@router.post("/register-council")
async def register_council_member(
    member_id: str = Body(...),
    member_name: str = Body(...),
    role: str = Body(...),
    seal_type: str = Body(default="RSA-2048")
):
    """
    Register a new council member seal

    Args:
        member_id: Unique identifier
        member_name: Full name
        role: Council role (e.g., "Senior Council", "Council Observer")
        seal_type: Cryptographic algorithm ("RSA-2048" or "ECC-P256")

    Returns:
        Public key and seal metadata
    """
    seal_service = get_seal_service()

    try:
        seal = seal_service.register_council_seal(
            member_id=member_id,
            member_name=member_name,
            role=role,
            seal_type=seal_type
        )

        return JSONResponse(content={
            "success": True,
            "message": f"Council seal registered for {member_name}",
            "seal": seal.to_dict()
        })

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/verify")
async def verify_seal(request: VerificationRequest):
    """
    Verify all signatures in a seal package

    Args:
        seal_package: Seal package with signatures
        content: Original export content
        content_encoding: "utf-8" or "base64"

    Returns:
        Verification results for each signer
    """
    seal_service = get_seal_service()

    try:
        # Decode content if base64
        content = request.content
        if request.content_encoding == "base64":
            import base64
            content = base64.b64decode(content)

        # Verify all signatures
        results = seal_service.verify_all_signatures(
            request.seal_package,
            content
        )

        all_valid = all(results.values())

        return JSONResponse(content={
            "valid": all_valid,
            "verification_results": results,
            "signature_count": len(request.seal_package["signatures"]),
            "content_hash": request.seal_package["content_hash"],
            "timestamp": request.seal_package["timestamp"]
        })

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Verification failed: {str(e)}")


@router.post("/add-council-signature")
async def add_council_signature(request: SignatureRequest):
    """
    Add a council member's signature to an existing seal package

    Args:
        seal_package: Existing seal package
        member_id: Council member ID to sign with

    Returns:
        Updated seal package with additional signature
    """
    seal_service = get_seal_service()

    try:
        updated_package = seal_service.add_council_signature(
            request.seal_package,
            request.member_id
        )

        return JSONResponse(content={
            "success": True,
            "message": f"Council signature added",
            "seal_package": updated_package,
            "signature_count": len(updated_package["signatures"])
        })

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/multi-signature-covenant")
async def create_multi_signature_covenant(request: MultiSignatureRequest):
    """
    Create a multi-signature covenant with custodian + council seals

    Args:
        content: Export content
        export_format: Format type ("pdf", "markdown", "yaml")
        council_member_ids: List of council member IDs to sign
        metadata: Additional metadata
        content_encoding: "utf-8" or "base64"

    Returns:
        Seal package with multiple signatures
    """
    seal_service = get_seal_service()

    try:
        # Decode content if base64
        content = request.content
        if request.content_encoding == "base64":
            import base64
            content = base64.b64decode(content)

        seal_package = seal_service.create_multi_signature_covenant(
            content=content,
            export_format=request.export_format,
            council_member_ids=request.council_member_ids,
            metadata=request.metadata
        )

        # Format for storage
        storage_json = seal_service.export_seal_package_for_storage(seal_package)

        return JSONResponse(content={
            "success": True,
            "message": "Multi-signature covenant created",
            "seal_package": seal_package,
            "storage_format": json.loads(storage_json),
            "signature_count": seal_package["signature_count"],
            "required_signatures": seal_package["required_signatures"]
        })

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/verify/{content_hash}")
async def verify_by_hash(content_hash: str):
    """
    Verify a seal by content hash lookup in ledger

    Args:
        content_hash: SHA-256 hash of content

    Returns:
        Seal information and verification status
    """
    seal_service = get_seal_service()
    ledger = seal_service.get_ledger()

    # Find in ledger
    for entry in ledger:
        if entry["content_hash"] == content_hash:
            return JSONResponse(content={
                "found": True,
                "entry": entry,
                "verification_url": f"https://codexdominion.app/api/seal/verify/{content_hash}",
                "immutable": True
            })

    raise HTTPException(status_code=404, detail="Seal not found in ledger")


@router.get("/stats")
async def get_seal_statistics():
    """
    Get statistics about seals and signatures

    Returns counts and metadata about seal operations
    """
    seal_service = get_seal_service()
    ledger = seal_service.get_ledger()
    council_seals = seal_service.get_council_seals()

    total_signatures = sum(entry["signature_count"] for entry in ledger)
    unique_signers = set()
    for entry in ledger:
        unique_signers.update(entry["signers"])

    formats = {}
    for entry in ledger:
        fmt = entry["export_format"]
        formats[fmt] = formats.get(fmt, 0) + 1

    return JSONResponse(content={
        "total_seals": len(ledger),
        "total_signatures": total_signatures,
        "unique_signers": len(unique_signers),
        "registered_council_members": len(council_seals),
        "formats": formats,
        "custodian": seal_service.custodian_name
    })
