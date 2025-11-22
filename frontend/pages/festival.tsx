import React, { useState, useEffect } from 'react';
import { NextPage } from 'next';
import Head from 'next/head';
import FestivalPanel from '../components/FestivalPanel';
import FestivalCeremonyPanel from '../components/FestivalCeremonyPanel';

interface TabProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

interface FestivalCycle {
  cycle_id: string;
  timestamp: string;
  ceremony_type: string;
  proclamation: string;
  rite: string;
  flame_status: string;
  recorded_by: string;
  sacred_checksum: string;
}

interface FestivalResponse {
  status: string;
  total_ceremonies: number;
  last_ceremony?: string;
  last_updated?: string;
  cycles: FestivalCycle[];
  metadata: {
    filtered_count: number;
    total_count: number;
    ceremony_types: string[];
    flame_status: string;
  };
}

const TabNavigation: React.FC<TabProps> = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { id: 'overview', label: '🎭 Festival Overview', icon: '🎭' },
    { id: 'cycles', label: '🔄 Festival Cycles', icon: '🔄' },
    { id: 'ceremonies', label: '⚡ Sacred Ceremonies', icon: '⚡' },
    { id: 'proclamations', label: '📢 Proclamations', icon: '📢' },
    { id: 'silences', label: '🤫 Silences', icon: '🤫' },
    { id: 'blessings', label: '🙏 Blessings', icon: '🙏' }
  ];

  return (
    <div className="flex flex-wrap gap-1 mb-6 p-1 bg-gray-800 rounded-lg">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => setActiveTab(tab.id)}
          className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all ${
            activeTab === tab.id
              ? 'bg-indigo-600 text-white shadow-lg'
              : 'text-gray-300 hover:text-white hover:bg-gray-700'
          }`}
        >
          <span>{tab.icon}</span>
          <span className="hidden sm:inline">{tab.label.split(' ').slice(1).join(' ')}</span>
          <span className="sm:hidden">{tab.icon}</span>
        </button>
      ))}
    </div>
  );
};

export default function FestivalDashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [festivalData, setFestivalData] = useState<FestivalResponse | null>(null);
  const [ceremonyData, setCeremonyData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedType, setSelectedType] = useState<string>('all');
  const [limit, setLimit] = useState<number>(10);

  const fetchFestivalData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const params = new URLSearchParams();
      if (selectedType !== 'all') {
        params.append('ceremony_type', selectedType);
      }
      params.append('limit', limit.toString());
      
      const [festivalResponse, ceremonyResponse] = await Promise.all([
        fetch(`/api/festival?${params.toString()}`),
        fetch('/api/ceremony')
      ]);
      
      if (!festivalResponse.ok) {
        throw new Error(`Failed to fetch festival data: ${festivalResponse.statusText}`);
      }
      
      const festivalData: FestivalResponse = await festivalResponse.json();
      setFestivalData(festivalData);
      
      if (ceremonyResponse.ok) {
        const ceremonyData = await ceremonyResponse.json();
        setCeremonyData(ceremonyData);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFestivalData();
  }, [selectedType, limit]);

  const getFlameStatusDisplay = (status: string): string => {
    switch (status) {
      case 'burning_bright':
        return '🔥 Burning Bright';
      case 'burning_local':
        return '🏠 Local Flame';
      case 'awaiting_ignition':
        return '🕯️ Awaiting Ignition';
      default:
        return '✨ Unknown Status';
    }
  };

  const formatCeremonyType = (type: string): string => {
    return type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  const OverviewPanel = () => (
    <div className="space-y-6">
      {/* Festival Overview Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl p-6 text-white">
        <h2 className="text-2xl font-bold mb-4">🎭 Codex Festival Dashboard</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
            <div className="text-sm text-indigo-200">Festival Cycles</div>
            <div className="text-2xl font-bold">{festivalData?.total_ceremonies || 0}</div>
          </div>
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
            <div className="text-sm text-purple-200">Sacred Ceremonies</div>
            <div className="text-2xl font-bold">{ceremonyData?.total_ceremonies || 0}</div>
          </div>
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
            <div className="text-sm text-blue-200">Flame Status</div>
            <div className="text-lg font-semibold capitalize">
              {ceremonyData?.metadata?.flame_status?.replace(/_/g, ' ') || 
               festivalData?.metadata?.flame_status?.replace(/_/g, ' ') || 'Dormant'}
            </div>
          </div>
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
            <div className="text-sm text-green-200">Last Activity</div>
            <div className="text-sm">
              {festivalData?.last_ceremony ? 
                new Date(festivalData.last_ceremony).toLocaleDateString() : 
                'No Activity'
              }
            </div>
          </div>
        </div>
      </div>

      {/* Ceremonial Statistics */}
      {ceremonyData?.metadata?.ceremonial_stats && (
        <div className="bg-white rounded-xl p-6 border border-gray-200">
          <h3 className="text-xl font-bold text-gray-900 mb-4">⚡ Ceremonial Activity</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-center gap-2 text-red-600 mb-2">
                <span>📢</span>
                <span className="font-semibold">Proclamations</span>
              </div>
              <div className="text-2xl font-bold text-gray-900">
                {ceremonyData.metadata.ceremonial_stats.proclamation || 0}
              </div>
            </div>
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-center gap-2 text-blue-600 mb-2">
                <span>🤫</span>
                <span className="font-semibold">Sacred Silences</span>
              </div>
              <div className="text-2xl font-bold text-gray-900">
                {ceremonyData.metadata.ceremonial_stats.silence || 0}
              </div>
            </div>
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-center gap-2 text-green-600 mb-2">
                <span>🙏</span>
                <span className="font-semibold">Divine Blessings</span>
              </div>
              <div className="text-2xl font-bold text-gray-900">
                {ceremonyData.metadata.ceremonial_stats.blessing || 0}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Recent Activity Preview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl p-6 border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">🔄 Recent Festival Cycles</h3>
          <div className="text-gray-500 text-sm">
            Switch to "Festival Cycles" tab to view detailed cycle information
          </div>
        </div>
        <div className="bg-white rounded-xl p-6 border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">⚡ Recent Ceremonies</h3>
          <div className="text-gray-500 text-sm">
            Switch to "Sacred Ceremonies" tab to view ceremonial inscriptions
          </div>
        </div>
      </div>
    </div>
  );

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return <OverviewPanel />;
      case 'cycles':
        return (
          <div>
            {/* Filters */}
            <div className="bg-white p-4 rounded-lg border border-gray-200 mb-6">
              <div className="flex flex-wrap items-center gap-4">
                <div>
                  <label htmlFor="ceremony-type" className="block text-sm font-medium text-gray-700 mb-1">
                    Ceremony Type
                  </label>
                  <select
                    id="ceremony-type"
                    value={selectedType}
                    onChange={(e) => setSelectedType(e.target.value)}
                    className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    <option value="all">All Ceremonies</option>
                    {festivalData?.metadata.ceremony_types.map(type => (
                      <option key={type} value={type}>
                        {formatCeremonyType(type)}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label htmlFor="limit" className="block text-sm font-medium text-gray-700 mb-1">
                    Show Recent
                  </label>
                  <select
                    id="limit"
                    value={limit}
                    onChange={(e) => setLimit(parseInt(e.target.value))}
                    className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    <option value={5}>5 ceremonies</option>
                    <option value={10}>10 ceremonies</option>
                    <option value={25}>25 ceremonies</option>
                    <option value={50}>50 ceremonies</option>
                  </select>
                </div>

                <div className="ml-auto">
                  <button
                    onClick={fetchFestivalData}
                    className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition-colors text-sm font-medium"
                  >
                    Refresh
                  </button>
                </div>
              </div>
            </div>
            <FestivalPanel cycles={festivalData?.cycles || []} />
          </div>
        );
      case 'ceremonies':
        return <FestivalCeremonyPanel />;
      case 'proclamations':
        return <FestivalCeremonyPanel kind="proclamation" />;
      case 'silences':
        return <FestivalCeremonyPanel kind="silence" />;
      case 'blessings':
        return <FestivalCeremonyPanel kind="blessing" />;
      default:
        return <OverviewPanel />;
    }
  };

  if (loading) {
    return (
      <>
        <Head>
          <title>Festival Dashboard - Codex Dominion</title>
          <meta name="description" content="Sacred Festival and Ceremonial Management Dashboard" />
        </Head>
        <div className="min-h-screen bg-gray-900 py-8">
          <div className="max-w-6xl mx-auto px-4">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-400 mx-auto"></div>
              <p className="mt-4 text-gray-300">Loading sacred ceremonies...</p>
            </div>
          </div>
        </div>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Head>
          <title>Festival Dashboard - Codex Dominion</title>
          <meta name="description" content="Sacred Festival and Ceremonial Management Dashboard" />
        </Head>
        <div className="min-h-screen bg-gray-900 py-8">
          <div className="max-w-6xl mx-auto px-4">
            <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-6 text-center">
              <p className="text-red-400 font-medium">Error loading festival data</p>
              <p className="text-red-300 text-sm mt-2">{error}</p>
              <button
                onClick={fetchFestivalData}
                className="mt-4 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition-colors"
              >
                Retry
              </button>
            </div>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Head>
        <title>Festival Dashboard - Codex Dominion</title>
        <meta name="description" content="Sacred Festival and Ceremonial Management Dashboard" />
      </Head>

      <div className="min-h-screen bg-gray-900">
        <div className="container mx-auto px-4 py-8">
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-white mb-2">
              🎭 Festival Dashboard
            </h1>
            <p className="text-gray-400">
              Sacred ceremonial management and festival cycle tracking
            </p>
          </div>

          <TabNavigation activeTab={activeTab} setActiveTab={setActiveTab} />
          
          <div className="transition-all duration-300">
            {renderTabContent()}
          </div>

          {/* Footer */}
          <div className="mt-8 text-center text-sm text-gray-500">
            <p>
              🕯️ May the eternal flame illuminate all who witness these sacred ceremonies 🕯️
            </p>
          </div>
        </div>
      </div>
    </>
  );
}