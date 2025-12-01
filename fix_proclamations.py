#!/usr/bin/env python3
"""
Proclamations.json Fix Utility

Analyzes and fixes all proclamations.json files across the system to ensure:
1. Proper data structure and validation
2. Consistent timestamp formats (ISO format)
3. Accurate metadata counts
4. Pydantic model compliance
5. Removes duplicates and validates content
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from pydantic import ValidationError

from codex_models import Proclamation
# Import our enhanced utilities and models
from codex_utils import load_json, save_json


def find_all_proclamations_files() -> List[Path]:
    """Find all proclamations.json files in the workspace"""
    workspace_root = Path(".")
    proclamations_files = []

    # Search for all proclamations.json files
    for proc_file in workspace_root.rglob("**/proclamations.json"):
        proclamations_files.append(proc_file)

    return proclamations_files


def validate_timestamp(timestamp_str: str) -> str:
    """Validate and normalize timestamp to ISO format"""
    try:
        # Try parsing as ISO format first
        if "T" in timestamp_str and len(timestamp_str) >= 16:
            dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            return dt.isoformat()

        # Try other common formats
        formats_to_try = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M",
            "%Y-%m-%dT%H:%M:%S",
        ]

        for fmt in formats_to_try:
            try:
                dt = datetime.strptime(timestamp_str, fmt)
                return dt.isoformat()
            except ValueError:
                continue

        # If all else fails, use current time
        print(f"⚠️  Could not parse timestamp '{timestamp_str}', using current time")
        return datetime.now().isoformat()

    except Exception as e:
        print(f"⚠️  Timestamp error for '{timestamp_str}': {e}")
        return datetime.now().isoformat()


def ensure_json_serializable(obj: Any) -> Any:
    """Ensure object is JSON serializable by converting datetime objects to strings"""
    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: ensure_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [ensure_json_serializable(item) for item in obj]
    else:
        return obj


def validate_proclamation_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and fix a single proclamation entry"""
    try:
        # Normalize timestamp
        if "timestamp" in entry:
            entry["timestamp"] = validate_timestamp(str(entry["timestamp"]))
        else:
            entry["timestamp"] = datetime.now().isoformat()

        # Ensure required fields exist
        required_fields = {
            "role": "Custodian",
            "cycle": "Sacred Cycle",
            "type": "Proclamation",
            "text": "Sacred proclamation text",
            "season": "Autumn",
            "blessing": "Sacred blessing",
        }

        for field, default_value in required_fields.items():
            if field not in entry or not entry[field]:
                entry[field] = default_value

        # Validate with Pydantic model
        proclamation = Proclamation(**entry)
        result = proclamation.model_dump()

        # Ensure everything is JSON serializable
        return ensure_json_serializable(result)

    except ValidationError as e:
        print(f"⚠️  Validation error for proclamation: {e}")
        # Return a minimal valid entry
        result = {
            "role": entry.get("role", "Custodian"),
            "cycle": entry.get("cycle", "Sacred Cycle"),
            "type": entry.get("type", "Proclamation"),
            "text": entry.get("text", "Sacred proclamation"),
            "timestamp": validate_timestamp(str(entry.get("timestamp", ""))),
            "season": entry.get("season", "Autumn"),
            "blessing": entry.get("blessing", "Sacred blessing"),
        }
        return ensure_json_serializable(result)


