/**
 * Workflow Detail Page
 * 
 * Shows full workflow information:
 * - Description
 * - Required inputs
 * - Execution steps
 * - Governance rules
 * - Start workflow button
 */

import { fetchWorkflowType } from "@/lib/api/workflows";

export default async function WorkflowDetailPage({ params }) {
  const workflow = await fetchWorkflowType(params.id);

  return (
    <div className="space-y-6 max-w-3xl">
      <header>
        <h1 className="text-3xl font-bold">{workflow.name}</h1>
        <p className="text-slate-400 mt-1">{workflow.description}</p>
      </header>

      <section className="border border-slate-800 rounded-lg p-4 bg-slate-900">
        <h2 className="text-sm font-semibold text-slate-100 mb-2">Required Inputs</h2>
        <ul className="text-sm text-slate-300 space-y-1">
          {Object.entries(workflow.required_inputs).map(([key, type]) => (
            <li key={key}>
              <span className="font-mono text-emerald-400">{key}</span>: {JSON.stringify(type)}
            </li>
          ))}
        </ul>
      </section>

      <section className="border border-slate-800 rounded-lg p-4 bg-slate-900">
        <h2 className="text-sm font-semibold text-slate-100 mb-2">Execution Steps</h2>
        <ol className="list-decimal ml-5 text-sm text-slate-300 space-y-1">
          {workflow.execution_steps.map((step, i) => (
            <li key={i}>{step}</li>
          ))}
        </ol>
      </section>

      <section className="border border-slate-800 rounded-lg p-4 bg-slate-900">
        <h2 className="text-sm font-semibold text-slate-100 mb-2">Governance</h2>
        <p className="text-sm text-slate-300">
          Reviewed by: <span className="text-emerald-400">{workflow.governance.review_council}</span>
        </p>
        <p className="text-sm text-slate-300">
          Auto-execute: {workflow.governance.auto_execute_if_low_risk ? "Yes" : "No"}
        </p>
      </section>

      <a
        href={`/dashboard/workflows/start/${workflow.id}`}
        className="inline-block px-4 py-2 rounded bg-emerald-600 text-white text-sm"
      >
        Start Workflow
      </a>
    </div>
  );
}
