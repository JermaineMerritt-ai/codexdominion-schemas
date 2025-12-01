"""
Cloud Storage artifact archiving for Codex Dominion capsules
"""

import datetime
import json
import os
from typing import Any, Dict

from google.cloud import storage


def archive_snapshot(snapshot: Dict[Any, Any], capsule_slug: str) -> str:
    """
    Archive a capsule execution snapshot to Cloud Storage

    Args:
        snapshot: Dictionary containing capsule execution data
        capsule_slug: Unique identifier for the capsule (e.g., 'signals-daily')

    Returns:
        str: GCS URI path to the archived snapshot
    """
    # Initialize Cloud Storage client
    client = storage.Client()

    # Use the actual Codex Dominion bucket
    bucket_name = "codex-artifacts-codex-dominion-prod"
    bucket = client.bucket(bucket_name)

    # Generate timestamp for unique artifact naming
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    # Create organized blob path: capsule/year/month/day/timestamp.json
    date_path = datetime.datetime.utcnow().strftime("%Y/%m/%d")
    blob_name = f"snapshots/{capsule_slug}/{date_path}/{ts}.json"

    # Create blob and upload snapshot
    blob = bucket.blob(blob_name)

    # Add metadata to snapshot
    enhanced_snapshot = {
        "metadata": {
            "capsule_slug": capsule_slug,
            "timestamp": ts,
            "archive_date": datetime.datetime.utcnow().isoformat(),
            "artifact_type": "execution_snapshot",
            "version": "1.0.0",
        },
        "data": snapshot,
    }

    # Upload with proper content type and metadata
    blob.metadata = {
        "capsule_slug": capsule_slug,
        "archived_at": ts,
        "artifact_type": "execution_snapshot",
    }

    blob.upload_from_string(
        json.dumps(enhanced_snapshot, indent=2, default=str),
        content_type="application/json",
    )

    # Return GCS URI
    return f"gs://{bucket_name}/{blob_name}"


def archive_bulletin(
    bulletin_content: str,
    bulletin_type: str,
    capsule_slug: str = "sovereignty-bulletin",
) -> str:
    """
    Archive a markdown bulletin to Cloud Storage

    Args:
        bulletin_content: Markdown content of the bulletin
        bulletin_type: Type of bulletin (e.g., 'daily', 'sovereignty', 'treasury')
        capsule_slug: Associated capsule slug

    Returns:
        str: GCS URI path to the archived bulletin
    """
    client = storage.Client()
    bucket_name = "codex-artifacts-codex-dominion-prod"
    bucket = client.bucket(bucket_name)

    # Generate timestamp
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    date_path = datetime.datetime.utcnow().strftime("%Y/%m/%d")

    # Create bulletin path
    blob_name = f"bulletins/{bulletin_type}/{date_path}/{ts}.md"

    # Create blob and upload
    blob = bucket.blob(blob_name)
    blob.metadata = {
        "capsule_slug": capsule_slug,
        "bulletin_type": bulletin_type,
        "archived_at": ts,
        "artifact_type": "bulletin",
    }

    blob.upload_from_string(bulletin_content, content_type="text/markdown")

    return f"gs://{bucket_name}/{blob_name}"


def archive_analysis_report(
    report_data: Dict[Any, Any], analysis_type: str, capsule_slug: str
) -> str:
    """
    Archive an analysis report (JSON) to Cloud Storage

    Args:
        report_data: Dictionary containing analysis results
        analysis_type: Type of analysis (e.g., 'treasury', 'performance', 'compliance')
        capsule_slug: Associated capsule slug

    Returns:
        str: GCS URI path to the archived report
    """
    client = storage.Client()
    bucket_name = "codex-artifacts-codex-dominion-prod"
    bucket = client.bucket(bucket_name)

    # Generate timestamp and path
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    date_path = datetime.datetime.utcnow().strftime("%Y/%m/%d")

    # Create report path
    blob_name = f"reports/{analysis_type}/{date_path}/{capsule_slug}-{ts}.json"

    # Enhanced report with metadata
    enhanced_report = {
        "metadata": {
            "capsule_slug": capsule_slug,
            "analysis_type": analysis_type,
            "timestamp": ts,
            "generated_at": datetime.datetime.utcnow().isoformat(),
            "artifact_type": "analysis_report",
            "version": "1.0.0",
        },
        "report": report_data,
    }

    # Create blob and upload
    blob = bucket.blob(blob_name)
    blob.metadata = {
        "capsule_slug": capsule_slug,
        "analysis_type": analysis_type,
        "archived_at": ts,
        "artifact_type": "analysis_report",
    }

    blob.upload_from_string(
        json.dumps(enhanced_report, indent=2, default=str),
        content_type="application/json",
    )

    return f"gs://{bucket_name}/{blob_name}"


def list_capsule_artifacts(capsule_slug: str, limit: int = 10) -> list:
    """
    List recent artifacts for a specific capsule

    Args:
        capsule_slug: Capsule to list artifacts for
        limit: Maximum number of artifacts to return

    Returns:
        list: List of artifact metadata dictionaries
    """
    client = storage.Client()
    bucket_name = "codex-artifacts-codex-dominion-prod"
    bucket = client.bucket(bucket_name)

    artifacts = []

    # Search in all artifact directories
    for prefix in ["snapshots", "bulletins", "reports"]:
        blobs = bucket.list_blobs(prefix=f"{prefix}/", max_results=limit)

        for blob in blobs:
            if capsule_slug in blob.name:
                artifacts.append(
                    {
                        "name": blob.name,
                        "uri": f"gs://{bucket_name}/{blob.name}",
                        "created": (
                            blob.time_created.isoformat() if blob.time_created else None
                        ),
                        "size": blob.size,
                        "content_type": blob.content_type,
                        "metadata": blob.metadata or {},
                    }
                )

    # Sort by creation time, newest first
    artifacts.sort(key=lambda x: x["created"] or "", reverse=True)

    return artifacts[:limit]


# Example usage functions
def example_usage():
    """Example usage of the archiving functions"""

    # Example snapshot archiving
    sample_snapshot = {
        "execution_id": "exec_001",
        "status": "success",
        "metrics": {"duration_seconds": 45.2, "items_processed": 150},
        "outputs": ["signal_1", "signal_2", "signal_3"],
    }

    snapshot_uri = archive_snapshot(sample_snapshot, "signals-daily")
    print(f"Snapshot archived: {snapshot_uri}")

    # Example bulletin archiving
    sample_bulletin = """# Daily Sovereignty Bulletin
    
## Operational Status: SOVEREIGN
    
### Key Metrics
- Capsules Active: 5
- Daily Executions: 2
- System Health: 100%
    
### Recent Activities
- Dawn dispatch completed successfully
- Signals processing optimal
- Treasury audit scheduled
    
*Generated on {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*
"""

    bulletin_uri = archive_bulletin(sample_bulletin, "daily")
    print(f"Bulletin archived: {bulletin_uri}")


if __name__ == "__main__":
    example_usage()
