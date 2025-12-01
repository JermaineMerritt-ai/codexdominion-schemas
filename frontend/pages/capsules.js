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
exports.getServerSideProps = void 0;
exports.default = Capsules;
// pages/capsules.tsx
var react_1 = require("react");
var capsules_module_css_1 = require("./capsules.module.css");
function Capsules(_a) {
    var _b = _a.capsules, capsules = _b === void 0 ? [] : _b, _c = _a.runs, runs = _c === void 0 ? [] : _c, error = _a.error;
    var formatDateTime = function (dateStr) {
        return new Date(dateStr).toLocaleString();
    };
    var getModeClass = function (mode) {
        switch (mode) {
            case 'automated':
                return capsules_module_css_1.default.modeAutomated;
            case 'custodian':
                return capsules_module_css_1.default.modeCustodian;
            case 'manual':
                return capsules_module_css_1.default.modeManual;
            default:
                return capsules_module_css_1.default.modeManual;
        }
    };
    var getStatusClass = function (status) {
        switch (status) {
            case 'success':
                return capsules_module_css_1.default.statusSuccess;
            case 'error':
                return capsules_module_css_1.default.statusError;
            case 'running':
                return capsules_module_css_1.default.statusRunning;
            default:
                return capsules_module_css_1.default.statusDefault;
        }
    };
    if (error) {
        return (<div className={capsules_module_css_1.default.container}>
        <h1>Codex Capsules</h1>
        <div className={capsules_module_css_1.default.error}>
          <strong>Error:</strong> {error}
        </div>
      </div>);
    }
    return (<div className={capsules_module_css_1.default.container}>
      <div className={capsules_module_css_1.default.header}>
        <h1 className={capsules_module_css_1.default.title}>🏛️ Codex Capsules Registry</h1>
        <p className={capsules_module_css_1.default.subtitle}>
          Operational sovereignty tracking for ceremonial and technical operations
        </p>
      </div>
      {/* Capsules Section */}
      <section className={capsules_module_css_1.default.section}>
        <h2 className={capsules_module_css_1.default.sectionTitle}>📦 Registered Capsules ({capsules.length})</h2>
        {capsules.length === 0 ? (<p className={capsules_module_css_1.default.italic}>No capsules registered yet.</p>) : (<div className={capsules_module_css_1.default.grid}>
            {capsules.map(function (c) { return (<div key={c.slug} className={capsules_module_css_1.default.capsuleCard}>
                <div className={capsules_module_css_1.default.capsuleHeader}>
                  <h3 className={capsules_module_css_1.default.capsuleTitle}>{c.title}</h3>
                  <span className={c.status === 'active'
                    ? capsules_module_css_1.default.capsuleStatusActive
                    : capsules_module_css_1.default.capsuleStatusInactive}>
                    {c.status.toUpperCase()}
                  </span>
                </div>
                <div className={capsules_module_css_1.default.capsuleGrid}>
                  <div>
                    <strong>Slug:</strong> <code className={capsules_module_css_1.default.capsuleSlug}>{c.slug}</code>
                  </div>
                  <div>
                    <strong>Kind:</strong> {c.kind}
                  </div>
                  <div>
                    <strong>Mode:</strong>
                    <span className={"".concat(capsules_module_css_1.default.capsuleMode, " ").concat(getModeClass(c.mode))}>
                      {c.mode}
                    </span>
                  </div>
                  <div>
                    <strong>Version:</strong> {c.version}
                  </div>
                  <div>
                    <strong>Schedule:</strong> {c.schedule || '—'}
                  </div>
                </div>
                {c.entrypoint && (<div className={capsules_module_css_1.default.capsuleEntrypoint}>
                    <strong>Entrypoint:</strong>
                    <code className={capsules_module_css_1.default.capsuleEntrypointCode}>{c.entrypoint}</code>
                  </div>)}
              </div>); })}
          </div>)}
      </section>
      {/* Recent Runs Section */}
      <section>
        <h2 className={capsules_module_css_1.default.sectionTitle}>🚀 Recent Execution Runs ({runs.length})</h2>
        {runs.length === 0 ? (<p className={capsules_module_css_1.default.italic}>No execution runs recorded yet.</p>) : (<div className={capsules_module_css_1.default.runGrid}>
            {runs.slice(0, 20).map(function (r, i) { return (<div key={i} className={capsules_module_css_1.default.runCard}>
                <div className={capsules_module_css_1.default.runHeader}>
                  <div>
                    <strong>{r.capsule_slug}</strong> executed by <em>{r.actor}</em>
                  </div>
                  <div className={capsules_module_css_1.default.flexRow}>
                    <span className={"".concat(capsules_module_css_1.default.runStatus, " ").concat(getStatusClass(r.status))}>●</span>
                    <span className={capsules_module_css_1.default.runDate}>{formatDateTime(r.started_at)}</span>
                  </div>
                </div>
                {r.artifact_uri && (<div className={capsules_module_css_1.default.runArtifact}>
                    📦 Artifact:
                    <a href={r.artifact_uri} className={capsules_module_css_1.default.runArtifactLink} target="_blank" rel="noopener noreferrer">
                      {r.artifact_uri.split('/').pop()}
                    </a>
                  </div>)}
              </div>); })}
          </div>)}
      </section>
    </div>);
}
var getServerSideProps = function () { return __awaiter(void 0, void 0, void 0, function () {
    var capsulesResponse, runsResponse, capsules, runs, error_1;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                _a.trys.push([0, 7, , 8]);
                return [4 /*yield*/, fetch('http://localhost:8080/api/capsules', {
                        method: 'GET',
                        headers: { Accept: 'application/json' },
                    })];
            case 1:
                capsulesResponse = _a.sent();
                return [4 /*yield*/, fetch('http://localhost:8080/api/capsules/runs', {
                        method: 'GET',
                        headers: { Accept: 'application/json' },
                    })];
            case 2:
                runsResponse = _a.sent();
                capsules = [];
                runs = [];
                if (!(capsulesResponse.ok && runsResponse.ok)) return [3 /*break*/, 5];
                return [4 /*yield*/, capsulesResponse.json()];
            case 3:
                capsules = _a.sent();
                return [4 /*yield*/, runsResponse.json()];
            case 4:
                runs = _a.sent();
                return [3 /*break*/, 6];
            case 5:
                // Fallback to mock data
                capsules = [
                    {
                        slug: 'signals-daily',
                        title: 'Daily Signals Engine',
                        kind: 'engine',
                        mode: 'custodian',
                        version: '2.0.0',
                        status: 'active',
                        entrypoint: 'POST https://codex-signals.run.app/signals/daily',
                        schedule: '0 6 * * *',
                        created_at: new Date().toISOString(),
                        updated_at: new Date().toISOString(),
                    },
                ];
                runs = [
                    {
                        id: 1,
                        capsule_slug: 'signals-daily',
                        actor: 'system-scheduler',
                        status: 'success',
                        started_at: new Date().toISOString(),
                        artifact_uri: 'https://storage.googleapis.com/codex-artifacts/signals-daily-20251108.tar.gz',
                    },
                ];
                _a.label = 6;
            case 6: return [2 /*return*/, {
                    props: {
                        capsules: capsules,
                        runs: runs,
                    },
                }];
            case 7:
                error_1 = _a.sent();
                console.error('Error fetching capsules data:', error_1);
                // Return mock data on error
                return [2 /*return*/, {
                        props: {
                            capsules: [
                                {
                                    slug: 'signals-daily',
                                    title: 'Daily Signals Engine (Demo)',
                                    kind: 'engine',
                                    mode: 'custodian',
                                    version: '2.0.0',
                                    status: 'active',
                                    entrypoint: 'POST https://codex-signals.run.app/signals/daily',
                                    schedule: '0 6 * * *',
                                    created_at: new Date().toISOString(),
                                    updated_at: new Date().toISOString(),
                                },
                            ],
                            runs: [
                                {
                                    id: 1,
                                    capsule_slug: 'signals-daily',
                                    actor: 'system-scheduler',
                                    status: 'success',
                                    started_at: new Date().toISOString(),
                                    artifact_uri: 'https://storage.googleapis.com/codex-artifacts/signals-daily-demo.tar.gz',
                                },
                            ],
                            error: 'Could not connect to Capsules API - showing demo data',
                        },
                    }];
            case 8: return [2 /*return*/];
        }
    });
}); };
exports.getServerSideProps = getServerSideProps;
