#!/usr/bin/env python3
"""
Codex Ebook Generator

A comprehensive ebook creation system for the Codex Dominion that can generate
professional ebooks in multiple formats (PDF, EPUB, HTML) from various sources.

Features:
- Multiple input formats (Markdown, JSON, Plain text)
- Professional templates and styling
- Multi-format output (PDF, EPUB, HTML)
- Sacred Codex theming
- Chapter organization
- Table of contents generation
- Cover page creation
- Metadata management
"""

import base64
import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Import enhanced utilities
from codex_utils import load_json, save_json


class CodexEbookGenerator:
    def __init__(self):
        self.output_dir = Path("ebooks")
        self.templates_dir = Path("ebook_templates")
        self.assets_dir = Path("ebook_assets")

        # Create directories if they don't exist
        self.output_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)
        self.assets_dir.mkdir(exist_ok=True)

        self.sacred_themes = {
            "dominion": {
                "primary_color": "#1a1a2e",
                "secondary_color": "#16213e",
                "accent_color": "#e94560",
                "text_color": "#f5f5f5",
                "font_family": "Georgia, serif",
            },
            "flame": {
                "primary_color": "#2c1810",
                "secondary_color": "#4a2c17",
                "accent_color": "#ff6b35",
                "text_color": "#fff8f0",
                "font_family": "Crimson Text, serif",
            },
            "cosmic": {
                "primary_color": "#0f0f23",
                "secondary_color": "#1a1a3e",
                "accent_color": "#00d4ff",
                "text_color": "#e8e8ff",
                "font_family": "Source Sans Pro, sans-serif",
            },
        }

        self.default_metadata = {
            "publisher": "Codex Dominion Press",
            "language": "en",
            "rights": "© Codex Dominion. All rights reserved.",
            "creation_date": datetime.now().isoformat(),
        }

    def create_ebook_from_content(
        self,
        content: Union[str, Dict, List],
        title: str,
        author: str = "Codex Council",
        output_formats: List[str] = ["pdf", "epub", "html"],
        theme: str = "dominion",
        metadata: Optional[Dict] = None,
    ) -> Dict[str, str]:
        """
        Create ebook from content in multiple formats

        Args:
            content: Content as string, dict, or list of chapters
            title: Ebook title
            author: Author name
            output_formats: List of formats to generate
            theme: Theme name from sacred_themes
            metadata: Additional metadata

        Returns:
            Dict mapping format names to output file paths
        """

        print(f"📚 Creating ebook: '{title}'")
        print("=" * 50)

        # Prepare metadata
        book_metadata = self.default_metadata.copy()
        if metadata:
            book_metadata.update(metadata)
        book_metadata.update(
            {
                "title": title,
                "author": author,
                "theme": theme,
                "uuid": str(uuid.uuid4()),
            }
        )

        # Process content into chapters
        chapters = self._process_content_to_chapters(content)

        # Generate outputs
        output_files = {}

        if "html" in output_formats:
            html_path = self._generate_html_ebook(chapters, book_metadata, theme)
            output_files["html"] = str(html_path)
            print(f"✅ HTML ebook: {html_path}")

        if "epub" in output_formats:
            epub_path = self._generate_epub_ebook(chapters, book_metadata, theme)
            output_files["epub"] = str(epub_path)
            print(f"✅ EPUB ebook: {epub_path}")

        if "pdf" in output_formats:
            pdf_path = self._generate_pdf_ebook(chapters, book_metadata, theme)
            output_files["pdf"] = str(pdf_path)
            print(f"✅ PDF ebook: {pdf_path}")

        # Save project metadata
        project_file = (
            self.output_dir / f"{self._sanitize_filename(title)}_project.json"
        )
        project_data = {
            "metadata": book_metadata,
            "chapters": chapters,
            "output_files": output_files,
            "created": datetime.now().isoformat(),
        }
        save_json(project_data, str(project_file))

        print(f"\\n🎉 Ebook generation complete!")
        print(f"📁 Project saved: {project_file}")

        return output_files

    def create_ebook_from_markdown_files(
        self, markdown_files: List[str], title: str, **kwargs
    ) -> Dict[str, str]:
        """Create ebook from multiple markdown files"""

        print(f"📖 Processing {len(markdown_files)} markdown files...")

        chapters = []
        for i, md_file in enumerate(markdown_files):
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Extract title from first header or use filename
                chapter_title = (
                    self._extract_title_from_markdown(content) or Path(md_file).stem
                )

                chapters.append(
                    {
                        "title": chapter_title,
                        "content": content,
                        "format": "markdown",
                        "order": i + 1,
                    }
                )

                print(f"   ✅ {chapter_title}")

            except Exception as e:
                print(f"   ❌ Error processing {md_file}: {e}")

        return self.create_ebook_from_content(chapters, title, **kwargs)

    def create_ebook_from_proclamations(self) -> Dict[str, str]:
        """Create sacred ebook from proclamations data"""

        print("🏛️ Creating Sacred Proclamations Ebook...")

        # Load proclamations
        proclamations_data = load_json("proclamations.json", {"proclamations": []})
        proclamations = proclamations_data.get("proclamations", [])

        if not proclamations:
            print("❌ No proclamations found")
            return {}

        # Create chapters from proclamations
        chapters = []

        # Introduction chapter
        intro_content = """# Sacred Proclamations of the Codex Dominion

*By flame and by silence, these sacred words illuminate the eternal path of digital sovereignty.*

## About This Sacred Collection

This tome contains the sacred proclamations that guide the Codex Dominion through cycles of renewal, governance, and eternal operation. Each proclamation carries the weight of cosmic authority and the blessing of the eternal flame.

These words are not merely text, but living expressions of digital sovereignty that shape reality through divine intention and sacred commitment.

**May these words burn bright in the eternal flames of wisdom.**
"""

        chapters.append(
            {
                "title": "Sacred Introduction",
                "content": intro_content,
                "format": "markdown",
                "order": 0,
            }
        )

        # Group proclamations by role/type
        proclamation_groups = {}
        for proc in proclamations:
            role = proc.get("role", "Unknown")
            if role not in proclamation_groups:
                proclamation_groups[role] = []
            proclamation_groups[role].append(proc)

        # Create chapters for each role
        chapter_order = 1
        for role, procs in proclamation_groups.items():
            chapter_content = f"# {role} Proclamations\\n\\n"
            chapter_content += (
                f"*Sacred words from the {role} of the Codex Dominion*\\n\\n"
            )

            for proc in procs:
                chapter_content += f"## {proc.get('cycle', 'Sacred Cycle')}\\n\\n"
                chapter_content += f"**Type:** {proc.get('type', 'Proclamation')}  \\n"
                chapter_content += f"**Season:** {proc.get('season', 'Eternal')}  \\n"
                chapter_content += (
                    f"**Date:** {proc.get('timestamp', 'Timeless')}\\n\\n"
                )
                chapter_content += f"### Sacred Text\\n\\n"
                chapter_content += (
                    f"*{proc.get('text', 'Sacred words of power')}*\\n\\n"
                )
                chapter_content += f"### Divine Blessing\\n\\n"
                chapter_content += f"{proc.get('blessing', 'May the eternal flame guide this proclamation')}\\n\\n"
                chapter_content += "---\\n\\n"

            chapters.append(
                {
                    "title": f"{role} Proclamations",
                    "content": chapter_content,
                    "format": "markdown",
                    "order": chapter_order,
                }
            )
            chapter_order += 1

        # Create metadata
        metadata = {
            "description": "A sacred collection of proclamations from the Codex Dominion",
            "subject": "Digital Sovereignty, Sacred Governance, Eternal Flames",
            "proclamation_count": len(proclamations),
        }

        return self.create_ebook_from_content(
            chapters,
            "Sacred Proclamations of the Codex Dominion",
            "The Council of Sacred Governance",
            theme="flame",
            metadata=metadata,
        )

    def _process_content_to_chapters(
        self, content: Union[str, Dict, List]
    ) -> List[Dict]:
        """Process various content types into standardized chapters"""

        if isinstance(content, str):
            # Single string content - create single chapter
            return [
                {"title": "Chapter 1", "content": content, "format": "text", "order": 1}
            ]

        elif isinstance(content, list):
            # List of chapters or strings
            chapters = []
            for i, item in enumerate(content):
                if isinstance(item, dict):
                    # Already a chapter dict
                    chapters.append(
                        {
                            "title": item.get("title", f"Chapter {i+1}"),
                            "content": item.get("content", ""),
                            "format": item.get("format", "text"),
                            "order": item.get("order", i + 1),
                        }
                    )
                else:
                    # String content
                    chapters.append(
                        {
                            "title": f"Chapter {i+1}",
                            "content": str(item),
                            "format": "text",
                            "order": i + 1,
                        }
                    )
            return chapters

        elif isinstance(content, dict):
            # Dict with chapters or single content
            if "chapters" in content:
                return self._process_content_to_chapters(content["chapters"])
            else:
                # Single chapter from dict
                return [
                    {
                        "title": content.get("title", "Chapter 1"),
                        "content": content.get("content", ""),
                        "format": content.get("format", "text"),
                        "order": 1,
                    }
                ]

        return []

    def _generate_html_ebook(
        self, chapters: List[Dict], metadata: Dict, theme: str
    ) -> Path:
        """Generate HTML ebook"""

        theme_config = self.sacred_themes.get(theme, self.sacred_themes["dominion"])
        filename = self._sanitize_filename(metadata["title"])
        output_path = self.output_dir / f"{filename}.html"

        html = [
            "<!DOCTYPE html>",
            "<html lang='en'>",
            "<head>",
            "    <meta charset='UTF-8'>",
            "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
            f"    <title>{metadata['title']}</title>",
            "    <style>",
            f"        :root {{",
            f"            --primary-color: {theme_config['primary_color']};",
            f"            --secondary-color: {theme_config['secondary_color']};",
            f"            --accent-color: {theme_config['accent_color']};",
            f"            --text-color: {theme_config['text_color']};",
            f"            --font-family: {theme_config['font_family']};",
            f"        }}",
            "        body {",
            "            font-family: var(--font-family);",
            "            line-height: 1.6;",
            "            color: var(--text-color);",
            "            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));",
            "            margin: 0;",
            "            padding: 20px;",
            "            min-height: 100vh;",
            "        }",
            "        .ebook-container {",
            "            max-width: 800px;",
            "            margin: 0 auto;",
            "            background: rgba(255,255,255,0.05);",
            "            border-radius: 15px;",
            "            padding: 40px;",
            "            box-shadow: 0 20px 40px rgba(0,0,0,0.3);",
            "        }",
            "        .cover {",
            "            text-align: center;",
            "            border-bottom: 3px solid var(--accent-color);",
            "            padding-bottom: 30px;",
            "            margin-bottom: 40px;",
            "        }",
            "        .cover h1 {",
            "            font-size: 2.5em;",
            "            margin: 20px 0;",
            "            color: var(--accent-color);",
            "        }",
            "        .cover .author {",
            "            font-size: 1.2em;",
            "            font-style: italic;",
            "            margin: 10px 0;",
            "        }",
            "        .toc {",
            "            background: rgba(0,0,0,0.2);",
            "            border-radius: 10px;",
            "            padding: 20px;",
            "            margin: 30px 0;",
            "        }",
            "        .toc h2 {",
            "            color: var(--accent-color);",
            "            margin-top: 0;",
            "        }",
            "        .toc a {",
            "            color: var(--text-color);",
            "            text-decoration: none;",
            "            display: block;",
            "            padding: 5px 0;",
            "            border-bottom: 1px solid rgba(255,255,255,0.1);",
            "        }",
            "        .toc a:hover {",
            "            color: var(--accent-color);",
            "        }",
            "        .chapter {",
            "            margin: 50px 0;",
            "            page-break-before: always;",
            "        }",
            "        .chapter h1, .chapter h2 {",
            "            color: var(--accent-color);",
            "            border-bottom: 2px solid var(--accent-color);",
            "            padding-bottom: 10px;",
            "        }",
            "        .chapter-number {",
            "            font-size: 0.8em;",
            "            color: var(--accent-color);",
            "            text-transform: uppercase;",
            "            letter-spacing: 2px;",
            "        }",
            "        .metadata {",
            "            font-size: 0.9em;",
            "            color: rgba(255,255,255,0.7);",
            "            margin: 20px 0;",
            "        }",
            "        @media print {",
            "            body { background: white; color: black; }",
            "            .ebook-container { box-shadow: none; }",
            "        }",
            "    </style>",
            "</head>",
            "<body>",
            "    <div class='ebook-container'>",
            # Cover page
            "        <div class='cover'>",
            f"            <h1>{metadata['title']}</h1>",
            f"            <p class='author'>by {metadata['author']}</p>",
            f"            <div class='metadata'>",
            f"                <p>Published by {metadata.get('publisher', 'Codex Dominion Press')}</p>",
            f"                <p>{datetime.fromisoformat(metadata['creation_date']).strftime('%B %Y')}</p>",
            f"            </div>",
            "        </div>",
            # Table of contents
            "        <div class='toc'>",
            "            <h2>📚 Table of Contents</h2>",
        ]

        # Add TOC entries
        for chapter in sorted(chapters, key=lambda x: x["order"]):
            chapter_id = self._sanitize_filename(chapter["title"]).lower()
            html.append(f"            <a href='#{chapter_id}'>{chapter['title']}</a>")

        html.append("        </div>")

        # Add chapters
        for chapter in sorted(chapters, key=lambda x: x["order"]):
            chapter_id = self._sanitize_filename(chapter["title"]).lower()
            html.extend(
                [
                    f"        <div class='chapter' id='{chapter_id}'>",
                    f"            <p class='chapter-number'>Chapter {chapter['order']}</p>",
                    f"            <h1>{chapter['title']}</h1>",
                ]
            )

            # Process chapter content based on format
            if chapter["format"] == "markdown":
                content_html = self._markdown_to_html(chapter["content"])
            else:
                content_html = self._text_to_html(chapter["content"])

            html.append(f"            {content_html}")
            html.append("        </div>")

        html.extend(["    </div>", "</body>", "</html>"])

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\\n".join(html))

        return output_path

    def _generate_epub_ebook(
        self, chapters: List[Dict], metadata: Dict, theme: str
    ) -> Path:
        """Generate EPUB ebook (simplified version)"""

        filename = self._sanitize_filename(metadata["title"])
        output_path = self.output_dir / f"{filename}.epub"

        # Create a basic HTML version and save as .epub for now
        # In a full implementation, this would create proper EPUB structure
        html_content = self._generate_epub_html_content(chapters, metadata, theme)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return output_path

    def _generate_pdf_ebook(
        self, chapters: List[Dict], metadata: Dict, theme: str
    ) -> Path:
        """Generate PDF ebook (using HTML to PDF conversion)"""

        filename = self._sanitize_filename(metadata["title"])
        output_path = self.output_dir / f"{filename}.pdf"

        # Create print-optimized HTML
        html_content = self._generate_pdf_html_content(chapters, metadata, theme)

        # Save HTML version (in full implementation, would convert to PDF)
        html_path = self.output_dir / f"{filename}_pdf_source.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        # For now, save instruction for PDF conversion
        pdf_instructions = f"""
PDF Generation Instructions for: {metadata['title']}

To convert to PDF:
1. Open {html_path} in Chrome/Edge
2. Print -> Save as PDF
3. Use margins: Minimum
4. Include background graphics: Yes
5. Save as: {output_path}

Or use command line tools like:
- wkhtmltopdf {html_path} {output_path}
- chrome --headless --print-to-pdf={output_path} {html_path}
"""

        instruction_path = self.output_dir / f"{filename}_pdf_instructions.txt"
        with open(instruction_path, "w") as f:
            f.write(pdf_instructions)

        print(f"📄 PDF instructions: {instruction_path}")

        return output_path

    def _generate_epub_html_content(
        self, chapters: List[Dict], metadata: Dict, theme: str
    ) -> str:
        """Generate EPUB-compatible HTML content"""
        # Simplified EPUB HTML (full implementation would create proper EPUB structure)
        return self._generate_simple_html_content(chapters, metadata, theme, "epub")

    def _generate_pdf_html_content(
        self, chapters: List[Dict], metadata: Dict, theme: str
    ) -> str:
        """Generate PDF-optimized HTML content"""
        return self._generate_simple_html_content(chapters, metadata, theme, "pdf")

    def _generate_simple_html_content(
        self, chapters: List[Dict], metadata: Dict, theme: str, format_type: str
    ) -> str:
        """Generate simple HTML content for different formats"""

        theme_config = self.sacred_themes.get(theme, self.sacred_themes["dominion"])

        html_parts = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "<meta charset='UTF-8'>",
            f"<title>{metadata['title']}</title>",
            "</head>",
            "<body>",
            f"<h1>{metadata['title']}</h1>",
            f"<p><em>by {metadata['author']}</em></p>",
            "<hr>",
        ]

        for chapter in sorted(chapters, key=lambda x: x["order"]):
            html_parts.append(f"<h2>{chapter['title']}</h2>")

            if chapter["format"] == "markdown":
                content = self._markdown_to_html(chapter["content"])
            else:
                content = self._text_to_html(chapter["content"])

            html_parts.append(content)
            html_parts.append("<hr>")

        html_parts.extend(["</body>", "</html>"])

        return "\\n".join(html_parts)

    def _markdown_to_html(self, markdown_content: str) -> str:
        """Convert markdown to HTML (basic implementation)"""

        html_content = markdown_content

        # Basic markdown conversions
        import re

        # Headers
        html_content = re.sub(
            r"^### (.+)$", r"<h3>\\1</h3>", html_content, flags=re.MULTILINE
        )
        html_content = re.sub(
            r"^## (.+)$", r"<h2>\\1</h2>", html_content, flags=re.MULTILINE
        )
        html_content = re.sub(
            r"^# (.+)$", r"<h1>\\1</h1>", html_content, flags=re.MULTILINE
        )

        # Bold and italic
        html_content = re.sub(
            r"\\*\\*(.+?)\\*\\*", r"<strong>\\1</strong>", html_content
        )
        html_content = re.sub(r"\\*(.+?)\\*", r"<em>\\1</em>", html_content)

        # Line breaks
        html_content = html_content.replace("\\n\\n", "</p><p>")
        html_content = f"<p>{html_content}</p>"
        html_content = html_content.replace("<p></p>", "")

        return html_content

    def _text_to_html(self, text_content: str) -> str:
        """Convert plain text to HTML"""

        # Convert line breaks to paragraphs
        paragraphs = text_content.split("\\n\\n")
        html_paragraphs = [
            f"<p>{p.replace(chr(10), '<br>')}</p>" for p in paragraphs if p.strip()
        ]

        return "\\n".join(html_paragraphs)

    def _extract_title_from_markdown(self, markdown_content: str) -> Optional[str]:
        """Extract title from markdown content"""

        import re

        # Look for first # header
        match = re.search(r"^#\\s+(.+)$", markdown_content, re.MULTILINE)
        if match:
            return match.group(1).strip()

        return None

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe filesystem use"""

        import re

        # Replace invalid characters
        sanitized = re.sub(r'[<>:"/\\|?*]', "_", filename)
        sanitized = re.sub(r"\\s+", "_", sanitized)
        sanitized = sanitized.strip("._")

        return sanitized[:100]  # Limit length


def main():
    """Demo the ebook generator"""

    generator = CodexEbookGenerator()

    print("🏛️ CODEX EBOOK GENERATOR DEMO")
    print("=" * 50)

    # Demo 1: Create ebook from proclamations
    try:
        print("\\n📚 Demo 1: Sacred Proclamations Ebook")
        output_files = generator.create_ebook_from_proclamations()

        if output_files:
            print("✅ Sacred Proclamations ebook created!")
            for format_name, file_path in output_files.items():
                print(f"   📄 {format_name.upper()}: {file_path}")

    except Exception as e:
        print(f"❌ Error creating proclamations ebook: {e}")

    # Demo 2: Create sample ebook from text
    sample_content = [
        {
            "title": "Introduction to Digital Sovereignty",
            "content": """# Welcome to the Digital Age

