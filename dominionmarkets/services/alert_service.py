"""
Alert Monitoring Service
=========================
Service for checking alert conditions and triggering notifications
"""

from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from decimal import Decimal
import logging

from models.alerts import (
    Alert, AlertTrigger, AlertType, AlertStatus, ConditionType, 
    get_active_alerts_by_type
)
from db import SessionLocal

logger = logging.getLogger(__name__)


class AlertService:
    """Service for monitoring and triggering alerts"""
    
    def __init__(self):
        self.session = SessionLocal()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
    
    # ==================== Price Alerts ====================
    
    def check_price_alert(self, alert: Alert, current_price: Decimal) -> bool:
        """
        Check if price alert condition is met
        
        Returns: True if condition met, False otherwise
        """
        if alert.condition_type == ConditionType.ABOVE:
            return current_price >= alert.target_value
        
        elif alert.condition_type == ConditionType.BELOW:
            return current_price <= alert.target_value
        
        elif alert.condition_type == ConditionType.PERCENT_UP:
            # Need opening price to calculate percent change
            # This would come from stock data service
            return False  # Placeholder
        
        elif alert.condition_type == ConditionType.PERCENT_DOWN:
            return False  # Placeholder
        
        return False
    
    def check_all_price_alerts(self, stock_data: Dict[str, Decimal]):
        """
        Check all active price alerts against current stock prices
        
        Args:
            stock_data: Dict of {symbol: current_price}
        """
        for symbol, current_price in stock_data.items():
            alerts = self.session.query(Alert).filter(
                Alert.alert_type == AlertType.PRICE,
                Alert.status == AlertStatus.ACTIVE,
                Alert.symbol == symbol.upper()
            ).all()
            
            for alert in alerts:
                if self.check_price_alert(alert, current_price):
                    self.trigger_alert(alert, float(current_price))
    
    # ==================== News Alerts ====================
    
    def check_news_alert(self, alert: Alert, articles: List[Dict]) -> Tuple[bool, Optional[Dict]]:
        """
        Check if news alert condition is met
        
        Args:
            alert: Alert object
            articles: List of verified news articles
        
        Returns: (condition_met: bool, trigger_data: dict)
        """
        if not articles:
            return False, None
        
        # Filter by verification score
        verified_articles = [
            a for a in articles 
            if a.get('verification_score', 0) >= alert.min_verification_score
        ]
        
        if len(verified_articles) >= alert.article_threshold:
            trigger_data = {
                'article_count': len(verified_articles),
                'avg_verification_score': sum(a.get('verification_score', 0) for a in verified_articles) / len(verified_articles),
                'articles': [
                    {
                        'id': a.get('id'),
                        'title': a.get('title'),
                        'verification_score': a.get('verification_score')
                    }
                    for a in verified_articles[:5]  # First 5 articles
                ]
            }
            return True, trigger_data
        
        return False, None
    
    # ==================== Earnings Alerts ====================
    
    def check_earnings_alert(self, alert: Alert, earnings_data: Dict) -> Tuple[bool, Optional[Dict]]:
        """
        Check if earnings alert condition is met
        
        Args:
            alert: Alert object
            earnings_data: Dict with earnings date and status
        
        Returns: (condition_met: bool, trigger_data: dict)
        """
        if not earnings_data:
            return False, None
        
        earnings_date = earnings_data.get('earnings_date')
        if not earnings_date:
            return False, None
        
        days_until = (earnings_date - datetime.now().date()).days
        
        trigger_data = None
        condition_met = False
        
        if alert.condition_type == ConditionType.EARNINGS_UPCOMING_7D:
            if days_until == 7:
                condition_met = True
                trigger_data = {
                    'days_until': 7,
                    'earnings_date': earnings_date.isoformat(),
                    'time_of_day': earnings_data.get('time_of_day', 'after close')
                }
        
        elif alert.condition_type == ConditionType.EARNINGS_UPCOMING_1D:
            if days_until == 1:
                condition_met = True
                trigger_data = {
                    'days_until': 1,
                    'earnings_date': earnings_date.isoformat(),
                    'time_of_day': earnings_data.get('time_of_day', 'after close')
                }
        
        elif alert.condition_type == ConditionType.EARNINGS_RELEASED:
            if earnings_data.get('status') == 'released':
                condition_met = True
                trigger_data = {
                    'revenue': earnings_data.get('revenue'),
                    'revenue_expected': earnings_data.get('revenue_expected'),
                    'eps': earnings_data.get('eps'),
                    'eps_expected': earnings_data.get('eps_expected'),
                    'release_time': earnings_data.get('release_time')
                }
        
        return condition_met, trigger_data
    
    # ==================== Dividend Alerts ====================
    
    def check_dividend_alert(self, alert: Alert, dividend_data: Dict) -> Tuple[bool, Optional[Dict]]:
        """
        Check if dividend alert condition is met
        
        Args:
            alert: Alert object
            dividend_data: Dict with dividend event information
        
        Returns: (condition_met: bool, trigger_data: dict)
        """
        if not dividend_data:
            return False, None
        
        trigger_data = None
        condition_met = False
        
        if alert.condition_type == ConditionType.EX_DATE_APPROACHING:
            ex_date = dividend_data.get('ex_date')
            if ex_date:
                days_until = (ex_date - datetime.now().date()).days
                if days_until == 3:
                    condition_met = True
                    trigger_data = {
                        'ex_date': ex_date.isoformat(),
                        'days_until': 3,
                        'dividend_amount': dividend_data.get('amount'),
                        'frequency': dividend_data.get('frequency', 'quarterly')
                    }
        
        elif alert.condition_type == ConditionType.PAYMENT_DATE_APPROACHING:
            payment_date = dividend_data.get('payment_date')
            if payment_date:
                days_until = (payment_date - datetime.now().date()).days
                if days_until == 1:
                    condition_met = True
                    trigger_data = {
                        'payment_date': payment_date.isoformat(),
                        'days_until': 1,
                        'dividend_amount': dividend_data.get('amount')
                    }
        
        elif alert.condition_type == ConditionType.DIVIDEND_ANNOUNCED:
            if dividend_data.get('status') == 'announced':
                condition_met = True
                trigger_data = {
                    'dividend_amount': dividend_data.get('amount'),
                    'ex_date': dividend_data.get('ex_date'),
                    'payment_date': dividend_data.get('payment_date'),
                    'announcement_date': dividend_data.get('announcement_date')
                }
        
        elif alert.condition_type == ConditionType.DIVIDEND_CHANGED:
            previous_amount = dividend_data.get('previous_amount')
            current_amount = dividend_data.get('amount')
            if previous_amount and current_amount and previous_amount != current_amount:
                change_percent = ((current_amount - previous_amount) / previous_amount) * 100
                condition_met = True
                trigger_data = {
                    'previous_amount': float(previous_amount),
                    'current_amount': float(current_amount),
                    'change_percent': round(change_percent, 2),
                    'change_type': 'increase' if current_amount > previous_amount else 'decrease'
                }
        
        return condition_met, trigger_data
    
    # ==================== Portfolio Alerts ====================
    
    def check_portfolio_alert(self, alert: Alert, portfolio_data: Dict) -> Tuple[bool, Optional[Dict]]:
        """
        Check if portfolio alert condition is met
        
        Args:
            alert: Alert object
            portfolio_data: Dict with portfolio metrics
        
        Returns: (condition_met: bool, trigger_data: dict)
        """
        if not portfolio_data:
            return False, None
        
        trigger_data = None
        condition_met = False
        
        if alert.condition_type == ConditionType.PORTFOLIO_GAIN:
            total_gain_percent = portfolio_data.get('total_gain_percent', 0)
            if total_gain_percent >= float(alert.target_value):
                condition_met = True
                trigger_data = {
                    'portfolio_id': str(alert.portfolio_id),
                    'portfolio_name': portfolio_data.get('name'),
                    'total_value': portfolio_data.get('total_value'),
                    'gain_percent': round(total_gain_percent, 2),
                    'gain_amount': portfolio_data.get('total_gain_amount'),
                    'threshold': float(alert.target_value)
                }
        
        elif alert.condition_type == ConditionType.PORTFOLIO_LOSS:
            total_gain_percent = portfolio_data.get('total_gain_percent', 0)
            if total_gain_percent <= -float(alert.target_value):
                condition_met = True
                trigger_data = {
                    'portfolio_id': str(alert.portfolio_id),
                    'portfolio_name': portfolio_data.get('name'),
                    'total_value': portfolio_data.get('total_value'),
                    'loss_percent': round(abs(total_gain_percent), 2),
                    'loss_amount': abs(portfolio_data.get('total_gain_amount', 0)),
                    'threshold': float(alert.target_value)
                }
        
        elif alert.condition_type == ConditionType.SECTOR_ALLOCATION:
            sector_allocations = portfolio_data.get('sector_allocations', {})
            for sector, percent in sector_allocations.items():
                if percent >= float(alert.target_value):
                    condition_met = True
                    trigger_data = {
                        'portfolio_id': str(alert.portfolio_id),
                        'sector': sector,
                        'allocation_percent': round(percent, 2),
                        'threshold': float(alert.target_value)
                    }
                    break
        
        elif alert.condition_type == ConditionType.DIVERSIFICATION_LOW:
            diversification_score = portfolio_data.get('diversification_score', 100)
            if diversification_score < float(alert.target_value):
                condition_met = True
                trigger_data = {
                    'portfolio_id': str(alert.portfolio_id),
                    'diversification_score': diversification_score,
                    'threshold': float(alert.target_value),
                    'recommendation': 'Consider adding holdings from different sectors'
                }
        
        return condition_met, trigger_data
    
    # ==================== Volume Alerts ====================
    
    def check_volume_alert(self, alert: Alert, volume_data: Dict) -> Tuple[bool, Optional[Dict]]:
        """
        Check if volume alert condition is met (Premium feature)
        
        Args:
            alert: Alert object
            volume_data: Dict with current and average volume
        
        Returns: (condition_met: bool, trigger_data: dict)
        """
        if not volume_data:
            return False, None
        
        current_volume = volume_data.get('current_volume', 0)
        average_volume = volume_data.get('average_volume', 0)
        
        if average_volume == 0:
            return False, None
        
        volume_ratio = current_volume / average_volume
        
        trigger_data = None
        condition_met = False
        
        if alert.condition_type == ConditionType.VOLUME_2X:
            if volume_ratio >= 2.0:
                condition_met = True
                trigger_data = {
                    'current_volume': current_volume,
                    'average_volume': average_volume,
                    'volume_ratio': round(volume_ratio, 2),
                    'threshold': '2x'
                }
        
        elif alert.condition_type == ConditionType.VOLUME_5X:
            if volume_ratio >= 5.0:
                condition_met = True
                trigger_data = {
                    'current_volume': current_volume,
                    'average_volume': average_volume,
                    'volume_ratio': round(volume_ratio, 2),
                    'threshold': '5x'
                }
        
        return condition_met, trigger_data
    
    # ==================== Alert Triggering ====================
    
    def trigger_alert(self, alert: Alert, trigger_value: Optional[float] = None, 
                     trigger_data: Optional[Dict] = None):
        """
        Trigger an alert and create trigger record
        
        Args:
            alert: Alert object
            trigger_value: Actual value when triggered (price, percent, etc.)
            trigger_data: Additional context data
        """
        try:
            # Create trigger record
            trigger = AlertTrigger(
                alert_id=alert.id,
                trigger_value=Decimal(str(trigger_value)) if trigger_value else None,
                trigger_data=trigger_data,
                triggered_at=datetime.utcnow()
            )
            self.session.add(trigger)
            
            # Update alert
            alert.status = AlertStatus.TRIGGERED
            alert.trigger_count += 1
            alert.last_triggered_at = datetime.utcnow()
            
            self.session.commit()
            
            # Send notification (async)
            self._send_notification(alert, trigger)
            
            logger.info(f"Alert {alert.id} triggered for user {alert.user_id}")
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to trigger alert {alert.id}: {str(e)}")
            alert.status = AlertStatus.ERROR
            self.session.commit()
    
    def _send_notification(self, alert: Alert, trigger: AlertTrigger):
        """
        Send notification for triggered alert
        
        This would integrate with Firebase (push), SendGrid (email), Twilio (SMS)
        For now, just log the notification
        """
        notification_message = self._format_notification_message(alert, trigger)
        
        if alert.notification_push:
            logger.info(f"PUSH notification: {notification_message}")
            # TODO: Send via Firebase Cloud Messaging
        
        if alert.notification_email:
            logger.info(f"EMAIL notification: {notification_message}")
            # TODO: Send via SendGrid
        
        if alert.notification_sms:
            logger.info(f"SMS notification: {notification_message}")
            # TODO: Send via Twilio
        
        # Update trigger record
        trigger.notification_sent = True
        trigger.notification_sent_at = datetime.utcnow()
        trigger.notification_method = 'push' if alert.notification_push else 'email'
        self.session.commit()
    
    def _format_notification_message(self, alert: Alert, trigger: AlertTrigger) -> str:
        """Format notification message based on alert type"""
        
        if alert.alert_type == AlertType.PRICE:
            condition = "above" if alert.condition_type == ConditionType.ABOVE else "below"
            return f"📈 {alert.symbol} is now ${trigger.trigger_value}, {condition} your alert at ${alert.target_value}"
        
        elif alert.alert_type == AlertType.NEWS:
            article_count = trigger.trigger_data.get('article_count', 0)
            avg_score = trigger.trigger_data.get('avg_verification_score', 0)
            return f"📰 {alert.symbol} • {article_count} new articles (avg score: {avg_score:.0f})"
        
        elif alert.alert_type == AlertType.EARNINGS:
            if alert.condition_type == ConditionType.EARNINGS_RELEASED:
                revenue = trigger.trigger_data.get('revenue')
                revenue_expected = trigger.trigger_data.get('revenue_expected')
                return f"💼 {alert.symbol} released earnings: Revenue ${revenue}B (expected ${revenue_expected}B)"
            else:
                days = trigger.trigger_data.get('days_until', 0)
                return f"💼 {alert.symbol} earnings in {days} day{'s' if days != 1 else ''}"
        
        elif alert.alert_type == AlertType.DIVIDEND:
            amount = trigger.trigger_data.get('dividend_amount', 0)
            return f"💰 {alert.symbol} dividend: ${amount} per share"
        
        elif alert.alert_type == AlertType.PORTFOLIO:
            gain_percent = trigger.trigger_data.get('gain_percent', 0)
            return f"📊 Your portfolio crossed +{gain_percent}% gain"
        
        elif alert.alert_type == AlertType.VOLUME:
            ratio = trigger.trigger_data.get('volume_ratio', 0)
            return f"🔊 {alert.symbol} volume is {ratio}x average (unusual activity)"
        
        return f"Alert {alert.id} triggered"
    
    # ==================== Utility Methods ====================
    
    def reset_triggered_alert(self, alert_id: str):
        """Reset a triggered alert back to active status"""
        alert = self.session.query(Alert).filter(Alert.id == alert_id).first()
        if alert and alert.status == AlertStatus.TRIGGERED:
            alert.status = AlertStatus.ACTIVE
            self.session.commit()
    
    def pause_alert(self, alert_id: str):
        """Pause an alert"""
        alert = self.session.query(Alert).filter(Alert.id == alert_id).first()
        if alert:
            alert.status = AlertStatus.PAUSED
            self.session.commit()
    
    def resume_alert(self, alert_id: str):
        """Resume a paused alert"""
        alert = self.session.query(Alert).filter(Alert.id == alert_id).first()
        if alert and alert.status == AlertStatus.PAUSED:
            alert.status = AlertStatus.ACTIVE
            self.session.commit()
    
    def delete_alert(self, alert_id: str):
        """Soft delete an alert"""
        alert = self.session.query(Alert).filter(Alert.id == alert_id).first()
        if alert:
            alert.status = AlertStatus.DELETED
            self.session.commit()


# Singleton instance
alert_service = AlertService()
