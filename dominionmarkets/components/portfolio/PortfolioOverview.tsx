/**
 * Portfolio Overview Component
 * Shows total value, P&L, and quick actions
 */

"use client"

import { ArrowUpIcon, ArrowDownIcon, RefreshCcw, Plus, Upload, Download } from 'lucide-react'

interface PortfolioOverviewProps {
  portfolio: {
    total_value: number
    daily_change: number
    daily_change_percent: number
    all_time_return: number
    all_time_return_percent: number
  }
  onAddHolding: () => void
  onRefresh: () => void
  userTier: string
}

export default function PortfolioOverview({ portfolio, onAddHolding, onRefresh, userTier }: PortfolioOverviewProps) {
  const isDailyPositive = portfolio.daily_change >= 0
  const isAllTimePositive = portfolio.all_time_return >= 0

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2
    }).format(value)
  }

  const formatPercent = (value: number) => {
    return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      {/* Total Value */}
      <div className="mb-6">
        <p className="text-sm text-gray-600 mb-1">Total Portfolio Value</p>
        <h2 className="text-4xl font-bold text-gray-900">{formatCurrency(portfolio.total_value)}</h2>
      </div>

      {/* P&L Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {/* Daily Change */}
        <div className="flex items-start">
          <div className={`p-2 rounded-lg ${isDailyPositive ? 'bg-emerald-50' : 'bg-red-50'} mr-3`}>
            {isDailyPositive ? (
              <ArrowUpIcon className="h-5 w-5 text-emerald-600" />
            ) : (
              <ArrowDownIcon className="h-5 w-5 text-red-600" />
            )}
          </div>
          <div>
            <p className="text-sm text-gray-600">Today's Change</p>
            <p className={`text-xl font-semibold ${isDailyPositive ? 'text-emerald-600' : 'text-red-600'}`}>
              {formatCurrency(portfolio.daily_change)}
            </p>
            <p className={`text-sm ${isDailyPositive ? 'text-emerald-600' : 'text-red-600'}`}>
              {formatPercent(portfolio.daily_change_percent)}
            </p>
          </div>
        </div>

        {/* All-Time Return */}
        <div className="flex items-start">
          <div className={`p-2 rounded-lg ${isAllTimePositive ? 'bg-emerald-50' : 'bg-red-50'} mr-3`}>
            {isAllTimePositive ? (
              <ArrowUpIcon className="h-5 w-5 text-emerald-600" />
            ) : (
              <ArrowDownIcon className="h-5 w-5 text-red-600" />
            )}
          </div>
          <div>
            <p className="text-sm text-gray-600">All-Time Return</p>
            <p className={`text-xl font-semibold ${isAllTimePositive ? 'text-emerald-600' : 'text-red-600'}`}>
              {formatCurrency(portfolio.all_time_return)}
            </p>
            <p className={`text-sm ${isAllTimePositive ? 'text-emerald-600' : 'text-red-600'}`}>
              {formatPercent(portfolio.all_time_return_percent)}
            </p>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="flex flex-wrap gap-3">
        <button
          onClick={onAddHolding}
          className="flex items-center px-4 py-2 bg-dominion-gold text-gray-900 rounded-lg font-semibold hover:bg-yellow-500 transition-colors"
        >
          <Plus className="h-4 w-4 mr-2" />
          Add Holding
        </button>

        <button
          onClick={onRefresh}
          className="flex items-center px-4 py-2 bg-gray-100 text-gray-700 rounded-lg font-semibold hover:bg-gray-200 transition-colors"
        >
          <RefreshCcw className="h-4 w-4 mr-2" />
          Refresh Prices
        </button>

        <button
          className="flex items-center px-4 py-2 bg-gray-100 text-gray-700 rounded-lg font-semibold hover:bg-gray-200 transition-colors"
        >
          <Upload className="h-4 w-4 mr-2" />
          Import CSV
        </button>

        <button
          className={`flex items-center px-4 py-2 rounded-lg font-semibold transition-colors ${
            userTier === 'pro'
              ? 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              : 'bg-gray-50 text-gray-400 cursor-not-allowed'
          }`}
          disabled={userTier !== 'pro'}
          title={userTier !== 'pro' ? 'Pro feature' : ''}
        >
          <Download className="h-4 w-4 mr-2" />
          Export CSV
          {userTier !== 'pro' && <span className="ml-1 text-xs">👑</span>}
        </button>
      </div>

      {/* Last Updated */}
      <p className="text-xs text-gray-500 mt-4">
        Prices updated 5 minutes ago • {userTier === 'free' ? '15-minute delayed data' : 'Real-time data'}
      </p>
    </div>
  )
}
