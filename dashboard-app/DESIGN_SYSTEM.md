# 🎨 CodexDominion Sovereign Design System

**Premium dashboard aesthetics for the digital sovereign**

## Installation

```bash
npm install lucide-react
```

## Quick Start

```tsx
import { Icon, Card, CardHeader, CardBody, Avatar, Badge, Button } from "@/components/ui";
import { formatCurrency, styles } from "@/lib/design-system";

export default function MyPage() {
  return (
    <Card>
      <CardHeader>
        <Icon name="crown" className="text-sovereign-gold" />
        <h2>My Component</h2>
      </CardHeader>
      <CardBody>
        <Badge variant="gold">Premium</Badge>
        <Avatar domain="commerce" icon="coins" size="md" />
      </CardBody>
    </Card>
  );
}
```

## Color Palette

### Primary Colors
- **Imperial Gold** `#F5C542` - Authority, mastery, sovereignty
- **Dominion Blue** `#3B82F6` - Clarity, intelligence, stability
- **Council Emerald** `#10B981` - Governance, trust, alignment

### Secondary Colors
- **Obsidian Black** `#0F172A` - Backgrounds, panels
- **Slate Steel** `#1E293B` - Borders, dividers
- **Violet Pulse** `#7C3AED` - AI intelligence indicators
- **Crimson Review** `#DC2626` - Warnings, denials

### Tailwind Classes
```tsx
className="bg-sovereign-gold text-sovereign-obsidian border-sovereign-slate"
```

## Components

### Icon
```tsx
import { Icon } from "@/components/ui";

<Icon name="crown" size={24} className="text-sovereign-gold" />
<Icon name="shield" strokeWidth={2} />
<Icon name="spark" color="#F5C542" />
```

**Available icons:** crown, shield, spark, layers, brain, users, chart, clipboard, workflow, coins, check, star, fire

### Avatar
```tsx
import { Avatar } from "@/components/ui";

<Avatar domain="commerce" icon="coins" size="md" />
<Avatar domain="governance" icon="shield" size="lg" />
<Avatar domain="media" icon="spark" size="sm" />
```

**Domains:** commerce (gold), governance (emerald), media (violet), youth (blue), research (slate), creator (pink)

### Card
```tsx
import { Card, CardHeader, CardBody } from "@/components/ui";

<Card>
  <CardHeader>
    <h2>Title</h2>
  </CardHeader>
  <CardBody>
    Content here
  </CardBody>
</Card>
```

### Badge
```tsx
import { Badge } from "@/components/ui";

<Badge variant="gold">Ultimate</Badge>
<Badge variant="emerald">Approved</Badge>
<Badge variant="crimson">Denied</Badge>
<Badge variant="blue">Pending</Badge>
<Badge variant="violet">AI Mode</Badge>
```

### Button
```tsx
import { Button } from "@/components/ui";

<Button variant="primary" icon="crown">Execute</Button>
<Button variant="secondary">Cancel</Button>
<Button variant="danger" icon="trash">Delete</Button>
<Button variant="ghost">More</Button>
```

### StatusBadge
```tsx
import { StatusBadge } from "@/components/ui";

<StatusBadge status="completed" />
<StatusBadge status="pending" />
<StatusBadge status="failed" />
```

Auto-colors based on status: completed/approved/success (emerald), pending/processing (blue), failed/rejected/denied (crimson)

### Table
```tsx
import { Table, TableHeader, TableBody, TableRow, TableCell, TableHead } from "@/components/ui";

<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Name</TableHead>
      <TableHead>Status</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell>Agent 1</TableCell>
      <TableCell><StatusBadge status="completed" /></TableCell>
    </TableRow>
  </TableBody>
</Table>
```

## Utility Functions

```tsx
import { formatCurrency, formatPercentage, getStatusColor } from "@/lib/design-system";

formatCurrency(15000) // "$15,000"
formatPercentage(0.89) // "89%"
getStatusColor("completed") // "#10B981"
```

## Style Constants

```tsx
import { styles } from "@/lib/design-system";

<div className={styles.card}>...</div>
<button className={styles.button.primary}>Click</button>
<span className={styles.badge.gold}>Gold</span>
<p className={styles.text.heading}>Title</p>
```

## Design Principles

1. **Bold & Sovereign** - Gold accents, crown icons, authoritative typography
2. **Dark Mode First** - Obsidian backgrounds, subtle borders
3. **Icon Consistency** - 18-20px, 1.5px stroke, Lucide React
4. **Card-Based Layout** - 8px rounded corners, subtle shadows
5. **Color-Coded Domains** - Instant recognition through consistent palette

## Examples

### Dashboard Header
```tsx
<header className="flex items-center justify-between">
  <div className="flex items-center gap-3">
    <Icon name="crown" size={32} className="text-sovereign-gold" />
    <h1 className="text-2xl font-bold">
      CODEXDOMINION <span className="text-sovereign-gold">Dashboard</span>
    </h1>
  </div>
  <Badge variant="emerald">
    <Icon name="checkCircle" size={14} className="inline mr-1" />
    Operational
  </Badge>
</header>
```

### Stat Card with Icon
```tsx
<Card>
  <CardBody className="flex items-center gap-3">
    <div className="p-2 rounded-lg bg-sovereign-gold/5 border border-sovereign-gold/30">
      <Icon name="coins" size={24} className="text-sovereign-gold" />
    </div>
    <div>
      <div className="text-xs uppercase text-slate-400 font-semibold">Total Savings</div>
      <div className="text-2xl font-bold text-white">{formatCurrency(95000)}</div>
    </div>
  </CardBody>
</Card>
```

### Agent Row with Avatar
```tsx
<div className="flex items-center gap-3">
  <Avatar domain="commerce" icon="spark" size="sm" />
  <div className="flex-1">
    <div className="font-medium text-white">Jermaine SuperAction</div>
    <div className="text-xs text-slate-400">agent_jermaine_super_action</div>
  </div>
  <div className="text-sovereign-gold font-bold">
    {formatCurrency(25000)}
  </div>
</div>
```

---

🔥 **The Design Burns Sovereign and Eternal!** 👑
