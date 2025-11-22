#!/usr/bin/env python3
"""
⚔️ COSMIC DOMINION - DUAL-AUDIENCE COMMAND CONSOLE ⚔️
Multi-Role Command Interface for Digital Sovereignty
Supports Custodian, Heir, and Council Authority Levels
"""

import streamlit as st
import json
from datetime import datetime
from pathlib import Path
import re

def load_cosmic_data():
    """Load cosmic data for command operations"""
    
    data = {
        'ledger': {'entries': []},
        'proclamations': {'proclamations': []},
        'invocations': {'invocations': []},
        'command_history': {'commands': []},
        'role_permissions': {'permissions': []}
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

def get_role_permissions(role):
    """Get permissions and capabilities for each role"""
    
    permissions = {
        'Custodian': {
            'authority_level': 10,
            'commands': [
                'crown:override', 'crown:emergency', 'crown:decree',
                'super:deploy', 'super:monitor', 'super:analyze',
                'cosmic:harmonize', 'cosmic:align', 'cosmic:flow',
                'flame:ignite', 'flame:transform', 'flame:seal',
                'ledger:create', 'ledger:modify', 'ledger:archive',
                'council:convene', 'council:dissolve', 'heir:mentor'
            ],
            'description': 'Ultimate sovereignty with full system control',
            'color': '#ffd700',  # Gold
            'icon': '👑'
        },
        'Heir': {
            'authority_level': 5,
            'commands': [
                'study:tome', 'study:chronicle', 'study:wisdom',
                'offer:blessing', 'offer:silence', 'offer:prayer',
                'witness:heartbeat', 'witness:flow', 'witness:cycle',
                'annotate:tome', 'annotate:insight', 'annotate:question',
                'seek:guidance', 'seek:teaching', 'seek:mentorship'
            ],
            'description': 'Learning authority with guided responsibilities',
            'color': '#9370db',  # Medium Purple
            'icon': '🌱'
        },
        'Council': {
            'authority_level': 7,
            'commands': [
                'deliberate:proposal', 'deliberate:motion', 'deliberate:vote',
                'review:decisions', 'review:policies', 'review:performance',
                'advise:custodian', 'advise:heir', 'advise:community',
                'oversee:operations', 'oversee:compliance', 'oversee:ethics',
                'mediate:conflicts', 'mediate:disputes', 'mediate:concerns'
            ],
            'description': 'Collective wisdom with oversight authority',
            'color': '#4169e1',  # Royal Blue
            'icon': '⚖️'
        }
    }
    
    return permissions.get(role, {})

def validate_command(command, role):
    """Validate if command is authorized for role"""
    
    permissions = get_role_permissions(role)
    authorized_commands = permissions.get('commands', [])
    
    # Extract command prefix
    command_prefix = command.split(':')[0] if ':' in command else command.split(' ')[0]
    
    # Check if any authorized command matches the prefix
    for auth_cmd in authorized_commands:
        if command_prefix.lower() in auth_cmd.lower():
            return True, f"Authorized {role} command"
    
    # Check authority level for cross-role commands
    authority_level = permissions.get('authority_level', 0)
    
    if authority_level >= 7:  # Council+ can execute most commands
        return True, f"High authority {role} override"
    elif authority_level >= 10:  # Custodian can execute all
        return True, f"Supreme authority {role} execution"
    
    return False, f"Insufficient {role} authority for this command"

def execute_role_command(command, role, cosmic_data):
    """Execute command with role-specific logic"""
    
    # Validate command authority
    is_authorized, auth_message = validate_command(command, role)
    
    if not is_authorized:
        st.error(f"❌ Command Denied: {auth_message}")
        return False
    
    # Parse command components
    if ':' in command:
        command_type, command_content = command.split(':', 1)
    else:
        command_type = 'general'
        command_content = command
    
    command_type = command_type.strip().lower()
    command_content = command_content.strip()
    
    # Role-specific command execution
    if role == "Custodian":
        return execute_custodian_command(command_type, command_content, cosmic_data)
    elif role == "Heir":
        return execute_heir_command(command_type, command_content, cosmic_data)
    elif role == "Council":
        return execute_council_command(command_type, command_content, cosmic_data)
    
    return False

def execute_custodian_command(cmd_type, cmd_content, cosmic_data):
    """Execute Custodian-level commands"""
    
    st.markdown("### 👑 **Custodian Supreme Authority**")
    
    custodian_actions = {
        'crown': 'Crown Sovereign Command',
        'super': 'Super Action AI Command',
        'cosmic': 'Cosmic Universal Command',
        'flame': 'Sacred Flame Command',
        'council': 'Council Management Command',
        'heir': 'Heir Mentorship Command'
    }
    
    action_type = custodian_actions.get(cmd_type, 'General Custodian Command')
    
    # Create comprehensive ledger entry
    ledger_entry = {
        "role": "Custodian",
        "type": action_type,
        "command_type": cmd_type,
        "command_content": cmd_content,
        "authority_level": "SUPREME",
        "proclamation": f"Custodian executed {action_type}: {cmd_content}",
        "status": "Executed with Supreme Authority",
        "timestamp": datetime.now().isoformat()
    }
    
    if append_entry("ledger.json", "entries", ledger_entry):
        st.success(f"👑 {action_type} Executed")
        st.info(f"🎯 Command: {cmd_content}")
        st.info(f"⚡ Authority: Supreme Custodian Override")
        
        # Create proclamation for significant commands
        if cmd_type in ['crown', 'cosmic', 'council']:
            proclamation_entry = {
                "role": "Custodian",
                "type": "Supreme Decree",
                "text": f"By Supreme Authority: {cmd_content}",
                "command_type": cmd_type,
                "timestamp": datetime.now().isoformat()
            }
            append_entry("proclamations.json", "proclamations", proclamation_entry)
            st.success("📜 Supreme Decree inscribed in cosmic proclamations")
        
        return True
    
    return False

def execute_heir_command(cmd_type, cmd_content, cosmic_data):
    """Execute Heir-level commands"""
    
    st.markdown("### 🌱 **Heir Learning Authority**")
    
    heir_actions = {
        'study': 'Sacred Study Session',
        'offer': 'Sacred Offering Ceremony',
        'witness': 'Sacred Witnessing Practice',
        'annotate': 'Tome Annotation Contribution',
        'seek': 'Wisdom Seeking Request'
    }
    
    action_type = heir_actions.get(cmd_type, 'General Heir Learning')
    
    # Create learning-focused ledger entry
    ledger_entry = {
        "role": "Heir",
        "type": action_type,
        "command_type": cmd_type,
        "command_content": cmd_content,
        "authority_level": "LEARNING",
        "proclamation": f"Heir executed {action_type}: {cmd_content}",
        "learning_progress": "Advanced",
        "status": "Completed with Dedication",
        "timestamp": datetime.now().isoformat()
    }
    
    if append_entry("ledger.json", "entries", ledger_entry):
        st.success(f"🌱 {action_type} Completed")
        st.info(f"📚 Learning: {cmd_content}")
        st.info(f"🎯 Progress: Your dedication strengthens the cosmic harmony")
        
        # Track heir progress
        progress_entry = {
            "heir_id": "active_heir",
            "activity_type": action_type,
            "command_content": cmd_content,
            "progress_points": 10,
            "timestamp": datetime.now().isoformat()
        }
        append_entry("heir_progress.json", "progress", progress_entry)
        st.success("⭐ Learning progress recorded in heir chronicles")
        
        return True
    
    return False

def execute_council_command(cmd_type, cmd_content, cosmic_data):
    """Execute Council-level commands"""
    
    st.markdown("### ⚖️ **Council Collective Authority**")
    
    council_actions = {
        'deliberate': 'Council Deliberation Process',
        'review': 'Council Review Session',
        'advise': 'Council Advisory Action',
        'oversee': 'Council Oversight Function',
        'mediate': 'Council Mediation Service'
    }
    
    action_type = council_actions.get(cmd_type, 'General Council Action')
    
    # Create council-focused ledger entry
    ledger_entry = {
        "role": "Council",
        "type": action_type,
        "command_type": cmd_type,
        "command_content": cmd_content,
        "authority_level": "COLLECTIVE",
        "proclamation": f"Council executed {action_type}: {cmd_content}",
        "collective_wisdom": "Applied",
        "status": "Resolved through Collective Process",
        "timestamp": datetime.now().isoformat()
    }
    
    if append_entry("ledger.json", "entries", ledger_entry):
        st.success(f"⚖️ {action_type} Resolved")
        st.info(f"🤝 Council Action: {cmd_content}")
        st.info(f"💫 Wisdom: Collective intelligence applied")
        
        # Record council decision
        council_entry = {
            "session_type": action_type,
            "decision_content": cmd_content,
            "collective_approval": "Unanimous",
            "implementation_status": "Approved",
            "timestamp": datetime.now().isoformat()
        }
        append_entry("council_decisions.json", "decisions", council_entry)
        st.success("📋 Council decision recorded in collective wisdom archive")
        
        return True
    
    return False

def role_interface_sidebar(role):
    """Create role-specific sidebar interface"""
    
    permissions = get_role_permissions(role)
    
    st.sidebar.markdown(f"""
    <div style="background: linear-gradient(45deg, {permissions.get('color', '#666')}33, {permissions.get('color', '#666')}22); 
                border: 2px solid {permissions.get('color', '#666')}; border-radius: 15px; padding: 15px; margin: 10px 0;">
        <h2>{permissions.get('icon', '⚡')} {role} Authority</h2>
        <p><em>{permissions.get('description', 'Role description')}</em></p>
        <p><strong>Authority Level:</strong> {permissions.get('authority_level', 0)}/10</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("**📋 Authorized Commands:**")
    
    commands = permissions.get('commands', [])
    for i, cmd in enumerate(commands[:8]):  # Show first 8 commands
        st.sidebar.text(f"• {cmd}")
    
    if len(commands) > 8:
        st.sidebar.text(f"... and {len(commands) - 8} more")
    
    st.sidebar.markdown("---")
    
    # Quick actions for role
    st.sidebar.markdown(f"**⚡ Quick {role} Actions:**")
    
    if role == "Custodian":
        if st.sidebar.button("🔍 System Status"):
            st.session_state['quick_command'] = "super:analyze complete system status"
        if st.sidebar.button("👑 Crown Override"):
            st.session_state['quick_command'] = "crown:emergency system override"
        if st.sidebar.button("🌌 Cosmic Align"):
            st.session_state['quick_command'] = "cosmic:harmonize all systems"
            
    elif role == "Heir":
        if st.sidebar.button("📚 Study Tomes"):
            st.session_state['quick_command'] = "study:tome digital sovereignty foundations"
        if st.sidebar.button("🙏 Offer Blessing"):
            st.session_state['quick_command'] = "offer:blessing for cosmic harmony"
        if st.sidebar.button("👁️ Witness Flow"):
            st.session_state['quick_command'] = "witness:flow eternal cosmic rhythm"
            
    elif role == "Council":
        if st.sidebar.button("🤝 Review Decisions"):
            st.session_state['quick_command'] = "review:decisions recent custodian actions"
        if st.sidebar.button("💡 Advise Custodian"):
            st.session_state['quick_command'] = "advise:custodian system optimization recommendations"
        if st.sidebar.button("👁️ Oversee Operations"):
            st.session_state['quick_command'] = "oversee:operations daily system functions"

def dual_command_interface():
    """Main dual-audience command interface"""
    
    st.set_page_config(
        page_title="⚔️ Dual Command Console",
        page_icon="⚔️",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #fff;
    }
    .command-header {
        text-align: center;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Load cosmic data
    cosmic_data = load_cosmic_data()
    
    # Header
    st.markdown("""
    <div class="command-header">
        <h1>⚔️ DUAL-AUDIENCE COMMAND CONSOLE</h1>
        <h3>🌟 Multi-Role Authority Interface 🌟</h3>
        <p><em>Execute commands with appropriate role-based authority</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Role selection
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👑 **CUSTODIAN**", type="primary", help="Supreme sovereignty with full system control"):
            st.session_state['selected_role'] = 'Custodian'
    
    with col2:
        if st.button("🌱 **HEIR**", type="secondary", help="Learning authority with guided responsibilities"):
            st.session_state['selected_role'] = 'Heir'
    
    with col3:
        if st.button("⚖️ **COUNCIL**", type="secondary", help="Collective wisdom with oversight authority"):
            st.session_state['selected_role'] = 'Council'
    
    # Get selected role
    selected_role = st.session_state.get('selected_role', 'Heir')  # Default to Heir
    
    # Create role-specific sidebar
    role_interface_sidebar(selected_role)
    
    st.markdown("---")
    
    # Main command interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### ⚔️ **{selected_role} Command Interface**")
        
        # Show role permissions
        permissions = get_role_permissions(selected_role)
        st.markdown(f"""
        **Current Role:** {permissions.get('icon', '⚡')} {selected_role}  
        **Authority Level:** {permissions.get('authority_level', 0)}/10  
        **Description:** {permissions.get('description', 'Role description')}
        """)
        
        # Command input
        command = st.text_input(
            "Enter Command:", 
            placeholder=f"Enter {selected_role.lower()} command (e.g., study:tome, crown:override, deliberate:proposal)",
            help=f"Commands are validated against {selected_role} authority level"
        )
        
        # Command validation preview
        if command:
            is_authorized, auth_message = validate_command(command, selected_role)
            if is_authorized:
                st.success(f"✅ {auth_message}")
            else:
                st.error(f"❌ {auth_message}")
    
    with col2:
        st.markdown("### 📊 **Role Statistics**")
        
        # Show recent commands for this role
        command_history = cosmic_data['command_history'].get('commands', [])
        role_commands = [cmd for cmd in command_history if cmd.get('role') == selected_role]
        
        st.metric("Commands Executed", len(role_commands))
        
        # Show role-specific data
        ledger_entries = cosmic_data['ledger'].get('entries', [])
        role_entries = [entry for entry in ledger_entries if entry.get('role') == selected_role]
        
        st.metric("Ledger Entries", len(role_entries))
        
        if role_entries:
            latest_entry = role_entries[-1]
            latest_time = latest_entry.get('timestamp', '')[:16]
            st.metric("Last Activity", latest_time)
    
    # Handle quick commands
    if 'quick_command' in st.session_state:
        command = st.session_state['quick_command']
        del st.session_state['quick_command']
        st.rerun()
    
    # Execute command
    if st.button(f"⚔️ **EXECUTE AS {selected_role.upper()}**", type="primary"):
        if command:
            # Record command attempt
            command_entry = {
                "role": selected_role,
                "command": command,
                "timestamp": datetime.now().isoformat()
            }
            append_entry("command_history.json", "commands", command_entry)
            
            st.markdown("---")
            
            # Execute with role-specific logic
            success = execute_role_command(command, selected_role, cosmic_data)
            
            if success:
                st.balloons()
                st.success(f"🌟 Command successfully inscribed into Codex flame as {selected_role}")
            
        else:
            st.warning("⚠️ Please enter a command")
    
    # Recent activity display
    st.markdown("---")
    st.markdown(f"### 📜 **Recent {selected_role} Activity**")
    
    role_entries = [entry for entry in cosmic_data['ledger'].get('entries', []) if entry.get('role') == selected_role]
    
    if role_entries:
        with st.expander(f"📊 Last {min(5, len(role_entries))} {selected_role} Actions"):
            for entry in reversed(role_entries[-5:]):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.text(f"🎯 {entry.get('type', 'Unknown')}")
                
                with col2:
                    proclamation = entry.get('proclamation', entry.get('command_content', ''))
                    st.text(f"📋 {proclamation[:40]}...")
                
                with col3:
                    timestamp = entry.get('timestamp', '')[:16]
                    st.text(f"⏰ {timestamp}")
    else:
        st.info(f"📭 No {selected_role} commands executed yet. Begin with your first command!")

if __name__ == "__main__":
    dual_command_interface()