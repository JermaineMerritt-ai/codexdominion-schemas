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
import { formatCurrency } from "@/lib/design-system";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";

// Core agent schema (from database)
interface Agent {
  id: string;
  name: string;
  role: string | null;
  personality: string | null;
  mode: string | null;
  avatar_icon: string | null;
  avatar_color: string | null;
  created_at: string;
}

// Agent reputation (from agent_reputation table)
interface AgentReputation {
  score: number;
  total_savings: number;
  workflows_executed: number;
  approval_rate: number;
  updated_at: string;
}

// Agent training (from agent_training table)
interface AgentTraining {
  strengths: string[];
  weaknesses: string[];
  restricted_workflow_types: string[];
  last_feedback: string | null;
  updated_at: string;
}

// Extended agent data (computed from relationships + reputation + training joins)
interface AgentExtended extends Agent {
  domain: string;
  reputation: AgentReputation | null;
  training: AgentTraining | null;
  engines: string[];
  councils: Array<{
    id: string;
    name: string;
    domain: string | null;
    status: string | null;
  }>;
  status: "active" | "inactive" | "training";
  last_active: string;
}

// Workflow metrics (from workflow_metrics table)
interface WorkflowMetrics {
  id: number; // SERIAL PRIMARY KEY
  workflow_id: string; // FK to workflows.id
  duration_seconds: number;
  estimated_weekly_savings: number;
  completed_at: string; // TIMESTAMP
}

// Workflow history for display (workflows JOIN workflow_metrics)
interface WorkflowHistory {
  id: string;
  workflow_type: string;
  council_id: string;
  council_name: string;
  decision: "pending" | "approved" | "denied";
  estimated_savings: number; // From workflow_metrics JOIN
  duration_seconds: number; // From workflow_metrics JOIN
  timestamp: number;
  feedback?: string;
}

interface AgentMetrics {
  avg_duration_seconds: number;
  councils_count: number;
  recent_workflows_count: number;
}

interface TrainingNote {
  id: string;
  note: string;
  council_id: string;
  timestamp: number;
  type: "feedback" | "improvement" | "commendation";
}

async function fetchAgent(agentId: string): Promise<AgentExtended | null> {
  try {
    const res = await fetch(`${API_BASE}/api/agents/${agentId}`, { cache: "no-store" });
    if (!res.ok) return null;
    return res.json();
  } catch (err) {
    console.error("Error fetching agent:", err);
    return null;
  }
}

async function fetchAgentMetrics(agentId: string): Promise<AgentMetrics> {
  try {
    const res = await fetch(`${API_BASE}/api/agents/${agentId}/metrics`, { cache: "no-store" });
    if (!res.ok) return { avg_duration_seconds: 0, councils_count: 0, recent_workflows_count: 0 };
    return res.json();
  } catch (err) {
    console.error("Error fetching agent metrics:", err);
    return { avg_duration_seconds: 0, councils_count: 0, recent_workflows_count: 0 };
  }
}

async function fetchAgentWorkflows(agentId: string): Promise<WorkflowHistory[]> {
  try {
    const res = await fetch(`${API_BASE}/api/agents/${agentId}/workflows`, { cache: "no-store" });
    if (!res.ok) return [];
    const data = await res.json();
    return data.workflows || [];
  } catch (err) {
    console.error("Error fetching agent workflows:", err);
    return [];
  }
}

async function fetchAgentTrainingNotes(agentId: string): Promise<TrainingNote[]> {
  try {
    const res = await fetch(`${API_BASE}/api/agents/${agentId}/training`, { cache: "no-store" });
    if (!res.ok) return [];
    const data = await res.json();
    return data.notes || [];
  } catch (err) {
    console.error("Error fetching training notes:", err);
    return [];
  }
}

function formatDuration(seconds: number): string {
  if (seconds < 60) return `${seconds}s`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ${seconds % 60}s`;
  return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m`;
}

function formatDate(ts: number): string {
  if (!ts) return "";
  return new Date(ts * 1000).toLocaleString();
}

function getReputationColor(score: number): string {
  if (score >= 90) return "text-sovereign-gold";
  if (score >= 75) return "text-sovereign-emerald";
  if (score >= 50) return "text-sovereign-blue";
  return "text-sovereign-crimson";
}

function getReputationLabel(score: number): string {
  if (score >= 90) return "Elite";
  if (score >= 75) return "Excellent";
  if (score >= 50) return "Competent";
  return "Learning";
}

