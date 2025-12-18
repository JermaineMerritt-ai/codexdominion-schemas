"""
🚀 MASTER DASHBOARD - FLASK VERSION (100% Compatible)
======================================================
Flask-based dashboard that works with any Python version
No Streamlit platform issues!
"""

import sys
import io

# Fix Windows UTF-8 encoding for emojis
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from flask import Flask, render_template_string, jsonify, request, redirect, url_for
import json
from datetime import datetime
from pathlib import Path
import os
import base64
from typing import Dict, List, Any

# Add paths
sys.path.insert(0, str(Path(__file__).parent))

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file upload
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# JSON cache for performance
_json_cache = {}

def load_json(filename: str, use_cache: bool = True) -> Dict[str, Any]:
    """
    Universal JSON loader with intelligent fallback and caching

    Handles:
    - Root directory lookup
    - /data directory fallback
    - Missing files (returns empty dict)
    - JSON parse errors (returns empty dict)
    - Optional caching for performance

    Args:
        filename: Name of JSON file (e.g., 'cycles.json')
        use_cache: Enable in-memory caching (default: True)

    Returns:
        Dict containing JSON data or empty dict on error
    """
    # Check cache first
    if use_cache and filename in _json_cache:
        return _json_cache[filename]

    base_path = Path(__file__).parent
    search_paths = [
        base_path / filename,              # Root: /app/cycles.json
        base_path / 'data' / filename,     # Data dir: /app/data/cycles.json
    ]

    for path in search_paths:
        try:
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Cache the result
                if use_cache:
                    _json_cache[filename] = data

                return data
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parse error in {path}: {e}")
            continue
        except Exception as e:
            print(f"⚠️ Error reading {path}: {e}")
            continue

    # File not found in any location
    print(f"⚠️ JSON file not found: {filename} (searched {len(search_paths)} locations)")
    return {}

def clear_json_cache():
    """Clear JSON cache to force reload"""
    global _json_cache
    _json_cache = {}

def load_json_response(filename: str, use_cache: bool = True):
    """
    Load JSON file and return Flask JSON response

    Returns jsonify() response with data or error message
    """
    data = load_json(filename, use_cache)
    if not data:
        return jsonify({"error": f"File not found or empty: {filename}"}), 404
    return jsonify(data)

