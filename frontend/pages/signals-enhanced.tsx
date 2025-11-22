// pages/signals-enhanced.tsx
import { useEffect, useState } from 'react';
import { SignalsCard } from '../components/SignalsCard';
import { TierSummary } from '../components/TierSummary';
import { useCodexSignals, SignalsSnapshot } from '../utils/api';

export default function SignalsEnhancedPage() {
  const [snapshot, setSnapshot] = useState<SignalsSnapshot | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Replace with your actual Cloud Run URL
  const API_URL = "https://codex-signals-<HASH>.run.app";
  const { api, utils } = useCodexSignals(API_URL);

  useEffect(() => {
    async function loadSignals() {
      try {
        setLoading(true);
        setError(null);
        
        // Try to get mock signals first (no auth required)
        const snapshot = await api.getMockSignals();
        setSnapshot(snapshot);
        
      } catch (err) {
        console.error('Error loading signals:', err);
        setError(err instanceof Error ? err.message : 'Failed to load signals');
      } finally {
        setLoading(false);
      }
    }

    loadSignals();
  }, []);

  const handleGenerateDaily = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Sample market data and positions
      const marketData = [
        { symbol: "MSFT", price: 420.1, vol_30d: 0.22, trend_20d: 0.48, liquidity_rank: 5 },
        { symbol: "AAPL", price: 185.0, vol_30d: 0.28, trend_20d: 0.15, liquidity_rank: 3 },
        { symbol: "GOOGL", price: 140.5, vol_30d: 0.31, trend_20d: -0.05, liquidity_rank: 8 },
        { symbol: "ETH-USD", price: 3500.0, vol_30d: 0.40, trend_20d: 0.30, liquidity_rank: 15 },
        { symbol: "BTC-USD", price: 67000.0, vol_30d: 0.38, trend_20d: 0.42, liquidity_rank: 10 }
      ];
      
      const positions = [
        { symbol: "MSFT", weight: 0.04, allowed_max: 0.08 },
        { symbol: "AAPL", weight: 0.03, allowed_max: 0.06 },
        { symbol: "ETH-USD", weight: 0.02, allowed_max: 0.06 },
        { symbol: "BTC-USD", weight: 0.015, allowed_max: 0.05 }
      ];
      
      const snapshot = await api.generateDailySignals(marketData, positions);
      setSnapshot(snapshot);
      
    } catch (err) {
      console.error('Error generating signals:', err);
      setError(err instanceof Error ? err.message : 'Failed to generate signals');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadBulletin = async () => {
    try {
      const bulletin = await api.generateBulletin('md');
      
      // Create and download file
      const blob = new Blob([bulletin.content], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `codex-signals-${new Date().toISOString().split('T')[0]}.md`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
    } catch (err) {
      console.error('Error downloading bulletin:', err);
      setError(err instanceof Error ? err.message : 'Failed to download bulletin');
    }
  };

  if (loading) {
    return (
      <div style={{ 
        padding: '24px', 
        textAlign: 'center',
        minHeight: '200px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <div>
          <div style={{ fontSize: '24px', marginBottom: '16px' }}>🔄</div>
          <div>Loading Codex Signals...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '24px' }}>
        <div style={{
          backgroundColor: '#fef2f2',
          border: '1px solid #fecaca',
          borderRadius: '8px',
          padding: '16px',
          color: '#dc2626'
        }}>
          <strong>Error:</strong> {error}
          <button 
            onClick={() => window.location.reload()}
            style={{
              marginLeft: '12px',
              padding: '4px 8px',
              backgroundColor: '#dc2626',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1 style={{ margin: 0, fontSize: '32px' }}>🔥 Codex Signals Dashboard</h1>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button
            onClick={handleGenerateDaily}
            style={{
              padding: '12px 24px',
              backgroundColor: '#3b82f6',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
          >
            Generate Daily Signals
          </button>
          <button
            onClick={handleDownloadBulletin}
            disabled={!snapshot}
            style={{
              padding: '12px 24px',
              backgroundColor: snapshot ? '#10b981' : '#9ca3af',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: snapshot ? 'pointer' : 'not-allowed',
              fontWeight: 'bold'
            }}
          >
            Download Bulletin
          </button>
        </div>
      </div>

      {snapshot && (
        <>
          {/* Tier Summary */}
          <TierSummary 
            tierCounts={snapshot.tier_counts}
            generatedAt={snapshot.generated_at}
            banner={snapshot.banner}
          />

          {/* Portfolio Metrics */}
          <div style={{
            backgroundColor: '#f9fafb',
            padding: '20px',
            borderRadius: '8px',
            marginBottom: '24px',
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '16px'
          }}>
            <div>
              <strong>Total Positions:</strong> {snapshot.picks.length}
            </div>
            <div>
              <strong>Total Allocation:</strong> {utils.formatWeight(utils.calculateTotalAllocation(snapshot.picks))}
            </div>
            <div>
              <strong>High Conviction:</strong> {snapshot.tier_counts.Alpha} Alpha picks
            </div>
            <div>
              <strong>Risk Positions:</strong> {snapshot.tier_counts.Delta} Delta positions
            </div>
          </div>

          {/* Signals Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '16px' }}>
            {snapshot.picks.map((pick, index) => (
              <SignalsCard key={`${pick.symbol}-${index}`} pick={pick} />
            ))}
          </div>

          {/* Footer */}
          <div style={{
            marginTop: '32px',
            textAlign: 'center',
            padding: '16px',
            backgroundColor: '#1f2937',
            color: 'white',
            borderRadius: '8px'
          }}>
            <div style={{ fontSize: '14px', opacity: 0.8 }}>
              Generated by <strong>The Merritt Method™</strong> | Codex Dominion Portfolio Intelligence
            </div>
            <div style={{ fontSize: '12px', opacity: 0.6, marginTop: '4px' }}>
              🔥 Digital Sovereignty • 📊 Quantitative Finance • 👑 Elite Performance
            </div>
          </div>
        </>
      )}
    </div>
  );
}