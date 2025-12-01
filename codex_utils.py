"""
Enhanced Codex Utilities
=======================
Comprehensive utility functions for the Codex Dominion system
"""

import functools
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== CLEAN FUNCTIONAL UTILITIES =====


# Load JSON data with enhanced error handling
def load_json(file_path: str, default: Any = None) -> Any:
    """
    Load JSON data from file with comprehensive error handling

    Args:
        file_path: Path to JSON file
        default: Default value if file doesn't exist or fails to load

    Returns:
        Loaded JSON data or default value
    """
    path = Path(file_path)

    try:
        if not path.exists():
            logger.info(f"File not found: {file_path}, using default")
            return default if default is not None else {}

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.debug(f"Successfully loaded: {file_path}")
            return data

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        return default if default is not None else {}
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        return default if default is not None else {}


# Save JSON data with backup and validation
def save_json(data: Any, file_path: str, create_backup: bool = True) -> bool:
    """
    Save JSON data to file with backup and validation

    Args:
        data: Data to save
        file_path: Target file path
        create_backup: Whether to create backup of existing file

    Returns:
        True if successful, False otherwise
    """
    path = Path(file_path)

    try:
        # Create directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)

        # Create backup if file exists
        if create_backup and path.exists():
            backup_path = path.with_suffix(
                f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            path.rename(backup_path)
            logger.debug(f"Created backup: {backup_path}")

        # Save data
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        logger.debug(f"Successfully saved: {file_path}")
        return True

    except Exception as e:
        logger.error(f"Error saving {file_path}: {e}")
        return False


# Append entry immutably with validation
def append_entry(
    file_path: str, key: str, new_entry: Dict, max_entries: Optional[int] = None
) -> bool:
    """
    Append entry to JSON array immutably with optional size limit

    Args:
        file_path: Path to JSON file
        key: Key for the array in JSON
        new_entry: Entry to append
        max_entries: Maximum number of entries to keep (oldest removed first)

    Returns:
        True if successful, False otherwise
    """
    try:
        # Load existing data
        data = load_json(file_path, {key: []})

        # Ensure key exists and is a list
        if key not in data:
            data[key] = []
        elif not isinstance(data[key], list):
            logger.warning(f"Key '{key}' is not a list, converting")
            data[key] = []

        # Add timestamp if not present
        if isinstance(new_entry, dict) and "timestamp" not in new_entry:
            new_entry["timestamp"] = datetime.now().isoformat()

        # Append new entry
        data[key].append(new_entry)

        # Enforce size limit if specified
        if max_entries and len(data[key]) > max_entries:
            data[key] = data[key][-max_entries:]  # Keep last N entries
            logger.info(f"Trimmed {key} to {max_entries} entries")

        # Save data
        success = save_json(data, file_path, create_backup=False)

        if success:
            logger.info(f"Appended entry to {key} in {file_path}")

        return success

    except Exception as e:
        logger.error(f"Error appending to {file_path}: {e}")
        return False


# Get entries with filtering and pagination
def get_entries(
    file_path: str,
    key: str,
    limit: Optional[int] = None,
    filter_func: Optional[callable] = None,
) -> List[Dict]:
    """
    Get entries from JSON array with optional filtering and pagination

    Args:
        file_path: Path to JSON file
        key: Key for the array in JSON
        limit: Maximum number of entries to return
        filter_func: Function to filter entries

    Returns:
        List of matching entries
    """
    try:
        data = load_json(file_path, {key: []})
        entries = data.get(key, [])

        # Apply filter if provided
        if filter_func:
            entries = [entry for entry in entries if filter_func(entry)]

        # Apply limit if provided
        if limit:
            entries = entries[-limit:]  # Get last N entries

        return entries

    except Exception as e:
        logger.error(f"Error getting entries from {file_path}: {e}")
        return []


class CodexUtils:
    """Enhanced utility class for Codex operations"""

    @staticmethod
    def safe_load_json(filepath: str, default: dict = None) -> dict:
        """Safely load JSON with fallback"""
        try:
            path = Path(filepath)
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            return default or {}
        except Exception as e:
            print(f"Warning: Could not load {filepath}: {e}")
            return default or {}

    @staticmethod
    def safe_save_json(filepath: str, data: dict) -> bool:
        """Safely save JSON with error handling"""
        try:
            path = Path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)

            # Backup existing file
            if path.exists():
                backup_path = path.with_suffix(".json.backup")
                path.rename(backup_path)

            # Save new data
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"Error saving {filepath}: {e}")
            return False

    @staticmethod
    def performance_timer(func=None, *, name=None):
        """Performance timing decorator"""

        def decorator(f):
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                start = time.time()
                result = f(*args, **kwargs)
                duration = time.time() - start

                op_name = name or f.__name__
                if duration > 1.0:
                    print(f"Performance: {op_name} took {duration:.2f}s")

                return result

            return wrapper

        if func is None:
            return decorator
        else:
            return decorator(func)

    @staticmethod
    def format_currency(amount: float, currency: str = "USD") -> str:
        """Format currency with proper symbols"""
        symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
        symbol = symbols.get(currency, "$")
        return f"{symbol}{amount:,.2f}"

    @staticmethod
    def calculate_percentage_change(old_value: float, new_value: float) -> float:
        """Calculate percentage change between values"""
        if old_value == 0:
            return 100.0 if new_value > 0 else 0.0
        return ((new_value - old_value) / old_value) * 100

    @staticmethod
    def get_timestamp() -> str:
        """Get current timestamp in ISO format"""
        return datetime.now().isoformat()

    @staticmethod
    def validate_data(data: dict, required_fields: list) -> tuple[bool, list]:
        """Validate data against required fields"""
        missing = [field for field in required_fields if field not in data]
        return len(missing) == 0, missing


# Global utilities instance
utils = CodexUtils()
