from fastapi import APIRouter
from google.cloud import storage
import json

router = APIRouter()

@router.get("/artifacts/{slug}/latest")
def latest_artifact(slug: str):
    client = storage.Client()
    bucket = client.bucket("codex-artifacts-YOUR_PROJECT_ID")

    # List objects in capsule folder
    blobs = list(bucket.list_blobs(prefix=f"{slug}/"))
    if not blobs:
        return {"error": "No artifacts found"}

    # Sort by name (timestamp in filename)
    blobs.sort(key=lambda b: b.name, reverse=True)
    latest = blobs[0]
    data = latest.download_as_text()
    return json.loads(data)