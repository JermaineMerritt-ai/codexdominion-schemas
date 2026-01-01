"""
🔥 CODEX DOMINION - AUTHENTICATION API 🔥
==========================================
User registration, login, and session management for CodexDominion platform

Features:
- User registration with validation
- Email/password login
- JWT token authentication
- Password reset flow
- Role-based access control
"""

from flask import Blueprint, request, jsonify, session
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
import jwt
import os
import re
from typing import Dict, Any, Optional

from db import SessionLocal
from models import User, UserRole
import uuid

# Create Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# JWT Configuration
JWT_SECRET = os.environ.get('JWT_SECRET', 'codex-dominion-secret-key-2025')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24


# ============================================================================
# VALIDATION HELPERS
# ============================================================================

def validate_email(email: str) -> tuple[bool, Optional[str]]:
    """Validate email format"""
    if not email:
        return False, "Email is required"
    
    # Basic email regex
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return False, "Please enter a valid email address"
    
    return True, None


def validate_password(password: str) -> tuple[bool, Optional[str]]:
    """Validate password strength"""
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    # Check for at least one letter and one number
    has_letter = any(c.isalpha() for c in password)
    has_number = any(c.isdigit() for c in password)
    
    if not (has_letter and has_number):
        return False, "Password must contain both letters and numbers"
    
    return True, None


def validate_name(name: str) -> tuple[bool, Optional[str]]:
    """Validate user name"""
    if not name:
        return False, "Name is required"
    
    if len(name) < 2:
        return False, "Name must be at least 2 characters"
    
    if len(name) > 100:
        return False, "Name is too long (max 100 characters)"
    
    return True, None


# ============================================================================
# JWT TOKEN HELPERS
# ============================================================================

def generate_token(user_id: str, email: str, role: str) -> str:
    """Generate JWT access token"""
    payload = {
        'user_id': user_id,
        'email': email,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


# ============================================================================
# REGISTRATION ENDPOINT
# ============================================================================

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    
    Request Body:
    {
        "name": "Marcus Thompson",
        "email": "marcus@example.com",
        "password": "SecurePass123"
    }
    
    Response:
    {
        "success": true,
        "message": "Account created successfully! 🎉",
        "user": {
            "id": "user_abc123",
            "name": "Marcus Thompson",
            "email": "marcus@example.com",
            "role": "viewer"
        },
        "token": "eyJhbGc..."
    }
    """
    try:
        # Parse request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Extract fields
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        country = data.get('country', '').strip()  # Optional field
        
        # Validate name
        valid_name, name_error = validate_name(name)
        if not valid_name:
            return jsonify({
                'success': False,
                'error': name_error,
                'field': 'name'
            }), 400
        
        # Validate email
        valid_email, email_error = validate_email(email)
        if not valid_email:
            return jsonify({
                'success': False,
                'error': email_error,
                'field': 'email'
            }), 400
        
        # Validate password
        valid_password, password_error = validate_password(password)
        if not valid_password:
            return jsonify({
                'success': False,
                'error': password_error,
                'field': 'password'
            }), 400
        
        # Create database session
        db: Session = SessionLocal()
        
        try:
            # Check if email already exists
            existing_user = db.query(User).filter_by(email=email).first()
            if existing_user:
                return jsonify({
                    'success': False,
                    'error': 'This email is already in use. Try signing in?',
                    'field': 'email'
                }), 409
            
            # Create new user
            user_id = f"user_{uuid.uuid4().hex[:12]}"
            new_user = User(
                id=user_id,
                email=email,
                full_name=name,
                role=UserRole.VIEWER,  # Default role for new users
                is_active=True,
                created_at=datetime.utcnow()
            )
            
            # Set password (hashes automatically)
            new_user.set_password(password)
            
            # Add to database
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            # Generate JWT token
            token = generate_token(
                user_id=new_user.id,
                email=new_user.email,
                role=new_user.role.value
            )
            
            # Return success response
            return jsonify({
                'success': True,
                'message': 'Account created successfully! 🎉',
                'user': {
                    'id': new_user.id,
                    'name': new_user.full_name,
                    'email': new_user.email,
                    'role': new_user.role.value,
                    'created_at': new_user.created_at.isoformat() + 'Z'
                },
                'token': token
            }), 201
            
        except IntegrityError:
            db.rollback()
            return jsonify({
                'success': False,
                'error': 'This email is already in use. Try signing in?',
                'field': 'email'
            }), 409
        
        except Exception as e:
            db.rollback()
            print(f"❌ Registration error: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Registration failed. Please try again.'
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        print(f"❌ Unexpected error in registration: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred'
        }), 500


# ============================================================================
# LOGIN ENDPOINT
# ============================================================================

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT token
    
    Request Body:
    {
        "email": "marcus@example.com",
        "password": "SecurePass123"
    }
    
    Response:
    {
        "success": true,
        "message": "Welcome back! 👑",
        "user": {
            "id": "user_abc123",
            "name": "Marcus Thompson",
            "email": "marcus@example.com",
            "role": "viewer"
        },
        "token": "eyJhbGc..."
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Email and password are required'
            }), 400
        
        # Create database session
        db: Session = SessionLocal()
        
        try:
            # Find user by email
            user = db.query(User).filter_by(email=email).first()
            
            if not user:
                return jsonify({
                    'success': False,
                    'error': 'Invalid email or password'
                }), 401
            
            # Check if user is active
            if not user.is_active:
                return jsonify({
                    'success': False,
                    'error': 'Account is inactive. Contact support.'
                }), 403
            
            # Verify password
            if not user.check_password(password):
                return jsonify({
                    'success': False,
                    'error': 'Invalid email or password'
                }), 401
            
            # Update last login
            user.last_login = datetime.utcnow()
            db.commit()
            
            # Generate JWT token
            token = generate_token(
                user_id=user.id,
                email=user.email,
                role=user.role.value
            )
            
            return jsonify({
                'success': True,
                'message': 'Welcome back! 👑',
                'user': {
                    'id': user.id,
                    'name': user.full_name,
                    'email': user.email,
                    'role': user.role.value,
                    'last_login': user.last_login.isoformat() + 'Z'
                },
                'token': token
            }), 200
        
        finally:
            db.close()
    
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Login failed. Please try again.'
        }), 500


# ============================================================================
# VERIFY TOKEN ENDPOINT
# ============================================================================

@auth_bp.route('/verify', methods=['GET'])
def verify():
    """
    Verify JWT token and return user info
    
    Headers:
    Authorization: Bearer <token>
    
    Response:
    {
        "success": true,
        "user": {
            "id": "user_abc123",
            "email": "marcus@example.com",
            "role": "viewer"
        }
    }
    """
    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'No token provided'
            }), 401
        
        token = auth_header.split(' ')[1]
        
        # Verify token
        payload = verify_token(token)
        
        if not payload:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired token'
            }), 401
        
        return jsonify({
            'success': True,
            'user': {
                'id': payload['user_id'],
                'email': payload['email'],
                'role': payload['role']
            }
        }), 200
    
    except Exception as e:
        print(f"❌ Token verification error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Token verification failed'
        }), 500


# ============================================================================
# LOGOUT ENDPOINT
# ============================================================================

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Logout user (client should discard token)
    
    Response:
    {
        "success": true,
        "message": "Logged out successfully"
    }
    """
    # Since we're using JWT, logout is handled client-side by discarding token
    # This endpoint exists for consistency and future server-side logout logic
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    }), 200


