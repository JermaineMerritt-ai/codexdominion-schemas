"""
🔥 CREATIVE INTELLIGENCE ENGINE - FLASK DASHBOARD INTEGRATION TEST 🔥

Test script to verify the Creative Intelligence Engine is fully integrated
with the Flask Dashboard.
"""

import sys
import io
import requests
import json
from datetime import datetime

# Fix Windows UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://localhost:5000"

def print_section(title: str):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"🔥 {title}")
    print("=" * 80 + "\n")

def test_creative_dashboard():
    """Test the main Creative Intelligence Engine dashboard"""
    print_section("TEST 1: Main Dashboard Access")
    
    try:
        response = requests.get(f"{BASE_URL}/creative/")
        if response.status_code == 200:
            print("✅ Dashboard accessible at /creative/")
            print(f"   Response length: {len(response.text)} characters")
            if "Creative Intelligence Engine" in response.text:
                print("   ✓ Dashboard HTML contains correct title")
        else:
            print(f"❌ Dashboard returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Flask server not running! Start with: python flask_dashboard.py")
        return False
    
    return True

def test_create_project():
    """Test project creation"""
    print_section("TEST 2: Project Creation")
    
    project_description = """
    Create a youth entrepreneurship video course. Target audience: teenagers and young adults (13-25).
    Content should be energetic, modern, and inspirational. Include topics: business planning, marketing,
    finance basics, and digital presence. Brand: CodexDominion (sovereign, empowering, innovative).
    Output: Multi-platform video series for YouTube, TikTok, and Instagram.
    """
    
    try:
        response = requests.post(
            f"{BASE_URL}/creative/api/project/create",
            json={"description": project_description.strip()}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                project_id = data.get('project_id')
                print(f"✅ Project created successfully")
                print(f"   Project ID: {project_id}")
                print(f"   Type: {data.get('project_type')}")
                print(f"   Complexity: {data.get('complexity')}")
                print(f"   Required Mediums: {data.get('required_mediums')}")
                return project_id
            else:
                print(f"❌ Project creation failed: {data}")
                return None
        else:
            print(f"❌ Request failed with status {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_project_status(project_id: str):
    """Test project status retrieval"""
    print_section("TEST 3: Project Status")
    
    try:
        response = requests.get(f"{BASE_URL}/creative/api/project/{project_id}/status")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Project status retrieved")
            print(f"   Status: {data.get('status')}")
            print(f"   Type: {data.get('type')}")
            print(f"   Created: {data.get('created_at')}")
            return True
        else:
            print(f"❌ Status request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_dashboard_data(project_id: str):
    """Test complete dashboard data retrieval"""
    print_section("TEST 4: Complete Dashboard Data")
    
    try:
        response = requests.get(f"{BASE_URL}/creative/api/dashboard/{project_id}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Dashboard data retrieved successfully\n")
            
            # Project Overview Panel
            overview = data.get('project_overview', {})
            print("📊 PROJECT OVERVIEW:")
            print(f"   Status: {overview.get('status')}")
            print(f"   Phase: {overview.get('current_phase')}")
            print(f"   Progress: {overview.get('progress_percentage', 0) * 100:.1f}%")
            
            # Studio Status Grid
            studio = data.get('studio_status', {})
            print("\n🏥 STUDIO STATUS:")
            print(f"   Overall Health: {studio.get('overall_health')}")
            print(f"   Graphics Studio: {studio.get('graphics_studio', {}).get('status')}")
            print(f"   Audio Studio: {studio.get('audio_studio', {}).get('status')}")
            print(f"   Video Studio: {studio.get('video_studio', {}).get('status')}")
            
            # Asset Dependency Map
            asset_map = data.get('asset_dependency_map', {})
            print("\n📦 ASSET DEPENDENCY MAP:")
            print(f"   Total Assets: {asset_map.get('total_assets')}")
            print(f"   Completed: {asset_map.get('completed_assets')}")
            print(f"   In Progress: {asset_map.get('in_progress_assets')}")
            
            # Continuity Report
            continuity = data.get('continuity_report', {})
            print("\n✅ CONTINUITY REPORT:")
            print(f"   Overall Score: {continuity.get('overall_score'):.2f}/10.0")
            violations = continuity.get('violations', [])
            print(f"   Violations: {len(violations)}")
            
            # Timeline Overview
            timeline = data.get('timeline_overview', {})
            print("\n📅 TIMELINE OVERVIEW:")
            print(f"   Start: {timeline.get('start_date')}")
            print(f"   End: {timeline.get('end_date')}")
            print(f"   Milestones: {len(timeline.get('milestones', []))}")
            
            # Final Deliverables Panel
            deliverables = data.get('final_deliverables', {})
            print("\n🎬 FINAL DELIVERABLES:")
            print(f"   Total: {deliverables.get('total_deliverables')}")
            print(f"   Ready: {deliverables.get('ready_deliverables')}")
            
            return True
        else:
            print(f"❌ Dashboard data request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_projects_list():
    """Test projects listing"""
    print_section("TEST 5: Projects List")
    
    try:
        response = requests.get(f"{BASE_URL}/creative/api/projects")
        
        if response.status_code == 200:
            data = response.json()
            projects = data.get('projects', [])
            print(f"✅ Projects list retrieved: {len(projects)} projects")
            
            for i, project in enumerate(projects[:3], 1):  # Show first 3
                print(f"\n   Project {i}:")
                print(f"      ID: {project.get('id')}")
                print(f"      Type: {project.get('type')}")
                print(f"      Status: {project.get('status')}")
                print(f"      Created: {project.get('created_at')}")
            
            if len(projects) > 3:
                print(f"\n   ... and {len(projects) - 3} more projects")
            
            return True
        else:
            print(f"❌ Projects list request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_all_tests():
    """Run all integration tests"""
    print("\n" + "="*80)
    print("🔥 CREATIVE INTELLIGENCE ENGINE - FLASK DASHBOARD INTEGRATION TEST 🔥")
    print("="*80)
    print(f"\nTesting server at: {BASE_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        "dashboard_access": False,
        "project_creation": False,
        "project_status": False,
        "dashboard_data": False,
        "projects_list": False
    }
    
    # Test 1: Dashboard Access
    results["dashboard_access"] = test_creative_dashboard()
    
    if not results["dashboard_access"]:
        print("\n❌ Flask server not accessible. Aborting tests.")
        return False
    
    # Test 2: Create Project
    project_id = test_create_project()
    if project_id:
        results["project_creation"] = True
        
        # Test 3: Project Status
        results["project_status"] = test_project_status(project_id)
        
        # Test 4: Dashboard Data
        results["dashboard_data"] = test_dashboard_data(project_id)
    
    # Test 5: Projects List
    results["projects_list"] = test_projects_list()
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅" if passed_test else "❌"
        print(f"{status} {test_name.replace('_', ' ').title()}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🔥🔥🔥 ALL TESTS PASSED! CREATIVE INTELLIGENCE ENGINE FULLY INTEGRATED! 🔥🔥🔥")
        print("\n👑 The Flame Burns Sovereign and Eternal! 👑")
        return True
    else:
        print(f"\n⚠️ {total - passed} tests failed. Review errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
