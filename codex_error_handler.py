"""
Enhanced Error Handling and Logging System for Codex Dominion
Provides robust error handling, logging, and monitoring capabilities
"""

import logging
import json
import traceback
from datetime import datetime
from functools import wraps
from pathlib import Path
import sys
import os

# Configure logging
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Create formatters
detailed_formatter = logging.Formatter(
    '%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s'
)

simple_formatter = logging.Formatter(
    '%(asctime)s | %(levelname)s | %(message)s'
)

# Create handlers
file_handler = logging.FileHandler(LOG_DIR / f"codex_system_{datetime.now().strftime('%Y%m%d')}.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(detailed_formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(simple_formatter)

error_handler = logging.FileHandler(LOG_DIR / f"codex_errors_{datetime.now().strftime('%Y%m%d')}.log")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(detailed_formatter)

# Create main logger
logger = logging.getLogger('codex_dominion')
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(error_handler)


class CodexErrorHandler:
    """Centralized error handling for Codex Dominion systems"""
    
    def __init__(self):
        self.error_log = LOG_DIR / f"error_summary_{datetime.now().strftime('%Y%m%d')}.json"
        self.error_counts = {}
    
    def log_error(self, module_name: str, error: Exception, context: dict = None):
        """Log error with context and tracking"""
        error_data = {
            'timestamp': datetime.now().isoformat(),
            'module': module_name,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {}
        }
        
        # Update error counts
        error_key = f"{module_name}:{type(error).__name__}"
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
        
        # Log to file
        logger.error(f"[{module_name}] {type(error).__name__}: {str(error)}")
        
        # Save detailed error log
        self._save_error_log(error_data)
        
        return error_data
    
    def _save_error_log(self, error_data: dict):
        """Save error data to JSON log"""
        try:
            errors = []
            if self.error_log.exists():
                with open(self.error_log, 'r', encoding='utf-8') as f:
                    errors = json.load(f)
            
            errors.append(error_data)
            
            # Keep only last 100 errors
            if len(errors) > 100:
                errors = errors[-100:]
            
            with open(self.error_log, 'w', encoding='utf-8') as f:
                json.dump(errors, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save error log: {e}")
    
    def get_error_summary(self) -> dict:
        """Get summary of recent errors"""
        return {
            'error_counts': self.error_counts,
            'total_errors': sum(self.error_counts.values()),
            'unique_error_types': len(self.error_counts),
            'log_file': str(self.error_log)
        }


# Global error handler instance
error_handler = CodexErrorHandler()


def safe_execute(module_name: str, default_return=None):
    """Decorator for safe function execution with error handling"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                logger.debug(f"[{module_name}] Executing {func.__name__}")
                result = func(*args, **kwargs)
                logger.debug(f"[{module_name}] {func.__name__} completed successfully")
                return result
            except Exception as e:
                context = {
                    'function': func.__name__,
                    'args_count': len(args),
                    'kwargs_keys': list(kwargs.keys())
                }
                error_handler.log_error(module_name, e, context)
                logger.warning(f"[{module_name}] {func.__name__} failed, returning default: {default_return}")
                return default_return
        return wrapper
    return decorator


def safe_file_operation(operation_type: str):
    """Decorator for safe file operations"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except FileNotFoundError as e:
                logger.error(f"File not found in {operation_type}: {e}")
                return None
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in {operation_type}: {e}")
                return None
            except PermissionError as e:
                logger.error(f"Permission denied in {operation_type}: {e}")
                return None
            except Exception as e:
                logger.error(f"Unexpected error in {operation_type}: {e}")
                return None
        return wrapper
    return decorator


def safe_api_call(platform_name: str, timeout: int = 30):
    """Decorator for safe API calls with timeout and retry logic"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            max_retries = 3
            retry_delay = 1
            
            for attempt in range(max_retries):
                try:
                    logger.debug(f"[{platform_name}] API call attempt {attempt + 1}")
                    result = func(*args, **kwargs)
                    logger.debug(f"[{platform_name}] API call successful")
                    return result
                except Exception as e:
                    context = {
                        'platform': platform_name,
                        'attempt': attempt + 1,
                        'max_retries': max_retries
                    }
                    
                    if attempt == max_retries - 1:
                        # Final attempt failed
                        error_handler.log_error(f"{platform_name}_api", e, context)
                        logger.error(f"[{platform_name}] API call failed after {max_retries} attempts")
                        return None
                    else:
                        # Retry
                        logger.warning(f"[{platform_name}] API call attempt {attempt + 1} failed, retrying...")
                        import time
                        time.sleep(retry_delay * (attempt + 1))
            
            return None
        return wrapper
    return decorator


class HealthMonitor:
    """System health monitoring and diagnostics"""
    
    def __init__(self):
        self.health_log = LOG_DIR / "system_health.json"
    
    def check_system_health(self) -> dict:
        """Comprehensive system health check"""
        health_status = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'healthy',
            'components': {},
            'warnings': [],
            'errors': []
        }
        
        # Check file system
        health_status['components']['filesystem'] = self._check_filesystem()
        
        # Check configurations
        health_status['components']['configurations'] = self._check_configurations()
        
        # Check platform modules
        health_status['components']['platform_modules'] = self._check_platform_modules()
        
        # Check archive system
        health_status['components']['archive_system'] = self._check_archive_system()
        
        # Determine overall status
        component_statuses = [comp['status'] for comp in health_status['components'].values()]
        if 'error' in component_statuses:
            health_status['overall_status'] = 'degraded'
        elif 'warning' in component_statuses:
            health_status['overall_status'] = 'warning'
        
        # Save health report
        self._save_health_report(health_status)
        
        return health_status
    
    def _check_filesystem(self) -> dict:
        """Check file system health"""
        try:
            # Check disk space
            import shutil
            total, used, free = shutil.disk_usage('.')
            free_percent = (free / total) * 100
            
            status = 'healthy'
            if free_percent < 5:
                status = 'error'
            elif free_percent < 15:
                status = 'warning'
            
            return {
                'status': status,
                'free_space_percent': round(free_percent, 2),
                'free_space_gb': round(free / (1024**3), 2),
                'total_space_gb': round(total / (1024**3), 2)
            }
        except Exception as e:
            logger.error(f"Filesystem check failed: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def _check_configurations(self) -> dict:
        """Check configuration files"""
        config_files = [
            'youtube_config.json', 'tiktok_config.json', 'threads_config.json',
            'whatsapp_config.json', 'pinterest_config.json', 'affiliate_config.json',
            'buffer_config.json'
        ]
        
        valid_configs = 0
        total_configs = len(config_files)
        
        for config_file in config_files:
            try:
                if Path(config_file).exists():
                    with open(config_file, 'r', encoding='utf-8') as f:
                        json.load(f)
                    valid_configs += 1
            except Exception:
                pass
        
        config_percent = (valid_configs / total_configs) * 100
        
        if config_percent == 100:
            status = 'healthy'
        elif config_percent >= 80:
            status = 'warning'
        else:
            status = 'error'
        
        return {
            'status': status,
            'valid_configs': valid_configs,
            'total_configs': total_configs,
            'config_health_percent': round(config_percent, 2)
        }
    
    def _check_platform_modules(self) -> dict:
        """Check platform module availability"""
        modules = [
            'codex_youtube_charts', 'codex_tiktok_earnings', 'codex_threads_engagement',
            'codex_whatsapp_business', 'codex_pinterest_capsule', 'codex_affiliate_command'
        ]
        
        working_modules = 0
        total_modules = len(modules)
        
        for module_name in modules:
            try:
                __import__(module_name)
                working_modules += 1
            except Exception:
                pass
        
        module_percent = (working_modules / total_modules) * 100
        
        if module_percent == 100:
            status = 'healthy'
        elif module_percent >= 80:
            status = 'warning'
        else:
            status = 'error'
        
        return {
            'status': status,
            'working_modules': working_modules,
            'total_modules': total_modules,
            'module_health_percent': round(module_percent, 2)
        }
    
    def _check_archive_system(self) -> dict:
        """Check archive system integrity"""
        archive_files = [
            'completed_archives.json', 'completed_archives.jsonl',
            'ledger_youtube.jsonl', 'ledger_tiktok.jsonl', 'ledger_threads.jsonl',
            'ledger_whatsapp.jsonl', 'ledger_pinterest.jsonl', 'ledger_affiliate.jsonl'
        ]
        
        healthy_archives = 0
        total_archives = len(archive_files)
        
        for archive_file in archive_files:
            try:
                if Path(archive_file).exists() and Path(archive_file).stat().st_size > 0:
                    healthy_archives += 1
            except Exception:
                pass
        
        archive_percent = (healthy_archives / total_archives) * 100
        
        if archive_percent >= 90:
            status = 'healthy'
        elif archive_percent >= 70:
            status = 'warning'
        else:
            status = 'error'
        
        return {
            'status': status,
            'healthy_archives': healthy_archives,
            'total_archives': total_archives,
            'archive_health_percent': round(archive_percent, 2)
        }
    
    def _save_health_report(self, health_status: dict):
        """Save health report to file"""
        try:
            with open(self.health_log, 'w', encoding='utf-8') as f:
                json.dump(health_status, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save health report: {e}")


# Global health monitor
health_monitor = HealthMonitor()


def get_system_status() -> dict:
    """Get comprehensive system status"""
    try:
        return {
            'health': health_monitor.check_system_health(),
            'errors': error_handler.get_error_summary(),
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }
    except Exception as e:
        logger.error(f"Failed to get system status: {e}")
        return {
            'health': {'overall_status': 'error', 'error': str(e)},
            'errors': {'error': 'Could not retrieve error summary'},
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }


# Usage examples and convenience functions
def log_info(message: str, module: str = 'system'):
    """Log info message"""
    logger.info(f"[{module}] {message}")

def log_warning(message: str, module: str = 'system'):
    """Log warning message"""
    logger.warning(f"[{module}] {message}")

def log_error(message: str, module: str = 'system'):
    """Log error message"""
    logger.error(f"[{module}] {message}")

def log_debug(message: str, module: str = 'system'):
    """Log debug message"""
    logger.debug(f"[{module}] {message}")


if __name__ == "__main__":
    # Test the error handling system
    print("🔧 Testing Enhanced Error Handling System")
    print("=" * 50)
    
    # Test logging
    log_info("Error handling system initialized", "test")
    log_warning("This is a test warning", "test")
    
    # Test error handling
    @safe_execute("test_module", default_return="fallback_value")
    def test_function():
        raise ValueError("This is a test error")
    
    result = test_function()
    print(f"Function result: {result}")
    
    # Test health check
    health = health_monitor.check_system_health()
    print(f"System health: {health['overall_status']}")
    
    # Test system status
    status = get_system_status()
    print(f"System status: {status['health']['overall_status']}")
    
    print("\n✅ Error handling system test completed")