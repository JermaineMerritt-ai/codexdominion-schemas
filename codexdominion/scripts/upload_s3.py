#!/usr/bin/env python3
"""
Codex Dominion S3 Upload Script

Uploads artifacts to S3 for global syndication.
Reads directly from artifact manifests and uploads individual files.
"""

import json
import os
from pathlib import Path

import boto3

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "artifact.manifest.json"


def main() -> None:
    """Upload artifacts to S3 based on manifest"""
    print("🔥 CODEX DOMINION S3 SYNDICATOR")
    print("=" * 60)

    # Load manifest
    if not MANIFEST.exists():
        print(f"❌ Manifest not found: {MANIFEST}")
        return

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    # Get S3 bucket from destinations
    bucket = data.get("syndication_config", {}).get("s3_bucket")
    if not bucket:
        print("❌ S3 bucket not set in manifest")
        return

    print(f"📋 Syndication ID: {data.get('syndication_id', 'unknown')}")
    print(f"📦 Bucket: {bucket}")
    print()

    # Check AWS credentials
    aws_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret = os.environ.get("AWS_SECRET_ACCESS_KEY")

    if not aws_key or not aws_secret:
        print("⚠️  AWS credentials not configured")
        print("   Set environment variables:")
        print("   - AWS_ACCESS_KEY_ID")
        print("   - AWS_SECRET_ACCESS_KEY")
        print()
        return

    # Initialize S3 client
    region = os.environ.get("AWS_REGION", "us-east-1")
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret,
        region_name=region
    )

    print(f"🌐 Region: {region}")
    print()

    uploaded_count = 0

    # Upload artifacts from each capsule
    for artifact in data.get("artifacts", []):
        artifact_id = artifact["id"]
        print(f"📤 Uploading: {artifact['name']}")

        # Load capsule-specific artifact.json
        capsule_artifact = ROOT / artifact["capsule_path"] / "artifact.json"
        if capsule_artifact.exists():
            capsule_data = json.loads(
                capsule_artifact.read_text(encoding="utf-8")
            )

            # Upload each file in the capsule
            for file_entry in capsule_data.get("files", []):
                src = ROOT / file_entry["path"]

                if not src.exists():
                    print(f"  ⚠️  File not found: {src.name}")
                    continue

                filename = Path(file_entry['path']).name
                key = f"artifacts/{artifact_id}/{filename}"
                extra = {
                    "ContentType": file_entry["contentType"],
                    "CacheControl": "public, max-age=3600",
                    "ACL": "public-read"
                }

                try:
                    s3.upload_file(str(src), bucket, key, ExtraArgs=extra)
                    url = f"https://{bucket}.s3.{region}.amazonaws.com/{key}"
                    print(f"  ✅ {src.name}")
                    print(f"     {url}")
                    uploaded_count += 1
                except Exception as e:
                    print(f"  ❌ Failed to upload {src.name}: {e}")

            # Upload capsule artifact.json
            key = f"artifacts/{artifact_id}/artifact.json"
            try:
                s3.upload_file(
                    str(capsule_artifact),
                    bucket,
                    key,
                    ExtraArgs={
                        "ContentType": "application/json",
                        "ACL": "public-read"
                    }
                )
                print("  ✅ artifact.json")
                uploaded_count += 1
            except Exception as e:
                print(f"  ❌ Failed to upload metadata: {e}")

        print()

    # Upload main manifest
    try:
        s3.upload_file(
            str(MANIFEST),
            bucket,
            "artifacts/manifest.json",
            ExtraArgs={
                "ContentType": "application/json",
                "ACL": "public-read"
            }
        )
        print("✅ Uploaded main manifest")
        uploaded_count += 1
    except Exception as e:
        print(f"❌ Failed to upload manifest: {e}")

    # Upload index
    idx = ROOT / "manifests" / "index.json"
    if idx.exists():
        try:
            s3.upload_file(
                str(idx),
                bucket,
                "artifacts/index.json",
                ExtraArgs={
                    "ContentType": "application/json",
                    "ACL": "public-read"
                }
            )
            print("✅ Uploaded index")
            uploaded_count += 1
        except Exception as e:
            print(f"❌ Failed to upload index: {e}")

    print()
    print(f"🚀 SYNDICATION COMPLETE: {uploaded_count} files uploaded")
    print("✨ Artifacts live on CDN!")


if __name__ == "__main__":
    main()
