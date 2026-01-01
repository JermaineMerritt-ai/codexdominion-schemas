import Link from "next/link";

// Temporary mock functions - replace with backend API calls
async function fetchCurrentTenant() {
  // TODO: GET /api/portal/tenant
  return {
    id: "tenant_demo",
    name: "Test Brand Alpha",
    slug: "test-brand-alpha"
  };
}

async function fetchStoresForTenant(tenantId: string) {
  // TODO: GET /api/portal/stores?tenant_id={tenantId}
  return [
    {
      id: "store_1",
      name: "Test Brand Main Store",
      platform: "shopify",
      domain: "testbrand.myshopify.com",
      storefront_url: "https://testbrand.myshopify.com",
      admin_url: "https://testbrand.myshopify.com/admin",
      status: "active"
    }
  ];
}

async function fetchRecentWorkflows(tenantId: string) {
  // TODO: GET /api/portal/workflows?tenant_id={tenantId}&limit=5
  return [
    {
      id: "workflow_intake_1",
      type: "sales.empire_store_ignition_intake",
      category: "sales",
      status: "completed"
    },
    {
      id: "workflow_store_1",
      type: "store.create_shopify_store",
      category: "store",
      status: "completed"
    },
    {
      id: "workflow_social_1",
      type: "social.generate_launch_campaign_for_store",
      category: "social",
      status: "pending_review"
    }
  ];
}

export default async function PortalDashboard() {
  const tenant = await fetchCurrentTenant();
  const stores = await fetchStoresForTenant(tenant.id);
  const workflows = await fetchRecentWorkflows(tenant.id);

  const store = stores[0]; // v1 assumption

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Welcome, {tenant.name}</h1>

      <section className="grid gap-4 md:grid-cols-2">
        {store && (
          <div className="border border-slate-800 rounded-lg p-4 bg-slate-900">
            <h2 className="text-lg font-semibold mb-2">Your Store</h2>
            <p className="text-slate-300">{store.name} ({store.platform})</p>
            <p className="text-xs text-slate-500 mt-1">Status: {store.status}</p>
            <a
              href={`/portal/stores/${store.id}`}
              className="inline-block mt-3 text-emerald-400 text-sm hover:underline"
            >
              View store →
            </a>
          </div>
        )}

        <div className="border border-slate-800 rounded-lg p-4 bg-slate-900">
          <h2 className="text-lg font-semibold mb-2">Recent Workflows</h2>
          <ul className="space-y-2 text-sm text-slate-300">
            {workflows.map(wf => (
              <li key={wf.id}>
                <a
                  href={`/portal/workflows/${wf.id}`}
                  className="hover:underline"
                >
                  {wf.type} – {wf.status}
                </a>
              </li>
            ))}
          </ul>
        </div>
      </section>
    </div>
  );
}
