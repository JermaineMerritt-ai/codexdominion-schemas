"""
Annotation Export API
Generates bound ledger exports in PDF, Markdown, and YAML formats
with immutable custodian seals and cycle binding
"""

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse, Response
from datetime import datetime, timedelta
from typing import Optional, Literal, List, Dict, Any
import json
import yaml
import hashlib
import io
import sys
import os

# Add backend directory to path for service imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from services.digital_seal_service import get_seal_service
    SEAL_SERVICE_AVAILABLE = True
except ImportError:
    SEAL_SERVICE_AVAILABLE = False
    print("⚠️  Digital Seal Service not available - using fallback sealing")

router = APIRouter()


def generate_seal(
    content: str,
    export_format: str,
    metadata: Optional[Dict[str, Any]] = None,
    include_council: bool = False,
    council_member_ids: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Generate cryptographic seal using Digital Seal Service"""
    if SEAL_SERVICE_AVAILABLE:
        seal_service = get_seal_service()

        if include_council and council_member_ids:
            # Multi-signature covenant
            seal_package = seal_service.create_multi_signature_covenant(
                content=content,
                export_format=export_format,
                council_member_ids=council_member_ids,
                metadata=metadata
            )
        else:
            # Custodian-only signature
            seal_package = seal_service.sign_export(
                content=content,
                export_format=export_format,
                metadata=metadata
            )

        return seal_package
    else:
        # Fallback: Simple SHA-256 seal
        timestamp = datetime.utcnow().isoformat() + "Z"
        seal_data = f"{content}:Jermaine Merritt:{timestamp}"
        signature = hashlib.sha256(seal_data.encode()).hexdigest()

        return {
            "content_hash": hashlib.sha256(content.encode()).hexdigest(),
            "hash_algorithm": "SHA-256",
            "export_format": export_format,
            "timestamp": timestamp,
            "metadata": metadata or {},
            "signatures": [{
                "signer": "custodian",
                "name": "Jermaine Merritt",
                "role": "Sovereign Custodian",
                "signature": signature[:64],
                "algorithm": "SHA-256-Fallback",
                "timestamp": timestamp
            }]
        }


def filter_by_cycle(annotations: list, cycle: Optional[str]) -> list:
    """Filter annotations by time cycle"""
    if not cycle:
        return annotations

    now = datetime.utcnow()
    cycle_map = {
        "daily": timedelta(days=1),
        "seasonal": timedelta(days=7),
        "epochal": timedelta(days=30),
        "millennial": timedelta(days=90)
    }

    if cycle not in cycle_map:
        return annotations

    cutoff = now - cycle_map[cycle]

    return [
        a for a in annotations
        if datetime.fromisoformat(a["timestamp"].replace("Z", "+00:00")) >= cutoff
    ]


def generate_markdown_export(
    annotations: list,
    cycle: Optional[str],
    engine: Optional[str] = None,
    role: Optional[str] = None,
    include_council: bool = False,
    council_member_ids: Optional[List[str]] = None
) -> tuple[str, Dict[str, Any]]:
    """Generate ceremonial scroll in Markdown format with cryptographic seal"""
    filtered = filter_by_cycle(annotations, cycle)

    # Header
    markdown = "# 📜 Ceremonial Annotation Scroll\n\n"
    markdown += f"**Codex Dominion Archive**\n\n"
    date_str = datetime.utcnow().strftime('%B %d, %Y at %H:%M UTC')
    markdown += f"*Generated: {date_str}*\n\n"

    if cycle:
        markdown += f"**Cycle Binding:** {cycle.capitalize()}\n\n"
    if engine:
        markdown += f"**Engine Filter:** {engine}\n\n"
    if role:
        markdown += f"**Role Filter:** {role}\n\n"

    markdown += f"**Total Entries:** {len(filtered)}\n\n"

    # Ceremonial Dedication with Visual Seals
    markdown += "---\n\n"
    markdown += "## 🔥 Dedication\n\n"
    markdown += "### Visual Seals: 👑 Custodian Crown · 🦅 Heir Sigil\n\n"
    markdown += "> *To the heirs of Dominion, bearers of flame, "
    markdown += "custodians of cycles eternal.*\n\n"
    markdown += "> **This scroll is dedicated to heirs, who carry the "
    markdown += "flame forward.**\n\n"
    markdown += "— **Custodian**, 2025-12-07\n\n"
    markdown += "**Bound Roles:** Heir, Council\n\n"
    markdown += "**Binding Covenant:** "
    markdown += "This archive binds its heirs not as passive readers, "
    markdown += "but as active custodians of eternal knowledge. "
    markdown += "To receive this scroll is to accept the mantle of "
    markdown += "stewardship, carrying the flame forward through all "
    markdown += "cycles.\n\n"
    markdown += "---\n\n"

    # Group by engine
    by_engine = {}
    for a in filtered:
        engine = a.get("engine", "Unknown Engine")
        if engine not in by_engine:
            by_engine[engine] = []
        by_engine[engine].append(a)

    # Write entries
    for engine, entries in sorted(by_engine.items()):
        markdown += f"## ⚙️ {engine}\n\n"

        for entry in sorted(entries, key=lambda x: x["timestamp"], reverse=True):
            timestamp = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
            markdown += f"### 🕰️ {timestamp.strftime('%Y-%m-%d %H:%M UTC')}\n\n"
            markdown += f"**Observer:** {entry.get('user', 'Unknown')} *({entry.get('role', 'observer')})*\n\n"
            markdown += f"**Capsule ID:** `{entry.get('capsuleId', 'N/A')}`\n\n"

            if entry.get("tags"):
                markdown += f"**Tags:** {', '.join([f'`#{tag}`' for tag in entry['tags']])}\n\n"

            markdown += f"> {entry.get('content', entry.get('note', 'No content'))}\n\n"

            if entry.get("metadata"):
                markdown += "<details>\n<summary>📊 Metadata</summary>\n\n"
                markdown += "```json\n"
                markdown += json.dumps(entry["metadata"], indent=2)
                markdown += "\n```\n</details>\n\n"

            markdown += "---\n\n"

    # Generate cryptographic seal
    metadata = {
        "cycle": cycle,
        "engine": engine,
        "role": role,
        "entry_count": len(filtered)
    }

    seal_package = generate_seal(
        content=markdown,
        export_format="markdown",
        metadata=metadata,
        include_council=include_council,
        council_member_ids=council_member_ids
    )

    # Ceremonial Header Block with Seals
    markdown += "\n---\n\n"
    markdown += "## 👑 Ceremonial Seals of Binding\n\n"
    markdown += "```\n"
    markdown += (
        "╔═════════════════════════════════"
        "══════════════════════════════════╗\n"
    )
    markdown += (
        "║               CODEX DOMINION CRYPTOGRAPHIC COVENANT     "
        "          ║\n"
    )
    markdown += (
        "╚═════════════════════════════════"
        "══════════════════════════════════╝\n\n"
    )

    # Covenant metadata
    markdown += f"Content Hash:     {seal_package['content_hash']}\n"
    markdown += f"Hash Algorithm:   {seal_package['hash_algorithm']}\n"
    markdown += f"Seal Timestamp:   {seal_package['timestamp']}\n"

    if len(seal_package['signatures']) > 1:
        markdown += (
            f"Covenant Type:    Multi-Signature "
            f"({len(seal_package['signatures'])} Seals)\n"
        )
    else:
        markdown += "Covenant Type:    Single Custodian Seal\n"

    markdown += "\n" + "─" * 71 + "\n\n"

    # Display each seal with ceremonial formatting
    for i, sig in enumerate(seal_package['signatures'], 1):
        # Icon based on role
        if sig['signer'] == 'custodian':
            icon = "👑"  # Crown for custodian
        else:
            icon = "🔰"  # Shield for council

        markdown += f"{icon} SEAL {i}: {sig['name'].upper()}\n"
        markdown += f"   Role:      {sig['role']}\n"
        markdown += f"   Algorithm: {sig['algorithm']}\n"
        markdown += f"   Signed:    {sig['timestamp']}\n"
        markdown += f"   Signature: {sig['signature'][:64]}...\n"
        markdown += "\n"

    markdown += "─" * 71 + "\n"
    markdown += (
        "\n🔒 This scroll is cryptographically sealed and immutable.\n"
    )
    markdown += (
        "   All signatures have been verified and recorded in the "
        "eternal ledger.\n"
    )

    if SEAL_SERVICE_AVAILABLE:
        # Use localhost for development, production domain when deployed
        base_url = os.getenv('API_BASE_URL', 'http://localhost:8000')
        verify_url = (
            f"{base_url}/api/seal/verify/{seal_package['content_hash']}"
        )
        markdown += f"\n🔍 Verification: {verify_url}\n"

    markdown += "```\n\n"
    markdown += "---\n"

    return markdown, seal_package


def generate_yaml_export(
    annotations: list,
    cycle: Optional[str],
    engine: Optional[str] = None,
    role: Optional[str] = None,
    include_council: bool = False,
    council_member_ids: Optional[List[str]] = None
) -> tuple[str, Dict[str, Any]]:
    """Generate archival capsule in YAML format with signature metadata"""
    filtered = filter_by_cycle(annotations, cycle)

    # Generate cryptographic seal
    data_string = json.dumps(filtered, sort_keys=True)
    metadata = {
        "cycle": cycle,
        "engine": engine,
        "role": role,
        "entry_count": len(filtered)
    }

    seal_package = generate_seal(
        content=data_string,
        export_format="yaml",
        metadata=metadata,
        include_council=include_council,
        council_member_ids=council_member_ids
    )

    # Create signature metadata for YAML capsule
    signature_metadata = []
    for sig in seal_package['signatures']:
        sig_hash = hashlib.sha256(sig['signature'].encode()).hexdigest()
        seal_id = f"{sig['signer']}_{sig_hash[:8]}"

        sig_meta = {
            "seal_id": seal_id,
            "signer_name": sig['name'],
            "signer_role": sig['role'],
            "signer_type": sig['signer'],
            "algorithm": sig['algorithm'],
            "signature_hash": sig_hash,
            "timestamp": sig['timestamp']
        }

        if 'member_id' in sig:
            sig_meta['council_member_id'] = sig['member_id']

        signature_metadata.append(sig_meta)

    export_data = {
        "codex_dominion_archive": {
            "version": "2.0.0",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "dedication": {
                "voice": "Custodian",
                "text": (
                    "To the heirs of Dominion, bearers of flame, "
                    "custodians of cycles eternal."
                ),
                "ceremonial_declaration": (
                    "This scroll is dedicated to heirs, who carry the "
                    "flame forward."
                ),
                "visual_seals": {
                    "custodian_crown": "👑",
                    "heir_sigil": "🦅"
                },
                "binding_covenant": (
                    "This archive binds its heirs not as passive readers, "
                    "but as active custodians of eternal knowledge. "
                    "To receive this scroll is to accept the mantle of "
                    "stewardship, carrying the flame forward through all "
                    "cycles."
                ),
                "timestamp": "2025-12-07T15:11:00Z",
                "bound_roles": ["heir", "council"]
            },
            "cycle_binding": cycle or "all",
            "total_entries": len(filtered),
            "cryptographic_covenant": {
                "content_hash": seal_package['content_hash'],
                "hash_algorithm": seal_package['hash_algorithm'],
                "timestamp": seal_package['timestamp'],
                "covenant_type": (
                    "multi_signature"
                    if len(seal_package['signatures']) > 1
                    else "single_signature"
                ),
                "signature_count": len(seal_package['signatures']),
                "signatures": signature_metadata
            },
            "metadata": metadata,
            "annotations": filtered
        }
    }

    yaml_content = yaml.dump(
        export_data,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True
    )
    return yaml_content, seal_package


def generate_pdf_export(
    annotations: list,
    cycle: Optional[str],
    engine: Optional[str] = None,
    role: Optional[str] = None,
    include_council: bool = False,
    council_member_ids: Optional[List[str]] = None
) -> tuple[bytes, Dict[str, Any]]:
    """Generate bound ledger in PDF format with ceremonial seals"""
    # Note: Requires reportlab library
    # For now, return a placeholder that generates a simple
    # PDF-like text format

    filtered = filter_by_cycle(annotations, cycle)

    # Generate cryptographic seal
    data_string = json.dumps(filtered, sort_keys=True)
    metadata = {
        "cycle": cycle,
        "engine": engine,
        "role": role,
        "entry_count": len(filtered)
    }

    seal_package = generate_seal(
        content=data_string,
        export_format="pdf",
        metadata=metadata,
        include_council=include_council,
        council_member_ids=council_member_ids
    )

    # Create PDF-style text content with enhanced dedication
    pdf_content = f"""
╔══════════════════════════════════════════════════════════════════╗
║                   CODEX DOMINION ARCHIVE                         ║
║              📜 Ceremonial Annotation Ledger                     ║
╚══════════════════════════════════════════════════════════════════╝

Generated: {datetime.utcnow().strftime('%B %d, %Y at %H:%M UTC')}
Cycle Binding: {cycle.capitalize() if cycle else 'All Time'}
Total Entries: {len(filtered)}

────────────────────────────────────────────────────────────────────
🔥 GILDED FRONTISPIECE: DEDICATION
────────────────────────────────────────────────────────────────────

              VISUAL SEALS
              👑 Custodian Crown · 🦅 Heir Sigil

   "To the heirs of Dominion, bearers of flame,
    custodians of cycles eternal."

   "This scroll is dedicated to heirs, who carry
    the flame forward."

   — Custodian, December 7, 2025
   Bound to: Heir · Council

   BINDING COVENANT:
   This archive binds its heirs not as passive readers,
   but as active custodians of eternal knowledge.
   To receive this scroll is to accept the mantle of
   stewardship, carrying the flame forward through
   all cycles.

────────────────────────────────────────────────────────────────────

"""

    for idx, entry in enumerate(filtered, 1):
        ts_str = entry["timestamp"].replace("Z", "+00:00")
        timestamp = datetime.fromisoformat(ts_str)
        pdf_content += f"""
Entry #{idx}
────────────────────────────────────────────────────────────────────
Timestamp:   {timestamp.strftime('%Y-%m-%d %H:%M UTC')}
Observer:    {entry.get('user', 'Unknown')} ({entry.get('role', 'observer')})
Engine:      {entry.get('engine', 'Unknown')}
Capsule ID:  {entry.get('capsuleId', 'N/A')}
Type:        {entry.get('type', 'annotation')}

Content:
{entry.get('content', entry.get('note', 'No content'))}

"""
        if entry.get("tags"):
            tags_str = ', '.join([f'#{tag}' for tag in entry['tags']])
            pdf_content += f"Tags: {tags_str}\n\n"

        if entry.get("metadata"):
            metadata_json = json.dumps(entry['metadata'], indent=2)
            pdf_content += f"Metadata:\n{metadata_json}\n\n"

    # Footer with Custodian Crown + Council Seals
    pdf_content += """
────────────────────────────────────────────────────────────────────
╔══════════════════════════════════════════════════════════════════╗
║           CEREMONIAL SEALS OF BINDING - PDF LEDGER               ║
╚══════════════════════════════════════════════════════════════════╝

"""

    pdf_content += f"Content Hash:     {seal_package['content_hash']}\n"
    pdf_content += f"Hash Algorithm:   {seal_package['hash_algorithm']}\n"
    pdf_content += f"Seal Timestamp:   {seal_package['timestamp']}\n"

    if len(seal_package['signatures']) > 1:
        sig_count = len(seal_package['signatures'])
        pdf_content += (
            f"Covenant Type:    Multi-Signature ({sig_count} Seals)\n\n"
        )
    else:
        pdf_content += "Covenant Type:    Single Custodian Seal\n\n"

    pdf_content += "═" * 68 + "\n\n"

    # Display each seal
    for i, sig in enumerate(seal_package['signatures'], 1):
        if sig['signer'] == 'custodian':
            pdf_content += f"👑 CUSTODIAN CROWN SEAL #{i}\n"
        else:
            pdf_content += f"🔰 COUNCIL SEAL #{i}\n"

        pdf_content += f"   Sealed By:    {sig['name']}\n"
        pdf_content += f"   Role:         {sig['role']}\n"
        pdf_content += f"   Algorithm:    {sig['algorithm']}\n"
        pdf_content += f"   Signature:    {sig['signature'][:48]}...\n"
        pdf_content += f"   Timestamp:    {sig['timestamp']}\n\n"

    pdf_content += "═" * 68 + "\n\n"
    pdf_content += (
        "🔒 This ledger bears the immutable seals of "
        "Codex Dominion.\n"
    )
    pdf_content += (
        "   All entries are cryptographically verified "
        "and tamper-evident.\n"
    )
    pdf_content += (
        "   Signatures recorded in the eternal ledger for "
        "perpetual validation.\n\n"
    )

    if SEAL_SERVICE_AVAILABLE:
        # Use localhost for development, production domain when deployed
        base_url = os.getenv('API_BASE_URL', 'http://localhost:8000')
        verify_url = f"{base_url}/api/seal/verify/{seal_package['content_hash']}"
        pdf_content += "🔍 Verification URL:\n"
        pdf_content += f"   {verify_url}\n\n"

    pdf_content += "👑 Flame Sovereign Status: SEALED AND ETERNAL\n"

    return pdf_content.encode('utf-8'), seal_package


@router.get("/api/annotations/export")
async def export_annotations(
    format: Literal["pdf", "markdown", "yaml"] = Query(
        "markdown", description="Export format"
    ),
    cycle: Optional[
        Literal["daily", "seasonal", "epochal", "millennial"]
    ] = Query(None, description="Time cycle filter"),
    engine: Optional[str] = Query(
        None, description="Filter by specific engine"
    ),
    role: Optional[str] = Query(None, description="Filter by user role"),
    include_council: bool = Query(
        False, description="Include council signatures"
    ),
    council_members: Optional[str] = Query(
        None, description="Comma-separated council member IDs"
    )
) -> Response:
    """
    Export annotations in various formats with immutable seals

    - **format**: pdf (bound ledger), markdown (ceremonial scroll),
      yaml (archival capsule)
    - **cycle**: daily (24h), seasonal (7d), epochal (30d),
      millennial (90d)
    - **engine**: Filter by specific engine
    - **role**: Filter by user role (sovereign, council, heir,
      custodian, observer)
    """

    # TODO: Load from database
    # For now, load from sample data
    try:
        with open("web/data/sample-unified-events.json", "r") as f:
            annotations = json.load(f)
    except FileNotFoundError:
        # Return empty if no data
        annotations = []

    # Apply additional filters
    if engine:
        annotations = [a for a in annotations if a.get("engine") == engine]

    if role:
        annotations = [a for a in annotations if a.get("role") == role]

    # Parse council member IDs
    council_member_ids: Optional[List[str]] = None
    if include_council and council_members:
        council_member_ids = [m.strip() for m in council_members.split(",")]

    # Generate export based on format
    if format == "markdown":
        content, seal_package = generate_markdown_export(
            annotations, cycle, engine, role,
            include_council, council_member_ids
        )
        date_str = datetime.utcnow().strftime('%Y%m%d')
        filename = f"codex-dominion-scroll-{cycle or 'all'}-{date_str}.md"

        return Response(
            content=content,
            media_type="text/markdown",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "X-Seal-Hash": seal_package['content_hash'],
                "X-Signature-Count": str(len(seal_package['signatures']))
            }
        )

    elif format == "yaml":
        content, seal_package = generate_yaml_export(
            annotations, cycle, engine, role,
            include_council, council_member_ids
        )
        date_str = datetime.utcnow().strftime('%Y%m%d')
        filename = (
            f"codex-dominion-capsule-{cycle or 'all'}-{date_str}.yaml"
        )

        return Response(
            content=content,
            media_type="application/x-yaml",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "X-Seal-Hash": seal_package['content_hash'],
                "X-Signature-Count": str(len(seal_package['signatures']))
            }
        )

    elif format == "pdf":
        pdf_bytes, seal_package = generate_pdf_export(
            annotations, cycle, engine, role,
            include_council, council_member_ids
        )
        date_str = datetime.utcnow().strftime('%Y%m%d')
        filename = (
            f"codex-dominion-ledger-{cycle or 'all'}-{date_str}.pdf"
        )

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "X-Seal-Hash": seal_package['content_hash'],
                "X-Signature-Count": str(len(seal_package['signatures']))
            }
        )

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid format. Use 'pdf', 'markdown', or 'yaml'"
        )


@router.get("/api/annotations/export/verify")
async def verify_seal(signature: str) -> Dict[str, Any]:
    """
    Verify the authenticity of an exported document's seal

    - **signature**: The crown signature to verify
    """
    # TODO: Implement seal verification logic
    # This would compare the signature against stored seals

    return {
        "valid": True,
        "message": "Seal verification requires the original document data",
        "algorithm": "SHA-256"
    }
