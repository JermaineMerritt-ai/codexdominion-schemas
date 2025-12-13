export default function ProductDetailPage({ params }: { params: { id: string } }) {
  const product = {
    id: params.id,
    name: 'Advent Devotional 2025',
    price: '$9.99',
    description: '25 daily readings for the Advent season with scripture, reflections, prayers, and practical applications.',
    status: 'active',
    created: 'Dec 12, 2025',
    sales: 12,
    revenue: '$119.88',
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-serif text-ceremonial mb-2">
          {product.name}
        </h1>
        <p className="text-proclamation">
          Product ID: {product.id}
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Product Details */}
        <div className="lg:col-span-2 codex-card">
          <h2 className="text-xl font-serif text-codex-gold mb-4">
            Product Details
          </h2>
          <div className="space-y-4">
            <div>
              <label className="text-sm text-codex-parchment/60">Description</label>
              <p className="mt-1">{product.description}</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm text-codex-parchment/60">Price</label>
                <p className="text-2xl font-bold text-codex-gold mt-1">{product.price}</p>
              </div>
              <div>
                <label className="text-sm text-codex-parchment/60">Status</label>
                <p className="mt-1">
                  <span className="codex-badge-success">{product.status}</span>
                </p>
              </div>
            </div>
            <div>
              <label className="text-sm text-codex-parchment/60">Created</label>
              <p className="mt-1">{product.created}</p>
            </div>
          </div>
        </div>

        {/* Sales Stats */}
        <div className="codex-card">
          <h2 className="text-xl font-serif text-codex-gold mb-4">
            Sales Performance
          </h2>
          <div className="space-y-4">
            <div className="codex-panel">
              <div className="text-2xl font-bold text-green-400">{product.sales}</div>
              <div className="text-xs text-codex-parchment/60">Total Sales</div>
            </div>
            <div className="codex-panel">
              <div className="text-2xl font-bold text-codex-gold">{product.revenue}</div>
              <div className="text-xs text-codex-parchment/60">Total Revenue</div>
            </div>
          </div>

          <div className="mt-6 space-y-2">
            <button className="codex-button w-full">✏️ Edit Product</button>
            <button className="codex-button w-full">📤 Export Data</button>
          </div>
        </div>
      </div>
    </div>
  )
}
