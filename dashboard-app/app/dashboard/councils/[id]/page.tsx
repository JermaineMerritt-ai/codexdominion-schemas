import {
  Icon,
  Card,
  CardHeader,
  CardBody,
  Badge,
  StatusBadge,
  Avatar,
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableCell,
  TableHead,
} from "@/components/ui";
import { formatCurrency, getCouncilTheme } from "@/lib/design-system";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";

// Core council schema (from database)
interface Council {
  id: string;
  name: string;
  purpose: string | null;
  domain: string | null;
  primary_engines: string[];
  oversight: {
    review_actions: boolean;
    review_threshold_weekly_savings: number;
    blocked_action_types: string[];
    requires_majority_vote: boolean;
    min_votes: number;
  } | null;
  status: string | null;
  created_at: string;
}

// Extended council data (with relationships from council_members junction table)
interface CouncilExtended extends Council {
  members: string[]; // agent_ids from council_members JOIN
  member_count: number;
  total_workflows: number;
  pending_workflows: number;
  total_savings: number;
}

// Core workflow schema (from workflows table)
interface Workflow {
  id: string;
  workflow_type_id: string | null; // References workflow_types.id
  action_type: string | null;
  created_by_agent: string | null; // References agents.id
  inputs: Record<string, any> | null;
  calculated_savings: {
    weekly?: number;
    monthly?: number;
    yearly?: number;
  } | null;
  status: string | null;
  decision: string | null;
  assigned_council_id: string | null; // References councils.id
  created_at: string;
  updated_at: string;
}

// Workflow metrics (from workflow_metrics table)
interface WorkflowMetrics {
  id: number; // SERIAL PRIMARY KEY
  workflow_id: string; // FK to workflows.id
  duration_seconds: number;
  estimated_weekly_savings: number;
  completed_at: string; // TIMESTAMP
}

// Extended workflow data for display (workflows JOIN workflow_metrics, agents, workflow_types, councils)
interface WorkflowExtended extends Workflow {
  agent_name?: string; // From agents JOIN
  workflow_type_name?: string; // From workflow_types JOIN
  council_name?: string; // From councils JOIN
  metrics?: WorkflowMetrics; // From workflow_metrics JOIN (1-to-1 or null if not completed)
}

// Legacy alias for backward compatibility
type WorkflowAction = WorkflowExtended;

async function fetchCouncil(councilId: string): Promise<CouncilExtended | null> {
  try {
    const res = await fetch(`${API_BASE}/api/councils/${councilId}`, { cache: "no-store" });
    if (!res.ok) return null;
    return res.json();
  } catch (err) {
    console.error("Error fetching council:", err);
    return null;
  }
}

async function fetchCouncilWorkflows(councilId: string): Promise<WorkflowAction[]> {
  try {
    const res = await fetch(`${API_BASE}/api/councils/${councilId}/workflows`, { cache: "no-store" });
    if (!res.ok) return [];
    const data = await res.json();
    return data.workflows || [];
  } catch (err) {
    console.error("Error fetching workflows:", err);
    return [];
  }
}

function formatDate(ts: string | number) {
  if (!ts) return "";
  if (typeof ts === 'number') {
    return new Date(ts * 1000).toLocaleString();
  }
  return new Date(ts).toLocaleString();
}

