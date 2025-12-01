"use strict";
var __makeTemplateObject = (this && this.__makeTemplateObject) || function (cooked, raw) {
    if (Object.defineProperty) { Object.defineProperty(cooked, "raw", { value: raw }); } else { cooked.raw = raw; }
    return cooked;
};
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
exports.default = CapsulesWithLinks;
var react_1 = require("react");
var styled_components_1 = require("styled-components");
var link_1 = require("next/link");
var Container = styled_components_1.default.div(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 24px;\n"], ["\n  padding: 24px;\n"])));
function CapsulesWithLinks() {
    var _a = (0, react_1.useState)([]), capsules = _a[0], setCapsules = _a[1];
    var _b = (0, react_1.useState)(true), loading = _b[0], setLoading = _b[1];
    var _c = (0, react_1.useState)(null), error = _c[0], setError = _c[1];
    (0, react_1.useEffect)(function () {
        function loadCapsules() {
            return __awaiter(this, void 0, void 0, function () {
                var response, data, localError_1, externalResponse, externalData, mappedCapsules, externalError_1;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            _a.trys.push([0, 3, 9, 10]);
                            setLoading(true);
                            return [4 /*yield*/, fetch('/api/capsules')];
                        case 1:
                            response = _a.sent();
                            if (!response.ok) {
                                throw new Error('Local API unavailable');
                            }
                            return [4 /*yield*/, response.json()];
                        case 2:
                            data = _a.sent();
                            setCapsules(data.capsules || []);
                            return [3 /*break*/, 10];
                        case 3:
                            localError_1 = _a.sent();
                            console.log('Local API unavailable, trying external service...');
                            _a.label = 4;
                        case 4:
                            _a.trys.push([4, 7, , 8]);
                            return [4 /*yield*/, fetch('http://localhost:8080/api/capsules')];
                        case 5:
                            externalResponse = _a.sent();
                            return [4 /*yield*/, externalResponse.json()];
                        case 6:
                            externalData = _a.sent();
                            mappedCapsules = externalData.map(function (c) { return ({
                                slug: c.slug,
                                name: c.title || c.slug,
                                description: "External capsule: ".concat(c.kind, " mode ").concat(c.mode),
                                schedule: c.schedule || 'Not scheduled',
                                archive_type: 'external',
                            }); });
                            setCapsules(mappedCapsules);
                            return [3 /*break*/, 8];
                        case 7:
                            externalError_1 = _a.sent();
                            console.error('Both APIs failed:', { localError: localError_1, externalError: externalError_1 });
                            setError('Unable to load capsules from any source');
                            return [3 /*break*/, 8];
                        case 8: return [3 /*break*/, 10];
                        case 9:
                            setLoading(false);
                            return [7 /*endfinally*/];
                        case 10: return [2 /*return*/];
                    }
                });
            });
        }
        loadCapsules();
    }, []);
    if (loading) {
        return (<Container>
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading capsules...</p>
        </div>
        <style jsx>{"\n          .loading-container {\n            display: flex;\n            flex-direction: column;\n            align-items: center;\n            margin-top: 2rem;\n          }\n          .spinner {\n            width: 40px;\n            height: 40px;\n            border: 4px solid #f3f3f3;\n            border-top: 4px solid #0070f3;\n            border-radius: 50%;\n            animation: spin 1s linear infinite;\n            margin-bottom: 1rem;\n          }\n          @keyframes spin {\n            0% {\n              transform: rotate(0deg);\n            }\n            100% {\n              transform: rotate(360deg);\n            }\n          }\n        "}</style>
      </Container>);
    }
    if (error) {
        return (<Container>
        <h1>❌ Error Loading Capsules</h1>
        <p className="error-message">{error}</p>
        <style jsx>{"\n          .error-message {\n            color: #e74c3c;\n            background: #fdf2f2;\n            padding: 1rem;\n            border-radius: 4px;\n            border-left: 4px solid #e74c3c;\n          }\n        "}</style>
      </Container>);
    }
    return (<Container>
      <div className="header">
        <h1>🏛️ Codex Dominion Capsule Registry</h1>
        <p className="subtitle">Operational sovereignty through autonomous capsule execution</p>
      </div>
      <div className="stats-bar">
        <div className="stat">
          <span className="stat-number">{capsules.length}</span>
          <span className="stat-label">Active Capsules</span>
        </div>
        <div className="stat">
          <span className="stat-number">100%</span>
          <span className="stat-label">Operational</span>
        </div>
        <div className="stat">
          <span className="stat-number">24/7</span>
          <span className="stat-label">Monitoring</span>
        </div>
      </div>
      <div className="capsules-grid">
        {capsules.map(function (capsule) { return (<link_1.default key={capsule.slug} href={"/capsule/".concat(capsule.slug)}>
            <div className="capsule-card">
              <div className="capsule-header">
                <h3>{capsule.name}</h3>
                <span className={"archive-badge ".concat(capsule.archive_type)}>
                  {capsule.archive_type}
                </span>
              </div>
              <p className="description">{capsule.description}</p>
              <div className="capsule-meta">
                <div className="meta-item">
                  <span className="meta-label">Slug:</span>
                  <code>{capsule.slug}</code>
                </div>
                <div className="meta-item">
                  <span className="meta-label">Schedule:</span>
                  <code>{capsule.schedule}</code>
                </div>
              </div>
              <div className="action-area">
                <span className="view-link">View Latest Artifact →</span>
              </div>
            </div>
          </link_1.default>); })}
      </div>
      <div className="footer-info">
        <p>
          💡 <strong>Tip:</strong> Click on any capsule to view its latest execution artifact and
          performance data.
        </p>
      </div>
      <style jsx>{"\n        .header {\n          text-align: center;\n          margin-bottom: 2rem;\n          border-bottom: 2px solid #e1e5e9;\n          padding-bottom: 1.5rem;\n        }\n        .subtitle {\n          color: #6c757d;\n          font-size: 1.1rem;\n          margin-top: 0.5rem;\n        }\n        .stats-bar {\n          display: flex;\n          justify-content: center;\n          gap: 3rem;\n          margin-bottom: 2rem;\n          padding: 1.5rem;\n          background: #f8f9fa;\n          border-radius: 8px;\n        }\n        .stat {\n          text-align: center;\n        }\n        .stat-number {\n          display: block;\n          font-size: 2rem;\n          font-weight: bold;\n          color: #0070f3;\n        }\n        .stat-label {\n          font-size: 0.9rem;\n          color: #6c757d;\n          text-transform: uppercase;\n        }\n        .capsules-grid {\n          display: grid;\n          grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));\n          gap: 1.5rem;\n          margin-bottom: 2rem;\n        }\n        .capsule-card {\n          border: 1px solid #dee2e6;\n          border-radius: 8px;\n          padding: 1.5rem;\n          background: white;\n          cursor: pointer;\n          transition: all 0.2s ease;\n          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);\n        }\n        .capsule-card:hover {\n          transform: translateY(-2px);\n          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);\n          border-color: #0070f3;\n        }\n        .capsule-header {\n          display: flex;\n          justify-content: space-between;\n          align-items: flex-start;\n          margin-bottom: 1rem;\n        }\n        .capsule-header h3 {\n          margin: 0;\n          color: #343a40;\n          font-size: 1.25rem;\n        }\n        .archive-badge {\n          padding: 0.25rem 0.5rem;\n          border-radius: 4px;\n          font-size: 0.75rem;\n          font-weight: bold;\n          text-transform: uppercase;\n        }\n        .archive-badge.snapshot {\n          background: #d1ecf1;\n          color: #0c5460;\n        }\n        .archive-badge.bulletin {\n          background: #d4edda;\n          color: #155724;\n        }\n        .archive-badge.analysis_report {\n          background: #fff3cd;\n          color: #856404;\n        }\n        .archive-badge.external {\n          background: #e2e3e5;\n          color: #383d41;\n        }\n        .description {\n          color: #6c757d;\n          margin: 1rem 0;\n          line-height: 1.5;\n        }\n        .capsule-meta {\n          margin: 1rem 0;\n        }\n        .meta-item {\n          display: flex;\n          align-items: center;\n          margin-bottom: 0.5rem;\n        }\n        .meta-label {\n          font-weight: 500;\n          margin-right: 0.5rem;\n          min-width: 70px;\n        }\n        code {\n          background: #f8f9fa;\n          padding: 0.2rem 0.4rem;\n          border-radius: 3px;\n          font-family: 'Courier New', monospace;\n          font-size: 0.9rem;\n        }\n        .action-area {\n          border-top: 1px solid #e9ecef;\n          padding-top: 1rem;\n          margin-top: 1rem;\n        }\n        .view-link {\n          color: #0070f3;\n          font-weight: 500;\n          font-size: 0.9rem;\n        }\n        .capsule-card:hover .view-link {\n          text-decoration: underline;\n        }\n        .footer-info {\n          text-align: center;\n          padding: 1.5rem;\n          background: #f8f9fa;\n          border-radius: 8px;\n          color: #6c757d;\n        }\n        @media (max-width: 768px) {\n          .stats-bar {\n            flex-direction: column;\n            gap: 1rem;\n          }\n          .capsules-grid {\n            grid-template-columns: 1fr;\n          }\n        }\n      "}</style>
    </Container>);
}
var templateObject_1;
