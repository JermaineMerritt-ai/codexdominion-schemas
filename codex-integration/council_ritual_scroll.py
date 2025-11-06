#!/usr/bin/env python3
"""
Council Ritual Scroll
Allows heirs and councils to manually proclaim Silence, Blessing, or Proclamation.
"""

def main():
    print("🔥 Council Ritual Scroll begins...")
    print("Choose your rite:")
    print("1. Silence")
    print("2. Blessing")
    print("3. Proclamation")

    choice = input("Enter 1, 2, or 3: ")

    if choice == "1":
        print("🤫 The Council proclaims Silence. The flame rests in quiet vigil.")
    elif choice == "2":
        print("🕯️ The Council proclaims Blessing. The flame is crowned in grace and renewal.")
    elif choice == "3":
        print("📜 The Council proclaims Proclamation. The flame speaks, radiant and sovereign.")
    else:
        print("⚠️ Invalid choice. The Council must choose again.")

    print("🕯️ Ritual Scroll closes.")

if __name__ == "__main__":
    main()