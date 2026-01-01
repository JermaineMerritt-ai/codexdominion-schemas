"""
🔥 CREATIVE AGENTS DASHBOARD TEMPLATE 🔥
==========================================
HTML template for displaying the first generation of creative agents
"""

CREATIVE_AGENTS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🔥 Creative Agents - Genesis Protocol - Codex Dominion</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #F5C542 0%, #f0b429 50%, #e89d16 100%);
            padding: 20px;
            color: #0F172A;
        }
        .container { 
            max-width: 1600px; 
            margin: 0 auto; 
            background: white; 
            padding: 40px; 
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        .back { 
            display: inline-block; 
            padding: 12px 24px; 
            background: #0F172A; 
            color: #F5C542; 
            text-decoration: none; 
            border-radius: 8px; 
            margin-bottom: 20px;
            font-weight: bold;
        }
        .back:hover { background: #1E293B; }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 20px;
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            border-radius: 15px;
            color: white;
        }
        .header h1 { 
            color: #F5C542; 
            font-size: 2.5em;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .header .subtitle {
            color: #F5C542;
            font-size: 1.2em;
            margin-top: 10px;
            opacity: 0.9;
        }
        .header .stats {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 20px;
        }
        .stat-box {
            text-align: center;
        }
        .stat-box .number {
            font-size: 2em;
            color: #F5C542;
            font-weight: bold;
        }
        .stat-box .label {
            color: #94a3b8;
            font-size: 0.9em;
        }
        
        .agents-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }
        
        .agent-card {
            padding: 25px;
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border-radius: 15px;
            border-left: 5px solid #F5C542;
            transition: all 0.3s ease;
            position: relative;
        }
        .agent-card:hover { 
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }
        
        .agent-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .agent-icon {
            font-size: 2.5em;
            margin-right: 15px;
        }
        .agent-title {
            display: flex;
            align-items: center;
            flex: 1;
        }
        .agent-title h2 { 
            color: #0F172A; 
            margin: 0;
            font-size: 1.5em;
        }
        .agent-status {
            display: inline-block;
            padding: 6px 16px;
            background: #10B981;
            color: white;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
        }
        
        .agent-domain {
            background: #0F172A;
            color: #F5C542;
            padding: 8px 16px;
            border-radius: 8px;
            margin: 10px 0;
            font-weight: bold;
            font-size: 0.9em;
        }
        
        .agent-description {
            color: #475569;
            line-height: 1.6;
            margin: 15px 0;
        }
        
        .agent-functions {
            margin-top: 15px;
            padding: 15px;
            background: white;
            border-radius: 10px;
        }
        .agent-functions h4 {
            color: #0F172A;
            margin: 0 0 10px 0;
            font-size: 1em;
        }
        .function-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        .function-list li {
            padding: 6px 0;
            color: #475569;
            display: flex;
            align-items: center;
        }
        .function-list li:before {
            content: "⚡";
            margin-right: 10px;
            color: #F5C542;
        }
        
        .agent-metadata {
            display: flex;
            gap: 20px;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #cbd5e1;
            font-size: 0.9em;
        }
        .metadata-item {
            display: flex;
            align-items: center;
            gap: 5px;
            color: #64748b;
        }
        .metadata-item strong {
            color: #0F172A;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            padding: 30px;
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            border-radius: 15px;
            color: white;
        }
        .footer h3 {
            color: #F5C542;
            margin-bottom: 15px;
        }
        .footer ul {
            list-style: none;
            padding: 0;
            color: #94a3b8;
        }
        .footer ul li {
            padding: 5px 0;
        }
        .footer .flame {
            font-size: 2em;
            color: #F5C542;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        
        <div class="header">
            <h1>🔥 AGENT GENESIS PROTOCOL 🔥</h1>
            <div class="subtitle">First Generation Creative Intelligence</div>
            <div class="stats">
                <div class="stat-box">
                    <div class="number" id="agent-count">9</div>
                    <div class="label">Active Agents</div>
                </div>
                <div class="stat-box">
                    <div class="number">100%</div>
                    <div class="label">Trust Score</div>
                </div>
                <div class="stat-box">
                    <div class="number">Gen 1</div>
                    <div class="label">Generation</div>
                </div>
            </div>
        </div>
        
        <div id="agents-container" class="agents-grid">
            <!-- Agents will be loaded via API -->
        </div>
        
        <div class="footer">
            <h3>🎯 The Future of Creative Intelligence</h3>
            <p style="color: #94a3b8; margin-bottom: 20px;">
                These agents will eventually:
            </p>
            <ul>
                <li>• Debate creative decisions</li>
                <li>• Vote on workflow directions</li>
                <li>• Collaborate across domains</li>
                <li>• Challenge each other's outputs</li>
                <li>• Improve each other's capabilities</li>
                <li>• Maintain quality standards</li>
                <li>• Evolve the creative system</li>
            </ul>
            <div class="flame">🔥 The Flame Burns Sovereign and Eternal! 👑</div>
        </div>
    </div>
    
    <script>
        // Load creative agents from API
        fetch('/api/agents/creative')
            .then(response => response.json())
            .then(data => {
                const container = document.getElementById('agents-container');
                document.getElementById('agent-count').textContent = data.agents.length;
                
                data.agents.forEach(agent => {
                    const card = createAgentCard(agent);
                    container.appendChild(card);
                });
            })
            .catch(error => {
                console.error('Error loading agents:', error);
                document.getElementById('agents-container').innerHTML = 
                    '<p style="color: red;">Error loading agents. Please refresh the page.</p>';
            });
        
        function createAgentCard(agent) {
            const card = document.createElement('div');
            card.className = 'agent-card';
            
            const icon = agent.display_name.split(' ')[0]; // Extract emoji
            const name = agent.display_name.substring(icon.length).trim();
            
            const capabilities = agent.capabilities || {};
            const functions = capabilities.primary_functions || [];
            const domain = capabilities.domain || 'Unknown';
            const role = capabilities.role || 'Unknown';
            
            card.innerHTML = `
                <div class="agent-header">
                    <div class="agent-title">
                        <span class="agent-icon">${icon}</span>
                        <h2>${name}</h2>
                    </div>
                    <span class="agent-status">✅ ACTIVE</span>
                </div>
                
                <div class="agent-domain">
                    <strong>Domain:</strong> ${domain}
                </div>
                
                <div class="agent-description">
                    ${agent.description}
                </div>
                
                <div class="agent-functions">
                    <h4>🎯 Primary Functions:</h4>
                    <ul class="function-list">
                        ${functions.map(f => `<li>${f}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="agent-metadata">
                    <div class="metadata-item">
                        <strong>Role:</strong> ${role}
                    </div>
                    <div class="metadata-item">
                        <strong>Trust:</strong> ${agent.reputation ? agent.reputation.trust_score.toFixed(1) : '100.0'}
                    </div>
                    <div class="metadata-item">
                        <strong>Actions:</strong> ${agent.reputation ? agent.reputation.total_actions : 0}
                    </div>
                </div>
            `;
            
            return card;
        }
    </script>
</body>
</html>
"""
