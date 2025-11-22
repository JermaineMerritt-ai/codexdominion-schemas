#!/usr/bin/env python3
"""
🕯️ Codex Ceremonial Inscription System
======================================

Sacred inscription interface for the three ceremonial kinds:
- Proclamations: Bold declarations and announcements
- Silences: Moments of reflection and remembrance  
- Blessings: Sacred invocations and well-wishes

Every inscription is preserved in the eternal festival log.
"""

import json
import datetime
import logging
from pathlib import Path
from typing import Dict, Any, Literal
from google.cloud import storage
from google.api_core import exceptions as gcs_exceptions

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Type definitions for ceremonial kinds
CeremonyKind = Literal['proclamation', 'silence', 'blessing']

class CodexCeremonialInscriber:
    """Sacred inscriber for ceremonial entries in the eternal bulletin."""
    
    def __init__(self, project_id: str = "codex-dominion-prod"):
        self.project_id = project_id
        self.bucket_name = f"codex-artifacts-{project_id}"
        self.festival_blob_name = "festival.json"
        
    def _get_storage_client(self) -> storage.Client:
        """Initialize Google Cloud Storage client."""
        try:
            return storage.Client(project=self.project_id)
        except Exception as e:
            logger.error(f"Failed to initialize GCS client: {e}")
            raise
    
    def inscribe_ceremony(self, kind: CeremonyKind, message: str) -> Dict[str, Any]:
        """
        Inscribe a ceremonial entry into the eternal bulletin.
        
        Args:
            kind: 'proclamation' | 'silence' | 'blessing'
            message: text to inscribe into the Bulletin
            
        Returns:
            Dict containing the inscribed entry information
        """
        try:
            client = self._get_storage_client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.festival_blob_name)
            
            # Load existing festival log
            try:
                data = json.loads(blob.download_as_text())
                logger.info("Loaded existing festival log for ceremonial inscription")
            except gcs_exceptions.NotFound:
                logger.info("Creating new festival log for ceremonial inscriptions")
                data = {
                    "codex_festival_status": "ACTIVE_CEREMONIAL",
                    "created": datetime.datetime.utcnow().isoformat(),
                    "cycles": [],
                    "total_ceremonies": 0
                }
            except Exception as e:
                logger.warning(f"Error loading festival log, creating new: {e}")
                data = {
                    "codex_festival_status": "ACTIVE_CEREMONIAL",
                    "created": datetime.datetime.utcnow().isoformat(),
                    "cycles": [],
                    "total_ceremonies": 0
                }
            
            # Create ceremonial entry with enhanced structure
            entry = {
                "cycle_id": f"ceremony_{len(data['cycles']) + 1:04d}",
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "ceremony_type": f"ceremonial_{kind}",
                "kind": kind,
                "message": message,
                "proclamation": self._format_ceremonial_proclamation(kind, message),
                "rite": self._get_ceremonial_rite_name(kind),
                "flame_status": "burning_ceremonial",
                "recorded_by": "CodexCeremonialInscriber",
                "sacred_checksum": self._calculate_ceremonial_checksum(kind, message)
            }
            
            # Append to cycles
            data["cycles"].append(entry)
            data["total_ceremonies"] = len(data["cycles"])
            data["last_ceremony"] = entry["timestamp"]
            data["last_updated"] = datetime.datetime.utcnow().isoformat()
            
            # Save back to cloud storage
            festival_json = json.dumps(data, indent=2, ensure_ascii=False)
            blob.upload_from_string(festival_json, content_type="application/json")
            
            logger.info(f"🕯️ Ceremonial {kind} inscribed successfully: {entry['cycle_id']}")
            
            return entry
            
        except Exception as e:
            logger.error(f"Failed to inscribe ceremony: {e}")
            # Fallback to local storage if cloud fails
            return self._fallback_local_inscription(kind, message)
    
    def _format_ceremonial_proclamation(self, kind: CeremonyKind, message: str) -> str:
        """Format the message into a proper ceremonial proclamation."""
        if kind == 'proclamation':
            return f"📢 Sacred Proclamation 📢\n\n{message}\n\nLet all who witness bear testimony to this declaration."
        elif kind == 'silence':
            return f"🤫 Moment of Sacred Silence 🤫\n\n{message}\n\nIn quiet reflection, wisdom emerges."
        elif kind == 'blessing':
            return f"🙏 Sacred Blessing 🙏\n\n{message}\n\nMay these words carry divine favor to all who receive them."
        else:
            return message
    
    def _get_ceremonial_rite_name(self, kind: CeremonyKind) -> str:
        """Get the appropriate rite name for the ceremonial kind."""
        if kind == 'proclamation':
            return "Rite of Sacred Declaration"
        elif kind == 'silence':
            return "Rite of Reflective Silence"
        elif kind == 'blessing':
            return "Rite of Divine Invocation"
        else:
            return f"Ceremonial Rite of {kind.title()}"
    
    def _calculate_ceremonial_checksum(self, kind: CeremonyKind, message: str) -> str:
        """Calculate sacred checksum for ceremonial integrity."""
        import hashlib
        content = f"{kind}{message}{datetime.datetime.utcnow().date().isoformat()}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _fallback_local_inscription(self, kind: CeremonyKind, message: str) -> Dict[str, Any]:
        """Fallback to local ceremonial inscription if cloud storage fails."""
        logger.warning("Using local fallback for ceremonial inscription")
        
        local_file = Path("ceremonial_inscriptions_backup.json")
        
        try:
            if local_file.exists():
                with open(local_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {
                    "codex_festival_status": "LOCAL_CEREMONIAL_BACKUP",
                    "created": datetime.datetime.utcnow().isoformat(),
                    "cycles": [],
                    "total_ceremonies": 0
                }
            
            entry = {
                "cycle_id": f"local_ceremony_{len(data['cycles']) + 1:04d}",
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "ceremony_type": f"ceremonial_{kind}",
                "kind": kind,
                "message": message,
                "proclamation": self._format_ceremonial_proclamation(kind, message),
                "rite": self._get_ceremonial_rite_name(kind),
                "flame_status": "burning_local_ceremonial",
                "recorded_by": "CodexCeremonialInscriber_LocalBackup",
                "sacred_checksum": self._calculate_ceremonial_checksum(kind, message)
            }
            
            data["cycles"].append(entry)
            data["total_ceremonies"] = len(data["cycles"])
            data["last_ceremony"] = entry["timestamp"]
            data["last_updated"] = datetime.datetime.utcnow().isoformat()
            
            with open(local_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"🏠 Local ceremonial {kind} inscribed: {entry['cycle_id']}")
            return entry
            
        except Exception as e:
            logger.error(f"Failed local ceremonial inscription: {e}")
            return {
                "cycle_id": f"emergency_ceremony_{kind}",
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "ceremony_type": f"ceremonial_{kind}",
                "kind": kind,
                "message": message,
                "status": "emergency_inscribed",
                "error": str(e)
            }
    
    def get_ceremonial_inscriptions(self, kind: CeremonyKind = None, limit: int = 10) -> list:
        """Retrieve recent ceremonial inscriptions, optionally filtered by kind."""
        try:
            client = self._get_storage_client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.festival_blob_name)
            
            data = json.loads(blob.download_as_text())
            cycles = data.get("cycles", [])
            
            # Filter by ceremonial entries
            ceremonial_cycles = [c for c in cycles if c.get('ceremony_type', '').startswith('ceremonial_')]
            
            # Further filter by kind if specified
            if kind:
                ceremonial_cycles = [c for c in ceremonial_cycles if c.get('kind') == kind]
            
            # Return most recent cycles
            return ceremonial_cycles[-limit:] if ceremonial_cycles else []
            
        except Exception as e:
            logger.error(f"Failed to retrieve ceremonial inscriptions: {e}")
            return []


