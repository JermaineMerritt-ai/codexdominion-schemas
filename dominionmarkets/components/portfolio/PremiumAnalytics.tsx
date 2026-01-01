/**
 * Premium Analytics Component
 * Advanced metrics and insights (Premium/Pro only)
 */

"use client"

import { useState } from 'react'
import { TrendingUp, AlertTriangle, Activity, Target } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts'

interface PremiumAnalyticsProps {
  analytics: {
    diversification: {
      score: number
      rating: string
      sector_count: number
      stock_count: number
      concentration_risk: string
    }
    risk: {
      overall_score: number
      overall_rating: string
      volatility_30d: number
      max_drawdown_30d?: number
      best_day_30d?: number
      worst_day_30d?: number
      high_risk_holdings?: number
      medium_risk_holdings?: number
      low_risk_holdings?: number
    }
    sector_allocation: Record<string, any>
  } | null
  portfolioId: string
}

export default function PremiumAnalytics({ analytics, portfolioId }: PremiumAnalyticsProps) {
  const [selectedTimeframe, setSelectedTimeframe] = useState('30D')

  if (!analytics) {
    return null
  }

  // Mock historical performance data (replace with real API data)
  const performanceData = [
    { date: 'Nov 24', portfolio: 38500, sp500: 38000 },
    { date: 'Nov 28', portfolio: 39200, sp500: 38500 },
    { date: 'Dec 2', portfolio: 40100, sp500: 39000 },
    { date: 'Dec 6', portfolio: 39800, sp500: 38900 },
    { date: 'Dec 10', portfolio: 41200, sp500: 39500 },
    { date: 'Dec 14', portfolio: 41800, sp500: 40000 },
    { date: 'Dec 18', portfolio: 42100, sp500: 40300 },
    { date: 'Dec 22', portfolio: 42850, sp500: 40800 }
  ]

  const getDiversificationColor = (score: number) => {
    if (score >= 80) return 'text-emerald-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getRiskColor = (score: number) => {
    if (score <= 3) return 'text-emerald-600'
    if (score <= 7) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <div className="mt-6 space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Advanced Analytics</h2>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Diversification Score */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-2">
            <Target className="h-5 w-5 text-dominion-gold" />
            <span className="text-xs font-medium text-gray-500 uppercase">Diversification</span>
          </div>
          <div className={`text-3xl font-bold ${getDiversificationColor(analytics.diversification.score)}`}>
            {analytics.diversification.score}/100
          </div>
          <p className="text-sm text-gray-600 mt-1">{analytics.diversification.rating}</p>
          <div className="mt-3 h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              className={`h-full ${
                analytics.diversification.score >= 80
                  ? 'bg-emerald-600'
                  : analytics.diversification.score >= 60
                  ? 'bg-yellow-500'
                  : 'bg-red-600'
              }`}
              style={{ width: `${analytics.diversification.score}%` }}
            />
          </div>
        </div>

        {/* Risk Exposure */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-2">
            <Activity className="h-5 w-5 text-dominion-gold" />
            <span className="text-xs font-medium text-gray-500 uppercase">Risk Level</span>
          </div>
          <div className={`text-3xl font-bold ${getRiskColor(analytics.risk.overall_score)}`}>
            {analytics.risk.overall_score}/10
          </div>
          <p className="text-sm text-gray-600 mt-1">{analytics.risk.overall_rating}</p>
          <p className="text-xs text-gray-500 mt-2">
            {analytics.risk.high_risk_holdings || 0} high-risk holdings
          </p>
        </div>

        {/* Volatility */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-2">
            <TrendingUp className="h-5 w-5 text-dominion-gold" />
            <span className="text-xs font-medium text-gray-500 uppercase">Volatility</span>
          </div>
          <div className="text-3xl font-bold text-gray-900">
            {analytics.risk.volatility_30d?.toFixed(1)}%
          </div>
          <p className="text-sm text-gray-600 mt-1">30-Day Standard Deviation</p>
          <p className="text-xs text-gray-500 mt-2">
            vs Market: {((analytics.risk.volatility_30d || 0) - 12.5).toFixed(1)}%
          </p>
        </div>

        {/* Max Drawdown */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-2">
            <AlertTriangle className="h-5 w-5 text-dominion-gold" />
            <span className="text-xs font-medium text-gray-500 uppercase">Max Drawdown</span>
          </div>
          <div className="text-3xl font-bold text-red-600">
            {analytics.risk.max_drawdown_30d?.toFixed(1)}%
          </div>
          <p className="text-sm text-gray-600 mt-1">Largest 30-Day Drop</p>
          <p className="text-xs text-gray-500 mt-2">
            Best Day: +{analytics.risk.best_day_30d?.toFixed(1)}%
          </p>
        </div>
      </div>

      {/* Historical Performance Chart */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-gray-900">Historical Performance</h3>
          <div className="flex gap-2">
            {['30D', '90D', '1Y', 'MAX'].map((timeframe) => (
              <button
                key={timeframe}
                onClick={() => setSelectedTimeframe(timeframe)}
                className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
                  selectedTimeframe === timeframe
                    ? 'bg-dominion-gold text-gray-900'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {timeframe}
              </button>
            ))}
          </div>
        </div>

        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={performanceData}>
              <XAxis dataKey="date" stroke="#6B7280" style={{ fontSize: '12px' }} />
              <YAxis stroke="#6B7280" style={{ fontSize: '12px' }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #E5E7EB',
                  borderRadius: '8px',
                  padding: '12px'
                }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="portfolio"
                stroke="#F5C542"
                strokeWidth={3}
                name="Your Portfolio"
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="sp500"
                stroke="#6B7280"
                strokeWidth={2}
                name="S&P 500"
                dot={false}
                strokeDasharray="5 5"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="mt-4 p-4 bg-blue-50 rounded-lg">
          <p className="text-sm text-blue-900">
            📈 Your portfolio has outperformed the S&P 500 by{' '}
            <span className="font-semibold">+5.2%</span> over the last 30 days.
          </p>
        </div>
      </div>

      {/* Sector Concentration Warning */}
      {Object.values(analytics.sector_allocation).some((s: any) => s.percentage > 50) && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 flex items-start">
          <AlertTriangle className="h-5 w-5 text-yellow-600 mr-3 mt-0.5 flex-shrink-0" />
          <div>
            <h4 className="font-semibold text-yellow-900 mb-1">High Sector Concentration</h4>
            <p className="text-sm text-yellow-800">
              Your portfolio is heavily concentrated in{' '}
              {Object.entries(analytics.sector_allocation).find(([_, s]: any) => s.percentage > 50)?.[0]}.
              This increases sector-specific risk. Consider exploring other sectors for better diversification.
            </p>
          </div>
        </div>
      )}

      {/* Risk Distribution */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Distribution</h3>
        <div className="space-y-3">
          <div>
            <div className="flex items-center justify-between mb-1">
              <span className="text-sm text-gray-700">High Risk</span>
              <span className="text-sm font-medium text-gray-900">
                {analytics.risk.high_risk_holdings || 0} holdings
              </span>
            </div>
            <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-red-600"
                style={{
                  width: `${((analytics.risk.high_risk_holdings || 0) / analytics.diversification.stock_count) * 100}%`
                }}
              />
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-1">
              <span className="text-sm text-gray-700">Medium Risk</span>
              <span className="text-sm font-medium text-gray-900">
                {analytics.risk.medium_risk_holdings || 0} holdings
              </span>
            </div>
            <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-yellow-500"
                style={{
                  width: `${((analytics.risk.medium_risk_holdings || 0) / analytics.diversification.stock_count) * 100}%`
                }}
              />
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-1">
              <span className="text-sm text-gray-700">Low Risk</span>
              <span className="text-sm font-medium text-gray-900">
                {analytics.risk.low_risk_holdings || 0} holdings
              </span>
            </div>
            <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-emerald-600"
                style={{
                  width: `${((analytics.risk.low_risk_holdings || 0) / analytics.diversification.stock_count) * 100}%`
                }}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
