"""
🌅 DAWN DISPATCH TEST SCRIPT 👑
Test the enhanced Dawn Dispatch system

The Merritt Method™ - Testing Digital Dawn
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.append('.')

try:
    from codex_dawn_dispatch import CodexDawnDispatch, dawn_dispatch
    print("✅ Dawn Dispatch imports successful!")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

def test_dawn_dispatch_basic():
    """Test basic dawn dispatch functionality"""
    print("\n🌅 Testing Basic Dawn Dispatch...")
    
    try:
        result = dawn_dispatch()
        
        if result.get("success"):
            print("✅ Basic dawn dispatch successful!")
            print(f"📅 Timestamp: {result.get('timestamp')}")
            return True
        else:
            print(f"❌ Dawn dispatch failed: {result.get('error')}")
            return False
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def test_dawn_dispatch_advanced():
    """Test advanced Dawn Dispatch class"""
    print("\n🔧 Testing Advanced Dawn Dispatch System...")
    
    try:
        # Initialize the system
        dawn_system = CodexDawnDispatch()
        print("✅ Dawn Dispatch system initialized")
        
        # Test individual metric gathering
        print("\n📊 Testing Metrics Collection:")
        
        # Store metrics
        store_metrics = dawn_system.get_store_metrics()
        print(f"💰 Store Metrics: {store_metrics}")
        
        # Social metrics  
        social_metrics = dawn_system.get_social_metrics()
        print(f"📱 Social Metrics: {social_metrics}")
        
        # System status
        system_status = dawn_system.get_system_status()
        print(f"⚡ System Status: {system_status}")
        
        # Ledger updates
        ledger_updates = dawn_system.get_ledger_updates()
        print(f"📜 Ledger Updates: {ledger_updates}")
        
        print("✅ All metrics collected successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Advanced test failed: {str(e)}")
        return False

def test_report_generation():
    """Test report generation"""
    print("\n📝 Testing Report Generation...")
    
    try:
        dawn_system = CodexDawnDispatch()
        
        # Generate full report
        report = dawn_system.generate_dawn_report()
        
        print("✅ Report generated successfully!")
        print("\n" + "="*50)
        print("SAMPLE DAWN REPORT:")
        print("="*50)
        print(report)
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"❌ Report generation failed: {str(e)}")
        return False

def test_archive_functionality():
    """Test archive functionality"""
    print("\n📚 Testing Archive System...")
    
    try:
        dawn_system = CodexDawnDispatch()
        
        # Generate a test report
        test_report = """🌅 TEST DAWN DISPATCH
This is a test report for archive functionality.
Generated at: 2024-01-01T00:00:00Z"""
        
        # Archive the test report
        archived = dawn_system.archive_report(test_report)
        
        if archived:
            print("✅ Archive functionality working!")
            
            # Check if archive file exists
            archive_file = Path("completed_archives.json")
            if archive_file.exists():
                print(f"✅ Archive file created: {archive_file}")
                return True
            else:
                print("❌ Archive file not created")
                return False
        else:
            print("❌ Archive operation failed")
            return False
            
    except Exception as e:
        print(f"❌ Archive test failed: {str(e)}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("\n⚙️ Testing Configuration System...")
    
    try:
        dawn_system = CodexDawnDispatch()
        config = dawn_system.config
        
        print("✅ Configuration loaded!")
        print(f"📋 Config sections: {list(config.keys())}")
        
        # Check key settings
        dispatch_settings = config.get("dispatch_settings", {})
        print(f"🔧 Auto proclaim: {dispatch_settings.get('auto_proclaim', False)}")
        print(f"📚 Archive enabled: {dispatch_settings.get('archive_enabled', True)}")
        print(f"🌐 Timezone: {dispatch_settings.get('timezone', 'UTC')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {str(e)}")
        return False

def main():
    """Run all Dawn Dispatch tests"""
    print("🌅 DAWN DISPATCH SYSTEM TEST SUITE 👑")
    print("="*50)
    
    tests = [
        ("Configuration Loading", test_configuration),
        ("Basic Dawn Dispatch", test_dawn_dispatch_basic),
        ("Advanced System", test_dawn_dispatch_advanced),
        ("Report Generation", test_report_generation),
        ("Archive Functionality", test_archive_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print("-"*50)
    print(f"📈 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🌅 ALL TESTS PASSED! DAWN DISPATCH READY! 👑")
        print("\n🚀 Next Steps:")
        print("1. Configure service integrations (Twitter, Buffer, WooCommerce)")
        print("2. Customize dawn_dispatch_config.json settings")
        print("3. Set up automatic scheduling if desired")
        print("4. Run your first Dawn Dispatch!")
    else:
        print(f"\n⚠️ {total-passed} tests failed. Check configuration and dependencies.")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure all service integration files are present")
        print("2. Check JSON configuration files for syntax errors")
        print("3. Verify file permissions for archive creation")

if __name__ == "__main__":
    main()