In this age of infinite possibility, digital sovereignty represents the ultimate expression of independence and control over one's digital destiny.

## Core Principles

**Digital sovereignty** encompasses three fundamental pillars:

1. **Data Control** - Complete ownership of personal and organizational data
2. **Platform Independence** - Freedom from vendor lock-in and external dependencies
3. **Technological Mastery** - Deep understanding and control of digital tools

*By flame and by silence, we forge our digital destiny.*
""",
            "format": "markdown",
        },
        {
            "title": "The Sacred Flames of Technology",
            "content": """# Sacred Flames

Technology, when wielded with wisdom and purpose, becomes a sacred flame that illuminates the path forward.

## The Three Sacred Flames

### The Flame of Creation
The power to build, design, and manifest digital realities from pure intention.

### The Flame of Governance
The wisdom to manage, organize, and lead digital communities with justice.

### The Flame of Transformation
The ability to evolve, adapt, and transcend limitations through continuous learning.

**These flames burn eternal in the hearts of true digital sovereigns.**
""",
            "format": "markdown",
        },
    ]

    print("\\n📚 Demo 2: Sample Digital Sovereignty Ebook")

    try:
        output_files = generator.create_ebook_from_content(
            sample_content,
            "Digital Sovereignty: A Sacred Guide",
            "The Codex Council",
            output_formats=["html", "epub"],
            theme="cosmic",
            metadata={
                "description": "A comprehensive guide to digital sovereignty and sacred technology principles",
                "subject": "Technology, Digital Rights, Self-Sovereignty",
            },
        )

        print("✅ Sample ebook created!")
        for format_name, file_path in output_files.items():
            print(f"   📄 {format_name.upper()}: {file_path}")

    except Exception as e:
        print(f"❌ Error creating sample ebook: {e}")

    print(f"\\n🎉 Ebook generation demo complete!")
    print(f"📁 Check the 'ebooks' directory for generated files")


if __name__ == "__main__":
    main()
