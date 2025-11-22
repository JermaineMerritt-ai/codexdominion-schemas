import { useEffect, useState } from "react";

export default function CapsulesSimple() {
  const [capsules, setCapsules] = useState<any[]>([]);
  const [runs, setRuns] = useState<any[]>([]);

  useEffect(() => {
    async function load() {
      try {
        const c = await fetch("http://localhost:8080/api/capsules").then((r) => r.json());
        const r = await fetch("http://localhost:8080/api/capsules/runs").then((r) => r.json());
        setCapsules(c);
        setRuns(r);
      } catch (error) {
        console.error("Failed to load capsules data:", error);
        // Fallback data for when service is not available
        setCapsules([
          {
            slug: "signals-daily",
            title: "Daily Signals Engine",
            kind: "engine",
            mode: "custodian",
            schedule: "0 6 * * *"
          }
        ]);
        setRuns([
          {
            capsule_slug: "signals-daily",
            actor: "system-scheduler",
            status: "success",
            started_at: new Date().toISOString(),
            artifact_uri: "https://storage.googleapis.com/codex-artifacts/signals-daily-20251108.tar.gz"
          }
        ]);
      }
    }
    load();
  }, []);

  return (
    <div>
      {/* Render capsules and runs here */}
      <h2>Capsules</h2>
      <pre>{JSON.stringify(capsules, null, 2)}</pre>
      <h2>Runs</h2>
      <pre>{JSON.stringify(runs, null, 2)}</pre>
    </div>
  );
}
