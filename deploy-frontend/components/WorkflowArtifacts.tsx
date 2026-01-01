"use client";

import { Icon, Badge } from "@/components/ui";

interface Artifact {
  id: string;
  kind: string;
  label: string;
  value: string | null;
}

interface WorkflowArtifactsProps {
  artifacts: Artifact[];
  workflowType: string;
  outputs: Record<string, any>;
}

export default function WorkflowArtifacts({
  artifacts,
  workflowType,
  outputs,
}: WorkflowArtifactsProps) {
  // Determine display mode based on workflow type
  const displayMode = detectDisplayMode(workflowType);

  return (
    <div className="space-y-6">
      {displayMode === "campaign" && (
        <CampaignArtifacts artifacts={artifacts} outputs={outputs} />
      )}
      {displayMode === "landing_page" && (
        <LandingPageArtifacts artifacts={artifacts} outputs={outputs} />
      )}
      {displayMode === "products" && (
        <ProductsArtifacts artifacts={artifacts} outputs={outputs} />
      )}
      {displayMode === "generic" && (
        <GenericArtifacts artifacts={artifacts} outputs={outputs} />
      )}
    </div>
  );
}

function detectDisplayMode(workflowType: string): "campaign" | "landing_page" | "products" | "generic" {
  if (workflowType.includes("campaign") || workflowType.includes("launch")) {
    return "campaign";
  }
  if (workflowType.includes("landing") || workflowType.includes("page")) {
    return "landing_page";
  }
  if (workflowType.includes("product") || workflowType.includes("store")) {
    return "products";
  }
  return "generic";
}

// ============================================================================
// CAMPAIGN ARTIFACTS
// ============================================================================

