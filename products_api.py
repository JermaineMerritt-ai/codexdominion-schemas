"""
🔥 CODEX DOMINION - PRODUCTS API 🔥
=====================================
Product management for digital marketplace

Features:
- Create, read, update, delete products
- Support for ebooks, templates, courses, presets, packs
- JWT authentication for protected operations
- Creator-based product ownership
"""

from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from datetime import datetime
from typing import Dict, Any, Optional, List
import uuid
import json

from db import SessionLocal
from auth_api import verify_token

# Create Blueprint
products_bp = Blueprint('products', __name__, url_prefix='/api/products')


# ============================================================================
# PRODUCT MODEL (Inline - will add to models.py)
# ============================================================================

from sqlalchemy import Column, String, Text, Float, Boolean, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from models import Base, User
import enum


class ProductCategory(enum.Enum):
    """Product category types"""
    EBOOK = 'ebook'
    TEMPLATE = 'template'
    COURSE = 'course'
    PRESET = 'preset'
    PACK = 'pack'
    OTHER = 'other'


class Product(Base):
    """
    Product model for digital marketplace
    Stores information about ebooks, templates, courses, presets, and other digital products
    """
    __tablename__ = 'products'
    
    id = Column(String, primary_key=True, default=lambda: f"product_{uuid.uuid4().hex[:12]}")
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Enum(ProductCategory), nullable=False)
    price = Column(Float, nullable=False)
    file_url = Column(String, nullable=False)
    status = Column(String, default='pending')  # 'published' or 'pending'
    
    # Creator information
    creator_id = Column(String, ForeignKey('users.id'), nullable=False)
    
    # Metadata
    is_active = Column(Boolean, default=True)
    downloads_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = relationship('User', foreign_keys=[creator_id])
    shares = relationship('ProductShare', back_populates='product', cascade='all, delete-orphan')
    purchases = relationship('Purchase', back_populates='product', cascade='all, delete-orphan')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert product to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category.value,
            'price': self.price,
            'fileUrl': self.file_url,
            'status': self.status or 'pending',
            'creatorId': self.creator_id,
            'isActive': self.is_active,
            'downloadsCount': self.downloads_count,
            'createdAt': self.created_at.isoformat() + 'Z' if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() + 'Z' if self.updated_at else None
        }


class ProductShare(Base):
    """
    Product share tracking model
    Records when users share products on social media channels
    """
    __tablename__ = 'product_shares'
    
    id = Column(String, primary_key=True, default=lambda: f"share_{uuid.uuid4().hex[:12]}")
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    product_id = Column(String, ForeignKey('products.id'), nullable=False)
    channel = Column(String, nullable=False)  # 'whatsapp', 'instagram', 'tiktok', 'other'
    shared_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User')
    product = relationship('Product', back_populates='shares')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert share to dictionary"""
        return {
            'id': self.id,
            'userId': self.user_id,
            'productId': self.product_id,
            'channel': self.channel,
            'sharedAt': self.shared_at.isoformat() + 'Z' if self.shared_at else None
        }


# Purchase model for tracking sales
class Purchase(Base):
    """Purchase record with referral tracking and earnings split"""
    __tablename__ = 'purchases'
    
    id = Column(String, primary_key=True)
    order_id = Column(String, nullable=True)  # External order/transaction ID
    product_id = Column(String, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    buyer_id = Column(String, ForeignKey('users.id'), nullable=True)  # Nullable for guest purchases
    referrer_id = Column(String, ForeignKey('users.id'), nullable=True)  # Nullable for non-referred purchases
    payment_method = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    creator_earning = Column(Float, default=0)  # Amount earned by creator
    referrer_earning = Column(Float, default=0)  # Commission earned by referrer
    status = Column(String, default='paid')  # paid, pending, refunded
    purchased_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship('Product', back_populates='purchases')
    buyer = relationship('User', foreign_keys=[buyer_id], backref='purchases_made')
    referrer = relationship('User', foreign_keys=[referrer_id], backref='referrals_made')
    
    def to_dict(self) -> dict:
        """Convert purchase to dictionary"""
        return {
            'id': self.id,
            'orderId': self.order_id,
            'productId': self.product_id,
            'buyerId': self.buyer_id,
            'referrerId': self.referrer_id,
            'paymentMethod': self.payment_method,
            'amount': self.amount,
            'creatorEarning': self.creator_earning,
            'referrerEarning': self.referrer_earning,
            'status': self.status,
            'purchasedAt': self.purchased_at.isoformat() + 'Z' if self.purchased_at else None,
            'product': self.product.to_dict() if self.product else None,
            'buyer': {
                'id': self.buyer.id,
                'name': self.buyer.full_name,
                'email': self.buyer.email
            } if self.buyer else None,
            'referrer': {
                'id': self.referrer.id,
                'name': self.referrer.full_name,
                'email': self.referrer.email
            } if self.referrer else None
        }


# ============================================================================
# WITHDRAWAL MODEL (PAYOUT SYSTEM)
# ============================================================================

class Withdrawal(Base):
    """Withdrawal/payout tracking for creator and referrer earnings"""
    __tablename__ = 'withdrawals'
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    destination = Column(String, nullable=False)  # 'paypal', 'bank', 'stripe', etc.
    destination_details = Column(Text, nullable=True)  # JSON: {"email": "user@paypal.com"}
    status = Column(String, nullable=False, default='pending', index=True)  # pending|processing|completed|failed
    failure_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    processed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship('User', foreign_keys=[user_id])
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert withdrawal to dictionary"""
        destination_details_dict = None
        if self.destination_details:
            try:
                destination_details_dict = json.loads(self.destination_details)
            except:
                pass
        
        return {
            'id': self.id,
            'userId': self.user_id,
            'amount': self.amount,
            'destination': self.destination,
            'destinationDetails': destination_details_dict,
            'status': self.status,
            'failureReason': self.failure_reason,
            'createdAt': self.created_at.isoformat() + 'Z' if self.created_at else None,
            'processedAt': self.processed_at.isoformat() + 'Z' if self.processed_at else None,
            'user': {
                'id': self.user.id,
                'name': self.user.full_name,
                'email': self.user.email
            } if self.user else None
        }


# ============================================================================
# VALIDATION HELPERS
# ============================================================================

