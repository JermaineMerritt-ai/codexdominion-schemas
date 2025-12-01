"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = CapsulePage;
var router_1 = require("next/router");
var react_1 = require("react");
var CapsuleView_1 = require("../../components/CapsuleView");
var capsule_slug_module_css_1 = require("./capsule-slug.module.css");
function CapsulePage() {
    var router = (0, router_1.useRouter)();
    var slug = router.query.slug;
    var _a = (0, react_1.useState)(null), artifact = _a[0], setArtifact = _a[1];
    var _b = (0, react_1.useState)(true), loading = _b[0], setLoading = _b[1];
    var _c = (0, react_1.useState)(null), error = _c[0], setError = _c[1];
    var _d = (0, react_1.useState)('heir'), userRole = _d[0], setUserRole = _d[1]; // Default role
    (0, react_1.useEffect)(function () {
        if (!slug || typeof slug !== 'string')
            return;
        function loadArtifact() {
            return __awaiter(this, void 0, void 0, function () {
                var res, data, err_1;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            _a.trys.push([0, 3, 4, 5]);
                            setLoading(true);
                            setError(null);
                            return [4 /*yield*/, fetch("/api/artifacts/".concat(slug, "/latest"))];
                        case 1:
                            res = _a.sent();
                            if (!res.ok) {
                                throw new Error("Failed to load artifact: ".concat(res.status, " ").concat(res.statusText));
                            }
                            return [4 /*yield*/, res.json()];
                        case 2:
                            data = _a.sent();
                            setArtifact(data);
                            return [3 /*break*/, 5];
                        case 3:
                            err_1 = _a.sent();
                            console.error('Error loading artifact:', err_1);
                            setError(err_1 instanceof Error ? err_1.message : 'Unknown error occurred');
                            return [3 /*break*/, 5];
                        case 4:
                            setLoading(false);
                            return [7 /*endfinally*/];
                        case 5: return [2 /*return*/];
                    }
                });
            });
        }
        loadArtifact();
    }, [slug]);
    if (loading) {
        return (<div className={capsule_slug_module_css_1.default.container}>
        <div className={capsule_slug_module_css_1.default.loadingContainer}>
          <div className={capsule_slug_module_css_1.default.spinner}></div>
          <p>Loading capsule artifact for {slug}...</p>
        </div>
      </div>);
    }
    if (error) {
        return (<div className={capsule_slug_module_css_1.default.container}>
        <div className={capsule_slug_module_css_1.default.errorContainer}>
          <h1>❌ Error Loading Capsule</h1>
          <p>
            <strong>Capsule:</strong> {slug}
          </p>
          <p className={capsule_slug_module_css_1.default.errorMessage}>{error}</p>
          <button onClick={function () { return router.back(); }} className={capsule_slug_module_css_1.default.backButton}>
            ← Back to Capsules
          </button>
        </div>
      </div>);
    }
    if (!artifact) {
        return (<div className={capsule_slug_module_css_1.default.container}>
        <p>No artifact found for capsule: {slug}</p>
      </div>);
    }
    return (<div className={capsule_slug_module_css_1.default.container}>
      <div className="capsule-header">
        <button onClick={function () { return router.back(); }} className="back-button">
          ← Back
        </button>
        <h1>{artifact.title}</h1>
        <div className="meta-info">
          <p>
            <strong>Capsule:</strong> <code>{slug}</code>
          </p>
          <p>
            <strong>Generated:</strong> {new Date(artifact.generated_at).toLocaleString()}
          </p>
          {artifact.execution_id && (<p>
              <strong>Execution ID:</strong> <code>{artifact.execution_id}</code>
            </p>)}
          {artifact.status && (<p>
              <strong>Status:</strong>
              <span className={"status-badge ".concat(artifact.status)}>
                {artifact.status.toUpperCase()}
              </span>
            </p>)}
        </div>
      </div>

      <div className="role-selector">
        <label htmlFor="role-select">View Mode:</label>
        <select id="role-select" value={userRole} onChange={function (e) { return setUserRole(e.target.value); }} className="role-dropdown">
          <option value="heir">Heir View</option>
          <option value="customer">Customer View</option>
          <option value="custodian">Custodian View</option>
        </select>
      </div>

      <div className="capsule-view-container">
        <CapsuleView_1.default artifact={artifact} role={userRole}/>
      </div>

      <div className="content-grid">
        <div className="tier-section">
          <h2>🎯 Tier Distribution</h2>
          <div className="tier-counts">
            <div className="tier-item alpha">
              <span className="tier-label">Alpha</span>
              <span className="tier-count">{artifact.tier_counts.Alpha}</span>
            </div>
            <div className="tier-item beta">
              <span className="tier-label">Beta</span>
              <span className="tier-count">{artifact.tier_counts.Beta}</span>
            </div>
            <div className="tier-item gamma">
              <span className="tier-label">Gamma</span>
              <span className="tier-count">{artifact.tier_counts.Gamma}</span>
            </div>
            <div className="tier-item delta">
              <span className="tier-label">Delta</span>
              <span className="tier-count">{artifact.tier_counts.Delta}</span>
            </div>
          </div>
        </div>

        <div className="picks-section">
          <h2>📊 Investment Picks</h2>
          <div className="picks-grid">
            {artifact.picks.map(function (pick, i) { return (<div key={i} className="pick-card">
                <div className="pick-header">
                  <h3 className="symbol">{pick.symbol}</h3>
                  <div className="pick-meta">
                    <span className={"tier-badge tier-".concat(pick.tier.toLowerCase())}>
                      {pick.tier}
                    </span>
                    <span className="weight">{(pick.target_weight * 100).toFixed(2)}%</span>
                  </div>
                </div>

                <div className="rationale">
                  <strong>Rationale:</strong>
                  <p>{pick.rationale}</p>
                </div>

                {pick.risk_factors && pick.risk_factors.length > 0 && (<div className="risks">
                    <strong>Risk Factors:</strong>
                    <ul>
                      {pick.risk_factors.map(function (risk, idx) { return (<li key={idx}>{risk}</li>); })}
                    </ul>
                  </div>)}
              </div>); })}
          </div>
        </div>
      </div>

      <style jsx>{"\n        .capsule-header {\n          border-bottom: 2px solid #e1e5e9;\n          padding-bottom: 1.5rem;\n          margin-bottom: 2rem;\n        }\n\n        .back-button {\n          background: #6c757d;\n          color: white;\n          border: none;\n          padding: 0.5rem 1rem;\n          border-radius: 4px;\n          cursor: pointer;\n          margin-bottom: 1rem;\n          font-size: 0.9rem;\n        }\n\n        .back-button:hover {\n          background: #5a6268;\n        }\n\n        .role-selector {\n          display: flex;\n          align-items: center;\n          interface Artifact {\n            title: string;\n            generated_at: string;\n            execution_id?: string;\n            status?: string;\n            tier_counts: {\n              Alpha: number;\n              Beta: number;\n              Gamma: number;\n              Delta: number;\n            };\n            picks: Array<{\n              symbol: string;\n              tier: string;\n              target_weight: number;\n              rationale: string;\n              risk_factors?: string[];\n            }>;\n          }\n          gap: 1rem;\n          margin-bottom: 2rem;\n          padding: 1rem;\n          background: #f8f9fa;\n          border-radius: 8px;\n        }\n\n        .role-dropdown {\n          padding: 0.5rem;\n        }\n\n        .meta-info p {\n          margin: 0.25rem 0;\n          color: #6c757d;\n        }\n\n        .meta-info code {\n          background: #f8f9fa;\n          padding: 0.2rem 0.4rem;\n          border-radius: 3px;\n          font-family: \"Courier New\", monospace;\n        }\n\n        .status-badge {\n          padding: 0.2rem 0.5rem;\n          border-radius: 3px;\n          font-size: 0.8rem;\n          font-weight: bold;\n          margin-left: 0.5rem;\n        }\n\n        .status-badge.success {\n          background: #d4edda;\n          color: #155724;\n        }\n\n        .banner-section {\n          background: #f8f9fa;\n          padding: 1.5rem;\n          border-radius: 8px;\n          border-left: 4px solid #0070f3;\n          margin-bottom: 2rem;\n        }\n\n        .banner-section blockquote {\n          margin: 0;\n          font-size: 1.1rem;\n          font-style: italic;\n          color: #495057;\n        }\n\n        .content-grid {\n          display: grid;\n          grid-template-columns: 1fr 2fr;\n          gap: 2rem;\n        }\n\n        @media (max-width: 768px) {\n          .content-grid {\n            grid-template-columns: 1fr;\n          }\n          .meta-info {\n            flex-direction: column;\n            gap: 0.5rem;\n          }\n        }\n\n        .tier-section h2,\n        .picks-section h2 {\n          color: #343a40;\n          border-bottom: 1px solid #dee2e6;\n          padding-bottom: 0.5rem;\n        }\n\n        .tier-counts {\n          display: grid;\n          grid-template-columns: repeat(2, 1fr);\n          gap: 1rem;\n          margin-top: 1rem;\n        }\n\n        .tier-item {\n          display: flex;\n          justify-content: space-between;\n          align-items: center;\n          padding: 1rem;\n          border-radius: 6px;\n          font-weight: bold;\n        }\n\n        .tier-item.alpha {\n          background: #fff3cd;\n          border-left: 4px solid #ffc107;\n        }\n\n        .tier-item.beta {\n          background: #d1ecf1;\n          border-left: 4px solid #17a2b8;\n        }\n\n        .tier-item.gamma {\n          background: #d4edda;\n          border-left: 4px solid #28a745;\n        }\n\n        .tier-item.delta {\n          background: #f8d7da;\n          border-left: 4px solid #dc3545;\n        }\n\n        .tier-count {\n          font-size: 1.25rem;\n        }\n\n        .picks-grid {\n          display: flex;\n          flex-direction: column;\n          gap: 1rem;\n          margin-top: 1rem;\n        }\n\n        .pick-card {\n          border: 1px solid #dee2e6;\n          border-radius: 8px;\n          padding: 1.5rem;\n          background: white;\n          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);\n        }\n\n        .pick-header {\n          display: flex;\n          justify-content: space-between;\n          align-items: center;\n          margin-bottom: 1rem;\n        }\n\n        .symbol {\n          margin: 0;\n          font-size: 1.25rem;\n          font-family: monospace;\n          color: #0070f3;\n        }\n\n        .pick-meta {\n          display: flex;\n          align-items: center;\n          gap: 1rem;\n        }\n\n        .tier-badge {\n          padding: 0.25rem 0.5rem;\n          border-radius: 4px;\n          font-size: 0.8rem;\n          font-weight: bold;\n          text-transform: uppercase;\n        }\n\n        .tier-badge.tier-alpha {\n          background: #ffc107;\n          color: #856404;\n        }\n\n        .tier-badge.tier-beta {\n          background: #17a2b8;\n          color: white;\n        }\n\n        .tier-badge.tier-gamma {\n          background: #28a745;\n          color: white;\n        }\n\n        .tier-badge.tier-delta {\n          background: #dc3545;\n          color: white;\n        }\n\n        .weight {\n          font-size: 1.1rem;\n          font-weight: bold;\n          color: #495057;\n        }\n\n        .rationale,\n        .risks {\n          margin-top: 1rem;\n        }\n\n        .rationale p,\n        .risks ul {\n          margin-top: 0.5rem;\n          color: #6c757d;\n        }\n\n        .risks ul {\n          padding-left: 1.25rem;\n        }\n\n        .risks li {\n          margin-bottom: 0.25rem;\n        }\n      "}</style>
    </div>);
}
