/**
 * Allocation Breakdown Component
 * Interactive pie chart showing sector diversification
 */

"use client"

import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface AllocationBreakdownProps {
  sectorAllocation: Record<string, { percentage: number; value: number; holdings: number }>
  totalValue: number
  onSectorClick: (sector: string) => void
  selectedSector: string | null
}

const SECTOR_COLORS: Record<string, string> = {
  'Technology': '#3B82F6',
  'Healthcare': '#10B981',
  'Finance': '#F59E0B',
  'Consumer Discretionary': '#8B5CF6',
  'Consumer Staples': '#EC4899',
  'Energy': '#EF4444',
  'Industrials': '#6366F1',
  'Materials': '#14B8A6',
  'Real Estate': '#F97316',
  'Utilities': '#06B6D4',
  'Other': '#6B7280'
}

export default function AllocationBreakdown({ 
  sectorAllocation, 
  totalValue, 
  onSectorClick, 
  selectedSector 
}: AllocationBreakdownProps) {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value)
  }

  // Convert allocation object to array for chart
  const chartData = Object.entries(sectorAllocation).map(([sector, data]) => ({
    name: sector,
    value: data.percentage,
    displayValue: data.value,
    holdings: data.holdings,
    color: SECTOR_COLORS[sector] || SECTOR_COLORS['Other']
  }))

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload
      return (
        <div className="bg-white p-3 rounded-lg shadow-lg border border-gray-200">
          <p className="font-semibold text-gray-900">{data.name}</p>
          <p className="text-sm text-gray-600">
            {formatCurrency(data.displayValue)} ({data.value.toFixed(1)}%)
          </p>
          <p className="text-xs text-gray-500">{data.holdings} holdings</p>
        </div>
      )
    }
    return null
  }

  if (chartData.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Allocation Breakdown</h3>
        <div className="text-center py-8 text-gray-500">
          <p>Add holdings to see allocation</p>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Allocation Breakdown</h3>

      {/* Pie Chart */}
      <div className="h-64 mb-4">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              paddingAngle={2}
              dataKey="value"
              onClick={(data) => onSectorClick(data.name)}
              cursor="pointer"
            >
              {chartData.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={entry.color}
                  opacity={selectedSector === null || selectedSector === entry.name ? 1 : 0.3}
                  stroke={selectedSector === entry.name ? '#F5C542' : 'none'}
                  strokeWidth={selectedSector === entry.name ? 3 : 0}
                />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Legend with click interaction */}
      <div className="space-y-2">
        {chartData.map((sector) => (
          <button
            key={sector.name}
            onClick={() => onSectorClick(sector.name)}
            className={`w-full flex items-center justify-between p-2 rounded-lg transition-colors ${
              selectedSector === null || selectedSector === sector.name
                ? 'bg-gray-50 hover:bg-gray-100'
                : 'bg-gray-50 opacity-50 hover:opacity-75'
            }`}
          >
            <div className="flex items-center">
              <div
                className="w-4 h-4 rounded mr-2"
                style={{ backgroundColor: sector.color }}
              ></div>
              <span className="text-sm font-medium text-gray-900">{sector.name}</span>
            </div>
            <div className="text-right">
              <div className="text-sm font-semibold text-gray-900">
                {sector.value.toFixed(1)}%
              </div>
              <div className="text-xs text-gray-500">
                {formatCurrency(sector.displayValue)}
              </div>
            </div>
          </button>
        ))}
      </div>

      {/* Identity-aware insight */}
      <div className="mt-4 p-3 bg-blue-50 rounded-lg">
        <p className="text-xs text-blue-900">
          💡 Your portfolio spans {chartData.length} {chartData.length === 1 ? 'sector' : 'sectors'}, 
          showing {chartData.length >= 4 ? 'good' : 'moderate'} diversification across industries.
        </p>
      </div>

      {selectedSector && (
        <div className="mt-4">
          <button
            onClick={() => onSectorClick(selectedSector)}
            className="text-sm text-dominion-gold hover:text-yellow-600 font-medium"
          >
            ← Clear filter
          </button>
        </div>
      )}
    </div>
  )
}
