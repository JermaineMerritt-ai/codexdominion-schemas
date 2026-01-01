/**
 * Holdings Table Component
 * Sortable table showing all stock positions
 */

"use client"

import { useState } from 'react'
import { ChevronUp, ChevronDown, Edit, Trash2 } from 'lucide-react'

interface Holding {
  id: string
  symbol: string
  company_name: string
  shares: number
  avg_cost: number
  current_price: number
  total_value: number
  gain_loss: number
  gain_loss_percent: number
  sector: string
}

interface HoldingsTableProps {
  holdings: Holding[]
  onEditHolding: (holding: Holding) => void
  onRemoveHolding: (holding: Holding) => void
  selectedSector: string | null
}

type SortField = 'symbol' | 'shares' | 'total_value' | 'gain_loss_percent'
type SortDirection = 'asc' | 'desc'

export default function HoldingsTable({ holdings, onEditHolding, onRemoveHolding, selectedSector }: HoldingsTableProps) {
  const [sortField, setSortField] = useState<SortField>('total_value')
  const [sortDirection, setSortDirection] = useState<SortDirection>('desc')

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

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDirection('desc')
    }
  }

  const sortedHoldings = [...holdings].sort((a, b) => {
    let aValue = a[sortField]
    let bValue = b[sortField]

    if (sortDirection === 'asc') {
      return aValue > bValue ? 1 : -1
    } else {
      return aValue < bValue ? 1 : -1
    }
  })

  const SortIcon = ({ field }: { field: SortField }) => {
    if (sortField !== field) return <ChevronUp className="h-4 w-4 text-gray-300" />
    return sortDirection === 'asc' ? (
      <ChevronUp className="h-4 w-4 text-dominion-gold" />
    ) : (
      <ChevronDown className="h-4 w-4 text-dominion-gold" />
    )
  }

  if (holdings.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
        <div className="text-6xl mb-4">🎯</div>
        <h3 className="text-xl font-bold text-gray-900 mb-2">Start Building Your Portfolio</h3>
        <p className="text-gray-600 mb-4">Add your first holding to begin tracking your investments.</p>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      <div className="p-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">Holdings</h3>
        {selectedSector && (
          <p className="text-sm text-gray-600 mt-1">
            Filtered by sector: <span className="font-semibold">{selectedSector}</span>
          </p>
        )}
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th
                className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                onClick={() => handleSort('symbol')}
              >
                <div className="flex items-center">
                  Symbol
                  <SortIcon field="symbol" />
                </div>
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider hidden md:table-cell">
                Company
              </th>
              <th
                className="px-4 py-3 text-right text-xs font-medium text-gray-700 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                onClick={() => handleSort('shares')}
              >
                <div className="flex items-center justify-end">
                  Shares
                  <SortIcon field="shares" />
                </div>
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-700 uppercase tracking-wider hidden lg:table-cell">
                Avg Cost
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-700 uppercase tracking-wider hidden lg:table-cell">
                Current
              </th>
              <th
                className="px-4 py-3 text-right text-xs font-medium text-gray-700 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                onClick={() => handleSort('total_value')}
              >
                <div className="flex items-center justify-end">
                  Value
                  <SortIcon field="total_value" />
                </div>
              </th>
              <th
                className="px-4 py-3 text-right text-xs font-medium text-gray-700 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                onClick={() => handleSort('gain_loss_percent')}
              >
                <div className="flex items-center justify-end">
                  Gain/Loss
                  <SortIcon field="gain_loss_percent" />
                </div>
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-700 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {sortedHoldings.map((holding) => {
              const isPositive = holding.gain_loss >= 0
              return (
                <tr key={holding.id} className="hover:bg-gray-50 cursor-pointer">
                  <td className="px-4 py-4">
                    <div className="font-semibold text-gray-900">{holding.symbol}</div>
                    <div className="text-xs text-gray-500 md:hidden">{holding.company_name}</div>
                  </td>
                  <td className="px-4 py-4 text-gray-700 hidden md:table-cell">
                    {holding.company_name}
                  </td>
                  <td className="px-4 py-4 text-right text-gray-700">
                    {holding.shares.toLocaleString()}
                  </td>
                  <td className="px-4 py-4 text-right text-gray-700 hidden lg:table-cell">
                    {formatCurrency(holding.avg_cost)}
                  </td>
                  <td className="px-4 py-4 text-right text-gray-700 hidden lg:table-cell">
                    {formatCurrency(holding.current_price)}
                  </td>
                  <td className="px-4 py-4 text-right font-semibold text-gray-900">
                    {formatCurrency(holding.total_value)}
                  </td>
                  <td className="px-4 py-4 text-right">
                    <div className={`font-semibold ${isPositive ? 'text-emerald-600' : 'text-red-600'}`}>
                      {formatCurrency(holding.gain_loss)}
                    </div>
                    <div className={`text-sm ${isPositive ? 'text-emerald-600' : 'text-red-600'}`}>
                      {formatPercent(holding.gain_loss_percent)}
                    </div>
                  </td>
                  <td className="px-4 py-4 text-right">
                    <div className="flex items-center justify-end gap-2">
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          onEditHolding(holding)
                        }}
                        className="p-1 text-gray-600 hover:text-dominion-gold transition-colors"
                        title="Edit holding"
                      >
                        <Edit className="h-4 w-4" />
                      </button>
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          onRemoveHolding(holding)
                        }}
                        className="p-1 text-gray-600 hover:text-red-600 transition-colors"
                        title="Remove holding"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
