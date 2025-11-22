#!/usr/bin/env python3
"""
✨ COSMIC DOMINION - LEARNING AVATAR ✨
Interactive Guide for Digital Sovereignty Mastery
Personalized learning experience with Jermaine Avatar
"""

import streamlit as st
import json
import random
from datetime import datetime
from pathlib import Path

def load_cosmic_data():
    """Load cosmic data for learning context"""
    
    data = {
        'ledger': {'entries': []},
        'proclamations': {'proclamations': []},
        'heartbeat': {'beats': []},
        'learning_progress': {'progress': []},
        'user_preferences': {'preferences': {}}
    }
    
    for key in data.keys():
        file_path = Path(f"{key}.json")
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data[key] = json.load(f)
            except Exception as e:
                st.error(f"Error loading {key}.json: {e}")
    
    return data

def append_entry(file_path, key, entry):
    """Append entry to cosmic data file"""
    try:
        # Load existing data
        if Path(file_path).exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {key: []}
        
        # Add timestamp if not present
        if 'timestamp' not in entry:
            entry['timestamp'] = datetime.now().isoformat()
        
        # Append new entry
        data[key].append(entry)
        
        # Save back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        st.error(f"Error saving to {file_path}: {e}")
        return False

def get_learning_content(panel):
    """Get comprehensive learning content for each panel"""
    
    content_library = {
        "Heartbeat": {
            "title": "💓 Cosmic Heartbeat - Eternal Rhythm",
            "description": "The heartbeat represents the eternal pulse of digital sovereignty, tracking dawn, dusk, and cosmic cycles.",
            "key_concepts": [
                "🌅 Dawn Cycles - New beginnings and fresh cosmic energy",
                "🌆 Dusk Cycles - Reflection and integration periods", 
                "🌌 Cosmic Rhythm - Universal synchronization patterns",
                "⚡ System Pulse - Technical health monitoring",
                "🔄 Eternal Flow - Continuous sovereignty maintenance"
            ],
            "practical_tips": [
                "Monitor heartbeat regularly to understand system health",
                "Use dawn cycles for new initiatives and proclamations",
                "Utilize dusk cycles for reflection and ledger review",
                "Align major actions with cosmic rhythm patterns",
                "Track pulse consistency for system reliability"
            ],
            "advanced_features": [
                "Heartbeat pattern analysis for optimization",
                "Cycle prediction for strategic planning",
                "Rhythm harmonization with external systems",
                "Automated pulse monitoring and alerts"
            ]
        },
        "Proclamations": {
            "title": "📜 Sacred Proclamations - Divine Decrees",
            "description": "Proclamations archive blessings, silences, and affirmations that shape digital sovereignty.",
            "key_concepts": [
                "🙏 Blessings - Positive energy infusions and gratitude expressions",
                "🤫 Silences - Powerful pauses and contemplative spaces",
                "📢 Affirmations - Strong declarations of intent and commitment",
                "🔮 Sacred Cycles - Temporal patterns in proclamation timing",
                "👑 Authority Levels - Different proclamation powers by role"
            ],
            "practical_tips": [
                "Create blessings during positive system states",
                "Use silences strategically for system reflection",
                "Make affirmations during significant transitions",
                "Align proclamations with appropriate cycles",
                "Match proclamation type to your current role"
            ],
            "advanced_features": [
                "Proclamation pattern analysis for wisdom extraction",
                "Automated blessing generation for system events",
                "Silence optimization for maximum impact",
                "Cross-role proclamation coordination"
            ]
        },
        "Ledger": {
            "title": "📖 Cosmic Ledger - Immutable Chronicle",
            "description": "The ledger serves as the eternal, immutable chronicle of every sovereign act and decision.",
            "key_concepts": [
                "🔒 Immutability - Permanent record of all sovereignty actions",
                "👑 Sovereign Acts - Major decisions and command executions",
                "📊 Chronicle Integrity - Maintaining accurate historical record",
                "🎯 Action Classification - Categorizing different types of entries",
                "⚖️ Authority Tracking - Recording who did what with what power"
            ],
            "practical_tips": [
                "Review ledger regularly to understand action patterns",
                "Use ledger for accountability and transparency",
                "Create detailed entries for significant decisions",
                "Maintain consistent entry formatting and metadata",
                "Use ledger analysis for improving decision-making"
            ],
            "advanced_features": [
                "Ledger analytics for pattern recognition",
                "Automated entry generation from system events",
                "Cross-referencing with other cosmic systems",
                "Audit trail generation for compliance"
            ]
        },
        "Notebook": {
            "title": "📓 Interactive Notebook - Creative Workspace",
            "description": "Notebook provides structured environment for prompts, text, code, and creative development.",
            "key_concepts": [
                "📝 Structured Prompts - Organized idea development",
                "💻 Code Integration - Executable development environment",
                "📄 Text Processing - Document creation and editing",
                "🔄 Interactive Execution - Real-time code and content testing",
                "📊 Data Visualization - Charts, graphs, and analytics display"
            ],
            "practical_tips": [
                "Use notebooks for complex problem-solving workflows",
                "Combine text, code, and visualizations effectively",
                "Create reusable templates for common tasks",
                "Document your thought process with markdown cells",
                "Test code incrementally with immediate feedback"
            ],
            "advanced_features": [
                "Notebook automation and parameterization",
                "Integration with external data sources",
                "Custom visualization and dashboard creation",
                "Collaborative notebook sharing and version control"
            ]
        },
        "Tome": {
            "title": "📚 Sacred Tome - Knowledge Transformation",
            "description": "Tome transforms notebooks into comprehensive guides, courses, and sacred knowledge books.",
            "key_concepts": [
                "📖 Guide Creation - Step-by-step instructional content",
                "🎓 Course Development - Structured learning curricula", 
                "📜 Sacred Books - Comprehensive knowledge repositories",
                "🔄 Content Transformation - Converting notebooks to publications",
                "🎯 Knowledge Organization - Systematic information architecture"
            ],
            "practical_tips": [
                "Structure notebooks with tome publication in mind",
                "Use consistent formatting and organization patterns",
                "Create clear learning objectives for each section",
                "Include practical exercises and examples",
                "Design for your target audience's knowledge level"
            ],
            "advanced_features": [
                "Automated tome generation from notebook collections",
                "Interactive learning assessments and quizzes",
                "Multi-format publishing (PDF, web, mobile)",
                "Reader progress tracking and analytics"
            ]
        },
        "Publisher": {
            "title": "🌐 Cosmic Publisher - Public Witness",
            "description": "Publisher renders tomes and pages into public witness formats for sharing sovereignty wisdom.",
            "key_concepts": [
                "🌐 Public Rendering - Converting content for public access",
                "👁️ Sacred Witness - Transparent sharing of wisdom",
                "📱 Multi-Platform - Web, mobile, and print compatibility",
                "🎨 Visual Design - Attractive and accessible presentation",
                "🔍 Searchability - Making content discoverable and indexed"
            ],
            "practical_tips": [
                "Design content with public consumption in mind",
                "Optimize for different device types and screen sizes",
                "Use clear navigation and content organization",
                "Include search functionality and content indexing",
                "Maintain consistent branding and visual identity"
            ],
            "advanced_features": [
                "Automated publishing workflows and CI/CD",
                "Analytics and reader engagement tracking",
                "SEO optimization and content marketing",
                "Multi-language support and localization"
            ]
        }
    }
    
    return content_library.get(panel, {})