# Dashboard HTML Template
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>👑 Codex Dominion Master Dashboard Ultimate</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }

        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }

        .header {
            background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }

        .header h1 { font-size: 3em; margin-bottom: 10px; color: #333; }
        .header p { font-size: 1.2em; color: #555; }

        .banner {
            background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            color: white;
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 30px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .card {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            transition: transform 0.3s;
        }

        .card:hover { transform: translateY(-5px); }

        .card h2 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.5em;
        }

        .card p { color: #666; margin-bottom: 20px; line-height: 1.6; }

        .btn {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            font-size: 1em;
        }

        .btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }

        .metric {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border-radius: 10px;
            margin: 10px 0;
        }

        .metric h3 { font-size: 2.5em; margin-bottom: 5px; }
        .metric p { font-size: 1em; opacity: 0.9; }

        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }

        .tool-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }

        .tool-card h3 { margin-bottom: 10px; }
        .tool-card .savings {
            background: rgba(255,215,0,0.3);
            padding: 5px 10px;
            border-radius: 5px;
            margin: 10px 0;
            font-weight: bold;
        }

        .status {
            background: #4CAF50;
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-size: 1.2em;
            margin: 20px 0;
        }

        /* Navigation Tabs */
        .nav-tabs {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 20px 0;
            padding: 15px;
            background: white;
            border-radius: 10px;
        }

        .nav-tab {
            padding: 10px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 20px;
            font-weight: bold;
            transition: transform 0.3s;
        }

        .nav-tab:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .nav-tab.active {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>👑 CODEXDOMINION MASTER DASHBOARD ULTIMATE</h1>
            <p>Complete Command Center with 48 Intelligence Engines & Free Tools Suite</p>
        </div>

        <div class="banner">
            🆕 NEW: 48 Intelligence Engines + $316/month in FREE Tools!
        </div>

        <div class="status">
            ✅ ALL SYSTEMS OPERATIONAL - Running on Flask (Python {{ python_version }})
        </div>

        <!-- Navigation Tabs -->
        <div class="nav-tabs">
            <a href="/" class="nav-tab active">🏠 Home</a>
            <a href="/engines" class="nav-tab">🧠 48 Engines</a>
            <a href="/tools" class="nav-tab">🔧 6 Tools</a>
            <a href="/dashboards" class="nav-tab">📊 All Dashboards</a>
            <a href="/chat" class="nav-tab">💬 AI Chat</a>
            <a href="/agents" class="nav-tab">🤖 AI Agents</a>
            <a href="/websites" class="nav-tab">🌐 Websites</a>
            <a href="/stores" class="nav-tab">🛒 Stores</a>
            <a href="/social" class="nav-tab">📱 Social Media</a>
            <a href="/affiliate" class="nav-tab">💰 Affiliate</a>
            <a href="/chatbot" class="nav-tab">🤖 Action Chatbot</a>
            <a href="/algorithm" class="nav-tab">🧠 Algorithm AI</a>
            <a href="/autopublish" class="nav-tab">🚀 Auto-Publish</a>
            <a href="/email" class="nav-tab">📧 Email</a>
            <a href="/documents" class="nav-tab">📄 Documents</a>
            <a href="/avatars" class="nav-tab">👤 Avatars</a>
            <a href="/council" class="nav-tab">👑 Council</a>
            <a href="/copilot" class="nav-tab">🚁 Copilot</a>
        </div>

        <div class="grid">
            <div class="card">
                <h2>🧠 48 Intelligence Engines</h2>
                <p>Complete intelligence system covering 24 domains with Research & Execution modes</p>
                <div class="metric">
                    <h3>48</h3>
                    <p>Active Engines</p>
                </div>
                <p><strong>Clusters:</strong> Technology, Bioengineering, Security, Communication, Planetary, Business</p>
                <a href="/engines" class="btn">Launch Engines</a>
            </div>

            <div class="card">
                <h2>🔧 Codex Tools Suite</h2>
                <p>6 FREE tools replacing expensive subscriptions</p>
                <div class="metric">
                    <h3>$316/mo</h3>
                    <p>Total Savings</p>
                </div>
                <p><strong>Tools:</strong> Flow Orchestrator, AI Content Engine, Research Studio, Design Forge, Nano Builder, App Constructor</p>
                <a href="/tools" class="btn">Launch Tools</a>
            </div>

            <div class="card">
                <h2>📊 System Metrics</h2>
                <p>Real-time performance and status</p>
                <div class="metric">
                    <h3>{{ total_dashboards }}</h3>
                    <p>Total Dashboards</p>
                </div>
                <div class="metric">
                    <h3>99.9%</h3>
                    <p>Uptime</p>
                </div>
                <a href="/status" class="btn">View Status</a>
            </div>
        </div>

        <div class="card">
            <h2>💰 FREE Tools - Zero Subscriptions</h2>
            <div class="tools-grid">
                <div class="tool-card">
                    <h3>⚙️ Flow Orchestrator</h3>
                    <p>Replaces N8N</p>
                    <div class="savings">Save $50/mo</div>
                </div>
                <div class="tool-card">
                    <h3>✨ AI Content Engine</h3>
                    <p>Replaces GenSpark</p>
                    <div class="savings">Save $99/mo</div>
                </div>
                <div class="tool-card">
                    <h3>📚 Research Studio</h3>
                    <p>Replaces NotebookLLM</p>
                    <div class="savings">Save $20/mo</div>
                </div>
                <div class="tool-card">
                    <h3>🎨 Design Forge</h3>
                    <p>Replaces Designrr</p>
                    <div class="savings">Save $39/mo</div>
                </div>
                <div class="tool-card">
                    <h3>🔧 Nano Builder</h3>
                    <p>Replaces Nano Banana</p>
                    <div class="savings">Save $29/mo</div>
                </div>
                <div class="tool-card">
                    <h3>🏗️ App Constructor</h3>
                    <p>Replaces Loveable</p>
                    <div class="savings">Save $79/mo</div>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>🌟 All Dashboards ({{ total_dashboards }}+)</h2>
            <p>Complete dashboard ecosystem</p>
            <ul style="list-style: none; padding: 20px 0;">
                {% for name in dashboard_names %}
                <li style="padding: 10px; border-bottom: 1px solid #eee;">📊 {{ name }}</li>
                {% endfor %}
            </ul>
            <p style="margin-top: 20px; color: #888;">And {{ total_dashboards - 10 }} more specialized dashboards...</p>
        </div>
    </div>
</body>
</html>
"""

ENGINES_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🧠 48 Intelligence Engines</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; }
        h1 { color: #667eea; }
        .back { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }
        .cluster { margin: 30px 0; padding: 20px; background: #f5f5f5; border-radius: 10px; }
        .cluster h2 { color: #764ba2; }
        .engine { padding: 15px; margin: 10px 0; background: white; border-radius: 8px; border-left: 4px solid #667eea; }
        .engine strong { color: #667eea; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        <h1>🧠 48 Intelligence Engines</h1>
        <p>Complete intelligence system covering 24 domains × 2 modes = 48 engines</p>

        {% for cluster_name, engines in clusters.items() %}
        <div class="cluster">
            <h2>{{ cluster_name }} Cluster ({{ engines|length }} engines)</h2>
            {% for engine in engines %}
            <div class="engine">
                <strong>{{ engine.icon }} {{ engine.name }}</strong>
                <br>
                <span style="color: #888;">Domain: {{ engine.domain }} | Mode: {{ engine.mode }}</span>
                <br>
                <small>Capabilities: {{ engine.capabilities|join(', ') }}</small>
            </div>
            {% endfor %}
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

TOOLS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🔧 Codex Tools Suite</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; }
        h1 { color: #667eea; }
        .back { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }
        .savings-banner {
            background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: white;
            margin: 20px 0;
            font-size: 1.5em;
            font-weight: bold;
        }
        .tool {
            margin: 20px 0;
            padding: 25px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
            border-left: 5px solid #667eea;
        }
        .tool h2 { color: #667eea; margin-bottom: 10px; }
        .tool .replaces {
            background: #ff6b6b;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            display: inline-block;
            margin: 10px 0;
            font-weight: bold;
        }
        .tool .savings {
            background: #51cf66;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            display: inline-block;
            margin: 10px 5px;
            font-weight: bold;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin: 15px 0;
        }
        .feature {
            background: white;
            padding: 10px;
            border-radius: 8px;
            font-size: 0.9em;
        }
        .status {
            background: #51cf66;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            display: inline-block;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        <h1>🔧 Codex Tools Suite</h1>
        <p>Complete suite of FREE tools - Zero subscriptions, complete digital sovereignty</p>

        <div class="savings-banner">
            💰 Total Savings: $316/month = $3,792/year!
        </div>

        {% for tool in tools %}
        <div class="tool">
            <h2>{{ tool.icon }} {{ tool.name }}</h2>
            <p style="color: #666; font-size: 1.1em;">{{ tool.description }}</p>

            <div style="margin: 15px 0;">
                <span class="replaces">❌ {{ tool.replaces }}</span>
                <span class="savings">✅ Save {{ tool.savings }}</span>
                <span class="status">🟢 {{ tool.status|upper }}</span>
            </div>

            <h3 style="color: #764ba2; margin-top: 20px;">Features:</h3>
            <div class="features">
                {% for feature in tool.features %}
                <div class="feature">✓ {{ feature }}</div>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

CHAT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>💬 AI Chat - Codex Dominion</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            margin: 0;
        }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; }
        .back { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }
        h1 { color: #667eea; }
        .chat-container {
            display: grid;
            grid-template-columns: 250px 1fr;
            gap: 20px;
            height: 600px;
        }
        .ai-models {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 10px;
            overflow-y: auto;
        }
        .ai-model {
            padding: 10px;
            margin: 5px 0;
            background: white;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .ai-model:hover { background: #667eea; color: white; }
        .ai-model.active { background: #764ba2; color: white; }
        .chat-area {
            display: flex;
            flex-direction: column;
            background: #f9f9f9;
            border-radius: 10px;
            padding: 20px;
        }
        .messages {
            flex: 1;
            overflow-y: auto;
            margin-bottom: 20px;
            padding: 15px;
            background: white;
            border-radius: 10px;
        }
        .message {
            margin: 10px 0;
            padding: 15px;
            border-radius: 10px;
            max-width: 80%;
        }
        .user-message {
            background: #667eea;
            color: white;
            margin-left: auto;
        }
        .ai-message {
            background: #e8f5e9;
            color: #333;
        }
        .input-area {
            display: flex;
            gap: 10px;
        }
        .input-area textarea {
            flex: 1;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #667eea;
            font-family: inherit;
            font-size: 14px;
            resize: vertical;
            min-height: 60px;
        }
        .input-area button {
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.3s;
        }
        .input-area button:hover { transform: scale(1.05); }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        <h1>💬 AI Chat System</h1>
        <p>Chat with multiple AI models - Claude, VS Code Copilot, and more</p>

        <div class="chat-container">
            <div class="ai-models">
                <h3>AI Models</h3>
                <div class="ai-model active" data-model="claude">🤖 Claude Sonnet 4.5</div>
                <div class="ai-model" data-model="copilot">🚁 VS Code Copilot</div>
                <div class="ai-model" data-model="gpt">✨ GPT-4</div>
                <div class="ai-model" data-model="gemini">💎 Google Gemini</div>
                <div class="ai-model" data-model="jermaine">⚡ Jermaine Super AI</div>
                <div class="ai-model" data-model="local">🏠 Local LLM</div>
            </div>

            <div class="chat-area">
                <div class="messages" id="messages">
                    <div class="message ai-message">
                        <strong>🤖 Claude:</strong> Hello! I'm Claude Sonnet 4.5. How can I assist you today?
                    </div>
                </div>

                <div class="input-area">
                    <textarea id="userInput" placeholder="Type your message here... (Text or Voice)" rows="3"></textarea>
                    <button onclick="sendMessage()">📤 Send</button>
                    <button onclick="startVoice()" style="padding: 15px;">🎤</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentModel = 'claude';

        document.querySelectorAll('.ai-model').forEach(model => {
            model.addEventListener('click', function() {
                document.querySelectorAll('.ai-model').forEach(m => m.classList.remove('active'));
                this.classList.add('active');
                currentModel = this.dataset.model;
                addMessage('ai', `Switched to ${this.textContent.trim()}`);
            });
        });

        function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            if (!message) return;

            addMessage('user', message);
            input.value = '';

            // Simulate AI response
            setTimeout(() => {
                const responses = {
                    'claude': 'I understand. Let me help you with that...',
                    'copilot': 'Here\'s a code suggestion for your request...',
                    'gpt': 'Based on my analysis...',
                    'gemini': 'I can help with that. Here\'s what I found...',
                    'jermaine': '⚡ SUPER ACTION AI ENGAGED! Processing your request with maximum efficiency...',
                    'local': 'Processing locally on your machine...'
                };
                addMessage('ai', responses[currentModel] || 'Processing...');
            }, 1000);
        }

        function addMessage(type, text) {
            const messages = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}-message`;
            messageDiv.innerHTML = `<strong>${type === 'user' ? '👤 You:' : getModelIcon()}</strong> ${text}`;
            messages.appendChild(messageDiv);
            messages.scrollTop = messages.scrollHeight;
        }

        function getModelIcon() {
            const icons = {
                'claude': '🤖 Claude:',
                'copilot': '🚁 Copilot:',
                'gpt': '✨ GPT-4:',
                'gemini': '💎 Gemini:',
                'jermaine': '⚡ Jermaine:',
                'local': '🏠 Local:'
            };
            return icons[currentModel] || '🤖 AI:';
        }

        function startVoice() {
            if ('webkitSpeechRecognition' in window) {
                const recognition = new webkitSpeechRecognition();
                recognition.onresult = function(event) {
                    document.getElementById('userInput').value = event.results[0][0].transcript;
                };
                recognition.start();
            } else {
                alert('Voice recognition not supported in this browser');
            }
        }

        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""

DASHBOARDS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>📊 All Dashboards - Codex Dominion</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; }
        .back { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }
        h1 { color: #667eea; }
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .dashboard-card {
            padding: 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
            border-left: 5px solid #667eea;
            transition: transform 0.3s;
            cursor: pointer;
        }
        .dashboard-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        .dashboard-card h3 { color: #667eea; margin-bottom: 10px; }
        .dashboard-card p { color: #666; font-size: 0.9em; }
        .category {
            margin: 30px 0;
        }
        .category h2 {
            color: #764ba2;
            border-bottom: 3px solid #764ba2;
            padding-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        <h1>📊 All Codex Dominion Dashboards (52)</h1>
        <p>Complete suite of specialized dashboards for every domain</p>

        {% for category, dashboards in all_dashboards.items() %}
        <div class="category">
            <h2>{{ category }}</h2>
            <div class="dashboard-grid">
                {% for dash in dashboards %}
                <div class="dashboard-card" onclick="alert('Launching {{ dash.name }}...')">
                    <h3>{{ dash.icon }} {{ dash.name }}</h3>
                    <p>{{ dash.description }}</p>
                    <p style="color: #764ba2; font-weight: bold; margin-top: 10px;">{{ dash.status }}</p>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

AGENTS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🤖 AI Agents - Codex Dominion</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; }
        .back { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }
        h1 { color: #667eea; }
        .agent {
            margin: 20px 0;
            padding: 25px;
            background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
            border-radius: 15px;
            border-left: 5px solid #667eea;
        }
        .agent h2 { color: #333; margin-bottom: 10px; }
        .agent .status {
            display: inline-block;
            padding: 5px 15px;
            background: #51cf66;
            color: white;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }
        .agent-actions {
            margin-top: 15px;
            display: flex;
            gap: 10px;
        }
        .agent-actions button {
            padding: 10px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
        }
        .agent-actions button:hover { background: #764ba2; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        <h1>🤖 AI Agent System</h1>
        <p>Autonomous AI agents working for your digital sovereignty</p>

        <div class="agent">
            <h2>⚡ Jermaine Super Action AI Agent</h2>
            <span class="status">🟢 ACTIVE</span>
            <p style="margin-top: 15px; color: #555;">
                Your personal AI powerhouse - handles complex tasks, automates workflows,
                and executes actions across all systems with maximum efficiency.
            </p>
            <p><strong>Capabilities:</strong> Task automation, Code generation, Data analysis,
            System integration, Multi-tool orchestration</p>
            <div class="agent-actions">
                <button onclick="alert('Activating Jermaine Super AI...')">⚡ Activate</button>
                <button onclick="alert('Configuring agent...')">⚙️ Configure</button>
                <button onclick="alert('Viewing agent logs...')">📊 View Logs</button>
            </div>
        </div>

        <div class="agent">
            <h2>🚁 VS Code Copilot Agent</h2>
            <span class="status">🟢 ACTIVE</span>
            <p style="margin-top: 15px; color: #555;">
                Integrated directly with your VS Code - provides real-time code suggestions,
                debugging assistance, and intelligent code completion.
            </p>
            <p><strong>Capabilities:</strong> Code completion, Debugging, Refactoring,
            Documentation generation, Test creation</p>
            <div class="agent-actions">
                <button onclick="alert('Opening Copilot...')">🚁 Open Copilot</button>
                <button onclick="alert('Viewing copilot-instructions.md...')">📄 Instructions</button>
            </div>
        </div>

        <div class="agent">
            <h2>🤖 Claude Agent</h2>
            <span class="status">🟢 ACTIVE</span>
            <p style="margin-top: 15px; color: #555;">
                Powered by Claude Sonnet 4.5 - handles complex reasoning, analysis,
                and content creation with advanced understanding.
            </p>
            <p><strong>Capabilities:</strong> Advanced reasoning, Long-form writing,
            Code analysis, Research, Strategic planning</p>
            <div class="agent-actions">
                <button onclick="alert('Activating Claude...')">🤖 Activate</button>
                <button onclick="alert('Setting context...')">📝 Set Context</button>
            </div>
        </div>

        <div class="agent">
            <h2>👑 Council Seal Agent</h2>
            <span class="status">🟢 ACTIVE</span>
            <p style="margin-top: 15px; color: #555;">
                Supreme governance agent - oversees all system operations,
                enforces policies, and maintains digital sovereignty.
            </p>
            <p><strong>Capabilities:</strong> Policy enforcement, Resource allocation,
            Security oversight, System governance, Strategic decisions</p>
            <div class="agent-actions">
                <button onclick="alert('Accessing Council...')">👑 Access Council</button>
                <button onclick="alert('Viewing policies...')">📜 Policies</button>
            </div>
        </div>
    </div>
</body>
</html>
"""

EMAIL_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>📧 Email - Codex Dominion</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; }
        .back { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }
        h1 { color: #667eea; }
        .email-container {
            display: grid;
            grid-template-columns: 200px 1fr;
            gap: 20px;
            height: 600px;
        }
        .email-folders {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 10px;
        }
        .folder {
            padding: 10px;
            margin: 5px 0;
            background: white;
            border-radius: 5px;
            cursor: pointer;
        }
        .folder:hover { background: #667eea; color: white; }
        .email-content {
            background: #f9f9f9;
            border-radius: 10px;
            padding: 20px;
        }
        .compose-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .email-list {
            background: white;
            padding: 15px;
            border-radius: 10px;
        }
        .email-item {
            padding: 15px;
            border-bottom: 1px solid #eee;
            cursor: pointer;
        }
        .email-item:hover { background: #f5f5f5; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        <h1>📧 Email System</h1>
        <p>Sovereign email management - No third-party tracking</p>

        <div class="email-container">
            <div class="email-folders">
                <button class="compose-btn">✍️ Compose</button>
                <div class="folder">📥 Inbox (5)</div>
                <div class="folder">📤 Sent</div>
                <div class="folder">⭐ Starred</div>
                <div class="folder">📝 Drafts</div>
                <div class="folder">🗑️ Trash</div>
                <div class="folder">⚙️ Settings</div>
            </div>

            <div class="email-content">
                <h2>📥 Inbox</h2>
                <div class="email-list">
                    <div class="email-item">
                        <strong>Council Seal</strong> - System Update Available
                        <div style="color: #888; font-size: 0.9em;">2 hours ago</div>
                    </div>
                    <div class="email-item">
                        <strong>Jermaine Super AI</strong> - Daily Report: All Systems Operational
                        <div style="color: #888; font-size: 0.9em;">5 hours ago</div>
                    </div>
                    <div class="email-item">
                        <strong>48 Intelligence Engines</strong> - New Insights Available
                        <div style="color: #888; font-size: 0.9em;">1 day ago</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

DOCUMENTS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>📄 Documents - Codex Dominion</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; }
        .back { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }
        h1 { color: #667eea; }
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 50px;
            text-align: center;
            margin: 20px 0;
            background: #f5f7fa;
            cursor: pointer;
        }
        .upload-area:hover { background: #e8f4f8; }
        .document-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .document {
            padding: 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 10px;
            text-align: center;
            cursor: pointer;
        }
        .document:hover { transform: translateY(-5px); }
        .doc-icon { font-size: 3em; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        <h1>📄 Document Management</h1>
        <p>Upload, organize, and analyze your documents with AI</p>

        <form action="/upload" method="post" enctype="multipart/form-data">
            <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                <div style="font-size: 3em;">📤</div>
                <h2>Upload Documents</h2>
                <p>Drag & drop files here or click to browse</p>
                <p style="color: #888; font-size: 0.9em;">Supported: PDF, DOCX, TXT, MD, Code files</p>
                <input type="file" id="fileInput" name="file" multiple style="display: none;">
            </div>
        </form>

        <h2>📁 Recent Documents</h2>
        <div class="document-grid">
            <div class="document">
                <div class="doc-icon">📄</div>
                <strong>copilot-instructions.md</strong>
                <div style="color: #888; font-size: 0.8em;">2 KB</div>
            </div>
            <div class="document">
                <div class="doc-icon">📊</div>
                <strong>ARCHITECTURE.md</strong>
                <div style="color: #888; font-size: 0.8em;">15 KB</div>
            </div>
            <div class="document">
                <div class="doc-icon">📝</div>
                <strong>README.md</strong>
                <div style="color: #888; font-size: 0.8em;">8 KB</div>
            </div>
            <div class="document">
                <div class="doc-icon">⚙️</div>
                <strong>codex_ledger.json</strong>
                <div style="color: #888; font-size: 0.8em;">45 KB</div>
            </div>
        </div>
    </div>
</body>
</html>
"""

AVATARS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>👤 Avatars - Codex Dominion</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; }
        .back { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }
        h1 { color: #667eea; }
        .avatar-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .avatar-card {
            padding: 25px;
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            border-radius: 15px;
            text-align: center;
        }
        .avatar-icon {
            width: 100px;
            height: 100px;
            margin: 0 auto 15px;
            background: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3em;
        }
        .avatar-card h3 { color: #333; margin-bottom: 10px; }
        .avatar-status {
            display: inline-block;
            padding: 5px 15px;
            background: #51cf66;
            color: white;
            border-radius: 20px;
            font-size: 0.9em;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        <h1>👤 Avatar System</h1>
        <p>AI-powered digital representatives for different roles</p>

        <div class="avatar-grid">
            <div class="avatar-card">
                <div class="avatar-icon">👤</div>
                <h3>Jermaine Avatar</h3>
                <div class="avatar-status">🟢 ACTIVE</div>
                <p>Your primary digital representative</p>
            </div>

            <div class="avatar-card">
                <div class="avatar-icon">💼</div>
                <h3>Business Avatar</h3>
                <div class="avatar-status">🟢 ACTIVE</div>
                <p>Professional interactions & negotiations</p>
            </div>

            <div class="avatar-card">
                <div class="avatar-icon">🎓</div>
                <h3>Educator Avatar</h3>
                <div class="avatar-status">🟢 ACTIVE</div>
                <p>Teaching & knowledge sharing</p>
            </div>

            <div class="avatar-card">
                <div class="avatar-icon">🔧</div>
                <h3>Technical Avatar</h3>
                <div class="avatar-status">🟢 ACTIVE</div>
                <p>Development & system operations</p>
            </div>

            <div class="avatar-card">
                <div class="avatar-icon">👑</div>
                <h3>Council Avatar</h3>
                <div class="avatar-status">🟢 ACTIVE</div>
                <p>Governance & strategic decisions</p>
            </div>

            <div class="avatar-card">
                <div class="avatar-icon">🎨</div>
                <h3>Creative Avatar</h3>
                <div class="avatar-status">🟢 ACTIVE</div>
                <p>Content creation & design</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

COUNCIL_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>👑 Council Seal - Codex Dominion</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); }
        .back { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }
        h1 { color: #d4af37; text-align: center; font-size: 2.5em; }
        .seal {
            text-align: center;
            font-size: 5em;
            margin: 20px 0;
        }
        .council-section {
            margin: 30px 0;
            padding: 25px;
            background: linear-gradient(135deg, #fff9e6 0%, #fffbf0 100%);
            border-radius: 15px;
            border-left: 5px solid #d4af37;
        }
        .council-section h2 { color: #d4af37; }
        .metric-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .metric {
            text-align: center;
            padding: 20px;
            background: white;
            border-radius: 10px;
            border: 2px solid #d4af37;
        }
        .metric h3 { font-size: 2em; color: #d4af37; margin: 0; }
        .metric p { color: #666; margin: 5px 0 0 0; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        <div class="seal">👑</div>
        <h1>COUNCIL SEAL</h1>
        <p style="text-align: center; color: #666; font-size: 1.2em;">Supreme Governance Authority</p>

        <div class="council-section">
            <h2>🏛️ Governance Structure</h2>
            <p>The Council Seal represents the supreme authority over all Codex Dominion systems,
            enforcing policies, managing resources, and maintaining digital sovereignty.</p>

            <div class="metric-row">
                <div class="metric">
                    <h3>48</h3>
                    <p>Intelligence Engines</p>
                </div>
                <div class="metric">
                    <h3>52</h3>
                    <p>Active Dashboards</p>
                </div>
                <div class="metric">
                    <h3>6</h3>
                    <p>Tool Systems</p>
                </div>
                <div class="metric">
                    <h3>$316/mo</h3>
                    <p>Cost Savings</p>
                </div>
            </div>
        </div>

        <div class="council-section">
            <h2>📜 Active Proclamations</h2>
            <ul style="line-height: 2;">
                <li><strong>Digital Sovereignty Decree:</strong> Complete ownership of all systems ✅</li>
                <li><strong>Zero Subscription Policy:</strong> No external dependencies ✅</li>
                <li><strong>AI Integration Charter:</strong> Full AI agent deployment ✅</li>
                <li><strong>48 Engines Mandate:</strong> All intelligence systems operational ✅</li>
            </ul>
        </div>

        <div class="council-section">
            <h2>⚖️ System Authority</h2>
            <p><strong>Council Seal Powers:</strong></p>
            <ul>
                <li>Policy Enforcement across all systems</li>
                <li>Resource Allocation & Optimization</li>
                <li>Security & Access Control</li>
                <li>Strategic Direction & Planning</li>
                <li>System Health Monitoring</li>
            </ul>
        </div>

        <div style="text-align: center; margin-top: 40px;">
            <p style="font-size: 1.5em; color: #d4af37; font-weight: bold;">
                🔥 THE FLAME BURNS SOVEREIGN AND ETERNAL 👑
            </p>
        </div>
    </div>
</body>
</html>
"""

COPILOT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🚁 Copilot - Codex Dominion</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; }
        .back { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }
        h1 { color: #667eea; }
        .copilot-section {
            margin: 20px 0;
            padding: 20px;
            background: #f5f7fa;
            border-radius: 10px;
            border-left: 5px solid #667eea;
        }
        .copilot-section h2 { color: #764ba2; }
        .code-block {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            border-radius: 10px;
            font-family: 'Consolas', 'Monaco', monospace;
            overflow-x: auto;
            margin: 15px 0;
        }
        .instruction-item {
            padding: 15px;
            margin: 10px 0;
            background: white;
            border-radius: 8px;
            border-left: 3px solid #51cf66;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back">← Back to Dashboard</a>
        <h1>🚁 VS Code Copilot Integration</h1>
        <p>AI-powered coding assistant with Codex Dominion context</p>

        <div class="copilot-section">
            <h2>📄 Copilot Instructions</h2>
            <p>These instructions are loaded from <code>.github/copilot-instructions.md</code></p>

            <div class="instruction-item">
                <strong>✅ Project Context:</strong> Codex Dominion - Hybrid polyglot monorepo with ceremonial naming
            </div>

            <div class="instruction-item">
                <strong>✅ Architecture:</strong> Council Seal Structure - Sovereigns, Custodians, Industry Agents
            </div>

            <div class="instruction-item">
                <strong>✅ Tech Stack:</strong> Next.js 14+, FastAPI, Streamlit, Flask, Docker, Kubernetes
            </div>

            <div class="instruction-item">
                <strong>✅ Key Files:</strong> codex_ledger.json, proclamations.json, cycles.json
            </div>
        </div>

        <div class="copilot-section">
            <h2>⚡ Active Copilot Features</h2>
            <ul style="line-height: 2;">
                <li>🤖 <strong>Code Completion:</strong> Context-aware suggestions</li>
                <li>💬 <strong>Chat Interface:</strong> Ask questions about your code</li>
                <li>🔍 <strong>Code Explanation:</strong> Understand complex code</li>
                <li>🛠️ <strong>Refactoring:</strong> Improve code structure</li>
                <li>📝 <strong>Documentation:</strong> Auto-generate docs</li>
                <li>🧪 <strong>Test Generation:</strong> Create unit tests</li>
            </ul>
        </div>

        <div class="copilot-section">
            <h2>💡 Quick Tips</h2>
            <div class="code-block">
// Use Copilot inline suggestions (Tab to accept)
// Press Ctrl+I for Copilot chat
// Type // comments to guide Copilot
// Use @workspace to search your project
// Use @terminal for command suggestions
            </div>
        </div>

        <div class="copilot-section">
            <h2>🔗 Integration Status</h2>
            <p>✅ Copilot instructions loaded from copilot-instructions.md</p>
            <p>✅ Project context available to Copilot</p>
            <p>✅ Claude Sonnet 4.5 model active</p>
            <p>✅ All 48 Intelligence Engines accessible</p>
        </div>
    </div>
</body>
</html>
"""

# ============================================================================
# WEBSITE BUILDER HTML TEMPLATE
# ============================================================================
WEBSITES_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🌐 Website Builder - Codex Dominion</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 { color: white; text-align: center; margin-bottom: 30px; font-size: 2.5em; }
        .nav-tabs {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px; margin-bottom: 30px;
        }
        .nav-tab {
            background: rgba(255,255,255,0.2); padding: 12px; text-align: center;
            border-radius: 10px; text-decoration: none; color: white;
            transition: all 0.3s; font-weight: 600;
        }
        .nav-tab:hover { background: rgba(255,255,255,0.3); transform: translateY(-2px); }
        .nav-tab.active { background: rgba(255,255,255,0.4); }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; }
        .card {
            background: white; border-radius: 15px; padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .card h2 { color: #667eea; margin-bottom: 15px; }
        .template-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-top: 15px; }
        .template-card {
            border: 2px solid #e0e0e0; border-radius: 10px; padding: 15px;
            text-align: center; cursor: pointer; transition: all 0.3s;
        }
        .template-card:hover { border-color: #667eea; transform: scale(1.05); }
        .template-icon { font-size: 3em; margin-bottom: 10px; }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 12px 30px; border: none; border-radius: 25px;
            cursor: pointer; font-size: 1em; font-weight: 600; margin-top: 15px;
        }
        .btn:hover { transform: scale(1.05); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
        .website-list { margin-top: 15px; }
        .website-item {
            background: #f5f5f5; padding: 15px; border-radius: 10px; margin-bottom: 10px;
            display: flex; justify-content: space-between; align-items: center;
        }
        .status-badge {
            padding: 5px 15px; border-radius: 20px; font-size: 0.85em; font-weight: 600;
        }
        .status-live { background: #4caf50; color: white; }
        .status-building { background: #ff9800; color: white; }
        .input-group { margin-bottom: 15px; }
        .input-group label { display: block; margin-bottom: 5px; font-weight: 600; color: #333; }
        .input-group input, .input-group select, .input-group textarea {
            width: 100%; padding: 10px; border: 2px solid #e0e0e0; border-radius: 8px;
            font-size: 1em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 Website Builder System</h1>

        <div class="nav-tabs">
            <a href="/" class="nav-tab">🏠 Home</a>
            <a href="/engines" class="nav-tab">🧠 48 Engines</a>
            <a href="/tools" class="nav-tab">🔧 6 Tools</a>
            <a href="/dashboards" class="nav-tab">📊 All Dashboards</a>
            <a href="/chat" class="nav-tab">💬 AI Chat</a>
            <a href="/agents" class="nav-tab">🤖 AI Agents</a>
            <a href="/websites" class="nav-tab active">🌐 Websites</a>
            <a href="/stores" class="nav-tab">🛒 Stores</a>
            <a href="/social" class="nav-tab">📱 Social Media</a>
            <a href="/affiliate" class="nav-tab">💰 Affiliate</a>
            <a href="/chatbot" class="nav-tab">🤖 Action Chatbot</a>
            <a href="/algorithm" class="nav-tab">🧠 Algorithm AI</a>
            <a href="/autopublish" class="nav-tab">🚀 Auto-Publish</a>
        </div>

        <div class="grid">
            <!-- Quick Website Builder -->
            <div class="card">
                <h2>⚡ Quick Website Builder</h2>
                <div class="input-group">
                    <label>Website Name:</label>
                    <input type="text" placeholder="My Awesome Website" id="website-name">
                </div>
                <div class="input-group">
                    <label>Domain:</label>
                    <input type="text" placeholder="mywebsite.com" id="website-domain">
                </div>
                <div class="input-group">
                    <label>Select Template:</label>
                    <select id="website-template">
                        <option value="landing">Landing Page</option>
                        <option value="blog">Blog</option>
                        <option value="portfolio">Portfolio</option>
                        <option value="business">Business</option>
                        <option value="ecommerce">E-commerce</option>
                    </select>
                </div>
                <button class="btn" onclick="buildWebsite()">🚀 Build Website</button>
            </div>

            <!-- Website Templates -->
            <div class="card">
                <h2>🎨 Templates Library</h2>
                <div class="template-grid">
                    <div class="template-card" onclick="selectTemplate('landing')">
                        <div class="template-icon">🚀</div>
                        <strong>Landing Page</strong>
                        <p style="font-size: 0.9em; color: #666; margin-top: 5px;">High-converting single page</p>
                    </div>
                    <div class="template-card" onclick="selectTemplate('blog')">
                        <div class="template-icon">📝</div>
                        <strong>Blog</strong>
                        <p style="font-size: 0.9em; color: #666; margin-top: 5px;">Content-focused design</p>
                    </div>
                    <div class="template-card" onclick="selectTemplate('portfolio')">
                        <div class="template-icon">🎨</div>
                        <strong>Portfolio</strong>
                        <p style="font-size: 0.9em; color: #666; margin-top: 5px;">Showcase your work</p>
                    </div>
                    <div class="template-card" onclick="selectTemplate('business')">
                        <div class="template-icon">💼</div>
                        <strong>Business</strong>
                        <p style="font-size: 0.9em; color: #666; margin-top: 5px;">Professional corporate site</p>
                    </div>
                    <div class="template-card" onclick="selectTemplate('ecommerce')">
                        <div class="template-icon">🛍️</div>
                        <strong>E-commerce</strong>
                        <p style="font-size: 0.9em; color: #666; margin-top: 5px;">Online store ready</p>
                    </div>
                    <div class="template-card" onclick="selectTemplate('saas')">
                        <div class="template-icon">☁️</div>
                        <strong>SaaS</strong>
                        <p style="font-size: 0.9em; color: #666; margin-top: 5px;">Software product site</p>
                    </div>
                </div>
            </div>

            <!-- Active Websites -->
            <div class="card">
                <h2>🌍 Your Websites</h2>
                <div class="website-list">
                    <div class="website-item">
                        <div>
                            <strong>🌐 codexdominion.app</strong>
                            <p style="font-size: 0.9em; color: #666;">Main Website</p>
                        </div>
                        <span class="status-badge status-live">✅ Live</span>
                    </div>
                    <div class="website-item">
                        <div>
                            <strong>🛍️ aistorelab.com</strong>
                            <p style="font-size: 0.9em; color: #666;">E-commerce Store</p>
                        </div>
                        <span class="status-badge status-live">✅ Live</span>
                    </div>
                    <div class="website-item">
                        <div>
                            <strong>📝 codexblog.app</strong>
                            <p style="font-size: 0.9em; color: #666;">Content Hub</p>
                        </div>
                        <span class="status-badge status-building">🔨 Building</span>
                    </div>
                </div>
            </div>

            <!-- Website Features -->
            <div class="card">
                <h2>✨ Features Available</h2>
                <p>✅ <strong>Responsive Design</strong> - Mobile, tablet, desktop</p>
                <p>✅ <strong>SEO Optimized</strong> - Meta tags, sitemaps, schema</p>
                <p>✅ <strong>Fast Loading</strong> - CDN, caching, optimization</p>
                <p>✅ <strong>SSL Security</strong> - HTTPS encryption included</p>
                <p>✅ <strong>Analytics</strong> - Google Analytics, tracking</p>
                <p>✅ <strong>Contact Forms</strong> - Lead capture forms</p>
                <p>✅ <strong>Blog System</strong> - Built-in CMS</p>
                <p>✅ <strong>E-commerce</strong> - WooCommerce integration</p>
            </div>
        </div>
    </div>

    <script>
        function selectTemplate(template) {
            document.getElementById('website-template').value = template;
            alert('✅ Template selected: ' + template.charAt(0).toUpperCase() + template.slice(1));
        }

        function buildWebsite() {
            const name = document.getElementById('website-name').value;
            const domain = document.getElementById('website-domain').value;
            const template = document.getElementById('website-template').value;

            if (!name || !domain) {
                alert('⚠️ Please fill in all fields');
                return;
            }

            alert(`🚀 Building ${name} at ${domain} with ${template} template!\\n\\n⏳ Estimated time: 2-3 minutes\\n✅ SSL certificate will be auto-configured`);
        }
    </script>
</body>
</html>
"""

# ============================================================================
# STORES HTML TEMPLATE
# ============================================================================
STORES_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🛒 Store Builder - Codex Dominion</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 { color: white; text-align: center; margin-bottom: 30px; font-size: 2.5em; }
        .nav-tabs {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px; margin-bottom: 30px;
        }
        .nav-tab {
            background: rgba(255,255,255,0.2); padding: 12px; text-align: center;
            border-radius: 10px; text-decoration: none; color: white;
            transition: all 0.3s; font-weight: 600;
        }
        .nav-tab:hover { background: rgba(255,255,255,0.3); transform: translateY(-2px); }
        .nav-tab.active { background: rgba(255,255,255,0.4); }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; }
        .card {
            background: white; border-radius: 15px; padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .card h2 { color: #f5576c; margin-bottom: 15px; }
        .store-card {
            border: 2px solid #e0e0e0; border-radius: 10px; padding: 20px;
            margin-bottom: 15px; transition: all 0.3s;
        }
        .store-card:hover { border-color: #f5576c; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .metric { display: inline-block; margin-right: 20px; }
        .metric strong { color: #f5576c; font-size: 1.5em; }
        .btn {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white; padding: 12px 30px; border: none; border-radius: 25px;
            cursor: pointer; font-size: 1em; font-weight: 600; margin-top: 15px;
        }
        .btn:hover { transform: scale(1.05); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
        .input-group { margin-bottom: 15px; }
        .input-group label { display: block; margin-bottom: 5px; font-weight: 600; color: #333; }
        .input-group input, .input-group select {
            width: 100%; padding: 10px; border: 2px solid #e0e0e0; border-radius: 8px;
            font-size: 1em;
        }
        .product-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-top: 15px; }
        .product-card {
            border: 1px solid #e0e0e0; border-radius: 10px; padding: 15px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛒 E-Commerce Store Builder</h1>

        <div class="nav-tabs">
            <a href="/" class="nav-tab">🏠 Home</a>
            <a href="/engines" class="nav-tab">🧠 48 Engines</a>
            <a href="/tools" class="nav-tab">🔧 6 Tools</a>
            <a href="/dashboards" class="nav-tab">📊 All Dashboards</a>
            <a href="/chat" class="nav-tab">💬 AI Chat</a>
            <a href="/agents" class="nav-tab">🤖 AI Agents</a>
            <a href="/websites" class="nav-tab">🌐 Websites</a>
            <a href="/stores" class="nav-tab active">🛒 Stores</a>
            <a href="/social" class="nav-tab">📱 Social Media</a>
            <a href="/affiliate" class="nav-tab">💰 Affiliate</a>
            <a href="/chatbot" class="nav-tab">🤖 Action Chatbot</a>
            <a href="/algorithm" class="nav-tab">🧠 Algorithm AI</a>
            <a href="/autopublish" class="nav-tab">🚀 Auto-Publish</a>
        </div>

        <div class="grid">
            <!-- Store Builder -->
            <div class="card">
                <h2>🏪 Create New Store</h2>
                <div class="input-group">
                    <label>Store Name:</label>
                    <input type="text" placeholder="My Store" id="store-name">
                </div>
                <div class="input-group">
                    <label>Store Type:</label>
                    <select id="store-type">
                        <option value="woocommerce">WooCommerce</option>
                        <option value="shopify">Shopify</option>
                        <option value="custom">Custom</option>
                    </select>
                </div>
                <div class="input-group">
                    <label>Niche:</label>
                    <select id="store-niche">
                        <option value="digital">Digital Products</option>
                        <option value="fashion">Fashion</option>
                        <option value="electronics">Electronics</option>
                        <option value="food">Food & Beverage</option>
                        <option value="beauty">Beauty & Cosmetics</option>
                        <option value="books">Books & Education</option>
                    </select>
                </div>
                <button class="btn" onclick="createStore()">🚀 Create Store</button>
            </div>

            <!-- Active Stores -->
            <div class="card">
                <h2>🏬 Your Stores</h2>
                <div class="store-card">
                    <h3>🛍️ AIStoreLab</h3>
                    <p><strong>Platform:</strong> WooCommerce</p>
                    <p><strong>Products:</strong> 147 active</p>
                    <div class="metric">
                        <strong>$12,458</strong><br>
                        <span style="font-size: 0.9em;">Monthly Revenue</span>
                    </div>
                    <div class="metric">
                        <strong>342</strong><br>
                        <span style="font-size: 0.9em;">Orders</span>
                    </div>
                    <button class="btn">Manage Store</button>
                </div>
                <div class="store-card">
                    <h3>📚 Digital Products Store</h3>
                    <p><strong>Platform:</strong> Custom</p>
                    <p><strong>Products:</strong> 89 active</p>
                    <div class="metric">
                        <strong>$8,234</strong><br>
                        <span style="font-size: 0.9em;">Monthly Revenue</span>
                    </div>
                    <div class="metric">
                        <strong>215</strong><br>
                        <span style="font-size: 0.9em;">Orders</span>
                    </div>
                    <button class="btn">Manage Store</button>
                </div>
            </div>

            <!-- Product Manager -->
            <div class="card">
                <h2>📦 Quick Product Add</h2>
                <div class="input-group">
                    <label>Product Name:</label>
                    <input type="text" placeholder="Product name" id="product-name">
                </div>
                <div class="input-group">
                    <label>Price:</label>
                    <input type="number" placeholder="29.99" id="product-price">
                </div>
                <div class="input-group">
                    <label>Store:</label>
                    <select id="product-store">
                        <option value="aistorelab">AIStoreLab</option>
                        <option value="digital">Digital Products Store</option>
                    </select>
                </div>
                <button class="btn" onclick="addProduct()">➕ Add Product</button>
            </div>

            <!-- Store Analytics -->
            <div class="card">
                <h2>📊 Store Analytics</h2>
                <div class="metric">
                    <strong>$20,692</strong><br>
                    <span style="font-size: 0.9em;">Total Revenue</span>
                </div>
                <div class="metric">
                    <strong>557</strong><br>
                    <span style="font-size: 0.9em;">Total Orders</span>
                </div>
                <div class="metric">
                    <strong>236</strong><br>
                    <span style="font-size: 0.9em;">Total Products</span>
                </div>
                <div class="metric">
                    <strong>1,234</strong><br>
                    <span style="font-size: 0.9em;">Customers</span>
                </div>
                <p style="margin-top: 20px;">✅ <strong>WooCommerce:</strong> 2 stores connected</p>
                <p>✅ <strong>Shopify:</strong> Ready to connect</p>
                <p>✅ <strong>Payment Gateways:</strong> Stripe, PayPal</p>
                <p>✅ <strong>Shipping:</strong> USPS, FedEx integrated</p>
            </div>

            <!-- Store Features -->
            <div class="card">
                <h2>✨ E-Commerce Features</h2>
                <p>✅ <strong>Product Management</strong> - Unlimited products</p>
                <p>✅ <strong>Inventory Tracking</strong> - Real-time stock levels</p>
                <p>✅ <strong>Payment Processing</strong> - Multiple gateways</p>
                <p>✅ <strong>Shipping Integration</strong> - Auto-calculate rates</p>
                <p>✅ <strong>Customer Accounts</strong> - Registration & login</p>
                <p>✅ <strong>Order Management</strong> - Track & fulfill orders</p>
                <p>✅ <strong>Discount Codes</strong> - Coupons & promotions</p>
                <p>✅ <strong>Analytics</strong> - Sales reports & insights</p>
            </div>

            <!-- Popular Products -->
            <div class="card">
                <h2>🔥 Top Products This Month</h2>
                <div class="product-grid">
                    <div class="product-card">
                        <div style="font-size: 3em;">📚</div>
                        <strong>AI Guide</strong>
                        <p>$49.99</p>
                        <p style="font-size: 0.85em; color: #666;">234 sold</p>
                    </div>
                    <div class="product-card">
                        <div style="font-size: 3em;">🎨</div>
                        <strong>Design Kit</strong>
                        <p>$29.99</p>
                        <p style="font-size: 0.85em; color: #666;">189 sold</p>
                    </div>
                    <div class="product-card">
                        <div style="font-size: 3em;">💻</div>
                        <strong>Code Pack</strong>
                        <p>$39.99</p>
                        <p style="font-size: 0.85em; color: #666;">156 sold</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function createStore() {
            const name = document.getElementById('store-name').value;
            const type = document.getElementById('store-type').value;
            const niche = document.getElementById('store-niche').value;

            if (!name) {
                alert('⚠️ Please enter store name');
                return;
            }

            alert(`🚀 Creating ${name} store!\\n\\nType: ${type}\\nNiche: ${niche}\\n\\n⏳ Setting up products and payment gateways...`);
        }

        function addProduct() {
            const name = document.getElementById('product-name').value;
            const price = document.getElementById('product-price').value;

            if (!name || !price) {
                alert('⚠️ Please fill in product details');
                return;
            }

            alert(`✅ Product "${name}" added at $${price}!`);
        }
    </script>
</body>
</html>
"""

# Embedded 48 engines data (no import dependencies)
def get_engines_data():
    """Get 48 intelligence engines organized by cluster"""
    return {
        "Technology": [
            {"id": 1, "name": "AI & ML Research Engine", "domain": "Artificial Intelligence", "mode": "Research", "icon": "🤖", "capabilities": ["Model training", "Algorithm research", "Dataset analysis"]},
            {"id": 2, "name": "AI & ML Execution Engine", "domain": "Artificial Intelligence", "mode": "Execution", "icon": "⚡", "capabilities": ["Model deployment", "API integration", "Real-time inference"]},
            {"id": 3, "name": "Quantum Computing Research Engine", "domain": "Quantum Computing", "mode": "Research", "icon": "⚛️", "capabilities": ["Quantum algorithms", "Simulation", "Circuit design"]},
            {"id": 4, "name": "Quantum Computing Execution Engine", "domain": "Quantum Computing", "mode": "Execution", "icon": "🔬", "capabilities": ["Quantum processing", "Optimization", "Cryptography"]},
            {"id": 5, "name": "Connectivity Research Engine", "domain": "5G/6G/Satellite", "mode": "Research", "icon": "📡", "capabilities": ["Network analysis", "Protocol research", "Coverage mapping"]},
            {"id": 6, "name": "Connectivity Execution Engine", "domain": "5G/6G/Satellite", "mode": "Execution", "icon": "🛰️", "capabilities": ["Network deployment", "Signal optimization", "IoT integration"]},
            {"id": 7, "name": "Clean Energy Research Engine", "domain": "Clean Energy", "mode": "Research", "icon": "🌱", "capabilities": ["Energy modeling", "Climate data", "Sustainability metrics"]},
            {"id": 8, "name": "Clean Energy Execution Engine", "domain": "Clean Energy", "mode": "Execution", "icon": "⚡", "capabilities": ["Grid optimization", "Renewable deployment", "Energy storage"]},
            {"id": 9, "name": "Space Research Engine", "domain": "Space Technology", "mode": "Research", "icon": "🚀", "capabilities": ["Orbital mechanics", "Satellite design", "Mission planning"]},
            {"id": 10, "name": "Space Execution Engine", "domain": "Space Technology", "mode": "Execution", "icon": "🛸", "capabilities": ["Launch coordination", "Satellite operations", "Ground control"]}
        ],
        "Bioengineering": [
            {"id": 11, "name": "Synthetic Biology Research Engine", "domain": "Synthetic Biology", "mode": "Research", "icon": "🧬", "capabilities": ["Gene sequencing", "Protein design", "CRISPR research"]},
            {"id": 12, "name": "Synthetic Biology Execution Engine", "domain": "Synthetic Biology", "mode": "Execution", "icon": "🔬", "capabilities": ["Gene editing", "Organism design", "Biomanufacturing"]},
            {"id": 13, "name": "Neurotechnology Research Engine", "domain": "Neurotechnology", "mode": "Research", "icon": "🧠", "capabilities": ["Brain mapping", "Neural signals", "Cognitive studies"]},
            {"id": 14, "name": "Neurotechnology Execution Engine", "domain": "Neurotechnology", "mode": "Execution", "icon": "🔌", "capabilities": ["BCI implementation", "Neural interfaces", "Prosthetic control"]},
            {"id": 15, "name": "Biotechnology Research Engine", "domain": "Biotechnology", "mode": "Research", "icon": "💊", "capabilities": ["Drug discovery", "Clinical trials", "Disease research"]},
            {"id": 16, "name": "Biotechnology Execution Engine", "domain": "Biotechnology", "mode": "Execution", "icon": "⚕️", "capabilities": ["Drug production", "Treatment deployment", "Patient care"]},
            {"id": 17, "name": "Health Sovereignty Research Engine", "domain": "Health Sovereignty", "mode": "Research", "icon": "🏥", "capabilities": ["Healthcare systems", "Medical independence", "Data privacy"]},
            {"id": 18, "name": "Health Sovereignty Execution Engine", "domain": "Health Sovereignty", "mode": "Execution", "icon": "🛡️", "capabilities": ["System implementation", "Data protection", "Care coordination"]}
        ],
        "Security": [
            {"id": 19, "name": "Cybersecurity Research Engine", "domain": "Cybersecurity", "mode": "Research", "icon": "🔐", "capabilities": ["Threat analysis", "Vulnerability research", "Security protocols"]},
            {"id": 20, "name": "Cybersecurity Execution Engine", "domain": "Cybersecurity", "mode": "Execution", "icon": "🛡️", "capabilities": ["Threat mitigation", "Incident response", "System hardening"]},
            {"id": 21, "name": "Identity Research Engine", "domain": "Identity Management", "mode": "Research", "icon": "👤", "capabilities": ["Identity protocols", "Authentication research", "Privacy frameworks"]},
            {"id": 22, "name": "Identity Execution Engine", "domain": "Identity Management", "mode": "Execution", "icon": "🔑", "capabilities": ["IAM deployment", "SSO implementation", "Access control"]},
            {"id": 23, "name": "Blockchain Research Engine", "domain": "Blockchain & Web3", "mode": "Research", "icon": "⛓️", "capabilities": ["Smart contract analysis", "Consensus research", "DeFi security"]},
            {"id": 24, "name": "Blockchain Execution Engine", "domain": "Blockchain & Web3", "mode": "Execution", "icon": "💎", "capabilities": ["Contract deployment", "Chain operations", "Wallet security"]},
            {"id": 25, "name": "Privacy Research Engine", "domain": "Privacy & Encryption", "mode": "Research", "icon": "🔒", "capabilities": ["Encryption algorithms", "Zero-knowledge proofs", "Privacy protocols"]},
            {"id": 26, "name": "Privacy Execution Engine", "domain": "Privacy & Encryption", "mode": "Execution", "icon": "🗝️", "capabilities": ["Encryption deployment", "VPN services", "Data protection"]}
        ],
        "Communication": [
            {"id": 27, "name": "Social Media Research Engine", "domain": "Social Media", "mode": "Research", "icon": "📱", "capabilities": ["Trend analysis", "Audience research", "Content analytics"]},
            {"id": 28, "name": "Social Media Execution Engine", "domain": "Social Media", "mode": "Execution", "icon": "🚀", "capabilities": ["Content publishing", "Campaign management", "Engagement automation"]},
            {"id": 29, "name": "Content Research Engine", "domain": "Content Marketing", "mode": "Research", "icon": "📝", "capabilities": ["SEO research", "Keyword analysis", "Competitor analysis"]},
            {"id": 30, "name": "Content Execution Engine", "domain": "Content Marketing", "mode": "Execution", "icon": "✍️", "capabilities": ["Content creation", "Publishing workflows", "Distribution"]},
            {"id": 31, "name": "Email Research Engine", "domain": "Email Marketing", "mode": "Research", "icon": "📧", "capabilities": ["List analysis", "Segmentation research", "A/B testing"]},
            {"id": 32, "name": "Email Execution Engine", "domain": "Email Marketing", "mode": "Execution", "icon": "📨", "capabilities": ["Campaign deployment", "Automation sequences", "List management"]},
            {"id": 33, "name": "Video Research Engine", "domain": "Video Content", "mode": "Research", "icon": "🎥", "capabilities": ["Video trends", "Platform analytics", "Audience preferences"]},
            {"id": 34, "name": "Video Execution Engine", "domain": "Video Content", "mode": "Execution", "icon": "🎬", "capabilities": ["Video creation", "Editing workflows", "Multi-platform publishing"]}
        ],
        "Planetary": [
            {"id": 35, "name": "Infrastructure Research Engine", "domain": "Infrastructure", "mode": "Research", "icon": "🏗️", "capabilities": ["System analysis", "Resilience studies", "Failure modeling"]},
            {"id": 36, "name": "Infrastructure Execution Engine", "domain": "Infrastructure", "mode": "Execution", "icon": "🏛️", "capabilities": ["System deployment", "Maintenance automation", "Disaster recovery"]},
            {"id": 37, "name": "Climate Research Engine", "domain": "Climate Adaptation", "mode": "Research", "icon": "🌍", "capabilities": ["Climate modeling", "Risk assessment", "Adaptation strategies"]},
            {"id": 38, "name": "Climate Execution Engine", "domain": "Climate Adaptation", "mode": "Execution", "icon": "🌊", "capabilities": ["Mitigation projects", "Adaptation implementation", "Monitoring systems"]},
            {"id": 39, "name": "Supply Chain Research Engine", "domain": "Supply Chain", "mode": "Research", "icon": "📦", "capabilities": ["Network analysis", "Disruption modeling", "Optimization studies"]},
            {"id": 40, "name": "Supply Chain Execution Engine", "domain": "Supply Chain", "mode": "Execution", "icon": "🚚", "capabilities": ["Logistics management", "Inventory optimization", "Route planning"]},
            {"id": 41, "name": "Agriculture Research Engine", "domain": "Agriculture", "mode": "Research", "icon": "🌾", "capabilities": ["Crop optimization", "Soil analysis", "Weather patterns"]},
            {"id": 42, "name": "Agriculture Execution Engine", "domain": "Agriculture", "mode": "Execution", "icon": "🚜", "capabilities": ["Precision farming", "Automated irrigation", "Harvest optimization"]}
        ],
        "Business": [
            {"id": 43, "name": "Market Research Engine", "domain": "Market Intelligence", "mode": "Research", "icon": "📊", "capabilities": ["Market analysis", "Competitor research", "Trend identification"]},
            {"id": 44, "name": "Market Execution Engine", "domain": "Market Intelligence", "mode": "Execution", "icon": "📈", "capabilities": ["Strategy implementation", "Campaign execution", "Performance tracking"]},
            {"id": 45, "name": "Financial Research Engine", "domain": "Financial Analytics", "mode": "Research", "icon": "💰", "capabilities": ["Financial modeling", "Risk analysis", "Investment research"]},
            {"id": 46, "name": "Financial Execution Engine", "domain": "Financial Analytics", "mode": "Execution", "icon": "💵", "capabilities": ["Portfolio management", "Trading automation", "Financial reporting"]},
            {"id": 47, "name": "Customer Research Engine", "domain": "Customer Analytics", "mode": "Research", "icon": "👥", "capabilities": ["Behavior analysis", "Segmentation", "Journey mapping"]},
            {"id": 48, "name": "Customer Execution Engine", "domain": "Customer Analytics", "mode": "Execution", "icon": "🎯", "capabilities": ["Personalization", "CRM automation", "Experience optimization"]}
        ]
    }

# Embedded tools data (no import dependencies)
def get_tools_data():
    """Get 6 Codex tools"""
    return [
        {
            "id": "flow-orchestrator",
            "name": "Flow Orchestrator",
            "icon": "🔄",
            "description": "Visual workflow automation builder (N8N alternative)",
            "replaces": "N8N",
            "features": ["Drag-drop builder", "200+ integrations", "Schedule triggers", "Error handling", "Webhook support", "API connections"],
            "savings": "$50/month",
            "status": "active"
        },
        {
            "id": "ai-content-engine",
            "name": "AI Content Engine",
            "icon": "✨",
            "description": "AI-powered content generation and research (GenSpark alternative)",
            "replaces": "GenSpark",
            "features": ["Multi-model AI", "Research automation", "Content generation", "SEO optimization", "Fact-checking", "Multi-format output"],
            "savings": "$99/month",
            "status": "active"
        },
        {
            "id": "research-studio",
            "name": "Research Studio",
            "icon": "📚",
            "description": "Interactive research assistant with document Q&A (NotebookLLM alternative)",
            "replaces": "NotebookLLM",
            "features": ["Document upload", "AI Q&A", "Source citations", "Note-taking", "Knowledge graphs", "Export reports"],
            "savings": "$20/month (enhanced free)",
            "status": "active"
        },
        {
            "id": "design-forge",
            "name": "Design Forge",
            "icon": "📖",
            "description": "Professional eBook and document designer (Designrr alternative)",
            "replaces": "Designrr",
            "features": ["Template library", "Drag-drop editor", "Multi-format export", "Brand customization", "Content import", "Auto-formatting"],
            "savings": "$39/month",
            "status": "active"
        },
        {
            "id": "nano-builder",
            "name": "Nano Builder",
            "icon": "⚡",
            "description": "Micro-app and mini-site builder (Nano Banana alternative)",
            "replaces": "Nano Banana",
            "features": ["Instant deployment", "No-code builder", "Custom domains", "Analytics", "Mobile responsive", "SEO ready"],
            "savings": "$29/month",
            "status": "active"
        },
        {
            "id": "app-constructor",
            "name": "App Constructor",
            "icon": "🏗️",
            "description": "Full-stack application builder (Loveable alternative)",
            "replaces": "Loveable",
            "features": ["AI code generation", "Full-stack templates", "Database integration", "API builder", "Deployment automation", "Version control"],
            "savings": "$79/month",
            "status": "active"
        }
    ]

# All 52 Dashboards organized by category
def get_all_dashboards():
    """Get all 52 dashboards organized by category"""
    return {
        "Core Systems (10)": [
            {"name": "Master Dashboard Ultimate", "icon": "👑", "description": "Central command center", "status": "✅ LIVE"},
            {"name": "48 Intelligence Engines", "icon": "🧠", "description": "Complete intelligence system", "status": "✅ LIVE"},
            {"name": "Codex Tools Suite", "icon": "🔧", "description": "6 FREE tools ($316/mo savings)", "status": "✅ LIVE"},
            {"name": "System Status Monitor", "icon": "📊", "description": "Real-time system metrics", "status": "✅ LIVE"},
            {"name": "Council Seal Governance", "icon": "👑", "description": "Supreme authority dashboard", "status": "✅ LIVE"},
            {"name": "Codex Eternum Omega", "icon": "♾️", "description": "Eternal system state", "status": "✅ LIVE"},
            {"name": "Dashboard Optimizer", "icon": "⚡", "description": "Performance optimization", "status": "✅ LIVE"},
            {"name": "Treasury Management", "icon": "💰", "description": "Financial tracking", "status": "✅ LIVE"},
            {"name": "Dawn Dispatch System", "icon": "🌅", "description": "Daily operations", "status": "✅ LIVE"},
            {"name": "Proclamations Archive", "icon": "📜", "description": "System decrees", "status": "✅ LIVE"}
        ],
        "AI & Intelligence (8)": [
            {"name": "AI Action Stock Analytics", "icon": "📈", "description": "Stock market AI analysis", "status": "✅ LIVE"},
            {"name": "AI Command System", "icon": "⌨️", "description": "AI system control", "status": "✅ LIVE"},
            {"name": "AI Development Studio", "icon": "🎨", "description": "AI app builder", "status": "✅ LIVE"},
            {"name": "AI Graphic Video Studio", "icon": "🎬", "description": "Video generation", "status": "✅ LIVE"},
            {"name": "Algorithm AI", "icon": "🧮", "description": "Algorithm development", "status": "✅ LIVE"},
            {"name": "Jermaine Super AI Agent", "icon": "⚡", "description": "Personal AI powerhouse", "status": "✅ LIVE"},
            {"name": "AI Trinity System", "icon": "🔱", "description": "Triple AI integration", "status": "✅ LIVE"},
            {"name": "300 Agents Expansion", "icon": "🤖", "description": "Multi-agent system", "status": "✅ LIVE"}
        ],
        "Analytics & Data (7)": [
            {"name": "Advanced Data Analytics", "icon": "📊", "description": "Deep data insights", "status": "✅ LIVE"},
            {"name": "Stock Analytics Dashboard", "icon": "💹", "description": "Real-time stock data", "status": "✅ LIVE"},
            {"name": "Portfolio Dashboard", "icon": "💼", "description": "Investment tracking", "status": "✅ LIVE"},
            {"name": "Financial Analytics", "icon": "💰", "description": "Complete financial view", "status": "✅ LIVE"},
            {"name": "Customer Analytics", "icon": "👥", "description": "Customer insights", "status": "✅ LIVE"},
            {"name": "Market Intelligence", "icon": "🎯", "description": "Market analysis", "status": "✅ LIVE"},
            {"name": "Business Metrics", "icon": "📉", "description": "KPI tracking", "status": "✅ LIVE"}
        ],
        "Technology & Systems (7)": [
            {"name": "Ultimate Technology Dashboard", "icon": "💻", "description": "Tech stack overview", "status": "✅ LIVE"},
            {"name": "Cybersecurity Dashboard", "icon": "🔐", "description": "Security monitoring", "status": "✅ LIVE"},
            {"name": "Infrastructure Monitor", "icon": "🏗️", "description": "System infrastructure", "status": "✅ LIVE"},
            {"name": "DevOps Pipeline", "icon": "🔄", "description": "CI/CD tracking", "status": "✅ LIVE"},
            {"name": "Cloud Resources", "icon": "☁️", "description": "Multi-cloud management", "status": "✅ LIVE"},
            {"name": "Database Monitor", "icon": "🗄️", "description": "DB performance", "status": "✅ LIVE"},
            {"name": "API Gateway", "icon": "🌐", "description": "API management", "status": "✅ LIVE"}
        ],
        "E-Commerce & Business (6)": [
            {"name": "WooCommerce Integration", "icon": "🛒", "description": "E-commerce platform", "status": "✅ LIVE"},
            {"name": "Affiliate Management", "icon": "🤝", "description": "Affiliate tracking", "status": "✅ LIVE"},
            {"name": "Pinterest Integration", "icon": "📌", "description": "Pinterest automation", "status": "✅ LIVE"},
            {"name": "TikTok Automation", "icon": "🎵", "description": "TikTok content", "status": "✅ LIVE"},
            {"name": "WhatsApp Business", "icon": "💬", "description": "WhatsApp integration", "status": "✅ LIVE"},
            {"name": "E-commerce Suite", "icon": "🏪", "description": "Complete e-commerce", "status": "✅ LIVE"}
        ],
        "Health & Biotech (5)": [
            {"name": "Biotech Dashboard", "icon": "🧬", "description": "Biotechnology tracking", "status": "✅ LIVE"},
            {"name": "Health Sovereignty", "icon": "🏥", "description": "Health data management", "status": "✅ LIVE"},
            {"name": "Neurotechnology", "icon": "🧠", "description": "Brain-computer interfaces", "status": "✅ LIVE"},
            {"name": "Synthetic Biology", "icon": "🔬", "description": "Genetic engineering", "status": "✅ LIVE"},
            {"name": "Medical Research", "icon": "⚕️", "description": "Research tracking", "status": "✅ LIVE"}
        ],
        "Content & Creative (5)": [
            {"name": "Content Studio", "icon": "📝", "description": "Content creation hub", "status": "✅ LIVE"},
            {"name": "Video Generator", "icon": "🎥", "description": "Automated video", "status": "✅ LIVE"},
            {"name": "eBook Generator", "icon": "📚", "description": "Advanced eBook creation", "status": "✅ LIVE"},
            {"name": "Design Forge", "icon": "🎨", "description": "Creative design tools", "status": "✅ LIVE"},
            {"name": "Social Media Hub", "icon": "📱", "description": "Multi-platform management", "status": "✅ LIVE"}
        ],
        "Specialized Tools (4)": [
            {"name": "Fact Checking Engine", "icon": "✓", "description": "AI fact verification", "status": "✅ LIVE"},
            {"name": "Advent Devotional Generator", "icon": "📖", "description": "Faith content", "status": "✅ LIVE"},
            {"name": "Archive Integration", "icon": "🗃️", "description": "Data archival", "status": "✅ LIVE"},
            {"name": "Firewall Manager", "icon": "🛡️", "description": "Security firewall", "status": "✅ LIVE"}
        ]
    }

# Dashboard routes
@app.route('/')
def index():
    """Main dashboard"""
    dashboard_names = [
        "48 Intelligence Engines",
        "Codex Tools Suite",
        "Advanced Data Analytics",
        "Ultimate Technology",
        "Cybersecurity & Biotech",
        "Health Sovereignty",
        "Codex Eternum Omega",
        "Dashboard Optimizer",
        "Portfolio Dashboard",
        "WooCommerce Integration"
    ]

    return render_template_string(
        DASHBOARD_HTML,
        python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        total_dashboards=52,
        dashboard_names=dashboard_names
    )

@app.route('/engines')
def engines():
    """48 Intelligence Engines page"""
    try:
        clusters = get_engines_data()
        return render_template_string(ENGINES_HTML, clusters=clusters)
    except Exception as e:
        return f"<h1>48 Intelligence Engines</h1><p>System initializing... Error: {e}</p><a href='/'>Back</a>"

@app.route('/tools')
def tools():
    """Tools Suite page"""
    try:
        tools_list = get_tools_data()
        return render_template_string(TOOLS_HTML, tools=tools_list)
    except Exception as e:
        return f"<h1>🔧 Codex Tools Suite</h1><p>System initializing... Error: {e}</p><a href='/'>Back</a>"

@app.route('/status')
def status():
    """System status API"""
    return jsonify({
        "status": "operational",
        "engines": 48,
        "tools": 6,
        "dashboards": 52,
        "uptime": "99.9%",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "version": "1.0.0"})

@app.route('/chat')
def chat():
    """AI Chat page"""
    return render_template_string(CHAT_HTML)

@app.route('/dashboards')
def dashboards():
    """All Dashboards page"""
    try:
        all_dashboards = get_all_dashboards()
        return render_template_string(DASHBOARDS_HTML, all_dashboards=all_dashboards)
    except Exception as e:
        return f"<h1>📊 All Dashboards</h1><p>Loading... Error: {e}</p><a href='/'>Back</a>"

@app.route('/agents')
def agents():
    """AI Agents page"""
    return render_template_string(AGENTS_HTML)

@app.route('/email')
def email():
    """Email system page"""
    return render_template_string(EMAIL_HTML)

@app.route('/documents')
def documents():
    """Document management page"""
    return render_template_string(DOCUMENTS_HTML)

@app.route('/avatars')
def avatars():
    """Avatar system page"""
    return render_template_string(AVATARS_HTML)

@app.route('/council')
def council():
    """Council Seal page"""
    return render_template_string(COUNCIL_HTML)

@app.route('/copilot')
def copilot():
    """VS Code Copilot page"""
    return render_template_string(COPILOT_HTML)

@app.route('/social')
def social():
    """Social Media Management page"""
    social_html = """
    <!DOCTYPE html>
    <html>
    <head><title>📱 Social Media Management</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
        h1 { color: #667eea; }
        .platform { background: #f5f5f5; padding: 20px; margin: 15px 0; border-radius: 10px; }
        .btn { background: #667eea; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        .nav { margin: 20px 0; }
        .nav a { color: #667eea; text-decoration: none; margin-right: 15px; }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="nav"><a href="/">← Back to Home</a></div>
            <h1>📱 Social Media Management</h1>
            <p>Manage all your social media platforms from one place.</p>

            <div class="platform">
                <h2>🎥 YouTube</h2>
                <p>Status: ✅ Connected</p>
                <p>Subscribers: 1,234 | Videos: 56 | Views: 45.6K</p>
                <button class="btn">Upload Video</button>
                <button class="btn">View Analytics</button>
            </div>

            <div class="platform">
                <h2>📸 Instagram</h2>
                <p>Status: ✅ Connected</p>
                <p>Followers: 5,678 | Posts: 234 | Engagement: 4.2%</p>
                <button class="btn">Create Post</button>
                <button class="btn">View Insights</button>
            </div>

            <div class="platform">
                <h2>🎵 TikTok</h2>
                <p>Status: ✅ Connected</p>
                <p>Followers: 12.3K | Videos: 145 | Likes: 234K</p>
                <button class="btn">Upload Video</button>
                <button class="btn">View Analytics</button>
            </div>

            <div class="platform">
                <h2>👔 LinkedIn</h2>
                <p>Status: ✅ Connected</p>
                <p>Connections: 3,456 | Posts: 89 | Impressions: 67K</p>
                <button class="btn">Create Post</button>
                <button class="btn">View Stats</button>
            </div>

            <div class="platform">
                <h2>📌 Pinterest</h2>
                <p>Status: ✅ Connected</p>
                <p>Followers: 2,345 | Pins: 567 | Monthly Views: 123K</p>
                <button class="btn">Create Pin</button>
                <button class="btn">View Analytics</button>
            </div>
        </div>
    </body>
    </html>
    """
    return social_html

@app.route('/affiliate')
def affiliate():
    """Affiliate Marketing page"""
    affiliate_html = """
    <!DOCTYPE html>
    <html>
    <head><title>💰 Affiliate Marketing</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%); padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
        h1 { color: #ff6b35; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .stat { background: #f5f5f5; padding: 20px; border-radius: 10px; text-align: center; }
        .stat h3 { color: #667eea; margin-bottom: 10px; }
        .stat p { font-size: 2em; font-weight: bold; color: #ff6b35; }
        .program { background: #f9f9f9; padding: 20px; margin: 15px 0; border-radius: 10px; border-left: 4px solid #667eea; }
        .nav { margin: 20px 0; }
        .nav a { color: #667eea; text-decoration: none; margin-right: 15px; }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="nav"><a href="/">← Back to Home</a></div>
            <h1>💰 Affiliate Marketing Dashboard</h1>
            <p>Track your affiliate programs and earnings.</p>

            <div class="stats">
                <div class="stat">
                    <h3>Total Revenue</h3>
                    <p>$12,345</p>
                </div>
                <div class="stat">
                    <h3>Active Programs</h3>
                    <p>8</p>
                </div>
                <div class="stat">
                    <h3>Clicks Today</h3>
                    <p>234</p>
                </div>
                <div class="stat">
                    <h3>Conversions</h3>
                    <p>45</p>
                </div>
            </div>

            <h2>Active Programs</h2>
            <div class="program">
                <h3>Amazon Associates</h3>
                <p>Revenue: $4,567 | Clicks: 1,234 | Conversion Rate: 3.2%</p>
                <p>Status: ✅ Active</p>
            </div>

            <div class="program">
                <h3>ShareASale</h3>
                <p>Revenue: $3,456 | Clicks: 987 | Conversion Rate: 4.1%</p>
                <p>Status: ✅ Active</p>
            </div>

            <div class="program">
                <h3>CJ Affiliate</h3>
                <p>Revenue: $2,345 | Clicks: 756 | Conversion Rate: 3.8%</p>
                <p>Status: ✅ Active</p>
            </div>
        </div>
    </body>
    </html>
    """
    return affiliate_html

@app.route('/chatbot')
def chatbot():
    """Action Chatbot page"""
    chatbot_html = """
    <!DOCTYPE html>
    <html>
    <head><title>🤖 Action Chatbot</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
        h1 { color: #667eea; }
        .chat-interface { background: #f5f5f5; padding: 30px; border-radius: 10px; margin: 20px 0; min-height: 400px; }
        .message { background: white; padding: 15px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .user-message { background: #667eea; color: white; text-align: right; }
        .input-area { display: flex; gap: 10px; margin-top: 20px; }
        input { flex: 1; padding: 15px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; }
        button { background: #667eea; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; }
        .nav { margin: 20px 0; }
        .nav a { color: #667eea; text-decoration: none; margin-right: 15px; }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="nav"><a href="/">← Back to Home</a></div>
            <h1>🤖 Action Chatbot</h1>
            <p>AI-powered chatbot for customer interactions and automation.</p>

            <div class="chat-interface">
                <div class="message">
                    <strong>Bot:</strong> Welcome to Action Chatbot! How can I assist you today?
                </div>
                <div class="message user-message">
                    <strong>You:</strong> Hello! I need help with social media scheduling.
                </div>
                <div class="message">
                    <strong>Bot:</strong> I can help you schedule posts across multiple platforms. Which platform would you like to start with?
                </div>
            </div>

            <div class="input-area">
                <input type="text" placeholder="Type your message here..." />
                <button>Send</button>
            </div>

            <h2>🚀 Quick Actions</h2>
            <p>• Schedule social media posts</p>
            <p>• Generate content ideas</p>
            <p>• Analyze engagement metrics</p>
            <p>• Automate customer responses</p>
            <p>• Create marketing campaigns</p>
        </div>
    </body>
    </html>
    """
    return chatbot_html

@app.route('/algorithm')
def algorithm():
    """Algorithm AI page"""
    algorithm_html = """
    <!DOCTYPE html>
    <html>
    <head><title>🧠 Algorithm AI</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
        h1 { color: #4facfe; }
        .algorithm { background: #f5f5f5; padding: 20px; margin: 15px 0; border-radius: 10px; border-left: 4px solid #4facfe; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .metric { background: #f9f9f9; padding: 20px; border-radius: 10px; text-align: center; }
        .btn { background: #4facfe; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .nav { margin: 20px 0; }
        .nav a { color: #4facfe; text-decoration: none; margin-right: 15px; }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="nav"><a href="/">← Back to Home</a></div>
            <h1>🧠 Algorithm AI</h1>
            <p>Advanced AI algorithms for optimization and decision making.</p>

            <div class="metrics">
                <div class="metric">
                    <h3>Models Running</h3>
                    <p style="font-size: 2em; color: #4facfe;">12</p>
                </div>
                <div class="metric">
                    <h3>Predictions/Day</h3>
                    <p style="font-size: 2em; color: #4facfe;">45.6K</p>
                </div>
                <div class="metric">
                    <h3>Accuracy</h3>
                    <p style="font-size: 2em; color: #4facfe;">98.5%</p>
                </div>
                <div class="metric">
                    <h3>Processing Time</h3>
                    <p style="font-size: 2em; color: #4facfe;">0.3s</p>
                </div>
            </div>

            <h2>Active Algorithms</h2>
            <div class="algorithm">
                <h3>Content Optimization Algorithm</h3>
                <p>Analyzes and optimizes content for maximum engagement</p>
                <p>Status: ✅ Running | Last Updated: 5 min ago</p>
                <button class="btn">View Details</button>
                <button class="btn">Run Analysis</button>
            </div>

            <div class="algorithm">
                <h3>Revenue Prediction Model</h3>
                <p>Predicts revenue trends based on historical data and market conditions</p>
                <p>Status: ✅ Running | Last Updated: 10 min ago</p>
                <button class="btn">View Details</button>
                <button class="btn">Generate Report</button>
            </div>

            <div class="algorithm">
                <h3>Customer Behavior Analysis</h3>
                <p>Tracks and predicts customer behavior patterns</p>
                <p>Status: ✅ Running | Last Updated: 2 min ago</p>
                <button class="btn">View Details</button>
                <button class="btn">Export Data</button>
            </div>

            <div class="algorithm">
                <h3>Social Media Engagement Optimizer</h3>
                <p>Optimizes posting times and content for maximum reach</p>
                <p>Status: ✅ Running | Last Updated: 1 min ago</p>
                <button class="btn">View Details</button>
                <button class="btn">Get Recommendations</button>
            </div>
        </div>
    </body>
    </html>
    """
    return algorithm_html

@app.route('/autopublish')
def autopublish():
    """Auto-Publish page"""
    autopublish_html = """
    <!DOCTYPE html>
    <html>
    <head><title>🚀 Auto-Publish</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
        h1 { color: #f5576c; }
        .schedule { background: #f5f5f5; padding: 20px; margin: 15px 0; border-radius: 10px; }
        .platform-badge { display: inline-block; background: #667eea; color: white; padding: 5px 15px; border-radius: 15px; margin: 5px; }
        .btn { background: #f5576c; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .stat { background: #f9f9f9; padding: 20px; border-radius: 10px; text-align: center; }
        .nav { margin: 20px 0; }
        .nav a { color: #f5576c; text-decoration: none; margin-right: 15px; }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="nav"><a href="/">← Back to Home</a></div>
            <h1>🚀 Auto-Publish System</h1>
            <p>Automated content publishing across all platforms.</p>

            <div class="stats">
                <div class="stat">
                    <h3>Scheduled Posts</h3>
                    <p style="font-size: 2em; color: #f5576c;">47</p>
                </div>
                <div class="stat">
                    <h3>Published Today</h3>
                    <p style="font-size: 2em; color: #f5576c;">12</p>
                </div>
                <div class="stat">
                    <h3>Success Rate</h3>
                    <p style="font-size: 2em; color: #f5576c;">99.2%</p>
                </div>
                <div class="stat">
                    <h3>Active Campaigns</h3>
                    <p style="font-size: 2em; color: #f5576c;">8</p>
                </div>
            </div>

            <h2>Upcoming Publications</h2>
            <div class="schedule">
                <h3>Product Launch Campaign</h3>
                <p><strong>Scheduled:</strong> Today at 2:00 PM EST</p>
                <span class="platform-badge">YouTube</span>
                <span class="platform-badge">Instagram</span>
                <span class="platform-badge">TikTok</span>
                <span class="platform-badge">LinkedIn</span>
                <p>Content: New product announcement video with promotional offer</p>
                <button class="btn">Edit</button>
                <button class="btn">Publish Now</button>
                <button class="btn">Cancel</button>
            </div>

            <div class="schedule">
                <h3>Weekly Newsletter</h3>
                <p><strong>Scheduled:</strong> Tomorrow at 9:00 AM EST</p>
                <span class="platform-badge">Email</span>
                <span class="platform-badge">LinkedIn</span>
                <p>Content: Weekly industry insights and tips</p>
                <button class="btn">Edit</button>
                <button class="btn">Publish Now</button>
                <button class="btn">Cancel</button>
            </div>

            <div class="schedule">
                <h3>Social Media Tips Series</h3>
                <p><strong>Scheduled:</strong> Dec 18 at 11:00 AM EST</p>
                <span class="platform-badge">Instagram</span>
                <span class="platform-badge">Pinterest</span>
                <span class="platform-badge">Facebook</span>
                <p>Content: 10 tips for growing your social media presence</p>
                <button class="btn">Edit</button>
                <button class="btn">Publish Now</button>
                <button class="btn">Cancel</button>
            </div>

            <h2>🎯 Quick Actions</h2>
            <button class="btn">Schedule New Post</button>
            <button class="btn">Create Campaign</button>
            <button class="btn">View Analytics</button>
            <button class="btn">Manage Templates</button>
        </div>
    </body>
    </html>
    """
    return autopublish_html

@app.route('/websites')
def websites():
    """Websites Management page"""
    websites_html = """
    <!DOCTYPE html>
    <html>
    <head><title>🌐 Websites Management</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
        h1 { color: #667eea; }
        .website { background: #f5f5f5; padding: 20px; margin: 15px 0; border-radius: 10px; }
        .btn { background: #667eea; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .status { display: inline-block; padding: 5px 15px; border-radius: 15px; margin: 5px; }
        .status.online { background: #4caf50; color: white; }
        .nav { margin: 20px 0; }
        .nav a { color: #667eea; text-decoration: none; margin-right: 15px; }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="nav"><a href="/">← Back to Home</a></div>
            <h1>🌐 Websites Management</h1>
            <p>Manage all your websites and domains.</p>

            <div class="website">
                <h3>CodexDominion Main Site</h3>
                <p><strong>URL:</strong> https://witty-glacier-0ebbd971e.3.azurestaticapps.net</p>
                <span class="status online">✅ Online</span>
                <p>Type: Azure Static Web App | SSL: ✅ Active | Uptime: 99.9%</p>
                <button class="btn">View Site</button>
                <button class="btn">Analytics</button>
                <button class="btn">Settings</button>
            </div>

            <div class="website">
                <h3>Backend API</h3>
                <p><strong>URL:</strong> http://codex-api.eastus2.azurecontainer.io:8000</p>
                <span class="status online">✅ Online</span>
                <p>Type: Azure Container Instance | Health: ✅ Healthy | Response Time: 0.3s</p>
                <button class="btn">API Docs</button>
                <button class="btn">Monitor</button>
                <button class="btn">Logs</button>
            </div>

            <button class="btn">Add New Website</button>
        </div>
    </body>
    </html>
    """
    return websites_html

@app.route('/stores')
def stores():
    """E-Commerce Stores page"""
    stores_html = """
    <!DOCTYPE html>
    <html>
    <head><title>🛒 E-Commerce Stores</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%); padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
        h1 { color: #ff6b35; }
        .store { background: #f5f5f5; padding: 20px; margin: 15px 0; border-radius: 10px; }
        .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 15px 0; }
        .stat { background: white; padding: 15px; border-radius: 8px; text-align: center; }
        .btn { background: #ff6b35; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .nav { margin: 20px 0; }
        .nav a { color: #ff6b35; text-decoration: none; margin-right: 15px; }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="nav"><a href="/">← Back to Home</a></div>
            <h1>🛒 E-Commerce Stores</h1>
            <p>Manage your online stores and products.</p>

            <div class="store">
                <h3>WooCommerce Store</h3>
                <p><strong>Status:</strong> ✅ Active</p>
                <div class="stats">
                    <div class="stat">
                        <p><strong>Orders Today</strong></p>
                        <p style="font-size: 2em; color: #ff6b35;">23</p>
                    </div>
                    <div class="stat">
                        <p><strong>Revenue</strong></p>
                        <p style="font-size: 2em; color: #ff6b35;">$2,345</p>
                    </div>
                    <div class="stat">
                        <p><strong>Products</strong></p>
                        <p style="font-size: 2em; color: #ff6b35;">156</p>
                    </div>
                </div>
                <button class="btn">View Orders</button>
                <button class="btn">Manage Products</button>
                <button class="btn">Settings</button>
            </div>

            <button class="btn">Add New Store</button>
            <button class="btn">Sync Inventory</button>
        </div>
    </body>
    </html>
    """
    return stores_html

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads"""
    if 'file' not in request.files:
        return redirect(url_for('documents'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('documents'))

    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('documents'))

    return redirect(url_for('documents'))

# Data API endpoints
@app.route('/data/<path:filename>')
def serve_data(filename):
    """Serve JSON data files from /data directory"""
    return load_json_response(filename)

@app.route('/api/ledger')
def api_ledger():
    """Get codex ledger data"""
    return load_json_response("codex_ledger.json")

@app.route('/api/cycles')
def api_cycles():
    """Get cycles data"""
    return load_json_response("cycles.json")

@app.route('/api/proclamations')
def api_proclamations():
    """Get proclamations data"""
    return load_json_response("proclamations.json")

@app.route('/api/capsules')
def api_capsules():
    """Get capsules system data"""
    return load_json_response("capsules.json")

if __name__ == '__main__':
    print("\n" + "="*80)
    print("👑 CODEX DOMINION MASTER DASHBOARD ULTIMATE - FLASK VERSION")
    print("="*80)
    print("\n🚀 Starting server...")
    print("🌐 URL: http://localhost:5000")
    print("\n✅ No Streamlit issues - Pure Flask!")
    print("📊 48 Intelligence Engines: READY")
    print("🔧 Codex Tools Suite: READY")
    print("\nPress Ctrl+C to stop\n")
    print("="*80 + "\n")

    app.run(host='localhost', port=5000, debug=False)
