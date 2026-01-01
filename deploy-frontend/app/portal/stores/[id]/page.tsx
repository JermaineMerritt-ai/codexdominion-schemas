import Link from "next/link";

// Temporary mock functions - replace with backend API calls
async function fetchStore(id: string) {
  // TODO: GET /api/portal/stores/{id}
  return {
    id: id,
    tenant_id: "tenant_demo",
    name: "Test Brand Main Store",
    platform: "shopify",
    domain: "testbrand.myshopify.com",
    storefront_url: "https://testbrand.myshopify.com",
    admin_url: "https://testbrand.myshopify.com/admin",
    status: "active",
    created_via_workflow_id: "workflow_store_1",
    created_at: "2025-12-15T10:30:00Z"
  };
}

async function fetchWorkflowsForStore(storeId: string) {
  // TODO: GET /api/portal/workflows?related_store_id={storeId}
  return [
    {
      id: "workflow_store_1",
      type: "store.create_shopify_store",
      category: "store",
      status: "completed",
      created_at: "2025-12-15T10:30:00Z"
    },
    {
      id: "workflow_social_1",
      type: "social.generate_launch_campaign_for_store",
      category: "social",
      status: "pending_review",
      decision: "pending",
      parent_workflow_id: "workflow_store_1",
      created_at: "2025-12-15T14:05:00Z"
    }
  ];
}

async function fetchWorkflowArtifacts(workflowId: string) {
  // TODO: GET /api/portal/workflows/{workflowId}/artifacts
  return [
    {
      id: "artifact_1",
      kind: "storefront_url",
      label: "Storefront URL",
      value: "https://testbrand.myshopify.com"
    },
    {
      id: "artifact_2",
      kind: "admin_url",
      label: "Admin Dashboard",
      value: "https://testbrand.myshopify.com/admin"
    },
    {
      id: "artifact_3",
      kind: "marketing_site_url",
      label: "Marketing Site",
      value: "https://testbrand-site.vercel.app"
    },
    {
      id: "artifact_4",
      kind: "product_list",
      label: "Products Created",
      value: "10"
    }
  ];
}

// Helper function to aggregate all store data
async function getStoreData(id: string) {
  const store = await fetchStore(id);
  const workflows = await fetchWorkflowsForStore(id);
  const creationWorkflow = workflows.find(wf => wf.type === "store.create_shopify_store");
  const artifacts = creationWorkflow ? await fetchWorkflowArtifacts(creationWorkflow.id) : [];
  
  return { store, workflows, artifacts };
}

export default async function StoreDetailPage({ params }: { params: { id: string } }) {
  const data = await getStoreData(params.id);
  const { store, workflows, artifacts } = data;
  
  const creationWorkflow = workflows.find(wf => wf.type === "store.create_shopify_store");
  const socialWorkflow = workflows.find(wf => wf.type === "social.generate_launch_campaign_for_store");
  
  return (
    <div className="space-y-6">
      {/* Back link */}
      <Link href="/portal" className="text-sm text-slate-400 hover:text-slate-300">
        ← Back to Dashboard
      </Link>

      {/* Store summary */}
      <section className="border border-slate-800 rounded-lg p-6 bg-slate-900">
        <h1 className="text-2xl font-bold mb-3">{store.name}</h1>
        <div className="space-y-2 text-sm text-slate-300">
          <p>Platform: <span className="capitalize font-medium">{store.platform}</span></p>
          <p>Status: <span className="capitalize font-medium">{store.status}</span></p>
        </div>
        
        {/* Links */}
        <div className="flex gap-3 mt-4">
          {store.storefront_url && (
            <a
              href={store.storefront_url}
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 bg-emerald-600 text-white text-sm font-medium rounded hover:bg-emerald-500"
            >
              View Storefront
            </a>
          )}
          {store.admin_url && (
            <a
              href={store.admin_url}
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 bg-slate-700 text-slate-200 text-sm font-medium rounded hover:bg-slate-600"
            >
              Open Admin
            </a>
          )}
        </div>
      </section>

      {/* Store creation workflow */}
      {creationWorkflow && (
        <section className="border border-slate-800 rounded-lg p-6 bg-slate-900">
          <h2 className="text-xl font-semibold mb-4">Store Creation Workflow</h2>
          
          <div className="mb-4">
            <a
              href={`/portal/workflows/${creationWorkflow.id}`}
              className="text-emerald-400 hover:underline text-sm"
            >
              {creationWorkflow.type} →
            </a>
            <p className="text-xs text-slate-500 mt-1">
              Status: <span className="capitalize">{creationWorkflow.status}</span>
            </p>
          </div>

          {/* Key artifacts */}
          {artifacts.length > 0 && (
            <div className="pt-4 border-t border-slate-800">
              <h3 className="text-sm font-semibold text-slate-400 mb-3">Key Artifacts</h3>
              <ul className="space-y-2">
                {artifacts.map(artifact => (
                  <li key={artifact.id} className="flex justify-between text-sm">
                    <span className="text-slate-400">{artifact.label}:</span>
                    {artifact.kind.includes("url") ? (
                      <a
                        href={artifact.value}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-emerald-400 hover:underline font-mono text-xs truncate ml-2"
                      >
                        {artifact.value}
                      </a>
                    ) : (
                      <span className="text-slate-200 font-medium">{artifact.value}</span>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>
      )}

      {/* Related workflows */}
      <section className="border border-slate-800 rounded-lg p-6 bg-slate-900">
        <h2 className="text-xl font-semibold mb-4">Related Workflows</h2>
        
        {socialWorkflow && (
          <div className="mb-4">
            <a
              href={`/portal/workflows/${socialWorkflow.id}`}
              className="text-emerald-400 hover:underline text-sm"
            >
              Social Launch Campaign →
            </a>
            <p className="text-xs text-slate-500 mt-1">
              Status: <span className="capitalize">{socialWorkflow.status}</span>
              {socialWorkflow.decision && ` · Decision: ${socialWorkflow.decision}`}
            </p>
          </div>
        )}

        {workflows.length === 0 && (
          <p className="text-slate-500 text-sm">No related workflows yet.</p>
        )}

        {workflows.length > 2 && (
          <div className="pt-4 border-t border-slate-800 mt-4">
            <h3 className="text-sm font-semibold text-slate-400 mb-2">All Workflows</h3>
            <ul className="space-y-2">
              {workflows.map(wf => (
                <li key={wf.id}>
                  <a
                    href={`/portal/workflows/${wf.id}`}
                    className="text-sm text-slate-300 hover:text-emerald-400"
                  >
                    {wf.type} – {wf.status}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </section>
    </div>
  );
}
