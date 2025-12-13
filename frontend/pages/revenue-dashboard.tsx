import React, { useState } from 'react';
import Head from 'next/head';

interface Sale {
  id: string;
  platform: string;
  product: string;
  amount: number;
  currency: string;
  timestamp: Date;
  customer: string;
  status: 'completed' | 'pending' | 'refunded';
}

interface PlatformBalance {
  platform: string;
  icon: string;
  balance: number;
  pendingBalance: number;
  totalSales: number;
  salesCount: number;
  color: string;
  change24h: number;
}

interface RevenueMetric {
  label: string;
  value: string;
  change: string;
  isPositive: boolean;
  icon: string;
}

export default function RevenueDashboard() {
  const [selectedTimeframe, setSelectedTimeframe] = useState<'today' | 'week' | 'month' | 'year'>('today');

  const platformBalances: PlatformBalance[] = [
    {
      platform: 'Shopify',
      icon: '🛒',
      balance: 12450.75,
      pendingBalance: 2340.50,
      totalSales: 14791.25,
      salesCount: 87,
      color: 'from-green-600 to-teal-600',
      change24h: 8.5,
    },
    {
      platform: 'Stripe',
      icon: '💳',
      balance: 8920.30,
      pendingBalance: 1200.00,
      totalSales: 10120.30,
      salesCount: 45,
      color: 'from-purple-600 to-pink-600',
      change24h: 12.3,
    },
    {
      platform: 'PayPal',
      icon: '💰',
      balance: 5680.90,
      pendingBalance: 890.25,
      totalSales: 6571.15,
      salesCount: 34,
      color: 'from-blue-600 to-cyan-600',
      change24h: -2.1,
    },
    {
      platform: 'WooCommerce',
      icon: '🏪',
      balance: 3420.60,
      pendingBalance: 450.00,
      totalSales: 3870.60,
      salesCount: 28,
      color: 'from-yellow-600 to-orange-600',
      change24h: 5.7,
    },
    {
      platform: 'Affiliate Network',
      icon: '🤝',
      balance: 2150.40,
      pendingBalance: 680.75,
      totalSales: 2831.15,
      salesCount: 56,
      color: 'from-indigo-600 to-purple-600',
      change24h: 15.2,
    },
    {
      platform: 'Digital Downloads',
      icon: '📥',
      balance: 1890.25,
      pendingBalance: 0,
      totalSales: 1890.25,
      salesCount: 42,
      color: 'from-red-600 to-pink-600',
      change24h: 6.8,
    },
    {
      platform: 'Subscriptions',
      icon: '📋',
      balance: 4560.00,
      pendingBalance: 0,
      totalSales: 4560.00,
      salesCount: 38,
      color: 'from-cyan-600 to-blue-600',
      change24h: 3.4,
    },
    {
      platform: 'Consulting',
      icon: '💼',
      balance: 7200.00,
      pendingBalance: 3600.00,
      totalSales: 10800.00,
      salesCount: 6,
      color: 'from-green-600 to-emerald-600',
      change24h: 20.0,
    },
  ];

  const recentSales: Sale[] = [
    {
      id: '1',
      platform: 'Shopify',
      product: 'Premium Course Bundle',
      amount: 299.00,
      currency: 'USD',
      timestamp: new Date(Date.now() - 300000),
      customer: 'John Smith',
      status: 'completed',
    },
    {
      id: '2',
      platform: 'Stripe',
      product: 'Monthly Subscription',
      amount: 49.00,
      currency: 'USD',
      timestamp: new Date(Date.now() - 600000),
      customer: 'Sarah Johnson',
      status: 'completed',
    },
    {
      id: '3',
      platform: 'PayPal',
      product: 'E-book: AI Mastery',
      amount: 27.00,
      currency: 'USD',
      timestamp: new Date(Date.now() - 900000),
      customer: 'Mike Chen',
      status: 'completed',
    },
    {
      id: '4',
      platform: 'Affiliate Network',
      product: 'Commission - Software Tool',
      amount: 125.50,
      currency: 'USD',
      timestamp: new Date(Date.now() - 1200000),
      customer: 'Affiliate Partner #47',
      status: 'pending',
    },
    {
      id: '5',
      platform: 'WooCommerce',
      product: 'Physical Product Pack',
      amount: 89.99,
      currency: 'USD',
      timestamp: new Date(Date.now() - 1500000),
      customer: 'Emily Davis',
      status: 'completed',
    },
  ];

  const totalBalance = platformBalances.reduce((sum, p) => sum + p.balance, 0);
  const totalPending = platformBalances.reduce((sum, p) => sum + p.pendingBalance, 0);
  const totalRevenue = platformBalances.reduce((sum, p) => sum + p.totalSales, 0);
  const totalSales = platformBalances.reduce((sum, p) => sum + p.salesCount, 0);

  const revenueMetrics: RevenueMetric[] = [
    {
      label: 'Total Revenue',
      value: `$${totalRevenue.toLocaleString('en-US', { minimumFractionDigits: 2 })}`,
      change: '+18.2%',
      isPositive: true,
      icon: '💰',
    },
    {
      label: 'Available Balance',
      value: `$${totalBalance.toLocaleString('en-US', { minimumFractionDigits: 2 })}`,
      change: '+12.5%',
      isPositive: true,
      icon: '💵',
    },
    {
      label: 'Pending Clearance',
      value: `$${totalPending.toLocaleString('en-US', { minimumFractionDigits: 2 })}`,
      change: '+5.3%',
      isPositive: true,
      icon: '⏳',
    },
    {
      label: 'Total Sales',
      value: totalSales.toString(),
      change: '+24.1%',
      isPositive: true,
      icon: '📊',
    },
  ];

  return (
    <>
      <Head>
        <title>Revenue Dashboard | CodexDominion</title>
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-green-900 to-gray-900 text-white">
        {/* Header */}
        <div className="bg-gray-800/50 backdrop-blur-lg border-b border-gray-700 p-6">
          <div className="max-w-7xl mx-auto">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-3">
                <span className="text-4xl">💰</span>
                <div>
                  <h1 className="text-3xl font-bold">Revenue Dashboard</h1>
                  <p className="text-gray-400">Real-time sales tracking across all platforms</p>
                </div>
              </div>
              <div className="flex space-x-2">
                {(['today', 'week', 'month', 'year'] as const).map((timeframe) => (
                  <button
                    key={timeframe}
                    onClick={() => setSelectedTimeframe(timeframe)}
                    className={`px-4 py-2 rounded-lg font-semibold capitalize ${
                      selectedTimeframe === timeframe
                        ? 'bg-green-600'
                        : 'bg-gray-700 hover:bg-gray-600'
                    }`}
                  >
                    {timeframe}
                  </button>
                ))}
              </div>
            </div>

            {/* Top Metrics */}
            <div className="grid grid-cols-4 gap-4">
              {revenueMetrics.map((metric) => (
                <div
                  key={metric.label}
                  className="bg-gradient-to-r from-green-600 to-teal-600 rounded-xl p-6 border border-white/20"
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-3xl">{metric.icon}</span>
                    <span className={`text-sm font-bold ${metric.isPositive ? 'text-green-200' : 'text-red-200'}`}>
                      {metric.change}
                    </span>
                  </div>
                  <div className="text-3xl font-bold mb-1">{metric.value}</div>
                  <div className="text-sm text-green-100">{metric.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="max-w-7xl mx-auto p-6 grid grid-cols-3 gap-6">
          {/* Platform Balances */}
          <div className="col-span-2 space-y-4">
            <h2 className="text-2xl font-bold mb-4">💳 Platform Balances</h2>
            {platformBalances.map((platform) => (
              <div
                key={platform.platform}
                className="bg-gray-800/50 backdrop-blur-lg border border-gray-700 rounded-xl p-6"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <span className="text-4xl">{platform.icon}</span>
                    <div>
                      <h3 className="text-xl font-bold">{platform.platform}</h3>
                      <p className="text-sm text-gray-400">{platform.salesCount} sales</p>
                    </div>
                  </div>
                  <div className={`flex items-center space-x-2 ${
                    platform.change24h >= 0 ? 'text-green-400' : 'text-red-400'
                  }`}>
                    <span className="text-2xl">{platform.change24h >= 0 ? '↑' : '↓'}</span>
                    <span className="text-xl font-bold">{Math.abs(platform.change24h)}%</span>
                  </div>
                </div>

                <div className="grid grid-cols-4 gap-4">
                  <div className="bg-gray-900/50 rounded-lg p-3 text-center">
                    <div className="text-2xl font-bold text-green-400">
                      ${platform.balance.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                    </div>
                    <div className="text-xs text-gray-400">Available</div>
                  </div>
                  <div className="bg-gray-900/50 rounded-lg p-3 text-center">
                    <div className="text-2xl font-bold text-yellow-400">
                      ${platform.pendingBalance.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                    </div>
                    <div className="text-xs text-gray-400">Pending</div>
                  </div>
                  <div className="bg-gray-900/50 rounded-lg p-3 text-center">
                    <div className="text-2xl font-bold text-blue-400">
                      ${platform.totalSales.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                    </div>
                    <div className="text-xs text-gray-400">Total Sales</div>
                  </div>
                  <div className="bg-gray-900/50 rounded-lg p-3 text-center">
                    <div className="text-2xl font-bold text-purple-400">{platform.salesCount}</div>
                    <div className="text-xs text-gray-400">Transactions</div>
                  </div>
                </div>

                <div className="mt-4 flex space-x-2">
                  <button className="flex-1 py-2 bg-green-600 rounded-lg hover:bg-green-700 font-semibold text-sm">
                    💸 Withdraw
                  </button>
                  <button className="flex-1 py-2 bg-blue-600 rounded-lg hover:bg-blue-700 font-semibold text-sm">
                    📊 View Details
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Recent Sales Feed */}
          <div className="space-y-4">
            <h2 className="text-2xl font-bold mb-4">🔔 Recent Sales</h2>
            <div className="space-y-3">
              {recentSales.map((sale) => (
                <div
                  key={sale.id}
                  className="bg-gray-800/50 backdrop-blur-lg border border-gray-700 rounded-xl p-4"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-1">
                        <span className={`px-2 py-1 rounded text-xs font-bold ${
                          sale.status === 'completed' ? 'bg-green-600' :
                          sale.status === 'pending' ? 'bg-yellow-600' :
                          'bg-red-600'
                        }`}>
                          {sale.status.toUpperCase()}
                        </span>
                        <span className="text-xs text-gray-400">{sale.platform}</span>
                      </div>
                      <h4 className="font-bold text-sm mb-1">{sale.product}</h4>
                      <p className="text-xs text-gray-400">{sale.customer}</p>
                    </div>
                    <div className="text-right">
                      <div className="text-xl font-bold text-green-400">
                        ${sale.amount.toFixed(2)}
                      </div>
                      <div className="text-xs text-gray-500">
                        {sale.timestamp.toLocaleTimeString()}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Quick Stats */}
            <div className="bg-gradient-to-br from-green-600/20 to-teal-600/20 border border-green-500/30 rounded-xl p-4 mt-6">
              <h3 className="font-bold mb-3">📈 Today's Performance</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-400">Avg Sale Value</span>
                  <span className="font-bold text-green-400">
                    ${(totalRevenue / totalSales).toFixed(2)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Conversion Rate</span>
                  <span className="font-bold text-blue-400">8.7%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Total Platforms</span>
                  <span className="font-bold text-purple-400">{platformBalances.length}</span>
                </div>
              </div>
            </div>

            {/* Auto-Withdrawal */}
            <div className="bg-gradient-to-br from-purple-600/20 to-pink-600/20 border border-purple-500/30 rounded-xl p-4">
              <h3 className="font-bold mb-3">⚙️ Auto-Withdrawal</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-400">Status</span>
                  <span className="text-sm font-bold text-green-400">ENABLED</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-400">Threshold</span>
                  <span className="text-sm font-bold">$10,000</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-400">Frequency</span>
                  <span className="text-sm font-bold">Weekly</span>
                </div>
                <button className="w-full py-2 bg-purple-600 rounded-lg hover:bg-purple-700 font-semibold text-sm">
                  ⚙️ Configure
                </button>
              </div>
            </div>

            {/* Payment Methods */}
            <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-4">
              <h3 className="font-bold mb-3">💳 Payment Methods</h3>
              <div className="space-y-2">
                <div className="flex items-center space-x-2 text-sm">
                  <span className="text-green-400">✓</span>
                  <span>Bank Account •••• 1234</span>
                </div>
                <div className="flex items-center space-x-2 text-sm">
                  <span className="text-green-400">✓</span>
                  <span>PayPal jermaine@***.com</span>
                </div>
                <div className="flex items-center space-x-2 text-sm">
                  <span className="text-green-400">✓</span>
                  <span>Crypto Wallet 0x***456</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