def validate_product_data(data: Dict[str, Any]) -> tuple[bool, Optional[str], Optional[str]]:
    """Validate product data"""
    
    # Validate title
    title = data.get('title', '').strip()
    if not title:
        return False, "Product title is required", "title"
    if len(title) < 3:
        return False, "Title must be at least 3 characters", "title"
    if len(title) > 200:
        return False, "Title must be less than 200 characters", "title"
    
    # Validate description
    description = data.get('description', '').strip()
    if not description:
        return False, "Product description is required", "description"
    if len(description) < 10:
        return False, "Description must be at least 10 characters", "description"
    
    # Validate category
    category = data.get('category', '').lower()
    valid_categories = ['ebook', 'template', 'course', 'preset', 'pack', 'other']
    if not category:
        return False, "Product category is required", "category"
    if category not in valid_categories:
        return False, f"Invalid category. Must be one of: {', '.join(valid_categories)}", "category"
    
    # Validate price
    price = data.get('price')
    if price is None:
        return False, "Product price is required", "price"
    try:
        price = float(price)
        if price < 0:
            return False, "Price cannot be negative", "price"
        if price > 10000:
            return False, "Price cannot exceed $10,000", "price"
    except (ValueError, TypeError):
        return False, "Price must be a valid number", "price"
    
    # Validate file URL
    file_url = data.get('fileUrl', '').strip()
    if not file_url:
        return False, "File URL is required", "fileUrl"
    if len(file_url) < 5:
        return False, "File URL must be a valid URL", "fileUrl"
    
    return True, None, None


def get_authenticated_user(token: str, db: Session) -> tuple[Optional[Any], Optional[dict]]:
    """
    Verify JWT token and return user
    Returns (user, error_response)
    """
    if not token:
        return None, {
            'success': False,
            'error': 'Authentication required. Please provide a valid token.'
        }
    
    # Remove 'Bearer ' prefix if present
    if token.startswith('Bearer '):
        token = token[7:]
    
    # Verify token
    payload = verify_token(token)
    if not payload:
        return None, {
            'success': False,
            'error': 'Invalid or expired token. Please log in again.'
        }
    
    # Get user from database
    from models import User
    user = db.query(User).filter_by(id=payload.get('user_id')).first()
    if not user:
        return None, {
            'success': False,
            'error': 'User not found'
        }
    
    return user, None


# ============================================================================
# ROUTES
# ============================================================================

@products_bp.route('', methods=['POST'])
def create_product():
    """
    Create a new product
    
    POST /api/products
    Headers: Authorization: Bearer <token>
    Body: {
        "title": "My Ebook",
        "description": "An amazing ebook about...",
        "category": "ebook",
        "price": 9.99,
        "fileUrl": "https://example.com/files/ebook.pdf"
    }
    
    Returns:
    {
        "success": true,
        "message": "Product created successfully! 🎉",
        "product": {...}
    }
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization', '')
        
        # Parse request data
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate product data
        valid, error, field = validate_product_data(data)
        if not valid:
            return jsonify({
                'success': False,
                'error': error,
                'field': field
            }), 400
        
        # Create database session
        db: Session = SessionLocal()
        
        try:
            # Authenticate user
            user, auth_error = get_authenticated_user(auth_header, db)
            if auth_error:
                return jsonify(auth_error), 401
            
            # Create product
            product_id = f"product_{uuid.uuid4().hex[:12]}"
            new_product = Product(
                id=product_id,
                title=data['title'].strip(),
                description=data['description'].strip(),
                category=ProductCategory(data['category'].lower()),
                price=float(data['price']),
                file_url=data['fileUrl'].strip(),
                creator_id=user.id,
                is_active=True,
                downloads_count=0,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            # Add to database
            db.add(new_product)
            db.commit()
            db.refresh(new_product)
            
            # Return success response
            return jsonify({
                'success': True,
                'message': 'Product created successfully! 🎉',
                'product': new_product.to_dict()
            }), 201
            
        except Exception as e:
            db.rollback()
            print(f"❌ Product creation error: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to create product. Please try again.'
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        print(f"❌ Request error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Invalid request'
        }), 400


@products_bp.route('', methods=['GET'])
def list_products():
    """
    Get all products with optional filters
    
    GET /api/products?category=ebook&creator_id=user_123&page=1&limit=20
    
    Query Parameters:
    - category: Filter by category (ebook, template, course, preset, pack, other)
    - creator_id: Filter by creator
    - page: Page number (default: 1)
    - limit: Items per page (default: 20, max: 100)
    - active_only: Show only active products (default: true)
    
    Returns:
    {
        "success": true,
        "products": [...],
        "pagination": {
            "page": 1,
            "limit": 20,
            "total": 50,
            "pages": 3
        }
    }
    """
    try:
        # Get query parameters
        category = request.args.get('category', '').lower()
        creator_id = request.args.get('creator_id', '').strip()
        page = int(request.args.get('page', 1))
        limit = min(int(request.args.get('limit', 20)), 100)  # Max 100 items
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        
        # Create database session
        db: Session = SessionLocal()
        
        try:
            # Build query
            query = db.query(Product)
            
            # Apply filters
            if active_only:
                query = query.filter(Product.is_active == True)
            
            if category and category in ['ebook', 'template', 'course', 'preset', 'pack', 'other']:
                query = query.filter(Product.category == ProductCategory(category))
            
            if creator_id:
                query = query.filter(Product.creator_id == creator_id)
            
            # Get total count
            total = query.count()
            
            # Apply pagination
            offset = (page - 1) * limit
            products = query.order_by(Product.created_at.desc()).offset(offset).limit(limit).all()
            
            # Calculate total pages
            total_pages = (total + limit - 1) // limit
            
            # Return results
            return jsonify({
                'success': True,
                'products': [p.to_dict() for p in products],
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': total,
                    'pages': total_pages
                }
            }), 200
            
        finally:
            db.close()
    
    except ValueError:
        return jsonify({
            'success': False,
            'error': 'Invalid pagination parameters'
        }), 400
    
    except Exception as e:
        print(f"❌ List products error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve products'
        }), 500


@products_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id: str):
    """
    Get a single product by ID
    
    GET /api/products/<product_id>
    
    Returns:
    {
        "success": true,
        "product": {...}
    }
    """
    try:
        # Create database session
        db: Session = SessionLocal()
        
        try:
            # Get product
            product = db.query(Product).filter_by(id=product_id).first()
            
            if not product:
                return jsonify({
                    'success': False,
                    'error': 'Product not found'
                }), 404
            
            return jsonify({
                'success': True,
                'product': product.to_dict()
            }), 200
            
        finally:
            db.close()
    
    except Exception as e:
        print(f"❌ Get product error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve product'
        }), 500


@products_bp.route('/<product_id>', methods=['PUT'])
def update_product(product_id: str):
    """
    Update a product (owner only)
    
    PUT /api/products/<product_id>
    Headers: Authorization: Bearer <token>
    Body: {
        "title": "Updated Title",
        "description": "Updated description",
        "price": 14.99
    }
    
    Returns:
    {
        "success": true,
        "message": "Product updated successfully! ✅",
        "product": {...}
    }
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization', '')
        
        # Parse request data
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Create database session
        db: Session = SessionLocal()
        
        try:
            # Authenticate user
            user, auth_error = get_authenticated_user(auth_header, db)
            if auth_error:
                return jsonify(auth_error), 401
            
            # Get product
            product = db.query(Product).filter_by(id=product_id).first()
            if not product:
                return jsonify({
                    'success': False,
                    'error': 'Product not found'
                }), 404
            
            # Check ownership
            if product.creator_id != user.id:
                return jsonify({
                    'success': False,
                    'error': 'You can only update your own products'
                }), 403
            
            # Update fields
            if 'title' in data:
                title = data['title'].strip()
                if len(title) < 3:
                    return jsonify({
                        'success': False,
                        'error': 'Title must be at least 3 characters',
                        'field': 'title'
                    }), 400
                product.title = title
            
            if 'description' in data:
                description = data['description'].strip()
                if len(description) < 10:
                    return jsonify({
                        'success': False,
                        'error': 'Description must be at least 10 characters',
                        'field': 'description'
                    }), 400
                product.description = description
            
            if 'category' in data:
                category = data['category'].lower()
                if category not in ['ebook', 'template', 'course', 'preset', 'pack', 'other']:
                    return jsonify({
                        'success': False,
                        'error': 'Invalid category',
                        'field': 'category'
                    }), 400
                product.category = ProductCategory(category)
            
            if 'price' in data:
                try:
                    price = float(data['price'])
                    if price < 0 or price > 10000:
                        return jsonify({
                            'success': False,
                            'error': 'Price must be between $0 and $10,000',
                            'field': 'price'
                        }), 400
                    product.price = price
                except (ValueError, TypeError):
                    return jsonify({
                        'success': False,
                        'error': 'Invalid price format',
                        'field': 'price'
                    }), 400
            
            if 'fileUrl' in data:
                file_url = data['fileUrl'].strip()
                if len(file_url) < 5:
                    return jsonify({
                        'success': False,
                        'error': 'Invalid file URL',
                        'field': 'fileUrl'
                    }), 400
                product.file_url = file_url
            
            if 'isActive' in data:
                product.is_active = bool(data['isActive'])
            
            # Update timestamp
            product.updated_at = datetime.utcnow()
            
            # Save changes
            db.commit()
            db.refresh(product)
            
            return jsonify({
                'success': True,
                'message': 'Product updated successfully! ✅',
                'product': product.to_dict()
            }), 200
            
        except Exception as e:
            db.rollback()
            print(f"❌ Product update error: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to update product'
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        print(f"❌ Request error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Invalid request'
        }), 400


