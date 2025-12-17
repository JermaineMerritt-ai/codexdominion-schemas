"""
Codex Dominion - Flask Application
Main application factory and routes
"""

from flask import Flask, render_template, jsonify
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config
from extensions import init_extensions
from database import db, init_db

def create_app(config_name='default'):
    """Application factory"""

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize database
    db.init_app(app)

    # Initialize extensions
    init_extensions(app)

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    # Register blueprints
    from auth.routes import auth_bp
    from portfolio.routes import portfolio_bp
    from stocks.routes import stocks_bp
    from newsletter.routes import newsletter_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(portfolio_bp, url_prefix='/portfolio')
    app.register_blueprint(stocks_bp, url_prefix='/stocks')
    app.register_blueprint(newsletter_bp, url_prefix='/newsletter')

    # Main routes
    @app.route('/')
    def home():
        """Home page"""
        return render_template('home.html')

    @app.route('/health')
    def health():
        """Health check"""
        return jsonify({
            "status": "healthy",
            "service": "codex-dominion-flask",
            "version": "1.0.0"
        })

    @app.errorhandler(404)
    def not_found(error):
        """404 error handler"""
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        """500 error handler"""
        return jsonify({"error": "Internal server error"}), 500

    return app

# Create app instance for Gunicorn
app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == '__main__':
    app_instance = create_app('development')
    print("🔥 Codex Dominion Flask App Starting 👑")
    print("📊 Portfolio Management System")
    print("🌐 Running on http://localhost:5001")
    app_instance.run(host='0.0.0.0', port=5001, debug=True)
