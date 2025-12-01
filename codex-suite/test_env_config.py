#!/usr/bin/env python3
"""
Environment Variable Test
========================

Test script to demonstrate environment variable configuration.
"""

import os
import sys
from pathlib import Path

# Add the codex-suite to path
sys.path.insert(0, str(Path(__file__).parent))

from core.settings import *


def test_environment_variables():
    """Test environment variable configuration"""

    print("🧪 ENVIRONMENT VARIABLE CONFIGURATION TEST")
    print("=" * 50)

    print("\n📁 PATH CONFIGURATION:")
    print(f"  DATA_DIR: {DATA_DIR}")
    print(f"  BRAND_FILE: {BRAND_FILE}")
    print(f"  REDIS_URL: {REDIS_URL}")

    print("\n⚙️  SYSTEM CONFIGURATION:")
    system_config = get_config("system")
    for key, value in system_config.items():
        print(f"  {key.upper()}: {value}")

    print("\n🔌 REDIS CONFIGURATION:")
    redis_config = get_config("redis")
    for key, value in redis_config.items():
        print(f"  {key.upper()}: {value}")

    print("\n🌐 API CONFIGURATION:")
    api_config = get_config("api")
    for key, value in api_config.items():
        print(f"  {key.upper()}: {value}")

    print("\n💡 ENVIRONMENT VARIABLE EXAMPLES:")
    print("Set these in your .env file or system environment:")
    print("  export DEBUG=true")
    print("  export REDIS_ENABLED=true")
    print("  export DATA_DIR=/custom/data/path")
    print("  export API_PORT=8080")

    print("\n✅ Environment configuration test complete!")


if __name__ == "__main__":
    test_environment_variables()
