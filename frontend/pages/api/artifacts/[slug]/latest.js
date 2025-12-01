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
exports.default = handler;
var fs_1 = require("fs");
var path_1 = require("path");
// Mock data generator for development
function generateMockArtifact(slug) {
    var mockPicks = [
        {
            symbol: 'AAPL',
            tier: 'Alpha',
            target_weight: 0.15,
            rationale: 'Strong fundamentals with consistent revenue growth and robust ecosystem lock-in effects.',
            risk_factors: ['Regulatory pressure in key markets', 'Supply chain dependencies'],
        },
        {
            symbol: 'GOOGL',
            tier: 'Alpha',
            target_weight: 0.12,
            rationale: 'Dominant position in search and advertising with growing cloud business.',
            risk_factors: ['Antitrust regulations', 'Competition in cloud services'],
        },
        {
            symbol: 'MSFT',
            tier: 'Beta',
            target_weight: 0.1,
            rationale: 'Leading cloud infrastructure and productivity software suite.',
            risk_factors: ['Market saturation', 'Cybersecurity threats'],
        },
        {
            symbol: 'NVDA',
            tier: 'Beta',
            target_weight: 0.08,
            rationale: 'AI and data center growth driving semiconductor demand.',
            risk_factors: ['Cyclical semiconductor market', 'Geopolitical tensions'],
        },
        {
            symbol: 'TSLA',
            tier: 'Gamma',
            target_weight: 0.05,
            rationale: 'Electric vehicle market leadership with energy storage expansion.',
            risk_factors: ['Execution risk on scaling', 'Increased competition', 'Regulatory changes'],
        },
    ];
    return {
        title: "".concat(slug.replace('-', ' ').toUpperCase(), " Market Analysis"),
        capsule_slug: slug,
        generated_at: new Date().toISOString(),
        execution_id: "".concat(slug, "_").concat(Date.now()),
        status: 'success',
        banner: "\uD83C\uDFAF Strategic market positioning analysis for ".concat(slug, " capsule. Comprehensive tier-based allocation strategy designed for optimal risk-adjusted returns while maintaining sovereign operational independence."),
        tier_counts: {
            Alpha: mockPicks.filter(function (p) { return p.tier === 'Alpha'; }).length,
            Beta: mockPicks.filter(function (p) { return p.tier === 'Beta'; }).length,
            Gamma: mockPicks.filter(function (p) { return p.tier === 'Gamma'; }).length,
            Delta: mockPicks.filter(function (p) { return p.tier === 'Delta'; }).length,
        },
        picks: mockPicks,
        metadata: {
            archive_version: '1.0',
            archiver: 'local_fallback',
            timestamp: new Date().toISOString(),
            total_weight: mockPicks.reduce(function (sum, pick) { return sum + pick.target_weight; }, 0),
        },
    };
}
function loadArtifactFromArchive(slug) {
    return __awaiter(this, void 0, void 0, function () {
        var archivePath_1, years, latestYear, yearPath_1, months, latestMonth, monthPath_1, days, latestDay, dayPath, files, latestFile, filePath, fileContent, archiveData, artifact, recommendations, generatedPicks;
        var _a, _b, _c;
        return __generator(this, function (_d) {
            try {
                archivePath_1 = path_1.default.join(process.cwd(), '..', 'archives', 'snapshots', slug);
                if (!fs_1.default.existsSync(archivePath_1)) {
                    console.log("No archive found for ".concat(slug, ", generating mock data"));
                    return [2 /*return*/, generateMockArtifact(slug)];
                }
                years = fs_1.default
                    .readdirSync(archivePath_1)
                    .filter(function (item) { return fs_1.default.statSync(path_1.default.join(archivePath_1, item)).isDirectory(); });
                if (years.length === 0) {
                    return [2 /*return*/, generateMockArtifact(slug)];
                }
                latestYear = years.sort().pop();
                yearPath_1 = path_1.default.join(archivePath_1, latestYear);
                months = fs_1.default
                    .readdirSync(yearPath_1)
                    .filter(function (item) { return fs_1.default.statSync(path_1.default.join(yearPath_1, item)).isDirectory(); });
                if (months.length === 0) {
                    return [2 /*return*/, generateMockArtifact(slug)];
                }
                latestMonth = months.sort().pop();
                monthPath_1 = path_1.default.join(yearPath_1, latestMonth);
                days = fs_1.default
                    .readdirSync(monthPath_1)
                    .filter(function (item) { return fs_1.default.statSync(path_1.default.join(monthPath_1, item)).isDirectory(); });
                if (days.length === 0) {
                    return [2 /*return*/, generateMockArtifact(slug)];
                }
                latestDay = days.sort().pop();
                dayPath = path_1.default.join(monthPath_1, latestDay);
                files = fs_1.default.readdirSync(dayPath).filter(function (file) { return file.endsWith('.json'); });
                if (files.length === 0) {
                    return [2 /*return*/, generateMockArtifact(slug)];
                }
                latestFile = files.sort().pop();
                filePath = path_1.default.join(dayPath, latestFile);
                fileContent = fs_1.default.readFileSync(filePath, 'utf-8');
                archiveData = JSON.parse(fileContent);
                artifact = {
                    title: "".concat(slug.replace('-', ' ').toUpperCase(), " Execution Result"),
                    capsule_slug: slug,
                    generated_at: ((_a = archiveData.metadata) === null || _a === void 0 ? void 0 : _a.timestamp) || new Date().toISOString(),
                    execution_id: ((_b = archiveData.data) === null || _b === void 0 ? void 0 : _b.execution_id) || "".concat(slug, "_archived"),
                    status: 'success',
                    banner: "\uD83D\uDCCA Archived execution data for ".concat(slug, " capsule. This represents a historical snapshot of system execution and performance metrics."),
                    tier_counts: {
                        Alpha: 0,
                        Beta: 0,
                        Gamma: 0,
                        Delta: 0,
                    },
                    picks: [],
                    metadata: archiveData.metadata || {},
                    raw_data: archiveData.data,
                };
                // If it's a signals-daily capsule with market data, create picks
                if (slug === 'signals-daily' && ((_c = archiveData.data) === null || _c === void 0 ? void 0 : _c.market_data)) {
                    recommendations = archiveData.data.recommendations || [];
                    generatedPicks = recommendations.map(function (rec, index) { return ({
                        symbol: "SIGNAL_".concat(index + 1),
                        tier: ['Alpha', 'Beta', 'Gamma'][index % 3],
                        target_weight: Math.random() * 0.1 + 0.05,
                        rationale: rec,
                        risk_factors: ['Market volatility', 'Execution risk'],
                    }); });
                    artifact.picks = generatedPicks;
                    // Update tier counts
                    artifact.tier_counts = {
                        Alpha: generatedPicks.filter(function (p) { return p.tier === 'Alpha'; }).length,
                        Beta: generatedPicks.filter(function (p) { return p.tier === 'Beta'; }).length,
                        Gamma: generatedPicks.filter(function (p) { return p.tier === 'Gamma'; }).length,
                        Delta: generatedPicks.filter(function (p) { return p.tier === 'Delta'; }).length,
                    };
                }
                return [2 /*return*/, artifact];
            }
            catch (error) {
                console.error('Error loading artifact from archive:', error);
                return [2 /*return*/, generateMockArtifact(slug)];
            }
            return [2 /*return*/];
        });
    });
}
function handler(req, res) {
    return __awaiter(this, void 0, void 0, function () {
        var slug, artifact, error_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    if (req.method !== 'GET') {
                        return [2 /*return*/, res.status(405).json({ error: 'Method not allowed' })];
                    }
                    slug = req.query.slug;
                    if (!slug || typeof slug !== 'string') {
                        return [2 /*return*/, res.status(400).json({ error: 'Invalid capsule slug' })];
                    }
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, loadArtifactFromArchive(slug)];
                case 2:
                    artifact = _a.sent();
                    res.status(200).json(artifact);
                    return [3 /*break*/, 4];
                case 3:
                    error_1 = _a.sent();
                    console.error('API error:', error_1);
                    res.status(500).json({
                        error: 'Failed to load artifact',
                        message: error_1 instanceof Error ? error_1.message : 'Unknown error',
                    });
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/];
            }
        });
    });
}
