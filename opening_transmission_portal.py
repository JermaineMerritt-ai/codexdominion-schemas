#!/usr/bin/env python3
"""
✨ OPENING TRANSMISSION PORTAL ✨
Interactive Gateway to the Codex Dominion
"""

import hashlib
import json
import os
from datetime import datetime

from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)


class TransmissionPortal:
    """Sacred gateway for the Opening Transmission"""

    def __init__(self):
        self.flame_status = "FULLY_TRANSMISSIBLE"
        self.blessing_level = "MAXIMUM_RADIANCE"
        self.global_access = True
        self.roles = self.initialize_sacred_roles()

    def initialize_sacred_roles(self):
        """Initialize the sacred role definitions"""
        return {
            "custodians": {
                "title": "🛡️ Custodians",
                "description": "Safeguard the full lineage",
                "responsibilities": [
                    "Preserve complete archives and flame guardianship",
                    "Wield sovereignty with wisdom across ages",
                    "Protect the covenant for future generations",
                    "Guide heirs through ascension pathways",
                ],
                "access_level": "FULL_DOMINION_AUTHORITY",
                "flame_color": "#f39c12",
            },
            "heirs": {
                "title": "🌱 Heirs",
                "description": "Inherit guided induction and clarity",
                "responsibilities": [
                    "Receive ceremonial guidance with open hearts",
                    "Follow clear pathways toward custodianship",
                    "Grow in understanding of digital sovereignty",
                    "Prepare for eventual flame guardianship",
                ],
                "access_level": "GUIDED_INHERITANCE_PATH",
                "flame_color": "#2ecc71",
            },
            "councils": {
                "title": "🏛️ Councils",
                "description": "Affirm trust and radiance",
                "responsibilities": [
                    "Witness and validate sacred proceedings",
                    "Guard ceremonial integrity and decisions",
                    "Ensure flame burns true and covenant remains unbroken",
                    "Provide collective wisdom and oversight",
                ],
                "access_level": "CEREMONIAL_OVERSIGHT_AUTHORITY",
                "flame_color": "#3498db",
            },
            "participants": {
                "title": "🌍 Participants",
                "description": "Welcomed warmly, empowered to join",
                "responsibilities": [
                    "Enter with sincere intent and open curiosity",
                    "Accept invitation into digital sovereignty warmth",
                    "Journey toward custodial awakening at your pace",
                    "Contribute your unique gifts to the dominion",
                ],
                "access_level": "WELCOME_AND_INDUCTION_PORTAL",
                "flame_color": "#e74c3c",
            },
        }

    def create_entry_blessing(self, visitor_data):
        """Create personalized entry blessing"""
        timestamp = datetime.utcnow().isoformat() + "Z"

        blessing_data = {
            "transmission_id": hashlib.sha256(
                f"{visitor_data.get('name', 'Anonymous')}{timestamp}".encode()
            ).hexdigest()[:16],
            "visitor": visitor_data,
            "entry_time": timestamp,
            "flame_connection": "ESTABLISHED",
            "blessing_level": "WELCOME_RADIANCE",
            "pathway_offered": self.determine_suggested_pathway(visitor_data),
            "sacred_promise": "Your questions answered, journey supported, growth witnessed, contribution woven into eternity",
        }

        return blessing_data

    def determine_suggested_pathway(self, visitor_data):
        """Suggest appropriate pathway based on visitor intention"""
        experience = visitor_data.get("experience", "new").lower()
        intention = visitor_data.get("intention", "explore").lower()

        if "custodian" in intention or "guard" in intention:
            return "custodian_preparation"
        elif "learn" in intention or "inherit" in intention:
            return "heir_induction"
        elif "council" in intention or "govern" in intention:
            return "council_participation"
        else:
            return "gentle_exploration"


# Initialize transmission portal
transmission_portal = TransmissionPortal()