@products_bp.route('/<product_id>/status', methods=['PATCH'])
def update_product_status(product_id: str):
    """
    Update product publication status (owner only)
    
    PATCH /api/products/<product_id>/status
    Headers: Authorization: Bearer <token>
    Body: {
        "productId": "product_abc123",
        "status": "published"  // or "pending"
    }
    
    Returns:
    {
        "success": true,
        "message": "Product status updated to published",
        "product": {...}
    }
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization', '')
        
        # Parse request data
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate status
        new_status = data.get('status', '').lower()
        if new_status not in ['published', 'pending']:
            return jsonify({
                'success': False,
                'error': 'Status must be either "published" or "pending"',
                'field': 'status'
            }), 400
        
        # Create database session
        db: Session = SessionLocal()
        
        try:
            # Authenticate user
            user, auth_error = get_authenticated_user(auth_header, db)
            if auth_error:
                return jsonify(auth_error), 401
            
            # Get product
            product = db.query(Product).filter_by(id=product_id).first()
            if not product:
                return jsonify({
                    'success': False,
                    'error': 'Product not found'
                }), 404
            
            # Check ownership
            if product.creator_id != user.id:
                return jsonify({
                    'success': False,
                    'error': 'You can only update status of your own products'
                }), 403
            
            # Update status
            old_status = product.status or 'pending'
            product.status = new_status
            product.updated_at = datetime.utcnow()
            
            # Save changes
            db.commit()
            db.refresh(product)
            
            return jsonify({
                'success': True,
                'message': f'Product status updated to {new_status}',
                'product': product.to_dict(),
                'previousStatus': old_status
            }), 200
            
        except Exception as e:
            db.rollback()
            print(f"❌ Status update error: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to update product status'
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        print(f"❌ Request error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Invalid request'
        }), 400


@products_bp.route('/<product_id>/share', methods=['POST'])
def track_product_share(product_id: str):
    """
    Track when a user shares a product on social media
    
    POST /api/products/<product_id>/share
    Headers: Authorization: Bearer <token>
    Body: {
        "userId": "user_abc123",
        "productId": "product_xyz789",
        "channel": "whatsapp"  // whatsapp, instagram, tiktok, other
    }
    
    Returns:
    {
        "success": true,
        "message": "Share tracked successfully!",
        "share": {...}
    }
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization', '')
        
        # Parse request data
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate channel
        channel = data.get('channel', '').lower()
        valid_channels = ['whatsapp', 'instagram', 'tiktok', 'other']
        if channel not in valid_channels:
            return jsonify({
                'success': False,
                'error': f'Invalid channel. Must be one of: {", ".join(valid_channels)}',
                'field': 'channel'
            }), 400
        
        # Create database session
        db: Session = SessionLocal()
        
        try:
            # Authenticate user
            user, auth_error = get_authenticated_user(auth_header, db)
            if auth_error:
                return jsonify(auth_error), 401
            
            # Verify product exists
            product = db.query(Product).filter_by(id=product_id).first()
            if not product:
                return jsonify({
                    'success': False,
                    'error': 'Product not found'
                }), 404
            
            # Create share record
            share_id = f"share_{uuid.uuid4().hex[:12]}"
            new_share = ProductShare(
                id=share_id,
                user_id=user.id,
                product_id=product_id,
                channel=channel,
                shared_at=datetime.utcnow()
            )
            
            # Add to database
            db.add(new_share)
            db.commit()
            db.refresh(new_share)
            
            # Return success response
            return jsonify({
                'success': True,
                'message': 'Share tracked successfully! 📊',
                'share': new_share.to_dict()
            }), 201
            
        except Exception as e:
            db.rollback()
            print(f"❌ Share tracking error: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to track share. Please try again.'
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        print(f"❌ Request error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Invalid request'
        }), 400


