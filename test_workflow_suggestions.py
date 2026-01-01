"""
Quick test for /api/workflow-suggestions endpoint
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_suggestions(message):
    """Test workflow suggestions with a message"""
    print(f"\n{'='*60}")
    print(f"Message: {message}")
    print('='*60)
    
    response = requests.post(
        f"{BASE_URL}/api/workflow-suggestions",
        json={"message": message}
    )
    
    data = response.json()
    suggestions = data.get("suggestions", [])
    
    print(f"Found {len(suggestions)} suggestions:")
    for i, sug in enumerate(suggestions[:5], 1):  # Show first 5
        print(f"  {i}. {sug['name']}")
        print(f"     {sug['description']}")
        print(f"     Category: {sug['category']}, Domain: {sug['domain']}")
    
    return suggestions

if __name__ == "__main__":
    print("\n🔥 TESTING /api/workflow-suggestions ENDPOINT 🔥\n")
    
    try:
        # Test 1: Customer follow-up
        test_suggestions("I need to follow up with my customers")
        
        # Test 2: Invoice reminders
        test_suggestions("Help me send payment reminders for unpaid invoices")
        
        # Test 3: Content scheduling
        test_suggestions("I want to schedule social media posts")
        
        # Test 4: Generic (should return all)
        test_suggestions("Help me automate something")
        
        print("\n✅ All tests complete!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to Flask backend")
        print("Make sure Flask is running on http://localhost:5000\n")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
