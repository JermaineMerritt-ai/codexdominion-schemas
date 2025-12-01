#!/usr/bin/env python3
"""
Codex Ebook Manager

Complete ebook management system for the Codex Dominion with creation,
viewing, organization, and publishing capabilities.
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import streamlit as st

# Import our ebook generation capabilities
from advanced_ebook_generator import AdvancedCodexEbookGenerator


class CodexEbookManager:
    """Complete ebook management system"""

    def __init__(self):
        self.ebook_dir = Path("ebooks")
        self.archive_dir = Path("ebook_archive")
        self.templates_dir = Path("ebook_templates")

        # Ensure directories exist
        for directory in [self.ebook_dir, self.archive_dir, self.templates_dir]:
            directory.mkdir(exist_ok=True)

        self.generator = AdvancedCodexEbookGenerator()

    def list_ebooks(self) -> Dict[str, Dict]:
        """List all available ebooks with metadata"""

        ebooks = {}

        for project_file in self.ebook_dir.glob("*_project.json"):
            try:
                with open(project_file, "r", encoding="utf-8") as f:
                    project_data = json.load(f)

                ebook_id = project_file.stem.replace("_project", "")
                ebooks[ebook_id] = project_data

            except Exception as e:
                st.error(f"Error loading {project_file}: {e}")

        return ebooks

    def create_ebook_from_template(
        self, template_type: str, **kwargs
    ) -> Optional[Dict[str, str]]:
        """Create ebook from predefined templates"""

        if template_type == "proclamations":
            return self.generator.create_proclamations_ebook()

        elif template_type == "comprehensive":
            return self.generator.create_comprehensive_ebook(
                kwargs.get("title", "Codex Dominion Guide"),
                kwargs.get("author", "Codex Council"),
                kwargs.get("theme", "dominion"),
                kwargs.get("sources", ["proclamations", "documentation"]),
                kwargs.get("formats", ["html", "markdown"]),
            )

        elif template_type == "custom":
            content = kwargs.get("content", [])
            if not content:
                return None

            return self.generator.create_ebook_from_content(
                content,
                kwargs.get("title", "Custom Ebook"),
                kwargs.get("author", "Codex Council"),
                kwargs.get("formats", ["html"]),
                kwargs.get("theme", "dominion"),
                kwargs.get("metadata", {}),
            )

        return None

    def archive_ebook(self, ebook_id: str) -> bool:
        """Archive an ebook to the archive directory"""

        try:
            # Find all files for this ebook
            ebook_files = list(self.ebook_dir.glob(f"{ebook_id}*"))

            if not ebook_files:
                return False

            # Create archive subdirectory
            archive_subdir = self.archive_dir / ebook_id
            archive_subdir.mkdir(exist_ok=True)

            # Move files to archive
            for file_path in ebook_files:
                dest_path = archive_subdir / file_path.name
                shutil.move(str(file_path), str(dest_path))

            return True

        except Exception as e:
            st.error(f"Error archiving ebook: {e}")
            return False

    def delete_ebook(self, ebook_id: str) -> bool:
        """Delete an ebook and all associated files"""

        try:
            # Find all files for this ebook
            ebook_files = list(self.ebook_dir.glob(f"{ebook_id}*"))

            # Delete files
            for file_path in ebook_files:
                file_path.unlink()

            return True

        except Exception as e:
            st.error(f"Error deleting ebook: {e}")
            return False

    def export_ebook(self, ebook_id: str, export_dir: str) -> bool:
        """Export ebook to external directory"""

        try:
            export_path = Path(export_dir)
            export_path.mkdir(parents=True, exist_ok=True)

            # Find all files for this ebook
            ebook_files = list(self.ebook_dir.glob(f"{ebook_id}*"))

            # Copy files to export directory
            for file_path in ebook_files:
                dest_path = export_path / file_path.name
                shutil.copy2(str(file_path), str(dest_path))

            return True

        except Exception as e:
            st.error(f"Error exporting ebook: {e}")
            return False

    def get_ebook_stats(self) -> Dict[str, Any]:
        """Get statistics about ebook collection"""

        ebooks = self.list_ebooks()

        stats = {
            "total_ebooks": len(ebooks),
            "formats": {"html": 0, "markdown": 0, "json": 0, "pdf": 0},
            "themes": {},
            "total_chapters": 0,
            "creation_dates": [],
        }

        for ebook_data in ebooks.values():
            metadata = ebook_data.get("metadata", {})

            # Count formats
            output_files = ebook_data.get("output_files", {})
            for fmt in output_files:
                if fmt in stats["formats"]:
                    stats["formats"][fmt] += 1

            # Count themes
            theme = metadata.get("theme", "unknown")
            stats["themes"][theme] = stats["themes"].get(theme, 0) + 1

            # Count chapters
            chapters = ebook_data.get("chapters", [])
            stats["total_chapters"] += len(chapters)

            # Track creation dates
            created = metadata.get("created")
            if created:
                stats["creation_dates"].append(created)

        return stats


def run_ebook_management_dashboard():
    """Run the Streamlit ebook management dashboard"""

    st.set_page_config(page_title="Codex Ebook Manager", page_icon="📚", layout="wide")

    st.title("📚 Codex Ebook Manager")
    st.markdown("*Complete ebook management system for the Codex Dominion*")

    manager = CodexEbookManager()

    # Sidebar navigation
    st.sidebar.title("🏛️ Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["📖 Library", "➕ Create New", "📊 Statistics", "⚙️ Management"],
    )

    if page == "📖 Library":
        show_library_page(manager)
    elif page == "➕ Create New":
        show_create_page(manager)
    elif page == "📊 Statistics":
        show_statistics_page(manager)
    elif page == "⚙️ Management":
        show_management_page(manager)


def show_library_page(manager):
    """Show the ebook library page"""

    st.header("📖 Ebook Library")

    ebooks = manager.list_ebooks()

    if not ebooks:
        st.info(
            "No ebooks found. Create your first ebook using the 'Create New' section!"
        )
        return

    # Display ebooks in a grid
    cols = st.columns(2)

    for i, (ebook_id, ebook_data) in enumerate(ebooks.items()):
        col = cols[i % 2]

        with col:
            with st.container():
                metadata = ebook_data.get("metadata", {})
                chapters = ebook_data.get("chapters", [])
                output_files = ebook_data.get("output_files", {})

                st.subheader(f"📖 {metadata.get('title', 'Unknown Title')}")

                st.write(f"**Author:** {metadata.get('author', 'Unknown')}")
                st.write(f"**Theme:** {metadata.get('theme', 'default')}")
                st.write(f"**Chapters:** {len(chapters)}")

                # Show available formats
                format_badges = []
                for fmt in output_files:
                    format_badges.append(f"`{fmt.upper()}`")

                if format_badges:
                    st.write(f"**Formats:** {' '.join(format_badges)}")

                # Action buttons
                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button(f"📖 View", key=f"view_{ebook_id}"):
                        st.session_state[f"viewing_{ebook_id}"] = True

                with col2:
                    if "html" in output_files:
                        html_path = Path(output_files["html"])
                        if html_path.exists():
                            with open(html_path, "rb") as f:
                                st.download_button(
                                    "⬇️ HTML",
                                    f.read(),
                                    file_name=html_path.name,
                                    mime="text/html",
                                    key=f"download_html_{ebook_id}",
                                )

                with col3:
                    if st.button(f"🗂️ Manage", key=f"manage_{ebook_id}"):
                        st.session_state[f"managing_{ebook_id}"] = True

                # Show content if viewing
                if st.session_state.get(f"viewing_{ebook_id}", False):
                    show_ebook_content(ebook_data, ebook_id)

                # Show management options if managing
                if st.session_state.get(f"managing_{ebook_id}", False):
                    show_ebook_management(manager, ebook_id, ebook_data)

                st.markdown("---")


def show_ebook_content(ebook_data, ebook_id):
    """Show ebook content in expandable section"""

    with st.expander(f"📄 Content Preview", expanded=True):
        output_files = ebook_data.get("output_files", {})

        if "html" in output_files:
            html_path = Path(output_files["html"])
            if html_path.exists():
                try:
                    with open(html_path, "r", encoding="utf-8") as f:
                        html_content = f.read()

                    # Show first part of HTML content
                    st.components.v1.html(html_content, height=400, scrolling=True)

                except Exception as e:
                    st.error(f"Error loading HTML content: {e}")

        if st.button(f"❌ Close Preview", key=f"close_view_{ebook_id}"):
            st.session_state[f"viewing_{ebook_id}"] = False
            st.experimental_rerun()


def show_ebook_management(manager, ebook_id, ebook_data):
    """Show ebook management options"""

    with st.expander(f"🗂️ Management Options", expanded=True):

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button(f"📦 Archive", key=f"archive_{ebook_id}"):
                if manager.archive_ebook(ebook_id):
                    st.success("Ebook archived successfully!")
                    st.experimental_rerun()

        with col2:
            export_dir = st.text_input(f"Export to:", key=f"export_dir_{ebook_id}")
            if st.button(f"📤 Export", key=f"export_{ebook_id}") and export_dir:
                if manager.export_ebook(ebook_id, export_dir):
                    st.success(f"Ebook exported to {export_dir}")

        with col3:
            if st.button(f"🗑️ Delete", key=f"delete_{ebook_id}"):
                if st.session_state.get(f"confirm_delete_{ebook_id}", False):
                    if manager.delete_ebook(ebook_id):
                        st.success("Ebook deleted successfully!")
                        st.experimental_rerun()
                else:
                    st.session_state[f"confirm_delete_{ebook_id}"] = True
                    st.warning("Click again to confirm deletion")

        if st.button(f"❌ Close Management", key=f"close_manage_{ebook_id}"):
            st.session_state[f"managing_{ebook_id}"] = False
            st.experimental_rerun()


def show_create_page(manager):
    """Show the ebook creation page"""

    st.header("➕ Create New Ebook")

    creation_type = st.selectbox(
        "Choose creation method:",
        ["📜 From Proclamations", "📋 Comprehensive Guide", "✏️ Custom Content"],
    )

    if creation_type == "📜 From Proclamations":
        st.subheader("Sacred Proclamations Ebook")
        st.info("Create an ebook from the sacred proclamations in proclamations.json")

        if st.button("🔥 Generate Sacred Proclamations Ebook"):
            with st.spinner("Creating sacred ebook..."):
                try:
                    output_files = manager.create_ebook_from_template("proclamations")

                    if output_files:
                        st.success("Sacred Proclamations ebook created successfully!")

                        for fmt, path in output_files.items():
                            st.write(f"📄 {fmt.upper()}: `{path}`")
                    else:
                        st.error("Failed to create ebook")

                except Exception as e:
                    st.error(f"Error creating ebook: {e}")

    elif creation_type == "📋 Comprehensive Guide":
        st.subheader("Comprehensive System Guide")

        with st.form("comprehensive_form"):
            title = st.text_input(
                "Ebook Title", value="Codex Dominion: Complete System Guide"
            )
            author = st.text_input("Author", value="The Codex Council")
            theme = st.selectbox("Theme", ["dominion", "flame", "cosmic", "council"])

            st.write("**Content Sources:**")
            include_proclamations = st.checkbox("📜 Proclamations", value=True)
            include_docs = st.checkbox("📚 Documentation", value=True)

            st.write("**Output Formats:**")
            format_html = st.checkbox("🌐 HTML", value=True)
            format_md = st.checkbox("📝 Markdown", value=True)
            format_json = st.checkbox("📊 JSON", value=False)

            submitted = st.form_submit_button("🚀 Generate Comprehensive Guide")

            if submitted:
                sources = []
                if include_proclamations:
                    sources.append("proclamations")
                if include_docs:
                    sources.append("documentation")

                formats = []
                if format_html:
                    formats.append("html")
                if format_md:
                    formats.append("markdown")
                if format_json:
                    formats.append("json")

                if not sources:
                    st.error("Please select at least one content source")
                elif not formats:
                    st.error("Please select at least one output format")
                else:
                    with st.spinner("Generating comprehensive ebook..."):
                        try:
                            output_files = manager.create_ebook_from_template(
                                "comprehensive",
                                title=title,
                                author=author,
                                theme=theme,
                                sources=sources,
                                formats=formats,
                            )

                            if output_files:
                                st.success("Comprehensive ebook created successfully!")

                                for fmt, path in output_files.items():
                                    st.write(f"📄 {fmt.upper()}: `{path}`")
                            else:
                                st.error("Failed to create ebook")

                        except Exception as e:
                            st.error(f"Error creating ebook: {e}")

    elif creation_type == "✏️ Custom Content":
        st.subheader("Custom Content Ebook")

        with st.form("custom_form"):
            title = st.text_input("Ebook Title", value="Custom Ebook")
            author = st.text_input("Author", value="Codex Council")
            theme = st.selectbox("Theme", ["dominion", "flame", "cosmic", "council"])

            st.write("**Chapter Content:**")

            num_chapters = st.number_input(
                "Number of Chapters", min_value=1, max_value=20, value=3
            )

            chapters = []
            for i in range(num_chapters):
                st.write(f"**Chapter {i+1}:**")
                chapter_title = st.text_input(
                    f"Chapter {i+1} Title", value=f"Chapter {i+1}"
                )
                chapter_content = st.text_area(
                    f"Chapter {i+1} Content", height=150, key=f"chapter_{i}"
                )

                if chapter_title and chapter_content:
                    chapters.append(
                        {
                            "title": chapter_title,
                            "content": chapter_content,
                            "format": "markdown",
                        }
                    )

            submitted = st.form_submit_button("📖 Create Custom Ebook")

            if submitted:
                if not chapters:
                    st.error("Please add content for at least one chapter")
                else:
                    with st.spinner("Creating custom ebook..."):
                        try:
                            output_files = manager.create_ebook_from_template(
                                "custom",
                                content=chapters,
                                title=title,
                                author=author,
                                theme=theme,
                                formats=["html", "markdown"],
                            )

                            if output_files:
                                st.success("Custom ebook created successfully!")

                                for fmt, path in output_files.items():
                                    st.write(f"📄 {fmt.upper()}: `{path}`")
                            else:
                                st.error("Failed to create ebook")

                        except Exception as e:
                            st.error(f"Error creating ebook: {e}")


def show_statistics_page(manager):
    """Show ebook statistics page"""

    st.header("📊 Ebook Collection Statistics")

    stats = manager.get_ebook_stats()

    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Ebooks", stats["total_ebooks"])

    with col2:
        st.metric("Total Chapters", stats["total_chapters"])

    with col3:
        avg_chapters = stats["total_chapters"] / max(stats["total_ebooks"], 1)
        st.metric("Avg Chapters/Ebook", f"{avg_chapters:.1f}")

    with col4:
        total_formats = sum(stats["formats"].values())
        st.metric("Total Format Files", total_formats)

    # Format distribution
    st.subheader("📄 Format Distribution")
    format_data = stats["formats"]

    if any(format_data.values()):
        col1, col2 = st.columns(2)

        with col1:
            for fmt, count in format_data.items():
                if count > 0:
                    st.write(f"**{fmt.upper()}:** {count} files")

        with col2:
            # Simple bar chart using text
            max_count = max(format_data.values()) if format_data.values() else 1

            for fmt, count in format_data.items():
                if count > 0:
                    bar_length = int((count / max_count) * 20)
                    bar = "█" * bar_length
                    st.write(f"{fmt.upper()}: {bar} ({count})")

    # Theme distribution
    st.subheader("🎨 Theme Distribution")
    theme_data = stats["themes"]

    if theme_data:
        for theme, count in theme_data.items():
            st.write(f"**{theme.title()}:** {count} ebooks")
    else:
        st.write("No theme data available")


def show_management_page(manager):
    """Show ebook management page"""

    st.header("⚙️ Ebook Management")

    # Bulk operations
    st.subheader("📦 Bulk Operations")

    ebooks = manager.list_ebooks()

    if ebooks:
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📦 Archive All Ebooks"):
                archived_count = 0
                for ebook_id in ebooks:
                    if manager.archive_ebook(ebook_id):
                        archived_count += 1

                st.success(f"Archived {archived_count} ebooks")

        with col2:
            export_all_dir = st.text_input("Export all to directory:")
            if st.button("📤 Export All") and export_all_dir:
                exported_count = 0
                for ebook_id in ebooks:
                    if manager.export_ebook(ebook_id, f"{export_all_dir}/{ebook_id}"):
                        exported_count += 1

                st.success(f"Exported {exported_count} ebooks")

        with col3:
            st.write("⚠️ **Danger Zone**")
            if st.button("🗑️ Delete All Ebooks", type="secondary"):
                if st.session_state.get("confirm_delete_all", False):
                    deleted_count = 0
                    for ebook_id in ebooks:
                        if manager.delete_ebook(ebook_id):
                            deleted_count += 1

                    st.success(f"Deleted {deleted_count} ebooks")
                    st.experimental_rerun()
                else:
                    st.session_state["confirm_delete_all"] = True
                    st.warning("Click again to confirm deletion of ALL ebooks")

    # Directory information
    st.subheader("📁 Directory Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Ebook Directory:**")
        st.code(str(manager.ebook_dir.absolute()))

        ebook_files = list(manager.ebook_dir.glob("*"))
        st.write(f"Files: {len(ebook_files)}")

    with col2:
        st.write("**Archive Directory:**")
        st.code(str(manager.archive_dir.absolute()))

        archive_files = list(manager.archive_dir.glob("*"))
        st.write(f"Archives: {len(archive_files)}")


if __name__ == "__main__":
    run_ebook_management_dashboard()
