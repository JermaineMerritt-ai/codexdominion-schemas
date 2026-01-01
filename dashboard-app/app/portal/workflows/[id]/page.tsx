import Link from "next/link";
import { Card, CardHeader, CardBody, Badge, StatusBadge } from "@/components/ui";
import { styles } from "@/lib/design-system";

// Mock data - replace with API call
async function getWorkflowData(id: string) {
  // TODO: Replace with actual API call scoped to current tenant
  // const workflow = await fetchWorkflow(id);
  // const artifacts = await fetchWorkflowArtifacts(id);
  
  return {
    workflow: {
      id: id,
      tenant_id: "tenant_demo",
      type: "store.create_shopify_store",
      category: "store",
      status: "completed",
      decision: "approved",
      related_store_id: "store_1",
      summary: "Creating Shopify store for Test Brand with 10 products, marketing site, and launch campaign.",
      created_at: "2025-12-15T10:30:00Z",
      started_at: "2025-12-15T10:35:00Z",
      completed_at: "2025-12-15T14:00:00Z",
      inputs: {
        brand_name: "Test Brand",
        platform: "shopify",
        initial_products_count: 10
      }
    },
    artifacts: [
      {
        id: "artifact_1",
        kind: "storefront_url",
        label: "Storefront URL",
        value: "https://testbrand.myshopify.com",
        created_at: "2025-12-15T14:00:00Z"
      },
      {
        id: "artifact_2",
        kind: "admin_url",
        label: "Admin Dashboard",
        value: "https://testbrand.myshopify.com/admin",
        created_at: "2025-12-15T14:00:00Z"
      },
      {
        id: "artifact_3",
        kind: "marketing_site_url",
        label: "Marketing Site",
        value: "https://testbrand-site.vercel.app",
        created_at: "2025-12-15T13:45:00Z"
      },
      {
        id: "artifact_4",
        kind: "product_list",
        label: "Products Created",
        value: "10",
        created_at: "2025-12-15T13:30:00Z"
      }
    ],
    steps: [
      {
        name: "Store Connection",
        status: "completed",
        started_at: "2025-12-15T10:35:00Z",
        completed_at: "2025-12-15T10:40:00Z",
        description: "Connected to Shopify store"
      },
      {
        name: "Product Creation",
        status: "completed",
        started_at: "2025-12-15T10:40:00Z",
        completed_at: "2025-12-15T13:30:00Z",
        description: "Generated 10 products with AI-assisted copy and images"
      },
      {
        name: "Site & Theme",
        status: "completed",
        started_at: "2025-12-15T13:30:00Z",
        completed_at: "2025-12-15T13:45:00Z",
        description: "Generated marketing website and configured theme"
      },
      {
        name: "Launch Readiness",
        status: "completed",
        started_at: "2025-12-15T13:45:00Z",
        completed_at: "2025-12-15T14:00:00Z",
        description: "Final checks and social campaign triggered"
      }
    ],
    logs: [
      {
        timestamp: "2025-12-15T10:35:00Z",
        message: "Workflow started"
      },
      {
        timestamp: "2025-12-15T10:36:00Z",
        message: "Connected to Shopify store: testbrand.myshopify.com"
      },
      {
        timestamp: "2025-12-15T10:40:00Z",
        message: "Store connection verified"
      },
      {
        timestamp: "2025-12-15T10:41:00Z",
        message: "Starting product generation..."
      },
      {
        timestamp: "2025-12-15T11:00:00Z",
        message: "Created product 1/10: Premium T-Shirt"
      },
      {
        timestamp: "2025-12-15T13:30:00Z",
        message: "All products created successfully"
      },
      {
        timestamp: "2025-12-15T13:45:00Z",
        message: "Marketing site deployed to Vercel"
      },
      {
        timestamp: "2025-12-15T14:00:00Z",
        message: "Workflow completed - social campaign triggered"
      }
    ]
  };
}

