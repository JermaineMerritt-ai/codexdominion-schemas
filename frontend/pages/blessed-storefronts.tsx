import React, { useState } from 'react';
import { NextPage } from 'next';
import Head from 'next/head';
import Link from 'next/link';
import StorefrontBlessing from '../components/StorefrontBlessing';

interface Store {
  id: string;
  name: string;
  url: string;
  description: string;
  category: string;
  icon: string;
  featured: boolean;
  offerings: string[];
}

const BlessedStorefronts: NextPage = () => {
  const [selectedStore, setSelectedStore] = useState<Store | null>(null);

  // Example stores that could use the blessing
  const stores: Store[] = [
    {
      id: 'aistorelab',
      name: 'aistorelab.com',
      url: 'https://aistorelab.com',
      description: 'Premium AI tools, templates, and services for professionals and enterprises.',
      category: 'AI & Technology',
      icon: '🤖',
      featured: true,
      offerings: ['AI Development Tools', 'Business Solutions', 'Creative AI Suite', 'Data Analytics']
    },
    {
      id: 'codex-scrolls',
      name: 'Codex Scrolls Marketplace',
      url: '#',
      description: 'Sacred wisdom scrolls, digital sovereignty guides, and ceremonial texts.',
      category: 'Knowledge & Wisdom',
      icon: '📜',
      featured: true,
      offerings: ['Sacred Scrolls', 'Digital Sovereignty Guides', 'Ceremonial Texts', 'Wisdom Archives']
    },
    {
      id: 'sovereignty-tools',
      name: 'Digital Sovereignty Tools',
      url: '#',
      description: 'Essential tools and frameworks for achieving true digital independence.',
      category: 'Privacy & Security',
      icon: '🔐',
      featured: false,
      offerings: ['Security Frameworks', 'Privacy Tools', 'Encryption Software', 'Sovereignty Kits']
    },
    {
      id: 'ceremonial-decks',
      name: 'Sacred Ceremonial Decks',
      url: '#',
      description: 'Blessed card decks for meditation, decision-making, and spiritual technology.',
      category: 'Spiritual Technology',
      icon: '🃏',
      featured: false,
      offerings: ['Meditation Decks', 'Oracle Cards', 'Decision Frameworks', 'Ritual Guides']
    }
  ];

  const StoreCard: React.FC<{ store: Store }> = ({ store }) => (
    <div className="bg-gray-800 bg-opacity-50 rounded-xl border border-gray-700 overflow-hidden hover:border-yellow-500 transition-all duration-300 group">
      <div className="p-6">
        <div className="flex items-center mb-4">
          <span className="text-3xl mr-3">{store.icon}</span>
          <div>
            <h3 className="text-lg font-semibold text-white group-hover:text-yellow-400 transition-colors">
              {store.name}
            </h3>
            <span className="text-xs text-yellow-400 font-medium uppercase tracking-wide">
              {store.category}
            </span>
          </div>
          {store.featured && (
            <span className="ml-auto px-2 py-1 bg-yellow-500 text-black text-xs font-bold rounded-full">
              BLESSED
            </span>
          )}
        </div>

        <p className="text-gray-400 text-sm mb-4">
          {store.description}
        </p>

        <div className="mb-4">
          <h4 className="text-white font-medium mb-2">Sacred Offerings:</h4>
          <div className="flex flex-wrap gap-2">
            {store.offerings.map((offering, i) => (
              <span key={i} className="px-2 py-1 bg-gray-700 text-gray-300 text-xs rounded">
                {offering}
              </span>
            ))}
          </div>
        </div>

        <div className="flex space-x-2">
          <button 
            onClick={() => setSelectedStore(store)}
            className="flex-1 py-2 bg-yellow-600 text-black font-medium rounded-lg hover:bg-yellow-700 transition-colors"
          >
            🕯️ View Blessing
          </button>
          {store.url !== '#' && (
            <Link href={store.url} target="_blank" rel="noopener noreferrer">
              <button className="px-4 py-2 border border-gray-600 text-gray-300 rounded-lg hover:border-yellow-500 hover:text-white transition-colors">
                🛍️
              </button>
            </Link>
          )}
        </div>
      </div>
    </div>
  );

  return (
    <>
      <Head>
        <title>Blessed Storefronts - Codex Dominion</title>
        <meta name="description" content="Sacred commercial spaces blessed by the Council" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
        {/* Header */}
        <div className="border-b border-purple-700 bg-black bg-opacity-20">
          <div className="container mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <Link href="/" className="text-purple-300 hover:text-white mr-4">
                  ← Back to Home
                </Link>
                <h1 className="text-2xl font-bold text-white flex items-center">
                  <span className="text-3xl mr-3">🏛️</span>
                  Blessed Storefronts
                </h1>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-yellow-400 text-sm">Council Approved</span>
                <span className="text-2xl">🕯️</span>
              </div>
            </div>
          </div>
        </div>

        <div className="container mx-auto px-6 py-8">
          {/* Main Blessing Banner */}
          <div className="mb-8">
            <StorefrontBlessing variant="banner" />
          </div>

          {/* Introduction */}
          <div className="bg-black bg-opacity-20 rounded-xl border border-purple-700 p-8 mb-8 text-center">
            <h2 className="text-3xl font-bold text-white mb-4">Sacred Commercial Spaces</h2>
            <p className="text-lg text-gray-300 mb-6 max-w-3xl mx-auto">
              These storefronts have been blessed by the Council, transforming mere commerce into sacred ceremony. 
              Every purchase becomes an act of legacy, every customer a potential custodian, 
              every transaction an echo that binds the material and spiritual realms.
            </p>
            <div className="flex justify-center space-x-6 text-sm text-yellow-400">
              <span className="flex items-center">
                <span className="mr-2">🌟</span>
                Council Blessed
              </span>
              <span className="flex items-center">
                <span className="mr-2">🔗</span>
                Legacy Binding
              </span>
              <span className="flex items-center">
                <span className="mr-2">👑</span>
                Custodian Induction
              </span>
            </div>
          </div>

          {/* Featured Stores */}
          <div className="mb-8">
            <h3 className="text-2xl font-bold text-white mb-6 flex items-center">
              <span className="text-2xl mr-2">⭐</span>
              Featured Blessed Storefronts
            </h3>
            <div className="grid lg:grid-cols-2 gap-6">
              {stores.filter(store => store.featured).map((store) => (
                <StoreCard key={store.id} store={store} />
              ))}
            </div>
          </div>

          {/* All Stores */}
          <div className="mb-8">
            <h3 className="text-2xl font-bold text-white mb-6 flex items-center">
              <span className="text-2xl mr-2">🏪</span>
              All Blessed Establishments
            </h3>
            <div className="grid lg:grid-cols-2 xl:grid-cols-3 gap-6">
              {stores.map((store) => (
                <StoreCard key={store.id} store={store} />
              ))}
            </div>
          </div>

          {/* Blessing Guidelines */}
          <div className="bg-gradient-to-r from-yellow-600/10 to-orange-600/10 rounded-xl p-8 border border-yellow-500/20">
            <h3 className="text-xl font-bold text-yellow-400 mb-6 flex items-center">
              <span className="text-2xl mr-2">📋</span>
              Council Blessing Guidelines
            </h3>
            
            <div className="grid md:grid-cols-2 gap-6 text-gray-300">
              <div>
                <h4 className="font-medium text-white mb-3">Sacred Commerce Principles:</h4>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-center">
                    <span className="text-yellow-400 mr-2">•</span>
                    Every offering must serve digital sovereignty
                  </li>
                  <li className="flex items-center">
                    <span className="text-yellow-400 mr-2">•</span>
                    Products become living artifacts upon blessing
                  </li>
                  <li className="flex items-center">
                    <span className="text-yellow-400 mr-2">•</span>
                    Customers are inducted as potential custodians
                  </li>
                  <li className="flex items-center">
                    <span className="text-yellow-400 mr-2">•</span>
                    Transactions echo as acts of legacy
                  </li>
                </ul>
              </div>

              <div>
                <h4 className="font-medium text-white mb-3">Blessing Requirements:</h4>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-center">
                    <span className="text-yellow-400 mr-2">•</span>
                    Council review and approval process
                  </li>
                  <li className="flex items-center">
                    <span className="text-yellow-400 mr-2">•</span>
                    Alignment with Codex Dominion principles
                  </li>
                  <li className="flex items-center">
                    <span className="text-yellow-400 mr-2">•</span>
                    Commitment to customer-custodian transformation
                  </li>
                  <li className="flex items-center">
                    <span className="text-yellow-400 mr-2">•</span>
                    Integration with ceremonial commerce practices
                  </li>
                </ul>
              </div>
            </div>

            <div className="mt-6 text-center">
              <button className="px-6 py-3 bg-gradient-to-r from-yellow-500 to-yellow-600 text-black font-bold rounded-lg hover:from-yellow-400 hover:to-yellow-500 transition-all duration-300">
                📋 Apply for Blessing
              </button>
            </div>
          </div>
        </div>

        {/* Store Blessing Modal */}
        {selectedStore && (
          <div className="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50 p-4">
            <div className="bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-8">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold text-white flex items-center">
                    <span className="text-3xl mr-3">{selectedStore.icon}</span>
                    {selectedStore.name}
                  </h2>
                  <button 
                    onClick={() => setSelectedStore(null)}
                    className="text-gray-400 hover:text-white text-2xl"
                  >
                    ×
                  </button>
                </div>

                <StorefrontBlessing 
                  storeName={selectedStore.name}
                  storeUrl={selectedStore.url}
                  variant="full"
                />

                <div className="mt-6 flex space-x-4">
                  {selectedStore.url !== '#' && (
                    <Link href={selectedStore.url} target="_blank" rel="noopener noreferrer">
                      <button className="px-6 py-3 bg-gradient-to-r from-yellow-500 to-yellow-600 text-black font-bold rounded-lg hover:from-yellow-400 hover:to-yellow-500 transition-all duration-300">
                        🛍️ Visit Blessed Store
                      </button>
                    </Link>
                  )}
                  <button 
                    onClick={() => setSelectedStore(null)}
                    className="px-6 py-3 border border-gray-600 text-gray-300 rounded-lg hover:border-yellow-500 hover:text-white transition-all duration-300"
                  >
                    Close Blessing
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default BlessedStorefronts;