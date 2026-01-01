'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  LayoutDashboard, 
  Package, 
  Cpu, 
  Building2, 
  BarChart3, 
  Settings,
  Globe
} from 'lucide-react';

const menuItems = [
  { href: '/dashboard/overview', icon: LayoutDashboard, label: 'Overview' },
  { href: '/dashboard/capsules', icon: Package, label: 'Capsules' },
  { href: '/dashboard/intelligence-core', icon: Cpu, label: 'Intelligence Core' },
  { href: '/dashboard/industries', icon: Building2, label: 'Industries' },
  { href: '/dashboard/platforms', icon: Globe, label: 'Platforms' },
  { href: '/dashboard/analytics', icon: BarChart3, label: 'Analytics' },
  { href: '/dashboard/settings', icon: Settings, label: 'Settings' },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-white border-r border-gray-200 h-screen sticky top-0 overflow-y-auto">
      {/* Logo Section */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-600 to-purple-900 flex items-center justify-center">
            <span className="text-white font-bold text-xl">🔥</span>
          </div>
          <div>
            <h1 className="text-lg font-bold text-gray-900">Codex Dominion</h1>
            <p className="text-xs text-gray-500">Master Dashboard</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="p-4">
        <ul className="space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || pathname.startsWith(item.href + '/');
            
            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={`
                    flex items-center gap-3 px-4 py-3 rounded-lg transition-all
                    ${isActive 
                      ? 'bg-gradient-to-r from-purple-600 to-purple-800 text-white shadow-lg' 
                      : 'text-gray-700 hover:bg-gray-100'
                    }
                  `}
                >
                  <Icon size={20} />
                  <span className="font-medium">{item.label}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Status Footer */}
      <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200 bg-white">
        <div className="flex items-center gap-2 text-sm">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
          <span className="text-gray-600">System Operational</span>
        </div>
        <p className="text-xs text-gray-400 mt-1">Flask Backend: Active</p>
      </div>
    </aside>
  );
}