export default async function WorkflowDetailPage({ params }: { params: { id: string } }) {
  const data = await getWorkflowData(params.id);
  const { workflow, artifacts, steps, logs } = data;
  
  const isCompleted = workflow.status === "completed";
  const isFailed = workflow.status === "failed";
  const isRunning = workflow.status === "running";
  
  return (
    <div className="min-h-screen bg-sovereign-obsidian">
      <div className="border-b border-sovereign-slate bg-slate-950/50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <Link
                href="/portal"
                className="text-sm text-slate-400 hover:text-sovereign-gold mb-2 inline-block"
              >
                ← Back to Dashboard
              </Link>
              <h1 className="text-2xl font-bold text-sovereign-gold">
                {workflow.type.replace(/_/g, " ").replace(/\./g, " › ")}
              </h1>
              <div className="flex items-center gap-3 mt-2">
                <p className="text-sm text-slate-400">ID: {workflow.id}</p>
                <StatusBadge status={workflow.status} />
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="container mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Progress Timeline */}
            <Card className={styles.card}>
              <CardHeader>
                <h2 className={styles.text.h3}>Progress</h2>
              </CardHeader>
              <CardBody>
                <div className="space-y-4">
                  {steps.map((step, idx) => (
                    <div key={idx} className="flex items-start gap-4">
                      <div className="flex-shrink-0 mt-1">
                        {step.status === "completed" && (
                          <div className="w-8 h-8 rounded-full bg-emerald-500/20 border-2 border-emerald-500 flex items-center justify-center">
                            <svg className="w-4 h-4 text-emerald-500" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                            </svg>
                          </div>
                        )}
                        {step.status === "running" && (
                          <div className="w-8 h-8 rounded-full bg-sovereign-gold/20 border-2 border-sovereign-gold flex items-center justify-center">
                            <div className="w-3 h-3 rounded-full bg-sovereign-gold animate-pulse" />
                          </div>
                        )}
                        {step.status === "pending" && (
                          <div className="w-8 h-8 rounded-full bg-slate-800 border-2 border-slate-700" />
                        )}
                        {step.status === "failed" && (
                          <div className="w-8 h-8 rounded-full bg-red-500/20 border-2 border-red-500 flex items-center justify-center">
                            <svg className="w-4 h-4 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                            </svg>
                          </div>
                        )}
                      </div>
                      
                      <div className="flex-1">
                        <h3 className="font-medium text-slate-200 mb-1">
                          {step.name}
                        </h3>
                        <p className="text-sm text-slate-400 mb-2">
                          {step.description}
                        </p>
                        {step.started_at && (
                          <p className="text-xs text-slate-500">
                            Started: {new Date(step.started_at).toLocaleTimeString()}
                            {step.completed_at && (
                              <> • Completed: {new Date(step.completed_at).toLocaleTimeString()}</>
                            )}
                          </p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardBody>
            </Card>
            
            {/* Activity Log */}
            <Card className={styles.card}>
              <CardHeader>
                <h2 className={styles.text.h3}>Activity Log</h2>
              </CardHeader>
              <CardBody>
                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {logs.map((log, idx) => (
                    <div
                      key={idx}
                      className="p-2 rounded bg-slate-900/30 border border-slate-800"
                    >
                      <p className="text-xs text-slate-500 mb-1">
                        {new Date(log.timestamp).toLocaleTimeString()}
                      </p>
                      <p className="text-sm text-slate-300">{log.message}</p>
                    </div>
                  ))}
                </div>
              </CardBody>
            </Card>
          </div>
          
          {/* Sidebar */}
          <div className="space-y-6">
            {/* Key Artifacts */}
            {artifacts && artifacts.length > 0 && (
              <Card className={styles.card}>
                <CardHeader>
                  <h2 className={styles.text.h3}>Key Artifacts</h2>
                </CardHeader>
                <CardBody>
                  <div className="space-y-3">
                    {artifacts.map((artifact) => (
                      <div key={artifact.id}>
                        <p className="text-xs text-slate-500 mb-1">{artifact.label}</p>
                        {artifact.kind.includes("url") ? (
                          <a
                            href={artifact.value}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-sm text-sovereign-gold hover:text-yellow-400 break-all"
                          >
                            {artifact.value}
                          </a>
                        ) : (
                          <p className="text-sm text-slate-300">{artifact.value}</p>
                        )}
                      </div>
                    ))}
                  </div>
                </CardBody>
              </Card>
            )}
            
            {/* Workflow Info */}
            <Card className={styles.card}>
              <CardHeader>
                <h2 className={styles.text.h3}>Workflow Info</h2>
              </CardHeader>
              <CardBody>
                <div className="space-y-3">
                  <div>
                    <p className="text-xs text-slate-500 mb-1">Type</p>
                    <p className="text-sm text-slate-300">
                      {workflow.type}
                    </p>
                  </div>
                  
                  <div>
                    <p className="text-xs text-slate-500 mb-1">Status</p>
                    <StatusBadge status={workflow.status} />
                  </div>
                  
                  <div>
                    <p className="text-xs text-slate-500 mb-1">Created</p>
                    <p className="text-sm text-slate-300">
                      {new Date(workflow.created_at).toLocaleString()}
                    </p>
                  </div>
                  
                  {workflow.started_at && (
                    <div>
                      <p className="text-xs text-slate-500 mb-1">Started</p>
                      <p className="text-sm text-slate-300">
                        {new Date(workflow.started_at).toLocaleString()}
                      </p>
                    </div>
                  )}
                </div>
              </CardBody>
            </Card>
            
            {/* Support */}
            <Card className={styles.card}>
              <CardBody>
                <h3 className="text-sm font-medium text-slate-200 mb-2">
                  Need Help?
                </h3>
                <p className="text-xs text-slate-400 mb-3">
                  Contact our support team if you have questions about this workflow.
                </p>
                <Link
                  href="/portal/support"
                  className="block w-full px-4 py-2 bg-slate-800 text-slate-200 font-medium rounded-lg hover:bg-slate-700 transition-colors text-center text-sm"
                >
                  Contact Support
                </Link>
              </CardBody>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
