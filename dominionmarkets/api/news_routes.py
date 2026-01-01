"""
DominionMarkets News Verification API
=====================================
Flask routes for news feed, verification, source management, and bookmarking.

Routes:
- GET/POST /api/news/ - News feed with filtering
- GET /api/news/<id> - Article details with verification
- GET /api/news/<id>/sources - Source comparison view (premium)
- GET /api/news/<id>/verify - Trigger re-verification
- POST /api/news/<id>/bookmark - Bookmark article
- DELETE /api/news/<id>/bookmark - Remove bookmark
- GET /api/news/bookmarks - User's bookmarked articles
- GET /api/news/sources - All news sources
- GET /api/news/sources/<id> - Source details
- POST /api/news/sources/<id>/follow - Follow source
- POST /api/news/sources/<id>/unfollow - Unfollow source
- GET /api/news/preferences - User news preferences
- PATCH /api/news/preferences - Update preferences
- GET /api/news/search - Search articles
- POST /api/news/<id>/sentiment - Generate sentiment analysis (premium)

Last Updated: December 24, 2025
"""

from flask import Blueprint, request, jsonify, session as flask_session
from datetime import datetime, timedelta
from sqlalchemy import or_, and_, desc
from typing import Optional, List
import uuid

from db import SessionLocal
from dominionmarkets.models.news import (
    NewsArticle, NewsSource, VerificationCheck, UserNewsPreference, 
    UserBookmark, VerificationStatus, NewsTier, BiasRating
)
from dominionmarkets.services.verification_service import VerificationService, format_verification_badge
from dominionmarkets.utils.premium import require_premium, get_user_tier

news_bp = Blueprint('news', __name__, url_prefix='/api/news')
verification_service = VerificationService()


# ============================================================================
# NEWS FEED
# ============================================================================

@news_bp.route('/', methods=['GET'])
def get_news_feed():
    """
    Get paginated news feed with optional filters.
    
    Query params:
        - page: Page number (default 1)
        - limit: Items per page (default 20, max 100)
        - category: Filter by category
        - ticker: Filter by ticker symbol
        - min_score: Minimum verification score (default 0)
        - source: Filter by source slug
        - identity: Filter by identity type (diaspora/youth/creator/legacy)
        - sort: Sort by 'published' (default), 'verification', 'bookmarks'
    """
    user_id = flask_session.get('user_id')
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    limit = min(request.args.get('limit', 20, type=int), 100)
    offset = (page - 1) * limit
    
    # Filters
    category = request.args.get('category')
    ticker = request.args.get('ticker', '').upper()
    min_score = request.args.get('min_score', 0, type=int)
    source_slug = request.args.get('source')
    identity = request.args.get('identity')
    sort_by = request.args.get('sort', 'published')
    
    session = SessionLocal()
    try:
        # Base query
        query = session.query(NewsArticle).filter(
            NewsArticle.is_active == True,
            NewsArticle.verification_status == VerificationStatus.VERIFIED
        )
        
        # Apply filters
        if category:
            query = query.filter(NewsArticle.category == category)
        
        if ticker:
            query = query.filter(NewsArticle.ticker_symbols.contains([ticker]))
        
        if min_score:
            query = query.filter(NewsArticle.verification_score >= min_score)
        
        if source_slug:
            source = session.query(NewsSource).filter_by(slug=source_slug).first()
            if source:
                query = query.filter(NewsArticle.sources.contains(source))
        
        if identity:
            identity_filters = {
                'diaspora': NewsArticle.relevant_for_diaspora == True,
                'youth': NewsArticle.relevant_for_youth == True,
                'creator': NewsArticle.relevant_for_creator == True,
                'legacy': NewsArticle.relevant_for_legacy == True
            }
            if identity in identity_filters:
                query = query.filter(identity_filters[identity])
        
        # Sorting
        if sort_by == 'verification':
            query = query.order_by(desc(NewsArticle.verification_score))
        elif sort_by == 'bookmarks':
            query = query.order_by(desc(NewsArticle.bookmark_count))
        else:  # 'published' (default)
            query = query.order_by(desc(NewsArticle.published_at))
        
        # Get total count
        total_count = query.count()
        
        # Get page of results
        articles = query.offset(offset).limit(limit).all()
        
        # Format response
        results = []
        for article in articles:
            article_dict = article.to_dict()
            article_dict['badge'] = format_verification_badge(article.verification_score or 0)
            article_dict['is_bookmarked'] = False
            
            # Check if user has bookmarked (if logged in)
            if user_id:
                bookmark = session.query(UserBookmark).filter_by(
                    user_id=user_id, 
                    article_id=article.id
                ).first()
                article_dict['is_bookmarked'] = bookmark is not None
            
            results.append(article_dict)
        
        return jsonify({
            'articles': results,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total_count,
                'pages': (total_count + limit - 1) // limit
            }
        }), 200
        
    finally:
        session.close()


