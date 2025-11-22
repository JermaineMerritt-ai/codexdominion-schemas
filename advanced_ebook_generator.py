#!/usr/bin/env python3
"""
Advanced Codex Ebook Generator

An advanced ebook creation system for the Codex Dominion that leverages existing
content generation capabilities and creates professional ebooks in multiple formats.

Features:
- Integration with existing Codex systems
- Advanced template engine with Sacred themes
- Multiple export formats (HTML, Markdown, JSON)
- Content aggregation from various sources
- Professional styling and layout
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

def load_json_safe(filepath: str, default: Any = None) -> Any:
    """Safely load JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load {filepath}: {e}")
        return default if default is not None else {}

def save_json_safe(data: Any, filepath: str) -> bool:
    """Safely save JSON file"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False

class AdvancedCodexEbookGenerator:
    """Advanced ebook generation system for the Codex Dominion"""
    
    def __init__(self):
        self.base_dir = Path(".")
        self.output_dir = Path("ebooks")
        self.output_dir.mkdir(exist_ok=True)
        
        # Sacred themes for different ebook types
        self.themes = {
            "dominion": {
                "name": "Sacred Dominion",
                "primary": "#1a1a2e",
                "secondary": "#16213e",
                "accent": "#e94560",
                "text": "#f5f5f5",
                "font": "Georgia, 'Times New Roman', serif",
                "description": "Official Codex Dominion theme with sacred colors"
            },
            "flame": {
                "name": "Eternal Flame", 
                "primary": "#2c1810",
                "secondary": "#4a2c17",
                "accent": "#ff6b35",
                "text": "#fff8f0",
                "font": "'Crimson Text', Georgia, serif",
                "description": "Warm flame theme for sacred texts"
            },
            "cosmic": {
                "name": "Cosmic Void",
                "primary": "#0f0f23",
                "secondary": "#1a1a3e", 
                "accent": "#00d4ff",
                "text": "#e8e8ff",
                "font": "'Source Sans Pro', Arial, sans-serif",
                "description": "Cool cosmic theme for technical content"
            },
            "council": {
                "name": "Council Chamber",
                "primary": "#1e1e2f",
                "secondary": "#2a2a3f",
                "accent": "#c9a961",
                "text": "#f0f0f5",
                "font": "'Palatino Linotype', 'Book Antiqua', Palatino, serif",
                "description": "Formal theme for governance documents"
            }
        }
        
        self.content_sources = {
            "proclamations": "proclamations.json",
            "documentation": ["*.md", "*.MD"],
            "code_comments": ["*.py", "*.js", "*.ts"],
            "json_data": ["*.json"]
        }
    
    def create_comprehensive_ebook(self, 
                                 title: str,
                                 author: str = "Codex Council",
                                 theme: str = "dominion",
                                 include_sources: List[str] = None,
                                 output_formats: List[str] = None) -> Dict[str, str]:
        """
        Create comprehensive ebook from multiple sources
        
        Args:
            title: Ebook title
            author: Author name
            theme: Theme name
            include_sources: List of content sources to include
            output_formats: List of formats to generate
            
        Returns:
            Dict mapping format to output path
        """
        
        if include_sources is None:
            include_sources = ["proclamations", "documentation"]
        
        if output_formats is None:
            output_formats = ["html", "markdown"]
        
        print(f"Creating comprehensive ebook: '{title}'")
        print("=" * 60)
        
        # Gather content from sources
        all_content = self._gather_content_from_sources(include_sources)
        
        if not all_content:
            print("No content found to generate ebook")
            return {}
        
        # Organize into chapters
        chapters = self._organize_content_into_chapters(all_content)
        
        # Create metadata
        metadata = {
            "title": title,
            "author": author,
            "theme": theme,
            "created": datetime.now().isoformat(),
            "sources": include_sources,
            "chapters": len(chapters),
            "generator": "Advanced Codex Ebook Generator v2.0"
        }
        
        # Generate outputs
        output_files = {}
        
        if "html" in output_formats:
            html_path = self._generate_advanced_html(chapters, metadata)
            output_files["html"] = str(html_path)
            print(f"Generated HTML: {html_path}")
        
        if "markdown" in output_formats:
            md_path = self._generate_markdown_book(chapters, metadata)
            output_files["markdown"] = str(md_path)
            print(f"Generated Markdown: {md_path}")
        
        if "json" in output_formats:
            json_path = self._generate_json_book(chapters, metadata)
            output_files["json"] = str(json_path)
            print(f"Generated JSON: {json_path}")
        
        # Save project file
        project_path = self._save_project_file(metadata, chapters, output_files)
        print(f"Project saved: {project_path}")
        
        print(f"\nEbook generation complete! Generated {len(output_files)} formats.")
        return output_files
    
    def create_proclamations_ebook(self) -> Dict[str, str]:
        """Create ebook specifically from proclamations"""
        
        print("Creating Sacred Proclamations Ebook")
        print("=" * 50)
        
        # Load proclamations
        proclamations_data = load_json_safe("proclamations.json", {"proclamations": []})
        proclamations = proclamations_data.get("proclamations", [])
        
        if not proclamations:
            print("No proclamations found")
            return {}
        
        print(f"Found {len(proclamations)} proclamations")
        
        # Process proclamations into chapters
        chapters = self._process_proclamations_to_chapters(proclamations)
        
        metadata = {
            "title": "Sacred Proclamations of the Codex Dominion",
            "author": "The Council of Sacred Governance",
            "theme": "flame",
            "created": datetime.now().isoformat(),
            "proclamation_count": len(proclamations),
            "description": "A sacred collection of divine proclamations that guide the eternal operations of the Codex Dominion"
        }
        
        # Generate formats
        output_files = {}
        
        html_path = self._generate_advanced_html(chapters, metadata)
        output_files["html"] = str(html_path)
        
        md_path = self._generate_markdown_book(chapters, metadata)
        output_files["markdown"] = str(md_path)
        
        project_path = self._save_project_file(metadata, chapters, output_files)
        
        print(f"Sacred Proclamations ebook created!")
        print(f"HTML: {html_path}")
        print(f"Markdown: {md_path}")
        
        return output_files
    
    def _gather_content_from_sources(self, sources: List[str]) -> Dict[str, Any]:
        """Gather content from various sources"""
        
        content = {}
        
        for source in sources:
            print(f"Gathering content from: {source}")
            
            if source == "proclamations":
                proclamations_data = load_json_safe("proclamations.json")
                if proclamations_data and "proclamations" in proclamations_data:
                    content["proclamations"] = proclamations_data["proclamations"]
                    print(f"  Found {len(content['proclamations'])} proclamations")
            
            elif source == "documentation":
                docs = []
                for pattern in ["*.md", "*.MD"]:
                    for file_path in self.base_dir.glob(pattern):
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                docs.append({
                                    "filename": file_path.name,
                                    "path": str(file_path),
                                    "content": f.read(),
                                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                                })
                        except Exception as e:
                            print(f"  Error reading {file_path}: {e}")
                
                if docs:
                    content["documentation"] = docs
                    print(f"  Found {len(docs)} documentation files")
        
        return content
    
    def _organize_content_into_chapters(self, content: Dict[str, Any]) -> List[Dict]:
        """Organize gathered content into book chapters"""
        
        chapters = []
        chapter_order = 1
        
        # Introduction chapter
        intro = {
            "title": "Introduction",
            "content": self._generate_introduction(content),
            "type": "introduction",
            "order": chapter_order
        }
        chapters.append(intro)
        chapter_order += 1
        
        # Proclamations chapters
        if "proclamations" in content:
            proc_chapters = self._process_proclamations_to_chapters(content["proclamations"])
            for chapter in proc_chapters:
                chapter["order"] = chapter_order
                chapters.append(chapter)
                chapter_order += 1
        
        # Documentation chapters
        if "documentation" in content:
            doc_chapters = self._process_documentation_to_chapters(content["documentation"])
            for chapter in doc_chapters:
                chapter["order"] = chapter_order
                chapters.append(chapter)
                chapter_order += 1
        
        return chapters
    
    def _process_proclamations_to_chapters(self, proclamations: List[Dict]) -> List[Dict]:
        """Process proclamations into chapters"""
        
        chapters = []
        
        # Group proclamations by role
        by_role = {}
        for proc in proclamations:
            role = proc.get("role", "Unknown")
            if role not in by_role:
                by_role[role] = []
            by_role[role].append(proc)
        
        # Create chapter for each role
        for role, procs in by_role.items():
            chapter_content = f"# {role} Proclamations\n\n"
            chapter_content += f"*Sacred words from the {role} of the Codex Dominion*\n\n"
            
            for proc in procs:
                chapter_content += f"## {proc.get('cycle', 'Sacred Cycle')}\n\n"
                chapter_content += f"**Type:** {proc.get('type', 'Proclamation')}  \n"
                chapter_content += f"**Season:** {proc.get('season', 'Eternal')}  \n"
                chapter_content += f"**Date:** {proc.get('timestamp', 'Timeless')}\n\n"
                chapter_content += f"### Sacred Text\n\n"
                chapter_content += f"*{proc.get('text', 'Sacred words of power')}*\n\n"
                chapter_content += f"### Divine Blessing\n\n"
                chapter_content += f"{proc.get('blessing', 'May the eternal flame guide this proclamation')}\n\n"
                chapter_content += "---\n\n"
            
            chapters.append({
                "title": f"{role} Proclamations",
                "content": chapter_content,
                "type": "proclamations",
                "role": role,
                "count": len(procs)
            })
        
        return chapters
    
    def _process_documentation_to_chapters(self, docs: List[Dict]) -> List[Dict]:
        """Process documentation files into chapters"""
        
        chapters = []
        
        for doc in docs:
            title = self._extract_title_from_markdown(doc["content"]) or doc["filename"]
            
            chapters.append({
                "title": title,
                "content": doc["content"],
                "type": "documentation",
                "filename": doc["filename"],
                "source_path": doc["path"]
            })
        
        return chapters
    
    def _generate_introduction(self, content: Dict[str, Any]) -> str:
        """Generate introduction chapter"""
        
        intro = "# Introduction to the Codex Dominion\n\n"
        intro += "*By flame and by silence, these sacred words illuminate the eternal path of digital sovereignty.*\n\n"
        intro += "## About This Collection\n\n"
        intro += "This tome contains the sacred knowledge, proclamations, and documentation that guide the Codex Dominion through cycles of renewal, governance, and eternal operation.\n\n"
        
        if "proclamations" in content:
            count = len(content["proclamations"])
            intro += f"This collection includes {count} sacred proclamations that carry the weight of cosmic authority and the blessing of the eternal flame.\n\n"
        
        if "documentation" in content:
            count = len(content["documentation"])
            intro += f"Additionally, this tome contains {count} documentation files that preserve the technical knowledge and wisdom of our digital realm.\n\n"
        
        intro += "These words are not merely text, but living expressions of digital sovereignty that shape reality through divine intention and sacred commitment.\n\n"
        intro += "**May these words burn bright in the eternal flames of wisdom.**\n\n"
        
        return intro
    
    def _generate_advanced_html(self, chapters: List[Dict], metadata: Dict) -> Path:
        """Generate advanced HTML ebook with professional styling"""
        
        theme = self.themes.get(metadata.get("theme", "dominion"), self.themes["dominion"])
        filename = self._sanitize_filename(metadata["title"])
        output_path = self.output_dir / f"{filename}.html"
        
        # Generate advanced HTML with professional styling
        html_content = self._build_advanced_html_content(chapters, metadata, theme)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def _build_advanced_html_content(self, chapters: List[Dict], metadata: Dict, theme: Dict) -> str:
        """Build advanced HTML content with professional styling"""
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{metadata['title']}</title>
    <style>
        :root {{
            --primary-color: {theme['primary']};
            --secondary-color: {theme['secondary']};
            --accent-color: {theme['accent']};
            --text-color: {theme['text']};
            --font-family: {theme['font']};
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: var(--font-family);
            line-height: 1.8;
            color: var(--text-color);
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            min-height: 100vh;
        }}
        
        .ebook-container {{
            max-width: 1000px;
            margin: 0 auto;
            background: rgba(255,255,255,0.03);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.4);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(45deg, var(--accent-color), var(--primary-color));
            padding: 60px 40px;
            text-align: center;
            position: relative;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            opacity: 0.3;
        }}
        
        .header h1 {{
            font-size: 3em;
            margin: 20px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            position: relative;
            z-index: 1;
        }}
        
        .header .author {{
            font-size: 1.4em;
            font-style: italic;
            margin: 15px 0;
            position: relative;
            z-index: 1;
        }}
        
        .header .meta {{
            font-size: 1em;
            opacity: 0.9;
            margin-top: 20px;
            position: relative;
            z-index: 1;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .toc {{
            background: rgba(0,0,0,0.2);
            border-radius: 15px;
            padding: 30px;
            margin: 30px 0 50px 0;
            border-left: 5px solid var(--accent-color);
        }}
        
        .toc h2 {{
            color: var(--accent-color);
            margin-bottom: 20px;
            font-size: 1.8em;
        }}
        
        .toc-entry {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
        }}
        
        .toc-entry:hover {{
            background: rgba(255,255,255,0.05);
            padding-left: 10px;
            border-left: 3px solid var(--accent-color);
        }}
        
        .toc-entry a {{
            color: var(--text-color);
            text-decoration: none;
            font-weight: 500;
        }}
        
        .chapter-num {{
            color: var(--accent-color);
            font-size: 0.9em;
            opacity: 0.8;
        }}
        
        .chapter {{
            margin: 60px 0;
            page-break-before: always;
        }}
        
        .chapter-header {{
            border-bottom: 3px solid var(--accent-color);
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        
        .chapter-number {{
            color: var(--accent-color);
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-bottom: 10px;
        }}
        
        .chapter-title {{
            font-size: 2.5em;
            color: var(--accent-color);
            margin: 0;
            line-height: 1.2;
        }}
        
        .chapter-content {{
            font-size: 1.1em;
        }}
        
        .chapter-content h1 {{
            color: var(--accent-color);
            font-size: 2.2em;
            margin: 40px 0 20px 0;
            border-bottom: 2px solid var(--accent-color);
            padding-bottom: 10px;
        }}
        
        .chapter-content h2 {{
            color: var(--accent-color);
            font-size: 1.8em;
            margin: 35px 0 15px 0;
        }}
        
        .chapter-content h3 {{
            color: var(--accent-color);
            font-size: 1.4em;
            margin: 25px 0 10px 0;
        }}
        
        .chapter-content p {{
            margin: 20px 0;
            text-align: justify;
            text-indent: 2em;
        }}
        
        .chapter-content em {{
            color: var(--accent-color);
            font-style: italic;
        }}
        
        .chapter-content strong {{
            color: var(--accent-color);
            font-weight: bold;
        }}
        
        .chapter-content ul, .chapter-content ol {{
            margin: 20px 0;
            padding-left: 40px;
        }}
        
        .chapter-content li {{
            margin: 10px 0;
        }}
        
        .chapter-content hr {{
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--accent-color), transparent);
            margin: 40px 0;
        }}
        
        .footer {{
            text-align: center;
            padding: 40px;
            border-top: 2px solid var(--accent-color);
            margin-top: 60px;
            opacity: 0.8;
        }}
        
        @media print {{
            body {{ background: white; color: black; }}
            .ebook-container {{ box-shadow: none; background: white; }}
            .header {{ background: #f5f5f5; color: black; }}
            .chapter {{ page-break-before: always; }}
        }}
        
        @media (max-width: 768px) {{
            .ebook-container {{ margin: 10px; }}
            .header {{ padding: 30px 20px; }}
            .header h1 {{ font-size: 2em; }}
            .content {{ padding: 20px; }}
        }}
    </style>
</head>
<body>
    <div class="ebook-container">
        <div class="header">
            <h1>{metadata['title']}</h1>
            <div class="author">by {metadata['author']}</div>
            <div class="meta">
                <div>Generated: {datetime.fromisoformat(metadata['created']).strftime('%B %d, %Y')}</div>
                <div>Theme: {theme['name']}</div>
            </div>
        </div>
        
        <div class="content">
            <div class="toc">
                <h2>Table of Contents</h2>
"""
        
        # Add table of contents
        for i, chapter in enumerate(chapters, 1):
            chapter_id = self._sanitize_filename(chapter['title']).lower()
            html += f"""
                <div class="toc-entry">
                    <a href="#{chapter_id}">{chapter['title']}</a>
                    <span class="chapter-num">Chapter {i}</span>
                </div>
"""
        
        html += """
            </div>
"""
        
        # Add chapters
        for i, chapter in enumerate(chapters, 1):
            chapter_id = self._sanitize_filename(chapter['title']).lower()
            chapter_content = self._markdown_to_advanced_html(chapter['content'])
            
            html += f"""
            <div class="chapter" id="{chapter_id}">
                <div class="chapter-header">
                    <div class="chapter-number">Chapter {i}</div>
                    <h2 class="chapter-title">{chapter['title']}</h2>
                </div>
                <div class="chapter-content">
                    {chapter_content}
                </div>
            </div>
"""
        
        html += f"""
        </div>
        
        <div class="footer">
            <p>Generated by Advanced Codex Ebook Generator</p>
            <p>{metadata.get('description', '')}</p>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def _generate_markdown_book(self, chapters: List[Dict], metadata: Dict) -> Path:
        """Generate markdown format ebook"""
        
        filename = self._sanitize_filename(metadata["title"])
        output_path = self.output_dir / f"{filename}.md"
        
        markdown_content = f"""# {metadata['title']}

