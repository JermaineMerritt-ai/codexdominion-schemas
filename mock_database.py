"""
Mock database integration for testing capsule runs when Cloud SQL is unavailable
"""
import hashlib
import json
import datetime
from typing import Dict, Any, List, Optional

class MockCapsuleDatabase:
    """Mock database for local testing and development"""
    
    def __init__(self):
        self.runs = []  # In-memory storage for testing
        self.next_id = 1
        
    def record_capsule_run(self, capsule_slug: str, actor: str, artifact_uri: str, 
                          checksum: str, status: str = "success", 
                          execution_data: Optional[Dict] = None) -> int:
        """Mock record capsule run"""
        
        run_record = {
            "id": self.next_id,
            "capsule_slug": capsule_slug,
            "actor": actor,
            "artifact_uri": artifact_uri, 
            "checksum": checksum,
            "status": status,
            "execution_data": execution_data,
            "executed_at": datetime.datetime.utcnow()
        }
        
        self.runs.append(run_record)
        run_id = self.next_id
        self.next_id += 1
        
        print(f"📝 [MOCK] Recorded capsule run: {capsule_slug} (ID: {run_id})")
        
        # Save to disk for persistence
        save_mock_db(self)
        
        return run_id
    
    def get_capsule_runs(self, capsule_slug: Optional[str] = None, 
                        limit: int = 10) -> List[Dict[str, Any]]:
        """Mock get capsule runs"""
        
        if capsule_slug:
            filtered_runs = [r for r in self.runs if r["capsule_slug"] == capsule_slug]
        else:
            filtered_runs = self.runs
        
        # Sort by executed_at desc and limit
        filtered_runs.sort(key=lambda x: x["executed_at"], reverse=True)
        
        # Convert to serializable format
        result = []
        for run in filtered_runs[:limit]:
            run_dict = dict(run)
            run_dict["executed_at"] = run["executed_at"].isoformat() + "Z"
            result.append(run_dict)
        
        return result
    
    def get_capsule_stats(self) -> Dict[str, Any]:
        """Mock get capsule statistics"""
        
        # Group by capsule
        capsule_stats = {}
        
        for run in self.runs:
            slug = run["capsule_slug"]
            if slug not in capsule_stats:
                capsule_stats[slug] = {
                    "total_runs": 0,
                    "successful_runs": 0,
                    "failed_runs": 0,
                    "last_execution": None
                }
            
            capsule_stats[slug]["total_runs"] += 1
            if run["status"] == "success":
                capsule_stats[slug]["successful_runs"] += 1
            elif run["status"] == "error":
                capsule_stats[slug]["failed_runs"] += 1
                
            if not capsule_stats[slug]["last_execution"]:
                capsule_stats[slug]["last_execution"] = run["executed_at"]
            elif run["executed_at"] > capsule_stats[slug]["last_execution"]:
                capsule_stats[slug]["last_execution"] = run["executed_at"]
        
        # Calculate success rates and convert timestamps
        for stats in capsule_stats.values():
            if stats["total_runs"] > 0:
                stats["success_rate"] = (stats["successful_runs"] / stats["total_runs"]) * 100
            else:
                stats["success_rate"] = 0
            
            # Convert last_execution to string if it's a datetime
            if stats["last_execution"] and hasattr(stats["last_execution"], 'isoformat'):
                stats["last_execution"] = stats["last_execution"].isoformat() + "Z"
        
        # Overall stats
        total_runs = len(self.runs)
        successful_runs = len([r for r in self.runs if r["status"] == "success"])
        overall_success_rate = (successful_runs / total_runs * 100) if total_runs > 0 else 0
        
        return {
            "overall": {
                "total_runs": total_runs,
                "active_capsules": len(capsule_stats),
                "successful_runs": successful_runs,
                "overall_success_rate": round(overall_success_rate, 1)
            },
            "by_capsule": capsule_stats
        }
    
    def verify_artifact_integrity(self, run_id: int, current_checksum: str) -> bool:
        """Mock verify artifact integrity"""
        for run in self.runs:
            if run["id"] == run_id:
                return run["checksum"] == current_checksum
        return False