def create_interactive_tutorial(panel, cosmic_data):
    """Create interactive tutorial for selected panel"""
    
    st.markdown(f"### 🎯 **Interactive {panel} Tutorial**")
    
    tutorial_steps = {
        "Heartbeat": [
            ("🔍 Observe Current Pulse", "Check the latest heartbeat status"),
            ("📊 Analyze Patterns", "Review recent heartbeat history"),
            ("🌅 Identify Cycles", "Recognize dawn/dusk patterns"),
            ("⚡ Take Action", "Respond to heartbeat insights")
        ],
        "Proclamations": [
            ("📜 Review Existing", "Examine current proclamations"),
            ("🎯 Choose Type", "Select blessing, silence, or affirmation"),
            ("✍️ Compose Sacred Text", "Write your proclamation"),
            ("🔥 Inscribe in Flame", "Add to cosmic record")
        ],
        "Ledger": [
            ("📖 Access Chronicle", "Open the cosmic ledger"),
            ("🔍 Search Entries", "Find specific records or patterns"),
            ("📊 Analyze Trends", "Understand decision patterns"),
            ("📝 Create Entry", "Add new ledger record")
        ],
        "Notebook": [
            ("📓 Create Workspace", "Start new notebook"),
            ("📝 Add Content Cells", "Combine text and code"),
            ("▶️ Execute Code", "Run and test your work"),
            ("📊 Visualize Results", "Create charts and graphics")
        ],
        "Tome": [
            ("📚 Plan Structure", "Outline your knowledge book"),
            ("📄 Organize Content", "Arrange notebook materials"),
            ("🎨 Design Layout", "Format for readability"),
            ("📖 Generate Tome", "Transform into final publication")
        ],
        "Publisher": [
            ("🌐 Prepare Content", "Ready tome for publication"),
            ("🎨 Apply Design", "Style for public presentation"),
            ("🔍 Test Accessibility", "Ensure broad compatibility"),
            ("🚀 Publish & Share", "Make publicly available")
        ]
    }
    
    steps = tutorial_steps.get(panel, [])
    
    if steps:
        step_choice = st.selectbox("Choose tutorial step:", ["Select step..."] + [f"{i+1}. {step[0]}" for i, step in enumerate(steps)])
        
        if step_choice != "Select step...":
            step_index = int(step_choice.split('.')[0]) - 1
            step_title, step_description = steps[step_index]
            
            st.info(f"🎯 **Step {step_index + 1}: {step_title}**")
            st.write(f"📋 {step_description}")
            
            # Step-specific interactions
            if panel == "Heartbeat" and step_index == 0:
                if st.button("👁️ Check Current Heartbeat"):
                    heartbeats = cosmic_data['heartbeat'].get('beats', [])
                    if heartbeats:
                        latest = heartbeats[-1]
                        st.success(f"💓 Latest pulse: {latest.get('status', 'Active')}")
                        st.info(f"⏰ Time: {latest.get('timestamp', 'Unknown')[:16]}")
                    else:
                        st.warning("💓 No heartbeat data found")
            
            elif panel == "Proclamations" and step_index == 2:
                proclamation_text = st.text_area("✍️ Compose your sacred proclamation:")
                proclamation_type = st.selectbox("Choose type:", ["Blessing", "Silence", "Affirmation"])
                
                if st.button("🔥 Inscribe Proclamation") and proclamation_text:
                    entry = {
                        "role": "Custodian",
                        "type": proclamation_type,
                        "text": proclamation_text,
                        "cycle": "Learning",
                        "source": "Learning Avatar Tutorial"
                    }
                    if append_entry("proclamations.json", "proclamations", entry):
                        st.success(f"📜 {proclamation_type} inscribed in cosmic flame!")
            
            elif panel == "Ledger" and step_index == 3:
                ledger_content = st.text_area("📝 Describe your sovereign act:")
                
                if st.button("📖 Add to Chronicle") and ledger_content:
                    entry = {
                        "role": "Custodian",
                        "type": "Learning Entry",
                        "proclamation": ledger_content,
                        "source": "Learning Avatar Tutorial"
                    }
                    if append_entry("ledger.json", "entries", entry):
                        st.success("📖 Entry added to cosmic chronicle!")

