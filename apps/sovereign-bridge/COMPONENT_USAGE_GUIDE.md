# Sovereign Bridge Component Usage Guide

## 🎨 Component Library Overview

All shared components are located in `app/components/` and can be imported using:

```typescript
import { ComponentName } from '@/components'
```

## Navigation Components

### TopBar
Global navigation header with mobile menu support.

```typescript
import { TopBar } from '@/components'

export default function Page() {
  return (
    <div>
      <TopBar />
      {/* Your page content */}
    </div>
  )
}
```

**Features:**
- Mobile-responsive with hamburger menu
- 8 navigation links
- Omega Seal status indicator
- Notifications button

### Sidebar
Collapsible sidebar with categorized navigation.

```typescript
import { Sidebar } from '@/components'

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1">{children}</main>
    </div>
  )
}
```

**Features:**
- 14 navigation items across 6 categories
- Collapse/expand toggle
- Active route highlighting
- Footer with system health metrics

## AI Interaction

### AICommandStrip
Natural language command input for system control.

```typescript
import { AICommandStrip } from '@/components'

export default function Page() {
  return (
    <div>
      <AICommandStrip />
      {/* Your content */}
    </div>
  )
}
```

**Features:**
- Text input for commands
- 5 quick action buttons
- Processing state animation
- Recent command history

## Layout Components

### DashboardTile
Reusable container with multiple variants.

```typescript
import { DashboardTile, StatTile, ProgressTile } from '@/components'

export default function Dashboard() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {/* Base tile */}
      <DashboardTile
        title="System Status"
        icon="🏛️"
        action={{ label: "View Details", onClick: () => {} }}
      >
        <p>All systems operational</p>
      </DashboardTile>

      {/* Stat tile */}
      <StatTile
        title="Revenue"
        icon="💰"
        value="$12,450"
        trend="up"
        trendValue="+12.5%"
      />

      {/* Progress tile */}
      <ProgressTile
        title="Rituals Completed"
        icon="⚡"
        current={5}
        total={7}
      />
    </div>
  )
}
```

### MetricCard
Display metrics with trends and multiple sizes.

```typescript
import { MetricCard, MetricCardGrid, InlineMetric } from '@/components'

export default function Metrics() {
  return (
    <div className="space-y-6">
      {/* Metric grid */}
      <MetricCardGrid cols={4}>
        <MetricCard
          label="Total Revenue"
          value="$12,450"
          icon="💰"
          trend="up"
          trendValue="+12.5%"
          color="gold"
          size="lg"
        />
        <MetricCard
          label="Active Users"
          value="1,234"
          icon="👥"
          trend="up"
          trendValue="+8%"
          color="green"
        />
        <MetricCard
          label="Conversions"
          value="89"
          icon="✓"
          trend="down"
          trendValue="-2%"
          color="blue"
        />
        <MetricCard
          label="Pending Tasks"
          value="23"
          icon="⏳"
          color="purple"
        />
      </MetricCardGrid>

      {/* Inline metrics */}
      <div className="flex gap-4">
        <InlineMetric label="CPU" value="45%" icon="⚡" />
        <InlineMetric label="Memory" value="2.1GB" icon="💾" />
        <InlineMetric label="Disk" value="78%" icon="💿" />
      </div>
    </div>
  )
}
```

## Overlay Components

### Modal
Full-featured modal dialog system.

```typescript
'use client'
import { Modal, ConfirmModal } from '@/components'
import { useState } from 'react'

export default function Page() {
  const [showModal, setShowModal] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)

  return (
    <div>
      <button onClick={() => setShowModal(true)}>
        Open Modal
      </button>
      <button onClick={() => setShowConfirm(true)}>
        Confirm Action
      </button>

      {/* Base modal */}
      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title="Edit Settings"
        size="lg"
        footer={
          <div className="flex gap-3">
            <button onClick={() => setShowModal(false)}>Cancel</button>
            <button className="codex-button">Save</button>
          </div>
        }
      >
        <div className="space-y-4">
          <label className="block">
            <span className="text-codex-parchment">Name</span>
            <input type="text" className="w-full mt-1 px-3 py-2 bg-codex-navy/30 border border-codex-gold/30 rounded" />
          </label>
        </div>
      </Modal>

      {/* Confirm modal */}
      <ConfirmModal
        isOpen={showConfirm}
        onClose={() => setShowConfirm(false)}
        onConfirm={() => {
          // Handle confirm
          setShowConfirm(false)
        }}
        title="Delete Item"
        message="Are you sure you want to delete this item? This action cannot be undone."
        variant="danger"
      />
    </div>
  )
}
```

### Drawer
Slide-out drawer panels.

