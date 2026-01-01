/**
 * DominionMarkets Portfolio Page
 * ===============================
 * Main portfolio view with Overview, Holdings, Allocation, Analytics, and AI Summary
 * 
 * Last Updated: December 24, 2025
 */

"use client"

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import PortfolioOverview from '@/components/portfolio/PortfolioOverview'
import HoldingsTable from '@/components/portfolio/HoldingsTable'
import AllocationBreakdown from '@/components/portfolio/AllocationBreakdown'
import PremiumAnalytics from '@/components/portfolio/PremiumAnalytics'
import AIPortfolioSummary from '@/components/portfolio/AIPortfolioSummary'
import AddHoldingModal from '@/components/portfolio/AddHoldingModal'
import EditHoldingModal from '@/components/portfolio/EditHoldingModal'
import RemoveHoldingModal from '@/components/portfolio/RemoveHoldingModal'
import { fetchPortfolio, refreshPrices } from '@/lib/api/portfolio'

interface Portfolio {
  id: string
  name: string
  total_value: number
  daily_change: number
  daily_change_percent: number
  all_time_return: number
  all_time_return_percent: number
}

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

interface Analytics {
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
  }
  sector_allocation: Record<string, { percentage: number; value: number; holdings: number }>
}

export default function PortfolioPage({ params }: { params: { id: string } }) {
  const router = useRouter()
  const [loading, setLoading] = useState(true)
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null)
  const [holdings, setHoldings] = useState<Holding[]>([])
  const [analytics, setAnalytics] = useState<Analytics | null>(null)
  const [userTier, setUserTier] = useState('free') // 'free', 'premium', 'pro'
  
  // Modal states
  const [showAddModal, setShowAddModal] = useState(false)
  const [showEditModal, setShowEditModal] = useState(false)
  const [showRemoveModal, setShowRemoveModal] = useState(false)
  const [selectedHolding, setSelectedHolding] = useState<Holding | null>(null)
  
  // Sector filter
  const [selectedSector, setSelectedSector] = useState<string | null>(null)

  useEffect(() => {
    loadPortfolio()
  }, [params.id])

  const loadPortfolio = async () => {
    try {
      setLoading(true)
      const data = await fetchPortfolio(params.id)
      setPortfolio({
        id: data.portfolio.id,
        name: data.portfolio.name,
        total_value: data.analytics?.total_value || 0,
        daily_change: data.analytics?.daily_change || 0,
        daily_change_percent: data.analytics?.daily_change_percent || 0,
        all_time_return: data.analytics?.total_gain_loss || 0,
        all_time_return_percent: data.analytics?.total_gain_loss_percent || 0
      })
      setHoldings(data.holdings || [])
      setAnalytics(data.analytics)
      
      // Get user tier from session/auth
      const tier = localStorage.getItem('dominion_tier') || 'free'
      setUserTier(tier)
    } catch (error) {
      console.error('Failed to load portfolio:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleRefresh = async () => {
    try {
      await refreshPrices(params.id)
      await loadPortfolio()
    } catch (error) {
      console.error('Failed to refresh prices:', error)
    }
  }

  const handleAddHolding = () => {
    setShowAddModal(true)
  }

  const handleEditHolding = (holding: Holding) => {
    setSelectedHolding(holding)
    setShowEditModal(true)
  }

  const handleRemoveHolding = (holding: Holding) => {
    setSelectedHolding(holding)
    setShowRemoveModal(true)
  }

  const handleSectorClick = (sector: string) => {
    setSelectedSector(selectedSector === sector ? null : sector)
  }

  const filteredHoldings = selectedSector
    ? holdings.filter(h => h.sector === selectedSector)
    : holdings

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-dominion-gold"></div>
      </div>
    )
  }

  if (!portfolio) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Portfolio Not Found</h2>
          <p className="text-gray-600 mb-4">The portfolio you're looking for doesn't exist.</p>
          <button
            onClick={() => router.push('/dashboard')}
            className="px-4 py-2 bg-dominion-gold text-gray-900 rounded-lg font-semibold hover:bg-yellow-500"
          >
            Return to Dashboard
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Portfolio Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">{portfolio.name}</h1>
        <p className="text-gray-600">
          {holdings.length} {holdings.length === 1 ? 'holding' : 'holdings'} across {analytics?.diversification.sector_count || 0} sectors
        </p>
      </div>

      {/* Portfolio Overview */}
      <PortfolioOverview
        portfolio={portfolio}
        onAddHolding={handleAddHolding}
        onRefresh={handleRefresh}
        userTier={userTier}
      />

      {/* Two-column layout for Holdings Table and Allocation */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
        {/* Holdings Table (2/3 width) */}
        <div className="lg:col-span-2">
          <HoldingsTable
            holdings={filteredHoldings}
            onEditHolding={handleEditHolding}
            onRemoveHolding={handleRemoveHolding}
            selectedSector={selectedSector}
          />
        </div>

        {/* Allocation Breakdown (1/3 width) */}
        <div className="lg:col-span-1">
          <AllocationBreakdown
            sectorAllocation={analytics?.sector_allocation || {}}
            totalValue={portfolio.total_value}
            onSectorClick={handleSectorClick}
            selectedSector={selectedSector}
          />
        </div>
      </div>

      {/* Premium Analytics */}
      {userTier !== 'free' ? (
        <PremiumAnalytics
          analytics={analytics}
          portfolioId={params.id}
        />
      ) : (
        <div className="mt-6 relative">
          {/* Blurred preview */}
          <div className="filter blur-sm pointer-events-none opacity-50">
            <PremiumAnalytics analytics={analytics} portfolioId={params.id} />
          </div>
          
          {/* Upgrade overlay */}
          <div className="absolute inset-0 flex items-center justify-center bg-gray-900 bg-opacity-10">
            <div className="bg-white rounded-lg shadow-xl p-8 max-w-md text-center">
              <div className="text-4xl mb-4">👑</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Unlock Advanced Analytics</h3>
              <p className="text-gray-600 mb-6">
                Get institutional-grade insights, risk metrics, and historical performance tracking for just $14.99/month.
              </p>
              <button
                onClick={() => router.push('/premium')}
                className="px-6 py-3 bg-dominion-gold text-gray-900 rounded-lg font-semibold hover:bg-yellow-500 transition-colors"
              >
                Upgrade to Premium
              </button>
            </div>
          </div>
        </div>
      )}

      {/* AI Portfolio Summary */}
      <AIPortfolioSummary
        portfolioId={params.id}
        identityType={userTier}
        userTier={userTier}
      />

      {/* Modals */}
      {showAddModal && (
        <AddHoldingModal
          portfolioId={params.id}
          onClose={() => {
            setShowAddModal(false)
            loadPortfolio()
          }}
        />
      )}

      {showEditModal && selectedHolding && (
        <EditHoldingModal
          portfolioId={params.id}
          holding={selectedHolding}
          onClose={() => {
            setShowEditModal(false)
            setSelectedHolding(null)
            loadPortfolio()
          }}
        />
      )}

      {showRemoveModal && selectedHolding && (
        <RemoveHoldingModal
          portfolioId={params.id}
          holding={selectedHolding}
          onClose={() => {
            setShowRemoveModal(false)
            setSelectedHolding(null)
            loadPortfolio()
          }}
        />
      )}
    </div>
  )
}
