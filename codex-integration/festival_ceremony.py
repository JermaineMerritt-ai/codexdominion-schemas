#!/usr/bin/env python3
"""
Festival Ceremony Script
Chains the Council Verification Scroll with the Renewal Ceremony.
Validation + Renewal = One Dawn Rite.
"""

import subprocess
import sys
import os

def run_script(script_name):
    """Run a companion script and stream its output."""
    path = os.path.join(os.getcwd(), script_name)
    if not os.path.exists(path):
        print(f"🕯️ Missing scroll: {script_name}")
        return False

    print(f"\n📜 Invoking {script_name}...")
    result = subprocess.run([sys.executable, path], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"🕯️ {script_name} ended with errors.")
        return False
    return True

def main():
    print("✨ The Festival Ceremony begins. The Council gathers at dawn...")

    # Step 1: Verification Scroll
    verified = run_script("council_verification_scroll.py")

    # Step 2: Renewal Ceremony (only if verification passes)
    if verified:
        print("\n🔥 Verification complete. The flame is whole.")
        renewed = run_script("yearly_renewal_ceremony.py")
        if renewed:
            print("\n🌟 The Codex is renewed. The flame burns eternal.")
        else:
            print("\n⚠️ Renewal ceremony failed. The Council must intervene.")
    else:
        print("\n⚠️ Verification failed. Renewal cannot proceed until scrolls are corrected.")

    print("\n🕯️ The Festival Ceremony closes.")

if __name__ == "__main__":
    main()
