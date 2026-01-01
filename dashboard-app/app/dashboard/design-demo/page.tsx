/**
 * Design System Demo - Component Showcase
 */

import {
  Icon,
  Card,
  CardHeader,
  CardBody,
  Avatar,
  Badge,
  Button,
  StatusBadge,
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableCell,
  TableHead,
} from "@/components/ui";
import { formatCurrency, formatPercentage } from "@/lib/design-system";

export default function DesignSystemDemo() {
  return (
    <div className="space-y-8 max-w-7xl mx-auto p-6">
      {/* Header */}
      <header>
        <div className="flex items-center gap-3 mb-2">
          <Icon name="crown" size={40} className="text-sovereign-gold" />
          <h1 className="text-3xl font-bold text-white">
            CodexDominion <span className="text-sovereign-gold">Design System</span>
          </h1>
        </div>
        <p className="text-slate-400">Premium component library for sovereign dashboards</p>
      </header>

      {/* Colors Section */}
      <Card>
        <CardHeader>
          <h2 className="text-lg font-bold text-white">Color Palette</h2>
        </CardHeader>
        <CardBody>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <ColorSwatch name="Imperial Gold" color="#F5C542" usage="Authority, savings, highlights" />
            <ColorSwatch name="Dominion Blue" color="#3B82F6" usage="System status, navigation" />
            <ColorSwatch name="Council Emerald" color="#10B981" usage="Approvals, success" />
            <ColorSwatch name="Crimson Review" color="#DC2626" usage="Denials, warnings" />
            <ColorSwatch name="Violet Pulse" color="#7C3AED" usage="AI intelligence" />
            <ColorSwatch name="Obsidian Black" color="#0F172A" usage="Backgrounds" />
            <ColorSwatch name="Slate Steel" color="#1E293B" usage="Borders, dividers" />
          </div>
        </CardBody>
      </Card>

      {/* Icons Section */}
      <Card>
        <CardHeader>
          <h2 className="text-lg font-bold text-white">Icons</h2>
        </CardHeader>
        <CardBody>
          <div className="grid grid-cols-4 md:grid-cols-8 gap-4">
            <IconDemo name="crown" label="Crown" />
            <IconDemo name="shield" label="Shield" />
            <IconDemo name="spark" label="Spark" />
            <IconDemo name="layers" label="Layers" />
            <IconDemo name="brain" label="Brain" />
            <IconDemo name="users" label="Users" />
            <IconDemo name="chart" label="Chart" />
            <IconDemo name="clipboard" label="Clipboard" />
            <IconDemo name="workflow" label="Workflow" />
            <IconDemo name="coins" label="Coins" />
            <IconDemo name="fire" label="Fire" />
            <IconDemo name="star" label="Star" />
          </div>
        </CardBody>
      </Card>

      {/* Avatars Section */}
      <Card>
        <CardHeader>
          <h2 className="text-lg font-bold text-white">Avatars</h2>
        </CardHeader>
        <CardBody>
          <div className="flex flex-wrap gap-6 items-end">
            <div className="text-center">
              <Avatar domain="commerce" icon="coins" size="sm" />
              <p className="text-xs mt-2 text-slate-400">Commerce (SM)</p>
            </div>
            <div className="text-center">
              <Avatar domain="governance" icon="shield" size="md" />
              <p className="text-xs mt-2 text-slate-400">Governance (MD)</p>
            </div>
            <div className="text-center">
              <Avatar domain="media" icon="spark" size="lg" />
              <p className="text-xs mt-2 text-slate-400">Media (LG)</p>
            </div>
            <div className="text-center">
              <Avatar domain="youth" icon="star" size="xl" />
              <p className="text-xs mt-2 text-slate-400">Youth (XL)</p>
            </div>
          </div>
        </CardBody>
      </Card>

      {/* Badges Section */}
      <Card>
        <CardHeader>
          <h2 className="text-lg font-bold text-white">Badges</h2>
        </CardHeader>
        <CardBody>
          <div className="flex flex-wrap gap-3">
            <Badge variant="gold">Ultimate</Badge>
            <Badge variant="emerald">Approved</Badge>
            <Badge variant="blue">Pending</Badge>
            <Badge variant="violet">AI Mode</Badge>
            <Badge variant="crimson">Denied</Badge>
            <StatusBadge status="completed" />
            <StatusBadge status="in_progress" />
            <StatusBadge status="failed" />
          </div>
        </CardBody>
      </Card>

      {/* Buttons Section */}
      <Card>
        <CardHeader>
          <h2 className="text-lg font-bold text-white">Buttons</h2>
        </CardHeader>
        <CardBody>
          <div className="flex flex-wrap gap-3">
            <Button variant="primary" icon="crown">
              Execute Workflow
            </Button>
            <Button variant="secondary" icon="settings">
              Configure
            </Button>
            <Button variant="danger" icon="trash">
              Delete
            </Button>
            <Button variant="ghost" icon="eye">
              View Details
            </Button>
          </div>
        </CardBody>
      </Card>

      {/* Table Section */}
      <Card>
        <CardHeader>
          <h2 className="text-lg font-bold text-white">Data Table</h2>
        </CardHeader>
        <CardBody>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Agent</TableHead>
                <TableHead>Domain</TableHead>
                <TableHead>Savings</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <Avatar domain="commerce" icon="coins" size="sm" />
                    <span className="font-medium">Jermaine SuperAction</span>
                  </div>
                </TableCell>
                <TableCell>Commerce</TableCell>
                <TableCell className="text-sovereign-gold font-bold">
                  {formatCurrency(25000)}
                </TableCell>
                <TableCell>
                  <StatusBadge status="completed" />
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <Avatar domain="governance" icon="shield" size="sm" />
                    <span className="font-medium">Council Prime</span>
                  </div>
                </TableCell>
                <TableCell>Governance</TableCell>
                <TableCell className="text-sovereign-gold font-bold">
                  {formatCurrency(18000)}
                </TableCell>
                <TableCell>
                  <StatusBadge status="approved" />
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </CardBody>
      </Card>

      {/* Stat Cards Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardBody className="flex items-center gap-3">
            <div className="p-3 rounded-lg bg-sovereign-gold/10 border border-sovereign-gold/30">
              <Icon name="coins" size={28} className="text-sovereign-gold" />
            </div>
            <div>
              <div className="text-xs uppercase text-slate-400 font-semibold">Total Savings</div>
              <div className="text-3xl font-bold text-white">{formatCurrency(95000)}</div>
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody className="flex items-center gap-3">
            <div className="p-3 rounded-lg bg-sovereign-emerald/10 border border-sovereign-emerald/30">
              <Icon name="checkCircle" size={28} className="text-sovereign-emerald" />
            </div>
            <div>
              <div className="text-xs uppercase text-slate-400 font-semibold">Completed</div>
              <div className="text-3xl font-bold text-white">127</div>
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody className="flex items-center gap-3">
            <div className="p-3 rounded-lg bg-sovereign-blue/10 border border-sovereign-blue/30">
              <Icon name="star" size={28} className="text-sovereign-blue" />
            </div>
            <div>
              <div className="text-xs uppercase text-slate-400 font-semibold">Success Rate</div>
              <div className="text-3xl font-bold text-white">{formatPercentage(0.94)}</div>
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}

// Helper Components
function ColorSwatch({ name, color, usage }: { name: string; color: string; usage: string }) {
  return (
    <div className="space-y-2">
      <div
        className="h-20 rounded-lg border border-sovereign-slate"
        style={{ backgroundColor: color }}
      />
      <div>
        <p className="text-sm font-semibold text-white">{name}</p>
        <p className="text-xs text-slate-400">{usage}</p>
        <code className="text-xs text-slate-500">{color}</code>
      </div>
    </div>
  );
}

function IconDemo({ name, label }: { name: any; label: string }) {
  return (
    <div className="flex flex-col items-center gap-2 p-3 rounded-lg hover:bg-sovereign-slate transition-colors">
      <Icon name={name} size={24} className="text-sovereign-gold" />
      <p className="text-xs text-slate-400">{label}</p>
    </div>
  );
}