@news_bp.route('/<string:article_id>', methods=['GET'])
def get_article_detail(article_id: str):
    """
    Get full article details with verification breakdown.
    """
    user_id = flask_session.get('user_id')
    
    session = SessionLocal()
    try:
        article = session.query(NewsArticle).filter_by(
            id=article_id, 
            is_active=True
        ).first()
        
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        
        # Increment view count
        article.view_count += 1
        session.commit()
        
        # Build response
        article_dict = article.to_dict()
        article_dict['badge'] = format_verification_badge(article.verification_score or 0)
        
        # Add sources
        article_dict['sources'] = [
            {
                'id': s.id,
                'name': s.name,
                'tier': s.tier.value if s.tier else None,
                'trust_score': s.trust_score,
                'bias_rating': s.bias_rating.value if s.bias_rating else None
            }
            for s in article.sources
        ]
        
        # Add verification breakdown
        verification_checks = session.query(VerificationCheck).filter_by(
            article_id=article_id
        ).all()
        
        article_dict['verification_breakdown'] = [
            check.to_dict() for check in verification_checks
        ]
        
        # Check bookmark status
        if user_id:
            bookmark = session.query(UserBookmark).filter_by(
                user_id=user_id, 
                article_id=article_id
            ).first()
            article_dict['is_bookmarked'] = bookmark is not None
        else:
            article_dict['is_bookmarked'] = False
        
        # Get related articles (same category or tickers)
        related_query = session.query(NewsArticle).filter(
            NewsArticle.id != article_id,
            NewsArticle.is_active == True,
            NewsArticle.verification_status == VerificationStatus.VERIFIED
        )
        
        if article.category:
            related_query = related_query.filter(NewsArticle.category == article.category)
        
        related_articles = related_query.order_by(
            desc(NewsArticle.published_at)
        ).limit(5).all()
        
        article_dict['related_articles'] = [
            {
                'id': a.id,
                'title': a.title,
                'verification_score': a.verification_score,
                'published_at': a.published_at.isoformat() if a.published_at else None,
                'badge': format_verification_badge(a.verification_score or 0)
            }
            for a in related_articles
        ]
        
        return jsonify(article_dict), 200
        
    finally:
        session.close()


# ============================================================================
# SOURCE COMPARISON (PREMIUM)
# ============================================================================

@news_bp.route('/<string:article_id>/sources', methods=['GET'])
@require_premium
def get_source_comparison(article_id: str):
    """
    Get side-by-side source comparison with conflict highlighting.
    Premium/Pro only.
    """
    session = SessionLocal()
    try:
        article = session.query(NewsArticle).filter_by(id=article_id).first()
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        
        # Get all sources reporting this article
        sources = article.sources
        
        if len(sources) < 2:
            return jsonify({'error': 'Need at least 2 sources for comparison'}), 400
        
        # Get verification checks with conflicts
        conflicts = session.query(VerificationCheck).filter_by(
            article_id=article_id,
            check_type='conflict'
        ).all()
        
        comparison = {
            'article_id': article_id,
            'article_title': article.title,
            'source_count': len(sources),
            'sources': [s.to_dict() for s in sources],
            'conflicts': [c.to_dict() for c in conflicts],
            'conflict_count': len(conflicts)
        }
        
        return jsonify(comparison), 200
        
    finally:
        session.close()