def calculate_execution_checksum(execution_data: Dict[str, Any]) -> str:
    """Calculate SHA256 checksum of execution data for integrity verification"""
    
    # Convert to JSON with sorted keys for consistent hashing
    json_str = json.dumps(execution_data, sort_keys=True, default=str)
    
    # Calculate SHA256 hash
    hash_object = hashlib.sha256(json_str.encode('utf-8'))
    return hash_object.hexdigest()

def record_capsule_run(db, capsule_slug: str, actor: str, 
                      artifact_uri: str, checksum: str, status: str = "success",
                      execution_data: Optional[Dict] = None) -> int:
    """
    Record a capsule run (works with both real and mock database)
    
    Args:
        db: Database instance (CapsuleDatabase or MockCapsuleDatabase)
        capsule_slug: The slug of the executed capsule
        actor: Who/what triggered the execution
        artifact_uri: URI where the execution artifact is stored
        checksum: SHA256 checksum of the execution data
        status: Execution status (default: 'success')
        execution_data: Optional execution metadata
        
    Returns:
        int: The ID of the created run record
    """
    return db.record_capsule_run(capsule_slug, actor, artifact_uri, checksum, status, execution_data)

# Global mock database instance for testing
import pickle
import os

def get_persistent_mock_db():
    """Get a persistent mock database that saves to disk"""
    db_file = "mock_capsule_db.pkl"
    
    if os.path.exists(db_file):
        try:
            with open(db_file, 'rb') as f:
                db = pickle.load(f)
            return db
        except Exception:
            pass
    
    return MockCapsuleDatabase()

def save_mock_db(db):
    """Save mock database to disk"""
    db_file = "mock_capsule_db.pkl"
    try:
        with open(db_file, 'wb') as f:
            pickle.dump(db, f)
    except Exception:
        pass

mock_capsule_db = get_persistent_mock_db()

if __name__ == "__main__":
    # Test mock database
    print("🗄️ Testing Mock Database Integration...")
    
    # Test recording runs
    test_execution_data = {
        "test_run": True,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "metrics": {"processed": 100, "errors": 0}
    }
    
    checksum = calculate_execution_checksum(test_execution_data)
    
    # Record multiple test runs
    run_ids = []
    
    for i in range(3):
        run_id = record_capsule_run(
            mock_capsule_db,
            "signals-daily",
            f"test_integration_{i}", 
            f"file://test_artifact_{i}.json",
            checksum,
            execution_data=test_execution_data
        )
        run_ids.append(run_id)
    
    # Record a run for another capsule
    run_id = record_capsule_run(
        mock_capsule_db,
        "treasury-audit",
        "test_integration", 
        "file://treasury_test.json",
        checksum,
        execution_data=test_execution_data
    )
    run_ids.append(run_id)
    
    print(f"✅ Recorded {len(run_ids)} test runs")
    
    # Test getting runs
    signals_runs = mock_capsule_db.get_capsule_runs("signals-daily")
    print(f"✅ Retrieved {len(signals_runs)} runs for signals-daily")
    
    all_runs = mock_capsule_db.get_capsule_runs()
    print(f"✅ Retrieved {len(all_runs)} total runs")
    
    # Test stats
    stats = mock_capsule_db.get_capsule_stats()
    print(f"✅ System stats: {stats['overall']['total_runs']} total runs, {stats['overall']['overall_success_rate']}% success rate")
    print(f"✅ Active capsules: {stats['overall']['active_capsules']}")
    
    # Test integrity verification
    integrity_ok = mock_capsule_db.verify_artifact_integrity(run_ids[0], checksum)
    print(f"✅ Integrity verification: {'PASS' if integrity_ok else 'FAIL'}")
    
    print("\n🎉 Mock database integration test completed successfully!")