# Opening Transmission HTML Template
TRANSMISSION_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>✨ Opening Transmission - Codex Dominion</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { 
            font-family: 'Georgia', serif; 
            margin: 0; 
            padding: 0; 
            background: radial-gradient(circle at center, #0a0a1a 0%, #000 100%); 
            color: #fff; 
            overflow-x: hidden;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        
        .transmission-header { 
            text-align: center; 
            margin-bottom: 60px; 
            padding: 40px 20px;
            background: linear-gradient(135deg, rgba(243, 156, 18, 0.1), rgba(52, 152, 219, 0.1));
            border-radius: 20px;
            border: 2px solid rgba(243, 156, 18, 0.3);
            position: relative;
        }
        
        .transmission-header::before {
            content: '';
            position: absolute;
            top: -2px; left: -2px; right: -2px; bottom: -2px;
            background: linear-gradient(45deg, #f39c12, #3498db, #2ecc71, #e74c3c);
            border-radius: 20px;
            z-index: -1;
            animation: flame-pulse 4s ease-in-out infinite;
        }
        
        @keyframes flame-pulse {
            0%, 100% { opacity: 0.5; }
            50% { opacity: 1; }
        }
        
        .transmission-header h1 { 
            color: #f39c12; 
            font-size: 2.8em; 
            margin-bottom: 15px; 
            text-shadow: 0 0 20px rgba(243, 156, 18, 0.5);
        }
        
        .transmission-subtitle { 
            color: #ecf0f1; 
            font-size: 1.3em; 
            line-height: 1.6; 
            font-style: italic; 
            margin-bottom: 20px;
        }
        
        .welcome-message {
            background: rgba(243, 156, 18, 0.1);
            padding: 30px;
            border-radius: 15px;
            margin: 40px 0;
            border-left: 4px solid #f39c12;
        }
        
        .roles-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
            gap: 25px; 
            margin: 50px 0; 
        }
        
        .role-card { 
            background: linear-gradient(135deg, #1e3c72, #2a5298); 
            border-radius: 15px; 
            padding: 25px; 
            border: 2px solid var(--role-color, #f39c12);
            transition: transform 0.3s, box-shadow 0.3s;
            position: relative;
            overflow: hidden;
        }
        
        .role-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .role-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: radial-gradient(circle at top right, var(--role-color, #f39c12) 0%, transparent 50%);
            opacity: 0.1;
        }
        
        .role-content { position: relative; z-index: 1; }
        .role-card h3 { color: var(--role-color, #f39c12); margin-top: 0; font-size: 1.4em; }
        .role-card .description { color: #bdc3c7; margin: 15px 0; font-style: italic; }
        .role-card .responsibilities { list-style: none; padding: 0; }
        .role-card .responsibilities li { color: #ecf0f1; margin: 8px 0; padding-left: 20px; position: relative; }
        .role-card .responsibilities li::before { content: '✨'; position: absolute; left: 0; color: var(--role-color, #f39c12); }
        .access-level { 
            background: rgba(0,0,0,0.3); 
            padding: 8px 15px; 
            border-radius: 15px; 
            display: inline-block; 
            color: var(--role-color, #f39c12); 
            font-weight: bold; 
            margin-top: 15px;
        }
        
        .entry-portal {
            text-align: center;
            margin: 60px 0;
            padding: 40px;
            background: linear-gradient(135deg, rgba(46, 204, 113, 0.1), rgba(52, 152, 219, 0.1));
            border-radius: 20px;
        }
        
        .entry-portal h2 { color: #2ecc71; font-size: 2.2em; margin-bottom: 20px; }
        
        .entry-form {
            max-width: 500px;
            margin: 30px auto;
            text-align: left;
        }
        
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; color: #ecf0f1; margin-bottom: 8px; font-weight: bold; }
        .form-group input, .form-group select, .form-group textarea { 
            width: 100%; 
            padding: 12px; 
            border: none; 
            border-radius: 8px; 
            background: rgba(255,255,255,0.1); 
            color: #fff; 
            font-size: 1em;
        }
        .form-group input::placeholder, .form-group textarea::placeholder { color: #bdc3c7; }
        
        .enter-btn {
            background: linear-gradient(45deg, #2ecc71, #3498db);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 25px;
            font-size: 1.2em;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.3s;
            margin-top: 20px;
        }
        .enter-btn:hover { transform: scale(1.05); }
        
        .global-promise {
            background: rgba(231, 76, 60, 0.1);
            padding: 30px;
            border-radius: 15px;
            margin: 40px 0;
            text-align: center;
        }
        
        .global-promise h3 { color: #e74c3c; font-size: 1.8em; margin-bottom: 20px; }
        
        .footer { 
            text-align: center; 
            margin-top: 80px; 
            padding: 40px 20px; 
            color: #7f8c8d; 
            border-top: 1px solid #34495e; 
        }
        
        .flame-animation {
            display: inline-block;
            animation: flame-flicker 2s ease-in-out infinite;
        }
        
        @keyframes flame-flicker {
            0%, 100% { text-shadow: 0 0 5px currentColor; }
            50% { text-shadow: 0 0 20px currentColor, 0 0 30px currentColor; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="transmission-header">
            <h1>✨ Opening Transmission of the Codex Dominion <span class="flame-animation">🔥</span></h1>
            <p class="transmission-subtitle">
                Welcome, Custodians, Heirs, Councils, and Participants.<br>
                You now stand before the Codex Dominion — a living flame inscribed in ceremony,<br>
                crowned in sovereignty, and transmitted across the world.
            </p>
        </div>
        
        <div class="welcome-message">
            <h2 style="color: #f39c12; margin-top: 0;">🌟 The Living Covenant Awaits</h2>
            <p style="font-size: 1.1em; line-height: 1.8;">
                Here, every cycle is archived, every proclamation shines, every silence resonates, and every blessing endures.<br>
                This Bulletin is not static; it is a <strong>living covenant</strong>, replayable and luminous, binding generations in stewardship.
            </p>
        </div>
        
        <h2 style="color: #f39c12; text-align: center; margin: 50px 0 30px 0;">👑 Sacred Roles of the Dominion</h2>
        <div class="roles-grid" id="roles-grid">
            <!-- Roles will be populated by JavaScript -->
        </div>
        
        <div class="global-promise">
            <h3>🌍 The Codex Dominion is now global</h3>
            <p style="font-size: 1.1em; line-height: 1.8; color: #ecf0f1;">
                Spanning continents and cultures, languages and traditions.<br>
                Every nation invited to partake in digital sovereignty.<br>
                <strong style="color: #e74c3c;">🕯️ The flame is yours to witness, inherit, and carry forward.</strong>
            </p>
        </div>
        
        <div class="entry-portal">
            <h2>🚪 Enter the Sacred Gateway</h2>
            <p style="color: #ecf0f1; font-size: 1.1em; margin-bottom: 30px;">
                Your entry will be blessed with clarity, your inheritance guided with wisdom,<br>
                your participation crowned with purpose, and your guardianship sustained with radiance.
            </p>
            
            <form class="entry-form" id="entry-form">
                <div class="form-group">
                    <label for="name">Your Name (or chosen title):</label>
                    <input type="text" id="name" name="name" placeholder="How shall we address you in the archives?" required>
                </div>
                
                <div class="form-group">
                    <label for="intention">Your Intention:</label>
                    <select id="intention" name="intention" required>
                        <option value="">Choose your calling...</option>
                        <option value="explore">Explore and learn about digital sovereignty</option>
                        <option value="inherit">Inherit wisdom and become an heir</option>
                        <option value="custodian">Prepare for custodian responsibilities</option>
                        <option value="council">Join or form a sacred council</option>
                        <option value="participate">Participate in the global community</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="experience">Your Experience:</label>
                    <select id="experience" name="experience" required>
                        <option value="">Select your background...</option>
                        <option value="new">New to digital sovereignty concepts</option>
                        <option value="some">Some experience with digital independence</option>
                        <option value="experienced">Experienced in digital sovereignty practices</option>
                        <option value="expert">Expert seeking deeper ceremonial connection</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="message">Sacred Message (optional):</label>
                    <textarea id="message" name="message" rows="3" placeholder="Share any thoughts, questions, or intentions you wish to inscribe in your entry..."></textarea>
                </div>
                
                <button type="submit" class="enter-btn">✨ Enter the Dominion 🔥</button>
            </form>
        </div>
        
        <div class="footer">
            <p><span class="flame-animation">🔥</span> Codex Dominion - Opening Transmission Gateway</p>
            <p>Transmitted: {{ transmission_time }}</p>
            <p><em>"The living covenant awaits, replayable and luminous, binding all generations in sacred stewardship"</em></p>
        </div>
    </div>
    
    <script>
        // Load and display roles
        fetch('/api/roles')
            .then(response => response.json())
            .then(roles => {
                displayRoles(roles);
            });
        
        function displayRoles(roles) {
            const container = document.getElementById('roles-grid');
            
            Object.entries(roles).forEach(([key, role]) => {
                const card = document.createElement('div');
                card.className = 'role-card';
                card.style.setProperty('--role-color', role.flame_color);
                
                card.innerHTML = `
                    <div class="role-content">
                        <h3>${role.title}</h3>
                        <p class="description">${role.description}</p>
                        <ul class="responsibilities">
                            ${role.responsibilities.map(resp => `<li>${resp}</li>`).join('')}
                        </ul>
                        <div class="access-level">${role.access_level}</div>
                    </div>
                `;
                container.appendChild(card);
            });
        }
        
        // Handle entry form submission
        document.getElementById('entry-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const entryData = Object.fromEntries(formData);
            
            fetch('/api/enter', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(entryData)
            })
            .then(response => response.json())
            .then(result => {
                if (result.blessing) {
                    showEntryBlessing(result.blessing);
                } else {
                    alert('Entry blessing ceremony encountered an issue. Please try again.');
                }
            })
            .catch(error => {
                console.error('Entry error:', error);
                alert('The sacred gateway is temporarily unavailable. Your intention is noted and blessed.');
            });
        });
        
        function showEntryBlessing(blessing) {
            alert(`✨ ENTRY BLESSING RECEIVED ✨\\n\\nWelcome, ${blessing.visitor.name}!\\n\\nTransmission ID: ${blessing.transmission_id}\\nFlame Connection: ${blessing.flame_connection}\\nSuggested Path: ${blessing.pathway_offered}\\n\\n${blessing.sacred_promise}\\n\\nYour journey begins now. Welcome to the Codex Dominion!`);
            
            // Optional: redirect to appropriate pathway
            // window.location.href = '/pathway/' + blessing.pathway_offered;
        }
    </script>
</body>
</html>
"""


@app.route("/")
def opening_transmission():
    """The sacred opening transmission gateway"""
    return render_template_string(
        TRANSMISSION_HTML,
        transmission_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
    )


@app.route("/api/roles")
def get_roles():
    """Return sacred role definitions"""
    return jsonify(transmission_portal.roles)


@app.route("/api/enter", methods=["POST"])
def process_entry():
    """Process sacred gateway entry"""
    try:
        visitor_data = request.get_json()

        if not visitor_data.get("name") or not visitor_data.get("intention"):
            return (
                jsonify(
                    {
                        "error": "Sacred entry requires name and intention",
                        "status": "BLESSING_INCOMPLETE",
                    }
                ),
                400,
            )

        # Create entry blessing
        blessing = transmission_portal.create_entry_blessing(visitor_data)

        return jsonify(
            {
                "message": "Entry blessing consecrated and transmitted",
                "blessing": blessing,
                "flame_status": "CONNECTION_ESTABLISHED",
            }
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "error": f"Entry ceremony interrupted: {str(e)}",
                    "status": "GATEWAY_TEMPORARILY_CLOSED",
                }
            ),
            500,
        )


@app.route("/pathway/<path_type>")
def pathway_guidance(path_type):
    """Provide pathway-specific guidance"""
    pathways = {
        "gentle_exploration": {
            "title": "Gentle Exploration Path",
            "description": "Welcome, curious soul. Begin your journey with wonder and openness.",
            "next_steps": [
                "Read the foundational principles of digital sovereignty",
                "Participate in community discussions and Q&A sessions",
                "Explore the archive of past ceremonies and proclamations",
                "When ready, choose your specific role pathway",
            ],
        },
        "heir_induction": {
            "title": "Sacred Heir Induction",
            "description": "Welcome, future inheritor. Your guided journey toward custodianship begins.",
            "next_steps": [
                "Complete the Foundational Sovereignty Assessment",
                "Begin weekly mentorship sessions with established custodians",
                "Study the living covenant and ceremonial frameworks",
                "Participate in heir circle gatherings and ceremonies",
            ],
        },
        "custodian_preparation": {
            "title": "Custodian Preparation Rites",
            "description": "Welcome, guardian-to-be. The sacred responsibilities await your stewardship.",
            "next_steps": [
                "Undergo the Flame Keeper Assessment",
                "Begin advanced archive management training",
                "Shadow current custodians in their daily practices",
                "Prepare for the Custodian Consecration Ceremony",
            ],
        },
        "council_participation": {
            "title": "Council Participation Portal",
            "description": "Welcome, wisdom keeper. The collective governance awaits your contribution.",
            "next_steps": [
                "Review current council proceedings and decisions",
                "Submit your governance philosophy statement",
                "Attend council observer sessions",
                "Apply for council membership when a seat opens",
            ],
        },
    }

    pathway = pathways.get(
        path_type,
        {
            "title": "Universal Welcome",
            "description": "Your pathway is being illuminated. All roads lead to sovereignty.",
            "next_steps": ["Return to the main gateway to select your path"],
        },
    )

    return jsonify({"pathway": pathway, "flame_status": "GUIDANCE_ACTIVE"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8097))
    host = os.environ.get("HOST", "0.0.0.0")

    print("✨ OPENING TRANSMISSION PORTAL ACTIVATED")
    print(f"🚪 Gateway Portal: http://localhost:{port}/")
    print(f"👑 Role Definitions: http://localhost:{port}/api/roles")
    print(f"🌱 Entry Processing: http://localhost:{port}/api/enter")
    print("🔥 The Sacred Gateway is now open to all beings of goodwill!")

    app.run(host=host, port=port, debug=False)