export default async function AgentProfilePage({ params }: { params: { id: string } }) {
  const agentId = params.id;
  const [agent, metrics, workflows, trainingNotes] = await Promise.all([
    fetchAgent(agentId),
    fetchAgentMetrics(agentId),
    fetchAgentWorkflows(agentId),
    fetchAgentTrainingNotes(agentId)
  ]);

  if (!agent) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <Icon name="users" size={48} className="text-slate-600 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-white mb-2">Agent Not Found</h2>
          <p className="text-slate-400">The agent "{agentId}" does not exist.</p>
        </div>
      </div>
    );
  }

  const recentWorkflows = workflows.slice(0, 10);
  const latestNote = trainingNotes[0];

  return (
    <div className="space-y-6 max-w-6xl">
      {/* Header Section */}
      <header className="space-y-4">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-4">
            <div 
              className="w-20 h-20 rounded-full flex items-center justify-center"
              style={{ 
                backgroundColor: agent.avatar_color || '#1e293b',
                border: `3px solid ${agent.avatar_color || '#1e293b'}40`
              }}
            >
              <Icon name={(agent.avatar_icon as any) || "users"} size={40} className="text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                {agent.name}
                <span className={`text-2xl font-bold ${getReputationColor(agent.reputation?.score || 0)}`}>
                  {agent.reputation?.score || 0}
                </span>
              </h1>
              <div className="flex items-center gap-3 mt-2">
                <Badge variant="blue">{agent.role || 'Agent'}</Badge>
                <Badge variant={getReputationLabel(agent.reputation?.score || 0) === "Elite" ? "gold" : "violet"}>
                  {getReputationLabel(agent.reputation?.score || 0)}
                </Badge>
                <StatusBadge status={agent.status} />
                {agent.mode && <Badge variant="violet">{agent.mode}</Badge>}
              </div>
              {agent.personality && (
                <p className="text-sm text-slate-400 mt-2 italic">"{agent.personality}"</p>
              )}
            </div>
          </div>
          <div className="text-right text-sm">
            <div className="text-slate-400">Member Since</div>
            <div className="text-white font-semibold">{new Date(agent.created_at).toLocaleDateString()}</div>
            <div className="text-slate-400 mt-2">Last Active</div>
            <div className="text-white font-semibold">{new Date(agent.last_active).toLocaleDateString()}</div>
          </div>
        </div>

        {/* Domain & Engine Tags */}
        <div className="flex flex-wrap gap-2">
          <Badge variant="emerald">
            <Icon name="layers" size={12} className="inline mr-1" />
            {agent.domain}
          </Badge>
          {agent.engines.map((engine) => (
            <Badge key={engine} variant="violet">
              <Icon name="brain" size={12} className="inline mr-1" />
              {engine.replace('engine_', '').replace(/_/g, ' ')}
            </Badge>
          ))}
        </div>
      </header>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <MetricCard
          icon="coins"
          label="Total Savings"
          value={formatCurrency(agent.reputation?.total_savings || 0)}
          color="gold"
          highlight={(agent.reputation?.total_savings || 0) > 10000}
        />
        <MetricCard
          icon="workflow"
          label="Workflows Executed"
          value={agent.reputation?.workflows_executed || 0}
          color="blue"
        />
        <MetricCard
          icon="checkCircle"
          label="Approval Rate"
          value={`${((agent.reputation?.approval_rate || 0) * 100).toFixed(1)}%`}
          color="emerald"
        />
        <MetricCard
          icon="spark"
          label="Avg Duration"
          value={formatDuration(metrics.avg_duration_seconds)}
          color="violet"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Strengths */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Icon name="star" className="text-sovereign-gold" />
              <h2 className="text-lg font-semibold text-white">Strengths</h2>
            </div>
          </CardHeader>
          <CardBody>
            {(!agent.training?.strengths || agent.training.strengths.length === 0) ? (
              <p className="text-sm text-slate-400">No strengths defined yet.</p>
            ) : (
              <div className="flex flex-wrap gap-2">
                {agent.training.strengths.map((strength) => (
                  <Badge key={strength} variant="emerald">
                    <Icon name="check" size={10} className="inline mr-1" />
                    {strength.replace(/_/g, ' ')}
                  </Badge>
                ))}
              </div>
            )}
          </CardBody>
        </Card>

        {/* Weaknesses */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Icon name="alert" className="text-sovereign-crimson" />
              <h2 className="text-lg font-semibold text-white">Areas for Growth</h2>
            </div>
          </CardHeader>
          <CardBody>
            {(!agent.training?.weaknesses || agent.training.weaknesses.length === 0) ? (
              <p className="text-sm text-slate-400">No weaknesses identified.</p>
            ) : (
              <div className="flex flex-wrap gap-2">
                {agent.training.weaknesses.map((weakness) => (
                  <Badge key={weakness} variant="crimson">
                    <Icon name="alert" size={10} className="inline mr-1" />
                    {weakness.replace(/_/g, ' ')}
                  </Badge>
                ))}
              </div>
            )}
          </CardBody>
        </Card>
      </div>

      {/* Restricted Workflows */}
      {(agent.training?.restricted_workflow_types && agent.training.restricted_workflow_types.length > 0) && (
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Icon name="shield" className="text-sovereign-crimson" />
              <h2 className="text-lg font-semibold text-white">Restricted Workflow Types</h2>
            </div>
          </CardHeader>
          <CardBody>
            <div className="flex flex-wrap gap-2">
              {agent.training.restricted_workflow_types.map((workflow) => (
                <Badge key={workflow} variant="crimson">
                  <Icon name="xCircle" size={10} className="inline mr-1" />
                  {workflow.replace(/_/g, ' ')}
                </Badge>
              ))}
            </div>
          </CardBody>
        </Card>
      )}

      {/* Governance Integration */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Icon name="crown" className="text-sovereign-gold" />
            <h2 className="text-lg font-semibold text-white">Council Membership</h2>
          </div>
        </CardHeader>
        <CardBody>
          {agent.councils.length === 0 ? (
            <p className="text-sm text-slate-400">Not assigned to any councils.</p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {agent.councils.map((council) => (
                <Badge key={council.id} variant="blue">
                  <Icon name="shield" size={10} className="inline mr-1" />
                  {council.name}
                </Badge>
              ))}
            </div>
          )}
        </CardBody>
      </Card>

      {/* Training Notes */}
      {trainingNotes.length > 0 && (
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Icon name="clipboard" className="text-sovereign-blue" />
              <h2 className="text-lg font-semibold text-white">Training Notes</h2>
            </div>
          </CardHeader>
          <CardBody className="space-y-3">
            {trainingNotes.slice(0, 5).map((note) => (
              <div key={note.id} className="p-3 rounded-lg bg-sovereign-slate border border-sovereign-slate">
                <div className="flex items-start justify-between mb-2">
                  <Badge variant={
                    note.type === "commendation" ? "emerald" :
                    note.type === "improvement" ? "violet" : "blue"
                  }>
                    {note.type}
                  </Badge>
                  <span className="text-xs text-slate-400">{formatDate(note.timestamp)}</span>
                </div>
                <p className="text-sm text-slate-300">{note.note}</p>
                <div className="mt-2 text-xs text-slate-400">
                  From: {note.council_id.replace('council_', '').replace(/_/g, ' ')}
                </div>
              </div>
            ))}
            {latestNote && (
              <div className="mt-4 pt-4 border-t border-sovereign-slate">
                <div className="text-xs text-slate-400 mb-2">Latest Feedback</div>
                <p className="text-sm text-white">{latestNote.note}</p>
              </div>
            )}
          </CardBody>
        </Card>
      )}

      {/* Workflow History */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Icon name="clipboard" className="text-sovereign-blue" />
              <h2 className="text-lg font-semibold text-white">Workflow History</h2>
            </div>
            <Badge variant="blue">{workflows.length} total</Badge>
          </div>
        </CardHeader>
        <CardBody>
          {recentWorkflows.length === 0 ? (
            <div className="text-center py-8">
              <Icon name="workflow" size={48} className="text-slate-600 mx-auto mb-3 opacity-50" />
              <p className="text-sm text-slate-400">No workflows executed yet.</p>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Workflow Type</TableHead>
                  <TableHead>Council</TableHead>
                  <TableHead>Decision</TableHead>
                  <TableHead>Savings</TableHead>
                  <TableHead>Duration</TableHead>
                  <TableHead>Timestamp</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {recentWorkflows.map((workflow) => (
                  <TableRow key={workflow.id}>
                    <TableCell>
                      <Badge variant="violet">{workflow.workflow_type.replace(/_/g, ' ')}</Badge>
                    </TableCell>
                    <TableCell className="text-sm text-slate-300">
                      {workflow.council_name || workflow.council_id.replace('council_', '').replace(/_/g, ' ')}
                    </TableCell>
                    <TableCell>
                      <StatusBadge status={workflow.decision} />
                    </TableCell>
                    <TableCell>
                      <span className="text-sovereign-gold font-semibold">
                        {workflow.estimated_savings > 0 ? formatCurrency(workflow.estimated_savings) : "—"}
                      </span>
                    </TableCell>
                    <TableCell className="text-sm text-slate-400">
                      {formatDuration(workflow.duration_seconds)}
                    </TableCell>
                    <TableCell className="text-xs text-slate-400">
                      {formatDate(workflow.timestamp)}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardBody>
      </Card>

      {/* Approval Patterns */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardBody className="text-center">
            <Icon name="checkCircle" size={32} className="text-sovereign-emerald mx-auto mb-2" />
            <div className="text-2xl font-bold text-white">
              {workflows.filter(w => w.decision === "approved").length}
            </div>
            <div className="text-xs uppercase text-slate-400 font-semibold mt-1">Approved</div>
          </CardBody>
        </Card>
        <Card>
          <CardBody className="text-center">
            <Icon name="workflow" size={32} className="text-sovereign-violet mx-auto mb-2" />
            <div className="text-2xl font-bold text-white">
              {workflows.filter(w => w.decision === "pending").length}
            </div>
            <div className="text-xs uppercase text-slate-400 font-semibold mt-1">Pending</div>
          </CardBody>
        </Card>
        <Card>
          <CardBody className="text-center">
            <Icon name="xCircle" size={32} className="text-sovereign-crimson mx-auto mb-2" />
            <div className="text-2xl font-bold text-white">
              {workflows.filter(w => w.decision === "denied").length}
            </div>
            <div className="text-xs uppercase text-slate-400 font-semibold mt-1">Denied</div>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}

interface MetricCardProps {
  icon: "coins" | "workflow" | "checkCircle" | "spark";
  label: string;
  value: string | number;
  color: "gold" | "blue" | "emerald" | "violet";
  highlight?: boolean;
}

function MetricCard({ icon, label, value, color, highlight = false }: MetricCardProps) {
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