@products_bp.route('/<product_id>/analytics', methods=['GET'])
def get_product_analytics(product_id: str):
    """
    Get share analytics for a product
    
    GET /api/products/<product_id>/analytics
    
    Returns:
    {
        "success": true,
        "analytics": {
            "totalShares": 125,
            "channelBreakdown": {
                "whatsapp": 50,
                "instagram": 40,
                "tiktok": 30,
                "other": 5
            },
            "uniqueSharers": 45,
            "recentShares": [...]
        }
    }
    """
    try:
        # Create database session
        db: Session = SessionLocal()
        
        try:
            # Verify product exists
            product = db.query(Product).filter_by(id=product_id).first()
            if not product:
                return jsonify({
                    'success': False,
                    'error': 'Product not found'
                }), 404
            
            # Get all shares for this product
            shares = db.query(ProductShare).filter_by(product_id=product_id).all()
            
            # Calculate analytics
            total_shares = len(shares)
            
            # Channel breakdown
            channel_breakdown = {
                'whatsapp': 0,
                'instagram': 0,
                'tiktok': 0,
                'other': 0
            }
            
            unique_sharers = set()
            
            for share in shares:
                channel_breakdown[share.channel] = channel_breakdown.get(share.channel, 0) + 1
                unique_sharers.add(share.user_id)
            
            # Get 10 most recent shares
            recent_shares = db.query(ProductShare)\
                .filter_by(product_id=product_id)\
                .order_by(ProductShare.shared_at.desc())\
                .limit(10)\
                .all()
            
            # Return analytics
            return jsonify({
                'success': True,
                'analytics': {
                    'totalShares': total_shares,
                    'channelBreakdown': channel_breakdown,
                    'uniqueSharers': len(unique_sharers),
                    'recentShares': [share.to_dict() for share in recent_shares]
                },
                'product': {
                    'id': product.id,
                    'title': product.title
                }
            }), 200
            
        finally:
            db.close()
    
    except Exception as e:
        print(f"❌ Analytics error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve analytics'
        }), 500


