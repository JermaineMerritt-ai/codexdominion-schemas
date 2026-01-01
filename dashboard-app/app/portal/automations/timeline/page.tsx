import { Icon, Card, CardHeader, CardBody, Badge, StatusBadge } from "@/components/ui";
import Link from "next/link";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";

// Hardcoded tenant for demo
const TENANT_ID = "tenant_codexdominion";

interface AutomationEvent {
  id: string;
  automation_id: string;
  automation_name: string;
  automation_category: string;
  trigger_type: string;
  timestamp: string;
  result: "success" | "skipped" | "failed";
  message: string;
  workflow: {
    id: string;
    status: string;
  } | null;
  metadata: Record<string, any>;
}

interface TimelineStats {
  total_events: number;
  success: number;
  skipped: number;
  failed: number;
  by_category: Record<string, number>;
}

async function fetchTimeline(category?: string, result?: string, days: number = 30): Promise<{
  events: AutomationEvent[];
  stats: TimelineStats;
  total_count: number;
}> {
  try {
    const params = new URLSearchParams({
      days: days.toString(),
      limit: '100'
    });
    
    if (category && category !== 'All') {
      params.append('category', category);
    }
    
    if (result && result !== 'All') {
      params.append('result', result);
    }
    
    const res = await fetch(
      `${API_BASE}/api/automation-timeline/tenant/${TENANT_ID}?${params}`,
      { cache: 'no-store' }
    );
    
    if (!res.ok) {
      console.error('Failed to fetch timeline:', res.status);
      return { events: [], stats: { total_events: 0, success: 0, skipped: 0, failed: 0, by_category: {} }, total_count: 0 };
    }
    
    return res.json();
  } catch (err) {
    console.error('Error fetching timeline:', err);
    return { events: [], stats: { total_events: 0, success: 0, skipped: 0, failed: 0, by_category: {} }, total_count: 0 };
  }
}

function formatTimestamp(ts: string): string {
  const date = new Date(ts);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);
  
  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
  if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
  if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
  
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' });
}

function getResultIcon(result: string): { icon: "checkCircle" | "info" | "xCircle", color: string } {
  switch (result) {
    case 'success':
      return { icon: 'checkCircle', color: 'text-sovereign-emerald' };
    case 'skipped':
      return { icon: 'info', color: 'text-sovereign-blue' };
    case 'failed':
      return { icon: 'xCircle', color: 'text-sovereign-crimson' };
    default:
      return { icon: 'info', color: 'text-slate-400' };
  }
}

function getTriggerLabel(triggerType: string): string {
  const labels: Record<string, string> = {
    'event': 'Event-triggered',
    'schedule': 'Scheduled',
    'threshold': 'Threshold-based',
    'behavior': 'Behavior-based'
  };
  return labels[triggerType] || triggerType;
}

