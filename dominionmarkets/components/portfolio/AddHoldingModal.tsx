/**
 * Add Holding Modal
 * Form to add new stock position to portfolio
 */

"use client"

import { useState } from 'react'
import { X, Search } from 'lucide-react'

interface AddHoldingModalProps {
  portfolioId: string
  onClose: () => void
}

export default function AddHoldingModal({ portfolioId, onClose }: AddHoldingModalProps) {
  const [formData, setFormData] = useState({
    symbol: '',
    shares: '',
    avgCost: '',
    purchaseDate: '',
    notes: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [searchResults, setSearchResults] = useState<any[]>([])

  const handleSymbolSearch = async (query: string) => {
    if (query.length < 1) {
      setSearchResults([])
      return
    }

    try {
      const response = await fetch(`/api/stocks/search?q=${query}`)
      const data = await response.json()
      setSearchResults(data.results || [])
    } catch (error) {
      console.error('Search failed:', error)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    if (!formData.symbol || !formData.shares) {
      setError('Symbol and shares are required')
      return
    }

    if (parseFloat(formData.shares) <= 0) {
      setError('Shares must be greater than 0')
      return
    }

    try {
      setLoading(true)
      const response = await fetch(`/api/portfolio/${portfolioId}/holdings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          symbol: formData.symbol.toUpperCase(),
          shares: parseFloat(formData.shares),
          avg_cost: formData.avgCost ? parseFloat(formData.avgCost) : null,
          purchase_date: formData.purchaseDate || null,
          notes: formData.notes || null
        })
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.error || 'Failed to add holding')
      }

      onClose()
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-xl font-bold text-gray-900">Add Holding</h2>
          <button
            onClick={onClose}
            className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-800">
              {error}
            </div>
          )}

          {/* Stock Symbol */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Stock Symbol *
            </label>
            <div className="relative">
              <input
                type="text"
                value={formData.symbol}
                onChange={(e) => {
                  setFormData({ ...formData, symbol: e.target.value.toUpperCase() })
                  handleSymbolSearch(e.target.value)
                }}
                placeholder="e.g., AAPL"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-dominion-gold focus:border-transparent uppercase"
                required
              />
              <Search className="absolute right-3 top-2.5 h-5 w-5 text-gray-400" />
            </div>

            {/* Search Results Dropdown */}
            {searchResults.length > 0 && (
              <div className="mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-48 overflow-y-auto">
                {searchResults.map((result) => (
                  <button
                    key={result.symbol}
                    type="button"
                    onClick={() => {
                      setFormData({ ...formData, symbol: result.symbol })
                      setSearchResults([])
                    }}
                    className="w-full px-3 py-2 text-left hover:bg-gray-50 transition-colors"
                  >
                    <div className="font-semibold text-gray-900">{result.symbol}</div>
                    <div className="text-sm text-gray-600">{result.name}</div>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Number of Shares */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Number of Shares *
            </label>
            <input
              type="number"
              step="0.0001"
              value={formData.shares}
              onChange={(e) => setFormData({ ...formData, shares: e.target.value })}
              placeholder="0.00"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-dominion-gold focus:border-transparent"
              required
            />
          </div>

          {/* Average Cost per Share */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Average Cost per Share (optional)
            </label>
            <div className="relative">
              <span className="absolute left-3 top-2.5 text-gray-500">$</span>
              <input
                type="number"
                step="0.01"
                value={formData.avgCost}
                onChange={(e) => setFormData({ ...formData, avgCost: e.target.value })}
                placeholder="0.00"
                className="w-full pl-7 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-dominion-gold focus:border-transparent"
              />
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Used to calculate gain/loss. Leave blank if unknown.
            </p>
          </div>

          {/* Purchase Date */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Purchase Date (optional)
            </label>
            <input
              type="date"
              value={formData.purchaseDate}
              onChange={(e) => setFormData({ ...formData, purchaseDate: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-dominion-gold focus:border-transparent"
            />
          </div>

          {/* Notes */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Notes (optional)
            </label>
            <textarea
              value={formData.notes}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
              placeholder="Add any notes about this investment..."
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-dominion-gold focus:border-transparent resize-none"
            />
          </div>

          {/* Actions */}
          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg font-semibold hover:bg-gray-200 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 px-4 py-2 bg-dominion-gold text-gray-900 rounded-lg font-semibold hover:bg-yellow-500 transition-colors disabled:opacity-50"
            >
              {loading ? 'Adding...' : 'Add to Portfolio'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