# Convenience function matching your original signature
def inscribe_ceremony(kind: CeremonyKind, message: str) -> Dict[str, Any]:
    """
    Inscribe a ceremonial entry into the eternal bulletin.
    
    Args:
        kind: 'proclamation' | 'silence' | 'blessing'
        message: text to inscribe into the Bulletin
        
    Returns:
        Dict containing the inscribed entry information
    """
    inscriber = CodexCeremonialInscriber()
    return inscriber.inscribe_ceremony(kind, message)


# Enhanced ceremonial functions
def proclaim_sacred_declaration(message: str) -> Dict[str, Any]:
    """Inscribe a sacred proclamation into the eternal bulletin."""
    return inscribe_ceremony('proclamation', message)

def observe_sacred_silence(message: str) -> Dict[str, Any]:
    """Inscribe a moment of sacred silence into the eternal bulletin."""
    return inscribe_ceremony('silence', message)

def offer_sacred_blessing(message: str) -> Dict[str, Any]:
    """Inscribe a sacred blessing into the eternal bulletin."""
    return inscribe_ceremony('blessing', message)


# CLI Interface for direct invocation
def main():
    """CLI interface for ceremonial inscriptions."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python codex_ceremonial_inscriber.py <kind> <message>")
        print("Kinds: proclamation, silence, blessing")
        print("Examples:")
        print("  python codex_ceremonial_inscriber.py proclamation 'The eternal flame burns bright'")
        print("  python codex_ceremonial_inscriber.py silence 'In memory of all who came before'") 
        print("  python codex_ceremonial_inscriber.py blessing 'May wisdom guide our path'")
        sys.exit(1)
    
    kind = sys.argv[1]
    message = sys.argv[2]
    
    if kind not in ['proclamation', 'silence', 'blessing']:
        print(f"Error: Invalid kind '{kind}'. Must be one of: proclamation, silence, blessing")
        sys.exit(1)
    
    try:
        entry = inscribe_ceremony(kind, message)
        print(f"🕯️ Ceremonial {kind} inscribed successfully!")
        print(f"Cycle ID: {entry.get('cycle_id', 'unknown')}")
        print(f"Timestamp: {entry.get('timestamp', 'unknown')}")
        print(f"Sacred Checksum: {entry.get('sacred_checksum', 'unknown')}")
    except Exception as e:
        print(f"❌ Failed to inscribe ceremony: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()