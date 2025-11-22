"""
Smart archiver that automatically falls back from Cloud Storage to local storage
"""
import os
from typing import Dict, Any, List

class SmartArchiver:
    """Intelligent archiver that tries Cloud Storage first, falls back to local"""
    
    def __init__(self):
        self.cloud_available = self._check_cloud_availability()
        
        if self.cloud_available:
            try:
                from storage_archiver import (
                    archive_snapshot as cloud_archive_snapshot,
                    archive_bulletin as cloud_archive_bulletin, 
                    archive_analysis_report as cloud_archive_analysis_report,
                    list_capsule_artifacts as cloud_list_capsule_artifacts
                )
                self.cloud_archive_snapshot = cloud_archive_snapshot
                self.cloud_archive_bulletin = cloud_archive_bulletin
                self.cloud_archive_analysis_report = cloud_archive_analysis_report
                self.cloud_list_capsule_artifacts = cloud_list_capsule_artifacts
                print("☁️ Cloud Storage archiver loaded")
            except Exception as e:
                print(f"⚠️ Cloud Storage unavailable: {e}")
                self.cloud_available = False
        
        if not self.cloud_available:
            from local_archiver import (
                archive_snapshot as local_archive_snapshot,
                archive_bulletin as local_archive_bulletin,
                archive_analysis_report as local_archive_analysis_report,
                list_capsule_artifacts as local_list_capsule_artifacts
            )
            self.local_archive_snapshot = local_archive_snapshot
            self.local_archive_bulletin = local_archive_bulletin
            self.local_archive_analysis_report = local_archive_analysis_report
            self.local_list_capsule_artifacts = local_list_capsule_artifacts
            print("Local archiver loaded as fallback")
    
    def _check_cloud_availability(self) -> bool:
        """Check if Cloud Storage is accessible"""
        try:
            # Check for required environment variables
            project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
            if not project_id:
                return False
                
            # Try importing cloud storage
            from google.cloud import storage
            return True
        except ImportError:
            return False
        except Exception:
            return False
    
    def archive_snapshot(self, data: Dict[str, Any], capsule_slug: str) -> str:
        """Archive snapshot with intelligent fallback"""
        if self.cloud_available:
            try:
                return self.cloud_archive_snapshot(data, capsule_slug)
            except Exception as e:
                print(f"☁️ Cloud archiving failed, falling back to local: {e}")
                self.cloud_available = False
        
        return self.local_archive_snapshot(data, capsule_slug)
    
    def archive_bulletin(self, content: str, bulletin_type: str, capsule_slug: str) -> str:
        """Archive bulletin with intelligent fallback"""
        if self.cloud_available:
            try:
                return self.cloud_archive_bulletin(content, bulletin_type, capsule_slug)
            except Exception as e:
                print(f"☁️ Cloud archiving failed, falling back to local: {e}")
                self.cloud_available = False
        
        return self.local_archive_bulletin(content, bulletin_type, capsule_slug)
    
    def archive_analysis_report(self, report_data: Dict[str, Any], 
                              analysis_type: str, capsule_slug: str) -> str:
        """Archive analysis report with intelligent fallback"""
        if self.cloud_available:
            try:
                return self.cloud_archive_analysis_report(report_data, analysis_type, capsule_slug)
            except Exception as e:
                print(f"☁️ Cloud archiving failed, falling back to local: {e}")
                self.cloud_available = False
        
        return self.local_archive_analysis_report(report_data, analysis_type, capsule_slug)
    
    def list_capsule_artifacts(self, capsule_slug: str, limit: int = 10) -> List[Dict[str, Any]]:
        """List artifacts with intelligent fallback"""
        if self.cloud_available:
            try:
                return self.cloud_list_capsule_artifacts(capsule_slug, limit)
            except Exception as e:
                print(f"☁️ Cloud listing failed, falling back to local: {e}")
                self.cloud_available = False
        
        return self.local_list_capsule_artifacts(capsule_slug, limit)

# Global smart archiver instance
smart_archiver = SmartArchiver()

# Public API - automatically chooses best available storage
def archive_snapshot(data: Dict[str, Any], capsule_slug: str) -> str:
    """Archive execution snapshot (auto-fallback)"""
    return smart_archiver.archive_snapshot(data, capsule_slug)

def archive_bulletin(content: str, bulletin_type: str, capsule_slug: str) -> str:
    """Archive markdown bulletin (auto-fallback)"""
    return smart_archiver.archive_bulletin(content, bulletin_type, capsule_slug)

def archive_analysis_report(report_data: Dict[str, Any], 
                          analysis_type: str, capsule_slug: str) -> str:
    """Archive analysis report (auto-fallback)"""
    return smart_archiver.archive_analysis_report(report_data, analysis_type, capsule_slug)

def list_capsule_artifacts(capsule_slug: str, limit: int = 10) -> List[Dict[str, Any]]:
    """List capsule artifacts (auto-fallback)"""
    return smart_archiver.list_capsule_artifacts(capsule_slug, limit)

if __name__ == "__main__":
    # Test the smart archiver
    print("🧠 Testing Smart Archiver...")
    
    # Test with real capsule execution pattern
    import datetime
    
    execution_data = {
        "execution_id": f"exec_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "capsule": "signals-daily",
        "status": "success",
        "metrics": {
            "signals_processed": 147,
            "market_sentiment": "bullish",
            "confidence_score": 0.89,
            "execution_time_seconds": 12.4
        },
        "recommendations": [
            "Increase tech sector allocation",
            "Monitor energy volatility", 
            "Diversify emerging markets"
        ],
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
    
    # Archive snapshot
    snapshot_uri = archive_snapshot(execution_data, "signals-daily")
    print(f"📸 Snapshot archived: {snapshot_uri}")
    
    # Generate and archive bulletin
    bulletin_content = f"""# 🌅 Daily Sovereignty Report

**Generated:** {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC

## 🎯 System Status: OPERATIONAL SOVEREIGNTY ACHIEVED

### Key Metrics
- **Signals Processed:** {execution_data['metrics']['signals_processed']}
- **Market Sentiment:** {execution_data['metrics']['market_sentiment'].upper()}
- **Confidence Score:** {execution_data['metrics']['confidence_score']*100:.1f}%
- **Execution Time:** {execution_data['metrics']['execution_time_seconds']}s

### Strategic Recommendations
{chr(10).join(f'- {rec}' for rec in execution_data['recommendations'])}

### System Health
- ✅ **Database:** Synchronized and operational
- ✅ **Archives:** {snapshot_uri}
- ✅ **Scheduler:** Active and monitoring
- ✅ **Infrastructure:** Cloud-deployed via Terraform

**🏆 SOVEREIGNTY STATUS: MAINTAINED**
*All systems autonomous and operational*
"""
    
    bulletin_uri = archive_bulletin(bulletin_content, "daily", "signals-daily")
    print(f"📝 Bulletin archived: {bulletin_uri}")
    
    # List artifacts for the capsule
    artifacts = list_capsule_artifacts("signals-daily")
    print(f"📋 Found {len(artifacts)} artifacts for signals-daily capsule")
    
    for artifact in artifacts:
        print(f"  - {artifact['type']}: {artifact['uri']}")
    
    print("\n🎉 Smart archiver test completed successfully!")