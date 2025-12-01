"use strict";
// Test the capsules page integration
// Run this from the frontend directory: npm run dev
// Then visit: http://localhost:3000/capsules
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = TestCapsules;
var test_capsules_module_css_1 = require("./test-capsules.module.css");
function TestCapsules() {
    return (<div className={test_capsules_module_css_1.default.container}>
      <h1>Capsules Integration Test</h1>
      <p>Testing the capsules page integration with the Codex Dominion dashboard.</p>

      <h2>Links to Test:</h2>
      <ul>
        <li>
          <a href="/capsules">Main Capsules Page (Enhanced)</a>
        </li>
        <li>
          <a href="/capsules-simple">Simple Capsules Page</a>
        </li>
        <li>
          <a href="/">Dashboard Home</a>
        </li>
      </ul>

      <h2>API Endpoints to Test:</h2>
      <ul>
        <li>
          <a href="http://localhost:8080/api/capsules" target="_blank" rel="noopener">
            GET /api/capsules
          </a>
        </li>
        <li>
          <a href="http://localhost:8080/api/capsules/runs" target="_blank" rel="noopener">
            GET /api/capsules/runs
          </a>
        </li>
        <li>
          <a href="http://localhost:8080/api/capsules/performance" target="_blank" rel="noopener">
            GET /api/capsules/performance
          </a>
        </li>
      </ul>

      <h2>Prerequisites:</h2>
      <ol>
        <li>Codex Capsules service running on port 8080</li>
        <li>Frontend dev server running on port 3000</li>
        <li>At least one capsule registered (signals-daily)</li>
      </ol>
    </div>);
}
