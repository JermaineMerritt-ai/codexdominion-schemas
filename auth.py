"""
🔐 Authentication Module - Flask-Login + JWT
============================================
Provides user authentication, session management, and JWT tokens
"""

import os
from functools import wraps
from datetime import datetime, timedelta
from flask import request, jsonify, g
from flask_login import LoginManager, current_user
import jwt
from db import SessionLocal
from models_auth import User, UserRole, AuditLog
import uuid

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "CHANGE_THIS_IN_PRODUCTION")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# Flask-Login setup
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id: str):
    """Load user by ID for Flask-Login"""
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        return user
    finally:
        session.close()


def create_jwt_token(user: User) -> str:
    """
    Create JWT token for user
    
    Token includes:
    - user_id
    - email
    - role
    - exp (expiration)
    """
    payload = {
        "user_id": user.id,
        "email": user.email,
        "role": user.role.value,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_jwt_token(token: str) -> dict:
    """Decode and verify JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")


def get_token_from_request() -> str:
    """Extract JWT token from Authorization header"""
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        return None
    
    # Format: "Bearer <token>"
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    
    return parts[1]


def jwt_required(f):
    """
    Decorator to require JWT authentication
    
    Usage:
        @app.route('/protected')
        @jwt_required
        def protected_route():
            user = g.current_user
            return jsonify({"user": user.email})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_request()
        
        if not token:
            return jsonify({"error": "Missing authentication token"}), 401
        
        try:
            payload = decode_jwt_token(token)
        except ValueError as e:
            return jsonify({"error": str(e)}), 401
        
        # Load user from database
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.id == payload["user_id"]).first()
            
            if not user or not user.is_active:
                return jsonify({"error": "User not found or inactive"}), 401
            
            # Store user in Flask g object
            g.current_user = user
            g.db_session = session  # Keep session open for request
            
            return f(*args, **kwargs)
        except Exception as e:
            session.close()
            return jsonify({"error": "Authentication failed"}), 401
    
    return decorated_function


def admin_required(f):
    """
    Decorator to require admin role
    
    Usage:
        @app.route('/admin/councils')
        @jwt_required
        @admin_required
        def admin_councils():
            return jsonify({"councils": [...]})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = g.get("current_user")
        
        if not user or user.role != UserRole.ADMIN:
            return jsonify({"error": "Admin access required"}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


def council_operator_required(council_id: str = None):
    """
    Decorator to require council operator role for specific council
    
    Usage:
        @app.route('/councils/<council_id>/vote')
        @jwt_required
        @council_operator_required()
        def vote_on_council(council_id):
            # User can vote on this council
            return jsonify({"vote": "recorded"})
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = g.get("current_user")
            
            if not user:
                return jsonify({"error": "Authentication required"}), 401
            
            # Extract council_id from URL params if not provided
            cid = council_id or kwargs.get("council_id")
            
            if not cid:
                return jsonify({"error": "Council ID required"}), 400
            
            # Check permission
            if not user.can_vote_in_council(cid):
                return jsonify({
                    "error": "Not authorized to vote in this council",
                    "council_id": cid
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator


def log_audit_action(user_id: str, action: str, resource_type: str = None, 
                     resource_id: str = None, details: str = None):
    """
    Log security-sensitive action to audit trail
    
    Args:
        user_id: ID of user performing action
        action: Action performed (login, vote, edit_council, etc.)
        resource_type: Type of resource (council, agent, workflow)
        resource_id: ID of affected resource
        details: Additional context (JSON string)
    """
    session = SessionLocal()
    try:
        audit_log = AuditLog(
            id=str(uuid.uuid4()),
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=request.remote_addr if request else None
        )
        session.add(audit_log)
        session.commit()
    except Exception as e:
        print(f"⚠️  Failed to log audit action: {e}")
        session.rollback()
    finally:
        session.close()


# Authentication routes (add to flask_dashboard.py)
"""
from auth import create_jwt_token, jwt_required, admin_required, log_audit_action

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.email == email).first()
        
        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid credentials"}), 401
        
        if not user.is_active:
            return jsonify({"error": "Account disabled"}), 403
        
        # Update last login
        user.last_login = datetime.utcnow()
        session.commit()
        
        # Create JWT token
        token = create_jwt_token(user)
        
        # Log login
        log_audit_action(user.id, "login")
        
        return jsonify({
            "token": token,
            "user": user.to_dict(),
            "expires_in": JWT_EXPIRATION_HOURS * 3600
        })
    finally:
        session.close()


@app.route('/api/auth/me', methods=['GET'])
@jwt_required
def get_current_user():
    user = g.current_user
    return jsonify({"user": user.to_dict()})


@app.route('/api/councils/<council_id>/vote', methods=['POST'])
@jwt_required
@council_operator_required()
def vote_on_council(council_id):
    user = g.current_user
    data = request.get_json()
    
    # Record vote...
    log_audit_action(
        user.id,
        "vote_workflow",
        resource_type="council",
        resource_id=council_id,
        details=json.dumps({"workflow_id": data.get("workflow_id")})
    )
    
    return jsonify({"status": "vote recorded"})
"""
