#!/usr/bin/env python3
"""
Codex Dominion Artifact Packaging Script

Packages capsule artifacts for syndication across platforms.
Validates manifests, compresses assets, and prepares for distribution.
"""

import json
import tarfile
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class ArtifactPackager:
    """Package Codex Dominion artifacts for syndication"""

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.capsules_dir = self.root_dir / "capsules"
        self.manifests_dir = self.root_dir / "manifests"
        self.output_dir = self.root_dir / "dist"
        self.output_dir.mkdir(exist_ok=True)

    def load_manifest(self) -> Dict[str, Any]:
        """Load the artifact manifest"""
        manifest_path = (
            self.manifests_dir / "artifact.manifest.json"
        )
        
        if not manifest_path.exists():
            raise FileNotFoundError(f"Manifest not found: {manifest_path}")
        
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def validate_capsule(self, capsule: Dict) -> bool:
        """Validate that all required capsule files exist"""
        capsule_path = self.root_dir / capsule["capsule_path"]
        
        if not capsule_path.exists():
            print(f"❌ Capsule directory not found: {capsule_path}")
            return False
        
        for asset in capsule["assets"]:
            asset_path = capsule_path / asset["filename"]
            if not asset_path.exists():
                print(f"⚠️  Warning: Asset not found: {asset_path}")
                # Don't fail validation for missing images
                # (they may be generated)
                if asset["type"] != "image/png":
                    return False
        
        print(f"✅ Capsule validated: {capsule['name']}")
        return True

    def package_capsule(
        self, capsule: Dict, format: str = "zip"
    ) -> Path:
        """Package a single capsule"""
        capsule_id = capsule["id"]
        capsule_path = self.root_dir / capsule["capsule_path"]
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"codex-{capsule_id}-{timestamp}"
        
        if format == "zip":
            output_file = self.output_dir / f"{output_name}.zip"
            with zipfile.ZipFile(
                output_file, "w", zipfile.ZIP_DEFLATED
            ) as zipf:
                for asset in capsule["assets"]:
                    asset_path = capsule_path / asset["filename"]
                    if asset_path.exists():
                        zipf.write(
                            asset_path,
                            arcname=f"{capsule_id}/{asset['filename']}"
                        )
        
        elif format == "tar.gz":
            output_file = self.output_dir / f"{output_name}.tar.gz"
            with tarfile.open(output_file, "w:gz") as tar:
                for asset in capsule["assets"]:
                    asset_path = capsule_path / asset["filename"]
                    if asset_path.exists():
                        tar.add(
                            asset_path,
                            arcname=f"{capsule_id}/{asset['filename']}"
                        )
        
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        print(f"📦 Packaged: {output_file}")
        return output_file

    def generate_syndication_metadata(
        self, manifest: Dict
    ) -> Dict[str, Any]:
        """Generate metadata for syndication"""
        return {
            "syndication_id": manifest["syndication_id"],
            "generated_at": datetime.now().isoformat(),
            "codex_version": manifest["codex_version"],
            "total_capsules": len(manifest["artifacts"]),
            "capsules": [
                {
                    "id": capsule["id"],
                    "name": capsule["name"],
                    "type": capsule["type"],
                    "package_file": f"codex-{capsule['id']}-latest.zip",
                    "targets": capsule["syndication_targets"],
                }
                for capsule in manifest["artifacts"]
            ],
            "cdn_base_url": manifest["syndication_config"]["cdn_base_url"],
            "cache_ttl": manifest["syndication_config"]["cache_ttl"],
        }

    def package_all(self) -> List[Path]:
        """Package all capsules"""
        print("🔥 CODEX DOMINION ARTIFACT PACKAGER")
        print("=" * 60)
        
        manifest = self.load_manifest()
        print(f"📋 Loaded manifest: {manifest['syndication_id']}")
        print(f"📦 Total capsules: {len(manifest['artifacts'])}")
        print()
        
        packaged_files = []
        
        for capsule in manifest["artifacts"]:
            print(f"\n🔍 Processing capsule: {capsule['name']}")
            
            if self.validate_capsule(capsule):
                output_file = self.package_capsule(capsule)
                packaged_files.append(output_file)
            else:
                print(f"⚠️  Skipping invalid capsule: {capsule['name']}")
        
        # Generate syndication metadata
        metadata = self.generate_syndication_metadata(manifest)
        metadata_file = self.output_dir / "syndication.json"
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n📄 Syndication metadata: {metadata_file}")
        print(f"\n✅ Packaging complete: {len(packaged_files)} capsules")
        print(f"📂 Output directory: {self.output_dir}")
        
        return packaged_files


def main() -> None:
    """Main execution"""
    packager = ArtifactPackager()
    
    try:
        packaged_files = packager.package_all()
        
        print("\n🚀 READY FOR SYNDICATION")
        print("-" * 60)
        for file in packaged_files:
            size_mb = file.stat().st_size / (1024 * 1024)
            print(f"  {file.name}: {size_mb:.2f} MB")
        
        print("\n✨ Next step: Run upload_s3.py to syndicate")
        
    except Exception as e:
        print(f"\n❌ Packaging failed: {e}")
        raise


if __name__ == "__main__":
    main()
