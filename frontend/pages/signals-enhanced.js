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
exports.default = SignalsEnhancedPage;
// pages/signals-enhanced.tsx
var react_1 = require("react");
var SignalsCard_1 = require("../components/SignalsCard");
var TierSummary_1 = require("../components/TierSummary");
var api_1 = require("../utils/api");
var signals_enhanced_module_css_1 = require("./signals-enhanced.module.css");
function SignalsEnhancedPage() {
    var _this = this;
    var _a = (0, react_1.useState)(null), snapshot = _a[0], setSnapshot = _a[1];
    var _b = (0, react_1.useState)(true), loading = _b[0], setLoading = _b[1];
    var _c = (0, react_1.useState)(null), error = _c[0], setError = _c[1];
    // Replace with your actual Cloud Run URL
    var API_URL = 'https://codex-signals-<HASH>.run.app';
    var _d = (0, api_1.useCodexSignals)(API_URL), api = _d.api, utils = _d.utils;
    (0, react_1.useEffect)(function () {
        function loadSignals() {
            return __awaiter(this, void 0, void 0, function () {
                var snapshot_1, err_1;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            _a.trys.push([0, 2, 3, 4]);
                            setLoading(true);
                            setError(null);
                            return [4 /*yield*/, api.getMockSignals()];
                        case 1:
                            snapshot_1 = _a.sent();
                            setSnapshot(snapshot_1);
                            return [3 /*break*/, 4];
                        case 2:
                            err_1 = _a.sent();
                            console.error('Error loading signals:', err_1);
                            setError(err_1 instanceof Error ? err_1.message : 'Failed to load signals');
                            return [3 /*break*/, 4];
                        case 3:
                            setLoading(false);
                            return [7 /*endfinally*/];
                        case 4: return [2 /*return*/];
                    }
                });
            });
        }
        loadSignals();
    }, []);
    var handleGenerateDaily = function () { return __awaiter(_this, void 0, void 0, function () {
        var marketData, positions, snapshot_2, err_2;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 2, 3, 4]);
                    setLoading(true);
                    setError(null);
                    marketData = [
                        {
                            symbol: 'MSFT',
                            price: 420.1,
                            vol_30d: 0.22,
                            trend_20d: 0.48,
                            liquidity_rank: 5,
                        },
                        {
                            symbol: 'AAPL',
                            price: 185.0,
                            vol_30d: 0.28,
                            trend_20d: 0.15,
                            liquidity_rank: 3,
                        },
                        {
                            symbol: 'GOOGL',
                            price: 140.5,
                            vol_30d: 0.31,
                            trend_20d: -0.05,
                            liquidity_rank: 8,
                        },
                        {
                            symbol: 'ETH-USD',
                            price: 3500.0,
                            vol_30d: 0.4,
                            trend_20d: 0.3,
                            liquidity_rank: 15,
                        },
                        {
                            symbol: 'BTC-USD',
                            price: 67000.0,
                            vol_30d: 0.38,
                            trend_20d: 0.42,
                            liquidity_rank: 10,
                        },
                    ];
                    positions = [
                        { symbol: 'MSFT', weight: 0.04, allowed_max: 0.08 },
                        { symbol: 'AAPL', weight: 0.03, allowed_max: 0.06 },
                        { symbol: 'ETH-USD', weight: 0.02, allowed_max: 0.06 },
                        { symbol: 'BTC-USD', weight: 0.015, allowed_max: 0.05 },
                    ];
                    return [4 /*yield*/, api.generateDailySignals(marketData, positions)];
                case 1:
                    snapshot_2 = _a.sent();
                    setSnapshot(snapshot_2);
                    return [3 /*break*/, 4];
                case 2:
                    err_2 = _a.sent();
                    console.error('Error generating signals:', err_2);
                    setError(err_2 instanceof Error ? err_2.message : 'Failed to generate signals');
                    return [3 /*break*/, 4];
                case 3:
                    setLoading(false);
                    return [7 /*endfinally*/];
                case 4: return [2 /*return*/];
            }
        });
    }); };
    var handleDownloadBulletin = function () { return __awaiter(_this, void 0, void 0, function () {
        var bulletin, blob, url, a, err_3;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 2, , 3]);
                    return [4 /*yield*/, api.generateBulletin('md')];
                case 1:
                    bulletin = _a.sent();
                    blob = new Blob([bulletin.content], { type: 'text/markdown' });
                    url = URL.createObjectURL(blob);
                    a = document.createElement('a');
                    a.href = url;
                    a.download = "codex-signals-".concat(new Date().toISOString().split('T')[0], ".md");
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                    return [3 /*break*/, 3];
                case 2:
                    err_3 = _a.sent();
                    console.error('Error downloading bulletin:', err_3);
                    setError(err_3 instanceof Error ? err_3.message : 'Failed to download bulletin');
                    return [3 /*break*/, 3];
                case 3: return [2 /*return*/];
            }
        });
    }); };
    if (loading) {
        return (<div className={signals_enhanced_module_css_1.default.loading}>
        <div>
          <div className={signals_enhanced_module_css_1.default.loadingIcon}>🔄</div>
          <div>Loading Codex Signals...</div>
        </div>
      </div>);
    }
    if (error) {
        return (<div className={signals_enhanced_module_css_1.default.container}>
        <div className={signals_enhanced_module_css_1.default.error}>
          <strong>Error:</strong> {error}
          <button onClick={function () { return window.location.reload(); }} className={signals_enhanced_module_css_1.default.retryBtn}>
            Retry
          </button>
        </div>
      </div>);
    }
    return (<div className={signals_enhanced_module_css_1.default.container}>
      {/* Header */}
      <div className={signals_enhanced_module_css_1.default.header}>
        <h1 className={signals_enhanced_module_css_1.default.title}>🔥 Codex Signals Dashboard</h1>
        <div className={signals_enhanced_module_css_1.default.headerBtns}>
          <button onClick={handleGenerateDaily} className={signals_enhanced_module_css_1.default.genBtn}>
            Generate Daily Signals
          </button>
          <button onClick={handleDownloadBulletin} disabled={!snapshot} className={"".concat(signals_enhanced_module_css_1.default.downloadBtn, " ").concat(!snapshot ? signals_enhanced_module_css_1.default.downloadBtnDisabled : '')}>
            Download Bulletin
          </button>
        </div>
      </div>

      {snapshot && (<>
          {/* Tier Summary */}
          <TierSummary_1.TierSummary tierCounts={snapshot.tier_counts} generatedAt={snapshot.generated_at} banner={snapshot.banner}/>
          {/* Portfolio Metrics */}
          <div className={signals_enhanced_module_css_1.default.metrics}>
            <div>
              <strong>Total Positions:</strong> {snapshot.picks.length}
            </div>
            <div>
              <strong>Total Allocation:</strong>{' '}
              {utils.formatWeight(utils.calculateTotalAllocation(snapshot.picks))}
            </div>
            <div>
              <strong>High Conviction:</strong> {snapshot.tier_counts.Alpha} Alpha picks
            </div>
            <div>
              <strong>Risk Positions:</strong> {snapshot.tier_counts.Delta} Delta positions
            </div>
          </div>
          {/* Signals Grid */}
          <div className={signals_enhanced_module_css_1.default.signalsGrid}>
            {snapshot.picks.map(function (pick, index) { return (<SignalsCard_1.SignalsCard key={"".concat(pick.symbol, "-").concat(index)} pick={pick}/>); })}
          </div>
          {/* Footer */}
          <div className={signals_enhanced_module_css_1.default.footer}>
            <div className={signals_enhanced_module_css_1.default.footerText}>
              Generated by <strong>The Merritt Method™</strong> | Codex Dominion Portfolio
              Intelligence
            </div>
            <div className={signals_enhanced_module_css_1.default.footerSub}>
              🔥 Digital Sovereignty • 📊 Quantitative Finance • 👑 Elite Performance
            </div>
          </div>
        </>)}
    </div>);
}
