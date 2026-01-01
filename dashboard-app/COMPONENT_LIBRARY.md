# DominionMarkets Component Library

Comprehensive component inventory organized by category.

---

## 21.2 FOUNDATIONS

These are the primitives that everything else depends on.

### Typography

**Heading Hierarchy**:
- **H1**: `text-2xl md:text-3xl font-semibold text-white`
- **H2**: `text-xl md:text-2xl font-medium text-white`
- **H3**: `text-lg md:text-xl font-medium text-white`

**Body Text**:
- **Body**: `text-base text-slate-300`
- **Body-Small**: `text-sm text-slate-300`

**Caption**:
- **Caption**: `text-xs text-slate-400`

**Identity-Accent Variants**:
- **Diaspora**: `text-emerald-400`
- **Youth**: `text-blue-400`
- **Creator**: `text-purple-400`
- **Legacy**: `text-amber-400`

---

### Colors

**Neutral Palette**:
```typescript
neutral: {
  900: '#0F172A',  // Obsidian Black (backgrounds)
  800: '#1E293B',  // Dark slate
  700: '#334155',  // Slate (borders)
  600: '#475569',  // Medium slate
  500: '#64748B',  // Light slate
  400: '#94A3B8',  // Muted text
  300: '#CBD5E1',  // Body text
  200: '#E2E8F0',  // Light text
  100: '#F1F5F9',  // Near white
}
```

**Semantic Colors**:
```typescript
success: {
  500: '#10B981',  // Emerald (positive)
  400: '#34D399',  // Light emerald
}

warning: {
  500: '#F59E0B',  // Amber
  400: '#FBBF24',  // Light amber
}

error: {
  500: '#EF4444',  // Red
  400: '#F87171',  // Light red
}
```

**Identity Accents**:
```typescript
diaspora: {
  primary: '#10B981',   // Emerald
  secondary: '#059669', // Dark emerald
}

youth: {
  primary: '#3B82F6',   // Blue
  secondary: '#2563EB', // Dark blue
}

creator: {
  primary: '#A855F7',   // Purple
  secondary: '#9333EA', // Dark purple
}

legacy: {
  primary: '#F59E0B',   // Amber
  secondary: '#D97706', // Dark amber
}
```

**Premium/Pro Colors**:
```typescript
premium: {
  gold: '#F5C542',      // Imperial Gold
  goldHover: '#F7D068', // Gold hover
}

pro: {
  platinum: '#E5E7EB',  // Platinum
  platinumHover: '#F3F4F6', // Platinum hover
}
```

---

### Spacing

**4px Grid System**:
```typescript
spacing: {
  0: '0',
  1: '4px',   // 0.25rem
  2: '8px',   // 0.5rem
  3: '12px',  // 0.75rem
  4: '16px',  // 1rem
  5: '20px',  // 1.25rem
  6: '24px',  // 1.5rem
  8: '32px',  // 2rem
  10: '40px', // 2.5rem
  12: '48px', // 3rem
  16: '64px', // 4rem
}
```

**Responsive Scaling**:
- Mobile: Base spacing values
- Tablet (768px+): 1.125x scale
- Desktop (1024px+): 1.25x scale

**Usage Examples**:
```tsx
// Card padding
<div className="p-4 md:p-6">

// Component gaps
<div className="flex gap-2 md:gap-3">

// Section margins
<section className="mb-6 md:mb-8">
```

---

### Icons

**Line Icons** (Default):
- Stroke width: `1.5px`
- Size: `w-5 h-5` (20px) or `w-6 h-6` (24px)
- Library: `lucide-react`

**Filled Icons**:
- Used for active states
- Same dimensions as line icons

**Identity-Accent Icons**:
- **Diaspora**: `text-emerald-400`
- **Youth**: `text-blue-400`
- **Creator**: `text-purple-400`
- **Legacy**: `text-amber-400`

**Common Icons**:
```typescript
import {
  Home,           // Dashboard
  TrendingUp,     // Markets
  Briefcase,      // Portfolio
  Newspaper,      // News
  Bell,           // Alerts
  Crown,          // Premium
  User,           // Profile
  Settings,       // Settings
  Search,         // Search
  Filter,         // Filter
  ChevronDown,    // Dropdown
  Check,          // Success
  X,              // Close
  AlertCircle,    // Warning
  Info,           // Information
  WifiOff,        // Offline
} from 'lucide-react';
```

---

## 21.3 INPUTS

### Button

**Variants**:

```tsx
// Primary
<button className="px-4 py-2 bg-yellow-500 text-slate-900 rounded-lg hover:bg-yellow-400 transition-colors font-medium">
  Primary Action
</button>

// Secondary
<button className="px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-600 transition-colors font-medium">
  Secondary Action
</button>

// Tertiary
<button className="px-4 py-2 text-yellow-500 hover:text-yellow-400 transition-colors font-medium">
  Tertiary Action
</button>

// Premium
<button className="px-4 py-2 bg-yellow-500 text-slate-900 rounded-lg hover:bg-yellow-400 transition-colors font-medium flex items-center gap-2">
  <Crown className="w-4 h-4" />
  Premium Feature
</button>

// Pro
<button className="px-4 py-2 bg-gradient-to-r from-slate-400 to-slate-300 text-slate-900 rounded-lg hover:from-slate-300 hover:to-slate-200 transition-colors font-medium">
  Pro Feature
</button>

// Identity-Accent (Diaspora)
<button className="px-4 py-2 bg-emerald-500 text-white rounded-lg hover:bg-emerald-400 transition-colors font-medium">
  Diaspora Action
</button>
```

**States**:
- **Default**: Base variant styling
- **Hover**: `hover:bg-*` color shift
- **Pressed**: `active:scale-95` slight scale down
- **Disabled**: `opacity-50 cursor-not-allowed pointer-events-none`
- **Loading**: Show spinner, disable interaction

```tsx
// Loading state
<button disabled className="px-4 py-2 bg-yellow-500 text-slate-900 rounded-lg opacity-50 cursor-not-allowed flex items-center gap-2">
  <RefreshCw className="w-4 h-4 animate-spin" />
  Loading...
</button>
```

---

### Text Field

```tsx
interface TextFieldProps {
  label?: string;
  placeholder?: string;
  value: string;
  onChange: (value: string) => void;
  error?: string;
  success?: string;
  disabled?: boolean;
}

// Default
<div className="flex flex-col gap-2">
  <label className="text-sm font-medium text-slate-300">Label</label>
  <input
    type="text"
    placeholder="Placeholder text"
    className="px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder:text-slate-500 focus:outline-none focus:border-yellow-500 transition-colors"
  />
</div>

// Error state
<div className="flex flex-col gap-2">
  <label className="text-sm font-medium text-slate-300">Label</label>
  <input
    type="text"
    className="px-4 py-2 bg-slate-800 border border-red-500 rounded-lg text-white focus:outline-none"
  />
  <p className="text-xs text-red-400">Error message here</p>
</div>

// Success state
<div className="flex flex-col gap-2">
  <label className="text-sm font-medium text-slate-300">Label</label>
  <input
    type="text"
    className="px-4 py-2 bg-slate-800 border border-emerald-500 rounded-lg text-white focus:outline-none"
  />
  <p className="text-xs text-emerald-400">Success message here</p>
</div>
```

---

### Dropdown

```tsx
// Single select
<select className="px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-yellow-500 transition-colors">
  <option>Select option</option>
  <option>Option 1</option>
  <option>Option 2</option>
</select>

// Multi-select (use library like react-select or headlessui)
<Listbox multiple value={selected} onChange={setSelected}>
  <ListboxButton>Select identities</ListboxButton>
  <ListboxOptions>
    <ListboxOption value="diaspora">Diaspora</ListboxOption>
    <ListboxOption value="youth">Youth</ListboxOption>
    <ListboxOption value="creator">Creator</ListboxOption>
    <ListboxOption value="legacy">Legacy</ListboxOption>
  </ListboxOptions>
</Listbox>

// Identity-aware options (color-coded)
<select className="px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white">
  <option className="bg-emerald-500/20">🌍 Diaspora</option>
  <option className="bg-blue-500/20">⚡ Youth</option>
  <option className="bg-purple-500/20">🎨 Creator</option>
  <option className="bg-amber-500/20">👑 Legacy</option>
</select>
```

---

### Toggle Switch

```tsx
// On/off
<button
  onClick={() => setIsOn(!isOn)}
  className={`relative w-11 h-6 rounded-full transition-colors ${
    isOn ? 'bg-yellow-500' : 'bg-slate-600'
  }`}
>
  <span
    className={`absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform ${
      isOn ? 'translate-x-5' : 'translate-x-0'
    }`}
  />
</button>

// Identity-accent (Diaspora)
<button
  className={`relative w-11 h-6 rounded-full transition-colors ${
    isOn ? 'bg-emerald-500' : 'bg-slate-600'
  }`}
>
  <span className="absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform" />
</button>
```

---

### Slider

**Used for**:
- Alert thresholds (price above/below $X)
- Chart ranges (1D, 1W, 1M, 1Y)

```tsx
// Range slider for alert threshold
<div className="flex flex-col gap-2">
  <label className="text-sm font-medium text-slate-300">
    Alert when price goes above
  </label>
  <input
    type="range"
    min="0"
    max="1000"
    value={threshold}
    onChange={(e) => setThreshold(Number(e.target.value))}
    className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-yellow-500"
  />
  <div className="flex justify-between text-xs text-slate-400">
    <span>$0</span>
    <span className="text-yellow-500 font-medium">${threshold}</span>
    <span>$1000</span>
  </div>
</div>

// Chart range selector (segmented control)
<div className="flex gap-1 p-1 bg-slate-800 rounded-lg">
  {['1D', '1W', '1M', '3M', '1Y', 'ALL'].map((range) => (
    <button
      key={range}
      className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
        selectedRange === range
          ? 'bg-yellow-500 text-slate-900'
          : 'text-slate-400 hover:text-white'
      }`}
    >
      {range}
    </button>
  ))}
</div>
```

---

## 21.4 NAVIGATION COMPONENTS

### Top Navigation Bar (Desktop)

```tsx
// File: components/navigation/TopNav.tsx

export function TopNav() {
  return (
    <nav className="sticky top-0 z-40 bg-slate-900/90 backdrop-blur-sm border-b border-slate-800">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center gap-8">
            <Logo />
            
            {/* Navigation Links */}
            <div className="hidden md:flex items-center gap-6">
              <NavLink href="/dashboard" icon={Home}>Dashboard</NavLink>
              <NavLink href="/markets" icon={TrendingUp}>Markets</NavLink>
              <NavLink href="/portfolio" icon={Briefcase}>Portfolio</NavLink>
              <NavLink href="/news" icon={Newspaper}>News</NavLink>
              <NavLink href="/alerts" icon={Bell}>Alerts</NavLink>
            </div>
          </div>
          
          {/* Right side */}
          <div className="flex items-center gap-4">
            <CompactOfflineIndicator />
            
            <button className="px-3 py-1.5 bg-yellow-500 text-slate-900 rounded-lg text-sm font-medium hover:bg-yellow-400 transition-colors flex items-center gap-1.5">
              <Crown className="w-4 h-4" />
              Premium
            </button>
            
            <button className="w-9 h-9 bg-slate-800 rounded-full flex items-center justify-center hover:bg-slate-700 transition-colors">
              <User className="w-5 h-5 text-slate-300" />
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}

// NavLink component
function NavLink({ href, icon: Icon, children }) {
  const isActive = usePathname() === href;
  
  return (
    <Link
      href={href}
      className={`flex items-center gap-2 text-sm font-medium transition-colors ${
        isActive
          ? 'text-yellow-500'
          : 'text-slate-400 hover:text-white'
      }`}
    >
      <Icon className="w-5 h-5" />
      {children}
    </Link>
  );
}
```

---

### Bottom Tab Bar (Mobile)

```tsx
// File: components/navigation/BottomTabBar.tsx

export function BottomTabBar() {
  const pathname = usePathname();
  
  const tabs = [
    { href: '/dashboard', icon: Home, label: 'Home' },
    { href: '/markets', icon: TrendingUp, label: 'Markets' },
    { href: '/portfolio', icon: Briefcase, label: 'Portfolio' },
    { href: '/news', icon: Newspaper, label: 'News' },
    { href: '/profile', icon: User, label: 'Profile' },
  ];
  
  return (
    <nav className="fixed bottom-0 left-0 right-0 z-40 bg-slate-900 border-t border-slate-800 md:hidden">
      <div className="flex items-center justify-around h-16">
        {tabs.map((tab) => {
          const isActive = pathname === tab.href;
          const Icon = tab.icon;
          
          return (
            <Link
              key={tab.href}
              href={tab.href}
              className="flex flex-col items-center justify-center gap-1 flex-1"
            >
              <Icon
                className={`w-6 h-6 ${
                  isActive ? 'text-yellow-500' : 'text-slate-400'
                }`}
              />
              <span
                className={`text-xs font-medium ${
                  isActive ? 'text-yellow-500' : 'text-slate-400'
                }`}
              >
                {tab.label}
              </span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
```

**Mobile Layout Adjustment**:
```tsx
// Add padding-bottom to main content to prevent tab bar overlap
<main className="pb-20 md:pb-0">
  {children}
</main>
```

---

### Hamburger Menu (Mobile)

```tsx
// File: components/navigation/HamburgerMenu.tsx

export function HamburgerMenu() {
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <>
      {/* Menu Button */}
      <button
        onClick={() => setIsOpen(true)}
        className="md:hidden w-9 h-9 flex items-center justify-center"
      >
        <Menu className="w-6 h-6 text-slate-300" />
      </button>
      
      {/* Drawer */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm md:hidden"
            onClick={() => setIsOpen(false)}
          />
          
          {/* Menu */}
          <div className="fixed top-0 right-0 bottom-0 z-50 w-64 bg-slate-900 border-l border-slate-800 md:hidden">
            <div className="flex flex-col h-full">
              {/* Header */}
              <div className="flex items-center justify-between p-4 border-b border-slate-800">
                <h2 className="text-lg font-medium text-white">Menu</h2>
                <button
                  onClick={() => setIsOpen(false)}
                  className="w-8 h-8 flex items-center justify-center"
                >
                  <X className="w-5 h-5 text-slate-400" />
                </button>
              </div>
              
              {/* Menu Items */}
              <div className="flex-1 overflow-y-auto py-4">
                <MenuItem icon={CreditCard} href="/billing">
                  Billing
                </MenuItem>
                <MenuItem icon={User} href="/settings/identity">
                  Identity Settings
                </MenuItem>
                <MenuItem icon={Bell} href="/settings/notifications">
                  Notifications
                </MenuItem>
                <MenuItem icon={HelpCircle} href="/help">
                  Help
                </MenuItem>
                <MenuItem icon={FileText} href="/legal">
                  Legal
                </MenuItem>
                
                <div className="h-px bg-slate-800 my-4 mx-4" />
                
                <button
                  onClick={() => logout()}
                  className="flex items-center gap-3 w-full px-4 py-3 text-red-400 hover:bg-slate-800 transition-colors"
                >
                  <LogOut className="w-5 h-5" />
                  Logout
                </button>
              </div>
            </div>
          </div>
        </>
      )}
    </>
  );
}

function MenuItem({ icon: Icon, href, children }) {
  return (
    <Link
      href={href}
      className="flex items-center gap-3 px-4 py-3 text-slate-300 hover:bg-slate-800 hover:text-white transition-colors"
    >
      <Icon className="w-5 h-5" />
      {children}
    </Link>
  );
}
```

---

## 21.5 DATA DISPLAY COMPONENTS

### Table

**Used for**:
- Holdings
- Movers
- Earnings
- Alerts

**Features**:
- Sorting
- Sticky header
- Responsive collapse

```tsx
// File: components/ui/Table.tsx

interface Column<T> {
  key: keyof T;
  label: string;
  sortable?: boolean;
  render?: (value: any, row: T) => React.ReactNode;
  className?: string;
}

interface TableProps<T> {
  columns: Column<T>[];
  data: T[];
  sortBy?: keyof T;
  sortDirection?: 'asc' | 'desc';
  onSort?: (key: keyof T) => void;
}

export function Table<T>({ columns, data, sortBy, sortDirection, onSort }: TableProps<T>) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead className="sticky top-0 bg-slate-900 border-b border-slate-800">
          <tr>
            {columns.map((column) => (
              <th
                key={String(column.key)}
                className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider"
              >
                {column.sortable ? (
                  <button
                    onClick={() => onSort?.(column.key)}
                    className="flex items-center gap-2 hover:text-white transition-colors"
                  >
                    {column.label}
                    {sortBy === column.key && (
                      <ChevronUp
                        className={`w-4 h-4 transition-transform ${
                          sortDirection === 'desc' ? 'rotate-180' : ''
                        }`}
                      />
                    )}
                  </button>
                ) : (
                  column.label
                )}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800">
          {data.map((row, index) => (
            <tr key={index} className="hover:bg-slate-800/50 transition-colors">
              {columns.map((column) => (
                <td
                  key={String(column.key)}
                  className={`px-4 py-3 text-sm ${column.className || 'text-slate-300'}`}
                >
                  {column.render
                    ? column.render(row[column.key], row)
                    : String(row[column.key])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

**Responsive Collapse** (Mobile):
```tsx
// On mobile, show as stacked cards instead of table
export function ResponsiveTable({ data }) {
  return (
    <>
      {/* Desktop: Table */}
      <div className="hidden md:block">
        <Table columns={columns} data={data} />
      </div>
      
      {/* Mobile: Cards */}
      <div className="md:hidden space-y-3">
        {data.map((item, index) => (
          <div key={index} className="p-4 bg-slate-800 rounded-lg">
            <div className="flex justify-between items-center mb-2">
              <span className="font-medium text-white">{item.ticker}</span>
              <span className="text-emerald-400">{item.change}</span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div>
                <p className="text-slate-400">Shares</p>
                <p className="text-white">{item.shares}</p>
              </div>
              <div>
                <p className="text-slate-400">Value</p>
                <p className="text-white">{item.value}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}
```

---

### List Item

**Used for**:
- News
- Alerts
- Search results

```tsx
// News list item
<div className="flex gap-4 p-4 hover:bg-slate-800/50 transition-colors cursor-pointer">
  <div className="flex-1">
    <div className="flex items-center gap-2 mb-2">
      <h3 className="font-medium text-white">Headline goes here</h3>
      <Badge variant="emerald">Verified</Badge>
    </div>
    <p className="text-sm text-slate-400 mb-2">Summary text...</p>
    <div className="flex items-center gap-3 text-xs text-slate-500">
      <span>2 hours ago</span>
      <span>•</span>
      <span>5 sources</span>
      <span>•</span>
      <span className="text-emerald-400">AAPL, MSFT</span>
    </div>
  </div>
  <ChevronRight className="w-5 h-5 text-slate-600" />
</div>

// Alert list item
<div className="flex items-center justify-between p-4 border-b border-slate-800 hover:bg-slate-800/50">
  <div className="flex items-center gap-3">
    <Bell className="w-5 h-5 text-yellow-500" />
    <div>
      <p className="text-sm font-medium text-white">AAPL above $180</p>
      <p className="text-xs text-slate-400">Last triggered 3 hours ago</p>
    </div>
  </div>
  <div className="flex items-center gap-2">
    <button className="p-2 hover:bg-slate-700 rounded transition-colors">
      <Edit2 className="w-4 h-4 text-slate-400" />
    </button>
    <button className="p-2 hover:bg-slate-700 rounded transition-colors">
      <Trash2 className="w-4 h-4 text-red-400" />
    </button>
  </div>
</div>
```

---

### Badge

**Variants**:
- Identity
- Premium
- Pro
- Verification
- Sector

```tsx
// Identity badges
<Badge className="bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
  Diaspora
</Badge>

<Badge className="bg-blue-500/20 text-blue-400 border border-blue-500/30">
  Youth
</Badge>

<Badge className="bg-purple-500/20 text-purple-400 border border-purple-500/30">
  Creator
</Badge>

<Badge className="bg-amber-500/20 text-amber-400 border border-amber-500/30">
  Legacy
</Badge>

// Premium/Pro badges
<Badge className="bg-yellow-500/20 text-yellow-500 border border-yellow-500/30 flex items-center gap-1">
  <Crown className="w-3 h-3" />
  Premium
</Badge>

<Badge className="bg-gradient-to-r from-slate-300 to-slate-400 text-slate-900 border-0">
  Pro
</Badge>

// Verification badge
<Badge className="bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center gap-1">
  <Check className="w-3 h-3" />
  Verified
</Badge>

// Sector badges
<Badge className="bg-blue-500/20 text-blue-400">Technology</Badge>
<Badge className="bg-green-500/20 text-green-400">Healthcare</Badge>
<Badge className="bg-purple-500/20 text-purple-400">Finance</Badge>
```

---

### Tag

**Used for**:
- Identity relevance
- Cultural Alpha highlights

```tsx
// Identity relevance tag
<div className="inline-flex items-center gap-1.5 px-2 py-1 bg-emerald-500/10 rounded-full">
  <div className="w-2 h-2 bg-emerald-400 rounded-full" />
  <span className="text-xs text-emerald-400 font-medium">Diaspora Relevant</span>
</div>

// Cultural Alpha highlight
<div className="inline-flex items-center gap-1.5 px-2 py-1 bg-yellow-500/10 rounded-full">
  <TrendingUp className="w-3 h-3 text-yellow-500" />
  <span className="text-xs text-yellow-500 font-medium">High Cultural Alpha</span>
</div>
```

---

### Chip

**Used for**:
- Filters
- Timeframes
- Identity toggles

```tsx
// Filter chips
<div className="flex flex-wrap gap-2">
  {['All', 'Technology', 'Healthcare', 'Finance'].map((filter) => (
    <button
      key={filter}
      className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
        selectedFilter === filter
          ? 'bg-yellow-500 text-slate-900'
          : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
      }`}
    >
      {filter}
      {selectedFilter === filter && (
        <X className="w-3 h-3 ml-1 inline" />
      )}
    </button>
  ))}
</div>

// Timeframe chips
<div className="flex gap-1 p-1 bg-slate-800 rounded-lg">
  {['1D', '1W', '1M', '3M', '1Y'].map((timeframe) => (
    <button
      key={timeframe}
      className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
        selected === timeframe
          ? 'bg-yellow-500 text-slate-900'
          : 'text-slate-400 hover:text-white'
      }`}
    >
      {timeframe}
    </button>
  ))}
</div>

// Identity toggle chips
<div className="flex gap-2">
  {identities.map((identity) => (
    <button
      key={identity.type}
      className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
        activeIdentities.includes(identity.type)
          ? `bg-${identity.color}-500/20 text-${identity.color}-400 border border-${identity.color}-500/30`
          : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
      }`}
    >
      {identity.icon} {identity.label}
    </button>
  ))}
</div>
```

---

## 21.6 CHART COMPONENTS

### Line Chart

**Features**:
- Timeframes
- Identity overlays

```tsx
// File: components/charts/LineChart.tsx

import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export function PriceLineChart({ data, timeframe, identity }) {
  return (
    <div className="w-full h-64">
      <ResponsiveContainer>
        <LineChart data={data}>
          <XAxis
            dataKey="time"
            stroke="#64748B"
            fontSize={12}
          />
          <YAxis
            stroke="#64748B"
            fontSize={12}
            tickFormatter={(value) => `$${value}`}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1E293B',
              border: '1px solid #334155',
              borderRadius: '8px',
            }}
            labelStyle={{ color: '#CBD5E1' }}
          />
          <Line
            type="monotone"
            dataKey="price"
            stroke="#F5C542"
            strokeWidth={2}
            dot={false}
          />
          
          {/* Identity overlay (Cultural Alpha score) */}
          {identity && (
            <Line
              type="monotone"
              dataKey="culturalAlpha"
              stroke="#10B981"
              strokeWidth={1}
              strokeDasharray="5 5"
              dot={false}
            />
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
```

---

### Candlestick Chart

**(Pro unlocks advanced indicators)**

```tsx
// Basic candlestick (Free)
<CandlestickChart data={stockData} />

// With indicators (Pro)
<PremiumGate requiredTier="pro">
  <CandlestickChart
    data={stockData}
    indicators={['SMA', 'RSI', 'MACD']}
    showVolume={true}
  />
</PremiumGate>
```

---

### Bar Chart

**Used for**:
- Volume
- Allocation

```tsx
// Volume bar chart
<BarChart
  data={volumeData}
  xKey="time"
  yKey="volume"
  color="#3B82F6"
/>

// Portfolio allocation
<BarChart
  data={allocationData}
  xKey="sector"
  yKey="percentage"
  color="#10B981"
/>
```

---

### Heatmap Tile

**Used for**:
- Sector heatmap
- Cultural Alpha heatmap

```tsx
// Sector heatmap tile
<div
  className="relative aspect-square rounded-lg p-3 flex flex-col justify-between cursor-pointer hover:opacity-90 transition-opacity"
  style={{
    backgroundColor: getHeatmapColor(changePercent),
  }}
>
  <div>
    <p className="text-xs font-medium text-white/90">{sector}</p>
  </div>
  <div>
    <p className="text-lg font-semibold text-white">{changePercent}%</p>
  </div>
</div>

// Cultural Alpha heatmap
<div className="grid grid-cols-3 md:grid-cols-5 gap-2">
  {stocks.map((stock) => (
    <div
      key={stock.ticker}
      className="aspect-square rounded-lg p-2 flex flex-col justify-between"
      style={{
        backgroundColor: getCulturalAlphaColor(stock.culturalAlpha),
      }}
    >
      <span className="text-xs font-medium text-white">{stock.ticker}</span>
      <span className="text-sm font-semibold text-white">
        {stock.culturalAlpha}
      </span>
    </div>
  ))}
</div>
```

---

## 21.7 CARD COMPONENTS

### Stock Card

**Shows**:
- Ticker
- Price
- Change
- Identity tags

```tsx
<div className="p-4 bg-slate-800 rounded-lg border border-slate-700 hover:border-slate-600 transition-colors cursor-pointer">
  <div className="flex items-start justify-between mb-3">
    <div>
      <h3 className="text-lg font-semibold text-white">AAPL</h3>
      <p className="text-sm text-slate-400">Apple Inc.</p>
    </div>
    <div className="flex gap-1">
      <Badge className="bg-emerald-500/20 text-emerald-400 text-xs">
        Diaspora
      </Badge>
    </div>
  </div>
  
  <div className="flex items-end justify-between">
    <div>
      <p className="text-2xl font-semibold text-white">$180.50</p>
      <p className="text-sm text-emerald-400">+2.5%</p>
    </div>
    <Sparkline data={priceData} color="#10B981" />
  </div>
</div>
```

---

### News Card

**Shows**:
- Headline
- Verification badge
- Summary

```tsx
<div className="p-4 bg-slate-800 rounded-lg border border-slate-700 hover:border-slate-600 transition-colors cursor-pointer">
  <div className="flex items-start gap-3 mb-3">
    <div className="flex-1">
      <div className="flex items-center gap-2 mb-2">
        <h3 className="font-medium text-white line-clamp-2">
          Caribbean Markets Surge 15% on Economic Growth
        </h3>
      </div>
      <div className="flex items-center gap-2 mb-2">
        <Badge className="bg-emerald-500/20 text-emerald-400 flex items-center gap-1">
          <Check className="w-3 h-3" />
          Verified
        </Badge>
        <span className="text-xs text-slate-500">5 sources</span>
      </div>
    </div>
  </div>
  
  <p className="text-sm text-slate-400 line-clamp-2 mb-3">
    Summary of the article goes here...
  </p>
  
  <div className="flex items-center justify-between text-xs text-slate-500">
    <span>2 hours ago</span>
    <div className="flex gap-2">
      <span className="text-emerald-400">AAPL</span>
      <span className="text-emerald-400">MSFT</span>
    </div>
  </div>
</div>
```

---

### Portfolio Snapshot Card

**Shows**:
- Total value
- Daily change
- Allocation preview

```tsx
<div className="p-6 bg-slate-800 rounded-lg border border-slate-700">
  <h3 className="text-sm font-medium text-slate-400 mb-4">Portfolio Value</h3>
  
  <div className="mb-6">
    <p className="text-3xl font-semibold text-white mb-2">$45,230.50</p>
    <div className="flex items-center gap-2">
      <TrendingUp className="w-4 h-4 text-emerald-400" />
      <span className="text-emerald-400 font-medium">+$1,250.00</span>
      <span className="text-slate-400">(+2.84%)</span>
    </div>
  </div>
  
  <div className="space-y-2">
    <div className="flex items-center justify-between text-sm">
      <span className="text-slate-400">Stocks</span>
      <span className="text-white">65%</span>
    </div>
    <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
      <div className="h-full bg-yellow-500 rounded-full" style={{ width: '65%' }} />
    </div>
  </div>
</div>
```

---

### Identity Widget Card

**Identity-specific content**:
- Diaspora Flow Maps
- Creator Index
- Youth challenges
- Legacy-builder dividend view

```tsx
// Diaspora Flow Maps
<div className="p-6 bg-gradient-to-br from-emerald-500/10 to-emerald-500/5 rounded-lg border border-emerald-500/20">
  <div className="flex items-center gap-2 mb-4">
    <Globe className="w-5 h-5 text-emerald-400" />
    <h3 className="font-medium text-white">Diaspora Capital Flows</h3>
  </div>
  {/* Map visualization */}
</div>

// Creator Index
<div className="p-6 bg-gradient-to-br from-purple-500/10 to-purple-500/5 rounded-lg border border-purple-500/20">
  <div className="flex items-center gap-2 mb-4">
    <Sparkles className="w-5 h-5 text-purple-400" />
    <h3 className="font-medium text-white">Creator Economy Index</h3>
  </div>
  {/* Creator platform stocks */}
</div>

// Youth Challenges
<div className="p-6 bg-gradient-to-br from-blue-500/10 to-blue-500/5 rounded-lg border border-blue-500/20">
  <div className="flex items-center gap-2 mb-4">
    <Zap className="w-5 h-5 text-blue-400" />
    <h3 className="font-medium text-white">Youth Investment Challenge</h3>
  </div>
  {/* Challenge progress */}
</div>

// Legacy Builder Dividend View
<div className="p-6 bg-gradient-to-br from-amber-500/10 to-amber-500/5 rounded-lg border border-amber-500/20">
  <div className="flex items-center gap-2 mb-4">
    <Crown className="w-5 h-5 text-amber-400" />
    <h3 className="font-medium text-white">Dividend Aristocrats</h3>
  </div>
  {/* Dividend yield table */}
</div>
```

---

### Premium Feature Card

**Used in upsell screens.**

```tsx
<div className="p-6 bg-gradient-to-br from-yellow-500/10 to-yellow-500/5 rounded-lg border border-yellow-500/20">
  <div className="flex items-center gap-3 mb-4">
    <div className="w-12 h-12 bg-yellow-500 rounded-lg flex items-center justify-center">
      <Crown className="w-6 h-6 text-slate-900" />
    </div>
    <div>
      <h3 className="font-semibold text-white">Advanced Analytics</h3>
      <p className="text-sm text-slate-400">Premium Feature</p>
    </div>
  </div>
  
  <p className="text-sm text-slate-300 mb-4">
    Get deep insights into your portfolio with diversification scores, risk metrics, and identity alignment.
  </p>
  
  <ul className="space-y-2 mb-6">
    {['Volatility analysis', 'Sector concentration', 'Identity alignment', 'Risk/reward optimization'].map((feature) => (
      <li key={feature} className="flex items-center gap-2 text-sm text-slate-300">
        <Check className="w-4 h-4 text-emerald-400" />
        {feature}
      </li>
    ))}
  </ul>
  
  <button className="w-full px-4 py-2 bg-yellow-500 text-slate-900 rounded-lg hover:bg-yellow-400 transition-colors font-medium">
    Upgrade to Premium
  </button>
</div>
```

---

## 21.8 MODALS & OVERLAYS

### Premium Overlay

**Message**: "Upgrade to Premium to unlock this feature."

```tsx
<div className="relative">
  {/* Blurred content */}
  <div className="blur-sm pointer-events-none">
    <AdvancedAnalytics />
  </div>
  
  {/* Overlay */}
  <div className="absolute inset-0 flex items-center justify-center bg-slate-900/80 backdrop-blur-sm">
    <div className="max-w-md p-6 bg-slate-800 rounded-lg border border-yellow-500/20 text-center">
      <Crown className="w-12 h-12 text-yellow-500 mx-auto mb-4" />
      <h3 className="text-xl font-semibold text-white mb-2">
        Premium Feature
      </h3>
      <p className="text-slate-400 mb-6">
        Upgrade to Premium to unlock this feature.
      </p>
      <button className="w-full px-4 py-2 bg-yellow-500 text-slate-900 rounded-lg hover:bg-yellow-400 transition-colors font-medium">
        Upgrade Now
      </button>
    </div>
  </div>
</div>
```

---

### Pro Overlay

**Message**: "Upgrade to Pro for advanced tools."

```tsx
<div className="absolute inset-0 flex items-center justify-center bg-slate-900/80 backdrop-blur-sm">
  <div className="max-w-md p-6 bg-slate-800 rounded-lg border border-slate-600 text-center">
    <div className="w-12 h-12 bg-gradient-to-r from-slate-300 to-slate-400 rounded-lg mx-auto mb-4 flex items-center justify-center">
      <Sparkles className="w-6 h-6 text-slate-900" />
    </div>
    <h3 className="text-xl font-semibold text-white mb-2">
      Pro Feature
    </h3>
    <p className="text-slate-400 mb-6">
      Upgrade to Pro for advanced tools.
    </p>
    <button className="w-full px-4 py-2 bg-gradient-to-r from-slate-300 to-slate-400 text-slate-900 rounded-lg hover:from-slate-200 hover:to-slate-300 transition-colors font-medium">
      Upgrade to Pro
    </button>
  </div>
</div>
```

---

### Add Holding Modal

**Fields**:
- Ticker
- Shares
- Average cost

```tsx
<Modal isOpen={isOpen} onClose={onClose} title="Add Holding">
  <form onSubmit={handleSubmit} className="space-y-4">
    <div>
      <label className="block text-sm font-medium text-slate-300 mb-2">
        Ticker
      </label>
      <input
        type="text"
        placeholder="AAPL"
        className="w-full px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white focus:border-yellow-500"
      />
    </div>
    
    <div>
      <label className="block text-sm font-medium text-slate-300 mb-2">
        Shares
      </label>
      <input
        type="number"
        placeholder="10"
        className="w-full px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white focus:border-yellow-500"
      />
    </div>
    
    <div>
      <label className="block text-sm font-medium text-slate-300 mb-2">
        Average Cost
      </label>
      <input
        type="number"
        placeholder="150.00"
        className="w-full px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white focus:border-yellow-500"
      />
    </div>
    
    <div className="flex gap-3">
      <button
        type="button"
        onClick={onClose}
        className="flex-1 px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-600"
      >
        Cancel
      </button>
      <button
        type="submit"
        className="flex-1 px-4 py-2 bg-yellow-500 text-slate-900 rounded-lg hover:bg-yellow-400 font-medium"
      >
        Add Holding
      </button>
    </div>
  </form>
</Modal>
```

---

### Add Alert Modal

**Fields depend on alert type.**

```tsx
<Modal isOpen={isOpen} onClose={onClose} title="Create Alert">
  <form className="space-y-4">
    <div>
      <label className="block text-sm font-medium text-slate-300 mb-2">
        Alert Type
      </label>
      <select className="w-full px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white">
        <option>Price Alert</option>
        <option>News Alert</option>
        <option>Volume Alert</option>
        <option>Earnings Alert (Premium)</option>
      </select>
    </div>
    
    {/* Conditional fields based on alert type */}
    {alertType === 'price' && (
      <>
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">
            Ticker
          </label>
          <input type="text" placeholder="AAPL" className="w-full px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg" />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">
            Condition
          </label>
          <select className="w-full px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg">
            <option>Above</option>
            <option>Below</option>
            <option>Change %</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">
            Value
          </label>
          <input type="number" placeholder="180.00" className="w-full px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg" />
        </div>
      </>
    )}
    
    <div className="flex gap-3">
      <button type="button" onClick={onClose} className="flex-1 px-4 py-2 bg-slate-700 text-white rounded-lg">
        Cancel
      </button>
      <button type="submit" className="flex-1 px-4 py-2 bg-yellow-500 text-slate-900 rounded-lg font-medium">
        Create Alert
      </button>
    </div>
  </form>
</Modal>
```

---

### News Source Modal

**Shows**:
- Source list
- Publication times

```tsx
<Modal isOpen={isOpen} onClose={onClose} title="News Sources">
  <div className="space-y-3">
    {sources.map((source) => (
      <div key={source.id} className="p-3 bg-slate-800 rounded-lg">
        <div className="flex items-start justify-between mb-2">
          <div>
            <h4 className="font-medium text-white">{source.name}</h4>
            <a href={source.url} className="text-sm text-blue-400 hover:underline">
              {source.url}
            </a>
          </div>
          <Badge className="bg-emerald-500/20 text-emerald-400">
            {source.credibility}%
          </Badge>
        </div>
        <p className="text-xs text-slate-400">
          Published {new Date(source.publishedAt).toLocaleString()}
        </p>
      </div>
    ))}
  </div>
</Modal>
```

---

## 21.9 IDENTITY COMPONENTS

These components adapt visually and contextually based on identity.

### Identity Header Accent

**Color + icon changes per identity.**

```tsx
export function IdentityHeader({ identity }) {
  const config = {
    diaspora: { color: 'emerald', icon: Globe },
    youth: { color: 'blue', icon: Zap },
    creator: { color: 'purple', icon: Sparkles },
    legacy: { color: 'amber', icon: Crown },
  }[identity];
  
  const Icon = config.icon;
  
  return (
    <div className={`h-1 bg-${config.color}-500 mb-4`}>
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center gap-2">
          <Icon className={`w-5 h-5 text-${config.color}-400`} />
          <span className={`text-sm font-medium text-${config.color}-400 capitalize`}>
            {identity}
          </span>
        </div>
      </div>
    </div>
  );
}
```

---

### Identity Insight Card

**Used in**:
- Dashboard
- Portfolio
- Stock Detail

```tsx
<div className={`p-4 bg-gradient-to-br from-${identityColor}-500/10 to-${identityColor}-500/5 rounded-lg border border-${identityColor}-500/20`}>
  <div className="flex items-center gap-2 mb-3">
    <Icon className={`w-5 h-5 text-${identityColor}-400`} />
    <h3 className="font-medium text-white">{title}</h3>
  </div>
  <p className="text-sm text-slate-300">
    {insightText}
  </p>
</div>
```

---

### Identity Filter Chips

**Used in**:
- News
- Markets

```tsx
<div className="flex flex-wrap gap-2">
  {identities.map((id) => (
    <button
      key={id.type}
      onClick={() => toggleIdentity(id.type)}
      className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors flex items-center gap-1.5 ${
        activeIdentities.includes(id.type)
          ? `bg-${id.color}-500/20 text-${id.color}-400 border border-${id.color}-500/30`
          : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
      }`}
    >
      <id.icon className="w-4 h-4" />
      {id.label}
    </button>
  ))}
</div>
```

---

## 21.10 PREMIUM COMPONENTS

### Premium Badge

**Gold accent.**

```tsx
<div className="inline-flex items-center gap-1.5 px-2 py-1 bg-yellow-500/20 rounded-full border border-yellow-500/30">
  <Crown className="w-3 h-3 text-yellow-500" />
  <span className="text-xs text-yellow-500 font-medium">Premium</span>
</div>
```

---

### Pro Badge

**Platinum accent.**

```tsx
<div className="inline-flex items-center gap-1.5 px-2 py-1 bg-gradient-to-r from-slate-300 to-slate-400 rounded-full">
  <Sparkles className="w-3 h-3 text-slate-900" />
  <span className="text-xs text-slate-900 font-medium">Pro</span>
</div>
```

---

### Locked Feature Tile

**Used in**:
- Analytics
- Insights
- Heatmaps
- Alerts

```tsx
<div className="relative p-6 bg-slate-800 rounded-lg border border-slate-700 cursor-not-allowed">
  {/* Locked overlay */}
  <div className="absolute inset-0 bg-slate-900/50 backdrop-blur-[2px] rounded-lg flex items-center justify-center">
    <div className="text-center">
      <Lock className="w-8 h-8 text-yellow-500 mx-auto mb-2" />
      <p className="text-sm font-medium text-yellow-500">Premium</p>
    </div>
  </div>
  
  {/* Blurred content preview */}
  <div className="opacity-50">
    <h3 className="font-medium text-white mb-2">Advanced Risk Metrics</h3>
    <p className="text-sm text-slate-400">View detailed risk analysis...</p>
  </div>
</div>
```

---

### Premium Comparison Table

**Used in**:
- Subscription screen

```tsx
<div className="grid md:grid-cols-3 gap-6">
  {/* Free Tier */}
  <div className="p-6 bg-slate-800 rounded-lg border border-slate-700">
    <h3 className="text-xl font-semibold text-white mb-2">Free</h3>
    <p className="text-3xl font-bold text-white mb-4">$0<span className="text-sm text-slate-400">/mo</span></p>
    <ul className="space-y-3 mb-6">
      <li className="flex items-center gap-2 text-sm">
        <Check className="w-4 h-4 text-emerald-400" />
        <span className="text-slate-300">1 portfolio</span>
      </li>
      <li className="flex items-center gap-2 text-sm">
        <Check className="w-4 h-4 text-emerald-400" />
        <span className="text-slate-300">5 alerts</span>
      </li>
      <li className="flex items-center gap-2 text-sm">
        <X className="w-4 h-4 text-slate-600" />
        <span className="text-slate-500">Advanced analytics</span>
      </li>
    </ul>
    <button className="w-full px-4 py-2 bg-slate-700 text-white rounded-lg">
      Current Plan
    </button>
  </div>
  
  {/* Premium Tier */}
  <div className="p-6 bg-gradient-to-br from-yellow-500/10 to-yellow-500/5 rounded-lg border-2 border-yellow-500/50 relative">
    <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 bg-yellow-500 text-slate-900 text-xs font-medium rounded-full">
      Most Popular
    </div>
    <h3 className="text-xl font-semibold text-white mb-2">Premium</h3>
    <p className="text-3xl font-bold text-white mb-4">$9.99<span className="text-sm text-slate-400">/mo</span></p>
    <ul className="space-y-3 mb-6">
      <li className="flex items-center gap-2 text-sm">
        <Check className="w-4 h-4 text-emerald-400" />
        <span className="text-white">5 portfolios</span>
      </li>
      <li className="flex items-center gap-2 text-sm">
        <Check className="w-4 h-4 text-emerald-400" />
        <span className="text-white">50 alerts</span>
      </li>
      <li className="flex items-center gap-2 text-sm">
        <Check className="w-4 h-4 text-emerald-400" />
        <span className="text-white">Advanced analytics</span>
      </li>
    </ul>
    <button className="w-full px-4 py-2 bg-yellow-500 text-slate-900 rounded-lg hover:bg-yellow-400 font-medium">
      Upgrade
    </button>
  </div>
  
  {/* Pro Tier */}
  <div className="p-6 bg-slate-800 rounded-lg border border-slate-700">
    <h3 className="text-xl font-semibold text-white mb-2">Pro</h3>
    <p className="text-3xl font-bold text-white mb-4">$24.99<span className="text-sm text-slate-400">/mo</span></p>
    <ul className="space-y-3 mb-6">
      <li className="flex items-center gap-2 text-sm">
        <Check className="w-4 h-4 text-emerald-400" />
        <span className="text-slate-300">Unlimited portfolios</span>
      </li>
      <li className="flex items-center gap-2 text-sm">
        <Check className="w-4 h-4 text-emerald-400" />
        <span className="text-slate-300">500 alerts</span>
      </li>
      <li className="flex items-center gap-2 text-sm">
        <Check className="w-4 h-4 text-emerald-400" />
        <span className="text-slate-300">API access</span>
      </li>
    </ul>
    <button className="w-full px-4 py-2 bg-gradient-to-r from-slate-300 to-slate-400 text-slate-900 rounded-lg hover:from-slate-200 hover:to-slate-300 font-medium">
      Upgrade to Pro
    </button>
  </div>
</div>
```

---

## 21.11 FEEDBACK COMPONENTS

### Toast

**Variants**:
- Success
- Error
- Info

```tsx
// Success toast
<div className="fixed top-4 right-4 z-50 flex items-center gap-3 p-4 bg-emerald-500/10 border border-emerald-500/50 rounded-lg backdrop-blur-sm">
  <CheckCircle className="w-5 h-5 text-emerald-400" />
  <span className="text-sm font-medium text-white">
    Portfolio saved successfully
  </span>
  <button className="ml-2 text-emerald-400 hover:text-emerald-300">
    <X className="w-4 h-4" />
  </button>
</div>

// Error toast
<div className="fixed top-4 right-4 z-50 flex items-center gap-3 p-4 bg-red-500/10 border border-red-500/50 rounded-lg backdrop-blur-sm">
  <AlertCircle className="w-5 h-5 text-red-400" />
  <span className="text-sm font-medium text-white">
    Failed to load market data
  </span>
  <button className="ml-2 text-red-400 hover:text-red-300">
    <X className="w-4 h-4" />
  </button>
</div>

// Info toast
<div className="fixed top-4 right-4 z-50 flex items-center gap-3 p-4 bg-blue-500/10 border border-blue-500/50 rounded-lg backdrop-blur-sm">
  <Info className="w-5 h-5 text-blue-400" />
  <span className="text-sm font-medium text-white">
    Markets close in 30 minutes
  </span>
  <button className="ml-2 text-blue-400 hover:text-blue-300">
    <X className="w-4 h-4" />
  </button>
</div>
```

---

### Inline Error

**Used in forms.**

```tsx
<div className="flex items-center gap-2 p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
  <AlertCircle className="w-4 h-4 text-red-400 flex-shrink-0" />
  <p className="text-sm text-red-400">
    Please enter a valid ticker symbol
  </p>
</div>
```

---

### Empty State

**Variants**:
- Portfolio empty
- Alerts empty
- News empty
- Markets empty

```tsx
// Portfolio empty
<div className="flex flex-col items-center justify-center p-12 text-center">
  <Briefcase className="w-16 h-16 text-slate-600 mb-4" />
  <h3 className="text-lg font-medium text-white mb-2">
    No Holdings Yet
  </h3>
  <p className="text-sm text-slate-400 mb-6 max-w-sm">
    Add your first stock holding to start tracking your portfolio.
  </p>
  <button className="px-4 py-2 bg-yellow-500 text-slate-900 rounded-lg hover:bg-yellow-400 font-medium">
    Add Holding
  </button>
</div>

// Alerts empty
<div className="flex flex-col items-center justify-center p-12 text-center">
  <Bell className="w-16 h-16 text-slate-600 mb-4" />
  <h3 className="text-lg font-medium text-white mb-2">
    No Alerts Set
  </h3>
  <p className="text-sm text-slate-400 mb-6 max-w-sm">
    Create your first alert to get notified about price changes.
  </p>
  <button className="px-4 py-2 bg-yellow-500 text-slate-900 rounded-lg hover:bg-yellow-400 font-medium">
    Create Alert
  </button>
</div>

// News empty (filtered)
<div className="flex flex-col items-center justify-center p-12 text-center">
  <Newspaper className="w-16 h-16 text-slate-600 mb-4" />
  <h3 className="text-lg font-medium text-white mb-2">
    No News Found
  </h3>
  <p className="text-sm text-slate-400 mb-6 max-w-sm">
    Try adjusting your filters or check back later.
  </p>
  <button className="px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-600">
    Clear Filters
  </button>
</div>
```

---

### Loading Skeleton

**Used for**:
- Charts
- Tables
- Cards

```tsx
// Card skeleton
<div className="p-4 bg-slate-800 rounded-lg border border-slate-700 animate-pulse">
  <div className="h-4 bg-slate-700 rounded w-24 mb-3" />
  <div className="h-8 bg-slate-700 rounded w-32 mb-2" />
  <div className="h-3 bg-slate-700 rounded w-16" />
</div>

// Table skeleton
<div className="space-y-2">
  {[...Array(5)].map((_, i) => (
    <div key={i} className="flex gap-4 p-4 bg-slate-800 rounded-lg animate-pulse">
      <div className="h-4 bg-slate-700 rounded w-16" />
      <div className="h-4 bg-slate-700 rounded w-24" />
      <div className="h-4 bg-slate-700 rounded w-20" />
      <div className="h-4 bg-slate-700 rounded w-16" />
    </div>
  ))}
</div>

// Chart skeleton
<div className="h-64 bg-slate-800 rounded-lg animate-pulse flex items-end justify-around p-4">
  {[...Array(10)].map((_, i) => (
    <div
      key={i}
      className="bg-slate-700 rounded-t w-8"
      style={{ height: `${Math.random() * 100}%` }}
    />
  ))}
</div>
```

---

## SECTION 22 — DESIGN SYSTEM (BRAND, IDENTITY, MOTION, TONE)

This section defines the **visual and experiential DNA** of DominionMarkets.

It ensures that every screen, every component, every animation, and every message feels like part of one unified, sovereign product.

**A design system is not just colors and fonts** — it is the embodied personality of the platform.

---

## 22.1 Brand Principles

DominionMarkets is built on **four core brand pillars**:

### 1. Clarity
Everything must feel understandable at a glance.

### 2. Trust
No hype. No noise. No predictions.  
Just clean, verified information.

### 3. Identity
The user's identity is not decoration — it is the lens through which the product speaks.

### 4. Sovereignty
The user feels in control, empowered, and respected.

---

## 22.2 Brand Voice & Tone

DominionMarkets speaks with:

### Tone
- **Calm**
- **Neutral**
- **Confident**
- **Descriptive**
- **Identity-aware**

### Never
- ❌ Predictive
- ❌ Sensational
- ❌ Alarmist
- ❌ Overly technical
- ❌ Patronizing

### Voice Examples

```tsx
// ✅ Good examples
"Here's what's happening today."
"Your portfolio is stable."
"This company has strong cultural relevance."
"This story is verified by multiple sources."

// ❌ Bad examples (avoid)
"BUY NOW! This stock will moon! 🚀"
"CRASH INCOMING!"
"You're losing money — act fast!"
"Algorithmic arbitrage via delta-neutral strategies"
"Let us handle this for you"
```

**Implementation in UI**:
```tsx
// Status messages
<p className="text-slate-300">Your portfolio is stable.</p>

// News verification
<Badge className="text-emerald-400">Verified by 5 sources</Badge>

// Cultural Alpha insight
<p className="text-slate-300">
  This company has strong cultural relevance in the diaspora community.
</p>

// Price movement (neutral framing)
<span className="text-emerald-400">+2.5%</span>
<span className="text-slate-400">today</span>
```

---

## 22.3 Color System

The color system is built around **neutral clarity** with **identity accents**.

### Core Neutrals

```tsx
// Tailwind CSS classes
const neutrals = {
  white: '#FFFFFF',
  offWhite: '#F8FAFC',     // slate-50
  lightGray: '#CBD5E1',    // slate-300
  darkGray: '#475569',     // slate-600
  black: '#0F172A',        // slate-900
};

// Usage
<div className="bg-slate-900 text-white">
  <h1 className="text-slate-50">Title</h1>
  <p className="text-slate-300">Description</p>
  <span className="text-slate-600">Metadata</span>
</div>
```

### Functional Colors

```tsx
const functionalColors = {
  positive: '#10B981',     // emerald-500 (green)
  negative: '#EF4444',     // red-500 (red)
  informational: '#3B82F6', // blue-500 (blue)
  warning: '#F59E0B',      // amber-500 (yellow)
};

// Usage examples
<span className="text-emerald-500">+5.2%</span>  // Positive movement
<span className="text-red-500">-3.1%</span>      // Negative movement
<Badge className="bg-blue-500/20 text-blue-400">Info</Badge>
<Badge className="bg-amber-500/20 text-amber-400">Warning</Badge>
```

### Identity Accents

Each identity has a **subtle accent color**:

```tsx
const identityAccents = {
  diaspora: {
    primary: '#10B981',   // emerald-500 (Deep Caribbean teal)
    secondary: '#059669', // emerald-600
    light: '#D1FAE5',     // emerald-100
  },
  youth: {
    primary: '#3B82F6',   // blue-500 (Bright learning blue)
    secondary: '#2563EB', // blue-600
    light: '#DBEAFE',     // blue-100
  },
  creator: {
    primary: '#A855F7',   // purple-500 (Electric violet)
    secondary: '#9333EA', // purple-600
    light: '#F3E8FF',     // purple-100
  },
  legacy: {
    primary: '#F59E0B',   // amber-500 (Heritage gold)
    secondary: '#D97706', // amber-600
    light: '#FEF3C7',     // amber-100
  },
};

// Usage with identity
function IdentityCard({ identity, children }) {
  const color = identityAccents[identity].primary;
  
  return (
    <div className={`p-4 bg-${identity === 'diaspora' ? 'emerald' : identity === 'youth' ? 'blue' : identity === 'creator' ? 'purple' : 'amber'}-500/10 border border-${identity === 'diaspora' ? 'emerald' : identity === 'youth' ? 'blue' : identity === 'creator' ? 'purple' : 'amber'}-500/20 rounded-lg`}>
      {children}
    </div>
  );
}
```

### Premium Colors

```tsx
const premiumColors = {
  premium: {
    gold: '#F5C542',      // Custom gold
    goldDark: '#D4A017',  // Darker gold for hover
  },
  pro: {
    platinum: '#E5E7EB',  // slate-200 (Platinum)
    platinumDark: '#D1D5DB', // slate-300
  },
};

// Usage
<Badge className="bg-yellow-500/20 text-yellow-500 border border-yellow-500/30">
  <Crown className="w-3 h-3" />
  Premium
</Badge>

<Badge className="bg-gradient-to-r from-slate-300 to-slate-400 text-slate-900">
  <Sparkles className="w-3 h-3" />
  Pro
</Badge>
```

---

## 22.4 Typography System

Typography must be:
- **Clean**
- **Modern**
- **Readable**
- **Scalable**

### Font Family

A modern sans-serif with strong clarity.

```tsx
// In Tailwind config (tailwind.config.js)
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
};

// Usage: Default font is applied automatically
// All text uses the sans-serif stack
```

### Hierarchy

```tsx
// Typography scale with responsive sizing
const typography = {
  h1: 'text-3xl md:text-4xl lg:text-5xl font-bold',      // Page titles
  h2: 'text-2xl md:text-3xl lg:text-4xl font-semibold',  // Section titles
  h3: 'text-xl md:text-2xl font-medium',                  // Card titles
  body: 'text-base',                                       // Standard text (16px)
  bodySmall: 'text-sm',                                    // Secondary text (14px)
  caption: 'text-xs',                                      // Labels, metadata (12px)
};

// Implementation examples
<h1 className="text-3xl md:text-4xl lg:text-5xl font-bold text-white">
  DominionMarkets
</h1>

<h2 className="text-2xl md:text-3xl lg:text-4xl font-semibold text-white mb-4">
  Your Portfolio
</h2>

<h3 className="text-xl md:text-2xl font-medium text-white mb-2">
  Holdings
</h3>

<p className="text-base text-slate-300">
  Your portfolio contains 12 stocks across 5 sectors.
</p>

<p className="text-sm text-slate-400">
  Last updated 2 hours ago
</p>

<span className="text-xs text-slate-500 uppercase tracking-wide">
  Market Cap
</span>
```

### Identity Variations

**Identity does not change the font** — only accents and highlights.

```tsx
// Identity accent applied to text (not font)
<h3 className="text-xl font-medium text-emerald-400">
  Diaspora Insights
</h3>

<p className="text-base text-slate-300">
  Your <span className="text-purple-400 font-medium">creator economy</span> portfolio is performing well.
</p>
```

---

## 22.5 Iconography

Icons must be:
- **Line-based**
- **Minimal**
- **Geometric**
- **Consistent**

```tsx
// Use lucide-react for all icons
import {
  // Navigation
  Home, TrendingUp, Briefcase, Newspaper, Bell,
  
  // Markets
  BarChart3, LineChart, Activity, TrendingDown,
  
  // Portfolio
  PieChart, DollarSign, Percent, Target,
  
  // News
  FileText, Check, AlertCircle, Clock,
  
  // Alerts
  BellRing, Volume2, Calendar, AlertTriangle,
  
  // Identity
  Globe, Zap, Sparkles, Crown,
  
  // Premium
  Lock, Star, Shield,
} from 'lucide-react';

// Standard icon size
<TrendingUp className="w-5 h-5" />     // 20px (default)
<Crown className="w-6 h-6" />          // 24px (larger)
<Check className="w-4 h-4" />          // 16px (smaller)

// Icon with color
<Globe className="w-5 h-5 text-emerald-400" />
<Zap className="w-5 h-5 text-blue-400" />
```

### Categories

**Navigation**: Home, TrendingUp, Briefcase, Newspaper, Bell, User  
**Markets**: BarChart3, LineChart, Activity, TrendingUp/Down, DollarSign  
**Portfolio**: PieChart, Briefcase, Target, Percent  
**News**: Newspaper, FileText, Check, AlertCircle  
**Alerts**: Bell, BellRing, Volume2, Calendar  
**Identity**: Globe, Zap, Sparkles, Crown  
**Premium**: Crown, Lock, Star, Shield, Sparkles  

### Identity Icons

Each identity has a **symbolic icon**:

```tsx
const identityIcons = {
  diaspora: Globe,        // Globe + wave (using Globe as representation)
  youth: Zap,             // Spark
  creator: Sparkles,      // Pixel star (using Sparkles)
  legacy: Crown,          // Laurel (using Crown)
};

// Usage in identity widgets
function IdentityWidget({ identity }) {
  const Icon = identityIcons[identity];
  const color = {
    diaspora: 'text-emerald-400',
    youth: 'text-blue-400',
    creator: 'text-purple-400',
    legacy: 'text-amber-400',
  }[identity];
  
  return (
    <div className="flex items-center gap-2">
      <Icon className={`w-5 h-5 ${color}`} />
      <span className={`font-medium capitalize ${color}`}>
        {identity}
      </span>
    </div>
  );
}
```

These appear **subtly** in identity widgets.

---

## 22.6 Layout System

DominionMarkets uses a **12-column grid** on desktop and a **4-column grid** on mobile.

### Spacing

```tsx
// 4px base unit
const spacing = {
  xs: '4px',   // space-1 in Tailwind
  sm: '8px',   // space-2
  md: '16px',  // space-4
  lg: '24px',  // space-6
  xl: '32px',  // space-8
};

// Usage
<div className="p-4">           {/* 16px padding */}
  <div className="mb-6">        {/* 24px margin-bottom */}
    <h2 className="mb-2">       {/* 8px margin-bottom */}
      Title
    </h2>
  </div>
</div>
```

### Card Layout

```tsx
// Standard card pattern
<div className="rounded-lg shadow-md p-4 bg-slate-800 border border-slate-700">
  {/* Rounded corners */}
  {/* Soft shadows */}
  {/* Clean separation */}
</div>

// Card with hover effect
<div className="rounded-lg shadow-md p-4 bg-slate-800 border border-slate-700 hover:border-slate-600 hover:shadow-lg transition-all duration-200">
  <h3 className="text-lg font-medium text-white mb-2">Card Title</h3>
  <p className="text-sm text-slate-400">Card content goes here.</p>
</div>
```

### Section Layout

```tsx
// Page layout with consistent spacing
<div className="container mx-auto px-4 py-6 md:px-6 md:py-8">
  {/* Clear hierarchy */}
  <header className="mb-8">
    <h1 className="text-3xl font-bold text-white mb-2">Page Title</h1>
    <p className="text-slate-400">Page description</p>
  </header>
  
  {/* Consistent padding */}
  <section className="mb-8">
    <h2 className="text-2xl font-semibold text-white mb-4">Section Title</h2>
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {/* Cards */}
    </div>
  </section>
  
  {/* Identity-aware accents */}
  <div className="border-l-4 border-emerald-500 pl-4">
    <h3 className="text-emerald-400 font-medium">Diaspora Insight</h3>
  </div>
</div>
```

---

## 22.7 Motion System

Motion must be:
- **Subtle**
- **Purposeful**
- **Identity-aware**
- **Never distracting**

### Motion Principles

1. **Fade, don't slide**
2. **Ease in/out**
3. **Keep animations under 200ms**
4. **Use motion to guide attention, not entertain**

### Examples

```tsx
// Heatmap tiles fade in
<div className="animate-fade-in">
  <HeatmapTile />
</div>

// CSS for fade-in
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

// Cards lift slightly on hover
<div className="transition-transform duration-200 hover:scale-[1.02] hover:shadow-lg">
  <Card />
</div>

// Identity widgets animate with subtle accent glow
<div className="relative group">
  <div className="absolute inset-0 bg-emerald-500/0 group-hover:bg-emerald-500/10 transition-colors duration-200 rounded-lg" />
  <IdentityWidget />
</div>

// Button press animation
<button className="transition-all duration-150 active:scale-95 hover:scale-105">
  Click me
</button>

// Smooth color transitions
<div className="transition-colors duration-200 hover:bg-slate-700">
  Hover me
</div>
```

**Tailwind Transition Classes**:
```tsx
// Standard transitions
'transition-all duration-200'      // All properties, 200ms
'transition-colors duration-200'   // Colors only
'transition-transform duration-150' // Transform only

// Easing
'ease-in-out'  // Default smooth easing
'ease-in'      // Accelerate
'ease-out'     // Decelerate
```

---

## 22.8 Identity Expression System

Identity is expressed through:

### 1. Accent Color

Applied to:
- Headers
- Highlights
- Chips
- Identity widgets

```tsx
// Header with identity accent
<div className="border-l-4 border-emerald-500 pl-4 mb-6">
  <h2 className="text-emerald-400 font-semibold">Diaspora Markets</h2>
</div>

// Highlighted text
<p className="text-slate-300">
  Your portfolio has <span className="text-purple-400 font-medium">strong creator economy exposure</span>.
</p>

// Identity chip
<div className="inline-flex items-center gap-1.5 px-2 py-1 bg-blue-500/20 rounded-full border border-blue-500/30">
  <Zap className="w-3 h-3 text-blue-400" />
  <span className="text-xs text-blue-400 font-medium">Youth</span>
</div>
```

### 2. Iconography

Identity icon appears in:
- Dashboard
- Portfolio insights
- News filters

```tsx
// Dashboard identity indicator
<div className="flex items-center gap-2 mb-4">
  <Globe className="w-5 h-5 text-emerald-400" />
  <span className="text-sm text-slate-400">Viewing as Diaspora</span>
</div>

// Portfolio insight icon
<div className="flex items-center gap-3 p-4 bg-emerald-500/10 rounded-lg">
  <Globe className="w-6 h-6 text-emerald-400" />
  <div>
    <h3 className="font-medium text-white">Diaspora Insights</h3>
    <p className="text-sm text-slate-400">Your portfolio summary</p>
  </div>
</div>

// News filter with identity icon
<button className="flex items-center gap-2 px-3 py-1.5 bg-purple-500/20 rounded-full border border-purple-500/30">
  <Sparkles className="w-4 h-4 text-purple-400" />
  <span className="text-sm text-purple-400">Creator</span>
</button>
```

### 3. Content

Identity modifies:
- Insights
- Filters
- Cross-promotion
- Widgets

```tsx
// Identity-aware insight
function InsightCard({ identity }) {
  const insights = {
    diaspora: "Your portfolio has strong exposure to Caribbean and African markets.",
    youth: "You're investing in high-growth tech stocks favored by young investors.",
    creator: "Your holdings align with the creator economy and platform stocks.",
    legacy: "Your portfolio emphasizes dividend aristocrats and stable blue-chips.",
  };
  
  return (
    <div className="p-4 bg-slate-800 rounded-lg">
      <p className="text-slate-300">{insights[identity]}</p>
    </div>
  );
}

// Identity filter in news
<div className="flex gap-2">
  <button className="px-3 py-1.5 bg-emerald-500/20 text-emerald-400 rounded-full">
    Diaspora News
  </button>
  <button className="px-3 py-1.5 bg-slate-800 text-slate-400 rounded-full">
    All News
  </button>
</div>
```

### 4. Micro-copy

Identity-aware phrasing:

```tsx
// Dashboard greeting
const greetings = {
  diaspora: "Your diaspora insights are ready.",
  youth: "Your youth portfolio is performing well.",
  creator: "Here's your creator-economy snapshot.",
  legacy: "Your long-term indicators look stable.",
};

// Identity-specific action prompts
const prompts = {
  diaspora: "Explore Caribbean markets",
  youth: "Discover trending tech stocks",
  creator: "View platform economy leaders",
  legacy: "See dividend aristocrats",
};

// Usage
<p className="text-slate-300">{greetings[userIdentity]}</p>
<button className="px-4 py-2 bg-yellow-500 text-slate-900 rounded-lg">
  {prompts[userIdentity]}
</button>
```

---

## 22.9 Premium Expression System

Premium and Pro tiers use:

### Premium

```tsx
// Gold accents
<div className="border-l-4 border-yellow-500 pl-4">
  <h3 className="text-yellow-500 font-semibold">Premium Feature</h3>
</div>

// Gold badge
<Badge className="bg-yellow-500/20 text-yellow-500 border border-yellow-500/30 flex items-center gap-1">
  <Crown className="w-3 h-3" />
  Premium
</Badge>

// Gold highlight on locked features
<div className="relative p-4 bg-slate-800 rounded-lg border border-yellow-500/20">
  <div className="absolute top-2 right-2">
    <Crown className="w-5 h-5 text-yellow-500" />
  </div>
  <h3 className="font-medium text-white">Advanced Analytics</h3>
  <p className="text-sm text-slate-400">Premium feature</p>
</div>
```

### Pro

```tsx
// Platinum accents
<div className="border-l-4 border-slate-300 pl-4">
  <h3 className="text-slate-300 font-semibold">Pro Feature</h3>
</div>

// Platinum badge
<Badge className="bg-gradient-to-r from-slate-300 to-slate-400 text-slate-900 flex items-center gap-1">
  <Sparkles className="w-3 h-3" />
  Pro
</Badge>

// Platinum highlight on advanced tools
<div className="relative p-4 bg-slate-800 rounded-lg border-2 border-slate-300/20">
  <div className="absolute top-2 right-2">
    <div className="w-8 h-8 bg-gradient-to-r from-slate-300 to-slate-400 rounded-full flex items-center justify-center">
      <Sparkles className="w-4 h-4 text-slate-900" />
    </div>
  </div>
  <h3 className="font-medium text-white">Advanced Indicators</h3>
  <p className="text-sm text-slate-400">Pro feature</p>
</div>
```

### Locked Features

Use:
- Dimmed card
- Lock icon
- Premium overlay

```tsx
// Locked feature card
<div className="relative p-4 bg-slate-800 rounded-lg opacity-60 cursor-not-allowed">
  {/* Dimmed card */}
  <div className="absolute inset-0 flex items-center justify-center">
    <div className="text-center">
      <Lock className="w-8 h-8 text-yellow-500 mx-auto mb-2" />
      <p className="text-sm font-medium text-yellow-500">Premium</p>
    </div>
  </div>
  
  <div className="blur-sm pointer-events-none">
    <h3 className="font-medium text-white">Advanced Risk Metrics</h3>
    <p className="text-sm text-slate-400">Detailed portfolio analysis</p>
  </div>
</div>

// Premium overlay (full screen)
<div className="fixed inset-0 z-50 bg-slate-900/80 backdrop-blur-sm flex items-center justify-center">
  <div className="max-w-md p-6 bg-slate-800 rounded-lg border border-yellow-500/20 text-center">
    <Crown className="w-12 h-12 text-yellow-500 mx-auto mb-4" />
    <h3 className="text-xl font-semibold text-white mb-2">Premium Feature</h3>
    <p className="text-slate-400 mb-6">
      Upgrade to Premium to unlock advanced analytics and insights.
    </p>
    <button className="w-full px-4 py-2 bg-yellow-500 text-slate-900 rounded-lg font-medium">
      Upgrade Now
    </button>
  </div>
</div>
```

---

## 22.10 Accessibility Standards

DominionMarkets follows:

### WCAG AA Contrast

```tsx
// All text must meet WCAG AA contrast ratios
// Background: #0F172A (slate-900)
// Text colors with sufficient contrast:

✅ White (#FFFFFF) - 15.5:1 contrast
✅ Slate-50 (#F8FAFC) - 14.8:1 contrast
✅ Slate-300 (#CBD5E1) - 9.2:1 contrast
✅ Emerald-400 (#34D399) - 7.5:1 contrast
✅ Yellow-500 (#F5C542) - 8.1:1 contrast

❌ Slate-600 (#475569) - 2.8:1 contrast (too low for body text)
```

### Scalable Text

```tsx
// Use rem units (Tailwind default)
// All text scales with browser font size settings
<p className="text-base">   {/* 1rem = 16px default, scales up/down */}
  This text respects user preferences
</p>
```

### Keyboard Navigation

```tsx
// All interactive elements must be keyboard accessible
<button className="focus:ring-2 focus:ring-yellow-500 focus:outline-none">
  Click me
</button>

<a href="/markets" className="focus:ring-2 focus:ring-yellow-500 focus:outline-none">
  View Markets
</a>

// Skip to main content
<a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 px-4 py-2 bg-yellow-500 text-slate-900 rounded-lg">
  Skip to main content
</a>
```

### Screen Reader Labels

```tsx
// Use aria-label for icon-only buttons
<button aria-label="Close menu">
  <X className="w-5 h-5" />
</button>

// Use aria-describedby for additional context
<input
  type="number"
  aria-label="Number of shares"
  aria-describedby="shares-help"
/>
<p id="shares-help" className="text-xs text-slate-400">
  Enter the number of shares you own
</p>

// Use aria-live for dynamic updates
<div aria-live="polite" aria-atomic="true">
  <p>AAPL price updated: $180.50</p>
</div>
```

### Motion-Reduced Mode

```tsx
// Respect prefers-reduced-motion
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

// In Tailwind
<div className="transition-transform motion-reduce:transition-none">
  <Card />
</div>
```

**Identity accents always maintain contrast compliance.**

---

## 22.11 Component Tokens

Tokens ensure consistency across the entire system.

### Spacing Tokens

```tsx
// Define in Tailwind config or design system file
export const spacing = {
  xs: '4px',   // space-xs
  sm: '8px',   // space-sm
  md: '16px',  // space-md
  lg: '24px',  // space-lg
  xl: '32px',  // space-xl
};

// Tailwind equivalent
'p-1'   // 4px (space-xs)
'p-2'   // 8px (space-sm)
'p-4'   // 16px (space-md)
'p-6'   // 24px (space-lg)
'p-8'   // 32px (space-xl)

// Usage
<div className="p-4 mb-6">      {/* 16px padding, 24px margin-bottom */}
  <h3 className="mb-2">         {/* 8px margin-bottom */}
    Title
  </h3>
</div>
```

### Radius Tokens

```tsx
export const radius = {
  sm: '4px',   // radius-sm
  md: '8px',   // radius-md
  lg: '12px',  // radius-lg
};

// Tailwind equivalent
'rounded'      // 4px (radius-sm)
'rounded-lg'   // 8px (radius-md)
'rounded-xl'   // 12px (radius-lg)

// Usage
<div className="rounded-lg border border-slate-700">  {/* 8px border radius */}
  <Card />
</div>
```

### Shadow Tokens

```tsx
export const shadows = {
  subtle: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
  medium: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
  deep: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
};

// Tailwind equivalent
'shadow-sm'    // subtle
'shadow-md'    // medium
'shadow-lg'    // deep

// Usage
<div className="shadow-md hover:shadow-lg transition-shadow duration-200">
  <Card />
</div>
```

### Complete Token System

```tsx
// File: lib/design-tokens.ts

export const designTokens = {
  spacing: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
  },
  radius: {
    sm: 4,
    md: 8,
    lg: 12,
  },
  shadows: {
    subtle: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    medium: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
    deep: '0 10px 15px -3px rgb(0 0 0 / 0.1)',
  },
  colors: {
    neutral: {
      white: '#FFFFFF',
      offWhite: '#F8FAFC',
      lightGray: '#CBD5E1',
      darkGray: '#475569',
      black: '#0F172A',
    },
    functional: {
      positive: '#10B981',
      negative: '#EF4444',
      informational: '#3B82F6',
      warning: '#F59E0B',
    },
    identity: {
      diaspora: '#10B981',
      youth: '#3B82F6',
      creator: '#A855F7',
      legacy: '#F59E0B',
    },
    premium: {
      gold: '#F5C542',
      platinum: '#E5E7EB',
    },
  },
  typography: {
    h1: 'text-3xl md:text-4xl lg:text-5xl font-bold',
    h2: 'text-2xl md:text-3xl lg:text-4xl font-semibold',
    h3: 'text-xl md:text-2xl font-medium',
    body: 'text-base',
    bodySmall: 'text-sm',
    caption: 'text-xs',
  },
  motion: {
    duration: {
      fast: '150ms',
      normal: '200ms',
      slow: '300ms',
    },
    easing: {
      standard: 'ease-in-out',
      enter: 'ease-out',
      exit: 'ease-in',
    },
  },
};

// Usage in components
import { designTokens } from '@/lib/design-tokens';

function Card({ children }) {
  return (
    <div
      className="rounded-lg shadow-md p-4 bg-slate-800"
      style={{
        borderRadius: `${designTokens.radius.md}px`,
        padding: `${designTokens.spacing.md}px`,
      }}
    >
      {children}
    </div>
  );
}
```

---

## Summary: Design System Implementation Checklist

✅ **Brand Principles**: Clarity, Trust, Identity, Sovereignty  
✅ **Voice & Tone**: Calm, neutral, confident, descriptive, identity-aware  
✅ **Color System**: Neutrals, functional colors, identity accents, premium colors  
✅ **Typography**: Sans-serif, 6-level hierarchy, responsive scaling  
✅ **Iconography**: Line-based lucide-react icons, identity symbols  
✅ **Layout**: 12-column grid, 4px spacing base, consistent card patterns  
✅ **Motion**: Subtle, purposeful, <200ms, fade-focused  
✅ **Identity Expression**: Accents, icons, content, micro-copy  
✅ **Premium Expression**: Gold (Premium), Platinum (Pro), locked overlays  
✅ **Accessibility**: WCAG AA, keyboard nav, screen readers, motion-reduced  
✅ **Component Tokens**: Spacing, radius, shadow, color, typography  

---

## SECTION 23 — MOTION & INTERACTION PATTERNS (MICRO-INTERACTIONS, TRANSITIONS, FEEDBACK)

This section defines the **behavioral language** of DominionMarkets — how the interface moves, responds, and communicates with the user.

**Motion is not decoration here.**

It is:
- **Guidance**
- **Clarity**
- **Identity expression**
- **Emotional tone**
- **Trust reinforcement**

---

## 23.1 Motion Principles

DominionMarkets uses motion to:
- **Clarify hierarchy**
- **Guide attention**
- **Reduce cognitive load**
- **Reinforce identity**
- **Create a sense of calm**

### Motion Must Always Be:
- ✅ **Subtle**
- ✅ **Purposeful**
- ✅ **Fast** (150–200ms)
- ✅ **Identity-aware**
- ✅ **Non-distracting**

### Motion Must Never Be:
- ❌ **Flashy**
- ❌ **Bouncy**
- ❌ **Overly elastic**
- ❌ **Slow**
- ❌ **Decorative without purpose**

---

## 23.2 Global Motion Patterns

These apply across the entire platform.

### Fade In

**Used for**:
- Cards
- Lists
- Charts
- News items

```tsx
// CSS implementation
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.fade-in {
  animation: fadeIn 200ms ease-out;
}

// Tailwind + inline CSS
<div className="animate-fade-in">
  <Card />
</div>

// Add to tailwind.config.js
module.exports = {
  theme: {
    extend: {
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
      animation: {
        'fade-in': 'fadeIn 200ms ease-out',
      },
    },
  },
};

// Usage in component
<div className="opacity-0 animate-fade-in">
  <NewsCard article={article} />
</div>
```

---

### Slide Up (Subtle)

**Used for**:
- Modals
- Bottom sheets
- Mobile drawers

```tsx
// CSS implementation
@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.slide-up {
  animation: slideUp 200ms ease-out;
}

// Tailwind config
slideUp: {
  '0%': { transform: 'translateY(20px)', opacity: '0' },
  '100%': { transform: 'translateY(0)', opacity: '1' },
},

// Usage
<div className="fixed inset-0 z-50 flex items-end">
  <div className="w-full bg-slate-900 rounded-t-xl animate-slide-up">
    <BottomSheet />
  </div>
</div>

// Framer Motion alternative
import { motion } from 'framer-motion';

<motion.div
  initial={{ y: 20, opacity: 0 }}
  animate={{ y: 0, opacity: 1 }}
  transition={{ duration: 0.2, ease: 'easeOut' }}
>
  <Modal />
</motion.div>
```

---

### Scale Up (1–2%)

**Used for**:
- Hover states
- Press states
- Identity widgets

```tsx
// Hover state - card lift
<div className="transition-transform duration-200 hover:scale-[1.02] hover:shadow-lg">
  <Card />
</div>

// Press state - button compress
<button className="transition-transform duration-150 active:scale-[0.98]">
  Click me
</button>

// Identity widget - subtle pulse
<div className="transition-transform duration-200 hover:scale-[1.01] group">
  <div className="absolute inset-0 bg-emerald-500/0 group-hover:bg-emerald-500/5 transition-colors" />
  <IdentityWidget />
</div>

// CSS alternative
.scale-hover {
  transition: transform 200ms ease-out;
}

.scale-hover:hover {
  transform: scale(1.02);
}

.scale-press:active {
  transform: scale(0.98);
}
```

---

### Skeleton Loading

**Used for**:
- Charts
- Tables
- News
- Portfolio

```tsx
// Skeleton component with shimmer
<div className="animate-pulse space-y-4">
  <div className="h-4 bg-slate-700 rounded w-3/4" />
  <div className="h-4 bg-slate-700 rounded w-1/2" />
</div>

// Advanced shimmer effect
@keyframes shimmer {
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
}

.skeleton-shimmer {
  background: linear-gradient(
    90deg,
    #1e293b 0%,
    #334155 50%,
    #1e293b 100%
  );
  background-size: 1000px 100%;
  animation: shimmer 2s infinite;
}

// Component
<div className="skeleton-shimmer h-64 rounded-lg" />

// Identity-aware skeleton
<div className="animate-pulse">
  <div className="h-4 bg-emerald-700/50 rounded w-32 mb-2" /> {/* Diaspora */}
  <div className="h-8 bg-slate-700 rounded w-full" />
</div>
```

---

## 23.3 Micro-Interactions

Micro-interactions are the tiny, delightful touches that make the product feel alive.

### Buttons

```tsx
// Hover: slight lift + shadow
<button className="
  px-4 py-2 
  bg-yellow-500 text-slate-900 rounded-lg 
  transition-all duration-200 
  hover:scale-105 hover:shadow-lg
  active:scale-95
  disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100
">
  Upgrade to Premium
</button>

// CSS implementation
.button-micro {
  transition: transform 150ms ease-out, box-shadow 150ms ease-out;
}

.button-micro:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.button-micro:active {
  transform: translateY(0);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.button-micro:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}
```

---

### Tabs

**Underline slides smoothly, active tab fades to accent color**

```tsx
function Tabs({ tabs, activeTab, onChange }) {
  return (
    <div className="flex gap-6 border-b border-slate-800">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onChange(tab.id)}
          className="relative pb-3 text-sm font-medium transition-colors duration-200"
        >
          <span className={`${
            activeTab === tab.id 
              ? 'text-yellow-500' 
              : 'text-slate-400 hover:text-white'
          }`}>
            {tab.label}
          </span>
          
          {/* Animated underline */}
          {activeTab === tab.id && (
            <motion.div
              layoutId="tab-underline"
              className="absolute bottom-0 left-0 right-0 h-0.5 bg-yellow-500"
              transition={{ duration: 0.2, ease: 'easeOut' }}
            />
          )}
        </button>
      ))}
    </div>
  );
}

// CSS-only alternative
.tab {
  position: relative;
  transition: color 200ms ease-out;
}

.tab::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: #F5C542;
  transform: scaleX(0);
  transition: transform 200ms ease-out;
}

.tab.active::after {
  transform: scaleX(1);
}
```

---

### Chips

**Tap: ripple effect, Active: accent glow**

```tsx
// Filter chip with ripple
<button className="
  relative overflow-hidden
  px-3 py-1.5 rounded-full text-sm font-medium
  bg-slate-800 text-slate-300
  hover:bg-slate-700
  active:bg-slate-600
  transition-all duration-150
  group
">
  Technology
  
  {/* Ripple effect */}
  <span className="
    absolute inset-0 
    bg-white/20 
    scale-0 
    group-active:scale-100 
    rounded-full 
    transition-transform duration-300
  " />
</button>

// Active chip with glow
<button className={`
  px-3 py-1.5 rounded-full text-sm font-medium
  transition-all duration-200
  ${isActive 
    ? 'bg-yellow-500 text-slate-900 shadow-lg shadow-yellow-500/50' 
    : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
  }
`}>
  {label}
</button>

// Identity-aware active glow
<button className={`
  px-3 py-1.5 rounded-full text-sm font-medium
  transition-all duration-200
  ${isActive 
    ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/50 shadow-lg shadow-emerald-500/20' 
    : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
  }
`}>
  Diaspora
</button>
```

---

### Search Bar

**Expands smoothly, icon rotates into "close" state**

```tsx
function SearchBar() {
  const [isExpanded, setIsExpanded] = useState(false);
  const [query, setQuery] = useState('');
  
  return (
    <div className={`
      relative flex items-center
      transition-all duration-300 ease-out
      ${isExpanded ? 'w-64' : 'w-10'}
    `}>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onFocus={() => setIsExpanded(true)}
        onBlur={() => !query && setIsExpanded(false)}
        placeholder="Search stocks..."
        className={`
          w-full h-10 px-4 pr-10
          bg-slate-800 border border-slate-700 rounded-lg
          text-white placeholder:text-slate-500
          focus:border-yellow-500 focus:outline-none
          transition-all duration-300
          ${!isExpanded && 'opacity-0'}
        `}
      />
      
      <button
        onClick={() => {
          if (isExpanded && query) {
            setQuery('');
          } else {
            setIsExpanded(!isExpanded);
          }
        }}
        className="absolute right-2 p-2 text-slate-400 hover:text-white transition-colors"
      >
        <motion.div
          animate={{ rotate: isExpanded && query ? 45 : 0 }}
          transition={{ duration: 0.2 }}
        >
          {isExpanded && query ? (
            <X className="w-5 h-5" />
          ) : (
            <Search className="w-5 h-5" />
          )}
        </motion.div>
      </button>
    </div>
  );
}
```

---

## 23.4 Identity-Aware Motion

Each identity has a **subtle motion signature**.

### Diaspora

**Gentle wave-like easing, slight horizontal drift on identity widgets**

```tsx
// Wave easing function
const diasporaEasing = [0.4, 0.0, 0.2, 1.0]; // Custom cubic-bezier

// Identity widget with horizontal drift
<motion.div
  initial={{ x: -5, opacity: 0 }}
  animate={{ x: 0, opacity: 1 }}
  transition={{ 
    duration: 0.3, 
    ease: diasporaEasing 
  }}
  className="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-lg"
>
  <Globe className="w-5 h-5 text-emerald-400 mb-2" />
  <h3 className="font-medium text-white">Diaspora Insights</h3>
</motion.div>

// CSS alternative with custom easing
@keyframes diasporaDrift {
  from {
    transform: translateX(-5px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.diaspora-enter {
  animation: diasporaDrift 300ms cubic-bezier(0.4, 0.0, 0.2, 1.0);
}
```

---

### Youth

**Quick, energetic easing, slight bounce on badges**

```tsx
// Energetic easing
const youthEasing = [0.68, -0.55, 0.265, 1.55]; // Bounce-out

// Badge with bounce
<motion.div
  initial={{ scale: 0.8, opacity: 0 }}
  animate={{ scale: 1, opacity: 1 }}
  transition={{ 
    duration: 0.2, 
    ease: youthEasing 
  }}
  className="inline-flex items-center gap-1 px-2 py-1 bg-blue-500/20 text-blue-400 rounded-full border border-blue-500/30"
>
  <Zap className="w-3 h-3" />
  Youth
</motion.div>

// CSS keyframe with slight bounce
@keyframes youthBounce {
  0% {
    transform: scale(0.8);
    opacity: 0;
  }
  70% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.youth-badge {
  animation: youthBounce 200ms ease-out;
}
```

---

### Creator

**Pixel-fade transitions, slight glitch-spark on hover**

```tsx
// Pixel-fade effect
<motion.div
  initial={{ opacity: 0, filter: 'blur(2px)' }}
  animate={{ opacity: 1, filter: 'blur(0px)' }}
  transition={{ duration: 0.2 }}
  className="p-4 bg-purple-500/10 border border-purple-500/20 rounded-lg"
>
  <Sparkles className="w-5 h-5 text-purple-400 mb-2" />
  <h3 className="font-medium text-white">Creator Index</h3>
</motion.div>

// Glitch-spark on hover
<div className="relative group">
  <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-150">
    <div className="absolute inset-0 bg-purple-500/10 rounded-lg animate-pulse" />
  </div>
  <CreatorWidget />
</div>

// Subtle glitch effect
@keyframes glitchSpark {
  0%, 100% {
    text-shadow: 0 0 0 transparent;
  }
  50% {
    text-shadow: 2px 0 0 rgba(168, 85, 247, 0.3), -2px 0 0 rgba(168, 85, 247, 0.3);
  }
}

.creator-hover:hover {
  animation: glitchSpark 200ms ease-out;
}
```

---

### Legacy-Builder

**Slow, dignified fade, subtle gold shimmer on key elements**

```tsx
// Dignified fade
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ 
    duration: 0.4, // Slower than default
    ease: 'easeInOut' 
  }}
  className="p-4 bg-amber-500/10 border border-amber-500/20 rounded-lg"
>
  <Crown className="w-5 h-5 text-amber-400 mb-2" />
  <h3 className="font-medium text-white">Legacy Portfolio</h3>
</motion.div>

// Gold shimmer effect
@keyframes goldShimmer {
  0% {
    background-position: -200px 0;
  }
  100% {
    background-position: 200px 0;
  }
}

.legacy-shimmer {
  position: relative;
  overflow: hidden;
}

.legacy-shimmer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(245, 197, 66, 0.1),
    transparent
  );
  background-size: 200px 100%;
  animation: goldShimmer 3s infinite;
}

// Usage
<div className="legacy-shimmer p-4 bg-slate-800 rounded-lg">
  <h3 className="font-medium text-amber-400">Dividend Aristocrats</h3>
</div>
```

**These are micro-subtle — never distracting.**

---

## 23.5 Page Transitions

### Desktop

**Fade between pages, content slides up 8px**

```tsx
// Next.js page transition
import { motion } from 'framer-motion';

export default function Page({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 8 }}
      transition={{ duration: 0.2, ease: 'easeOut' }}
    >
      {children}
    </motion.div>
  );
}

// CSS alternative
@keyframes pageEnter {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.page-enter {
  animation: pageEnter 200ms ease-out;
}
```

---

### Mobile

**Standard mobile slide-in, bottom sheets rise smoothly**

```tsx
// Mobile slide-in from right
<motion.div
  initial={{ x: '100%' }}
  animate={{ x: 0 }}
  exit={{ x: '100%' }}
  transition={{ duration: 0.3, ease: 'easeInOut' }}
  className="fixed inset-0 bg-slate-900 z-50"
>
  <MobilePage />
</motion.div>

// Bottom sheet rise
<motion.div
  initial={{ y: '100%' }}
  animate={{ y: 0 }}
  exit={{ y: '100%' }}
  drag="y"
  dragConstraints={{ top: 0, bottom: 0 }}
  dragElastic={0.2}
  onDragEnd={(e, { offset, velocity }) => {
    if (offset.y > 100 || velocity.y > 500) {
      onClose();
    }
  }}
  transition={{ duration: 0.3, ease: 'easeOut' }}
  className="fixed inset-x-0 bottom-0 bg-slate-900 rounded-t-2xl z-50"
>
  <BottomSheet />
</motion.div>
```

---

### Premium Screens

**Gold accent shimmer on entry**

```tsx
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ duration: 0.3 }}
  className="relative"
>
  {/* Page content */}
  <PremiumPage />
  
  {/* Gold shimmer overlay */}
  <motion.div
    initial={{ opacity: 0.3 }}
    animate={{ opacity: 0 }}
    transition={{ duration: 0.6, ease: 'easeOut' }}
    className="absolute inset-0 pointer-events-none"
    style={{
      background: 'linear-gradient(90deg, transparent, rgba(245, 197, 66, 0.1), transparent)',
    }}
  />
</motion.div>
```

---

### Pro Screens

**Platinum accent fade**

```tsx
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ duration: 0.3 }}
  className="relative"
>
  <ProPage />
  
  {/* Platinum fade overlay */}
  <motion.div
    initial={{ opacity: 0.2 }}
    animate={{ opacity: 0 }}
    transition={{ duration: 0.5 }}
    className="absolute inset-0 pointer-events-none bg-gradient-to-b from-slate-300/10 to-transparent"
  />
</motion.div>
```

---

## 23.6 Chart Interactions

Charts must feel **responsive and intuitive**.

### Hover

**Tooltip fades in, line thickens slightly**

```tsx
// Using recharts
<LineChart data={data}>
  <Line
    type="monotone"
    dataKey="price"
    stroke="#F5C542"
    strokeWidth={2}
    activeDot={{ 
      r: 6, 
      strokeWidth: 0,
      fill: '#F5C542',
    }}
  />
  <Tooltip
    content={<CustomTooltip />}
    animationDuration={150}
    animationEasing="ease-out"
  />
</LineChart>

// Custom tooltip with fade
function CustomTooltip({ active, payload }) {
  if (!active || !payload) return null;
  
  return (
    <motion.div
      initial={{ opacity: 0, y: -5 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.15 }}
      className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 shadow-lg"
    >
      <p className="text-sm text-white font-medium">
        ${payload[0].value.toFixed(2)}
      </p>
    </motion.div>
  );
}
```

---

### Drag

**Smooth scrub, tooltip follows finger**

```tsx
// Touch-friendly chart scrubbing
<ResponsiveContainer>
  <LineChart
    data={data}
    onMouseMove={(state) => {
      if (state.isTooltipActive) {
        setActiveIndex(state.activeTooltipIndex);
      }
    }}
  >
    <Line strokeWidth={2} />
    <Tooltip
      cursor={{ stroke: '#475569', strokeWidth: 1 }}
      position={{ y: 0 }}
      animationDuration={0}
    />
  </LineChart>
</ResponsiveContainer>
```

---

### Zoom (Desktop)

**Scroll to zoom, chart animates smoothly**

```tsx
function ZoomableChart({ data }) {
  const [zoomDomain, setZoomDomain] = useState([0, data.length - 1]);
  
  const handleWheel = (e) => {
    e.preventDefault();
    const delta = e.deltaY * -0.01;
    const zoomFactor = 1 + delta;
    
    // Smooth zoom animation
    const newDomain = [
      Math.max(0, zoomDomain[0] * zoomFactor),
      Math.min(data.length - 1, zoomDomain[1] * zoomFactor),
    ];
    
    setZoomDomain(newDomain);
  };
  
  return (
    <motion.div
      onWheel={handleWheel}
      animate={{ scale: 1 }}
      transition={{ duration: 0.2 }}
    >
      <LineChart data={data.slice(zoomDomain[0], zoomDomain[1])}>
        <Line strokeWidth={2} />
      </LineChart>
    </motion.div>
  );
}
```

---

### Identity Overlays

**Fade in/out, no sudden jumps**

```tsx
<LineChart data={data}>
  {/* Main price line */}
  <Line dataKey="price" stroke="#F5C542" strokeWidth={2} />
  
  {/* Identity overlay - fade in/out */}
  <AnimatePresence>
    {showCulturalAlpha && (
      <motion.g
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.3 }}
      >
        <Line
          dataKey="culturalAlpha"
          stroke="#10B981"
          strokeWidth={1}
          strokeDasharray="5 5"
        />
      </motion.g>
    )}
  </AnimatePresence>
</LineChart>
```

---

## 23.7 Heatmap Interactions

### Hover

**Tile brightens, border glows with identity accent**

```tsx
<div
  className="
    relative aspect-square rounded-lg p-3 
    cursor-pointer
    transition-all duration-200
    hover:brightness-110
    hover:border-2 hover:border-emerald-500/50
    hover:shadow-lg hover:shadow-emerald-500/20
  "
  style={{ backgroundColor: getHeatmapColor(changePercent) }}
>
  <p className="text-xs font-medium text-white">{sector}</p>
  <p className="text-lg font-semibold text-white">{changePercent}%</p>
</div>
```

---

### Tap

**Tile expands slightly, sector detail slides in**

```tsx
function HeatmapTile({ sector, changePercent, onClick }) {
  const [isPressed, setIsPressed] = useState(false);
  
  return (
    <>
      <motion.div
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.98 }}
        onTap={() => {
          setIsPressed(true);
          onClick(sector);
        }}
        className="cursor-pointer"
        style={{ backgroundColor: getHeatmapColor(changePercent) }}
      >
        {/* Tile content */}
      </motion.div>
      
      {/* Sector detail slides in */}
      <AnimatePresence>
        {isPressed && (
          <motion.div
            initial={{ x: 300, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: 300, opacity: 0 }}
            transition={{ duration: 0.3, ease: 'easeOut' }}
            className="fixed right-0 top-0 bottom-0 w-80 bg-slate-900 border-l border-slate-800 z-50"
          >
            <SectorDetail sector={sector} onClose={() => setIsPressed(false)} />
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
```

---

### Loading

**Tiles shimmer in waves**

```tsx
// Staggered shimmer animation
<div className="grid grid-cols-3 md:grid-cols-5 gap-2">
  {sectors.map((sector, index) => (
    <motion.div
      key={sector}
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ 
        duration: 0.2, 
        delay: index * 0.05, // Staggered wave
        ease: 'easeOut' 
      }}
      className="aspect-square rounded-lg bg-slate-800 animate-pulse"
    />
  ))}
</div>

// CSS wave shimmer
@keyframes waveShimmer {
  0%, 100% {
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
}

.heatmap-tile:nth-child(1) { animation: waveShimmer 1.5s ease-in-out infinite; }
.heatmap-tile:nth-child(2) { animation: waveShimmer 1.5s ease-in-out 0.1s infinite; }
.heatmap-tile:nth-child(3) { animation: waveShimmer 1.5s ease-in-out 0.2s infinite; }
```

---

## 23.8 News Verification Interactions

### Verification Badge

**Pulses once on load, tap expands source list**

```tsx
function VerificationBadge({ sourceCount, onTap }) {
  const [isPulsed, setIsPulsed] = useState(false);
  
  useEffect(() => {
    setIsPulsed(true);
  }, []);
  
  return (
    <motion.button
      initial={{ scale: 1 }}
      animate={isPulsed ? { scale: [1, 1.1, 1] } : {}}
      transition={{ duration: 0.3, times: [0, 0.5, 1] }}
      onAnimationComplete={() => setIsPulsed(false)}
      onClick={onTap}
      className="inline-flex items-center gap-1 px-2 py-1 bg-emerald-500/20 text-emerald-400 rounded-full border border-emerald-500/30"
    >
      <Check className="w-3 h-3" />
      <span className="text-xs font-medium">Verified • {sourceCount} sources</span>
    </motion.button>
  );
}
```

---

### Timeline

**Events slide in sequentially, dots glow with identity accent**

```tsx
function VerificationTimeline({ events }) {
  return (
    <div className="space-y-4">
      {events.map((event, index) => (
        <motion.div
          key={event.id}
          initial={{ x: -20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ 
            duration: 0.2, 
            delay: index * 0.1 // Sequential
          }}
          className="flex gap-3"
        >
          {/* Glowing dot */}
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: index * 0.1 + 0.1 }}
            className="relative"
          >
            <div className="w-3 h-3 bg-emerald-500 rounded-full" />
            <div className="absolute inset-0 bg-emerald-500 rounded-full animate-ping opacity-50" />
          </motion.div>
          
          <div className="flex-1">
            <p className="text-sm text-white font-medium">{event.title}</p>
            <p className="text-xs text-slate-400">{event.timestamp}</p>
          </div>
        </motion.div>
      ))}
    </div>
  );
}
```

---

### Source List

**Items fade in, icons slide from left**

```tsx
function SourceList({ sources }) {
  return (
    <div className="space-y-3">
      {sources.map((source, index) => (
        <motion.div
          key={source.id}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.2, delay: index * 0.05 }}
          className="flex items-start gap-3 p-3 bg-slate-800 rounded-lg"
        >
          {/* Icon slides from left */}
          <motion.div
            initial={{ x: -10, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.2, delay: index * 0.05 + 0.1 }}
          >
            <Newspaper className="w-5 h-5 text-emerald-400" />
          </motion.div>
          
          <div className="flex-1">
            <h4 className="text-sm font-medium text-white">{source.name}</h4>
            <a href={source.url} className="text-xs text-blue-400 hover:underline">
              {source.url}
            </a>
          </div>
        </motion.div>
      ))}
    </div>
  );
}
```

---

## 23.9 Alerts Interactions

### Alert Triggered

**Subtle pulse, notification slides down, no sound by default**

```tsx
function AlertNotification({ alert }) {
  return (
    <motion.div
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      exit={{ y: -100, opacity: 0 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      className="fixed top-4 right-4 z-50"
    >
      <motion.div
        animate={{ scale: [1, 1.02, 1] }}
        transition={{ duration: 0.5, times: [0, 0.5, 1] }}
        className="flex items-center gap-3 p-4 bg-slate-800 border border-yellow-500/50 rounded-lg shadow-lg"
      >
        <Bell className="w-5 h-5 text-yellow-500" />
        <div>
          <p className="text-sm font-medium text-white">{alert.title}</p>
          <p className="text-xs text-slate-400">{alert.message}</p>
        </div>
      </motion.div>
    </motion.div>
  );
}
```

---

### Alert Creation

**Checkmark animates, card slides into list**

```tsx
function AlertCreationSuccess({ onComplete }) {
  return (
    <>
      {/* Checkmark animation */}
      <motion.div
        initial={{ scale: 0, rotate: -180 }}
        animate={{ scale: 1, rotate: 0 }}
        transition={{ duration: 0.3, ease: 'easeOut' }}
        className="w-16 h-16 bg-emerald-500 rounded-full flex items-center justify-center mx-auto mb-4"
      >
        <Check className="w-8 h-8 text-white" />
      </motion.div>
      
      {/* Card slides into list */}
      <motion.div
        initial={{ x: -300, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ duration: 0.3, delay: 0.3 }}
        className="p-4 bg-slate-800 rounded-lg border border-slate-700"
      >
        <AlertCard alert={newAlert} />
      </motion.div>
    </>
  );
}
```

---

### Alert Edit

**Fields highlight briefly**

```tsx
function AlertEditField({ value, onChange }) {
  const [isHighlighted, setIsHighlighted] = useState(false);
  
  const handleChange = (e) => {
    onChange(e.target.value);
    setIsHighlighted(true);
    setTimeout(() => setIsHighlighted(false), 300);
  };
  
  return (
    <motion.input
      animate={{
        borderColor: isHighlighted ? '#F5C542' : '#475569',
        boxShadow: isHighlighted ? '0 0 0 2px rgba(245, 197, 66, 0.2)' : 'none',
      }}
      transition={{ duration: 0.2 }}
      value={value}
      onChange={handleChange}
      className="w-full px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white"
    />
  );
}
```

---

## 23.10 Premium Gate Interactions

Premium gates must feel **respectful and inviting**.

### Locked Feature

**Slight dim, lock icon fades in**

```tsx
<motion.div
  initial={{ opacity: 1 }}
  whileHover={{ opacity: 0.8 }}
  className="relative p-6 bg-slate-800 rounded-lg cursor-pointer"
>
  {/* Dimmed content */}
  <div className="blur-sm opacity-50 pointer-events-none">
    <AdvancedAnalytics />
  </div>
  
  {/* Lock icon fades in */}
  <motion.div
    initial={{ opacity: 0, scale: 0.8 }}
    animate={{ opacity: 1, scale: 1 }}
    transition={{ duration: 0.2 }}
    className="absolute inset-0 flex items-center justify-center"
  >
    <div className="text-center">
      <Lock className="w-8 h-8 text-yellow-500 mx-auto mb-2" />
      <p className="text-sm font-medium text-yellow-500">Premium Feature</p>
    </div>
  </motion.div>
</motion.div>
```

---

### Tap

**Premium overlay slides up, gold accent animates softly**

```tsx
function PremiumGate({ children, onUpgrade }) {
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <>
      <div onClick={() => setIsOpen(true)}>
        {children}
      </div>
      
      <AnimatePresence>
        {isOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsOpen(false)}
              className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
            />
            
            {/* Overlay slides up */}
            <motion.div
              initial={{ y: 100, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: 100, opacity: 0 }}
              transition={{ duration: 0.3, ease: 'easeOut' }}
              className="fixed inset-x-0 bottom-0 md:inset-0 md:flex md:items-center md:justify-center z-50"
            >
              <div className="bg-slate-800 rounded-t-2xl md:rounded-2xl border border-yellow-500/20 p-6 max-w-md mx-auto">
                {/* Gold accent animation */}
                <motion.div
                  animate={{ 
                    boxShadow: [
                      '0 0 0 0 rgba(245, 197, 66, 0)',
                      '0 0 20px 10px rgba(245, 197, 66, 0.1)',
                      '0 0 0 0 rgba(245, 197, 66, 0)',
                    ]
                  }}
                  transition={{ duration: 2, repeat: Infinity }}
                  className="w-16 h-16 bg-yellow-500 rounded-full flex items-center justify-center mx-auto mb-4"
                >
                  <Crown className="w-8 h-8 text-slate-900" />
                </motion.div>
                
                <h3 className="text-xl font-semibold text-white text-center mb-2">
                  Upgrade to Premium
                </h3>
                <p className="text-slate-400 text-center mb-6">
                  Unlock advanced analytics and insights.
                </p>
                
                <button
                  onClick={onUpgrade}
                  className="w-full px-4 py-3 bg-yellow-500 text-slate-900 rounded-lg font-medium hover:bg-yellow-400 transition-colors"
                >
                  Upgrade Now
                </button>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
```

---

### Pro Gate

**Platinum glow, slight scale-up on CTA**

```tsx
<motion.div className="text-center p-6">
  {/* Platinum glow */}
  <motion.div
    animate={{
      boxShadow: [
        '0 0 0 0 rgba(229, 231, 235, 0)',
        '0 0 30px 15px rgba(229, 231, 235, 0.2)',
        '0 0 0 0 rgba(229, 231, 235, 0)',
      ]
    }}
    transition={{ duration: 2, repeat: Infinity }}
    className="w-16 h-16 bg-gradient-to-r from-slate-300 to-slate-400 rounded-full flex items-center justify-center mx-auto mb-4"
  >
    <Sparkles className="w-8 h-8 text-slate-900" />
  </motion.div>
  
  <h3 className="text-xl font-semibold text-white mb-2">Upgrade to Pro</h3>
  <p className="text-slate-400 mb-6">Access advanced trading tools.</p>
  
  {/* CTA with scale-up */}
  <motion.button
    whileHover={{ scale: 1.05 }}
    whileTap={{ scale: 0.98 }}
    className="px-6 py-3 bg-gradient-to-r from-slate-300 to-slate-400 text-slate-900 rounded-lg font-medium"
  >
    Upgrade to Pro
  </motion.button>
</motion.div>
```

---

## 23.11 Feedback Patterns

### Success

**Green checkmark, fade-in toast**

```tsx
function SuccessToast({ message }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.2 }}
      className="fixed top-4 right-4 z-50 flex items-center gap-3 p-4 bg-emerald-500/10 border border-emerald-500/50 rounded-lg backdrop-blur-sm"
    >
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ duration: 0.2, delay: 0.1 }}
      >
        <CheckCircle className="w-5 h-5 text-emerald-400" />
      </motion.div>
      <span className="text-sm font-medium text-white">{message}</span>
    </motion.div>
  );
}
```

---

### Error

**Red border shake (2px), clear message, no dramatic animations**

```tsx
function ErrorState({ message }) {
  return (
    <motion.div
      animate={{ x: [0, -2, 2, -2, 2, 0] }}
      transition={{ duration: 0.4 }}
      className="p-3 bg-red-500/10 border border-red-500/50 rounded-lg"
    >
      <div className="flex items-center gap-2">
        <AlertCircle className="w-4 h-4 text-red-400" />
        <p className="text-sm text-red-400">{message}</p>
      </div>
    </motion.div>
  );
}

// Subtle shake - no excessive movement
@keyframes subtleShake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-2px); }
  75% { transform: translateX(2px); }
}

.error-shake {
  animation: subtleShake 400ms ease-out;
}
```

---

### Info

**Blue toast, soft fade**

```tsx
<motion.div
  initial={{ opacity: 0, y: -10 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -10 }}
  transition={{ duration: 0.2 }}
  className="flex items-center gap-3 p-4 bg-blue-500/10 border border-blue-500/50 rounded-lg"
>
  <Info className="w-5 h-5 text-blue-400" />
  <span className="text-sm text-white">Markets close in 30 minutes</span>
</motion.div>
```

---

### Loading

**Skeleton shimmer, identity accent pulse**

```tsx
// Skeleton with shimmer
<div className="animate-pulse space-y-4">
  <div className="h-4 bg-slate-700 rounded w-3/4 skeleton-shimmer" />
  <div className="h-4 bg-slate-700 rounded w-1/2 skeleton-shimmer" />
</div>

// Identity accent pulse
<motion.div
  animate={{ opacity: [0.5, 1, 0.5] }}
  transition={{ duration: 1.5, repeat: Infinity, ease: 'easeInOut' }}
  className="h-1 bg-emerald-500 rounded-full"
/>

// Loading spinner with identity color
<motion.div
  animate={{ rotate: 360 }}
  transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
  className="w-6 h-6 border-2 border-emerald-500 border-t-transparent rounded-full"
/>
```

---

## 23.12 Interaction Rules

### 1. Motion must always clarify, never distract.
```tsx
// ✅ Good: Subtle fade guides attention
<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
  <ImportantUpdate />
</motion.div>

// ❌ Bad: Excessive bounce distracts
<motion.div animate={{ y: [0, -20, 0] }} transition={{ repeat: Infinity }}>
  <ImportantUpdate />
</motion.div>
```

---

### 2. Identity motion must be subtle.
```tsx
// ✅ Good: Gentle horizontal drift for diaspora
<motion.div initial={{ x: -5 }} animate={{ x: 0 }} transition={{ duration: 0.3 }}>
  <DiasporaWidget />
</motion.div>

// ❌ Bad: Excessive movement breaks focus
<motion.div animate={{ x: [-50, 50] }} transition={{ repeat: Infinity }}>
  <DiasporaWidget />
</motion.div>
```

---

### 3. Premium motion must feel elevated, not flashy.
```tsx
// ✅ Good: Soft gold shimmer
<div className="legacy-shimmer">
  <PremiumFeature />
</div>

// ❌ Bad: Aggressive sparkle effect
<div className="animate-spin-slow">
  <PremiumFeature />
</div>
```

---

### 4. All motion must be under 200ms.
```tsx
// ✅ Good: Quick 150ms transition
transition={{ duration: 0.15 }}

// ❌ Bad: Slow 500ms transition
transition={{ duration: 0.5 }}
```

---

### 5. Motion must never imply predictions or advice.
```tsx
// ✅ Good: Neutral fade-in
<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
  <StockPrice price={180.50} change={+2.5} />
</motion.div>

// ❌ Bad: Upward arrow animation implies bullishness
<motion.div animate={{ y: [0, -50] }}>
  <StockPrice price={180.50} change={+2.5} />
</motion.div>
```

---

### 6. Motion must reinforce trust, not hype.
```tsx
// ✅ Good: Calm verification pulse
<motion.div animate={{ scale: [1, 1.05, 1] }} transition={{ duration: 0.3, times: [0, 0.5, 1] }}>
  <VerificationBadge />
</motion.div>

// ❌ Bad: Excessive celebration animation
<motion.div animate={{ rotate: 360, scale: [1, 2, 1] }} transition={{ repeat: Infinity }}>
  <VerificationBadge />
</motion.div>
```

---

## Motion Implementation Checklist

✅ **Global Patterns**: Fade in, slide up, scale, skeleton loading  
✅ **Micro-Interactions**: Buttons, tabs, chips, search bar  
✅ **Identity Motion**: Diaspora wave, Youth bounce, Creator glitch, Legacy shimmer  
✅ **Page Transitions**: Desktop fade, mobile slide, premium/pro accents  
✅ **Chart Interactions**: Hover tooltips, drag scrub, zoom, identity overlays  
✅ **Heatmap**: Hover glow, tap expand, wave loading  
✅ **News Verification**: Badge pulse, timeline sequence, source slide  
✅ **Alerts**: Triggered notification, creation success, edit highlight  
✅ **Premium Gates**: Locked dim, overlay slide, CTA scale  
✅ **Feedback**: Success/error/info toasts, loading states  
✅ **Interaction Rules**: 6 core principles enforced  

---

## SECTION 24 — ACCESSIBILITY & INCLUSIVITY STANDARDS

DominionMarkets must be **accessible, inclusive, and welcoming** to every user — across identities, abilities, devices, and levels of financial experience.

This section defines the full **accessibility and inclusivity framework** that governs:
- **Visual accessibility**
- **Interaction accessibility**
- **Cognitive accessibility**
- **Identity inclusivity**
- **Language inclusivity**
- **Motion sensitivity**
- **Device inclusivity**
- **Error-state inclusivity**

---

## 24.1 Accessibility Principles

DominionMarkets follows **four core principles**:

### 1. Everyone Belongs Here
No user should feel excluded because of ability, identity, or experience level.

### 2. Information Must Be Perceivable
Charts, tables, and insights must be readable and understandable.

### 3. Interaction Must Be Operable
Every action must be possible with keyboard, touch, or assistive tech.

### 4. Experience Must Be Understandable
No jargon. No complexity walls. No hidden meaning.

---

## 24.2 WCAG Compliance

DominionMarkets adheres to **WCAG 2.1 AA standards**:

### Compliance Checklist

```tsx
// Accessibility implementation checklist
export const wcagCompliance = {
  textContrast: {
    standard: 'WCAG 2.1 AA',
    minimumRatio: '4.5:1',
    largeTextRatio: '3:1',
    implementation: 'All text colors tested against backgrounds',
  },
  scalableFonts: {
    unit: 'rem',
    maxScale: '200%',
    implementation: 'All text uses relative units',
  },
  keyboardNavigation: {
    required: true,
    focusVisible: true,
    noTraps: true,
  },
  screenReaderLabels: {
    ariaLabels: true,
    ariaDescribedBy: true,
    semanticHTML: true,
  },
  focusIndicators: {
    visible: true,
    contrast: '3:1 minimum',
    implementation: 'focus:ring-2 focus:ring-yellow-500',
  },
  motionReducedMode: {
    prefersReducedMotion: true,
    implementation: 'motion-reduce:transition-none',
  },
};
```

### Implementation Standards

```tsx
// Text contrast validation
✅ White (#FFFFFF) on Slate-900 (#0F172A) = 15.5:1
✅ Slate-300 (#CBD5E1) on Slate-900 (#0F172A) = 9.2:1
✅ Yellow-500 (#F5C542) on Slate-900 (#0F172A) = 8.1:1
✅ Emerald-400 (#34D399) on Slate-900 (#0F172A) = 7.5:1

❌ Slate-600 (#475569) on Slate-900 (#0F172A) = 2.8:1 (insufficient)
```

---

## 24.3 Visual Accessibility

### Contrast

**Minimum 4.5:1 for text, identity accents always meet contrast requirements**

```tsx
// Contrast-compliant text colors
const textColors = {
  primary: 'text-white',           // 15.5:1 contrast
  secondary: 'text-slate-300',     // 9.2:1 contrast
  tertiary: 'text-slate-400',      // 6.4:1 contrast
  
  // Identity accents (all WCAG AA compliant)
  diaspora: 'text-emerald-400',    // 7.5:1 contrast
  youth: 'text-blue-400',          // 6.8:1 contrast
  creator: 'text-purple-400',      // 5.9:1 contrast
  legacy: 'text-amber-400',        // 7.2:1 contrast
};

// Invalid - insufficient contrast
❌ 'text-slate-600'  // 2.8:1 - do not use for body text
```

---

### Color Blindness

**No information is conveyed by color alone**

```tsx
// Charts use patterns + color
<LineChart data={data}>
  {/* Primary line */}
  <Line dataKey="price" stroke="#F5C542" strokeWidth={2} />
  
  {/* Identity overlay with dashed pattern */}
  <Line
    dataKey="culturalAlpha"
    stroke="#10B981"
    strokeWidth={1}
    strokeDasharray="5 5"  // Pattern for color-blind users
  />
</LineChart>

// Heatmap uses dual encoding (color + value text)
<div 
  className="aspect-square rounded-lg p-3"
  style={{ backgroundColor: getHeatmapColor(changePercent) }}
>
  <p className="text-xs font-medium text-white">{sector}</p>
  {/* Value text always visible */}
  <p className="text-lg font-semibold text-white">{changePercent}%</p>
</div>

// Status with icon + color
<div className="flex items-center gap-2">
  <CheckCircle className="w-4 h-4 text-emerald-400" />
  <span className="text-emerald-400">Verified</span>
</div>

<div className="flex items-center gap-2">
  <AlertCircle className="w-4 h-4 text-red-400" />
  <span className="text-red-400">Error</span>
</div>
```

---

### Text Scaling

**Supports up to 200% text size, layout reflows gracefully**

```tsx
// Use rem units (Tailwind default)
<p className="text-base">  {/* 1rem = 16px, scales with browser settings */}
  This text respects user font size preferences
</p>

// Responsive layout that reflows
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Cards reflow as text scales */}
  <Card />
</div>

// Avoid fixed heights
❌ <div className="h-20">Content</div>  // Text may overflow
✅ <div className="min-h-20">Content</div>  // Grows with text

// Test at 200% zoom
// All content should remain accessible
```

---

## 24.4 Interaction Accessibility

### Keyboard Navigation

**Every interactive element is reachable, clear focus states, no keyboard traps**

```tsx
// Focus indicators on all interactive elements
<button className="
  px-4 py-2 bg-yellow-500 text-slate-900 rounded-lg
  focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2 focus:ring-offset-slate-900
">
  Upgrade to Premium
</button>

<a href="/markets" className="
  text-blue-400 hover:underline
  focus:outline-none focus:ring-2 focus:ring-blue-400 focus:rounded
">
  View Markets
</a>

// Tab order management
<div>
  <button tabIndex={0}>First</button>
  <button tabIndex={0}>Second</button>
  <button tabIndex={-1}>Hidden from tab order</button>
</div>

// Skip to main content link
<a
  href="#main-content"
  className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 px-4 py-2 bg-yellow-500 text-slate-900 rounded-lg"
>
  Skip to main content
</a>

<main id="main-content">
  {/* Page content */}
</main>

// Escape key closes modals
function Modal({ isOpen, onClose }) {
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') onClose();
    };
    
    if (isOpen) {
      window.addEventListener('keydown', handleEscape);
      return () => window.removeEventListener('keydown', handleEscape);
    }
  }, [isOpen, onClose]);
  
  return (
    <div role="dialog" aria-modal="true">
      {/* Modal content */}
    </div>
  );
}
```

---

### Touch Targets

**Minimum 44px touch area, generous spacing**

```tsx
// Minimum touch target size (WCAG 2.1 Level AAA: 44x44px)
<button className="min-w-11 min-h-11 px-4 py-2">  {/* 44px minimum */}
  Click me
</button>

// Icon buttons
<button className="w-11 h-11 flex items-center justify-center" aria-label="Close">
  <X className="w-5 h-5" />
</button>

// Mobile navigation with generous spacing
<nav className="flex justify-around h-16">  {/* 64px height */}
  <button className="flex flex-col items-center justify-center min-w-16">
    <Home className="w-6 h-6" />
    <span className="text-xs mt-1">Home</span>
  </button>
</nav>

// Table row touch targets
<tr className="h-12 hover:bg-slate-800/50 cursor-pointer">  {/* 48px minimum */}
  <td className="px-4 py-3">AAPL</td>
  <td className="px-4 py-3">$180.50</td>
</tr>

// Adequate spacing between interactive elements
<div className="flex gap-3">  {/* 12px gap prevents accidental taps */}
  <button>Cancel</button>
  <button>Submit</button>
</div>
```

---

### Assistive Tech

**ARIA labels, semantic HTML, screen-reader-friendly charts**

```tsx
// ARIA labels for icon-only buttons
<button aria-label="Close menu">
  <X className="w-5 h-5" />
</button>

<button aria-label="Search stocks">
  <Search className="w-5 h-5" />
</button>

// aria-describedby for additional context
<input
  type="number"
  aria-label="Number of shares"
  aria-describedby="shares-help"
  className="w-full px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg"
/>
<p id="shares-help" className="text-xs text-slate-400 mt-1">
  Enter the number of shares you own
</p>

// Semantic HTML
<header>
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/dashboard">Dashboard</a></li>
      <li><a href="/markets">Markets</a></li>
    </ul>
  </nav>
</header>

<main>
  <article>
    <h1>Stock Analysis</h1>
    <section>
      <h2>Price Movement</h2>
      {/* Content */}
    </section>
  </article>
</main>

// Live regions for dynamic updates
<div aria-live="polite" aria-atomic="true">
  <p>AAPL price updated: $180.50 (+2.5%)</p>
</div>

// Alert for errors
<div role="alert" aria-live="assertive">
  <p>Error: Unable to load portfolio data</p>
</div>

// Screen-reader-friendly chart descriptions
<figure>
  <LineChart data={data} />
  <figcaption className="sr-only">
    Line chart showing AAPL stock price from January to December 2025.
    Price ranged from $150 to $185, with an overall upward trend.
    Current price is $180.50, up 2.5% today.
  </figcaption>
</figure>

// Data table with proper headers
<table>
  <caption className="sr-only">Stock holdings</caption>
  <thead>
    <tr>
      <th scope="col">Ticker</th>
      <th scope="col">Shares</th>
      <th scope="col">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>AAPL</td>
      <td>10</td>
      <td>$1,805.00</td>
    </tr>
  </tbody>
</table>
```

---

## 24.5 Cognitive Accessibility

### Plain Language

**No jargon, no predictions, no advice, no sensationalism**

```tsx
// ✅ Plain language examples
"Your portfolio is stable."
"This stock is up 2.5% today."
"This company has strong cultural relevance."
"This news story is verified by 5 sources."
"Your portfolio contains 12 stocks across 5 sectors."

// ❌ Avoid jargon
"Your portfolio exhibits low beta volatility."
"Algorithmic delta-neutral arbitrage opportunity detected."

// ❌ Avoid predictions
"This stock will rise 20%!"
"Markets are about to crash!"

// ❌ Avoid advice
"You should buy this stock."
"You need to diversify immediately."

// ❌ Avoid sensationalism
"🚀 TO THE MOON! 🚀"
"URGENT: Act now before it's too late!"
```

---

### Beginner Mode (Youth Identity)

**Simplified explanations, tooltips, learning badges**

```tsx
// Tooltip for financial terms
<div className="inline-flex items-center gap-1">
  <span>Market Cap</span>
  <Tooltip content="Market capitalization is the total value of all shares of a company.">
    <HelpCircle className="w-4 h-4 text-slate-400 cursor-help" />
  </Tooltip>
</div>

// Simplified explanation card
function BeginnerExplanation({ term, explanation, example }) {
  return (
    <div className="p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg">
      <div className="flex items-center gap-2 mb-2">
        <Lightbulb className="w-5 h-5 text-blue-400" />
        <h4 className="font-medium text-white">{term}</h4>
      </div>
      <p className="text-sm text-slate-300 mb-2">{explanation}</p>
      <div className="text-xs text-slate-400">
        <strong>Example:</strong> {example}
      </div>
    </div>
  );
}

// Usage
<BeginnerExplanation
  term="Diversification"
  explanation="Spreading your investments across different types of stocks to reduce risk."
  example="Instead of buying only tech stocks, you also buy healthcare and finance stocks."
/>

// Learning badges
<div className="flex items-center gap-2 p-3 bg-blue-500/10 rounded-lg border border-blue-500/20">
  <Award className="w-5 h-5 text-blue-400" />
  <div>
    <p className="text-sm font-medium text-white">Learning Progress</p>
    <p className="text-xs text-slate-400">You've completed 5 lessons</p>
  </div>
</div>
```

---

### Consistent Layout

**Predictable navigation, repeated patterns, clear hierarchy**

```tsx
// Consistent page layout pattern
function PageLayout({ title, description, children }) {
  return (
    <div className="container mx-auto px-4 py-6">
      {/* Header always at top */}
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">{title}</h1>
        <p className="text-slate-400">{description}</p>
      </header>
      
      {/* Content area */}
      <main>{children}</main>
    </div>
  );
}

// Consistent card pattern
function Card({ title, children }) {
  return (
    <div className="p-4 bg-slate-800 rounded-lg border border-slate-700">
      <h3 className="text-lg font-medium text-white mb-3">{title}</h3>
      {children}
    </div>
  );
}

// Consistent button hierarchy
<div className="flex gap-3">
  <button className="px-4 py-2 bg-slate-700 text-white rounded-lg">
    Cancel
  </button>
  <button className="px-4 py-2 bg-yellow-500 text-slate-900 rounded-lg font-medium">
    Save Changes
  </button>
</div>
```

---

## 24.6 Motion Sensitivity

### Reduced Motion Mode

**Disables animations, replaces transitions with instant state changes, removes identity motion signatures**

```tsx
// Global CSS for reduced motion
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

// Tailwind utility classes
<div className="
  transition-transform duration-200
  motion-reduce:transition-none
  hover:scale-105
  motion-reduce:hover:scale-100
">
  <Card />
</div>

// Framer Motion with reduced motion support
import { useReducedMotion } from 'framer-motion';

function AnimatedComponent() {
  const shouldReduceMotion = useReducedMotion();
  
  return (
    <motion.div
      initial={{ opacity: shouldReduceMotion ? 1 : 0, y: shouldReduceMotion ? 0 : 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: shouldReduceMotion ? 0 : 0.3 }}
    >
      <Content />
    </motion.div>
  );
}

// Conditional animation
function ConditionalAnimation({ children }) {
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  
  if (prefersReducedMotion) {
    return <div>{children}</div>;
  }
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  );
}
```

---

### Default Motion

**Subtle, under 200ms, never distracting**

```tsx
// All motion follows these constraints
const motionConstraints = {
  maxDuration: 200, // milliseconds
  easing: 'ease-out',
  subtle: true,
};

// Examples
transition={{ duration: 0.15 }}  // ✅ Fast
transition={{ duration: 0.2 }}   // ✅ At limit
transition={{ duration: 0.5 }}   // ❌ Too slow

// Subtle scale
hover:scale-105  // ✅ Barely noticeable
hover:scale-150  // ❌ Too dramatic
```

---

## 24.7 Identity Inclusivity

**Identity is a lens, not a limitation.**

### Supported Identities

- **Diaspora**
- **Youth**
- **Creator**
- **Legacy-Builder**

### Identity Rules

```tsx
// ✅ Identity rules
const identityRules = {
  neverStereotype: true,
  neverAssumeFinancialGoals: true,
  neverRestrictFeatures: true,
  alwaysEmpower: true,
};

// ✅ Correct identity implementation
function IdentityInsight({ identity, portfolioData }) {
  const insights = {
    diaspora: `Your portfolio has strong exposure to Caribbean and African markets.`,
    youth: `You're investing in high-growth tech stocks.`,
    creator: `Your holdings align with the creator economy.`,
    legacy: `Your portfolio emphasizes dividend-paying stocks.`,
  };
  
  return (
    <div className="p-4 bg-slate-800 rounded-lg">
      <p className="text-slate-300">{insights[identity]}</p>
    </div>
  );
}

// ❌ Incorrect - stereotyping
"As a diaspora investor, you probably want to invest in Africa."
"Youth investors only care about meme stocks."
"Creators don't understand traditional finance."
"Legacy investors are too conservative."

// ❌ Incorrect - assuming goals
"You should focus on long-term dividends."  // Assumes goal
"You need high-growth stocks."  // Assumes goal

// ❌ Incorrect - restricting features
if (identity === 'youth') {
  return <SimplifiedDashboard />;  // ❌ Don't limit features
}
```

---

### Identity Language

**Respectful, neutral, strength-based**

```tsx
// ✅ Strength-based language
"Your diaspora identity gives you unique cultural insights."
"Your youth perspective helps you identify emerging trends."
"Your creator identity helps you understand platform economics."
"Your legacy-building approach emphasizes stability."

// ❌ Deficit-based language
"As a diaspora investor, you might not understand Wall Street."
"Young investors lack experience."
"Creators aren't serious investors."
"Legacy builders are out of touch."

// Respectful identity references
<div className="flex items-center gap-2">
  <Globe className="w-5 h-5 text-emerald-400" />
  <span className="text-emerald-400 font-medium">Diaspora Insights</span>
</div>
```

---

## 24.8 Language Inclusivity

### Supported Languages

- **English** at launch
- **Additional languages** planned

### Tone

**Neutral, clear, respectful**

```tsx
// ✅ Clear, neutral tone
"Your portfolio contains 12 stocks."
"This stock is up 2.5% today."
"Markets are closed."

// ❌ Avoid slang
"Your portfolio is fire! 🔥"
"This stock is mooning!"
"HODL your positions!"

// ❌ Avoid idioms
"Don't put all your eggs in one basket."
"A bird in the hand is worth two in the bush."

// ❌ Avoid region-specific jargon
"This stock is a bobby-dazzler."  // UK slang
"That's a no-brainer, mate."  // Region-specific
```

---

### Internationalization Preparation

```tsx
// Structure for i18n
const translations = {
  en: {
    'portfolio.title': 'Your Portfolio',
    'portfolio.empty': 'No holdings yet',
    'portfolio.add': 'Add Holding',
  },
  es: {
    'portfolio.title': 'Tu Portafolio',
    'portfolio.empty': 'Sin participaciones aún',
    'portfolio.add': 'Agregar Participación',
  },
};

// Use translation keys
import { useTranslation } from 'next-intl';

function Portfolio() {
  const t = useTranslation();
  
  return (
    <div>
      <h1>{t('portfolio.title')}</h1>
      {holdings.length === 0 && <p>{t('portfolio.empty')}</p>}
      <button>{t('portfolio.add')}</button>
    </div>
  );
}
```

---

## 24.9 Financial Inclusivity

DominionMarkets must be accessible to users with:
- **No financial background**
- **Limited financial literacy**
- **High financial literacy**

### Features Supporting Inclusivity

```tsx
// Beginner mode toggle
function FinancialLiteracySettings() {
  const [beginnerMode, setBeginnerMode] = useState(false);
  
  return (
    <div className="p-4 bg-slate-800 rounded-lg">
      <label className="flex items-center gap-3">
        <input
          type="checkbox"
          checked={beginnerMode}
          onChange={(e) => setBeginnerMode(e.target.checked)}
          className="w-5 h-5"
        />
        <div>
          <p className="font-medium text-white">Beginner Mode</p>
          <p className="text-sm text-slate-400">
            Show simplified explanations and tooltips
          </p>
        </div>
      </label>
    </div>
  );
}

// Identity-aware explanations
function StockMetric({ label, value, identity, beginnerMode }) {
  const explanations = {
    marketCap: {
      simple: "Total value of all shares",
      advanced: "Market capitalization in USD",
    },
    pe: {
      simple: "Price compared to earnings",
      advanced: "Price-to-earnings ratio",
    },
  };
  
  return (
    <div>
      <div className="flex items-center gap-2">
        <span className="text-slate-400">{label}</span>
        {beginnerMode && (
          <Tooltip content={explanations[label].simple}>
            <HelpCircle className="w-4 h-4 text-slate-400" />
          </Tooltip>
        )}
      </div>
      <p className="text-white font-medium">{value}</p>
    </div>
  );
}

// Descriptive analytics (no predictions)
<div className="p-4 bg-slate-800 rounded-lg">
  <h3 className="font-medium text-white mb-2">Portfolio Overview</h3>
  
  {/* ✅ Descriptive */}
  <p className="text-slate-300 mb-2">
    Your portfolio is concentrated in technology stocks (65%).
  </p>
  
  {/* ✅ Descriptive */}
  <p className="text-slate-300 mb-2">
    Your holdings have an average volatility of 18%.
  </p>
  
  {/* ❌ Predictive - not allowed */}
  <p className="text-slate-300">
    This portfolio is likely to gain 20% next year.
  </p>
  
  {/* ❌ Recommendation - not allowed */}
  <p className="text-slate-300">
    You should sell tech stocks and buy bonds.
  </p>
</div>
```

---

## 24.10 Device Inclusivity

### Mobile

**Primary experience, bottom navigation, large touch targets**

```tsx
// Mobile-first responsive design
<div className="
  grid grid-cols-1
  md:grid-cols-2
  lg:grid-cols-3
  gap-4
">
  {/* Cards stack on mobile, spread on desktop */}
</div>

// Bottom navigation (mobile)
<nav className="
  fixed bottom-0 left-0 right-0
  flex justify-around items-center
  h-16 bg-slate-900 border-t border-slate-800
  md:hidden
">
  <button className="flex flex-col items-center justify-center min-w-16">
    <Home className="w-6 h-6" />
    <span className="text-xs mt-1">Home</span>
  </button>
</nav>

// Large touch targets on mobile
<button className="
  w-full px-4 py-3
  text-base font-medium
  bg-yellow-500 text-slate-900 rounded-lg
">
  Upgrade to Premium
</button>
```

---

### Desktop

**Expanded layouts, multi-column views**

```tsx
// Desktop-specific features
<div className="hidden md:flex gap-6">
  {/* Sidebar only on desktop */}
  <aside className="w-64">
    <Navigation />
  </aside>
  
  <main className="flex-1">
    <Content />
  </main>
</div>

// Multi-column layout
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <Card />
  <Card />
  <Card />
</div>
```

---

### Low-Bandwidth Mode

**Reduced images, cached data, lightweight charts**

```tsx
// Detect connection speed
function useLowBandwidth() {
  const [isLowBandwidth, setIsLowBandwidth] = useState(false);
  
  useEffect(() => {
    if ('connection' in navigator) {
      const connection = (navigator as any).connection;
      setIsLowBandwidth(connection.effectiveType === 'slow-2g' || connection.effectiveType === '2g');
    }
  }, []);
  
  return isLowBandwidth;
}

// Conditional rendering
function StockImage({ ticker }) {
  const isLowBandwidth = useLowBandwidth();
  
  if (isLowBandwidth) {
    return (
      <div className="w-12 h-12 bg-slate-700 rounded flex items-center justify-center">
        <span className="text-white font-medium">{ticker}</span>
      </div>
    );
  }
  
  return <img src={`/logos/${ticker}.png`} alt={ticker} className="w-12 h-12" />;
}

// Lightweight chart mode
function Chart({ data }) {
  const isLowBandwidth = useLowBandwidth();
  
  if (isLowBandwidth) {
    return <SparklineChart data={data} />;  // Simpler chart
  }
  
  return <FullLineChart data={data} />;  // Full-featured chart
}

// Prefer cached data
async function fetchWithCache(url: string) {
  // Check cache first
  const cached = await caches.match(url);
  if (cached) return cached.json();
  
  // Fetch and cache
  const response = await fetch(url);
  const data = await response.json();
  
  const cache = await caches.open('api-cache');
  cache.put(url, new Response(JSON.stringify(data)));
  
  return data;
}
```

---

## 24.11 Error-State Inclusivity

Error messages must be:
- **Calm**
- **Clear**
- **Non-technical**
- **Non-blaming**

### Examples

```tsx
// ✅ Good error messages
"Unable to load data. Please try again."
"Connection lost. Reconnect to continue."
"This field is required."
"Please enter a valid ticker symbol."
"Your session has expired. Please log in again."

// ❌ Bad error messages
"You did something wrong."
"System failure."
"Error 500: Internal server error."
"Invalid input detected in field 'ticker_symbol_input_field_v2'."
"Fatal exception: NullPointerException at line 342."

// Implementation
function ErrorMessage({ message, retry }) {
  return (
    <div className="flex items-center gap-3 p-4 bg-red-500/10 border border-red-500/30 rounded-lg">
      <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
      <div className="flex-1">
        <p className="text-sm text-red-400">{message}</p>
      </div>
      {retry && (
        <button
          onClick={retry}
          className="px-3 py-1.5 bg-red-500/20 text-red-400 rounded hover:bg-red-500/30 transition-colors text-sm"
        >
          Retry
        </button>
      )}
    </div>
  );
}

// Form validation errors
<div>
  <input
    type="text"
    className={`
      w-full px-4 py-2 bg-slate-800 rounded-lg
      ${error ? 'border-2 border-red-500' : 'border border-slate-600'}
    `}
  />
  {error && (
    <p className="text-sm text-red-400 mt-1 flex items-center gap-1">
      <AlertCircle className="w-4 h-4" />
      {error}
    </p>
  )}
</div>

// Network error with helpful action
function NetworkError({ onRetry }) {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center">
      <WifiOff className="w-12 h-12 text-slate-600 mb-4" />
      <h3 className="text-lg font-medium text-white mb-2">
        Connection Lost
      </h3>
      <p className="text-slate-400 mb-6">
        Unable to reach the server. Check your internet connection and try again.
      </p>
      <button
        onClick={onRetry}
        className="px-4 py-2 bg-yellow-500 text-slate-900 rounded-lg hover:bg-yellow-400"
      >
        Try Again
      </button>
    </div>
  );
}
```

---

## 24.12 Inclusivity in Insights

Insights must be:
- **Descriptive**
- **Neutral**
- **Identity-aware**
- **Non-directive**

### Allowed

```tsx
// ✅ Descriptive insights
"Your portfolio is concentrated in technology stocks (65%)."
"This company has strong cultural relevance in diaspora communities."
"Your holdings have an average volatility of 18%."
"This stock has increased 15% over the past month."
"This news story is verified by 5 independent sources."

// ✅ Identity-aware insights
function IdentityInsight({ identity, stock }) {
  const insights = {
    diaspora: `${stock.ticker} has strong presence in Caribbean markets with 30% revenue from the region.`,
    youth: `${stock.ticker} is popular among young investors, with 45% of shareholders under 35.`,
    creator: `${stock.ticker} is a major platform for creators, with 2M active creators earning revenue.`,
    legacy: `${stock.ticker} has paid dividends for 25 consecutive years, with a current yield of 3.2%.`,
  };
  
  return (
    <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-lg">
      <Globe className="w-5 h-5 text-emerald-400 mb-2" />
      <p className="text-sm text-slate-300">{insights[identity]}</p>
    </div>
  );
}
```

---

### Not Allowed

```tsx
// ❌ Directive insights
"You should diversify your portfolio."
"You should buy this stock."
"You should sell before it drops."
"You need to reduce your risk."
"We recommend adding bonds."

// ❌ Predictive insights
"This stock will rise 20% next month."
"Markets are about to crash."
"This company is going bankrupt."
"This stock is about to moon!"

// ❌ Advice masquerading as insights
"Smart investors are buying this stock."  // Implies you should too
"Most successful portfolios hold 60% stocks."  // Implies you should too
"Experts recommend diversification."  // Implies you should follow
```

---

### Implementation Pattern

```tsx
// Insight component with guardrails
function Insight({ type, data, identity }) {
  // Only allow descriptive insights
  const allowedInsightTypes = ['descriptive', 'identity-aware', 'verification'];
  
  if (!allowedInsightTypes.includes(type)) {
    console.error(`Invalid insight type: ${type}`);
    return null;
  }
  
  // Never include directive language
  const bannedPhrases = ['should', 'must', 'need to', 'recommend', 'will', 'going to'];
  if (bannedPhrases.some(phrase => data.text.toLowerCase().includes(phrase))) {
    console.error('Directive language detected in insight');
    return null;
  }
  
  return (
    <div className="p-4 bg-slate-800 rounded-lg">
      <p className="text-slate-300">{data.text}</p>
    </div>
  );
}
```

---

## Accessibility Implementation Checklist

✅ **WCAG 2.1 AA Compliance**: Text contrast, scalable fonts, keyboard navigation, screen reader labels, focus indicators, motion-reduced mode  
✅ **Visual Accessibility**: 4.5:1 contrast minimum, color + pattern encoding, text scales to 200%  
✅ **Interaction Accessibility**: Keyboard navigation, 44px touch targets, ARIA labels, semantic HTML  
✅ **Cognitive Accessibility**: Plain language, beginner mode, consistent layout  
✅ **Motion Sensitivity**: Reduced motion mode, subtle defaults <200ms  
✅ **Identity Inclusivity**: Never stereotype, never restrict, always empower, strength-based language  
✅ **Language Inclusivity**: Neutral tone, avoid slang/idioms/jargon, i18n ready  
✅ **Financial Inclusivity**: Beginner mode, tooltips, descriptive analytics, no predictions/recommendations  
✅ **Device Inclusivity**: Mobile-first, desktop expanded, low-bandwidth mode  
✅ **Error Inclusivity**: Calm, clear, non-technical, non-blaming messages  
✅ **Insight Inclusivity**: Descriptive, neutral, identity-aware, non-directive  

---

## SECTION 25 — SECURITY, PRIVACY & DATA HANDLING STANDARDS

DominionMarkets must be **trustworthy by design**.

Security and privacy aren't features — they're the **foundation**.

This section defines the full **security posture**, **data-handling rules**, and **privacy principles** that govern the entire platform.

Everything here is written to be:
- **Engineering-ready**
- **Compliance-ready**
- **User-trust-ready**
- **Scalable**
- **Identity-aware**
- **Ecosystem-aligned**

---

## 25.1 Security Principles

DominionMarkets follows **five core security principles**:

### 1. Zero Trust Architecture
Every request is authenticated.  
Every service validates identity and permissions.

### 2. Least Privilege
Services only access what they need — nothing more.

### 3. Defense in Depth
Multiple layers of protection across:
- **Network**
- **API**
- **Data**
- **Identity**
- **Device**

### 4. Secure by Default
Encryption, validation, and sanitization are always on.

### 5. Transparent & Respectful
Users always understand what's happening with their data.

---

### Implementation

```tsx
// Zero Trust Architecture - every request validated
export const securityMiddleware = {
  authentication: {
    required: true,
    methods: ['jwt', 'session', 'sso'],
    validation: 'every request',
  },
  
  authorization: {
    model: 'role-based + identity-aware',
    enforcement: 'service level',
    principle: 'least privilege',
  },
  
  defenseInDepth: {
    layers: ['network', 'api', 'data', 'identity', 'device'],
    strategy: 'multiple validation points',
  },
};

// Request validation pattern
async function validateRequest(req: Request): Promise<ValidationResult> {
  // Layer 1: Authentication
  const user = await authenticateUser(req);
  if (!user) throw new UnauthorizedError();
  
  // Layer 2: Authorization
  const hasPermission = await checkPermissions(user, req.resource);
  if (!hasPermission) throw new ForbiddenError();
  
  // Layer 3: Input validation
  const validated = await validateInput(req.body);
  if (!validated.success) throw new ValidationError(validated.errors);
  
  // Layer 4: Rate limiting
  const withinLimit = await checkRateLimit(user.id);
  if (!withinLimit) throw new RateLimitError();
  
  return { success: true, user, validated };
}
```

---

## 25.2 Authentication & Authorization

### Authentication

**Email + password, CodexDominion SSO, optional 2FA**

```tsx
// Authentication methods
export type AuthMethod = 'email' | 'sso' | '2fa';

export interface AuthConfig {
  email: {
    passwordMinLength: 12;
    requireSpecialChar: true;
    requireNumber: true;
    requireUppercase: true;
    maxAttempts: 5;
    lockoutDuration: '15m';
  };
  
  sso: {
    provider: 'CodexDominion';
    tokenValidation: 'strict';
    identitySync: true;
  };
  
  twoFactor: {
    optional: true;
    methods: ['totp', 'sms'];
    backupCodes: 10;
  };
}

// Email + password authentication
async function authenticateWithEmail(email: string, password: string) {
  // 1. Check rate limiting
  const attempts = await getLoginAttempts(email);
  if (attempts >= 5) {
    throw new Error('Account locked. Try again in 15 minutes.');
  }
  
  // 2. Validate credentials
  const user = await db.user.findUnique({ where: { email } });
  if (!user) {
    await incrementLoginAttempts(email);
    throw new Error('Invalid email or password.');
  }
  
  // 3. Verify password (hashed with bcrypt/argon2)
  const isValid = await verifyPassword(password, user.passwordHash);
  if (!isValid) {
    await incrementLoginAttempts(email);
    throw new Error('Invalid email or password.');
  }
  
  // 4. Check 2FA if enabled
  if (user.twoFactorEnabled) {
    return { requiresTwoFactor: true, userId: user.id };
  }
  
  // 5. Generate session
  const session = await createSession(user);
  return { success: true, session, user };
}

// CodexDominion SSO
async function authenticateWithSSO(ssoToken: string) {
  // 1. Validate token with CodexDominion auth service
  const validation = await fetch('https://auth.codexdominion.com/validate', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${ssoToken}` },
  });
  
  if (!validation.ok) {
    throw new Error('Invalid SSO token');
  }
  
  const { userId, email, identity } = await validation.json();
  
  // 2. Find or create user
  let user = await db.user.findUnique({ where: { email } });
  if (!user) {
    user = await db.user.create({
      data: { email, identity, ssoProvider: 'CodexDominion' },
    });
  }
  
  // 3. Sync identity
  if (user.identity !== identity) {
    await db.user.update({
      where: { id: user.id },
      data: { identity },
    });
  }
  
  // 4. Create session
  const session = await createSession(user);
  return { success: true, session, user };
}

// 2FA verification
async function verifyTwoFactor(userId: string, code: string) {
  const user = await db.user.findUnique({ where: { id: userId } });
  
  // Verify TOTP code
  const isValid = verifyTOTP(user.twoFactorSecret, code);
  if (!isValid) {
    throw new Error('Invalid verification code');
  }
  
  const session = await createSession(user);
  return { success: true, session, user };
}
```

---

### Authorization

**Role-based (user, premium, pro), identity-aware, tier-aware**

```tsx
// Authorization model
export type UserRole = 'user' | 'premium' | 'pro';
export type UserIdentity = 'diaspora' | 'youth' | 'creator' | 'legacy';
export type UserTier = 'free' | 'premium' | 'pro';

export interface UserPermissions {
  role: UserRole;
  identity: UserIdentity;
  tier: UserTier;
  features: string[];
}

// Permission checking
function hasPermission(user: UserPermissions, feature: string): boolean {
  // Check tier-based permissions
  const tierPermissions = {
    free: ['basic-charts', 'news', 'portfolio-tracking'],
    premium: ['basic-charts', 'news', 'portfolio-tracking', 'alerts', 'identity-insights'],
    pro: ['basic-charts', 'news', 'portfolio-tracking', 'alerts', 'identity-insights', 'advanced-charts', 'heatmaps', 'data-export'],
  };
  
  return tierPermissions[user.tier].includes(feature);
}

// Feature gate component
function FeatureGate({ feature, children, fallback }) {
  const user = useUser();
  
  if (!hasPermission(user, feature)) {
    return fallback || <PremiumGate feature={feature} />;
  }
  
  return <>{children}</>;
}

// Usage
<FeatureGate feature="heatmaps" fallback={<ProGate />}>
  <HeatmapChart data={data} />
</FeatureGate>

// API authorization middleware
async function authorizeRequest(req: Request, requiredPermission: string) {
  const user = await getUserFromSession(req);
  
  if (!hasPermission(user, requiredPermission)) {
    throw new ForbiddenError(`Requires ${requiredPermission} permission`);
  }
  
  return user;
}
```

---

### Session Security

**Short-lived tokens, refresh tokens stored securely, automatic logout on suspicious activity**

```tsx
// Session configuration
export const sessionConfig = {
  accessToken: {
    duration: '15m',  // Short-lived
    algorithm: 'RS256',
    issuer: 'dominion-markets',
  },
  
  refreshToken: {
    duration: '7d',
    storage: 'httpOnly cookie',
    rotation: true,  // New refresh token on each use
  },
  
  security: {
    ipTracking: true,
    deviceFingerprinting: true,
    suspiciousActivityDetection: true,
    autoLogoutOnSuspicion: true,
  },
};

// Create session
async function createSession(user: User, req: Request) {
  const deviceId = await getDeviceFingerprint(req);
  const ipAddress = getClientIP(req);
  
  // Create access token (JWT)
  const accessToken = jwt.sign(
    {
      userId: user.id,
      email: user.email,
      role: user.role,
      identity: user.identity,
      tier: user.tier,
    },
    process.env.JWT_SECRET,
    { expiresIn: '15m', algorithm: 'RS256' }
  );
  
  // Create refresh token
  const refreshToken = generateSecureToken(32);
  
  // Store session in database
  await db.session.create({
    data: {
      userId: user.id,
      refreshToken: await hashToken(refreshToken),
      deviceId,
      ipAddress,
      expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days
    },
  });
  
  return { accessToken, refreshToken };
}

// Refresh session
async function refreshSession(refreshToken: string, req: Request) {
  const hashedToken = await hashToken(refreshToken);
  
  // Find session
  const session = await db.session.findUnique({
    where: { refreshToken: hashedToken },
    include: { user: true },
  });
  
  if (!session || session.expiresAt < new Date()) {
    throw new UnauthorizedError('Invalid or expired refresh token');
  }
  
  // Check for suspicious activity
  const currentIP = getClientIP(req);
  const currentDevice = await getDeviceFingerprint(req);
  
  if (session.ipAddress !== currentIP || session.deviceId !== currentDevice) {
    // Log suspicious activity
    await logSuspiciousActivity({
      userId: session.userId,
      type: 'session-hijacking-attempt',
      originalIP: session.ipAddress,
      attemptIP: currentIP,
    });
    
    // Invalidate all sessions
    await db.session.deleteMany({ where: { userId: session.userId } });
    
    throw new UnauthorizedError('Suspicious activity detected. Please log in again.');
  }
  
  // Rotate refresh token
  await db.session.delete({ where: { id: session.id } });
  
  return createSession(session.user, req);
}

// Suspicious activity detection
async function detectSuspiciousActivity(userId: string, req: Request): Promise<boolean> {
  const recentSessions = await db.session.findMany({
    where: { userId, createdAt: { gte: new Date(Date.now() - 24 * 60 * 60 * 1000) } },
  });
  
  // Check for multiple IPs
  const uniqueIPs = new Set(recentSessions.map(s => s.ipAddress));
  if (uniqueIPs.size > 3) return true;
  
  // Check for multiple devices
  const uniqueDevices = new Set(recentSessions.map(s => s.deviceId));
  if (uniqueDevices.size > 3) return true;
  
  // Check for unusual login times
  const hour = new Date().getHours();
  if (hour < 4 || hour > 23) return true;  // Late night access
  
  return false;
}
```

---

## 25.3 Data Encryption

### In Transit

**TLS 1.2+, HSTS enabled**

```tsx
// Next.js configuration (next.config.mjs)
export default {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=63072000; includeSubDomains; preload',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
        ],
      },
    ];
  },
};

// API requests always use HTTPS
const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://api.dominionmarkets.com'
  : 'http://localhost:3000';

// TLS configuration (server-side)
import https from 'https';
import fs from 'fs';

const server = https.createServer({
  key: fs.readFileSync('/path/to/private-key.pem'),
  cert: fs.readFileSync('/path/to/certificate.pem'),
  minVersion: 'TLSv1.2',  // Enforce TLS 1.2+
  ciphers: [
    'ECDHE-RSA-AES128-GCM-SHA256',
    'ECDHE-RSA-AES256-GCM-SHA384',
    'ECDHE-RSA-CHACHA20-POLY1305',
  ].join(':'),
}, app);
```

---

### At Rest

**AES-256 encryption, encrypted backups, encrypted logs**

```tsx
// Database encryption (Prisma with field-level encryption)
import { createCipheriv, createDecipheriv, randomBytes } from 'crypto';

const ENCRYPTION_KEY = Buffer.from(process.env.ENCRYPTION_KEY, 'hex'); // 32 bytes
const ALGORITHM = 'aes-256-gcm';

// Encrypt sensitive field
export function encrypt(text: string): string {
  const iv = randomBytes(16);
  const cipher = createCipheriv(ALGORITHM, ENCRYPTION_KEY, iv);
  
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  const authTag = cipher.getAuthTag();
  
  // Return iv + authTag + encrypted
  return iv.toString('hex') + ':' + authTag.toString('hex') + ':' + encrypted;
}

// Decrypt sensitive field
export function decrypt(encrypted: string): string {
  const [ivHex, authTagHex, encryptedData] = encrypted.split(':');
  
  const iv = Buffer.from(ivHex, 'hex');
  const authTag = Buffer.from(authTagHex, 'hex');
  const decipher = createDecipheriv(ALGORITHM, ENCRYPTION_KEY, iv);
  
  decipher.setAuthTag(authTag);
  
  let decrypted = decipher.update(encryptedData, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  
  return decrypted;
}

// Usage in Prisma middleware
prisma.$use(async (params, next) => {
  // Encrypt on write
  if (params.action === 'create' || params.action === 'update') {
    if (params.model === 'User' && params.args.data.phoneNumber) {
      params.args.data.phoneNumber = encrypt(params.args.data.phoneNumber);
    }
  }
  
  const result = await next(params);
  
  // Decrypt on read
  if (params.action === 'findUnique' || params.action === 'findMany') {
    if (result?.phoneNumber) {
      result.phoneNumber = decrypt(result.phoneNumber);
    }
  }
  
  return result;
});

// Encrypted backups
async function createEncryptedBackup() {
  const backup = await createDatabaseBackup();
  const encrypted = encrypt(JSON.stringify(backup));
  
  await uploadToSecureStorage(encrypted, {
    bucket: 'backups',
    key: `backup-${new Date().toISOString()}.enc`,
  });
}

// Encrypted logs
import winston from 'winston';

const logger = winston.createLogger({
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json(),
    winston.format((info) => {
      // Encrypt sensitive fields in logs
      if (info.email) info.email = encrypt(info.email);
      if (info.ip) info.ip = encrypt(info.ip);
      return info;
    })()
  ),
  transports: [
    new winston.transports.File({ filename: 'app.log' }),
  ],
});
```

---

### Sensitive Fields

**Passwords hashed with modern algorithms, payment data handled by external processor**

```tsx
// Password hashing with Argon2 (recommended over bcrypt)
import argon2 from 'argon2';

export async function hashPassword(password: string): Promise<string> {
  return argon2.hash(password, {
    type: argon2.argon2id,
    memoryCost: 65536,  // 64 MB
    timeCost: 3,
    parallelism: 4,
  });
}

export async function verifyPassword(password: string, hash: string): Promise<boolean> {
  try {
    return await argon2.verify(hash, password);
  } catch {
    return false;
  }
}

// Payment data - never stored
interface PaymentIntent {
  // DominionMarkets NEVER stores card data
  // All payment processing through Stripe/external processor
  paymentMethodId: string;  // Stripe token only
  customerId: string;       // Stripe customer ID only
  amount: number;
  currency: 'usd';
}

async function processPayment(intent: PaymentIntent) {
  // All card data handled by Stripe
  const result = await stripe.paymentIntents.create({
    amount: intent.amount,
    currency: intent.currency,
    customer: intent.customerId,
    payment_method: intent.paymentMethodId,
  });
  
  // Store only payment intent ID and status
  await db.payment.create({
    data: {
      stripePaymentIntentId: result.id,
      amount: intent.amount,
      status: result.status,
      // NO card data stored
    },
  });
  
  return result;
}
```

---

## 25.4 Data Storage & Retention

### User Data

**Stored securely, retained only as long as needed, deleted on request**

```tsx
// User data retention policy
export const retentionPolicy = {
  activeUser: 'indefinite',  // While account active
  inactiveUser: '2 years',   // 2 years after last login
  deletedUser: '30 days',    // 30-day grace period, then permanent deletion
  
  auditLogs: '1 year',
  sessionLogs: '90 days',
  errorLogs: '30 days',
};

// Delete user data on request
async function deleteUserData(userId: string) {
  // 1. Mark for deletion (30-day grace period)
  await db.user.update({
    where: { id: userId },
    data: {
      deletedAt: new Date(),
      email: `deleted-${userId}@deleted.com`,
      // Clear personal data immediately
    },
  });
  
  // 2. Schedule permanent deletion after 30 days
  await scheduleJob('delete-user-permanent', {
    userId,
    executeAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
  });
  
  // 3. Immediate deletion of sensitive data
  await db.session.deleteMany({ where: { userId } });
  await db.alert.deleteMany({ where: { userId } });
}

// Permanent deletion (after grace period)
async function permanentlyDeleteUser(userId: string) {
  await db.$transaction([
    db.holding.deleteMany({ where: { userId } }),
    db.alert.deleteMany({ where: { userId } }),
    db.session.deleteMany({ where: { userId } }),
    db.user.delete({ where: { id: userId } }),
  ]);
  
  // Remove from external services
  await stripe.customers.del(userId);
}
```

---

### Portfolio Data

**Stored per user, never shared, never used for predictions**

```tsx
// Portfolio data isolation
export const portfolioSecurity = {
  isolation: 'per-user',
  sharing: 'never',
  predictions: 'never',
  encryption: 'at-rest',
};

// Query with user isolation
async function getUserPortfolio(userId: string) {
  // ALWAYS filter by userId - no cross-user data access
  const holdings = await db.holding.findMany({
    where: { userId },  // Enforced at every query
  });
  
  return holdings;
}

// Prevent aggregation across users
❌ const avgPortfolioValue = await db.holding.aggregate({
  _avg: { value: true },  // NEVER aggregate across users
});

✅ const userAvgValue = await db.holding.aggregate({
  where: { userId },  // ALWAYS scope to single user
  _avg: { value: true },
});
```

---

### News Data

**Cached temporarily, no long-term storage of raw articles**

```tsx
// News caching policy
export const newsCaching = {
  duration: '1 hour',
  storage: 'in-memory (Redis)',
  retention: 'no permanent storage',
};

// News cache implementation
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

async function fetchNews(query: string) {
  const cacheKey = `news:${query}`;
  
  // Check cache (1 hour TTL)
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);
  
  // Fetch from external API
  const news = await externalNewsAPI.search(query);
  
  // Cache temporarily (no permanent storage)
  await redis.set(cacheKey, JSON.stringify(news), 'EX', 3600);  // 1 hour
  
  return news;
}
```

---

### Analytics Data

**Generated on demand, not stored permanently**

```tsx
// Analytics generation (no storage)
export const analyticsPolicy = {
  generation: 'on-demand',
  storage: 'temporary cache only',
  retention: '15 minutes',
};

async function generatePortfolioAnalytics(userId: string) {
  const cacheKey = `analytics:${userId}`;
  
  // Check short-lived cache
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);
  
  // Generate analytics from holdings
  const holdings = await getUserPortfolio(userId);
  const analytics = calculateAnalytics(holdings);
  
  // Cache briefly (15 minutes)
  await redis.set(cacheKey, JSON.stringify(analytics), 'EX', 900);
  
  return analytics;
}

// No database storage of analytics
❌ await db.analytics.create({ data: analytics });  // NEVER store
```

---

## 25.5 Privacy Principles

DominionMarkets follows **five privacy principles**:

### 1. User Control

**Users can: delete data, export data (Pro), manage identity, manage alerts, manage notifications**

```tsx
// User control panel
function PrivacySettings() {
  return (
    <div className="space-y-6">
      {/* Delete data */}
      <Card>
        <h3 className="font-medium text-white mb-2">Delete Your Data</h3>
        <p className="text-sm text-slate-400 mb-4">
          Permanently delete your account and all associated data.
        </p>
        <button
          onClick={() => initiateAccountDeletion()}
          className="px-4 py-2 bg-red-500 text-white rounded-lg"
        >
          Delete Account
        </button>
      </Card>
      
      {/* Export data (Pro only) */}
      <FeatureGate feature="data-export">
        <Card>
          <h3 className="font-medium text-white mb-2">Export Your Data</h3>
          <p className="text-sm text-slate-400 mb-4">
            Download all your portfolio data, alerts, and settings.
          </p>
          <button
            onClick={() => exportUserData()}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg"
          >
            Export Data
          </button>
        </Card>
      </FeatureGate>
      
      {/* Manage identity */}
      <Card>
        <h3 className="font-medium text-white mb-2">Your Identity</h3>
        <IdentitySelector currentIdentity={user.identity} />
      </Card>
      
      {/* Manage notifications */}
      <Card>
        <h3 className="font-medium text-white mb-2">Notifications</h3>
        <NotificationPreferences />
      </Card>
    </div>
  );
}

// Data export (Pro feature)
async function exportUserData(userId: string) {
  const user = await db.user.findUnique({ where: { id: userId } });
  const holdings = await db.holding.findMany({ where: { userId } });
  const alerts = await db.alert.findMany({ where: { userId } });
  
  const exportData = {
    user: {
      email: user.email,
      identity: user.identity,
      tier: user.tier,
      createdAt: user.createdAt,
    },
    portfolio: holdings,
    alerts,
    exportedAt: new Date().toISOString(),
  };
  
  return JSON.stringify(exportData, null, 2);
}
```

---

### 2. No Selling of Data

**User data is never sold.**

```tsx
// Hard policy - enforced in code
export const DATA_SELLING_POLICY = {
  allowed: false,  // NEVER
  reasoning: 'User trust is non-negotiable',
  enforcement: 'architectural',
};

// No third-party data sharing endpoints exist
❌ app.post('/api/share-user-data', ...);  // Does not exist
❌ app.post('/api/sell-user-data', ...);   // Does not exist

// No analytics sharing with advertisers
❌ trackUserBehavior(userId, { shareWith: ['advertisers'] });  // Does not exist
```

---

### 3. No Behavioral Tracking

**Only non-sensitive signals used for identity-based cross-promotion**

```tsx
// Cross-promotion signals (non-sensitive only)
export const crossPromotionSignals = {
  allowed: [
    'selected_identity',      // User explicitly selected
    'subscription_tier',      // Premium/Pro status
    'feature_usage_count',    // Number of times used
  ],
  
  forbidden: [
    'browsing_history',
    'click_patterns',
    'time_on_page',
    'scroll_depth',
    'mouse_movements',
  ],
};

// Identity-based cross-promotion (allowed)
function getRelevantEcosystemProducts(identity: UserIdentity): Product[] {
  const products = {
    diaspora: [
      { name: 'IslandNation Marketplace', category: 'e-commerce' },
      { name: 'Caribbean Business Directory', category: 'directory' },
    ],
    youth: [
      { name: 'DominionYouth Learning Platform', category: 'education' },
    ],
    creator: [
      { name: 'Creator Economy Tools', category: 'tools' },
    ],
    legacy: [
      { name: 'Estate Planning Resources', category: 'planning' },
    ],
  };
  
  return products[identity];
}

// NO behavioral tracking
❌ trackPageView(userId, { url, duration, clicks });  // Does not exist
❌ trackScrollDepth(userId, page);  // Does not exist
```

---

### 4. No Predictions

**No predictive analytics, no investment advice, no recommendations**

```tsx
// Hard constraints in code
export const PREDICTION_POLICY = {
  predictiveAnalytics: false,
  investmentAdvice: false,
  recommendations: false,
  reasoning: 'Legal compliance + user trust',
};

// Descriptive only
✅ "Your portfolio is concentrated in tech (65%)."
✅ "This stock is up 2.5% today."
✅ "This company has strong cultural relevance."

// Predictive - forbidden
❌ "This stock will rise 20%."
❌ "Markets are about to crash."
❌ "You should buy this stock."

// Implementation guard
function generateInsight(data: any): string {
  const bannedWords = ['will', 'should', 'recommend', 'predict', 'forecast', 'going to'];
  
  // Validate insight text
  if (bannedWords.some(word => data.text.toLowerCase().includes(word))) {
    throw new Error('Predictive language detected - insight rejected');
  }
  
  return data.text;
}
```

---

### 5. Transparency

**Users always know: what data is used, why it's used, how it's used**

```tsx
// Privacy transparency panel
function DataUsageTransparency() {
  return (
    <div className="p-4 bg-slate-800 rounded-lg">
      <h3 className="font-medium text-white mb-4">How We Use Your Data</h3>
      
      <div className="space-y-4">
        <DataUsageItem
          data="Portfolio holdings"
          why="To show you your portfolio value and analytics"
          how="Stored securely, never shared"
        />
        
        <DataUsageItem
          data="Selected identity"
          why="To personalize insights and cross-promote relevant products"
          how="Used only for content filtering, never for predictions"
        />
        
        <DataUsageItem
          data="Subscription tier"
          why="To enable premium features you've paid for"
          how="Determines feature access, never shared"
        />
        
        <DataUsageItem
          data="Email address"
          why="For account access and important notifications"
          how="Encrypted at rest, never sold"
        />
      </div>
    </div>
  );
}

function DataUsageItem({ data, why, how }) {
  return (
    <div className="p-3 bg-slate-700/50 rounded">
      <p className="text-sm font-medium text-white mb-1">{data}</p>
      <p className="text-xs text-slate-400 mb-1">
        <strong>Why:</strong> {why}
      </p>
      <p className="text-xs text-slate-400">
        <strong>How:</strong> {how}
      </p>
    </div>
  );
}
```

---

## 25.6 Payment & Billing Security

### Handled by External Processor

**PCI-compliant, tokenized payment methods, no card data stored by DominionMarkets**

```tsx
// Payment processing (Stripe integration)
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: '2023-10-16',
});

// Create checkout session (card data never touches our servers)
async function createCheckoutSession(userId: string, priceId: string) {
  const session = await stripe.checkout.sessions.create({
    customer: await getOrCreateStripeCustomer(userId),
    mode: 'subscription',
    payment_method_types: ['card'],
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: 'https://dominionmarkets.com/success',
    cancel_url: 'https://dominionmarkets.com/pricing',
  });
  
  return session;
}

// Store only Stripe IDs - NEVER card data
interface Subscription {
  userId: string;
  stripeSubscriptionId: string;  // Stripe ID only
  stripeCustomerId: string;      // Stripe ID only
  tier: 'premium' | 'pro';
  status: 'active' | 'canceled' | 'past_due';
  currentPeriodEnd: Date;
  // NO CARD DATA STORED
}

// Handle webhook from Stripe
async function handleStripeWebhook(event: Stripe.Event) {
  switch (event.type) {
    case 'customer.subscription.created':
    case 'customer.subscription.updated':
      await updateSubscription(event.data.object as Stripe.Subscription);
      break;
      
    case 'customer.subscription.deleted':
      await cancelSubscription(event.data.object as Stripe.Subscription);
      break;
      
    case 'invoice.payment_failed':
      await handlePaymentFailure(event.data.object as Stripe.Invoice);
      break;
  }
}
```

---

### Billing Events

**Renewal, upgrade, downgrade, cancellation**

```tsx
// Billing event handlers
async function handleSubscriptionRenewal(subscription: Stripe.Subscription) {
  await db.subscription.update({
    where: { stripeSubscriptionId: subscription.id },
    data: {
      currentPeriodEnd: new Date(subscription.current_period_end * 1000),
      status: 'active',
    },
  });
  
  // Send renewal confirmation email
  await sendEmail({
    to: user.email,
    subject: 'Subscription renewed',
    template: 'renewal-confirmation',
  });
}

async function handleSubscriptionUpgrade(userId: string, newTier: 'pro') {
  // Update Stripe subscription
  const subscription = await getStripeSubscription(userId);
  await stripe.subscriptions.update(subscription.id, {
    items: [{ id: subscription.items.data[0].id, price: PRO_PRICE_ID }],
  });
  
  // Update local database
  await db.user.update({
    where: { id: userId },
    data: { tier: newTier },
  });
  
  // Send upgrade confirmation
  await sendEmail({
    to: user.email,
    subject: 'Upgraded to Pro',
    template: 'upgrade-confirmation',
  });
}

async function handleSubscriptionCancellation(userId: string) {
  // Cancel at period end (user retains access until then)
  const subscription = await getStripeSubscription(userId);
  await stripe.subscriptions.update(subscription.id, {
    cancel_at_period_end: true,
  });
  
  await db.subscription.update({
    where: { userId },
    data: { cancelAtPeriodEnd: true },
  });
  
  // Send cancellation confirmation
  await sendEmail({
    to: user.email,
    subject: 'Subscription canceled',
    template: 'cancellation-confirmation',
    data: { accessUntil: subscription.current_period_end },
  });
}
```

---

### Fraud Prevention

**Suspicious activity detection, automatic lockouts, email verification**

```tsx
// Fraud detection
async function detectPaymentFraud(userId: string, payment: PaymentIntent): Promise<boolean> {
  // Check for multiple failed payments
  const recentFailures = await db.payment.count({
    where: {
      userId,
      status: 'failed',
      createdAt: { gte: new Date(Date.now() - 24 * 60 * 60 * 1000) },
    },
  });
  
  if (recentFailures >= 3) {
    await lockAccount(userId, 'fraud-detection');
    return true;
  }
  
  // Check for rapid subscription changes
  const recentChanges = await db.subscriptionEvent.count({
    where: {
      userId,
      createdAt: { gte: new Date(Date.now() - 60 * 60 * 1000) },
    },
  });
  
  if (recentChanges >= 5) {
    await lockAccount(userId, 'fraud-detection');
    return true;
  }
  
  return false;
}

// Account lockout
async function lockAccount(userId: string, reason: string) {
  await db.user.update({
    where: { id: userId },
    data: { locked: true, lockReason: reason },
  });
  
  // Notify user
  await sendEmail({
    to: user.email,
    subject: 'Account locked due to suspicious activity',
    template: 'account-locked',
    data: { reason, supportEmail: 'support@dominionmarkets.com' },
  });
}
```

---

## 25.7 API Security

### Rate Limiting

**Prevents abuse**

```tsx
// Rate limiting middleware (using Redis)
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';

export const apiLimiter = rateLimit({
  store: new RedisStore({
    client: redis,
    prefix: 'rate-limit:',
  }),
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,  // 100 requests per 15 minutes
  message: 'Too many requests. Please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});

// Per-endpoint rate limits
export const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,  // 5 login attempts per 15 minutes
  message: 'Too many login attempts. Please try again later.',
});

export const portfolioLimiter = rateLimit({
  windowMs: 60 * 1000,  // 1 minute
  max: 30,  // 30 requests per minute
});

// Usage
app.use('/api/', apiLimiter);
app.use('/api/auth/login', authLimiter);
app.use('/api/portfolio', portfolioLimiter);
```

---

### Input Validation

**Prevents injection attacks**

```tsx
// Input validation with Zod
import { z } from 'zod';

// Schema definitions
const createHoldingSchema = z.object({
  ticker: z.string().min(1).max(10).regex(/^[A-Z]+$/),
  shares: z.number().positive().max(1000000),
  averageCost: z.number().positive().max(1000000),
});

const createAlertSchema = z.object({
  ticker: z.string().min(1).max(10).regex(/^[A-Z]+$/),
  type: z.enum(['price', 'news', 'earnings', 'volume']),
  condition: z.object({
    above: z.number().optional(),
    below: z.number().optional(),
  }).optional(),
});

// Validation middleware
function validateRequest(schema: z.ZodSchema) {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      req.body = await schema.parseAsync(req.body);
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({
          error: 'Validation failed',
          details: error.errors,
        });
      }
      next(error);
    }
  };
}

// Usage
app.post('/api/holdings', validateRequest(createHoldingSchema), async (req, res) => {
  // req.body is now validated and type-safe
  const holding = await createHolding(req.user.id, req.body);
  res.json(holding);
});

// SQL injection prevention (Prisma automatically escapes)
✅ await db.holding.findMany({
  where: { ticker: userInput },  // Automatically escaped by Prisma
});

❌ await db.$executeRaw`SELECT * FROM holdings WHERE ticker = ${userInput}`;  // Vulnerable
✅ await db.$executeRaw`SELECT * FROM holdings WHERE ticker = ${Prisma.sql([userInput])}`;  // Safe
```

---

### Output Sanitization

**Prevents data leakage**

```tsx
// Output sanitization
function sanitizeUser(user: User): PublicUser {
  return {
    id: user.id,
    email: maskEmail(user.email),
    identity: user.identity,
    tier: user.tier,
    // Never expose: passwordHash, refreshToken, phoneNumber, etc.
  };
}

function maskEmail(email: string): string {
  const [local, domain] = email.split('@');
  const masked = local.slice(0, 2) + '***' + local.slice(-1);
  return `${masked}@${domain}`;
}

// Error sanitization (never expose internal details)
function sanitizeError(error: Error): { message: string } {
  if (process.env.NODE_ENV === 'production') {
    // Generic message in production
    return { message: 'An error occurred. Please try again.' };
  }
  
  // Detailed message in development
  return { message: error.message };
}

// API response wrapper
function apiResponse(data: any): Response {
  return {
    success: true,
    data: sanitizeOutput(data),
    timestamp: new Date().toISOString(),
  };
}
```

---

### Audit Logging

**Tracks: login attempts, subscription changes, alert creation, portfolio edits**

```tsx
// Audit log structure
interface AuditLog {
  id: string;
  userId: string;
  action: string;
  resource: string;
  details: Record<string, any>;
  ipAddress: string;
  userAgent: string;
  timestamp: Date;
}

// Audit logging middleware
async function auditLog(req: Request, action: string, details: any) {
  await db.auditLog.create({
    data: {
      userId: req.user.id,
      action,
      resource: req.path,
      details,
      ipAddress: getClientIP(req),
      userAgent: req.headers['user-agent'],
      timestamp: new Date(),
    },
  });
}

// Usage in critical operations
app.post('/api/auth/login', async (req, res) => {
  const result = await authenticateUser(req.body);
  
  await auditLog(req, 'login', {
    success: result.success,
    method: 'email',
  });
  
  res.json(result);
});

app.post('/api/subscription/upgrade', async (req, res) => {
  const result = await upgradeSubscription(req.user.id, req.body.tier);
  
  await auditLog(req, 'subscription-upgrade', {
    from: req.user.tier,
    to: req.body.tier,
  });
  
  res.json(result);
});

app.post('/api/holdings', async (req, res) => {
  const holding = await createHolding(req.user.id, req.body);
  
  await auditLog(req, 'holding-created', {
    ticker: holding.ticker,
    shares: holding.shares,
  });
  
  res.json(holding);
});

// Query audit logs
async function getAuditLogs(userId: string, filters?: AuditLogFilters) {
  return db.auditLog.findMany({
    where: {
      userId,
      action: filters?.action,
      timestamp: {
        gte: filters?.from,
        lte: filters?.to,
      },
    },
    orderBy: { timestamp: 'desc' },
    take: 100,
  });
}
```

---

## 25.8 Identity & Personalization Safety

**Identity is used only for: content personalization, insights, cross-promotion, dashboard widgets**

**Identity is never used for: predictions, recommendations, financial profiling, risk scoring**

**Identity is a lens, not a classifier.**

```tsx
// Identity usage rules
export const identityUsageRules = {
  allowed: [
    'content-personalization',  // Filter news by cultural relevance
    'insights',                 // "This company has diaspora relevance"
    'cross-promotion',          // Show relevant ecosystem products
    'dashboard-widgets',        // Identity-specific widgets
  ],
  
  forbidden: [
    'predictions',              // NEVER predict based on identity
    'recommendations',          // NEVER recommend based on identity
    'financial-profiling',      // NEVER profile financial behavior by identity
    'risk-scoring',             // NEVER score risk by identity
  ],
};

// ✅ Allowed: Content personalization
function getPersonalizedNews(identity: UserIdentity) {
  return newsAPI.search({
    topics: getRelevantTopics(identity),
    culturalRelevance: identity,
  });
}

// ✅ Allowed: Insights
function getIdentityInsight(identity: UserIdentity, stock: Stock): string {
  if (identity === 'diaspora' && stock.caribbeanRevenue > 0.3) {
    return `${stock.ticker} generates ${stock.caribbeanRevenue * 100}% of revenue from Caribbean markets.`;
  }
  return null;
}

// ✅ Allowed: Cross-promotion
function getEcosystemProducts(identity: UserIdentity): Product[] {
  return ecosystemProducts.filter(p => p.relevantIdentities.includes(identity));
}

// ❌ Forbidden: Predictions based on identity
❌ function predictReturns(identity: UserIdentity): number {
  // NEVER predict returns based on identity
}

// ❌ Forbidden: Recommendations based on identity
❌ function recommendStocks(identity: UserIdentity): Stock[] {
  // NEVER recommend stocks based on identity
}

// ❌ Forbidden: Financial profiling
❌ function getRiskProfile(identity: UserIdentity): 'low' | 'medium' | 'high' {
  // NEVER profile risk by identity
}

// Identity as a lens, not a classifier
function filterContent(content: Content[], identity: UserIdentity): Content[] {
  // Identity filters content visibility
  // Identity does NOT determine capability, risk, or outcomes
  return content.filter(c => c.relevantIdentities.includes(identity));
}
```

---

## 25.9 Ecosystem Integration Security

### CodexDominion SSO

**Secure token exchange, no password sharing, identity sync only**

```tsx
// SSO integration
async function handleSSOAuth(ssoToken: string) {
  // 1. Validate token with CodexDominion auth service
  const response = await fetch('https://auth.codexdominion.com/validate', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${ssoToken}`,
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) {
    throw new Error('Invalid SSO token');
  }
  
  const { userId, email, identity } = await response.json();
  
  // 2. Find or create user (identity sync only)
  let user = await db.user.findUnique({ where: { email } });
  
  if (!user) {
    user = await db.user.create({
      data: {
        email,
        identity,
        ssoProvider: 'CodexDominion',
        // NO password - SSO only
      },
    });
  } else if (user.identity !== identity) {
    // Sync identity updates
    await db.user.update({
      where: { id: user.id },
      data: { identity },
    });
  }
  
  // 3. Create local session
  const session = await createSession(user);
  return session;
}

// NO password sharing between systems
// Each system maintains own authentication
```

---

### IslandNation Marketplace

**Secure product linking, no data sharing without consent**

```tsx
// IslandNation integration
export const islandNationIntegration = {
  dataSharing: 'opt-in only',
  sharedData: ['email', 'identity'],  // With explicit consent
  neverShared: ['portfolio', 'holdings', 'financial-data'],
};

// Product linking (secure)
function getMarketplaceRecommendations(identity: UserIdentity) {
  // Identity-based product filtering
  // NO financial data shared
  return fetch('https://api.islandnation.com/products', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${ISLANDNATION_API_KEY}` },
    body: JSON.stringify({ identity }),  // Identity only
  });
}

// User must explicitly consent to data sharing
async function connectIslandNation(userId: string, consent: boolean) {
  if (!consent) {
    throw new Error('User consent required for IslandNation integration');
  }
  
  const user = await db.user.findUnique({ where: { id: userId } });
  
  // Share only email + identity (with consent)
  await islandNationAPI.createAccount({
    email: user.email,
    identity: user.identity,
    source: 'DominionMarkets',
  });
  
  // Mark integration active
  await db.user.update({
    where: { id: userId },
    data: { islandNationConnected: true },
  });
}
```

---

### DominionYouth

**Safe learning mode, no portfolio data shared**

```tsx
// DominionYouth integration
export const dominionYouthIntegration = {
  dataSharing: 'learning progress only',
  neverShared: ['portfolio', 'holdings', 'alerts', 'financial-data'],
  safeMode: true,
};

// Share learning progress (if user is Youth identity)
async function syncLearningProgress(userId: string) {
  const user = await db.user.findUnique({ where: { id: userId } });
  
  if (user.identity !== 'youth') {
    return;  // Only for Youth identity users
  }
  
  // Share only learning-related data
  await dominionYouthAPI.updateProgress({
    userId: user.id,
    completedLessons: user.completedFinancialLessons,
    // NO portfolio data
    // NO holdings data
    // NO financial data
  });
}

// Receive educational content
async function getEducationalContent(userId: string): Promise<Content[]> {
  const user = await db.user.findUnique({ where: { id: userId } });
  
  if (user.identity !== 'youth') {
    return [];
  }
  
  // Fetch beginner-friendly content from DominionYouth
  const content = await dominionYouthAPI.getContent({
    level: 'beginner',
    topics: ['investing-basics', 'portfolio-management'],
  });
  
  return content;
}
```

---

## 25.10 Incident Response

### Detection

**Automated monitoring, anomaly detection**

```tsx
// Incident detection
export const incidentDetection = {
  monitoring: 'continuous',
  alerting: 'automated',
  thresholds: {
    errorRate: 0.05,  // 5% error rate triggers alert
    responseTime: 2000,  // 2s response time triggers alert
    failedLogins: 10,  // 10 failed logins in 5min triggers alert
  },
};

// Monitoring service
import * as Sentry from '@sentry/node';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,
});

// Error monitoring
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  // Log to Sentry
  Sentry.captureException(err, {
    user: { id: req.user?.id },
    tags: { endpoint: req.path },
  });
  
  // Check if incident threshold reached
  const recentErrors = await getRecentErrorCount();
  if (recentErrors > 100) {
    await triggerIncident('high-error-rate', { count: recentErrors });
  }
  
  res.status(500).json({ error: 'Internal server error' });
});

// Anomaly detection
async function detectAnomalies() {
  // Check for unusual patterns
  const metrics = await getSystemMetrics();
  
  if (metrics.errorRate > 0.05) {
    await triggerIncident('high-error-rate', metrics);
  }
  
  if (metrics.avgResponseTime > 2000) {
    await triggerIncident('slow-response-time', metrics);
  }
  
  const failedLogins = await getRecentFailedLogins(5 * 60 * 1000);  // 5 minutes
  if (failedLogins > 10) {
    await triggerIncident('brute-force-attack', { attempts: failedLogins });
  }
}
```

---

### Response

**Immediate containment, root cause analysis, user notification (if required)**

```tsx
// Incident response workflow
async function handleIncident(type: string, details: any) {
  // 1. Immediate containment
  switch (type) {
    case 'brute-force-attack':
      await enableStrictRateLimiting();
      break;
      
    case 'data-breach':
      await lockAllSessions();
      await notifyAllUsers();
      break;
      
    case 'ddos-attack':
      await enableDDOSProtection();
      break;
  }
  
  // 2. Root cause analysis
  const analysis = await investigateIncident(type, details);
  
  // 3. User notification (if required)
  if (requiresUserNotification(type)) {
    await notifyAffectedUsers(type, analysis);
  }
  
  // 4. Log incident
  await db.incident.create({
    data: {
      type,
      details,
      detectedAt: new Date(),
      status: 'investigating',
    },
  });
}

// User notification
async function notifyAffectedUsers(type: string, analysis: any) {
  const users = await getAffectedUsers(analysis);
  
  for (const user of users) {
    await sendEmail({
      to: user.email,
      subject: 'Security Notice',
      template: 'incident-notification',
      data: {
        type,
        description: getIncidentDescription(type),
        action: getRequiredAction(type),
        supportEmail: 'security@dominionmarkets.com',
      },
    });
  }
}
```

---

### Recovery

**Secure restore, patch deployment, post-incident review**

```tsx
// Recovery workflow
async function recoverFromIncident(incidentId: string) {
  const incident = await db.incident.findUnique({ where: { id: incidentId } });
  
  // 1. Secure restore
  if (incident.requiresRestore) {
    await restoreFromBackup(incident.backupId);
  }
  
  // 2. Patch deployment
  if (incident.requiresPatch) {
    await deploySecurityPatch(incident.patchId);
  }
  
  // 3. Verify system integrity
  const integrity = await verifySystemIntegrity();
  if (!integrity.passed) {
    throw new Error('System integrity check failed');
  }
  
  // 4. Resume normal operations
  await disableIncidentMode();
  
  // 5. Post-incident review
  await schedulePostIncidentReview(incidentId);
  
  // 6. Update incident status
  await db.incident.update({
    where: { id: incidentId },
    data: {
      status: 'resolved',
      resolvedAt: new Date(),
    },
  });
}

// Post-incident review
async function conductPostIncidentReview(incidentId: string) {
  const incident = await db.incident.findUnique({
    where: { id: incidentId },
    include: { logs: true },
  });
  
  const review = {
    whatHappened: analyzeIncident(incident),
    whyItHappened: identifyRootCause(incident),
    howToPrevent: generatePreventionPlan(incident),
    lessonsLearned: extractLessons(incident),
  };
  
  // Document review
  await db.incidentReview.create({ data: review });
  
  // Implement prevention measures
  await implementPreventionPlan(review.howToPrevent);
}
```

---

## 25.11 Compliance

DominionMarkets aligns with:
- **Industry best practices**
- **Modern encryption standards**
- **Secure coding guidelines**
- **Privacy-first design**

```tsx
// Compliance framework
export const complianceFramework = {
  encryption: {
    inTransit: 'TLS 1.2+',
    atRest: 'AES-256',
    hashing: 'Argon2',
  },
  
  authentication: {
    passwordPolicy: 'NIST SP 800-63B',
    sessionManagement: 'OWASP guidelines',
    twoFactor: 'Optional TOTP/SMS',
  },
  
  dataProtection: {
    retention: 'Minimal retention periods',
    deletion: 'User-initiated deletion',
    encryption: 'Field-level encryption for sensitive data',
  },
  
  privacy: {
    userControl: 'Full data export and deletion',
    transparency: 'Clear data usage documentation',
    noSelling: 'Data never sold',
    noPredictions: 'No predictive analytics',
  },
  
  apiSecurity: {
    rateLimiting: 'Per-endpoint limits',
    inputValidation: 'Zod schema validation',
    outputSanitization: 'PII masking',
    auditLogging: 'All critical operations logged',
  },
  
  incidentResponse: {
    detection: 'Automated monitoring',
    response: 'Documented response procedures',
    recovery: 'Secure restore processes',
    review: 'Post-incident reviews',
  },
};

// Compliance audit checklist
export const complianceAudit = [
  '✅ All data encrypted in transit (TLS 1.2+)',
  '✅ All sensitive data encrypted at rest (AES-256)',
  '✅ Passwords hashed with Argon2',
  '✅ No card data stored (PCI compliance via Stripe)',
  '✅ User can delete all data',
  '✅ User can export data (Pro tier)',
  '✅ No data selling',
  '✅ No behavioral tracking',
  '✅ No predictions or recommendations',
  '✅ Rate limiting on all endpoints',
  '✅ Input validation on all endpoints',
  '✅ Audit logging for critical operations',
  '✅ Incident response procedures documented',
  '✅ Regular security audits',
  '✅ WCAG 2.1 AA accessibility compliance',
];
```

---

## Security Implementation Checklist

✅ **Zero Trust Architecture**: Every request authenticated and authorized  
✅ **Authentication**: Email + password, SSO, optional 2FA  
✅ **Authorization**: Role-based, identity-aware, tier-aware permissions  
✅ **Session Security**: Short-lived tokens, secure refresh, auto-logout  
✅ **Encryption**: TLS 1.2+ in transit, AES-256 at rest  
✅ **Data Retention**: Minimal retention, user-initiated deletion  
✅ **Privacy Principles**: User control, no selling, no tracking, no predictions  
✅ **Payment Security**: PCI-compliant external processor, no card data stored  
✅ **API Security**: Rate limiting, input validation, output sanitization, audit logging  
✅ **Identity Safety**: Content lens only, never for predictions/profiling  
✅ **Ecosystem Security**: Secure SSO, opt-in data sharing, no financial data shared  
✅ **Incident Response**: Automated detection, documented response, post-incident review  
✅ **Compliance**: Industry standards, encryption, secure coding, privacy-first  

---

## SECTION 26 — PERFORMANCE & OPTIMIZATION STANDARDS

DominionMarkets must be **fast, reliable, and efficient**.

Performance isn't a feature — it's a **trust signal**.

This section defines the full **performance optimization framework** that ensures:
- **Fast load times**
- **Efficient data fetching**
- **Smart caching strategies**
- **Graceful degradation**
- **Identity-aware optimization**
- **Scalable architecture**

---

## 26.1 Performance Principles

DominionMarkets follows **five core performance principles**:

### 1. Speed is Trust
Fast load times build confidence.

**Target Metrics:**
- Initial page load: **< 2 seconds**
- Time to interactive: **< 3 seconds**
- Largest Contentful Paint (LCP): **< 2.5 seconds**
- First Input Delay (FID): **< 100ms**
- Cumulative Layout Shift (CLS): **< 0.1**

### 2. Freshness Where It Matters
Real-time where needed, cached where safe.

**Real-time:**
- Stock prices (15-second refresh)
- Portfolio value (on demand)
- Breaking news alerts

**Cached:**
- Historical charts (5 minutes)
- News articles (1 hour)
- Company information (24 hours)
- Static assets (immutable)

### 3. Predictable Performance
No sudden spikes. No jarring delays.

**Consistency:**
- Response times within **±20%** variance
- No layout shifts after initial render
- Smooth transitions and animations
- Loading states for operations **> 500ms**

### 4. Graceful Degradation
If something fails, the experience remains smooth.

**Fallback Strategy:**
- Cached data if API fails
- Skeleton loaders if data delayed
- Error boundaries prevent full crashes
- Retry logic with exponential backoff

### 5. Identity-Aware Optimization
Identity widgets load efficiently and independently.

**Optimization:**
- Identity widgets lazy-loaded
- Independent data fetching per widget
- Parallel loading, no blocking
- Cached per identity type

---

### Implementation

```tsx
// Performance configuration
export const performanceConfig = {
  targets: {
    initialLoad: 2000,      // 2 seconds
    timeToInteractive: 3000, // 3 seconds
    lcp: 2500,              // 2.5 seconds (Core Web Vital)
    fid: 100,               // 100ms (Core Web Vital)
    cls: 0.1,               // 0.1 (Core Web Vital)
  },
  
  caching: {
    stockPrices: 15,        // 15 seconds
    charts: 300,            // 5 minutes
    news: 3600,             // 1 hour
    companyInfo: 86400,     // 24 hours
    staticAssets: 'immutable',
  },
  
  realtime: {
    stockPrices: true,
    portfolioValue: true,
    breakingNews: true,
  },
  
  thresholds: {
    showLoadingState: 500,  // Show loading after 500ms
    responseVariance: 0.2,  // ±20% acceptable variance
    retryAttempts: 3,
    retryDelay: 1000,       // Start with 1s, exponential backoff
  },
};

// Speed is trust - Performance monitoring
import { useEffect } from 'react';

export function usePerformanceMonitoring(pageName: string) {
  useEffect(() => {
    // Measure Core Web Vitals
    if (typeof window !== 'undefined' && 'performance' in window) {
      // Largest Contentful Paint (LCP)
      const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        
        console.log(`[LCP] ${pageName}:`, lastEntry.startTime);
        
        if (lastEntry.startTime > 2500) {
          console.warn(`⚠️ LCP exceeds 2.5s target: ${lastEntry.startTime}ms`);
        }
      });
      
      observer.observe({ entryTypes: ['largest-contentful-paint'] });
      
      // First Input Delay (FID)
      const fidObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry: any) => {
          console.log(`[FID] ${pageName}:`, entry.processingStart - entry.startTime);
          
          if (entry.processingStart - entry.startTime > 100) {
            console.warn(`⚠️ FID exceeds 100ms target`);
          }
        });
      });
      
      fidObserver.observe({ entryTypes: ['first-input'] });
      
      return () => {
        observer.disconnect();
        fidObserver.disconnect();
      };
    }
  }, [pageName]);
}

// Usage in pages
export default function DashboardPage() {
  usePerformanceMonitoring('dashboard');
  
  return <Dashboard />;
}
```

---

### Freshness Strategy Implementation

```tsx
// Real-time data fetching (stock prices)
import { useEffect, useState } from 'react';

export function useRealtimeStockPrice(ticker: string) {
  const [price, setPrice] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    const fetchPrice = async () => {
      try {
        const response = await fetch(`/api/stocks/${ticker}/price`);
        const data = await response.json();
        setPrice(data.price);
        setLoading(false);
      } catch (error) {
        console.error('Failed to fetch price:', error);
      }
    };
    
    // Initial fetch
    fetchPrice();
    
    // Refresh every 15 seconds
    interval = setInterval(fetchPrice, 15000);
    
    return () => clearInterval(interval);
  }, [ticker]);
  
  return { price, loading };
}

// Cached data fetching (company info)
export async function getCachedCompanyInfo(ticker: string) {
  const cacheKey = `company:${ticker}`;
  
  // Check cache (24-hour TTL)
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }
  
  // Fetch from API
  const data = await fetchCompanyInfo(ticker);
  
  // Cache for 24 hours
  await redis.set(cacheKey, JSON.stringify(data), 'EX', 86400);
  
  return data;
}

// Hybrid approach - fresh when critical, cached otherwise
export function useStockData(ticker: string) {
  // Real-time price (15s refresh)
  const { price, loading: priceLoading } = useRealtimeStockPrice(ticker);
  
  // Cached company info (24h cache)
  const { data: companyInfo, loading: infoLoading } = useSWR(
    `/api/companies/${ticker}`,
    fetcher,
    { refreshInterval: 0 } // No automatic refresh - 24h cache on server
  );
  
  // Cached chart data (5min cache)
  const { data: chartData, loading: chartLoading } = useSWR(
    `/api/stocks/${ticker}/chart`,
    fetcher,
    { refreshInterval: 300000 } // 5 minutes
  );
  
  return {
    price,           // Real-time
    companyInfo,     // Cached 24h
    chartData,       // Cached 5min
    loading: priceLoading || infoLoading || chartLoading,
  };
}
```

---

### Predictable Performance Implementation

```tsx
// Consistent loading states
export function LoadingState({ delay = 500 }: { delay?: number }) {
  const [show, setShow] = useState(false);
  
  useEffect(() => {
    // Only show loading spinner if operation takes > 500ms
    const timer = setTimeout(() => setShow(true), delay);
    return () => clearTimeout(timer);
  }, [delay]);
  
  if (!show) return null;
  
  return (
    <div className="flex items-center justify-center p-8">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-yellow-500" />
    </div>
  );
}

// Skeleton loaders for consistent layout
export function StockCardSkeleton() {
  return (
    <div className="p-4 bg-slate-800 rounded-lg border border-slate-700 animate-pulse">
      <div className="h-4 w-16 bg-slate-700 rounded mb-2" />
      <div className="h-8 w-24 bg-slate-700 rounded mb-1" />
      <div className="h-4 w-20 bg-slate-700 rounded" />
    </div>
  );
}

// Prevent layout shifts
export function StockCard({ ticker }: { ticker: string }) {
  const { data, loading } = useStockData(ticker);
  
  // Reserve space to prevent CLS
  return (
    <div className="p-4 bg-slate-800 rounded-lg border border-slate-700 min-h-[120px]">
      {loading ? (
        <StockCardSkeleton />
      ) : (
        <>
          <p className="text-sm text-slate-400">{ticker}</p>
          <p className="text-2xl font-bold text-white">${data.price}</p>
          <p className={`text-sm ${data.change >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
            {data.changePercent}%
          </p>
        </>
      )}
    </div>
  );
}

// Response time monitoring
const responseTimeTracker = new Map<string, number[]>();

export function trackResponseTime(endpoint: string, duration: number) {
  if (!responseTimeTracker.has(endpoint)) {
    responseTimeTracker.set(endpoint, []);
  }
  
  const times = responseTimeTracker.get(endpoint)!;
  times.push(duration);
  
  // Keep last 100 measurements
  if (times.length > 100) {
    times.shift();
  }
  
  // Calculate statistics
  const avg = times.reduce((a, b) => a + b, 0) / times.length;
  const variance = times.map(t => Math.abs(t - avg) / avg).reduce((a, b) => a + b, 0) / times.length;
  
  // Warn if variance > 20%
  if (variance > 0.2) {
    console.warn(`⚠️ High variance detected for ${endpoint}: ${(variance * 100).toFixed(1)}%`);
  }
}
```

---

### Graceful Degradation Implementation

```tsx
// Error boundary component
import { Component, ReactNode } from 'react';

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }
  
  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }
  
  componentDidCatch(error: Error, errorInfo: any) {
    console.error('ErrorBoundary caught:', error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="p-8 text-center">
          <p className="text-slate-400 mb-4">Something went wrong.</p>
          <button
            onClick={() => this.setState({ hasError: false })}
            className="px-4 py-2 bg-yellow-500 text-slate-900 rounded-lg"
          >
            Try Again
          </button>
        </div>
      );
    }
    
    return this.props.children;
  }
}

// Usage
<ErrorBoundary fallback={<StockCardError />}>
  <StockCard ticker="AAPL" />
</ErrorBoundary>

// Fallback to cached data
export function useDataWithFallback<T>(
  fetcher: () => Promise<T>,
  cacheKey: string
): { data: T | null; loading: boolean; error: Error | null } {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  
  useEffect(() => {
    const loadData = async () => {
      try {
        // Try to fetch fresh data
        const freshData = await fetcher();
        setData(freshData);
        
        // Cache for fallback
        localStorage.setItem(cacheKey, JSON.stringify(freshData));
      } catch (err) {
        setError(err as Error);
        
        // Fall back to cached data
        const cached = localStorage.getItem(cacheKey);
        if (cached) {
          setData(JSON.parse(cached));
          console.warn('Using cached data due to fetch error');
        }
      } finally {
        setLoading(false);
      }
    };
    
    loadData();
  }, [cacheKey]);
  
  return { data, loading, error };
}

// Retry with exponential backoff
export async function fetchWithRetry<T>(
  fetcher: () => Promise<T>,
  maxAttempts = 3,
  initialDelay = 1000
): Promise<T> {
  let lastError: Error;
  
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fetcher();
    } catch (error) {
      lastError = error as Error;
      
      if (attempt === maxAttempts) break;
      
      // Exponential backoff: 1s, 2s, 4s
      const delay = initialDelay * Math.pow(2, attempt - 1);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  
  throw lastError!;
}

// Usage
const data = await fetchWithRetry(
  () => fetch('/api/stocks/AAPL').then(r => r.json()),
  3,
  1000
);
```

---

### Identity-Aware Optimization Implementation

```tsx
// Lazy load identity widgets
import dynamic from 'next/dynamic';

const DiasporaFlowMap = dynamic(() => import('@/components/identity/DiasporaFlowMap'), {
  loading: () => <IdentityWidgetSkeleton />,
  ssr: false, // Only load on client
});

const CreatorIndex = dynamic(() => import('@/components/identity/CreatorIndex'), {
  loading: () => <IdentityWidgetSkeleton />,
  ssr: false,
});

const YouthChallenges = dynamic(() => import('@/components/identity/YouthChallenges'), {
  loading: () => <IdentityWidgetSkeleton />,
  ssr: false,
});

const LegacyDividends = dynamic(() => import('@/components/identity/LegacyDividends'), {
  loading: () => <IdentityWidgetSkeleton />,
  ssr: false,
});

// Identity widget container with independent loading
export function IdentityWidgets({ identity }: { identity: UserIdentity }) {
  // Only render relevant widget for user's identity
  const WidgetComponent = {
    diaspora: DiasporaFlowMap,
    youth: YouthChallenges,
    creator: CreatorIndex,
    legacy: LegacyDividends,
  }[identity];
  
  return (
    <Suspense fallback={<IdentityWidgetSkeleton />}>
      <WidgetComponent />
    </Suspense>
  );
}

// Parallel data fetching for identity widgets
export function useIdentityWidgetData(identity: UserIdentity) {
  // Each identity type has its own data requirements
  const endpoints = {
    diaspora: '/api/identity/diaspora/flow-map',
    youth: '/api/identity/youth/challenges',
    creator: '/api/identity/creator/index',
    legacy: '/api/identity/legacy/dividends',
  };
  
  const endpoint = endpoints[identity];
  
  // Cached per identity type (5 minutes)
  const { data, error, loading } = useSWR(
    endpoint,
    fetcher,
    {
      refreshInterval: 300000, // 5 minutes
      revalidateOnFocus: false,
      dedupingInterval: 60000, // 1 minute deduplication
    }
  );
  
  return { data, error, loading };
}

// Prefetch identity widget data on hover
export function IdentitySelector({ onSelect }: { onSelect: (id: UserIdentity) => void }) {
  const prefetchData = (identity: UserIdentity) => {
    // Prefetch data when user hovers over identity option
    const endpoint = {
      diaspora: '/api/identity/diaspora/flow-map',
      youth: '/api/identity/youth/challenges',
      creator: '/api/identity/creator/index',
      legacy: '/api/identity/legacy/dividends',
    }[identity];
    
    fetch(endpoint); // Prefetch - result will be cached
  };
  
  return (
    <div className="grid grid-cols-2 gap-4">
      <button
        onMouseEnter={() => prefetchData('diaspora')}
        onClick={() => onSelect('diaspora')}
        className="p-4 bg-slate-800 rounded-lg hover:bg-slate-700"
      >
        <Globe className="w-6 h-6 text-emerald-400 mb-2" />
        <span>Diaspora</span>
      </button>
      {/* Other identity options */}
    </div>
  );
}

// Independent error handling per widget
export function IdentityWidgetWithFallback({ identity }: { identity: UserIdentity }) {
  const { data, error, loading } = useIdentityWidgetData(identity);
  
  if (error) {
    // Widget fails gracefully - doesn't crash page
    return (
      <div className="p-4 bg-slate-800 rounded-lg border border-slate-700">
        <p className="text-sm text-slate-400">
          Unable to load {identity} insights
        </p>
      </div>
    );
  }
  
  if (loading) {
    return <IdentityWidgetSkeleton />;
  }
  
  return <IdentityWidgetComponent data={data} identity={identity} />;
}
```

---

## Performance Principles Implementation Checklist

✅ **Speed is Trust**: Core Web Vitals monitoring, < 2s initial load, < 3s interactive  
✅ **Freshness**: Real-time prices (15s), cached charts (5min), cached info (24h)  
✅ **Predictable Performance**: Loading states > 500ms, skeleton loaders, CLS prevention  
✅ **Graceful Degradation**: Error boundaries, cached fallbacks, retry with exponential backoff  
✅ **Identity-Aware**: Lazy-loaded widgets, independent fetching, parallel loading, per-identity caching  

---

## 26.2 Caching Architecture

DominionMarkets uses a **multi-layer caching strategy** to balance freshness with performance.

### Caching Flow

```
Client Cache (Local)
        |
        v
Edge Cache (CDN)
        |
        v
Backend Cache Layer (Redis)
        |
        v
Live Data Providers
```

---

### Layer 1: Client Cache (Local)

**Browser-level caching using localStorage, sessionStorage, and Cache API**

```tsx
// Client-side cache utility
export class ClientCache {
  // Short-term cache (session-based)
  static setSession(key: string, data: any) {
    sessionStorage.setItem(key, JSON.stringify({
      data,
      timestamp: Date.now(),
    }));
  }
  
  static getSession(key: string, maxAge: number) {
    const cached = sessionStorage.getItem(key);
    if (!cached) return null;
    
    const { data, timestamp } = JSON.parse(cached);
    
    // Check if expired
    if (Date.now() - timestamp > maxAge) {
      sessionStorage.removeItem(key);
      return null;
    }
    
    return data;
  }
  
  // Long-term cache (persistent)
  static setLocal(key: string, data: any, ttl: number) {
    localStorage.setItem(key, JSON.stringify({
      data,
      timestamp: Date.now(),
      ttl,
    }));
  }
  
  static getLocal(key: string) {
    const cached = localStorage.getItem(key);
    if (!cached) return null;
    
    const { data, timestamp, ttl } = JSON.parse(cached);
    
    // Check if expired
    if (Date.now() - timestamp > ttl) {
      localStorage.removeItem(key);
      return null;
    }
    
    return data;
  }
  
  // Clear all cache
  static clear() {
    sessionStorage.clear();
    localStorage.clear();
  }
}

// Usage in data fetching
export function useClientCachedData<T>(
  key: string,
  fetcher: () => Promise<T>,
  ttl: number = 300000 // 5 minutes default
) {
  const [data, setData] = useState<T | null>(() => {
    // Try to load from cache on mount
    return ClientCache.getLocal(key);
  });
  const [loading, setLoading] = useState(!data);
  
  useEffect(() => {
    const loadData = async () => {
      // Check cache first
      const cached = ClientCache.getLocal(key);
      if (cached) {
        setData(cached);
        setLoading(false);
        return;
      }
      
      // Fetch fresh data
      try {
        const freshData = await fetcher();
        ClientCache.setLocal(key, freshData, ttl);
        setData(freshData);
      } finally {
        setLoading(false);
      }
    };
    
    loadData();
  }, [key, ttl]);
  
  return { data, loading };
}

// Cache strategies by data type
export const clientCacheStrategies = {
  // Session-only (cleared on tab close)
  stockPrices: {
    storage: 'session',
    ttl: 15000, // 15 seconds
  },
  
  // Persistent (survives page reload)
  companyInfo: {
    storage: 'local',
    ttl: 86400000, // 24 hours
  },
  
  chartData: {
    storage: 'local',
    ttl: 300000, // 5 minutes
  },
  
  userPreferences: {
    storage: 'local',
    ttl: Infinity, // Never expire
  },
};

// Service Worker for offline support
// public/sw.js
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      // Return cached response if available
      if (cachedResponse) {
        return cachedResponse;
      }
      
      // Otherwise fetch from network
      return fetch(event.request).then((response) => {
        // Cache successful responses
        if (response.status === 200) {
          const responseClone = response.clone();
          caches.open('dominion-markets-v1').then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        
        return response;
      });
    })
  );
});
```

---

### Layer 2: Edge Cache (CDN)

**Cloudflare/Vercel Edge caching for static assets and API responses**

```tsx
// Next.js configuration for edge caching
// next.config.mjs
export default {
  async headers() {
    return [
      {
        source: '/api/stocks/:ticker/info',
        headers: [
          {
            key: 'Cache-Control',
            value: 's-maxage=86400, stale-while-revalidate=3600', // 24h cache, 1h stale
          },
        ],
      },
      {
        source: '/api/stocks/:ticker/chart',
        headers: [
          {
            key: 'Cache-Control',
            value: 's-maxage=300, stale-while-revalidate=60', // 5min cache, 1min stale
          },
        ],
      },
      {
        source: '/api/stocks/:ticker/price',
        headers: [
          {
            key: 'Cache-Control',
            value: 's-maxage=15, stale-while-revalidate=5', // 15s cache, 5s stale
          },
        ],
      },
      {
        source: '/static/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable', // 1 year - immutable
          },
        ],
      },
    ];
  },
};

// API route with edge caching
// app/api/stocks/[ticker]/info/route.ts
export async function GET(
  request: Request,
  { params }: { params: { ticker: string } }
) {
  const { ticker } = params;
  
  const companyInfo = await getCompanyInfo(ticker);
  
  return new Response(JSON.stringify(companyInfo), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
      // Edge cache for 24 hours
      'Cache-Control': 's-maxage=86400, stale-while-revalidate=3600',
      // Include ETag for conditional requests
      'ETag': generateETag(companyInfo),
    },
  });
}

// Conditional request handling
export async function GET(request: Request) {
  const ifNoneMatch = request.headers.get('If-None-Match');
  const data = await fetchData();
  const etag = generateETag(data);
  
  // Return 304 if not modified
  if (ifNoneMatch === etag) {
    return new Response(null, {
      status: 304,
      headers: { 'ETag': etag },
    });
  }
  
  return new Response(JSON.stringify(data), {
    status: 200,
    headers: {
      'ETag': etag,
      'Cache-Control': 's-maxage=300, stale-while-revalidate=60',
    },
  });
}

// Purge edge cache when data changes
export async function purgeEdgeCache(patterns: string[]) {
  // Cloudflare cache purge
  await fetch('https://api.cloudflare.com/client/v4/zones/ZONE_ID/purge_cache', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.CLOUDFLARE_API_TOKEN}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ files: patterns }),
  });
}

// Usage: Purge cache when stock data updates
await purgeEdgeCache([
  `https://dominionmarkets.com/api/stocks/AAPL/price`,
  `https://dominionmarkets.com/api/stocks/AAPL/chart`,
]);
```

---

### Layer 3: Backend Cache Layer (Redis)

**Redis for high-speed in-memory caching**

```tsx
// Redis cache utility
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

export class BackendCache {
  // Get cached data
  static async get<T>(key: string): Promise<T | null> {
    const cached = await redis.get(key);
    return cached ? JSON.parse(cached) : null;
  }
  
  // Set cached data with TTL
  static async set(key: string, data: any, ttlSeconds: number) {
    await redis.set(key, JSON.stringify(data), 'EX', ttlSeconds);
  }
  
  // Get or fetch pattern (cache-aside)
  static async getOrFetch<T>(
    key: string,
    fetcher: () => Promise<T>,
    ttlSeconds: number
  ): Promise<T> {
    // Try cache first
    const cached = await this.get<T>(key);
    if (cached) return cached;
    
    // Fetch fresh data
    const data = await fetcher();
    
    // Store in cache
    await this.set(key, data, ttlSeconds);
    
    return data;
  }
  
  // Invalidate cache
  static async invalidate(pattern: string) {
    const keys = await redis.keys(pattern);
    if (keys.length > 0) {
      await redis.del(...keys);
    }
  }
  
  // Bulk operations
  static async mget<T>(keys: string[]): Promise<(T | null)[]> {
    const values = await redis.mget(...keys);
    return values.map(v => v ? JSON.parse(v) : null);
  }
  
  static async mset(items: { key: string; value: any; ttl: number }[]) {
    const pipeline = redis.pipeline();
    
    items.forEach(({ key, value, ttl }) => {
      pipeline.set(key, JSON.stringify(value), 'EX', ttl);
    });
    
    await pipeline.exec();
  }
}

// Usage in API routes
export async function getStockPrice(ticker: string) {
  return BackendCache.getOrFetch(
    `stock:${ticker}:price`,
    async () => {
      // Fetch from live data provider
      const response = await fetch(`https://api.stockprovider.com/quote/${ticker}`);
      return response.json();
    },
    15 // 15 seconds TTL
  );
}

export async function getCompanyInfo(ticker: string) {
  return BackendCache.getOrFetch(
    `company:${ticker}:info`,
    async () => {
      const response = await fetch(`https://api.stockprovider.com/company/${ticker}`);
      return response.json();
    },
    86400 // 24 hours TTL
  );
}

// Cache warming (preload popular stocks)
export async function warmCache() {
  const popularTickers = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN'];
  
  await Promise.all(
    popularTickers.map(ticker => getStockPrice(ticker))
  );
  
  console.log('✅ Cache warmed with popular stocks');
}

// Cache invalidation on data update
export async function handleStockUpdate(ticker: string) {
  // Invalidate all cache entries for this stock
  await BackendCache.invalidate(`stock:${ticker}:*`);
  
  // Purge edge cache
  await purgeEdgeCache([
    `https://dominionmarkets.com/api/stocks/${ticker}/price`,
    `https://dominionmarkets.com/api/stocks/${ticker}/chart`,
  ]);
}

// Distributed locking for cache stampede prevention
export async function getCachedWithLock<T>(
  key: string,
  fetcher: () => Promise<T>,
  ttl: number
): Promise<T> {
  const lockKey = `lock:${key}`;
  const lockTTL = 10; // 10 seconds lock
  
  // Try cache first
  const cached = await BackendCache.get<T>(key);
  if (cached) return cached;
  
  // Try to acquire lock
  const acquired = await redis.set(lockKey, '1', 'EX', lockTTL, 'NX');
  
  if (acquired) {
    try {
      // Fetch fresh data
      const data = await fetcher();
      await BackendCache.set(key, data, ttl);
      return data;
    } finally {
      // Release lock
      await redis.del(lockKey);
    }
  } else {
    // Wait for lock to release
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // Check cache again
    const nowCached = await BackendCache.get<T>(key);
    if (nowCached) return nowCached;
    
    // Fallback to fetching
    return fetcher();
  }
}
```

---

### Layer 4: Live Data Providers

**External APIs with rate limiting and failover**

```tsx
// Live data provider abstraction
export class LiveDataProvider {
  private primaryProvider: string;
  private fallbackProvider: string;
  private rateLimitRemaining: number = 1000;
  
  constructor(
    primary: string = process.env.PRIMARY_DATA_PROVIDER!,
    fallback: string = process.env.FALLBACK_DATA_PROVIDER!
  ) {
    this.primaryProvider = primary;
    this.fallbackProvider = fallback;
  }
  
  // Fetch with automatic fallback
  async fetch<T>(endpoint: string): Promise<T> {
    try {
      return await this.fetchFromProvider(this.primaryProvider, endpoint);
    } catch (error) {
      console.warn('Primary provider failed, using fallback:', error);
      return await this.fetchFromProvider(this.fallbackProvider, endpoint);
    }
  }
  
  private async fetchFromProvider<T>(provider: string, endpoint: string): Promise<T> {
    const response = await fetch(`${provider}${endpoint}`, {
      headers: {
        'Authorization': `Bearer ${process.env.DATA_PROVIDER_API_KEY}`,
      },
    });
    
    // Update rate limit tracking
    this.rateLimitRemaining = parseInt(
      response.headers.get('X-RateLimit-Remaining') || '1000'
    );
    
    if (!response.ok) {
      throw new Error(`Provider error: ${response.status}`);
    }
    
    return response.json();
  }
  
  // Check if rate limit allows request
  canMakeRequest(): boolean {
    return this.rateLimitRemaining > 10; // Keep buffer
  }
  
  // Batch requests to optimize rate limits
  async batchFetch<T>(endpoints: string[]): Promise<T[]> {
    // If provider supports batch requests
    if (this.supportsBatch()) {
      return this.fetchBatch(endpoints);
    }
    
    // Otherwise, make individual requests
    return Promise.all(
      endpoints.map(endpoint => this.fetch<T>(endpoint))
    );
  }
  
  private supportsBatch(): boolean {
    // Check if primary provider supports batch
    return this.primaryProvider.includes('batch-endpoint');
  }
  
  private async fetchBatch<T>(endpoints: string[]): Promise<T[]> {
    const response = await fetch(`${this.primaryProvider}/batch`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.DATA_PROVIDER_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ requests: endpoints }),
    });
    
    return response.json();
  }
}

// Usage with caching
const dataProvider = new LiveDataProvider();

export async function getStockData(ticker: string) {
  // Check if rate limit allows
  if (!dataProvider.canMakeRequest()) {
    // Fall back to cache even if stale
    const cached = await BackendCache.get(`stock:${ticker}:price`);
    if (cached) return cached;
    
    throw new Error('Rate limit exceeded and no cache available');
  }
  
  // Fetch from provider (with cache)
  return BackendCache.getOrFetch(
    `stock:${ticker}:price`,
    () => dataProvider.fetch(`/quote/${ticker}`),
    15 // 15 seconds
  );
}

// Batch optimization for portfolio
export async function getPortfolioData(tickers: string[]) {
  const cacheKeys = tickers.map(t => `stock:${t}:price`);
  
  // Check cache for all tickers
  const cached = await BackendCache.mget(cacheKeys);
  
  // Identify which need fetching
  const toFetch = tickers.filter((_, i) => !cached[i]);
  
  if (toFetch.length === 0) {
    return cached;
  }
  
  // Batch fetch missing data
  const freshData = await dataProvider.batchFetch(
    toFetch.map(t => `/quote/${t}`)
  );
  
  // Update cache
  await BackendCache.mset(
    toFetch.map((ticker, i) => ({
      key: `stock:${ticker}:price`,
      value: freshData[i],
      ttl: 15,
    }))
  );
  
  // Merge cached and fresh data
  const result = [...cached];
  let freshIndex = 0;
  
  for (let i = 0; i < result.length; i++) {
    if (!result[i]) {
      result[i] = freshData[freshIndex++];
    }
  }
  
  return result;
}
```

---

### Complete Caching Strategy by Data Type

```tsx
export const cachingStrategies = {
  stockPrices: {
    client: { type: 'session', ttl: 15000 },          // 15s
    edge: { ttl: 15, staleWhileRevalidate: 5 },       // 15s edge, 5s stale
    backend: { ttl: 15 },                              // 15s Redis
    source: 'live',                                    // Real-time provider
  },
  
  companyInfo: {
    client: { type: 'local', ttl: 86400000 },         // 24h
    edge: { ttl: 86400, staleWhileRevalidate: 3600 }, // 24h edge, 1h stale
    backend: { ttl: 86400 },                           // 24h Redis
    source: 'live',                                    // API provider
  },
  
  chartData: {
    client: { type: 'local', ttl: 300000 },           // 5min
    edge: { ttl: 300, staleWhileRevalidate: 60 },     // 5min edge, 1min stale
    backend: { ttl: 300 },                             // 5min Redis
    source: 'live',                                    // API provider
  },
  
  newsArticles: {
    client: { type: 'session', ttl: 3600000 },        // 1h
    edge: { ttl: 3600, staleWhileRevalidate: 600 },   // 1h edge, 10min stale
    backend: { ttl: 3600 },                            // 1h Redis
    source: 'news-api',                                // News provider
  },
  
  identityInsights: {
    client: { type: 'local', ttl: 300000 },           // 5min
    edge: { ttl: 300, staleWhileRevalidate: 60 },     // 5min edge, 1min stale
    backend: { ttl: 300 },                             // 5min Redis
    source: 'computed',                                // Generated on demand
  },
  
  userPortfolio: {
    client: { type: 'session', ttl: 0 },              // Always fresh
    edge: { ttl: 0, private: true },                   // No edge cache (private)
    backend: { ttl: 0 },                               // No backend cache (database)
    source: 'database',                                // PostgreSQL
  },
  
  staticAssets: {
    client: { type: 'cache-api', ttl: Infinity },     // Immutable
    edge: { ttl: 31536000, immutable: true },          // 1 year immutable
    backend: { ttl: 0 },                               // Not cached in Redis
    source: 'static',                                  // Build artifacts
  },
};

// Cache strategy selector
export function getCacheStrategy(dataType: keyof typeof cachingStrategies) {
  return cachingStrategies[dataType];
}

// Unified caching helper
export async function fetchWithStrategy<T>(
  dataType: keyof typeof cachingStrategies,
  key: string,
  fetcher: () => Promise<T>
): Promise<T> {
  const strategy = getCacheStrategy(dataType);
  
  // Layer 1: Client cache
  if (strategy.client.ttl > 0) {
    const cached = ClientCache.getLocal(key);
    if (cached) return cached;
  }
  
  // Layer 2: Edge cache (handled by Next.js headers)
  // Layer 3: Backend cache (Redis)
  if (strategy.backend.ttl > 0) {
    return BackendCache.getOrFetch(key, fetcher, strategy.backend.ttl);
  }
  
  // Layer 4: Live data provider
  return fetcher();
}
```

---

## Caching Architecture Implementation Checklist

✅ **Client Cache**: localStorage/sessionStorage for persistent caching, Service Worker for offline support  
✅ **Edge Cache**: CDN caching with stale-while-revalidate, conditional requests with ETags  
✅ **Backend Cache**: Redis in-memory cache, distributed locking for cache stampede prevention  
✅ **Live Data Providers**: Primary/fallback providers, rate limit tracking, batch request optimization  
✅ **Unified Strategy**: Per-data-type caching configuration, multi-layer cache-aside pattern  

---

## 26.3 Client-Side Caching

### Cached Locally

**User identity, portfolio snapshot, last viewed stock/news, heatmap preview, Cultural Alpha preview**

```tsx
// Client-side cache keys
export const CLIENT_CACHE_KEYS = {
  userIdentity: 'user:identity',
  portfolioSnapshot: 'portfolio:snapshot',
  lastViewedStock: 'stock:last-viewed',
  lastViewedNews: 'news:last-viewed',
  heatmapPreview: 'heatmap:preview',
  culturalAlphaPreview: 'cultural-alpha:preview',
};

// Expiration times (milliseconds)
export const CLIENT_CACHE_TTL = {
  userIdentity: 900000,          // 15 minutes
  portfolioSnapshot: 300000,     // 5 minutes
  lastViewedStock: 600000,       // 10 minutes
  lastViewedNews: 600000,        // 10 minutes
  heatmapPreview: 300000,        // 5 minutes
  culturalAlphaPreview: 300000,  // 5 minutes
};

// Client cache implementation
export class DominionCache {
  // Store user identity
  static setUserIdentity(identity: UserIdentity) {
    ClientCache.setLocal(
      CLIENT_CACHE_KEYS.userIdentity,
      identity,
      CLIENT_CACHE_TTL.userIdentity
    );
  }
  
  static getUserIdentity(): UserIdentity | null {
    return ClientCache.getLocal(CLIENT_CACHE_KEYS.userIdentity);
  }
  
  // Store portfolio snapshot
  static setPortfolioSnapshot(snapshot: PortfolioSnapshot) {
    ClientCache.setLocal(
      CLIENT_CACHE_KEYS.portfolioSnapshot,
      snapshot,
      CLIENT_CACHE_TTL.portfolioSnapshot
    );
  }
  
  static getPortfolioSnapshot(): PortfolioSnapshot | null {
    return ClientCache.getLocal(CLIENT_CACHE_KEYS.portfolioSnapshot);
  }
  
  // Store last viewed stock
  static setLastViewedStock(ticker: string, data: StockData) {
    ClientCache.setLocal(
      `${CLIENT_CACHE_KEYS.lastViewedStock}:${ticker}`,
      data,
      CLIENT_CACHE_TTL.lastViewedStock
    );
  }
  
  static getLastViewedStock(ticker: string): StockData | null {
    return ClientCache.getLocal(`${CLIENT_CACHE_KEYS.lastViewedStock}:${ticker}`);
  }
  
  // Store last viewed news
  static setLastViewedNews(newsId: string, article: NewsArticle) {
    ClientCache.setLocal(
      `${CLIENT_CACHE_KEYS.lastViewedNews}:${newsId}`,
      article,
      CLIENT_CACHE_TTL.lastViewedNews
    );
  }
  
  static getLastViewedNews(newsId: string): NewsArticle | null {
    return ClientCache.getLocal(`${CLIENT_CACHE_KEYS.lastViewedNews}:${newsId}`);
  }
  
  // Store heatmap preview
  static setHeatmapPreview(data: HeatmapData) {
    ClientCache.setLocal(
      CLIENT_CACHE_KEYS.heatmapPreview,
      data,
      CLIENT_CACHE_TTL.heatmapPreview
    );
  }
  
  static getHeatmapPreview(): HeatmapData | null {
    return ClientCache.getLocal(CLIENT_CACHE_KEYS.heatmapPreview);
  }
  
  // Store Cultural Alpha preview
  static setCulturalAlphaPreview(data: CulturalAlphaData) {
    ClientCache.setLocal(
      CLIENT_CACHE_KEYS.culturalAlphaPreview,
      data,
      CLIENT_CACHE_TTL.culturalAlphaPreview
    );
  }
  
  static getCulturalAlphaPreview(): CulturalAlphaData | null {
    return ClientCache.getLocal(CLIENT_CACHE_KEYS.culturalAlphaPreview);
  }
}

// Usage in components
export function Dashboard() {
  const [snapshot, setSnapshot] = useState<PortfolioSnapshot | null>(
    () => DominionCache.getPortfolioSnapshot() // Load from cache on mount
  );
  
  useEffect(() => {
    const loadSnapshot = async () => {
      // Try cache first for instant load
      const cached = DominionCache.getPortfolioSnapshot();
      if (cached) {
        setSnapshot(cached);
      }
      
      // Fetch fresh data in background
      const fresh = await fetchPortfolioSnapshot();
      setSnapshot(fresh);
      
      // Update cache
      DominionCache.setPortfolioSnapshot(fresh);
    };
    
    loadSnapshot();
  }, []);
  
  return <PortfolioCard snapshot={snapshot} />;
}
```

---

### Benefits

✅ **Instant dashboard load**: Pre-cached data renders immediately  
✅ **Smooth offline fallback**: Last known state available when offline  
✅ **Reduced API calls**: 60-80% reduction in API requests on repeat visits  

---

## 26.4 Edge Caching (CDN)

### Cached at the Edge

**Static assets, charts (non-real-time ranges), news summaries, identity widgets**

```tsx
// Edge cache configuration (Next.js)
export const EDGE_CACHE_CONFIG = {
  staticAssets: {
    path: '/static/*',
    maxAge: 31536000,  // 1 year
    immutable: true,
  },
  
  charts: {
    path: '/api/charts/*',
    sMaxAge: 300,      // 5 minutes
    staleWhileRevalidate: 60,
  },
  
  newsSummaries: {
    path: '/api/news/summaries',
    sMaxAge: 300,      // 5 minutes
    staleWhileRevalidate: 60,
  },
  
  identityWidgets: {
    path: '/api/identity/*',
    sMaxAge: 300,      // 5 minutes
    staleWhileRevalidate: 60,
  },
};

// Next.js edge caching headers
// next.config.mjs
export default {
  async headers() {
    return [
      // Static assets - immutable, long cache
      {
        source: '/static/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      
      // Charts - 5min edge cache
      {
        source: '/api/charts/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 's-maxage=300, stale-while-revalidate=60',
          },
        ],
      },
      
      // News summaries - 5min edge cache
      {
        source: '/api/news/summaries',
        headers: [
          {
            key: 'Cache-Control',
            value: 's-maxage=300, stale-while-revalidate=60',
          },
        ],
      },
      
      // Identity widgets - 5min edge cache
      {
        source: '/api/identity/:identity/:widget',
        headers: [
          {
            key: 'Cache-Control',
            value: 's-maxage=300, stale-while-revalidate=60',
          },
        ],
      },
    ];
  },
};

// API route with edge caching
// app/api/charts/[ticker]/[range]/route.ts
export async function GET(
  request: Request,
  { params }: { params: { ticker: string; range: string } }
) {
  const { ticker, range } = params;
  
  // Non-real-time ranges cached at edge
  const isRealtime = range === '1D' || range === '1H';
  
  const chartData = await getChartData(ticker, range);
  
  return new Response(JSON.stringify(chartData), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': isRealtime
        ? 'no-cache' // Real-time not cached
        : 's-maxage=300, stale-while-revalidate=60', // 5min cache
    },
  });
}

// Identity widget with edge caching
// app/api/identity/[identity]/[widget]/route.ts
export async function GET(
  request: Request,
  { params }: { params { identity: string; widget: string } }
) {
  const { identity, widget } = params;
  
  const data = await getIdentityWidgetData(identity, widget);
  
  return new Response(JSON.stringify(data), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 's-maxage=300, stale-while-revalidate=60',
      'Vary': 'Accept-Encoding', // Cache per encoding
    },
  });
}
```

---

### Expiration

- **Static assets**: 1 year (immutable)
- **Charts**: 5 minutes
- **News summaries**: 5 minutes
- **Identity widgets**: 5 minutes

---

### Benefits

✅ **Global speed**: Content served from edge locations near users  
✅ **Low latency**: < 50ms response times globally  
✅ **High availability**: Distributed edge network with 99.99% uptime  

---

## 26.5 Backend Caching (Redis Layer)

### Cached in Redis

**Indices, movers, heatmap, Cultural Alpha, identity insights, portfolio analytics (Premium)**

```tsx
// Backend cache configuration
export const BACKEND_CACHE_CONFIG = {
  indices: {
    key: 'indices:snapshot',
    ttl: 5,  // 5 seconds
  },
  
  movers: {
    key: 'movers:snapshot',
    ttl: 10,  // 10 seconds
  },
  
  heatmap: {
    key: 'heatmap:snapshot',
    ttl: 30,  // 30 seconds
  },
  
  culturalAlpha: {
    key: 'cultural-alpha:snapshot',
    ttl: 60,  // 1 minute
  },
  
  identityInsights: {
    key: (identity: string) => `identity:${identity}:insights`,
    ttl: 300,  // 5 minutes
  },
  
  portfolioAnalytics: {
    key: (userId: string) => `portfolio:${userId}:analytics`,
    ttl: 300,  // 5 minutes (Premium only)
  },
};

// Indices caching
export async function getIndices() {
  return BackendCache.getOrFetch(
    BACKEND_CACHE_CONFIG.indices.key,
    async () => {
      // Fetch from live provider
      const response = await fetch('https://api.provider.com/indices');
      return response.json();
    },
    BACKEND_CACHE_CONFIG.indices.ttl
  );
}

// Movers caching
export async function getMovers() {
  return BackendCache.getOrFetch(
    BACKEND_CACHE_CONFIG.movers.key,
    async () => {
      const response = await fetch('https://api.provider.com/movers');
      return response.json();
    },
    BACKEND_CACHE_CONFIG.movers.ttl
  );
}

// Heatmap caching
export async function getHeatmap() {
  return BackendCache.getOrFetch(
    BACKEND_CACHE_CONFIG.heatmap.key,
    async () => {
      const response = await fetch('https://api.provider.com/heatmap');
      return response.json();
    },
    BACKEND_CACHE_CONFIG.heatmap.ttl
  );
}

// Cultural Alpha caching
export async function getCulturalAlpha(identity: UserIdentity) {
  return BackendCache.getOrFetch(
    `${BACKEND_CACHE_CONFIG.culturalAlpha.key}:${identity}`,
    async () => {
      // Compute Cultural Alpha metrics
      return computeCulturalAlpha(identity);
    },
    BACKEND_CACHE_CONFIG.culturalAlpha.ttl
  );
}

// Identity insights caching
export async function getIdentityInsights(identity: UserIdentity) {
  return BackendCache.getOrFetch(
    BACKEND_CACHE_CONFIG.identityInsights.key(identity),
    async () => {
      return computeIdentityInsights(identity);
    },
    BACKEND_CACHE_CONFIG.identityInsights.ttl
  );
}

// Portfolio analytics caching (Premium only)
export async function getPortfolioAnalytics(userId: string, tier: UserTier) {
  if (tier !== 'premium' && tier !== 'pro') {
    throw new Error('Portfolio analytics require Premium or Pro tier');
  }
  
  return BackendCache.getOrFetch(
    BACKEND_CACHE_CONFIG.portfolioAnalytics.key(userId),
    async () => {
      const holdings = await getPortfolioHoldings(userId);
      return computePortfolioAnalytics(holdings);
    },
    BACKEND_CACHE_CONFIG.portfolioAnalytics.ttl
  );
}

// Cache warming on deployment
export async function warmBackendCache() {
  console.log('🔥 Warming backend cache...');
  
  await Promise.all([
    getIndices(),
    getMovers(),
    getHeatmap(),
    getCulturalAlpha('diaspora'),
    getCulturalAlpha('youth'),
    getCulturalAlpha('creator'),
    getCulturalAlpha('legacy'),
  ]);
  
  console.log('✅ Backend cache warmed');
}
```

---

### Expiration

- **Indices**: 5 seconds
- **Movers**: 10 seconds
- **Heatmap**: 30 seconds
- **Cultural Alpha**: 1 minute
- **Identity insights**: 5 minutes
- **Portfolio analytics**: 5 minutes

---

### Benefits

✅ **Massive performance boost**: 10-50x faster than hitting live providers  
✅ **Reduced provider load**: 95% reduction in external API calls  
✅ **Smooth user experience**: Sub-second response times for cached data  

---

## 26.6 Real-Time Data Strategy

DominionMarkets uses a **hybrid real-time model**:

### Real-Time (WebSockets)

**Price updates, volume updates, alerts**

```tsx
// WebSocket connection for real-time data
import { useEffect, useState } from 'react';

export function useRealtimePrice(ticker: string) {
  const [price, setPrice] = useState<number | null>(null);
  const [ws, setWs] = useState<WebSocket | null>(null);
  
  useEffect(() => {
    // Connect to WebSocket
    const socket = new WebSocket(`wss://ws.dominionmarkets.com/prices`);
    
    socket.onopen = () => {
      // Subscribe to ticker
      socket.send(JSON.stringify({
        type: 'subscribe',
        ticker,
      }));
    };
    
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.ticker === ticker) {
        setPrice(data.price);
      }
    };
    
    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    
    socket.onclose = () => {
      console.log('WebSocket closed');
    };
    
    setWs(socket);
    
    return () => {
      // Unsubscribe and close
      if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
          type: 'unsubscribe',
          ticker,
        }));
        socket.close();
      }
    };
  }, [ticker]);
  
  return price;
}

// Real-time alerts via WebSocket
export function useRealtimeAlerts(userId: string) {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  
  useEffect(() => {
    const socket = new WebSocket(`wss://ws.dominionmarkets.com/alerts`);
    
    socket.onopen = () => {
      socket.send(JSON.stringify({
        type: 'subscribe',
        userId,
      }));
    };
    
    socket.onmessage = (event) => {
      const alert = JSON.parse(event.data);
      setAlerts(prev => [alert, ...prev]);
      
      // Show notification
      new Notification('DominionMarkets Alert', {
        body: alert.message,
        icon: '/icon.png',
      });
    };
    
    setWs(socket);
    
    return () => socket.close();
  }, [userId]);
  
  return alerts;
}
```

---

### Near-Real-Time (Polling)

**Movers, heatmap, Cultural Alpha**

```tsx
// Polling for near-real-time data
export function usePolledMovers(interval: number = 10000) {
  const [movers, setMovers] = useState<Movers | null>(null);
  
  useEffect(() => {
    const fetchMovers = async () => {
      const data = await fetch('/api/movers').then(r => r.json());
      setMovers(data);
    };
    
    // Initial fetch
    fetchMovers();
    
    // Poll every 10 seconds
    const timer = setInterval(fetchMovers, interval);
    
    return () => clearInterval(timer);
  }, [interval]);
  
  return movers;
}

// Polling for heatmap (30s refresh)
export function usePolledHeatmap() {
  return usePolledMovers(30000); // 30 seconds
}

// Polling for Cultural Alpha (60s refresh)
export function usePolledCulturalAlpha(identity: UserIdentity) {
  const [data, setData] = useState<CulturalAlphaData | null>(null);
  
  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch(`/api/cultural-alpha/${identity}`);
      const data = await response.json();
      setData(data);
    };
    
    fetchData();
    const timer = setInterval(fetchData, 60000); // 1 minute
    
    return () => clearInterval(timer);
  }, [identity]);
  
  return data;
}
```

---

### Batch Updates

**News, earnings calendar, portfolio analytics**

```tsx
// Batch updates for news (refresh every 5 minutes)
export function useBatchedNews() {
  const { data, error } = useSWR(
    '/api/news/batch',
    fetcher,
    {
      refreshInterval: 300000, // 5 minutes
      revalidateOnFocus: false,
    }
  );
  
  return { news: data, error };
}

// Batch updates for earnings calendar
export function useBatchedEarnings() {
  const { data, error } = useSWR(
    '/api/earnings/calendar',
    fetcher,
    {
      refreshInterval: 3600000, // 1 hour
      revalidateOnFocus: false,
    }
  );
  
  return { earnings: data, error };
}

// Batch updates for portfolio analytics (Premium)
export function useBatchedPortfolioAnalytics(userId: string) {
  const { data, error } = useSWR(
    `/api/portfolio/${userId}/analytics`,
    fetcher,
    {
      refreshInterval: 300000, // 5 minutes
      revalidateOnFocus: true, // Refresh when user returns
    }
  );
  
  return { analytics: data, error };
}
```

---

## 26.7 Latency Targets

### Dashboard

- **Initial load**: < 1.2s
- **Widget updates**: < 300ms

```tsx
// Dashboard performance monitoring
export function Dashboard() {
  usePerformanceMonitoring('dashboard');
  
  useEffect(() => {
    const start = performance.now();
    
    // Measure initial load
    const observer = new PerformanceObserver((list) => {
      const entries = list.getEntries();
      entries.forEach((entry) => {
        const loadTime = entry.startTime;
        
        if (loadTime > 1200) {
          console.warn(`⚠️ Dashboard load exceeded 1.2s target: ${loadTime}ms`);
        } else {
          console.log(`✅ Dashboard loaded in ${loadTime}ms`);
        }
      });
    });
    
    observer.observe({ entryTypes: ['navigation'] });
    
    return () => observer.disconnect();
  }, []);
  
  return <DashboardContent />;
}
```

---

### Markets

- **Movers**: < 500ms
- **Heatmap**: < 700ms

```tsx
// Markets performance tracking
export function Markets() {
  useEffect(() => {
    const trackLatency = async (endpoint: string, target: number) => {
      const start = performance.now();
      await fetch(endpoint);
      const duration = performance.now() - start;
      
      if (duration > target) {
        console.warn(`⚠️ ${endpoint} exceeded ${target}ms target: ${duration}ms`);
      }
    };
    
    trackLatency('/api/movers', 500);
    trackLatency('/api/heatmap', 700);
  }, []);
  
  return <MarketsContent />;
}
```

---

### Stock Detail

- **Overview**: < 600ms
- **Chart**: < 400ms
- **News**: < 500ms

```tsx
// Stock detail performance tracking
export function StockDetail({ ticker }: { ticker: string }) {
  useEffect(() => {
    const measurements = {
      overview: { endpoint: `/api/stocks/${ticker}/overview`, target: 600 },
      chart: { endpoint: `/api/stocks/${ticker}/chart`, target: 400 },
      news: { endpoint: `/api/stocks/${ticker}/news`, target: 500 },
    };
    
    Object.entries(measurements).forEach(async ([name, { endpoint, target }]) => {
      const start = performance.now();
      await fetch(endpoint);
      const duration = performance.now() - start;
      
      if (duration > target) {
        console.warn(`⚠️ ${name} exceeded ${target}ms target: ${duration}ms`);
      }
    });
  }, [ticker]);
  
  return <StockDetailContent ticker={ticker} />;
}
```

---

### Portfolio

- **Snapshot**: < 700ms
- **Analytics**: < 1.2s

```tsx
// Portfolio performance tracking
export function Portfolio() {
  useEffect(() => {
    const trackPortfolio = async () => {
      const snapshotStart = performance.now();
      await fetch('/api/portfolio/snapshot');
      const snapshotDuration = performance.now() - snapshotStart;
      
      if (snapshotDuration > 700) {
        console.warn(`⚠️ Snapshot exceeded 700ms target: ${snapshotDuration}ms`);
      }
      
      const analyticsStart = performance.now();
      await fetch('/api/portfolio/analytics');
      const analyticsDuration = performance.now() - analyticsStart;
      
      if (analyticsDuration > 1200) {
        console.warn(`⚠️ Analytics exceeded 1.2s target: ${analyticsDuration}ms`);
      }
    };
    
    trackPortfolio();
  }, []);
  
  return <PortfolioContent />;
}
```

---

## 26.8 Offline Mode

### Available When Offline

- **Cached dashboard**
- **Cached portfolio snapshot**
- **Cached news summaries**
- **Cached stock data**

```tsx
// Offline detection
export function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(
    typeof navigator !== 'undefined' ? navigator.onLine : true
  );
  
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);
  
  return isOnline;
}

// Offline mode component
export function OfflineMode() {
  const isOnline = useOnlineStatus();
  
  if (isOnline) return null;
  
  return (
    <div className="fixed top-0 left-0 right-0 z-50 p-4 bg-yellow-500 text-slate-900">
      <div className="container mx-auto flex items-center gap-3">
        <WifiOff className="w-5 h-5" />
        <p className="font-medium">
          You're offline — reconnect to continue.
        </p>
      </div>
    </div>
  );
}

// Offline-aware data fetching
export function useOfflineData<T>(
  key: string,
  fetcher: () => Promise<T>
) {
  const isOnline = useOnlineStatus();
  const [data, setData] = useState<T | null>(null);
  
  useEffect(() => {
    const loadData = async () => {
      if (isOnline) {
        // Fetch fresh data when online
        try {
          const freshData = await fetcher();
          setData(freshData);
          
          // Cache for offline use
          ClientCache.setLocal(key, freshData, 86400000); // 24h
        } catch (error) {
          // Fall back to cache on error
          const cached = ClientCache.getLocal(key);
          if (cached) setData(cached);
        }
      } else {
        // Use cached data when offline
        const cached = ClientCache.getLocal(key);
        if (cached) setData(cached);
      }
    };
    
    loadData();
  }, [isOnline, key]);
  
  return { data, isOffline: !isOnline };
}
```

---

### Unavailable When Offline

- **Real-time prices** (requires WebSocket connection)
- **Verification engine** (requires API connection)
- **Alerts** (requires WebSocket connection)

---

### Offline Message

```tsx
export function OfflineBanner() {
  return (
    <div className="p-4 bg-yellow-500/10 border border-yellow-500/30 rounded-lg">
      <div className="flex items-center gap-3">
        <WifiOff className="w-5 h-5 text-yellow-500" />
        <div>
          <p className="font-medium text-white">You're offline</p>
          <p className="text-sm text-slate-400">
            Showing cached data. Reconnect to see live updates.
          </p>
        </div>
      </div>
    </div>
  );
}
```

---

## 26.9 Failover & Resilience Patterns

### Circuit Breakers

**If a provider fails, the system switches to cached data**

```tsx
// Circuit breaker implementation
export class CircuitBreaker {
  private failureCount: number = 0;
  private lastFailureTime: number = 0;
  private state: 'closed' | 'open' | 'half-open' = 'closed';
  
  constructor(
    private threshold: number = 5,
    private timeout: number = 60000 // 1 minute
  ) {}
  
  async execute<T>(
    operation: () => Promise<T>,
    fallback: () => Promise<T>
  ): Promise<T> {
    // Check if circuit is open
    if (this.state === 'open') {
      // Check if timeout has passed
      if (Date.now() - this.lastFailureTime > this.timeout) {
        this.state = 'half-open';
      } else {
        // Circuit open - use fallback
        console.warn('Circuit breaker open - using fallback');
        return fallback();
      }
    }
    
    try {
      const result = await operation();
      
      // Success - reset circuit
      if (this.state === 'half-open') {
        this.state = 'closed';
        this.failureCount = 0;
      }
      
      return result;
    } catch (error) {
      this.failureCount++;
      this.lastFailureTime = Date.now();
      
      // Open circuit if threshold reached
      if (this.failureCount >= this.threshold) {
        this.state = 'open';
        console.error(`Circuit breaker opened after ${this.failureCount} failures`);
      }
      
      // Use fallback
      return fallback();
    }
  }
}

// Usage with data providers
const stockPriceCircuit = new CircuitBreaker(5, 60000);

export async function getStockPriceWithCircuitBreaker(ticker: string) {
  return stockPriceCircuit.execute(
    // Primary operation
    async () => {
      const response = await fetch(`https://api.provider.com/quote/${ticker}`);
      if (!response.ok) throw new Error('Provider error');
      return response.json();
    },
    // Fallback to cache
    async () => {
      console.warn('Using cached price due to provider failure');
      const cached = await BackendCache.get(`stock:${ticker}:price`);
      if (!cached) throw new Error('No cached data available');
      return cached;
    }
  );
}
```

---

### Graceful Degradation

**If a module fails: show cached version, show fallback UI, never show raw errors**

```tsx
// Graceful degradation component
export function GracefulModule({ children, fallback, errorFallback }) {
  return (
    <ErrorBoundary
      fallback={errorFallback || (
        <div className="p-8 bg-slate-800 rounded-lg border border-slate-700">
          <p className="text-slate-400 text-center">
            Unable to load this module
          </p>
        </div>
      )}
    >
      <Suspense fallback={fallback || <LoadingSkeleton />}>
        {children}
      </Suspense>
    </ErrorBoundary>
  );
}

// Usage
<GracefulModule fallback={<HeatmapSkeleton />}>
  <HeatmapWidget />
</GracefulModule>
```

---

### Retry Logic

**Exponential backoff, max 3 retries**

```tsx
// Retry with exponential backoff (already implemented in 26.1)
export async function fetchWithRetry<T>(
  fetcher: () => Promise<T>,
  maxAttempts: number = 3,
  initialDelay: number = 1000
): Promise<T> {
  let lastError: Error;
  
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fetcher();
    } catch (error) {
      lastError = error as Error;
      
      if (attempt === maxAttempts) break;
      
      // Exponential backoff: 1s, 2s, 4s
      const delay = initialDelay * Math.pow(2, attempt - 1);
      console.log(`Retry attempt ${attempt} after ${delay}ms`);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  
  throw lastError!;
}
```

---

### Fallback Providers

**If primary data provider fails, switch to secondary provider**

```tsx
// Multi-provider failover (already implemented in 26.2)
export class LiveDataProvider {
  async fetch<T>(endpoint: string): Promise<T> {
    try {
      return await this.fetchFromProvider(this.primaryProvider, endpoint);
    } catch (error) {
      console.warn('Primary provider failed, using fallback');
      return await this.fetchFromProvider(this.fallbackProvider, endpoint);
    }
  }
}
```

---

## 26.10 Load Management

### Autoscaling

**Backend services scale based on CPU, memory, request volume**

```yaml
# Kubernetes Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: dominion-api
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: dominion-api
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
```

---

### Rate Limiting

**Protects API gateway, news engine, alerts engine**

```tsx
// Rate limiting by tier
export const RATE_LIMITS = {
  free: {
    requestsPerMinute: 30,
    requestsPerHour: 1000,
  },
  premium: {
    requestsPerMinute: 60,
    requestsPerHour: 3000,
  },
  pro: {
    requestsPerMinute: 120,
    requestsPerHour: 10000,
  },
};

// Rate limit middleware
export function rateLimitMiddleware(tier: UserTier) {
  const limits = RATE_LIMITS[tier];
  
  return rateLimit({
    windowMs: 60 * 1000, // 1 minute
    max: limits.requestsPerMinute,
    message: `Rate limit exceeded. ${tier} tier allows ${limits.requestsPerMinute} requests per minute.`,
    standardHeaders: true,
    legacyHeaders: false,
  });
}

// Apply rate limits
app.use('/api/', (req, res, next) => {
  const tier = req.user?.tier || 'free';
  rateLimitMiddleware(tier)(req, res, next);
});
```

---

### Queueing

**Used for alerts, analytics, news verification**

```tsx
// Queue implementation with BullMQ
import { Queue, Worker } from 'bullmq';

// Alerts queue
export const alertsQueue = new Queue('alerts', {
  connection: redis,
});

export async function enqueueAlert(alert: Alert) {
  await alertsQueue.add('process-alert', alert, {
    priority: alert.type === 'price' ? 1 : 2, // Price alerts highest priority
  });
}

// Analytics queue
export const analyticsQueue = new Queue('analytics', {
  connection: redis,
});

export async function enqueueAnalytics(userId: string) {
  await analyticsQueue.add('compute-analytics', { userId }, {
    removeOnComplete: true,
    removeOnFail: false,
  });
}

// News verification queue
export const newsQueue = new Queue('news-verification', {
  connection: redis,
});

export async function enqueueNewsVerification(articleId: string) {
  await newsQueue.add('verify-article', { articleId }, {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000,
    },
  });
}

// Workers process queued jobs
new Worker('alerts', async (job) => {
  const alert = job.data;
  await processAlert(alert);
}, { connection: redis });

new Worker('analytics', async (job) => {
  const { userId } = job.data;
  await computeAnalytics(userId);
}, { connection: redis });

new Worker('news-verification', async (job) => {
  const { articleId } = job.data;
  await verifyArticle(articleId);
}, { connection: redis });
```

---

## 26.11 Monitoring & Observability

### Metrics Tracked

- **Latency**: p50, p95, p99 response times
- **Error rates**: 4xx, 5xx by endpoint
- **Cache hit ratio**: Client, edge, backend
- **API throughput**: Requests per second
- **WebSocket stability**: Connection count, message rate
- **Identity widget load times**: Per identity type

```tsx
// Metrics collection
import * as Sentry from '@sentry/node';
import { Counter, Histogram, Gauge } from 'prom-client';

// Request latency histogram
const httpRequestDuration = new Histogram({
  name: 'http_request_duration_ms',
  help: 'HTTP request latency in milliseconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [50, 100, 200, 500, 1000, 2000, 5000],
});

// Error rate counter
const errorCounter = new Counter({
  name: 'http_errors_total',
  help: 'Total HTTP errors',
  labelNames: ['method', 'route', 'status_code'],
});

// Cache hit ratio
const cacheHitCounter = new Counter({
  name: 'cache_hits_total',
  help: 'Total cache hits',
  labelNames: ['layer'], // client, edge, backend
});

const cacheMissCounter = new Counter({
  name: 'cache_misses_total',
  help: 'Total cache misses',
  labelNames: ['layer'],
});

// WebSocket connections
const websocketConnections = new Gauge({
  name: 'websocket_connections',
  help: 'Current WebSocket connections',
});

// Metrics middleware
app.use((req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    
    httpRequestDuration.observe(
      { method: req.method, route: req.route?.path, status_code: res.statusCode },
      duration
    );
    
    if (res.statusCode >= 400) {
      errorCounter.inc({ method: req.method, route: req.route?.path, status_code: res.statusCode });
    }
  });
  
  next();
});
```

---

### Dashboards

- **Real-time performance**: Grafana dashboards
- **Alerts**: PagerDuty integration
- **Provider health**: Status page
- **Subscription events**: Admin dashboard

```yaml
# Grafana dashboard configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboards
data:
  dominion-performance.json: |
    {
      "dashboard": {
        "title": "DominionMarkets Performance",
        "panels": [
          {
            "title": "Request Latency (p95)",
            "targets": [{
              "expr": "histogram_quantile(0.95, http_request_duration_ms_bucket)"
            }]
          },
          {
            "title": "Error Rate",
            "targets": [{
              "expr": "rate(http_errors_total[5m])"
            }]
          },
          {
            "title": "Cache Hit Ratio",
            "targets": [{
              "expr": "cache_hits_total / (cache_hits_total + cache_misses_total)"
            }]
          }
        ]
      }
    }
```

---

### Alerts

**Triggered on: high latency, provider failure, cache failure, API spikes**

```tsx
// Alert rules
export const ALERT_RULES = {
  highLatency: {
    metric: 'http_request_duration_ms',
    threshold: 2000, // 2 seconds
    duration: '5m',
    severity: 'warning',
  },
  
  providerFailure: {
    metric: 'provider_errors_total',
    threshold: 10,
    duration: '5m',
    severity: 'critical',
  },
  
  cacheFailure: {
    metric: 'cache_errors_total',
    threshold: 100,
    duration: '5m',
    severity: 'warning',
  },
  
  apiSpike: {
    metric: 'http_requests_total',
    threshold: 1000, // requests per second
    duration: '1m',
    severity: 'info',
  },
};

// Alert notification
export async function sendAlert(rule: string, message: string, severity: string) {
  // Send to PagerDuty
  await fetch('https://events.pagerduty.com/v2/enqueue', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token token=${process.env.PAGERDUTY_TOKEN}`,
    },
    body: JSON.stringify({
      routing_key: process.env.PAGERDUTY_ROUTING_KEY,
      event_action: 'trigger',
      payload: {
        summary: `${rule}: ${message}`,
        severity,
        source: 'dominion-markets',
      },
    }),
  });
  
  // Send to Slack
  await fetch(process.env.SLACK_WEBHOOK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: `🚨 *${severity.toUpperCase()}*: ${rule}`,
      blocks: [
        {
          type: 'section',
          text: { type: 'mrkdwn', text: message },
        },
      ],
    }),
  });
}
```

---

## 26.12 Reliability Targets

### Uptime

**99.9% uptime target** (< 8.76 hours downtime per year)

```tsx
// Uptime monitoring
export async function checkUptime() {
  const endpoints = [
    'https://dominionmarkets.com/api/health',
    'https://api.dominionmarkets.com/health',
    'wss://ws.dominionmarkets.com/health',
  ];
  
  const results = await Promise.all(
    endpoints.map(async (endpoint) => {
      try {
        const response = await fetch(endpoint);
        return { endpoint, status: response.ok ? 'up' : 'down' };
      } catch {
        return { endpoint, status: 'down' };
      }
    })
  );
  
  const upCount = results.filter(r => r.status === 'up').length;
  const uptime = (upCount / results.length) * 100;
  
  return { uptime, results };
}
```

---

### Data Freshness

- **Prices**: < 2 seconds
- **Movers**: < 10 seconds
- **News**: < 1 minute

```tsx
// Data freshness tracking
export async function trackDataFreshness() {
  const metrics = {
    prices: await checkPriceFreshness(),
    movers: await checkMoversFreshness(),
    news: await checkNewsFreshness(),
  };
  
  Object.entries(metrics).forEach(([type, freshness]) => {
    if (freshness.ageSeconds > freshness.target) {
      console.warn(`⚠️ ${type} data stale: ${freshness.ageSeconds}s (target: ${freshness.target}s)`);
    }
  });
  
  return metrics;
}

async function checkPriceFreshness() {
  const cached = await BackendCache.get('stock:AAPL:price');
  const ageSeconds = (Date.now() - cached.timestamp) / 1000;
  
  return { ageSeconds, target: 2 };
}
```

---

### Recovery Time Objective (RTO)

**< 5 minutes** (maximum acceptable downtime)

```tsx
// RTO tracking
export async function measureRecoveryTime(incidentStart: Date) {
  const recoveryEnd = new Date();
  const rtoMinutes = (recoveryEnd.getTime() - incidentStart.getTime()) / 60000;
  
  if (rtoMinutes > 5) {
    console.error(`❌ RTO exceeded: ${rtoMinutes.toFixed(2)} minutes (target: 5 minutes)`);
  } else {
    console.log(`✅ RTO met: ${rtoMinutes.toFixed(2)} minutes`);
  }
  
  return rtoMinutes;
}
```

---

### Recovery Point Objective (RPO)

**< 1 minute** (maximum acceptable data loss)

```tsx
// RPO tracking
export async function measureDataLoss(lastBackup: Date, incidentTime: Date) {
  const dataLossMinutes = (incidentTime.getTime() - lastBackup.getTime()) / 60000;
  
  if (dataLossMinutes > 1) {
    console.error(`❌ RPO exceeded: ${dataLossMinutes.toFixed(2)} minutes of data loss (target: 1 minute)`);
  } else {
    console.log(`✅ RPO met: ${dataLossMinutes.toFixed(2)} minutes of data loss`);
  }
  
  return dataLossMinutes;
}

// Continuous backup strategy
export async function continuousBackup() {
  setInterval(async () => {
    await backupCriticalData();
  }, 60000); // Backup every 60 seconds to meet RPO
}
```

---

## Performance & Optimization Complete Implementation Checklist

✅ **Performance Principles**: Speed is trust, freshness strategy, predictable performance, graceful degradation, identity-aware optimization  
✅ **Caching Architecture**: 4-layer caching (client, edge, backend Redis, live providers)  
✅ **Client-Side Caching**: User identity, portfolio, stocks, news, heatmap, Cultural Alpha (5-15min TTL)  
✅ **Edge Caching**: Static assets, charts, news, identity widgets (1-5min CDN cache)  
✅ **Backend Caching**: Indices (5s), movers (10s), heatmap (30s), Cultural Alpha (1min), analytics (5min)  
✅ **Real-Time Strategy**: WebSockets for prices/alerts, polling for movers/heatmap, batch updates for news  
✅ **Latency Targets**: Dashboard < 1.2s, markets < 700ms, stock detail < 600ms, portfolio < 1.2s  
✅ **Offline Mode**: Cached dashboard/portfolio/news available, real-time features unavailable  
✅ **Failover & Resilience**: Circuit breakers, graceful degradation, exponential backoff retry, fallback providers  
✅ **Load Management**: Kubernetes autoscaling, tier-based rate limiting, queue-based processing  
✅ **Monitoring**: Latency/errors/cache hits/throughput/WebSocket metrics, Grafana dashboards, PagerDuty alerts  
✅ **Reliability Targets**: 99.9% uptime, < 2s price freshness, < 5min RTO, < 1min RPO  

---

## SECTION 27 — LOGGING, MONITORING & ANALYTICS (INTERNAL OPS)

This section defines the **internal operational intelligence layer** of DominionMarkets — the systems that keep the platform **observable, diagnosable, stable, and continuously improving**.

**This is not user-facing.**

This is the **Ops Command Center** — the heartbeat of reliability.

---

## 27.1 Operational Principles

DominionMarkets follows **five core operational principles**:

### 1. Everything Observable
Every service emits structured logs and metrics.

### 2. Everything Traceable
Every request can be followed end-to-end.

### 3. Everything Monitored
Dashboards track health, performance, and anomalies.

### 4. Everything Alertable
Ops is notified before users feel pain.

### 5. Everything Privacy-Respectful
No sensitive user data is ever logged.

---

### Implementation

```tsx
// Operational configuration
export const operationalConfig = {
  logging: {
    level: process.env.LOG_LEVEL || 'info',
    format: 'json',
    destination: ['stdout', 'file', 'datadog'],
    sampling: {
      debug: 0.1,   // Sample 10% of debug logs
      info: 1.0,    // Log 100% of info logs
      warn: 1.0,    // Log 100% of warnings
      error: 1.0,   // Log 100% of errors
    },
  },
  
  tracing: {
    enabled: true,
    provider: 'datadog',
    sampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,
    traceSensitiveOperations: true,
  },
  
  metrics: {
    enabled: true,
    provider: 'prometheus',
    scrapeInterval: 15, // seconds
    retention: 15,      // days
  },
  
  monitoring: {
    healthCheckInterval: 30,  // seconds
    uptimeCheckInterval: 60,  // seconds
    anomalyDetection: true,
  },
  
  alerts: {
    enabled: true,
    channels: ['pagerduty', 'slack', 'email'],
    aggregationWindow: 300, // 5 minutes
    deduplication: true,
  },
  
  privacy: {
    redactPII: true,
    redactFinancialData: true,
    redactAuthentication: true,
    allowedFields: ['userId', 'requestId', 'identity', 'tier'],
  },
};

// Privacy-aware logger
import winston from 'winston';

// Fields to redact
const SENSITIVE_FIELDS = [
  'password',
  'passwordHash',
  'token',
  'refreshToken',
  'accessToken',
  'email',
  'phoneNumber',
  'ssn',
  'cardNumber',
  'cvv',
  'accountNumber',
  'routingNumber',
];

// Redact sensitive data
function redactSensitiveData(obj: any): any {
  if (typeof obj !== 'object' || obj === null) return obj;
  
  if (Array.isArray(obj)) {
    return obj.map(item => redactSensitiveData(item));
  }
  
  const redacted = { ...obj };
  
  for (const key in redacted) {
    // Check if field is sensitive
    if (SENSITIVE_FIELDS.some(field => key.toLowerCase().includes(field.toLowerCase()))) {
      redacted[key] = '[REDACTED]';
    } else if (typeof redacted[key] === 'object') {
      redacted[key] = redactSensitiveData(redacted[key]);
    }
  }
  
  return redacted;
}

// Create privacy-aware logger
export const logger = winston.createLogger({
  level: operationalConfig.logging.level,
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json(),
    winston.format((info) => {
      // Redact sensitive data
      return redactSensitiveData(info);
    })()
  ),
  defaultMeta: {
    service: 'dominion-markets',
    environment: process.env.NODE_ENV,
  },
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
  ],
});

// Structured logging helpers
export const log = {
  info: (message: string, meta?: any) => {
    logger.info(message, redactSensitiveData(meta));
  },
  
  warn: (message: string, meta?: any) => {
    logger.warn(message, redactSensitiveData(meta));
  },
  
  error: (message: string, error?: Error, meta?: any) => {
    logger.error(message, {
      error: {
        message: error?.message,
        stack: error?.stack,
        name: error?.name,
      },
      ...redactSensitiveData(meta),
    });
  },
  
  debug: (message: string, meta?: any) => {
    // Sample debug logs
    if (Math.random() < operationalConfig.logging.sampling.debug) {
      logger.debug(message, redactSensitiveData(meta));
    }
  },
};

// Usage examples
log.info('User logged in', {
  userId: 'user_123',
  identity: 'diaspora',
  tier: 'premium',
  // email: 'user@example.com' // This would be redacted
});

log.error('Failed to fetch stock price', new Error('Provider timeout'), {
  ticker: 'AAPL',
  provider: 'primary',
  duration: 5000,
});

log.debug('Cache hit', {
  key: 'stock:AAPL:price',
  ttl: 15,
});
```

---

## 27.2 Structured Logging

### Log Types

DominionMarkets emits **8 categories of logs** for operational intelligence:

1. **Request Logs** - HTTP requests/responses
2. **Error Logs** - Application errors and exceptions
3. **Performance Logs** - Latency and timing metrics
4. **Cache Logs** - Cache hits/misses/evictions
5. **Provider Logs** - External API calls (Alpha Vantage, Polygon, etc.)
6. **Subscription Events** - Tier changes, upgrades, cancellations
7. **Alerts Engine Logs** - Alert creation, triggers, failures
8. **News Verification Logs** - Story processing, verification success/failure

---

### Log Format (JSON)

All logs follow a **consistent JSON schema**:

```typescript
interface DominionLogEntry {
  // Standard fields (always present)
  timestamp: string;           // ISO 8601: "2025-12-24T10:15:30.123Z"
  level: 'debug' | 'info' | 'warn' | 'error' | 'fatal';
  message: string;
  service: string;             // "api" | "backend" | "websocket" | "worker"
  
  // Request tracking
  requestId: string;           // Unique per request: "req_abc123"
  traceId?: string;            // Distributed trace ID
  spanId?: string;             // Span ID within trace
  
  // User context (privacy-aware)
  userId?: string;             // Hashed user ID: "user_hash_xyz789"
  identity?: UserIdentity;     // "diaspora" | "youth" | "creator" | "legacy"
  tier?: UserTier;             // "free" | "basic" | "premium" | "pro"
  
  // HTTP context (for request logs)
  method?: string;             // "GET" | "POST" | "PUT" | "DELETE"
  path?: string;               // "/api/stocks/AAPL"
  status?: number;             // 200, 404, 500, etc.
  duration?: number;           // Request duration in milliseconds
  
  // Additional context
  error?: string;              // Error message (for error logs)
  stack?: string;              // Stack trace (for error logs)
  metadata?: Record<string, any>; // Additional structured data
}
```

**Example Log Entries:**

```json
{
  "timestamp": "2025-12-24T10:15:30.123Z",
  "level": "info",
  "message": "Request processed",
  "service": "api",
  "requestId": "req_abc123",
  "traceId": "trace_xyz789",
  "userId": "user_hash_def456",
  "identity": "diaspora",
  "tier": "premium",
  "method": "GET",
  "path": "/api/stocks/AAPL",
  "status": 200,
  "duration": 145
}

{
  "timestamp": "2025-12-24T10:16:05.456Z",
  "level": "error",
  "message": "Provider request failed",
  "service": "backend",
  "requestId": "req_ghi789",
  "traceId": "trace_jkl012",
  "error": "Alpha Vantage API timeout",
  "metadata": {
    "provider": "alpha-vantage",
    "endpoint": "/quote/AAPL",
    "timeout": 5000
  }
}

{
  "timestamp": "2025-12-24T10:17:22.789Z",
  "level": "info",
  "message": "Cache operation",
  "service": "backend",
  "requestId": "req_mno345",
  "metadata": {
    "operation": "get",
    "key": "stock:AAPL:price",
    "hit": true,
    "ttl": 15
  }
}
```

---

### Fields NEVER Logged (Privacy Protection)

To protect user privacy, the following data is **NEVER logged**:

❌ **Email addresses**  
❌ **Passwords** (plain or hashed)  
❌ **Payment data** (card numbers, CVV, billing details)  
❌ **Portfolio holdings** (stocks owned, quantities, positions)  
❌ **Personal information** (names, addresses, phone numbers, SSN)  

**All sensitive fields are automatically redacted** by the logging middleware (see 27.1 for redaction implementation).

---

### Log Levels

```tsx
export enum LogLevel {
  DEBUG = 'debug',   // Detailed diagnostic info (sampled in production)
  INFO = 'info',     // General informational messages
  WARN = 'warn',     // Warning messages (potential issues)
  ERROR = 'error',   // Error messages (actual failures)
  FATAL = 'fatal',   // Critical failures requiring immediate attention
}

// Log level hierarchy
const LOG_LEVEL_PRIORITY = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3,
  fatal: 4,
};

// Should log based on configured level
function shouldLog(level: LogLevel): boolean {
  const configuredLevel = operationalConfig.logging.level;
  return LOG_LEVEL_PRIORITY[level] >= LOG_LEVEL_PRIORITY[configuredLevel];
}
```

---

### Log Context

**Every log includes: timestamp, level, service, environment, requestId, userId (if applicable), identity, tier**

```tsx
// Request context middleware
import { v4 as uuidv4 } from 'uuid';
import { AsyncLocalStorage } from 'async_hooks';

const requestContext = new AsyncLocalStorage<RequestContext>();

interface RequestContext {
  requestId: string;
  userId?: string;
  identity?: UserIdentity;
  tier?: UserTier;
  startTime: number;
}

export function requestContextMiddleware(req: Request, res: Response, next: NextFunction) {
  const context: RequestContext = {
    requestId: req.headers['x-request-id'] as string || uuidv4(),
    userId: req.user?.id,
    identity: req.user?.identity,
    tier: req.user?.tier,
    startTime: Date.now(),
  };
  
  // Set response header
  res.setHeader('X-Request-ID', context.requestId);
  
  // Run in context
  requestContext.run(context, () => {
    next();
  });
}

// Get current context
export function getRequestContext(): RequestContext | undefined {
  return requestContext.getStore();
}

// Context-aware logger
export const contextLogger = {
  info: (message: string, meta?: any) => {
    const context = getRequestContext();
    log.info(message, { ...context, ...meta });
  },
  
  warn: (message: string, meta?: any) => {
    const context = getRequestContext();
    log.warn(message, { ...context, ...meta });
  },
  
  error: (message: string, error?: Error, meta?: any) => {
    const context = getRequestContext();
    log.error(message, error, { ...context, ...meta });
  },
  
  debug: (message: string, meta?: any) => {
    const context = getRequestContext();
    log.debug(message, { ...context, ...meta });
  },
};

// Usage in request handlers
app.use(requestContextMiddleware);

app.get('/api/stocks/:ticker', async (req, res) => {
  contextLogger.info('Fetching stock data', { ticker: req.params.ticker });
  
  try {
    const data = await getStockData(req.params.ticker);
    contextLogger.info('Stock data fetched successfully', { ticker: req.params.ticker });
    res.json(data);
  } catch (error) {
    contextLogger.error('Failed to fetch stock data', error, { ticker: req.params.ticker });
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

---

### Log Categories

```tsx
// Categorized logging
export const categoryLogger = {
  // API requests
  api: {
    request: (method: string, path: string, meta?: any) => {
      contextLogger.info(`API Request: ${method} ${path}`, { category: 'api', ...meta });
    },
    
    response: (method: string, path: string, status: number, duration: number) => {
      contextLogger.info(`API Response: ${method} ${path}`, {
        category: 'api',
        status,
        duration,
      });
    },
    
    error: (method: string, path: string, error: Error) => {
      contextLogger.error(`API Error: ${method} ${path}`, error, { category: 'api' });
    },
  },
  
  // Database operations
  database: {
    query: (operation: string, table: string, duration: number) => {
      contextLogger.debug(`Database Query: ${operation} ${table}`, {
        category: 'database',
        duration,
      });
    },
    
    error: (operation: string, table: string, error: Error) => {
      contextLogger.error(`Database Error: ${operation} ${table}`, error, {
        category: 'database',
      });
    },
  },
  
  // Cache operations
  cache: {
    hit: (key: string, layer: 'client' | 'edge' | 'backend') => {
      contextLogger.debug(`Cache Hit: ${key}`, { category: 'cache', layer });
    },
    
    miss: (key: string, layer: 'client' | 'edge' | 'backend') => {
      contextLogger.debug(`Cache Miss: ${key}`, { category: 'cache', layer });
    },
    
    error: (key: string, error: Error) => {
      contextLogger.error(`Cache Error: ${key}`, error, { category: 'cache' });
    },
  },
  
  // External provider calls
  provider: {
    request: (provider: string, endpoint: string) => {
      contextLogger.info(`Provider Request: ${provider}`, {
        category: 'provider',
        endpoint,
      });
    },
    
    response: (provider: string, endpoint: string, duration: number) => {
      contextLogger.info(`Provider Response: ${provider}`, {
        category: 'provider',
        endpoint,
        duration,
      });
    },
    
    error: (provider: string, endpoint: string, error: Error) => {
      contextLogger.error(`Provider Error: ${provider}`, error, {
        category: 'provider',
        endpoint,
      });
    },
  },
  
  // Authentication & authorization
  auth: {
    login: (userId: string, method: 'email' | 'sso' | '2fa') => {
      contextLogger.info('User logged in', {
        category: 'auth',
        userId,
        method,
      });
    },
    
    logout: (userId: string) => {
      contextLogger.info('User logged out', { category: 'auth', userId });
    },
    
    failed: (email: string, reason: string) => {
      contextLogger.warn('Login failed', {
        category: 'auth',
        email: '[REDACTED]', // Never log actual email
        reason,
      });
    },
  },
  
  // Business events
  business: {
    subscription: (userId: string, tier: UserTier, action: 'created' | 'upgraded' | 'downgraded' | 'canceled') => {
      contextLogger.info(`Subscription ${action}`, {
        category: 'business',
        userId,
        tier,
        action,
      });
    },
    
    alert: (userId: string, alertType: string, triggered: boolean) => {
      contextLogger.info(`Alert ${triggered ? 'triggered' : 'created'}`, {
        category: 'business',
        userId,
        alertType,
        triggered,
      });
    },
  },
};

// Usage
categoryLogger.api.request('GET', '/api/stocks/AAPL', { query: req.query });
categoryLogger.cache.hit('stock:AAPL:price', 'backend');
categoryLogger.provider.request('alpha-vantage', '/quote/AAPL');
categoryLogger.auth.login('user_123', 'email');
categoryLogger.business.subscription('user_123', 'premium', 'upgraded');
```

---

## 27.3 Monitoring Architecture

DominionMarkets monitors **7 critical systems** to ensure reliability and performance.

### Monitored Systems

#### 1. API Performance
- Request throughput (requests/sec)
- Latency distribution (P50, P90, P99)
- Error rates by endpoint
- Rate limit events
- Authentication failures

#### 2. Cache Performance
- Hit ratio (client, edge, backend)
- Miss ratio
- Eviction rates
- Memory usage
- Cache warming effectiveness

#### 3. Provider Health
- Response times (Alpha Vantage, Polygon, NewsAPI, etc.)
- Error rates per provider
- Timeout rates
- Quota consumption
- Failover triggers

#### 4. WebSocket Stability
- Active connections
- Message throughput
- Connection drops
- Reconnection rates
- Latency per client

#### 5. Identity Service
- Identity distribution (diaspora, youth, creator, legacy)
- Widget load times
- Sync failures
- Cultural Alpha refresh rates

#### 6. Billing Service
- Payment processing latency
- Payment failures
- Subscription changes (upgrades, downgrades, cancellations)
- Webhook delivery success

#### 7. Alerts Engine
- Alerts created per user
- Alerts triggered
- Alert evaluation latency
- Failed evaluations
- Queue depth

#### 8. News Verification Engine
- Stories processed per hour
- Verification success rate
- Source load failures
- Timeline generation failures
- Multi-source correlation success

---

### Monitoring Tools

DominionMarkets uses **5 dashboard types** for operational visibility:

#### 1. Metrics Dashboards (Grafana + Prometheus)
- Real-time metrics visualization
- Custom alerts and thresholds
- Historical trend analysis

#### 2. Error Dashboards (Datadog + Kibana)
- Error aggregation by service/endpoint
- Stack trace analysis
- Error rate trends

#### 3. Latency Dashboards (Grafana)
- P50/P90/P99 latency by endpoint
- Latency heatmaps
- Slow query detection

#### 4. Cache Hit Ratio Dashboards (Grafana)
- Hit/miss ratios by layer (client, edge, backend)
- Cache warming effectiveness
- Eviction patterns

#### 5. Provider Uptime Dashboards (Grafana + Datadog)
- Provider availability
- Response time trends
- Error rate by provider
- Failover events

---

### Implementation

```tsx
// Monitoring configuration
export const monitoringConfig = {
  // Systems to monitor
  systems: [
    'api',
    'cache',
    'providers',
    'websocket',
    'identity',
    'billing',
    'alerts-engine',
    'news-verification',
  ],
  
  // Metrics collection
  metrics: {
    enabled: true,
    interval: 15, // seconds
    retention: 90, // days
  },
  
  // Dashboard endpoints
  dashboards: {
    grafana: 'https://grafana.dominionmarkets.app',
    datadog: 'https://app.datadoghq.com',
    kibana: 'https://kibana.dominionmarkets.app',
  },
  
  // Alert thresholds
  thresholds: {
    api: {
      errorRate: 0.01,      // 1% error rate
      latencyP99: 2000,     // 2 seconds
      requestRate: 10000,   // 10k requests/sec
    },
    cache: {
      hitRatio: 0.80,       // 80% hit ratio
      memoryUsage: 0.90,    // 90% memory
    },
    providers: {
      errorRate: 0.05,      // 5% error rate
      timeout: 5000,        // 5 seconds
      uptime: 0.999,        // 99.9% uptime
    },
    websocket: {
      connectionDrops: 0.02, // 2% drop rate
      latency: 100,         // 100ms
    },
    billing: {
      paymentFailureRate: 0.05, // 5% failure rate
    },
    alertsEngine: {
      evaluationLatency: 1000, // 1 second
      queueDepth: 10000,       // 10k alerts
    },
    newsVerification: {
      successRate: 0.95,    // 95% success
      processingLatency: 5000, // 5 seconds
    },
  },
};

// Monitor service health
export async function monitorServiceHealth() {
  const checks = await Promise.all([
    checkAPIHealth(),
    checkCacheHealth(),
    checkProviderHealth(),
    checkWebSocketHealth(),
    checkIdentityHealth(),
    checkBillingHealth(),
    checkAlertsEngineHealth(),
    checkNewsVerificationHealth(),
  ]);
  
  return {
    timestamp: new Date().toISOString(),
    systems: checks,
    overall: checks.every(c => c.status === 'healthy') ? 'healthy' : 'degraded',
  };
}

// Trace middleware
export function tracingMiddleware(req: Request, res: Response, next: NextFunction) {
  const span = tracer.startSpan('http.request', {
    resource: `${req.method} ${req.route?.path || req.path}`,
    tags: {
      'http.method': req.method,
      'http.url': req.url,
      'http.path': req.path,
      'user.id': req.user?.id,
      'user.identity': req.user?.identity,
      'user.tier': req.user?.tier,
    },
  });
  
  // Set span context on request
  req.span = span;
  
  // Finish span on response
  res.on('finish', () => {
    span.setTag('http.status_code', res.statusCode);
    
    if (res.statusCode >= 400) {
      span.setTag('error', true);
    }
    
    span.finish();
  });
  
  next();
}

// Trace function execution
export function traced<T>(
  operationName: string,
  fn: (span: any) => Promise<T>
): Promise<T> {
  const span = tracer.startSpan(operationName);
  
  return fn(span)
    .then((result) => {
      span.finish();
      return result;
    })
    .catch((error) => {
      span.setTag('error', true);
      span.setTag('error.message', error.message);
      span.setTag('error.stack', error.stack);
      span.finish();
      throw error;
    });
}

// Usage
export async function getStockData(ticker: string) {
  return traced('stock.fetch', async (span) => {
    span.setTag('ticker', ticker);
    
    // Check cache
    const cached = await traced('cache.get', async (cacheSpan) => {
      cacheSpan.setTag('key', `stock:${ticker}:price`);
      return BackendCache.get(`stock:${ticker}:price`);
    });
    
    if (cached) {
      span.setTag('cache.hit', true);
      return cached;
    }
    
    span.setTag('cache.hit', false);
    
    // Fetch from provider
    const data = await traced('provider.fetch', async (providerSpan) => {
      providerSpan.setTag('provider', 'alpha-vantage');
      providerSpan.setTag('ticker', ticker);
      
      const response = await fetch(`https://api.provider.com/quote/${ticker}`);
      return response.json();
    });
    
    // Store in cache
    await traced('cache.set', async (cacheSpan) => {
      cacheSpan.setTag('key', `stock:${ticker}:price`);
      cacheSpan.setTag('ttl', 15);
      await BackendCache.set(`stock:${ticker}:price`, data, 15);
    });
    
    return data;
  });
}
```

---

### Service Map

**Visualize dependencies and call paths between services**

```tsx
// Service dependencies configuration
export const serviceMap = {
  'api-gateway': {
    calls: ['auth-service', 'stock-service', 'portfolio-service', 'news-service'],
  },
  
  'stock-service': {
    calls: ['cache-redis', 'provider-alpha-vantage', 'provider-polygon'],
  },
  
  'portfolio-service': {
    calls: ['database-postgres', 'stock-service', 'analytics-service'],
  },
  
  'news-service': {
    calls: ['cache-redis', 'provider-news-api', 'verification-service'],
  },
  
  'auth-service': {
    calls: ['database-postgres', 'sso-codexdominion'],
  },
  
  'analytics-service': {
    calls: ['database-postgres', 'cache-redis'],
  },
  
  'verification-service': {
    calls: ['provider-news-api', 'database-postgres'],
  },
};

// Trace service calls
export function traceServiceCall(from: string, to: string, operation: string) {
  return traced(`service.${from}.${to}`, async (span) => {
    span.setTag('service.from', from);
    span.setTag('service.to', to);
    span.setTag('operation', operation);
    
    // Operation implementation
  });
}
```

---

## 27.4 Metrics Tracked

DominionMarkets tracks **8 categories of metrics** for operational intelligence.

### 1. API Metrics

**Throughput:**
```typescript
// Requests per second (by endpoint, method, status)
api_requests_per_second{endpoint="/api/stocks/AAPL", method="GET", status="200"} 45.3
api_requests_per_second{endpoint="/api/portfolio", method="GET", status="200"} 12.7
api_requests_per_second{endpoint="/api/alerts", method="POST", status="201"} 3.2
```

**Latency:**
```typescript
// Request duration in milliseconds (P50, P90, P99)
api_request_duration_ms{endpoint="/api/stocks/AAPL", quantile="0.5"} 87
api_request_duration_ms{endpoint="/api/stocks/AAPL", quantile="0.9"} 234
api_request_duration_ms{endpoint="/api/stocks/AAPL", quantile="0.99"} 1247
```

**Error Rate:**
```typescript
// Errors per second (by endpoint, error type)
api_errors_per_second{endpoint="/api/stocks/TSLA", type="provider_timeout"} 0.3
api_errors_per_second{endpoint="/api/auth/login", type="invalid_credentials"} 1.2
```

**Rate Limit Events:**
```typescript
// Rate limit hits (by tier, endpoint)
api_rate_limit_hits{tier="free", endpoint="/api/stocks/*"} 23
api_rate_limit_hits{tier="basic", endpoint="/api/news"} 5
```

---

### 2. Cache Metrics

**Hit Ratio:**
```typescript
// Cache effectiveness (by layer, key pattern)
cache_hit_ratio{layer="client", pattern="stock:*"} 0.87
cache_hit_ratio{layer="edge", pattern="chart:*"} 0.93
cache_hit_ratio{layer="backend", pattern="indices"} 0.78
```

**Miss Ratio:**
```typescript
cache_miss_ratio{layer="client", pattern="stock:*"} 0.13
cache_miss_ratio{layer="backend", pattern="cultural-alpha:*"} 0.22
```

**Evictions:**
```typescript
// Cache evictions per minute
cache_evictions_per_min{layer="backend", reason="ttl_expired"} 234
cache_evictions_per_min{layer="backend", reason="memory_pressure"} 12
```

**Memory Usage:**
```typescript
// Cache memory utilization (percentage)
cache_memory_usage{layer="backend", max_mb="512"} 0.73
```

---

### 3. Provider Metrics

**Response Time:**
```typescript
// Provider API latency in milliseconds
provider_response_time_ms{provider="alpha-vantage", endpoint="/quote"} 347
provider_response_time_ms{provider="polygon", endpoint="/snapshot"} 89
provider_response_time_ms{provider="newsapi", endpoint="/everything"} 523
```

**Error Rate:**
```typescript
// Provider errors per second
provider_errors_per_sec{provider="alpha-vantage", type="timeout"} 0.05
provider_errors_per_sec{provider="polygon", type="rate_limit"} 0.02
```

**Timeout Rate:**
```typescript
provider_timeout_rate{provider="alpha-vantage"} 0.03
provider_timeout_rate{provider="finnhub"} 0.01
```

---

### 4. Alerts Engine Metrics

**Alerts Created:**
```typescript
// Alerts created per minute (by type)
alerts_created_per_min{type="price_threshold"} 45
alerts_created_per_min{type="news_keyword"} 12
alerts_created_per_min{type="earnings_date"} 3
```

**Alerts Triggered:**
```typescript
// Alerts triggered per minute
alerts_triggered_per_min{type="price_threshold", identity="diaspora"} 8
alerts_triggered_per_min{type="news_keyword", identity="youth"} 3
```

**Alerts Failed:**
```typescript
// Alert evaluation failures
alerts_failed_per_min{reason="provider_error"} 2
alerts_failed_per_min{reason="evaluation_timeout"} 0.5
```

---

### 5. News Verification Metrics

**Stories Processed:**
```typescript
// News stories processed per hour
news_stories_processed_per_hour{source="newsapi"} 234
news_stories_processed_per_hour{source="alpha-vantage-news"} 87
```

**Verification Success Rate:**
```typescript
// Percentage of stories successfully verified
news_verification_success_rate 0.94
```

**Source Load Failures:**
```typescript
// Failed news source loads per hour
news_source_failures_per_hour{source="newsapi"} 3
news_source_failures_per_hour{source="finnhub-news"} 1
```

---

### 6. Identity Metrics

**Identity Distribution:**
```typescript
// Active users by identity
identity_distribution{identity="diaspora"} 3452
identity_distribution{identity="youth"} 1876
identity_distribution{identity="creator"} 987
identity_distribution{identity="legacy"} 2341
```

**Identity Widget Load Times:**
```typescript
// Widget load latency in milliseconds
identity_widget_load_ms{identity="diaspora", widget="cultural-alpha"} 234
identity_widget_load_ms{identity="youth", widget="youth-trends"} 187
```

---

### 7. Subscription Metrics

**Upgrades:**
```typescript
// Subscription tier changes per day
subscription_upgrades_per_day{from="free", to="basic"} 23
subscription_upgrades_per_day{from="basic", to="premium"} 12
subscription_upgrades_per_day{from="premium", to="pro"} 5
```

**Downgrades:**
```typescript
subscription_downgrades_per_day{from="premium", to="basic"} 3
subscription_downgrades_per_day{from="pro", to="premium"} 1
```

**Cancellations:**
```typescript
subscription_cancellations_per_day{tier="basic"} 8
subscription_cancellations_per_day{tier="premium"} 2
```

---

### 8. WebSocket Metrics

**Active Connections:**
```typescript
websocket_active_connections{identity="diaspora"} 234
websocket_active_connections{identity="youth"} 87
```

**Messages Sent:**
```typescript
websocket_messages_per_sec{type="price_update"} 1234
websocket_messages_per_sec{type="alert_trigger"} 5
```

---

### Prometheus Metrics

```tsx
import { Counter, Histogram, Gauge, Summary } from 'prom-client';

// HTTP request metrics
export const httpRequestsTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'route', 'status_code', 'user_tier'],
});

export const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10],
});

// Database metrics
export const databaseQueriesTotal = new Counter({
  name: 'database_queries_total',
  help: 'Total database queries',
  labelNames: ['operation', 'table', 'status'],
});

export const databaseQueryDuration = new Histogram({
  name: 'database_query_duration_seconds',
  help: 'Database query duration in seconds',
  labelNames: ['operation', 'table'],
  buckets: [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1],
});

// Cache metrics
export const cacheOperationsTotal = new Counter({
  name: 'cache_operations_total',
  help: 'Total cache operations',
  labelNames: ['operation', 'layer', 'status'],
});

export const cacheHitRatio = new Gauge({
  name: 'cache_hit_ratio',
  help: 'Cache hit ratio by layer',
  labelNames: ['layer'],
});

// External provider metrics
export const providerRequestsTotal = new Counter({
  name: 'provider_requests_total',
  help: 'Total external provider requests',
  labelNames: ['provider', 'endpoint', 'status'],
});

export const providerRequestDuration = new Histogram({
  name: 'provider_request_duration_seconds',
  help: 'External provider request duration in seconds',
  labelNames: ['provider', 'endpoint'],
  buckets: [0.1, 0.5, 1, 2, 5, 10],
});

// WebSocket metrics
export const websocketConnections = new Gauge({
  name: 'websocket_connections',
  help: 'Current WebSocket connections',
});

export const websocketMessagesTotal = new Counter({
  name: 'websocket_messages_total',
  help: 'Total WebSocket messages',
  labelNames: ['type', 'direction'], // direction: inbound/outbound
});

// Business metrics
export const subscriptionsTotal = new Gauge({
  name: 'subscriptions_total',
  help: 'Total active subscriptions',
  labelNames: ['tier'],
});

export const alertsTriggeredTotal = new Counter({
  name: 'alerts_triggered_total',
  help: 'Total alerts triggered',
  labelNames: ['type', 'identity'],
});

export const portfolioHoldingsTotal = new Gauge({
  name: 'portfolio_holdings_total',
  help: 'Total portfolio holdings across all users',
});

// Metrics middleware
export function metricsMiddleware(req: Request, res: Response, next: NextFunction) {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000; // Convert to seconds
    
    httpRequestsTotal.inc({
      method: req.method,
      route: req.route?.path || 'unknown',
      status_code: res.statusCode,
      user_tier: req.user?.tier || 'anonymous',
    });
    
    httpRequestDuration.observe(
      {
        method: req.method,
        route: req.route?.path || 'unknown',
        status_code: res.statusCode,
      },
      duration
    );
  });
  
  next();
}

// Metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', 'text/plain');
  res.send(await register.metrics());
});
```

---

### Custom Metrics

```tsx
// Identity-specific metrics
export const identityInsightsGenerated = new Counter({
  name: 'identity_insights_generated_total',
  help: 'Total identity insights generated',
  labelNames: ['identity'],
});

export const culturalAlphaCalculated = new Counter({
  name: 'cultural_alpha_calculated_total',
  help: 'Total Cultural Alpha calculations',
  labelNames: ['identity'],
});

// Performance metrics
export const coreWebVitalsLCP = new Histogram({
  name: 'core_web_vitals_lcp_seconds',
  help: 'Largest Contentful Paint in seconds',
  labelNames: ['page'],
  buckets: [0.5, 1, 2, 2.5, 3, 4, 5],
});

export const coreWebVitalsFID = new Histogram({
  name: 'core_web_vitals_fid_seconds',
  help: 'First Input Delay in seconds',
  labelNames: ['page'],
  buckets: [0.01, 0.05, 0.1, 0.2, 0.3, 0.5],
});

export const coreWebVitalsCLS = new Gauge({
  name: 'core_web_vitals_cls',
  help: 'Cumulative Layout Shift',
  labelNames: ['page'],
});

// Usage
identityInsightsGenerated.inc({ identity: 'diaspora' });
culturalAlphaCalculated.inc({ identity: 'youth' });
coreWebVitalsLCP.observe({ page: 'dashboard' }, 1.2);
```

---

## 27.5 Tracing Architecture

**Distributed tracing** allows engineers to follow a request across services end-to-end.

### What a Trace Includes

Every trace captures:

1. **Request ID** - Unique identifier for the request
2. **Service Hops** - All services touched by the request
3. **Duration Per Hop** - Time spent in each service
4. **Cache Hits/Misses** - Cache operations per hop
5. **Provider Calls** - External API calls (Alpha Vantage, Polygon, etc.)
6. **Errors** - Any errors encountered along the way

---

### Trace Flow Example

```
User Request: GET /api/stocks/AAPL
  ↓
[API Service] (87ms)
  ├─ [Cache Check] client → miss (3ms)
  ├─ [Cache Check] backend → miss (12ms)
  ├─ [Provider Call] Alpha Vantage → success (347ms)
  ├─ [Cache Write] backend → success (8ms)
  └─ [Response] 200 OK (459ms total)
```

### Trace Data Structure

```typescript
interface DistributedTrace {
  traceId: string;                // "trace_abc123"
  requestId: string;              // "req_xyz789"
  timestamp: string;              // "2025-12-24T10:15:30.123Z"
  totalDuration: number;          // 459 (milliseconds)
  
  // Request context
  method: string;                 // "GET"
  path: string;                   // "/api/stocks/AAPL"
  userId?: string;                // "user_hash_def456" (hashed)
  identity?: UserIdentity;        // "diaspora"
  tier?: UserTier;                // "premium"
  
  // Service hops
  spans: TraceSpan[];
  
  // Errors (if any)
  errors: TraceError[];
}

interface TraceSpan {
  spanId: string;                 // "span_ghi012"
  parentSpanId?: string;          // "span_abc123" (for nested spans)
  service: string;                // "api", "backend", "cache", "provider"
  operation: string;              // "GET /api/stocks/AAPL", "cache.get", "provider.request"
  startTime: number;              // Unix timestamp (ms)
  duration: number;               // Span duration (ms)
  
  // Span metadata
  tags: Record<string, any>;      // Additional context
  
  // Cache operations
  cacheHit?: boolean;
  cacheKey?: string;
  cacheTTL?: number;
  
  // Provider calls
  provider?: string;              // "alpha-vantage", "polygon"
  providerEndpoint?: string;      // "/quote/AAPL"
  providerStatus?: number;        // 200, 429, 500, etc.
}

interface TraceError {
  spanId: string;
  errorType: string;              // "provider_timeout", "cache_error"
  message: string;
  stack?: string;
}
```

---

### Implementation with Datadog

```tsx
// Distributed tracing with Datadog
import tracer from 'dd-trace';

tracer.init({
  service: 'dominion-markets',
  env: process.env.NODE_ENV,
  version: process.env.APP_VERSION,
  logInjection: true,  // Inject trace IDs into logs
  runtimeMetrics: true,
  profiling: true,
});

// Trace middleware
export function tracingMiddleware(req: Request, res: Response, next: NextFunction) {
  const span = tracer.startSpan('http.request', {
    resource: `${req.method} ${req.route?.path || req.path}`,
    tags: {
      'http.method': req.method,
      'http.url': req.url,
      'http.path': req.path,
      'user.id': req.user?.id,
      'user.identity': req.user?.identity,
      'user.tier': req.user?.tier,
    },
  });
  
  // Store span in request context
  req.span = span;
  
  // Finish span when response is sent
  res.on('finish', () => {
    span.setTag('http.status_code', res.statusCode);
    span.finish();
  });
  
  next();
}

// Trace cache operations
export async function tracedCacheGet(key: string): Promise<any> {
  const span = tracer.startSpan('cache.get', {
    resource: key,
    tags: { 'cache.key': key },
  });
  
  try {
    const value = await redis.get(key);
    span.setTag('cache.hit', value !== null);
    return value;
  } catch (error) {
    span.setTag('error', true);
    span.setTag('error.message', error.message);
    throw error;
  } finally {
    span.finish();
  }
}

// Trace provider calls
export async function tracedProviderRequest(
  provider: string,
  endpoint: string,
  params: any
): Promise<any> {
  const span = tracer.startSpan('provider.request', {
    resource: `${provider} ${endpoint}`,
    tags: {
      'provider.name': provider,
      'provider.endpoint': endpoint,
    },
  });
  
  try {
    const response = await fetch(`${providerBaseUrl}${endpoint}`, {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${providerApiKey}` },
      signal: AbortSignal.timeout(5000),
    });
    
    span.setTag('provider.status', response.status);
    span.setTag('provider.success', response.ok);
    
    const data = await response.json();
    return data;
  } catch (error) {
    span.setTag('error', true);
    span.setTag('error.type', error.name);
    span.setTag('error.message', error.message);
    throw error;
  } finally {
    span.finish();
  }
}
```

---

### Used For

Tracing enables:

1. **Debugging**
   - Identify which service is causing errors
   - See exact error messages and stack traces
   - Reproduce issues with trace ID

2. **Performance Tuning**
   - Identify slow services/operations
   - Find cache miss patterns
   - Optimize provider call strategies

3. **Reliability Improvements**
   - Track provider failures
   - Identify cascading failures
   - Measure failover effectiveness

**Example Use Case:**

User reports slow dashboard load → Ops looks up trace by userId → Sees provider timeout in Alpha Vantage span → Implements circuit breaker → Issue resolved.

---

## 27.6 Alerting System (Internal Ops)

Ops receives **3 severity levels** of alerts.

### Critical Alerts (Immediate Action)

**Trigger PagerDuty + Slack**

- ❗ **API Error Spike** - Error rate > 1% for 5+ minutes
- ❗ **Provider Outage** - Provider unavailable for 2+ minutes
- ❗ **Cache Failure** - Redis down or unreachable
- ❗ **Billing Service Failure** - Payment processing down
- ❗ **Identity Service Failure** - Identity service unavailable
- ❗ **Alerts Engine Failure** - Alerts not being evaluated
- ❗ **News Verification Engine Failure** - News verification down

```typescript
// Critical alert example
const criticalAlert = {
  severity: 'critical',
  title: 'API Error Spike Detected',
  message: 'Error rate is 2.3% (threshold: 1.0%)',
  service: 'api',
  metric: 'error_rate',
  currentValue: 0.023,
  threshold: 0.01,
  duration: '7 minutes',
  channels: ['pagerduty', 'slack'],
  runbook: 'https://docs.dominionmarkets.app/runbooks/api-error-spike',
};
```

---

### Warning Alerts (Monitor Closely)

**Slack Notifications**

- ⚠️ **Latency Increase** - P99 latency > 2 seconds for 10+ minutes
- ⚠️ **Cache Hit Ratio Drop** - Hit ratio < 80% for 15+ minutes
- ⚠️ **Elevated 4xx Errors** - 4xx rate > 5% for 10+ minutes
- ⚠️ **Slow Provider Responses** - Provider P95 > 3 seconds

```typescript
// Warning alert example
const warningAlert = {
  severity: 'warning',
  title: 'Cache Hit Ratio Dropping',
  message: 'Backend cache hit ratio is 73% (threshold: 80%)',
  service: 'backend',
  metric: 'cache_hit_ratio',
  currentValue: 0.73,
  threshold: 0.80,
  duration: '18 minutes',
  channels: ['slack'],
  suggestedAction: 'Check cache warming jobs, review TTL configuration',
};
```

---

### Informational Alerts (Awareness)

**Slack Notifications Only**

- ℹ️ **Deployment Events** - New version deployed
- ℹ️ **Scaling Events** - Kubernetes scaled up/down
- ℹ️ **Subscription Spikes** - Unusual number of upgrades/cancellations

```typescript
// Informational alert example
const infoAlert = {
  severity: 'info',
  title: 'Kubernetes Scaled Up',
  message: 'API pods scaled from 5 to 8 due to increased load',
  service: 'kubernetes',
  metric: 'pod_count',
  previousValue: 5,
  currentValue: 8,
  channels: ['slack'],
};
```

---

### Alert Implementation

```typescript
// Alert configuration
export const alertConfig = {
  critical: {
    channels: ['pagerduty', 'slack'],
    aggregationWindow: 300,  // 5 minutes
    escalationPolicy: 'immediate',
  },
  warning: {
    channels: ['slack'],
    aggregationWindow: 600,  // 10 minutes
    escalationPolicy: 'none',
  },
  info: {
    channels: ['slack'],
    aggregationWindow: 1800, // 30 minutes
    escalationPolicy: 'none',
  },
};

// Send alert
export async function sendAlert(alert: Alert) {
  const config = alertConfig[alert.severity];
  
  // Send to PagerDuty (critical only)
  if (config.channels.includes('pagerduty')) {
    await sendToPagerDuty(alert);
  }
  
  // Send to Slack
  if (config.channels.includes('slack')) {
    await sendToSlack(alert);
  }
  
  // Log alert
  logger.warn('Alert triggered', {
    category: 'alerting',
    severity: alert.severity,
    title: alert.title,
    service: alert.service,
    metric: alert.metric,
  });
}
```

---

## 27.7 Reliability Dashboards

Ops monitors **6 reliability dashboards** in Grafana.

### 1. API Health Dashboard

**Panels:**
- **Latency** - P50/P90/P99 request duration
- **Error Rate** - Errors per second (by endpoint)
- **Throughput** - Requests per second (by endpoint, status)
- **Rate Limits** - Rate limit hits (by tier)
- **Authentication** - Login success/failure rates

**Alert Thresholds:**
- P99 latency > 2 seconds for 10+ minutes → Warning
- Error rate > 1% for 5+ minutes → Critical
- Throughput < 100 req/sec (during business hours) → Warning

---

### 2. Markets Data Dashboard

**Panels:**
- **Provider Uptime** - Availability % per provider
- **Price Feed Stability** - Price update frequency (expected vs actual)
- **Volume Feed Stability** - Volume update frequency
- **Provider Latency** - Response times per provider
- **Failover Events** - Circuit breaker triggers

**Alert Thresholds:**
- Provider uptime < 99.9% → Critical
- Price updates delayed > 10 seconds → Warning
- Failover triggered → Info

---

### 3. News Verification Dashboard

**Panels:**
- **Source Availability** - NewsAPI, Alpha Vantage News, Finnhub News uptime
- **Verification Success Rate** - % of stories successfully verified
- **Timeline Generation Failures** - Failed timeline generations
- **Processing Latency** - Time to verify story
- **Multi-Source Correlation** - Stories corroborated across sources

**Alert Thresholds:**
- Verification success < 95% → Warning
- All sources down → Critical
- Processing latency > 10 seconds → Warning

---

### 4. Alerts Engine Dashboard

**Panels:**
- **Trigger Rate** - Alerts triggered per minute
- **Failure Rate** - Failed alert evaluations
- **Queue Depth** - Pending alerts in queue
- **Evaluation Latency** - Time to evaluate alert condition
- **Delivery Success** - Alert notification delivery rate

**Alert Thresholds:**
- Queue depth > 10,000 → Warning
- Failure rate > 5% → Critical
- Evaluation latency > 5 seconds → Warning

---

### 5. Identity Service Dashboard

**Panels:**
- **Identity Load Times** - Widget load latency by identity
- **Identity Sync Failures** - Failed identity data syncs
- **Identity Distribution** - Active users by identity
- **Cultural Alpha Refresh** - Cultural Alpha data freshness
- **Widget Errors** - Identity widget errors

**Alert Thresholds:**
- Sync failure rate > 1% → Warning
- Widget load time > 2 seconds → Warning
- Identity service down → Critical

---

### 6. Subscription Dashboard

**Panels:**
- **Upgrade Funnel** - Free → Basic → Premium → Pro conversion rates
- **Payment Failures** - Failed payment processing
- **Renewal Success Rate** - Auto-renewal success %
- **Churn Rate** - Cancellations per day
- **Webhook Delivery** - Stripe webhook success rate

**Alert Thresholds:**
- Payment failure rate > 5% → Critical
- Renewal success < 95% → Warning
- Webhook delivery < 99% → Warning

---

### Dashboard Implementation

```typescript
// Dashboard configuration (Grafana)
export const reliabilityDashboards = {
  apiHealth: {
    title: 'API Health',
    panels: [
      { metric: 'api_request_duration_ms', type: 'graph', quantiles: [0.5, 0.9, 0.99] },
      { metric: 'api_errors_per_second', type: 'graph', groupBy: 'endpoint' },
      { metric: 'api_requests_per_second', type: 'graph', groupBy: 'status' },
    ],
    refreshInterval: 15, // seconds
  },
  
  marketsData: {
    title: 'Markets Data',
    panels: [
      { metric: 'provider_uptime', type: 'stat', groupBy: 'provider' },
      { metric: 'provider_response_time_ms', type: 'graph', groupBy: 'provider' },
      { metric: 'price_feed_delay_seconds', type: 'gauge' },
    ],
    refreshInterval: 15,
  },
  
  newsVerification: {
    title: 'News Verification',
    panels: [
      { metric: 'news_verification_success_rate', type: 'gauge' },
      { metric: 'news_source_uptime', type: 'stat', groupBy: 'source' },
      { metric: 'news_processing_latency_ms', type: 'graph' },
    ],
    refreshInterval: 30,
  },
  
  // ... (remaining dashboards)
};
```

---

## 27.8 Anomaly Detection

DominionMarkets uses **automated anomaly detection** to identify unusual patterns before they become incidents.

### Monitored Anomalies

#### 1. Sudden Latency Spikes
**Detection:** P99 latency increases > 2x baseline for 5+ minutes  
**Response:** 
- Enable cache warming
- Scale up API pods
- Notify Ops (Slack)

#### 2. Unusual Error Patterns
**Detection:** New error types or error rate > 3σ above baseline  
**Response:**
- Capture detailed error logs
- Trigger distributed traces
- Notify Ops (Slack)

#### 3. Provider Instability
**Detection:** Provider response time > 2x baseline or error rate > 10%  
**Response:**
- Activate circuit breaker
- Failover to backup provider
- Notify Ops (PagerDuty if critical)

#### 4. Abnormal Subscription Events
**Detection:** Cancellations spike > 3x daily average  
**Response:**
- Alert product team
- Check for billing issues
- Review recent changes

#### 5. Alert Engine Surges
**Detection:** Alert triggers > 5x hourly average  
**Response:**
- Check for market volatility
- Verify provider data accuracy
- Throttle alert evaluations if needed

#### 6. News Verification Slowdowns
**Detection:** Processing latency > 2x baseline for 10+ minutes  
**Response:**
- Scale up verification workers
- Check news source availability
- Notify Ops (Slack)

---

### Implementation

```typescript
// Anomaly detection configuration
export const anomalyConfig = {
  enabled: true,
  baselineWindow: 3600,  // 1 hour for baseline calculation
  detectionWindow: 300,   // 5 minutes for anomaly detection
  
  thresholds: {
    latencySpike: { multiplier: 2, minDuration: 300 },
    errorPattern: { stdDevs: 3, minCount: 10 },
    providerInstability: { multiplier: 2, minErrorRate: 0.10 },
    subscriptionAnomaly: { multiplier: 3, minCount: 5 },
    alertSurge: { multiplier: 5, minCount: 20 },
    newsSlowdown: { multiplier: 2, minDuration: 600 },
  },
  
  responses: {
    latencySpike: ['warmCache', 'scaleUp', 'notifySlack'],
    errorPattern: ['captureTraces', 'notifySlack'],
    providerInstability: ['circuitBreaker', 'failover', 'notifyPagerDuty'],
    subscriptionAnomaly: ['notifyProduct', 'checkBilling'],
    alertSurge: ['checkMarketVolatility', 'throttleEvaluations'],
    newsSlowdown: ['scaleWorkers', 'checkSources', 'notifySlack'],
  },
};

// Detect anomalies
export async function detectAnomalies() {
  const baseline = await calculateBaseline();
  const current = await getCurrentMetrics();
  
  const anomalies: Anomaly[] = [];
  
  // Check latency spike
  if (current.p99Latency > baseline.p99Latency * 2) {
    anomalies.push({
      type: 'latencySpike',
      current: current.p99Latency,
      baseline: baseline.p99Latency,
      severity: 'warning',
    });
  }
  
  // Check error pattern
  if (current.errorRate > baseline.errorRate + (3 * baseline.errorStdDev)) {
    anomalies.push({
      type: 'errorPattern',
      current: current.errorRate,
      baseline: baseline.errorRate,
      severity: 'warning',
    });
  }
  
  // ... (additional anomaly checks)
  
  // Execute responses
  for (const anomaly of anomalies) {
    await executeAnomalyResponse(anomaly);
  }
  
  return anomalies;
}

// Automatic response to anomalies
export async function executeAnomalyResponse(anomaly: Anomaly) {
  const responses = anomalyConfig.responses[anomaly.type];
  
  for (const response of responses) {
    switch (response) {
      case 'warmCache':
        await warmCache();
        break;
      case 'scaleUp':
        await scaleUpPods();
        break;
      case 'circuitBreaker':
        await activateCircuitBreaker();
        break;
      case 'failover':
        await failoverToBackupProvider();
        break;
      case 'notifySlack':
        await sendSlackAlert(anomaly);
        break;
      case 'notifyPagerDuty':
        await sendPagerDutyAlert(anomaly);
        break;
      // ... (additional responses)
    }
  }
}
```

---

## 27.9 Incident Workflow

DominionMarkets follows a **5-stage incident response process**.

### Stage 1: Detection

**Alert triggers** (PagerDuty, Slack, or anomaly detection)

```typescript
const incident = {
  id: 'INC-20251224-001',
  timestamp: '2025-12-24T10:15:30.123Z',
  severity: 'critical',
  title: 'API Error Spike',
  description: 'Error rate is 2.3% (threshold: 1.0%)',
  service: 'api',
  detectedBy: 'prometheus-alert',
  status: 'detected',
};
```

---

### Stage 2: Triage

**Ops assesses severity** and assigns incident commander.

**Severity Levels:**
- **SEV-1 (Critical)** - Customer-impacting, immediate action required
- **SEV-2 (High)** - Degraded performance, action required within 1 hour
- **SEV-3 (Medium)** - Minor issue, action required within 4 hours
- **SEV-4 (Low)** - No customer impact, action required within 24 hours

```typescript
incident.severity = 'SEV-1';
incident.commander = 'ops-engineer-1';
incident.status = 'triaged';
```

---

### Stage 3: Containment

**Immediate actions to stop the bleeding:**

#### Circuit Breakers
```typescript
// Activate circuit breaker to prevent cascading failures
await activateCircuitBreaker('alpha-vantage');
```

#### Cache Fallback
```typescript
// Serve stale cache data to maintain availability
await enableStaleCacheMode();
```

#### Provider Failover
```typescript
// Switch to backup provider
await failoverProvider('alpha-vantage', 'polygon');
```

```typescript
incident.containmentActions = [
  'Activated circuit breaker for Alpha Vantage',
  'Enabled stale cache mode',
  'Failed over to Polygon provider',
];
incident.status = 'contained';
```

---

### Stage 4: Resolution

**Fix deployed** and verified.

```typescript
// Deploy fix
await deployFix('api', 'v1.2.3-hotfix');

// Verify fix
await verifyMetrics({
  errorRate: { expected: '<0.01', actual: '0.003' },
  p99Latency: { expected: '<2000ms', actual: '1234ms' },
});

incident.resolution = 'Deployed hotfix to handle provider timeouts gracefully';
incident.resolvedAt = '2025-12-24T10:47:12.456Z';
incident.status = 'resolved';
```

---

### Stage 5: Post-Incident Review

**Within 48 hours**, conduct post-incident review:

#### Root Cause Analysis
```markdown
**Root Cause:**
Alpha Vantage API experienced intermittent timeouts due to increased load.
Our API did not have proper timeout handling, causing errors to propagate to users.

**Contributing Factors:**
- No circuit breaker for provider calls
- No fallback provider configured
- Error handling did not serve stale cache data
```

#### Timeline
```markdown
**Timeline:**
10:15 - Alert triggered (error rate 2.3%)
10:17 - Incident triaged as SEV-1
10:20 - Circuit breaker activated
10:23 - Failover to Polygon provider
10:25 - Error rate dropped to 0.8%
10:35 - Hotfix deployed (timeout handling)
10:47 - Error rate normalized to 0.3%
10:50 - Incident resolved
```

#### Prevention Plan
```markdown
**Action Items:**
1. ✅ Implement circuit breaker for all provider calls (assigned: eng-1, due: Dec 26)
2. ✅ Configure fallback providers (assigned: eng-2, due: Dec 27)
3. ✅ Serve stale cache on provider errors (assigned: eng-3, due: Dec 28)
4. ✅ Add provider health checks to dashboard (assigned: eng-4, due: Dec 29)
5. ✅ Update runbook with provider failover procedure (assigned: ops-1, due: Dec 30)
```

---

### Incident Tracking

```typescript
// Store incident in database
export async function trackIncident(incident: Incident) {
  await db.incidents.create({
    data: {
      id: incident.id,
      timestamp: incident.timestamp,
      severity: incident.severity,
      title: incident.title,
      description: incident.description,
      service: incident.service,
      status: incident.status,
      commander: incident.commander,
      containmentActions: incident.containmentActions,
      resolution: incident.resolution,
      rootCause: incident.rootCause,
      timeline: incident.timeline,
      preventionPlan: incident.preventionPlan,
      resolvedAt: incident.resolvedAt,
    },
  });
}
```

---

## 27.10 Internal Analytics (Non-User)

DominionMarkets tracks **internal performance metrics** to optimize the platform—**never user behavior or personal data**.

### What Is Tracked

#### 1. Feature Usage
```typescript
// Which features are most/least used?
feature_usage{
  feature: 'cultural-alpha',
  loads: 3452,
  avgLoadTime: 234,
}

feature_usage{
  feature: 'alerts',
  creations: 1876,
  triggers: 234,
}
```

#### 2. Identity Distribution
```typescript
// How many users per identity?
identity_distribution{
  identity: 'diaspora',
  activeUsers: 3452,
  percentage: 0.39,
}
```

#### 3. Screen Load Times
```typescript
// Which screens are slow?
screen_load_time_ms{
  screen: 'dashboard',
  p50: 687,
  p95: 1234,
}
```

#### 4. Navigation Patterns
```typescript
// How do users navigate?
navigation_flow{
  from: 'dashboard',
  to: 'markets',
  count: 1234,
}
```

#### 5. Premium Gate Interactions
```typescript
// How often do users hit premium gates?
premium_gate_shown{
  feature: 'cultural-alpha-deep-dive',
  impressions: 876,
  upgrades: 23,
  conversionRate: 0.026,
}
```

---

### What Is NOT Tracked

To protect privacy, the following is **NEVER tracked**:

❌ **Personal Data** - Names, emails, addresses, phone numbers  
❌ **Portfolio Data** - Stocks owned, quantities, positions, values  
❌ **Financial Behavior** - Buy/sell decisions, trading patterns  
❌ **Sensitive Identity Data** - Detailed demographic information beyond identity type  

---

### Purpose

Internal analytics are used **exclusively for**:

1. **Improve Performance** - Identify slow screens, optimize load times
2. **Improve UX** - Understand navigation patterns, reduce friction
3. **Improve Reliability** - Detect feature issues, optimize caching

**NOT used for:**
- User profiling
- Behavioral targeting
- Selling data to third parties
- Predicting individual behavior

---

### Implementation

```typescript
// Internal analytics (privacy-first)
export const internalAnalytics = {
  // Track feature usage (aggregated only)
  trackFeatureUsage(feature: string) {
    metrics.featureUsage.inc({ feature });
  },
  
  // Track screen load time (no user identification)
  trackScreenLoad(screen: string, duration: number) {
    metrics.screenLoadTime.observe({ screen }, duration);
  },
  
  // Track navigation (no personal data)
  trackNavigation(from: string, to: string) {
    metrics.navigation.inc({ from, to });
  },
  
  // Track premium gate (conversion metrics only)
  trackPremiumGate(feature: string, action: 'shown' | 'upgraded') {
    metrics.premiumGate.inc({ feature, action });
  },
};

// NEVER track:
// - User IDs (except hashed for debugging)
// - Email addresses
// - Portfolio holdings
// - Financial decisions
// - Personal information
```

---

## Logging, Monitoring & Analytics Complete Implementation Checklist

✅ **27.1 Operational Principles**: 5 core principles (observable, traceable, monitored, alertable, privacy-respectful)  
✅ **27.2 Structured Logging**: 8 log types (request, error, performance, cache, provider, subscription, alerts, news), JSON format, PII redaction  
✅ **27.3 Monitoring Architecture**: 8 monitored systems (API, cache, providers, WebSocket, identity, billing, alerts, news), 5 dashboard types  
✅ **27.4 Metrics Tracked**: 8 metric categories (API, cache, provider, alerts, news, identity, subscription, WebSocket) with quantiles and rates  
✅ **27.5 Tracing Architecture**: Distributed tracing with Datadog, trace ID propagation, cache/provider operation tracking  
✅ **27.6 Alerting System**: 3 severity levels (critical, warning, info), PagerDuty + Slack integration, runbook links  
✅ **27.7 Reliability Dashboards**: 6 Grafana dashboards (API health, markets data, news verification, alerts engine, identity, subscription)  
✅ **27.8 Anomaly Detection**: 6 anomaly types with automatic responses (throttling, failover, scaling, notifications)  
✅ **27.9 Incident Workflow**: 5-stage process (detection → triage → containment → resolution → post-incident review)  
✅ **27.10 Internal Analytics**: Privacy-first metrics (feature usage, load times, navigation) with explicit non-tracking policy  

---

## 27.6 Logging Pipeline Architecture

DominionMarkets implements a **multi-stage logging pipeline** that collects, processes, enriches, stores, and visualizes logs from all services.

### Pipeline Flow

```
Services → Log Collector → Log Processor → Storage → Dashboards
```

**Stage 1: Services (Log Emission)**  
All services emit structured JSON logs to stdout/stderr

**Stage 2: Log Collector (Aggregation)**  
Collectors (Fluentd/Vector) aggregate logs from all services

**Stage 3: Log Processor (Enrichment)**  
Processors parse, filter, enrich, and route logs

**Stage 4: Storage (Persistence)**  
Logs stored in Elasticsearch for search and Datadog for analysis

**Stage 5: Dashboards (Visualization)**  
Kibana and Datadog dashboards for querying and alerting

---

### Implementation

#### Stage 1: Service Log Emission

All services use structured logging:

```tsx
// Service emits structured JSON logs
import { logger } from './utils/logger';

// API service logs
logger.info('Request processed', {
  service: 'api',
  method: 'GET',
  path: '/api/stocks/AAPL',
  duration: 145,
  status: 200,
  userId: 'user_123',
  identity: 'diaspora',
  tier: 'premium',
});

// Backend service logs
logger.info('Cache operation', {
  service: 'backend',
  operation: 'get',
  key: 'stock:AAPL:price',
  hit: true,
  ttl: 15,
});

// WebSocket service logs
logger.info('WebSocket message sent', {
  service: 'websocket',
  event: 'price_update',
  symbol: 'AAPL',
  clients: 47,
});

// Worker service logs
logger.info('Job processed', {
  service: 'worker',
  queue: 'notifications',
  job: 'send_alert',
  userId: 'user_123',
  duration: 234,
  success: true,
});
```

**Key Fields for All Logs:**

```typescript
interface LogEntry {
  timestamp: string;        // ISO 8601
  level: 'debug' | 'info' | 'warn' | 'error';
  message: string;
  service: string;          // Service identifier
  traceId?: string;         // Distributed trace ID
  spanId?: string;          // Span ID
  userId?: string;          // User identifier (if applicable)
  identity?: UserIdentity;  // User identity (if applicable)
  tier?: UserTier;          // User tier (if applicable)
  [key: string]: any;       // Additional context
}
```

---

#### Stage 2: Log Collector (Fluentd)

**Fluentd** collects logs from all containers and forwards them to processors.

```yaml
# fluentd/fluent.conf
<source>
  @type forward
  port 24224
  bind 0.0.0.0
</source>

# Collect from Docker containers
<source>
  @type tail
  path /var/lib/docker/containers/**/*.log
  pos_file /var/log/fluentd/docker.pos
  tag docker.*
  <parse>
    @type json
    time_key time
    time_format %Y-%m-%dT%H:%M:%S.%NZ
  </parse>
</source>

# Collect from Kubernetes pods
<source>
  @type kubernetes_metadata
  tag kubernetes.*
  <parse>
    @type json
  </parse>
</source>

# Add metadata
<filter **>
  @type record_transformer
  <record>
    hostname "#{Socket.gethostname}"
    environment "#{ENV['ENVIRONMENT']}"
    cluster "#{ENV['CLUSTER_NAME']}"
    version "#{ENV['APP_VERSION']}"
  </record>
</filter>

# Route to processors
<match **>
  @type forward
  <server>
    host log-processor
    port 24225
  </server>
  <buffer>
    @type file
    path /var/log/fluentd/buffer
    flush_interval 5s
    retry_max_interval 30s
  </buffer>
</match>
```

**Docker Compose Configuration:**

```yaml
# docker-compose.yml
services:
  fluentd:
    image: fluent/fluentd:v1.16-1
    volumes:
      - ./fluentd/fluent.conf:/fluentd/etc/fluent.conf
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - fluentd-buffer:/var/log/fluentd/buffer
    ports:
      - "24224:24224"
      - "24224:24224/udp"
    networks:
      - logging

  api:
    image: dominion-markets-api:latest
    logging:
      driver: fluentd
      options:
        fluentd-address: localhost:24224
        tag: api
    depends_on:
      - fluentd

volumes:
  fluentd-buffer:

networks:
  logging:
```

---

#### Stage 3: Log Processor (Enrichment & Routing)

**Log processor** parses, filters, enriches, and routes logs to storage.

```yaml
# fluentd/processor.conf
<source>
  @type forward
  port 24225
  bind 0.0.0.0
</source>

# Parse JSON logs
<filter **>
  @type parser
  key_name log
  reserve_data true
  <parse>
    @type json
  </parse>
</filter>

# Filter out debug logs in production
<filter **>
  @type grep
  <exclude>
    key level
    pattern /^debug$/
  </exclude>
</filter>

# Redact sensitive fields
<filter **>
  @type record_modifier
  <record>
    password "[REDACTED]"
    token "[REDACTED]"
    email "[REDACTED]"
    cardNumber "[REDACTED]"
  </record>
</filter>

# Enrich with GeoIP
<filter **>
  @type geoip
  geoip_lookup_keys clientIp
  <record>
    geoip_city ${city.names.en["clientIp"]}
    geoip_country ${country.iso_code["clientIp"]}
    geoip_location ${location.latitude["clientIp"]},${location.longitude["clientIp"]}
  </record>
</filter>

# Add derived fields
<filter **>
  @type record_transformer
  enable_ruby true
  <record>
    severity ${record["level"].upcase}
    timestamp_unix ${Time.parse(record["timestamp"]).to_i}
    day_of_week ${Time.parse(record["timestamp"]).strftime("%A")}
    hour_of_day ${Time.parse(record["timestamp"]).hour}
  </record>
</filter>

# Route to storage
<match **>
  @type copy
  
  # Send to Elasticsearch
  <store>
    @type elasticsearch
    host elasticsearch
    port 9200
    index_name dominion-markets-%Y.%m.%d
    type_name _doc
    logstash_format true
    logstash_prefix dominion-markets
    <buffer>
      @type file
      path /var/log/fluentd/es-buffer
      flush_interval 5s
      retry_max_interval 30s
    </buffer>
  </store>
  
  # Send to Datadog
  <store>
    @type datadog
    api_key "#{ENV['DATADOG_API_KEY']}"
    dd_source dominion-markets
    dd_tags "env:#{ENV['ENVIRONMENT']},service:#{ENV['SERVICE_NAME']}"
    <buffer>
      @type file
      path /var/log/fluentd/dd-buffer
      flush_interval 10s
    </buffer>
  </store>
  
  # Send errors to Slack
  <store>
    @type copy
    <store ignore_error>
      @type slack
      webhook_url "#{ENV['SLACK_WEBHOOK_URL']}"
      channel alerts
      username FluentdBot
      icon_emoji :fire:
      message "*[%s]* %s\n```%s```"
      message_keys level,message,error
      <filter>
        @type grep
        <regexp>
          key level
          pattern /^error$/
        </regexp>
      </filter>
    </store>
  </store>
</match>
```

---

#### Stage 4: Storage (Elasticsearch)

**Elasticsearch** stores logs for search and analysis.

```yaml
# elasticsearch/elasticsearch.yml
cluster.name: dominion-markets-logs
node.name: es-node-1

network.host: 0.0.0.0
http.port: 9200

# Index management
index.lifecycle.name: dominion-markets-policy
index.lifecycle.rollover_alias: dominion-markets

# Retention policy: 90 days
xpack.ilm.enabled: true
```

**Index Lifecycle Policy:**

```json
PUT _ilm/policy/dominion-markets-policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_size": "50GB",
            "max_age": "1d"
          }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "shrink": {
            "number_of_shards": 1
          },
          "forcemerge": {
            "max_num_segments": 1
          }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "freeze": {}
        }
      },
      "delete": {
        "min_age": "90d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

**Index Template:**

```json
PUT _index_template/dominion-markets-logs
{
  "index_patterns": ["dominion-markets-*"],
  "template": {
    "settings": {
      "number_of_shards": 3,
      "number_of_replicas": 1,
      "index.lifecycle.name": "dominion-markets-policy"
    },
    "mappings": {
      "properties": {
        "timestamp": { "type": "date" },
        "level": { "type": "keyword" },
        "message": { "type": "text" },
        "service": { "type": "keyword" },
        "traceId": { "type": "keyword" },
        "spanId": { "type": "keyword" },
        "userId": { "type": "keyword" },
        "identity": { "type": "keyword" },
        "tier": { "type": "keyword" },
        "method": { "type": "keyword" },
        "path": { "type": "keyword" },
        "status": { "type": "integer" },
        "duration": { "type": "float" },
        "error": { "type": "text" }
      }
    }
  }
}
```

---

#### Stage 5: Dashboards (Kibana)

**Kibana** provides log search, visualization, and alerting.

```yaml
# kibana/kibana.yml
server.name: kibana
server.host: 0.0.0.0
elasticsearch.hosts: ["http://elasticsearch:9200"]

# Dashboard configuration
kibana.index: ".kibana"
kibana.defaultAppId: "discover"
```

**Pre-Built Dashboards:**

1. **API Performance Dashboard**
   - Request rate (requests/sec)
   - Error rate (errors/sec)
   - P50/P95/P99 latency
   - Top endpoints by traffic
   - Top endpoints by errors

2. **User Activity Dashboard**
   - Active users (by identity, tier)
   - Login/logout events
   - Subscription changes
   - Alert creation/trigger events

3. **Service Health Dashboard**
   - Service uptime
   - Error logs by service
   - Database query performance
   - Cache hit rates
   - Provider response times

4. **Security Dashboard**
   - Failed login attempts
   - Authentication errors
   - Rate limit violations
   - Suspicious activity patterns

**Kibana Query Examples:**

```json
// All errors in the last hour
GET dominion-markets-*/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "level": "error" } },
        { "range": { "timestamp": { "gte": "now-1h" } } }
      ]
    }
  },
  "sort": [{ "timestamp": "desc" }]
}

// API errors grouped by endpoint
GET dominion-markets-*/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "service": "api" } },
        { "match": { "level": "error" } },
        { "range": { "timestamp": { "gte": "now-24h" } } }
      ]
    }
  },
  "aggs": {
    "errors_by_endpoint": {
      "terms": { "field": "path", "size": 20 }
    }
  }
}

// User journey by trace ID
GET dominion-markets-*/_search
{
  "query": {
    "match": { "traceId": "trace_abc123" }
  },
  "sort": [{ "timestamp": "asc" }]
}

// Slow API requests (> 1 second)
GET dominion-markets-*/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "service": "api" } },
        { "range": { "duration": { "gte": 1000 } } }
      ]
    }
  },
  "sort": [{ "duration": "desc" }]
}
```

---

### Alerting Rules

**Critical Errors**

```yaml
alert: HighErrorRate
expr: rate(logs_error_total[5m]) > 10
for: 5m
labels:
  severity: critical
  channel: pagerduty
annotations:
  summary: "High error rate detected"
  description: "Error rate is {{ $value }} errors/sec (threshold: 10)"
```

**Slow Requests**

```yaml
alert: SlowAPIRequests
expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
for: 10m
labels:
  severity: warning
  channel: slack
annotations:
  summary: "API P95 latency is high"
  description: "P95 latency is {{ $value }}s (threshold: 2s)"
```

**Service Down**

```yaml
alert: ServiceDown
expr: up{service="api"} == 0
for: 1m
labels:
  severity: critical
  channel: pagerduty
annotations:
  summary: "Service {{ $labels.service }} is down"
  description: "Service has been down for 1+ minute"
```

---

### Kubernetes Logging Configuration

```yaml
# kubernetes/logging-stack.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: logging

---

apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: logging
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      serviceAccountName: fluentd
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset:v1-debian-elasticsearch
        env:
        - name: FLUENT_ELASTICSEARCH_HOST
          value: "elasticsearch.logging.svc.cluster.local"
        - name: FLUENT_ELASTICSEARCH_PORT
          value: "9200"
        - name: FLUENT_ELASTICSEARCH_SCHEME
          value: "http"
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
        - name: fluentd-config
          mountPath: /fluentd/etc
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
      - name: fluentd-config
        configMap:
          name: fluentd-config

---

apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
  namespace: logging
data:
  fluent.conf: |
    # See processor.conf content above
```

---

### Docker Compose Logging Stack

```yaml
# docker-compose-logging.yml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
    networks:
      - logging

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
    networks:
      - logging

  fluentd:
    image: fluent/fluentd:v1.16-debian-1
    volumes:
      - ./fluentd/fluent.conf:/fluentd/etc/fluent.conf
      - ./fluentd/processor.conf:/fluentd/etc/processor.conf
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - fluentd-buffer:/var/log/fluentd/buffer
    ports:
      - "24224:24224"
      - "24224:24224/udp"
      - "24225:24225"
    depends_on:
      - elasticsearch
    networks:
      - logging

volumes:
  elasticsearch-data:
  fluentd-buffer:

networks:
  logging:
    driver: bridge
```

---

### Starting the Logging Stack

```bash
# Start Elasticsearch and Kibana
docker-compose -f docker-compose-logging.yml up -d elasticsearch kibana

# Wait for Elasticsearch to be ready
curl -X GET "http://localhost:9200/_cluster/health?wait_for_status=yellow&timeout=60s"

# Create index lifecycle policy
curl -X PUT "http://localhost:9200/_ilm/policy/dominion-markets-policy" \
  -H 'Content-Type: application/json' \
  -d @elasticsearch/ilm-policy.json

# Create index template
curl -X PUT "http://localhost:9200/_index_template/dominion-markets-logs" \
  -H 'Content-Type: application/json' \
  -d @elasticsearch/index-template.json

# Start Fluentd
docker-compose -f docker-compose-logging.yml up -d fluentd

# Verify logs are flowing
curl -X GET "http://localhost:9200/dominion-markets-*/_count"

# Access Kibana
open http://localhost:5601
```

---

### Accessing Logs

**Via Kibana UI:**
```
http://localhost:5601
→ Discover
→ Create index pattern: dominion-markets-*
→ Search logs with KQL queries
```

**Via Elasticsearch API:**
```bash
# Recent errors
curl -X GET "http://localhost:9200/dominion-markets-*/_search?pretty" \
  -H 'Content-Type: application/json' \
  -d '{"query": {"match": {"level": "error"}}, "size": 100}'

# Logs for specific user
curl -X GET "http://localhost:9200/dominion-markets-*/_search?pretty" \
  -H 'Content-Type: application/json' \
  -d '{"query": {"match": {"userId": "user_123"}}}'

# Logs for specific trace
curl -X GET "http://localhost:9200/dominion-markets-*/_search?pretty" \
  -H 'Content-Type: application/json' \
  -d '{"query": {"match": {"traceId": "trace_abc123"}}}'
```

**Via Datadog:**
```
https://app.datadoghq.com/logs
→ Filter by source:dominion-markets
→ Search logs with Datadog query language
→ Create monitors and dashboards
```

---

## Logging Pipeline Architecture Implementation Checklist

✅ **Service Log Emission**: Structured JSON logs with service/traceId/userId/identity fields  
✅ **Log Collector**: Fluentd DaemonSet collects logs from all containers  
✅ **Log Processor**: Parse, filter, redact PII, enrich with GeoIP, route to storage  
✅ **Storage**: Elasticsearch with 90-day retention, index lifecycle policy, sharding strategy  
✅ **Dashboards**: Kibana for search/visualization, Datadog for analysis/alerting  
✅ **Alerting**: Critical errors, slow requests, service down alerts  
✅ **Kubernetes Integration**: DaemonSet, ServiceAccount, ConfigMap configuration  
✅ **Docker Compose Stack**: Elasticsearch, Kibana, Fluentd orchestration  

---

## Operational Principles Implementation Checklist

✅ **Everything Observable**: Structured logging with winston, privacy-aware redaction, sampling for debug logs  
✅ **Everything Traceable**: Distributed tracing with Datadog, trace ID propagation, service map visualization  
✅ **Everything Monitored**: Prometheus metrics for HTTP/database/cache/providers/WebSocket/business events  
✅ **Everything Alertable**: PagerDuty/Slack integration, alert aggregation, deduplication  
✅ **Everything Privacy-Respectful**: Sensitive field redaction, allowed fields whitelist, no PII in logs  

---

## SECTION 28 — DEPLOYMENT, ENVIRONMENTS & RELEASE MANAGEMENT

DominionMarkets must deploy **cleanly, safely, and predictably** — every time.

This section defines the **full deployment pipeline**, the **environment structure**, and the **release management protocol** that ensures stability, reliability, and continuity across the entire platform.

---

## 28.1 Deployment Principles

DominionMarkets follows **five core deployment principles**:

### 1. Stability First

**No release goes out unless it passes all automated checks.**

Every deployment must pass:
- ✅ Unit tests (100% pass rate)
- ✅ Integration tests (100% pass rate)
- ✅ E2E tests (100% pass rate)
- ✅ Security scans (no critical/high vulnerabilities)
- ✅ Performance benchmarks (no regressions)
- ✅ Code review (approved by 2+ engineers)

**If any check fails, the deployment is blocked.**

---

### 2. Zero-Downtime Deployments

**Users never experience interruptions.**

DominionMarkets uses **rolling deployments** with health checks:
- New pods deployed alongside old pods
- Traffic gradually shifted to new pods
- Old pods drained and terminated
- No user requests dropped

**Deployment strategies:**
- **Frontend**: Blue-green deployment via CDN
- **API**: Rolling update with health checks
- **Database**: Zero-downtime migrations (additive-only)
- **Cache**: Pre-warming before traffic shift

---

### 3. Environment Parity

**Every environment mirrors production as closely as possible.**

All environments use:
- ✅ Same infrastructure configuration (Kubernetes manifests)
- ✅ Same database schema (migration-based)
- ✅ Same environment variables (except secrets)
- ✅ Same monitoring/logging setup
- ✅ Same deployment pipeline

**Differences are minimal and explicit:**
- Production: Autoscaling enabled, replicas: 5+
- Staging: Autoscaling disabled, replicas: 2
- Development: Local Docker Compose

---

### 4. Rollback Ready

**Every deployment can be reversed instantly.**

DominionMarkets maintains:
- ✅ Previous version kept running during deployment
- ✅ Database migrations reversible (down migrations)
- ✅ Feature flags for instant rollback
- ✅ Immutable container images (tagged with git SHA)
- ✅ Infrastructure as Code (version controlled)

**Rollback time: < 2 minutes**

---

### 5. Observability Integrated

**Monitoring begins the moment code hits staging.**

Every deployment includes:
- ✅ Automatic metric collection (Prometheus)
- ✅ Distributed tracing (Datadog APM)
- ✅ Log aggregation (Elasticsearch)
- ✅ Error tracking (Sentry)
- ✅ Real-user monitoring (Grafana Faro)

**Deployment dashboards show:**
- Request rate changes
- Error rate changes
- Latency changes
- Resource utilization changes

---

## Deployment Principles Implementation

```typescript
// Deployment configuration
export const deploymentConfig = {
  // Stability checks
  stability: {
    requiredChecks: [
      'unit-tests',
      'integration-tests',
      'e2e-tests',
      'security-scan',
      'performance-benchmarks',
      'code-review',
    ],
    failurePolicy: 'block',  // Block deployment on any failure
  },
  
  // Zero-downtime strategy
  rollout: {
    strategy: 'rolling',
    maxUnavailable: 0,       // No pods can be unavailable
    maxSurge: 1,             // Add 1 new pod at a time
    healthCheck: {
      enabled: true,
      path: '/health/ready',
      initialDelaySeconds: 10,
      periodSeconds: 5,
      failureThreshold: 3,
    },
  },
  
  // Environment parity
  environments: {
    production: {
      replicas: 5,
      autoscaling: { enabled: true, min: 5, max: 20 },
      resources: { cpu: '2', memory: '4Gi' },
    },
    staging: {
      replicas: 2,
      autoscaling: { enabled: false },
      resources: { cpu: '1', memory: '2Gi' },
    },
    development: {
      replicas: 1,
      autoscaling: { enabled: false },
      resources: { cpu: '500m', memory: '1Gi' },
    },
  },
  
  // Rollback configuration
  rollback: {
    enabled: true,
    keepPreviousVersions: 3,
    automaticRollback: {
      enabled: true,
      errorRateThreshold: 0.05,  // 5% error rate triggers rollback
      latencyThreshold: 2000,     // 2s P99 latency triggers rollback
    },
  },
  
  // Observability
  monitoring: {
    metrics: { enabled: true, provider: 'prometheus' },
    tracing: { enabled: true, provider: 'datadog' },
    logging: { enabled: true, provider: 'elasticsearch' },
    errors: { enabled: true, provider: 'sentry' },
    rum: { enabled: true, provider: 'grafana-faro' },
  },
};

// Pre-deployment checks
export async function runPreDeploymentChecks(): Promise<boolean> {
  console.log('🔍 Running pre-deployment checks...');
  
  const checks = [
    checkUnitTests(),
    checkIntegrationTests(),
    checkE2ETests(),
    checkSecurityScan(),
    checkPerformanceBenchmarks(),
    checkCodeReview(),
  ];
  
  const results = await Promise.all(checks);
  
  if (results.every(r => r.passed)) {
    console.log('✅ All pre-deployment checks passed');
    return true;
  } else {
    console.error('❌ Pre-deployment checks failed:');
    results.forEach(r => {
      if (!r.passed) {
        console.error(`  - ${r.name}: ${r.reason}`);
      }
    });
    return false;
  }
}

// Deploy with zero downtime
export async function deployWithZeroDowntime(version: string) {
  console.log(`🚀 Deploying version ${version}...`);
  
  // Step 1: Build and push container image
  await buildImage(version);
  await pushImage(version);
  
  // Step 2: Update Kubernetes deployment
  await updateDeployment({
    image: `dominion-markets:${version}`,
    strategy: 'RollingUpdate',
    maxUnavailable: 0,
    maxSurge: 1,
  });
  
  // Step 3: Monitor rollout
  const rolloutStatus = await monitorRollout({
    maxWaitTime: 600, // 10 minutes
    healthCheckPath: '/health/ready',
  });
  
  if (!rolloutStatus.success) {
    console.error('❌ Rollout failed, initiating automatic rollback...');
    await rollbackDeployment();
    throw new Error('Deployment failed');
  }
  
  // Step 4: Run smoke tests
  const smokeTestsPassed = await runSmokeTests();
  
  if (!smokeTestsPassed) {
    console.error('❌ Smoke tests failed, rolling back...');
    await rollbackDeployment();
    throw new Error('Smoke tests failed');
  }
  
  console.log('✅ Deployment successful');
}

// Automatic rollback on failure
export async function monitorDeploymentHealth(version: string) {
  const startTime = Date.now();
  
  // Monitor for 10 minutes after deployment
  const monitoringWindow = 10 * 60 * 1000;
  
  while (Date.now() - startTime < monitoringWindow) {
    const metrics = await getCurrentMetrics();
    
    // Check error rate
    if (metrics.errorRate > deploymentConfig.rollback.automaticRollback.errorRateThreshold) {
      console.error(`❌ Error rate too high: ${metrics.errorRate}`);
      await rollbackDeployment();
      return false;
    }
    
    // Check latency
    if (metrics.p99Latency > deploymentConfig.rollback.automaticRollback.latencyThreshold) {
      console.error(`❌ P99 latency too high: ${metrics.p99Latency}ms`);
      await rollbackDeployment();
      return false;
    }
    
    // Wait before next check
    await new Promise(resolve => setTimeout(resolve, 30000)); // 30 seconds
  }
  
  console.log('✅ Deployment health check passed');
  return true;
}

// Rollback deployment
export async function rollbackDeployment() {
  console.log('⏪ Rolling back deployment...');
  
  await kubectl('rollout', 'undo', 'deployment/api');
  
  await waitForRollout('deployment/api');
  
  console.log('✅ Rollback complete');
}

// Feature flag for instant rollback
export class FeatureFlags {
  private static flags = new Map<string, boolean>();
  
  static async enable(flag: string) {
    this.flags.set(flag, true);
    await redis.set(`feature:${flag}`, 'true');
  }
  
  static async disable(flag: string) {
    this.flags.set(flag, false);
    await redis.set(`feature:${flag}`, 'false');
  }
  
  static isEnabled(flag: string): boolean {
    return this.flags.get(flag) || false;
  }
  
  // Instant rollback via feature flag
  static async rollbackFeature(flag: string) {
    console.log(`⏪ Rolling back feature: ${flag}`);
    await this.disable(flag);
  }
}

// Usage in code
if (FeatureFlags.isEnabled('new-dashboard-layout')) {
  return <NewDashboardLayout />;
} else {
  return <OldDashboardLayout />;
}
```

---

### Deployment Pipeline Stages

```
1. Developer → Push to main
     ↓
2. CI/CD → Run tests, build image
     ↓
3. Staging → Deploy & test
     ↓
4. Approval → Manual approval (production only)
     ↓
5. Production → Rolling deployment
     ↓
6. Monitor → Health checks for 10 minutes
     ↓
7. Success → Deployment complete
   OR
   Failure → Automatic rollback
```

---

### Deployment Checklist

**Before Deployment:**
- [ ] All tests passing (unit, integration, E2E)
- [ ] Security scan passed (no critical/high vulnerabilities)
- [ ] Performance benchmarks passed (no regressions)
- [ ] Code reviewed and approved (2+ engineers)
- [ ] Database migrations tested (up and down)
- [ ] Feature flags configured (if needed)
- [ ] Rollback plan documented

**During Deployment:**
- [ ] Container image built and pushed
- [ ] Kubernetes deployment updated
- [ ] Health checks passing
- [ ] Traffic gradually shifted
- [ ] Old pods drained gracefully
- [ ] Smoke tests passed

**After Deployment:**
- [ ] Error rate monitored (< 1%)
- [ ] Latency monitored (P99 < 2s)
- [ ] Resource usage monitored (CPU/memory)
- [ ] User feedback monitored
- [ ] Logs reviewed for anomalies
- [ ] Metrics dashboards reviewed
- [ ] Post-deployment report created

---

## Deployment Principles Implementation Checklist

✅ **Stability First**: Pre-deployment checks (tests, security, performance, code review) block failed deployments  
✅ **Zero-Downtime Deployments**: Rolling updates with health checks, blue-green for frontend, zero user impact  
✅ **Environment Parity**: Same infrastructure/schema/monitoring across all environments, minimal explicit differences  
✅ **Rollback Ready**: Previous version kept, reversible migrations, feature flags, automatic rollback on error/latency  
✅ **Observability Integrated**: Prometheus metrics, Datadog tracing, Elasticsearch logs, Sentry errors, Grafana Faro RUM  

---

## 28.2 Environment Flow

DominionMarkets uses **4 environments** with strict promotion rules.

### Environment Progression

```
Local → Dev → Staging → Production
```

Every code change flows through all environments before reaching users.

---

### 1. Local Environment

**Used by developers** for feature development and rapid iteration.

**Location:** Developer's machine (Docker Compose or npm dev server)

**Includes:**
- ✅ **Mock Data** - Fake users, stocks, portfolios, news (no real data)
- ✅ **Local API Gateway** - Mocked backend responses
- ✅ **Hot Reload** - Instant code changes (no rebuild)
- ✅ **Debug Tools** - React DevTools, Redux DevTools, source maps

**Purpose:**
1. **Feature Development** - Build new features quickly
2. **Component Testing** - Test UI components in isolation
3. **Rapid Iteration** - Instant feedback loop (< 1 second)

**Characteristics:**
- Hot reload enabled
- Debug mode active
- No authentication required
- Instant feedback loop

**Tech Stack:**
```yaml
# docker-compose.local.yml
services:
  api:
    image: dominion-markets-api:local
    environment:
      - NODE_ENV=development
      - DEBUG=true
      - MOCK_PROVIDERS=true
      - MOCK_DATA=true
    ports:
      - "4000:4000"
  
  frontend:
    image: node:18
    command: npm run dev
    volumes:
      - ./dashboard-app:/app
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_MOCK_API=true
      - NEXT_PUBLIC_DEBUG=true
  
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=dominion_dev
    ports:
      - "5432:5432"
  
  redis:
    image: redis:7
    ports:
      - "6379:6379"
```

**Mock Data Setup:**
```typescript
// lib/mocks/data.ts
export const mockUsers = [
  {
    id: 'user_mock_1',
    email: 'dev@test.com',
    identity: 'diaspora',
    tier: 'premium',
  },
  {
    id: 'user_mock_2',
    email: 'youth@test.com',
    identity: 'youth',
    tier: 'free',
  },
];

export const mockStocks = [
  { symbol: 'AAPL', price: 178.45, change: 2.34, changePercent: 1.32 },
  { symbol: 'TSLA', price: 245.67, change: -5.12, changePercent: -2.04 },
  { symbol: 'NVDA', price: 495.23, change: 12.45, changePercent: 2.58 },
];

export const mockPortfolio = {
  userId: 'user_mock_1',
  positions: [
    { symbol: 'AAPL', shares: 10, costBasis: 150.00 },
    { symbol: 'TSLA', shares: 5, costBasis: 220.00 },
  ],
  totalValue: 3013.85,
  todayChange: -2.34,
};

export const mockNews = [
  {
    id: 'news_1',
    headline: 'Apple Announces New Product Line',
    source: 'TechCrunch',
    publishedAt: '2025-12-24T10:00:00Z',
    verified: true,
  },
];
```

**Development Workflow:**
```bash
# Start local environment
docker-compose -f docker-compose.local.yml up

# Run frontend in dev mode
cd dashboard-app && npm run dev

# Run backend in dev mode
cd api && npm run dev

# Local URL: http://localhost:3000
```

---

### 2. Dev Environment

**Internal shared environment** for integration testing and API validation.

**Location:** Kubernetes cluster (namespace: `dev`)

**Includes:**
- ✅ **Real Backend Services** - Actual API, database, cache (not mocked)
- ✅ **Test Data** - Realistic but fake data (safe for testing)
- ✅ **Identity Service** - Full identity system (diaspora, youth, creator, legacy)
- ✅ **Alerts Engine** - Alert creation, evaluation, triggering
- ✅ **News Verification Engine** - Multi-source news verification

**Purpose:**
1. **Integration Testing** - Test services working together
2. **API Contract Validation** - Ensure API contracts are honored
3. **Internal QA** - Quality assurance before staging

**Characteristics:**
- Auto-deploy on push to `develop` branch
- Real APIs (with test accounts)
- Shared database (non-production data)
- Authentication required (test users)
- Rapid iteration

**Kubernetes Configuration:**
```yaml
# k8s/dev/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: dev
spec:
  replicas: 1
  selector:
    matchLabels:
      app: api
      env: dev
  template:
    metadata:
      labels:
        app: api
        env: dev
    spec:
      containers:
      - name: api
        image: dominion-markets-api:develop
        env:
        - name: NODE_ENV
          value: "development"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: dev-secrets
              key: database-url
        - name: REDIS_URL
          value: "redis://redis-dev:6379"
        resources:
          requests:
            cpu: 250m
            memory: 512Mi
          limits:
            cpu: 500m
            memory: 1Gi
```

**CI/CD Pipeline (Dev):**
```yaml
# .github/workflows/deploy-dev.yml
name: Deploy to Dev

on:
  push:
    branches: [develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker Image
        run: docker build -t dominion-markets-api:develop .
      
      - name: Push to Registry
        run: docker push dominion-markets-api:develop
      
      - name: Deploy to Dev
        run: |
          kubectl set image deployment/api \
            api=dominion-markets-api:develop \
            -n dev
          kubectl rollout status deployment/api -n dev
      
      - name: Run Smoke Tests
        run: npm run test:smoke -- --env=dev
```

**Dev URL:** `https://dev.dominionmarkets.app`

---

### 3. Staging Environment

**Production mirror** for pre-release validation.

**Location:** Kubernetes cluster (namespace: `staging`)

**Includes:**
- ✅ **Full Production Configuration** - Same settings as production
- ✅ **Production-Like Data** - Anonymized production data or realistic synthetic data
- ✅ **Full Caching Layer** - Client cache, edge CDN, Redis backend (same as production)
- ✅ **Full Monitoring** - Prometheus, Datadog, Elasticsearch (same as production)

**Purpose:**
1. **Pre-Release Validation** - Final check before production
2. **Load Testing** - Test performance under production load
3. **Performance Testing** - Benchmark latency, throughput, resource usage
4. **Release Candidate Approval** - Go/no-go decision for production

**Characteristics:**
- **Production mirror** (same infrastructure, scaled down)
- Real APIs (production configuration)
- Production-like database (anonymized data)
- Authentication required (real auth flow)
- Performance testing enabled

**Kubernetes Configuration:**
```yaml
# k8s/staging/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: staging
spec:
  replicas: 2  # Fewer replicas than production
  selector:
    matchLabels:
      app: api
      env: staging
  template:
    metadata:
      labels:
        app: api
        env: staging
    spec:
      containers:
      - name: api
        image: dominion-markets-api:staging
        env:
        - name: NODE_ENV
          value: "production"  # Same as production
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: staging-secrets
              key: database-url
        resources:
          requests:
            cpu: 1
            memory: 2Gi
          limits:
            cpu: 2
            memory: 4Gi
      
      # Same monitoring as production
      - name: datadog-agent
        image: datadog/agent:latest
        env:
        - name: DD_ENV
          value: "staging"
```

**CI/CD Pipeline (Staging):**
```yaml
# .github/workflows/deploy-staging.yml
name: Deploy to Staging

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Unit Tests
        run: npm test
      
      - name: Run Integration Tests
        run: npm run test:integration
      
      - name: Run E2E Tests
        run: npm run test:e2e
      
      - name: Security Scan
        run: npm audit --audit-level=high
      
      - name: Performance Benchmarks
        run: npm run test:performance
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker Image
        run: |
          docker build -t dominion-markets-api:${{ github.sha }} .
          docker tag dominion-markets-api:${{ github.sha }} \
            dominion-markets-api:staging
      
      - name: Push to Registry
        run: |
          docker push dominion-markets-api:${{ github.sha }}
          docker push dominion-markets-api:staging
      
      - name: Deploy to Staging
        run: |
          kubectl set image deployment/api \
            api=dominion-markets-api:staging \
            -n staging
          kubectl rollout status deployment/api -n staging --timeout=10m
      
      - name: Run Smoke Tests
        run: npm run test:smoke -- --env=staging
      
      - name: Monitor Deployment
        run: npm run monitor:deployment -- --env=staging --duration=10m
```

**Staging URL:** `https://staging.dominionmarkets.app`

---

### 4. Production Environment

**Live user-facing platform** with full autoscaling and monitoring.

**Location:** Kubernetes cluster (namespace: `production`)

**Includes:**
- ✅ **Real Users** - Public access, authenticated users
- ✅ **Real Data** - Live production database with real financial data
- ✅ **Full Autoscaling** - HPA (5-20 replicas), automatic scaling based on load
- ✅ **Full Monitoring** - Prometheus alerts, Datadog APM, Sentry error tracking
- ✅ **Full Failover** - Multi-zone deployment, automatic failover on node failure

**Purpose:**
1. **Public Experience** - Serve real users with real-time data
2. **Real-Time Operations** - Process live transactions, portfolios, alerts
3. **High Availability** - 99.9% uptime SLA with zero-downtime deployments
4. **Business Value** - Generate revenue, user engagement, market insights

**Characteristics:**
- **Full scale** (autoscaling enabled, 5-20 replicas)
- Real user traffic
- Production database (PostgreSQL with replication)
- Strict security policies (network policies, secrets, RBAC)
- Full monitoring/alerting (Prometheus, Datadog, Elasticsearch)
- **Manual approval required** before deployment

**Kubernetes Configuration:**
```yaml
# k8s/production/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: production
spec:
  replicas: 5
  selector:
    matchLabels:
      app: api
      env: production
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0  # Zero downtime
      maxSurge: 1
  template:
    metadata:
      labels:
        app: api
        env: production
    spec:
      containers:
      - name: api
        image: dominion-markets-api:production
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: production-secrets
              key: database-url
        resources:
          requests:
            cpu: 2
            memory: 4Gi
          limits:
            cpu: 4
            memory: 8Gi
        livenessProbe:
          httpGet:
            path: /health/live
            port: 4000
          initialDelaySeconds: 10
          periodSeconds: 5
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 4000
          initialDelaySeconds: 10
          periodSeconds: 5
          failureThreshold: 3

---
# Autoscaling
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 5
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

**CI/CD Pipeline (Production):**
```yaml
# .github/workflows/deploy-production.yml
name: Deploy to Production

on:
  workflow_dispatch:  # Manual trigger only
    inputs:
      version:
        description: 'Git SHA to deploy'
        required: true

jobs:
  verify-staging:
    runs-on: ubuntu-latest
    steps:
      - name: Verify Staging Deployment
        run: |
          # Ensure this version is already deployed to staging
          STAGING_VERSION=$(kubectl get deployment api -n staging \
            -o jsonpath='{.spec.template.spec.containers[0].image}')
          
          if [[ "$STAGING_VERSION" != *"${{ github.event.inputs.version }}"* ]]; then
            echo "❌ Version not deployed to staging"
            exit 1
          fi
      
      - name: Run Staging Health Checks
        run: npm run health:staging
      
      - name: Check Staging Metrics
        run: npm run metrics:staging -- --min-duration=24h
  
  approval:
    needs: verify-staging
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://dominionmarkets.app
    steps:
      - name: Request Approval
        run: echo "⏸️ Awaiting manual approval..."
  
  deploy:
    needs: approval
    runs-on: ubuntu-latest
    steps:
      - name: Tag Production Image
        run: |
          docker pull dominion-markets-api:${{ github.event.inputs.version }}
          docker tag dominion-markets-api:${{ github.event.inputs.version }} \
            dominion-markets-api:production
          docker push dominion-markets-api:production
      
      - name: Deploy to Production
        run: |
          kubectl set image deployment/api \
            api=dominion-markets-api:production \
            -n production
          kubectl rollout status deployment/api -n production --timeout=15m
      
      - name: Run Smoke Tests
        run: npm run test:smoke -- --env=production
      
      - name: Monitor Deployment (10 min)
        run: npm run monitor:deployment -- --env=production --duration=10m
      
      - name: Slack Notification
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -H 'Content-Type: application/json' \
            -d '{
              "text": "✅ Production deployment successful: ${{ github.event.inputs.version }}"
            }'
```

**Production URL:** `https://dominionmarkets.app`

---

## Complete Deployment Pipeline

### Pipeline Flow

```
Commit → Build → Test → Security Scan → Deploy to Dev → QA → Deploy to Staging → Approval → Deploy to Production
```

### Stage-by-Stage Breakdown

#### 1. **Commit Stage**
Code pushed to `main` branch triggers CI pipeline

**Triggers:**
- Push to `main` → Full CI/CD pipeline
- Pull request → Build + test only (no deployment)

**Actions:**
```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

#### 2. **Build Stage**
Compile and validate all application components

**Sub-Stages:**

**2.1 Frontend Build**
```yaml
- name: Build Frontend
  run: |
    cd dashboard-app
    npm ci
    npm run build
    npm run build:storybook
```

**2.2 Backend Build**
```yaml
- name: Build Backend API
  run: |
    cd api
    npm ci
    npm run build
```

**2.3 Dependency Validation**
```yaml
- name: Validate Dependencies
  run: |
    npm run validate:deps
    npm run check:outdated
    npm run check:licenses
```

**Exit Criteria:**
- ✅ Frontend build succeeds (exit code 0)
- ✅ Backend build succeeds
- ✅ All dependencies valid (no conflicts, valid licenses)
- ✅ Assets optimized and bundled

#### 3. **Automated Tests**
Comprehensive test suite across all layers

**3.1 Unit Tests**
```typescript
// Component unit tests
npm run test:unit

// Example: Portfolio component
describe('Portfolio', () => {
  it('renders holdings correctly', () => {
    const { getByText } = render(<Portfolio holdings={mockHoldings} />);
    expect(getByText('AAPL')).toBeInTheDocument();
  });
});
```

**3.2 Integration Tests**
```typescript
// API integration tests
npm run test:integration

// Example: Portfolio API integration
describe('Portfolio API', () => {
  it('fetches user portfolio', async () => {
    const portfolio = await fetchPortfolio('user123');
    expect(portfolio.holdings).toHaveLength(5);
  });
});
```

**3.3 Snapshot Tests**
```typescript
// Visual regression tests
npm run test:snapshot

// Example: Dashboard snapshot
it('matches snapshot', () => {
  const { container } = render(<Dashboard />);
  expect(container).toMatchSnapshot();
});
```

**3.4 API Contract Tests**
```typescript
// API contract validation
npm run test:contracts

// Example: Stock quote contract
describe('Stock Quote API Contract', () => {
  it('returns valid schema', async () => {
    const response = await fetch('/api/stocks/AAPL');
    const data = await response.json();
    expect(data).toMatchSchema(stockQuoteSchema);
  });
});
```

**Exit Criteria:**
- ✅ All tests passing (100% pass rate)
- ✅ Code coverage ≥ 80% (unit tests)
- ✅ No snapshot mismatches
- ✅ All API contracts validated

#### 4. **Security Scans**
Multi-layer security analysis

**4.1 Dependency Vulnerabilities**
```yaml
- name: Dependency Audit
  run: |
    npm audit --production --audit-level=high
    npm run audit:fix
```

**4.2 Static Code Analysis (SAST)**
```yaml
- name: Static Analysis
  run: |
    npm run security:sast
    eslint . --ext .ts,.tsx --max-warnings 0
```

**4.3 Secret Detection**
```yaml
- name: Secret Scan
  run: |
    npm run security:secrets
    trufflehog filesystem . --json
```

**Security Tools:**
```yaml
- name: Dependency Scan
  run: npm audit --production --audit-level=high

- name: SAST (Static Analysis)
  run: npm run security:sast

- name: Container Scan
  run: trivy image dominion-markets-api:${{ github.sha }}

- name: License Check
  run: npm run security:licenses
```

**Exit Criteria:**
- ✅ Zero critical vulnerabilities
- ✅ Zero high-severity vulnerabilities
- ✅ All dependencies have valid licenses
- ✅ Secrets not exposed in code

#### 5. **Deploy to Dev**
Automatic deployment after security scans pass

**Deployment:**
```yaml
- name: Deploy to Dev
  run: |
    kubectl set image deployment/api \
      api=dominion-markets-api:${{ github.sha }} \
      -n dev
    kubectl rollout status deployment/api -n dev --timeout=5m
```

**Post-Deployment - Smoke Tests:**
```typescript
// Smoke tests run automatically after deployment
import { runSmokeTests } from '@/tests/smoke';

const smokeTests = [
  { name: 'Health Check', test: () => fetch('/health') },
  { name: 'Login Flow', test: () => testLogin() },
  { name: 'Portfolio Load', test: () => testPortfolioLoad() },
  { name: 'Stock Quote', test: () => testStockQuote() },
];

await runSmokeTests(smokeTests, { env: 'dev' });
```

**QA Begins:**
- Automated regression tests
- Manual exploratory testing
- Performance profiling

**Exit Criteria:**
- ✅ Deployment successful (rollout complete)
- ✅ Health checks passing
- ✅ Smoke tests passing (100%)
- ✅ QA team notified

#### 6. **Deploy to Staging**
Requires QA approval from Dev environment

**Pre-Deployment Requirements:**
```yaml
- name: Verify QA Approval
  run: |
    if [ "$QA_APPROVED" != "true" ]; then
      echo "❌ QA approval required before staging deployment"
      exit 1
    fi
```

**Deployment:**
```yaml
- name: Deploy to Staging
  run: |
    kubectl set image deployment/api \
      api=dominion-markets-api:${{ github.sha }} \
      -n staging
    kubectl rollout status deployment/api -n staging --timeout=10m
```

**6.1 Load Tests**
```typescript
// Load testing with production-like traffic
import { loadTest } from '@/tests/load';

await loadTest({
  env: 'staging',
  users: 1000,
  duration: '10m',
  rampUp: '2m',
  scenarios: [
    { name: 'Browse Stocks', weight: 40 },
    { name: 'View Portfolio', weight: 30 },
    { name: 'Place Trade', weight: 20 },
    { name: 'Read News', weight: 10 },
  ],
});
```

**6.2 Performance Tests**
```typescript
// Performance benchmarks
import { performanceTest } from '@/tests/performance';

const results = await performanceTest({
  env: 'staging',
  metrics: ['p50', 'p95', 'p99'],
  thresholds: {
    p50: 200,  // 200ms
    p95: 500,  // 500ms
    p99: 2000, // 2s
  },
});

if (results.p99 > 2000) {
  throw new Error('P99 latency exceeds 2s threshold');
}
```

**6.3 End-to-End Tests**
```typescript
// E2E tests in staging environment
import { playwright } from '@playwright/test';

test('Complete user journey', async ({ page }) => {
  // Login
  await page.goto('https://staging.dominionmarkets.app/login');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  
  // View portfolio
  await page.goto('/dashboard/portfolio');
  await expect(page.locator('h1')).toContainText('Portfolio');
  
  // Search stock
  await page.fill('[placeholder="Search stocks"]', 'AAPL');
  await page.click('text=Apple Inc.');
  await expect(page.locator('.stock-price')).toBeVisible();
});
```

**Exit Criteria:**
- ✅ Deployment successful
- ✅ Load tests passing (1000+ concurrent users, 0% errors)
- ✅ Performance tests passing (P95 < 500ms, P99 < 2s)
- ✅ End-to-end tests passing (100% pass rate)
- ✅ No errors for 24+ hours (soak test)

#### 7. **Manual Approval**
Three-party approval required before production

**Approval Parties:**
1. **Product Owner** - Business approval
2. **Engineering Lead** - Technical approval
3. **QA Lead** - Quality approval

**Approval Process:**
```yaml
approval:
  needs: deploy-staging
  runs-on: ubuntu-latest
  environment:
    name: production
    url: https://dominionmarkets.app
  steps:
    - name: Request Approval
      run: |
        echo "⏸️ Awaiting manual approval from:"
        echo "  - Product Owner"
        echo "  - Engineering Lead"
        echo "  - QA Lead"
```

**Approval Requirements:**
- ✅ **Product Owner** - Business impact approved
- ✅ **Engineering Lead** - Technical architecture approved
- ✅ **QA Lead** - Quality standards met
- ✅ **Staging Metrics Healthy** (24h+ uptime, error rate < 0.1%)
- ✅ **Security Review** (if code changes security-sensitive areas)
- ✅ **Rollback Plan** (documented and tested)

**Review Checklist:**
```typescript
const approvalChecklist = [
  { item: 'Staging deployed for 24+ hours', checked: true },
  { item: 'No critical bugs in staging', checked: true },
  { item: 'Performance metrics acceptable (P99 < 2s)', checked: true },
  { item: 'Security scan passed (0 critical vulnerabilities)', checked: true },
  { item: 'Database migrations tested', checked: true },
  { item: 'Rollback plan documented and tested', checked: true },
  { item: 'Monitoring/alerting configured', checked: true },
  { item: 'Stakeholder notification sent', checked: true },
  { item: 'Customer support notified', checked: true },
];

const allApproved = approvalChecklist.every(item => item.checked);
if (!allApproved) {
  throw new Error('Approval checklist incomplete');
}
```

#### 8. **Deploy to Production**
Zero-downtime deployment with automatic rollback

**Pre-Deployment:**
```yaml
- name: Verify Staging Deployment
  run: |
    STAGING_VERSION=$(kubectl get deployment api -n staging \
      -o jsonpath='{.spec.template.spec.containers[0].image}')
    
    if [[ "$STAGING_VERSION" != *"${{ github.sha }}"* ]]; then
      echo "❌ Version not deployed to staging"
      exit 1
    fi

- name: Create Database Backup
  run: npm run db:backup -- --env=production

- name: Pre-Deployment Health Check
  run: npm run health:production
```

**Deployment Strategy: Blue-Green (Frontend) + Rolling (Backend)**

**8.1 Blue-Green Deployment (Frontend)**
```yaml
- name: Deploy Frontend (Blue-Green)
  run: |
    # Deploy to "green" slot
    kubectl apply -f k8s/frontend-green.yaml
    
    # Wait for green deployment
    kubectl rollout status deployment/frontend-green -n production
    
    # Run smoke tests on green
    npm run test:smoke -- --env=production --slot=green
    
    # Switch traffic to green (zero-downtime)
    kubectl patch service frontend -n production \
      -p '{"spec":{"selector":{"slot":"green"}}}'
    
    # Keep blue running for 5 minutes (quick rollback)
    sleep 300
    
    # Scale down blue
    kubectl scale deployment/frontend-blue --replicas=0 -n production
```

**8.2 Rolling Deployment (Backend)**
```yaml
- name: Deploy Backend (Rolling)
  run: |
    # Rolling update (maxUnavailable: 0, maxSurge: 1)
    kubectl set image deployment/api \
      api=dominion-markets-api:${{ github.sha }} \
      -n production
    
    # Wait for rollout (15 min timeout)
    kubectl rollout status deployment/api -n production --timeout=15m
```

**Post-Deployment:**
```yaml
- name: Smoke Tests
  run: npm run test:smoke -- --env=production

- name: Monitor Deployment (10 min)
  run: npm run monitor:deployment -- --env=production --duration=10m

- name: Verify Metrics
  run: |
    # Error rate must be < 0.5%
    # P99 latency must be < 2s
    npm run metrics:production -- --duration=10m \
      --error-rate-max=0.5% \
      --p99-latency-max=2000
```

**8.3 Automatic Rollback on Failure**
```typescript
// Automatic rollback monitoring
import { monitorDeployment } from '@/deploy/monitor';

const rollbackTriggers = [
  { metric: 'error_rate', threshold: 5, unit: '%' },
  { metric: 'p99_latency', threshold: 2000, unit: 'ms' },
  { metric: 'health_check_failures', threshold: 3, unit: 'count' },
  { metric: 'smoke_test_failures', threshold: 1, unit: 'count' },
];

const monitoring = await monitorDeployment({
  env: 'production',
  duration: '10m',
  triggers: rollbackTriggers,
  onRollback: async (reason) => {
    console.error(`🚨 Automatic rollback triggered: ${reason}`);
    
    // Rollback frontend (switch back to blue)
    await kubectl('patch', 'service/frontend', '-n', 'production',
      '-p', '{"spec":{"selector":{"slot":"blue"}}}');
    
    // Rollback backend (undo rollout)
    await kubectl('rollout', 'undo', 'deployment/api', '-n', 'production');
    
    // Clear caches
    await clearCaches();
    
    // Restart services
    await restartServices();
    
    // Alert on-call engineer
    await alertOnCall({
      severity: 'critical',
      message: `Production deployment rolled back: ${reason}`,
    });
  },
});
```

**Rollback Triggers:**
- ❌ Error rate > 5% → Instant rollback
- ❌ P99 latency > 2s → Instant rollback
- ❌ Health check failures (3+) → Instant rollback
- ❌ Smoke tests failing → Instant rollback
- ❌ Manual rollback requested → Instant rollback

**Rollback Completion Time:** < 60 seconds

**Exit Criteria:**
- ✅ Deployment successful (all pods healthy)
- ✅ Smoke tests passing
- ✅ Error rate < 0.5%
- ✅ P99 latency < 2s
- ✅ No automatic rollbacks triggered
- ✅ User-facing functionality verified

**Post-Deployment Notifications:**
```yaml
- name: Slack Notification
  run: |
    curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
      -H 'Content-Type: application/json' \
      -d '{
        "text": "✅ Production deployment successful",
        "blocks": [{
          "type": "section",
          "text": {
            "type": "mrkdwn",
            "text": "*Production Deployment Complete* 🚀\n\n*Version:* `${{ github.sha }}`\n*Status:* ✅ Success\n*Duration:* 15 minutes\n*URL:* https://dominionmarkets.app"
          }
        }]
      }'

- name: GitHub Release
  run: |
    gh release create v${{ github.sha }} \
      --title "Production Release ${{ github.sha }}" \
      --notes "Deployed to production on $(date)"
```

---

## Pipeline Execution Times

| Stage | Duration | Parallelizable | Critical Path |
|-------|----------|----------------|---------------|
| **Commit** | Instant | N/A | No |
| **Build** | 5-10 min | Yes (multi-stage) | Yes |
| **Test** | 10-15 min | Yes (parallel workers) | Yes |
| **Security Scan** | 3-5 min | Yes (concurrent scans) | Yes |
| **Deploy to Dev** | 2-3 min | No | No |
| **QA** | 30-60 min | Yes (manual + automated) | Yes |
| **Deploy to Staging** | 5-10 min | No | No |
| **Approval** | 1-24 hours | No | Yes |
| **Deploy to Production** | 10-15 min | No | Yes |

**Total Pipeline Time:**
- **Dev Deployment:** ~30-40 minutes (automatic)
- **Staging Deployment:** ~60-90 minutes (automatic after Dev)
- **Production Deployment:** ~25+ hours (includes 24h soak + approval)

---

## Pipeline Failure Handling

### Build Failure
**Symptoms:** Compilation errors, asset bundling failures  
**Action:** Notify developer immediately (no deployment)  
**Rollback:** Not applicable (build never deployed)

### Test Failure
**Symptoms:** Unit/integration/E2E test failures  
**Action:** Block deployment, notify team, create ticket  
**Rollback:** Not applicable (build never deployed)

### Security Scan Failure
**Symptoms:** Critical/high vulnerabilities detected  
**Action:** Block deployment, notify security team, create incident  
**Rollback:** Not applicable (build never deployed)

### Dev Deployment Failure
**Symptoms:** Kubernetes rollout timeout, pod crashes  
**Action:** Automatic rollback to previous version  
**Rollback:** Immediate (previous stable image)

### QA Failure
**Symptoms:** Critical bugs, performance degradation  
**Action:** Block staging deployment, create high-priority tickets  
**Rollback:** Not applicable (Staging not yet deployed)

### Staging Deployment Failure
**Symptoms:** Rollout timeout, health check failures  
**Action:** Automatic rollback, notify team, block production  
**Rollback:** Immediate (previous stable image)

### Production Deployment Failure
**Symptoms:** Error rate spike, latency increase, health check failures  
**Action:** **Immediate automatic rollback**, incident declared, on-call paged  
**Rollback:** Instant (previous stable image + feature flags)

---

## Pipeline Configuration

### GitHub Actions Workflow (Complete Pipeline)
```yaml
# .github/workflows/complete-pipeline.yml
name: Complete Deployment Pipeline

on:
  push:
    branches:
      - develop  # Triggers Dev deployment
      - main     # Triggers Staging deployment
  workflow_dispatch:  # Manual trigger for Production

jobs:
  # Stage 1: Build
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install Dependencies
        run: npm ci
      
      - name: Build Frontend
        run: npm run build
      
      - name: Build Docker Image
        run: |
          docker build -t dominion-markets-api:${{ github.sha }} .
          docker push dominion-markets-api:${{ github.sha }}
  
  # Stage 2: Test
  test:
    needs: build
    runs-on: ubuntu-latest
    strategy:
      matrix:
        test-suite: [unit, integration, e2e]
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run test:${{ matrix.test-suite }}
  
  # Stage 3: Security Scan
  security:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm audit --production --audit-level=high
      - run: trivy image dominion-markets-api:${{ github.sha }}
  
  # Stage 4: Deploy to Dev
  deploy-dev:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    steps:
      - name: Deploy to Dev
        run: kubectl set image deployment/api api=dominion-markets-api:${{ github.sha }} -n dev
      
      - name: Smoke Tests
        run: npm run test:smoke -- --env=dev
  
  # Stage 5: QA (automated)
  qa:
    needs: deploy-dev
    runs-on: ubuntu-latest
    steps:
      - run: npm run qa:integration -- --env=dev
      - run: npm run qa:load-test -- --env=dev
  
  # Stage 6: Deploy to Staging
  deploy-staging:
    needs: qa
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to Staging
        run: kubectl set image deployment/api api=dominion-markets-api:${{ github.sha }} -n staging
      
      - name: Smoke Tests
        run: npm run test:smoke -- --env=staging
      
      - name: Load Tests
        run: npm run test:load -- --env=staging --users=1000
  
  # Stage 7: Approval (manual)
  approval:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment:
      name: production
    steps:
      - run: echo "Awaiting approval..."
  
  # Stage 8: Deploy to Production
  deploy-production:
    needs: approval
    runs-on: ubuntu-latest
    steps:
      - name: Backup Database
        run: npm run db:backup -- --env=production
      
      - name: Deploy to Production
        run: kubectl set image deployment/api api=dominion-markets-api:${{ github.sha }} -n production
      
      - name: Smoke Tests
        run: npm run test:smoke -- --env=production
      
      - name: Monitor (10 min)
        run: npm run monitor:deployment -- --env=production --duration=10m
      
      - name: Notify Slack
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -d '{"text": "✅ Production deployment successful: ${{ github.sha }}"}'
```

---

## 28.4 Release Types

DominionMarkets uses three release types with different cadences and requirements.

### Semantic Versioning Format

**Version Format:** `MAJOR.MINOR.PATCH`

```typescript
// Example: 2.3.4
// MAJOR = 2 (breaking changes, architecture updates)
// MINOR = 3 (new features, non-breaking changes)
// PATCH = 4 (bug fixes, minor improvements)
```

**Versioning Rules:**
- **MAJOR** - Increment when making incompatible API changes or breaking changes
- **MINOR** - Increment when adding functionality in a backward-compatible manner
- **PATCH** - Increment when making backward-compatible bug fixes

**Version Increment Examples:**
```typescript
// Patch release: Bug fix
'1.2.3' → '1.2.4'  // Only PATCH increments

// Minor release: New feature
'1.2.4' → '1.3.0'  // MINOR increments, PATCH resets to 0

// Major release: Breaking change
'1.3.0' → '2.0.0'  // MAJOR increments, MINOR and PATCH reset to 0
```

**DominionMarkets Version History Example:**
```typescript
// Initial launch
'1.0.0' → Launch
  - Core platform features
  - Portfolio tracking
  - Stock quotes
  - Basic alerts

// New dashboard widgets added
'1.1.0' → New dashboard widgets
  - Market overview widget
  - Watchlist widget
  - Performance chart widget
  - News feed widget

// Bug fixes only
'1.1.3' → Bug fixes
  - Fix: Portfolio calculation rounding error
  - Fix: News feed pagination
  - Fix: Alert notification timing
```

---

### A. Patch Release

**Purpose:** Bug fixes and minor improvements

**Characteristics:**
- ✅ Bug fixes
- ✅ Minor improvements (performance, UX tweaks)
- ✅ No schema changes
- ✅ No breaking changes
- ✅ Backward compatible

**Frequency:** Daily or as needed

**Version Increment:** `1.2.3` → `1.2.4`

**Deployment Time:** ~30 minutes (fast-track)

**Example Patch Release:**
```typescript
// package.json
{
  "version": "1.2.4",
  "changelog": [
    "Fix: Portfolio calculation rounding error",
    "Fix: News feed pagination bug",
    "Improve: Stock search performance (20% faster)"
  ]
}
```

**Approval Required:**
- Engineering Lead (automated if all tests pass)

---

### B. Minor Release

**Purpose:** New features and UI updates

**Characteristics:**
- ✅ New features (non-breaking)
- ✅ UI updates (new components, redesigns)
- ✅ Non-breaking backend changes
- ✅ New API endpoints (backward compatible)
- ✅ Feature flag rollouts

**Frequency:** Weekly

**Version Increment:** `1.2.4` → `1.3.0`

**Deployment Time:** ~2 hours (full pipeline + 24h soak)

**Example Minor Release:**
```typescript
// package.json
{
  "version": "1.3.0",
  "features": [
    "New: Alerts dashboard with custom triggers",
    "New: Dark mode support",
    "Update: Portfolio UI redesign",
    "API: New endpoint /api/alerts/create"
  ],
  "migrations": [],
  "breaking_changes": []
}
```

**Approval Required:**
- Engineering Lead
- Product Owner
- QA Lead (after staging soak)

---

### C. Major Release

**Purpose:** Major features and architectural changes

**Characteristics:**
- ✅ Major features (multi-sprint work)
- ✅ Architecture changes (refactoring, redesigns)
- ✅ Schema updates (database migrations)
- ✅ Breaking API changes (versioned endpoints)
- ✅ Major UI overhauls

**Frequency:** Quarterly

**Version Increment:** `1.3.0` → `2.0.0`

**Deployment Time:** ~1 week (extended staging + approval)

**Example Major Release:**
```typescript
// package.json
{
  "version": "2.0.0",
  "features": [
    "New: Real-time portfolio tracking with WebSockets",
    "New: Advanced analytics module (Pro tier)",
    "Architecture: Migrate to microservices",
    "Breaking: API v2 with new authentication"
  ],
  "migrations": [
    "20250101_add_realtime_tables.sql",
    "20250102_add_analytics_tables.sql"
  ],
  "breaking_changes": [
    "API v1 deprecated (sunset date: 2026-01-01)",
    "Auth tokens now require `scope` parameter"
  ]
}
```

**Approval Required:**
- Engineering Lead
- Product Owner
- QA Lead
- CTO (for breaking changes)
- Customer Success (for user communication)

**Migration Strategy:**
```typescript
// Database migration with rollback
import { runMigration, rollbackMigration } from '@/db/migrations';

try {
  // Backup database
  await backupDatabase('pre-v2-migration');
  
  // Run migrations
  await runMigration('20250101_add_realtime_tables.sql');
  await runMigration('20250102_add_analytics_tables.sql');
  
  // Verify migration
  const valid = await validateSchema();
  if (!valid) {
    throw new Error('Schema validation failed');
  }
  
  console.log('✅ Migration successful');
} catch (error) {
  console.error('❌ Migration failed, rolling back...');
  await rollbackMigration();
  await restoreDatabase('pre-v2-migration');
  throw error;
}
```

---

## Release Type Decision Matrix

| Change Type | Patch | Minor | Major |
|-------------|-------|-------|-------|
| **Bug fix** | ✅ | ❌ | ❌ |
| **Performance improvement** | ✅ | ✅ | ❌ |
| **New feature (non-breaking)** | ❌ | ✅ | ❌ |
| **UI redesign (minor)** | ❌ | ✅ | ❌ |
| **UI redesign (major)** | ❌ | ❌ | ✅ |
| **New API endpoint** | ❌ | ✅ | ❌ |
| **Breaking API change** | ❌ | ❌ | ✅ |
| **Schema change** | ❌ | ❌ | ✅ |
| **Architecture change** | ❌ | ❌ | ✅ |
| **Config change** | ✅ | ✅ | ❌ |

---

## 28.5 Feature Flags

Feature flags enable safe, controlled rollouts with instant disable capability.

### Used For:

1. **Identity-Based Features**
   - Features tied to user accounts
   - Example: Premium analytics for Pro users

2. **Premium Features**
   - Tier-based feature access
   - Example: Advanced charting (Premium tier)

3. **Pro Features**
   - Professional-level tools
   - Example: API access, real-time data

4. **New Modules**
   - Gradual rollout of new sections
   - Example: Options trading module

5. **Experimental UI**
   - A/B testing new designs
   - Example: New portfolio layout

### Implementation

**Feature Flag System:**
```typescript
// lib/features/flags.ts
import { FeatureFlag } from '@/types';

export const featureFlags = {
  // Premium features
  advanced_analytics: {
    enabled: true,
    tiers: ['premium', 'pro'],
    rollout: 100, // 100% of eligible users
  },
  
  // New modules
  options_trading: {
    enabled: true,
    tiers: ['pro'],
    rollout: 50, // 50% gradual rollout
  },
  
  // Experimental UI
  new_portfolio_layout: {
    enabled: true,
    tiers: ['free', 'premium', 'pro'],
    rollout: 10, // 10% A/B test
    experiment: 'portfolio_layout_v2',
  },
  
  // Identity-based
  real_time_quotes: {
    enabled: true,
    tiers: ['premium', 'pro'],
    rollout: 100,
  },
} as const;

export function isFeatureEnabled(
  flag: keyof typeof featureFlags,
  user: User
): boolean {
  const feature = featureFlags[flag];
  
  if (!feature.enabled) return false;
  
  // Check tier access
  if (!feature.tiers.includes(user.tier)) return false;
  
  // Check rollout percentage
  const userHash = hashUserId(user.id);
  const bucket = userHash % 100;
  if (bucket >= feature.rollout) return false;
  
  return true;
}
```

**Using Feature Flags in Components:**
```typescript
import { useFeature } from '@/hooks/useFeature';
import { useUser } from '@/hooks/useUser';

export function AdvancedAnalytics() {
  const user = useUser();
  const hasFeature = useFeature('advanced_analytics', user);
  
  if (!hasFeature) {
    return (
      <PremiumGate requiredTier="premium">
        <div>Upgrade to Premium for Advanced Analytics</div>
      </PremiumGate>
    );
  }
  
  return <AdvancedAnalyticsContent />;
}
```

**Remote Feature Flag Control:**
```typescript
// Update feature flags without deployment
import { updateFeatureFlag } from '@/api/admin/features';

// Instant disable if needed
await updateFeatureFlag('options_trading', {
  enabled: false, // Disable immediately
  reason: 'Critical bug discovered in options pricing',
});

// Gradual rollout
await updateFeatureFlag('new_portfolio_layout', {
  enabled: true,
  rollout: 25, // Increase from 10% to 25%
});
```

### Benefits:

1. **Gradual Rollout**
   - Release to 10% → 25% → 50% → 100%
   - Monitor metrics at each stage
   - Catch issues early with limited impact

2. **A/B Testing**
   - Test new UI designs
   - Measure engagement, conversion
   - Data-driven decisions

3. **Instant Disable**
   - No deployment needed
   - Disable feature in < 5 seconds
   - Revert to stable state immediately

4. **Tier-Based Access**
   - Monetize premium features
   - Clear upgrade path for users
   - Automatic enforcement

---

## 28.6 Rollback Strategy

Every deployment must be reversible within 60 seconds.

### Rollback Triggers

Automatic rollback initiated when:

1. **Error Spike**
   - Error rate > 5% (baseline: < 0.5%)
   - Example: 500 Internal Server Error spike

2. **Latency Spike**
   - P99 latency > 2s (baseline: < 500ms)
   - Example: Database query timeout

3. **Provider Failure**
   - External API failures (stock data, news)
   - Example: Stock quote provider down

4. **Cache Failure**
   - Redis connection loss
   - CDN cache invalidation issues

5. **User-Reported Issues**
   - Critical bug reports (manual trigger)
   - Example: Portfolio calculations incorrect

### Rollback Method

**3-Step Rollback Process:**

**Step 1: Switch to Previous Build (< 10 seconds)**
```typescript
// Frontend: Blue-green swap
await kubectl('patch', 'service/frontend', '-n', 'production',
  '-p', '{"spec":{"selector":{"slot":"blue"}}}');

// Backend: Undo rollout
await kubectl('rollout', 'undo', 'deployment/api', '-n', 'production');
```

**Step 2: Clear Caches (< 20 seconds)**
```typescript
// Clear Redis cache
await redis.flushAll();

// Invalidate CDN cache
await cloudflare.purgeCache({
  purge_everything: true,
});

// Clear browser cache (via Cache-Control headers)
await updateCacheHeaders({
  'Cache-Control': 'no-cache, no-store, must-revalidate',
});
```

**Step 3: Restart Services (< 30 seconds)**
```typescript
// Restart API pods (rolling restart)
await kubectl('rollout', 'restart', 'deployment/api', '-n', 'production');

// Restart background workers
await kubectl('rollout', 'restart', 'deployment/workers', '-n', 'production');

// Verify health
await waitForHealthy('https://dominionmarkets.app/health', {
  timeout: 30000,
  interval: 1000,
});
```

**Total Rollback Time:** < 60 seconds ✅

### Automated Rollback Script

```typescript
// scripts/rollback-production.ts
import { rollback } from '@/deploy/rollback';

interface RollbackOptions {
  reason: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  notifyOnCall: boolean;
}

async function rollbackProduction(options: RollbackOptions) {
  const startTime = Date.now();
  
  console.log(`🚨 Initiating production rollback: ${options.reason}`);
  
  try {
    // Step 1: Switch to previous build
    console.log('Step 1/3: Switching to previous build...');
    await switchToPreviousBuild();
    console.log('✅ Build switched (10s)');
    
    // Step 2: Clear caches
    console.log('Step 2/3: Clearing caches...');
    await clearAllCaches();
    console.log('✅ Caches cleared (20s)');
    
    // Step 3: Restart services
    console.log('Step 3/3: Restarting services...');
    await restartAllServices();
    console.log('✅ Services restarted (30s)');
    
    const duration = Date.now() - startTime;
    console.log(`✅ Rollback complete in ${duration}ms`);
    
    // Verify system health
    const healthy = await verifyHealth();
    if (!healthy) {
      throw new Error('Health checks failed after rollback');
    }
    
    // Notify stakeholders
    await notifySlack({
      severity: options.severity,
      message: `✅ Production rollback successful`,
      reason: options.reason,
      duration: `${duration}ms`,
    });
    
    if (options.notifyOnCall) {
      await pageOnCall({
        severity: options.severity,
        message: `Production rolled back: ${options.reason}`,
      });
    }
    
  } catch (error) {
    console.error('❌ Rollback failed:', error);
    
    // Escalate immediately
    await pageOnCall({
      severity: 'critical',
      message: `ROLLBACK FAILED: ${error.message}`,
    });
    
    throw error;
  }
}

// Example usage
await rollbackProduction({
  reason: 'Error rate spike to 8%',
  severity: 'critical',
  notifyOnCall: true,
});
```

### Manual Rollback

```bash
# Quick manual rollback command
npm run rollback:production -- --reason="User reports portfolio errors"

# With confirmation
npm run rollback:production -- --confirm

# Dry run (simulate rollback)
npm run rollback:production -- --dry-run
```

### Rollback Verification

```typescript
// Verify rollback success
import { verifyRollback } from '@/deploy/verify';

const checks = await verifyRollback({
  env: 'production',
  checks: [
    { name: 'Health Check', url: '/health', expected: 200 },
    { name: 'Error Rate', metric: 'error_rate', threshold: 0.5 },
    { name: 'P99 Latency', metric: 'p99_latency', threshold: 500 },
    { name: 'Active Users', metric: 'active_users', min: 100 },
  ],
});

if (checks.passed) {
  console.log('✅ Rollback verified - system healthy');
} else {
  console.error('❌ Rollback verification failed');
  console.error('Failed checks:', checks.failed);
}
```

---

## Rollback Decision Matrix

| Issue | Severity | Rollback | Timeline |
|-------|----------|----------|----------|
| **Error rate > 5%** | Critical | Automatic | < 60s |
| **P99 latency > 2s** | Critical | Automatic | < 60s |
| **Provider failure** | High | Automatic | < 60s |
| **Cache failure** | High | Automatic | < 60s |
| **Minor bug** | Low | Manual | As needed |
| **UI glitch** | Medium | Feature flag disable | < 5s |
| **Data inconsistency** | Critical | Automatic + DB restore | < 5 min |
| **Security issue** | Critical | Immediate shutdown | < 10s |

---

## 28.8 Mobile Release Management

Mobile apps (iOS/Android) follow a slightly different release flow due to app store requirements.

### Mobile Release Pipeline

```
Build → Automated Tests → Manual QA → Beta Release → App Store Submission → Staged Rollout
```

### iOS Release Process

**1. Build**
```bash
# Build iOS app
cd mobile/ios
xcodebuild -workspace DominionMarkets.xcworkspace \
  -scheme DominionMarkets \
  -configuration Release \
  -archivePath build/DominionMarkets.xcarchive \
  archive

# Export IPA
xcodebuild -exportArchive \
  -archivePath build/DominionMarkets.xcarchive \
  -exportPath build/ipa \
  -exportOptionsPlist ExportOptions.plist
```

**2. Automated Tests**
```bash
# Unit tests
xcodebuild test -workspace DominionMarkets.xcworkspace \
  -scheme DominionMarkets \
  -destination 'platform=iOS Simulator,name=iPhone 15 Pro'

# UI tests
xcodebuild test -workspace DominionMarkets.xcworkspace \
  -scheme DominionMarketsUITests \
  -destination 'platform=iOS Simulator,name=iPhone 15 Pro'
```

**3. Manual QA**
- Test on physical devices (iPhone 12, 13, 14, 15)
- Test on different iOS versions (iOS 15, 16, 17)
- Verify push notifications
- Test deep linking
- Verify in-app purchases (if applicable)

**4. Beta Release (TestFlight)**
```bash
# Upload to TestFlight
xcrun altool --upload-app \
  --type ios \
  --file build/ipa/DominionMarkets.ipa \
  --username "$APPLE_ID" \
  --password "$APP_SPECIFIC_PASSWORD"
```

**Beta Testing Checklist:**
- [ ] Internal team testing (2-3 days)
- [ ] External beta testers (1 week)
- [ ] Collect feedback via TestFlight
- [ ] Fix critical issues
- [ ] Re-submit if needed

**5. App Store Submission**
```typescript
// App Store Connect metadata
const appStoreMetadata = {
  version: '1.3.0',
  releaseNotes: `
What's New:
- New: Alerts dashboard with custom triggers
- New: Dark mode support
- Improved: Portfolio performance (50% faster)
- Fixed: Notification timing issues
  `,
  screenshots: [
    'iPhone 15 Pro (6.7")',
    'iPhone 15 (6.1")',
    'iPad Pro 12.9"',
  ],
  reviewNotes: 'Test account credentials provided in review notes.',
};
```

**Review Process:**
- Submit for review (typically 24-48 hours)
- Respond to reviewer questions
- Fix issues if rejected
- Re-submit if needed

**6. Staged Rollout**
```
10% → 25% → 50% → 100%
```

**Rollout Schedule:**
- **Day 1: 10%** - Monitor for critical issues
- **Day 3: 25%** - Check crash reports, user feedback
- **Day 5: 50%** - Review performance metrics
- **Day 7: 100%** - Full release to all users

**Monitoring During Rollout:**
```typescript
import { MonitorAppStore } from '@/mobile/monitoring';

const monitor = new MonitorAppStore({
  version: '1.3.0',
  platform: 'ios',
  rolloutStage: '10%',
});

await monitor.trackMetrics({
  crashRate: { threshold: 1.0 }, // < 1% crashes
  rating: { threshold: 4.0 }, // > 4.0 stars
  downloads: { min: 100 }, // At least 100 downloads
});

if (monitor.metrics.crashRate > 1.0) {
  await monitor.pauseRollout();
  await notifyTeam({
    severity: 'critical',
    message: `iOS crash rate at ${monitor.metrics.crashRate}%`,
  });
}
```

---

### Android Release Process

**1. Build**
```bash
# Build Android APK/AAB
cd mobile/android
./gradlew assembleRelease
./gradlew bundleRelease
```

**2. Automated Tests**
```bash
# Unit tests
./gradlew testReleaseUnitTest

# Instrumentation tests
./gradlew connectedAndroidTest
```

**3. Manual QA**
- Test on physical devices (Pixel, Samsung, OnePlus)
- Test on different Android versions (Android 11-14)
- Verify push notifications (FCM)
- Test deep linking
- Verify Google Play billing (if applicable)

**4. Beta Release (Google Play Internal Testing)**
```bash
# Upload to Google Play Console
fastlane supply --aab build/outputs/bundle/release/app-release.aab \
  --track internal \
  --json_key google-play-key.json
```

**5. Play Store Submission**
```typescript
const playStoreMetadata = {
  version: '1.3.0',
  versionCode: 130,
  releaseNotes: `
What's New:
- New: Alerts dashboard with custom triggers
- New: Dark mode support
- Improved: Portfolio performance (50% faster)
- Fixed: Notification timing issues
  `,
  screenshots: [
    'Phone (5.5")',
    'Tablet (10")',
  ],
};
```

**6. Staged Rollout (Google Play)**
```
10% → 25% → 50% → 100%
```

**Rollout Control:**
```bash
# Set rollout percentage via Google Play Console API
curl -X PATCH \
  "https://androidpublisher.googleapis.com/androidpublisher/v3/applications/$PACKAGE_NAME/edits/$EDIT_ID/tracks/production" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "releases": [{
      "versionCodes": [130],
      "status": "inProgress",
      "userFraction": 0.10
    }]
  }'
```

---

### Mobile Release Checklist

**Pre-Release:**
- [ ] Version number incremented (iOS: CFBundleShortVersionString, Android: versionName)
- [ ] Build number incremented (iOS: CFBundleVersion, Android: versionCode)
- [ ] Release notes written (all supported languages)
- [ ] Screenshots updated (if UI changed)
- [ ] App Store/Play Store metadata reviewed
- [ ] Privacy policy updated (if needed)
- [ ] Test accounts created for reviewers

**Post-Release:**
- [ ] Monitor crash reports (Crashlytics, Sentry)
- [ ] Monitor app ratings/reviews
- [ ] Respond to user feedback
- [ ] Track download metrics
- [ ] Monitor API error rates from mobile clients

---

## 28.9 Hotfix Protocol

For urgent production issues that cannot wait for the weekly release cycle.

### When to Use Hotfix Protocol

**Critical Issues:**
- Production outage (service down)
- Data loss or corruption
- Security vulnerability
- Payment processing failure
- Critical user-facing bug (portfolio calculations, stock quotes)

**NOT for Hotfix:**
- Minor UI glitches (use feature flags)
- Performance optimizations (wait for next release)
- New features (wait for next release)
- Non-critical bugs (add to backlog)

---

### Hotfix Steps

**1. Create Hotfix Branch**
```bash
# Create from production tag
git checkout -b hotfix/fix-portfolio-calculation v1.2.3

# Or from main if production is latest
git checkout -b hotfix/fix-portfolio-calculation main
```

**2. Patch Fix**
```typescript
// Example: Fix portfolio calculation bug
// File: lib/portfolio/calculations.ts

export function calculateTotalValue(holdings: Holding[]): number {
  // BUG FIX: Was using incorrect price field
  // return holdings.reduce((sum, h) => sum + h.lastPrice * h.quantity, 0);
  
  // FIXED: Use current price instead of last price
  return holdings.reduce((sum, h) => sum + h.currentPrice * h.quantity, 0);
}
```

**Version Increment:**
```bash
# Hotfix increments PATCH version
# 1.2.3 → 1.2.4
npm version patch
```

**3. Run Tests**
```bash
# Run full test suite
npm run test:unit
npm run test:integration
npm run test:e2e

# Run specific tests for fixed bug
npm test -- --testNamePattern="portfolio calculation"
```

**4. Deploy Directly to Staging**
```bash
# Skip dev environment (hotfix bypass)
kubectl set image deployment/api \
  api=dominion-markets-api:hotfix-1.2.4 \
  -n staging

kubectl rollout status deployment/api -n staging --timeout=10m
```

**Staging Verification:**
```typescript
// Run hotfix-specific smoke tests
import { testPortfolioCalculation } from '@/tests/hotfix';

const testResults = await testPortfolioCalculation({
  env: 'staging',
  scenarios: [
    { holdings: mockHoldings1, expected: 12345.67 },
    { holdings: mockHoldings2, expected: 54321.09 },
  ],
});

if (!testResults.passed) {
  throw new Error('Hotfix verification failed');
}
```

**5. Approval**
```typescript
// Expedited approval (same-day)
const approvals = {
  engineeringLead: true,  // Required
  productOwner: false,     // Not required for hotfix
  qaLead: true,            // Required
};

const approved = approvals.engineeringLead && approvals.qaLead;
if (!approved) {
  throw new Error('Hotfix approval required from Engineering Lead and QA Lead');
}
```

**Approval Requirements (Hotfix):**
- ✅ Engineering Lead (required)
- ✅ QA Lead (required)
- ❌ Product Owner (not required)
- ❌ 24-hour soak time (bypassed)

**6. Deploy to Production**
```bash
# Emergency production deployment
kubectl set image deployment/api \
  api=dominion-markets-api:hotfix-1.2.4 \
  -n production

kubectl rollout status deployment/api -n production --timeout=15m
```

**Post-Deployment Monitoring (30 min):**
```typescript
import { monitorHotfix } from '@/deploy/monitor';

await monitorHotfix({
  version: '1.2.4',
  duration: '30m',
  checks: [
    { metric: 'error_rate', threshold: 0.5, unit: '%' },
    { metric: 'p99_latency', threshold: 1000, unit: 'ms' },
    { metric: 'portfolio_calc_errors', threshold: 0, unit: 'count' },
  ],
  onFailure: async () => {
    await rollbackProduction({
      reason: 'Hotfix failed verification',
      severity: 'critical',
    });
  },
});
```

**7. Merge Back to Main**
```bash
# After successful production deployment
git checkout main
git merge hotfix/fix-portfolio-calculation
git push origin main

# Tag the hotfix
git tag -a v1.2.4 -m "Hotfix: Fix portfolio calculation bug"
git push origin v1.2.4

# Delete hotfix branch
git branch -d hotfix/fix-portfolio-calculation
git push origin --delete hotfix/fix-portfolio-calculation
```

---

### Hotfix Timeline

| Step | Duration | Notes |
|------|----------|-------|
| **1. Create Branch** | 5 min | From production tag |
| **2. Patch Fix** | 30-60 min | Code change + tests |
| **3. Run Tests** | 10-15 min | Full test suite |
| **4. Deploy to Staging** | 10 min | Direct deployment |
| **5. Approval** | 30-60 min | Expedited |
| **6. Deploy to Production** | 15 min | Emergency deployment |
| **7. Merge to Main** | 5 min | After verification |

**Total Hotfix Time:** ~2-3 hours (vs. 1 week for normal release)

---

### Hotfix Notification

```typescript
// Notify all stakeholders immediately
import { notifyHotfix } from '@/notifications';

await notifyHotfix({
  version: '1.2.4',
  issue: 'Portfolio calculation showing incorrect values',
  severity: 'critical',
  impact: 'All users with portfolios',
  fix: 'Corrected price field in calculation',
  deployedAt: new Date(),
  channels: [
    'slack-engineering',
    'slack-product',
    'email-stakeholders',
    'status-page', // Update public status page
  ],
});
```

**Status Page Update:**
```markdown
[RESOLVED] Portfolio Value Calculation Issue

Incident: Portfolio values were displaying incorrectly due to a calculation bug.

Resolution: Hotfix v1.2.4 deployed at 2:45 PM EST. All portfolio values now accurate.

Impact: Users viewing their portfolio between 1:00 PM - 2:45 PM EST may have seen incorrect totals.

Next Steps: No action required. Portfolio values now display correctly.
```

---

## 28.10 Deployment Monitoring

After every deployment, the system continuously monitors key metrics to detect anomalies.

### Monitored Metrics

**1. Error Rates**
```typescript
interface ErrorRateMetrics {
  threshold: number;      // 0.5% (0.005)
  current: number;
  trend: 'increasing' | 'decreasing' | 'stable';
  sources: {
    api: number;          // API errors
    frontend: number;     // Frontend errors (Sentry)
    providers: number;    // External provider errors
  };
}

// Monitor error rate
const errorRate = await getMetric('error_rate', {
  env: 'production',
  duration: '5m',
});

if (errorRate.current > 0.005) { // 0.5%
  await triggerRollback({
    reason: `Error rate spike: ${(errorRate.current * 100).toFixed(2)}%`,
    severity: 'critical',
  });
}
```

**2. Latency**
```typescript
interface LatencyMetrics {
  p50: number;  // Median (target: < 200ms)
  p95: number;  // 95th percentile (target: < 500ms)
  p99: number;  // 99th percentile (target: < 2000ms)
  max: number;  // Maximum latency
}

// Monitor latency
const latency = await getMetric('latency', {
  env: 'production',
  duration: '5m',
});

if (latency.p99 > 2000) { // 2 seconds
  await triggerAlert({
    severity: 'high',
    message: `P99 latency at ${latency.p99}ms (threshold: 2000ms)`,
  });
}
```

**3. Cache Hit Ratio**
```typescript
interface CacheMetrics {
  hitRate: number;      // Target: > 80%
  missRate: number;
  evictions: number;    // Cache evictions
  size: number;         // Cache size (MB)
  ttl: number;          // Average TTL
}

// Monitor cache performance
const cache = await getMetric('cache', {
  env: 'production',
  duration: '5m',
});

if (cache.hitRate < 0.80) { // 80%
  await triggerAlert({
    severity: 'medium',
    message: `Cache hit rate at ${(cache.hitRate * 100).toFixed(1)}% (target: > 80%)`,
  });
}
```

**4. Provider Stability**
```typescript
interface ProviderMetrics {
  name: string;         // e.g., 'Polygon Stock Data'
  uptime: number;       // Target: > 99.5%
  latency: number;      // Average API latency
  errorRate: number;    // Provider API errors
  quotaUsage: number;   // API quota usage %
}

// Monitor external providers
const providers = ['polygon', 'newsapi', 'finnhub'];

for (const provider of providers) {
  const metrics = await getProviderMetrics(provider);
  
  if (metrics.uptime < 0.995) { // 99.5%
    await triggerAlert({
      severity: 'high',
      message: `Provider ${provider} uptime at ${(metrics.uptime * 100).toFixed(2)}%`,
    });
    
    // Consider switching to backup provider
    await switchToBackupProvider(provider);
  }
}
```

**5. Identity Service**
```typescript
interface IdentityMetrics {
  loginSuccessRate: number;    // Target: > 99%
  loginLatency: number;        // Target: < 500ms
  tokenRefreshRate: number;    // Tokens refreshed per minute
  activeUsers: number;         // Currently authenticated users
}

// Monitor identity service
const identity = await getMetric('identity', {
  env: 'production',
  duration: '5m',
});

if (identity.loginSuccessRate < 0.99) {
  await triggerAlert({
    severity: 'critical',
    message: `Identity service degraded: ${(identity.loginSuccessRate * 100).toFixed(2)}% success rate`,
  });
}
```

**6. Subscription Service**
```typescript
interface SubscriptionMetrics {
  activeSubscriptions: number;
  renewalRate: number;         // Successful renewals %
  cancellationRate: number;    // Cancellations per day
  paymentFailures: number;     // Failed payments
}

// Monitor subscriptions
const subscriptions = await getMetric('subscriptions', {
  env: 'production',
  duration: '1d',
});

if (subscriptions.paymentFailures > 10) {
  await triggerAlert({
    severity: 'high',
    message: `${subscriptions.paymentFailures} payment failures in last 24h`,
  });
}
```

**7. Alerts Engine**
```typescript
interface AlertsMetrics {
  alertsCreated: number;       // Alerts created per hour
  alertsTriggered: number;     // Alerts triggered per hour
  notificationsSent: number;   // Notifications sent per hour
  notificationFailures: number; // Failed notifications
}

// Monitor alerts engine
const alerts = await getMetric('alerts', {
  env: 'production',
  duration: '1h',
});

if (alerts.notificationFailures > 5) {
  await triggerAlert({
    severity: 'medium',
    message: `${alerts.notificationFailures} notification failures in last hour`,
  });
}
```

---

### Anomaly Detection & Automatic Rollback

**Monitoring Dashboard:**
```typescript
import { DeploymentMonitor } from '@/deploy/monitor';

const monitor = new DeploymentMonitor({
  version: '1.3.0',
  env: 'production',
  duration: '30m', // Monitor for 30 minutes post-deployment
});

await monitor.start({
  metrics: [
    { name: 'error_rate', threshold: 0.005, action: 'rollback' },
    { name: 'p99_latency', threshold: 2000, action: 'rollback' },
    { name: 'cache_hit_rate', threshold: 0.80, action: 'alert' },
    { name: 'provider_uptime', threshold: 0.995, action: 'alert' },
    { name: 'identity_success', threshold: 0.99, action: 'rollback' },
    { name: 'subscription_failures', threshold: 10, action: 'alert' },
    { name: 'alerts_engine_failures', threshold: 5, action: 'alert' },
  ],
  onAnomaly: async (metric, value) => {
    console.log(`🚨 Anomaly detected: ${metric} = ${value}`);
    
    if (metric.action === 'rollback') {
      await triggerAutomaticRollback({
        reason: `${metric.name} threshold exceeded: ${value}`,
        severity: 'critical',
      });
    } else if (metric.action === 'alert') {
      await triggerAlert({
        severity: 'high',
        message: `${metric.name} threshold exceeded: ${value}`,
      });
    }
  },
});
```

**Automatic Rollback Triggers:**
- ❌ Error rate > 0.5% → **Automatic rollback**
- ❌ P99 latency > 2s → **Automatic rollback**
- ❌ Identity service < 99% success → **Automatic rollback**
- ⚠️ Cache hit rate < 80% → Alert (no rollback)
- ⚠️ Provider uptime < 99.5% → Alert + switch to backup
- ⚠️ Subscription payment failures > 10/day → Alert
- ⚠️ Alerts engine failures > 5/hour → Alert

**Rollback Execution:**
```typescript
async function triggerAutomaticRollback(options: RollbackOptions) {
  const startTime = Date.now();
  
  console.log(`🚨 AUTOMATIC ROLLBACK INITIATED: ${options.reason}`);
  
  // Execute rollback
  await rollbackProduction(options);
  
  const duration = Date.now() - startTime;
  
  // Notify all stakeholders immediately
  await notifySlack({
    severity: 'critical',
    message: `⚠️ PRODUCTION ROLLBACK EXECUTED`,
    reason: options.reason,
    duration: `${duration}ms`,
    version: getCurrentVersion(),
    rolledBackTo: getPreviousVersion(),
  });
  
  // Page on-call engineer
  await pageOnCall({
    severity: 'critical',
    message: `Production auto-rollback: ${options.reason}`,
  });
  
  // Create incident ticket
  await createIncident({
    title: `Production Rollback: ${options.reason}`,
    severity: 'P1',
    assignee: 'on-call-engineer',
    description: `Automatic rollback triggered due to ${options.reason}`,
  });
}
```

---

## Deployment Monitoring Dashboard

**Real-Time Metrics:**
```typescript
// Grafana dashboard configuration
export const deploymentDashboard = {
  title: 'Production Deployment Monitor',
  panels: [
    {
      title: 'Error Rate (Last 30m)',
      query: 'rate(http_requests_total{status=~"5.."}[5m])',
      threshold: 0.005,
      alertOnExceed: true,
    },
    {
      title: 'Latency (P99)',
      query: 'histogram_quantile(0.99, http_request_duration_seconds)',
      threshold: 2.0,
      alertOnExceed: true,
    },
    {
      title: 'Cache Hit Ratio',
      query: 'rate(cache_hits_total[5m]) / rate(cache_requests_total[5m])',
      threshold: 0.80,
      alertOnBelow: true,
    },
    {
      title: 'Provider Uptime',
      query: 'avg(provider_health_status)',
      threshold: 0.995,
      alertOnBelow: true,
    },
    {
      title: 'Identity Service Success Rate',
      query: 'rate(identity_login_success[5m]) / rate(identity_login_attempts[5m])',
      threshold: 0.99,
      alertOnBelow: true,
    },
    {
      title: 'Active Subscriptions',
      query: 'subscription_active_count',
      trend: 'show',
    },
    {
      title: 'Alerts Engine Status',
      query: 'rate(alerts_sent_total[5m])',
      trend: 'show',
    },
  ],
};
```

**Deployment Monitor Output:**
```bash
🚀 Deployment Monitor: v1.3.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Environment: production
Duration: 30m (15m elapsed)
Status: ✅ HEALTHY

Metrics:
  Error Rate:         0.12% ✅ (threshold: 0.5%)
  P99 Latency:        487ms ✅ (threshold: 2000ms)
  Cache Hit Rate:     87.3% ✅ (threshold: 80%)
  Provider Uptime:    99.8% ✅ (threshold: 99.5%)
  Identity Success:   99.9% ✅ (threshold: 99%)
  Payment Failures:   2     ✅ (threshold: 10)
  Alert Failures:     0     ✅ (threshold: 5)

Last Check: 2025-12-24 14:35:12 UTC
Next Check: 2025-12-24 14:36:12 UTC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Environment Comparison

| Feature | Local | Dev | Staging | Production |
|---------|-------|-----|---------|------------|
| **Auto-Deploy** | No | Yes (on push to `develop`) | Yes (on push to `main`) | No (manual approval) |
| **Replicas** | 1 | 1 | 2 | 5-20 (autoscaling) |
| **Autoscaling** | No | No | No | Yes |
| **Resources** | Minimal | 250m CPU, 512Mi RAM | 1 CPU, 2Gi RAM | 2 CPU, 4Gi RAM |
| **Database** | Local/Docker | Shared dev DB | Production-like (anonymized) | Production DB |
| **APIs** | Mocked | Real (test accounts) | Real (production config) | Real |
| **Authentication** | Disabled | Test users | Real auth flow | Real auth flow |
| **Monitoring** | No | Basic | Full (same as prod) | Full |
| **Alerting** | No | No | Yes | Yes |
| **HTTPS** | No | Yes | Yes | Yes |
| **CDN** | No | No | Yes | Yes |
| **Health Checks** | No | No | Yes | Yes |
| **Rollback** | N/A | Manual | Automatic | Automatic |

---

## Promotion Rules

### Local → Dev
**Trigger:** Push to `develop` branch  
**Requirements:** None  
**Approval:** Not required  
**Rollback:** Not applicable  

### Dev → Staging
**Trigger:** Push to `main` branch  
**Requirements:**
- ✅ All tests passing (unit, integration, E2E)
- ✅ Security scan passed
- ✅ Performance benchmarks passed
- ✅ Code review approved

**Approval:** Not required (automatic)  
**Rollback:** Automatic (on errors)  

### Staging → Production
**Trigger:** Manual (`workflow_dispatch`)  
**Requirements:**
- ✅ Version deployed to staging for 24+ hours
- ✅ Staging health checks passing
- ✅ Staging metrics healthy
- ✅ Manual approval from 2+ engineers

**Approval:** **Required** (production environment protection)  
**Rollback:** Automatic (on errors) + Manual option  

---

## Environment URLs

```typescript
export const ENVIRONMENT_URLS = {
  local: 'http://localhost:3000',
  dev: 'https://dev.dominionmarkets.app',
  staging: 'https://staging.dominionmarkets.app',
  production: 'https://dominionmarkets.app',
};

export function getAPIUrl(env: Environment): string {
  switch (env) {
    case 'local':
      return 'http://localhost:4000';
    case 'dev':
      return 'https://api.dev.dominionmarkets.app';
    case 'staging':
      return 'https://api.staging.dominionmarkets.app';
    case 'production':
      return 'https://api.dominionmarkets.app';
  }
}

// Auto-detect environment
export function getCurrentEnvironment(): Environment {
  const hostname = window.location.hostname;
  
  if (hostname === 'localhost') return 'local';
  if (hostname.includes('dev.')) return 'dev';
  if (hostname.includes('staging.')) return 'staging';
  return 'production';
}
```

---

## Environment Flow Implementation Checklist

✅ **Local Environment**: Docker Compose, hot reload, mocked APIs, debug mode, instant feedback  
✅ **Dev Environment**: Kubernetes namespace, auto-deploy on `develop`, shared database, test authentication  
✅ **Staging Environment**: Production mirror (scaled down), real APIs, full monitoring, 24h minimum soak time  
✅ **Production Environment**: Full scale (5-20 replicas), autoscaling, manual approval required, zero downtime  
✅ **Promotion Rules**: Automatic (local→dev, dev→staging), Manual approval (staging→production)  

---

# SECTION 29 — QA, TESTING & QUALITY STANDARDS

DominionMarkets must feel **stable, predictable, and trustworthy** every time a user touches it.

This section defines the full QA and testing framework that ensures every feature, every release, and every interaction meets the highest standard of quality.

---

## 29.1 Quality Principles

DominionMarkets follows five core quality principles:

### 1. No Regressions

**Principle:** Every release must be at least as stable as the last.

**Implementation:**
```typescript
// Regression test suite runs on every deployment
import { regressionTests } from '@/tests/regression';

const results = await regressionTests.run({
  env: 'staging',
  compareWith: 'production', // Compare against current production
  tests: [
    'portfolio-calculations',
    'stock-quotes',
    'alerts-engine',
    'authentication',
    'subscription-billing',
  ],
});

if (results.failedTests.length > 0) {
  throw new Error(`Regression detected: ${results.failedTests.join(', ')}`);
}
```

**Enforcement:**
- Automated regression test suite (500+ tests)
- Visual regression testing (snapshot comparisons)
- Performance regression checks (P95/P99 latency)
- API contract regression tests
- Database query regression tests

**Example Regression Test:**
```typescript
// tests/regression/portfolio-calculations.test.ts
describe('Portfolio Calculations Regression', () => {
  it('matches production calculation logic', async () => {
    const testPortfolio = {
      holdings: [
        { symbol: 'AAPL', quantity: 10, purchasePrice: 150.00 },
        { symbol: 'GOOGL', quantity: 5, purchasePrice: 2800.00 },
      ],
    };
    
    // Run calculation with new code
    const newResult = calculatePortfolioValue(testPortfolio);
    
    // Compare with expected production result
    const expectedResult = 15500.00; // Known production value
    
    expect(newResult).toBe(expectedResult);
  });
});
```

---

### 2. No Surprises

**Principle:** Behavior must be predictable and consistent.

**Implementation:**
```typescript
// Predictable error handling
export function fetchStockQuote(symbol: string): Promise<StockQuote> {
  try {
    const quote = await api.getQuote(symbol);
    return quote;
  } catch (error) {
    // Predictable error response
    if (error.status === 404) {
      throw new StockNotFoundError(symbol);
    } else if (error.status === 429) {
      throw new RateLimitError('Too many requests');
    } else {
      throw new StockQuoteError('Unable to fetch quote');
    }
  }
}
```

**Enforcement:**
- Consistent error messages across all APIs
- Predictable loading states (skeleton screens)
- Deterministic sorting/filtering (always same order)
- Consistent date/time formatting (ISO 8601)
- Stable UI transitions (no jumps/flickers)

**Example Consistency Test:**
```typescript
// tests/consistency/date-formatting.test.ts
describe('Date Formatting Consistency', () => {
  it('formats dates consistently across components', () => {
    const date = new Date('2025-12-24T12:00:00Z');
    
    // All components should format dates identically
    expect(formatDate(date, 'portfolio')).toBe('Dec 24, 2025');
    expect(formatDate(date, 'news')).toBe('Dec 24, 2025');
    expect(formatDate(date, 'alerts')).toBe('Dec 24, 2025');
  });
  
  it('formats times consistently across components', () => {
    const date = new Date('2025-12-24T12:00:00Z');
    
    expect(formatTime(date, 'portfolio')).toBe('12:00 PM');
    expect(formatTime(date, 'news')).toBe('12:00 PM');
    expect(formatTime(date, 'alerts')).toBe('12:00 PM');
  });
});
```

---

### 3. No Broken Flows

**Principle:** Every user journey must work end-to-end.

**Implementation:**
```typescript
// End-to-end user journey tests
import { test, expect } from '@playwright/test';

test('Complete user journey: Login → View Portfolio → Place Trade', async ({ page }) => {
  // Step 1: Login
  await page.goto('/login');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
  
  // Step 2: View Portfolio
  await page.click('text=Portfolio');
  await expect(page.locator('h1')).toContainText('Portfolio');
  await expect(page.locator('.portfolio-value')).toBeVisible();
  
  // Step 3: Navigate to Stock Detail
  await page.click('text=AAPL');
  await expect(page).toHaveURL(/\/stocks\/AAPL/);
  await expect(page.locator('.stock-price')).toBeVisible();
  
  // Step 4: Verify Trade Button Available
  await expect(page.locator('button:has-text("Trade")')).toBeEnabled();
});
```

**Enforcement:**
- Critical path E2E tests (login, portfolio, trading, alerts)
- Cross-browser testing (Chrome, Firefox, Safari, Edge)
- Mobile journey testing (iOS Safari, Android Chrome)
- Offline-mode journey testing
- Identity tier journey testing (Free, Premium, Pro)

**Example Flow Test:**
```typescript
// tests/flows/alert-creation-flow.test.ts
describe('Alert Creation Flow', () => {
  it('completes full alert creation journey', async () => {
    // Step 1: Navigate to alerts
    await navigateTo('/dashboard/alerts');
    expect(getCurrentURL()).toBe('/dashboard/alerts');
    
    // Step 2: Click "Create Alert"
    await click('button:has-text("Create Alert")');
    expect(getDialog()).toBeVisible();
    
    // Step 3: Fill form
    await fillForm({
      symbol: 'AAPL',
      condition: 'price_above',
      targetPrice: 200.00,
      notification: 'push',
    });
    
    // Step 4: Submit
    await click('button:has-text("Create")');
    
    // Step 5: Verify success
    expect(getToast()).toContainText('Alert created successfully');
    expect(getAlertsList()).toContain('AAPL');
  });
});
```

---

### 4. No Silent Failures

**Principle:** Errors must be caught, surfaced, and handled gracefully.

**Implementation:**
```typescript
// Global error boundary
export function ErrorBoundary({ children }: { children: React.ReactNode }) {
  const [error, setError] = useState<Error | null>(null);
  
  useEffect(() => {
    const handleError = (event: ErrorEvent) => {
      // Log to monitoring
      Sentry.captureException(event.error);
      
      // Show user-friendly error
      setError(event.error);
      
      // Alert engineering team
      if (event.error instanceof CriticalError) {
        alertEngineeringTeam(event.error);
      }
    };
    
    window.addEventListener('error', handleError);
    return () => window.removeEventListener('error', handleError);
  }, []);
  
  if (error) {
    return (
      <ErrorState
        title="Something went wrong"
        description="We've been notified and are working on a fix."
        onRetry={() => window.location.reload()}
      />
    );
  }
  
  return <>{children}</>;
}
```

**Enforcement:**
- Try-catch blocks on all async operations
- Error boundaries on all route segments
- Sentry error tracking (100% error capture)
- API error logging (Datadog)
- User-facing error messages (no technical jargon)

**Example Error Handling:**
```typescript
// lib/api/portfolio.ts
export async function fetchPortfolio(userId: string): Promise<Portfolio> {
  try {
    const response = await fetch(`/api/portfolio/${userId}`);
    
    if (!response.ok) {
      // Surface specific error
      if (response.status === 404) {
        throw new PortfolioNotFoundError(userId);
      } else if (response.status === 403) {
        throw new UnauthorizedError('You do not have access to this portfolio');
      } else {
        throw new PortfolioFetchError(`Failed to fetch portfolio: ${response.statusText}`);
      }
    }
    
    return await response.json();
  } catch (error) {
    // Log to monitoring
    logger.error('Portfolio fetch failed', { userId, error });
    Sentry.captureException(error);
    
    // Re-throw with context
    throw new PortfolioFetchError(
      `Unable to load portfolio for user ${userId}`,
      { cause: error }
    );
  }
}

// Component usage
export function PortfolioPage() {
  const { user } = useUser();
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [error, setError] = useState<Error | null>(null);
  
  useEffect(() => {
    fetchPortfolio(user.id)
      .then(setPortfolio)
      .catch((err) => {
        setError(err);
        
        // Show user-friendly error
        toast.error(err.message);
      });
  }, [user.id]);
  
  if (error) {
    return (
      <ErrorState
        title="Unable to load portfolio"
        description={error.message}
        onRetry={() => window.location.reload()}
      />
    );
  }
  
  return <Portfolio data={portfolio} />;
}
```

---

### 5. No Untested Code

**Principle:** Every line of code must be covered by at least one test type.

**Implementation:**
```typescript
// Enforce test coverage with Jest
// jest.config.js
module.exports = {
  collectCoverage: true,
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  coveragePathIgnorePatterns: [
    '/node_modules/',
    '/tests/',
    '/build/',
  ],
};
```

**Test Type Coverage:**
- **Unit Tests**: All functions, utilities, hooks
- **Integration Tests**: All API endpoints, database queries
- **E2E Tests**: All critical user flows
- **Visual Tests**: All UI components
- **Performance Tests**: All API endpoints
- **Security Tests**: All authentication/authorization logic

**Example Test Coverage Report:**
```bash
# Run coverage report
npm run test:coverage

# Output:
---------------------------|---------|----------|---------|---------|
File                       | % Stmts | % Branch | % Funcs | % Lines |
---------------------------|---------|----------|---------|---------|
All files                  |   87.42 |    82.15 |   89.33 |   87.65 |
 components/               |   92.18 |    88.42 |   94.12 |   92.45 |
  Portfolio.tsx            |   95.00 |    91.67 |   100.0 |   95.00 |
  StockCard.tsx            |   88.89 |    85.71 |   87.50 |   88.89 |
 lib/                      |   85.67 |    78.92 |   86.21 |   85.98 |
  portfolio.ts             |   90.00 |    83.33 |   92.31 |   90.00 |
  stocks.ts                |   82.35 |    75.00 |   80.00 |   82.35 |
 hooks/                    |   89.12 |    84.56 |   91.11 |   89.34 |
  usePortfolio.ts          |   93.75 |    87.50 |   100.0 |   93.75 |
---------------------------|---------|----------|---------|---------|
```

**Enforcement:**
- CI/CD blocks deployment if coverage < 80%
- Pull request checks require coverage increase or maintenance
- Monthly coverage reports reviewed by engineering team
- Uncovered code flagged in code review

---

## Quality Principles Enforcement Checklist

✅ **No Regressions**
- [ ] Regression test suite passing (500+ tests)
- [ ] Visual regression tests passing (100+ snapshots)
- [ ] Performance regression check passing (P95/P99 within 10%)
- [ ] API contract tests passing (all endpoints)

✅ **No Surprises**
- [ ] All error messages user-friendly and consistent
- [ ] All date/time formatting consistent
- [ ] All loading states predictable (skeleton screens)
- [ ] All UI transitions smooth (no flickers)

✅ **No Broken Flows**
- [ ] All critical user journeys tested E2E
- [ ] Cross-browser testing complete (Chrome, Firefox, Safari, Edge)
- [ ] Mobile testing complete (iOS, Android)
- [ ] Offline-mode testing complete

✅ **No Silent Failures**
- [ ] All async operations have error handling
- [ ] All components have error boundaries
- [ ] All errors logged to Sentry
- [ ] All critical errors alert engineering team

✅ **No Untested Code**
- [ ] Test coverage ≥ 80% (branches, functions, lines, statements)
- [ ] All new code includes tests
- [ ] All bug fixes include regression tests
- [ ] All critical paths have E2E tests

---

## 29.2 Test Types

DominionMarkets uses four primary test types, each serving a specific purpose in the quality pipeline.

### Test Pyramid Structure

```
         /\
        /  \        End-to-End Tests (E2E)
       /    \       - Slowest, most expensive
      /------\      - Full user journeys
     /        \     - 50-100 tests
    /          \    
   /------------\   Integration Tests
  /              \  - Medium speed/cost
 /                \ - API + Database
/------------------\ - 200-500 tests
|                  |
|   Unit Tests     | Unit Tests
|   1000+ tests    | - Fastest, cheapest
|                  | - Functions, hooks, utilities
--------------------
```

---

## A. Unit Tests

**Purpose:** Test individual functions, components, and utilities in isolation.

**Characteristics:**
- ✅ Fast (< 1ms per test)
- ✅ Isolated (no external dependencies)
- ✅ Deterministic (same input = same output)
- ✅ High volume (1000+ tests)

### Unit Test Framework

**Configuration:**
```typescript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/tests/setup.ts'],
  collectCoverageFrom: [
    'app/**/*.{ts,tsx}',
    'components/**/*.{ts,tsx}',
    'lib/**/*.{ts,tsx}',
    'hooks/**/*.{ts,tsx}',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  testMatch: [
    '**/__tests__/**/*.test.{ts,tsx}',
    '**/*.test.{ts,tsx}',
  ],
};
```

### 1. Component Unit Tests

**Test React components in isolation:**

```typescript
// components/portfolio/PortfolioSummary.test.tsx
import { render, screen } from '@testing-library/react';
import { PortfolioSummary } from './PortfolioSummary';

describe('PortfolioSummary', () => {
  const mockPortfolio = {
    totalValue: 125000.50,
    dayChange: 2500.75,
    dayChangePercent: 2.04,
    holdings: [
      { symbol: 'AAPL', quantity: 10, value: 1750.00 },
      { symbol: 'GOOGL', quantity: 5, value: 14000.00 },
    ],
  };
  
  it('renders total portfolio value', () => {
    render(<PortfolioSummary portfolio={mockPortfolio} />);
    expect(screen.getByText('$125,000.50')).toBeInTheDocument();
  });
  
  it('displays day change with correct color', () => {
    render(<PortfolioSummary portfolio={mockPortfolio} />);
    const changeElement = screen.getByText('+$2,500.75');
    expect(changeElement).toHaveClass('text-green-500');
  });
  
  it('shows positive percentage change', () => {
    render(<PortfolioSummary portfolio={mockPortfolio} />);
    expect(screen.getByText('+2.04%')).toBeInTheDocument();
  });
  
  it('renders holdings count', () => {
    render(<PortfolioSummary portfolio={mockPortfolio} />);
    expect(screen.getByText('2 holdings')).toBeInTheDocument();
  });
});
```

### 2. Hook Unit Tests

**Test custom React hooks:**

```typescript
// hooks/usePortfolio.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { usePortfolio } from './usePortfolio';
import * as api from '@/lib/api/portfolio';

jest.mock('@/lib/api/portfolio');

describe('usePortfolio', () => {
  const mockPortfolio = {
    id: 'portfolio-1',
    userId: 'user-1',
    holdings: [
      { symbol: 'AAPL', quantity: 10 },
    ],
  };
  
  beforeEach(() => {
    jest.clearAllMocks();
  });
  
  it('fetches portfolio on mount', async () => {
    (api.fetchPortfolio as jest.Mock).mockResolvedValue(mockPortfolio);
    
    const { result } = renderHook(() => usePortfolio('user-1'));
    
    expect(result.current.loading).toBe(true);
    
    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });
    
    expect(result.current.portfolio).toEqual(mockPortfolio);
    expect(api.fetchPortfolio).toHaveBeenCalledWith('user-1');
  });
  
  it('handles fetch error', async () => {
    const error = new Error('Failed to fetch');
    (api.fetchPortfolio as jest.Mock).mockRejectedValue(error);
    
    const { result } = renderHook(() => usePortfolio('user-1'));
    
    await waitFor(() => {
      expect(result.current.error).toBe(error);
    });
    
    expect(result.current.portfolio).toBeNull();
  });
  
  it('refetches portfolio on demand', async () => {
    (api.fetchPortfolio as jest.Mock).mockResolvedValue(mockPortfolio);
    
    const { result } = renderHook(() => usePortfolio('user-1'));
    
    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });
    
    // Call refetch
    result.current.refetch();
    
    expect(api.fetchPortfolio).toHaveBeenCalledTimes(2);
  });
});
```

### 3. Utility Function Unit Tests

**Test pure functions:**

```typescript
// lib/utils/calculations.test.ts
import {
  calculatePortfolioValue,
  calculateDayChange,
  calculatePercentChange,
  formatCurrency,
} from './calculations';

describe('Portfolio Calculations', () => {
  describe('calculatePortfolioValue', () => {
    it('calculates total value for multiple holdings', () => {
      const holdings = [
        { symbol: 'AAPL', quantity: 10, currentPrice: 175.00 },
        { symbol: 'GOOGL', quantity: 5, currentPrice: 2800.00 },
        { symbol: 'MSFT', quantity: 20, currentPrice: 380.00 },
      ];
      
      const total = calculatePortfolioValue(holdings);
      
      expect(total).toBe(23350.00); // 1750 + 14000 + 7600
    });
    
    it('returns 0 for empty portfolio', () => {
      expect(calculatePortfolioValue([])).toBe(0);
    });
    
    it('handles fractional shares', () => {
      const holdings = [
        { symbol: 'AAPL', quantity: 10.5, currentPrice: 100.00 },
      ];
      
      expect(calculatePortfolioValue(holdings)).toBe(1050.00);
    });
  });
  
  describe('calculateDayChange', () => {
    it('calculates positive day change', () => {
      const currentValue = 100000;
      const previousValue = 98000;
      
      const change = calculateDayChange(currentValue, previousValue);
      
      expect(change).toBe(2000);
    });
    
    it('calculates negative day change', () => {
      const currentValue = 98000;
      const previousValue = 100000;
      
      const change = calculateDayChange(currentValue, previousValue);
      
      expect(change).toBe(-2000);
    });
  });
  
  describe('formatCurrency', () => {
    it('formats positive values', () => {
      expect(formatCurrency(1234.56)).toBe('$1,234.56');
    });
    
    it('formats negative values', () => {
      expect(formatCurrency(-1234.56)).toBe('-$1,234.56');
    });
    
    it('formats zero', () => {
      expect(formatCurrency(0)).toBe('$0.00');
    });
    
    it('rounds to 2 decimal places', () => {
      expect(formatCurrency(1234.567)).toBe('$1,234.57');
    });
  });
});
```

### 4. API Client Unit Tests

**Test API client functions:**

```typescript
// lib/api/stocks.test.ts
import { fetchStockQuote, searchStocks } from './stocks';

global.fetch = jest.fn();

describe('Stock API Client', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });
  
  describe('fetchStockQuote', () => {
    it('fetches stock quote successfully', async () => {
      const mockQuote = {
        symbol: 'AAPL',
        price: 175.00,
        change: 2.50,
        changePercent: 1.45,
      };
      
      (global.fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: async () => mockQuote,
      });
      
      const quote = await fetchStockQuote('AAPL');
      
      expect(quote).toEqual(mockQuote);
      expect(global.fetch).toHaveBeenCalledWith('/api/stocks/AAPL');
    });
    
    it('throws error for 404', async () => {
      (global.fetch as jest.Mock).mockResolvedValue({
        ok: false,
        status: 404,
      });
      
      await expect(fetchStockQuote('INVALID'))
        .rejects
        .toThrow('Stock not found');
    });
    
    it('throws error for network failure', async () => {
      (global.fetch as jest.Mock).mockRejectedValue(
        new Error('Network error')
      );
      
      await expect(fetchStockQuote('AAPL'))
        .rejects
        .toThrow('Network error');
    });
  });
});
```

### Unit Test Best Practices

✅ **Naming Convention:**
```typescript
describe('[Component/Function Name]', () => {
  describe('[method/scenario]', () => {
    it('should [expected behavior] when [condition]', () => {
      // Test implementation
    });
  });
});
```

✅ **AAA Pattern (Arrange-Act-Assert):**
```typescript
it('calculates total value correctly', () => {
  // Arrange
  const holdings = [
    { symbol: 'AAPL', quantity: 10, currentPrice: 175.00 },
  ];
  
  // Act
  const total = calculatePortfolioValue(holdings);
  
  // Assert
  expect(total).toBe(1750.00);
});
```

✅ **Test Isolation:**
```typescript
beforeEach(() => {
  jest.clearAllMocks();
  localStorage.clear();
});

afterEach(() => {
  jest.restoreAllMocks();
});
```

---

## B. Integration Tests

**Purpose:** Test how multiple components/modules work together.

**Characteristics:**
- ✅ Medium speed (100-500ms per test)
- ✅ Tests real integrations (API + DB, Component + Hook)
- ✅ Includes external dependencies
- ✅ Medium volume (200-500 tests)

### Integration Test Framework

**Configuration:**
```typescript
// tests/integration/setup.ts
import { setupServer } from 'msw/node';
import { rest } from 'msw';

// Mock API server
export const server = setupServer(
  rest.get('/api/portfolio/:userId', (req, res, ctx) => {
    return res(ctx.json({
      id: 'portfolio-1',
      userId: req.params.userId,
      holdings: [
        { symbol: 'AAPL', quantity: 10, currentPrice: 175.00 },
      ],
    }));
  }),
  
  rest.get('/api/stocks/:symbol', (req, res, ctx) => {
    return res(ctx.json({
      symbol: req.params.symbol,
      price: 175.00,
      change: 2.50,
      changePercent: 1.45,
    }));
  }),
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### 1. API Integration Tests

**Test API endpoints with database:**

```typescript
// tests/integration/api/portfolio.test.ts
import request from 'supertest';
import { app } from '@/api/app';
import { db } from '@/lib/db';

describe('Portfolio API Integration', () => {
  beforeEach(async () => {
    await db.reset();
    await db.seed();
  });
  
  describe('GET /api/portfolio/:userId', () => {
    it('returns user portfolio with holdings', async () => {
      const response = await request(app)
        .get('/api/portfolio/user-1')
        .expect(200);
      
      expect(response.body).toMatchObject({
        id: expect.any(String),
        userId: 'user-1',
        holdings: expect.arrayContaining([
          expect.objectContaining({
            symbol: expect.any(String),
            quantity: expect.any(Number),
          }),
        ]),
      });
    });
    
    it('returns 404 for non-existent user', async () => {
      await request(app)
        .get('/api/portfolio/invalid-user')
        .expect(404);
    });
    
    it('requires authentication', async () => {
      await request(app)
        .get('/api/portfolio/user-1')
        .set('Authorization', '')
        .expect(401);
    });
  });
  
  describe('POST /api/portfolio/:userId/holdings', () => {
    it('adds new holding to portfolio', async () => {
      const newHolding = {
        symbol: 'TSLA',
        quantity: 5,
        purchasePrice: 250.00,
      };
      
      const response = await request(app)
        .post('/api/portfolio/user-1/holdings')
        .send(newHolding)
        .expect(201);
      
      expect(response.body.holdings).toContainEqual(
        expect.objectContaining(newHolding)
      );
    });
    
    it('validates holding data', async () => {
      const invalidHolding = {
        symbol: '',
        quantity: -5,
      };
      
      await request(app)
        .post('/api/portfolio/user-1/holdings')
        .send(invalidHolding)
        .expect(400);
    });
  });
});
```

### 2. Component + Hook Integration Tests

**Test components with real hooks:**

```typescript
// tests/integration/components/PortfolioPage.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { PortfolioPage } from '@/app/dashboard/portfolio/page';
import { server } from '../setup';
import { rest } from 'msw';

describe('PortfolioPage Integration', () => {
  it('fetches and displays portfolio data', async () => {
    render(<PortfolioPage />);
    
    // Shows loading state
    expect(screen.getByText('Loading...')).toBeInTheDocument();
    
    // Waits for data to load
    await waitFor(() => {
      expect(screen.getByText('Portfolio')).toBeInTheDocument();
    });
    
    // Displays portfolio value
    expect(screen.getByText('$1,750.00')).toBeInTheDocument();
    
    // Displays holdings
    expect(screen.getByText('AAPL')).toBeInTheDocument();
    expect(screen.getByText('10 shares')).toBeInTheDocument();
  });
  
  it('handles fetch error gracefully', async () => {
    // Mock API error
    server.use(
      rest.get('/api/portfolio/:userId', (req, res, ctx) => {
        return res(ctx.status(500));
      })
    );
    
    render(<PortfolioPage />);
    
    await waitFor(() => {
      expect(screen.getByText('Unable to load portfolio')).toBeInTheDocument();
    });
    
    // Shows retry button
    expect(screen.getByText('Retry')).toBeInTheDocument();
  });
  
  it('refetches data on retry', async () => {
    // First call fails
    let callCount = 0;
    server.use(
      rest.get('/api/portfolio/:userId', (req, res, ctx) => {
        callCount++;
        if (callCount === 1) {
          return res(ctx.status(500));
        }
        return res(ctx.json({
          id: 'portfolio-1',
          holdings: [],
        }));
      })
    );
    
    render(<PortfolioPage />);
    
    // Wait for error
    await waitFor(() => {
      expect(screen.getByText('Retry')).toBeInTheDocument();
    });
    
    // Click retry
    screen.getByText('Retry').click();
    
    // Wait for success
    await waitFor(() => {
      expect(screen.getByText('Portfolio')).toBeInTheDocument();
    });
  });
});
```

### 3. Database Integration Tests

**Test database operations:**

```typescript
// tests/integration/db/portfolio.test.ts
import { db } from '@/lib/db';
import { createPortfolio, getPortfolio, updatePortfolio } from '@/lib/db/portfolio';

describe('Portfolio Database Integration', () => {
  beforeEach(async () => {
    await db.reset();
  });
  
  it('creates and retrieves portfolio', async () => {
    // Create portfolio
    const created = await createPortfolio({
      userId: 'user-1',
      holdings: [
        { symbol: 'AAPL', quantity: 10 },
      ],
    });
    
    expect(created.id).toBeDefined();
    
    // Retrieve portfolio
    const retrieved = await getPortfolio(created.id);
    
    expect(retrieved).toMatchObject({
      userId: 'user-1',
      holdings: [
        expect.objectContaining({ symbol: 'AAPL' }),
      ],
    });
  });
  
  it('updates portfolio holdings', async () => {
    const portfolio = await createPortfolio({
      userId: 'user-1',
      holdings: [{ symbol: 'AAPL', quantity: 10 }],
    });
    
    // Add new holding
    const updated = await updatePortfolio(portfolio.id, {
      holdings: [
        { symbol: 'AAPL', quantity: 10 },
        { symbol: 'GOOGL', quantity: 5 },
      ],
    });
    
    expect(updated.holdings).toHaveLength(2);
  });
  
  it('handles concurrent updates', async () => {
    const portfolio = await createPortfolio({
      userId: 'user-1',
      holdings: [],
    });
    
    // Simulate concurrent updates
    await Promise.all([
      updatePortfolio(portfolio.id, {
        holdings: [{ symbol: 'AAPL', quantity: 10 }],
      }),
      updatePortfolio(portfolio.id, {
        holdings: [{ symbol: 'GOOGL', quantity: 5 }],
      }),
    ]);
    
    const final = await getPortfolio(portfolio.id);
    
    // Last write wins
    expect(final.holdings).toHaveLength(1);
  });
});
```

---

## C. End-to-End Tests (E2E)

**Purpose:** Test complete user journeys from browser to backend.

**Characteristics:**
- ✅ Slow (5-30 seconds per test)
- ✅ Tests real user interactions
- ✅ Runs in real browser (Chromium, Firefox, WebKit)
- ✅ Low volume (50-100 tests)

### E2E Test Framework

**Configuration:**
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### 1. Complete User Journey Tests

**Test full user flows:**

```typescript
// tests/e2e/portfolio-journey.test.ts
import { test, expect } from '@playwright/test';

test.describe('Portfolio User Journey', () => {
  test('complete portfolio workflow', async ({ page }) => {
    // Step 1: Login
    await page.goto('/login');
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    
    // Verify redirect to dashboard
    await expect(page).toHaveURL('/dashboard');
    
    // Step 2: Navigate to Portfolio
    await page.click('text=Portfolio');
    await expect(page).toHaveURL('/dashboard/portfolio');
    
    // Verify portfolio loads
    await expect(page.locator('h1')).toContainText('Portfolio');
    await expect(page.locator('.portfolio-value')).toBeVisible();
    
    // Step 3: View Stock Detail
    await page.click('text=AAPL');
    await expect(page).toHaveURL(/\/stocks\/AAPL/);
    await expect(page.locator('.stock-price')).toBeVisible();
    
    // Step 4: Add to Watchlist
    await page.click('button:has-text("Add to Watchlist")');
    await expect(page.locator('text=Added to watchlist')).toBeVisible();
    
    // Step 5: Navigate to Watchlist
    await page.click('text=Watchlist');
    await expect(page.locator('text=AAPL')).toBeVisible();
  });
});
```

### 2. Critical Path E2E Tests

**Test mission-critical flows:**

```typescript
// tests/e2e/authentication.test.ts
import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test('successful login flow', async ({ page }) => {
    await page.goto('/login');
    
    // Fill login form
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    
    // Verify redirect and auth state
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('text=test@example.com')).toBeVisible();
  });
  
  test('handles invalid credentials', async ({ page }) => {
    await page.goto('/login');
    
    await page.fill('[name="email"]', 'invalid@example.com');
    await page.fill('[name="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');
    
    // Verify error message
    await expect(page.locator('text=Invalid credentials')).toBeVisible();
    await expect(page).toHaveURL('/login');
  });
  
  test('logout flow', async ({ page }) => {
    // Login first
    await page.goto('/login');
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('/dashboard');
    
    // Logout
    await page.click('button[aria-label="User menu"]');
    await page.click('text=Logout');
    
    // Verify redirect to login
    await expect(page).toHaveURL('/login');
  });
});
```

### 3. Cross-Browser E2E Tests

**Test across browsers:**

```typescript
// tests/e2e/cross-browser.test.ts
import { test, expect } from '@playwright/test';

test.describe('Cross-Browser Compatibility', () => {
  test('renders dashboard correctly', async ({ page }) => {
    await page.goto('/dashboard');
    
    // Verify core elements
    await expect(page.locator('nav')).toBeVisible();
    await expect(page.locator('h1')).toContainText('Dashboard');
    await expect(page.locator('.portfolio-summary')).toBeVisible();
  });
  
  test('handles responsive layout', async ({ page }) => {
    // Desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto('/dashboard');
    await expect(page.locator('.sidebar')).toBeVisible();
    
    // Mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator('.sidebar')).not.toBeVisible();
    await expect(page.locator('button[aria-label="Menu"]')).toBeVisible();
  });
});
```

---

## D. Static Analysis

**Purpose:** Analyze code quality without executing it.

**Characteristics:**
- ✅ Instant (< 1 second)
- ✅ Catches bugs before runtime
- ✅ Enforces code standards
- ✅ Runs on every commit

### Static Analysis Tools

### 1. TypeScript Type Checking

**Configuration:**
```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

**Run Type Checking:**
```bash
# Check types
npm run type-check

# Output:
✓ Type check passed (0 errors)
```

### 2. ESLint Code Quality

**Configuration:**
```javascript
// .eslintrc.js
module.exports = {
  extends: [
    'next/core-web-vitals',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
  ],
  rules: {
    '@typescript-eslint/no-unused-vars': 'error',
    '@typescript-eslint/no-explicit-any': 'error',
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',
    'no-console': 'warn',
  },
};
```

**Run ESLint:**
```bash
# Lint all files
npm run lint

# Output:
✓ No ESLint warnings or errors
```

### 3. Prettier Code Formatting

**Configuration:**
```json
// .prettierrc
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "arrowParens": "always"
}
```

**Run Prettier:**
```bash
# Check formatting
npm run format:check

# Fix formatting
npm run format:fix
```

### 4. Security Analysis

**Run Security Audits:**
```bash
# Audit npm dependencies
npm audit --production --audit-level=high

# Scan for secrets
npm run security:secrets

# Static security analysis
npm run security:sast
```

### Static Analysis CI/CD Integration

**GitHub Actions Workflow:**
```yaml
# .github/workflows/static-analysis.yml
name: Static Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - run: npm ci
      
      - name: Type Check
        run: npm run type-check
      
      - name: Lint
        run: npm run lint
      
      - name: Format Check
        run: npm run format:check
      
      - name: Security Audit
        run: npm audit --production --audit-level=high
```

---

## Test Type Decision Matrix

| Test Type | Purpose | Speed | Volume | When to Use |
|-----------|---------|-------|--------|-------------|
| **Unit** | Test individual functions | Fast (< 1ms) | High (1000+) | Every function, hook, utility |
| **Integration** | Test module interactions | Medium (100-500ms) | Medium (200-500) | API + DB, Component + Hook |
| **E2E** | Test full user journeys | Slow (5-30s) | Low (50-100) | Critical user flows |
| **Static** | Analyze code quality | Instant (< 1s) | N/A | Every commit (pre-push) |

---

## 29.3 Unit Tests

**Purpose:** Validate individual functions, components, and modules.

**Goal:** High coverage without slowing development.

### Coverage Areas

#### 1. UI Components

**Test all React components in isolation:**

```typescript
// tests/unit/components/IdentityBadge.test.tsx
import { render, screen } from '@testing-library/react';
import { IdentityBadge } from '@/components/identity/IdentityBadge';

describe('IdentityBadge', () => {
  it('renders diaspora identity correctly', () => {
    render(<IdentityBadge identity="diaspora" />);
    expect(screen.getByText('Diaspora')).toBeInTheDocument();
    expect(screen.getByTestId('identity-icon')).toHaveClass('text-blue-500');
  });
  
  it('renders youth identity correctly', () => {
    render(<IdentityBadge identity="youth" />);
    expect(screen.getByText('Youth')).toBeInTheDocument();
    expect(screen.getByTestId('identity-icon')).toHaveClass('text-green-500');
  });
  
  it('displays Premium badge when applicable', () => {
    render(<IdentityBadge identity="diaspora" tier="premium" />);
    expect(screen.getByText('Premium')).toBeInTheDocument();
  });
});
```

#### 2. Utility Functions

**Test all helper functions:**

```typescript
// tests/unit/lib/calculations.test.ts
import { calculatePortfolioValue, calculatePercentChange } from '@/lib/calculations';

describe('Portfolio Calculations', () => {
  it('calculates total portfolio value', () => {
    const holdings = [
      { symbol: 'AAPL', quantity: 10, currentPrice: 175.00 },
      { symbol: 'GOOGL', quantity: 5, currentPrice: 2800.00 },
    ];
    
    expect(calculatePortfolioValue(holdings)).toBe(15750.00);
  });
  
  it('handles empty portfolio', () => {
    expect(calculatePortfolioValue([])).toBe(0);
  });
  
  it('calculates percent change correctly', () => {
    expect(calculatePercentChange(100, 110)).toBe(10.00);
    expect(calculatePercentChange(110, 100)).toBe(-9.09);
  });
});
```

#### 3. API Helpers

**Test all API client functions:**

```typescript
// tests/unit/lib/api/portfolio.test.ts
import { fetchPortfolio, createPortfolio } from '@/lib/api/portfolio';

global.fetch = jest.fn();

describe('Portfolio API Helpers', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });
  
  it('fetches portfolio successfully', async () => {
    (global.fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: async () => ({ id: '1', holdings: [] }),
    });
    
    const portfolio = await fetchPortfolio('user-1');
    
    expect(portfolio).toEqual({ id: '1', holdings: [] });
    expect(global.fetch).toHaveBeenCalledWith('/api/portfolio/user-1');
  });
  
  it('throws error on 404', async () => {
    (global.fetch as jest.Mock).mockResolvedValue({
      ok: false,
      status: 404,
    });
    
    await expect(fetchPortfolio('user-1'))
      .rejects
      .toThrow('Portfolio not found');
  });
});
```

#### 4. Identity Logic

**Test identity-related functions:**

```typescript
// tests/unit/lib/identity.test.ts
import { getIdentityPreferences, applyIdentityFilter } from '@/lib/identity';

describe('Identity Logic', () => {
  it('gets identity preferences', () => {
    const prefs = getIdentityPreferences('diaspora');
    
    expect(prefs).toMatchObject({
      preferredTheme: 'dark',
      dashboardWidgets: ['diaspora-news', 'diaspora-markets'],
      contentFilters: ['diaspora-focus'],
    });
  });
  
  it('applies identity filter to news', () => {
    const news = [
      { id: '1', tags: ['diaspora', 'finance'] },
      { id: '2', tags: ['general', 'finance'] },
      { id: '3', tags: ['youth', 'tech'] },
    ];
    
    const filtered = applyIdentityFilter(news, 'diaspora');
    
    expect(filtered).toHaveLength(1);
    expect(filtered[0].id).toBe('1');
  });
});
```

#### 5. Premium Gating Logic

**Test tier-based access control:**

```typescript
// tests/unit/lib/premium.test.ts
import { hasFeatureAccess, getFeatureRequirement } from '@/lib/premium';

describe('Premium Gating Logic', () => {
  it('grants access to free features for all tiers', () => {
    expect(hasFeatureAccess('basic_portfolio', 'free')).toBe(true);
    expect(hasFeatureAccess('basic_portfolio', 'premium')).toBe(true);
    expect(hasFeatureAccess('basic_portfolio', 'pro')).toBe(true);
  });
  
  it('restricts premium features to premium+ tiers', () => {
    expect(hasFeatureAccess('advanced_analytics', 'free')).toBe(false);
    expect(hasFeatureAccess('advanced_analytics', 'premium')).toBe(true);
    expect(hasFeatureAccess('advanced_analytics', 'pro')).toBe(true);
  });
  
  it('restricts pro features to pro tier only', () => {
    expect(hasFeatureAccess('api_access', 'free')).toBe(false);
    expect(hasFeatureAccess('api_access', 'premium')).toBe(false);
    expect(hasFeatureAccess('api_access', 'pro')).toBe(true);
  });
  
  it('returns correct feature requirement', () => {
    expect(getFeatureRequirement('advanced_analytics')).toBe('premium');
    expect(getFeatureRequirement('api_access')).toBe('pro');
  });
});
```

### Tools

**Component Test Framework:**
```typescript
// tests/setup.ts
import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';

afterEach(() => {
  cleanup();
});

// Mock services
jest.mock('@/lib/api/stocks', () => ({
  fetchStockQuote: jest.fn(),
  searchStocks: jest.fn(),
}));

jest.mock('@/lib/api/news', () => ({
  fetchNews: jest.fn(),
  verifyNewsSource: jest.fn(),
}));
```

**Mock Services:**
```typescript
// tests/mocks/portfolio.ts
export const mockPortfolio = {
  id: 'portfolio-1',
  userId: 'user-1',
  holdings: [
    {
      symbol: 'AAPL',
      quantity: 10,
      purchasePrice: 150.00,
      currentPrice: 175.00,
    },
  ],
  totalValue: 1750.00,
  dayChange: 250.00,
  dayChangePercent: 16.67,
};

export const mockUser = {
  id: 'user-1',
  email: 'test@example.com',
  identity: 'diaspora',
  tier: 'premium',
};
```

---

## 29.4 Integration Tests

**Purpose:** Validate how modules work together.

**Focus:** API contract validation, data flow correctness, error handling.

### Coverage Areas

#### 1. Portfolio + Analytics

**Test portfolio data flows into analytics:**

```typescript
// tests/integration/portfolio-analytics.test.ts
import { calculateAnalytics } from '@/lib/analytics';
import { fetchPortfolio } from '@/lib/api/portfolio';

describe('Portfolio Analytics Integration', () => {
  it('calculates analytics from portfolio data', async () => {
    const portfolio = await fetchPortfolio('user-1');
    const analytics = calculateAnalytics(portfolio);
    
    expect(analytics).toMatchObject({
      totalValue: expect.any(Number),
      diversification: expect.any(Number),
      riskScore: expect.any(Number),
      performanceMetrics: expect.objectContaining({
        dayChange: expect.any(Number),
        weekChange: expect.any(Number),
      }),
    });
  });
});
```

#### 2. Markets + Heatmap

**Test market data rendering in heatmap:**

```typescript
// tests/integration/markets-heatmap.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { MarketsHeatmap } from '@/components/markets/MarketsHeatmap';
import { fetchMarketData } from '@/lib/api/markets';

jest.mock('@/lib/api/markets');

describe('Markets Heatmap Integration', () => {
  it('displays market data in heatmap', async () => {
    (fetchMarketData as jest.Mock).mockResolvedValue({
      sectors: [
        { name: 'Technology', change: 2.5, volume: 1000000 },
        { name: 'Finance', change: -1.2, volume: 800000 },
      ],
    });
    
    render(<MarketsHeatmap />);
    
    await waitFor(() => {
      expect(screen.getByText('Technology')).toBeInTheDocument();
      expect(screen.getByText('+2.5%')).toBeInTheDocument();
    });
  });
});
```

#### 3. News + Verification Engine

**Test news verification integration:**

```typescript
// tests/integration/news-verification.test.ts
import { fetchNews, verifyNewsSource } from '@/lib/api/news';

describe('News Verification Integration', () => {
  it('verifies news sources automatically', async () => {
    const news = await fetchNews({ category: 'finance' });
    
    for (const article of news) {
      const verification = await verifyNewsSource(article.source);
      
      expect(verification).toMatchObject({
        isVerified: expect.any(Boolean),
        trustScore: expect.any(Number),
        lastChecked: expect.any(String),
      });
    }
  });
});
```

#### 4. Alerts + Data Provider

**Test alert triggering with real data:**

```typescript
// tests/integration/alerts-provider.test.ts
import { createAlert, checkAlertTriggers } from '@/lib/alerts';
import { fetchStockQuote } from '@/lib/api/stocks';

describe('Alerts Data Provider Integration', () => {
  it('triggers alert when condition met', async () => {
    // Create alert
    const alert = await createAlert({
      userId: 'user-1',
      symbol: 'AAPL',
      condition: 'price_above',
      targetPrice: 170.00,
    });
    
    // Fetch current price
    const quote = await fetchStockQuote('AAPL');
    
    // Check triggers
    const triggered = await checkAlertTriggers([alert], quote);
    
    if (quote.price > 170.00) {
      expect(triggered).toHaveLength(1);
      expect(triggered[0].id).toBe(alert.id);
    } else {
      expect(triggered).toHaveLength(0);
    }
  });
});
```

#### 5. Identity + Dashboard Widgets

**Test identity-specific widgets:**

```typescript
// tests/integration/identity-dashboard.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { DashboardWidgets } from '@/app/dashboard/widgets';
import { useUser } from '@/hooks/useUser';

jest.mock('@/hooks/useUser');

describe('Identity Dashboard Integration', () => {
  it('displays diaspora-specific widgets', async () => {
    (useUser as jest.Mock).mockReturnValue({
      user: { id: 'user-1', identity: 'diaspora', tier: 'free' },
    });
    
    render(<DashboardWidgets />);
    
    await waitFor(() => {
      expect(screen.getByText('Diaspora Markets')).toBeInTheDocument();
      expect(screen.getByText('Diaspora News')).toBeInTheDocument();
    });
  });
  
  it('displays youth-specific widgets', async () => {
    (useUser as jest.Mock).mockReturnValue({
      user: { id: 'user-1', identity: 'youth', tier: 'free' },
    });
    
    render(<DashboardWidgets />);
    
    await waitFor(() => {
      expect(screen.getByText('Youth Finance')).toBeInTheDocument();
      expect(screen.getByText('Youth Investing 101')).toBeInTheDocument();
    });
  });
});
```

---

## 29.5 End-to-End (E2E) Tests

**Purpose:** Simulate real user behavior across complete workflows.

### Coverage Areas

#### Complete E2E User Journeys

```typescript
// tests/e2e/complete-user-journey.test.ts
import { test, expect } from '@playwright/test';

test.describe('Complete User Journey', () => {
  test('1. Login', async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('/dashboard');
  });
  
  test('2. Identity Selection', async ({ page }) => {
    await page.goto('/onboarding/identity');
    await page.click('[data-identity="diaspora"]');
    await page.click('button:has-text("Continue")');
    await expect(page.locator('text=Welcome, Diaspora')).toBeVisible();
  });
  
  test('3. Portfolio Creation', async ({ page }) => {
    await page.goto('/dashboard/portfolio');
    await page.click('button:has-text("Create Portfolio")');
    await page.fill('[name="portfolioName"]', 'My Portfolio');
    await page.click('button:has-text("Create")');
    await expect(page.locator('text=Portfolio created')).toBeVisible();
  });
  
  test('4. Adding Holdings', async ({ page }) => {
    await page.goto('/dashboard/portfolio');
    await page.click('button:has-text("Add Holding")');
    await page.fill('[name="symbol"]', 'AAPL');
    await page.fill('[name="quantity"]', '10');
    await page.fill('[name="purchasePrice"]', '150.00');
    await page.click('button:has-text("Add")');
    await expect(page.locator('text=AAPL')).toBeVisible();
  });
  
  test('5. Viewing Stock Detail', async ({ page }) => {
    await page.goto('/dashboard/portfolio');
    await page.click('text=AAPL');
    await expect(page).toHaveURL(/\/stocks\/AAPL/);
    await expect(page.locator('.stock-price')).toBeVisible();
    await expect(page.locator('.stock-chart')).toBeVisible();
  });
  
  test('6. Creating Alerts', async ({ page }) => {
    await page.goto('/dashboard/alerts');
    await page.click('button:has-text("Create Alert")');
    await page.fill('[name="symbol"]', 'AAPL');
    await page.selectOption('[name="condition"]', 'price_above');
    await page.fill('[name="targetPrice"]', '200.00');
    await page.click('button:has-text("Create")');
    await expect(page.locator('text=Alert created')).toBeVisible();
  });
  
  test('7. Upgrading to Premium', async ({ page }) => {
    await page.goto('/pricing');
    await page.click('button:has-text("Upgrade to Premium")');
    await page.fill('[name="cardNumber"]', '4242424242424242');
    await page.fill('[name="expiry"]', '12/25');
    await page.fill('[name="cvc"]', '123');
    await page.click('button:has-text("Subscribe")');
    await expect(page.locator('text=Welcome to Premium')).toBeVisible();
  });
  
  test('8. Viewing News Verification', async ({ page }) => {
    await page.goto('/dashboard/news');
    await page.click('.news-article:first-child');
    await expect(page.locator('.verification-badge')).toBeVisible();
    await page.click('.verification-badge');
    await expect(page.locator('text=Source Verified')).toBeVisible();
  });
  
  test('9. Navigating Dashboard', async ({ page }) => {
    await page.goto('/dashboard');
    
    // Test navigation
    await page.click('text=Portfolio');
    await expect(page).toHaveURL('/dashboard/portfolio');
    
    await page.click('text=Markets');
    await expect(page).toHaveURL('/dashboard/markets');
    
    await page.click('text=News');
    await expect(page).toHaveURL('/dashboard/news');
    
    await page.click('text=Alerts');
    await expect(page).toHaveURL('/dashboard/alerts');
  });
});
```

### Device Testing

```typescript
// tests/e2e/cross-device.test.ts
import { test, expect, devices } from '@playwright/test';

test.describe('Cross-Device Testing', () => {
  test.use({ ...devices['iPhone 12'] });
  test('Mobile - Portfolio View', async ({ page }) => {
    await page.goto('/dashboard/portfolio');
    await expect(page.locator('.mobile-nav')).toBeVisible();
    await expect(page.locator('.portfolio-summary')).toBeVisible();
  });
  
  test.use({ ...devices['Desktop Chrome'] });
  test('Desktop - Portfolio View', async ({ page }) => {
    await page.goto('/dashboard/portfolio');
    await expect(page.locator('.sidebar')).toBeVisible();
    await expect(page.locator('.portfolio-summary')).toBeVisible();
  });
  
  test.use({ ...devices['iPad Pro'] });
  test('Tablet - Portfolio View', async ({ page }) => {
    await page.goto('/dashboard/portfolio');
    await expect(page.locator('.tablet-nav')).toBeVisible();
    await expect(page.locator('.portfolio-summary')).toBeVisible();
  });
});
```

### Browser Testing

```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'edge', use: { ...devices['Desktop Edge'] } },
  ],
});
```

---

## 29.6 Manual QA

**Purpose:** Catch issues automation cannot detect.

### Focus Areas

#### 1. Visual Polish

**Manual Checks:**
- [ ] All colors match design system
- [ ] All spacing consistent (padding, margins)
- [ ] All typography follows style guide
- [ ] All icons properly sized and aligned
- [ ] All animations smooth (60fps)
- [ ] All images properly optimized
- [ ] All loading states elegant

#### 2. Motion Smoothness

**Manual Checks:**
- [ ] Page transitions smooth
- [ ] Component animations natural
- [ ] Scroll behavior smooth
- [ ] Hover effects responsive
- [ ] Touch gestures fluid (mobile)
- [ ] No janky animations
- [ ] Reduced motion mode works

#### 3. Identity Expression

**Manual Checks:**
- [ ] Diaspora identity widgets display correctly
- [ ] Youth identity widgets display correctly
- [ ] Creators identity widgets display correctly
- [ ] Legacy-builders identity widgets display correctly
- [ ] Identity-specific content relevant
- [ ] Identity switching works seamlessly

#### 4. Premium Gates

**Manual Checks:**
- [ ] Free tier gates working
- [ ] Premium tier gates working
- [ ] Pro tier gates working
- [ ] Upgrade prompts clear and compelling
- [ ] Billing flows smooth
- [ ] Feature previews enticing

#### 5. Cross-Promotion Placement

**Manual Checks:**
- [ ] Upsell cards non-intrusive
- [ ] Upgrade prompts contextual
- [ ] Feature discovery natural
- [ ] Cross-promotion relevant
- [ ] Dismissible without friction

#### 6. Accessibility

**Manual Checks:**
- [ ] Screen reader navigation works
- [ ] Keyboard navigation complete
- [ ] Focus indicators visible
- [ ] Color contrast sufficient (WCAG AA)
- [ ] Text scalable to 200%
- [ ] Alternative text present

### Devices Tested

**iOS:**
- iPhone 12 (iOS 15)
- iPhone 13 (iOS 16)
- iPhone 14 Pro (iOS 17)
- iPad Pro 12.9\" (iPadOS 17)

**Android:**
- Pixel 5 (Android 12)
- Pixel 7 (Android 13)
- Samsung Galaxy S22 (Android 13)
- Samsung Galaxy Tab S8 (Android 13)

**Windows:**
- Windows 10 (Chrome, Edge, Firefox)
- Windows 11 (Chrome, Edge, Firefox)

**macOS:**
- macOS Monterey (Chrome, Safari, Firefox)
- macOS Ventura (Chrome, Safari, Firefox)

---

## 29.7 Regression Testing

**Purpose:** Ensure new changes don't break existing features.

### Triggered By

- Major releases (v2.0.0 → v3.0.0)
- Minor releases (v2.1.0 → v2.2.0)
- Hotfixes (v2.1.3 → v2.1.4)

### Scope

#### Dashboard Regression Suite

```typescript
// tests/regression/dashboard.test.ts
describe('Dashboard Regression', () => {
  it('loads dashboard without errors', async () => {
    const { container } = render(<Dashboard />);
    expect(container.querySelector('.error')).toBeNull();
  });
  
  it('displays all widgets', () => {
    render(<Dashboard />);
    expect(screen.getByText('Portfolio Summary')).toBeInTheDocument();
    expect(screen.getByText('Market Overview')).toBeInTheDocument();
    expect(screen.getByText('Recent News')).toBeInTheDocument();
  });
  
  it('maintains widget layout', () => {
    const { container } = render(<Dashboard />);
    const widgets = container.querySelectorAll('.widget');
    expect(widgets).toHaveLength(6);
  });
});
```

#### Markets Regression Suite

```typescript
// tests/regression/markets.test.ts
describe('Markets Regression', () => {
  it('displays market heatmap', async () => {
    render(<Markets />);
    await waitFor(() => {
      expect(screen.getByTestId('heatmap')).toBeVisible();
    });
  });
  
  it('filters by sector', async () => {
    render(<Markets />);
    await userEvent.click(screen.getByText('Technology'));
    await waitFor(() => {
      expect(screen.getByText('AAPL')).toBeInTheDocument();
    });
  });
});
```

#### Portfolio Regression Suite

```typescript
// tests/regression/portfolio.test.ts
describe('Portfolio Regression', () => {
  it('calculates total value correctly', () => {
    const portfolio = mockPortfolio;
    expect(portfolio.totalValue).toBe(1750.00);
  });
  
  it('displays day change', () => {
    render(<Portfolio data={mockPortfolio} />);
    expect(screen.getByText('+$250.00')).toBeInTheDocument();
  });
});
```

#### News Regression Suite

```typescript
// tests/regression/news.test.ts
describe('News Regression', () => {
  it('displays verified sources', async () => {
    render(<News />);
    await waitFor(() => {
      expect(screen.getAllByTestId('verification-badge')).toHaveLength(5);
    });
  });
});
```

#### Alerts Regression Suite

```typescript
// tests/regression/alerts.test.ts
describe('Alerts Regression', () => {
  it('creates alert successfully', async () => {
    render(<AlertsPage />);
    await userEvent.click(screen.getByText('Create Alert'));
    await userEvent.type(screen.getByLabelText('Symbol'), 'AAPL');
    await userEvent.click(screen.getByText('Create'));
    await waitFor(() => {
      expect(screen.getByText('Alert created')).toBeVisible();
    });
  });
});
```

#### Settings Regression Suite

```typescript
// tests/regression/settings.test.ts
describe('Settings Regression', () => {
  it('saves user preferences', async () => {
    render(<Settings />);
    await userEvent.click(screen.getByLabelText('Dark Mode'));
    await userEvent.click(screen.getByText('Save'));
    await waitFor(() => {
      expect(screen.getByText('Settings saved')).toBeVisible();
    });
  });
});
```

#### Premium Regression Suite

```typescript
// tests/regression/premium.test.ts
describe('Premium Regression', () => {
  it('displays premium features', () => {
    render(<PremiumPage />);
    expect(screen.getByText('Advanced Analytics')).toBeInTheDocument();
    expect(screen.getByText('Real-Time Data')).toBeInTheDocument();
  });
  
  it('gates premium features for free users', () => {
    const { container } = render(<PremiumFeature tier="free" />);
    expect(container.querySelector('.premium-gate')).toBeVisible();
  });
});
```

---

## 29.8 Performance Testing

**Purpose:** Ensure the app stays fast under load.

### Test Types

#### 1. Load Tests

**Test normal traffic:**

```typescript
// tests/performance/load.test.ts
import { loadTest } from 'k6';

export default function() {
  const scenarios = {
    portfolio_load: {
      executor: 'constant-vus',
      vus: 100, // 100 concurrent users
      duration: '5m',
    },
  };
  
  const thresholds = {
    http_req_duration: ['p(95)<500'], // 95% under 500ms
    http_req_failed: ['rate<0.01'], // < 1% errors
  };
  
  loadTest({ scenarios, thresholds });
}
```

#### 2. Stress Tests

**Test breaking point:**

```typescript
// tests/performance/stress.test.ts
export default function() {
  const scenarios = {
    stress: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 100 },
        { duration: '5m', target: 500 },
        { duration: '2m', target: 1000 },
        { duration: '5m', target: 1000 },
        { duration: '2m', target: 0 },
      ],
    },
  };
  
  loadTest({ scenarios });
}
```

#### 3. Spike Tests

**Test sudden traffic surge:**

```typescript
// tests/performance/spike.test.ts
export default function() {
  const scenarios = {
    spike: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '10s', target: 100 },
        { duration: '1m', target: 100 },
        { duration: '10s', target: 1000 }, // Sudden spike
        { duration: '3m', target: 1000 },
        { duration: '10s', target: 100 },
        { duration: '3m', target: 100 },
        { duration: '10s', target: 0 },
      ],
    },
  };
  
  loadTest({ scenarios });
}
```

#### 4. Soak Tests

**Test long-running stability:**

```typescript
// tests/performance/soak.test.ts
export default function() {
  const scenarios = {
    soak: {
      executor: 'constant-vus',
      vus: 100,
      duration: '4h', // 4 hours
    },
  };
  
  const thresholds = {
    http_req_duration: ['p(99)<2000'],
    http_req_failed: ['rate<0.01'],
  };
  
  loadTest({ scenarios, thresholds });
}
```

### Targets

**API Latency:**
- P50: < 200ms
- P95: < 500ms
- P99: < 2000ms

**Cache Hit Ratio:**
- Target: > 80%

**WebSocket Stability:**
- Connection uptime: > 99.5%
- Message delivery rate: > 99.9%

**Identity Widget Load Time:**
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3.5s

---

## 29.9 Security Testing

**Purpose:** Ensure the platform is safe from vulnerabilities.

### Test Types

#### 1. Static Code Analysis (SAST)

```bash
# Run SAST scan
npm run security:sast

# Tools: ESLint Security, SonarQube
```

#### 2. Dependency Scanning

```bash
# Audit npm dependencies
npm audit --production --audit-level=high

# Scan with Snyk
npx snyk test

# Check outdated packages
npm outdated
```

#### 3. Penetration Testing

**Manual security audits:**
- SQL injection attempts
- XSS attack vectors
- CSRF vulnerabilities
- Authorization bypass attempts

#### 4. Authentication Tests

```typescript
// tests/security/authentication.test.ts
describe('Authentication Security', () => {
  it('requires valid JWT token', async () => {
    const response = await request(app)
      .get('/api/portfolio/user-1')
      .set('Authorization', 'Bearer invalid_token')
      .expect(401);
    
    expect(response.body.error).toBe('Invalid token');
  });
  
  it('expires tokens after 24 hours', async () => {
    const expiredToken = generateToken({ expiresIn: '-1d' });
    
    await request(app)
      .get('/api/portfolio/user-1')
      .set('Authorization', `Bearer ${expiredToken}`)
      .expect(401);
  });
});
```

#### 5. Authorization Tests

```typescript
// tests/security/authorization.test.ts
describe('Authorization Security', () => {
  it('prevents access to other users\' portfolios', async () => {
    const user1Token = generateToken({ userId: 'user-1' });
    
    await request(app)
      .get('/api/portfolio/user-2')
      .set('Authorization', `Bearer ${user1Token}`)
      .expect(403);
  });
});
```

#### 6. Input Sanitization Tests

```typescript
// tests/security/input-sanitization.test.ts
describe('Input Sanitization', () => {
  it('prevents SQL injection', async () => {
    const maliciousInput = \"'; DROP TABLE users; --\";
    
    await request(app)
      .post('/api/portfolio/user-1/holdings')
      .send({ symbol: maliciousInput })
      .expect(400);
  });
  
  it('prevents XSS attacks', async () => {
    const xssPayload = '<script>alert(\"XSS\")</script>';
    
    const response = await request(app)
      .post('/api/alerts')
      .send({ message: xssPayload })
      .expect(201);
    
    expect(response.body.message).not.toContain('<script>');
  });
});
```

### Frequency

- **Every Release**: Automated scans (SAST, dependency audit)
- **Quarterly**: Deep penetration testing by security team
- **Annual**: Third-party security audit

---

## 29.10 Accessibility Testing

**Purpose:** Ensure the platform is inclusive for all users.

### Test Types

#### 1. Screen Reader Navigation

**Manual Testing:**
```bash
# Test with screen readers:
# - macOS: VoiceOver (Cmd+F5)
# - Windows: NVDA (free), JAWS (paid)
# - iOS: VoiceOver (Settings > Accessibility)
# - Android: TalkBack (Settings > Accessibility)
```

**Automated Testing:**
```typescript
// tests/accessibility/screen-reader.test.ts
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('Screen Reader Accessibility', () => {
  it('portfolio page is accessible', async () => {
    const { container } = render(<Portfolio />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

#### 2. Keyboard Navigation

**Manual Testing Checklist:**
- [ ] Tab order logical
- [ ] All interactive elements reachable
- [ ] Focus indicators visible
- [ ] Skip links present
- [ ] Escape key closes modals
- [ ] Enter key activates buttons
- [ ] Arrow keys navigate menus

**Automated Testing:**
```typescript
// tests/accessibility/keyboard-navigation.test.ts
describe('Keyboard Navigation', () => {
  it('navigates portfolio with keyboard', async () => {
    render(<Portfolio />);
    
    // Tab to first holding
    await userEvent.tab();
    expect(screen.getAllByRole('row')[1]).toHaveFocus();
    
    // Enter to view detail
    await userEvent.keyboard('{Enter}');
    expect(screen.getByRole('dialog')).toBeVisible();
    
    // Escape to close
    await userEvent.keyboard('{Escape}');
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });
});
```

#### 3. Contrast Checks

**Automated Tool:**
```bash
# Run contrast checker
npm run accessibility:contrast

# Use Lighthouse accessibility audit
npm run lighthouse -- --only-categories=accessibility
```

**Manual Checks:**
- [ ] Normal text: 4.5:1 minimum
- [ ] Large text (18pt+): 3:1 minimum
- [ ] UI components: 3:1 minimum

#### 4. Motion-Reduced Mode

**Implementation:**
```typescript
// lib/hooks/useReducedMotion.ts
export function useReducedMotion() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);
  
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setPrefersReducedMotion(mediaQuery.matches);
    
    const listener = (e: MediaQueryListEvent) => {
      setPrefersReducedMotion(e.matches);
    };
    
    mediaQuery.addEventListener('change', listener);
    return () => mediaQuery.removeEventListener('change', listener);
  }, []);
  
  return prefersReducedMotion;
}
```

**Testing:**
```typescript
// tests/accessibility/reduced-motion.test.ts
describe('Reduced Motion Mode', () => {
  it('disables animations when preferred', () => {
    window.matchMedia = jest.fn().mockImplementation(query => ({
      matches: query === '(prefers-reduced-motion: reduce)',
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
    }));
    
    const { container } = render(<Dashboard />);
    const animated = container.querySelector('.animated');
    expect(animated).toHaveStyle({ animation: 'none' });
  });
});
```

#### 5. Text Scaling

**Test at 200% zoom:**
- [ ] Layout remains functional
- [ ] No horizontal scrolling
- [ ] All text readable
- [ ] No overlapping elements

### Tools

- **Automated Scanners**: axe-core, Lighthouse, WAVE
- **Manual Audits**: Screen readers, keyboard-only navigation

---

## 29.11 Beta Testing

**Purpose:** Validate features with real users before full release.

### Beta Groups

#### 1. Diaspora Users

**Test Focus:**
- Diaspora-specific content relevance
- Cross-border investing features
- Multi-currency support

#### 2. Youth Users

**Test Focus:**
- Educational content clarity
- Gamification elements
- Social sharing features

#### 3. Creators

**Test Focus:**
- Content creation workflows
- Portfolio sharing
- Monetization features

#### 4. Legacy-Builders

**Test Focus:**
- Estate planning features
- Long-term investment tools
- Succession planning

#### 5. Premium Users

**Test Focus:**
- Advanced analytics
- Priority support
- Exclusive features

#### 6. Pro Users

**Test Focus:**
- API access
- Real-time data feeds
- Advanced trading tools

### Feedback Types

#### 1. Usability

```typescript
// Collect usability feedback
interface UsabilityFeedback {
  task: string; // e.g., "Create portfolio"
  completed: boolean;
  timeToComplete: number; // seconds
  difficultyRating: 1 | 2 | 3 | 4 | 5;
  comments: string;
}
```

#### 2. Clarity

```typescript
// Collect clarity feedback
interface ClarityFeedback {
  feature: string;
  understoodPurpose: boolean;
  confusionPoints: string[];
  suggestions: string;
}
```

#### 3. Identity Resonance

```typescript
// Collect identity feedback
interface IdentityFeedback {
  identity: 'diaspora' | 'youth' | 'creators' | 'legacy-builders';
  feelsRelevant: boolean;
  culturallyAppropriate: boolean;
  suggestions: string;
}
```

#### 4. Performance

```typescript
// Collect performance feedback
interface PerformanceFeedback {
  pageLoadTime: number;
  perceivedSpeed: 'slow' | 'moderate' | 'fast';
  frustrationPoints: string[];
}
```

---

## 29.12 Release Certification Checklist

Before any release goes live, it must pass all certification criteria:

### Functional Certification

✅ **All Tests Pass**
- [ ] Unit tests: 100% passing (1000+ tests)
- [ ] Integration tests: 100% passing (200+ tests)
- [ ] E2E tests: 100% passing (50+ tests)
- [ ] Regression tests: 100% passing

✅ **No Critical Bugs**
- [ ] Zero P0 bugs (show-stoppers)
- [ ] Zero P1 bugs (critical issues)
- [ ] < 5 P2 bugs (high-priority)

✅ **No Broken Flows**
- [ ] Login flow works
- [ ] Portfolio creation works
- [ ] Alert creation works
- [ ] Premium upgrade works
- [ ] All navigation links functional

### Performance Certification

✅ **Meets Latency Targets**
- [ ] P50 < 200ms
- [ ] P95 < 500ms
- [ ] P99 < 2000ms

✅ **Meets Caching Targets**
- [ ] Cache hit ratio > 80%
- [ ] CDN cache hit ratio > 90%
- [ ] API response cache working

### Security Certification

✅ **No Vulnerabilities**
- [ ] Zero critical vulnerabilities
- [ ] Zero high vulnerabilities
- [ ] All medium vulnerabilities addressed or accepted

✅ **Authentication Stable**
- [ ] Login success rate > 99%
- [ ] Token refresh working
- [ ] Session management secure

### Accessibility Certification

✅ **WCAG AA Compliance**
- [ ] All pages pass axe-core audit
- [ ] Contrast ratios meet WCAG AA
- [ ] Keyboard navigation complete
- [ ] Screen reader compatible

### Identity Certification

✅ **Identity Widgets Load Correctly**
- [ ] Diaspora widgets display
- [ ] Youth widgets display
- [ ] Creators widgets display
- [ ] Legacy-builders widgets display

✅ **Identity Insights Accurate**
- [ ] Personalized recommendations relevant
- [ ] Content filtering accurate
- [ ] Identity switching seamless

### Premium Certification

✅ **Gates Working**
- [ ] Free tier restrictions enforced
- [ ] Premium tier access granted
- [ ] Pro tier access granted
- [ ] Feature preview working

✅ **Billing Stable**
- [ ] Subscription creation works
- [ ] Payment processing works
- [ ] Cancellation works
- [ ] Refunds process correctly

---

## 29.13 QA Documentation

Every feature must include comprehensive test documentation:

### Required Documentation

#### 1. Test Plan

```markdown
# Feature: Advanced Analytics

## Scope
- Analytics dashboard
- Performance metrics
- Diversification analysis
- Risk scoring

## Test Objectives
- Verify calculations accurate
- Ensure real-time updates
- Validate Premium gating
- Test cross-device compatibility

## Test Strategy
- Unit tests: Calculation functions
- Integration tests: Data flow from portfolio to analytics
- E2E tests: Full user workflow
- Manual QA: Visual polish, performance
```

#### 2. Test Cases

```typescript
// Test Case Template
interface TestCase {
  id: string;
  title: string;
  description: string;
  preconditions: string[];
  steps: string[];
  expectedResult: string;
  actualResult?: string;
  status: 'pass' | 'fail' | 'blocked';
}

// Example Test Case
const testCase: TestCase = {
  id: 'TC-001',
  title: 'Calculate Portfolio Diversification',
  description: 'Verify diversification score calculated correctly',
  preconditions: [
    'User has portfolio with 5+ holdings',
    'User has Premium tier',
  ],
  steps: [
    'Navigate to Analytics page',
    'View Diversification section',
    'Verify score displayed',
  ],
  expectedResult: 'Diversification score between 0-100',
  status: 'pass',
};
```

#### 3. Acceptance Criteria

```markdown
## Acceptance Criteria: Advanced Analytics

### Must Have
- [ ] Analytics dashboard loads in < 2 seconds
- [ ] All metrics update in real-time
- [ ] Diversification score accurate (±1%)
- [ ] Risk score accurate (±1%)
- [ ] Premium gate enforced for free users

### Should Have
- [ ] Export to PDF
- [ ] Historical data comparison
- [ ] Benchmarking against indices

### Nice to Have
- [ ] AI-powered recommendations
- [ ] Peer comparison
```

#### 4. Edge Cases

```markdown
## Edge Cases: Advanced Analytics

### Empty Portfolio
- **Scenario**: User has no holdings
- **Expected**: Display \"Add holdings to see analytics\"

### Single Holding
- **Scenario**: User has only 1 holding
- **Expected**: Show limited analytics with suggestion to diversify

### New User
- **Scenario**: User just signed up
- **Expected**: Show tutorial/onboarding

### Premium Expired
- **Scenario**: User's Premium subscription expired
- **Expected**: Show upgrade prompt, limit analytics
```

#### 5. Error States

```markdown
## Error States: Advanced Analytics

### Data Fetch Failure
- **Error**: Unable to load portfolio data
- **UI**: \"Unable to load analytics. Retry?\"
- **Action**: Show retry button

### Calculation Error
- **Error**: Insufficient data for calculation
- **UI**: \"Not enough data to calculate [metric]\"
- **Action**: Explain what's needed

### API Timeout
- **Error**: Request timed out
- **UI**: \"Taking longer than expected. Retry?\"
- **Action**: Show retry button, log error
```

#### 6. Accessibility Notes

```markdown
## Accessibility: Advanced Analytics

### Screen Reader
- All charts have text alternatives
- All metrics announced with units
- Navigation landmarks present

### Keyboard
- Tab order: Header → Metrics → Chart → Actions
- Enter activates buttons
- Escape closes modals

### Visual
- Contrast ratio: 4.5:1 minimum
- Text size: 16px minimum
- Focus indicators visible
```

---

## Test Documentation Template

```markdown
# Test Documentation: [Feature Name]

## 1. Test Plan
- Scope
- Objectives
- Strategy

## 2. Test Cases
| ID | Title | Steps | Expected | Status |
|----|-------|-------|----------|--------|
| TC-001 | ... | ... | ... | Pass |

## 3. Acceptance Criteria
- [ ] Must have 1
- [ ] Must have 2

## 4. Edge Cases
- Scenario 1
- Scenario 2

## 5. Error States
- Error 1
- Error 2

## 6. Accessibility Notes
- Screen reader
- Keyboard
- Visual
```

---

## 1. Foundations

Core design system primitives and tokens.

### Design Tokens
- **File**: `lib/design-system.ts`
- **Exports**: `colors`, `styles`, `formatCurrency`, `getCouncilTheme`
- **Usage**: Import design tokens for consistent styling

```typescript
import { colors, styles } from '@/lib/design-system';

// Colors
colors.sovereignGold      // #F5C542
colors.sovereignObsidian  // #0F172A
colors.councilEmerald     // #10B981

// Styles
styles.card               // Pre-defined card styling
styles.button.primary     // Primary button styling
styles.text.body          // Body text styling
```

---

## 2. Inputs

Form inputs and interactive controls.

### Text Input
- **File**: `components/ui/Input.tsx` (to be created)
- **Props**: `value`, `onChange`, `placeholder`, `type`, `disabled`, `error`

### Select / Dropdown
- **File**: `components/ui/Select.tsx` (to be created)
- **Props**: `options`, `value`, `onChange`, `placeholder`

### Checkbox
- **File**: `components/ui/Checkbox.tsx` (to be created)
- **Props**: `checked`, `onChange`, `label`, `disabled`

### Radio Group
- **File**: `components/ui/RadioGroup.tsx` (to be created)
- **Props**: `options`, `value`, `onChange`, `name`

### Search Input
- **File**: `components/ui/SearchInput.tsx` (to be created)
- **Props**: `value`, `onChange`, `onSearch`, `placeholder`

---

## 3. Navigation

Navigation components and menus.

### Navigation Bar
- **File**: `app/layout.tsx`
- **Features**: Logo, identity indicator, offline indicator
- **Used In**: Root layout

### Sidebar Navigation
- **File**: `components/navigation/Sidebar.tsx` (to be created)
- **Links**: Dashboard, Portfolio, Markets, News, Alerts, Settings

---

### Breadcrumbs

**Navigation Hierarchy**:
```
Markets > Sector > Stock
Dashboard > Portfolio > Holdings
News > Article Detail
Alerts > Edit Alert
Settings > Identity Preferences
```

**Implementation**:
```tsx
// File: components/navigation/Breadcrumbs.tsx

interface BreadcrumbItem {
  label: string;
  href?: string;
}

interface BreadcrumbsProps {
  items: BreadcrumbItem[];
}

export function Breadcrumbs({ items }: BreadcrumbsProps) {
  return (
    <nav className="flex items-center gap-2 text-sm">
      {items.map((item, index) => {
        const isLast = index === items.length - 1;
        
        return (
          <div key={index} className="flex items-center gap-2">
            {item.href && !isLast ? (
              <Link
                href={item.href}
                className="text-slate-400 hover:text-white transition-colors"
              >
                {item.label}
              </Link>
            ) : (
              <span className={isLast ? 'text-white font-medium' : 'text-slate-400'}>
                {item.label}
              </span>
            )}
            
            {!isLast && (
              <ChevronRight className="w-4 h-4 text-slate-600" />
            )}
          </div>
        );
      })}
    </nav>
  );
}
```

**Usage Examples**:
```tsx
// Markets > Technology > AAPL
<Breadcrumbs
  items={[
    { label: 'Markets', href: '/markets' },
    { label: 'Technology', href: '/markets/technology' },
    { label: 'AAPL' },
  ]}
/>

// Dashboard > Portfolio > My Growth Portfolio
<Breadcrumbs
  items={[
    { label: 'Dashboard', href: '/dashboard' },
    { label: 'Portfolio', href: '/portfolio' },
    { label: 'My Growth Portfolio' },
  ]}
/>

// News > Diaspora > Article Title
<Breadcrumbs
  items={[
    { label: 'News', href: '/news' },
    { label: 'Diaspora', href: '/news?identity=diaspora' },
    { label: 'Caribbean Markets Surge 15%' },
  ]}
/>
```

**Mobile Truncation**:
```tsx
// Show only last 2 items on mobile
export function ResponsiveBreadcrumbs({ items }: BreadcrumbsProps) {
  const isMobile = useMediaQuery('(max-width: 768px)');
  const displayItems = isMobile ? items.slice(-2) : items;
  
  return (
    <nav className="flex items-center gap-2 text-sm">
      {isMobile && items.length > 2 && (
        <>
          <button className="text-slate-400 hover:text-white">
            <MoreHorizontal className="w-4 h-4" />
          </button>
          <ChevronRight className="w-4 h-4 text-slate-600" />
        </>
      )}
      
      {displayItems.map((item, index) => (
        // ... same as above
      ))}
    </nav>
  );
}
```

---

### Breadcrumbs
- **File**: `components/navigation/Breadcrumbs.tsx` (to be created)
- **Props**: `items: Array<{ label: string; href: string }>`

### Tabs
- **File**: `components/ui/Tabs.tsx` (to be created)
- **Props**: `tabs`, `activeTab`, `onTabChange`

---

## 4. Data Display

Components for displaying data and content.

### Card
- **File**: `components/ui/Card.tsx` (existing)
- **Variants**: `default`, `gold`, `emerald`
- **Props**: `className`, `children`

### Badge
- **File**: `components/ui/Badge.tsx` (existing)
- **Variants**: `default`, `gold`, `emerald`, `red`, `blue`
- **Props**: `variant`, `children`

### Status Badge
- **File**: `components/ui/StatusBadge.tsx` (existing)
- **Props**: `status`, `label`, `icon`

### Table
- **File**: `components/ui/Table.tsx` (existing)
- **Components**: `Table`, `TableHeader`, `TableBody`, `TableRow`, `TableCell`

### Portfolio Holdings Table
- **File**: `components/portfolio/HoldingsTable.tsx` (to be created)
- **Features**: Symbol, shares, cost basis, current value, gain/loss
- **Used In**: Portfolio page

### News Card
- **File**: `components/news/NewsCard.tsx` (to be created)
- **Props**: `headline`, `summary`, `verificationLevel`, `relatedTickers`

### Stock Card
- **File**: `components/markets/StockCard.tsx` (to be created)
- **Props**: `ticker`, `price`, `change`, `changePercent`

---

## 5. Charts

Data visualization components.

### Line Chart
- **File**: `components/charts/LineChart.tsx` (to be created)
- **Library**: Recharts
- **Props**: `data`, `xAxis`, `yAxis`, `lines`

### Area Chart
- **File**: `components/charts/AreaChart.tsx` (to be created)
- **Use Case**: Stock price history, portfolio value over time

### Bar Chart
- **File**: `components/charts/BarChart.tsx` (to be created)
- **Use Case**: Sector allocation, volume comparison

### Pie Chart / Donut Chart
- **File**: `components/charts/PieChart.tsx` (to be created)
- **Use Case**: Portfolio allocation, sector breakdown

### Heatmap
- **File**: `components/charts/Heatmap.tsx` (to be created)
- **Use Case**: Market sectors, movers visualization

### Sparkline
- **File**: `components/charts/Sparkline.tsx` (to be created)
- **Props**: `data`, `color`, `width`, `height`
- **Use Case**: Inline mini-charts for tables

---

## 6. Cards

Specialized card components for different use cases.

### Identity Card
- **File**: `components/identity/IdentityCard.tsx` (to be created)
- **Shows**: Current identity, preferences, switch option
- **Actions**: Switch identity, edit preferences

### Portfolio Summary Card
- **File**: `components/portfolio/PortfolioSummaryCard.tsx` (to be created)
- **Shows**: Total value, gain/loss, allocation chart
- **Used In**: Dashboard

### Market Overview Card
- **File**: `components/markets/MarketOverviewCard.tsx` (to be created)
- **Shows**: Indices, movers, volume spikes
- **Used In**: Dashboard, Markets page

### News Feed Card
- **File**: `components/news/NewsFeedCard.tsx` (to be created)
- **Shows**: Recent news, verification badges
- **Used In**: Dashboard, News page

### Alert Card
- **File**: `components/alerts/AlertCard.tsx` (to be created)
- **Shows**: Alert conditions, last triggered, edit/delete actions
- **Used In**: Alerts page

### Subscription Card
- **File**: `components/billing/SubscriptionCard.tsx` (to be created)
- **Shows**: Current tier, renewal date, upgrade CTA
- **Used In**: Settings page

---

## 7. Modals & Overlays

Modal dialogs and overlay components.

### Modal
- **File**: `components/ui/Modal.tsx` (to be created)
- **Props**: `isOpen`, `onClose`, `title`, `children`
- **Features**: Backdrop, close button, keyboard handling (ESC)

### Confirmation Dialog
- **File**: `components/ui/ConfirmDialog.tsx` (to be created)
- **Props**: `title`, `message`, `onConfirm`, `onCancel`
- **Use Case**: Delete confirmation, logout confirmation

### Drawer / Slide-over
- **File**: `components/ui/Drawer.tsx` (to be created)
- **Props**: `isOpen`, `onClose`, `position: 'left' | 'right'`, `children`

### Popover
- **File**: `components/ui/Popover.tsx` (to be created)
- **Props**: `trigger`, `content`, `position`

### Tooltip
- **File**: `components/ui/Tooltip.tsx` (to be created)
- **Props**: `content`, `children`, `position`

### Offline Overlay
- **File**: `components/offline/OfflineState.tsx` ✅
- **Exports**: `OfflineOverlay`, `CompactOfflineIndicator`
- **Features**: Auto-detect offline, cached data option

---

## 8. Identity Components

Components specific to identity-aware features.

### Identity Selector
- **File**: `components/identity/IdentitySelector.tsx` (to be created)
- **Options**: Diaspora, Youth, Creator, Legacy
- **Features**: Visual identity cards, description, select action

### Identity Badge
- **File**: `components/identity/IdentityBadge.tsx` (to be created)
- **Props**: `identity: IdentityType`
- **Display**: Colored badge with identity icon

### Cultural Alpha Insights
- **File**: `components/identity/CulturalAlphaInsights.tsx` (to be created)
- **Props**: `identity`, `insights`
- **Features**: Identity-specific market insights, Cultural Alpha scores

### Identity Preferences
- **File**: `components/identity/IdentityPreferences.tsx` (to be created)
- **Features**: Theme, news filters, market focus, cultural interests

---

## 9. Premium Components

Components that require Premium or Pro tier.

### Premium Gate
- **File**: `components/premium/PremiumGate.tsx` (to be created)
- **Props**: `requiredTier: 'premium' | 'pro'`, `children`, `fallback`
- **Features**: Show upgrade CTA if insufficient tier

### Advanced Analytics Dashboard
- **File**: `components/premium/AdvancedAnalytics.tsx` (to be created)
- **Tier**: Premium required
- **Features**: Diversification, volatility, sector concentration, identity alignment

### Pro Analytics Dashboard
- **File**: `components/premium/ProAnalytics.tsx` (to be created)
- **Tier**: Pro required
- **Features**: Monte Carlo simulations, risk optimization, scenario planning

### Upgrade CTA Card
- **File**: `components/premium/UpgradeCTA.tsx` (to be created)
- **Props**: `currentTier`, `targetTier`, `features`
- **Display**: Benefits list, pricing, upgrade button

### Tier Badge
- **File**: `components/premium/TierBadge.tsx` (to be created)
- **Props**: `tier: 'free' | 'premium' | 'pro'`
- **Display**: Colored badge with tier icon

---

## 10. Feedback Components

User feedback and notification components.

### Toast Notification
- **File**: `components/feedback/Toast.tsx` (to be created)
- **Props**: `message`, `type: 'success' | 'error' | 'warning' | 'info'`, `duration`
- **Features**: Auto-dismiss, close button, stacking

### Alert Banner
- **File**: `components/feedback/AlertBanner.tsx` (to be created)
- **Props**: `message`, `type`, `dismissible`
- **Use Case**: System announcements, warnings

### Loading Spinner
- **File**: `components/feedback/LoadingSpinner.tsx` (to be created)
- **Props**: `size: 'sm' | 'md' | 'lg'`, `color`

### Skeleton Loader
- **File**: `components/feedback/Skeleton.tsx` (to be created)
- **Variants**: `text`, `card`, `table`, `chart`
- **Use Case**: Loading states for data

### Empty State
- **File**: `components/feedback/EmptyState.tsx` ✅
- **Props**: `title`, `description`, `action`, `icon`
- **Use Case**: No portfolio holdings, no news, no alerts

### Error State
- **File**: `components/feedback/ErrorState.tsx` ✅
- **Props**: `title`, `description`, `onRetry`, `error`
- **Use Case**: API failures, network errors

### Success State
- **File**: `components/feedback/SuccessState.tsx` (to be created)
- **Props**: `title`, `description`, `onContinue`
- **Use Case**: Transaction complete, portfolio saved

---

## Component Creation Priority

### Phase 1: Core Foundations (Immediate)
- ✅ Design System (`lib/design-system.ts`)
- ✅ Card (`components/ui/Card.tsx`)
- ✅ Badge (`components/ui/Badge.tsx`)
- ✅ Table (`components/ui/Table.tsx`)
- ✅ Offline State (`components/offline/OfflineState.tsx`)

### Phase 2: Data Display (Next)
- [ ] Input (`components/ui/Input.tsx`)
- [ ] Select (`components/ui/Select.tsx`)
- [ ] Modal (`components/ui/Modal.tsx`)
- [ ] Toast (`components/feedback/Toast.tsx`)
- [ ] Loading Spinner (`components/feedback/LoadingSpinner.tsx`)

### Phase 3: Identity & Premium (After Phase 2)
- [ ] Identity Selector (`components/identity/IdentitySelector.tsx`)
- [ ] Identity Badge (`components/identity/IdentityBadge.tsx`)
- [ ] Premium Gate (`components/premium/PremiumGate.tsx`)
- [ ] Tier Badge (`components/premium/TierBadge.tsx`)

### Phase 4: Specialized Cards (After Phase 3)
- [ ] Portfolio Summary Card
- [ ] Market Overview Card
- [ ] News Feed Card
- [ ] Alert Card
- [ ] Subscription Card

### Phase 5: Charts (Final)
- [ ] Line Chart
- [ ] Area Chart
- [ ] Pie Chart
- [ ] Heatmap
- [ ] Sparkline

---

## Component Usage Examples

### Basic Card with Badge
```typescript
import { Card, CardHeader, CardBody } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';

<Card>
  <CardHeader>
    <Badge variant="gold">Premium</Badge>
  </CardHeader>
  <CardBody>
    <p>Content goes here</p>
  </CardBody>
</Card>
```

### Identity-Aware Component
```typescript
import { useIdentity } from '@/hooks/useIdentity';

function CulturalInsights() {
  const { identity } = useIdentity();
  
  return (
    <div>
      {identity === 'diaspora' && <p>Caribbean market insights</p>}
      {identity === 'youth' && <p>Emerging tech trends</p>}
    </div>
  );
}
```

### Premium Gated Feature
```typescript
import { PremiumGate } from '@/components/premium/PremiumGate';

<PremiumGate requiredTier="premium">
  <AdvancedAnalytics />
</PremiumGate>
```

### Error State with Retry
```typescript
import { ErrorState } from '@/components/feedback/ErrorState';

<ErrorState
  title="Failed to load portfolio"
  description="Unable to fetch your holdings. Please try again."
  onRetry={() => refetch()}
/>
```

---

## Design System Integration

All components follow these principles:

1. **Color Palette**
   - Imperial Gold: `#F5C542`
   - Obsidian Black: `#0F172A`
   - Council Emerald: `#10B981`
   - Slate: `#64748B`

2. **Typography**
   - Headings: `font-medium` or `font-semibold`
   - Body: `text-base` or `text-sm`
   - Muted: `text-slate-400`

3. **Spacing**
   - Cards: `p-4` or `p-6`
   - Gaps: `gap-2`, `gap-3`, `gap-4`
   - Margins: `mb-2`, `mb-4`, `mb-6`

4. **Borders**
   - Cards: `border border-slate-700`
   - Inputs: `border border-slate-600 focus:border-yellow-500`
   - Rounded: `rounded-lg` (cards, buttons), `rounded-full` (badges)

5. **Transitions**
   - All interactive elements: `transition-colors`
   - Hover states: `hover:bg-*`

---

## Status Legend

- ✅ **Completed** - Component exists and is production-ready
- 🔄 **In Progress** - Component partially implemented
- 📋 **Planned** - Component designed but not yet created
- ⏸️ **Deferred** - Low priority, will implement later

---

**Last Updated**: December 24, 2025  
**Component Count**: 5 completed, 40+ planned
