// ProfitEngine - Echo-driven profit tracking and analytics
import React, { useState, useEffect } from 'react';
import type { EchoConfig } from './types';

interface ProfitEngineProps {
  echoWith?: EchoConfig;
  onProfitUpdate?: (totalProfit: number) => void;
}

interface ProfitRecord {
  id: string;
  amount: number;
  source: string;
  timestamp: Date;
  echoId?: string;
}

export const ProfitEngine: React.FC<ProfitEngineProps> = ({ echoWith, onProfitUpdate }) => {
  const [profits, setProfits] = useState<ProfitRecord[]>([]);
  const [totalProfit, setTotalProfit] = useState(0);
  const [isTracking, setIsTracking] = useState(false);

  useEffect(() => {
    // Load profit records
    const loadProfits = async () => {
      // Mock data
      const mockProfits: ProfitRecord[] = [
        {
          id: 'profit-001',
          amount: 1500,
          source: 'Echo Channel Alpha',
          timestamp: new Date(),
          echoId: echoWith?.echoChannelId,
        },
        {
          id: 'profit-002',
          amount: 2300,
          source: 'Echo Channel Beta',
          timestamp: new Date(Date.now() - 86400000),
          echoId: echoWith?.echoChannelId,
        },
      ];
      setProfits(mockProfits);

      const total = mockProfits.reduce((sum, p) => sum + p.amount, 0);
      setTotalProfit(total);

      if (onProfitUpdate) {
        onProfitUpdate(total);
      }
    };

    loadProfits();
  }, [echoWith, onProfitUpdate]);

  const startTracking = () => {
    setIsTracking(true);
    // Start echo tracking
  };

  const stopTracking = () => {
    setIsTracking(false);
  };

  return (
    <div className="profit-engine">
      <header className="engine-header">
        <h2>💰 Profit Engine</h2>
        {echoWith && (
          <span className="echo-status">
            🔊 Echo: {echoWith.echoChannelId} @ {echoWith.echoFrequency}Hz
          </span>
        )}
      </header>

      <div className="profit-overview">
        <div className="total-profit">
          <span className="label">Total Profit</span>
          <span className="amount">${totalProfit.toLocaleString()}</span>
        </div>

        <div className="tracking-control">
          {isTracking ? (
            <button onClick={stopTracking} className="btn-stop">Stop Tracking</button>
          ) : (
            <button onClick={startTracking} className="btn-start">Start Tracking</button>
          )}
        </div>
      </div>

      <div className="profit-records">
        <h3>Recent Profit Records</h3>
        {profits.length === 0 ? (
          <p className="empty-state">No profit records yet</p>
        ) : (
          <table className="profit-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Amount</th>
                <th>Source</th>
                <th>Echo ID</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {profits.map((profit) => (
                <tr key={profit.id}>
                  <td>{profit.id}</td>
                  <td className="amount">${profit.amount.toLocaleString()}</td>
                  <td>{profit.source}</td>
                  <td>{profit.echoId || 'N/A'}</td>
                  <td>{profit.timestamp.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};
