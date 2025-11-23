// Test the capsules page integration
// Run this from the frontend directory: npm run dev
// Then visit: http://localhost:3000/capsules

import styles from './test-capsules.module.css';

export default function TestCapsules() {
  return (
    <div className={styles.container}>
      <h1>Capsules Integration Test</h1>
      <p>Testing the capsules page integration with the Codex Dominion dashboard.</p>

      <h2>Links to Test:</h2>
      <ul>
        <li><a href="/capsules">Main Capsules Page (Enhanced)</a></li>
        <li><a href="/capsules-simple">Simple Capsules Page</a></li>
        <li><a href="/">Dashboard Home</a></li>
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
    </div>
  );
}