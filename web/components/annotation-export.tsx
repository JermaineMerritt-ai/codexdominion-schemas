'use client';

import { useState } from 'react';
import CouncilSignatureSelector from './council-signature-selector';

interface AnnotationExportProps {
  cycle?: string;
  engine?: string;
  role?: string;
}

export default function AnnotationExport({ cycle, engine, role }: AnnotationExportProps) {
  const [isExporting, setIsExporting] = useState<string | null>(null);
  const [includeCouncil, setIncludeCouncil] = useState(false);
  const [selectedCouncilMembers, setSelectedCouncilMembers] = useState<string[]>([]);

  const exportFile = async (format: 'pdf' | 'markdown' | 'yaml') => {
    setIsExporting(format);

    try {
      // Build query parameters
      const params = new URLSearchParams();
      params.set('format', format);
      if (cycle) params.set('cycle', cycle);
      if (engine) params.set('engine', engine);
      if (role) params.set('role', role);

      // Add council signatures if selected
      if (includeCouncil && selectedCouncilMembers.length > 0) {
        params.set('include_council', 'true');
        params.set('council_members', selectedCouncilMembers.join(','));
      }

      // Open export in new tab
      window.open(`/api/annotations/export?${params.toString()}`, '_blank');

      // Reset after short delay
      setTimeout(() => setIsExporting(null), 1000);
    } catch (error) {
      console.error('Export failed:', error);
      setIsExporting(null);
      alert('Export failed. Please try again.');
    }
  };

  return (
    <div className="space-y-4">
      <div className="bg-[#1A1F3C] p-6 rounded-lg border-2 border-[#FFD700]">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-[#FFD700]">📜 Ritual Print & Export</h2>
          {(cycle || engine || role) && (
            <span className="text-xs text-gray-400">
              Filters applied: {[cycle, engine, role].filter(Boolean).join(', ')}
            </span>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <button
            onClick={() => exportFile('pdf')}
            disabled={isExporting === 'pdf'}
            className="flex flex-col items-center gap-2 px-6 py-4 bg-[#FFD700] text-[#0A0F29] rounded-lg font-bold hover:bg-[#FFC700] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span className="text-3xl">📕</span>
            <span className="text-sm">
              {isExporting === 'pdf' ? 'Generating...' : 'Export PDF Ledger'}
            </span>
            <span className="text-xs opacity-70">Bound ceremonial document</span>
          </button>

          <button
            onClick={() => exportFile('markdown')}
            disabled={isExporting === 'markdown'}
            className="flex flex-col items-center gap-2 px-6 py-4 bg-[#FFD700] text-[#0A0F29] rounded-lg font-bold hover:bg-[#FFC700] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span className="text-3xl">📜</span>
            <span className="text-sm">
              {isExporting === 'markdown' ? 'Generating...' : 'Export Scroll'}
            </span>
            <span className="text-xs opacity-70">Markdown format (.md)</span>
          </button>

          <button
            onClick={() => exportFile('yaml')}
            disabled={isExporting === 'yaml'}
            className="flex flex-col items-center gap-2 px-6 py-4 bg-[#FFD700] text-[#0A0F29] rounded-lg font-bold hover:bg-[#FFC700] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span className="text-3xl">🔐</span>
            <span className="text-sm">
              {isExporting === 'yaml' ? 'Generating...' : 'Export Capsule'}
            </span>
            <span className="text-xs opacity-70">YAML archive (.yaml)</span>
          </button>
        </div>

        <div className="mt-4 bg-[#0A0F29] rounded p-4 border border-[#FFD700]/20">
          <p className="text-xs text-gray-400 mb-2">All exports include:</p>
          <ul className="text-xs text-gray-300 space-y-1">
            <li>✅ Immutable custodian seal with crown signature</li>
            <li>✅ Timestamp and cycle binding metadata</li>
            <li>✅ Complete annotation, chat, feedback & capsule events</li>
            <li>✅ SHA-256 cryptographic verification</li>
            {includeCouncil && selectedCouncilMembers.length > 0 && (
              <li className="text-[#FFD700] font-bold">
                ✅ Multi-signature covenant ({selectedCouncilMembers.length} council seals)
              </li>
            )}
          </ul>
        </div>

        <p className="text-xs text-gray-500 text-center mt-3">
          👑 Sealed by Jermaine Merritt, Custodian of Codex Dominion
        </p>
      </div>

      {/* Multi-Signature Toggle */}
      <div className="bg-[#1A1F3C] p-4 rounded-lg border-2 border-[#FFD700]/50">
        <label className="flex items-center gap-3 cursor-pointer">
          <input
            type="checkbox"
            checked={includeCouncil}
            onChange={(e) => {
              setIncludeCouncil(e.target.checked);
              if (!e.target.checked) {
                setSelectedCouncilMembers([]);
              }
            }}
            className="w-5 h-5 rounded border-2 border-[#FFD700] bg-[#0A0F29] checked:bg-[#FFD700] focus:ring-2 focus:ring-[#FFD700] focus:ring-offset-2 focus:ring-offset-[#1A1F3C] transition-colors"
          />
          <div>
            <span className="text-white font-semibold">
              Include Council Signatures
            </span>
            <p className="text-xs text-gray-400">
              Create multi-signature covenant with council member seals
            </p>
          </div>
        </label>
      </div>

      {/* Council Signature Selector */}
      {includeCouncil && (
        <CouncilSignatureSelector
          onSelectionChange={setSelectedCouncilMembers}
          maxSignatures={5}
        />
      )}
    </div>
  );
}
