/**
 * Workflow Catalog Card Component
 * 
 * Displays a workflow in the catalog grid with:
 * - Icon + name + description
 * - Domain badge
 * - Hover effects
 * - Link to detail page
 */

export default function WorkflowCard({ workflow }) {
  return (
    <div className="border border-slate-800 rounded-lg p-4 bg-slate-900 hover:border-emerald-500 transition">
      <div className="flex items-center gap-3 mb-3">
        <div className="w-10 h-10 rounded bg-emerald-700 flex items-center justify-center text-xl">
          🖥️
        </div>
        <div>
          <h3 className="text-lg font-semibold">{workflow.name}</h3>
          <p className="text-sm text-slate-400">{workflow.description}</p>
        </div>
      </div>

      <div className="flex justify-between items-center mt-4">
        <span className="px-2 py-1 text-xs rounded bg-slate-800 text-slate-300">
          {workflow.domain}
        </span>

        <a
          href={`/dashboard/workflows/${workflow.id}`}
          className="text-emerald-400 text-sm hover:underline"
        >
          View Details →
        </a>
      </div>
    </div>
  );
}
