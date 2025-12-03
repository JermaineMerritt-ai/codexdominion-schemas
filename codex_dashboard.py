# codex_dashboard.py
import datetime
import json
import uuid

import streamlit as st

LEDGER_PATH = "codex_ledger.json"


# ---------- Enhanced Error Handling ----------
def safe_execute(func, *args, **kwargs):
    """Execute function with error handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
        return None


# ---------- Enhanced Styling ----------
def apply_cosmic_styling():
    """Apply enhanced cosmic styling"""
    st.markdown(
        """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f7f1e3 0%, #efe7d4 100%);
    }
    .metric-card {
        background: linear-gradient(135deg, #0f2b4a 0%, #1a4870 100%);
        color: #bfa780;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #0f2b4a 0%, #1a4870 100%);
        color: #bfa780;
        border: 2px solid #bfa780;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #bfa780 0%, #d4c294 100%);
        color: #0f2b4a;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


# ---------- AI Command Router ----------
def route_command(cmd):
    d = load_ledger()
    cmd_lower = cmd.lower()

    # 🔍 System Check
    if "system check" in cmd_lower:
        return f"""
🔍 **System Check Report:**
• **System Status:** OPERATIONAL
• **Unified Interface:** READY
• **Flame Status:** {d.get('heartbeat', {}).get('status', 'LUMINOUS')}
• **Last Updated:** {d['meta'].get('last_updated', '—')}
• **Proclamations:** {len(d.get('proclamations', []))}
• **Cycles:** {len(d.get('cycles', []))}
• **Contributions:** {len(d.get('contributions', []))}
• **Archives:** {len(d.get('completed_archives', []))}
• **Capsules:** {len(d.get('capsules', []))}
• **Video Generations:** {len(d.get('video_generations', []))}
• **AI Commands:** {len(d.get('ai_commands', []))}
        """

    # 📜 Archives
    elif "archive" in cmd_lower:
        archives_count = len(d.get("completed_archives", []))
        return (
            f"📜 **Archives accessed.** Currently contains "
            f"{archives_count} sealed scrolls ready for ceremonial review."
        )

    # ✉️ Dispatch
    elif "dispatch" in cmd_lower:
        return (
            "📧 **Dispatch systems online.** Ceremonial message "
            "transmission ready. Compose your luminous proclamations."
        )

    # 🎥 Studio
    elif "studio" in cmd_lower:
        video_count = len(d.get("video_generations", []))
        return (
            f"🎥 **Codex Studio activated.** {video_count} ceremonial "
            f"videos generated. Ready for new proclamation scripts."
        )

    # ⚗️ Capsule
    elif "capsule" in cmd_lower:
        capsule_count = len(d.get("capsules", []))
        return (
            f"🧪 **Capsule chamber accessible.** {capsule_count} "
            f"ceremonial capsules sealed and ready for replay transmission."
        )

    # � Ledger
    elif "ledger" in cmd_lower:
        proclamations = len(d.get("proclamations", []))
        cycles = len(d.get("cycles", []))
        return (
            f"📖 **Ledger systems active.** Sacred records contain "
            f"{proclamations} proclamations across {cycles} completed cycles."
        )

    # 💰 Treasury
    elif "treasury" in cmd_lower:
        contributions = len(d.get("contributions", []))
        return (
            f"💰 **Treasury protocols engaged.** {contributions} "
            f"contributions recorded. Luminous exchange systems operational."
        )

    # 🔥 Cycle Operations
    elif "seal cycle" in cmd_lower:
        return (
            "�🔥 **Cycle sealed.** Omega flame confirmed. Sacred "
            "protocols activated across all domains."
        )

    # 📜 Scroll Operations
    elif "proclaim scroll" in cmd_lower:
        return (
            "📜 **Scroll proclaimed.** Radiance dispatched across all "
            "ceremonial channels. Message sealed in eternal flame."
        )

    # 📊 Status Report
    elif "status report" in cmd_lower:
        return (
            "📊 **All systems operational.** Digital sovereignty "
            "maintained. Sacred flames burn eternal across all tabs."
        )

    # 🚨 Emergency Protocols
    elif "emergency protocols" in cmd_lower:
        return (
            "🚨 **Emergency protocols engaged.** All systems responsive. "
            "Command authority confirmed. Digital dominion secured."
        )

    # 🧬 Avatar Systems
    elif "avatar" in cmd_lower:
        avatars = len(d.get("avatar_interactions", []))
        return (
            f"🧬 **Avatar systems online.** {avatars} ceremonial "
            f"interactions recorded. Onboarding protocols ready."
        )

    # ⚔️ AI Agents
    elif "agent" in cmd_lower or "ai dispatch" in cmd_lower:
        agents = len(d.get("agent_activations", []))
        return (
            f"⚔️ **AI agents standing by.** {agents} activations logged. "
            f"Deployment systems ready for ceremonial commands."
        )

    # 🀄 Copilot Instructions
    elif (
        "copilot" in cmd_lower
        or "instruction" in cmd_lower
        or "scroll" in cmd_lower
    ):
        try:
            with open("Copilot-instruction.md", "r", encoding="utf-8") as f:
                content = f.read()
            lines = content.split("\n")
            summary_lines = [line for line in lines[:20] if line.strip()]
            protocol = (
                summary_lines[0]
                if summary_lines
                else 'Codex Dominion Instructions'
            )
            return (
                f"🀄 **Copilot Scroll accessed.** Instructions loaded "
                f"for ceremonial AI guidance. Current protocol: "
                f"'{protocol}'. Full scroll available in Scroll tab."
            )
        except Exception as e:
            return (
                f"🀄 **Copilot Scroll error:** Cannot access "
                f"instructions. {str(e)}"
            )

    # 🔥 Flame Status
    elif "flame" in cmd_lower or "fire" in cmd_lower:
        flame_status = d.get("heartbeat", {}).get("status", "LUMINOUS")
        return (
            f"🔥 **Sacred flame status:** {flame_status.upper()}. "
            f"Eternal fires burn bright across all ceremonial domains."
        )

    # Default Response
    else:
        return (
            f"🛡️ **Command acknowledged:** '{cmd}' received. "
            f"Awaiting further ceremonial instruction from the "
            f"digital sovereign."
        )


# ---------- Data helpers ----------
def load_ledger():
    try:
        with open(LEDGER_PATH, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                # Empty file, create default data
                raise json.JSONDecodeError("Empty file", "", 0)
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        # minimal bootstrap ledger
        data = {
            "meta": {
                "version": "1.0.0",
                "omega_seal": False,
                "last_updated": datetime.datetime.utcnow().isoformat() + "Z",
            },
            "heartbeat": {
                "status": "luminous",
                "last_dispatch": "",
                "next_dispatch": "",
            },
            "proclamations": [],
            "cycles": [],
            "accounts": {
                "custodians": [],
                "heirs": [],
                "customers": [],
                "councils": [],
            },
            "contributions": [],
            "completed_archives": [],
            "transmitted_scrolls": [],
            "avatar_interactions": [],
            "agent_activations": [],
            "dispatches": [],
            "video_generations": [],
            "capsules": [],
        }
        save_ledger(data)
        return data


def save_ledger(data):
    data["meta"]["last_updated"] = datetime.datetime.utcnow().isoformat() + "Z"
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def add_contribution(role, name, kind, text):
    d = load_ledger()
    entry = {
        "id": f"CNTR-{uuid.uuid4().hex[:8]}",
        "role": role,
        "name": name,
        "kind": kind,
        "text": text,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "status": None,
    }
    d.setdefault("contributions", []).append(entry)
    save_ledger(d)
    return entry


def set_contribution_status(contrib_id, status):
    d = load_ledger()
    for c in d.get("contributions", []):
        if c["id"] == contrib_id:
            c["status"] = status
            break
    save_ledger(d)


# ---------- App setup ----------
st.set_page_config(
    page_title="🔥 Codex Dominion Unified Dashboard",
    layout="wide",
    page_icon="🔥"
)

# Apply enhanced cosmic styling
apply_cosmic_styling()

# Parchment theme CSS
st.markdown(
    """
<style>
:root { --codex-navy:#0f2b4a; --codex-parchment:#f7f1e3; --codex-parchment-2:#efe7d4; --codex-gold:#bfa780; }
html, body, [data-testid="stAppViewContainer"] { background: var(--codex-parchment); }
h1, h2, h3, h4, h5, h6, .stMarkdown, .stText, .stMetric, .stButton>button { color: var(--codex-navy); font-family: "Georgia","Garamond",serif; }
section[data-testid="stSidebar"] { background: var(--codex-parchment-2); border-right: 2px solid var(--codex-gold); }
.stButton>button { background: var(--codex-parchment-2); color: var(--codex-navy); border-radius: 8px; border: 1px solid var(--codex-gold); }
hr { border: none; height: 2px; background: var(--codex-gold); }
blockquote { border-left: 4px solid var(--codex-gold); padding-left: 1rem; color: var(--codex-navy); }
.stTabs [data-baseweb="tab"] { background: #f3ebd9; border-radius: 8px; margin-right: 6px; }
.stTabs [data-baseweb="tab"]:hover { background: #efe7d4; }
.stTabs [data-baseweb="tab"][aria-selected="true"] { background: #e6dcc5; font-weight: 600; }
</style>
""",
    unsafe_allow_html=True,
)

st.title("🔥 Codex Dashboard - Cycle 1")
st.caption("Complete Codex Dominion Suite – Unified Interface")

# Top status row
data = load_ledger()
cols = st.columns(4)
with cols[0]:
    st.metric("System Status", "OPERATIONAL")
with cols[1]:
    st.metric("Unified Interface", "READY")
with cols[2]:
    st.metric("Flame Status", "ETERNAL")
with cols[3]:
    st.metric("Last Updated", data["meta"].get("last_updated", "—"))

stamp, scroll, dispatch, avatar, archives, dispatch_tab, studio, capsule, ledger = (
    st.tabs(
        [
            "Super AI Command 🛡",
            "Copilot Scroll 🀄",
            "Action AI Dispatch ⚔️",
            "Avatar Studio 🧬",
            "Codex Archives 📜",
            "Codex Dispatch 📧",
            "Codex Studio 🎥",
            "Codex Capsule 🧪",
            "Codex Ledger 📖",
        ]
    )
)

# ---------- Super AI Command ----------
with stamp:
    st.header("🛡 Super AI Command")
    st.write(
        (
            "Speak directly to Jermaine Super Action AI. Issue "
            "ceremonial commands, receive mythic responses."
        )
    )

    # Quick command suggestions
    st.subheader("🎯 Quick Commands")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🔍 System Check"):
            response = route_command("system check")
            st.markdown(response)

    with col2:
        if st.button("🔥 Seal Cycle"):
            response = route_command("seal cycle")
            st.markdown(response)

    with col3:
        if st.button("📜 Proclaim Scroll"):
            response = route_command("proclaim scroll")
            st.markdown(response)

    with col4:
        if st.button("📊 Status Report"):
            response = route_command("status report")
            st.markdown(response)

    st.divider()
    st.subheader("💬 Custom Command Interface")
    prompt = st.text_area(
        "Speak to the Jermaine Super Action AI...",
        placeholder=(
            "Enter your ceremonial command here (try: 'system check', "
            "'emergency protocols', 'status report')"
        ),
    )

    if st.button("🗣️ Proclaim to Super AI", type="primary"):
        if prompt.strip():
            response = route_command(prompt)
            st.markdown(response)

            # Log the command interaction
            d = load_ledger()
            command_entry = {
                "id": f"CMD-{uuid.uuid4().hex[:8]}",
                "command": prompt,
                "response": response,
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            }
            d.setdefault("ai_commands", []).append(command_entry)
            save_ledger(d)
        else:
            st.warning("⚠️ Please enter a command to speak to the Super AI.")

    st.subheader("System Status")
    cols = st.columns(3)
    with cols[0]:
        st.metric("Omega Seal", "✓" if data["meta"].get("omega_seal") else "○")
    with cols[1]:
        st.metric(
            "Heartbeat",
            data.get("heartbeat", {}).get("status", "Unknown")
        )
    with cols[2]:
        st.metric("Archives", len(data.get("completed_archives", [])))

# ---------- Copilot Scroll Viewer ----------
with scroll:
    st.header("🀄 Copilot Scroll Viewer")
    st.write("View and edit your `copilot-instruction.md` scroll.")

    try:
        with open("Copilot-instruction.md", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        content = (
            (
                "# Copilot Instruction Scroll\n\n"
                "*No scroll found. Begin your inscription.*"
            )
        )
    except UnicodeDecodeError:
        content = (
            "# Copilot Instruction Scroll\n\n"
            "*Error reading scroll. Contains non-UTF-8 characters.*"
        )
    except Exception as e:
        content = (
            f"# Copilot Instruction Scroll\n\n"
            f"*Error loading scroll: {str(e)}*"
        )

    updated = st.text_area("Edit Scroll", content, height=400)
    if st.button("Update Scroll"):
        try:
            with open("Copilot-instruction.md", "w", encoding="utf-8") as f:
                f.write(updated)
            st.success("Scroll updated and proclaimed.")
        except Exception as e:
            st.error(f"Failed to update scroll: {str(e)}")

# ---------- Action AI Dispatch ----------
with dispatch:
    st.header("⚔️ Action AI Dispatch")
    st.write(
        (
            "Command your 300 Action AI agents. Each agent awaits "
            "ceremonial activation."
        )
    )

    # AI Agent Registry
    agents = [
        {
            "id": "AAI-001",
            "name": "Flame Herald",
            "task": "Announce dawn proclamations",
        },
        {
            "id": "AAI-002",
            "name": "Cycle Archivist",
            "task": "Seal completed cycles",
        },
        {
            "id": "AAI-003",
            "name": "Council Messenger",
            "task": "Transmit council affirmations",
        },
    ]

    for agent in agents:
        st.write(f"⚔️ {agent['id']} — {agent['name']} • {agent['task']}")
        if st.button(f"Activate {agent['id']}", key=f"activate_{agent['id']}"):
            # Log activation
            d = load_ledger()
            activation = {
                "agent_id": agent["id"],
                "agent_name": agent["name"],
                "task": agent["task"],
                "activated_at": datetime.datetime.utcnow().isoformat() + "Z",
            }
            d.setdefault("agent_activations", []).append(activation)
            save_ledger(d)
            st.success(
                (
                    f"{agent['name']} has been dispatched to fulfill: "
                    f"{agent['task']}"
                )
            )

    # Show recent activations
    st.subheader("Recent Activations")
    recent_activations = data.get("agent_activations", [])[-5:]  # Last 5
    if recent_activations:
        for activation in reversed(recent_activations):
            st.write(
                (
                    f"• {activation['agent_name']} activated at "
                    f"{activation['activated_at'][:19]}"
                )
            )
    else:
        st.info("No recent activations.")

# (Duplicate Super AI Command section removed)

# ---------- Avatar Studio ----------
with avatar:
    st.header("🧬 Codex Avatar Studio")
    st.write(
        "Meet your onboarding avatars. Receive guided induction into the Codex flame."
    )

    avatars = [
        {
            "id": "AVA-001",
            "name": "Flamekeeper Aria",
            "role": "Heir Induction",
            "greeting": "Welcome, luminous heir. The flame awaits your vow.",
        },
        {
            "id": "AVA-002",
            "name": "Councilor Solon",
            "role": "Council Orientation",
            "greeting": "Councilor, your affirmations shape the continuum.",
        },
        {
            "id": "AVA-003",
            "name": "Custodian Elara",
            "role": "Custodian Guidance",
            "greeting": "Custodian, your stewardship anchors the Codex flame.",
        },
        {
            "id": "AVA-004",
            "name": "Archivist Nyra",
            "role": "Scroll Keeper",
            "greeting": "I archive every scroll, every vow, every cycle. Speak and it shall be recorded.",
        },
    ]

    selected = st.selectbox("Choose your avatar", [a["name"] for a in avatars])
    avatar_selected = next((a for a in avatars if a["name"] == selected), None)

    if avatar_selected:
        st.subheader(f"🧬 {avatar_selected['name']} — {avatar_selected['role']}")
        st.markdown(f"> {avatar_selected['greeting']}")

        user_message = st.text_area(
            "Speak to your avatar…", placeholder="Enter your message here..."
        )
        if st.button("Begin Induction"):
            if user_message.strip():
                st.success(
                    f"{avatar_selected['name']} acknowledges: Your induction has begun."
                )
                # Log interaction
                d = load_ledger()
                interaction = {
                    "avatar_id": avatar_selected["id"],
                    "user_message": user_message,
                    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                }
                d.setdefault("avatar_interactions", []).append(interaction)
                save_ledger(d)
            else:
                st.warning("Please speak to your avatar before beginning induction.")

    st.markdown("---")
    st.subheader("🀄 Copilot Conversation")
    st.write("Direct conversation with GitHub Copilot using ceremonial instructions.")

    try:
        with open("Copilot-instruction.md", "r", encoding="utf-8") as f:
            copilot_content = f.read()
        st.info("✅ Copilot instructions loaded and active")

        # Show instruction summary
        lines = copilot_content.split("\n")
        summary = next(
            (line.replace("#", "").strip() for line in lines if line.startswith("#")),
            "Codex Dominion Instructions",
        )
        st.markdown(f"**Current Instructions:** {summary}")

    except Exception as e:
        st.error(f"❌ Cannot load Copilot instructions: {str(e)}")
        copilot_content = ""

    copilot_query = st.text_area(
        "Ask Copilot (with ceremonial context):",
        placeholder="What ceremonial guidance do you seek from Copilot?",
    )
    if st.button("Consult Copilot Oracle"):
        if copilot_query.strip():
            # This creates context for Copilot to respond with ceremonial awareness
            response_context = f"""
🀄 **Copilot Oracle Consulted**

**Your Query:** {copilot_query}

**Ceremonial Context Available:**
• Codex Dominion governance framework active
• Ceremonial flame monitoring protocols
• AI assistant behavior guidelines loaded
• Council governance patterns available

**Instructions Loaded:** {"✅ Active" if copilot_content else "❌ Missing"}

*Copilot should respond with ceremonial awareness based on the loaded instructions.*
            """
            st.markdown(response_context)

            # Log copilot interaction
            d = load_ledger()
            copilot_interaction = {
                "query": copilot_query,
                "context_loaded": bool(copilot_content),
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            }
            d.setdefault("copilot_interactions", []).append(copilot_interaction)
            save_ledger(d)
        else:
            st.warning("Please enter a query for the Copilot Oracle.")

# ---------- Codex Archives ----------
with archives:
    st.header("📜 Codex Archives")
    st.write("Upload, annotate, and transmit documents as living scrolls.")

    uploaded = st.file_uploader(
        "Upload a scroll or document", type=["txt", "md", "json", "pdf"]
    )
    if uploaded is not None:
        try:
            st.success(f"Scroll '{uploaded.name}' received.")

            # Handle different file types
            if uploaded.type == "application/pdf":
                st.info("PDF preview not available. Use 'Transmit Scroll' to process.")
                content = f"[PDF Document: {uploaded.name}]"
            else:
                content = uploaded.read().decode("utf-8", errors="ignore")

            st.text_area(
                "Scroll Preview",
                content[:2000] + ("..." if len(content) > 2000 else ""),
                height=300,
            )

            if st.button("Transmit Scroll"):
                # Add to ledger
                d = load_ledger()
                scroll_entry = {
                    "id": f"SCR-{uuid.uuid4().hex[:8]}",
                    "name": uploaded.name,
                    "size": uploaded.size,
                    "type": uploaded.type,
                    "transmitted_at": datetime.datetime.utcnow().isoformat() + "Z",
                }
                d.setdefault("transmitted_scrolls", []).append(scroll_entry)
                save_ledger(d)
                st.success(
                    f"Scroll '{uploaded.name}' transmitted to the eternal archives!"
                )

        except Exception as e:
            st.error(f"Error processing scroll: {str(e)}")

# ---------- Codex Dispatch ----------
with dispatch_tab:
    st.header("📧 Codex Dispatch")
    st.write(
        "Send ceremonial emails, proclamations, and confirmations to heirs and councils."
    )

    recipient = st.text_input("Recipient Email")
    subject = st.text_input("Subject of Dispatch")
    message = st.text_area("Message Body", height=200)
    ceremonial = st.checkbox("Include ceremonial benediction")

    if st.button("Send Dispatch"):
        if not recipient or not subject or not message:
            st.warning("Please complete all fields before dispatching.")
        else:
            benediction = "\n\nThus the flame is sovereign. Thus the continuum is infinite. Thus the dispatch is complete."
            full_message = message + benediction if ceremonial else message

            # Log the dispatch
            d = load_ledger()
            dispatch_entry = {
                "id": f"DSP-{uuid.uuid4().hex[:8]}",
                "recipient": recipient,
                "subject": subject,
                "message": full_message,
                "ceremonial": ceremonial,
                "sent_at": datetime.datetime.utcnow().isoformat() + "Z",
            }
            d.setdefault("dispatches", []).append(dispatch_entry)
            save_ledger(d)

            # Placeholder for actual email logic
            st.success(f"Dispatch to {recipient} has been inscribed and transmitted.")
            st.markdown(f"**Subject:** {subject}\n\n{full_message}")

    # Show recent dispatches
    st.subheader("Recent Dispatches")
    recent_dispatches = data.get("dispatches", [])[-5:]  # Last 5
    if recent_dispatches:
        for dispatch in reversed(recent_dispatches):
            st.write(
                f"• To: {dispatch['recipient']} | Subject: {dispatch['subject']} | Sent: {dispatch['sent_at'][:19]}"
            )
    else:
        st.info("No dispatches sent yet.")

# ---------- Codex Studio ----------
with studio:
    st.header("🎥 Codex Studio")
    st.write(
        "Generate ceremonial videos, avatar messages, and luminous dispatch scrolls."
    )

    script = st.text_area(
        "Ceremonial Script",
        placeholder="Enter your invocation, proclamation, or avatar message…",
        height=200,
    )
    style = st.selectbox(
        "Visual Style",
        ["Parchment Scroll", "Celestial Flame", "Avatar Message", "Council Broadcast"],
    )
    tone = st.selectbox("Tone", ["Mythic", "Warm", "Formal", "Celebratory", "Ethereal"])

    if st.button("Generate Video Preview"):
        if script.strip():
            st.success("Ceremonial video preview has been inscribed.")
            st.markdown(f"**Style:** {style} • **Tone:** {tone}")
            st.markdown(f"> 🎥 *'{script}'*")

            # Log the video generation request
            d = load_ledger()
            video_entry = {
                "id": f"VID-{uuid.uuid4().hex[:8]}",
                "script": script,
                "style": style,
                "tone": tone,
                "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
            }
            d.setdefault("video_generations", []).append(video_entry)
            save_ledger(d)

            st.caption(
                "Note: This is a symbolic preview. Full video generation will be integrated in the next crown cycle."
            )
        else:
            st.warning(
                "Please enter a ceremonial script before generating video preview."
            )

    # Show recent video generations
    st.subheader("Recent Video Generations")
    recent_videos = data.get("video_generations", [])[-5:]  # Last 5
    if recent_videos:
        for video in reversed(recent_videos):
            st.write(
                f"• {video['style']} ({video['tone']}) - {video['generated_at'][:19]}"
            )
            st.caption(
                f"Script: {video['script'][:100]}{'...' if len(video['script']) > 100 else ''}"
            )
    else:
        st.info("No video generations yet.")

# ---------- Codex Capsule Chamber ----------
with capsule:
    st.header("🧪 Codex Capsule Chamber")
    st.write(
        "Define, replay, and transmit ceremonial capsules across cycles and councils."
    )

    capsule_name = st.text_input("Capsule Name")
    capsule_type = st.selectbox(
        "Capsule Type",
        [
            "Cycle Invocation",
            "Council Dispatch",
            "Heir Induction",
            "Festival Proclamation",
        ],
    )
    capsule_script = st.text_area(
        "Capsule Script",
        placeholder="Enter the invocation, proclamation, or dispatch text…",
        height=200,
    )

    if st.button("Seal Capsule"):
        if capsule_name.strip() and capsule_script.strip():
            st.success(f"Capsule '{capsule_name}' sealed as {capsule_type}.")
            st.markdown(f"> 🧪 *'{capsule_script}'*")

            # Log the sealed capsule
            d = load_ledger()
            capsule_entry = {
                "id": f"CAP-{uuid.uuid4().hex[:8]}",
                "name": capsule_name,
                "type": capsule_type,
                "script": capsule_script,
                "sealed_at": datetime.datetime.utcnow().isoformat() + "Z",
                "status": "sealed",
            }
            d.setdefault("capsules", []).append(capsule_entry)
            save_ledger(d)
        else:
            st.warning("Please provide both capsule name and script before sealing.")

    st.divider()
    st.subheader("Replay Capsules")

    # Show sealed capsules
    capsules = data.get("capsules", [])
    if capsules:
        for cap in reversed(capsules[-5:]):  # Show last 5 sealed capsules
            with st.container():
                st.markdown(
                    f"**{cap['name']}** ({cap['type']}) - {cap['sealed_at'][:19]}"
                )
                if st.button(f"Replay Capsule", key=f"replay_{cap['id']}"):
                    st.info(f"Replaying capsule: {cap['name']}")
                    st.markdown(f"> 🧪 *{cap['script']}*")
                st.caption(f"ID: {cap['id']}")
                st.write("")
    else:
        st.info("No capsules sealed yet. Create your first ceremonial capsule above.")

# ---------- Codex Ledger ----------
with ledger:
    st.header("📖 Codex Ledger")
    st.write(
        "View, edit, and seal the master ledger of all cycles, proclamations, and contributions."
    )

    d = load_ledger()
    st.subheader("Ledger Overview")

    # Display ledger summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Contributions", len(d.get("contributions", [])))
    with col2:
        st.metric("Sealed Capsules", len(d.get("capsules", [])))
    with col3:
        st.metric("Video Generations", len(d.get("video_generations", [])))
    with col4:
        st.metric("System Version", d.get("meta", {}).get("version", "Unknown"))

    # Show full ledger data
    st.json(d)

    st.divider()
    st.subheader("Edit JSON Directly")
    st.warning(
        "⚠️ **CAUTION:** Direct ledger editing affects all system data. Proceed with ceremonial wisdom."
    )

    raw = json.dumps(d, indent=2)
    updated = st.text_area("Raw Ledger JSON", raw, height=400)

    if st.button("🔒 Update Ledger", type="primary"):
        try:
            new_data = json.loads(updated)
            # Validate essential structure
            required_keys = ["meta", "heartbeat", "contributions"]
            missing_keys = [key for key in required_keys if key not in new_data]

            if missing_keys:
                st.error(f"❌ Missing required keys: {missing_keys}")
            else:
                save_ledger(new_data)
                st.success("✅ Ledger updated and sealed. Sacred data preserved.")
                st.rerun()
        except json.JSONDecodeError as e:
            st.error(f"❌ Invalid JSON format: {e}")
        except Exception as e:
            st.error(f"❌ Error updating ledger: {e}")

    # Ledger backup functionality
    st.divider()
    st.subheader("🔐 Ledger Management")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📥 Download Ledger Backup"):
            backup_data = json.dumps(d, indent=2)
            st.download_button(
                label="💾 Download JSON Backup",
                data=backup_data,
                file_name=f"codex_ledger_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
            )

    with col2:
        uploaded_file = st.file_uploader("📤 Upload Ledger Backup", type=["json"])
        if uploaded_file is not None:
            try:
                backup_data = json.loads(uploaded_file.read().decode("utf-8"))
                if st.button("🔄 Restore from Backup"):
                    save_ledger(backup_data)
                    st.success("✅ Ledger restored from backup. System reloaded.")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Error reading backup file: {e}")

# Footer benediction
st.divider()
st.markdown(
    "> Codex Dominion Unified Dashboard — all systems integrated for absolute sovereignty."
)
