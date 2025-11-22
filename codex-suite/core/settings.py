#!/usr/bin/env python3
"""
Codex Suite Settings
==================

Core configuration module for the Codex Dominion Suite.
Centralizes all settings, paths, and configuration management.
"""

import os
from pathlib import Path
from typing import Dict, Any
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base paths
CODEX_SUITE_ROOT = Path(__file__).parent.parent
CODEX_DOMINION_ROOT = CODEX_SUITE_ROOT.parent

# Environment-configurable paths
DATA_DIR = Path(os.getenv("DATA_DIR", str(CODEX_SUITE_ROOT / "data")))
STATIC_DIR = CODEX_SUITE_ROOT / "static"
APPS_DIR = CODEX_SUITE_ROOT / "apps"
MODULES_DIR = CODEX_SUITE_ROOT / "modules"
CORE_DIR = CODEX_SUITE_ROOT / "core"

# Brand voice file path (configurable)
BRAND_FILE = Path(os.getenv("BRAND_FILE", str(STATIC_DIR / "brand_voice.md")))

# Redis URL (configurable)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Ensure directories exist
for directory in [DATA_DIR, STATIC_DIR, APPS_DIR, MODULES_DIR, CORE_DIR]:
    directory.mkdir(exist_ok=True)

# Configuration settings
CODEX_CONFIG = {
    "system": {
        "name": os.getenv("SYSTEM_NAME", "Codex Dominion Suite"),
        "version": os.getenv("SYSTEM_VERSION", "1.0.0"),
        "environment": os.getenv("ENVIRONMENT", "production"),
        "debug": os.getenv("DEBUG", "false").lower() == "true"
    },
    "dashboard": {
        "title": "👑 Codex Dominion Dashboard",
        "theme": "dark",
        "port": 8530,
        "auto_refresh": True,
        "refresh_interval": 30
    },
    "api": {
        "host": os.getenv("API_HOST", "127.0.0.1"),
        "port": int(os.getenv("API_PORT", "8531")),
        "cors_enabled": os.getenv("CORS_ENABLED", "true").lower() == "true",
        "rate_limit": int(os.getenv("RATE_LIMIT", "1000"))
    },
    "redis": {
        "url": REDIS_URL,
        "host": os.getenv("REDIS_HOST", "127.0.0.1"),
        "port": int(os.getenv("REDIS_PORT", "6379")),
        "db": int(os.getenv("REDIS_DB", "0")),
        "enabled": os.getenv("REDIS_ENABLED", "false").lower() == "true",
        "cache_ttl": int(os.getenv("REDIS_CACHE_TTL", "3600"))
    },
    "vector_db": {
        "faiss_enabled": True,
        "index_path": str(DATA_DIR / "faiss_index"),
        "dimension": 384,  # Default embedding dimension
        "similarity_threshold": 0.7
    },
    "data": {
        "ledger_file": str(DATA_DIR / "ledger.json"),
        "invocations_file": str(DATA_DIR / "invocations.json"),
        "proclamations_file": str(DATA_DIR / "proclamations.json"),
        "heartbeat_file": str(DATA_DIR / "heartbeat.json")
    },
    "security": {
        "ssl_enabled": False,
        "auth_required": False,
        "api_key_length": 32
    },
    "integrations": {
        "technical_operations_council": True,
        "video_studio_omega": True,
        "master_launcher": True,
        "spark_studio": True
    }
}

# Color scheme
CODEX_COLORS = {
    "primary": "#ff6b6b",
    "secondary": "#ee5a24", 
    "accent": "#ff9f43",
    "success": "#00ff88",
    "warning": "#feca57",
    "danger": "#ff4444",
    "dark": "#1e1e1e",
    "light": "#ffffff"
}

# Authority levels
AUTHORITY_LEVELS = {
    "Custodian": 10,
    "Emperor": 9,
    "Heirs": 8,
    "Councils": 7,
    "Technical Operations": 6,
    "Cosmos": 5,
    "Legacy": 1
}

def get_config(key_path: str = None) -> Any:
    """Get configuration value by dot notation path"""
    if not key_path:
        return CODEX_CONFIG
    
    keys = key_path.split('.')
    value = CODEX_CONFIG
    
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return None
    
    return value

def update_config(key_path: str, value: Any) -> bool:
    """Update configuration value by dot notation path"""
    try:
        keys = key_path.split('.')
        config = CODEX_CONFIG
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
        return True
    except Exception:
        return False

def get_data_path(filename: str) -> Path:
    """Get full path to data file"""
    return DATA_DIR / filename

def ensure_data_files():
    """Ensure all required data files exist"""
    data_files = {
        "ledger.json": {"entries": []},
        "invocations.json": {"invocations": []},
        "proclamations.json": {"proclamations": []},
        "heartbeat.json": {"beats": []}
    }
    
    for filename, default_content in data_files.items():
        file_path = DATA_DIR / filename
        if not file_path.exists():
            with open(file_path, 'w') as f:
                json.dump(default_content, f, indent=4)

# Initialize on import
ensure_data_files()

if __name__ == "__main__":
    print(f"🔧 Codex Suite Settings Initialized")
    print(f"📁 Root: {CODEX_SUITE_ROOT}")
    print(f"📊 Config: {json.dumps(CODEX_CONFIG, indent=2)}")