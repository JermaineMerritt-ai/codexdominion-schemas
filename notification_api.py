"""
🔥 CODEX DOMINION - NOTIFICATION API 🔥
========================================
Flask API endpoints for portal notifications

Add these routes to flask_dashboard.py or import as blueprint.
"""

from flask import request, jsonify, g
from datetime import datetime
from models import PortalNotification, NotificationType


# ============================================================================
# PORTAL NOTIFICATIONS API
# ============================================================================

def register_notification_routes(app):
    """Register notification routes with Flask app"""
    
    @app.route('/api/notifications', methods=['GET'])
    def api_get_notifications():
        """
        Get portal notifications for current user/tenant
        
        Query params:
        - tenant_id: Filter by tenant (required)
        - user_id: Filter by user (optional, defaults to all tenant users)
        - type: Filter by notification type (optional)
        - is_read: Filter by read status (optional: true/false)
        - limit: Max results (default: 50)
        - offset: Pagination offset (default: 0)
        
        Returns:
            JSON array of notifications with metadata
        """
        try:
            tenant_id = request.args.get('tenant_id')
            user_id = request.args.get('user_id')
            notif_type = request.args.get('type')
            is_read = request.args.get('is_read')
            limit = int(request.args.get('limit', 50))
            offset = int(request.args.get('offset', 0))
            
            if not tenant_id:
                return jsonify({"error": "tenant_id required"}), 400
            
            session = g.db_session
            
            # Build query
            query = session.query(PortalNotification).filter(
                PortalNotification.tenant_id == tenant_id
            )
            
            if user_id:
                query = query.filter(PortalNotification.user_id == user_id)
            
            if notif_type:
                try:
                    type_enum = NotificationType[notif_type.upper()]
                    query = query.filter(PortalNotification.type == type_enum)
                except KeyError:
                    pass  # Invalid type, ignore filter
            
            if is_read is not None:
                is_read_bool = is_read.lower() == 'true'
                query = query.filter(PortalNotification.is_read == is_read_bool)
            
            # Order by created_at descending (newest first)
            query = query.order_by(PortalNotification.created_at.desc())
            
            # Apply pagination
            total_count = query.count()
            notifications = query.limit(limit).offset(offset).all()
            
            return jsonify({
                "notifications": [n.to_dict() for n in notifications],
                "total": total_count,
                "limit": limit,
                "offset": offset,
                "has_more": (offset + limit) < total_count
            })
            
        except Exception as e:
            print(f"❌ Error fetching notifications: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500
    
    
    @app.route('/api/notifications/<notification_id>/mark-read', methods=['POST'])
    def api_mark_notification_read(notification_id):
        """
        Mark a notification as read
        
        Args:
            notification_id: ID of notification to mark read
            
        Returns:
            JSON with success status
        """
        try:
            session = g.db_session
            
            notification = session.query(PortalNotification).filter_by(
                id=notification_id
            ).first()
            
            if not notification:
                return jsonify({"error": "Notification not found"}), 404
            
            notification.mark_read()
            session.commit()
            
            return jsonify({
                "success": True,
                "notification_id": notification_id,
                "read_at": notification.read_at.isoformat() if notification.read_at else None
            })
            
        except Exception as e:
            print(f"❌ Error marking notification read: {e}")
            return jsonify({"error": str(e)}), 500
    
    
    @app.route('/api/notifications/mark-all-read', methods=['POST'])
    def api_mark_all_notifications_read():
        """
        Mark all notifications as read for a tenant/user
        
        JSON body:
        - tenant_id: Required
        - user_id: Optional (marks all for tenant if omitted)
        
        Returns:
            JSON with count of notifications marked read
        """
        try:
            data = request.get_json() or {}
            tenant_id = data.get('tenant_id')
            user_id = data.get('user_id')
            
            if not tenant_id:
                return jsonify({"error": "tenant_id required"}), 400
            
            session = g.db_session
            
            # Build query for unread notifications
            query = session.query(PortalNotification).filter(
                PortalNotification.tenant_id == tenant_id,
                PortalNotification.is_read == False
            )
            
            if user_id:
                query = query.filter(PortalNotification.user_id == user_id)
            
            notifications = query.all()
            count = len(notifications)
            
            # Mark all as read
            for notification in notifications:
                notification.mark_read()
            
            session.commit()
            
            return jsonify({
                "success": True,
                "notifications_marked": count
            })
            
        except Exception as e:
            print(f"❌ Error marking all notifications read: {e}")
            return jsonify({"error": str(e)}), 500
    
    
    @app.route('/api/notifications/unread-count', methods=['GET'])
    def api_get_unread_count():
        """
        Get count of unread notifications
        
        Query params:
        - tenant_id: Required
        - user_id: Optional (counts all tenant notifications if omitted)
        
        Returns:
            JSON with unread count
        """
        try:
            tenant_id = request.args.get('tenant_id')
            user_id = request.args.get('user_id')
            
            if not tenant_id:
                return jsonify({"error": "tenant_id required"}), 400
            
            session = g.db_session
            
            # Build query
            query = session.query(PortalNotification).filter(
                PortalNotification.tenant_id == tenant_id,
                PortalNotification.is_read == False
            )
            
            if user_id:
                query = query.filter(PortalNotification.user_id == user_id)
            
            count = query.count()
            
            return jsonify({
                "unread_count": count,
                "tenant_id": tenant_id,
                "user_id": user_id
            })
            
        except Exception as e:
            print(f"❌ Error getting unread count: {e}")
            return jsonify({"error": str(e)}), 500
    
    
    @app.route('/api/notifications/<notification_id>', methods=['DELETE'])
    def api_delete_notification(notification_id):
        """
        Delete a specific notification
        
        Args:
            notification_id: ID of notification to delete
            
        Returns:
            JSON with success status
        """
        try:
            session = g.db_session
            
            notification = session.query(PortalNotification).filter_by(
                id=notification_id
            ).first()
            
            if not notification:
                return jsonify({"error": "Notification not found"}), 404
            
            session.delete(notification)
            session.commit()
            
            return jsonify({
                "success": True,
                "notification_id": notification_id
            })
            
        except Exception as e:
            print(f"❌ Error deleting notification: {e}")
            return jsonify({"error": str(e)}), 500
    
    print("✅ Notification API routes registered")


# ============================================================================
# USAGE IN FLASK_DASHBOARD.PY
# ============================================================================
"""
Add to flask_dashboard.py after app initialization:

from notification_api import register_notification_routes
register_notification_routes(app)
"""