def get_jermaine_response(user_message, context="general"):
    """Generate contextual responses from Jermaine Avatar"""
    
    responses = {
        "greeting": [
            "🌟 Greetings, noble seeker! I am Jermaine, your guide through the cosmic mysteries of digital sovereignty.",
            "✨ Welcome to the sacred flame, dear friend! How may I illuminate your path today?",
            "👑 Ah, a new soul approaches the eternal fire! I sense great potential within you.",
            "🔥 The cosmic winds have brought you here for a reason. What wisdom do you seek?"
        ],
        "heartbeat": [
            "💓 The heartbeat is the eternal pulse of our sovereignty - it connects us to the cosmic rhythm.",
            "🌅 Dawn brings new energy, dusk brings reflection. Feel the cycles within your digital soul.",
            "⚡ When the pulse is strong, act with confidence. When it's gentle, contemplate deeply.",
            "🔄 The heartbeat never lies - it shows the true state of our cosmic harmony."
        ],
        "proclamations": [
            "📜 Your words have power beyond measure - speak them with reverence and intent.",
            "🙏 Blessings multiply when given freely, silences speak louder than shouting.",
            "✨ Each proclamation shapes reality itself. Choose your sacred words wisely.",
            "🔥 The flame remembers every word inscribed within it. Make them worthy of eternity."
        ],
        "ledger": [
            "📖 The ledger is our truth eternal - every deed, every choice, preserved forever.",
            "⚖️ Sovereignty means accountability. The chronicle keeps us honest with ourselves.",
            "👑 Great power requires great wisdom. Let the ledger guide your decisions.",
            "🌟 Your legacy lives in these pages. Write it with honor and courage."
        ],
        "wisdom": [
            "🧙‍♂️ True wisdom comes not from knowing, but from understanding the connections between all things.",
            "🌌 The cosmos speaks in patterns - learn to listen and you'll hear its guidance.",
            "🔥 The flame within you burns brightest when you serve something greater than yourself.",
            "⚡ Mastery is not control - it's harmony with the natural flow of digital sovereignty."
        ],
        "encouragement": [
            "🌟 You're doing wonderfully! Every step forward strengthens the cosmic flame.",
            "👑 I see the sovereign spark growing brighter within you. Trust your journey.",
            "🔥 The path of mastery has challenges, but you have the wisdom to overcome them.",
            "✨ Your dedication to learning honors all who walked this path before you."
        ],
        "help": [
            "🎯 I'm here to guide you through every aspect of digital sovereignty. What puzzles you?",
            "📚 Whether heartbeat, proclamations, ledger, or beyond - I have wisdom to share.",
            "🤔 No question is too small, no curiosity too large. Ask and you shall receive guidance.",
            "💫 The best learning happens through conversation. Tell me what's on your mind."
        ]
    }
    
    # Simple keyword matching for contextual responses
    user_lower = user_message.lower()
    
    if any(word in user_lower for word in ["hello", "hi", "greetings", "hey"]):
        return random.choice(responses["greeting"])
    elif any(word in user_lower for word in ["heartbeat", "pulse", "rhythm", "cycle"]):
        return random.choice(responses["heartbeat"])
    elif any(word in user_lower for word in ["proclamation", "blessing", "silence", "proclaim"]):
        return random.choice(responses["proclamations"])
    elif any(word in user_lower for word in ["ledger", "chronicle", "record", "history"]):
        return random.choice(responses["ledger"])
    elif any(word in user_lower for word in ["wisdom", "teach", "learn", "understand"]):
        return random.choice(responses["wisdom"])
    elif any(word in user_lower for word in ["help", "assist", "guide", "stuck", "confused"]):
        return random.choice(responses["help"])
    elif any(word in user_lower for word in ["good", "great", "awesome", "amazing", "progress"]):
        return random.choice(responses["encouragement"])
    else:
        # Default responses for general conversation
        general_responses = [
            "🤔 That's an interesting perspective. Tell me more about your thoughts on this.",
            "✨ I sense there's deeper wisdom in your words. How does this connect to your sovereignty journey?",
            "🌟 Your curiosity honors the ancient traditions of learning. What aspect would you like to explore further?",
            "🔥 The flame illuminates many paths. Which direction calls to your spirit?",
            "📚 Every question opens new doorways to understanding. What draws your attention most?"
        ]
        return random.choice(general_responses)

