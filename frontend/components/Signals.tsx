import { useEffect, useState } from 'react';

type Pick = {
  symbol: string;
  tier: string;
  target_weight: number;
  rationale: string;
  risk_factors: string[];
};

type Snapshot = {
  generated_at: string;
  banner: string;
  tier_counts: { Alpha: number; Beta: number; Gamma: number; Delta: number };
  picks: Pick[];
};

export default function SignalsPage() {
  const [snapshot, setSnapshot] = useState<Snapshot | null>(null);
  const [bulletin, setBulletin] = useState<string>("");

  useEffect(() => {
    async function load() {
      // Replace with your Cloud Run URL
      const res = await fetch("https://codex-signals-<HASH>.run.app/signals/daily", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          market: [
            { symbol: "MSFT", price: 420.1, vol_30d: 0.22, trend_20d: 0.48, liquidity_rank: 5 },
            { symbol: "ETH-USD", price: 3500.0, vol_30d: 0.40, trend_20d: 0.30, liquidity_rank: 15 },
            { symbol: "XYZ", price: 12.0, vol_30d: 0.65, trend_20d: -0.10, liquidity_rank: 250 },
          ],
          positions: [
            { symbol: "MSFT", weight: 0.04, allowed_max: 0.08 },
            { symbol: "ETH-USD", weight: 0.02, allowed_max: 0.06 },
          ],
        }),
      });
      const snap = await res.json();
      setSnapshot(snap);
      // Simple client-side MD render (no external deps): convert minimal MD to HTML
      const md = buildBulletinMD(snap);
      setBulletin(mdToHtml(md));
    }
    load();
  }, []);

  function buildBulletinMD(snap: Snapshot) {
    const header = `# Daily Signals — ${snap.generated_at}\n\n`;
    const banner = `> ${snap.banner}\n\n`;
    const tiers = `- Alpha: ${snap.tier_counts.Alpha}\n- Beta: ${snap.tier_counts.Beta}\n- Gamma: ${snap.tier_counts.Gamma}\n- Delta: ${snap.tier_counts.Delta}\n\n`;
    const body = (snap.picks || [])
      .map(
        (p) =>
          `**${p.symbol}** — Tier ${p.tier} | target ${(p.target_weight * 100).toFixed(2)}%\n- Rationale: ${p.rationale}\n- Risks: ${p.risk_factors.join(", ") || "None"}\n`
      )
      .join("\n");
    return header + banner + tiers + body;
  }

  function mdToHtml(md: string) {
    // Minimal converter: headings, blockquote, bold, line breaks
    return md
      .replace(/^# (.*)$/gm, "<h1>$1</h1>")
      .replace(/^> (.*)$/gm, "<blockquote>$1</blockquote>")
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\n- (.*)/g, "<br>• $1")
      .replace(/\n/g, "<br>");
  }

  return (
    <div style={{ padding: 24 }}>
      <h1>Signals</h1>
      {!snapshot ? (
        <p>Loading snapshot…</p>
      ) : (
        <>
          <div>
            <strong>Banner:</strong> {snapshot.banner}
          </div>
          <div style={{ marginTop: 16 }}>
            <strong>Tiers:</strong>{' '}
            Alpha {snapshot.tier_counts.Alpha} | Beta {snapshot.tier_counts.Beta} | Gamma {snapshot.tier_counts.Gamma} | Delta {snapshot.tier_counts.Delta}
          </div>
          <div style={{ marginTop: 24 }}>
            <strong>Bulletin:</strong>
            <div dangerouslySetInnerHTML={{ __html: bulletin }} />
          </div>
        </>
      )}
    </div>
  );
}
