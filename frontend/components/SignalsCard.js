"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.SignalsCard = void 0;
// components/SignalsCard.tsx
var react_1 = require("react");
var SignalsCard_module_css_1 = require("./SignalsCard.module.css");
var tierColors = {
    Alpha: '#10b981', // green
    Beta: '#3b82f6', // blue
    Gamma: '#f59e0b', // orange
    Delta: '#ef4444', // red
};
var SignalsCard = function (_a) {
    var pick = _a.pick;
    var borderClass = pick.tier === 'Alpha'
        ? SignalsCard_module_css_1.default.borderAlpha
        : pick.tier === 'Beta'
            ? SignalsCard_module_css_1.default.borderBeta
            : pick.tier === 'Gamma'
                ? SignalsCard_module_css_1.default.borderGamma
                : pick.tier === 'Delta'
                    ? SignalsCard_module_css_1.default.borderDelta
                    : '';
    var tierClass = pick.tier === 'Alpha'
        ? SignalsCard_module_css_1.default.tierAlpha
        : pick.tier === 'Beta'
            ? SignalsCard_module_css_1.default.tierBeta
            : pick.tier === 'Gamma'
                ? SignalsCard_module_css_1.default.tierGamma
                : pick.tier === 'Delta'
                    ? SignalsCard_module_css_1.default.tierDelta
                    : '';
    return (<div className={"".concat(SignalsCard_module_css_1.default.card, " ").concat(borderClass)}>
      <div className={SignalsCard_module_css_1.default.header}>
        <h3 className={SignalsCard_module_css_1.default.symbol}>{pick.symbol}</h3>
        <div className={"".concat(SignalsCard_module_css_1.default.tier, " ").concat(tierClass)}>{pick.tier}</div>
      </div>
      <div className={SignalsCard_module_css_1.default.targetWeight}>
        <strong>Target Weight:</strong> {(pick.target_weight * 100).toFixed(2)}%
      </div>
      <div className={SignalsCard_module_css_1.default.rationale}>
        <strong>Rationale:</strong>
        <p className={SignalsCard_module_css_1.default.rationaleText}>{pick.rationale}</p>
      </div>
      {pick.risk_factors && pick.risk_factors.length > 0 && (<div>
          <strong>Risk Factors:</strong>
          <ul className={SignalsCard_module_css_1.default.riskFactors}>
            {pick.risk_factors.map(function (risk, index) { return (<li key={index} className={SignalsCard_module_css_1.default.riskItem}>
                {risk}
              </li>); })}
          </ul>
        </div>)}
    </div>);
};
exports.SignalsCard = SignalsCard;
