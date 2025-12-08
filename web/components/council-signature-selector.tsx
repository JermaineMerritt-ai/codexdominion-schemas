'use client';

import { useState, useEffect } from 'react';

interface CouncilSeal {
  member_id: string;
  member_name: string;
  role: string;
  seal_type: string;
  created_at: string;
}

interface CouncilSignatureSelectorProps {
  onSelectionChange: (memberIds: string[]) => void;
  maxSignatures?: number;
}

export default function CouncilSignatureSelector({
  onSelectionChange,
  maxSignatures = 5
}: CouncilSignatureSelectorProps) {
  const [councilSeals, setCouncilSeals] = useState<CouncilSeal[]>([]);
  const [selectedMembers, setSelectedMembers] = useState<Set<string>>(new Set());
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load council seals from backend
  useEffect(() => {
    loadCouncilSeals();
  }, []);

  const loadCouncilSeals = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/api/seal/council-seals');

      if (!response.ok) {
        throw new Error('Failed to load council seals');
      }

      const data = await response.json();
      setCouncilSeals(data.council_seals || []);
    } catch (err) {
      console.error('Error loading council seals:', err);
      setError('Could not load council members. Using sample data.');

      // Fallback to sample data if backend unavailable
      setCouncilSeals([
        {
          member_id: 'council_001',
          member_name: 'Elena Rodriguez',
          role: 'Senior Council',
          seal_type: 'ECC-P256',
          created_at: new Date().toISOString()
        },
        {
          member_id: 'council_002',
          member_name: 'Marcus Chen',
          role: 'Council Observer',
          seal_type: 'RSA-2048',
          created_at: new Date().toISOString()
        },
        {
          member_id: 'council_003',
          member_name: 'Aisha Patel',
          role: 'Technical Council',
          seal_type: 'ECC-P256',
          created_at: new Date().toISOString()
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleMember = (memberId: string) => {
    const newSelected = new Set(selectedMembers);

    if (newSelected.has(memberId)) {
      newSelected.delete(memberId);
    } else {
      if (newSelected.size < maxSignatures) {
        newSelected.add(memberId);
      } else {
        alert(`Maximum ${maxSignatures} council signatures allowed`);
        return;
      }
    }

    setSelectedMembers(newSelected);
    onSelectionChange(Array.from(newSelected));
  };

  const selectAll = () => {
    const allIds = councilSeals.slice(0, maxSignatures).map(s => s.member_id);
    setSelectedMembers(new Set(allIds));
    onSelectionChange(allIds);
  };

  const clearAll = () => {
    setSelectedMembers(new Set());
    onSelectionChange([]);
  };

  const getSealIcon = (sealType: string) => {
    return sealType === 'ECC-P256' ? '🔐' : '🔑';
  };

  if (isLoading) {
    return (
      <div className="bg-[#1A1F3C] p-4 rounded-lg border border-[#FFD700]/30">
        <div className="flex items-center gap-2 text-gray-400">
          <span className="animate-pulse">⏳</span>
          <span>Loading council seals...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-[#1A1F3C] p-4 rounded-lg border-2 border-[#FFD700]/50">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-bold text-[#FFD700]">
          🎭 Council Signatures
        </h3>
        <div className="flex gap-2">
          <button
            onClick={selectAll}
            className="text-xs px-2 py-1 bg-[#FFD700]/20 text-[#FFD700] rounded hover:bg-[#FFD700]/30 transition-colors"
          >
            Select All
          </button>
          <button
            onClick={clearAll}
            className="text-xs px-2 py-1 bg-red-500/20 text-red-400 rounded hover:bg-red-500/30 transition-colors"
          >
            Clear
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-3 text-xs text-yellow-400 bg-yellow-400/10 p-2 rounded">
          ⚠️ {error}
        </div>
      )}

      <p className="text-xs text-gray-400 mb-3">
        Select council members to co-sign this export. Creates a multi-signature covenant.
      </p>

      {councilSeals.length === 0 ? (
        <div className="text-sm text-gray-500 text-center py-4">
          No council members registered yet.
        </div>
      ) : (
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {councilSeals.map((seal) => {
            const isSelected = selectedMembers.has(seal.member_id);

            return (
              <button
                key={seal.member_id}
                onClick={() => toggleMember(seal.member_id)}
                className={`w-full p-3 rounded-lg border-2 transition-all text-left ${
                  isSelected
                    ? 'bg-[#FFD700]/20 border-[#FFD700]'
                    : 'bg-[#0A0F29] border-[#FFD700]/20 hover:border-[#FFD700]/40'
                }`}
              >
                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 text-2xl">
                    {isSelected ? '✅' : getSealIcon(seal.seal_type)}
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className={`font-semibold ${
                        isSelected ? 'text-[#FFD700]' : 'text-white'
                      }`}>
                        {seal.member_name}
                      </span>
                      {isSelected && (
                        <span className="text-xs bg-[#FFD700] text-[#0A0F29] px-2 py-0.5 rounded-full font-bold">
                          SIGNING
                        </span>
                      )}
                    </div>

                    <div className="flex items-center gap-2 mt-1">
                      <span className="text-xs text-gray-400">
                        {seal.role}
                      </span>
                      <span className="text-xs text-gray-500">•</span>
                      <span className="text-xs text-gray-500">
                        {seal.seal_type}
                      </span>
                    </div>

                    <div className="text-xs text-gray-600 mt-1">
                      ID: {seal.member_id}
                    </div>
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      )}

      {selectedMembers.size > 0 && (
        <div className="mt-3 pt-3 border-t border-[#FFD700]/20">
          <div className="text-sm text-gray-300">
            <span className="text-[#FFD700] font-bold">{selectedMembers.size}</span>
            {' '}council member{selectedMembers.size !== 1 ? 's' : ''} will co-sign this export
          </div>
          <div className="text-xs text-gray-500 mt-1">
            Export will contain {selectedMembers.size + 1} cryptographic signatures
            (Custodian + {selectedMembers.size} Council)
          </div>
        </div>
      )}
    </div>
  );
}
