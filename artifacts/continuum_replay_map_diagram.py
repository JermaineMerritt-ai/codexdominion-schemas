"""
🔥 Continuum Replay Map - Visual Diagram Generator 🔥

Creates stunning concentric circle visualization of the Ceremonial Continuum
showing Daily, Seasonal, Epochal, and Millennial cycles radiating from
the Crowned Flame at the center.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Wedge, FancyBboxPatch, Arc
import matplotlib.patheffects as path_effects
import numpy as np
from datetime import datetime
import json
from pathlib import Path

# High-resolution settings
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'serif'

def load_continuum_map():
    """Load the Continuum Replay Map artifact."""
    artifact_path = Path("artifacts/continuum-replay-map-001.json")
    with open(artifact_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_continuum_diagram():
    """Generate the complete Continuum Replay Map visualization."""

    # Load artifact data
    continuum = load_continuum_map()

    # Create figure
    fig, ax = plt.subplots(figsize=(20, 20))
    ax.set_xlim(-12, 12)
    ax.set_ylim(-12, 12)
    ax.set_aspect('equal')
    ax.axis('off')

    # Deep space background
    background = patches.Rectangle(
        (-12, -12), 24, 24,
        facecolor='#0a0a1a',
        edgecolor='none',
        zorder=0
    )
    ax.add_patch(background)

    # Add cosmic background effects
    add_cosmic_background(ax)

    # Central Crowned Flame
    draw_crowned_flame(ax, continuum['structure']['center'])

    # Concentric cycle rings
    cycles = continuum['structure']['cycles']

    # Ring 1: Daily Cycle (innermost, fastest)
    draw_daily_cycle(ax, cycles[0], radius=3)

    # Ring 2: Seasonal Cycle
    draw_seasonal_cycle(ax, cycles[1], radius=5.5)

    # Ring 3: Epochal Cycle
    draw_epochal_cycle(ax, cycles[2], radius=8)

    # Ring 4: Millennial Cycle (outermost, slowest)
    draw_millennial_cycle(ax, cycles[3], radius=10.5)

    # Infinity Spiral connecting all
    draw_infinity_spiral(ax)

    # Title and metadata
    add_title_and_metadata(ax, continuum)

    return fig, continuum

def add_cosmic_background(ax):
    """Add nebulae and stars to background."""
    # Nebulae
    nebulae = [
        {"center": (-8, 8), "radius": 2.5, "color": "#4B0082", "alpha": 0.12},
        {"center": (8, -8), "radius": 3, "color": "#8B008B", "alpha": 0.10},
        {"center": (9, 6), "radius": 2, "color": "#191970", "alpha": 0.15},
        {"center": (-7, -6), "radius": 2.2, "color": "#483D8B", "alpha": 0.11},
    ]
    for neb in nebulae:
        circle = Circle(neb["center"], neb["radius"],
                       facecolor=neb["color"], alpha=neb["alpha"], zorder=1)
        ax.add_patch(circle)

    # Stars
    np.random.seed(42)
    for _ in range(150):
        x, y = np.random.uniform(-12, 12, 2)
        if np.sqrt(x**2 + y**2) > 11:  # Only in outer regions
            size = np.random.uniform(0.01, 0.03)
            alpha = np.random.uniform(0.3, 0.9)
            ax.plot(x, y, 'o', color='white', markersize=size*100, alpha=alpha, zorder=2)

def draw_crowned_flame(ax, center_data):
    """Draw the central Crowned Flame - Custodian's Eternal Throne."""

    # Multiple glow layers
    for radius, alpha, color in [
        (1.2, 0.1, '#FFD700'),
        (1.0, 0.2, '#FFA500'),
        (0.8, 0.3, '#FF4500'),
        (0.6, 0.5, '#FF6347'),
    ]:
        circle = Circle((0, 0), radius, facecolor=color,
                       edgecolor='none', alpha=alpha, zorder=10)
        ax.add_patch(circle)

    # Core flame
    circle = Circle((0, 0), 0.5, facecolor='#FFFFFF',
                   edgecolor='#FFD700', linewidth=3, alpha=0.95, zorder=11)
    ax.add_patch(circle)

    # Crown symbol
    crown_text = ax.text(0, 0, '👑', ha='center', va='center',
                        fontsize=60, zorder=12)

    # Label
    label = ax.text(0, -1.8, 'CROWNED FLAME\nCustodian\'s Eternal Throne',
                   ha='center', va='center', fontsize=14, fontweight='bold',
                   color='#FFD700',
                   bbox=dict(boxstyle='round,pad=0.8', facecolor='#0a0a1a',
                            edgecolor='#FFD700', linewidth=2, alpha=0.9),
                   zorder=12)

