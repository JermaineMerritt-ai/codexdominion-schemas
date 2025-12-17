"""
Authentication routes
"""

from flask import render_template, request, session, redirect, url_for, jsonify, flash
from datetime import datetime, timedelta
import sys
import os
import secrets

# Import blueprint
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import auth_bp
from database import db, User, Session as UserSession

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('auth/login.html')

        # Query user from database
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # Create session
            session['user_id'] = user.id
            session['username'] = user.email
            session['role'] = user.role
            session['logged_in'] = True
            session['login_time'] = datetime.utcnow().isoformat()

            # Create session token in database
            session_token = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(hours=24)

            user_session = UserSession(
                user_id=user.id,
                session_token=session_token,
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string,
                expires_at=expires_at
            )
            db.session.add(user_session)
            db.session.commit()

            session['session_token'] = session_token

            flash(f'Welcome back, {user.email}! 🔥', 'success')
            return redirect(url_for('portfolio.dashboard'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """Logout"""
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('home'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        risk_profile = request.form.get('risk_profile', 'moderate')

        # Validation
        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('auth/register.html')

        if password != password_confirm:
            flash('Passwords do not match', 'error')
            return render_template('auth/register.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters', 'error')
            return render_template('auth/register.html')

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'error')
            return render_template('auth/register.html')

        # Create new user
        user = User(
            email=email,
            role='user',
            risk_profile_default=risk_profile
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login. 👑', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/api/session')
def get_session():
    """Get current session info"""
    if session.get('logged_in'):
        return jsonify({
            "logged_in": True,
            "user_id": session.get('user_id'),
            "username": session.get('username'),
            "login_time": session.get('login_time')
        })
    else:
        return jsonify({"logged_in": False}), 401
