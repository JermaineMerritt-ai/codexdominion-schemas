'use client';

import Link from 'next/link';
import { useState } from 'react';
import productsData from '../data/products.json';

interface Product {
  id: string;
  title: string;
  slug: string;
  description: string;
  price: number;
  salePrice?: number | null;
  regularPrice?: number;
  category: string;
  imageUrl: string;
  tags: string[];
  bestseller: boolean;
  featured: boolean;
  rating: number;
  reviewCount: number;
}

function ProductsPage() {
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState<string>('');

  // Combine all products from different categories
  const allProducts: Product[] = [
    ...productsData.devotionals,
    ...productsData.journals,
    ...productsData.bundles
  ];

  // Filter products
  const filteredProducts = allProducts.filter(product => {
    const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory;
    const matchesSearch = product.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         product.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         product.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    return matchesCategory && matchesSearch;
  });

  const categories = [
    { id: 'all', name: 'All Products', icon: '🔥' },
    { id: 'devotional', name: 'Devotionals', icon: '📖' },
    { id: 'journal', name: 'Journals', icon: '📝' },
    { id: 'bundle', name: 'Bundles', icon: '📦' }
  ];

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
            <Link href="/products" className="text-gold-300 font-bold">
              Shop
            </Link>
            <Link href="/about" className="text-purple-200 hover:text-gold-300 transition-colors">
              About
            </Link>
            <Link href="/contact" className="text-purple-200 hover:text-gold-300 transition-colors">
              Contact
            </Link>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-6 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-gold-300 via-yellow-300 to-gold-400 bg-clip-text text-transparent">
            Faith-Driven Resources
          </h1>
          <p className="text-xl text-purple-200 max-w-2xl mx-auto">
            Premium devotionals, journals, and bundles designed for Christian entrepreneurs and ministry leaders.
          </p>
        </div>

        {/* Search Bar */}
        <div className="max-w-2xl mx-auto mb-8">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search products by name, description, or tags..."
            className="w-full px-6 py-4 rounded-xl text-gray-900 font-semibold focus:outline-none focus:ring-4 focus:ring-gold-400"
          />
        </div>

        {/* Category Filter */}
        <div className="flex flex-wrap justify-center gap-4 mb-12">
          {categories.map(category => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`px-6 py-3 rounded-xl font-bold transition-all duration-300 ${
                selectedCategory === category.id
                  ? 'bg-gradient-to-r from-gold-500 to-amber-500 text-white shadow-lg scale-105'
                  : 'bg-gray-800/60 text-purple-200 hover:bg-gray-700/80 border-2 border-purple-600/30'
              }`}
            >
              {category.icon} {category.name}
            </button>
          ))}
        </div>

        {/* Products Grid */}
        {filteredProducts.length === 0 ? (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">🔍</div>
            <p className="text-xl text-purple-200">No products found matching your search.</p>
            <button
              onClick={() => {
                setSearchTerm('');
                setSelectedCategory('all');
              }}
              className="mt-6 px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-xl font-bold transition-all"
            >
              Clear Filters
            </button>
          </div>
        ) : (
          <>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-8">
              {filteredProducts.map(product => (
                <Link key={product.id} href={`/products/${product.slug}`}>
                  <div className="bg-gradient-to-br from-gray-800/90 to-purple-900/80 rounded-2xl overflow-hidden hover:scale-105 transition-all duration-300 shadow-xl border-2 border-purple-600/50 hover:border-gold-400/80 cursor-pointer relative h-full flex flex-col">
                    {/* Badges */}
                    <div className="absolute top-4 right-4 flex flex-col gap-2 z-10">
                      {product.bestseller && (
                        <div className="bg-red-500 text-white px-3 py-1 rounded-full text-xs font-bold">
                          BESTSELLER
                        </div>
                      )}
                      {product.featured && (
                        <div className="bg-gold-500 text-gray-900 px-3 py-1 rounded-full text-xs font-bold">
                          FEATURED
                        </div>
                      )}
                    </div>

                    {/* Image Placeholder */}
                    <div className="bg-gradient-to-br from-purple-800 to-blue-800 h-48 flex items-center justify-center text-6xl">
                      {product.category === 'devotional' && '📖'}
                      {product.category === 'journal' && '📝'}
                      {product.category === 'bundle' && '📦'}
                    </div>

                    {/* Content */}
                    <div className="p-6 flex flex-col flex-1">
                      <h3 className="text-xl font-bold text-white mb-2 line-clamp-2">{product.title}</h3>

                      <p className="text-purple-200 text-sm mb-4 line-clamp-3 flex-1">{product.description}</p>

                      {/* Rating */}
                      <div className="flex items-center mb-4">
                        <div className="text-gold-400 text-sm">
                          {'★'.repeat(Math.floor(product.rating))}
                          {product.rating % 1 !== 0 && '⯨'}
                          {'☆'.repeat(5 - Math.ceil(product.rating))}
                        </div>
                        <span className="text-purple-300 text-xs ml-2">({product.reviewCount})</span>
                      </div>

                      {/* Price */}
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-2">
                          <span className="text-2xl font-bold text-gold-300">
                            ${product.salePrice || product.price}
                          </span>
                          {(product.salePrice || product.regularPrice) && (
                            <span className="text-sm text-gray-400 line-through">
                              ${product.regularPrice || product.price}
                            </span>
                          )}
                        </div>
                        <span className="text-xs text-purple-300 uppercase font-bold bg-purple-800/50 px-2 py-1 rounded">
                          {product.category}
                        </span>
                      </div>

                      {/* CTA Button */}
                      <button className="w-full py-3 bg-gradient-to-r from-gold-600 to-amber-600 hover:from-gold-700 hover:to-amber-700 rounded-lg font-bold transition-all duration-300 shadow-lg">
                        View Details
                      </button>
                    </div>
                  </div>
                </Link>
              ))}
            </div>

            {/* Product Count */}
            <div className="text-center text-purple-300">
              Showing {filteredProducts.length} of {allProducts.length} products
            </div>
          </>
        )}

        {/* Email Capture CTA */}
        <div className="max-w-3xl mx-auto mt-16 bg-gradient-to-br from-gold-900/40 to-amber-900/40 rounded-3xl p-8 md:p-12 border-2 border-gold-500/50 text-center">
          <h2 className="text-3xl font-bold mb-4 text-gold-300">Get 10% Off Your First Order</h2>
          <p className="text-lg text-purple-200 mb-6">
            Subscribe to our newsletter and receive exclusive discounts, free resources, and spiritual insights.
          </p>
          <form className="flex flex-col sm:flex-row gap-4 max-w-xl mx-auto">
            <input
              type="email"
              placeholder="Enter your email"
              required
              className="flex-1 px-6 py-4 rounded-xl text-gray-900 font-semibold focus:outline-none focus:ring-4 focus:ring-gold-400"
            />
            <button
              type="submit"
              className="px-8 py-4 bg-gradient-to-r from-gold-500 to-amber-500 hover:from-gold-600 hover:to-amber-600 rounded-xl font-bold transition-all duration-300 shadow-lg"
            >
              Subscribe
            </button>
          </form>
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

export default ProductsPage;

export async function getServerSideProps() {
  return { props: {} };
}
