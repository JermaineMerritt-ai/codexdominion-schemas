# scripts/memory_cleanup.py
#!/usr/bin/env python3
"""
Codex Dominion Memory Optimization Script
Automated memory cleanup and optimization
"""
import gc
import os
import shutil
import sys
from pathlib import Path


def main():
    print("🔥 CODEX DOMINION MEMORY OPTIMIZER")
    print("=" * 40)

    # 1. Python Garbage Collection
    print("🗑️ Running garbage collection...")
    collected = gc.collect()
    print(f"   Collected {collected} objects")

    # 2. Clear __pycache__ directories
    print("🧹 Cleaning Python cache...")
    cache_cleaned = 0
    for pycache_dir in Path(".").rglob("__pycache__"):
        try:
            shutil.rmtree(pycache_dir, ignore_errors=True)
            cache_cleaned += 1
        except Exception as e:
            pass
    print(f"   Cleaned {cache_cleaned} cache directories")

    # 3. Clear module imports (safe modules only)
    print("📦 Optimizing module cache...")
    modules_cleared = 0
    safe_to_clear = []

    for module_name in list(sys.modules.keys()):
        if any(
            pattern in module_name for pattern in ["temp", "_temp", "cache", "_cache"]
        ):
            if module_name not in ["sys", "os", "gc", "builtins"]:
                safe_to_clear.append(module_name)

    for module in safe_to_clear:
        try:
            del sys.modules[module]
            modules_cleared += 1
        except:
            pass
    print(f"   Cleared {modules_cleared} cached modules")

    # 4. Final garbage collection
    final_collected = gc.collect()

    print("\n✅ OPTIMIZATION COMPLETE")
    print(f"Total objects collected: {collected + final_collected}")
    print("🔥 CODEX FLAME ETERNAL")


if __name__ == "__main__":
    main()