**Author:** {metadata['author']}  
**Generated:** {datetime.fromisoformat(metadata['created']).strftime('%B %d, %Y')}  
**Theme:** {metadata.get('theme', 'default')}  

---

## Table of Contents

"""
        
        # Add TOC
        for i, chapter in enumerate(chapters, 1):
            markdown_content += f"{i}. [{chapter['title']}](#{self._sanitize_filename(chapter['title']).lower()})\n"
        
        markdown_content += "\n---\n\n"
        
        # Add chapters
        for i, chapter in enumerate(chapters, 1):
            chapter_id = self._sanitize_filename(chapter['title']).lower()
            markdown_content += f"<div id='{chapter_id}'></div>\n\n"
            markdown_content += f"## Chapter {i}: {chapter['title']}\n\n"
            markdown_content += chapter['content'] + "\n\n"
            markdown_content += "---\n\n"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return output_path
    
    def _generate_json_book(self, chapters: List[Dict], metadata: Dict) -> Path:
        """Generate JSON format ebook"""
        
        filename = self._sanitize_filename(metadata["title"])
        output_path = self.output_dir / f"{filename}.json"
        
        json_data = {
            "metadata": metadata,
            "chapters": chapters,
            "generated": datetime.now().isoformat(),
            "format_version": "1.0"
        }
        
        save_json_safe(json_data, str(output_path))
        return output_path
    
    def _save_project_file(self, metadata: Dict, chapters: List[Dict], output_files: Dict) -> Path:
        """Save project file with all data"""
        
        filename = self._sanitize_filename(metadata["title"])
        project_path = self.output_dir / f"{filename}_project.json"
        
        project_data = {
            "metadata": metadata,
            "chapters": chapters,
            "output_files": output_files,
            "themes": self.themes,
            "generator_version": "2.0",
            "created": datetime.now().isoformat()
        }
        
        save_json_safe(project_data, str(project_path))
        return project_path
    
    def _markdown_to_advanced_html(self, markdown: str) -> str:
        """Convert markdown to advanced HTML with better formatting"""
        
        html = markdown
        
        # Convert headers
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)  
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # Convert emphasis
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        
        # Convert paragraphs
        paragraphs = html.split('\n\n')
        formatted_paragraphs = []
        
        for para in paragraphs:
            para = para.strip()
            if para:
                if para.startswith('<h') or para.startswith('<hr'):
                    formatted_paragraphs.append(para)
                else:
                    formatted_paragraphs.append(f'<p>{para.replace(chr(10), " ")}</p>')
        
        return '\n'.join(formatted_paragraphs)
    
    def _extract_title_from_markdown(self, content: str) -> Optional[str]:
        """Extract title from markdown content"""
        
        # Look for first # header
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        return None
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe use"""
        
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        sanitized = re.sub(r'\s+', '_', sanitized)
        sanitized = sanitized.strip('._')
        return sanitized[:100]

def main():
    """Demonstrate the advanced ebook generator"""
    
    print("ADVANCED CODEX EBOOK GENERATOR")
    print("=" * 60)
    
    generator = AdvancedCodexEbookGenerator()
    
    # Create proclamations ebook
    print("\n1. Creating Sacred Proclamations Ebook...")
    try:
        output_files = generator.create_proclamations_ebook()
        if output_files:
            print("Success! Created:")
            for fmt, path in output_files.items():
                print(f"  - {fmt.upper()}: {path}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Create comprehensive ebook
    print("\n2. Creating Comprehensive System Ebook...")
    try:
        output_files = generator.create_comprehensive_ebook(
            "Codex Dominion: Complete System Guide",
            "The Codex Council", 
            theme="council",
            include_sources=["proclamations", "documentation"],
            output_formats=["html", "markdown", "json"]
        )
        if output_files:
            print("Success! Created:")
            for fmt, path in output_files.items():
                print(f"  - {fmt.upper()}: {path}")
    except Exception as e:
        print(f"Error: {e}")
    
    print(f"\nAdvanced ebook generation complete!")
    print(f"Check the 'ebooks' directory for all generated files.")

if __name__ == "__main__":
    main()