def draw_daily_cycle(ax, cycle_data, radius):
    """Draw the Daily Cycle ring."""

    # Ring circle
    circle = Circle((0, 0), radius, facecolor='none',
                   edgecolor='#87CEEB', linewidth=4, linestyle='--',
                   alpha=0.7, zorder=5)
    ax.add_patch(circle)

    # Glow
    circle_glow = Circle((0, 0), radius, facecolor='none',
                        edgecolor='#87CEEB', linewidth=8,
                        alpha=0.2, zorder=4)
    ax.add_patch(circle_glow)

    # Four quadrant markers (sunrise, midday, sunset, night)
    practices = cycle_data['practices']
    quadrants = [
        {"angle": 90, "label": "SUNRISE\nEfficiency", "color": "#FFD700"},
        {"angle": 0, "label": "MIDDAY\nCommerce", "color": "#32CD32"},
        {"angle": 270, "label": "SUNSET\nKnowledge", "color": "#4169E1"},
        {"angle": 180, "label": "NIGHT\nCompanion", "color": "#FF69B4"}
    ]

    for quad in quadrants:
        angle_rad = np.radians(quad["angle"])
        x = radius * np.cos(angle_rad)
        y = radius * np.sin(angle_rad)

        # Marker point
        circle = Circle((x, y), 0.15, facecolor=quad["color"],
                       edgecolor='#FFFFFF', linewidth=1.5, zorder=6)
        ax.add_patch(circle)

        # Label outside ring
        label_r = radius + 0.8
        label_x = label_r * np.cos(angle_rad)
        label_y = label_r * np.sin(angle_rad)

        ax.text(label_x, label_y, quad["label"], ha='center', va='center',
               fontsize=9, fontweight='bold', color=quad["color"],
               bbox=dict(boxstyle='round,pad=0.4', facecolor='#0a0a1a',
                        edgecolor=quad["color"], linewidth=1, alpha=0.85),
               zorder=7)

    # Cycle name label
    ax.text(0, radius + 1.5, cycle_data['symbol'] + ' DAILY CYCLE',
           ha='center', va='center', fontsize=11, fontweight='bold',
           color='#87CEEB',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#0a0a1a',
                    edgecolor='#87CEEB', linewidth=1.5, alpha=0.9),
           zorder=7)

