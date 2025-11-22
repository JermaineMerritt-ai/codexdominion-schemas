"""
Example integration of storage archiver with Codex Dominion capsules
"""
from storage_archiver import archive_snapshot, archive_bulletin, archive_analysis_report
import datetime

# Example: Integrating with signals-daily capsule
def run_signals_capsule_with_archiving():
    """Example of how to integrate archiving with capsule execution"""
    
    capsule_slug = "signals-daily"
    
    # 1. Execute capsule logic (your existing code)
    execution_results = {
        "signals_processed": 150,
        "market_analysis": {
            "trend": "bullish",
            "confidence": 0.87,
            "volatility": "moderate"
        },
        "recommendations": [
            "Increase position in tech sector",
            "Monitor energy sector closely", 
            "Diversify emerging markets"
        ]
    }
    
    # 2. Archive the execution snapshot
    try:
        snapshot_uri = archive_snapshot(execution_results, capsule_slug)
        print(f"✅ Execution archived: {snapshot_uri}")
        
        # 3. Record in database with artifact URI
        from database import CapsuleDatabase
        db = CapsuleDatabase()
        
        run_data = {
            "capsule_slug": capsule_slug,
            "actor": "system_scheduler",
            "status": "success",
            "artifact_uri": snapshot_uri,  # Link to archived artifact
            "checksum": calculate_checksum(execution_results)
        }
        
        db.record_run(run_data)
        print(f"✅ Run recorded with artifact link")
        
        return snapshot_uri
        
    except Exception as e:
        print(f"❌ Archiving failed: {e}")
        return None

# Example: Dawn bulletin generation
def generate_dawn_bulletin():
    """Generate and archive a dawn sovereignty bulletin"""
    
    bulletin_content = f"""# 🌅 Dawn Sovereignty Report

**Generated:** {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC

## 🎯 System Status: OPERATIONAL SOVEREIGNTY

### Key Metrics
- **Active Capsules:** 5/5 (100%)  
- **Daily Executions:** On Schedule
- **Storage Health:** Optimal
- **Database Status:** Synchronized

### Recent Activities
- Dawn dispatch initiated successfully
- All scheduled capsules queued
- System diagnostics: PASS

**🏆 Sovereignty maintained. Systems autonomous.**
"""
    
    try:
        bulletin_uri = archive_bulletin(bulletin_content, "dawn", "dawn-dispatch")
        print(f"✅ Dawn bulletin archived: {bulletin_uri}")
        return bulletin_uri
    except Exception as e:
        print(f"❌ Bulletin archiving failed: {e}")
        return None

def calculate_checksum(data):
    """Calculate checksum for data integrity"""
    import hashlib
    import json
    
    content = json.dumps(data, sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()

# Integration points for your existing capsules:
INTEGRATION_EXAMPLES = {
    "signals-daily": {
        "function": "run_signals_capsule_with_archiving",
        "archive_type": "snapshot",
        "schedule": "0 6 * * *"
    },
    "dawn-dispatch": {
        "function": "generate_dawn_bulletin", 
        "archive_type": "bulletin",
        "schedule": "0 6 * * *"
    },
    "treasury-audit": {
        "archive_type": "analysis_report",
        "schedule": "0 0 1 * *"
    }
}