import {
  Icon,
  Card,
  CardHeader,
  CardBody,
  Badge,
  StatusBadge,
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableCell,
  TableHead,
} from "@/components/ui";
import { colors } from "@/lib/design-system";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";

interface DebugLog {
  id: string;
  timestamp: string;
  trigger_fired: boolean;
  all_conditions_passed: boolean;
  result: string;
  execution_time_ms: number;
  workflow_id: string | null;
  has_errors: boolean;
  has_warnings: boolean;
}

interface ConditionResult {
  condition: string;
  passed: boolean;
  actual_value: any;
  expected?: string;
}

interface ActionResult {
  action: string;
  status: string;
  workflow_id?: string;
}

interface DebugLogDetails {
  id: string;
  automation_id: string;
  timestamp: string;
  trigger_fired: boolean;
  trigger_type: string;
  trigger_details: Record<string, any>;
  next_scheduled_run: string | null;
  conditions_evaluated: ConditionResult[];
  all_conditions_passed: boolean;
  actions_taken: ActionResult[];
  actions_skipped: ActionResult[];
  execution_time_ms: number;
  errors: string[];
  warnings: string[];
  data_snapshot: Record<string, any>;
  result: string;
  workflow_id: string | null;
}

async function fetchAutomationLogs(automationId: string, days: number = 7): Promise<{
  automation_id: string;
  automation_name: string;
  total_logs: number;
  logs: DebugLog[];
  summary: {
    total_runs: number;
    successful: number;
    skipped: number;
    failed: number;
    avg_execution_time_ms: number;
  };
}> {
  try {
    const res = await fetch(
      `${API_BASE}/api/automation-debugger/${automationId}/logs?days=${days}`,
      { cache: 'no-store' }
    );
    
    if (!res.ok) {
      console.error('Failed to fetch debug logs:', res.status);
      return {
        automation_id: automationId,
        automation_name: 'Unknown',
        total_logs: 0,
        logs: [],
        summary: { total_runs: 0, successful: 0, skipped: 0, failed: 0, avg_execution_time_ms: 0 }
      };
    }
    
    return res.json();
  } catch (err) {
    console.error('Error fetching debug logs:', err);
    return {
      automation_id: automationId,
      automation_name: 'Unknown',
      total_logs: 0,
      logs: [],
      summary: { total_runs: 0, successful: 0, skipped: 0, failed: 0, avg_execution_time_ms: 0 }
    };
  }
}

async function fetchLatestLog(automationId: string): Promise<DebugLogDetails | null> {
  try {
    const res = await fetch(
      `${API_BASE}/api/automation-debugger/${automationId}/latest`,
      { cache: 'no-store' }
    );
    
    if (!res.ok) return null;
    return res.json();
  } catch (err) {
    console.error('Error fetching latest log:', err);
    return null;
  }
}

function formatTimestamp(ts: string): string {
  const date = new Date(ts);
  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    second: '2-digit'
  });
}

