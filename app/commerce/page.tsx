import Link from 'next/link'

export default function CommercePage() {
  const products = [
    { id: 'advent-2025', name: 'Advent Devotional 2025', price: '$9.99', status: 'active', sales: 12 },
    { id: 'kids-bible', name: 'Kids Bible Story Pack', price: '$14.99', status: 'active', sales: 87 },
    { id: 'wedding-pack', name: 'Wedding Printables Bundle', price: '$29.99', status: 'active', sales: 45 },
    { id: 'homeschool', name: 'Homeschool Starter Kit', price: '$19.99', status: 'active', sales: 63 },
  ]

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-serif text-ceremonial mb-2">
          🛍️ Commerce Center
        </h1>
        <p className="text-proclamation">
          Faith-Empire Product Catalog & E-Commerce Management
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="codex-panel">
          <div className="text-2xl font-bold text-codex-gold">127</div>
          <div className="text-xs text-codex-parchment/60">Total Products</div>
        </div>
        <div className="codex-panel">
          <div className="text-2xl font-bold text-green-400">$3,456</div>
          <div className="text-xs text-codex-parchment/60">This Month</div>
        </div>
        <div className="codex-panel">
          <div className="text-2xl font-bold text-blue-400">892</div>
          <div className="text-xs text-codex-parchment/60">Orders</div>
        </div>
        <div className="codex-panel">
          <div className="text-2xl font-bold text-purple-400">4.8★</div>
          <div className="text-xs text-codex-parchment/60">Avg Rating</div>
        </div>
      </div>

      {/* Products List */}
      <div className="codex-card">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-serif text-codex-gold">
            Recent Products
          </h2>
          <button className="codex-button">
            ➕ Add New Product
          </button>
        </div>

        <div className="space-y-4">
          {products.map((product) => (
            <Link key={product.id} href={`/commerce/products/${product.id}`}>
              <div className="codex-panel hover:bg-codex-gold/10 transition-all cursor-pointer">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold">{product.name}</h3>
                    <p className="text-sm text-codex-parchment/60">{product.sales} sales</p>
                  </div>
                  <div className="text-right">
                    <div className="text-xl font-bold text-codex-gold">{product.price}</div>
                    <span className="codex-badge-success">{product.status}</span>
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}
