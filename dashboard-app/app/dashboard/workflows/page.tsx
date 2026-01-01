/**
 * Workflow Catalog Page
 * 
 * Grid of all available workflows
 */

import WorkflowCard from "@/components/workflows/WorkflowCard";

interface Workflow {
  id: string;
  name: string;
  description: string;
  domain: string;
  icon?: string;
}

async function fetchWorkflows(): Promise<Workflow[]> {
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";
  
  try {
    const res = await fetch(`${API_BASE}/api/workflows/types`, { 
      cache: "no-store" 
    });
    
    if (!res.ok) {
      return [];
    }
    
    const data = await res.json();
    // Flask returns {success: true, workflow_types: [...]}
    return Array.isArray(data.workflow_types) ? data.workflow_types : [];
  } catch (error) {
    console.error('Error fetching workflows:', error);
    return [];
  }
}

export default async function WorkflowsPage() {
  const workflows = await fetchWorkflows();
  
  // Defensive check to ensure workflows is an array
  const safeWorkflows = Array.isArray(workflows) ? workflows : [];

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-3xl font-bold">Workflow Catalog</h1>
        <p className="text-slate-400 mt-1">
          Browse available workflows and start new executions
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {safeWorkflows.map((workflow) => (
          <WorkflowCard key={workflow.id} workflow={workflow} />
        ))}
      </div>

      {workflows.length === 0 && (
        <div className="border border-slate-800 rounded-lg p-8 bg-slate-900 text-center">
          <p className="text-slate-400">No workflows available</p>
        </div>
      )}
    </div>
  );
}