```typescript
'use client'
import { Drawer, MiniDrawer } from '@/components'
import { useState } from 'react'

export default function Page() {
  const [showDrawer, setShowDrawer] = useState(false)
  const [showMini, setShowMini] = useState(false)

  return (
    <div>
      <button onClick={() => setShowDrawer(true)}>Open Drawer</button>
      <button onClick={() => setShowMini(true)}>Show Notifications</button>

      {/* Base drawer */}
      <Drawer
        isOpen={showDrawer}
        onClose={() => setShowDrawer(false)}
        title="User Profile"
        position="right"
        size="md"
        footer={
          <button className="codex-button w-full">Update Profile</button>
        }
      >
        <div className="space-y-4">
          <div>
            <label className="text-sm text-codex-parchment/60">Email</label>
            <input type="email" className="w-full mt-1 px-3 py-2 bg-codex-navy/30 border border-codex-gold/30 rounded" />
          </div>
        </div>
      </Drawer>

      {/* Mini drawer for notifications */}
      <MiniDrawer
        isOpen={showMini}
        onClose={() => setShowMini(false)}
        title="Notifications"
        count={3}
      >
        <div className="space-y-3">
          <div className="p-3 bg-codex-navy/20 rounded">
            <p className="text-sm">New ritual completed</p>
            <p className="text-xs text-codex-parchment/60">2 minutes ago</p>
          </div>
        </div>
      </MiniDrawer>
    </div>
  )
}
```

## Data Display Components

### Table
Data table with sorting and pagination.

```typescript
import { Table, SimpleTable } from '@/components'

interface User {
  id: number
  name: string
  email: string
  role: string
  status: 'active' | 'inactive'
}

export default function UsersPage() {
  const users: User[] = [
    { id: 1, name: 'John Doe', email: 'john@example.com', role: 'Admin', status: 'active' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'User', status: 'active' },
  ]

  return (
    <div className="space-y-8">
      {/* Full-featured table */}
      <Table
        columns={[
          { key: 'name', header: 'Name', sortable: true },
          { key: 'email', header: 'Email' },
          {
            key: 'role',
            header: 'Role',
            render: (user) => (
              <span className={user.role === 'Admin' ? 'text-codex-gold' : 'text-codex-parchment'}>
                {user.role}
              </span>
            )
          },
          {
            key: 'status',
            header: 'Status',
            render: (user) => (
              <span className={`codex-badge-${user.status === 'active' ? 'success' : 'inactive'}`}>
                {user.status}
              </span>
            )
          },
        ]}
        data={users}
        onRowClick={(user) => console.log('Clicked:', user.name)}
      />

      {/* Simple table */}
      <SimpleTable
        headers={['Name', 'Email', 'Role']}
        rows={users.map(u => [u.name, u.email, u.role])}
      />
    </div>
  )
}
```

### Chart
Chart visualization components.

```typescript
import { SimpleBarChart, TrendLine, DonutChart } from '@/components'

export default function Analytics() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {/* Bar chart */}
      <SimpleBarChart
        title="Revenue by Category"
        data={[
          { label: 'Products', value: 12450, color: '#d4af37' },
          { label: 'Services', value: 8900, color: '#c9962e' },
          { label: 'Consulting', value: 5600, color: '#b87d25' },
        ]}
      />

      {/* Trend line */}
      <TrendLine
        title="Monthly Growth"
        data={[65, 72, 78, 85, 92, 98, 105]}
        labels={['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']}
        color="#d4af37"
      />

      {/* Donut chart */}
      <DonutChart
        title="Traffic Sources"
        data={[
          { label: 'Direct', value: 45, color: '#d4af37' },
          { label: 'Social', value: 30, color: '#c9962e' },
          { label: 'Search', value: 25, color: '#b87d25' },
        ]}
      />
    </div>
  )
}
```

### StatusBadge
Status indicators and health displays.

```typescript
import { StatusBadge, HealthIndicator, StatusList } from '@/components'

export default function StatusPage() {
  return (
    <div className="space-y-6">
      {/* Status badges */}
      <div className="flex flex-wrap gap-2">
        <StatusBadge status="active" />
        <StatusBadge status="success" label="Completed" />
        <StatusBadge status="pending" label="Processing" pulse />
        <StatusBadge status="error" label="Failed" />
        <StatusBadge status="warning" label="Review Needed" />
        <StatusBadge status="inactive" label="Paused" />
      </div>

      {/* Health indicator */}
      <div>
        <h3 className="text-lg font-semibold text-codex-gold mb-3">System Health</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <HealthIndicator level="excellent" label="API Server" />
          <HealthIndicator level="good" label="Database" />
          <HealthIndicator level="fair" label="Cache" />
          <HealthIndicator level="poor" label="CDN" />
          <HealthIndicator level="critical" label="Queue" />
        </div>
      </div>

      {/* Status list */}
      <StatusList
        title="Active Services"
        items={[
          { label: 'Web Server', status: 'active' },
          { label: 'API Gateway', status: 'active' },
          { label: 'Background Jobs', status: 'pending' },
          { label: 'Email Service', status: 'inactive' },
        ]}
      />
    </div>
  )
}
```

