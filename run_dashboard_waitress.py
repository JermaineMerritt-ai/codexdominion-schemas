"""
🚀 FLASK DASHBOARD - WAITRESS LAUNCHER
Production-ready WSGI server (no crashes!)
"""
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Import Flask app
from flask_dashboard import app

if __name__ == '__main__':
    try:
        from waitress import serve
        
        logger.info("="*80)
        logger.info("👑 CODEX DOMINION - WAITRESS MODE")
        logger.info("="*80)
        logger.info("🚀 Starting WSGI server...")
        logger.info("🌐 URL: http://localhost:5000")
        logger.info("✅ Using Waitress (production-ready)")
        logger.info("")
        logger.info("Press Ctrl+C to stop")
        logger.info("="*80)
        
        # Serve with Waitress (production-ready)
        serve(app, host='0.0.0.0', port=5000, threads=4)
        
    except KeyboardInterrupt:
        logger.info("\n👋 Dashboard stopped by user")
    except Exception as e:
        logger.error(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
