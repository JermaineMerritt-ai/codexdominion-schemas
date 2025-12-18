"""
Newsletter Routes
"""
from flask import render_template, jsonify, request, redirect, url_for, flash
from . import newsletter_bp
from extensions import db
from models import Subscriber
import ai_prompts

@newsletter_bp.route('/')
def index():
    """Newsletter homepage - redirect to subscribe"""
    return redirect(url_for('newsletter.subscribe'))

@newsletter_bp.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    """Newsletter subscription"""
    if request.method == 'POST':
        email = request.form.get('email')
        risk_profile = request.form.get('risk_profile', 'moderate')
        segments = request.form.getlist('segments')  # Get list of checked segments

        # Check if already subscribed
        existing = Subscriber.query.filter_by(email=email).first()

        if existing:
            # Update existing subscriber
            existing.risk_preference = risk_profile
            existing.daily_email = 'daily_picks' in segments
            existing.weekly_email = 'weekly_portfolio' in segments
            existing.monthly_email = 'monthly_deep_dive' in segments
            db.session.commit()
            flash('Subscription preferences updated!', 'success')
        else:
            # Create new subscriber
            subscriber = Subscriber(
                email=email,
                risk_preference=risk_profile,
                daily_email='daily_picks' in segments,
                weekly_email='weekly_portfolio' in segments,
                monthly_email='monthly_deep_dive' in segments
            )
            db.session.add(subscriber)
            db.session.commit()
            flash('Successfully subscribed! Check your inbox.', 'success')

        return redirect(url_for('newsletter.subscribe'))

    return render_template('newsletter/subscribe.html')

@newsletter_bp.route('/unsubscribe/<email>')
def unsubscribe(email):
    """Unsubscribe from newsletter"""
    subscriber = Subscriber.query.filter_by(email=email).first()

    if subscriber:
        db.session.delete(subscriber)
        db.session.commit()
        flash('Successfully unsubscribed.', 'info')

    return render_template('newsletter/unsubscribed.html')

@newsletter_bp.route('/preview/<type>')
def preview(type):
    """Preview newsletter templates"""
    valid_types = ['daily', 'weekly', 'monthly']

    if type not in valid_types:
        return jsonify({'error': 'Invalid newsletter type'}), 400

    # Load appropriate prompt
    prompt_map = {
        'daily': 'daily_email',
        'weekly': 'weekly_email',
        'monthly': 'monthly_email'
    }

    prompt = ai_prompts.load_prompt(prompt_map[type])

    return render_template('newsletter/preview.html',
                          newsletter_type=type,
                          prompt_template=prompt)

@newsletter_bp.route('/generate/<type>')
def generate(type):
    """Generate newsletter content (for admin)"""
    # TODO: Implement actual newsletter generation with AI
    return jsonify({
        'status': 'ready',
        'type': type,
        'message': 'Newsletter generation not yet implemented'
    })
