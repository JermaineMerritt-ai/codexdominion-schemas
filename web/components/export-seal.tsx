'use client';

interface Signature {
  signer: string;
  name: string;
  role: string;
  signature: string;
  algorithm: string;
  timestamp: string;
  member_id?: string;
}

interface ExportSealProps {
  seals: Signature[];
  contentHash?: string;
  timestamp?: string;
  covenantType?: string;
}

export default function ExportSeal({
  seals,
  contentHash,
  timestamp,
  covenantType
}: ExportSealProps) {
  const getSealIcon = (algorithm: string) => {
    if (algorithm.includes('ECC') || algorithm.includes('ECDSA')) {
      return '🔐'; // ECC signature
    } else if (algorithm.includes('RSA')) {
      return '🔑'; // RSA signature
    } else {
      return '🔒'; // Generic seal
    }
  };

  const getRoleBadge = (role: string) => {
    const roleColors: Record<string, string> = {
      'Sovereign Custodian': 'bg-[#FFD700] text-[#0A0F29]',
      'Senior Council': 'bg-purple-600 text-white',
      'Council Observer': 'bg-blue-600 text-white',
      'Technical Council': 'bg-green-600 text-white',
      'Commerce Council': 'bg-orange-600 text-white',
      'Marketing Council': 'bg-pink-600 text-white'
    };

    return roleColors[role] || 'bg-gray-600 text-white';
  };

  const formatTimestamp = (ts: string) => {
    try {
      return new Date(ts).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZone: 'UTC',
        timeZoneName: 'short'
      });
    } catch {
      return ts;
    }
  };

  return (
    <div className="bg-[#1A1F3C] p-6 rounded-lg border-2 border-[#FFD700]">
      <div className="flex items-center gap-2 mb-4">
        <span className="text-3xl">👑</span>
        <div>
          <h2 className="text-xl font-bold text-[#FFD700]">
            Cryptographic Seals
          </h2>
          {covenantType && (
            <p className="text-xs text-gray-400">
              {covenantType === 'multi-signature'
                ? `Multi-Signature Covenant (${seals.length} seals)`
                : 'Single Custodian Seal'}
            </p>
          )}
        </div>
      </div>

      {/* Seal Metadata */}
      {(contentHash || timestamp) && (
        <div className="mb-4 p-3 bg-[#0A0F29] rounded border border-[#FFD700]/20">
          {contentHash && (
            <div className="flex items-start gap-2 mb-2">
              <span className="text-xs text-gray-500 font-mono">Hash:</span>
              <span className="text-xs text-gray-300 font-mono break-all">
                {contentHash}
              </span>
            </div>
          )}
          {timestamp && (
            <div className="flex items-start gap-2">
              <span className="text-xs text-gray-500">Sealed:</span>
              <span className="text-xs text-gray-300">
                {formatTimestamp(timestamp)}
              </span>
            </div>
          )}
        </div>
      )}

      {/* Seal List */}
      <ul className="space-y-3">
        {seals.map((seal, idx) => (
          <li
            key={idx}
            className="p-3 bg-[#0A0F29] rounded-lg border border-[#FFD700]/30 hover:border-[#FFD700]/50 transition-colors"
          >
            <div className="flex items-start gap-3">
              <span className="text-2xl flex-shrink-0 mt-1">
                {getSealIcon(seal.algorithm)}
              </span>

              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-bold text-white">
                    {seal.name}
                  </span>
                  <span className={`text-xs px-2 py-0.5 rounded-full ${getRoleBadge(seal.role)}`}>
                    {seal.role}
                  </span>
                </div>

                <div className="text-xs text-gray-400 mb-2">
                  {seal.algorithm}
                </div>

                <div className="bg-[#1A1F3C] p-2 rounded border border-[#FFD700]/10">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs text-gray-500">Signature:</span>
                    <button
                      onClick={() => {
                        navigator.clipboard.writeText(seal.signature);
                        // Optional: Show toast notification
                      }}
                      className="text-xs text-[#FFD700] hover:underline"
                      title="Copy full signature"
                    >
                      Copy
                    </button>
                  </div>
                  <code className="text-xs text-gray-300 font-mono break-all block">
                    {seal.signature.slice(0, 64)}...
                  </code>
                </div>

                <div className="text-xs text-gray-500 mt-2">
                  Signed: {formatTimestamp(seal.timestamp)}
                </div>
              </div>
            </div>
          </li>
        ))}
      </ul>

      {/* Footer */}
      <div className="mt-4 pt-4 border-t border-[#FFD700]/20">
        <div className="flex items-start gap-2">
          <span className="text-sm">🛡️</span>
          <div>
            <p className="text-xs text-gray-300 mb-1">
              <strong className="text-[#FFD700]">Cryptographically Sealed:</strong>
              {' '}Each seal is cryptographically bound to the export content using SHA-256 hashing and RSA-2048/ECC-P256 signatures.
            </p>
            <p className="text-xs text-gray-400">
              These seals ensure authenticity, tamper-evidence, and eternal validity.
              Any modification to the export content will invalidate all signatures.
            </p>
          </div>
        </div>
      </div>

      {/* Verification Info */}
      {contentHash && (
        <div className="mt-3 p-3 bg-[#FFD700]/10 rounded border border-[#FFD700]/30">
          <div className="flex items-center gap-2 text-xs">
            <span>🔍</span>
            <span className="text-gray-300">
              Verify this export at:{' '}
              <a
                href={`https://codexdominion.app/api/seal/verify/${contentHash}`}
                className="text-[#FFD700] hover:underline font-mono"
                target="_blank"
                rel="noopener noreferrer"
              >
                /api/seal/verify/{contentHash.slice(0, 16)}...
              </a>
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
