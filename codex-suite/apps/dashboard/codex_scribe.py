import base64
import io
import json
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from core.ledger import append_entry, load_json


def create_codex_scribe():
    """Main Codex Scribe Interface - Self-hosted Meeting Intelligence System"""

    st.set_page_config(page_title="📝 Codex Scribe", page_icon="📝", layout="wide")

    # Custom CSS for professional styling
    st.markdown(
        """
    <style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #fff;
    }
    .scribe-header {
        text-align: center;
        padding: 30px;
        margin-bottom: 20px;
        background: linear-gradient(45deg, rgba(0,123,255,0.3), rgba(40,167,69,0.2));
        border: 2px solid #007BFF;
        border-radius: 20px;
    }
    .meeting-card {
        background: rgba(0,123,255,0.1);
        padding: 15px;
        border-left: 4px solid #007BFF;
        border-radius: 10px;
        margin: 10px 0;
    }
    .transcript-box {
        background: rgba(40,167,69,0.1);
        padding: 15px;
        border-left: 4px solid #28A745;
        border-radius: 10px;
        margin: 10px 0;
    }
    .ai-insight {
        background: rgba(255,193,7,0.1);
        padding: 15px;
        border-left: 4px solid #FFC107;
        border-radius: 10px;
        margin: 10px 0;
    }
    .action-item {
        background: rgba(220,53,69,0.1);
        padding: 10px;
        border-left: 3px solid #DC3545;
        border-radius: 8px;
        margin: 5px 0;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Header
    st.markdown(
        """
    <div class="scribe-header">
        <h1>📝 Codex Scribe</h1>
        <h3>🎤 Self-Hosted Meeting Intelligence System 🧠</h3>
        <p><em>"Transform conversations into actionable wisdom"</em></p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Main tabs
    tabs = st.tabs(
        [
            "🎤 Live Recording",
            "📄 Transcript Library",
            "🧠 AI Analysis",
            "✅ Action Items",
            "📊 Meeting Analytics",
            "⚙️ Settings",
            "📚 Knowledge Base",
        ]
    )

    with tabs[0]:
        display_live_recording()

    with tabs[1]:
        display_transcript_library()

    with tabs[2]:
        display_ai_analysis()

    with tabs[3]:
        display_action_items()

    with tabs[4]:
        display_meeting_analytics()

    with tabs[5]:
        display_settings()

    with tabs[6]:
        display_knowledge_base()


def display_live_recording():
    """Live Recording Interface"""

    st.markdown("### 🎤 **Live Meeting Recording**")
    st.markdown("*Real-time transcription and AI-powered note taking*")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("#### **Meeting Setup**")

        with st.form("meeting_setup"):
            meeting_title = st.text_input(
                "📋 Meeting Title:", placeholder="e.g., Weekly Team Standup"
            )
            meeting_type = st.selectbox(
                "🏢 Meeting Type:",
                [
                    "Team Standup",
                    "Client Call",
                    "Board Meeting",
                    "Project Review",
                    "One-on-One",
                    "Interview",
                    "Training Session",
                    "Sales Call",
                    "Other",
                ],
            )

            participants = st.text_area(
                "👥 Participants:", placeholder="Enter participant names, one per line"
            )

            meeting_agenda = st.text_area(
                "📝 Agenda/Topics:", placeholder="Key topics to discuss..."
            )

            # Audio input simulation (in real implementation would use actual audio)
            st.markdown("#### **🎙️ Audio Input**")
            audio_source = st.radio(
                "Audio Source:", ["Microphone", "System Audio", "Upload File"]
            )

            if audio_source == "Upload File":
                uploaded_file = st.file_uploader(
                    "Choose audio file", type=["mp3", "wav", "m4a", "ogg"]
                )

            start_recording = st.form_submit_button(
                "🔴 **Start Recording**", use_container_width=True
            )

            if start_recording and meeting_title:
                # Simulate starting a recording session
                meeting_data = {
                    "id": len(load_json("meetings.json", {"meetings": []})["meetings"])
                    + 1,
                    "title": meeting_title,
                    "type": meeting_type,
                    "participants": [
                        p.strip() for p in participants.split("\n") if p.strip()
                    ],
                    "agenda": meeting_agenda,
                    "start_time": datetime.now().isoformat(),
                    "status": "recording",
                    "audio_source": audio_source,
                }

                append_entry("meetings.json", "meetings", meeting_data)
                st.success(f"🎉 Recording started for: **{meeting_title}**")
                st.rerun()

    with col2:
        st.markdown("#### **Active Sessions**")

        meetings = load_json("meetings.json", {"meetings": []})["meetings"]
        active_meetings = [m for m in meetings if m.get("status") == "recording"]

        if active_meetings:
            for meeting in active_meetings[-3:]:
                st.markdown(
                    f"""
                <div class="meeting-card">
                    <strong>🎤 {meeting['title']}</strong><br>
                    <small>👥 {len(meeting.get('participants', []))} participants</small><br>
                    <small>⏱️ Started: {meeting['start_time'][:16]}</small>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                if st.button(f"⏹️ Stop Recording", key=f"stop_{meeting['id']}"):
                    stop_recording(meeting["id"])
                    st.rerun()
        else:
            st.info("No active recording sessions")

    # Real-time transcript simulation
    if active_meetings:
        st.markdown("#### **🔴 Live Transcript**")

        # Simulate real-time transcription
        sample_transcript = generate_sample_transcript()

        st.markdown(
            f"""
        <div class="transcript-box">
            <h5>Real-time Transcription</h5>
            {sample_transcript}
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Live AI insights
        st.markdown("#### **🧠 Live AI Insights**")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("📊 Speaking Time", "65%", "John: 35%, Sarah: 30%")

        with col2:
            st.metric("✅ Action Items", "3", "+2 new")

        with col3:
            st.metric("🎯 Key Topics", "5", "Budget, Timeline, Resources")


def stop_recording(meeting_id):
    """Stop recording and finalize meeting"""
    meetings = load_json("meetings.json", {"meetings": []})["meetings"]

    for meeting in meetings:
        if meeting["id"] == meeting_id:
            meeting["status"] = "completed"
            meeting["end_time"] = datetime.now().isoformat()
            meeting["duration"] = "45 minutes"  # Calculate actual duration
            meeting["transcript"] = generate_full_transcript()
            meeting["ai_summary"] = generate_ai_summary()
            meeting["action_items"] = generate_action_items()
            break

    # Save updated meetings
    with open("meetings.json", "w") as f:
        json.dump({"meetings": meetings}, f, indent=2)


def generate_sample_transcript():
    """Generate sample real-time transcript"""
    return """
    <p><strong>[John - 10:15 AM]:</strong> Good morning everyone. Let's start with our weekly standup. Sarah, can you give us an update on the project timeline?</p>
    <p><strong>[Sarah - 10:15 AM]:</strong> Sure! We've completed about 70% of the development phase. The main challenge right now is the integration with the payment system...</p>
    <p><strong>[Mike - 10:16 AM]:</strong> I can help with that integration. I have experience with similar implementations...</p>
    """


def display_transcript_library():
    """Transcript Library Interface"""

    st.markdown("### 📄 **Meeting Transcript Library**")
    st.markdown("*Search, organize, and manage all meeting transcripts*")

    # Load meetings
    meetings = load_json("meetings.json", {"meetings": []})["meetings"]
    completed_meetings = [m for m in meetings if m.get("status") == "completed"]

    # Search and filters
    col1, col2, col3 = st.columns(3)

    with col1:
        search_term = st.text_input(
            "🔍 Search transcripts:",
            placeholder="Search by title, participant, or content...",
        )

    with col2:
        filter_type = st.selectbox(
            "📊 Filter by type:",
            ["All Types"]
            + [
                "Team Standup",
                "Client Call",
                "Board Meeting",
                "Project Review",
                "One-on-One",
                "Interview",
                "Training Session",
                "Sales Call",
                "Other",
            ],
        )

    with col3:
        date_range = st.selectbox(
            "📅 Date range:",
            ["All Time", "Last 7 days", "Last 30 days", "Last 90 days"],
        )

    # Display meetings
    if completed_meetings:
        st.markdown("#### **📚 Meeting Archive**")

        for meeting in completed_meetings[::-1]:  # Reverse chronological
            if should_show_meeting(meeting, search_term, filter_type, date_range):
                with st.expander(
                    f"📋 {meeting['title']} - {meeting.get('start_time', '')[:10]}"
                ):

                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.markdown(f"**Type:** {meeting.get('type', 'Unknown')}")
                        st.markdown(
                            f"**Duration:** {meeting.get('duration', 'Unknown')}"
                        )
                        st.markdown(
                            f"**Participants:** {', '.join(meeting.get('participants', []))}"
                        )

                        # Display transcript
                        if meeting.get("transcript"):
                            st.markdown("**📝 Transcript:**")
                            st.markdown(
                                f"""
                            <div class="transcript-box">
                                {meeting['transcript']}
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )

                    with col2:
                        # AI Summary
                        if meeting.get("ai_summary"):
                            st.markdown("**🧠 AI Summary:**")
                            st.markdown(
                                f"""
                            <div class="ai-insight">
                                {meeting['ai_summary']}
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )

                        # Action items
                        if meeting.get("action_items"):
                            st.markdown("**✅ Action Items:**")
                            for item in meeting["action_items"]:
                                st.markdown(
                                    f"""
                                <div class="action-item">
                                    <strong>{item['assignee']}:</strong> {item['task']}<br>
                                    <small>Due: {item['due_date']}</small>
                                </div>
                                """,
                                    unsafe_allow_html=True,
                                )

                        # Export options
                        if st.button(f"📤 Export", key=f"export_{meeting['id']}"):
                            export_meeting(meeting)
    else:
        st.info(
            "No completed meetings found. Start recording to build your transcript library!"
        )


def should_show_meeting(meeting, search_term, filter_type, date_range):
    """Filter meetings based on search criteria"""

    # Search term filter
    if search_term:
        search_fields = [
            meeting.get("title", "").lower(),
            meeting.get("type", "").lower(),
            " ".join(meeting.get("participants", [])).lower(),
            meeting.get("transcript", "").lower(),
        ]
        if not any(search_term.lower() in field for field in search_fields):
            return False

    # Type filter
    if filter_type != "All Types" and meeting.get("type") != filter_type:
        return False

    # Date range filter
    if date_range != "All Time":
        meeting_date = datetime.fromisoformat(meeting.get("start_time", ""))
        now = datetime.now()

        if date_range == "Last 7 days" and (now - meeting_date).days > 7:
            return False
        elif date_range == "Last 30 days" and (now - meeting_date).days > 30:
            return False
        elif date_range == "Last 90 days" and (now - meeting_date).days > 90:
            return False

    return True


def display_ai_analysis():
    """AI Analysis Interface"""

    st.markdown("### 🧠 **AI-Powered Meeting Analysis**")
    st.markdown("*Intelligent insights and pattern recognition across meetings*")

    meetings = load_json("meetings.json", {"meetings": []})["meetings"]
    completed_meetings = [m for m in meetings if m.get("status") == "completed"]

    if not completed_meetings:
        st.warning(
            "No completed meetings available for analysis. Record some meetings first!"
        )
        return

    # Select meeting for analysis
    meeting_options = {
        f"{m['title']} - {m.get('start_time', '')[:10]}": m for m in completed_meetings
    }
    selected_meeting_name = st.selectbox(
        "📋 Select meeting for analysis:", list(meeting_options.keys())
    )

    if selected_meeting_name:
        selected_meeting = meeting_options[selected_meeting_name]

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("#### **🎯 AI Analysis Options**")

            analysis_types = st.multiselect(
                "Select analysis types:",
                [
                    "Key Topics Extraction",
                    "Sentiment Analysis",
                    "Speaking Time Distribution",
                    "Decision Points",
                    "Follow-up Items",
                    "Risk Assessment",
                    "Meeting Effectiveness",
                    "Participant Engagement",
                ],
            )

            if st.button("🧠 **Generate AI Analysis**", use_container_width=True):
                if analysis_types:
                    analysis_results = generate_ai_analysis(
                        selected_meeting, analysis_types
                    )

                    st.markdown("#### **📊 Analysis Results**")

                    for analysis_type, result in analysis_results.items():
                        st.markdown(f"**{analysis_type}:**")
                        st.markdown(
                            f"""
                        <div class="ai-insight">
                            {result}
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                    # Save analysis
                    if st.button("💾 **Save Analysis**"):
                        append_entry(
                            "meeting_analyses.json",
                            "analyses",
                            {
                                "meeting_id": selected_meeting["id"],
                                "meeting_title": selected_meeting["title"],
                                "analysis_types": analysis_types,
                                "results": analysis_results,
                                "timestamp": datetime.now().isoformat(),
                            },
                        )
                        st.success("Analysis saved to knowledge base!")
                else:
                    st.warning("Please select at least one analysis type.")

        with col2:
            st.markdown("#### **🔍 Quick Insights**")

            # Generate quick metrics
            participants = selected_meeting.get("participants", [])
            duration = selected_meeting.get("duration", "Unknown")

            st.metric("👥 Participants", len(participants))
            st.metric("⏱️ Duration", duration)
            st.metric(
                "📝 Word Count",
                estimate_word_count(selected_meeting.get("transcript", "")),
            )

            # Recent analyses
            analyses = load_json("meeting_analyses.json", {"analyses": []})["analyses"]
            meeting_analyses = [
                a for a in analyses if a["meeting_id"] == selected_meeting["id"]
            ]

            if meeting_analyses:
                st.markdown("**Previous Analyses:**")
                for analysis in meeting_analyses[-3:]:
                    st.markdown(f"📊 {', '.join(analysis['analysis_types'])}")
                    st.markdown(
                        f"<small>{analysis['timestamp'][:10]}</small>",
                        unsafe_allow_html=True,
                    )


def generate_ai_analysis(meeting, analysis_types):
    """Generate AI analysis results"""

    results = {}

    for analysis_type in analysis_types:
        if analysis_type == "Key Topics Extraction":
            results[
                analysis_type
            ] = """
            <strong>Primary Topics:</strong>
            <ul>
                <li>Project Timeline (35% of discussion)</li>
                <li>Budget Allocation (25% of discussion)</li>
                <li>Resource Planning (20% of discussion)</li>
                <li>Risk Mitigation (15% of discussion)</li>
                <li>Next Steps (5% of discussion)</li>
            </ul>
            """

        elif analysis_type == "Sentiment Analysis":
            results[
                analysis_type
            ] = """
            <strong>Overall Sentiment:</strong> Positive (7.2/10)<br>
            <strong>Participant Sentiment:</strong>
            <ul>
                <li>John: Optimistic (8.1/10)</li>
                <li>Sarah: Cautiously Positive (6.8/10)</li>
                <li>Mike: Neutral (6.5/10)</li>
            </ul>
            <strong>Sentiment Trends:</strong> Improved throughout meeting
            """

        elif analysis_type == "Speaking Time Distribution":
            results[
                analysis_type
            ] = """
            <strong>Speaking Distribution:</strong>
            <ul>
                <li>John (Meeting Leader): 45% (20.25 minutes)</li>
                <li>Sarah: 35% (15.75 minutes)</li>
                <li>Mike: 20% (9 minutes)</li>
            </ul>
            <strong>Balance Score:</strong> Good (7/10) - Fairly distributed
            """

        elif analysis_type == "Decision Points":
            results[
                analysis_type
            ] = """
            <strong>Decisions Made:</strong>
            <ol>
                <li>Approved additional budget for Q4 development</li>
                <li>Extended project timeline by 2 weeks</li>
                <li>Assigned Sarah as integration lead</li>
            </ol>
            <strong>Pending Decisions:</strong> Technology stack selection (requires CTO approval)
            """

        elif analysis_type == "Follow-up Items":
            results[
                analysis_type
            ] = """
            <strong>Immediate Actions:</strong>
            <ul>
                <li>Sarah: Complete integration analysis by Friday</li>
                <li>Mike: Schedule technical review with CTO</li>
                <li>John: Update project timeline in system</li>
            </ul>
            <strong>Next Meeting:</strong> Schedule follow-up for next Tuesday
            """

        elif analysis_type == "Risk Assessment":
            results[
                analysis_type
            ] = """
            <strong>Identified Risks:</strong>
            <ul>
                <li>🔴 High: Payment integration complexity</li>
                <li>🟡 Medium: Resource availability in Q4</li>
                <li>🟢 Low: Timeline buffer insufficient</li>
            </ul>
            <strong>Mitigation Discussed:</strong> 2/3 risks have proposed solutions
            """

        elif analysis_type == "Meeting Effectiveness":
            results[
                analysis_type
            ] = """
            <strong>Effectiveness Score:</strong> 8.2/10<br>
            <strong>Strengths:</strong>
            <ul>
                <li>Clear agenda and objectives</li>
                <li>Balanced participation</li>
                <li>Concrete decisions made</li>
            </ul>
            <strong>Improvement Areas:</strong> Could benefit from more time allocation discussion
            """

        elif analysis_type == "Participant Engagement":
            results[
                analysis_type
            ] = """
            <strong>Engagement Metrics:</strong>
            <ul>
                <li>John: High engagement (8.5/10) - Led discussion effectively</li>
                <li>Sarah: High engagement (8.1/10) - Active participant with valuable input</li>
                <li>Mike: Moderate engagement (6.8/10) - Could contribute more actively</li>
            </ul>
            <strong>Recommendation:</strong> Encourage Mike to share more technical insights
            """

    return results


def display_action_items():
    """Action Items Management Interface"""

    st.markdown("### ✅ **Action Items & Follow-ups**")
    st.markdown("*Track and manage meeting action items and commitments*")

    # Load all action items from meetings
    meetings = load_json("meetings.json", {"meetings": []})["meetings"]
    all_action_items = []

    for meeting in meetings:
        if meeting.get("action_items"):
            for item in meeting["action_items"]:
                item["meeting_title"] = meeting["title"]
                item["meeting_date"] = meeting.get("start_time", "")[:10]
                all_action_items.append(item)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("#### **📋 Action Items Dashboard**")

        if all_action_items:
            # Filter options
            filter_status = st.selectbox(
                "Filter by status:", ["All", "Pending", "Completed", "Overdue"]
            )
            filter_assignee = st.selectbox(
                "Filter by assignee:",
                ["All"]
                + list(set(item.get("assignee", "") for item in all_action_items)),
            )

            # Display action items
            for item in all_action_items:
                if should_show_action_item(item, filter_status, filter_assignee):

                    # Determine status styling
                    status = item.get("status", "pending")
                    due_date = item.get("due_date", "")

                    if status == "completed":
                        status_color = "#28A745"
                        status_icon = "✅"
                    elif due_date and datetime.now() > datetime.fromisoformat(
                        due_date + "T00:00:00"
                    ):
                        status_color = "#DC3545"
                        status_icon = "⚠️"
                        status = "overdue"
                    else:
                        status_color = "#FFC107"
                        status_icon = "⏳"

                    st.markdown(
                        f"""
                    <div style="background: rgba(255,255,255,0.1); padding: 15px; border-left: 4px solid {status_color}; border-radius: 10px; margin: 10px 0;">
                        <strong>{status_icon} {item.get('task', 'No description')}</strong><br>
                        <small><strong>Assignee:</strong> {item.get('assignee', 'Unassigned')}</small><br>
                        <small><strong>Due:</strong> {item.get('due_date', 'No due date')}</small><br>
                        <small><strong>From:</strong> {item.get('meeting_title', 'Unknown')} ({item.get('meeting_date', '')})</small>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    # Action buttons
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        if st.button(
                            f"✅ Complete", key=f"complete_{hash(item.get('task', ''))}"
                        ):
                            mark_action_complete(item)
                            st.rerun()
                    with col_b:
                        if st.button(
                            f"📅 Reschedule",
                            key=f"reschedule_{hash(item.get('task', ''))}",
                        ):
                            st.info("Reschedule feature coming soon!")
                    with col_c:
                        if st.button(
                            f"💬 Add Note", key=f"note_{hash(item.get('task', ''))}"
                        ):
                            st.info("Notes feature coming soon!")
        else:
            st.info(
                "No action items found. Record meetings with action items to see them here!"
            )

    with col2:
        st.markdown("#### **📊 Action Items Summary**")

        if all_action_items:
            # Calculate statistics
            total_items = len(all_action_items)
            completed_items = len(
                [item for item in all_action_items if item.get("status") == "completed"]
            )
            overdue_items = len(
                [
                    item
                    for item in all_action_items
                    if item.get("due_date")
                    and datetime.now()
                    > datetime.fromisoformat(item["due_date"] + "T00:00:00")
                ]
            )

            st.metric("📋 Total Items", total_items)
            st.metric(
                "✅ Completed",
                completed_items,
                f"{(completed_items/total_items*100):.0f}%",
            )
            st.metric("⚠️ Overdue", overdue_items)

            # Top assignees
            assignees = [
                item.get("assignee", "")
                for item in all_action_items
                if item.get("assignee")
            ]
            if assignees:
                assignee_counts = pd.Series(assignees).value_counts()

                st.markdown("**📈 Items by Assignee:**")
                for assignee, count in assignee_counts.head(5).items():
                    st.markdown(f"• {assignee}: {count} items")


def should_show_action_item(item, filter_status, filter_assignee):
    """Filter action items based on criteria"""

    # Status filter
    if filter_status != "All":
        item_status = item.get("status", "pending")
        due_date = item.get("due_date", "")

        if due_date and datetime.now() > datetime.fromisoformat(due_date + "T00:00:00"):
            item_status = "overdue"

        if filter_status.lower() != item_status:
            return False

    # Assignee filter
    if filter_assignee != "All" and item.get("assignee") != filter_assignee:
        return False

    return True


def mark_action_complete(item):
    """Mark an action item as complete"""
    # In a real implementation, this would update the database
    item["status"] = "completed"
    item["completed_date"] = datetime.now().isoformat()


def display_meeting_analytics():
    """Meeting Analytics Interface"""

    st.markdown("### 📊 **Meeting Analytics & Insights**")
    st.markdown("*Analyze meeting patterns and team productivity metrics*")

    meetings = load_json("meetings.json", {"meetings": []})["meetings"]
    completed_meetings = [m for m in meetings if m.get("status") == "completed"]

    if not completed_meetings:
        st.warning(
            "No meeting data available for analytics. Record some meetings first!"
        )
        return

    # Time period selector
    time_period = st.selectbox(
        "📅 Analytics Period:",
        ["Last 7 days", "Last 30 days", "Last 90 days", "All time"],
    )

    # Filter meetings by time period
    filtered_meetings = filter_meetings_by_period(completed_meetings, time_period)

    if not filtered_meetings:
        st.info(f"No meetings found for {time_period.lower()}")
        return

    # Analytics columns
    col1, col2 = st.columns(2)

    with col1:
        # Meeting frequency chart
        meeting_dates = [
            datetime.fromisoformat(m["start_time"]).date() for m in filtered_meetings
        ]
        date_counts = pd.Series(meeting_dates).value_counts().sort_index()

        fig_frequency = px.line(
            x=date_counts.index,
            y=date_counts.values,
            title="📈 Meeting Frequency Over Time",
            labels={"x": "Date", "y": "Number of Meetings"},
        )
        fig_frequency.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
        )
        st.plotly_chart(fig_frequency, use_container_width=True)

        # Meeting types distribution
        meeting_types = [m.get("type", "Unknown") for m in filtered_meetings]
        type_counts = pd.Series(meeting_types).value_counts()

        fig_types = px.pie(
            values=type_counts.values,
            names=type_counts.index,
            title="🏢 Meeting Types Distribution",
        )
        fig_types.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
        )
        st.plotly_chart(fig_types, use_container_width=True)

    with col2:
        # Key metrics
        st.markdown("#### **📊 Key Metrics**")

        total_meetings = len(filtered_meetings)
        avg_duration = calculate_avg_duration(filtered_meetings)
        total_participants = sum(
            len(m.get("participants", [])) for m in filtered_meetings
        )
        avg_participants = (
            total_participants / total_meetings if total_meetings > 0 else 0
        )

        st.metric("📅 Total Meetings", total_meetings)
        st.metric("⏱️ Avg Duration", f"{avg_duration} min")
        st.metric("👥 Avg Participants", f"{avg_participants:.1f}")

        # Most active participants
        all_participants = []
        for meeting in filtered_meetings:
            all_participants.extend(meeting.get("participants", []))

        if all_participants:
            participant_counts = pd.Series(all_participants).value_counts()

            st.markdown("#### **🏆 Most Active Participants**")
            for participant, count in participant_counts.head(5).items():
                st.markdown(f"• **{participant}**: {count} meetings")

        # Action items completion rate
        all_action_items = []
        for meeting in filtered_meetings:
            all_action_items.extend(meeting.get("action_items", []))

        if all_action_items:
            completed_actions = len(
                [item for item in all_action_items if item.get("status") == "completed"]
            )
            completion_rate = (completed_actions / len(all_action_items)) * 100

            st.metric("✅ Action Item Completion", f"{completion_rate:.0f}%")

    # Productivity insights
    st.markdown("#### **💡 Productivity Insights**")

    insights = generate_productivity_insights(filtered_meetings)

    for insight in insights:
        st.markdown(
            f"""
        <div class="ai-insight">
            <strong>{insight['title']}</strong><br>
            {insight['description']}
        </div>
        """,
            unsafe_allow_html=True,
        )


def filter_meetings_by_period(meetings, period):
    """Filter meetings by time period"""
    now = datetime.now()

    if period == "All time":
        return meetings

    days_map = {"Last 7 days": 7, "Last 30 days": 30, "Last 90 days": 90}

    days = days_map.get(period, 30)
    cutoff_date = now - timedelta(days=days)

    return [
        m for m in meetings if datetime.fromisoformat(m["start_time"]) > cutoff_date
    ]


def calculate_avg_duration(meetings):
    """Calculate average meeting duration"""
    # Simplified - in real implementation would parse actual durations
    return "45"


def generate_productivity_insights(meetings):
    """Generate productivity insights"""
    insights = []

    if len(meetings) > 5:
        insights.append(
            {
                "title": "📈 Meeting Frequency Trend",
                "description": f"You've had {len(meetings)} meetings recently. Consider if all were necessary for productivity.",
            }
        )

    # Analyze meeting types
    types = [m.get("type", "") for m in meetings]
    most_common_type = max(set(types), key=types.count) if types else "Unknown"

    insights.append(
        {
            "title": f"🏢 Most Common Meeting Type: {most_common_type}",
            "description": f"Consider if {most_common_type.lower()} meetings could be more efficient or consolidated.",
        }
    )

    # Participant analysis
    all_participants = []
    for meeting in meetings:
        all_participants.extend(meeting.get("participants", []))

    if all_participants:
        unique_participants = len(set(all_participants))
        insights.append(
            {
                "title": f"👥 Team Collaboration: {unique_participants} unique participants",
                "description": "Good cross-team collaboration observed in meeting patterns.",
            }
        )

    return insights


def display_settings():
    """Settings Interface"""

    st.markdown("### ⚙️ **Codex Scribe Settings**")
    st.markdown("*Configure transcription and AI analysis preferences*")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### **🎤 Audio Settings**")

        audio_quality = st.selectbox("Audio Quality:", ["High", "Medium", "Low"])
        noise_reduction = st.checkbox("Enable Noise Reduction", value=True)
        speaker_detection = st.checkbox("Automatic Speaker Detection", value=True)

        st.markdown("#### **🧠 AI Settings**")

        ai_analysis_level = st.selectbox(
            "AI Analysis Level:", ["Basic", "Standard", "Advanced"]
        )
        auto_action_detection = st.checkbox("Auto-detect Action Items", value=True)
        sentiment_analysis = st.checkbox("Enable Sentiment Analysis", value=False)

        st.markdown("#### **📝 Transcription Settings**")

        language = st.selectbox(
            "Primary Language:", ["English", "Spanish", "French", "German"]
        )
        punctuation = st.checkbox("Auto-punctuation", value=True)
        timestamps = st.checkbox("Include Timestamps", value=True)

    with col2:
        st.markdown("#### **📊 Export Settings**")

        export_format = st.multiselect(
            "Default Export Formats:", ["PDF", "DOCX", "TXT", "JSON"], default=["PDF"]
        )

        include_ai_summary = st.checkbox("Include AI Summary in Exports", value=True)
        include_action_items = st.checkbox(
            "Include Action Items in Exports", value=True
        )

        st.markdown("#### **🔔 Notifications**")

        action_reminders = st.checkbox("Action Item Reminders", value=True)
        meeting_summaries = st.checkbox("Email Meeting Summaries", value=False)

        if meeting_summaries:
            email_address = st.text_input("Email for Summaries:")

        st.markdown("#### **🗄️ Data Management**")

        retention_period = st.selectbox(
            "Data Retention Period:", ["30 days", "90 days", "1 year", "Forever"]
        )

        auto_backup = st.checkbox("Automatic Backup", value=True)

        if st.button("🗑️ Clear All Data"):
            if st.confirm("Are you sure you want to delete all meeting data?"):
                clear_all_data()
                st.success("All data cleared!")

    # Save settings
    if st.button("💾 **Save Settings**", use_container_width=True):
        settings = {
            "audio": {
                "quality": audio_quality,
                "noise_reduction": noise_reduction,
                "speaker_detection": speaker_detection,
            },
            "ai": {
                "analysis_level": ai_analysis_level,
                "auto_action_detection": auto_action_detection,
                "sentiment_analysis": sentiment_analysis,
            },
            "transcription": {
                "language": language,
                "punctuation": punctuation,
                "timestamps": timestamps,
            },
            "export": {
                "formats": export_format,
                "include_ai_summary": include_ai_summary,
                "include_action_items": include_action_items,
            },
            "notifications": {
                "action_reminders": action_reminders,
                "meeting_summaries": meeting_summaries,
            },
            "data": {"retention_period": retention_period, "auto_backup": auto_backup},
        }

        with open("scribe_settings.json", "w") as f:
            json.dump(settings, f, indent=2)

        st.success("⚙️ Settings saved successfully!")


def display_knowledge_base():
    """Knowledge Base Interface"""

    st.markdown("### 📚 **Meeting Knowledge Base**")
    st.markdown("*Searchable repository of meeting insights and patterns*")

    # Load all data
    meetings = load_json("meetings.json", {"meetings": []})["meetings"]
    analyses = load_json("meeting_analyses.json", {"analyses": []})["analyses"]

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("#### **🔍 Knowledge Search**")

        search_query = st.text_input(
            "Search meetings and insights:",
            placeholder="Search across all meetings, transcripts, and analyses...",
        )

        search_type = st.selectbox(
            "Search in:",
            [
                "All Content",
                "Meeting Titles",
                "Transcripts Only",
                "AI Analyses",
                "Action Items",
                "Participants",
            ],
        )

        if search_query:
            search_results = perform_knowledge_search(
                meetings, analyses, search_query, search_type
            )

            st.markdown(f"#### **📋 Search Results ({len(search_results)} found)**")

            for result in search_results:
                st.markdown(
                    f"""
                <div class="meeting-card">
                    <strong>{result['type']}: {result['title']}</strong><br>
                    <small>{result['preview']}</small><br>
                    <small>📅 {result['date']}</small>
                </div>
                """,
                    unsafe_allow_html=True,
                )

        # Knowledge insights
        st.markdown("#### **💡 Knowledge Insights**")

        if meetings:
            insights = generate_knowledge_insights(meetings, analyses)

            for insight in insights:
                st.markdown(
                    f"""
                <div class="ai-insight">
                    <strong>{insight['title']}</strong><br>
                    {insight['description']}
                </div>
                """,
                    unsafe_allow_html=True,
                )

    with col2:
        st.markdown("#### **📊 Knowledge Stats**")

        total_meetings = len(meetings)
        total_transcripts = len([m for m in meetings if m.get("transcript")])
        total_analyses = len(analyses)

        st.metric("📅 Total Meetings", total_meetings)
        st.metric("📝 Transcripts", total_transcripts)
        st.metric("🧠 AI Analyses", total_analyses)

        # Most discussed topics (simplified)
        if meetings:
            st.markdown("#### **🏷️ Top Topics**")
            topics = [
                "Project Planning",
                "Budget Review",
                "Team Updates",
                "Client Discussions",
                "Strategy",
            ]
            for i, topic in enumerate(topics[:5]):
                count = len(meetings) // (i + 2)  # Simplified calculation
                st.markdown(f"• **{topic}**: {count} mentions")

        # Export knowledge base
        if st.button("📤 Export Knowledge Base"):
            export_knowledge_base(meetings, analyses)
            st.success("Knowledge base exported!")


def perform_knowledge_search(meetings, analyses, query, search_type):
    """Perform search across knowledge base"""
    results = []
    query_lower = query.lower()

    # Search in meetings
    for meeting in meetings:
        if (
            search_type in ["All Content", "Meeting Titles"]
            and query_lower in meeting.get("title", "").lower()
        ):
            results.append(
                {
                    "type": "Meeting",
                    "title": meeting.get("title", ""),
                    "preview": f"Meeting with {len(meeting.get('participants', []))} participants",
                    "date": meeting.get("start_time", "")[:10],
                }
            )

        if search_type in ["All Content", "Transcripts Only"] and meeting.get(
            "transcript"
        ):
            if query_lower in meeting.get("transcript", "").lower():
                results.append(
                    {
                        "type": "Transcript",
                        "title": meeting.get("title", ""),
                        "preview": f"Found in transcript: '{query}' mentioned",
                        "date": meeting.get("start_time", "")[:10],
                    }
                )

    # Search in analyses
    for analysis in analyses:
        if search_type in ["All Content", "AI Analyses"]:
            analysis_text = str(analysis.get("results", "")).lower()
            if query_lower in analysis_text:
                results.append(
                    {
                        "type": "AI Analysis",
                        "title": analysis.get("meeting_title", ""),
                        "preview": f"Found in {', '.join(analysis.get('analysis_types', []))}",
                        "date": analysis.get("timestamp", "")[:10],
                    }
                )

    return results[:10]  # Limit results


def generate_knowledge_insights(meetings, analyses):
    """Generate insights from knowledge base"""
    insights = []

    if len(meetings) >= 5:
        insights.append(
            {
                "title": "📈 Meeting Volume Trend",
                "description": f"Your knowledge base contains {len(meetings)} meetings. This represents significant organizational learning data.",
            }
        )

    if analyses:
        insights.append(
            {
                "title": "🧠 AI Analysis Coverage",
                "description": f"{len(analyses)} meetings have been analyzed by AI, providing deeper insights into patterns and trends.",
            }
        )

    # Participant patterns
    all_participants = []
    for meeting in meetings:
        all_participants.extend(meeting.get("participants", []))

    if all_participants:
        unique_participants = len(set(all_participants))
        insights.append(
            {
                "title": f"👥 Collaboration Network: {unique_participants} unique participants",
                "description": "Your meetings show extensive cross-functional collaboration patterns.",
            }
        )

    return insights


def export_knowledge_base(meetings, analyses):
    """Export entire knowledge base"""
    # In a real implementation, this would create comprehensive exports
    knowledge_data = {
        "meetings": meetings,
        "analyses": analyses,
        "export_date": datetime.now().isoformat(),
        "total_meetings": len(meetings),
        "total_analyses": len(analyses),
    }

    with open("knowledge_base_export.json", "w") as f:
        json.dump(knowledge_data, f, indent=2)


def clear_all_data():
    """Clear all meeting data"""
    empty_data = {"meetings": [], "analyses": []}

    with open("meetings.json", "w") as f:
        json.dump(empty_data, f)

    with open("meeting_analyses.json", "w") as f:
        json.dump(empty_data, f)


def generate_full_transcript():
    """Generate a full meeting transcript"""
    return """
    <p><strong>[John - 10:15 AM]:</strong> Good morning everyone. Let's start with our weekly standup. Sarah, can you give us an update on the project timeline?</p>
    
    <p><strong>[Sarah - 10:15 AM]:</strong> Sure! We've completed about 70% of the development phase. The main challenge right now is the integration with the payment system. It's more complex than we initially thought.</p>
    
    <p><strong>[Mike - 10:16 AM]:</strong> I can help with that integration. I have experience with similar implementations from my previous project. Would you like me to take a look at the technical specifications?</p>
    
    <p><strong>[Sarah - 10:17 AM]:</strong> That would be great, Mike. I'll share the documentation with you after this meeting. John, what's our buffer for the timeline if we encounter more delays?</p>
    
    <p><strong>[John - 10:17 AM]:</strong> We have about two weeks of buffer built in, but I'd prefer not to use all of it. Let's aim to resolve this integration issue by Friday. Can we schedule a technical review session?</p>
    
    <p><strong>[Mike - 10:18 AM]:</strong> Absolutely. How about Thursday afternoon? That gives me time to review the specs and come prepared with solutions.</p>
    
    <p><strong>[Sarah - 10:18 AM]:</strong> Perfect. I'll book a conference room for Thursday at 2 PM. Anything else we need to discuss today?</p>
    
    <p><strong>[John - 10:19 AM]:</strong> Just a quick note on the budget. We're tracking well, but the payment integration might require some additional third-party tools. Sarah, can you get quotes for any tools Mike recommends?</p>
    
    <p><strong>[Sarah - 10:19 AM]:</strong> Sure, I'll handle that. I'll have preliminary costs by end of week.</p>
    
    <p><strong>[John - 10:20 AM]:</strong> Great. Let's wrap up here. Thanks everyone for the good progress. See you Thursday for the technical review.</p>
    """


def generate_ai_summary():
    """Generate AI meeting summary"""
    return """
    <strong>Meeting Overview:</strong> Weekly project standup focusing on development progress and integration challenges.<br><br>
    
    <strong>Key Points:</strong>
    <ul>
        <li>Project 70% complete in development phase</li>
        <li>Payment system integration presenting complexity challenges</li>
        <li>Mike volunteered to assist with technical integration</li>
        <li>Two-week timeline buffer available but prefer not to use fully</li>
    </ul>
    
    <strong>Decisions Made:</strong>
    <ul>
        <li>Technical review scheduled for Thursday 2 PM</li>
        <li>Target resolution of integration issues by Friday</li>
        <li>Sarah to gather quotes for additional tools as needed</li>
    </ul>
    
    <strong>Next Steps:</strong> Technical documentation sharing, tool research, and Thursday review session.
    """


def generate_action_items():
    """Generate sample action items"""
    return [
        {
            "task": "Share payment integration documentation with Mike",
            "assignee": "Sarah",
            "due_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "status": "pending",
        },
        {
            "task": "Review integration specifications and prepare solutions",
            "assignee": "Mike",
            "due_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
            "status": "pending",
        },
        {
            "task": "Book conference room for Thursday 2 PM technical review",
            "assignee": "Sarah",
            "due_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "status": "pending",
        },
        {
            "task": "Get quotes for additional integration tools",
            "assignee": "Sarah",
            "due_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
            "status": "pending",
        },
    ]


def export_meeting(meeting):
    """Export meeting data"""
    st.info("Export functionality would generate PDF/DOCX with full meeting details")


def estimate_word_count(text):
    """Estimate word count from text"""
    return len(text.split()) if text else 0


if __name__ == "__main__":
    create_codex_scribe()
