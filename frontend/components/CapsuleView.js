"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = CapsuleView;
var react_1 = require("react");
function CapsuleView(_a) {
    var artifact = _a.artifact, role = _a.role;
    if (!artifact)
        return <p>No artifact available</p>;
    if (role === 'custodian') {
        return (<div>
        <h2>Custodian View</h2>
        <pre>{JSON.stringify(artifact, null, 2)}</pre>
      </div>);
    }
    if (role === 'heir') {
        return (<div>
        <h2>Heir View</h2>
        <blockquote>{artifact.banner}</blockquote>
        <p>
          Tier Counts: Alpha {artifact.tier_counts.Alpha}, Beta {artifact.tier_counts.Beta}, Gamma{' '}
          {artifact.tier_counts.Gamma}, Delta {artifact.tier_counts.Delta}
        </p>
        <h3>Top Picks</h3>
        <ul>
          {artifact.picks.slice(0, 3).map(function (p, i) { return (<li key={i}>
              <strong>{p.symbol}</strong> — Tier {p.tier} | target{' '}
              {(p.target_weight * 100).toFixed(2)}%
              <br />
              Summary: {p.rationale.split('.')[0]}
            </li>); })}
        </ul>
      </div>);
    }
    if (role === 'customer') {
        return (<div>
        <h2>Customer View</h2>
        <p>{artifact.banner}</p>
        <h3>Featured Capsules</h3>
        <ul>
          {artifact.picks.slice(0, 2).map(function (p, i) { return (<li key={i}>
              <strong>{p.symbol}</strong> — Tier {p.tier}
              <br />
              Guidance: {p.rationale.split('.')[0]}
            </li>); })}
        </ul>
      </div>);
    }
    return <p>Unknown role</p>;
}
