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
exports.default = FestivalCeremonyPanel;
var react_1 = require("react");
function FestivalCeremonyPanel(_a) {
    var _this = this;
    var kind = _a.kind;
    var _b = (0, react_1.useState)(null), ceremonialData = _b[0], setCeremonialData = _b[1];
    var _c = (0, react_1.useState)(true), loading = _c[0], setLoading = _c[1];
    var _d = (0, react_1.useState)(null), error = _d[0], setError = _d[1];
    (0, react_1.useEffect)(function () {
        var fetchCeremonialData = function () { return __awaiter(_this, void 0, void 0, function () {
            var params, response, data, err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        setLoading(true);
                        setError(null);
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 4, 5, 6]);
                        params = new URLSearchParams();
                        if (kind) {
                            params.append('kind', kind);
                        }
                        return [4 /*yield*/, fetch("/api/ceremony?".concat(params.toString()))];
                    case 2:
                        response = _a.sent();
                        if (!response.ok) {
                            throw new Error("Failed to fetch ceremonial data: ".concat(response.statusText));
                        }
                        return [4 /*yield*/, response.json()];
                    case 3:
                        data = _a.sent();
                        setCeremonialData(data);
                        return [3 /*break*/, 6];
                    case 4:
                        err_1 = _a.sent();
                        setError(err_1 instanceof Error ? err_1.message : 'Unknown error occurred');
                        return [3 /*break*/, 6];
                    case 5:
                        setLoading(false);
                        return [7 /*endfinally*/];
                    case 6: return [2 /*return*/];
                }
            });
        }); };
        fetchCeremonialData();
    }, [kind]);
    var getCeremonialIcon = function (kind) {
        switch (kind) {
            case 'proclamation':
                return '📢';
            case 'silence':
                return '🤫';
            case 'blessing':
                return '🙏';
            default:
                return '🕯️';
        }
    };
    var getCeremonialColor = function (kind) {
        switch (kind) {
            case 'proclamation':
                return 'text-orange-700 bg-orange-100 border-orange-300';
            case 'silence':
                return 'text-slate-700 bg-slate-100 border-slate-300';
            case 'blessing':
                return 'text-emerald-700 bg-emerald-100 border-emerald-300';
            default:
                return 'text-indigo-700 bg-indigo-100 border-indigo-300';
        }
    };
    var getCeremonialBgClass = function (kind) {
        switch (kind) {
            case 'proclamation':
                return 'bg-orange-50 border-l-orange-400';
            case 'silence':
                return 'bg-slate-50 border-l-slate-400';
            case 'blessing':
                return 'bg-emerald-50 border-l-emerald-400';
            default:
                return 'bg-indigo-50 border-l-indigo-400';
        }
    };
    if (loading) {
        return (<div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-2 text-gray-600">Loading ceremonial inscriptions...</p>
        </div>
      </div>);
    }
    if (error) {
        return (<div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <p className="text-red-800 font-medium">Error loading ceremonial data</p>
        <p className="text-red-600 text-sm mt-2">{error}</p>
      </div>);
    }
    // Get cycles from fetched data
    var ceremonialCycles = (ceremonialData === null || ceremonialData === void 0 ? void 0 : ceremonialData.cycles) || [];
    if (!ceremonialCycles || ceremonialCycles.length === 0) {
        return (<div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <span className="mr-2">{kind ? getCeremonialIcon(kind) : '🕯️'}</span>
          {kind ? "Sacred ".concat(kind.charAt(0).toUpperCase() + kind.slice(1), "s") : 'Festival Ceremony'}
        </h2>
        <div className="text-center py-8">
          <div className="text-gray-400 text-4xl mb-4">🕯️</div>
          <p className="text-gray-600 italic">
            {kind
                ? "No ".concat(kind, "s have been inscribed yet. The sacred altar awaits your first ").concat(kind, ".")
                : 'No ceremonial inscriptions yet. The sacred altar awaits your first ceremony.'}
          </p>
          <div className="mt-4 text-sm text-gray-500">
            <p>Sacred ceremonies available:</p>
            <div className="flex justify-center space-x-4 mt-2">
              <span>📢 Proclamations</span>
              <span>🤫 Silences</span>
              <span>🙏 Blessings</span>
            </div>
          </div>
        </div>
      </div>);
    }
    return (<div className="bg-white border border-gray-200 rounded-lg shadow-sm">
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-xl font-bold text-gray-800 flex items-center">
          <span className="mr-2">{kind ? getCeremonialIcon(kind) : '🕯️'}</span>
          {kind ? "Sacred ".concat(kind.charAt(0).toUpperCase() + kind.slice(1), "s") : 'Sacred Ceremonies'}
          <span className="ml-2 text-sm font-normal text-gray-500">
            ({ceremonialCycles.length} {kind ? kind + 's' : 'inscriptions'})
          </span>
        </h2>
        <p className="text-sm text-gray-600 mt-1">
          Sacred proclamations, silences, and blessings inscribed in the eternal bulletin
        </p>
      </div>

      <div className="p-4">
        <div className="space-y-4 max-h-96 overflow-y-auto">
          {ceremonialCycles.map(function (cycle, index) {
            var _a, _b;
            return (<div key={cycle.cycle_id || index} className="border rounded-lg overflow-hidden hover:shadow-md transition-shadow duration-200">
              {/* Header with ceremony kind and timestamp */}
              <div className="flex items-start justify-between p-4 border-b border-gray-100">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">{getCeremonialIcon(cycle.kind)}</span>
                  <div>
                    <span className={"inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ".concat(getCeremonialColor(cycle.kind))}>
                      {cycle.kind.toUpperCase()}
                    </span>
                    <p className="text-xs text-gray-500 mt-1">{cycle.cycle_id}</p>
                  </div>
                </div>

                <div className="text-right">
                  <p className="text-sm font-medium text-gray-900">
                    {new Date(cycle.timestamp).toLocaleString()}
                  </p>
                  <p className="text-xs text-gray-500">{cycle.rite}</p>
                </div>
              </div>

              {/* Ceremonial message */}
              <div className={"p-4 border-l-4 ".concat(getCeremonialBgClass(cycle.kind))}>
                <div className="flex items-start space-x-3">
                  <div className="flex-1">
                    <p className="text-gray-800 font-medium text-base leading-relaxed">
                      {cycle.message}
                    </p>

                    {/* Show formatted proclamation if available */}
                    {cycle.proclamation && cycle.proclamation !== cycle.message && (<details className="mt-3">
                        <summary className="text-sm text-gray-600 cursor-pointer hover:text-gray-800">
                          View Sacred Formatting
                        </summary>
                        <div className="mt-2 p-3 bg-white bg-opacity-50 rounded border text-sm text-gray-700 whitespace-pre-line">
                          {cycle.proclamation}
                        </div>
                      </details>)}
                  </div>
                </div>
              </div>

              {/* Footer with metadata */}
              <div className="px-4 py-2 bg-gray-50 border-t border-gray-100">
                <div className="flex items-center justify-between text-xs text-gray-500">
                  <span>
                    Flame:{' '}
                    <span className="font-mono">{(_a = cycle.flame_status) === null || _a === void 0 ? void 0 : _a.replace('_', ' ')}</span>
                  </span>
                  <span>
                    Checksum:{' '}
                    <span className="font-mono">{(_b = cycle.sacred_checksum) === null || _b === void 0 ? void 0 : _b.substring(0, 8)}...</span>
                  </span>
                </div>
              </div>
            </div>);
        })}
        </div>
      </div>

      {/* Footer with ceremonial stats */}
      <div className="px-6 py-3 bg-gray-50 border-t border-gray-200 rounded-b-lg">
        <div className="flex items-center justify-center space-x-6 text-xs text-gray-600">
          {(function () {
            var counts = ceremonialCycles.reduce(function (acc, cycle) {
                acc[cycle.kind] = (acc[cycle.kind] || 0) + 1;
                return acc;
            }, {});
            return (<>
                {counts.proclamation && (<span className="flex items-center">
                    📢 <strong className="ml-1">{counts.proclamation}</strong> Proclamations
                  </span>)}
                {counts.silence && (<span className="flex items-center">
                    🤫 <strong className="ml-1">{counts.silence}</strong> Silences
                  </span>)}
                {counts.blessing && (<span className="flex items-center">
                    🙏 <strong className="ml-1">{counts.blessing}</strong> Blessings
                  </span>)}
              </>);
        })()}
        </div>
        <p className="text-xs text-gray-500 text-center mt-2">
          🕯️ Sacred ceremonies preserved in the eternal bulletin
        </p>
      </div>
    </div>);
}