@products_bp.route('/<product_id>', methods=['DELETE'])
def delete_product(product_id: str):
    """
    Delete a product (owner only)
    
    DELETE /api/products/<product_id>
    Headers: Authorization: Bearer <token>
    
    Returns:
    {
        "success": true,
        "message": "Product deleted successfully"
    }
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization', '')
        
        # Create database session
        db: Session = SessionLocal()
        
        try:
            # Authenticate user
            user, auth_error = get_authenticated_user(auth_header, db)
            if auth_error:
                return jsonify(auth_error), 401
            
            # Get product
            product = db.query(Product).filter_by(id=product_id).first()
            if not product:
                return jsonify({
                    'success': False,
                    'error': 'Product not found'
                }), 404
            
            # Check ownership
            if product.creator_id != user.id:
                return jsonify({
                    'success': False,
                    'error': 'You can only delete your own products'
                }), 403
            
            # Delete associated shares first (CASCADE)
            db.query(ProductShare).filter_by(product_id=product_id).delete()
            
            # Delete product
            db.delete(product)
            db.commit()
            
            return jsonify({
                'success': True,
                'message': 'Product deleted successfully'
            }), 200
            
        except Exception as e:
            db.rollback()
            print(f"❌ Product deletion error: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to delete product'
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        print(f"❌ Request error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Invalid request'
        }), 400


# ============================================================================
# PURCHASE TRACKING ENDPOINTS
# ============================================================================

@products_bp.route('/purchases', methods=['POST'])
def record_purchase():
    """
    🛒 Record a product purchase
    
    POST /api/products/purchases
    Body: {
        "productId": "product_abc123",
        "buyerId": "user_xyz789" (optional - null for guest purchases),
        "referrerId": "user_def456" (optional - null for non-referred purchases),
        "paymentMethod": "stripe" (required)
    }
    
    Returns: Purchase record with ID
    """
    try:
        data = request.get_json()
        
        # Get product ID
        product_id = data.get('productId')
        if not product_id:
            return jsonify({
                'success': False,
                'error': 'Product ID is required',
                'field': 'productId'
            }), 400
        
        # Get payment method
        payment_method = data.get('paymentMethod', '').strip()
        if not payment_method:
            return jsonify({
                'success': False,
                'error': 'Payment method is required',
                'field': 'paymentMethod'
            }), 400
        
        # Get optional buyer and referrer IDs
        buyer_id = data.get('buyerId')
        referrer_id = data.get('referrerId')
        
        # Database operations
        db = SessionLocal()
        
        try:
            # Verify product exists and is published
            product = db.query(Product).filter_by(id=product_id).first()
            if not product:
                return jsonify({
                    'success': False,
                    'error': 'Product not found'
                }), 404
            
            if product.status != 'published':
                return jsonify({
                    'success': False,
                    'error': 'Product is not available for purchase'
                }), 400
            
            # Verify buyer exists (if provided)
            if buyer_id:
                buyer = db.query(User).filter_by(id=buyer_id).first()
                if not buyer:
                    return jsonify({
                        'success': False,
                        'error': 'Buyer not found'
                    }), 404
            
            # Verify referrer exists (if provided)
            if referrer_id:
                referrer = db.query(User).filter_by(id=referrer_id).first()
                if not referrer:
                    print(f"❌ Referrer validation failed: {referrer_id} not found in database")
                    return jsonify({
                        'success': False,
                        'error': 'Referrer not found',
                        'referrerId': referrer_id
                    }), 404
                print(f"✅ Referrer validated: {referrer_id} ({referrer.full_name})")
            
            # Calculate earnings split
            # Default: 20% commission for referrers, 80% for creators
            REFERRER_COMMISSION_RATE = 0.20
            
            if referrer_id:
                referrer_earning = product.price * REFERRER_COMMISSION_RATE
                creator_earning = product.price - referrer_earning
            else:
                referrer_earning = 0
                creator_earning = product.price
            
            # Generate order ID
            order_id = data.get('orderId') or f"order_{uuid.uuid4().hex[:12]}"
            
            # Get status (default to 'paid')
            status = data.get('status', 'paid')
            valid_statuses = ['paid', 'pending', 'refunded']
            if status not in valid_statuses:
                status = 'paid'
            
            # Create purchase record
            purchase = Purchase(
                id=f"purchase_{uuid.uuid4().hex[:12]}",
                order_id=order_id,
                product_id=product_id,
                buyer_id=buyer_id,
                referrer_id=referrer_id,
                payment_method=payment_method,
                amount=product.price,
                creator_earning=creator_earning,
                referrer_earning=referrer_earning,
                status=status,
                purchased_at=datetime.utcnow()
            )
            
            # Update product downloads count
            product.downloads_count += 1
            
            db.add(purchase)
            db.commit()
            db.refresh(purchase)
            
            print(f"✅ Purchase recorded: {purchase.id}")
            print(f"   Order ID: {order_id}")
            print(f"   Product: {product.title} (${purchase.amount})")
            print(f"   Creator Earning: ${creator_earning:.2f}")
            print(f"   Referrer Earning: ${referrer_earning:.2f}")
            print(f"   Buyer: {buyer_id or 'Guest'}")
            print(f"   Referrer: {referrer_id or 'None'}")
            print(f"   Payment Method: {payment_method}")
            print(f"   Status: {status}")
            
            return jsonify({
                'success': True,
                'message': 'Purchase recorded successfully',
                'purchase': purchase.to_dict()
            }), 201
            
        except Exception as e:
            db.rollback()
            import traceback
            error_traceback = traceback.format_exc()
            print(f"❌ Purchase recording error: {str(e)}")
            print(f"❌ Error type: {type(e).__name__}")
            print(f"❌ Traceback:\n{error_traceback}")
            print(f"❌ Debug Info:")
            print(f"   - Product ID: {product_id}")
            print(f"   - Buyer ID: {buyer_id}")
            print(f"   - Referrer ID: {referrer_id}")
            try:
                print(f"   - Product Price: {product.price}")
                print(f"   - Creator Earning: {creator_earning}")
                print(f"   - Referrer Earning: {referrer_earning}")
                print(f"   - Order ID: {order_id}")
                print(f"   - Status: {status}")
            except NameError:
                print(f"   - (Some variables not yet defined)")
            return jsonify({
                'success': False,
                'error': 'Failed to record purchase',
                'debug': str(e)
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"❌ record_purchase() outer exception: {str(e)}")
        print(f"❌ Error type: {type(e).__name__}")
        print(f"❌ Full traceback:\n{error_traceback}")
        try:
            request_data = request.get_json() if request.is_json else None
            print(f"❌ Request data: {request_data}")
        except:
            print(f"❌ Could not parse request data")
        return jsonify({
            'success': False,
            'error': 'Invalid request',
            'debug': str(e)
        }), 400


@products_bp.route('/purchases/analytics', methods=['GET'])
def get_purchase_analytics():
    """
    📊 Get purchase analytics
    
    GET /api/products/purchases/analytics
    
    Optional query params:
    - startDate: ISO 8601 date string
    - endDate: ISO 8601 date string
    - productId: Filter by specific product
    - referrerId: Filter by specific referrer
    
    Returns: {
        totalRevenue: number,
        totalPurchases: number,
        averageOrderValue: number,
        revenueByPaymentMethod: {},
        topProducts: [],
        referralStats: {}
    }
    """
    try:
        # Get optional filters
        start_date_str = request.args.get('startDate')
        end_date_str = request.args.get('endDate')
        product_id = request.args.get('productId')
        referrer_id = request.args.get('referrerId')
        
        db = SessionLocal()
        
        try:
            # Build query
            query = db.query(Purchase)
            
            # Apply filters
            if start_date_str:
                try:
                    start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
                    query = query.filter(Purchase.purchased_at >= start_date)
                except:
                    pass
            
            if end_date_str:
                try:
                    end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
                    query = query.filter(Purchase.purchased_at <= end_date)
                except:
                    pass
            
            if product_id:
                query = query.filter(Purchase.product_id == product_id)
            
            if referrer_id:
                query = query.filter(Purchase.referrer_id == referrer_id)
            
            # Get all matching purchases
            purchases = query.all()
            
            # Calculate total revenue and earnings
            total_revenue = sum(p.amount for p in purchases)
            total_creator_earnings = sum(p.creator_earning for p in purchases)
            total_referrer_earnings = sum(p.referrer_earning for p in purchases)
            total_purchases = len(purchases)
            average_order_value = total_revenue / total_purchases if total_purchases > 0 else 0
            
            # Revenue by payment method
            revenue_by_payment = {}
            for purchase in purchases:
                method = purchase.payment_method
                if method not in revenue_by_payment:
                    revenue_by_payment[method] = {'count': 0, 'revenue': 0}
                revenue_by_payment[method]['count'] += 1
                revenue_by_payment[method]['revenue'] += purchase.amount
            
            # Top products by revenue
            product_revenue = {}
            for purchase in purchases:
                if purchase.product_id not in product_revenue:
                    product_revenue[purchase.product_id] = {
                        'productId': purchase.product_id,
                        'productTitle': purchase.product.title if purchase.product else 'Unknown',
                        'count': 0,
                        'revenue': 0
                    }
                product_revenue[purchase.product_id]['count'] += 1
                product_revenue[purchase.product_id]['revenue'] += purchase.amount
            
            # Sort by revenue and take top 10
            top_products = sorted(
                product_revenue.values(),
                key=lambda x: x['revenue'],
                reverse=True
            )[:10]
            
            # Referral statistics
            referral_stats = {
                'totalReferredPurchases': sum(1 for p in purchases if p.referrer_id),
                'totalReferralRevenue': sum(p.amount for p in purchases if p.referrer_id),
                'totalReferrerEarnings': sum(p.referrer_earning for p in purchases if p.referrer_id),
                'uniqueReferrers': len(set(p.referrer_id for p in purchases if p.referrer_id)),
                'nonReferredPurchases': sum(1 for p in purchases if not p.referrer_id),
                'nonReferredRevenue': sum(p.amount for p in purchases if not p.referrer_id)
            }
            
            # Top referrers
            referrer_stats = {}
            for purchase in purchases:
                if purchase.referrer_id:
                    if purchase.referrer_id not in referrer_stats:
                        referrer_stats[purchase.referrer_id] = {
                            'referrerId': purchase.referrer_id,
                            'referrerName': purchase.referrer.full_name if purchase.referrer else 'Unknown',
                            'referrerEmail': purchase.referrer.email if purchase.referrer else 'Unknown',
                            'count': 0,
                            'revenue': 0,
                            'earnings': 0
                        }
                    referrer_stats[purchase.referrer_id]['count'] += 1
                    referrer_stats[purchase.referrer_id]['revenue'] += purchase.amount
                    referrer_stats[purchase.referrer_id]['earnings'] += purchase.referrer_earning
            
            # Sort by revenue
            top_referrers = sorted(
                referrer_stats.values(),
                key=lambda x: x['revenue'],
                reverse=True
            )[:10]
            
            referral_stats['topReferrers'] = top_referrers
            
            # Recent purchases (last 10)
            recent_purchases = sorted(purchases, key=lambda p: p.purchased_at, reverse=True)[:10]
            
            analytics = {
                'totalRevenue': round(total_revenue, 2),
                'totalCreatorEarnings': round(total_creator_earnings, 2),
                'totalReferrerEarnings': round(total_referrer_earnings, 2),
                'totalPurchases': total_purchases,
                'averageOrderValue': round(average_order_value, 2),
                'revenueByPaymentMethod': revenue_by_payment,
                'topProducts': top_products,
                'referralStats': referral_stats,
                'recentPurchases': [p.to_dict() for p in recent_purchases]
            }
            
            return jsonify({
                'success': True,
                'analytics': analytics
            }), 200
            
        except Exception as e:
            print(f"❌ Analytics error: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to get analytics'
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        print(f"❌ Request error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Invalid request'
        }), 400


@products_bp.route('/<product_id>/purchases', methods=['GET'])
def get_product_purchases(product_id: str):
    """
    📦 Get all purchases for a specific product
    
    GET /api/products/{product_id}/purchases
    
    Requires authentication (creator only)
    
    Returns: List of purchases for the product
    """
    try:
        # Get auth header
        auth_header = request.headers.get('Authorization', '')
        if not auth_header:
            return jsonify({
                'success': False,
                'error': 'Authorization required'
            }), 401
        
        db = SessionLocal()
        
        try:
            # Authenticate user
            user, auth_error = get_authenticated_user(auth_header, db)
            if auth_error:
                return jsonify(auth_error), 401
            
            # Get product
            product = db.query(Product).filter_by(id=product_id).first()
            if not product:
                return jsonify({
                    'success': False,
                    'error': 'Product not found'
                }), 404
            
            # Check ownership
            if product.creator_id != user.id:
                return jsonify({
                    'success': False,
                    'error': 'You can only view purchases for your own products'
                }), 403
            
            # Get all purchases
            purchases = db.query(Purchase).filter_by(product_id=product_id).order_by(Purchase.purchased_at.desc()).all()
            
            # Calculate revenue
            total_revenue = sum(p.amount for p in purchases)
            
            return jsonify({
                'success': True,
                'product': {
                    'id': product.id,
                    'title': product.title
                },
                'totalPurchases': len(purchases),
                'totalRevenue': round(total_revenue, 2),
                'purchases': [p.to_dict() for p in purchases]
            }), 200
            
        except Exception as e:
            print(f"❌ Product purchases error: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to get product purchases'
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        print(f"❌ Request error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Invalid request'
        }), 400


# ============================================================================
# WITHDRAWAL/PAYOUT ENDPOINTS
# ============================================================================

@products_bp.route('/withdrawals', methods=['POST'])
def create_withdrawal():
    """
    💰 Create a withdrawal request
    
    POST /api/withdrawals
    Body: {
        "userId": "user_abc123",
        "amount": 50.00,
        "destination": "paypal",
        "destinationDetails": {"email": "user@paypal.com"} (optional)
    }
    
    Returns: Withdrawal record with status 'pending'
    """
    try:
        data = request.get_json()
        
        # Get user ID
        user_id = data.get('userId')
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'User ID is required',
                'field': 'userId'
            }), 400
        
        # Get amount
        amount = data.get('amount')
        if not amount:
            return jsonify({
                'success': False,
                'error': 'Amount is required',
                'field': 'amount'
            }), 400
        
        try:
            amount = float(amount)
            if amount <= 0:
                return jsonify({
                    'success': False,
                    'error': 'Amount must be greater than 0',
                    'field': 'amount'
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'Invalid amount format',
                'field': 'amount'
            }), 400
        
        # Get destination
        destination = data.get('destination', '').strip().lower()
        if not destination:
            return jsonify({
                'success': False,
                'error': 'Destination is required',
                'field': 'destination'
            }), 400
        
        valid_destinations = ['paypal', 'bank', 'stripe', 'venmo', 'cashapp']
        if destination not in valid_destinations:
            return jsonify({
                'success': False,
                'error': f'Invalid destination. Must be one of: {", ".join(valid_destinations)}',
                'field': 'destination'
            }), 400
        
        # Get optional destination details
        destination_details = data.get('destinationDetails')
        destination_details_json = None
        if destination_details:
            if isinstance(destination_details, dict):
                destination_details_json = json.dumps(destination_details)
            else:
                destination_details_json = str(destination_details)
        
        # Database operations
        db = SessionLocal()
        
        try:
            # Verify user exists
            from models import User
            user = db.query(User).filter_by(id=user_id).first()
            if not user:
                return jsonify({
                    'success': False,
                    'error': 'User not found'
                }), 404
            
            # Calculate available balance
            # Total earnings = creator earnings + referrer earnings from purchases
            creator_earnings = db.query(func.sum(Purchase.creator_earning)).filter(
                Purchase.product.has(creator_id=user_id),
                Purchase.status == 'paid'
            ).scalar() or 0
            
            referrer_earnings = db.query(func.sum(Purchase.referrer_earning)).filter(
                Purchase.referrer_id == user_id,
                Purchase.status == 'paid'
            ).scalar() or 0
            
            total_earnings = creator_earnings + referrer_earnings
            
            # Total already withdrawn (completed withdrawals)
            total_withdrawn = db.query(func.sum(Withdrawal.amount)).filter(
                Withdrawal.user_id == user_id,
                Withdrawal.status == 'completed'
            ).scalar() or 0
            
            available_balance = total_earnings - total_withdrawn
            
            # Validate sufficient balance
            if amount > available_balance:
                return jsonify({
                    'success': False,
                    'error': f'Insufficient balance. Available: ${available_balance:.2f}, Requested: ${amount:.2f}',
                    'availableBalance': available_balance,
                    'requestedAmount': amount
                }), 400
            
            # Create withdrawal record
            withdrawal = Withdrawal(
                id=f"withdrawal_{uuid.uuid4().hex[:12]}",
                user_id=user_id,
                amount=amount,
                destination=destination,
                destination_details=destination_details_json,
                status='pending',
                created_at=datetime.utcnow()
            )
            
            db.add(withdrawal)
            db.commit()
            db.refresh(withdrawal)
            
            print(f"✅ Withdrawal created: {withdrawal.id}")
            print(f"   User: {user.full_name} ({user_id})")
            print(f"   Amount: ${amount:.2f}")
            print(f"   Available Balance: ${available_balance:.2f}")
            print(f"   Destination: {destination}")
            print(f"   Status: pending")
            
            return jsonify({
                'success': True,
                'message': 'Withdrawal request created successfully',
                'withdrawal': withdrawal.to_dict(),
                'availableBalance': available_balance - amount  # Remaining after this withdrawal
            }), 201
            
        except Exception as e:
            db.rollback()
            import traceback
            error_traceback = traceback.format_exc()
            print(f"❌ Withdrawal creation error: {str(e)}")
            print(f"❌ Traceback:\n{error_traceback}")
            return jsonify({
                'success': False,
                'error': 'Failed to create withdrawal',
                'debug': str(e)
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"❌ create_withdrawal() outer exception: {str(e)}")
        print(f"❌ Traceback:\n{error_traceback}")
        return jsonify({
            'success': False,
            'error': 'Invalid request',
            'debug': str(e)
        }), 400


@products_bp.route('/withdrawals/<withdrawal_id>', methods=['PATCH'])
def update_withdrawal_status(withdrawal_id):
    """
    🔄 Update withdrawal status (admin/system endpoint)
    
    PATCH /api/withdrawals/:id
    Body: {
        "status": "processing | completed | failed",
        "failureReason": "Optional error message for failed withdrawals"
    }
    
    Returns: Updated withdrawal record
    """
    try:
        data = request.get_json()
        
        # Get status
        status = data.get('status', '').strip().lower()
        if not status:
            return jsonify({
                'success': False,
                'error': 'Status is required',
                'field': 'status'
            }), 400
        
        valid_statuses = ['processing', 'completed', 'failed']
        if status not in valid_statuses:
            return jsonify({
                'success': False,
                'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}',
                'field': 'status'
            }), 400
        
        # Get optional failure reason
        failure_reason = data.get('failureReason')
        
        # Database operations
        db = SessionLocal()
        
        try:
            # Get withdrawal
            withdrawal = db.query(Withdrawal).filter_by(id=withdrawal_id).first()
            if not withdrawal:
                return jsonify({
                    'success': False,
                    'error': 'Withdrawal not found'
                }), 404
            
            # Update status
            old_status = withdrawal.status
            withdrawal.status = status
            
            # Set processed_at timestamp for completed/failed
            if status in ['completed', 'failed']:
                withdrawal.processed_at = datetime.utcnow()
            
            # Set failure reason if provided
            if failure_reason and status == 'failed':
                withdrawal.failure_reason = failure_reason
            
            db.commit()
            db.refresh(withdrawal)
            
            print(f"✅ Withdrawal status updated: {withdrawal.id}")
            print(f"   Old Status: {old_status}")
            print(f"   New Status: {status}")
            if failure_reason:
                print(f"   Failure Reason: {failure_reason}")
            
            return jsonify({
                'success': True,
                'message': f'Withdrawal status updated to {status}',
                'withdrawal': withdrawal.to_dict()
            }), 200
            
        except Exception as e:
            db.rollback()
            import traceback
            error_traceback = traceback.format_exc()
            print(f"❌ Withdrawal update error: {str(e)}")
            print(f"❌ Traceback:\n{error_traceback}")
            return jsonify({
                'success': False,
                'error': 'Failed to update withdrawal',
                'debug': str(e)
            }), 500
        
        finally:
            db.close()
    
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"❌ update_withdrawal_status() outer exception: {str(e)}")
        print(f"❌ Traceback:\n{error_traceback}")
        return jsonify({
            'success': False,
            'error': 'Invalid request',
            'debug': str(e)
        }), 400


@products_bp.route('/users/<user_id>/balance', methods=['GET'])
def get_user_balance(user_id):
    """
    💵 Get user's available balance
    
    GET /api/users/:id/balance
    
    Returns: {
        availableBalance: Total earnings - completed withdrawals,
        totalEarnings: Sum of creator + referrer earnings,
        creatorEarnings: Earnings from own products,
        referrerEarnings: Commission from referrals,
        totalWithdrawn: Sum of completed withdrawals,
        pendingWithdrawals: Sum of pending + processing withdrawals
    }
    """
    try:
        db = SessionLocal()
        
        try:
            # Verify user exists
            from models import User
            user = db.query(User).filter_by(id=user_id).first()
            if not user:
                return jsonify({
                    'success': False,
                    'error': 'User not found'
                }), 404
            
            # Calculate creator earnings (from products they own)
            creator_earnings = db.query(func.sum(Purchase.creator_earning)).filter(
                Purchase.product.has(creator_id=user_id),
                Purchase.status == 'paid'
            ).scalar() or 0
            
            # Calculate referrer earnings (commission from referrals)
            referrer_earnings = db.query(func.sum(Purchase.referrer_earning)).filter(
                Purchase.referrer_id == user_id,
                Purchase.status == 'paid'
            ).scalar() or 0
            
            total_earnings = creator_earnings + referrer_earnings
            
            # Calculate total withdrawn (completed withdrawals)
            total_withdrawn = db.query(func.sum(Withdrawal.amount)).filter(
                Withdrawal.user_id == user_id,
                Withdrawal.status == 'completed'
            ).scalar() or 0
            
            # Calculate pending withdrawals (pending + processing)
            pending_withdrawals = db.query(func.sum(Withdrawal.amount)).filter(
                Withdrawal.user_id == user_id,
                Withdrawal.status.in_(['pending', 'processing'])
            ).scalar() or 0
            
            # Available balance = total earned - withdrawn
            available_balance = total_earnings - total_withdrawn - pending_withdrawals
            
            return jsonify({
                'success': True,
                'balance': {
                    'availableBalance': round(available_balance, 2),
                    'totalEarnings': round(total_earnings, 2),
                    'creatorEarnings': round(creator_earnings, 2),
                    'referrerEarnings': round(referrer_earnings, 2),
                    'totalWithdrawn': round(total_withdrawn, 2),
                    'pendingWithdrawals': round(pending_withdrawals, 2)
                }
            }), 200
            
        finally:
            db.close()
    
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"❌ get_user_balance() exception: {str(e)}")
        print(f"❌ Traceback:\n{error_traceback}")
        return jsonify({
            'success': False,
            'error': 'Failed to get balance',
            'debug': str(e)
        }), 500


@products_bp.route('/users/<user_id>/withdrawals', methods=['GET'])
def get_user_withdrawals(user_id):
    """
    📋 Get user's withdrawal history
    
    GET /api/users/:id/withdrawals
    
    Optional query params:
    - status: Filter by status (pending|processing|completed|failed)
    - limit: Number of results (default: 50)
    - offset: Pagination offset (default: 0)
    
    Returns: List of withdrawals
    """
    try:
        db = SessionLocal()
        
        try:
            # Verify user exists
            from models import User
            user = db.query(User).filter_by(id=user_id).first()
            if not user:
                return jsonify({
                    'success': False,
                    'error': 'User not found'
                }), 404
            
            # Build query
            query = db.query(Withdrawal).filter_by(user_id=user_id)
            
            # Filter by status if provided
            status_filter = request.args.get('status')
            if status_filter:
                query = query.filter_by(status=status_filter.lower())
            
            # Get pagination params
            limit = int(request.args.get('limit', 50))
            offset = int(request.args.get('offset', 0))
            
            # Get total count
            total_count = query.count()
            
            # Get withdrawals with pagination, ordered by created_at desc
            withdrawals = query.order_by(Withdrawal.created_at.desc()).offset(offset).limit(limit).all()
            
            return jsonify({
                'success': True,
                'withdrawals': [w.to_dict() for w in withdrawals],
                'pagination': {
                    'total': total_count,
                    'limit': limit,
                    'offset': offset,
                    'hasMore': (offset + limit) < total_count
                }
            }), 200
            
        finally:
            db.close()
    
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"❌ get_user_withdrawals() exception: {str(e)}")
        print(f"❌ Traceback:\n{error_traceback}")
        return jsonify({
            'success': False,
            'error': 'Failed to get withdrawals',
            'debug': str(e)
        }), 500


# ============================================================================
# LEADERBOARD ENDPOINT
# ============================================================================

@products_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """
    🏆 Get earnings leaderboard
    
    GET /api/products/leaderboard?period=week|month&currentUserId=user_xyz
    
    Query params:
    - period: 'week' or 'month' (default: 'week')
    - currentUserId: Show this user's rank (optional)
    - limit: Number of top users to return (default: 50)
    
    Returns: {
        period: 'week',
        entries: [
            {
                rank: 1,
                userId: 'user_abc',
                username: 'John Doe',
                earnings: 1250.50,
                badges: ['top-10', 'first-sale', 'top-referrer']
            }
        ],
        currentUser: {
            rank: 12,
            earnings: 450.25,
            badges: ['first-sale']
        } (only if currentUserId provided)
    }
    
    Badges:
    - 'top-10': In top 10
    - 'top-creator': #1 creator earnings
    - 'top-referrer': #1 referrer earnings
    - 'first-sale': Has at least 1 sale
    - 'high-roller': Earnings > $1000
    """
    try:
        from models import User
        from datetime import timedelta
        
        # Get query parameters
        period = request.args.get('period', 'week').lower()
        current_user_id = request.args.get('currentUserId')
        limit = int(request.args.get('limit', 50))
        
        if period not in ['week', 'month']:
            return jsonify({
                'success': False,
                'error': 'Invalid period. Must be "week" or "month"',
                'field': 'period'
            }), 400
        
        db = SessionLocal()
        
        try:
            # Calculate date range
            now = datetime.utcnow()
            if period == 'week':
                start_date = now - timedelta(days=7)
            else:  # month
                start_date = now - timedelta(days=30)
            
            # Get all users with their earnings in the period
            # Creator earnings: sum of creator_earning from purchases of their products
            creator_earnings_subquery = db.query(
                Purchase.product.has(Product.creator_id),
                func.sum(Purchase.creator_earning).label('creator_total')
            ).filter(
                Purchase.status == 'paid',
                Purchase.purchased_at >= start_date
            ).group_by(Purchase.product.has(Product.creator_id)).subquery()
            
            # Referrer earnings: sum of referrer_earning from purchases they referred
            referrer_earnings_subquery = db.query(
                Purchase.referrer_id,
                func.sum(Purchase.referrer_earning).label('referrer_total')
            ).filter(
                Purchase.status == 'paid',
                Purchase.referrer_id.isnot(None),
                Purchase.purchased_at >= start_date
            ).group_by(Purchase.referrer_id).subquery()
            
            # Build user earnings map
            user_earnings = {}
            user_creator_earnings = {}
            user_referrer_earnings = {}
            
            # Get creator earnings
            for product in db.query(Product).filter(Product.creator_id.isnot(None)).all():
                creator_id = product.creator_id
                earnings = db.query(func.sum(Purchase.creator_earning)).filter(
                    Purchase.product_id == product.id,
                    Purchase.status == 'paid',
                    Purchase.purchased_at >= start_date
                ).scalar() or 0
                
                if earnings > 0:
                    user_earnings[creator_id] = user_earnings.get(creator_id, 0) + earnings
                    user_creator_earnings[creator_id] = user_creator_earnings.get(creator_id, 0) + earnings
            
            # Get referrer earnings
            referrer_data = db.query(
                Purchase.referrer_id,
                func.sum(Purchase.referrer_earning)
            ).filter(
                Purchase.referrer_id.isnot(None),
                Purchase.status == 'paid',
                Purchase.purchased_at >= start_date
            ).group_by(Purchase.referrer_id).all()
            
            for referrer_id, earnings in referrer_data:
                if earnings and earnings > 0:
                    user_earnings[referrer_id] = user_earnings.get(referrer_id, 0) + earnings
                    user_referrer_earnings[referrer_id] = user_referrer_earnings.get(referrer_id, 0) + earnings
            
            # Sort users by total earnings
            sorted_users = sorted(user_earnings.items(), key=lambda x: x[1], reverse=True)
            
            # Find top creator and referrer for badges
            top_creator_id = max(user_creator_earnings.items(), key=lambda x: x[1])[0] if user_creator_earnings else None
            top_referrer_id = max(user_referrer_earnings.items(), key=lambda x: x[1])[0] if user_referrer_earnings else None
            
            # Build leaderboard entries
            entries = []
            current_user_entry = None
            
            for rank, (user_id, earnings) in enumerate(sorted_users[:limit], start=1):
                # Get user details
                user = db.query(User).filter_by(id=user_id).first()
                if not user:
                    continue
                
                # Calculate badges
                badges = []
                
                if rank <= 10:
                    badges.append('top-10')
                
                if user_id == top_creator_id:
                    badges.append('top-creator')
                
                if user_id == top_referrer_id:
                    badges.append('top-referrer')
                
                if earnings >= 1000:
                    badges.append('high-roller')
                
                # Check if has at least one sale
                has_sale = db.query(Purchase).filter(
                    ((Purchase.product.has(creator_id=user_id)) | (Purchase.referrer_id == user_id)),
                    Purchase.status == 'paid',
                    Purchase.purchased_at >= start_date
                ).first() is not None
                
                if has_sale:
                    badges.append('first-sale')
                
                entry = {
                    'rank': rank,
                    'userId': user_id,
                    'username': user.full_name,
                    'earnings': round(earnings, 2),
                    'badges': badges
                }
                
                entries.append(entry)
                
                # Track current user if this is them
                if current_user_id and user_id == current_user_id:
                    current_user_entry = entry
            
            # If current user not in top results, find their rank
            if current_user_id and not current_user_entry:
                for rank, (user_id, earnings) in enumerate(sorted_users, start=1):
                    if user_id == current_user_id:
                        user = db.query(User).filter_by(id=user_id).first()
                        
                        # Calculate badges for current user
                        badges = []
                        if rank <= 10:
                            badges.append('top-10')
                        if user_id == top_creator_id:
                            badges.append('top-creator')
                        if user_id == top_referrer_id:
                            badges.append('top-referrer')
                        if earnings >= 1000:
                            badges.append('high-roller')
                        
                        has_sale = db.query(Purchase).filter(
                            ((Purchase.product.has(creator_id=user_id)) | (Purchase.referrer_id == user_id)),
                            Purchase.status == 'paid',
                            Purchase.purchased_at >= start_date
                        ).first() is not None
                        
                        if has_sale:
                            badges.append('first-sale')
                        
                        current_user_entry = {
                            'rank': rank,
                            'userId': user_id,
                            'username': user.full_name if user else 'Unknown',
                            'earnings': round(earnings, 2),
                            'badges': badges
                        }
                        break
            
            response_data = {
                'success': True,
                'period': period,
                'entries': entries,
                'totalUsers': len(sorted_users)
            }
            
            if current_user_entry:
                response_data['currentUser'] = current_user_entry
            
            return jsonify(response_data), 200
            
        finally:
            db.close()
    
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"❌ get_leaderboard() exception: {str(e)}")
        print(f"❌ Traceback:\n{error_traceback}")
        return jsonify({
            'success': False,
            'error': 'Failed to get leaderboard',
            'debug': str(e)
        }), 500


# ============================================================================
# EXPORT BLUEPRINT
# ============================================================================

def register_products_routes(app):
    """Register product routes with Flask app"""
    app.register_blueprint(products_bp)
    print("✅ Products routes registered at /api/products")
