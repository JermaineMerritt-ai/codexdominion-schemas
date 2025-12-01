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
exports.default = SignalsPage;
// pages/signals.tsx
var react_1 = require("react");
var signals_module_css_1 = require("./signals.module.css");
function SignalsPage() {
    var _a = (0, react_1.useState)(null), snapshot = _a[0], setSnapshot = _a[1];
    var _b = (0, react_1.useState)(''), bulletin = _b[0], setBulletin = _b[1];
    (0, react_1.useEffect)(function () {
        function load() {
            return __awaiter(this, void 0, void 0, function () {
                var res, snap, md;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, fetch('https://codex-signals-<HASH>.run.app/signals/daily', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({
                                    market: [
                                        {
                                            symbol: 'MSFT',
                                            price: 420.1,
                                            vol_30d: 0.22,
                                            trend_20d: 0.48,
                                            liquidity_rank: 5,
                                        },
                                        {
                                            symbol: 'ETH-USD',
                                            price: 3500.0,
                                            vol_30d: 0.4,
                                            trend_20d: 0.3,
                                            liquidity_rank: 15,
                                        },
                                        {
                                            symbol: 'XYZ',
                                            price: 12.0,
                                            vol_30d: 0.65,
                                            trend_20d: -0.1,
                                            liquidity_rank: 250,
                                        },
                                    ],
                                    positions: [
                                        { symbol: 'MSFT', weight: 0.04, allowed_max: 0.08 },
                                        { symbol: 'ETH-USD', weight: 0.02, allowed_max: 0.06 },
                                    ],
                                }),
                            })];
                        case 1:
                            res = _a.sent();
                            return [4 /*yield*/, res.json()];
                        case 2:
                            snap = _a.sent();
                            setSnapshot(snap);
                            md = buildBulletinMD(snap);
                            setBulletin(mdToHtml(md));
                            return [2 /*return*/];
                    }
                });
            });
        }
        load();
    }, []);
    function buildBulletinMD(snap) {
        var header = "# Daily Signals \u2014 ".concat(snap.generated_at, "\n\n");
        var banner = "> ".concat(snap.banner, "\n\n");
        var tiers = "- Alpha: ".concat(snap.tier_counts.Alpha, "\n- Beta: ").concat(snap.tier_counts.Beta, "\n- Gamma: ").concat(snap.tier_counts.Gamma, "\n- Delta: ").concat(snap.tier_counts.Delta, "\n\n");
        var body = (snap.picks || [])
            .map(function (p) {
            return "**".concat(p.symbol, "** \u2014 Tier ").concat(p.tier, " | target ").concat((p.target_weight * 100).toFixed(2), "%\n- Rationale: ").concat(p.rationale, "\n- Risks: ").concat(p.risk_factors.join(', ') || 'None', "\n");
        })
            .join('\n');
        return header + banner + tiers + body;
    }
    function mdToHtml(md) {
        // Minimal converter: headings, blockquote, bold, line breaks
        return md
            .replace(/^# (.*)$/gm, '<h1>$1</h1>')
            .replace(/^> (.*)$/gm, '<blockquote>$1</blockquote>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n- (.*)/g, '<br>• $1')
            .replace(/\n/g, '<br>');
    }
    return (<div className={signals_module_css_1.default.container}>
      <h1>Signals</h1>
      {!snapshot ? (<p>Loading snapshot…</p>) : (<>
          <div className={signals_module_css_1.default.banner}>
            <strong>Banner:</strong> {snapshot.banner}
          </div>
          <div className={signals_module_css_1.default.tiers}>
            <strong>Tiers:</strong> Alpha {snapshot.tier_counts.Alpha} | Beta{' '}
            {snapshot.tier_counts.Beta} | Gamma {snapshot.tier_counts.Gamma} | Delta{' '}
            {snapshot.tier_counts.Delta}
          </div>
          <div className={signals_module_css_1.default.bulletin}>
            <strong>Bulletin:</strong>
            <div dangerouslySetInnerHTML={{ __html: bulletin }}/>
          </div>
        </>)}
    </div>);
}
