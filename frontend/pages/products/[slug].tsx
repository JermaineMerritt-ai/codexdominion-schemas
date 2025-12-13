import { useRouter } from 'next/router';
import Link from 'next/link';
import productsData from '../../data/products.json';

export default function ProductDetail() {
  const router = useRouter();
  const { slug } = router.query;

  // Combine all products
  const allProducts = [
    ...productsData.devotionals,
    ...productsData.journals,
    ...productsData.bundles
  ];

  // Find the product by slug
  const product = allProducts.find(p => p.slug === slug);

  // Loading state
  if (!router.isReady || !product) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-blue-900 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4 animate-pulse">🔥</div>
          <p className="text-xl text-purple-200">Loading product...</p>
        </div>
      </div>
    );
  }

  const displayPrice = product.salePrice || product.price;
  const originalPrice = product.salePrice ? product.price : null;
  const savings = originalPrice ? (originalPrice - displayPrice).toFixed(2) : null;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-blue-900">
      {/* Navigation */}
      <nav className="container mx-auto px-6 py-4 border-b-2 border-purple-800/50">
        <div className="flex justify-between items-center">
          <Link href="/" className="flex items-center space-x-2">
            <span className="text-3xl">🔥</span>
            <span className="text-2xl font-bold text-gold-300">Codex Dominion</span>
          </Link>
          <div className="flex space-x-6">
            <Link href="/products" className="text-purple-200 hover:text-gold-300 transition-colors">
              ← Back to Shop
            </Link>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-6 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12">
            {/* Product Image */}
            <div>
              <div className="bg-gradient-to-br from-purple-800 to-blue-800 rounded-3xl h-96 flex items-center justify-center text-9xl shadow-2xl border-4 border-gold-500/30">
                {product.category === 'devotional' && '📖'}
                {product.category === 'journal' && '📝'}
                {product.category === 'bundle' && '📦'}
              </div>

              {/* Badges */}
              <div className="flex gap-3 mt-6">
                {product.bestseller && (
                  <span className="bg-red-500 text-white px-4 py-2 rounded-full text-sm font-bold">
                    ⭐ BESTSELLER
                  </span>
                )}
                {product.featured && (
                  <span className="bg-gold-500 text-gray-900 px-4 py-2 rounded-full text-sm font-bold">
                    ✨ FEATURED
                  </span>
                )}
                {product.type === 'digital' && (
                  <span className="bg-blue-600 text-white px-4 py-2 rounded-full text-sm font-bold">
                    ⚡ INSTANT ACCESS
                  </span>
                )}
              </div>
            </div>

            {/* Product Info */}
            <div>
              <div className="mb-4">
                <span className="text-purple-300 uppercase text-sm font-bold bg-purple-800/50 px-3 py-1 rounded">
                  {product.category}
                </span>
              </div>

              <h1 className="text-4xl md:text-5xl font-bold mb-4 text-gold-300 leading-tight">
                {product.title}
              </h1>

              {/* Rating */}
              <div className="flex items-center mb-6">
                <div className="text-gold-400 text-xl">
                  {'★'.repeat(Math.floor(product.rating))}
                  {product.rating % 1 !== 0 && '⯨'}
                  {'☆'.repeat(5 - Math.ceil(product.rating))}
                </div>
                <span className="text-purple-300 ml-3">
                  {product.rating} ({product.reviewCount} reviews)
                </span>
              </div>

              <p className="text-xl text-purple-200 mb-8 leading-relaxed">
                {product.longDescription || product.description}
              </p>

              {/* Price */}
              <div className="bg-gray-800/60 rounded-2xl p-6 mb-8 border-2 border-gold-500/30">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <div className="flex items-center space-x-4">
                      <span className="text-5xl font-bold text-gold-300">
                        ${displayPrice}
                      </span>
                      {originalPrice && (
                        <span className="text-2xl text-gray-400 line-through">
                          ${originalPrice}
                        </span>
                      )}
                    </div>
                    {savings && (
                      <p className="text-green-400 font-bold mt-2">
                        Save ${savings}!
                      </p>
                    )}
                  </div>
                </div>

                {/* Buy Button */}
                <button className="w-full py-5 bg-gradient-to-r from-gold-500 to-amber-500 hover:from-gold-600 hover:to-amber-600 rounded-xl font-bold text-xl transition-all duration-300 shadow-2xl transform hover:scale-105">
                  🛒 Buy Now - Instant Access
                </button>

                <div className="flex items-center justify-center mt-4 text-purple-300 text-sm">
                  <span>🔒 Secure Checkout</span>
                  <span className="mx-2">•</span>
                  <span>💳 All Cards Accepted</span>
                  <span className="mx-2">•</span>
                  <span>✓ Money-Back Guarantee</span>
                </div>
              </div>

              {/* Features */}
              <div className="bg-gradient-to-br from-gray-800/80 to-purple-900/60 rounded-2xl p-6 border-2 border-purple-600/50">
                <h3 className="text-2xl font-bold text-gold-300 mb-4">✨ Features</h3>
                <ul className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {product.features.map((feature, idx) => (
                    <li key={idx} className="text-purple-200 flex items-start">
                      <span className="text-gold-400 mr-2">•</span>
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          {/* Additional Details */}
          <div className="mt-16 grid md:grid-cols-3 gap-6">
            <div className="bg-gray-800/60 rounded-xl p-6 border-2 border-purple-600/30 text-center">
              <div className="text-4xl mb-3">⚡</div>
              <h4 className="text-lg font-bold text-white mb-2">Instant Delivery</h4>
              <p className="text-purple-200 text-sm">Access your purchase immediately after checkout</p>
            </div>
            <div className="bg-gray-800/60 rounded-xl p-6 border-2 border-purple-600/30 text-center">
              <div className="text-4xl mb-3">🔄</div>
              <h4 className="text-lg font-bold text-white mb-2">30-Day Guarantee</h4>
              <p className="text-purple-200 text-sm">Not satisfied? Get a full refund within 30 days</p>
            </div>
            <div className="bg-gray-800/60 rounded-xl p-6 border-2 border-purple-600/30 text-center">
              <div className="text-4xl mb-3">💼</div>
              <h4 className="text-lg font-bold text-white mb-2">Lifetime Access</h4>
              <p className="text-purple-200 text-sm">Download anytime, keep forever with free updates</p>
            </div>
          </div>

          {/* Related Products */}
          <div className="mt-16">
            <h2 className="text-3xl font-bold text-center mb-8 text-gold-300">You May Also Like</h2>
            <div className="grid md:grid-cols-3 gap-6">
              {allProducts
                .filter(p => p.slug !== slug && p.category === product.category)
                .slice(0, 3)
                .map(relatedProduct => (
                  <Link key={relatedProduct.id} href={`/products/${relatedProduct.slug}`}>
                    <div className="bg-gradient-to-br from-gray-800/90 to-purple-900/80 rounded-xl p-6 hover:scale-105 transition-all duration-300 shadow-xl border-2 border-purple-600/50 hover:border-gold-400/80 cursor-pointer">
                      <div className="text-5xl mb-4 text-center">
                        {relatedProduct.category === 'devotional' && '📖'}
                        {relatedProduct.category === 'journal' && '📝'}
                        {relatedProduct.category === 'bundle' && '📦'}
                      </div>
                      <h3 className="text-lg font-bold text-white mb-2 line-clamp-2">{relatedProduct.title}</h3>
                      <p className="text-purple-200 text-sm mb-4 line-clamp-2">{relatedProduct.description}</p>
                      <div className="flex items-center justify-between">
                        <span className="text-xl font-bold text-gold-300">
                          ${relatedProduct.salePrice || relatedProduct.price}
                        </span>
                        <span className="text-gold-400 text-sm">
                          ★ {relatedProduct.rating}
                        </span>
                      </div>
                    </div>
                  </Link>
                ))}
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="container mx-auto px-6 py-12 border-t-2 border-purple-800/50 mt-16">
        <div className="text-center text-purple-300 text-sm">
          <p>© 2024 Codex Dominion. All rights reserved.</p>
          <p className="mt-2">🔥 Empowering Faith-Driven Entrepreneurs</p>
        </div>
      </footer>
    </div>
  );
}
