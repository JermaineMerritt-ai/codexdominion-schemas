"""
Newsletter routes
"""

from flask import render_template, request, jsonify, flash, redirect, url_for
import sys
import os

# Import blueprint and service
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from newsletter import newsletter_bp
from newsletter.services import NewsletterService

newsletter_service = NewsletterService()

@newsletter_bp.route('/')
def index():
    """Newsletter home"""
    stats = newsletter_service.get_subscriber_stats()
    return render_template('newsletter/index.html', stats=stats)

@newsletter_bp.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    """Subscribe to newsletter"""
    if request.method == 'POST':
        email = request.form.get('email')
        risk_profile = request.form.get('risk_profile', 'moderate')
        segments = request.form.getlist('segments')

        subscriber = newsletter_service.subscribe(email, risk_profile, segments)

        if subscriber:
            flash('Subscription successful! 🔥', 'success')
            return redirect(url_for('newsletter.index'))
        else:
            flash('Email already subscribed', 'warning')

    return render_template('newsletter/subscribe.html')

@newsletter_bp.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    """Unsubscribe from newsletter"""
    email = request.form.get('email')

    success = newsletter_service.unsubscribe(email)

    if success:
        flash('Unsubscribed successfully', 'info')
    else:
        flash('Email not found', 'error')

    return redirect(url_for('newsletter.index'))

# API Routes
@newsletter_bp.route('/api/subscribers')
def api_get_subscribers():
    """Get all subscribers (API)"""
    subscribers = newsletter_service.get_all_subscribers()
    return jsonify([s.to_dict() for s in subscribers])

@newsletter_bp.route('/api/subscribers/<segment>')
def api_get_segment_subscribers(segment):
    """Get subscribers by segment (API)"""
    subscribers = newsletter_service.get_subscribers_by_segment(segment)
    return jsonify({
        "segment": segment,
        "count": len(subscribers),
        "subscribers": [s.to_dict() for s in subscribers]
    })

@newsletter_bp.route('/api/stats')
def api_get_stats():
    """Get subscriber statistics (API)"""
    stats = newsletter_service.get_subscriber_stats()
    return jsonify(stats)