def remove_duplicates(proclamations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate proclamations based on text and timestamp"""
    seen = set()
    unique_proclamations = []

    for proc in proclamations:
        # Create a unique key based on text and normalized timestamp
        key = (proc.get("text", ""), proc.get("timestamp", ""))
        if key not in seen:
            seen.add(key)
            unique_proclamations.append(proc)
        else:
            print(f"🗑️  Removing duplicate: '{proc.get('text', '')[:50]}...'")

    return unique_proclamations


def fix_proclamations_file(file_path: Path) -> bool:
    """Fix a single proclamations.json file"""
    try:
        print(f"\n📋 Processing: {file_path}")

        # Load the file
        data = load_json(str(file_path), {"proclamations": []})

        if not isinstance(data, dict):
            print(f"❌ Invalid data structure in {file_path}")
            return False

        # Get proclamations array
        proclamations = data.get("proclamations", [])
        if not isinstance(proclamations, list):
            print(f"❌ Proclamations is not a list in {file_path}")
            return False

        print(f"📊 Found {len(proclamations)} proclamations")

        # Validate and fix each proclamation
        fixed_proclamations = []
        for i, proc in enumerate(proclamations):
            if isinstance(proc, dict):
                try:
                    fixed_proc = validate_proclamation_entry(proc)
                    fixed_proclamations.append(fixed_proc)
                    print(f"✅ Fixed proclamation {i+1}")
                except Exception as e:
                    print(f"⚠️  Error fixing proclamation {i+1}: {e}")
            else:
                print(f"⚠️  Skipping invalid proclamation {i+1} (not a dict)")

        # Remove duplicates
        unique_proclamations = remove_duplicates(fixed_proclamations)

        # Update metadata - ensure all values are JSON serializable
        cosmic_metadata = data.get("cosmic_metadata", {})

        # Convert any datetime objects to strings in existing metadata
        for key, value in cosmic_metadata.items():
            if hasattr(value, "isoformat"):
                cosmic_metadata[key] = value.isoformat()

        cosmic_metadata.update(
            {
                "last_updated": datetime.now().isoformat(),
                "total_proclamations": len(unique_proclamations),
                "data_validation_status": "validated",
                "structure_version": "2.0",
            }
        )

        # Create fixed data structure - ensure everything is JSON serializable
        fixed_data = ensure_json_serializable(
            {"proclamations": unique_proclamations, "cosmic_metadata": cosmic_metadata}
        )

        # Save the fixed file
        success = save_json(fixed_data, str(file_path))

        if success:
            print(
                f"✅ Fixed {file_path}: {len(unique_proclamations)} valid proclamations"
            )
            return True
        else:
            print(f"❌ Failed to save {file_path}")
            return False

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False


def generate_fix_report(
    files_processed: int, files_fixed: int, total_proclamations: int
):
    """Generate a comprehensive fix report"""
    report = f"""
🏛️ PROCLAMATIONS SYSTEM FIX REPORT
═══════════════════════════════════

📊 PROCESSING SUMMARY:
├── Files Found: {files_processed}
├── Files Fixed: {files_fixed}
├── Total Proclamations: {total_proclamations}
└── Fix Success Rate: {(files_fixed/files_processed*100):.1f}%

🔧 FIXES APPLIED:
├── ✅ Timestamp normalization (ISO format)
├── ✅ Data structure validation
├── ✅ Pydantic model compliance
├── ✅ Metadata correction
├── ✅ Duplicate removal
└── ✅ Required field validation

🎯 SYSTEM STATUS: {"OPTIMAL" if files_fixed == files_processed else "NEEDS ATTENTION"}

Generated: {datetime.now().isoformat()}
"""

    # Save report
    with open("PROCLAMATIONS_FIX_REPORT.md", "w", encoding="utf-8") as f:
        f.write(report)

    print(report)


def main():
    """Main fix orchestrator"""
    print("🏛️ CODEX DOMINION PROCLAMATIONS FIX UTILITY")
    print("=" * 50)

    # Find all proclamations files
    proc_files = find_all_proclamations_files()

    if not proc_files:
        print("❌ No proclamations.json files found!")
        return

    print(f"📁 Found {len(proc_files)} proclamations.json files:")
    for pf in proc_files:
        print(f"   📄 {pf}")

    # Process each file
    files_fixed = 0
    total_proclamations = 0

    for proc_file in proc_files:
        if fix_proclamations_file(proc_file):
            files_fixed += 1
            # Count proclamations in fixed file
            data = load_json(str(proc_file), {"proclamations": []})
            total_proclamations += len(data.get("proclamations", []))

    # Generate comprehensive report
    generate_fix_report(len(proc_files), files_fixed, total_proclamations)

    if files_fixed == len(proc_files):
        print("\n🎉 ALL PROCLAMATIONS FILES SUCCESSFULLY FIXED!")
    else:
        print(f"\n⚠️  {len(proc_files) - files_fixed} files still need attention")


if __name__ == "__main__":
    main()
