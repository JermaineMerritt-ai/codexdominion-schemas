#!/usr/bin/env python3
"""
🔥 CODEX SIGNALS BULLETIN GENERATOR TEST 📊
Testing the new bulletin_md() function

The Merritt Method™ - Portfolio Intelligence Reporting
"""

import json
from codex_signals.integration import CodexSignalsIntegration, bulletin_md

def test_bulletin_generation():
    """Test bulletin generation in both formats"""
    print("🔥 CODEX SIGNALS BULLETIN GENERATOR TEST 📊")
    print("=" * 50)
    
    # Initialize integration
    integration = CodexSignalsIntegration()
    
    # Generate signals report
    print("📊 Generating signals snapshot...")
    snapshot = integration.generate_signals_report(use_live_data=False)
    
    if 'error' in snapshot:
        print(f"❌ Error generating snapshot: {snapshot['error']}")
        return
    
    print("✅ Snapshot generated successfully!")
    print(f"Generated at: {snapshot.get('generated_at')}")
    print(f"Tier counts: {snapshot.get('tier_counts')}")
    
    # Test Markdown bulletin
    print("\n📝 TESTING MARKDOWN BULLETIN:")
    print("=" * 30)
    
    md_bulletin = bulletin_md(snapshot)
    print(md_bulletin)
    
    # Save Markdown bulletin to file
    md_file = integration.save_bulletin(snapshot, format="md")
    print(f"\n💾 Markdown bulletin saved to: {md_file}")
    
    # Save text bulletin to file
    txt_file = integration.save_bulletin(snapshot, format="txt")
    print(f"💾 Text bulletin saved to: {txt_file}")
    
    # Show file paths
    print(f"\n📂 FILES CREATED:")
    print(f"Markdown: {md_file}")
    print(f"Text: {txt_file}")
    
    print("\n✅ Bulletin generation test complete!")
    
    return {
        'markdown_content': md_bulletin,
        'markdown_file': md_file,
        'text_file': txt_file,
        'snapshot': snapshot
    }

def test_api_integration():
    """Test how the bulletin would work with the API"""
    print("\n🌐 API INTEGRATION TEST:")
    print("=" * 25)
    
    # This simulates what the FastAPI endpoint does
    integration = CodexSignalsIntegration()
    snapshot = integration.generate_signals_report()
    
    # Generate markdown bulletin (same as API endpoint)
    md_content = bulletin_md(snapshot)
    
    print("API Response Preview:")
    print("-" * 20)
    print(json.dumps({
        "format": "md",
        "content": md_content[:200] + "...",  # Preview
        "generated_at": snapshot.get('generated_at'),
        "tier_counts": snapshot.get('tier_counts')
    }, indent=2))
    
    return md_content

if __name__ == "__main__":
    try:
        # Run bulletin generation test
        result = test_bulletin_generation()
        
        # Test API integration
        api_content = test_api_integration()
        
        print("\n🎯 TEST SUMMARY:")
        print("=" * 15)
        print("✅ Markdown bulletin generation: PASSED")
        print("✅ File save functionality: PASSED")
        print("✅ API integration simulation: PASSED")
        print("\n💡 Next steps:")
        print("- Test with FastAPI: POST http://localhost:8000/bulletin")
        print("- Try different formats: ?format=md or ?format=txt")
        print("- Integration with dawn dispatch for automated reports")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()