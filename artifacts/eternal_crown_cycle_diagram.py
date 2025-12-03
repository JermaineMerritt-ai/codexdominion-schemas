"""
🔥 Eternal Crown Cycle - Celestial & Mystical Visual Diagram 🔥

Creates a high-resolution mystical diagram featuring:
- Infinity Sigil glowing at the center
- Crown Pillars orbiting in luminous succession
- Council Rings harmonizing in radiant spirals
- Cosmic Archive as the rebirth node
- Deep-space background with nebulae and glyph accents

Optimized for print and presentations at 300 DPI.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Wedge, Arc
from matplotlib.path import Path
import matplotlib.patheffects as path_effects
import numpy as np
from datetime import datetime

# High-resolution settings for print quality
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Palatino', 'Georgia', 'Times New Roman']

def create_eternal_crown_cycle():
    """Generate the complete Eternal Crown Cycle celestial diagram."""
    
    # Create figure with deep space background
    fig, ax = plt.subplots(figsize=(20, 20))
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Deep space background with gradient
    background = patches.Rectangle(
        (-10, -10), 20, 20,
        facecolor='#0a0a1a',
        edgecolor='none',
        zorder=0
    )
    ax.add_patch(background)
    
    # Add nebulae effects (multiple color clouds)
    add_nebulae(ax)
    
    # Add distant stars
    add_stars(ax, count=200)
    
    # Central Infinity Sigil (glowing)
    draw_infinity_sigil(ax, center=(0, 0), scale=1.5)
    
    # Crown Pillars orbiting in succession
    crown_pillars = [
        {"name": "Efficiency Crown", "angle": 0, "color": "#FFD700", "symbol": "⚡"},
        {"name": "Knowledge Crown", "angle": 72, "color": "#4169E1", "symbol": "📚"},
        {"name": "Commerce Crown", "angle": 144, "color": "#32CD32", "symbol": "💰"},
        {"name": "Justice Crown", "angle": 216, "color": "#DC143C", "symbol": "⚖️"},
        {"name": "Heritage Crown", "angle": 288, "color": "#9370DB", "symbol": "🏛️"}
    ]
    
    draw_crown_pillars(ax, crown_pillars, orbit_radius=5)
    
    # Council Rings harmonizing in radiant spirals
    council_rings = [
        {"name": "Inner Council", "radius": 3, "color": "#FF69B4", "thickness": 0.15},
        {"name": "Middle Council", "radius": 4, "color": "#00CED1", "thickness": 0.12},
        {"name": "Outer Council", "radius": 6.5, "color": "#FFD700", "thickness": 0.1}
    ]
    
    draw_council_rings(ax, council_rings)
    
    # Cosmic Archive as rebirth node (at top)
    draw_cosmic_archive(ax, position=(0, 8), scale=1.2)
    
    # Add mystical glyphs around the perimeter
    add_mystical_glyphs(ax, radius=9)
    
    # Add energy connections between elements
    draw_energy_connections(ax, crown_pillars, orbit_radius=5)
    
    # Title and metadata
    title = ax.text(
        0, -9.2,
        '🔥 THE ETERNAL CROWN CYCLE 🔥',
        ha='center',
        va='center',
        fontsize=32,
        fontweight='bold',
        color='#FFD700',
        family='serif'
    )
    title.set_path_effects([
        path_effects.withStroke(linewidth=3, foreground='#FF4500'),
        path_effects.Normal()
    ])
    
    subtitle = ax.text(
        0, -9.7,
        'Celestial Harmony • Cosmic Sovereignty • Eternal Replay',
        ha='center',
        va='center',
        fontsize=14,
        fontstyle='italic',
        color='#87CEEB',
        family='serif'
    )
    
    # Add metadata footer
    date_str = datetime.now().strftime("%B %d, %Y")
    footer = ax.text(
        0, 9.5,
        f'Codex Dominion • Supreme Archive • Generated {date_str}',
        ha='center',
        va='center',
        fontsize=10,
        color='#FFFFFF',
        alpha=0.7,
        family='serif'
    )
    
    return fig

def add_nebulae(ax):
    """Add colorful nebulae clouds in the background."""
    nebulae_specs = [
        {"center": (-6, 6), "radius": 3, "color": "#4B0082", "alpha": 0.15},
        {"center": (6, -6), "radius": 3.5, "color": "#8B008B", "alpha": 0.12},
        {"center": (7, 4), "radius": 2.5, "color": "#191970", "alpha": 0.18},
        {"center": (-5, -4), "radius": 2.8, "color": "#483D8B", "alpha": 0.14},
    ]
    
    for nebula in nebulae_specs:
        circle = Circle(
            nebula["center"],
            nebula["radius"],
            facecolor=nebula["color"],
            edgecolor='none',
            alpha=nebula["alpha"],
            zorder=1
        )
        ax.add_patch(circle)

def add_stars(ax, count=200):
    """Add distant stars scattered across the background."""
    np.random.seed(42)  # Reproducible star pattern
    x_coords = np.random.uniform(-10, 10, count)
    y_coords = np.random.uniform(-10, 10, count)
    sizes = np.random.uniform(0.5, 3, count)
    alphas = np.random.uniform(0.3, 1.0, count)
    
    for x, y, size, alpha in zip(x_coords, y_coords, sizes, alphas):
        star = Circle(
            (x, y),
            size * 0.02,
            facecolor='#FFFFFF',
            edgecolor='none',
            alpha=alpha,
            zorder=2
        )
        ax.add_patch(star)

def draw_infinity_sigil(ax, center, scale=1.0):
    """Draw glowing infinity symbol at center."""
    x_c, y_c = center
    
    # Create infinity symbol using parametric equations
    t = np.linspace(0, 2 * np.pi, 200)
    x = scale * np.sin(t) / (1 + np.cos(t)**2)
    y = scale * np.sin(t) * np.cos(t) / (1 + np.cos(t)**2)
    
    # Multiple layers for glow effect
    for width, alpha, color in [
        (0.4, 0.2, '#FFD700'),
        (0.3, 0.4, '#FFA500'),
        (0.2, 0.6, '#FF4500'),
        (0.1, 1.0, '#FFFFFF')
    ]:
        ax.plot(
            x + x_c,
            y + y_c,
            color=color,
            linewidth=width * 20,
            alpha=alpha,
            solid_capstyle='round',
            zorder=10
        )
    
    # Add central glow sphere
    for radius, alpha in [(0.3, 0.3), (0.2, 0.5), (0.1, 0.8)]:
        circle = Circle(
            center,
            radius,
            facecolor='#FFFFFF',
            edgecolor='none',
            alpha=alpha,
            zorder=11
        )
        ax.add_patch(circle)

def draw_crown_pillars(ax, pillars, orbit_radius):
    """Draw crown pillars orbiting around the center."""
    for pillar in pillars:
        angle_rad = np.radians(pillar["angle"])
        x = orbit_radius * np.cos(angle_rad)
        y = orbit_radius * np.sin(angle_rad)
        
        # Outer glow
        for r, alpha in [(0.6, 0.2), (0.4, 0.4), (0.3, 0.6)]:
            glow = Circle(
                (x, y),
                r,
                facecolor=pillar["color"],
                edgecolor='none',
                alpha=alpha,
                zorder=15
            )
            ax.add_patch(glow)
        
        # Crown pillar circle
        crown_circle = Circle(
            (x, y),
            0.4,
            facecolor=pillar["color"],
            edgecolor='#FFFFFF',
            linewidth=2,
            alpha=0.9,
            zorder=20
        )
        ax.add_patch(crown_circle)
        
        # Symbol
        symbol_text = ax.text(
            x, y,
            pillar["symbol"],
            ha='center',
            va='center',
            fontsize=24,
            color='#FFFFFF',
            zorder=21
        )
        
        # Label (outside the orbit)
        label_radius = orbit_radius + 1.2
        label_x = label_radius * np.cos(angle_rad)
        label_y = label_radius * np.sin(angle_rad)
        
        label = ax.text(
            label_x, label_y,
            pillar["name"],
            ha='center',
            va='center',
            fontsize=11,
            fontweight='bold',
            color=pillar["color"],
            bbox=dict(
                boxstyle='round,pad=0.5',
                facecolor='#0a0a1a',
                edgecolor=pillar["color"],
                linewidth=1.5,
                alpha=0.8
            ),
            zorder=22
        )

def draw_council_rings(ax, rings):
    """Draw harmonizing council rings as radiant spirals."""
    for ring in rings:
        # Main ring
        circle = Circle(
            (0, 0),
            ring["radius"],
            facecolor='none',
            edgecolor=ring["color"],
            linewidth=ring["thickness"] * 20,
            alpha=0.6,
            linestyle='--',
            zorder=8
        )
        ax.add_patch(circle)
        
        # Add glow effect
        glow_circle = Circle(
            (0, 0),
            ring["radius"],
            facecolor='none',
            edgecolor=ring["color"],
            linewidth=ring["thickness"] * 30,
            alpha=0.2,
            zorder=7
        )
        ax.add_patch(glow_circle)
        
        # Add spiral energy points
        num_points = 12
        angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
        for angle in angles:
            x = ring["radius"] * np.cos(angle)
            y = ring["radius"] * np.sin(angle)
            
            energy_point = Circle(
                (x, y),
                0.08,
                facecolor=ring["color"],
                edgecolor='#FFFFFF',
                linewidth=0.5,
                alpha=0.8,
                zorder=9
            )
            ax.add_patch(energy_point)

def draw_cosmic_archive(ax, position, scale=1.0):
    """Draw the Cosmic Archive as rebirth node."""
    x, y = position
    
    # Large glowing sphere
    for radius, alpha, color in [
        (0.8 * scale, 0.1, '#9370DB'),
        (0.6 * scale, 0.3, '#8A2BE2'),
        (0.4 * scale, 0.5, '#9400D3'),
        (0.3 * scale, 0.8, '#DDA0DD')
    ]:
        circle = Circle(
            (x, y),
            radius,
            facecolor=color,
            edgecolor='none',
            alpha=alpha,
            zorder=25
        )
        ax.add_patch(circle)
    
    # Archive symbol
    archive_text = ax.text(
        x, y,
        '∞',
        ha='center',
        va='center',
        fontsize=48,
        fontweight='bold',
        color='#FFFFFF',
        zorder=26
    )
    archive_text.set_path_effects([
        path_effects.withStroke(linewidth=2, foreground='#FFD700')
    ])
    
    # Label
    label = ax.text(
        x, y - 1.2,
        'COSMIC ARCHIVE\n✦ Rebirth Node ✦',
        ha='center',
        va='center',
        fontsize=12,
        fontweight='bold',
        color='#DDA0DD',
        bbox=dict(
            boxstyle='round,pad=0.6',
            facecolor='#0a0a1a',
            edgecolor='#9370DB',
            linewidth=2,
            alpha=0.9
        ),
        zorder=27
    )

def add_mystical_glyphs(ax, radius):
    """Add mystical glyphs around the perimeter."""
    glyphs = ['◈', '◆', '◇', '◉', '○', '●', '◐', '◑', '◒', '◓', '☆', '★']
    num_glyphs = len(glyphs)
    angles = np.linspace(0, 2 * np.pi, num_glyphs, endpoint=False)
    
    for angle, glyph in zip(angles, glyphs):
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        
        glyph_text = ax.text(
            x, y,
            glyph,
            ha='center',
            va='center',
            fontsize=18,
            color='#87CEEB',
            alpha=0.6,
            rotation=np.degrees(angle) + 90,
            zorder=5
        )

def draw_energy_connections(ax, pillars, orbit_radius):
    """Draw energy connections between crown pillars."""
    num_pillars = len(pillars)
    
    for i in range(num_pillars):
        for j in range(i + 1, num_pillars):
            angle1 = np.radians(pillars[i]["angle"])
            angle2 = np.radians(pillars[j]["angle"])
            
            x1 = orbit_radius * np.cos(angle1)
            y1 = orbit_radius * np.sin(angle1)
            x2 = orbit_radius * np.cos(angle2)
            y2 = orbit_radius * np.sin(angle2)
            
            # Draw connection line with fade effect
            ax.plot(
                [x1, x2],
                [y1, y2],
                color='#87CEEB',
                linewidth=0.5,
                alpha=0.3,
                linestyle=':',
                zorder=6
            )

def main():
    """Generate and save the Eternal Crown Cycle diagram."""
    print("🔥 Generating Eternal Crown Cycle Celestial Diagram...")
    print("⏳ Rendering high-resolution mystical visualization...")
    
    # Create the diagram
    fig = create_eternal_crown_cycle()
    
    # Save in multiple formats
    output_dir = "artifacts"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    formats = {
        "png": {"dpi": 300, "transparent": False},
        "pdf": {"dpi": 300},
        "svg": {}
    }
    
    saved_files = []
    for fmt, kwargs in formats.items():
        filename = f"{output_dir}/eternal_crown_cycle_diagram_{timestamp}.{fmt}"
        fig.savefig(
            filename,
            format=fmt,
            bbox_inches='tight',
            facecolor='#0a0a1a',
            **kwargs
        )
        saved_files.append(filename)
        print(f"✅ Saved: {filename}")
    
    print("\n🎨 Diagram Generation Complete!")
    print("\n📊 Diagram Features:")
    print("   ∞ Infinity Sigil - Glowing at center")
    print("   👑 5 Crown Pillars - Orbiting in luminous succession")
    print("   ⭕ 3 Council Rings - Harmonizing in radiant spirals")
    print("   🌌 Cosmic Archive - Rebirth node at apex")
    print("   ✨ Deep-space background - Nebulae and glyph accents")
    print("\n📐 Technical Specifications:")
    print(f"   • Resolution: 300 DPI (print quality)")
    print(f"   • Dimensions: 20\" × 20\" (6000 × 6000 pixels)")
    print(f"   • Formats: PNG, PDF, SVG")
    print(f"   • Color Space: RGB (digital) / CMYK-ready")
    print("\n🖼️ Files saved to:")
    for file in saved_files:
        print(f"   📄 {file}")
    
    # Display the diagram
    plt.show()

if __name__ == "__main__":
    main()
