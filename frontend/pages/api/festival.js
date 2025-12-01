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
var __spreadArray = (this && this.__spreadArray) || function (to, from, pack) {
    if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
        if (ar || !(i in from)) {
            if (!ar) ar = Array.prototype.slice.call(from, 0, i);
            ar[i] = from[i];
        }
    }
    return to.concat(ar || Array.prototype.slice.call(from));
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = handler;
var fs_1 = require("fs");
var path_1 = require("path");
function handler(req, res) {
    return __awaiter(this, void 0, void 0, function () {
        var festivalFilePath, ceremonialFilePath, festivalData, fileContent, ceremonialContent, ceremonialData, _a, limit, ceremony_type_1, cycles, limitNum, response;
        return __generator(this, function (_b) {
            if (req.method !== 'GET') {
                return [2 /*return*/, res.status(405).json({ error: 'Method not allowed' })];
            }
            try {
                festivalFilePath = path_1.default.join(process.cwd(), '..', 'festival_local_backup.json');
                ceremonialFilePath = path_1.default.join(process.cwd(), '..', 'ceremonial_inscriptions_backup.json');
                festivalData = {
                    codex_festival_status: 'AWAITING_FIRST_CEREMONY',
                    created: new Date().toISOString(),
                    cycles: [],
                    total_ceremonies: 0,
                };
                // Load regular festival data
                if (fs_1.default.existsSync(festivalFilePath)) {
                    fileContent = fs_1.default.readFileSync(festivalFilePath, 'utf-8');
                    festivalData = JSON.parse(fileContent);
                }
                // Load and merge ceremonial inscriptions
                if (fs_1.default.existsSync(ceremonialFilePath)) {
                    ceremonialContent = fs_1.default.readFileSync(ceremonialFilePath, 'utf-8');
                    ceremonialData = JSON.parse(ceremonialContent);
                    if (ceremonialData.cycles && ceremonialData.cycles.length > 0) {
                        // Merge ceremonial cycles with festival cycles
                        festivalData.cycles = __spreadArray(__spreadArray([], (festivalData.cycles || []), true), ceremonialData.cycles, true);
                        festivalData.total_ceremonies = festivalData.cycles.length;
                        // Update status to reflect combined data
                        if (festivalData.codex_festival_status === 'AWAITING_FIRST_CEREMONY') {
                            festivalData.codex_festival_status = 'ACTIVE_WITH_CEREMONIAL';
                        }
                    }
                }
                _a = req.query, limit = _a.limit, ceremony_type_1 = _a.ceremony_type;
                cycles = festivalData.cycles || [];
                // Filter by ceremony type if specified
                if (ceremony_type_1 && typeof ceremony_type_1 === 'string') {
                    cycles = cycles.filter(function (cycle) { return cycle.ceremony_type === ceremony_type_1; });
                }
                // Apply limit if specified
                if (limit && typeof limit === 'string') {
                    limitNum = parseInt(limit, 10);
                    if (!isNaN(limitNum) && limitNum > 0) {
                        cycles = cycles.slice(-limitNum); // Get most recent cycles
                    }
                }
                // Sort by timestamp (most recent first)
                cycles.sort(function (a, b) { return new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime(); });
                response = {
                    status: festivalData.codex_festival_status,
                    total_ceremonies: festivalData.total_ceremonies,
                    last_ceremony: festivalData.last_ceremony,
                    last_updated: festivalData.last_updated,
                    cycles: cycles,
                    metadata: {
                        filtered_count: cycles.length,
                        total_count: festivalData.total_ceremonies,
                        ceremony_types: Array.from(new Set(festivalData.cycles.map(function (c) { return c.ceremony_type; }))),
                        flame_status: festivalData.cycles.length > 0
                            ? festivalData.cycles[festivalData.cycles.length - 1].flame_status
                            : 'awaiting_ignition',
                    },
                };
                res.status(200).json(response);
            }
            catch (error) {
                console.error('Error reading festival data:', error);
                // Return graceful error response
                res.status(500).json({
                    error: 'Failed to read festival data',
                    status: 'ERROR',
                    cycles: [],
                    total_ceremonies: 0,
                    message: 'The eternal flame flickers - festival data temporarily unavailable',
                });
            }
            return [2 /*return*/];
        });
    });
}
