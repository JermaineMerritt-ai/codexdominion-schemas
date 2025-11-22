#!/usr/bin/env python3
"""
Enhanced Codex Ledger
=====================

Advanced ledger system with caching, validation, and performance optimization.
Provides backward compatibility while adding modern features.
"""

import json
import os
import time
import threading
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Enhanced logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from .settings import DATA_DIR
except ImportError:
    # Fallback for direct execution
    DATA_DIR = "data"

class EnhancedDataCache:
    """Thread-safe data caching with TTL support"""
    
    def __init__(self, default_ttl=300):
        self.cache = {}
        self.cache_ttl = {}
        self.default_ttl = default_ttl
        self.lock = threading.RLock()
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached data if valid"""
        with self.lock:
            current_time = time.time()
            if key in self.cache and key in self.cache_ttl:
                if current_time - self.cache_ttl[key] < self.default_ttl:
                    return self.cache[key]
                else:
                    # Remove expired cache
                    del self.cache[key]
                    del self.cache_ttl[key]
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set cached data with TTL"""
        with self.lock:
            self.cache[key] = value
            self.cache_ttl[key] = time.time()
    
    def clear(self):
        """Clear all cached data"""
        with self.lock:
            self.cache.clear()
            self.cache_ttl.clear()

# Global cache instance
_data_cache = EnhancedDataCache()

def _path(name): 
    """Enhanced path resolution with validation"""
    path = os.path.join(DATA_DIR, name)
    return os.path.abspath(path)

def load_json(name, default, use_cache=True, cache_ttl=300):
    """Enhanced JSON loading with caching, validation, and error recovery"""
    filepath = _path(name)
    
    try:
        # Check cache first
        if use_cache:
            cached_data = _data_cache.get(filepath)
            if cached_data is not None:
                return cached_data
        
        if os.path.exists(filepath):
            # Validate file size (prevent loading huge files accidentally)
            file_size = os.path.getsize(filepath)
            if file_size > 50 * 1024 * 1024:  # 50MB limit
                logger.warning(f"Large file detected: {filepath} ({file_size} bytes)")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate JSON structure
            if not isinstance(data, (dict, list)):
                logger.warning(f"Unexpected JSON structure in {filepath}")
            
            # Cache the data
            if use_cache:
                _data_cache.set(filepath, data, cache_ttl)
            
            return data
        else:
            # Create file with default data if it doesn't exist
            if default is not None:
                logger.info(f"Creating new file with default data: {filepath}")
                save_json(name, default)
                return default
            return {}
            
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in {filepath}: {e}")
        # Attempt to recover from backup
        backup_path = f"{filepath}.backup"
        if os.path.exists(backup_path):
            logger.info(f"Attempting recovery from backup: {backup_path}")
            try:
                with open(backup_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return default or {}
    except Exception as e:
        logger.error(f"Error loading {filepath}: {e}")
        return default or {}

def save_json(name, data, create_backup=True, atomic=True):
    """Enhanced JSON saving with atomic writes, backups, and validation"""
    filepath = _path(name)
    
    try:
        # Create directory if it doesn't exist
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Validate data before saving
        if not isinstance(data, (dict, list)):
            raise ValueError(f"Invalid data type for JSON: {type(data)}")
        
        # Create backup of existing file
        if create_backup and os.path.exists(filepath):
            backup_path = f"{filepath}.backup"
            try:
                with open(filepath, 'r') as src, open(backup_path, 'w') as dst:
                    dst.write(src.read())
            except Exception as e:
                logger.warning(f"Failed to create backup: {e}")
        
        if atomic:
            # Atomic write using temporary file
            temp_filepath = f"{filepath}.tmp"
            try:
                with open(temp_filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False, separators=(',', ': '))
                
                # Atomic rename
                os.rename(temp_filepath, filepath)
                
            except Exception as e:
                # Clean up temp file on error
                if os.path.exists(temp_filepath):
                    os.remove(temp_filepath)
                raise e
        else:
            # Direct write
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, separators=(',', ': '))
        
        # Update cache
        _data_cache.set(filepath, data)
        logger.debug(f"Successfully saved: {filepath}")
        
    except Exception as e:
        logger.error(f"Error saving {filepath}: {e}")
        raise

def append_entry(file, key, entry, validate_entry=True, max_entries=10000):
    """Enhanced entry appending with validation, limits, and deduplication"""
    try:
        # Validate entry structure
        if validate_entry and not isinstance(entry, dict):
            raise ValueError("Entry must be a dictionary")
        
        data = load_json(file, {key: []})
        
        # Ensure key exists and is a list
        if key not in data:
            data[key] = []
        elif not isinstance(data[key], list):
            logger.warning(f"Key '{key}' is not a list, converting")
            data[key] = []
        
        # Add enhanced metadata
        if 'timestamp' not in entry:
            entry['timestamp'] = datetime.now().isoformat()
        
        if 'id' not in entry:
            existing_entries = data[key]
            # Generate unique ID based on existing IDs
            existing_ids = [e.get('id', 0) for e in existing_entries if isinstance(e.get('id'), int)]
            entry['id'] = max(existing_ids, default=0) + 1
        
        # Add entry hash for deduplication
        entry_hash = hash(json.dumps(entry, sort_keys=True))
        entry['_hash'] = entry_hash
        
        # Check for duplicates
        existing_hashes = [e.get('_hash') for e in data[key]]
        if entry_hash in existing_hashes:
            logger.warning(f"Duplicate entry detected, skipping: {entry.get('id', 'unknown')}")
            return False
        
        # Check entry limits
        if len(data[key]) >= max_entries:
            logger.warning(f"Maximum entries reached ({max_entries}), removing oldest")
            data[key] = data[key][-(max_entries-1):]  # Keep most recent entries
        
        # Append entry
        data[key].append(entry)
        
        # Save with validation
        save_json(file, data)
        
        logger.info(f"Successfully appended entry to {file}:{key}")
        return entry
        
    except Exception as e:
        logger.error(f"Error appending to {file}: {e}")
        return False

