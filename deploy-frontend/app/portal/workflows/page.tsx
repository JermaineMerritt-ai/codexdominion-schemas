import Link from "next/link";
import { Card, CardHeader, CardBody, Badge } from "@/components/ui";
import { styles } from "@/lib/design-system";

// Workflow catalog - filtered for customer-facing workflows
const WORKFLOW_CATALOG = [
  {
    id: "store.create_shopify_store",
    category: "Store",
    name: "Create Shopify Store",
    description: "Launch a complete Shopify store with products, marketing site, and automations",
    expected_output: "Live storefront, admin dashboard, 5-10 initial products, marketing website",
    estimated_time: "7-14 days",
    icon: "🏪"
  },
  {
    id: "store.create_product_listing",
    category: "Store",
    name: "Add Product (AI-Assisted)",
    description: "Generate product listing with AI-created copy, images, and SEO optimization",
    expected_output: "Product page with description, images, pricing, and variants",
    estimated_time: "2-4 hours",
    icon: "📦"
  },
  {
    id: "store.sync_inventory",
    category: "Store",
    name: "Sync Inventory",
    description: "Update stock levels, variants, and product availability across platforms",
    expected_output: "Updated inventory counts and variant availability",
    estimated_time: "30 minutes",
    icon: "📊"
  },
  {
    id: "website.create_basic_site",
    category: "Website",
    name: "Generate Marketing Website",
    description: "Create branded marketing site with custom pages and deployment",
    expected_output: "Live website with home, about, products, contact pages",
    estimated_time: "1-2 days",
    icon: "🌐"
  },
  {
    id: "website.add_landing_page",
    category: "Website",
    name: "Add Landing Page",
    description: "Design high-converting landing page for specific product or campaign",
    expected_output: "Landing page with CTA, social proof, and conversion tracking",
    estimated_time: "4-6 hours",
    icon: "📄"
  },
  {
    id: "social.generate_launch_campaign_for_store",
    category: "Social",
    name: "Generate Launch Campaign",
    description: "Create 7-day social media campaign for Instagram, YouTube, and email",
    expected_output: "Social posts, video scripts, email sequence, content calendar",
    estimated_time: "2-3 days",
    icon: "📱"
  },
  {
    id: "social.create_content_series",
    category: "Social",
    name: "Create Content Series",
    description: "Generate themed content series for consistent social presence",
    expected_output: "10-15 posts with copy, image concepts, and posting schedule",
    estimated_time: "1-2 days",
    icon: "📸"
  },
  {
    id: "analytics.setup_tracking",
    category: "Analytics",
    name: "Setup Analytics Tracking",
    description: "Configure Google Analytics, conversion tracking, and reporting dashboards",
    expected_output: "Analytics dashboard with e-commerce tracking and custom reports",
    estimated_time: "1 day",
    icon: "📈"
  }
];

const CATEGORIES = ["All", "Store", "Website", "Social", "Analytics"];

export default function WorkflowCatalog() {
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
                Workflow Catalog
              </h1>
              <p className="text-sm text-slate-400 mt-1">
                Start a new workflow to build, optimize, or automate your business
              </p>
            </div>
          </div>
        </div>
      </div>
      
      <div className="container mx-auto px-6 py-8">
        {/* Category Filters */}
        <div className="flex gap-2 mb-8 overflow-x-auto pb-2">
          {CATEGORIES.map((category) => (
            <button
              key={category}
              className={`px-4 py-2 rounded-lg font-medium whitespace-nowrap transition-colors ${
                category === "All"
                  ? "bg-sovereign-gold text-slate-950"
                  : "bg-slate-900 text-slate-400 hover:bg-slate-800 hover:text-slate-200"
              }`}
            >
              {category}
            </button>
          ))}
        </div>
        
        {/* Workflow Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {WORKFLOW_CATALOG.map((workflow) => (
            <Card key={workflow.id} className={styles.card}>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div>
                    <div className="text-3xl mb-2">{workflow.icon}</div>
                    <Badge variant="slate" className="text-xs mb-2">
                      {workflow.category}
                    </Badge>
                    <h3 className="text-lg font-bold text-slate-200">
                      {workflow.name}
                    </h3>
                  </div>
                </div>
              </CardHeader>
              <CardBody>
                <p className="text-sm text-slate-400 mb-4">
                  {workflow.description}
                </p>
                
                <div className="space-y-3 mb-4">
                  <div>
                    <p className="text-xs text-slate-500 mb-1">Expected Output</p>
                    <p className="text-sm text-slate-300">
                      {workflow.expected_output}
                    </p>
                  </div>
                  
                  <div>
                    <p className="text-xs text-slate-500 mb-1">Estimated Time</p>
                    <p className="text-sm text-slate-300">
                      {workflow.estimated_time}
                    </p>
                  </div>
                </div>
                
                <Link
                  href={`/portal/workflows/start/${workflow.id}`}
                  className="block w-full px-4 py-2 bg-sovereign-gold text-slate-950 font-medium rounded-lg hover:bg-yellow-500 transition-colors text-center"
                >
                  Start Workflow
                </Link>
              </CardBody>
            </Card>
          ))}
        </div>
        
        {/* Help Section */}
        <Card className={`${styles.card} mt-8`}>
          <CardBody>
            <div className="text-center py-6">
              <h3 className="text-lg font-bold text-slate-200 mb-2">
                Need help choosing?
              </h3>
              <p className="text-sm text-slate-400 mb-4">
                Not sure which workflow fits your needs? Our team can guide you.
              </p>
              <Link
                href="/portal/support"
                className="inline-block px-6 py-2 bg-slate-800 text-slate-200 font-medium rounded-lg hover:bg-slate-700 transition-colors"
              >
                Contact Support
              </Link>
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
