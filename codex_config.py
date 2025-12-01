"""
Advanced Codex Configuration
===========================
"""

import json
from pathlib import Path
from typing import Any, Dict


class CodexConfig:
    """Advanced configuration management"""

    def __init__(self, config_file="config.json"):
        self.config_file = Path(config_file)
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration with defaults"""
        defaults = {
            "performance": {
                "cache_enabled": True,
                "cache_ttl": 300,
                "monitoring_enabled": True,
            },
            "ui": {"theme": "cosmic", "animations": True, "responsive": True},
            "data": {
                "backup_enabled": True,
                "validation_enabled": True,
                "compression": False,
            },
            "security": {"input_validation": True, "audit_logging": True},
        }

        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    file_config = json.load(f)
                    self._merge_configs(defaults, file_config)
            except Exception as e:
                print(f"Warning: Error loading config: {e}")

        return defaults

    def _merge_configs(self, base: dict, override: dict):
        """Merge configuration dictionaries"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_configs(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default=None):
        """Get configuration value"""
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split(".")
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value
        self.save()

    def save(self):
        """Save configuration to file"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")


# Global config instance
config = CodexConfig()
