"""
🔥 CODEX SIGNALS INTEGRATION 📊
Integration with Codex Dominion systems

The Merritt Method™ - Unified Financial Intelligence
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import logging

from .engine import SignalsEngine, MarketSnapshot, Position
from .data_feeds import MockDataFeed, DataFeedManager

def bulletin_md(snapshot: dict) -> str:
    """
    Generate Markdown bulletin from signals snapshot
    Perfect for sharing, documentation, or publishing
    """
    header = f"# Daily Signals — {snapshot['generated_at']}\n\n"
    banner = f"> {snapshot['banner']}\n\n"
    tiers = snapshot["tier_counts"]
    counts = f"- Alpha: {tiers['Alpha']}\n- Beta: {tiers['Beta']}\n- Gamma: {tiers['Gamma']}\n- Delta: {tiers['Delta']}\n\n"
    body = []
    for p in snapshot["picks"]:
        line = f"**{p['symbol']}** — Tier {p['tier']} | target {p['target_weight']:.2%}\n- Rationale: {p['rationale']}\n- Risks: {', '.join(p['risk_factors']) or 'None'}\n"
        body.append(line + "\n")
    return header + banner + counts + "".join(body)

class CodexSignalsIntegration:
    """
    Integration layer for Codex Signals with main Codex Dominion systems
    """
    
    def __init__(self, config_dir: str = "."):
        self.config_dir = config_dir
        self.engine = SignalsEngine()
        self.data_feed = DataFeedManager()
        self.logger = logging.getLogger(__name__)
        
        # File paths
        self.signals_file = os.path.join(config_dir, "codex_signals.json")
        self.positions_file = os.path.join(config_dir, "portfolio_positions.json")
        self.signals_history_file = os.path.join(config_dir, "signals_history.json")
    
    def load_positions_from_ledger(self) -> Dict[str, Position]:
        """Load positions from Codex ledger system"""
        try:
            ledger_file = os.path.join(self.config_dir, "codex_ledger.json")
            
            if os.path.exists(ledger_file):
                with open(ledger_file, 'r') as f:
                    ledger_data = json.load(f)
                
                # Extract portfolio positions from ledger
                positions = {}
                
                # Look for treasury/investment data in ledger
                if isinstance(ledger_data, dict):
                    treasury_data = ledger_data.get('treasury', {})
                    investments = treasury_data.get('investments', {})
                    
                    for symbol, data in investments.items():
                        if isinstance(data, dict):
                            weight = data.get('weight', 0.0)
                            max_weight = data.get('max_weight', 0.10)
                            
                            positions[symbol] = Position(
                                symbol=symbol,
                                weight=weight,
                                allowed_max=max_weight
                            )
            
            # If no positions found, return defaults
            if not positions:
                return self._get_default_positions()
            
            return positions
            
        except Exception as e:
            self.logger.error(f"Error loading positions from ledger: {e}")
            return self._get_default_positions()
    
    def _get_default_positions(self) -> Dict[str, Position]:
        """Get default portfolio positions"""
        return {
            "MSFT": Position(symbol="MSFT", weight=0.04, allowed_max=0.08),
            "AAPL": Position(symbol="AAPL", weight=0.03, allowed_max=0.06),
            "BTC-USD": Position(symbol="BTC-USD", weight=0.02, allowed_max=0.06),
            "ETH-USD": Position(symbol="ETH-USD", weight=0.015, allowed_max=0.05),
        }
    
    def save_positions(self, positions: Dict[str, Position]) -> bool:
        """Save positions to file"""
        try:
            positions_data = {
                symbol: {
                    'weight': pos.weight,
                    'allowed_max': pos.allowed_max,
                    'last_updated': datetime.utcnow().isoformat()
                }
                for symbol, pos in positions.items()
            }
            
            with open(self.positions_file, 'w') as f:
                json.dump(positions_data, f, indent=2)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving positions: {e}")
            return False
    
    def generate_signals_report(self, use_live_data: bool = False) -> Dict:
        """Generate comprehensive signals report"""
        try:
            # Load market data
            if use_live_data:
                snapshots = self.data_feed.get_market_snapshots()
            else:
                snapshots = MockDataFeed.get_mock_snapshots()
            
            # Load positions
            positions = self.load_positions_from_ledger()
            
            # Generate signals
            signals_snapshot = self.engine.generate(snapshots, positions)
            
            # Enhanced report with additional context
            enhanced_report = {
                **signals_snapshot,
                'codex_integration': {
                    'version': '1.0.0',
                    'data_source': 'live' if use_live_data else 'mock',
                    'positions_loaded': len(positions),
                    'snapshots_processed': len(snapshots),
                    'integration_timestamp': datetime.utcnow().isoformat()
                },
                'market_summary': {
                    'total_symbols': len(snapshots),
                    'avg_volatility': sum(s.vol_30d for s in snapshots) / len(snapshots),
                    'avg_trend': sum(s.trend_20d for s in snapshots) / len(snapshots),
                    'high_liquidity_count': sum(1 for s in snapshots if s.liquidity_rank <= 50)
                }
            }
            
            return enhanced_report
            
        except Exception as e:
            self.logger.error(f"Error generating signals report: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat(),
                'success': False
            }
    
    def save_signals_snapshot(self, snapshot: Dict) -> bool:
        """Save signals snapshot to file"""
        try:
            with open(self.signals_file, 'w') as f:
                json.dump(snapshot, f, indent=2)
            
            # Also append to history
            self._append_to_history(snapshot)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving signals snapshot: {e}")
            return False
    
    def _append_to_history(self, snapshot: Dict) -> bool:
        """Append snapshot to signals history"""
        try:
            history = []
            
            # Load existing history
            if os.path.exists(self.signals_history_file):
                with open(self.signals_history_file, 'r') as f:
                    history = json.load(f)
            
            # Add new snapshot
            history.append({
                'timestamp': snapshot.get('generated_at', datetime.utcnow().isoformat()),
                'tier_counts': snapshot.get('tier_counts', {}),
                'total_picks': len(snapshot.get('picks', [])),
                'banner': snapshot.get('banner', ''),
                'snapshot_id': datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            })
            
            # Keep only last 30 days
            cutoff = datetime.utcnow()
            history = [h for h in history[-100:]]  # Keep last 100 entries
            
            # Save updated history
            with open(self.signals_history_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error appending to history: {e}")
            return False
    
    def get_signals_for_dawn_dispatch(self) -> Dict:
        """Get signals summary for dawn dispatch integration"""
        try:
            snapshot = self.generate_signals_report()
            
            if 'error' in snapshot:
                return {
                    'signals_status': 'ERROR',
                    'error': snapshot['error']
                }
            
            # Create summary for dawn dispatch
            tier_counts = snapshot.get('tier_counts', {})
            picks = snapshot.get('picks', [])
            
            active_positions = len([p for p in picks if p['target_weight'] > 0])
            total_allocated = sum(p['target_weight'] for p in picks)
            
            signals_summary = {
                'signals_status': 'OPERATIONAL',
                'timestamp': snapshot.get('generated_at'),
                'tier_distribution': tier_counts,
                'active_positions': active_positions,
                'total_allocated_weight': f"{total_allocated*100:.1f}%",
                'high_conviction_picks': len([p for p in picks if p['tier'] == 'Alpha']),
                'risk_factors_detected': sum(len(p['risk_factors']) for p in picks),
                'banner': snapshot.get('banner', '')
            }
            
            return signals_summary
            
        except Exception as e:
            self.logger.error(f"Error getting signals for dawn dispatch: {e}")
            return {
                'signals_status': 'ERROR',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def save_bulletin(self, snapshot: Dict, filename: str = None, format: str = "txt") -> str:
        """Save signals as bulletin for sharing - supports txt and md formats"""
        try:
            if not filename:
                if 'generated_at' in snapshot:
                    # Clean the timestamp for filename (remove colons and other invalid chars)
                    timestamp = snapshot['generated_at'].replace(':', '').replace('-', '').replace('T', '_').split('.')[0]
                    date_str = timestamp[:8]  # YYYYMMDD
                else:
                    date_str = datetime.utcnow().strftime('%Y%m%d')
                ext = "md" if format == "md" else "txt"
                filename = f"signals_bulletin_{date_str}.{ext}"
                
            path = os.path.join(self.config_dir, filename)
            
            if format == "md":
                # Use the markdown generator
                bulletin = bulletin_md(snapshot)
            else:
                # Original text format
                bulletin = f"""CODEX SIGNALS DAILY BULLETIN - {snapshot.get('generated_at', 'Unknown')}

