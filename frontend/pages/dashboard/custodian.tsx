import React, { useState, useEffect } from 'react';
import { NextPage } from 'next';
import Head from 'next/head';
import Link from 'next/link';

interface ArtifactData {
  id: string;
  name: string;
  type: 'json' | 'markdown' | 'configuration';
  size: string;
  lastModified: string;
  status: 'active' | 'archived' | 'pending';
  checksum: string;
}

interface InfrastructureCrown {
  name: string;
  status: 'operational' | 'maintenance' | 'error';
  uptime: string;
  lastAudit: string;
  dependencies: string[];
}

const CustodianDashboard: NextPage = () => {
  const [activeTab, setActiveTab] = useState('artifacts');
  const [artifacts, setArtifacts] = useState<ArtifactData[]>([]);
  const [crowns, setCrowns] = useState<InfrastructureCrown[]>([]);
  const [loading, setLoading] = useState(true);

  // Mock data - replace with actual API calls
  useEffect(() => {
    // Simulate loading artifacts
    setTimeout(() => {
      setArtifacts([
        {
          id: '1',
          name: 'ceremony_records.json',
          type: 'json',
          size: '2.4 MB',
          lastModified: '2025-11-08T14:30:00Z',
          status: 'active',
          checksum: 'sha256:a1b2c3...',
        },
        {
          id: '2',
          name: 'festival_lineage.md',
          type: 'markdown',
          size: '156 KB',
          lastModified: '2025-11-08T13:15:00Z',
          status: 'active',
          checksum: 'sha256:d4e5f6...',
        },
        {
          id: '3',
          name: 'system_config.json',
          type: 'configuration',
          size: '45 KB',
          lastModified: '2025-11-08T12:00:00Z',
          status: 'pending',
          checksum: 'sha256:g7h8i9...',
        },
      ]);

      setCrowns([
        {
          name: 'Festival Transmission Crown',
          status: 'operational',
          uptime: '99.98%',
          lastAudit: '2025-11-07T09:00:00Z',
          dependencies: ['Cloud Functions', 'Storage', 'Pub/Sub'],
        },
        {
          name: 'Capsule Matrix Crown',
          status: 'operational',
          uptime: '99.95%',
          lastAudit: '2025-11-06T15:30:00Z',
          dependencies: ['Cloud Run', 'Firestore', 'Auth'],
        },
        {
          name: 'Signal Intelligence Crown',
          status: 'maintenance',
          uptime: '98.50%',
          lastAudit: '2025-11-05T11:00:00Z',
          dependencies: ['FastAPI', 'PostgreSQL', 'Redis'],
        },
      ]);

      setLoading(false);
    }, 1000);
  }, []);

  const TabButton: React.FC<{
    id: string;
    label: string;
    icon: string;
    active: boolean;
  }> = ({ id, label, icon, active }) => (
    <button
      onClick={() => setActiveTab(id)}
      className={`
        flex items-center px-6 py-3 rounded-lg font-medium transition-all duration-200
        ${
          active
            ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/30'
            : 'text-gray-300 hover:text-white hover:bg-gray-700'
        }
      `}
    >
      <span className="text-lg mr-2">{icon}</span>
      {label}
    </button>
  );

  const StatusBadge: React.FC<{ status: string }> = ({ status }) => {
    const colors = {
      active: 'bg-green-500 text-white',
      operational: 'bg-green-500 text-white',
      archived: 'bg-gray-500 text-white',
      pending: 'bg-yellow-500 text-black',
      maintenance: 'bg-orange-500 text-white',
      error: 'bg-red-500 text-white',
    };

    return (
      <span
        className={`px-2 py-1 rounded-full text-xs font-medium ${colors[status as keyof typeof colors]}`}
      >
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </span>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-purple-400 border-t-transparent mx-auto mb-4"></div>
          <p className="text-white text-lg">Loading Custodian Systems...</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <Head>
        <title>Custodian Dashboard - Codex Dominion</title>
        <meta name="description" content="Full system administration and artifact management" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
        {/* Header */}
        <div className="border-b border-purple-800 bg-black bg-opacity-20">
          <div className="container mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <Link href="/dashboard-selector" className="text-purple-300 hover:text-white mr-4">
                  ← Back
                </Link>
                <h1 className="text-2xl font-bold text-white flex items-center">
                  <span className="text-3xl mr-3">🏛️</span>
                  Custodian Dashboard
                </h1>
              </div>
              <div className="text-purple-300 text-sm">
                Last Login: {new Date().toLocaleString()}
              </div>
            </div>
          </div>
        </div>

        <div className="container mx-auto px-6 py-8">
          {/* Tab Navigation */}
          <div className="flex flex-wrap gap-4 mb-8">
            <TabButton
              id="artifacts"
              label="Artifacts"
              icon="📦"
              active={activeTab === 'artifacts'}
            />
            <TabButton
              id="crowns"
              label="Infrastructure Crowns"
              icon="👑"
              active={activeTab === 'crowns'}
            />
            <TabButton
              id="inscriptions"
              label="Inscription Tools"
              icon="✒️"
              active={activeTab === 'inscriptions'}
            />
            <TabButton id="audit" label="Audit Lineage" icon="🔍" active={activeTab === 'audit'} />
          </div>

          {/* Artifacts Tab */}
          {activeTab === 'artifacts' && (
            <div className="space-y-6">
              <div className="bg-black bg-opacity-20 rounded-xl border border-purple-800 p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold text-white flex items-center">
                    <span className="text-2xl mr-2">📦</span>
                    System Artifacts
                  </h2>
                  <button className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors">
                    + New Artifact
                  </button>
                </div>

                <div className="grid gap-4">
                  {artifacts.map((artifact) => (
                    <div
                      key={artifact.id}
                      className="bg-gray-800 bg-opacity-50 rounded-lg p-4 border border-gray-700 hover:border-purple-500 transition-colors"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                          <div className="text-2xl">
                            {artifact.type === 'json'
                              ? '📄'
                              : artifact.type === 'markdown'
                                ? '📝'
                                : '⚙️'}
                          </div>
                          <div>
                            <h3 className="font-medium text-white">{artifact.name}</h3>
                            <p className="text-sm text-gray-400">
                              {artifact.size} • Modified{' '}
                              {new Date(artifact.lastModified).toLocaleString()}
                            </p>
                            <p className="text-xs text-gray-500 font-mono">{artifact.checksum}</p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-3">
                          <StatusBadge status={artifact.status} />
                          <div className="flex space-x-2">
                            <button className="p-2 text-gray-400 hover:text-white">📥</button>
                            <button className="p-2 text-gray-400 hover:text-white">✏️</button>
                            <button className="p-2 text-gray-400 hover:text-red-400">🗑️</button>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Infrastructure Crowns Tab */}
          {activeTab === 'crowns' && (
            <div className="space-y-6">
              <div className="bg-black bg-opacity-20 rounded-xl border border-purple-800 p-6">
                <h2 className="text-2xl font-bold text-white flex items-center mb-6">
                  <span className="text-2xl mr-2">👑</span>
                  Infrastructure Crowns
                </h2>

                <div className="grid lg:grid-cols-2 gap-6">
                  {crowns.map((crown, index) => (
                    <div
                      key={index}
                      className="bg-gray-800 bg-opacity-50 rounded-lg p-6 border border-gray-700"
                    >
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-medium text-white">{crown.name}</h3>
                        <StatusBadge status={crown.status} />
                      </div>

                      <div className="space-y-3 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-400">Uptime:</span>
                          <span className="text-white font-mono">{crown.uptime}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Last Audit:</span>
                          <span className="text-white">
                            {new Date(crown.lastAudit).toLocaleString()}
                          </span>
                        </div>
                        <div>
                          <p className="text-gray-400 mb-2">Dependencies:</p>
                          <div className="flex flex-wrap gap-1">
                            {crown.dependencies.map((dep, i) => (
                              <span
                                key={i}
                                className="px-2 py-1 bg-purple-800 text-purple-200 rounded text-xs"
                              >
                                {dep}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>

                      <div className="flex space-x-2 mt-4">
                        <button className="px-3 py-1 bg-purple-600 text-white rounded text-sm hover:bg-purple-700 transition-colors">
                          Monitor
                        </button>
                        <button className="px-3 py-1 bg-gray-600 text-white rounded text-sm hover:bg-gray-700 transition-colors">
                          Logs
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Inscription Tools Tab */}
          {activeTab === 'inscriptions' && (
            <div className="space-y-6">
              <div className="bg-black bg-opacity-20 rounded-xl border border-purple-800 p-6">
                <h2 className="text-2xl font-bold text-white flex items-center mb-6">
                  <span className="text-2xl mr-2">✒️</span>
                  Inscription Tools
                </h2>

                <div className="grid md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <h3 className="text-lg font-medium text-white">Manual Inscription</h3>

                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          Ceremony Type
                        </label>
                        <select
                          className="w-full p-3 bg-gray-800 border border-gray-600 rounded-lg text-white"
                          title="Select an option"
                        >
                          <option>Festival Transmission</option>
                          <option>Sacred Proclamation</option>
                          <option>System Blessing</option>
                          <option>Audit Record</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          Inscription Content
                        </label>
                        <textarea
                          className="w-full p-3 bg-gray-800 border border-gray-600 rounded-lg text-white h-32"
                          placeholder="Enter sacred inscription..."
                        />
                      </div>

                      <button className="w-full py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors">
                        Inscribe Manually
                      </button>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <h3 className="text-lg font-medium text-white">Automated Tools</h3>

                    <div className="grid gap-3">
                      <button className="p-4 bg-gray-800 border border-gray-600 rounded-lg text-left hover:border-purple-500 transition-colors">
                        <div className="flex items-center">
                          <span className="text-2xl mr-3">🤖</span>
                          <div>
                            <p className="font-medium text-white">Auto-Ceremony Scanner</p>
                            <p className="text-sm text-gray-400">
                              Detect and process system events
                            </p>
                          </div>
                        </div>
                      </button>

                      <button className="p-4 bg-gray-800 border border-gray-600 rounded-lg text-left hover:border-purple-500 transition-colors">
                        <div className="flex items-center">
                          <span className="text-2xl mr-3">📊</span>
                          <div>
                            <p className="font-medium text-white">Batch Processor</p>
                            <p className="text-sm text-gray-400">Process multiple inscriptions</p>
                          </div>
                        </div>
                      </button>

                      <button className="p-4 bg-gray-800 border border-gray-600 rounded-lg text-left hover:border-purple-500 transition-colors">
                        <div className="flex items-center">
                          <span className="text-2xl mr-3">🔄</span>
                          <div>
                            <p className="font-medium text-white">Scheduled Inscriptions</p>
                            <p className="text-sm text-gray-400">Automated ceremony triggers</p>
                          </div>
                        </div>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Audit Lineage Tab */}
          {activeTab === 'audit' && (
            <div className="space-y-6">
              <div className="bg-black bg-opacity-20 rounded-xl border border-purple-800 p-6">
                <h2 className="text-2xl font-bold text-white flex items-center mb-6">
                  <span className="text-2xl mr-2">🔍</span>
                  Audit Lineage & Traceability
                </h2>

                <div className="space-y-6">
                  {/* Audit Timeline */}
                  <div className="bg-gray-800 bg-opacity-30 rounded-lg p-4">
                    <h3 className="text-lg font-medium text-white mb-4">Recent System Events</h3>
                    <div className="space-y-3">
                      {[
                        {
                          time: '14:30',
                          event: 'Festival ceremony inscribed',
                          type: 'ceremony',
                          user: 'system',
                        },
                        {
                          time: '13:15',
                          event: 'Infrastructure crown updated',
                          type: 'maintenance',
                          user: 'custodian_01',
                        },
                        {
                          time: '12:00',
                          event: 'Artifact backup completed',
                          type: 'backup',
                          user: 'automated',
                        },
                        {
                          time: '11:45',
                          event: 'New heir registered',
                          type: 'registration',
                          user: 'heir_dashboard',
                        },
                      ].map((log, i) => (
                        <div
                          key={i}
                          className="flex items-center justify-between p-3 bg-gray-700 bg-opacity-50 rounded"
                        >
                          <div className="flex items-center">
                            <span className="text-sm text-gray-400 font-mono mr-4">{log.time}</span>
                            <span className="text-white">{log.event}</span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className="text-xs text-gray-400">{log.user}</span>
                            <span
                              className={`w-2 h-2 rounded-full ${
                                log.type === 'ceremony'
                                  ? 'bg-purple-500'
                                  : log.type === 'maintenance'
                                    ? 'bg-orange-500'
                                    : log.type === 'backup'
                                      ? 'bg-green-500'
                                      : 'bg-blue-500'
                              }`}
                            ></span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* System Health Metrics */}
                  <div className="grid md:grid-cols-3 gap-6">
                    <div className="bg-gray-800 bg-opacity-30 rounded-lg p-4 text-center">
                      <p className="text-2xl font-bold text-green-400">99.8%</p>
                      <p className="text-gray-400">System Uptime</p>
                    </div>
                    <div className="bg-gray-800 bg-opacity-30 rounded-lg p-4 text-center">
                      <p className="text-2xl font-bold text-purple-400">1,247</p>
                      <p className="text-gray-400">Total Inscriptions</p>
                    </div>
                    <div className="bg-gray-800 bg-opacity-30 rounded-lg p-4 text-center">
                      <p className="text-2xl font-bold text-cyan-400">23</p>
                      <p className="text-gray-400">Active Heirs</p>
                    </div>
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

export default CustodianDashboard;
