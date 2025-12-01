#!/usr/bin/env python3
"""
🎭 Codex Festival Proclamation System
=====================================

Sacred ceremony recorder for the eternal flame's festivals and rites.
Every proclamation, every rite, every cycle is preserved in the cloud archive.

The Festival Log captures the living ceremonies of the Codex Dominion.
"""

import datetime
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from google.api_core import exceptions as gcs_exceptions
from google.cloud import storage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CodexFestivalKeeper:
    """Sacred keeper of festival proclamations and ceremonial rites."""

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

    def append_festival_proclamation(
        self, proclamation: str, rite: str, ceremony_type: str = "sacred_cycle"
    ) -> Dict[str, Any]:
        """
        Append a festival proclamation to the eternal ceremony log.

        Args:
            proclamation: The sacred proclamation text
            rite: The ceremonial rite being performed
            ceremony_type: Type of ceremony (sacred_cycle, crowning, dispatch, etc.)

        Returns:
            Dict containing the recorded cycle information
        """
        try:
            client = self._get_storage_client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.festival_blob_name)

            # Load existing festival log
            try:
                data = json.loads(blob.download_as_text())
                logger.info("Loaded existing festival log")
            except gcs_exceptions.NotFound:
                logger.info("Creating new festival log")
                data = {
                    "codex_festival_status": "ACTIVE",
                    "created": datetime.datetime.utcnow().isoformat(),
                    "cycles": [],
                    "total_ceremonies": 0,
                }
            except Exception as e:
                logger.warning(f"Error loading festival log, creating new: {e}")
                data = {
                    "codex_festival_status": "ACTIVE",
                    "created": datetime.datetime.utcnow().isoformat(),
                    "cycles": [],
                    "total_ceremonies": 0,
                }

            # Create new ceremonial cycle
            cycle = {
                "cycle_id": f"cycle_{len(data['cycles']) + 1:04d}",
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "ceremony_type": ceremony_type,
                "proclamation": proclamation,
                "rite": rite,
                "flame_status": "burning_bright",
                "recorded_by": "CodexFestivalKeeper",
                "sacred_checksum": self._calculate_cycle_checksum(proclamation, rite),
            }

            # Append to cycles
            data["cycles"].append(cycle)
            data["total_ceremonies"] = len(data["cycles"])
            data["last_ceremony"] = cycle["timestamp"]
            data["last_updated"] = datetime.datetime.utcnow().isoformat()

            # Save back to cloud storage
            festival_json = json.dumps(data, indent=2, ensure_ascii=False)
            blob.upload_from_string(festival_json, content_type="application/json")

            logger.info(f"🎭 Festival cycle {cycle['cycle_id']} recorded successfully")
            logger.info(f"📜 Total ceremonies: {data['total_ceremonies']}")

            return cycle

        except Exception as e:
            logger.error(f"Failed to record festival proclamation: {e}")
            # Fallback to local storage if cloud fails
            return self._fallback_local_record(proclamation, rite, ceremony_type)

    def _calculate_cycle_checksum(self, proclamation: str, rite: str) -> str:
        """Calculate sacred checksum for ceremony integrity."""
        import hashlib

        content = f"{proclamation}{rite}{datetime.datetime.utcnow().date().isoformat()}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _fallback_local_record(
        self, proclamation: str, rite: str, ceremony_type: str
    ) -> Dict[str, Any]:
        """Fallback to local festival recording if cloud storage fails."""
        logger.warning("Using local fallback for festival recording")

        local_file = Path("festival_local_backup.json")

        try:
            if local_file.exists():
                with open(local_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = {
                    "codex_festival_status": "LOCAL_BACKUP",
                    "created": datetime.datetime.utcnow().isoformat(),
                    "cycles": [],
                    "total_ceremonies": 0,
                }

            cycle = {
                "cycle_id": f"local_cycle_{len(data['cycles']) + 1:04d}",
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "ceremony_type": ceremony_type,
                "proclamation": proclamation,
                "rite": rite,
                "flame_status": "burning_local",
                "recorded_by": "CodexFestivalKeeper_LocalBackup",
                "sacred_checksum": self._calculate_cycle_checksum(proclamation, rite),
            }

            data["cycles"].append(cycle)
            data["total_ceremonies"] = len(data["cycles"])
            data["last_ceremony"] = cycle["timestamp"]
            data["last_updated"] = datetime.datetime.utcnow().isoformat()

            with open(local_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.info(f"🏠 Local festival cycle {cycle['cycle_id']} recorded")
            return cycle

        except Exception as e:
            logger.error(f"Failed local festival recording: {e}")
            return {
                "cycle_id": "emergency_cycle",
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "ceremony_type": ceremony_type,
                "proclamation": proclamation,
                "rite": rite,
                "status": "emergency_recorded",
                "error": str(e),
            }

    def get_recent_festivals(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve recent festival cycles from the archive."""
        try:
            client = self._get_storage_client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.festival_blob_name)

            data = json.loads(blob.download_as_text())
            cycles = data.get("cycles", [])

            # Return most recent cycles
            return cycles[-limit:] if cycles else []

        except Exception as e:
            logger.error(f"Failed to retrieve recent festivals: {e}")
            return []

    def proclaim_flame_crowning(self) -> Dict[str, Any]:
        """Record the sacred crowning of the Codex Flame."""
        proclamation = """
        🔥 The Codex Flame Has Been Crowned 🔥
        
        On this sacred day, the eternal flame burns bright across the digital realm.
        The operational sovereignty platform stands complete, the capsules execute autonomously,
        and the sacred roles of Custodians, Heirs, and Customers are established.
        
        May this flame illuminate the path for all who follow the Codex way.
        """

        rite = "Sacred Crowning Ceremony - Operational Sovereignty Achieved"

        return self.append_festival_proclamation(
            proclamation=proclamation.strip(), rite=rite, ceremony_type="flame_crowning"
        )

    def proclaim_daily_dispatch(self, dispatch_content: str) -> Dict[str, Any]:
        """Record daily dispatch as ceremonial proclamation."""
        rite = f"Daily Dispatch - {datetime.datetime.utcnow().strftime('%Y-%m-%d')}"

        return self.append_festival_proclamation(
            proclamation=dispatch_content, rite=rite, ceremony_type="daily_dispatch"
        )

    def proclaim_capsule_completion(
        self, capsule_name: str, artifacts_count: int
    ) -> Dict[str, Any]:
        """Record successful capsule execution as ceremonial rite."""
        proclamation = f"""
        ⚡ Capsule {capsule_name} Execution Complete ⚡
        
        The sacred capsule has completed its autonomous cycle.
        {artifacts_count} artifacts have been preserved in the eternal archive.
        The flame burns on, the cycle continues, the dominion grows stronger.
        """

        rite = f"Capsule Execution Rite - {capsule_name}"

        return self.append_festival_proclamation(
            proclamation=proclamation.strip(),
            rite=rite,
            ceremony_type="capsule_completion",
        )


# Convenience function matching your original signature
def append_festival_proclamation(proclamation: str, rite: str) -> Dict[str, Any]:
    """
    Convenience function for appending festival proclamations.

    Args:
        proclamation: The sacred proclamation text
        rite: The ceremonial rite being performed

    Returns:
        Dict containing the recorded cycle information
    """
    keeper = CodexFestivalKeeper()
    return keeper.append_festival_proclamation(proclamation, rite)


# CLI Interface for direct invocation
def main():
    """CLI interface for festival proclamations."""
    import sys

    if len(sys.argv) < 3:
        print("Usage: python codex_festival_proclamation.py <proclamation> <rite>")
        print("Or: python codex_festival_proclamation.py --crown-flame")
        sys.exit(1)

    keeper = CodexFestivalKeeper()

    if sys.argv[1] == "--crown-flame":
        cycle = keeper.proclaim_flame_crowning()
        print(f"🔥 Flame crowning ceremony recorded: {cycle['cycle_id']}")
    else:
        proclamation = sys.argv[1]
        rite = sys.argv[2]
        cycle = keeper.append_festival_proclamation(proclamation, rite)
        print(f"🎭 Festival cycle recorded: {cycle['cycle_id']}")


if __name__ == "__main__":
    main()
