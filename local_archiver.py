"""
Local archiving system as fallback for Cloud Storage billing issues
Maintains same structure and functionality but stores artifacts locally
"""

import datetime
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


class LocalArchiver:
    """Local file system archiver with Cloud Storage compatible structure"""

    def __init__(self, base_path: str = "archives"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

        # Create directory structure
        for subdir in ["snapshots", "bulletins", "reports"]:
            (self.base_path / subdir).mkdir(exist_ok=True)

    def archive_snapshot(self, data: Dict[str, Any], capsule_slug: str) -> str:
        """Archive execution snapshot locally"""
        timestamp = datetime.datetime.utcnow()
        date_path = timestamp.strftime("%Y/%m/%d")
        filename = f"{timestamp.strftime('%Y%m%dT%H%M%SZ')}.json"

        # Create directory structure
        archive_path = self.base_path / "snapshots" / capsule_slug / date_path
        archive_path.mkdir(parents=True, exist_ok=True)

        # Prepare data with metadata
        archived_data = {
            "metadata": {
                "capsule_slug": capsule_slug,
                "timestamp": timestamp.isoformat() + "Z",
                "archive_version": "1.0",
                "archiver": "local_fallback",
            },
            "data": data,
        }

        # Write file
        file_path = archive_path / filename
        with open(file_path, "w") as f:
            json.dump(archived_data, f, indent=2, default=str)

        return f"file://{file_path.absolute()}"

    def archive_bulletin(
        self, content: str, bulletin_type: str, capsule_slug: str
    ) -> str:
        """Archive markdown bulletin locally"""
        timestamp = datetime.datetime.utcnow()
        date_path = timestamp.strftime("%Y/%m/%d")
        filename = f"{timestamp.strftime('%Y%m%dT%H%M%SZ')}.md"

        # Create directory structure
        archive_path = self.base_path / "bulletins" / bulletin_type / date_path
        archive_path.mkdir(parents=True, exist_ok=True)

        # Add metadata header to markdown
        bulletin_with_metadata = f"""---
capsule_slug: {capsule_slug}
bulletin_type: {bulletin_type}
timestamp: {timestamp.isoformat()}Z
archive_version: "1.0"
archiver: "local_fallback"
---

{content}
"""

        # Write file
        file_path = archive_path / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(bulletin_with_metadata)

        return f"file://{file_path.absolute()}"

    def archive_analysis_report(
        self, report_data: Dict[str, Any], analysis_type: str, capsule_slug: str
    ) -> str:
        """Archive analysis report locally"""
        timestamp = datetime.datetime.utcnow()
        date_str = timestamp.strftime("%Y/%m/%d")
        filename = f"{capsule_slug}-{timestamp.strftime('%Y%m%dT%H%M%SZ')}.json"

        # Create directory structure
        archive_path = self.base_path / "reports" / analysis_type / date_str
        archive_path.mkdir(parents=True, exist_ok=True)

        # Prepare report with metadata
        archived_report = {
            "metadata": {
                "capsule_slug": capsule_slug,
                "analysis_type": analysis_type,
                "timestamp": timestamp.isoformat() + "Z",
                "archive_version": "1.0",
                "archiver": "local_fallback",
            },
            "report": report_data,
        }

        # Write file
        file_path = archive_path / filename
        with open(file_path, "w") as f:
            json.dump(archived_report, f, indent=2, default=str)

        return f"file://{file_path.absolute()}"

    def list_capsule_artifacts(
        self, capsule_slug: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """List artifacts for a specific capsule"""
        artifacts = []

        # Check snapshots
        snapshots_path = self.base_path / "snapshots" / capsule_slug
        if snapshots_path.exists():
            for json_file in snapshots_path.rglob("*.json"):
                try:
                    with open(json_file, "r") as f:
                        data = json.load(f)
                    artifacts.append(
                        {
                            "type": "snapshot",
                            "path": str(json_file),
                            "uri": f"file://{json_file.absolute()}",
                            "timestamp": data.get("metadata", {}).get("timestamp", ""),
                            "size": json_file.stat().st_size,
                        }
                    )
                except Exception as e:
                    print(f"Error reading {json_file}: {e}")

        # Check bulletins
        bulletins_path = self.base_path / "bulletins"
        if bulletins_path.exists():
            for md_file in bulletins_path.rglob("*.md"):
                try:
                    with open(md_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Extract metadata from frontmatter
                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            import yaml

                            try:
                                metadata = yaml.safe_load(parts[1])
                                if metadata.get("capsule_slug") == capsule_slug:
                                    artifacts.append(
                                        {
                                            "type": "bulletin",
                                            "path": str(md_file),
                                            "uri": f"file://{md_file.absolute()}",
                                            "timestamp": metadata.get("timestamp", ""),
                                            "size": md_file.stat().st_size,
                                        }
                                    )
                            except Exception:
                                # Fallback for bulletins without proper YAML
                                if capsule_slug in str(md_file):
                                    artifacts.append(
                                        {
                                            "type": "bulletin",
                                            "path": str(md_file),
                                            "uri": f"file://{md_file.absolute()}",
                                            "timestamp": "",
                                            "size": md_file.stat().st_size,
                                        }
                                    )
                except Exception as e:
                    print(f"Error reading {md_file}: {e}")

        # Check reports
        reports_path = self.base_path / "reports"
        if reports_path.exists():
            for json_file in reports_path.rglob(f"{capsule_slug}-*.json"):
                try:
                    with open(json_file, "r") as f:
                        data = json.load(f)
                    artifacts.append(
                        {
                            "type": "report",
                            "path": str(json_file),
                            "uri": f"file://{json_file.absolute()}",
                            "timestamp": data.get("metadata", {}).get("timestamp", ""),
                            "size": json_file.stat().st_size,
                        }
                    )
                except Exception as e:
                    print(f"Error reading {json_file}: {e}")

        # Sort by timestamp string (newest first) and limit
        artifacts.sort(key=lambda x: str(x["timestamp"]), reverse=True)
        return artifacts[:limit]

    def get_storage_stats(self) -> Dict[str, Any]:
        """Get local storage statistics"""
        stats = {
            "total_artifacts": 0,
            "total_size": 0,
            "by_type": {"snapshots": 0, "bulletins": 0, "reports": 0},
            "by_capsule": {},
        }

        for artifact_type in ["snapshots", "bulletins", "reports"]:
            type_path = self.base_path / artifact_type
            if type_path.exists():
                for file_path in type_path.rglob("*"):
                    if file_path.is_file():
                        stats["total_artifacts"] += 1
                        stats["total_size"] += file_path.stat().st_size
                        stats["by_type"][artifact_type] += 1

        return stats


# Global local archiver instance
local_archiver = LocalArchiver()


# Compatibility functions that match Cloud Storage API
def archive_snapshot(data: Dict[str, Any], capsule_slug: str) -> str:
    """Archive snapshot using local fallback"""
    return local_archiver.archive_snapshot(data, capsule_slug)


def archive_bulletin(content: str, bulletin_type: str, capsule_slug: str) -> str:
    """Archive bulletin using local fallback"""
    return local_archiver.archive_bulletin(content, bulletin_type, capsule_slug)


def archive_analysis_report(
    report_data: Dict[str, Any], analysis_type: str, capsule_slug: str
) -> str:
    """Archive report using local fallback"""
    return local_archiver.archive_analysis_report(
        report_data, analysis_type, capsule_slug
    )


def list_capsule_artifacts(capsule_slug: str, limit: int = 10) -> List[Dict[str, Any]]:
    """List capsule artifacts using local fallback"""
    return local_archiver.list_capsule_artifacts(capsule_slug, limit)


if __name__ == "__main__":
    # Test the local archiver
    print("🗂️ Testing Local Archiver...")

    # Test snapshot archiving
    test_data = {
        "execution_id": "test_001",
        "status": "success",
        "metrics": {"processed": 100, "errors": 0},
    }

    snapshot_uri = archive_snapshot(test_data, "test-capsule")
    print(f"✅ Snapshot archived: {snapshot_uri}")

    # Test bulletin archiving
    bulletin_content = "# Test Bulletin\n\nThis is a test bulletin."
    bulletin_uri = archive_bulletin(bulletin_content, "test", "test-capsule")
    print(f"✅ Bulletin archived: {bulletin_uri}")

    # Test listing artifacts
    artifacts = list_capsule_artifacts("test-capsule")
    print(f"✅ Found {len(artifacts)} artifacts")

    # Show storage stats
    stats = local_archiver.get_storage_stats()
    print(f"📊 Storage Stats: {stats}")
