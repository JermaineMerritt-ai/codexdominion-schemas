#!/usr/bin/env python3
"""
Codex Dominion Suite - Integration Test Suite
============================================

Comprehensive testing suite to verify all system components 
work together seamlessly.
"""

import sys
import os
import asyncio
import time
import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import subprocess
import requests

# Add codex-suite to path
sys.path.insert(0, str(Path(__file__).parent / "codex-suite"))

class IntegrationTester:
    """Comprehensive integration testing for Codex Dominion Suite"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.codex_path = self.base_path / "codex-suite"
        self.test_results = {}
        self.start_time = datetime.now()
        
        os.chdir(self.codex_path)
    
    def log_test(self, test_name: str, result: bool, details: str = ""):
        """Log test result"""
        status = "✅ PASS" if result else "❌ FAIL"
        message = f"{status} {test_name}"
        if details:
            message += f" - {details}"
        
        print(message)
        
        self.test_results[test_name] = {
            "passed": result,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
    
    def test_python_environment(self) -> bool:
        """Test Python environment compatibility"""
        try:
            version_info = sys.version_info
            python_ok = version_info >= (3, 8)
            
            self.log_test(
                "Python Version", 
                python_ok,
                f"Python {version_info.major}.{version_info.minor} {'(Compatible)' if python_ok else '(Requires 3.8+)'}"
            )
            
            return python_ok
            
        except Exception as e:
            self.log_test("Python Environment", False, str(e))
            return False
    
    def test_core_dependencies(self) -> bool:
        """Test core dependency imports"""
        dependencies = {
            "streamlit": "Streamlit web framework",
            "fastapi": "FastAPI REST framework", 
            "uvicorn": "ASGI server",
            "pydantic": "Data validation",
            "dotenv": "Environment management (python-dotenv)",
            "redis": "Redis caching",
            "requests": "HTTP requests",
            "faiss": "FAISS vector search (faiss-cpu)"
        }
        
        all_passed = True
        
        for module, description in dependencies.items():
            try:
                __import__(module)
                self.log_test(f"Dependency: {module}", True, description)
            except ImportError as e:
                self.log_test(f"Dependency: {module}", False, f"Missing - {description}")
                all_passed = False
        
        return all_passed
    
    def test_core_modules(self) -> bool:
        """Test core module imports"""
        modules = {
            "core.settings": "Settings management",
            "core.ai_engine": "AI processing engine",
            "core.ledger": "Blockchain-style ledger",
            "core.enhanced_memory": "FAISS vector search system",
            "core.cache": "Redis caching system"
        }
        
        all_passed = True
        
        for module, description in modules.items():
            try:
                __import__(module)
                self.log_test(f"Core Module: {module}", True, description)
            except ImportError as e:
                self.log_test(f"Core Module: {module}", False, f"Import error - {str(e)}")
                all_passed = False
        
        return all_passed
    
    def test_app_modules(self) -> bool:
        """Test application module imports"""
        modules = {
            "apps.codex_dashboard": "Main Codex Dashboard",
            "modules.spark_studio": "Spark Studio AI content generation"
        }
        
        all_passed = True
        
        for module, description in modules.items():
            try:
                __import__(module)
                self.log_test(f"App Module: {module}", True, description)
            except ImportError as e:
                self.log_test(f"App Module: {module}", False, f"Import error - {str(e)}")
                all_passed = False
        
        return all_passed
    
    def test_file_structure(self) -> bool:
        """Test required file structure"""
        required_files = [
            "main.py",
            "apps/codex_dashboard.py",
            "core/settings.py",
            "core/ai_engine.py", 
            "core/ledger.py",
            "core/enhanced_memory.py",
            "core/cache.py",
            "modules/spark_studio.py",
            "deployment.py"
        ]
        
        required_dirs = [
            "apps",
            "core", 
            "modules",
            "data",
            "static"
        ]
        
        all_passed = True
        
        # Check files
        for file_path in required_files:
            full_path = self.codex_path / file_path
            if full_path.exists():
                self.log_test(f"File: {file_path}", True, "Exists")
            else:
                self.log_test(f"File: {file_path}", False, "Missing")
                all_passed = False
        
        # Check directories  
        for dir_path in required_dirs:
            full_path = self.codex_path / dir_path
            if full_path.exists() and full_path.is_dir():
                self.log_test(f"Directory: {dir_path}", True, "Exists")
            else:
                self.log_test(f"Directory: {dir_path}", False, "Missing")
                all_passed = False
        
        return all_passed
    
    def test_api_server_startup(self) -> bool:
        """Test FastAPI server can start"""
        try:
            # Start server in background
            process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", 
                "main:app", "--host", "127.0.0.1", "--port", "8001"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Give it time to start
            time.sleep(3)
            
            # Check if still running
            if process.poll() is None:
                # Try to connect
                try:
                    response = requests.get("http://127.0.0.1:8001/health", timeout=5)
                    api_ok = response.status_code == 200
                    
                    self.log_test("FastAPI Server", api_ok, f"Started on port 8001, health: {response.status_code}")
                    
                    # Cleanup
                    process.terminate()
                    process.wait(timeout=5)
                    
                    return api_ok
                    
                except requests.RequestException as e:
                    self.log_test("FastAPI Server", False, f"Connection failed: {e}")
                    process.terminate()
                    return False
            else:
                # Server failed to start
                stderr = process.stderr.read().decode() if process.stderr else "Unknown error"
                self.log_test("FastAPI Server", False, f"Failed to start: {stderr[:100]}...")
                return False
                
        except Exception as e:
            self.log_test("FastAPI Server", False, str(e))
            return False
    
    def test_memory_system(self) -> bool:
        """Test enhanced memory system functionality"""
        try:
            from core.enhanced_memory import enhanced_codex_memory
            
            if enhanced_codex_memory is None:
                self.log_test("Memory System", False, "Enhanced memory not initialized")
                return False
            
            # Test basic memory operations
            test_memory = {
                "content": "Integration test memory entry",
                "category": "test",
                "tags": ["integration", "test", "memory"]
            }
            
            # Store memory
            result = enhanced_codex_memory.store_memory(**test_memory)
            if not result:
                self.log_test("Memory System", False, "Failed to store test memory")
                return False
            
            # Search memory
            search_results = enhanced_codex_memory.search_memories("integration test")
            found = any("integration test" in str(mem).lower() for mem in search_results)
            
            if found:
                self.log_test("Memory System", True, "Store and search operations successful")
                return True
            else:
                self.log_test("Memory System", False, "Search operation failed")
                return False
                
        except Exception as e:
            self.log_test("Memory System", False, str(e))
            return False
    
    def test_cache_system(self) -> bool:
        """Test caching system functionality"""
        try:
            from core.cache import codex_cache
            
            # Test cache operations
            test_key = "integration_test"
            test_value = {"message": "Integration test cache entry", "timestamp": time.time()}
            
            # Set value
            set_result = codex_cache.set("test", test_key, test_value)
            if not set_result:
                self.log_test("Cache System", False, "Failed to set cache value")
                return False
            
            # Get value
            retrieved = codex_cache.get("test", test_key)
            if retrieved and retrieved["message"] == test_value["message"]:
                # Get cache stats
                stats = codex_cache.get_stats()
                backend = stats.get("backend", "unknown")
                
                self.log_test("Cache System", True, f"Operations successful (backend: {backend})")
                return True
            else:
                self.log_test("Cache System", False, "Retrieval failed")
                return False
                
        except Exception as e:
            self.log_test("Cache System", False, str(e))
            return False
    
    def test_ai_engine(self) -> bool:
        """Test AI engine functionality"""
        try:
            from core.ai_engine import ai_engine
            
            # Test basic AI processing
            test_request = "Hello, this is an integration test"
            result = ai_engine.process_request(test_request)
            
            if result and isinstance(result, str) and len(result) > 0:
                self.log_test("AI Engine", True, "Processing request successful")
                return True
            else:
                self.log_test("AI Engine", False, "Processing request failed")
                return False
                
        except Exception as e:
            self.log_test("AI Engine", False, str(e))
            return False
    
    def test_ledger_system(self) -> bool:
        """Test ledger system functionality"""
        try:
            from core.ledger import codex_ledger
            
            # Test ledger operations
            test_transaction = {
                "type": "integration_test",
                "data": {"test": "Integration test transaction"},
                "metadata": {"source": "integration_test"}
            }
            
            # Add transaction (using correct parameter names)
            tx_id = codex_ledger.add_transaction(
                type=test_transaction["type"],
                data=test_transaction["data"],
                metadata=test_transaction["metadata"]
            )
            if not tx_id:
                self.log_test("Ledger System", False, "Failed to add transaction")
                return False
            
            # Verify transaction
            transaction = codex_ledger.get_transaction(tx_id)
            if transaction and transaction.get("type") == "integration_test":
                self.log_test("Ledger System", True, "Transaction operations successful")
                return True
            else:
                self.log_test("Ledger System", False, "Transaction verification failed")
                return False
                
        except Exception as e:
            self.log_test("Ledger System", False, str(e))
            return False
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run complete integration test suite"""
        print("🧪 CODEX DOMINION SUITE - INTEGRATION TEST SUITE")
        print("=" * 60)
        print(f"Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Environment tests
        print("🐍 Environment Tests:")
        env_ok = self.test_python_environment()
        deps_ok = self.test_core_dependencies()
        
        # Structure tests
        print("\n📁 Structure Tests:")
        structure_ok = self.test_file_structure()
        
        # Module tests
        print("\n🧩 Module Tests:")
        core_ok = self.test_core_modules()
        app_ok = self.test_app_modules()
        
        # Functional tests
        print("\n⚡ Functional Tests:")
        memory_ok = self.test_memory_system()
        cache_ok = self.test_cache_system()
        ai_ok = self.test_ai_engine()
        ledger_ok = self.test_ledger_system()
        
        # Server tests
        print("\n🌐 Server Tests:")
        api_ok = self.test_api_server_startup()
        
        # Calculate results
        all_tests = [
            env_ok, deps_ok, structure_ok, core_ok, app_ok,
            memory_ok, cache_ok, ai_ok, ledger_ok, api_ok
        ]
        
        passed_tests = sum(all_tests)
        total_tests = len(all_tests)
        success_rate = (passed_tests / total_tests) * 100
        
        # Generate summary
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        summary = {
            "overall_result": success_rate >= 80,  # 80% pass rate required
            "success_rate": success_rate,
            "passed_tests": passed_tests,
            "total_tests": total_tests,
            "duration_seconds": duration,
            "test_results": self.test_results,
            "recommendations": self._generate_recommendations()
        }
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {passed_tests}/{total_tests} tests ({success_rate:.1f}%)")
        print(f"⏱️  Duration: {duration:.2f} seconds")
        
        if success_rate >= 80:
            print("🎉 INTEGRATION TEST SUITE: PASSED")
            print("🚀 System ready for deployment!")
        else:
            print("⚠️  INTEGRATION TEST SUITE: NEEDS ATTENTION")
            print("🔧 Please review failed tests and fix issues")
        
        # Show recommendations
        if summary["recommendations"]:
            print("\n💡 Recommendations:")
            for rec in summary["recommendations"]:
                print(f"   {rec}")
        
        return summary
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        failed_tests = [name for name, result in self.test_results.items() if not result["passed"]]
        
        if any("Dependency" in test for test in failed_tests):
            recommendations.append("📦 Install missing dependencies with: pip install -r requirements.txt")
        
        if any("Core Module" in test for test in failed_tests):
            recommendations.append("🔧 Check core module import paths and __init__.py files")
        
        if any("FastAPI Server" in test for test in failed_tests):
            recommendations.append("🌐 Ensure port 8001 is available for API testing")
        
        if any("Memory System" in test for test in failed_tests):
            recommendations.append("🧠 Check FAISS installation: pip install faiss-cpu")
        
        if any("Cache System" in test for test in failed_tests):
            recommendations.append("⚡ Install Redis for better caching: pip install redis")
        
        if not recommendations:
            recommendations.append("✨ All systems operational - ready for launch!")
        
        return recommendations

async def main():
    """Main test runner"""
    tester = IntegrationTester()
    
    try:
        results = await tester.run_all_tests()
        
        # Save results
        results_file = Path(__file__).parent / "integration_test_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Results saved to: {results_file}")
        
        # Exit with appropriate code
        sys.exit(0 if results["overall_result"] else 1)
        
    except Exception as e:
        print(f"❌ Integration test suite failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())