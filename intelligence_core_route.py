# Add this route to flask_dashboard.py before the "if __name__ == '__main__':" line

@app.route('/intelligence-core')
def intelligence_core_view():
    """Intelligence Core dashboard with 12 engines"""
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>🧠 Intelligence Core - 12 Engines</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1600px; margin: 0 auto; }
        .back {
            display: inline-block;
            padding: 12px 24px;
            background: rgba(255,255,255,0.1);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            transition: all 0.3s;
        }
        .back:hover { background: rgba(255,255,255,0.2); transform: translateX(-5px); }
        .header {
            text-align: center;
            margin-bottom: 50px;
            background: rgba(255,255,255,0.1);
            padding: 40px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        .header h1 { font-size: 3em; margin-bottom: 15px; color: #ffd700; text-shadow: 0 0 20px rgba(255,215,0,0.5); }
        .header p { font-size: 1.3em; opacity: 0.9; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .stat-card {
            background: rgba(255,255,255,0.1);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        .stat-card h3 { font-size: 2.5em; color: #ffd700; margin-bottom: 10px; }
        .stat-card p { opacity: 0.8; }
        .status-filter {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        .filter-btn {
            padding: 10px 25px;
            background: rgba(255,255,255,0.1);
            border: 2px solid rgba(255,255,255,0.3);
            color: white;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s;
            backdrop-filter: blur(10px);
            font-size: 0.95em;
        }
        .filter-btn:hover, .filter-btn.active {
            background: rgba(255,215,0,0.3);
            border-color: #ffd700;
            transform: translateY(-3px);
        }
        .engines-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }
        .engine-card {
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            transition: all 0.3s;
            border-left: 5px solid #ffd700;
        }
        .engine-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
            border-left-width: 8px;
        }
        .engine-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }
        .engine-name { font-size: 1.5em; color: #ffd700; font-weight: bold; }
        .engine-status { padding: 5px 15px; border-radius: 20px; font-size: 0.8em; font-weight: bold; white-space: nowrap; }
        .status-active { background: #4CAF50; }
        .status-in_progress { background: #FFA726; }
        .status-planned { background: #42A5F5; }
        .engine-role { font-style: italic; color: #ffd700; margin-bottom: 10px; opacity: 0.9; font-size: 0.95em; }
        .engine-description { line-height: 1.6; margin-bottom: 15px; opacity: 0.9; }
        .lifecycle { display: inline-block; padding: 5px 12px; background: rgba(255,215,0,0.2); border-radius: 15px; font-size: 0.85em; margin-bottom: 15px; }
        .capabilities, .capsules { margin: 15px 0; }
        .section-title { font-size: 0.9em; color: #ffd700; margin-bottom: 8px; font-weight: bold; text-transform: uppercase; }
        .tag {
            display: inline-block;
            padding: 4px 10px;
            background: rgba(255,255,255,0.15);
            border-radius: 12px;
            font-size: 0.85em;
            margin: 3px;
        }
        .overlays { margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.2); }
        .overlay-item {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            margin: 5px;
            padding: 5px 12px;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            font-size: 0.85em;
        }
        .overlay-enabled { background: rgba(76, 175, 80, 0.3); }
        .overlay-disabled { background: rgba(239, 83, 80, 0.3); opacity: 0.6; }
        .loading { text-align: center; padding: 100px 20px; font-size: 1.5em; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        <div class="header">
            <h1>🧠 Intelligence Core</h1>
            <p>12 Advanced Intelligence Engines - The Mind of CodexDominion</p>
        </div>
        <div id="stats" class="stats"></div>
        <div class="status-filter">
            <button class="filter-btn active" onclick="filterByStatus('all')">All Engines</button>
            <button class="filter-btn" onclick="filterByStatus('active')">Active</button>
            <button class="filter-btn" onclick="filterByStatus('in_progress')">In Progress</button>
            <button class="filter-btn" onclick="filterByStatus('planned')">Planned</button>
        </div>
        <div id="engines" class="engines-grid">
            <div class="loading">Loading Intelligence Core...</div>
        </div>
    </div>
    <script>
        let engines = [];
        let currentFilter = 'all';
        
        async function loadEngines() {
            try {
                const response = await fetch('/api/intelligence-core');
                if (!response.ok) throw new Error('Failed to load engines');
                engines = await response.json();
                displayStats();
                displayEngines();
            } catch (error) {
                document.getElementById('engines').innerHTML = '<div class="loading">⚠️ Error: ' + error.message + '</div>';
            }
        }
        
        function displayStats() {
            const stats = {
                total: engines.length,
                active: engines.filter(e => e.status === 'active').length,
                in_progress: engines.filter(e => e.status === 'in_progress').length,
                planned: engines.filter(e => e.status === 'planned').length
            };
            
            document.getElementById('stats').innerHTML = `
                <div class="stat-card"><h3>${stats.total}</h3><p>Total Engines</p></div>
                <div class="stat-card"><h3>${stats.active}</h3><p>Active</p></div>
                <div class="stat-card"><h3>${stats.in_progress}</h3><p>In Progress</p></div>
                <div class="stat-card"><h3>${stats.planned}</h3><p>Planned</p></div>
            `;
        }
        
        function displayEngines() {
            const filtered = currentFilter === 'all' 
                ? engines 
                : engines.filter(e => e.status === currentFilter);
                
            if (filtered.length === 0) {
                document.getElementById('engines').innerHTML = '<div class="loading">No engines found for this filter</div>';
                return;
            }
            
            const html = filtered.map(engine => `
                <div class="engine-card">
                    <div class="engine-header">
                        <div class="engine-name">${engine.name}</div>
                        <div class="engine-status status-${engine.status}">${engine.status.replace('_', ' ').toUpperCase()}</div>
                    </div>
                    <div class="engine-role">"${engine.role}"</div>
                    <div class="lifecycle">Lifecycle: ${engine.lifecycle.toUpperCase()}</div>
                    <div class="engine-description">${engine.description}</div>
                    <div class="capabilities">
                        <div class="section-title">Capabilities</div>
                        ${engine.capabilities.map(c => `<span class="tag">${c.replace(/_/g, ' ')}</span>`).join('')}
                    </div>
                    <div class="capsules">
                        <div class="section-title">Primary Capsules</div>
                        ${engine.primary_capsules.map(c => `<span class="tag">${c}</span>`).join('')}
                    </div>
                    <div class="overlays">
                        <div class="section-title">Overlays</div>
                        <span class="overlay-item ${engine.overlays.stewardship ? 'overlay-enabled' : 'overlay-disabled'}">
                            ${engine.overlays.stewardship ? '✓' : '✗'} Stewardship
                        </span>
                        <span class="overlay-item ${engine.overlays.wellbeing ? 'overlay-enabled' : 'overlay-disabled'}">
                            ${engine.overlays.wellbeing ? '✓' : '✗'} Wellbeing
                        </span>
                        <span class="overlay-item ${engine.overlays.planetary ? 'overlay-enabled' : 'overlay-disabled'}">
                            ${engine.overlays.planetary ? '✓' : '✗'} Planetary
                        </span>
                        <span class="overlay-item ${engine.overlays.intergenerational ? 'overlay-enabled' : 'overlay-disabled'}">
                            ${engine.overlays.intergenerational ? '✓' : '✗'} Intergenerational
                        </span>
                    </div>
                </div>
            `).join('');
            
            document.getElementById('engines').innerHTML = html;
        }
        
        function filterByStatus(status) {
            currentFilter = status;
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            displayEngines();
        }
        
        // Load on page ready
        loadEngines();
    </script>
</body>
</html>
    """
    return html