# ============================================================================
# PASSWORD RESET REQUEST ENDPOINT
# ============================================================================

@auth_bp.route('/reset-password-request', methods=['POST'])
def reset_password_request():
    """
    Request password reset email
    
    Request Body:
    {
        "email": "marcus@example.com"
    }
    
    Response:
    {
        "success": true,
        "message": "If that email exists, we've sent reset instructions."
    }
    """
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({
                'success': False,
                'error': 'Email is required'
            }), 400
        
        # Always return success (don't reveal if email exists)
        # TODO: Send password reset email
        return jsonify({
            'success': True,
            'message': "If that email exists, we've sent reset instructions."
        }), 200
    
    except Exception as e:
        print(f"❌ Password reset request error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Request failed. Please try again.'
        }), 500


# ============================================================================
# GET USER PROFILE ENDPOINT
# ============================================================================

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """
    Get current user profile
    
    Headers:
    Authorization: Bearer <token>
    
    Response:
    {
        "success": true,
        "user": {
            "id": "user_abc123",
            "name": "Marcus Thompson",
            "email": "marcus@example.com",
            "role": "viewer",
            "created_at": "2025-12-23T...",
            "last_login": "2025-12-23T..."
        }
    }
    """
    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'No token provided'
            }), 401
        
        token = auth_header.split(' ')[1]
        payload = verify_token(token)
        
        if not payload:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired token'
            }), 401
        
        db: Session = SessionLocal()
        
        try:
            user = db.query(User).filter_by(id=payload['user_id']).first()
            
            if not user:
                return jsonify({
                    'success': False,
                    'error': 'User not found'
                }), 404
            
            return jsonify({
                'success': True,
                'user': {
                    'id': user.id,
                    'name': user.full_name,
                    'email': user.email,
                    'role': user.role.value,
                    'created_at': user.created_at.isoformat() + 'Z',
                    'last_login': user.last_login.isoformat() + 'Z' if user.last_login else None
                }
            }), 200
        
        finally:
            db.close()
    
    except Exception as e:
        print(f"❌ Get profile error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get profile'
        }), 500


# ============================================================================
# ONBOARDING ENDPOINT
# ============================================================================

