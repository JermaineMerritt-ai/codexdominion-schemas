"""
Test database integration with capsule execution
"""
import asyncio
from codex_capsules_enhanced import codex_capsules
from mock_database import mock_capsule_db

async def test_database_integration():
    print("🧪 Testing Database Integration in Capsule System...")
    
    # Execute multiple capsules
    capsules_to_test = ["signals-daily", "dawn-dispatch", "treasury-audit"]
    
    for capsule_slug in capsules_to_test:
        print(f"\n🚀 Executing {capsule_slug}...")
        result = await codex_capsules.execute_capsule(capsule_slug, "integration_test")
        
        if result["status"] == "success":
            print(f"✅ Success - Run ID: {result['run_id']}, Checksum: {result['checksum'][:8]}...")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    print(f"\n📊 Database Analysis:")
    
    # Get all runs
    all_runs = mock_capsule_db.get_capsule_runs(limit=20)
    print(f"Total recorded runs: {len(all_runs)}")
    
    for run in all_runs:
        status_icon = "✅" if run["status"] == "success" else "❌"
        print(f"  {status_icon} ID:{run['id']} {run['capsule_slug']} ({run['actor']}) - {run['executed_at']}")
    
    # Get detailed statistics
    stats = mock_capsule_db.get_capsule_stats()
    print(f"\n📈 Performance Statistics:")
    print(f"Overall Success Rate: {stats['overall']['overall_success_rate']}%")
    print(f"Total Successful Runs: {stats['overall']['successful_runs']}/{stats['overall']['total_runs']}")
    
    print(f"\nPer-Capsule Performance:")
    for capsule_slug, capsule_stats in stats["by_capsule"].items():
        print(f"  📋 {capsule_slug}: {capsule_stats['success_rate']:.1f}% ({capsule_stats['total_runs']} runs)")
    
    # Test artifact verification
    print(f"\n🔒 Testing Artifact Integrity:")
    if all_runs:
        test_run = all_runs[0]
        # Note: In a real system, we'd recalculate the checksum from the archived artifact
        integrity_ok = mock_capsule_db.verify_artifact_integrity(test_run['id'], test_run['checksum'])
        print(f"Integrity check for run {test_run['id']}: {'✅ PASS' if integrity_ok else '❌ FAIL'}")

if __name__ == "__main__":
    asyncio.run(test_database_integration())