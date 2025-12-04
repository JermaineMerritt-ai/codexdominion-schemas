#!/usr/bin/env python3
"""
🔥 ARTIFACT FORMAT CONVERTER 🔥

Converts Codex Dominion artifacts between JSON and YAML formats.
Maintains complete data integrity and validation.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any

class ArtifactConverter:
    """Converts artifacts between JSON and YAML formats"""

    def __init__(self):
        self.root_dir = Path(__file__).parent.parent.parent
        self.artifacts_dir = self.root_dir / "artifacts"

    def json_to_yaml(self, artifact_id: str) -> bool:
        """Convert JSON artifact to YAML"""
        json_path = self.artifacts_dir / f"{artifact_id}.json"
        yaml_path = self.artifacts_dir / f"{artifact_id}.yaml"

        if not json_path.exists():
            print(f"❌ JSON file not found: {json_path}")
            return False

        print(f"📥 Loading JSON: {json_path.name}")
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"💾 Converting to YAML: {yaml_path.name}")
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        print(f"✅ Successfully converted JSON → YAML")
        return True

    def yaml_to_json(self, artifact_id: str) -> bool:
        """Convert YAML artifact to JSON"""
        yaml_path = self.artifacts_dir / f"{artifact_id}.yaml"
        json_path = self.artifacts_dir / f"{artifact_id}.json"

        if not yaml_path.exists():
            print(f"❌ YAML file not found: {yaml_path}")
            return False

        print(f"📥 Loading YAML: {yaml_path.name}")
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        print(f"💾 Converting to JSON: {json_path.name}")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✅ Successfully converted YAML → JSON")
        return True

    def validate_formats(self, artifact_id: str) -> bool:
        """Validate both JSON and YAML formats match"""
        json_path = self.artifacts_dir / f"{artifact_id}.json"
        yaml_path = self.artifacts_dir / f"{artifact_id}.yaml"

        if not json_path.exists() or not yaml_path.exists():
            print("❌ Both JSON and YAML files must exist for validation")
            return False

        print("🔍 Validating format consistency...")

        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        with open(yaml_path, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)

        # Compare key structure
        json_keys = set(self._get_all_keys(json_data))
        yaml_keys = set(self._get_all_keys(yaml_data))

        if json_keys != yaml_keys:
            print("⚠️  Key structure differs between formats")
            print(f"JSON only: {json_keys - yaml_keys}")
            print(f"YAML only: {yaml_keys - json_keys}")
            return False

        print("✅ Format validation successful - structures match")
        return True

    def _get_all_keys(self, d: Dict, parent_key: str = '') -> set:
        """Recursively get all keys from nested dict"""
        keys = set()
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            keys.add(new_key)
            if isinstance(v, dict):
                keys.update(self._get_all_keys(v, new_key))
        return keys

    def show_info(self, artifact_id: str):
        """Display information about artifact files"""
        json_path = self.artifacts_dir / f"{artifact_id}.json"
        yaml_path = self.artifacts_dir / f"{artifact_id}.yaml"

        print("\n" + "=" * 80)
        print(f"🔥 ARTIFACT FORMAT INFO: {artifact_id}")
        print("=" * 80)

        if json_path.exists():
            json_size = json_path.stat().st_size
            print(f"📄 JSON: {json_path.name} ({json_size:,} bytes)")
        else:
            print(f"📄 JSON: Not found")

        if yaml_path.exists():
            yaml_size = yaml_path.stat().st_size
            print(f"📄 YAML: {yaml_path.name} ({yaml_size:,} bytes)")
        else:
            print(f"📄 YAML: Not found")

        if json_path.exists() and yaml_path.exists():
            ratio = (yaml_size / json_size) * 100
            print(f"\n📊 Size comparison: YAML is {ratio:.1f}% of JSON size")

        print("=" * 80 + "\n")


def main():
    """Main execution"""
    converter = ArtifactConverter()
    artifact_id = "supreme-eternal-replay-archive-001"

    print("\n🔥 CODEX DOMINION ARTIFACT FORMAT CONVERTER 🔥\n")

    # Show current state
    converter.show_info(artifact_id)

    # Validate both formats
    converter.validate_formats(artifact_id)

    print("\n✨ Artifact available in both JSON and YAML formats ✨\n")


if __name__ == "__main__":
    main()
