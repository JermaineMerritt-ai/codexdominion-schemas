import os
import shutil

# Codex Dominion Cleanup Scroll
targets = [
    "recent_uploads", ".terraform", "node_modules", ".venv",
    ".mypy_cache", ".next", "coverage", "__pycache__",
    "ebooks", "templates"
]

print("🔥 Initiating Custodian’s Sweep...")

for target in targets:
    if os.path.exists(target):
        shutil.rmtree(target, ignore_errors=True)
        print(f"✅ Removed {target}")

print("✨ Sweep complete. Workspace purified.")
