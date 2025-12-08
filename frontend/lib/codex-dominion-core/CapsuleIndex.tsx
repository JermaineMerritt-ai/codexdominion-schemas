// CapsuleIndex - Searchable capsule archive
import React, { useState, useEffect } from 'react';
import type { Capsule } from './types';

interface CapsuleIndexProps {
  onCapsuleSelect?: (capsule: Capsule) => void;
}

export const CapsuleIndex: React.FC<CapsuleIndexProps> = ({ onCapsuleSelect }) => {
  const [capsules, setCapsules] = useState<Capsule[]>([]);
  const [filteredCapsules, setFilteredCapsules] = useState<Capsule[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [searchField, setSearchField] = useState<'steward' | 'cycle' | 'engine' | 'seal'>('steward');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Load capsules
    const loadCapsules = async () => {
      setIsLoading(true);

      // Mock data
      const mockCapsules: Capsule[] = [
        {
          id: 'capsule-001',
          steward: 'Alpha Steward',
          cycle: 'Q1-2024',
          engine: 'ProfitEngine-Alpha',
          seal: 'seal-001',
          timestamp: new Date('2024-01-15T10:30:00'),
        },
        {
          id: 'capsule-002',
          steward: 'Beta Steward',
          cycle: 'Q2-2024',
          engine: 'ProfitEngine-Beta',
          seal: 'seal-002',
          timestamp: new Date('2024-02-20T14:45:00'),
        },
        {
          id: 'capsule-003',
          steward: 'Gamma Steward',
          cycle: 'Q3-2024',
          engine: 'ProfitEngine-Gamma',
          seal: 'seal-003',
          timestamp: new Date('2024-03-10T08:15:00'),
        },
      ];

      setCapsules(mockCapsules);
      setFilteredCapsules(mockCapsules);
      setIsLoading(false);
    };

    loadCapsules();
  }, []);

  useEffect(() => {
    // Filter capsules based on search
    if (!searchTerm) {
      setFilteredCapsules(capsules);
      return;
    }

    const filtered = capsules.filter((capsule) =>
      capsule[searchField].toLowerCase().includes(searchTerm.toLowerCase())
    );

    setFilteredCapsules(filtered);
  }, [searchTerm, searchField, capsules]);

  const handleCapsuleClick = (capsule: Capsule) => {
    if (onCapsuleSelect) {
      onCapsuleSelect(capsule);
    }
  };

  return (
    <div className="capsule-index">
      <header className="index-header">
        <h2>📦 Capsule Index</h2>
        <span className="capsule-count">{filteredCapsules.length} of {capsules.length} capsules</span>
      </header>

      <div className="search-panel">
        <select
          value={searchField}
          onChange={(e) => setSearchField(e.target.value as typeof searchField)}
          className="field-selector"
        >
          <option value="steward">Steward</option>
          <option value="cycle">Cycle</option>
          <option value="engine">Engine</option>
          <option value="seal">Seal</option>
        </select>

        <input
          type="text"
          placeholder={`Search by ${searchField}...`}
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>

      {isLoading ? (
        <div className="loading">Loading capsules...</div>
      ) : (
        <div className="capsule-list">
          {filteredCapsules.length === 0 ? (
            <p className="empty-state">No capsules found</p>
          ) : (
            <table className="capsule-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Steward</th>
                  <th>Cycle</th>
                  <th>Engine</th>
                  <th>Seal</th>
                  <th>Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {filteredCapsules.map((capsule) => (
                  <tr
                    key={capsule.id}
                    onClick={() => handleCapsuleClick(capsule)}
                    className="capsule-row"
                  >
                    <td>{capsule.id}</td>
                    <td>{capsule.steward}</td>
                    <td>{capsule.cycle}</td>
                    <td>{capsule.engine}</td>
                    <td>{capsule.seal}</td>
                    <td>{capsule.timestamp.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
};
