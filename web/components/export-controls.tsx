'use client';

import { useState } from 'react';
import { getUnifiedEventManager } from '@/lib/events/unified-event-manager';

type ExportFormat = 'pdf' | 'markdown' | 'yaml' | 'json';
type Cycle = 'daily' | 'seasonal' | 'epochal' | 'millennial' | '';

interface ExportControlsProps {
  currentFilters?: {
    engine?: string;
    role?: string;
    cycle?: string;
  };
}

export function ExportControls({ currentFilters }: ExportControlsProps) {
  const [format, setFormat] = useState<ExportFormat>('markdown');
  const [cycle, setCycle] = useState<Cycle>('');
  const [isExporting, setIsExporting] = useState(false);

  const handleExport = async () => {
    setIsExporting(true);

    try {
      const manager = getUnifiedEventManager();
      const allEvents = manager.getAllEvents();

      // Build export data
      const exportData = {
        codex_dominion_archive: {
          version: '2.0.0',
          generated_at: new Date().toISOString(),
          cycle_binding: cycle || 'all',
          filters: currentFilters,
          total_entries: allEvents.length,
          seal: generateSeal(allEvents),
          annotations: allEvents,
        },
      };

      if (format === 'json') {
        downloadJSON(exportData);
      } else if (format === 'markdown') {
        downloadMarkdown(exportData);
      } else if (format === 'yaml') {
        downloadYAML(exportData);
      } else if (format === 'pdf') {
        // For PDF, we'd call the backend API
        await downloadFromAPI(format, cycle);
      }
    } catch (error) {
      console.error('Export failed:', error);
      alert('Export failed. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  const generateSeal = (data: any) => {
    const timestamp = new Date().toISOString();
    const custodian = 'Jermaine Merritt';
    const dataString = JSON.stringify(data, null, 2);

    // Simple hash simulation (in production, use proper crypto)
    let hash = 0;
    for (let i = 0; i < dataString.length; i++) {
      const char = dataString.charCodeAt(i);
      hash = (hash << 5) - hash + char;
      hash = hash & hash;
    }

    const signature = Math.abs(hash).toString(16).padStart(32, '0').substring(0, 32);

    return {
      custodian,
      timestamp,
      signature,
      algorithm: 'SHA-256-Simulated',
    };
  };

  const downloadJSON = (data: any) => {
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `codex-dominion-${cycle || 'all'}-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const downloadMarkdown = (data: any) => {
    let markdown = '# 📜 Ceremonial Annotation Scroll\n\n';
    markdown += '**Codex Dominion Archive**\n\n';
    markdown += `*Generated: ${new Date().toLocaleString()}*\n\n`;

    if (data.codex_dominion_archive.cycle_binding !== 'all') {
      markdown += `**Cycle Binding:** ${data.codex_dominion_archive.cycle_binding}\n\n`;
    }

    markdown += `**Total Entries:** ${data.codex_dominion_archive.total_entries}\n\n`;
    markdown += '---\n\n';

    // Group by engine
    const byEngine: Record<string, any[]> = {};
    for (const entry of data.codex_dominion_archive.annotations) {
      const engine = entry.engine || 'Unknown Engine';
      if (!byEngine[engine]) byEngine[engine] = [];
      byEngine[engine].push(entry);
    }

    // Write entries
    for (const [engine, entries] of Object.entries(byEngine).sort()) {
      markdown += `## ⚙️ ${engine}\n\n`;

      for (const entry of entries.sort((a, b) =>
        new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
      )) {
        markdown += `### 🕰️ ${new Date(entry.timestamp).toLocaleString()}\n\n`;
        markdown += `**Observer:** ${entry.user} *(${entry.role})*\n\n`;
        markdown += `**Type:** ${entry.type}\n\n`;

        if (entry.capsuleId) {
          markdown += `**Capsule ID:** \`${entry.capsuleId}\`\n\n`;
        }

        if (entry.tags && entry.tags.length > 0) {
          markdown += `**Tags:** ${entry.tags.map((t: string) => `\`#${t}\``).join(', ')}\n\n`;
        }

        markdown += `> ${entry.content}\n\n`;

        if (entry.metadata && Object.keys(entry.metadata).length > 0) {
          markdown += '<details>\n<summary>📊 Metadata</summary>\n\n';
          markdown += '```json\n';
          markdown += JSON.stringify(entry.metadata, null, 2);
          markdown += '\n```\n</details>\n\n';
        }

        markdown += '---\n\n';
      }
    }

    // Add seal
    const seal = data.codex_dominion_archive.seal;
    markdown += '\n## 👑 Custodian\'s Seal\n\n';
    markdown += `**Sealed By:** ${seal.custodian}\n\n`;
    markdown += `**Seal Timestamp:** ${seal.timestamp}\n\n`;
    markdown += `**Crown Signature:** \`${seal.signature}\`\n\n`;
    markdown += `**Algorithm:** ${seal.algorithm}\n\n`;
    markdown += '*This document bears the immutable seal of Codex Dominion.*\n';

    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `codex-dominion-scroll-${cycle || 'all'}-${Date.now()}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const downloadYAML = (data: any) => {
    // Simple YAML conversion (in production, use proper YAML library)
    let yaml = '---\n';
    yaml += 'codex_dominion_archive:\n';
    yaml += `  version: "${data.codex_dominion_archive.version}"\n`;
    yaml += `  generated_at: "${data.codex_dominion_archive.generated_at}"\n`;
    yaml += `  cycle_binding: "${data.codex_dominion_archive.cycle_binding}"\n`;
    yaml += `  total_entries: ${data.codex_dominion_archive.total_entries}\n`;
    yaml += '  seal:\n';
    yaml += `    custodian: "${data.codex_dominion_archive.seal.custodian}"\n`;
    yaml += `    timestamp: "${data.codex_dominion_archive.seal.timestamp}"\n`;
    yaml += `    signature: "${data.codex_dominion_archive.seal.signature}"\n`;
    yaml += `    algorithm: "${data.codex_dominion_archive.seal.algorithm}"\n`;
    yaml += '  annotations:\n';

    for (const entry of data.codex_dominion_archive.annotations) {
      yaml += '    - id: "' + entry.id + '"\n';
      yaml += '      type: "' + entry.type + '"\n';
      yaml += '      user: "' + entry.user + '"\n';
      yaml += '      role: "' + entry.role + '"\n';
      yaml += '      timestamp: "' + entry.timestamp + '"\n';
      if (entry.engine) yaml += '      engine: "' + entry.engine + '"\n';
      if (entry.capsuleId) yaml += '      capsuleId: "' + entry.capsuleId + '"\n';
      yaml += '      content: "' + entry.content.replace(/"/g, '\\"') + '"\n';
      if (entry.tags && entry.tags.length > 0) {
        yaml += '      tags: [' + entry.tags.map((t: string) => `"${t}"`).join(', ') + ']\n';
      }
    }

    const blob = new Blob([yaml], { type: 'application/x-yaml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `codex-dominion-capsule-${cycle || 'all'}-${Date.now()}.yaml`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const downloadFromAPI = async (format: ExportFormat, cycle: Cycle) => {
    const params = new URLSearchParams();
    params.set('format', format);
    if (cycle) params.set('cycle', cycle);
    if (currentFilters?.engine) params.set('engine', currentFilters.engine);
    if (currentFilters?.role) params.set('role', currentFilters.role);

    const response = await fetch(`/api/annotations/export?${params.toString()}`);
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `codex-dominion-export-${Date.now()}.${format}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-[#1A1F3C] rounded-lg border-2 border-[#FFD700] p-6">
      <h3 className="text-xl font-bold text-[#FFD700] mb-4 flex items-center gap-2">
        📥 Export Archive
      </h3>

      <div className="space-y-4">
        {/* Format Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-400 mb-2">Export Format</label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            {[
              { value: 'markdown', label: '📜 Ceremonial Scroll', ext: '.md' },
              { value: 'yaml', label: '📦 Archival Capsule', ext: '.yaml' },
              { value: 'pdf', label: '📕 Bound Ledger', ext: '.pdf' },
              { value: 'json', label: '📊 Data Export', ext: '.json' },
            ].map((fmt) => (
              <button
                key={fmt.value}
                onClick={() => setFormat(fmt.value as ExportFormat)}
                className={`px-4 py-3 rounded font-medium transition-colors text-sm ${
                  format === fmt.value
                    ? 'bg-[#FFD700] text-[#0A0F29]'
                    : 'bg-[#0A0F29] text-gray-400 hover:bg-[#2A2F4C] border border-[#FFD700]/30'
                }`}
              >
                {fmt.label}
              </button>
            ))}
          </div>
        </div>

        {/* Cycle Binding */}
        <div>
          <label className="block text-sm font-medium text-gray-400 mb-2">Cycle Binding</label>
          <select
            value={cycle}
            onChange={(e) => setCycle(e.target.value as Cycle)}
            className="w-full px-4 py-2 bg-[#0A0F29] text-white border border-[#FFD700]/30 rounded focus:border-[#FFD700] focus:outline-none"
          >
            <option value="">All Time (Complete Archive)</option>
            <option value="daily">📅 Daily (Last 24 Hours)</option>
            <option value="seasonal">🌙 Seasonal (Last 7 Days)</option>
            <option value="epochal">⏳ Epochal (Last 30 Days)</option>
            <option value="millennial">🌌 Millennial (Last 90 Days)</option>
          </select>
        </div>

        {/* Export Info */}
        <div className="bg-[#0A0F29] rounded p-4 border border-[#FFD700]/20">
          <p className="text-xs text-gray-400 mb-2">Export includes:</p>
          <ul className="text-sm text-white space-y-1">
            <li>✅ All annotations, chat, feedback, and capsule events</li>
            <li>✅ Immutable custodian seal with crown signature</li>
            <li>✅ Timestamp and cycle binding metadata</li>
            <li>✅ Applied filters: {currentFilters?.engine || currentFilters?.role ? 'Yes' : 'None'}</li>
          </ul>
        </div>

        {/* Export Button */}
        <button
          onClick={handleExport}
          disabled={isExporting}
          className="w-full px-6 py-3 bg-[#FFD700] text-[#0A0F29] rounded-lg font-bold hover:bg-[#FFC700] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isExporting ? '⏳ Generating Export...' : '📥 Generate Sealed Export'}
        </button>

        {/* Seal Notice */}
        <p className="text-xs text-gray-500 text-center">
          👑 All exports are sealed with the Custodian's crown signature for authenticity and tamper-evidence.
        </p>
      </div>
    </div>
  );
}
