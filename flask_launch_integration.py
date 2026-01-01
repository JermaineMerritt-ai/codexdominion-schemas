"""
Flask Dashboard Integration for Launch Social Content
======================================================

Add these routes to flask_dashboard.py to integrate launch social content.

Location: Add near other API routes in flask_dashboard.py
"""

from launch_social_integration import LaunchSocialManager
from flask import jsonify, request

# Initialize the manager (add near top of file with other initializations)
launch_social_manager = LaunchSocialManager()


# ============================================================================
# LAUNCH SOCIAL CONTENT ROUTES
# ============================================================================

@app.route('/api/launch-posts')
def api_launch_posts():
    """
    Get all launch posts organized by category
    
    Returns:
        JSON: All 50 posts grouped by category
    
    Example:
        GET /api/launch-posts
    """
    return jsonify(launch_social_manager.get_all_posts())


@app.route('/api/launch-posts/category/<category>')
def api_launch_posts_by_category(category):
    """
    Get posts for a specific category
    
    Args:
        category: hero, creator, youth, diaspora, brand, marketplace, hype
    
    Returns:
        JSON: List of posts in that category
    
    Example:
        GET /api/launch-posts/category/hero
    """
    posts = launch_social_manager.get_posts_by_category(category)
    if not posts:
        return jsonify({"error": f"Category '{category}' not found"}), 404
    return jsonify(posts)


@app.route('/api/launch-posts/priority/<priority>')
def api_launch_posts_by_priority(priority):
    """
    Get posts by priority level
    
    Args:
        priority: critical, high, medium, low
    
    Returns:
        JSON: List of posts matching priority
    
    Example:
        GET /api/launch-posts/priority/critical
    """
    posts = launch_social_manager.get_posts_by_priority(priority)
    if not posts:
        return jsonify({"error": f"No posts found with priority '{priority}'"}), 404
    return jsonify(posts)


@app.route('/api/launch-posts/audience/<audience>')
def api_launch_posts_by_audience(audience):
    """
    Get posts targeting specific audience
    
    Args:
        audience: creators, youth, diaspora
    
    Returns:
        JSON: List of posts for that audience
    
    Example:
        GET /api/launch-posts/audience/creators
    """
    posts = launch_social_manager.get_posts_by_audience(audience)
    if not posts:
        return jsonify({"error": f"No posts found for audience '{audience}'"}), 404
    return jsonify(posts)


@app.route('/api/launch-posts/id/<int:post_id>')
def api_launch_post_by_id(post_id):
    """
    Get a specific post by ID
    
    Args:
        post_id: Post ID (1-50)
    
    Returns:
        JSON: Single post object
    
    Example:
        GET /api/launch-posts/id/1
    """
    post = launch_social_manager.get_post_by_id(post_id)
    if not post:
        return jsonify({"error": f"Post #{post_id} not found"}), 404
    return jsonify(post)


@app.route('/api/launch-posts/schedule/launch-day')
def api_launch_day_schedule():
    """
    Get launch day posting schedule organized by waves
    
    Returns:
        JSON: Posts grouped by wave (wave_1, wave_2, wave_3)
    
    Example:
        GET /api/launch-posts/schedule/launch-day
    """
    waves = launch_social_manager.get_launch_day_posts()
    return jsonify(waves)


@app.route('/api/launch-posts/schedule/week/<int:week>')
def api_week_schedule(week):
    """
    Get posting schedule for a specific week
    
    Args:
        week: Week number (1, 2, or 3+)
    
    Returns:
        JSON: Posts grouped by focus area
    
    Example:
        GET /api/launch-posts/schedule/week/1
    """
    if week < 1:
        return jsonify({"error": "Week must be 1 or greater"}), 400
    
    week_posts = launch_social_manager.get_week_posts(week)
    if not week_posts:
        return jsonify({"error": f"No schedule found for week {week}"}), 404
    return jsonify(week_posts)


@app.route('/api/launch-posts/format', methods=['POST'])
def api_format_post():
    """
    Format a post for a specific platform
    
    Request Body:
        {
            "post_id": 1,
            "platform": "instagram"
        }
    
    Returns:
        JSON: Formatted post text
    
    Example:
        POST /api/launch-posts/format
        Body: {"post_id": 1, "platform": "instagram"}
    """
    data = request.get_json()
    
    if not data or 'post_id' not in data or 'platform' not in data:
        return jsonify({"error": "post_id and platform required"}), 400
    
    post = launch_social_manager.get_post_by_id(data['post_id'])
    if not post:
        return jsonify({"error": f"Post #{data['post_id']} not found"}), 404
    
    formatted = launch_social_manager.format_for_platform(post, data['platform'])
    return jsonify({
        "post_id": data['post_id'],
        "platform": data['platform'],
        "formatted_text": formatted
    })


@app.route('/api/launch-posts/stats')
def api_launch_posts_stats():
    """
    Get statistics about launch content
    
    Returns:
        JSON: Stats including total posts, categories, priorities
    
    Example:
        GET /api/launch-posts/stats
    """
    stats = launch_social_manager.get_stats()
    return jsonify(stats)


# ============================================================================
# LAUNCH DASHBOARD PAGE (Optional - HTML UI)
# ============================================================================