def query_entries(file: str, key: str, filters: Optional[Dict] = None, 
                 sort_by: Optional[str] = None, limit: Optional[int] = None) -> List[Dict]:
    """Enhanced querying with filtering, sorting, and pagination"""
    try:
        data = load_json(file, {key: []})
        entries = data.get(key, [])
        
        # Apply filters
        if filters:
            filtered_entries = []
            for entry in entries:
                match = True
                for filter_key, filter_value in filters.items():
                    if filter_key not in entry:
                        match = False
                        break
                    
                    entry_value = entry[filter_key]
                    
                    # Support different filter types
                    if isinstance(filter_value, dict):
                        if 'equals' in filter_value and entry_value != filter_value['equals']:
                            match = False
                            break
                        if 'contains' in filter_value and filter_value['contains'].lower() not in str(entry_value).lower():
                            match = False
                            break
                        if 'greater_than' in filter_value and entry_value <= filter_value['greater_than']:
                            match = False
                            break
                    else:
                        # Simple equality check
                        if entry_value != filter_value:
                            match = False
                            break
                
                if match:
                    filtered_entries.append(entry)
            
            entries = filtered_entries
        
        # Apply sorting
        if sort_by:
            reverse = sort_by.startswith('-')
            sort_key = sort_by[1:] if reverse else sort_by
            
            try:
                entries.sort(key=lambda x: x.get(sort_key, ''), reverse=reverse)
            except Exception as e:
                logger.warning(f"Sort error: {e}")
        
        # Apply limit
        if limit and limit > 0:
            entries = entries[:limit]
        
        return entries
        
    except Exception as e:
        logger.error(f"Error querying {file}: {e}")
        return []

def update_entry(file: str, key: str, entry_id: Any, updates: Dict) -> bool:
    """Update specific entry by ID"""
    try:
        data = load_json(file, {key: []})
        entries = data.get(key, [])
        
        for i, entry in enumerate(entries):
            if entry.get('id') == entry_id:
                # Update fields
                entry.update(updates)
                entry['last_modified'] = datetime.now().isoformat()
                
                # Recalculate hash
                entry_hash = hash(json.dumps(entry, sort_keys=True))
                entry['_hash'] = entry_hash
                
                # Save changes
                save_json(file, data)
                logger.info(f"Updated entry {entry_id} in {file}:{key}")
                return True
        
        logger.warning(f"Entry {entry_id} not found in {file}:{key}")
        return False
        
    except Exception as e:
        logger.error(f"Error updating entry in {file}: {e}")
        return False

def delete_entry(file: str, key: str, entry_id: Any) -> bool:
    """Delete specific entry by ID"""
    try:
        data = load_json(file, {key: []})
        entries = data.get(key, [])
        
        original_length = len(entries)
        entries[:] = [entry for entry in entries if entry.get('id') != entry_id]
        
        if len(entries) < original_length:
            data[key] = entries
            save_json(file, data)
            logger.info(f"Deleted entry {entry_id} from {file}:{key}")
            return True
        else:
            logger.warning(f"Entry {entry_id} not found in {file}:{key}")
            return False
            
    except Exception as e:
        logger.error(f"Error deleting entry from {file}: {e}")
        return False

# Legacy compatibility classes and functions for existing code
class CodexLedger:
    """Simplified ledger wrapper for compatibility"""
    
    def __init__(self):
        self.ledger_file = "ledger.json"
    
    def add_entry(self, entry_type, description, authority="System", metadata=None):
        """Add entry using the streamlined system"""
        entry = {
            "type": entry_type,
            "description": description,
            "authority": authority,
            "metadata": metadata or {}
        }
        return append_entry(self.ledger_file, "entries", entry)
    
    def add_transaction(self, type, data, metadata=None):
        """Add transaction for compatibility"""
        entry = {
            "type": type,
            "description": f"Transaction: {type}",
            "data": data,
            "metadata": metadata or {}
        }
        result = append_entry(self.ledger_file, "entries", entry)
        # Return the timestamp as the transaction ID
        return result.get("timestamp")
    
    def get_transaction(self, transaction_id):
        """Get transaction by ID (simplified)"""
        data = load_json(self.ledger_file, {"entries": []})
        entries = data.get("entries", [])
        
        for entry in entries:
            if entry.get("timestamp") == transaction_id:
                return entry
        return None
    
    def get_entries(self, entry_type=None, authority=None, limit=None):
        """Get entries with filtering"""
        data = load_json(self.ledger_file, {"entries": []})
        entries = data.get("entries", [])
        
        if entry_type:
            entries = [e for e in entries if e.get("type") == entry_type]
        if authority:
            entries = [e for e in entries if e.get("authority") == authority]
        if limit:
            entries = entries[:limit]
        
        return entries

# Global instance for compatibility
codex_ledger = CodexLedger()

if __name__ == "__main__":
    print("📚 Streamlined Codex Ledger initialized")
    
    # Test functionality
    test_entry = {
        "type": "test",
        "description": "Test entry from streamlined ledger"
    }
    
    result = append_entry("test.json", "entries", test_entry)
    print(f"✅ Test entry created: {result.get('timestamp')}")
    
    # Load and display
    data = load_json("test.json", {"entries": []})
    print(f"📊 Total entries: {len(data.get('entries', []))}")