{snapshot.get('banner', 'Daily Portfolio Intelligence')}

TIER DISTRIBUTION:
- Alpha Tier: {snapshot.get('tier_counts', {}).get('Alpha', 0)} positions
- Beta Tier: {snapshot.get('tier_counts', {}).get('Beta', 0)} positions  
- Gamma Tier: {snapshot.get('tier_counts', {}).get('Gamma', 0)} positions
- Delta Tier: {snapshot.get('tier_counts', {}).get('Delta', 0)} positions

POSITION RECOMMENDATIONS:
"""
                
                for pick in snapshot.get('picks', []):
                    bulletin += f"""
{pick['symbol']} - Tier {pick['tier']}
Target Weight: {pick['target_weight']:.2%}
Rationale: {pick['rationale']}
Risk Factors: {', '.join(pick['risk_factors']) if pick['risk_factors'] else 'None'}
"""
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(bulletin)
            
            self.logger.info(f"Bulletin saved to {path}")
            return path
            
        except Exception as e:
            self.logger.error(f"Error saving bulletin: {e}")
            return ""

    def update_positions_from_signals(self, snapshot: Dict, auto_rebalance: bool = False) -> Dict:
        """Update portfolio positions based on signals (simulation only)"""
        try:
            picks = snapshot.get('picks', [])
            current_positions = self.load_positions_from_ledger()
            
            updates = []
            
            for pick in picks:
                symbol = pick['symbol']
                target_weight = pick['target_weight']
                current_weight = current_positions.get(symbol, Position(symbol, 0.0, 0.10)).weight
                
                if abs(target_weight - current_weight) > 0.01:  # 1% threshold
                    updates.append({
                        'symbol': symbol,
                        'current_weight': current_weight,
                        'target_weight': target_weight,
                        'change': target_weight - current_weight,
                        'tier': pick['tier'],
                        'rationale': pick['rationale']
                    })
            
            rebalance_summary = {
                'rebalance_needed': len(updates) > 0,
                'updates_count': len(updates),
                'updates': updates,
                'simulation_only': not auto_rebalance,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            if auto_rebalance and updates:
                # In a real system, this would execute trades
                # For now, just update position weights
                for update in updates:
                    symbol = update['symbol']
                    if symbol in current_positions:
                        current_positions[symbol].weight = update['target_weight']
                
                # Save updated positions
                self.save_positions(current_positions)
                rebalance_summary['executed'] = True
            
            return rebalance_summary
            
        except Exception as e:
            self.logger.error(f"Error updating positions from signals: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }

def run_signals_integration():
    """Run signals integration and generate report"""
    print("🔥 CODEX SIGNALS INTEGRATION 📊")
    print("=" * 40)
    
    integration = CodexSignalsIntegration()
    
    # Generate signals report
    print("📊 Generating signals report...")
    report = integration.generate_signals_report()
    
    if 'error' in report:
        print(f"❌ Error: {report['error']}")
        return
    
    # Save snapshot
    print("💾 Saving signals snapshot...")
    saved = integration.save_signals_snapshot(report)
    
    if saved:
        print("✅ Signals snapshot saved successfully")
    else:
        print("⚠️ Warning: Could not save signals snapshot")
    
    # Show summary
    print("\n📈 SIGNALS SUMMARY:")
    print("=" * 20)
    
    tier_counts = report.get('tier_counts', {})
    for tier, count in tier_counts.items():
        print(f"{tier}: {count} symbols")
    
    print(f"\nBanner: {report.get('banner', 'N/A')}")
    
    # Show dawn dispatch summary
    print("\n🌅 DAWN DISPATCH INTEGRATION:")
    print("=" * 30)
    
    dawn_summary = integration.get_signals_for_dawn_dispatch()
    for key, value in dawn_summary.items():
        print(f"{key}: {value}")
    
    print("\n✅ Codex Signals integration complete!")

if __name__ == "__main__":
    run_signals_integration()