@auth_bp.route('/onboarding', methods=['POST'])
def onboarding():
    """
    Complete user onboarding by selecting role type
    
    Request Body:
    {
        "userId": "user_abc123",
        "role": "creator",  // "creator", "youth", or "both"
        "token": "jwt-token-here"
    }
    
    Response:
    {
        "success": true,
        "message": "Onboarding complete! Welcome to CodexDominion 🔥",
        "user": {
            "id": "user_abc123",
            "name": "Marcus Thompson",
            "email": "marcus@example.com",
            "role": "viewer",
            "user_type": "creator",
            "onboarding_completed": true
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        user_id = data.get('userId')
        user_type = data.get('role')  # 'creator', 'youth', or 'both'
        token = data.get('token')
        
        # Validate required fields
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'User ID is required',
                'field': 'userId'
            }), 400
        
        if not user_type:
            return jsonify({
                'success': False,
                'error': 'Role selection is required',
                'field': 'role'
            }), 400
        
        if not token:
            return jsonify({
                'success': False,
                'error': 'Authentication token is required',
                'field': 'token'
            }), 400
        
        # Validate user_type value
        if user_type not in ['creator', 'youth', 'both']:
            return jsonify({
                'success': False,
                'error': 'Role must be "creator", "youth", or "both"',
                'field': 'role'
            }), 400
        
        # Verify token
        payload = verify_token(token)
        
        if not payload:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired token'
            }), 401
        
        # Verify user_id matches token
        if payload['user_id'] != user_id:
            return jsonify({
                'success': False,
                'error': 'User ID does not match token'
            }), 403
        
        # Update user in database
        db: Session = SessionLocal()
        
        try:
            user = db.query(User).filter_by(id=user_id).first()
            
            if not user:
                return jsonify({
                    'success': False,
                    'error': 'User not found'
                }), 404
            
            # Update user type and onboarding status
            user.user_type = user_type
            user.onboarding_completed = True
            
            db.commit()
            db.refresh(user)
            
            # Determine welcome message based on user type
            if user_type == 'creator':
                message = "Welcome, Creator! 🎨 Start uploading your products and earning."
            elif user_type == 'youth':
                message = "Welcome, Youth! 🔥 Start exploring challenges and rising up the leaderboard."
            else:  # both
                message = "Welcome! 👑 You're ready to create AND compete. Let's go!"
            
            return jsonify({
                'success': True,
                'message': message,
                'user': {
                    'id': user.id,
                    'name': user.full_name,
                    'email': user.email,
                    'role': user.role.value,
                    'user_type': user.user_type,
                    'onboarding_completed': user.onboarding_completed,
                    'created_at': user.created_at.isoformat() + 'Z'
                },
                'next_steps': get_next_steps(user_type)
            }), 200
        
        except Exception as e:
            db.rollback()
            print(f"❌ Onboarding error: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Onboarding failed. Please try again.'
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        print(f"❌ Unexpected error in onboarding: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred'
        }), 500


def get_next_steps(user_type: str) -> list:
    """
    Get recommended next steps based on user type
    """
    if user_type == 'creator':
        return [
            {
                'title': 'Upload Your First Product',
                'description': 'Share your digital creations with the community',
                'url': '/upload',
                'icon': '📦'
            },
            {
                'title': 'Set Up Your Profile',
                'description': 'Tell the community about yourself',
                'url': '/profile/edit',
                'icon': '👤'
            },
            {
                'title': 'Explore Marketplace',
                'description': 'See what other creators are sharing',
                'url': '/marketplace',
                'icon': '🛍️'
            }
        ]
    elif user_type == 'youth':
        return [
            {
                'title': 'View Challenges',
                'description': 'Complete challenges to earn badges and climb the leaderboard',
                'url': '/challenges',
                'icon': '🏆'
            },
            {
                'title': 'Check Leaderboard',
                'description': 'See where you rank among the community',
                'url': '/leaderboard',
                'icon': '👑'
            },
            {
                'title': 'Explore Products',
                'description': 'Discover digital products from Caribbean creators',
                'url': '/marketplace',
                'icon': '🛍️'
            }
        ]
    else:  # both
        return [
            {
                'title': 'Upload Your First Product',
                'description': 'Share your digital creations',
                'url': '/upload',
                'icon': '📦'
            },
            {
                'title': 'Complete Challenges',
                'description': 'Earn badges and climb the leaderboard',
                'url': '/challenges',
                'icon': '🏆'
            },
            {
                'title': 'Explore Community',
                'description': 'Connect with creators and youth',
                'url': '/community',
                'icon': '🌎'
            }
        ]


# ============================================================================
# EXPORT BLUEPRINT
# ============================================================================

def register_auth_routes(app):
    """Register authentication routes with Flask app"""
    app.register_blueprint(auth_bp)
    print("✅ Authentication routes registered at /api/auth")