export default async function CouncilConsolePage({ params }: { params: { id: string } }) {
  const councilId = params.id;
  const [council, workflows] = await Promise.all([
    fetchCouncil(councilId),
    fetchCouncilWorkflows(councilId)
  ]);

  if (!council) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <Icon name="shield" size={48} className="text-slate-600 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-white mb-2">Council Not Found</h2>
          <p className="text-slate-400">The council "{councilId}" does not exist.</p>
        </div>
      </div>
    );
  }

  const theme = getCouncilTheme(council.id);
  const reviewed = workflows.filter(w => w.decision && w.decision !== "pending");
  const totalReviewed = reviewed.length;
  const totalSavingsApproved = reviewed
    .filter(w => w.decision === "approved")
    .reduce((sum, w) => sum + (w.calculated_savings?.weekly || 0), 0);
  const approvalRate =
    totalReviewed > 0
      ? Math.round(
          (reviewed.filter(w => w.decision === "approved").length / totalReviewed) * 100
        )
      : 0;

  const pending = workflows.filter(w => w.decision === "pending");

  return (
    <div className="space-y-6 max-w-5xl">
      {/* Header Section */}
      <header className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div 
              className="w-16 h-16 rounded-full flex items-center justify-center"
              style={{ backgroundColor: `${theme.color}20`, border: `2px solid ${theme.color}` }}
            >
              <div style={{ color: theme.color }}>
                <Icon name={theme.icon as any} size={32} />
              </div>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white flex items-center gap-2">
                {council.name}
              </h1>
              <div className="flex items-center gap-2 text-sm text-slate-400 mt-1">
                <span className="font-mono">{council.domain || 'default'}</span>
                <span>•</span>
                <StatusBadge status={council.status || 'active'} />
              </div>
            </div>
          </div>
          <Badge variant="blue">
            <Icon name="info" size={12} className="inline mr-1" />
            {council.id}
          </Badge>
        </div>
        
        <p className="text-sm text-slate-300">{council.purpose || 'No purpose defined'}</p>
        
        <div className="flex flex-wrap gap-2">
          {council.primary_engines.map((engine) => (
            <Badge key={engine} variant="violet">
              <Icon name="brain" size={12} className="inline mr-1" />
              {engine.replace('engine_', '').replace(/_/g, ' ')}
            </Badge>
          ))}
        </div>
      </header>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard
          icon="clipboard"
          label="Workflows Reviewed"
          value={totalReviewed}
          color="blue"
        />
        <StatCard
          icon="coins"
          label="Savings Approved"
          value={formatCurrency(totalSavingsApproved)}
          color="gold"
          highlight={totalSavingsApproved > 0}
        />
        <StatCard
          icon="checkCircle"
          label="Approval Rate"
          value={`${approvalRate}%`}
          color="emerald"
        />
        <StatCard
          icon="workflow"
          label="Pending Review"
          value={pending.length}
          color={pending.length > 0 ? "violet" : "blue"}
        />
      </div>

      {/* Oversight Configuration */}
      {council.oversight?.review_actions && (
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Icon name="shield" className="text-sovereign-emerald" />
              <h2 className="text-lg font-semibold text-white">Oversight Configuration</h2>
            </div>
          </CardHeader>
          <CardBody>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-slate-400">Review Threshold:</span>{" "}
                <span className="text-white font-semibold">
                  {formatCurrency(council.oversight.review_threshold_weekly_savings)}/week
                </span>
              </div>
              <div>
                <span className="text-slate-400">Voting:</span>{" "}
                <span className="text-white font-semibold">
                  {council.oversight.requires_majority_vote 
                    ? `Majority (${council.oversight.min_votes} min)` 
                    : "Single Approver"}
                </span>
              </div>
              {council.oversight.blocked_action_types.length > 0 && (
                <div className="md:col-span-2">
                  <span className="text-slate-400">Blocked Actions:</span>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {council.oversight.blocked_action_types.map((action) => (
                      <Badge key={action} variant="crimson">
                        <Icon name="xCircle" size={10} className="inline mr-1" />
                        {action.replace(/_/g, ' ')}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </CardBody>
        </Card>
      )}

      {/* Council Members */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Icon name="users" className="text-sovereign-blue" />
            <h2 className="text-lg font-semibold text-white">Council Members</h2>
          </div>
        </CardHeader>
        <CardBody>
          <div className="flex flex-wrap gap-3">
            {council.members.map((memberId) => (
              <div key={memberId} className="flex items-center gap-2 px-3 py-2 rounded-lg bg-sovereign-slate border border-sovereign-slate">
                <Avatar domain={council.domain || 'default'} icon="users" size="sm" />
                <span className="text-sm text-white font-medium">
                  {memberId.replace('agent_', '').replace(/_/g, ' ')}
                </span>
              </div>
            ))}
          </div>
        </CardBody>
      </Card>

      {/* Pending Review Section */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Icon name="workflow" className="text-sovereign-violet" />
              <h2 className="text-lg font-semibold text-white">Pending Review</h2>
            </div>
            <Badge variant={pending.length > 0 ? "violet" : "blue"}>
              {pending.length} pending
            </Badge>
          </div>
        </CardHeader>
        <CardBody>
          {pending.length === 0 ? (
            <div className="text-center py-8">
              <Icon name="checkCircle" size={48} className="text-sovereign-emerald mx-auto mb-3 opacity-50" />
              <p className="text-sm text-slate-400">
                No workflows pending review for this council.
              </p>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Agent</TableHead>
                  <TableHead>Action Type</TableHead>
                  <TableHead>Timestamp</TableHead>
                  <TableHead>Est. Savings</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {pending.map((w) => (
                  <TableRow key={w.id}>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Avatar domain={council.domain || 'default'} icon="users" size="sm" />
                        <span className="text-sm">
                          {w.created_by_agent?.replace('agent_', '').replace(/_/g, ' ') || 'Unknown'}
                        </span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge variant="violet">{w.action_type?.replace(/_/g, ' ') || 'N/A'}</Badge>
                    </TableCell>
                    <TableCell className="text-xs text-slate-400">
                      {formatDate(w.created_at)}
                    </TableCell>
                    <TableCell>
                      <span className="text-sovereign-gold font-semibold">
                        {w.calculated_savings?.weekly
                          ? formatCurrency(w.calculated_savings.weekly)
                          : "—"}
                      </span>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardBody>
      </Card>

      {/* Review History Section */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Icon name="clipboard" className="text-sovereign-blue" />
            <h2 className="text-lg font-semibold text-white">Review History</h2>
          </div>
        </CardHeader>
        <CardBody>
          {reviewed.length === 0 ? (
            <div className="text-center py-8">
              <Icon name="info" size={48} className="text-slate-600 mx-auto mb-3 opacity-50" />
              <p className="text-sm text-slate-400">
                No review history yet for this council.
              </p>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Agent</TableHead>
                  <TableHead>Action Type</TableHead>
                  <TableHead>Decision</TableHead>
                  <TableHead>Est. Savings</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {reviewed.slice(0, 10).map((w) => (
                  <TableRow key={w.id}>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Avatar domain={council.domain || 'default'} icon="users" size="sm" />
                        <span className="text-sm">
                          {w.created_by_agent?.replace('agent_', '').replace(/_/g, ' ') || 'Unknown'}
                        </span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge variant="blue">{w.action_type?.replace(/_/g, ' ') || 'N/A'}</Badge>
                    </TableCell>
                    <TableCell>
                      <StatusBadge status={w.decision || 'unknown'} />
                    </TableCell>
                    <TableCell>
                      <span className="text-sovereign-gold font-semibold">
                        {w.calculated_savings?.weekly
                          ? formatCurrency(w.calculated_savings.weekly)
                          : "—"}
                      </span>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardBody>
      </Card>
    </div>
  );
}

interface StatCardProps {
  icon: "clipboard" | "coins" | "checkCircle" | "workflow";
  label: string;
  value: string | number;
  color: "gold" | "blue" | "emerald" | "violet";
  highlight?: boolean;
}

function StatCard({ icon, label, value, color, highlight = false }: StatCardProps) {
  const colorMap = {
    gold: "text-sovereign-gold border-sovereign-gold/30 bg-sovereign-gold/5",
    blue: "text-sovereign-blue border-sovereign-blue/30 bg-sovereign-blue/5",
    emerald: "text-sovereign-emerald border-sovereign-emerald/30 bg-sovereign-emerald/5",
    violet: "text-sovereign-violet border-sovereign-violet/30 bg-sovereign-violet/5",
  };

  return (
    <Card className={highlight ? "ring-2 ring-sovereign-gold" : ""}>
      <CardBody className="flex items-center gap-3">
        <div className={`p-2 rounded-lg ${colorMap[color]}`}>
          <Icon name={icon} size={24} className={colorMap[color].split(" ")[0]} />
        </div>
        <div>
          <div className="text-xs uppercase text-slate-400 font-semibold">{label}</div>
          <div className="text-2xl font-bold text-white mt-0.5">{value}</div>
        </div>
      </CardBody>
    </Card>
  );
}
