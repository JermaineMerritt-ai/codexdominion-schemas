import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { NextPage } from 'next';
import Head from 'next/head';
import Link from 'next/link';

interface Banner {
  id: string;
  title: string;
  message: string;
  season: string;
  type: 'seasonal' | 'announcement' | 'ceremony';
  active: boolean;
}

interface InductionStep {
  id: string;
  title: string;
  description: string;
  type: 'proclamation' | 'silence' | 'blessing';
  completed: boolean;
  required: boolean;
}

interface HeritageEvent {
  id: string;
  date: string;
  title: string;
  description: string;
  significance: 'foundational' | 'expansion' | 'transformation';
  participants: string[];
}

const HeirDashboard: NextPage = () => {
  const [activeTab, setActiveTab] = useState('banners');
  const [banners, setBanners] = useState<Banner[]>([]);
  const [inductionSteps, setInductionSteps] = useState<InductionStep[]>([]);
  const [heritageEvents, setHeritageEvents] = useState<HeritageEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [inductionProgress, setInductionProgress] = useState(0);

  // Mock data - replace with actual API calls
  useEffect(() => {
    setTimeout(() => {
      setBanners([
        {
          id: '1',
          title: 'Autumn Equinox Celebration',
          message: 'The season of harvest brings wisdom to those who seek the ancient ways.',
          season: '🍂 Autumn Equinox',
          type: 'seasonal',
          active: true,
        },
        {
          id: '2',
          title: 'New Heir Welcome Ceremony',
          message: 'Join us in welcoming the newest members to our sacred lineage.',
          season: 'Eternal',
          type: 'ceremony',
          active: true,
        },
      ]);

      setInductionSteps([
        {
          id: '1',
          title: 'Sacred Proclamation',
          description: 'Declare your intent to join the Codex Dominion lineage.',
          type: 'proclamation',
          completed: true,
          required: true,
        },
        {
          id: '2',
          title: 'Period of Silence',
          description: 'Observe the traditional period of contemplative silence.',
          type: 'silence',
          completed: true,
          required: true,
        },
        {
          id: '3',
          title: 'Blessing Ceremony',
          description: 'Receive the ceremonial blessing from the Custodians.',
          type: 'blessing',
          completed: false,
          required: true,
        },
      ]);

      setHeritageEvents([
        {
          id: '1',
          date: '2024-01-15',
          title: 'Foundation of the Codex',
          description:
            'The first sacred inscriptions were made, establishing the eternal digital sovereignty.',
          significance: 'foundational',
          participants: ['Founding Custodian', 'Sacred Architects'],
        },
        {
          id: '2',
          date: '2024-06-21',
          title: 'Summer Solstice Expansion',
          description: 'The Festival Transmission system was blessed and made eternal.',
          significance: 'expansion',
          participants: ['Festival Keepers', 'Sacred Engineers'],
        },
        {
          id: '3',
          date: '2024-09-15',
          title: 'Heritage Documentation Project',
          description: 'Comprehensive lineage tracking system implemented for future heirs.',
          significance: 'transformation',
          participants: ['Heritage Guardians', 'Lineage Chroniclers'],
        },
      ]);

      // Calculate induction progress
      const completed = inductionSteps.filter((step) => step.completed).length;
      const total = inductionSteps.filter((step) => step.required).length;
      setInductionProgress((completed / total) * 100);

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
            ? 'bg-amber-600 text-white shadow-lg shadow-amber-500/30'
            : 'text-gray-300 hover:text-white hover:bg-gray-700'
        }
      `}
    >
      <span className="text-lg mr-2">{icon}</span>
      {label}
    </button>
  );

  const InductionStepCard: React.FC<{ step: InductionStep }> = ({ step }) => {
    const typeIcons = {
      proclamation: '📢',
      silence: '🤫',
      blessing: '🙏',
    };

    const typeColors = {
      proclamation: 'border-orange-500 bg-orange-500/10',
      silence: 'border-blue-500 bg-blue-500/10',
      blessing: 'border-purple-500 bg-purple-500/10',
    };

    return (
      <div
        className={`
        p-6 rounded-xl border-2 transition-all duration-300
        ${step.completed ? 'bg-green-500/10 border-green-500' : typeColors[step.type]}
      `}
      >
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center">
            <span className="text-3xl mr-3">{step.completed ? '✅' : typeIcons[step.type]}</span>
            <div>
              <h3 className="text-lg font-medium text-white">{step.title}</h3>
              <p className="text-sm text-gray-400">
                {step.type.charAt(0).toUpperCase() + step.type.slice(1)} Ceremony
              </p>
            </div>
          </div>
          {step.required && (
            <span className="px-2 py-1 bg-red-500 text-white text-xs rounded-full">Required</span>
          )}
        </div>

        <p className="text-gray-300 mb-4">{step.description}</p>

        {!step.completed && (
          <button className="px-4 py-2 bg-amber-600 text-white rounded-lg hover:bg-amber-700 transition-colors">
            Begin {step.title}
          </button>
        )}
      </div>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-800 via-orange-800 to-red-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-amber-400 border-t-transparent mx-auto mb-4"></div>
          <p className="text-white text-lg">Loading Heritage Systems...</p>
        </div>
      </div>
    );
  }

  // Styled component for progress bar
  const ProgressBar = styled.div<{ width: number }>`
    background: linear-gradient(to right, #f59e42, #fb923c);
    height: 0.75rem;
    border-radius: 9999px;
    transition: width 0.5s;
    width: ${({ width }) => width}%;
  `;

  return (
    <>
      <Head>
        <title>Heir Dashboard - Codex Dominion</title>
        <meta name="description" content="Guided induction and ceremonial participation" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-amber-800 via-orange-800 to-red-900">
        {/* Header */}
        <div className="border-b border-orange-700 bg-black bg-opacity-20">
          <div className="container mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <Link href="/dashboard-selector" className="text-amber-300 hover:text-white mr-4">
                  ← Back
                </Link>
                <h1 className="text-2xl font-bold text-white flex items-center">
                  <span className="text-3xl mr-3">👑</span>
                  Heir Dashboard
                </h1>
              </div>
              <div className="text-amber-300 text-sm">
                Induction Progress: {inductionProgress.toFixed(0)}%
              </div>
            </div>
          </div>
        </div>

        <div className="container mx-auto px-6 py-8">
          {/* Progress Banner */}
          <div className="bg-black bg-opacity-20 rounded-xl border border-amber-700 p-6 mb-8">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold text-white">Heritage Induction Journey</h2>
              <span className="text-amber-300 font-medium">
                {inductionProgress.toFixed(0)}% Complete
              </span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-3 mb-4">
              <ProgressBar width={inductionProgress} />
            </div>
            <p className="text-gray-300">
              Continue your sacred journey to become a full member of the Codex Dominion lineage.
            </p>
          </div>

          {/* Tab Navigation */}
          <div className="flex flex-wrap gap-4 mb-8">
            <TabButton
              id="banners"
              label="Banners & Proclamations"
              icon="🏴"
              active={activeTab === 'banners'}
            />
            <TabButton
              id="induction"
              label="Guided Induction"
              icon="🌟"
              active={activeTab === 'induction'}
            />
            <TabButton
              id="heritage"
              label="Lineage Replay"
              icon="📚"
              active={activeTab === 'heritage'}
            />
            <TabButton
              id="ceremonies"
              label="Ceremony Archive"
              icon="🎭"
              active={activeTab === 'ceremonies'}
            />
          </div>

          {/* Banners Tab */}
          {activeTab === 'banners' && (
            <div className="space-y-6">
              <div className="bg-black bg-opacity-20 rounded-xl border border-amber-700 p-6">
                <h2 className="text-2xl font-bold text-white flex items-center mb-6">
                  <span className="text-2xl mr-2">🏴</span>
                  Seasonal Banners & Proclamations
                </h2>

                <div className="space-y-4">
                  {banners.map((banner) => (
                    <div
                      key={banner.id}
                      className="bg-gradient-to-r from-amber-800/30 to-orange-800/30 rounded-xl p-6 border border-amber-600"
                    >
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex items-center">
                          <span className="text-3xl mr-4">
                            {banner.type === 'seasonal'
                              ? '🌟'
                              : banner.type === 'ceremony'
                                ? '🎭'
                                : '📢'}
                          </span>
                          <div>
                            <h3 className="text-xl font-bold text-white">{banner.title}</h3>
                            <p className="text-amber-300">{banner.season}</p>
                          </div>
                        </div>
                        {banner.active && (
                          <span className="px-3 py-1 bg-green-500 text-white text-sm rounded-full">
                            Active
                          </span>
                        )}
                      </div>

                      <p className="text-gray-200 text-lg leading-relaxed mb-4">{banner.message}</p>

                      <div className="flex space-x-3">
                        <button className="px-4 py-2 bg-amber-600 text-white rounded-lg hover:bg-amber-700 transition-colors">
                          View Details
                        </button>
                        <button className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors">
                          Share
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Induction Tab */}
          {activeTab === 'induction' && (
            <div className="space-y-6">
              <div className="bg-black bg-opacity-20 rounded-xl border border-amber-700 p-6">
                <h2 className="text-2xl font-bold text-white flex items-center mb-6">
                  <span className="text-2xl mr-2">🌟</span>
                  Guided Induction Forms
                </h2>

                <div className="grid gap-6">
                  {inductionSteps.map((step) => (
                    <InductionStepCard key={step.id} step={step} />
                  ))}
                </div>

                {inductionProgress < 100 && (
                  <div className="mt-8 p-6 bg-amber-900/30 rounded-xl border border-amber-600">
                    <h3 className="text-lg font-medium text-white mb-3">Next Steps</h3>
                    <p className="text-gray-300 mb-4">
                      Complete your remaining induction ceremonies to unlock full heir privileges
                      and access to advanced heritage documentation.
                    </p>
                    <button className="px-6 py-3 bg-amber-600 text-white rounded-lg hover:bg-amber-700 transition-colors">
                      Continue Induction Journey
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Heritage Tab */}
          {activeTab === 'heritage' && (
            <div className="space-y-6">
              <div className="bg-black bg-opacity-20 rounded-xl border border-amber-700 p-6">
                <h2 className="text-2xl font-bold text-white flex items-center mb-6">
                  <span className="text-2xl mr-2">📚</span>
                  Educational Lineage Replay
                </h2>

                <div className="space-y-6">
                  {heritageEvents.map((event, index) => (
                    <div key={event.id} className="relative">
                      {/* Timeline Line */}
                      {index < heritageEvents.length - 1 && (
                        <div className="absolute left-6 top-12 w-px h-20 bg-amber-500"></div>
                      )}

                      <div className="flex items-start space-x-4">
                        <div
                          className={`
                          w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 border-2
                          ${
                            event.significance === 'foundational'
                              ? 'bg-purple-600 border-purple-400'
                              : event.significance === 'expansion'
                                ? 'bg-blue-600 border-blue-400'
                                : 'bg-green-600 border-green-400'
                          }
                        `}
                        >
                          <span className="text-white font-bold">{index + 1}</span>
                        </div>

                        <div className="flex-1 bg-gray-800 bg-opacity-50 rounded-lg p-6">
                          <div className="flex items-center justify-between mb-3">
                            <h3 className="text-lg font-medium text-white">{event.title}</h3>
                            <span className="text-sm text-gray-400">
                              {new Date(event.date).toLocaleDateString()}
                            </span>
                          </div>

                          <p className="text-gray-300 mb-4">{event.description}</p>

                          <div className="flex flex-wrap items-center gap-4">
                            <span
                              className={`
                              px-3 py-1 rounded-full text-sm
                              ${
                                event.significance === 'foundational'
                                  ? 'bg-purple-500/20 text-purple-300'
                                  : event.significance === 'expansion'
                                    ? 'bg-blue-500/20 text-blue-300'
                                    : 'bg-green-500/20 text-green-300'
                              }
                            `}
                            >
                              {event.significance.charAt(0).toUpperCase() +
                                event.significance.slice(1)}
                            </span>

                            <div className="flex items-center space-x-2">
                              <span className="text-sm text-gray-400">Participants:</span>
                              {event.participants.map((participant, i) => (
                                <span key={i} className="text-sm text-amber-300">
                                  {participant}
                                  {i < event.participants.length - 1 ? ', ' : ''}
                                </span>
                              ))}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Ceremonies Tab */}
          {activeTab === 'ceremonies' && (
            <div className="space-y-6">
              <div className="bg-black bg-opacity-20 rounded-xl border border-amber-700 p-6">
                <h2 className="text-2xl font-bold text-white flex items-center mb-6">
                  <span className="text-2xl mr-2">🎭</span>
                  Ceremony Archive & Calendar
                </h2>

                <div className="grid md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <h3 className="text-lg font-medium text-white">Upcoming Ceremonies</h3>

                    <div className="space-y-3">
                      {[
                        {
                          date: '2025-11-15',
                          name: 'Full Moon Blessing',
                          type: 'monthly',
                        },
                        {
                          date: '2025-12-21',
                          name: 'Winter Solstice Gathering',
                          type: 'seasonal',
                        },
                        {
                          date: '2025-12-31',
                          name: 'Year Transition Rite',
                          type: 'annual',
                        },
                      ].map((ceremony, i) => (
                        <div
                          key={i}
                          className="p-4 bg-gray-800 bg-opacity-50 rounded-lg border border-gray-600"
                        >
                          <div className="flex justify-between items-center">
                            <div>
                              <p className="font-medium text-white">{ceremony.name}</p>
                              <p className="text-sm text-gray-400">
                                {new Date(ceremony.date).toLocaleDateString()}
                              </p>
                            </div>
                            <span
                              className={`
                              px-2 py-1 rounded text-xs
                              ${
                                ceremony.type === 'seasonal'
                                  ? 'bg-amber-500 text-white'
                                  : ceremony.type === 'monthly'
                                    ? 'bg-blue-500 text-white'
                                    : 'bg-purple-500 text-white'
                              }
                            `}
                            >
                              {ceremony.type}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="space-y-4">
                    <h3 className="text-lg font-medium text-white">Recent Participation</h3>

                    <div className="space-y-3">
                      {[
                        {
                          date: '2025-10-31',
                          name: 'Harvest Festival',
                          participation: 'Observer',
                        },
                        {
                          date: '2025-10-15',
                          name: 'New Moon Silence',
                          participation: 'Participant',
                        },
                        {
                          date: '2025-09-22',
                          name: 'Autumn Equinox',
                          participation: 'Initiate',
                        },
                      ].map((event, i) => (
                        <div
                          key={i}
                          className="p-4 bg-gray-800 bg-opacity-50 rounded-lg border border-gray-600"
                        >
                          <div className="flex justify-between items-center">
                            <div>
                              <p className="font-medium text-white">{event.name}</p>
                              <p className="text-sm text-gray-400">
                                {new Date(event.date).toLocaleDateString()}
                              </p>
                            </div>
                            <span className="px-2 py-1 bg-green-500 text-white rounded text-xs">
                              {event.participation}
                            </span>
                          </div>
                        </div>
                      ))}
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

export default HeirDashboard;
