'use client'

import { DashboardTile, StatusBadge } from '@/components'

interface Product {
  id: string
  name: string
  price: string
  stock: number
  status: 'active' | 'inactive'
}

export default function ProductList() {
  const products: Product[] = [
    { id: '1', name: 'Kids Bible Story Pack', price: '$12.99', stock: 999, status: 'active' },
    { id: '2', name: 'Wedding Planner Kit', price: '$19.99', stock: 845, status: 'active' },
    { id: '3', name: 'Homeschool Bundle', price: '$24.99', stock: 567, status: 'active' },
    { id: '4', name: 'Christmas Coloring Book', price: '$8.99', stock: 0, status: 'inactive' },
  ]

  return (
    <DashboardTile title="Products" icon="📦" action={{ label: "+ Add Product", onClick: () => {} }}>
      <div className="space-y-2">
        {products.map((product) => (
          <div key={product.id} className="codex-panel hover:bg-codex-gold/10 cursor-pointer flex items-center justify-between">
            <div className="flex-1">
              <div className="font-medium text-codex-parchment">{product.name}</div>
              <div className="text-sm text-codex-parchment/60">{product.price} • Stock: {product.stock}</div>
            </div>
            <div className="flex items-center gap-3">
              <StatusBadge status={product.status === 'active' ? 'success' : 'inactive'} />
              <button className="text-xs codex-button py-1 px-3">Edit</button>
            </div>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
