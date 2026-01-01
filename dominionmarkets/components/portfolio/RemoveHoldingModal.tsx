/**
 * Remove Holding Modal
 * Confirmation dialog for deleting a holding
 */

"use client"

import { useState } from 'react'
import { X, AlertTriangle } from 'lucide-react'

interface RemoveHoldingModalProps {
  portfolioId: string
  holdingId: string
  symbol: string
  shares: number
  currentValue: number
  onClose: () => void
}

export default function RemoveHoldingModal({
  portfolioId,
  holdingId,
  symbol,
  shares,
  currentValue,
  onClose
}: RemoveHoldingModalProps) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleRemove = async () => {
    try {
      setLoading(true)
      const response = await fetch(`/api/portfolio/${portfolioId}/holdings/${holdingId}`, {
        method: 'DELETE'
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.error || 'Failed to remove holding')
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
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-xl font-bold text-gray-900">Remove Holding</h2>
          <button
            onClick={onClose}
            className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-800">
              {error}
            </div>
          )}

          {/* Warning */}
          <div className="flex items-start mb-4 p-4 bg-red-50 rounded-lg">
            <AlertTriangle className="h-5 w-5 text-red-600 mr-3 mt-0.5 flex-shrink-0" />
            <div className="text-sm text-red-800">
              <p className="font-semibold mb-1">This action cannot be undone</p>
              <p>You are about to remove this holding from your portfolio. All historical data will be permanently deleted.</p>
            </div>
          </div>

          {/* Holding Details */}
          <div className="bg-gray-50 rounded-lg p-4 space-y-2">
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Symbol:</span>
              <span className="text-sm font-semibold text-gray-900">{symbol}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Shares:</span>
              <span className="text-sm font-semibold text-gray-900">{shares.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Current Value:</span>
              <span className="text-sm font-semibold text-gray-900">
                ${currentValue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </span>
            </div>
          </div>

          {/* Confirmation Text */}
          <p className="mt-4 text-sm text-gray-600">
            Are you sure you want to remove <strong>{symbol}</strong> from your portfolio?
          </p>
        </div>

        {/* Actions */}
        <div className="flex gap-3 p-6 bg-gray-50 rounded-b-lg">
          <button
            type="button"
            onClick={onClose}
            className="flex-1 px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handleRemove}
            disabled={loading}
            className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg font-semibold hover:bg-red-700 transition-colors disabled:opacity-50"
          >
            {loading ? 'Removing...' : 'Remove Holding'}
          </button>
        </div>
      </div>
    </div>
  )
}
