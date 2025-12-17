"""
Newsletter services
"""

from flask import current_app
from typing import List, Dict, Any, Optional
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Subscriber, LedgerManager

class NewsletterService:
    """Service for newsletter operations"""

    def get_all_subscribers(self) -> List[Subscriber]:
        """Get all subscribers"""
        filepath = current_app.config['NEWSLETTER_FILE']
        data = LedgerManager.load_json(filepath)

        subscribers = []
        for s_data in data.get('subscribers', []):
            subscribers.append(Subscriber(s_data))

        return subscribers

    def get_subscribers_by_segment(self, segment: str) -> List[Subscriber]:
        """Get subscribers for specific segment"""
        all_subscribers = self.get_all_subscribers()
        return [
            s for s in all_subscribers
            if s.status == 'active' and segment in s.segments
        ]

    def subscribe(self, email: str, risk_profile: str, segments: List[str]) -> Optional[Subscriber]:
        """Subscribe email to newsletter"""
        filepath = current_app.config['NEWSLETTER_FILE']
        data = LedgerManager.load_json(filepath)

        if 'subscribers' not in data:
            data['subscribers'] = []

        # Check if already exists
        for sub in data['subscribers']:
            if sub['email'] == email:
                return None

        # Create subscriber
        subscriber_id = max([s['id'] for s in data['subscribers']], default=0) + 1
        now = datetime.utcnow().isoformat() + 'Z'

        subscriber = {
            'id': subscriber_id,
            'email': email,
            'risk_profile': risk_profile,
            'segments': segments,
            'preferences': {
                'frequency': 'daily',
                'format': 'html'
            },
            'status': 'active',
            'subscribed_at': now,
            'unsubscribed_at': None
        }

        data['subscribers'].append(subscriber)
        LedgerManager.save_json(filepath, data)

        return Subscriber(subscriber)

    def unsubscribe(self, email: str) -> bool:
        """Unsubscribe email"""
        filepath = current_app.config['NEWSLETTER_FILE']
        data = LedgerManager.load_json(filepath)

        for sub in data.get('subscribers', []):
            if sub['email'] == email:
                sub['status'] = 'unsubscribed'
                sub['unsubscribed_at'] = datetime.utcnow().isoformat() + 'Z'

                LedgerManager.save_json(filepath, data)
                return True

        return False

    def get_subscriber_stats(self) -> Dict[str, Any]:
        """Get subscriber statistics"""
        filepath = current_app.config['NEWSLETTER_FILE']
        data = LedgerManager.load_json(filepath)

        subscribers = data.get('subscribers', [])
        active = [s for s in subscribers if s['status'] == 'active']

        # Count by segment
        segments = data.get('segments', {})
        segment_counts = {}
        for segment_name in segments.keys():
            count = len([s for s in active if segment_name in s.get('segments', [])])
            segment_counts[segment_name] = count

        return {
            'total_subscribers': len(subscribers),
            'active_subscribers': len(active),
            'segment_counts': segment_counts
        }
