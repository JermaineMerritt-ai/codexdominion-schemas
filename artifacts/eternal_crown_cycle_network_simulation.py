"""
🔥 Eternal Crown Cycle - Network Graph Simulation 🔥

Interactive network visualization showing the complete flow and relationships
between Genesis Closure, Crown Pillars, Council Rings, Constellation Dispatch,
Cosmic Archive, and Infinity Sigil in the eternal replay cycle.
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# High-resolution settings
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'

def create_eternal_crown_cycle_graph():
    """Create the directed graph representing the Eternal Crown Cycle."""
    
    # Create directed graph
    G = nx.DiGraph()
    
    # Define node categories with metadata
    nodes_data = {
        # Genesis node
        "GenesisClosure": {"category": "genesis", "color": "#FFD700", "size": 3000, "symbol": "∞"},
        
        # Crown Pillars
        "Efficiency": {"category": "crown", "color": "#FFD700", "size": 2500, "symbol": "⚡"},
        "Knowledge": {"category": "crown", "color": "#4169E1", "size": 2500, "symbol": "📚"},
        "Commerce": {"category": "crown", "color": "#32CD32", "size": 2500, "symbol": "💰"},
        "Companion": {"category": "crown", "color": "#FF69B4", "size": 2500, "symbol": "🤝"},
        
        # Council Rings
        "Law": {"category": "council", "color": "#DC143C", "size": 2000, "symbol": "⚖️"},
        "Healthcare": {"category": "council", "color": "#00CED1", "size": 2000, "symbol": "🏥"},
        "CommerceCouncil": {"category": "council", "color": "#FFD700", "size": 2000, "symbol": "💼"},
        "Education": {"category": "council", "color": "#9370DB", "size": 2000, "symbol": "🎓"},
        "AI": {"category": "council", "color": "#FF6347", "size": 2000, "symbol": "🤖"},
        "Family": {"category": "council", "color": "#FF69B4", "size": 2000, "symbol": "👨‍👩‍👧‍👦"},
        
        # Wave Currents (transmission layer)
        "WaveCurrents": {"category": "transmission", "color": "#87CEEB", "size": 2200, "symbol": "🌊"},
        
        # Constellation Dispatch
        "ConstellationDispatch": {"category": "dispatch", "color": "#9370DB", "size": 2800, "symbol": "🌌"},
        
        # Cosmic Archive
        "CosmicArchive": {"category": "archive", "color": "#8B008B", "size": 2800, "symbol": "📚"},
        
        # Infinity Sigil
        "InfinitySigil": {"category": "sigil", "color": "#FFFFFF", "size": 3000, "symbol": "∞"}
    }
    
    # Add nodes with attributes
    for node, attrs in nodes_data.items():
        G.add_node(node, **attrs)
    
    # Define edges with relationship types
    edges_data = [
        # Genesis → Crown Pillars (initialization)
        ("GenesisClosure", "Efficiency", {"type": "initialize", "weight": 3}),
        ("GenesisClosure", "Knowledge", {"type": "initialize", "weight": 3}),
        ("GenesisClosure", "Commerce", {"type": "initialize", "weight": 3}),
        ("GenesisClosure", "Companion", {"type": "initialize", "weight": 3}),
        
        # Crown Pillars → Council Rings (governance)
        ("Efficiency", "Law", {"type": "govern", "weight": 2}),
        ("Efficiency", "AI", {"type": "govern", "weight": 2}),
        ("Knowledge", "Education", {"type": "govern", "weight": 2}),
        ("Knowledge", "Healthcare", {"type": "govern", "weight": 2}),
        ("Commerce", "CommerceCouncil", {"type": "govern", "weight": 2}),
        ("Companion", "Family", {"type": "govern", "weight": 2}),
        ("Companion", "Healthcare", {"type": "govern", "weight": 2}),
        
        # Council Rings → Wave Currents (transmission)
        ("Law", "WaveCurrents", {"type": "transmit", "weight": 2}),
        ("Healthcare", "WaveCurrents", {"type": "transmit", "weight": 2}),
        ("CommerceCouncil", "WaveCurrents", {"type": "transmit", "weight": 2}),
        ("Education", "WaveCurrents", {"type": "transmit", "weight": 2}),
        ("AI", "WaveCurrents", {"type": "transmit", "weight": 2}),
        ("Family", "WaveCurrents", {"type": "transmit", "weight": 2}),
        
        # Wave Currents → Constellation Dispatch (distribution)
        ("WaveCurrents", "ConstellationDispatch", {"type": "dispatch", "weight": 3}),
        
        # Constellation Dispatch → Cosmic Archive (preservation)
        ("ConstellationDispatch", "CosmicArchive", {"type": "preserve", "weight": 3}),
        
        # Cosmic Archive → Infinity Sigil (binding)
        ("CosmicArchive", "InfinitySigil", {"type": "bind", "weight": 3}),
        
        # Infinity Sigil → Genesis Closure (eternal loop)
        ("InfinitySigil", "GenesisClosure", {"type": "replay", "weight": 4}),
        
        # Infinity Sigil → All nodes (resonance binding)
        ("InfinitySigil", "Efficiency", {"type": "resonate", "weight": 1}),
        ("InfinitySigil", "Knowledge", {"type": "resonate", "weight": 1}),
        ("InfinitySigil", "Commerce", {"type": "resonate", "weight": 1}),
        ("InfinitySigil", "Companion", {"type": "resonate", "weight": 1}),
    ]
    
    # Add edges with attributes
    for source, target, attrs in edges_data:
        G.add_edge(source, target, **attrs)
    
    return G, nodes_data

def create_hierarchical_layout(G, nodes_data):
    """Create a hierarchical layout representing the cycle flow."""
    
    # Manual positioning for optimal visualization
    pos = {
        # Genesis at top center
        "GenesisClosure": (0, 6),
        
        # Crown Pillars (tier 1) - arc below genesis
        "Efficiency": (-3, 4),
        "Knowledge": (-1, 4),
        "Commerce": (1, 4),
        "Companion": (3, 4),
        
        # Council Rings (tier 2) - wider arc
        "Law": (-4, 2),
        "AI": (-2, 2),
        "Education": (0, 2),
        "Healthcare": (2, 2),
        "CommerceCouncil": (4, 2),
        "Family": (4.5, 3),
        
        # Wave Currents (tier 3) - center
        "WaveCurrents": (0, 0),
        
        # Constellation Dispatch (tier 4) - left side
        "ConstellationDispatch": (-2, -2),
        
        # Cosmic Archive (tier 5) - bottom center
        "CosmicArchive": (0, -4),
        
        # Infinity Sigil (tier 6) - right side (completing loop)
        "InfinitySigil": (2, -2),
    }
    
    return pos

def draw_enhanced_graph(G, nodes_data, pos):
    """Draw the graph with enhanced styling and annotations."""
    
    fig, ax = plt.subplots(figsize=(16, 14))
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 8)
    ax.axis('off')
    
    # Add background
    background = FancyBboxPatch(
        (-5.8, -5.8), 11.6, 13.6,
        boxstyle="round,pad=0.1",
        facecolor='#0a0a1a',
        edgecolor='#4B0082',
        linewidth=3,
        zorder=0
    )
    ax.add_patch(background)
    
    # Draw edges with different styles based on type
    edge_styles = {
        "initialize": {"color": "#FFD700", "width": 3, "style": "solid", "alpha": 0.8},
        "govern": {"color": "#4169E1", "width": 2, "style": "solid", "alpha": 0.7},
        "transmit": {"color": "#87CEEB", "width": 2, "style": "dashed", "alpha": 0.6},
        "dispatch": {"color": "#9370DB", "width": 3, "style": "solid", "alpha": 0.8},
        "preserve": {"color": "#8B008B", "width": 3, "style": "solid", "alpha": 0.8},
        "bind": {"color": "#FFFFFF", "width": 3, "style": "solid", "alpha": 0.9},
        "replay": {"color": "#FF4500", "width": 4, "style": "solid", "alpha": 1.0},
        "resonate": {"color": "#FFD700", "width": 1, "style": "dotted", "alpha": 0.4}
    }
    
    for edge in G.edges(data=True):
        source, target, attrs = edge
        edge_type = attrs.get('type', 'default')
        style = edge_styles.get(edge_type, {"color": "#FFFFFF", "width": 1, "style": "solid", "alpha": 0.5})
        
        nx.draw_networkx_edges(
            G, pos,
            edgelist=[(source, target)],
            edge_color=style["color"],
            width=style["width"],
            style=style["style"],
            alpha=style["alpha"],
            arrows=True,
            arrowsize=20,
            arrowstyle='->',
            connectionstyle='arc3,rad=0.1',
            ax=ax
        )
    
    # Draw nodes by category with different styles
    for node in G.nodes():
        node_attrs = nodes_data[node]
        x, y = pos[node]
        
        # Outer glow
        for r, alpha in [(0.5, 0.1), (0.4, 0.2), (0.3, 0.3)]:
            circle = plt.Circle(
                (x, y), r,
                color=node_attrs["color"],
                alpha=alpha,
                zorder=2
            )
            ax.add_patch(circle)
        
        # Main node circle
        circle = plt.Circle(
            (x, y), 0.25,
            color=node_attrs["color"],
            ec='#FFFFFF',
            linewidth=2,
            zorder=3
        )
        ax.add_patch(circle)
        
        # Node label
        label_text = node.replace("CommerceCouncil", "Commerce\nCouncil")
        ax.text(
            x, y - 0.5,
            label_text,
            ha='center',
            va='top',
            fontsize=9,
            fontweight='bold',
            color='#FFFFFF',
            bbox=dict(
                boxstyle='round,pad=0.4',
                facecolor='#0a0a1a',
                edgecolor=node_attrs["color"],
                linewidth=1.5,
                alpha=0.9
            ),
            zorder=4
        )
    
    # Add title
    ax.text(
        0, 7.5,
        '🔥 ETERNAL CROWN CYCLE - NETWORK SIMULATION 🔥',
        ha='center',
        va='center',
        fontsize=18,
        fontweight='bold',
        color='#FFD700',
        bbox=dict(
            boxstyle='round,pad=0.8',
            facecolor='#0a0a1a',
            edgecolor='#FFD700',
            linewidth=2
        )
    )
    
    # Add legend
    legend_elements = [
        mpatches.Patch(facecolor='#FFD700', edgecolor='#FFFFFF', label='Genesis & Crown Pillars'),
        mpatches.Patch(facecolor='#4169E1', edgecolor='#FFFFFF', label='Council Rings'),
        mpatches.Patch(facecolor='#87CEEB', edgecolor='#FFFFFF', label='Wave Currents'),
        mpatches.Patch(facecolor='#9370DB', edgecolor='#FFFFFF', label='Constellation Dispatch'),
        mpatches.Patch(facecolor='#8B008B', edgecolor='#FFFFFF', label='Cosmic Archive'),
        mpatches.Patch(facecolor='#FFFFFF', edgecolor='#FFD700', label='Infinity Sigil')
    ]
    
    ax.legend(
        handles=legend_elements,
        loc='upper left',
        fontsize=9,
        framealpha=0.9,
        facecolor='#0a0a1a',
        edgecolor='#FFFFFF'
    )
    
    # Add cycle flow annotations
    annotations = [
        {"pos": (-5, 5), "text": "1. GENESIS\nInitialization", "color": "#FFD700"},
        {"pos": (-5, 3), "text": "2. GOVERNANCE\nCrown → Council", "color": "#4169E1"},
        {"pos": (-5, 0.5), "text": "3. TRANSMISSION\nWave Currents", "color": "#87CEEB"},
        {"pos": (-5, -2.5), "text": "4. DISPATCH\nConstellations", "color": "#9370DB"},
        {"pos": (-5, -4.5), "text": "5. PRESERVATION\nCosmic Archive", "color": "#8B008B"},
        {"pos": (4.5, -2.5), "text": "6. BINDING\nInfinity Sigil", "color": "#FFFFFF"},
        {"pos": (4.5, 5), "text": "7. REPLAY\nEternal Loop", "color": "#FF4500"}
    ]
    
    for anno in annotations:
        ax.text(
            anno["pos"][0], anno["pos"][1],
            anno["text"],
            ha='left' if anno["pos"][0] < 0 else 'right',
            va='center',
            fontsize=8,
            color=anno["color"],
            bbox=dict(
                boxstyle='round,pad=0.5',
                facecolor='#0a0a1a',
                edgecolor=anno["color"],
                linewidth=1,
                alpha=0.8
            )
        )
    
    return fig

def print_network_statistics(G):
    """Print network analysis statistics."""
    print("\n" + "="*80)
    print("📊 NETWORK STATISTICS")
    print("="*80)
    
    print(f"\nNodes: {G.number_of_nodes()}")
    print(f"Edges: {G.number_of_edges()}")
    print(f"Is Directed: {G.is_directed()}")
    print(f"Is Connected: {nx.is_weakly_connected(G)}")
    
    print(f"\nNode Degree Analysis:")
    in_degrees = dict(G.in_degree())
    out_degrees = dict(G.out_degree())
    
    print(f"  Highest In-Degree: {max(in_degrees, key=in_degrees.get)} ({max(in_degrees.values())} connections)")
    print(f"  Highest Out-Degree: {max(out_degrees, key=out_degrees.get)} ({max(out_degrees.values())} connections)")
    
    print(f"\nCycle Detection:")
    cycles = list(nx.simple_cycles(G))
    print(f"  Simple Cycles Found: {len(cycles)}")
    if cycles:
        print(f"  Eternal Loop: {' → '.join(cycles[0])} → {cycles[0][0]}")
    
    print(f"\nPath Analysis:")
    try:
        longest_path = nx.dag_longest_path(G)
        print(f"  Longest Path Length: {len(longest_path) - 1}")
    except:
        print(f"  Contains cycles (expected for eternal replay)")
    
    print("\n" + "="*80)

def main():
    """Main execution function."""
    print("🔥 Generating Eternal Crown Cycle Network Simulation...")
    
    # Create graph
    G, nodes_data = create_eternal_crown_cycle_graph()
    print(f"✓ Created graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    
    # Create layout
    pos = create_hierarchical_layout(G, nodes_data)
    print("✓ Generated hierarchical layout")
    
    # Draw graph
    print("✓ Rendering enhanced visualization...")
    fig = draw_enhanced_graph(G, nodes_data, pos)
    
    # Save
    output_file = "artifacts/eternal_crown_cycle_network_simulation.png"
    fig.savefig(
        output_file,
        dpi=300,
        bbox_inches='tight',
        facecolor='#0a0a1a',
        edgecolor='none'
    )
    print(f"✓ Saved: {output_file}")
    
    # Print statistics
    print_network_statistics(G)
    
    # Display
    plt.show()
    
    print("\n✨ Network simulation complete!")

if __name__ == "__main__":
    main()