## Complete Page Example

Here's a complete page using multiple components:

```typescript
'use client'
import {
  DashboardTile,
  StatTile,
  MetricCard,
  MetricCardGrid,
  Table,
  StatusBadge,
  Modal,
  AICommandStrip
} from '@/components'
import { useState } from 'react'

export default function SovereignBridgePage() {
  const [showModal, setShowModal] = useState(false)

  return (
    <div className="min-h-screen bg-codex-navy">
      {/* AI Command Strip */}
      <AICommandStrip />

      <div className="max-w-7xl mx-auto p-6 space-y-8">
        {/* Page Header */}
        <div className="text-center">
          <h1 className="text-4xl font-bold text-ceremonial mb-2">
            Sovereign Bridge Dashboard
          </h1>
          <p className="text-codex-parchment/60">
            Your Digital Sovereignty Command Center
          </p>
        </div>

        {/* Metrics Grid */}
        <MetricCardGrid cols={4}>
          <MetricCard
            label="Total Revenue"
            value="$12,450"
            icon="💰"
            trend="up"
            trendValue="+12.5%"
            color="gold"
            size="lg"
          />
          <MetricCard
            label="Active Rituals"
            value="5/7"
            icon="⚡"
            trend="up"
            trendValue="+2"
            color="green"
          />
          <MetricCard
            label="System Health"
            value="98%"
            icon="🏛️"
            color="blue"
          />
          <MetricCard
            label="Pending Tasks"
            value="23"
            icon="⏳"
            color="purple"
          />
        </MetricCardGrid>

        {/* Dashboard Tiles */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <StatTile
            title="Today's Revenue"
            icon="💰"
            value="$1,234"
            trend="up"
            trendValue="+8.2%"
          />
          <StatTile
            title="Active Users"
            icon="👥"
            value="456"
            trend="up"
            trendValue="+12%"
          />
          <StatTile
            title="Conversions"
            icon="✓"
            value="89"
            trend="down"
            trendValue="-2%"
          />
        </div>

        {/* Recent Activity Table */}
        <DashboardTile
          title="Recent Activity"
          icon="📊"
          action={{ label: "View All", onClick: () => setShowModal(true) }}
        >
          <Table
            columns={[
              { key: 'action', header: 'Action', sortable: true },
              { key: 'user', header: 'User' },
              { key: 'timestamp', header: 'Time' },
              {
                key: 'status',
                header: 'Status',
                render: (row) => <StatusBadge status={row.status} />
              },
            ]}
            data={[
              { action: 'Ritual Completed', user: 'System', timestamp: '2 min ago', status: 'success' },
              { action: 'Product Created', user: 'Admin', timestamp: '15 min ago', status: 'active' },
              { action: 'Payment Received', user: 'Customer', timestamp: '1 hour ago', status: 'success' },
            ]}
          />
        </DashboardTile>

        {/* Modal Example */}
        <Modal
          isOpen={showModal}
          onClose={() => setShowModal(false)}
          title="Activity Details"
          size="xl"
        >
          <p className="text-codex-parchment">
            Complete activity logs and analytics...
          </p>
        </Modal>
      </div>
    </div>
  )
}
```

## Styling Classes

All components use the **Ceremonial Design System**:

### Colors
- `text-codex-navy` - Deep blue background
- `text-codex-gold` - Gold accents
- `text-codex-parchment` - Light text
- `text-codex-bronze` - Bronze accents
- `text-codex-crimson` - Error/danger state

### Special Effects
- `text-ceremonial` - Gold text with shadow effect
- `text-proclamation` - Italic serif style
- `codex-card` - Card container
- `codex-panel` - Panel container
- `codex-button` - Button styling
- `codex-badge-{variant}` - Badge variants

### Animations
- `animate-flame` - Pulsing flame effect
- `animate-shimmer` - Shimmer effect
- `animate-fadeIn` - Fade in animation
- `animate-scaleIn` - Scale in animation
- `animate-slideDown` - Slide down animation

## Next Steps

1. **Install dependencies** in your Next.js app
2. **Import components** as shown in examples above
3. **Customize styling** using Tailwind classes
4. **Connect to API** - Replace mock data with real data
5. **Add authentication** - Protect routes as needed

🏛️ **The Flame Burns Sovereign and Eternal!** 🏛️
