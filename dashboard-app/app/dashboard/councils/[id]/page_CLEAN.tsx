import { fetchCouncil, fetchCouncilWorkflows } from "@/lib/api";
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
import { formatCurrency, formatPercentage } from "@/lib/design-system";

function formatDate(ts: number) {
  if (!ts) return "";
  return new Date(ts * 1000).toLocaleString();
}

export default async function CouncilConsolePage({ params }: { params: { id: string } }) {
  const councilId = params.id;
  const [council, workflows] = await Promise.all([
    fetchCouncil(councilId),
    fetchCouncilWorkflows(councilId)
  ]);

  const reviewed = workflows.filter(w => w.decision !== "pending");
  const totalReviewed = reviewed.length;
  const totalSavingsApproved = reviewed
    .filter(w => w.decision === "approved")
    .reduce((sum, w) => sum + (w.estimated_weekly_savings || 0), 0);
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
            <Avatar domain="governance" icon="shield" size="lg" />
            <div>
              <h1 className="text-2xl font-bold text-white flex items-center gap-2">
                {council.name}
                <Icon name="shield" size={20} className="text-sovereign-emerald" />
              </h1>
              <div className="flex items-center gap-2 text-sm text-slate-400 mt-1">
                <span className="font-mono">{council.domain}</span>
                <span>•</span>
                <StatusBadge status={council.status} />
              </div>
            </div>
          </div>
          <Badge variant="blue">
            <Icon name="info" size={12} className="inline mr-1" />
            {council.id}
          </Badge>
        </div>
        
        <p className="text-sm text-slate-300">{council.purpose}</p>
        
        <div className="flex flex-wrap gap-2">
          {council.primary_engines.map((engine) => (
            <Badge key={engine} variant="violet">
              <Icon name="brain" size={12} className="inline mr-1" />
              {engine.replace('_engine', '').replace(/_/g, ' ')}
            </Badge>
          ))}
        </div>
      </header>

      {/* Metrics Grid */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
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
          highlight
        />
        <StatCard
          icon="checkCircle"
          label="Approval Rate"
          value={`${approvalRate}%`}
          color="emerald"
        />
        <StatCard
          icon="workflow"
          label="Pending Workflows"
          value={pending.length}
          color={pending.length > 0 ? "violet" : "blue"}
        />
      </section>

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
                  <TableHead>Workflow ID</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Agent</TableHead>
                  <TableHead>Savings (weekly)</TableHead>
                  <TableHead>Created</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {pending.map(w => (
                  <TableRow key={w.id}>
                    <TableCell>
                      <span className="font-mono text-xs text-sovereign-blue">{w.id}</span>
                    </TableCell>
                    <TableCell>
                      <Badge variant="violet">{w.workflow_type_id}</Badge>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Avatar domain="commerce" icon="spark" size="sm" />
                        <span className="text-sm">{w.created_by_agent}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <span className="text-sovereign-gold font-semibold">
                        {w.estimated_weekly_savings
                          ? formatCurrency(w.estimated_weekly_savings)
                          : "—"}
                      </span>
                    </TableCell>
                    <TableCell className="text-xs text-slate-400">
                      {formatDate(w.created_at)}
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
              <Icon name="info" size={48} className="text-slate-600 mx-auto mb-3" />
              <p className="text-sm text-slate-400">
                No workflows have been reviewed yet.
              </p>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Workflow ID</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Agent</TableHead>
                  <TableHead>Decision</TableHead>
                  <TableHead>Savings (weekly)</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {reviewed
                  .slice()
                  .reverse()
                  .map(w => (
                    <TableRow key={w.id}>
                      <TableCell>
                        <span className="font-mono text-xs text-sovereign-blue">{w.id}</span>
                      </TableCell>
                      <TableCell>
                        <Badge variant="violet">{w.workflow_type_id}</Badge>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <Avatar domain="commerce" icon="spark" size="sm" />
                          <span className="text-sm">{w.created_by_agent}</span>
                        </div>
                      </TableCell>
                      <TableCell>
                        <StatusBadge status={w.decision} />
                      </TableCell>
                      <TableCell>
                        <span className="text-sovereign-gold font-semibold">
                          {w.estimated_weekly_savings
                            ? formatCurrency(w.estimated_weekly_savings)
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