function CampaignArtifacts({ artifacts, outputs }: { artifacts: Artifact[]; outputs: Record<string, any> }) {
  const posts = outputs.posts || [];
  const emailSequence = outputs.email_sequence || [];
  const videoScript = outputs.video_script || "";
  const summary = outputs.campaign_summary || "";

  return (
    <div className="space-y-6">
      {/* Campaign Summary */}
      {summary && (
        <div className="p-4 rounded-lg bg-sovereign-slate border border-sovereign-slate">
          <h3 className="text-sm font-semibold text-slate-300 uppercase mb-2">
            Campaign Summary
          </h3>
          <p className="text-sm text-slate-400 whitespace-pre-wrap">{summary}</p>
        </div>
      )}

      {/* Social Media Posts */}
      {posts.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-slate-300 uppercase mb-3 flex items-center gap-2">
            <Icon name="share" size={14} />
            Social Media Posts ({posts.length})
          </h3>
          <div className="space-y-3">
            {posts.map((post: any, idx: number) => (
              <div
                key={idx}
                className="p-4 rounded-lg bg-sovereign-slate border border-sovereign-slate"
              >
                <div className="flex items-center justify-between mb-2">
                  <Badge variant="blue">{post.platform || "Social"}</Badge>
                  {post.schedule_time && (
                    <span className="text-xs text-slate-500">
                      {new Date(post.schedule_time).toLocaleDateString()}
                    </span>
                  )}
                </div>
                <p className="text-sm text-slate-300 whitespace-pre-wrap">{post.content}</p>
                {post.hashtags && post.hashtags.length > 0 && (
                  <div className="mt-2 flex flex-wrap gap-1">
                    {post.hashtags.map((tag: string, i: number) => (
                      <span key={i} className="text-xs text-sovereign-blue">
                        #{tag}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Email Sequence */}
      {emailSequence.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-slate-300 uppercase mb-3 flex items-center gap-2">
            <Icon name="mail" size={14} />
            Email Sequence ({emailSequence.length})
          </h3>
          <div className="space-y-3">
            {emailSequence.map((email: any, idx: number) => (
              <div
                key={idx}
                className="p-4 rounded-lg bg-sovereign-slate border border-sovereign-slate"
              >
                <div className="text-xs text-slate-500 mb-1">Day {email.day}</div>
                <div className="text-sm font-semibold text-white mb-2">
                  {email.subject}
                </div>
                <p className="text-sm text-slate-400 whitespace-pre-wrap">
                  {email.body}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Video Script */}
      {videoScript && (
        <div>
          <h3 className="text-sm font-semibold text-slate-300 uppercase mb-3 flex items-center gap-2">
            <Icon name="video" size={14} />
            Video Script
          </h3>
          <div className="p-4 rounded-lg bg-sovereign-slate border border-sovereign-slate">
            <pre className="text-sm text-slate-300 whitespace-pre-wrap font-mono">
              {videoScript}
            </pre>
          </div>
        </div>
      )}

      {/* Generic Artifacts */}
      {artifacts.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-slate-300 uppercase mb-3 flex items-center gap-2">
            <Icon name="link" size={14} />
            Resources
          </h3>
          <div className="space-y-2">
            {artifacts.map((artifact) => (
              <ArtifactLink key={artifact.id} artifact={artifact} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ============================================================================
// LANDING PAGE ARTIFACTS
// ============================================================================

function LandingPageArtifacts({ artifacts, outputs }: { artifacts: Artifact[]; outputs: Record<string, any> }) {
  const headline = outputs.headline || "";
  const subheadline = outputs.subheadline || "";
  const sections = outputs.sections || [];
  const cta = outputs.cta || {};
  const imagePrompts = outputs.image_prompts || [];

  return (
    <div className="space-y-6">
      {/* Hero Section */}
      {(headline || subheadline) && (
        <div className="p-4 rounded-lg bg-sovereign-slate border border-sovereign-slate">
          <h3 className="text-sm font-semibold text-slate-300 uppercase mb-3">Hero Section</h3>
          {headline && (
            <h1 className="text-2xl font-bold text-white mb-2">{headline}</h1>
          )}
          {subheadline && (
            <p className="text-lg text-slate-400">{subheadline}</p>
          )}
        </div>
      )}

      {/* Page Sections */}
      {sections.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-slate-300 uppercase mb-3 flex items-center gap-2">
            <Icon name="layout" size={14} />
            Page Sections ({sections.length})
          </h3>
          <div className="space-y-4">
            {sections.map((section: any, idx: number) => (
              <div
                key={idx}
                className="p-4 rounded-lg bg-sovereign-slate border border-sovereign-slate"
              >
                <h4 className="text-base font-semibold text-white mb-2">
                  {section.title}
                </h4>
                <p className="text-sm text-slate-400 whitespace-pre-wrap">
                  {section.content}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Call to Action */}
      {cta.text && (
        <div className="p-4 rounded-lg bg-sovereign-gold/10 border border-sovereign-gold/30">
          <h3 className="text-sm font-semibold text-slate-300 uppercase mb-3">Call to Action</h3>
          <div className="flex items-center gap-4">
            <span className="text-lg font-bold text-sovereign-gold">{cta.text}</span>
            {cta.url && (
              <a
                href={cta.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-slate-400 hover:text-white"
              >
                {cta.url}
              </a>
            )}
          </div>
        </div>
      )}

      {/* Image Prompts */}
      {imagePrompts.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-slate-300 uppercase mb-3 flex items-center gap-2">
            <Icon name="image" size={14} />
            Image Prompts ({imagePrompts.length})
          </h3>
          <div className="space-y-2">
            {imagePrompts.map((prompt: string, idx: number) => (
              <div
                key={idx}
                className="p-3 rounded-lg bg-sovereign-slate border border-sovereign-slate text-sm text-slate-400"
              >
                {prompt}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Artifacts Links */}
      {artifacts.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-slate-300 uppercase mb-3 flex items-center gap-2">
            <Icon name="link" size={14} />
            Resources
          </h3>
          <div className="space-y-2">
            {artifacts.map((artifact) => (
              <ArtifactLink key={artifact.id} artifact={artifact} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ============================================================================
// PRODUCTS ARTIFACTS
// ============================================================================

function ProductsArtifacts({ artifacts, outputs }: { artifacts: Artifact[]; outputs: Record<string, any> }) {
  const products = outputs.products || [];

  return (
    <div className="space-y-6">
      {/* Products List */}
      {products.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-slate-300 uppercase mb-3 flex items-center gap-2">
            <Icon name="package" size={14} />
            Products ({products.length})
          </h3>
          <div className="space-y-4">
            {products.map((product: any, idx: number) => (
              <div
                key={idx}
                className="p-4 rounded-lg bg-sovereign-slate border border-sovereign-slate"
              >
                <div className="flex items-start justify-between mb-2">
                  <h4 className="text-base font-semibold text-white">{product.title}</h4>
                  {product.price && (
                    <Badge variant="gold">${product.price}</Badge>
                  )}
                </div>
                {product.description && (
                  <p className="text-sm text-slate-400 mb-3">
                    {product.description}
                  </p>
                )}
                {product.tags && product.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {product.tags.map((tag: string, i: number) => (
                      <Badge key={i} variant="blue">
                        {tag}
                      </Badge>
                    ))}
                  </div>
                )}
                {product.image_prompt && (
                  <div className="mt-3 pt-3 border-t border-sovereign-slate text-xs text-slate-500">
                    <span className="font-semibold">Image:</span> {product.image_prompt}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Artifacts Links */}
      {artifacts.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-slate-300 uppercase mb-3 flex items-center gap-2">
            <Icon name="link" size={14} />
            Resources
          </h3>
          <div className="space-y-2">
            {artifacts.map((artifact) => (
              <ArtifactLink key={artifact.id} artifact={artifact} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ============================================================================
// GENERIC ARTIFACTS
// ============================================================================

function GenericArtifacts({ artifacts, outputs }: { artifacts: Artifact[]; outputs: Record<string, any> }) {
  return (
    <div className="space-y-6">
      {/* Outputs (JSON) */}
      {Object.keys(outputs).length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-slate-300 uppercase mb-3 flex items-center gap-2">
            <Icon name="file" size={14} />
            Workflow Outputs
          </h3>
          <div className="p-4 rounded-lg bg-sovereign-slate border border-sovereign-slate">
            <pre className="text-xs text-slate-400 whitespace-pre-wrap font-mono overflow-x-auto">
              {JSON.stringify(outputs, null, 2)}
            </pre>
          </div>
        </div>
      )}

      {/* Artifacts */}
      {artifacts.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-slate-300 uppercase mb-3 flex items-center gap-2">
            <Icon name="link" size={14} />
            Artifacts ({artifacts.length})
          </h3>
          <div className="space-y-2">
            {artifacts.map((artifact) => (
              <ArtifactLink key={artifact.id} artifact={artifact} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ============================================================================
// ARTIFACT LINK COMPONENT
// ============================================================================

function ArtifactLink({ artifact }: { artifact: Artifact }) {
  const isUrl = artifact.value?.startsWith("http");

  return (
    <div className="flex items-center justify-between p-3 rounded-lg bg-sovereign-slate border border-sovereign-slate">
      <div className="flex items-center gap-3">
        <Icon name={isUrl ? "link" : "file"} size={16} className="text-slate-500" />
        <div>
          <div className="text-sm font-semibold text-white">{artifact.label}</div>
          <div className="text-xs text-slate-500">{artifact.kind}</div>
        </div>
      </div>
      {isUrl ? (
        <a
          href={artifact.value}
          target="_blank"
          rel="noopener noreferrer"
          className="text-xs text-sovereign-gold hover:underline"
        >
          View →
        </a>
      ) : (
        <span className="text-xs text-slate-500 font-mono max-w-xs truncate">
          {artifact.value}
        </span>
      )}
    </div>
  );
}
