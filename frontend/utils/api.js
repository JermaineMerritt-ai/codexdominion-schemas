"use strict";
// utils/api.ts
/**
 * 🔥 CODEX SIGNALS API CLIENT 📊
 * TypeScript utilities for frontend integration
 *
 * The Merritt Method™ - Frontend Portfolio Intelligence
 */
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
exports.SignalsUtils = exports.CodexSignalsAPI = void 0;
exports.useCodexSignals = useCodexSignals;
var CodexSignalsAPI = /** @class */ (function () {
    function CodexSignalsAPI(baseURL) {
        this.baseURL = baseURL;
    }
    /**
     * Generate daily signals with market data and positions
     */
    CodexSignalsAPI.prototype.generateDailySignals = function (market, positions) {
        return __awaiter(this, void 0, void 0, function () {
            var response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, fetch("".concat(this.baseURL, "/signals/daily"), {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ market: market, positions: positions }),
                        })];
                    case 1:
                        response = _a.sent();
                        if (!response.ok) {
                            throw new Error("HTTP ".concat(response.status, ": ").concat(response.statusText));
                        }
                        return [4 /*yield*/, response.json()];
                    case 2: return [2 /*return*/, _a.sent()];
                }
            });
        });
    };
    /**
     * Get mock signals for testing
     */
    CodexSignalsAPI.prototype.getMockSignals = function () {
        return __awaiter(this, void 0, void 0, function () {
            var response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, fetch("".concat(this.baseURL, "/signals/mock"))];
                    case 1:
                        response = _a.sent();
                        if (!response.ok) {
                            throw new Error("HTTP ".concat(response.status, ": ").concat(response.statusText));
                        }
                        return [4 /*yield*/, response.json()];
                    case 2: return [2 /*return*/, _a.sent()];
                }
            });
        });
    };
    /**
     * Generate formatted bulletin
     */
    CodexSignalsAPI.prototype.generateBulletin = function () {
        return __awaiter(this, arguments, void 0, function (format) {
            var response;
            if (format === void 0) { format = 'md'; }
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, fetch("".concat(this.baseURL, "/signals/bulletin?format=").concat(format), {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                        })];
                    case 1:
                        response = _a.sent();
                        if (!response.ok) {
                            throw new Error("HTTP ".concat(response.status, ": ").concat(response.statusText));
                        }
                        return [4 /*yield*/, response.json()];
                    case 2: return [2 /*return*/, _a.sent()];
                }
            });
        });
    };
    /**
     * Check API health
     */
    CodexSignalsAPI.prototype.healthCheck = function () {
        return __awaiter(this, void 0, void 0, function () {
            var response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, fetch("".concat(this.baseURL, "/signals/health"))];
                    case 1:
                        response = _a.sent();
                        if (!response.ok) {
                            throw new Error("HTTP ".concat(response.status, ": ").concat(response.statusText));
                        }
                        return [4 /*yield*/, response.json()];
                    case 2: return [2 /*return*/, _a.sent()];
                }
            });
        });
    };
    /**
     * Get engine configuration
     */
    CodexSignalsAPI.prototype.getEngineConfig = function () {
        return __awaiter(this, void 0, void 0, function () {
            var response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, fetch("".concat(this.baseURL, "/signals/engine/config"))];
                    case 1:
                        response = _a.sent();
                        if (!response.ok) {
                            throw new Error("HTTP ".concat(response.status, ": ").concat(response.statusText));
                        }
                        return [4 /*yield*/, response.json()];
                    case 2: return [2 /*return*/, _a.sent()];
                }
            });
        });
    };
    return CodexSignalsAPI;
}());
exports.CodexSignalsAPI = CodexSignalsAPI;
/**
 * Utility functions for frontend
 */
exports.SignalsUtils = {
    /**
     * Convert Markdown to HTML (minimal implementation)
     */
    mdToHtml: function (markdown) {
        return markdown
            .replace(/^# (.*)$/gm, '<h1>$1</h1>')
            .replace(/^## (.*)$/gm, '<h2>$1</h2>')
            .replace(/^> (.*)$/gm, '<blockquote>$1</blockquote>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n- (.*)/g, '<br>• $1')
            .replace(/\n/g, '<br>');
    },
    /**
     * Generate bulletin markdown from snapshot
     */
    generateBulletinMD: function (snapshot) {
        var header = "# Daily Signals \u2014 ".concat(snapshot.generated_at, "\n\n");
        var banner = "> ".concat(snapshot.banner, "\n\n");
        var tiers = "- Alpha: ".concat(snapshot.tier_counts.Alpha, "\n- Beta: ").concat(snapshot.tier_counts.Beta, "\n- Gamma: ").concat(snapshot.tier_counts.Gamma, "\n- Delta: ").concat(snapshot.tier_counts.Delta, "\n\n");
        var body = (snapshot.picks || [])
            .map(function (p) { var _a; return "**".concat(p.symbol, "** \u2014 Tier ").concat(p.tier, " | target ").concat((p.target_weight * 100).toFixed(2), "%\n- Rationale: ").concat(p.rationale, "\n- Risks: ").concat(((_a = p.risk_factors) === null || _a === void 0 ? void 0 : _a.join(', ')) || 'None', "\n"); })
            .join('\n');
        return header + banner + tiers + body;
    },
    /**
     * Format weight as percentage
     */
    formatWeight: function (weight) {
        return "".concat((weight * 100).toFixed(2), "%");
    },
    /**
     * Get tier color for UI
     */
    getTierColor: function (tier) {
        var colors = {
            Alpha: '#10b981',
            Beta: '#3b82f6',
            Gamma: '#f59e0b',
            Delta: '#ef4444',
        };
        return colors[tier] || '#6b7280';
    },
    /**
     * Calculate total allocation
     */
    calculateTotalAllocation: function (picks) {
        return picks.reduce(function (total, pick) { return total + pick.target_weight; }, 0);
    },
    /**
     * Get risk level description
     */
    getRiskDescription: function (tier) {
        var descriptions = {
            Alpha: 'High conviction positions with strong fundamentals',
            Beta: 'Balanced exposure with measured risk/reward',
            Gamma: 'Elevated risk requiring defensive positioning',
            Delta: 'High turbulence - capital preservation priority',
        };
        return descriptions[tier] || 'Unknown risk level';
    },
};
/**
 * React hook for Codex Signals API
 */
function useCodexSignals(baseURL) {
    var api = new CodexSignalsAPI(baseURL);
    return {
        api: api,
        utils: exports.SignalsUtils,
    };
}
