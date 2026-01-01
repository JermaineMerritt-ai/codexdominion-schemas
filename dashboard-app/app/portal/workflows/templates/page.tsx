"use client";

import { useState } from "react";
import { Icon, Card, CardHeader, CardBody, Badge } from "@/components/ui";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";

// Template schema from database
interface WorkflowTemplate {
  id: string;
  name: string;
  description: string;
  workflow_type_id: string;
  category: string | null;
  tags: string[];
  default_inputs: Record<string, any> | null;
  required_fields: string[];
  optional_fields: string[];
  approved_structure: Record<string, any> | null;
  approved_copy_blocks: Record<string, any> | null;
  is_pre_approved: boolean;
  is_active: boolean;
  usage_count: number;
  last_used_at: string | null;
  created_by_user_id: string;
  approved_by_council_id: string | null;
  created_at: string;
  updated_at: string;
}

async function fetchTemplates(): Promise<WorkflowTemplate[]> {
  try {
    const res = await fetch(`${API_BASE}/api/templates?is_active=true`, { cache: "no-store" });
    if (!res.ok) return [];
    const data = await res.json();
    return data.templates || [];
  } catch (err) {
    console.error("Error fetching templates:", err);
    return [];
  }
}

function groupByCategory(templates: WorkflowTemplate[]): Record<string, WorkflowTemplate[]> {
  const grouped: Record<string, WorkflowTemplate[]> = {};
  templates.forEach((t) => {
    const category = t.category || "Other";
    if (!grouped[category]) grouped[category] = [];
    grouped[category].push(t);
  });
  return grouped;
}

export default async function TemplatesPage() {
  const templates = await fetchTemplates();
  const groupedTemplates = groupByCategory(templates);
  const categories = Object.keys(groupedTemplates).sort();

  return (
    <div className="space-y-6 max-w-7xl">
      {/* Header */}
      <header className="space-y-2">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white flex items-center gap-2">
              <Icon name="clipboard" className="text-sovereign-gold" />
              Workflow Templates
            </h1>
            <p className="text-sm text-slate-400 mt-1">
              Pre-approved workflow blueprints you can use instantly
            </p>
          </div>
          <Badge variant="gold">
            {templates.length} template{templates.length !== 1 ? "s" : ""}
          </Badge>
        </div>
      </header>

      {/* Templates Grid by Category */}
      {templates.length === 0 ? (
        <Card>
          <CardBody>
            <div className="text-center py-12">
              <Icon name="clipboard" size={64} className="text-slate-600 mx-auto mb-4 opacity-50" />
              <h2 className="text-lg font-semibold text-white mb-2">No Templates Available</h2>
              <p className="text-sm text-slate-400">
                Templates will appear here once they're approved by councils.
              </p>
            </div>
          </CardBody>
        </Card>
      ) : (
        <div className="space-y-8">
          {categories.map((category) => (
            <section key={category}>
              <div className="mb-4">
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                  <Icon name={getCategoryIcon(category)} size={20} className="text-sovereign-blue" />
                  {category}
                </h2>
                <p className="text-sm text-slate-400 mt-1">
                  {groupedTemplates[category].length} template{groupedTemplates[category].length !== 1 ? "s" : ""}
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {groupedTemplates[category].map((template) => (
                  <TemplateCard key={template.id} template={template} />
                ))}
              </div>
            </section>
          ))}
        </div>
      )}
    </div>
  );
}

// ============================================================================
// CLIENT COMPONENTS
// ============================================================================