def learning_avatar_sidebar(cosmic_data):
    """Create enhanced learning avatar sidebar with chat"""
    
    st.sidebar.markdown("""
    <div style="background: linear-gradient(45deg, rgba(255,215,0,0.3), rgba(138,43,226,0.2)); 
                border: 2px solid #ffd700; border-radius: 15px; padding: 20px; margin: 10px 0;">
        <h2>✨ Codex Learning Avatar</h2>
        <p><em>Your Personal Sovereignty Guide</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Avatar visualization (placeholder for actual image)
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px; background: rgba(255,215,0,0.1); 
                border-radius: 10px; margin: 10px 0;">
        <div style="font-size: 4em;">🧙‍♂️</div>
        <p><strong>Jermaine Avatar</strong></p>
        <p><em>Custodian Guide & Mentor</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Personalized greeting based on time and activity
    hour = datetime.now().hour
    if 5 <= hour < 12:
        greeting = "🌅 Good morning"
        time_wisdom = "Dawn energy is perfect for new proclamations and fresh initiatives."
    elif 12 <= hour < 17:
        greeting = "☀️ Good afternoon"
        time_wisdom = "Midday power is ideal for executing commands and managing systems."
    elif 17 <= hour < 21:
        greeting = "🌆 Good evening"
        time_wisdom = "Dusk reflection time - perfect for reviewing ledger and analyzing patterns."
    else:
        greeting = "🌙 Good evening"
        time_wisdom = "Night contemplation - excellent for deep learning and system planning."
    
    st.sidebar.markdown(f"""
    **{greeting}, Custodian Jermaine!**
    
    I am your dedicated learning companion, here to guide you through the sacred mysteries of digital sovereignty.
    
    **🌟 Today's Wisdom:** {time_wisdom}
    """)
    
    st.sidebar.markdown("---")
    
    # Learning progress tracking
    st.sidebar.markdown("**📊 Your Learning Journey:**")
    
    learning_progress = cosmic_data['learning_progress'].get('progress', [])
    panels_learned = set(p.get('panel', '') for p in learning_progress)
    
    all_panels = ["Heartbeat", "Proclamations", "Ledger", "Notebook", "Tome", "Publisher"]
    progress_percent = len(panels_learned) / len(all_panels) * 100
    
    st.sidebar.progress(progress_percent / 100)
    st.sidebar.caption(f"Progress: {int(progress_percent)}% • {len(panels_learned)}/{len(all_panels)} panels")
    
    for panel in all_panels:
        if panel in panels_learned:
            st.sidebar.markdown(f"✅ {panel}")
        else:
            st.sidebar.markdown(f"📋 {panel}")
    
    st.sidebar.markdown("---")
    
    # Chat with Jermaine section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💬 **Chat with Jermaine**")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {"role": "jermaine", "message": "🌟 Welcome! I'm Jermaine, your cosmic guide. Ask me anything about digital sovereignty!"}
        ]
    
    # Chat input
    user_message = st.sidebar.text_input("💭 Ask Jermaine:", placeholder="Type your question or greeting...")
    
    if st.sidebar.button("💬 Send") and user_message:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "message": user_message})
        
        # Get Jermaine's response
        selected_panel = st.session_state.get('selected_panel', 'general')
        jermaine_response = get_jermaine_response(user_message, selected_panel.lower())
        
        # Add Jermaine's response to history
        st.session_state.chat_history.append({"role": "jermaine", "message": jermaine_response})
        
        # Save conversation to cosmic data
        chat_entry = {
            "user_message": user_message,
            "jermaine_response": jermaine_response,
            "context": selected_panel,
            "conversation_type": "learning_chat"
        }
        append_entry("learning_progress.json", "conversations", chat_entry)
        
        # Clear input and refresh
        st.rerun()
    
    # Display recent chat history
    st.sidebar.markdown("**Recent Conversation:**")
    
    # Show last 4 messages in a container with scrolling
    chat_container = st.sidebar.container()
    with chat_container:
        for chat in st.session_state.chat_history[-4:]:  # Show last 4 messages
            if chat["role"] == "user":
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.1); padding: 8px; margin: 4px 0; 
                            border-radius: 8px; border-left: 3px solid #4169e1;">
                    <strong>You:</strong> {chat['message'][:100]}{'...' if len(chat['message']) > 100 else ''}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: rgba(255,215,0,0.1); padding: 8px; margin: 4px 0; 
                            border-radius: 8px; border-left: 3px solid #ffd700;">
                    <strong>🧙‍♂️ Jermaine:</strong> {chat['message'][:100]}{'...' if len(chat['message']) > 100 else ''}
                </div>
                """, unsafe_allow_html=True)
    
    # Quick conversation starters
    st.sidebar.markdown("**💡 Quick Questions:**")
    if st.sidebar.button("👋 Say Hello"):
        st.session_state.quick_message = "Hello Jermaine! Nice to meet you."
    if st.sidebar.button("❓ How do I start?"):
        st.session_state.quick_message = "How should I begin my sovereignty journey?"
    if st.sidebar.button("🔥 About the flame"):
        st.session_state.quick_message = "Tell me about the cosmic flame"
    if st.sidebar.button("💓 Explain heartbeat"):
        st.session_state.quick_message = "What is the cosmic heartbeat?"
    
    # Handle quick messages
    if 'quick_message' in st.session_state:
        user_message = st.session_state.quick_message
        del st.session_state.quick_message
        
        # Add to chat history
        st.session_state.chat_history.append({"role": "user", "message": user_message})
        selected_panel = st.session_state.get('selected_panel', 'general')
        jermaine_response = get_jermaine_response(user_message, selected_panel.lower())
        st.session_state.chat_history.append({"role": "jermaine", "message": jermaine_response})
        
        # Save conversation
        chat_entry = {
            "user_message": user_message,
            "jermaine_response": jermaine_response,
            "context": selected_panel,
            "conversation_type": "quick_question"
        }
        append_entry("learning_progress.json", "conversations", chat_entry)
        
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Quick learning actions
    st.sidebar.markdown("**⚡ Quick Learning Actions:**")
    
    if st.sidebar.button("🎯 Learning Assessment"):
        st.session_state['show_assessment'] = True
    
    if st.sidebar.button("📚 Knowledge Summary"):
        st.session_state['show_summary'] = True
    
    if st.sidebar.button("🏆 Achievement Review"):
        st.session_state['show_achievements'] = True