export default async function AutomationDebuggerPage({
  searchParams
}: {
  searchParams: { automation?: string; days?: string }
}) {
  const automationId = searchParams.automation || 'auto_weekly_social';
  const days = parseInt(searchParams.days || '7');
  
  const [logsData, latestLog] = await Promise.all([
    fetchAutomationLogs(automationId, days),
    fetchLatestLog(automationId)
  ]);

  return (
    <div className="space-y-6 max-w-7xl">
      {/* Header */}
      <header className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white flex items-center gap-2">
              <Icon name="bug" size={28} className="text-sovereign-violet" />
              Automation Debugger
            </h1>
            <p className="text-sm text-slate-400 mt-1">
              The truth table of your empire - see exactly why automations trigger or don't
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="blue">
              <Icon name="clock" size={12} className="inline mr-1" />
              Last {days} days
            </Badge>
          </div>
        </div>
        
        <div className="flex items-center gap-2 text-sm">
          <span className="text-slate-400">Debugging:</span>
          <Badge variant="violet">{logsData.automation_name}</Badge>
        </div>
      </header>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <StatCard
          icon="activity"
          label="Total Runs"
          value={logsData.summary.total_runs}
          color="blue"
        />
        <StatCard
          icon="checkCircle"
          label="Successful"
          value={logsData.summary.successful}
          color="emerald"
        />
        <StatCard
          icon="info"
          label="Skipped"
          value={logsData.summary.skipped}
          color="blue"
        />
        <StatCard
          icon="xCircle"
          label="Failed"
          value={logsData.summary.failed}
          color="crimson"
        />
        <StatCard
          icon="clock"
          label="Avg Time"
          value={`${logsData.summary.avg_execution_time_ms}ms`}
          color="violet"
        />
      </div>

      {/* Latest Execution Deep Dive */}
      {latestLog && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Icon name="search" className="text-sovereign-violet" />
                <h2 className="text-lg font-semibold text-white">Latest Execution Analysis</h2>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-400">
                  {formatTimestamp(latestLog.timestamp)}
                </span>
                <StatusBadge status={latestLog.result} />
              </div>
            </div>
          </CardHeader>
          <CardBody>
            <div className="space-y-6">
              {/* Trigger Evaluation */}
              <div>
                <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
                  <Icon name="zap" size={16} className="text-sovereign-gold" />
                  Trigger Evaluation
                </h3>
                <div className="bg-sovereign-slate rounded-lg p-4 border border-sovereign-slate">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-sm text-slate-300">
                        Type: <Badge variant="blue">{latestLog.trigger_type}</Badge>
                      </div>
                      {latestLog.next_scheduled_run && (
                        <div className="text-xs text-slate-400 mt-1">
                          Next run: {formatTimestamp(latestLog.next_scheduled_run)}
                        </div>
                      )}
                    </div>
                    <div className="flex items-center gap-2">
                      {latestLog.trigger_fired ? (
                        <>
                          <Icon name="checkCircle" size={20} className="text-sovereign-emerald" />
                          <span className="text-sm font-medium text-sovereign-emerald">Fired</span>
                        </>
                      ) : (
                        <>
                          <Icon name="clock" size={20} className="text-slate-400" />
                          <span className="text-sm font-medium text-slate-400">Waiting</span>
                        </>
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {/* Condition Breakdown */}
              <div>
                <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
                  <Icon name="list" size={16} className="text-sovereign-gold" />
                  Condition Breakdown
                </h3>
                <div className="space-y-2">
                  {latestLog.conditions_evaluated.map((condition, idx) => (
                    <div
                      key={idx}
                      className={`p-3 rounded-lg border ${
                        condition.passed
                          ? 'bg-sovereign-emerald/10 border-sovereign-emerald/30'
                          : 'bg-sovereign-crimson/10 border-sovereign-crimson/30'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <Icon
                            name={condition.passed ? 'checkCircle' : 'xCircle'}
                            size={18}
                            className={condition.passed ? 'text-sovereign-emerald' : 'text-sovereign-crimson'}
                          />
                          <div>
                            <div className="text-sm font-medium text-white">
                              {condition.condition}
                            </div>
                            <div className="text-xs text-slate-400 mt-0.5">
                              Actual: <span className="font-mono">{JSON.stringify(condition.actual_value)}</span>
                              {condition.expected && (
                                <> · Expected: <span className="font-mono">{condition.expected}</span></>
                              )}
                            </div>
                          </div>
                        </div>
                        <Badge variant={condition.passed ? 'emerald' : 'crimson'}>
                          {condition.passed ? 'Passed' : 'Failed'}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Action Results */}
              <div>
                <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
                  <Icon name="workflow" size={16} className="text-sovereign-gold" />
                  Actions
                </h3>
                <div className="space-y-2">
                  {latestLog.actions_taken.map((action, idx) => (
                    <div
                      key={idx}
                      className="p-3 rounded-lg bg-sovereign-emerald/10 border border-sovereign-emerald/30"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Icon name="checkCircle" size={16} className="text-sovereign-emerald" />
                          <span className="text-sm text-white">{action.action}</span>
                        </div>
                        {action.workflow_id && (
                          <Badge variant="blue">
                            <Icon name="workflow" size={10} className="inline mr-1" />
                            {action.workflow_id}
                          </Badge>
                        )}
                      </div>
                    </div>
                  ))}
                  
                  {latestLog.actions_skipped.map((action, idx) => (
                    <div
                      key={idx}
                      className="p-3 rounded-lg bg-slate-700/30 border border-slate-600/30"
                    >
                      <div className="flex items-center gap-2">
                        <Icon name="info" size={16} className="text-slate-400" />
                        <span className="text-sm text-slate-300">{action.action}</span>
                        <Badge variant="blue">Skipped</Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Errors & Warnings */}
              {(latestLog.errors.length > 0 || latestLog.warnings.length > 0) && (
                <div>
                  <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
                    <Icon name="alert" size={16} className="text-sovereign-crimson" />
                    Diagnostics
                  </h3>
                  <div className="space-y-2">
                    {latestLog.errors.map((error, idx) => (
                      <div key={idx} className="p-3 rounded-lg bg-sovereign-crimson/10 border border-sovereign-crimson/30">
                        <div className="flex items-center gap-2">
                          <Icon name="xCircle" size={16} className="text-sovereign-crimson" />
                          <span className="text-sm text-white font-mono">{error}</span>
                        </div>
                      </div>
                    ))}
                    
                    {latestLog.warnings.map((warning, idx) => (
                      <div key={idx} className="p-3 rounded-lg bg-yellow-500/10 border border-yellow-500/30">
                        <div className="flex items-center gap-2">
                          <Icon name="alert" size={16} className="text-yellow-400" />
                          <span className="text-sm text-white">{warning}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Performance */}
              <div className="flex items-center justify-between pt-4 border-t border-slate-700">
                <div className="text-sm text-slate-400">
                  <Icon name="clock" size={14} className="inline mr-1" />
                  Execution time: <span className="font-semibold text-white">{latestLog.execution_time_ms}ms</span>
                </div>
                {latestLog.workflow_id && (
                  <Badge variant="violet">
                    <Icon name="workflow" size={12} className="inline mr-1" />
                    Workflow: {latestLog.workflow_id}
                  </Badge>
                )}
              </div>
            </div>
          </CardBody>
        </Card>
      )}

      {/* Execution History */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Icon name="list" className="text-sovereign-blue" />
            <h2 className="text-lg font-semibold text-white">Execution History</h2>
          </div>
        </CardHeader>
        <CardBody>
          {logsData.logs.length === 0 ? (
            <div className="text-center py-8">
              <Icon name="info" size={48} className="text-slate-600 mx-auto mb-3 opacity-50" />
              <p className="text-sm text-slate-400">
                No execution logs found for this automation in the last {days} days.
              </p>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Timestamp</TableHead>
                  <TableHead>Trigger</TableHead>
                  <TableHead>Conditions</TableHead>
                  <TableHead>Result</TableHead>
                  <TableHead>Time</TableHead>
                  <TableHead>Workflow</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {logsData.logs.map((log) => (
                  <TableRow key={log.id}>
                    <TableCell className="text-xs text-slate-400">
                      {formatTimestamp(log.timestamp)}
                    </TableCell>
                    <TableCell>
                      {log.trigger_fired ? (
                        <Icon name="checkCircle" size={16} className="text-sovereign-emerald" />
                      ) : (
                        <Icon name="clock" size={16} className="text-slate-400" />
                      )}
                    </TableCell>
                    <TableCell>
                      {log.all_conditions_passed ? (
                        <Badge variant="emerald">All Passed</Badge>
                      ) : (
                        <Badge variant="crimson">Failed</Badge>
                      )}
                    </TableCell>
                    <TableCell>
                      <StatusBadge status={log.result} />
                    </TableCell>
                    <TableCell className="text-xs text-slate-300">
                      {log.execution_time_ms}ms
                    </TableCell>
                    <TableCell>
                      {log.workflow_id ? (
                        <Badge variant="blue">{log.workflow_id}</Badge>
                      ) : (
                        <span className="text-xs text-slate-500">—</span>
                      )}
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
  icon: "activity" | "checkCircle" | "info" | "xCircle" | "clock";
  label: string;
  value: string | number;
  color: "gold" | "blue" | "emerald" | "violet" | "crimson";
}

function StatCard({ icon, label, value, color }: StatCardProps) {
  const colorMap = {
    gold: "text-sovereign-gold border-sovereign-gold/30 bg-sovereign-gold/5",
    blue: "text-sovereign-blue border-sovereign-blue/30 bg-sovereign-blue/5",
    emerald: "text-sovereign-emerald border-sovereign-emerald/30 bg-sovereign-emerald/5",
    violet: "text-sovereign-violet border-sovereign-violet/30 bg-sovereign-violet/5",
    crimson: "text-sovereign-crimson border-sovereign-crimson/30 bg-sovereign-crimson/5",
  };

  return (
    <Card>
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
