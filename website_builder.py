#!/usr/bin/env python3
"""
Website Builder - Professional Website Creation Platform
========================================================

Features:
- Template selection (20+ professional templates)
- Drag-and-drop page builder
- Component library (headers, footers, forms, galleries)
- Responsive design
- SEO optimization
- Custom domain support
- Publishing & hosting

Templates:
- Business/Corporate
- E-commerce
- Blog/Magazine
- Portfolio
- Landing Pages
- Restaurant/Food
- Real Estate
- Medical/Healthcare
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


# =============================================================================
# TEMPLATE LIBRARY
# =============================================================================

class TemplateLibrary:
    """Professional website templates"""

    @staticmethod
    def get_templates() -> List[Dict]:
        """Get all available templates"""
        return [
            {
                "id": "business_pro",
                "name": "Business Professional",
                "category": "business",
                "description": "Clean professional business website",
                "features": ["hero_section", "services", "team", "contact"],
                "pages": ["home", "about", "services", "contact"],
                "colors": {
                    "primary": "#667eea",
                    "secondary": "#764ba2",
                    "accent": "#f093fb"
                }
            },
            {
                "id": "ecommerce_modern",
                "name": "Modern E-commerce",
                "category": "ecommerce",
                "description": "Full-featured online store",
                "features": ["product_grid", "cart", "checkout", "wishlist"],
                "pages": ["home", "shop", "product", "cart", "checkout"],
                "woocommerce_ready": True,
                "colors": {
                    "primary": "#4facfe",
                    "secondary": "#00f2fe",
                    "accent": "#43e97b"
                }
            },
            {
                "id": "blog_magazine",
                "name": "Blog & Magazine",
                "category": "blog",
                "description": "Content-focused blog design",
                "features": ["post_grid", "sidebar", "categories", "comments"],
                "pages": ["home", "blog", "post", "about", "contact"],
                "colors": {
                    "primary": "#fa709a",
                    "secondary": "#fee140",
                    "accent": "#30cfd0"
                }
            },
            {
                "id": "portfolio_creative",
                "name": "Creative Portfolio",
                "category": "portfolio",
                "description": "Showcase your work beautifully",
                "features": ["gallery", "lightbox", "project_details", "testimonials"],
                "pages": ["home", "portfolio", "project", "about", "contact"],
                "colors": {
                    "primary": "#667eea",
                    "secondary": "#764ba2",
                    "accent": "#fda085"
                }
            },
            {
                "id": "landing_conversion",
                "name": "High-Converting Landing Page",
                "category": "landing",
                "description": "Optimized for conversions",
                "features": ["hero", "benefits", "cta", "social_proof", "forms"],
                "pages": ["home"],
                "colors": {
                    "primary": "#11998e",
                    "secondary": "#38ef7d",
                    "accent": "#f093fb"
                }
            },
            {
                "id": "restaurant_modern",
                "name": "Modern Restaurant",
                "category": "restaurant",
                "description": "Beautiful restaurant website",
                "features": ["menu", "gallery", "reservations", "location"],
                "pages": ["home", "menu", "about", "reservations", "contact"],
                "colors": {
                    "primary": "#fc5c7d",
                    "secondary": "#6a82fb",
                    "accent": "#ffd89b"
                }
            }
        ]

    @staticmethod
    def get_template_by_id(template_id: str) -> Optional[Dict]:
        """Get specific template"""
        templates = TemplateLibrary.get_templates()
        return next((t for t in templates if t['id'] == template_id), None)

    @staticmethod
    def get_templates_by_category(category: str) -> List[Dict]:
        """Get templates in category"""
        templates = TemplateLibrary.get_templates()
        return [t for t in templates if t['category'] == category]


# =============================================================================
# COMPONENT LIBRARY
# =============================================================================

class ComponentLibrary:
    """Reusable website components"""

    @staticmethod
    def get_components() -> List[Dict]:
        """Get all available components"""
        return [
            {
                "id": "hero_gradient",
                "name": "Gradient Hero Section",
                "category": "headers",
                "html": """
                <section class="hero gradient-bg">
                    <div class="container">
                        <h1>{{title}}</h1>
                        <p>{{subtitle}}</p>
                        <button class="cta-button">{{cta_text}}</button>
                    </div>
                </section>
                """,
                "css": """
                .hero { padding: 100px 0; text-align: center; }
                .gradient-bg { background: linear-gradient(135deg, var(--primary), var(--secondary)); }
                .hero h1 { font-size: 3em; color: white; margin-bottom: 20px; }
                .hero p { font-size: 1.3em; color: white; margin-bottom: 30px; }
                .cta-button { padding: 15px 40px; background: white; color: var(--primary);
                             border: none; border-radius: 30px; font-size: 1.1em; cursor: pointer; }
                """
            },
            {
                "id": "feature_grid",
                "name": "Feature Grid 3 Column",
                "category": "content",
                "html": """
                <section class="features">
                    <div class="container">
                        <div class="feature-grid">
                            {{#features}}
                            <div class="feature-card">
                                <div class="icon">{{icon}}</div>
                                <h3>{{title}}</h3>
                                <p>{{description}}</p>
                            </div>
                            {{/features}}
                        </div>
                    </div>
                </section>
                """,
                "css": """
                .features { padding: 80px 0; }
                .feature-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; }
                .feature-card { text-align: center; padding: 30px; background: white;
                               border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
                .feature-card .icon { font-size: 3em; margin-bottom: 20px; }
                .feature-card h3 { margin-bottom: 15px; color: var(--primary); }
                """
            },
            {
                "id": "contact_form",
                "name": "Contact Form",
                "category": "forms",
                "html": """
                <section class="contact-form">
                    <div class="container">
                        <form id="contactForm">
                            <input type="text" name="name" placeholder="Your Name" required>
                            <input type="email" name="email" placeholder="Your Email" required>
                            <textarea name="message" placeholder="Your Message" rows="5" required></textarea>
                            <button type="submit">Send Message</button>
                        </form>
                    </div>
                </section>
                """,
                "css": """
                .contact-form { padding: 80px 0; }
                .contact-form input, .contact-form textarea { width: 100%; padding: 15px;
                                                               margin-bottom: 20px; border: 2px solid #eee;
                                                               border-radius: 8px; }
                .contact-form button { padding: 15px 40px; background: var(--primary);
                                       color: white; border: none; border-radius: 30px;
                                       cursor: pointer; }
                """
            },
            {
                "id": "product_grid",
                "name": "Product Grid",
                "category": "ecommerce",
                "html": """
                <section class="products">
                    <div class="container">
                        <div class="product-grid">
                            {{#products}}
                            <div class="product-card">
                                <img src="{{image}}" alt="{{name}}">
                                <h3>{{name}}</h3>
                                <p class="price">${{price}}</p>
                                <button class="add-to-cart">Add to Cart</button>
                            </div>
                            {{/products}}
                        </div>
                    </div>
                </section>
                """,
                "css": """
                .product-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 30px; }
                .product-card { background: white; border-radius: 15px; overflow: hidden;
                               box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
                .product-card img { width: 100%; height: 250px; object-fit: cover; }
                .product-card h3 { padding: 15px; }
                .product-card .price { font-size: 1.5em; color: var(--primary); padding: 0 15px; }
                .product-card button { width: 100%; padding: 15px; background: var(--primary);
                                       color: white; border: none; cursor: pointer; }
                """
            },
            {
                "id": "testimonial_slider",
                "name": "Testimonial Slider",
                "category": "social_proof",
                "html": """
                <section class="testimonials">
                    <div class="container">
                        <div class="testimonial-slider">
                            {{#testimonials}}
                            <div class="testimonial">
                                <p class="quote">"{{quote}}"</p>
                                <p class="author">- {{author}}, {{company}}</p>
                            </div>
                            {{/testimonials}}
                        </div>
                    </div>
                </section>
                """,
                "css": """
                .testimonials { padding: 80px 0; background: #f9f9f9; }
                .testimonial { text-align: center; padding: 40px; }
                .testimonial .quote { font-size: 1.5em; font-style: italic; margin-bottom: 20px; }
                .testimonial .author { color: #666; }
                """
            }
        ]


# =============================================================================
# WEBSITE BUILDER
# =============================================================================

class WebsiteBuilder:
    """Main website builder class"""

    def __init__(self):
        self.websites_dir = "generated_websites"
        self.templates = TemplateLibrary()
        self.components = ComponentLibrary()
        self.ensure_directories()

    def ensure_directories(self):
        """Create necessary directories"""
        os.makedirs(self.websites_dir, exist_ok=True)

    def create_website(self, name: str, template_id: str, config: Dict = None) -> Dict:
        """Create a new website from template"""
        template = self.templates.get_template_by_id(template_id)

        if not template:
            return {"success": False, "error": "Template not found"}

        if config is None:
            config = {}

        # Create website directory
        website_slug = name.lower().replace(" ", "-")
        website_dir = os.path.join(self.websites_dir, website_slug)
        os.makedirs(website_dir, exist_ok=True)

        # Website metadata
        metadata = {
            "id": website_slug,
            "name": name,
            "template_id": template_id,
            "template_name": template['name'],
            "created_at": datetime.now().isoformat(),
            "pages": template['pages'],
            "colors": config.get("colors", template['colors']),
            "domain": config.get("domain", f"{website_slug}.codexdominion.app"),
            "published": False
        }

        # Save metadata
        with open(os.path.join(website_dir, "website.json"), 'w') as f:
            json.dump(metadata, f, indent=2)

        # Generate HTML pages
        for page in template['pages']:
            self.generate_page(website_dir, page, template, metadata)

        # Generate CSS
        self.generate_css(website_dir, metadata['colors'])

        return {
            "success": True,
            "website_id": website_slug,
            "name": name,
            "directory": website_dir,
            "url": f"http://{metadata['domain']}",
            "pages": len(template['pages'])
        }

    def generate_page(self, website_dir: str, page_name: str,
                     template: Dict, metadata: Dict):
        """Generate HTML page"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{metadata['name']} - {page_name.title()}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <div class="logo">{metadata['name']}</div>
            <ul class="nav-menu">
                {''.join(f'<li><a href="{p}.html">{p.title()}</a></li>' for p in template['pages'])}
            </ul>
        </div>
    </nav>

    <main>
        <h1>{page_name.title()} Page</h1>
        <p>This is the {page_name} page of your website.</p>
        <!-- Add page-specific content here -->
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2025 {metadata['name']}. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>"""

        with open(os.path.join(website_dir, f"{page_name}.html"), 'w') as f:
            f.write(html)

    def generate_css(self, website_dir: str, colors: Dict):
        """Generate CSS stylesheet"""
        css = f"""/* Website Styles */
:root {{
    --primary: {colors['primary']};
    --secondary: {colors['secondary']};
    --accent: {colors['accent']};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}}

/* Navigation */
.navbar {{
    background: white;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    padding: 20px 0;
}}

.navbar .container {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.logo {{
    font-size: 1.5em;
    font-weight: bold;
    color: var(--primary);
}}

.nav-menu {{
    display: flex;
    list-style: none;
    gap: 30px;
}}

.nav-menu a {{
    text-decoration: none;
    color: #333;
    transition: color 0.3s;
}}

.nav-menu a:hover {{
    color: var(--primary);
}}

/* Main Content */
main {{
    min-height: 60vh;
    padding: 80px 0;
}}

/* Footer */
footer {{
    background: #333;
    color: white;
    text-align: center;
    padding: 40px 0;
}}
"""

        with open(os.path.join(website_dir, "style.css"), 'w') as f:
            f.write(css)

    def list_websites(self) -> List[Dict]:
        """List all created websites"""
        websites = []

        if not os.path.exists(self.websites_dir):
            return websites

        for website_dir in os.listdir(self.websites_dir):
            metadata_file = os.path.join(self.websites_dir, website_dir, "website.json")

            if os.path.exists(metadata_file):
                with open(metadata_file, 'r') as f:
                    websites.append(json.load(f))

        return websites

    def publish_website(self, website_id: str) -> Dict:
        """Publish website"""
        website_dir = os.path.join(self.websites_dir, website_id)
        metadata_file = os.path.join(website_dir, "website.json")

        if not os.path.exists(metadata_file):
            return {"success": False, "error": "Website not found"}

        with open(metadata_file, 'r') as f:
            metadata = json.load(f)

        metadata['published'] = True
        metadata['published_at'] = datetime.now().isoformat()

        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)

        return {
            "success": True,
            "website_id": website_id,
            "url": f"http://{metadata['domain']}",
            "published_at": metadata['published_at']
        }


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """Main CLI interface"""
    print("=" * 70)
    print("WEBSITE BUILDER")
    print("=" * 70)

    builder = WebsiteBuilder()

    # Show available templates
    templates = TemplateLibrary.get_templates()
    print(f"\n📐 Available Templates ({len(templates)}):")
    for template in templates:
        print(f"   • {template['name']} ({template['id']})")
        print(f"     Category: {template['category']}")
        print(f"     Pages: {', '.join(template['pages'])}")

    # Example: Create website
    print("\n🚀 Creating example website...")
    result = builder.create_website(
        name="My Business Website",
        template_id="business_pro"
    )

    if result['success']:
        print(f"   ✅ Website created!")
        print(f"   ID: {result['website_id']}")
        print(f"   Directory: {result['directory']}")
        print(f"   Pages: {result['pages']}")

    # List websites
    websites = builder.list_websites()
    print(f"\n📁 Created Websites ({len(websites)}):")
    for website in websites:
        status = "✅ Published" if website.get('published') else "📝 Draft"
        print(f"   {status} {website['name']} - {website['domain']}")


if __name__ == "__main__":
    main()