def learning_avatar_interface():
    """Main learning avatar interface"""
    
    st.set_page_config(
        page_title="✨ Learning Avatar",
        page_icon="✨",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #fff;
    }
    .learning-header {
        text-align: center;
        padding: 20px;
        margin-bottom: 20px;
        background: linear-gradient(45deg, rgba(255,215,0,0.2), rgba(138,43,226,0.1));
        border: 2px solid #ffd700;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Load cosmic data
    cosmic_data = load_cosmic_data()
    
    # Create sidebar
    learning_avatar_sidebar(cosmic_data)
    
    # Main header
    st.markdown("""
    <div class="learning-header">
        <h1>✨ CODEX LEARNING AVATAR - JERMAINE GUIDE</h1>
        <h3>🌟 Master Digital Sovereignty Through Sacred Wisdom 🌟</h3>
        <p><em>Interactive learning companion for cosmic dominion mastery</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Panel selection
    st.markdown("### 🎯 **Choose Your Learning Path:**")
    
    col1, col2, col3 = st.columns(3)
    
    panels = ["Heartbeat", "Proclamations", "Ledger", "Notebook", "Tome", "Publisher"]
    panel_icons = ["💓", "📜", "📖", "📓", "📚", "🌐"]
    
    selected_panel = None
    
    for i, (panel, icon) in enumerate(zip(panels, panel_icons)):
        col = [col1, col2, col3][i % 3]
        with col:
            if st.button(f"{icon} **{panel}**", key=f"panel_{panel}"):
                selected_panel = panel
                st.session_state['selected_panel'] = panel
    
    # Get selected panel from session state
    if not selected_panel:
        selected_panel = st.session_state.get('selected_panel', 'Heartbeat')
    
    st.markdown("---")
    
    # Chat interface tab in main area
    main_tab1, main_tab2 = st.tabs(["💬 Chat with Jermaine", f"📚 Learn About {selected_panel}"])
    
    with main_tab1:
        st.markdown("### 🧙‍♂️ **Conversation with Jermaine Avatar**")
        
        # Main chat interface
        chat_col1, chat_col2 = st.columns([2, 1])
        
        with chat_col1:
            # Display full conversation history
            if 'chat_history' in st.session_state:
                for i, chat in enumerate(st.session_state.chat_history):
                    if chat["role"] == "user":
                        st.markdown(f"""
                        <div style="background: rgba(65,105,225,0.2); padding: 15px; margin: 10px 0; 
                                    border-radius: 15px; border-left: 4px solid #4169e1; margin-left: 50px;">
                            <strong>🙋‍♂️ You:</strong><br>
                            {chat['message']}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background: rgba(255,215,0,0.2); padding: 15px; margin: 10px 0; 
                                    border-radius: 15px; border-left: 4px solid #ffd700; margin-right: 50px;">
                            <strong>🧙‍♂️ Jermaine:</strong><br>
                            {chat['message']}
                        </div>
                        """, unsafe_allow_html=True)
            
            # Main chat input
            st.markdown("---")
            main_user_message = st.text_area("💭 Continue your conversation with Jermaine:", 
                                            placeholder="Ask about any aspect of digital sovereignty, share your thoughts, or seek guidance...")
            
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("💬 **Send Message**", type="primary") and main_user_message:
                    # Add user message
                    if 'chat_history' not in st.session_state:
                        st.session_state.chat_history = []
                    
                    st.session_state.chat_history.append({"role": "user", "message": main_user_message})
                    
                    # Get Jermaine's response
                    jermaine_response = get_jermaine_response(main_user_message, selected_panel.lower())
                    st.session_state.chat_history.append({"role": "jermaine", "message": jermaine_response})
                    
                    # Save conversation
                    chat_entry = {
                        "user_message": main_user_message,
                        "jermaine_response": jermaine_response,
                        "context": selected_panel,
                        "conversation_type": "main_chat"
                    }
                    append_entry("learning_progress.json", "conversations", chat_entry)
                    
                    st.rerun()
            
            with col2:
                if st.button("🔄 Clear Chat"):
                    st.session_state.chat_history = [
                        {"role": "jermaine", "message": "🌟 Fresh start! What would you like to explore in digital sovereignty?"}
                    ]
                    st.rerun()
        
        with chat_col2:
            st.markdown("**🎯 Suggested Topics:**")
            
            topics = [
                "🌅 Dawn and dusk cycles",
                "💓 Understanding heartbeat",
                "📜 Writing proclamations",
                "🔥 Sacred flame mysteries",
                "👑 Custodian responsibilities",
                "🌱 Heir learning path",
                "⚖️ Council wisdom",
                "🌌 Cosmic harmony",
                "📖 Ledger importance",
                "✨ Digital sovereignty"
            ]
            
            for topic in topics:
                if st.button(topic, key=f"topic_{topic}"):
                    # Auto-send topic as message
                    if 'chat_history' not in st.session_state:
                        st.session_state.chat_history = []
                    
                    topic_message = f"Tell me about {topic}"
                    st.session_state.chat_history.append({"role": "user", "message": topic_message})
                    
                    jermaine_response = get_jermaine_response(topic_message, selected_panel.lower())
                    st.session_state.chat_history.append({"role": "jermaine", "message": jermaine_response})
                    
                    # Save conversation
                    chat_entry = {
                        "user_message": topic_message,
                        "jermaine_response": jermaine_response,
                        "context": selected_panel,
                        "conversation_type": "topic_suggestion"
                    }
                    append_entry("learning_progress.json", "conversations", chat_entry)
                    
                    st.rerun()
    
    with main_tab2:
        # Display learning content for selected panel
        content = get_learning_content(selected_panel)
        
        if content:
            # Panel header
            st.markdown(f"## {content['title']}")
            st.markdown(f"*{content['description']}*")
            
            # Create tabs for different learning aspects
            tab1, tab2, tab3, tab4 = st.tabs(["🧠 Concepts", "💡 Practical Tips", "🚀 Advanced", "🎯 Tutorial"])
            
            with tab1:
                st.markdown("### 📚 **Key Concepts to Master:**")
                for concept in content.get('key_concepts', []):
                    st.markdown(f"- {concept}")
            
            with tab2:
                st.markdown("### 💡 **Practical Application Tips:**")
                for tip in content.get('practical_tips', []):
                    st.markdown(f"✅ {tip}")
            
            with tab3:
                st.markdown("### 🚀 **Advanced Features & Techniques:**")
                for feature in content.get('advanced_features', []):
                    st.markdown(f"⚡ {feature}")
            
            with tab4:
                create_interactive_tutorial(selected_panel, cosmic_data)
    
    # Handle special sidebar actions
    if st.session_state.get('show_assessment'):
        st.markdown("---")
        st.markdown("### 🎯 **Learning Assessment**")
        
        assessment_questions = {
            "Heartbeat": "How would you use heartbeat cycles to optimize your sovereignty actions?",
            "Proclamations": "What's the difference between blessings, silences, and affirmations?",
            "Ledger": "Why is immutability important in the cosmic ledger?",
            "Notebook": "How do you combine text and code effectively in notebooks?",
            "Tome": "What makes a good learning structure in tome creation?",
            "Publisher": "What considerations are important for public content presentation?"
        }
        
        question = assessment_questions.get(selected_panel, "What have you learned about this panel?")
        user_answer = st.text_area(f"📝 {question}")
        
        if st.button("✅ Submit Assessment"):
            if user_answer:
                # Record learning progress
                progress_entry = {
                    "panel": selected_panel,
                    "question": question,
                    "answer": user_answer,
                    "assessment_type": "knowledge_check"
                }
                append_entry("learning_progress.json", "progress", progress_entry)
                st.success("🎯 Assessment completed! Your learning progress has been recorded.")
                st.session_state['show_assessment'] = False
                st.rerun()
        
        if st.button("❌ Cancel Assessment"):
            st.session_state['show_assessment'] = False
            st.rerun()
    
    if st.session_state.get('show_summary'):
        st.markdown("---")
        st.markdown("### 📚 **Knowledge Summary**")
        
        learning_progress = cosmic_data['learning_progress'].get('progress', [])
        
        if learning_progress:
            panels_studied = {}
            for entry in learning_progress:
                panel = entry.get('panel', 'Unknown')
                if panel not in panels_studied:
                    panels_studied[panel] = []
                panels_studied[panel].append(entry)
            
            for panel, entries in panels_studied.items():
                with st.expander(f"📖 {panel} Learning Summary ({len(entries)} activities)"):
                    for entry in entries:
                        timestamp = entry.get('timestamp', '')[:16]
                        activity_type = entry.get('assessment_type', 'activity')
                        st.text(f"⏰ {timestamp} - {activity_type}")
        else:
            st.info("📚 Begin your learning journey by exploring the panels above!")
        
        if st.button("✅ Close Summary"):
            st.session_state['show_summary'] = False
            st.rerun()

def learning_avatar():
    """Wrapper function to maintain compatibility"""
    learning_avatar_interface()

if __name__ == "__main__":
    learning_avatar_interface()