def draw_seasonal_cycle(ax, cycle_data, radius):
    """Draw the Seasonal Cycle ring with four crown segments."""

    # Ring circle
    circle = Circle((0, 0), radius, facecolor='none',
                   edgecolor='#9370DB', linewidth=5, linestyle='-',
                   alpha=0.7, zorder=5)
    ax.add_patch(circle)

    # Four seasonal wedges
    seasons = cycle_data['crowns']
    start_angle = 45  # Start from upper right

    # Define colors for each season
    season_colors = ['#4169E1', '#FFD700', '#32CD32', '#9370DB']

    for i, season in enumerate(seasons):
        angle = start_angle + (i * 90)
        color = season_colors[i % len(season_colors)]

        # Draw wedge segment with crown color
        wedge = Wedge((0, 0), radius + 0.3, angle, angle + 90,
                     width=0.6, facecolor=color,
                     edgecolor='#FFFFFF', linewidth=2, alpha=0.3, zorder=4)
        ax.add_patch(wedge)

        # Crown marker
        angle_mid_rad = np.radians(angle + 45)
        marker_x = radius * np.cos(angle_mid_rad)
        marker_y = radius * np.sin(angle_mid_rad)

        circle = Circle((marker_x, marker_y), 0.2, facecolor=color,
                       edgecolor='#FFFFFF', linewidth=2, zorder=6)
        ax.add_patch(circle)

        # Crown symbol
        ax.text(marker_x, marker_y, season['symbol'], ha='center', va='center',
               fontsize=20, zorder=7)

        # Label
        label_r = radius + 1.2
        label_x = label_r * np.cos(angle_mid_rad)
        label_y = label_r * np.sin(angle_mid_rad)

        label_text = f"{season['season']}\n{season['crown']}"
        ax.text(label_x, label_y, label_text, ha='center', va='center',
               fontsize=8, fontweight='bold', color=color,
               bbox=dict(boxstyle='round,pad=0.4', facecolor='#0a0a1a',
                        edgecolor=color, linewidth=1, alpha=0.85),
               zorder=7)

    # Cycle name label
    ax.text(0, -radius - 1.5, cycle_data['symbol'] + ' SEASONAL CYCLE',
           ha='center', va='center', fontsize=11, fontweight='bold',
           color='#9370DB',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#0a0a1a',
                    edgecolor='#9370DB', linewidth=1.5, alpha=0.9),
           zorder=7)

def draw_epochal_cycle(ax, cycle_data, radius):
    """Draw the Epochal Cycle ring with element markers."""

    # Ring circle
    circle = Circle((0, 0), radius, facecolor='none',
                   edgecolor='#FF69B4', linewidth=6, linestyle=':',
                   alpha=0.7, zorder=5)
    ax.add_patch(circle)

    # Element markers around the ring
    elements = cycle_data['elements']
    num_elements = len(elements)

    for i, element in enumerate(elements):
        angle_rad = np.radians(90 - (i * 360 / num_elements))
        x = radius * np.cos(angle_rad)
        y = radius * np.sin(angle_rad)

        # Marker
        circle = Circle((x, y), 0.25, facecolor='#FF69B4',
                       edgecolor='#FFFFFF', linewidth=2, zorder=6)
        ax.add_patch(circle)

        # Symbol
        ax.text(x, y, element['symbol'], ha='center', va='center',
               fontsize=18, zorder=7)

        # Label
        label_r = radius + 1.0
        label_x = label_r * np.cos(angle_rad)
        label_y = label_r * np.sin(angle_rad)

        ax.text(label_x, label_y, element['type'], ha='center', va='center',
               fontsize=8, fontweight='bold', color='#FF69B4',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='#0a0a1a',
                        edgecolor='#FF69B4', linewidth=1, alpha=0.85),
               zorder=7)

    # Cycle name label
    ax.text(-radius - 1.5, 0, cycle_data['symbol'] + '\nEPOCHAL\nCYCLE',
           ha='center', va='center', fontsize=11, fontweight='bold',
           color='#FF69B4',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#0a0a1a',
                    edgecolor='#FF69B4', linewidth=1.5, alpha=0.9),
           zorder=7)