function TemplateCard({ template }: { template: WorkflowTemplate }) {
  const [loading, setLoading] = useState(false);

  const handleUseTemplate = async () => {
    // In production, this would get tenant_id and user_id from session
    const tenant_id = "tenant_demo";
    const user_id = "user_demo";

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/templates/${template.id}/use`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tenant_id, user_id })
      });

      if (res.ok) {
        const data = await res.json();
        // Navigate to draft editor
        window.location.href = `/portal/workflows/drafts/${data.draft.id}`;
      } else {
        const error = await res.json();
        alert(`Error: ${error.error}`);
      }
    } catch (err) {
      alert(`Error: ${err}`);
    } finally {
      setLoading(false);
    }
  };

  const handleInstantRun = async () => {
    if (!confirm(`Instantly run "${template.name}" workflow? This will use default values.`)) return;

    // In production, this would create a draft and immediately convert it
    const tenant_id = "tenant_demo";
    const user_id = "user_demo";

    setLoading(true);
    try {
      // Step 1: Create draft from template
      const createRes = await fetch(`${API_BASE}/api/templates/${template.id}/use`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tenant_id, user_id })
      });

      if (!createRes.ok) {
        const error = await createRes.json();
        alert(`Error creating draft: ${error.error}`);
        return;
      }

      const createData = await createRes.json();
      const draftId = createData.draft.id;

      // Step 2: Convert draft to workflow (pre-approved templates skip review)
      const convertRes = await fetch(`${API_BASE}/api/drafts/${draftId}/convert`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ auto_execute: true })
      });

      if (convertRes.ok) {
        const convertData = await convertRes.json();
        alert("Workflow started!");
        window.location.href = `/portal/workflows/${convertData.workflow_id}`;
      } else {
        const error = await convertRes.json();
        alert(`Error: ${error.error}`);
      }
    } catch (err) {
      alert(`Error: ${err}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="hover:ring-2 hover:ring-sovereign-blue transition-all">
      <CardBody className="space-y-4">
        {/* Header */}
        <div>
          <div className="flex items-start justify-between mb-2">
            <h3 className="text-lg font-semibold text-white">{template.name}</h3>
            {template.is_pre_approved && (
              <Badge variant="gold" size="sm">
                <Icon name="checkCircle" size={10} className="inline mr-1" />
                Instant
              </Badge>
            )}
          </div>
          <p className="text-sm text-slate-400 line-clamp-3">{template.description}</p>
        </div>

        {/* Tags */}
        {template.tags.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {template.tags.slice(0, 3).map((tag) => (
              <Badge key={tag} variant="blue" size="sm">
                {tag}
              </Badge>
            ))}
            {template.tags.length > 3 && (
              <Badge variant="slate" size="sm">
                +{template.tags.length - 3} more
              </Badge>
            )}
          </div>
        )}

        {/* Stats */}
        <div className="flex items-center gap-4 text-xs text-slate-400">
          <div className="flex items-center gap-1">
            <Icon name="workflow" size={12} />
            <span>Used {template.usage_count} times</span>
          </div>
          {template.last_used_at && (
            <div className="flex items-center gap-1">
              <Icon name="clock" size={12} />
              <span>Last: {new Date(template.last_used_at).toLocaleDateString()}</span>
            </div>
          )}
        </div>

        {/* Fields Info */}
        <div className="text-xs space-y-1">
          {template.required_fields.length > 0 && (
            <div className="flex items-start gap-2">
              <Icon name="info" size={12} className="text-sovereign-crimson mt-0.5" />
              <span className="text-slate-400">
                <span className="font-semibold text-sovereign-crimson">{template.required_fields.length} required field{template.required_fields.length !== 1 ? "s" : ""}:</span>{" "}
                {template.required_fields.slice(0, 2).join(", ")}
                {template.required_fields.length > 2 && `, +${template.required_fields.length - 2} more`}
              </span>
            </div>
          )}
          {template.optional_fields.length > 0 && (
            <div className="flex items-start gap-2">
              <Icon name="info" size={12} className="text-slate-500 mt-0.5" />
              <span className="text-slate-400">
                {template.optional_fields.length} optional field{template.optional_fields.length !== 1 ? "s" : ""}
              </span>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex gap-2 pt-2">
          {template.is_pre_approved ? (
            <>
              <button
                onClick={handleInstantRun}
                disabled={loading}
                className="flex-1 px-4 py-2 rounded-lg bg-sovereign-gold hover:bg-yellow-600 text-black font-semibold flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <Icon name="clock" size={16} className="animate-spin" />
                    Running...
                  </>
                ) : (
                  <>
                    <Icon name="play" size={16} />
                    Instant Run
                  </>
                )}
              </button>
              <button
                onClick={handleUseTemplate}
                disabled={loading}
                className="px-4 py-2 rounded-lg bg-sovereign-blue hover:bg-blue-600 text-white font-semibold flex items-center gap-2 disabled:opacity-50"
              >
                <Icon name="edit" size={16} />
              </button>
            </>
          ) : (
            <button
              onClick={handleUseTemplate}
              disabled={loading}
              className="flex-1 px-4 py-2 rounded-lg bg-sovereign-blue hover:bg-blue-600 text-white font-semibold flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Icon name="clock" size={16} className="animate-spin" />
                  Creating...
                </>
              ) : (
                <>
                  <Icon name="clipboard" size={16} />
                  Use Template
                </>
              )}
            </button>
          )}
        </div>
      </CardBody>
    </Card>
  );
}

// ============================================================================
// HELPERS
// ============================================================================

function getCategoryIcon(category: string): "users" | "coins" | "workflow" | "edit" | "shield" | "clipboard" {
  const map: Record<string, any> = {
    "Marketing": "users",
    "E-commerce": "coins",
    "Automation": "workflow",
    "Content": "edit",
    "Security": "shield",
    "Other": "clipboard"
  };
  return map[category] || "clipboard";
}
