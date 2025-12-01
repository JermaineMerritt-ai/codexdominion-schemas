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
exports.default = FestivalDashboard;
var react_1 = require("react");
var head_1 = require("next/head");
var FestivalPanel_1 = require("../components/FestivalPanel");
var FestivalCeremonyPanel_1 = require("../components/FestivalCeremonyPanel");
var TabNavigation = function (_a) {
    var activeTab = _a.activeTab, setActiveTab = _a.setActiveTab;
    var tabs = [
        { id: 'overview', label: '🎭 Festival Overview', icon: '🎭' },
        { id: 'cycles', label: '🔄 Festival Cycles', icon: '🔄' },
        { id: 'ceremonies', label: '⚡ Sacred Ceremonies', icon: '⚡' },
        { id: 'proclamations', label: '📢 Proclamations', icon: '📢' },
        { id: 'silences', label: '🤫 Silences', icon: '🤫' },
        { id: 'blessings', label: '🙏 Blessings', icon: '🙏' },
    ];
    return (<div className="flex flex-wrap gap-1 mb-6 p-1 bg-gray-800 rounded-lg">
      {tabs.map(function (tab) { return (<button key={tab.id} onClick={function () { return setActiveTab(tab.id); }} className={"flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all ".concat(activeTab === tab.id
                ? 'bg-indigo-600 text-white shadow-lg'
                : 'text-gray-300 hover:text-white hover:bg-gray-700')}>
          <span>{tab.icon}</span>
          <span className="hidden sm:inline">{tab.label.split(' ').slice(1).join(' ')}</span>
          <span className="sm:hidden">{tab.icon}</span>
        </button>); })}
    </div>);
};
function FestivalDashboard() {
    var _this = this;
    var _a = (0, react_1.useState)('overview'), activeTab = _a[0], setActiveTab = _a[1];
    var _b = (0, react_1.useState)(null), festivalData = _b[0], setFestivalData = _b[1];
    var _c = (0, react_1.useState)(null), ceremonyData = _c[0], setCeremonyData = _c[1];
    var _d = (0, react_1.useState)(true), loading = _d[0], setLoading = _d[1];
    var _e = (0, react_1.useState)(null), error = _e[0], setError = _e[1];
    var _f = (0, react_1.useState)('all'), selectedType = _f[0], setSelectedType = _f[1];
    var _g = (0, react_1.useState)(10), limit = _g[0], setLimit = _g[1];
    var fetchFestivalData = function () { return __awaiter(_this, void 0, void 0, function () {
        var params, _a, festivalResponse, ceremonyResponse, festivalData_1, ceremonyData_1, err_1;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    setLoading(true);
                    setError(null);
                    _b.label = 1;
                case 1:
                    _b.trys.push([1, 6, 7, 8]);
                    params = new URLSearchParams();
                    if (selectedType !== 'all') {
                        params.append('ceremony_type', selectedType);
                    }
                    params.append('limit', limit.toString());
                    return [4 /*yield*/, Promise.all([
                            fetch("/api/festival?".concat(params.toString())),
                            fetch('/api/ceremony'),
                        ])];
                case 2:
                    _a = _b.sent(), festivalResponse = _a[0], ceremonyResponse = _a[1];
                    if (!festivalResponse.ok) {
                        throw new Error("Failed to fetch festival data: ".concat(festivalResponse.statusText));
                    }
                    return [4 /*yield*/, festivalResponse.json()];
                case 3:
                    festivalData_1 = _b.sent();
                    setFestivalData(festivalData_1);
                    if (!ceremonyResponse.ok) return [3 /*break*/, 5];
                    return [4 /*yield*/, ceremonyResponse.json()];
                case 4:
                    ceremonyData_1 = _b.sent();
                    setCeremonyData(ceremonyData_1);
                    _b.label = 5;
                case 5: return [3 /*break*/, 8];
                case 6:
                    err_1 = _b.sent();
                    setError(err_1 instanceof Error ? err_1.message : 'Unknown error occurred');
                    return [3 /*break*/, 8];
                case 7:
                    setLoading(false);
                    return [7 /*endfinally*/];
                case 8: return [2 /*return*/];
            }
        });
    }); };
    (0, react_1.useEffect)(function () {
        fetchFestivalData();
    }, [selectedType, limit]);
    var getFlameStatusDisplay = function (status) {
        switch (status) {
            case 'burning_bright':
                return '🔥 Burning Bright';
            case 'burning_local':
                return '🏠 Local Flame';
            case 'awaiting_ignition':
                return '🕯️ Awaiting Ignition';
            default:
                return '✨ Unknown Status';
        }
    };
    var formatCeremonyType = function (type) {
        return type.replace(/_/g, ' ').replace(/\b\w/g, function (l) { return l.toUpperCase(); });
    };
    var OverviewPanel = function () {
        var _a, _b, _c, _d, _e;
        return (<div className="space-y-6">
      {/* Festival Overview Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl p-6 text-white">
        <h2 className="text-2xl font-bold mb-4">🎭 Codex Festival Dashboard</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
            <div className="text-sm text-indigo-200">Festival Cycles</div>
            <div className="text-2xl font-bold">{(festivalData === null || festivalData === void 0 ? void 0 : festivalData.total_ceremonies) || 0}</div>
          </div>
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
            <div className="text-sm text-purple-200">Sacred Ceremonies</div>
            <div className="text-2xl font-bold">{(ceremonyData === null || ceremonyData === void 0 ? void 0 : ceremonyData.total_ceremonies) || 0}</div>
          </div>
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
            <div className="text-sm text-blue-200">Flame Status</div>
            <div className="text-lg font-semibold capitalize">
              {((_b = (_a = ceremonyData === null || ceremonyData === void 0 ? void 0 : ceremonyData.metadata) === null || _a === void 0 ? void 0 : _a.flame_status) === null || _b === void 0 ? void 0 : _b.replace(/_/g, ' ')) ||
                ((_d = (_c = festivalData === null || festivalData === void 0 ? void 0 : festivalData.metadata) === null || _c === void 0 ? void 0 : _c.flame_status) === null || _d === void 0 ? void 0 : _d.replace(/_/g, ' ')) ||
                'Dormant'}
            </div>
          </div>
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
            <div className="text-sm text-green-200">Last Activity</div>
            <div className="text-sm">
              {(festivalData === null || festivalData === void 0 ? void 0 : festivalData.last_ceremony)
                ? new Date(festivalData.last_ceremony).toLocaleDateString()
                : 'No Activity'}
            </div>
          </div>
        </div>
      </div>

      {/* Ceremonial Statistics */}
      {((_e = ceremonyData === null || ceremonyData === void 0 ? void 0 : ceremonyData.metadata) === null || _e === void 0 ? void 0 : _e.ceremonial_stats) && (<div className="bg-white rounded-xl p-6 border border-gray-200">
          <h3 className="text-xl font-bold text-gray-900 mb-4">⚡ Ceremonial Activity</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-center gap-2 text-red-600 mb-2">
                <span>📢</span>
                <span className="font-semibold">Proclamations</span>
              </div>
              <div className="text-2xl font-bold text-gray-900">
                {ceremonyData.metadata.ceremonial_stats.proclamation || 0}
              </div>
            </div>
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-center gap-2 text-blue-600 mb-2">
                <span>🤫</span>
                <span className="font-semibold">Sacred Silences</span>
              </div>
              <div className="text-2xl font-bold text-gray-900">
                {ceremonyData.metadata.ceremonial_stats.silence || 0}
              </div>
            </div>
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-center gap-2 text-green-600 mb-2">
                <span>🙏</span>
                <span className="font-semibold">Divine Blessings</span>
              </div>
              <div className="text-2xl font-bold text-gray-900">
                {ceremonyData.metadata.ceremonial_stats.blessing || 0}
              </div>
            </div>
          </div>
        </div>)}

      {/* Recent Activity Preview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl p-6 border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">🔄 Recent Festival Cycles</h3>
          <div className="text-gray-500 text-sm">
            Switch to "Festival Cycles" tab to view detailed cycle information
          </div>
        </div>
        <div className="bg-white rounded-xl p-6 border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">⚡ Recent Ceremonies</h3>
          <div className="text-gray-500 text-sm">
            Switch to "Sacred Ceremonies" tab to view ceremonial inscriptions
          </div>
        </div>
      </div>
    </div>);
    };
    var renderTabContent = function () {
        switch (activeTab) {
            case 'overview':
                return <OverviewPanel />;
            case 'cycles':
                return (<div>
            {/* Filters */}
            <div className="bg-white p-4 rounded-lg border border-gray-200 mb-6">
              <div className="flex flex-wrap items-center gap-4">
                <div>
                  <label htmlFor="ceremony-type" className="block text-sm font-medium text-gray-700 mb-1">
                    Ceremony Type
                  </label>
                  <select id="ceremony-type" value={selectedType} onChange={function (e) { return setSelectedType(e.target.value); }} className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" aria-label="Select ceremony type" title="Select ceremony type">
                    <option value="all">All Ceremonies</option>
                    {festivalData === null || festivalData === void 0 ? void 0 : festivalData.metadata.ceremony_types.map(function (type) { return (<option key={type} value={type}>
                        {formatCeremonyType(type)}
                      </option>); })}
                  </select>
                </div>

                <div>
                  <label htmlFor="limit" className="block text-sm font-medium text-gray-700 mb-1">
                    Show Recent
                  </label>
                  <select id="limit" value={limit} onChange={function (e) { return setLimit(parseInt(e.target.value)); }} className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" aria-label="Select number of recent ceremonies to show" title="Select number of recent ceremonies to show">
                    <option value={5}>5 ceremonies</option>
                    <option value={10}>10 ceremonies</option>
                    <option value={25}>25 ceremonies</option>
                    <option value={50}>50 ceremonies</option>
                  </select>
                </div>

                <div className="ml-auto">
                  <button onClick={fetchFestivalData} className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition-colors text-sm font-medium" aria-label="Refresh festival data" title="Refresh festival data">
                    Refresh
                  </button>
                </div>
              </div>
            </div>
            <FestivalPanel_1.default cycles={(festivalData === null || festivalData === void 0 ? void 0 : festivalData.cycles) || []}/>
          </div>);
            case 'ceremonies':
                return <FestivalCeremonyPanel_1.default />;
            case 'proclamations':
                return <FestivalCeremonyPanel_1.default kind="proclamation"/>;
            case 'silences':
                return <FestivalCeremonyPanel_1.default kind="silence"/>;
            case 'blessings':
                return <FestivalCeremonyPanel_1.default kind="blessing"/>;
            default:
                return <OverviewPanel />;
        }
    };
    if (loading) {
        return (<>
        <head_1.default>
          <title>Festival Dashboard - Codex Dominion</title>
          <meta name="description" content="Sacred Festival and Ceremonial Management Dashboard"/>
        </head_1.default>
        <div className="min-h-screen bg-gray-900 py-8">
          <div className="max-w-6xl mx-auto px-4">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-400 mx-auto"></div>
              <p className="mt-4 text-gray-300">Loading sacred ceremonies...</p>
            </div>
          </div>
        </div>
      </>);
    }
    if (error) {
        return (<>
        <head_1.default>
          <title>Festival Dashboard - Codex Dominion</title>
          <meta name="description" content="Sacred Festival and Ceremonial Management Dashboard"/>
        </head_1.default>
        <div className="min-h-screen bg-gray-900 py-8">
          <div className="max-w-6xl mx-auto px-4">
            <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-6 text-center">
              <p className="text-red-400 font-medium">Error loading festival data</p>
              <p className="text-red-300 text-sm mt-2">{error}</p>
              <button onClick={fetchFestivalData} className="mt-4 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition-colors">
                Retry
              </button>
            </div>
          </div>
        </div>
      </>);
    }
    return (<>
      <head_1.default>
        <title>Festival Dashboard - Codex Dominion</title>
        <meta name="description" content="Sacred Festival and Ceremonial Management Dashboard"/>
      </head_1.default>

      <div className="min-h-screen bg-gray-900">
        <div className="container mx-auto px-4 py-8">
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-white mb-2">🎭 Festival Dashboard</h1>
            <p className="text-gray-400">
              Sacred ceremonial management and festival cycle tracking
            </p>
          </div>

          <TabNavigation activeTab={activeTab} setActiveTab={setActiveTab}/>

          <div className="transition-all duration-300">{renderTabContent()}</div>

          {/* Footer */}
          <div className="mt-8 text-center text-sm text-gray-500">
            <p>🕯️ May the eternal flame illuminate all who witness these sacred ceremonies 🕯️</p>
          </div>
        </div>
      </div>
    </>);
}
