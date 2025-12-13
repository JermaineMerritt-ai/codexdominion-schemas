'use client'

import ProductList from './components/ProductList'
import CollectionBuilder from './components/CollectionBuilder'
import PricingPanel from './components/PricingPanel'
import FunnelBuilder from './components/FunnelBuilder'
import StoreSettings from './components/StoreSettings'

export default function StoreBuilderPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-serif text-ceremonial mb-2">
          🏪 Store Builder
        </h1>
        <p className="text-proclamation">
          Design your e-commerce experience
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Products & Collections */}
        <div className="lg:col-span-2 space-y-6">
          <ProductList />
          <CollectionBuilder />
          <FunnelBuilder />
        </div>

        {/* Right Column - Pricing & Settings */}
        <div className="space-y-6">
          <PricingPanel />
          <StoreSettings />
        </div>
      </div>
    </div>
  )
}
