"""
Codex Dominion - Investment Platform
Main Flask Application
"""
from flask import Flask, render_template, jsonify
from config import Config
from extensions import db, migrate, login_manager
from models import User, Portfolio, Stock, Alert
import ai_prompts
import os
import atexit

# Load environment variables from .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not required, just helpful

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Make current_user available to templates even when not logged in
    from flask_login import current_user

    @app.context_processor
    def inject_user():
        return {'current_user': current_user}

    # Register blueprints
    from portfolio import portfolio_bp
    from stocks import stocks_bp
    from newsletter import newsletter_bp
    from auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(portfolio_bp, url_prefix='/portfolio')
    app.register_blueprint(stocks_bp, url_prefix='/stocks')
    app.register_blueprint(newsletter_bp, url_prefix='/newsletter')

    # Initialize background scheduler
    try:
        from tasks import init_scheduler, shutdown_scheduler
        with app.app_context():
            init_scheduler(app)
        atexit.register(shutdown_scheduler)
    except ImportError:
        app.logger.warning("Tasks module not available - scheduled jobs disabled")
    except Exception as e:
        app.logger.error(f"Failed to initialize scheduler: {e}")

    # Home route
    @app.route('/')
    def index():
        return render_template('index.html')

    # Health check
    @app.route('/health')
    def health():
        try:
            from ai_services import get_ai_status
            ai_status = get_ai_status()
        except ImportError:
            ai_status = {"configured": False, "error": "ai_services module not found"}

        return jsonify({
            'status': 'operational',
            'database': 'connected',
            'ai_prompts': len(ai_prompts.get_all_prompts()),
            'ai_service': ai_status
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
