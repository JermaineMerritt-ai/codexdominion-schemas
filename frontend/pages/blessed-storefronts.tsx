type Store = {
  id: string;
  name: string;
  url: string;
  description: string;
  category: string;
  icon: string;
  featured: boolean;
  offerings: string[];
};

type BlessingModalProps = {
  selectedStore: Store;
  setSelectedStore: React.Dispatch<React.SetStateAction<Store | null>>;
};

const BlessingModal: React.FC<BlessingModalProps> = ({ selectedStore, setSelectedStore }) => (
  <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-70">
    <div className="bg-gray-900 rounded-2xl p-8 max-w-lg w-full border border-yellow-500 shadow-2xl">
      <div className="flex items-center mb-4">
        <span className="text-3xl mr-3">{selectedStore.icon}</span>
        <h2 className="text-2xl font-bold text-yellow-400">{selectedStore.name}</h2>
        <button
          onClick={() => setSelectedStore(null)}
          className="ml-auto text-gray-400 hover:text-white text-2xl"
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
);

const BlessedStorefrontsPage: React.FC = () => {
  const [selectedStore, setSelectedStore] = useState<Store | null>(null);
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white">
      <Head>
        <title>Blessed Storefronts | Codex Dominion</title>
        <meta name="description" content="Discover and visit blessed AI-powered storefronts." />
      </Head>
      <div className="container mx-auto py-16 px-4">
        <h1 className="text-5xl font-bold mb-8 text-yellow-400 text-center">Blessed Storefronts</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {stores.map((store) => (
            <div key={store.id}>
              <StoreCard store={store} setSelectedStore={setSelectedStore} />
            </div>
          ))}
        </div>
        {/* Blessing Modal */}
        {selectedStore && (
          <BlessingModal selectedStore={selectedStore} setSelectedStore={setSelectedStore} />
        )}
      </div>
    </div>
  );
};

export default BlessedStorefrontsPage;
// @ts-nocheck
import React, { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import StorefrontBlessing from '../components/StorefrontBlessing';

const stores: Store[] = [
  {
    id: 'aistorelab',
    name: 'aistorelab.com',
    url: 'https://aistorelab.com',
    description: 'Premium AI tools, templates, and services for professionals and enterprises.',
    category: 'AI & Technology',
    icon: '🤖',
    featured: true,
    offerings: [
      'AI Development Tools',
      'Business Solutions',
      'Creative AI Suite',
      'Data Analytics',
    ],
  },
  // ... other stores
];

const StoreCard: React.FC<{
  store: Store;
  setSelectedStore: React.Dispatch<React.SetStateAction<Store | null>>;
}> = ({ store, setSelectedStore }) => (
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
      <p className="text-gray-400 text-sm mb-4">{store.description}</p>
      <div className="mb-4">
        <h4 className="text-white font-medium mb-2">Sacred Offerings:</h4>
        <div className="flex flex-wrap gap-2">
          {store.offerings.map((offering: string, i: number) => (
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
          aria-label={`View blessing for ${store.name}`}
          title={`View blessing for ${store.name}`}
        >
          🕯️ View Blessing
        </button>
        {store.url !== '#' && (
          <Link href={store.url} target="_blank" rel="noopener noreferrer">
            <button
              className="px-4 py-2 border border-gray-600 text-gray-300 rounded-lg hover:border-yellow-500 hover:text-white transition-colors"
              aria-label={`Visit ${store.name} storefront`}
              title={`Visit ${store.name} storefront`}
            >
              🛍️
            </button>
          </Link>
        )}
      </div>
    </div>
  </div>
);

const BlessedStorefronts = () => {
  const [selectedStore, setSelectedStore] = useState<Store | null>(null);
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
          {/* Featured Stores */}
          <div className="mb-8">
            <h3 className="text-2xl font-bold text-white mb-6 flex items-center">
              <span className="text-2xl mr-2">⭐</span>
              Featured Blessed Storefronts
            </h3>
            <div className="grid lg:grid-cols-2 gap-6">
              {stores
                .filter((store) => store.featured)
                .map((store) => (
                  <StoreCard key={store.id} store={store} setSelectedStore={setSelectedStore} />
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
                <StoreCard key={store.id} store={store} setSelectedStore={setSelectedStore} />
              ))}
            </div>
          </div>
          {/* Store Blessing Modal */}
          {selectedStore && (
            <div className="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50 p-4">
              <div className="bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
                <div className="p-8">
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-2xl font-bold text-white flex items-center">
                      <span className="text-3xl mr-3">{selectedStore?.icon}</span>
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
      </div>
    </>
  );
};
