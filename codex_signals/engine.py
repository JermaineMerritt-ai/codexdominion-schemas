# codex_signals/engine.py
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class MarketSnapshot:
    symbol: str
    price: float
    vol_30d: float  # 30-day realized volatility
    trend_20d: float  # normalized 20-day trend score [-1, 1]
    liquidity_rank: int  # 1=highest liquidity


@dataclass
class Position:
    symbol: str
    weight: float  # current portfolio weight
    allowed_max: float  # governance cap


@dataclass
class Pick:
    symbol: str
    tier: str
    target_weight: float
    rationale: str
    risk_factors: List[str]


class SignalsEngine:
    def __init__(
        self,
        exposure_cap: float = 0.10,
        vol_alpha: float = 0.25,
        trend_alpha: float = 0.35,
    ):
        self.exposure_cap = exposure_cap  # max per-symbol target weight
        self.vol_alpha = vol_alpha  # volatility ceiling for Tier Alpha
        self.trend_alpha = trend_alpha  # trend threshold for Tier Alpha

    def classify_tier(self, m: MarketSnapshot) -> str:
        if (
            m.trend_20d >= self.trend_alpha
            and m.vol_30d <= self.vol_alpha
            and m.liquidity_rank <= 50
        ):
            return "Alpha"
        if m.vol_30d <= 0.35 and abs(m.trend_20d) < 0.35:
            return "Beta"
        if m.vol_30d <= 0.55:
            return "Gamma"
        return "Delta"

    def target_weight(
        self, tier: str, m: MarketSnapshot, current_weight: float, allowed_max: float
    ) -> float:
        base = {
            "Alpha": min(self.exposure_cap, 0.08),
            "Beta": min(self.exposure_cap, 0.05),
            "Gamma": min(self.exposure_cap, 0.03),
            "Delta": 0.0,
        }[tier]
        tw = min(base, allowed_max)
        # Avoid large step changes (smooth rebalance)
        step = 0.02
        if tw > current_weight:
            tw = min(tw, current_weight + step)
        else:
            tw = max(tw, max(0.0, current_weight - step))
        return round(tw, 4)

    def rationale(self, tier: str, m: MarketSnapshot) -> str:
        parts = []
        parts.append(
            f"20d trend={m.trend_20d:.2f}, 30d vol={m.vol_30d:.2f}, liquidity_rank={m.liquidity_rank}"
        )
        if tier == "Alpha":
            parts.append(
                "Strong positive trend with controlled volatility and deep liquidity."
            )
        elif tier == "Beta":
            parts.append(
                "Neutral/stable regime; measured exposure and diversification preferred."
            )
        elif tier == "Gamma":
            parts.append("Elevated risk; defensive posture and reduced sizing.")
        else:
            parts.append("High turbulence; preserve capital, avoid new exposure.")
        return " ".join(parts)

    def risk_factors(self, m: MarketSnapshot) -> List[str]:
        factors = []
        if m.vol_30d > 0.35:
            factors.append("Volatility above comfort threshold")
        if abs(m.trend_20d) < 0.15:
            factors.append("Weak/indecisive trend")
        if m.liquidity_rank > 100:
            factors.append("Lower liquidity")
        return factors

    def generate(
        self, market: List[MarketSnapshot], positions: Dict[str, Position]
    ) -> Dict[str, Any]:
        picks: List[Pick] = []
        tier_counts = {"Alpha": 0, "Beta": 0, "Gamma": 0, "Delta": 0}

        for m in market:
            tier = self.classify_tier(m)
            tier_counts[tier] += 1

            pos = positions.get(m.symbol, Position(m.symbol, 0.0, self.exposure_cap))
            tw = self.target_weight(tier, m, pos.weight, pos.allowed_max)
            rationale = self.rationale(tier, m)
            risks = self.risk_factors(m)

            if tier == "Delta":
                tw = 0.0  # kill switch for high turbulence

            picks.append(
                Pick(
                    symbol=m.symbol,
                    tier=tier,
                    target_weight=tw,
                    rationale=rationale,
                    risk_factors=risks,
                )
            )

        banner = self.compliance_banner(tier_counts)
        snapshot = {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "tier_counts": tier_counts,
            "banner": banner,
            "picks": [pick.__dict__ for pick in picks],
        }
        return snapshot

    def compliance_banner(self, tier_counts: Dict[str, int]) -> str:
        if tier_counts["Delta"] > 0:
            return "High-risk environment detected. Signals are informational. Consider capital preservation."
        if tier_counts["Gamma"] > tier_counts["Alpha"] + tier_counts["Beta"]:
            return "Elevated uncertainty. Size positions defensively and respect governance caps."
        return "Signals are educational and informational. Past performance does not guarantee future results."


# Example usage
if __name__ == "__main__":
    market = [
        MarketSnapshot(
            symbol="MSFT", price=420.1, vol_30d=0.22, trend_20d=0.48, liquidity_rank=5
        ),
        MarketSnapshot(
            symbol="ETH-USD",
            price=3500.0,
            vol_30d=0.40,
            trend_20d=0.30,
            liquidity_rank=15,
        ),
        MarketSnapshot(
            symbol="XYZ", price=12.0, vol_30d=0.65, trend_20d=-0.10, liquidity_rank=250
        ),
    ]
    positions = {
        "MSFT": Position(symbol="MSFT", weight=0.04, allowed_max=0.08),
        "ETH-USD": Position(symbol="ETH-USD", weight=0.02, allowed_max=0.06),
    }
    engine = SignalsEngine()
    snapshot = engine.generate(market, positions)
    from pprint import pprint

    pprint(snapshot)
