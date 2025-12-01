#!/usr/bin/env python3
"""
Codex Ebook Viewer

A simple web-based viewer for generated Codex ebooks with navigation and preview capabilities.
"""

import json
import os
from datetime import datetime
from pathlib import Path

import streamlit as st


def load_ebook_metadata():
    """Load metadata for all available ebooks"""

    ebook_dir = Path("ebooks")
    if not ebook_dir.exists():
        return {}

    ebooks = {}

    # Look for project files
    for project_file in ebook_dir.glob("*_project.json"):
        try:
            with open(project_file, "r", encoding="utf-8") as f:
                project_data = json.load(f)

            ebook_id = project_file.stem.replace("_project", "")
            ebooks[ebook_id] = project_data

        except Exception as e:
            st.error(f"Error loading {project_file}: {e}")

    return ebooks


def display_ebook_preview(ebook_data):
    """Display ebook preview and metadata"""

    metadata = ebook_data.get("metadata", {})
    chapters = ebook_data.get("chapters", [])
    output_files = ebook_data.get("output_files", {})

    st.subheader(f"📖 {metadata.get('title', 'Unknown Title')}")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.write(f"**Author:** {metadata.get('author', 'Unknown')}")
        st.write(f"**Theme:** {metadata.get('theme', 'default')}")
        st.write(
            f"**Created:** {datetime.fromisoformat(metadata.get('created', '2024-01-01')).strftime('%B %d, %Y')}"
        )
        st.write(f"**Chapters:** {len(chapters)}")

        if metadata.get("description"):
            st.write(f"**Description:** {metadata['description']}")

    with col2:
        st.write("**Available Formats:**")
        for format_name, file_path in output_files.items():
            if Path(file_path).exists():
                st.success(f"✅ {format_name.upper()}")
            else:
                st.error(f"❌ {format_name.upper()}")

    # Chapter list
    if chapters:
        st.write("**Chapters:**")
        for i, chapter in enumerate(chapters, 1):
            chapter_title = chapter.get("title", f"Chapter {i}")
            chapter_type = chapter.get("type", "content")
            st.write(f"{i}. {chapter_title} *({chapter_type})*")


def display_ebook_content(ebook_data, format_type="html"):
    """Display ebook content"""

    output_files = ebook_data.get("output_files", {})

    if format_type not in output_files:
        st.error(f"Format '{format_type}' not available for this ebook")
        return

    file_path = Path(output_files[format_type])

    if not file_path.exists():
        st.error(f"File not found: {file_path}")
        return

    try:
        if format_type == "html":
            # Display HTML content in an iframe or direct HTML
            with open(file_path, "r", encoding="utf-8") as f:
                html_content = f.read()

            st.components.v1.html(html_content, height=800, scrolling=True)

        elif format_type == "markdown":
            # Display markdown content
            with open(file_path, "r", encoding="utf-8") as f:
                md_content = f.read()

            st.markdown(md_content)

        elif format_type == "json":
            # Display JSON content formatted
            with open(file_path, "r", encoding="utf-8") as f:
                json_content = json.load(f)

            st.json(json_content)

    except Exception as e:
        st.error(f"Error loading content: {e}")


def main():
    """Main ebook viewer application"""

    st.set_page_config(page_title="Codex Ebook Viewer", page_icon="📚", layout="wide")

    st.title("📚 Codex Ebook Viewer")
    st.markdown("*Browse and preview generated Codex Dominion ebooks*")

    # Load available ebooks
    ebooks = load_ebook_metadata()

    if not ebooks:
        st.warning(
            "No ebooks found. Generate some ebooks first using the Codex Ebook Generator!"
        )
        st.code("python advanced_ebook_generator.py")
        return

    # Sidebar for ebook selection
    st.sidebar.title("📖 Available Ebooks")

    selected_ebook = st.sidebar.selectbox(
        "Choose an ebook:",
        options=list(ebooks.keys()),
        format_func=lambda x: ebooks[x]["metadata"]["title"],
    )

    if selected_ebook:
        ebook_data = ebooks[selected_ebook]

        # Display mode selection
        display_mode = st.sidebar.radio(
            "Display Mode:", ["Preview", "Read HTML", "Read Markdown", "View JSON"]
        )

        # Main content area
        if display_mode == "Preview":
            display_ebook_preview(ebook_data)

            # Show sample chapter content
            chapters = ebook_data.get("chapters", [])
            if chapters:
                st.subheader("📄 Sample Chapter Content")

                sample_chapter = chapters[0]
                st.write(f"**{sample_chapter.get('title', 'Sample Chapter')}**")

                content = sample_chapter.get("content", "")
                # Show first 500 characters
                preview_text = content[:500]
                if len(content) > 500:
                    preview_text += "..."

                st.markdown(preview_text)

        elif display_mode == "Read HTML":
            display_ebook_content(ebook_data, "html")

        elif display_mode == "Read Markdown":
            display_ebook_content(ebook_data, "markdown")

        elif display_mode == "View JSON":
            display_ebook_content(ebook_data, "json")

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🏛️ Codex Dominion**")
    st.sidebar.markdown("*Sacred Knowledge Archive*")


if __name__ == "__main__":
    main()