# ============================================================================
# VERIFICATION
# ============================================================================

@news_bp.route('/<string:article_id>/verify', methods=['POST'])
def trigger_verification(article_id: str):
    """
    Manually trigger article re-verification.
    Useful when sources are updated or conflicts resolved.
    """
    session = SessionLocal()
    try:
        article = session.query(NewsArticle).filter_by(id=article_id).first()
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        
        # Get sources
        sources = article.sources
        
        if not sources:
            return jsonify({'error': 'No sources to verify'}), 400
        
        # Calculate new verification score
        score, breakdown = verification_service.calculate_verification_score(article, sources)
        
        # Update article
        article.verification_score = score
        article.verification_status = VerificationStatus.VERIFIED
        article.source_count = len(sources)
        article.agreement_rate = breakdown.get('agreement_rate')
        article.updated_at = datetime.utcnow()
        
        # Create verification records
        verification_service.create_verification_record(
            session, article, 'source_count', 
            passed=breakdown['source_count_score'] >= 15,
            score=breakdown['source_count_score'],
            details={'source_count': len(sources)}
        )
        
        verification_service.create_verification_record(
            session, article, 'agreement',
            passed=breakdown['agreement_score'] >= 25,
            score=breakdown['agreement_score'],
            details={'agreement_rate': breakdown['agreement_rate']}
        )
        
        verification_service.create_verification_record(
            session, article, 'quality',
            passed=breakdown['quality_score'] >= 15,
            score=breakdown['quality_score'],
            details={}
        )
        
        session.commit()
        
        return jsonify({
            'success': True,
            'verification_score': score,
            'breakdown': breakdown,
            'verified_at': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


# ============================================================================
# BOOKMARKS
# ============================================================================

@news_bp.route('/<string:article_id>/bookmark', methods=['POST'])
def bookmark_article(article_id: str):
    """Add article to user's bookmarks"""
    user_id = flask_session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    session = SessionLocal()
    try:
        # Check article exists
        article = session.query(NewsArticle).filter_by(id=article_id).first()
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        
        # Check if already bookmarked
        existing = session.query(UserBookmark).filter_by(
            user_id=user_id,
            article_id=article_id
        ).first()
        
        if existing:
            return jsonify({'error': 'Already bookmarked'}), 400
        
        # Create bookmark
        bookmark = UserBookmark(
            user_id=user_id,
            article_id=article_id,
            notes=request.json.get('notes') if request.json else None
        )
        session.add(bookmark)
        
        # Increment article bookmark count
        article.bookmark_count += 1
        
        session.commit()
        
        return jsonify({
            'success': True,
            'bookmark_id': bookmark.id,
            'bookmarked_at': bookmark.bookmarked_at.isoformat()
        }), 201
        
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@news_bp.route('/<string:article_id>/bookmark', methods=['DELETE'])
def remove_bookmark(article_id: str):
    """Remove article from user's bookmarks"""
    user_id = flask_session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    session = SessionLocal()
    try:
        bookmark = session.query(UserBookmark).filter_by(
            user_id=user_id,
            article_id=article_id
        ).first()
        
        if not bookmark:
            return jsonify({'error': 'Bookmark not found'}), 404
        
        # Decrement article bookmark count
        article = session.query(NewsArticle).filter_by(id=article_id).first()
        if article:
            article.bookmark_count = max(0, article.bookmark_count - 1)
        
        session.delete(bookmark)
        session.commit()
        
        return jsonify({'success': True}), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@news_bp.route('/bookmarks', methods=['GET'])
def get_bookmarks():
    """Get user's bookmarked articles"""
    user_id = flask_session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    page = request.args.get('page', 1, type=int)
    limit = min(request.args.get('limit', 20, type=int), 100)
    offset = (page - 1) * limit
    
    session = SessionLocal()
    try:
        bookmarks_query = session.query(UserBookmark).filter_by(user_id=user_id)
        total_count = bookmarks_query.count()
        
        bookmarks = bookmarks_query.order_by(
            desc(UserBookmark.bookmarked_at)
        ).offset(offset).limit(limit).all()
        
        results = []
        for bookmark in bookmarks:
            article = bookmark.article
            if article and article.is_active:
                article_dict = article.to_dict()
                article_dict['bookmark_notes'] = bookmark.notes
                article_dict['bookmarked_at'] = bookmark.bookmarked_at.isoformat()
                article_dict['badge'] = format_verification_badge(article.verification_score or 0)
                results.append(article_dict)
        
        return jsonify({
            'bookmarks': results,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total_count,
                'pages': (total_count + limit - 1) // limit
            }
        }), 200
        
    finally:
        session.close()


# ============================================================================
# SOURCES
# ============================================================================

@news_bp.route('/sources', methods=['GET'])
def get_sources():
    """Get all news sources with optional filtering"""
    tier = request.args.get('tier')
    following_only = request.args.get('following', 'false').lower() == 'true'
    user_id = flask_session.get('user_id')
    
    session = SessionLocal()
    try:
        query = session.query(NewsSource).filter(NewsSource.is_active == True)
        
        if tier:
            query = query.filter(NewsSource.tier == NewsTier[tier.upper()])
        
        if following_only and user_id:
            # Get sources user is following
            followed_source_ids = session.query(UserNewsPreference.source_id).filter_by(
                user_id=user_id,
                is_following=True
            ).all()
            followed_ids = [s[0] for s in followed_source_ids]
            query = query.filter(NewsSource.id.in_(followed_ids))
        
        sources = query.order_by(desc(NewsSource.trust_score)).all()
        
        # Add following status for logged-in users
        results = []
        for source in sources:
            source_dict = source.to_dict()
            if user_id:
                pref = session.query(UserNewsPreference).filter_by(
                    user_id=user_id,
                    source_id=source.id
                ).first()
                source_dict['is_following'] = pref.is_following if pref else False
            else:
                source_dict['is_following'] = False
            results.append(source_dict)
        
        return jsonify({'sources': results}), 200
        
    finally:
        session.close()


@news_bp.route('/sources/<string:source_id>', methods=['GET'])
def get_source_detail(source_id: str):
    """Get detailed source information"""
    session = SessionLocal()
    try:
        source = session.query(NewsSource).filter_by(id=source_id).first()
        if not source:
            return jsonify({'error': 'Source not found'}), 404
        
        source_dict = source.to_dict()
        
        # Get recent articles from this source
        recent_articles = session.query(NewsArticle).filter(
            NewsArticle.sources.contains(source),
            NewsArticle.is_active == True
        ).order_by(desc(NewsArticle.published_at)).limit(10).all()
        
        source_dict['recent_articles'] = [
            {
                'id': a.id,
                'title': a.title,
                'published_at': a.published_at.isoformat() if a.published_at else None,
                'verification_score': a.verification_score
            }
            for a in recent_articles
        ]
        
        return jsonify(source_dict), 200
        
    finally:
        session.close()


@news_bp.route('/sources/<string:source_id>/follow', methods=['POST'])
def follow_source(source_id: str):
    """Follow a news source"""
    user_id = flask_session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    session = SessionLocal()
    try:
        # Check source exists
        source = session.query(NewsSource).filter_by(id=source_id).first()
        if not source:
            return jsonify({'error': 'Source not found'}), 404
        
        # Get or create preference
        pref = session.query(UserNewsPreference).filter_by(
            user_id=user_id,
            source_id=source_id
        ).first()
        
        if not pref:
            pref = UserNewsPreference(user_id=user_id, source_id=source_id)
            session.add(pref)
        
        pref.is_following = True
        pref.is_blocked = False
        session.commit()
        
        return jsonify({'success': True}), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@news_bp.route('/sources/<string:source_id>/unfollow', methods=['POST'])
def unfollow_source(source_id: str):
    """Unfollow a news source"""
    user_id = flask_session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    session = SessionLocal()
    try:
        pref = session.query(UserNewsPreference).filter_by(
            user_id=user_id,
            source_id=source_id
        ).first()
        
        if pref:
            pref.is_following = False
            session.commit()
        
        return jsonify({'success': True}), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


# ============================================================================
# USER PREFERENCES
# ============================================================================

@news_bp.route('/preferences', methods=['GET'])
def get_preferences():
    """Get user's news preferences"""
    user_id = flask_session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    session = SessionLocal()
    try:
        # Get all preferences for this user
        prefs = session.query(UserNewsPreference).filter_by(user_id=user_id).all()
        
        # Aggregate preferences
        result = {
            'user_id': user_id,
            'following_sources': [p.source_id for p in prefs if p.is_following],
            'blocked_sources': [p.source_id for p in prefs if p.is_blocked],
            'preferred_categories': prefs[0].preferred_categories if prefs else [],
            'watched_tickers': prefs[0].watched_tickers if prefs else [],
            'identity_type': prefs[0].identity_type if prefs else None,
            'min_verification_score': prefs[0].min_verification_score if prefs else 60
        }
        
        return jsonify(result), 200
        
    finally:
        session.close()


@news_bp.route('/preferences', methods=['PATCH'])
def update_preferences():
    """Update user's news preferences"""
    user_id = flask_session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    
    session = SessionLocal()
    try:
        # Get or create preference record
        pref = session.query(UserNewsPreference).filter_by(user_id=user_id).first()
        
        if not pref:
            pref = UserNewsPreference(user_id=user_id)
            session.add(pref)
        
        # Update fields
        if 'preferred_categories' in data:
            pref.preferred_categories = data['preferred_categories']
        if 'watched_tickers' in data:
            pref.watched_tickers = data['watched_tickers']
        if 'identity_type' in data:
            pref.identity_type = data['identity_type']
        if 'min_verification_score' in data:
            pref.min_verification_score = data['min_verification_score']
        if 'email_alerts_enabled' in data:
            pref.email_alerts_enabled = data['email_alerts_enabled']
        
        pref.updated_at = datetime.utcnow()
        session.commit()
        
        return jsonify({'success': True}), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


# ============================================================================
# SEARCH
# ============================================================================

@news_bp.route('/search', methods=['GET'])
def search_articles():
    """
    Search articles by title, content, or ticker.
    """
    query_text = request.args.get('q', '').strip()
    
    if not query_text:
        return jsonify({'error': 'Query parameter required'}), 400
    
    page = request.args.get('page', 1, type=int)
    limit = min(request.args.get('limit', 20, type=int), 100)
    offset = (page - 1) * limit
    
    session = SessionLocal()
    try:
        # Search in title and summary
        query = session.query(NewsArticle).filter(
            NewsArticle.is_active == True,
            or_(
                NewsArticle.title.ilike(f'%{query_text}%'),
                NewsArticle.summary.ilike(f'%{query_text}%')
            )
        )
        
        total_count = query.count()
        articles = query.order_by(desc(NewsArticle.published_at)).offset(offset).limit(limit).all()
        
        results = [
            {
                **article.to_dict(),
                'badge': format_verification_badge(article.verification_score or 0)
            }
            for article in articles
        ]
        
        return jsonify({
            'results': results,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total_count,
                'pages': (total_count + limit - 1) // limit
            }
        }), 200
        
    finally:
        session.close()