export default async function AutomationTimelinePage({
  searchParams
}: {
  searchParams: { category?: string; result?: string; days?: string }
}) {
  const category = searchParams.category || 'All';
  const result = searchParams.result || 'All';
  const days = parseInt(searchParams.days || '30');
  
  const { events, stats, total_count } = await fetchTimeline(
    category !== 'All' ? category : undefined,
    result !== 'All' ? result : undefined,
    days
  );
  
  const categories = ['All', 'Store', 'Marketing', 'Website', 'Customer Behavior', 'Analytics'];
  const resultFilters = ['All', 'success', 'skipped', 'Errors'];
  
  return (
    <div className="space-y-6 max-w-5xl">
      {/* Header */}
      <header>
        <h1 className="text-2xl font-bold text-white mb-2">Automation Timeline</h1>
        <p className="text-sm text-slate-400">
          A history of every automation that has fired across your empire.
        </p>
      </header>
      
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard
          icon="activity"
          label="Total Events"
          value={stats.total_events}
          color="blue"
        />
        <StatCard
          icon="checkCircle"
          label="Successful"
          value={stats.success}
          color="emerald"
        />
        <StatCard
          icon="info"
          label="Skipped"
          value={stats.skipped}
          color="blue"
        />
        <StatCard
          icon="xCircle"
          label="Failed"
          value={stats.failed}
          color="crimson"
          highlight={stats.failed > 0}
        />
      </div>
      
      {/* Filters */}
      <Card>
        <CardBody className="space-y-4">
          {/* Category Filters */}
          <div>
            <div className="text-xs uppercase text-slate-400 font-semibold mb-2">Category</div>
            <div className="flex flex-wrap gap-2">
              {categories.map((cat) => (
                <Link key={cat} href={`/portal/automations/timeline?category=${cat}&result=${result}&days=${days}`}>
                  <Badge
                    variant={category === cat ? 'gold' : 'slate'}
                    className="cursor-pointer hover:opacity-80 transition-opacity"
                  >
                    {cat}
                    {cat !== 'All' && stats.by_category[cat] && (
                      <span className="ml-1 opacity-70">({stats.by_category[cat]})</span>
                    )}
                  </Badge>
                </Link>
              ))}
            </div>
          </div>
          
          {/* Result Filters */}
          <div>
            <div className="text-xs uppercase text-slate-400 font-semibold mb-2">Result</div>
            <div className="flex flex-wrap gap-2">
              {resultFilters.map((res) => (
                <Link key={res} href={`/portal/automations/timeline?category=${category}&result=${res}&days=${days}`}>
                  <Badge
                    variant={result === res ? 'gold' : 'slate'}
                    className="cursor-pointer hover:opacity-80 transition-opacity"
                  >
                    {res === 'Errors' ? 'Errors' : res.charAt(0).toUpperCase() + res.slice(1)}
                  </Badge>
                </Link>
              ))}
            </div>
          </div>
          
          {/* Time Range */}
          <div>
            <div className="text-xs uppercase text-slate-400 font-semibold mb-2">Time Range</div>
            <div className="flex flex-wrap gap-2">
              {[7, 30, 90].map((d) => (
                <Link key={d} href={`/portal/automations/timeline?category=${category}&result=${result}&days=${d}`}>
                  <Badge
                    variant={days === d ? 'gold' : 'slate'}
                    className="cursor-pointer hover:opacity-80 transition-opacity"
                  >
                    {d} days
                  </Badge>
                </Link>
              ))}
            </div>
          </div>
        </CardBody>
      </Card>
      
      {/* Timeline */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Icon name="clock" className="text-sovereign-blue" />
              <h2 className="text-lg font-semibold text-white">Timeline</h2>
            </div>
            <Badge variant="blue">{total_count} events</Badge>
          </div>
        </CardHeader>
        <CardBody>
          {events.length === 0 ? (
            <div className="text-center py-12">
              <Icon name="clock" size={48} className="text-slate-600 mx-auto mb-3 opacity-50" />
              <p className="text-sm text-slate-400">
                No automation events found for the selected filters.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {events.map((event) => (
                <TimelineEntry key={event.id} event={event} />
              ))}
            </div>
          )}
        </CardBody>
      </Card>
    </div>
  );
}

interface StatCardProps {
  icon: "activity" | "checkCircle" | "info" | "xCircle";
  label: string;
  value: number;
  color: "gold" | "blue" | "emerald" | "crimson";
  highlight?: boolean;
}

function StatCard({ icon, label, value, color, highlight = false }: StatCardProps) {
  const colorMap = {
    gold: "text-sovereign-gold border-sovereign-gold/30 bg-sovereign-gold/5",
    blue: "text-sovereign-blue border-sovereign-blue/30 bg-sovereign-blue/5",
    emerald: "text-sovereign-emerald border-sovereign-emerald/30 bg-sovereign-emerald/5",
    crimson: "text-sovereign-crimson border-sovereign-crimson/30 bg-sovereign-crimson/5",
  };

  return (
    <Card className={highlight ? "ring-2 ring-sovereign-crimson" : ""}>
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

function TimelineEntry({ event }: { event: AutomationEvent }) {
  const { icon, color } = getResultIcon(event.result);
  const triggerLabel = getTriggerLabel(event.trigger_type);
  const timestamp = formatTimestamp(event.timestamp);
  
  const resultLabels: Record<string, string> = {
    'success': 'Fired',
    'skipped': 'Skipped',
    'failed': 'Failed'
  };
  const resultLabel = resultLabels[event.result] || 'Unknown';
  
  return (
    <div className="flex gap-4 p-4 rounded-lg border border-sovereign-slate bg-sovereign-obsidian/30 hover:bg-sovereign-obsidian/50 transition-colors">
      {/* Icon */}
      <div className="flex-shrink-0 mt-1">
        <div className={`p-2 rounded-lg bg-sovereign-slate border border-sovereign-slate ${color}`}>
          <Icon name={icon} size={20} />
        </div>
      </div>
      
      {/* Content */}
      <div className="flex-1 min-w-0">
        {/* Header */}
        <div className="flex items-start justify-between gap-2 mb-2">
          <div>
            <h3 className="text-white font-semibold">
              {event.automation_name} {resultLabel}
            </h3>
            <div className="flex items-center gap-2 mt-1">
              <Badge variant="slate" className="text-xs">
                {triggerLabel}
              </Badge>
              <Badge variant="slate" className="text-xs">
                {event.automation_category}
              </Badge>
            </div>
          </div>
          <div className="text-xs text-slate-400 whitespace-nowrap">
            {timestamp}
          </div>
        </div>
        
        {/* Message */}
        <p className="text-sm text-slate-300 mb-2">
          {event.message}
        </p>
        
        {/* Workflow Link */}
        {event.workflow && (
          <Link
            href={`/portal/workflows/${event.workflow.id}`}
            className="inline-flex items-center gap-1 text-xs text-sovereign-gold hover:underline"
          >
            <Icon name="arrowRight" size={12} />
            View workflow
          </Link>
        )}
        
        {/* Metadata (for failed events) */}
        {event.result === 'failed' && event.metadata && Object.keys(event.metadata).length > 0 && (
          <details className="mt-3">
            <summary className="text-xs text-slate-400 cursor-pointer hover:text-slate-300">
              View error details
            </summary>
            <pre className="mt-2 text-xs text-slate-400 bg-sovereign-slate/30 p-2 rounded overflow-x-auto">
              {JSON.stringify(event.metadata, null, 2)}
            </pre>
          </details>
        )}
      </div>
    </div>
  );
}
