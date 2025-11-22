#!/usr/bin/env python3
"""
Comprehensive Proclamations Validation Script

Performs final validation of all proclamations.json files to ensure:
1. Proper JSON structure
2. Pydantic model compliance  
3. Metadata accuracy
4. Timestamp format consistency
5. No data corruption or errors
"""

from pathlib import Path
from typing import List, Dict, Any
from pydantic import ValidationError

from codex_utils import load_json
from codex_models import Proclamation

def validate_file_structure(file_path: str) -> Dict[str, Any]:
    """Validate a single proclamations file"""
    result = {
        'file_path': file_path,
        'exists': False,
        'valid_json': False,
        'valid_structure': False,
        'proclamations_count': 0,
        'metadata_accurate': False,
        'pydantic_valid': False,
        'issues': []
    }
    
    try:
        # Check if file exists
        path = Path(file_path)
        result['exists'] = path.exists()
        
        if not result['exists']:
            result['issues'].append("File does not exist")
            return result
        
        # Load and validate JSON
        data = load_json(file_path)
        result['valid_json'] = True
        
        # Check basic structure
        if not isinstance(data, dict):
            result['issues'].append("Root is not a dictionary")
            return result
            
        if 'proclamations' not in data:
            result['issues'].append("Missing 'proclamations' key")
            return result
            
        if 'cosmic_metadata' not in data:
            result['issues'].append("Missing 'cosmic_metadata' key")
            return result
            
        result['valid_structure'] = True
        
        # Validate proclamations
        proclamations = data['proclamations']
        result['proclamations_count'] = len(proclamations)
        
        # Check metadata accuracy
        metadata = data['cosmic_metadata']
        metadata_count = metadata.get('total_proclamations', 0)
        result['metadata_accurate'] = (metadata_count == len(proclamations))
        
        if not result['metadata_accurate']:
            result['issues'].append(f"Metadata count ({metadata_count}) doesn't match actual count ({len(proclamations)})")
        
        # Validate each proclamation with Pydantic
        valid_proclamations = 0
        for i, proc in enumerate(proclamations):
            try:
                Proclamation(**proc)
                valid_proclamations += 1
            except ValidationError as e:
                result['issues'].append(f"Proclamation {i+1} validation failed: {e}")
        
        result['pydantic_valid'] = (valid_proclamations == len(proclamations))
        
        if result['pydantic_valid']:
            result['issues'].append(f"All {valid_proclamations} proclamations are valid")
        else:
            result['issues'].append(f"Only {valid_proclamations}/{len(proclamations)} proclamations are valid")
    
    except Exception as e:
        result['issues'].append(f"Validation error: {e}")
    
    return result

def run_comprehensive_validation():
    """Run validation on all proclamations files"""
    files_to_validate = [
        "proclamations.json",
        "data/proclamations.json",
        "codex-suite/data/proclamations.json"
    ]
    
    print("🏛️ COMPREHENSIVE PROCLAMATIONS VALIDATION")
    print("=" * 50)
    
    results = []
    total_files = len(files_to_validate)
    valid_files = 0
    total_proclamations = 0
    
    for file_path in files_to_validate:
        print(f"\n📋 Validating: {file_path}")
        result = validate_file_structure(file_path)
        results.append(result)
        
        # Display results
        print(f"   📁 Exists: {'✅' if result['exists'] else '❌'}")
        print(f"   📄 Valid JSON: {'✅' if result['valid_json'] else '❌'}")
        print(f"   🏗️ Structure: {'✅' if result['valid_structure'] else '❌'}")
        print(f"   📊 Proclamations: {result['proclamations_count']}")
        print(f"   📈 Metadata Accurate: {'✅' if result['metadata_accurate'] else '❌'}")
        print(f"   🔍 Pydantic Valid: {'✅' if result['pydantic_valid'] else '❌'}")
        
        if result['issues']:
            print(f"   📝 Issues:")
            for issue in result['issues']:
                if "All" in issue and "valid" in issue:
                    print(f"      ✅ {issue}")
                else:
                    print(f"      ⚠️ {issue}")
        
        if all([result['exists'], result['valid_json'], result['valid_structure'], 
                result['metadata_accurate'], result['pydantic_valid']]):
            valid_files += 1
            total_proclamations += result['proclamations_count']
            print(f"   🎯 Status: OPTIMAL")
        else:
            print(f"   🎯 Status: NEEDS ATTENTION")
    
    # Generate final report
    print(f"\n🏛️ VALIDATION SUMMARY REPORT")
    print("=" * 40)
    print(f"📊 Files Processed: {total_files}")
    print(f"✅ Files Valid: {valid_files}")
    print(f"❌ Files with Issues: {total_files - valid_files}")
    print(f"📄 Total Proclamations: {total_proclamations}")
    print(f"📈 Success Rate: {(valid_files/total_files*100):.1f}%")
    
    if valid_files == total_files:
        print(f"\n🎉 SYSTEM STATUS: FULLY OPERATIONAL")
        print("All proclamations.json files are valid and properly structured!")
    else:
        print(f"\n⚠️ SYSTEM STATUS: REQUIRES ATTENTION")
        print(f"{total_files - valid_files} file(s) need to be fixed")
    
    return valid_files == total_files

if __name__ == "__main__":
    success = run_comprehensive_validation()
    exit(0 if success else 1)