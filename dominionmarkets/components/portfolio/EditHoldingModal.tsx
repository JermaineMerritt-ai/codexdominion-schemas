/**
 * Edit Holding Modal
 * Form to update shares and cost of existing holding
 */

"use client"

import { useState, useEffect } from 'react'
import { X } from 'lucide-react'

interface EditHoldingModalProps {
  portfolioId: string
  holdingId: string
  onClose: () => void
}

export default function EditHoldingModal({ portfolioId, holdingId, onClose }: EditHoldingModalProps) {
  const [formData, setFormData] = useState({
    symbol: '',
    shares: '',
    avgCost: '',
    notes: ''
  })
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadHolding()
  }, [holdingId])

  const loadHolding = async () => {
    try {
      const response = await fetch(`/api/portfolio/${portfolioId}/holdings/${holdingId}`)
      const data = await response.json()
      
      setFormData({
        symbol: data.symbol,
        shares: data.shares.toString(),
        avgCost: data.avg_cost ? data.avg_cost.toString() : '',
        notes: data.notes || ''
      })
    } catch (error) {
      console.error('Failed to load holding:', error)
      setError('Failed to load holding details')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    if (!formData.shares) {
      setError('Shares are required')
      return
    }

    if (parseFloat(formData.shares) <= 0) {
      setError('Shares must be greater than 0')
      return
    }

    try {
      setSaving(true)
      const response = await fetch(`/api/portfolio/${portfolioId}/holdings/${holdingId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          shares: parseFloat(formData.shares),
          avg_cost: formData.avgCost ? parseFloat(formData.avgCost) : null,
          notes: formData.notes || null
        })
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.error || 'Failed to update holding')
      }

      onClose()
    } catch (err: any) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg shadow-xl p-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-dominion-gold mx-auto"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h2 className="text-xl font-bold text-gray-900">Edit Holding</h2>
            <p className="text-sm text-gray-600 mt-1">{formData.symbol}</p>
          </div>
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

          {/* Info Box */}
          <div className="p-3 bg-blue-50 rounded-lg">
            <p className="text-xs text-blue-800">
              <strong>Tip:</strong> Updating shares or cost will recalculate your portfolio metrics automatically.
            </p>
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
              disabled={saving}
              className="flex-1 px-4 py-2 bg-dominion-gold text-gray-900 rounded-lg font-semibold hover:bg-yellow-500 transition-colors disabled:opacity-50"
            >
              {saving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
