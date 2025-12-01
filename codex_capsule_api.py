import json
import os
from typing import Any, Dict, List

from fastapi import Depends, FastAPI, HTTPException
from google.cloud import storage

app = FastAPI(
    title="Codex Dominion Capsule API",
    description="Role-based access to operational sovereignty capsule artifacts",
    version="1.0.0",
)

# Use the correct project ID from your Terraform configuration
PROJECT_ID = "codex-dominion-prod"
BUCKET_NAME = f"codex-artifacts-{PROJECT_ID}"


def fetch_artifact(slug: str) -> Dict[str, Any]:
    """Fetch the latest artifact for a given capsule slug from Cloud Storage"""
    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)

        # List objects with the capsule slug prefix
        blobs = list(bucket.list_blobs(prefix=f"{slug}/"))

        if not blobs:
            raise HTTPException(
                status_code=404, detail=f"No artifacts found for capsule: {slug}"
            )

        # Sort by name (timestamp in filename) to get the latest
        blobs.sort(key=lambda b: b.name, reverse=True)
        latest = blobs[0]

        # Download and parse the artifact
        artifact_data = latest.download_as_text()
        return json.loads(artifact_data)

    except storage.exceptions.NotFound:
        raise HTTPException(
            status_code=404,
            detail=f"Bucket {BUCKET_NAME} not found or capsule {slug} does not exist",
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail=f"Invalid JSON in artifact for capsule: {slug}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching artifact: {str(e)}"
        )


@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "service": "Codex Dominion Capsule API",
        "status": "operational",
        "sovereignty": "fully autonomous",
        "available_roles": ["custodian", "heir", "customer"],
    }


@app.get("/health")
def health_check():
    """Detailed health check for Cloud Run"""
    return {
        "status": "healthy",
        "service": "codex-capsule-api",
        "bucket": BUCKET_NAME,
        "project": PROJECT_ID,
    }


@app.get("/capsules")
def list_capsules():
    """List all available capsule slugs"""
    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)

        # Get unique capsule slugs from bucket prefixes
        blobs = bucket.list_blobs()
        capsule_slugs = set()

        for blob in blobs:
            # Extract capsule slug from path (first part before /)
            parts = blob.name.split("/")
            if len(parts) > 1:
                capsule_slugs.add(parts[0])

        return {
            "available_capsules": sorted(list(capsule_slugs)),
            "total_count": len(capsule_slugs),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing capsules: {str(e)}")


@app.get("/capsules/{slug}")
def get_capsule_artifact(slug: str):
    """Get the raw artifact for a capsule (custodian-level access)"""
    return fetch_artifact(slug)


@app.get("/capsules/{slug}/{role}")
def get_capsule(slug: str, role: str):
    """Get role-based filtered view of capsule artifact"""

    # Validate role
    valid_roles = ["custodian", "heir", "customer"]
    if role not in valid_roles:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role: {role}. Must be one of {valid_roles}",
        )

    # Fetch the full artifact
    artifact = fetch_artifact(slug)

    # Return role-based filtered data
    if role == "custodian":
        # Full access to all data
        return artifact

    if role == "heir":
        # Strategic overview with tier distribution and top picks
        return {
            "capsule_slug": slug,
            "role": "heir",
            "banner": artifact.get("banner", ""),
            "tier_counts": artifact.get("tier_counts", {}),
            "top_picks": artifact.get("picks", [])[:3],
            "generated_at": artifact.get("generated_at", ""),
            "total_picks_available": len(artifact.get("picks", [])),
        }

    if role == "customer":
        # Simplified customer view with featured picks
        return {
            "capsule_slug": slug,
            "role": "customer",
            "banner": artifact.get("banner", ""),
            "featured": artifact.get("picks", [])[:2],
            "generated_at": artifact.get("generated_at", ""),
            "summary": "Featured investment guidance from operational sovereignty analysis",
        }

    # This should never be reached due to validation above
    return {"error": "Unknown role"}


@app.get("/capsules/{slug}/latest")
def get_latest_artifact(slug: str):
    """Get the latest artifact metadata without full content"""
    artifact = fetch_artifact(slug)

    return {
        "capsule_slug": slug,
        "generated_at": artifact.get("generated_at", ""),
        "title": artifact.get("title", ""),
        "banner": artifact.get("banner", ""),
        "pick_count": len(artifact.get("picks", [])),
        "tier_distribution": artifact.get("tier_counts", {}),
        "execution_id": artifact.get("execution_id", ""),
        "status": "available",
    }


# Enhanced error handling
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "Resource not found",
        "message": str(exc.detail),
        "sovereignty_status": "maintained",
    }


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "error": "Internal server error",
        "message": "Operational sovereignty system encountered an issue",
        "details": str(exc.detail),
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