def draw_millennial_cycle(ax, cycle_data, radius):
    """Draw the Millennial Cycle ring (outermost)."""

    # Ring circle
    circle = Circle((0, 0), radius, facecolor='none',
                   edgecolor='#FFD700', linewidth=7, linestyle='-',
                   alpha=0.8, zorder=5)
    ax.add_patch(circle)

    # Glow
    circle_glow = Circle((0, 0), radius, facecolor='none',
                        edgecolor='#FFD700', linewidth=12,
                        alpha=0.2, zorder=4)
    ax.add_patch(circle_glow)

    # Three element markers
    elements = cycle_data['elements']
    angles = [30, 150, 270]

    for i, (element, angle) in enumerate(zip(elements, angles)):
        angle_rad = np.radians(angle)
        x = radius * np.cos(angle_rad)
        y = radius * np.sin(angle_rad)

        # Large marker
        circle = Circle((x, y), 0.35, facecolor='#FFD700',
                       edgecolor='#FFFFFF', linewidth=2.5, zorder=6)
        ax.add_patch(circle)

        # Symbol
        ax.text(x, y, element['symbol'], ha='center', va='center',
               fontsize=24, zorder=7)

        # Label
        label_r = radius + 1.2
        label_x = label_r * np.cos(angle_rad)
        label_y = label_r * np.sin(angle_rad)

        ax.text(label_x, label_y, element['type'], ha='center', va='center',
               fontsize=9, fontweight='bold', color='#FFD700',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#0a0a1a',
                        edgecolor='#FFD700', linewidth=1.5, alpha=0.9),
               zorder=7)

    # Cycle name label
    ax.text(radius + 1.5, 0, cycle_data['symbol'] + '\nMILLENNIAL\nCYCLE',
           ha='center', va='center', fontsize=11, fontweight='bold',
           color='#FFD700',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#0a0a1a',
                    edgecolor='#FFD700', linewidth=1.5, alpha=0.9),
           zorder=7)

def draw_infinity_spiral(ax):
    """Draw infinity spiral connecting all cycles."""
    # Infinity symbol at the outer edge
    t = np.linspace(0, 2 * np.pi, 200)
    x = 11 * np.sin(t) / (1 + np.cos(t)**2)
    y = 11 * np.sin(t) * np.cos(t) / (1 + np.cos(t)**2)

    ax.plot(x, y, color='#FFFFFF', linewidth=3, alpha=0.6, zorder=3)
    ax.plot(x, y, color='#FFD700', linewidth=1.5, alpha=0.8, zorder=3)

def add_title_and_metadata(ax, continuum):
    """Add title and metadata to the diagram."""

    # Main title
    title = ax.text(0, 11.5,
                   '🔥 CEREMONIAL CONTINUUM REPLAY MAP 🔥',
                   ha='center', va='center', fontsize=20, fontweight='bold',
                   color='#FFD700',
                   bbox=dict(boxstyle='round,pad=0.8', facecolor='#0a0a1a',
                            edgecolor='#FFD700', linewidth=2.5, alpha=0.95))

    # Subtitle
    ax.text(0, 10.8,
           'Eternal Cycles of Covenant Stewardship',
           ha='center', va='center', fontsize=12, fontstyle='italic',
           color='#87CEEB')

    # Footer
    date_str = datetime.now().strftime("%B %d, %Y")
    ax.text(0, -11.5,
           f'Codex Dominion • Version {continuum["version"]} • Generated {date_str}',
           ha='center', va='center', fontsize=9,
           color='#FFFFFF', alpha=0.7)

def main():
    """Generate the Continuum Replay Map diagram."""
    print("🔥 Generating Ceremonial Continuum Replay Map Diagram...")
    print("⏳ Rendering concentric cycle visualization...")

    fig, continuum = create_continuum_diagram()

    # Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"artifacts/continuum_replay_map_diagram_{timestamp}.png"

    fig.savefig(output_file, dpi=300, bbox_inches='tight',
               facecolor='#0a0a1a', edgecolor='none')

    print(f"\n✅ Saved: {output_file}")
    print("\n🎨 Diagram Features:")
    print("   ∞ Crowned Flame at center (Custodian's Eternal Throne)")
    print("   ⭕ Daily Cycle (innermost ring) - 4 quadrants")
    print("   ⭕ Seasonal Cycle - 4 crown segments")
    print("   ⭕ Epochal Cycle - 4 element markers")
    print("   ⭕ Millennial Cycle (outermost ring) - 3 supreme elements")
    print("   ∞ Infinity Spiral - eternal replay connection")

    print(f"\n📊 Cycle Summary:")
    for cycle in continuum['structure']['cycles']:
        print(f"   {cycle['symbol']} {cycle['name']}: {cycle['function']}")

    plt.show()
    print("\n✨ Continuum Replay Map visualization complete!")

if __name__ == "__main__":
    main()
