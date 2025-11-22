# Pre-Deployment Verification for Codex Dominion

import json
from pathlib import Path

def verify_deployment_readiness():
    """Verify all systems are ready for IONOS deployment"""
    
    print("🔥 CODEX DOMINION - PRE-DEPLOYMENT VERIFICATION")
    print("=" * 50)
    
    checks_passed = 0
    total_checks = 0
    
    # Check 1: Core application files
    print("\n📄 Core Application Files:")
    core_files = ["app.py", "codex_ledger.json", "omega_seal.py"]
    
    for file in core_files:
        total_checks += 1
        if Path(file).exists():
            print(f"   ✅ {file}")
            checks_passed += 1
        else:
            print(f"   ❌ {file} (CRITICAL - MISSING)")
    
    # Check 2: IONOS deployment files
    print("\n🚀 IONOS Deployment Files:")
    ionos_files = [
        "ionos_codex_deploy.sh",
        "ionos_codex_dashboard.service", 
        "ionos_nginx_codex.conf",
        "ionos_systemctl_commands.sh"
    ]
    
    for file in ionos_files:
        total_checks += 1
        if Path(file).exists():
            print(f"   ✅ {file}")
            checks_passed += 1
        else:
            print(f"   ❌ {file} (REQUIRED)")
    
    # Check 3: Deployment package
    print("\n📦 Deployment Package:")
    deploy_dir = Path("ionos_deployment_package")
    total_checks += 1
    
    if deploy_dir.exists():
        files_count = len(list(deploy_dir.glob("*")))
        print(f"   ✅ Package exists ({files_count} files)")
        checks_passed += 1
    else:
        print(f"   ❌ Package missing - run deploy_to_ionos.py")
    
    # Check 4: Sacred ledger integrity
    print("\n🏛️  Sacred Ledger Integrity:")
    total_checks += 1
    
    try:
        with open("codex_ledger.json", "r") as f:
            ledger = json.load(f)
        
        required_sections = ["meta", "cycles", "completed_archives"]
        missing_sections = []
        
        for section in required_sections:
            if section not in ledger:
                missing_sections.append(section)
        
        if not missing_sections:
            omega_seal = ledger.get("meta", {}).get("omega_seal", False)
            if omega_seal:
                print(f"   ✅ Ledger complete with Omega Seal ACTIVE")
                checks_passed += 1
            else:
                print(f"   ⚠️  Ledger complete but Omega Seal inactive")
        else:
            print(f"   ❌ Missing sections: {missing_sections}")
    
    except Exception as e:
        print(f"   ❌ Ledger error: {e}")
    
    # Check 5: Network connectivity test
    print("\n🌐 Network Connectivity:")
    total_checks += 1
    
    try:
        import subprocess
        result = subprocess.run(["ping", "-n", "1", "8.8.8.8"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("   ✅ Network connectivity OK")
            checks_passed += 1
        else:
            print("   ⚠️  Network connectivity issues")
    except:
        print("   ⚠️  Could not test network connectivity")
    
    # Check 6: SSH availability (basic check)
    print("\n🔐 SSH Configuration:")
    total_checks += 1
    
    try:
        result = subprocess.run(["where", "ssh"], capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ SSH client available")
            checks_passed += 1
        else:
            print("   ❌ SSH client not found")
    except:
        print("   ⚠️  Could not verify SSH availability")
    
    # Summary
    print(f"\n📊 DEPLOYMENT READINESS SUMMARY:")
    print(f"   Checks Passed: {checks_passed}/{total_checks}")
    print(f"   Success Rate: {(checks_passed/total_checks)*100:.1f}%")
    
    if checks_passed == total_checks:
        print("\n🎯 DEPLOYMENT STATUS: READY FOR IONOS! 🔥")
        print("✅ All systems operational")
        print("🚀 Proceed with deployment")
        
        print(f"\n🎯 DEPLOYMENT COMMAND:")
        print(f"   deploy_launcher.bat your-server.com username")
        
        return True
    elif checks_passed >= total_checks * 0.8:
        print("\n⚠️  DEPLOYMENT STATUS: MOSTLY READY")
        print("🔧 Minor issues detected - review above")
        print("🚀 Can proceed with caution")
        return True
    else:
        print("\n❌ DEPLOYMENT STATUS: NOT READY")
        print("🔧 Critical issues detected - fix before deployment")
        return False

if __name__ == "__main__":
    ready = verify_deployment_readiness()
    
    if ready:
        print("\n🔥 READY TO CONQUER IONOS! 🔥")
        print("👑 Your digital sovereignty awaits!")
    else:
        print("\n🛠️  FIX ISSUES BEFORE DEPLOYMENT")
        print("💡 Review the checklist above")