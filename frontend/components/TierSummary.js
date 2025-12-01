"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.TierSummary = void 0;
// components/TierSummary.tsx
var react_1 = require("react");
var TierSummary_module_css_1 = require("./TierSummary.module.css");
var TierSummary = function (_a) {
    var tierCounts = _a.tierCounts, generatedAt = _a.generatedAt, banner = _a.banner;
    var total = tierCounts.Alpha + tierCounts.Beta + tierCounts.Gamma + tierCounts.Delta;
    var tierData = [
        {
            name: 'Alpha',
            count: tierCounts.Alpha,
            color: '#10b981',
            description: 'High conviction',
        },
        {
            name: 'Beta',
            count: tierCounts.Beta,
            color: '#3b82f6',
            description: 'Balanced exposure',
        },
        {
            name: 'Gamma',
            count: tierCounts.Gamma,
            color: '#f59e0b',
            description: 'Elevated risk',
        },
        {
            name: 'Delta',
            count: tierCounts.Delta,
            color: '#ef4444',
            description: 'High turbulence',
        },
    ];
    return (<div className={TierSummary_module_css_1.default.container}>
      <div className={TierSummary_module_css_1.default.header}>
        <h2 className={TierSummary_module_css_1.default.title}>🔥 Codex Signals</h2>
        <div className={TierSummary_module_css_1.default.date}>{new Date(generatedAt).toLocaleString()}</div>
      </div>
      <div className={TierSummary_module_css_1.default.banner}>
        <strong>📢 Market Banner:</strong> {banner}
      </div>
      <div className={TierSummary_module_css_1.default.tierGrid}>
        {tierData.map(function (tier) { return (<div key={tier.name} className={"".concat(TierSummary_module_css_1.default.tierCard, " ").concat(tier.name === 'Alpha'
                ? TierSummary_module_css_1.default.tierAlpha
                : tier.name === 'Beta'
                    ? TierSummary_module_css_1.default.tierBeta
                    : tier.name === 'Gamma'
                        ? TierSummary_module_css_1.default.tierGamma
                        : tier.name === 'Delta'
                            ? TierSummary_module_css_1.default.tierDelta
                            : '')}>
            <div className={"".concat(TierSummary_module_css_1.default.tierCount, " ").concat(tier.name === 'Alpha'
                ? TierSummary_module_css_1.default.tierCountAlpha
                : tier.name === 'Beta'
                    ? TierSummary_module_css_1.default.tierCountBeta
                    : tier.name === 'Gamma'
                        ? TierSummary_module_css_1.default.tierCountGamma
                        : tier.name === 'Delta'
                            ? TierSummary_module_css_1.default.tierCountDelta
                            : '')}>
              {tier.count}
            </div>
            <div className={TierSummary_module_css_1.default.tierName}>{tier.name}</div>
            <div className={TierSummary_module_css_1.default.tierDesc}>{tier.description}</div>
            <div className={TierSummary_module_css_1.default.tierPercent}>
              {total > 0 ? "".concat(((tier.count / total) * 100).toFixed(1), "%") : '0%'}
            </div>
          </div>); })}
      </div>
      <div className={TierSummary_module_css_1.default.footer}>
        <strong>Total Positions:</strong> {total} |<strong> Portfolio Intelligence:</strong> Active
        |<strong> The Merritt Method™</strong> 👑
      </div>
    </div>);
};
exports.TierSummary = TierSummary;