@app.route('/launch')
def launch_dashboard():
    """
    Launch content management dashboard
    
    Displays all launch content with filtering and copy functionality
    """
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>CodexDominion Launch Dashboard</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                background: #0F172A;
                color: #E2E8F0;
                margin: 0;
                padding: 20px;
            }
            .header {
                background: linear-gradient(135deg, #F5C542 0%, #FFA500 100%);
                color: #0F172A;
                padding: 30px;
                border-radius: 12px;
                margin-bottom: 30px;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat-card {
                background: #1E293B;
                padding: 20px;
                border-radius: 8px;
                border: 1px solid #334155;
            }
            .stat-number {
                font-size: 2em;
                font-weight: bold;
                color: #F5C542;
            }
            .filters {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
                flex-wrap: wrap;
            }
            .filter-btn {
                padding: 10px 20px;
                background: #334155;
                border: 1px solid #475569;
                border-radius: 6px;
                color: #E2E8F0;
                cursor: pointer;
                transition: all 0.2s;
            }
            .filter-btn:hover {
                background: #475569;
            }
            .filter-btn.active {
                background: #F5C542;
                color: #0F172A;
                border-color: #F5C542;
            }
            .post-card {
                background: #1E293B;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 15px;
            }
            .post-id {
                display: inline-block;
                background: #F5C542;
                color: #0F172A;
                padding: 4px 12px;
                border-radius: 4px;
                font-weight: bold;
                margin-right: 10px;
            }
            .post-category {
                display: inline-block;
                background: #334155;
                padding: 4px 12px;
                border-radius: 4px;
                font-size: 0.9em;
                margin-right: 10px;
            }
            .post-priority {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 4px;
                font-size: 0.9em;
            }
            .priority-critical { background: #DC2626; }
            .priority-high { background: #EF4444; }
            .priority-medium { background: #F59E0B; }
            .priority-low { background: #10B981; }
            .post-text {
                margin: 15px 0;
                line-height: 1.6;
                white-space: pre-wrap;
            }
            .post-hashtags {
                color: #60A5FA;
                font-size: 0.9em;
            }
            .copy-btn {
                background: #10B981;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                cursor: pointer;
                margin-right: 10px;
            }
            .copy-btn:hover {
                background: #059669;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🔥 CodexDominion Launch Dashboard</h1>
            <p>50 Social Posts | Launch Day Operations</p>
        </div>
        
        <div class="stats" id="stats"></div>
        
        <div class="filters">
            <button class="filter-btn active" onclick="filterPosts('all')">All Posts</button>
            <button class="filter-btn" onclick="filterPosts('critical')">Critical</button>
            <button class="filter-btn" onclick="filterPosts('high')">High Priority</button>
            <button class="filter-btn" onclick="filterPosts('hero')">Hero</button>
            <button class="filter-btn" onclick="filterPosts('creator')">Creators</button>
            <button class="filter-btn" onclick="filterPosts('youth')">Youth</button>
            <button class="filter-btn" onclick="filterPosts('diaspora')">Diaspora</button>
            <button class="filter-btn" onclick="filterPosts('hype')">Hype</button>
        </div>
        
        <div id="posts"></div>
        
        <script>
            let allPosts = [];
            let currentFilter = 'all';
            
            // Load stats
            fetch('/api/launch-posts/stats')
                .then(r => r.json())
                .then(stats => {
                    document.getElementById('stats').innerHTML = `
                        <div class="stat-card">
                            <div class="stat-number">${stats.total_posts}</div>
                            <div>Total Posts</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">${stats.critical_posts}</div>
                            <div>Critical</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">${stats.high_priority_posts}</div>
                            <div>High Priority</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">${stats.categories.length}</div>
                            <div>Categories</div>
                        </div>
                    `;
                });
            
            // Load all posts
            fetch('/api/launch-posts')
                .then(r => r.json())
                .then(data => {
                    // Flatten categories into single array
                    for (const [category, posts] of Object.entries(data)) {
                        posts.forEach(post => {
                            post.category = category;
                            allPosts.push(post);
                        });
                    }
                    renderPosts();
                });
            
            function filterPosts(filter) {
                currentFilter = filter;
                document.querySelectorAll('.filter-btn').forEach(btn => {
                    btn.classList.remove('active');
                });
                event.target.classList.add('active');
                renderPosts();
            }
            
            function renderPosts() {
                let filtered = allPosts;
                
                if (currentFilter !== 'all') {
                    if (['critical', 'high', 'medium', 'low'].includes(currentFilter)) {
                        filtered = allPosts.filter(p => p.priority === currentFilter);
                    } else {
                        filtered = allPosts.filter(p => p.category === currentFilter);
                    }
                }
                
                const html = filtered.map(post => `
                    <div class="post-card">
                        <div>
                            <span class="post-id">#${post.id}</span>
                            <span class="post-category">${post.category}</span>
                            <span class="post-priority priority-${post.priority}">${post.priority}</span>
                        </div>
                        <div class="post-text">${post.text}</div>
                        <div class="post-hashtags">${post.hashtags ? post.hashtags.join(' ') : ''}</div>
                        <div style="margin-top: 15px;">
                            <button class="copy-btn" onclick="copyPost(${post.id})">📋 Copy</button>
                            ${post.audience ? `<span style="color: #94A3B8;">Target: ${post.audience}</span>` : ''}
                        </div>
                    </div>
                `).join('');
                
                document.getElementById('posts').innerHTML = html;
            }
            
            function copyPost(id) {
                const post = allPosts.find(p => p.id === id);
                const text = post.text + '\\n\\n' + (post.hashtags ? post.hashtags.join(' ') : '');
                navigator.clipboard.writeText(text).then(() => {
                    alert('✅ Post copied to clipboard!');
                });
            }
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("✅ Flask routes ready for integration")
    print("\nAdd these routes to flask_dashboard.py:")
    print("  /api/launch-posts")
    print("  /api/launch-posts/category/<category>")
    print("  /api/launch-posts/priority/<priority>")
    print("  /api/launch-posts/stats")
    print("  /launch (dashboard page)")
