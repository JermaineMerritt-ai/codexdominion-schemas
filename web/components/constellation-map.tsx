'use client';

import { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { useReplay } from '@/context/ReplayContext';

interface Node {
  id: string;
  group: string;
  x?: number;
  y?: number;
  fx?: number | null;
  fy?: number | null;
}

interface Link {
  source: string | Node;
  target: string | Node;
}

export function ConstellationMap() {
  const ref = useRef<SVGSVGElement>(null);
  const { index, capsules } = useReplay();

  useEffect(() => {
    if (!ref.current) return;

    const nodes: Node[] = [
      { id: 'Distribution Engine', group: 'engine' },
      { id: 'Marketing Engine', group: 'engine' },
      { id: 'Commerce Engine', group: 'engine' },
      { id: 'Video Studio', group: 'engine' },
      { id: 'Automations', group: 'automation' },
      { id: 'Avatars', group: 'avatar' },
      { id: 'Products', group: 'product' },
    ];

    const links: Link[] = [
      { source: 'Distribution Engine', target: 'Marketing Engine' },
      { source: 'Marketing Engine', target: 'Commerce Engine' },
      { source: 'Commerce Engine', target: 'Products' },
      { source: 'Video Studio', target: 'Products' },
      { source: 'Automations', target: 'Commerce Engine' },
      { source: 'Avatars', target: 'Video Studio' },
      { source: 'Avatars', target: 'Automations' },
    ];

    const width = 600;
    const height = 400;

    // Clear any existing SVG content
    d3.select(ref.current).selectAll('*').remove();

    const svg = d3
      .select(ref.current)
      .attr('viewBox', [0, 0, width, height])
      .style('background', '#0A0F29');

    const simulation = d3
      .forceSimulation(nodes)
      .force(
        'link',
        d3
          .forceLink(links)
          .id((d: any) => d.id)
          .distance(120)
      )
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2));

    const link = svg
      .append('g')
      .attr('stroke', '#FFD700')
      .attr('stroke-opacity', 0.6)
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('stroke-width', 2);

    const node = svg
      .append('g')
      .attr('stroke', '#fff')
      .attr('stroke-width', 1.5)
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', 20)
      .attr('fill', (d) => {
        if (d.group === 'engine') return '#FFD700'; // gold
        if (d.group === 'avatar') return '#C41E3A'; // crimson
        if (d.group === 'automation') return '#1E90FF'; // blue
        return '#32CD32'; // green for products
      })
      .style('cursor', 'pointer')
      .call(drag(simulation) as any);

    const label = svg
      .append('g')
      .selectAll('text')
      .data(nodes)
      .join('text')
      .text((d) => d.id)
      .attr('fill', '#FFFFFF')
      .attr('font-size', 12)
      .attr('text-anchor', 'middle')
      .style('pointer-events', 'none');

    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      node.attr('cx', (d: any) => d.x).attr('cy', (d: any) => d.y);

      label.attr('x', (d: any) => d.x).attr('y', (d: any) => d.y - 25);
    });

    function drag(simulation: d3.Simulation<Node, undefined>) {
      function dragstarted(event: any, d: Node) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      }
      function dragged(event: any, d: Node) {
        d.fx = event.x;
        d.fy = event.y;
      }
      function dragended(event: any, d: Node) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }
      return d3
        .drag<SVGCircleElement, Node>()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended);
    }

    // Cleanup on unmount
    return () => {
      simulation.stop();
    };
  }, []);

  // Highlight current engine based on replay state
  useEffect(() => {
    if (!ref.current || capsules.length === 0) return;

    const svg = d3.select(ref.current);
    const current = capsules[index];

    // Update node appearance based on current replay capsule
    svg.selectAll('circle')
      .attr('stroke', (d: any) => d.id === current.engine ? '#FFD700' : '#fff')
      .attr('stroke-width', (d: any) => d.id === current.engine ? 4 : 1.5)
      .attr('fill', (d: any) => {
        if (d.id === current.engine) {
          // Color based on status
          if (current.status === 'operational') return '#32CD32'; // green
          if (current.status === 'degraded') return '#FFA500'; // orange
          if (current.status === 'failed') return '#FF0000'; // red
        }
        // Default colors by group
        if (d.group === 'engine') return '#FFD700'; // gold
        if (d.group === 'avatar') return '#C41E3A'; // crimson
        if (d.group === 'automation') return '#1E90FF'; // blue
        return '#32CD32'; // green for products
      });
  }, [index, capsules]);

  return (
    <svg
      ref={ref}
      className="w-full h-96 rounded-lg border border-[#FFD700]"
    ></svg>
  );
}
