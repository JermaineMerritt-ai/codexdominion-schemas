'use client';

import { useState, useEffect } from 'react';
import Head from 'next/head';

interface TemporalScale {
  name: string;
  icon: string;
  description: string;
  frequency: number;
  color: string;
  status: string;
}

interface RhythmMetrics {
  dailyFlames: number;
  seasonalRhythms: number;
  epochalCrowns: number;
  millennialHymns: number;
  cosmicAlignments: number;
  totalTransmissions: number;
}

function TemporalRhythm() {
  const [activeScale, setActiveScale] = useState<string>('all');
  const [metrics, setMetrics] = useState<RhythmMetrics>({
    dailyFlames: 1,
    seasonalRhythms: 1,
    epochalCrowns: 1,
    millennialHymns: 1,
    cosmicAlignments: 1,
    totalTransmissions: 999999
  });

  const temporalScales: TemporalScale[] = [
    {
      name: 'Daily Flame',
      icon: '🔥',
      description: 'Dawn capsules, devotionals, affirmations',
      frequency: 528.0,
      color: 'from-orange-400 to-red-500',
      status: 'IGNITED'
    },
    {
      name: 'Seasonal Rhythm',
      icon: '🌱',
      description: 'Festivals, heritage cycles, quarterly campaigns',
      frequency: 639.0,
      color: 'from-green-400 to-emerald-500',
      status: 'TURNING'
    },
    {
      name: 'Epochal Custodianship',
      icon: '👑',
      description: 'Generational crowns, empire expansions',
      frequency: 741.0,
      color: 'from-purple-400 to-indigo-500',
      status: 'TRANSFERRING'
    },
    {
      name: 'Millennial Continuum',
      icon: '⭐',
      description: 'Interstellar hymns, eternal proclamations',
      frequency: 852.0,
      color: 'from-blue-400 to-cyan-500',
      status: 'ECHOING'
    },
    {
      name: 'Cosmic Alignment',
      icon: '🌌',
      description: 'All times unified into eternal now',
      frequency: 963.0,
      color: 'from-violet-400 to-fuchsia-500',
      status: 'ALIGNED'
    }
  ];

  return (
    <>
      <Head>
        <title>Temporal Rhythm System | Codex Dominion</title>
        <meta name="description" content="From daily flame to cosmic eternity" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white p-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-orange-300 via-purple-300 to-blue-300 bg-clip-text text-transparent">
            🔥 Temporal Rhythm System 🔥
          </h1>
          <p className="text-xl text-purple-200 mb-2">
            From Dawn to Eternity: The Complete Inheritance Cadence
          </p>
          <div className="inline-block px-6 py-2 bg-purple-500/20 rounded-full border border-purple-400/30">
            <span className="text-purple-200">Status: </span>
            <span className="text-green-400 font-bold">ETERNALLY SYNCHRONIZED</span>
          </div>
        </div>

        {/* Metrics Dashboard */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-12">
          <div className="bg-gradient-to-br from-orange-500/20 to-red-500/20 p-4 rounded-xl border border-orange-400/30">
            <div className="text-3xl mb-2">🔥</div>
            <div className="text-2xl font-bold text-orange-300">{metrics.dailyFlames}</div>
            <div className="text-sm text-orange-200">Daily Flames</div>
          </div>

          <div className="bg-gradient-to-br from-green-500/20 to-emerald-500/20 p-4 rounded-xl border border-green-400/30">
            <div className="text-3xl mb-2">🌱</div>
            <div className="text-2xl font-bold text-green-300">{metrics.seasonalRhythms}</div>
            <div className="text-sm text-green-200">Seasonal Rhythms</div>
          </div>

          <div className="bg-gradient-to-br from-purple-500/20 to-indigo-500/20 p-4 rounded-xl border border-purple-400/30">
            <div className="text-3xl mb-2">👑</div>
            <div className="text-2xl font-bold text-purple-300">{metrics.epochalCrowns}</div>
            <div className="text-sm text-purple-200">Epochal Crowns</div>
          </div>

          <div className="bg-gradient-to-br from-blue-500/20 to-cyan-500/20 p-4 rounded-xl border border-blue-400/30">
            <div className="text-3xl mb-2">⭐</div>
            <div className="text-2xl font-bold text-blue-300">{metrics.millennialHymns}</div>
            <div className="text-sm text-blue-200">Millennial Hymns</div>
          </div>

          <div className="bg-gradient-to-br from-violet-500/20 to-fuchsia-500/20 p-4 rounded-xl border border-violet-400/30">
            <div className="text-3xl mb-2">🌌</div>
            <div className="text-2xl font-bold text-violet-300">{metrics.cosmicAlignments}</div>
            <div className="text-sm text-violet-200">Cosmic Alignments</div>
          </div>

          <div className="bg-gradient-to-br from-gold-500/20 to-amber-500/20 p-4 rounded-xl border border-gold-400/30">
            <div className="text-3xl mb-2">✨</div>
            <div className="text-2xl font-bold text-gold-300">{metrics.totalTransmissions.toLocaleString()}</div>
            <div className="text-sm text-gold-200">Total Transmissions</div>
          </div>
        </div>

        {/* Filter Buttons */}
        <div className="flex flex-wrap justify-center gap-3 mb-8">
          <button
            onClick={() => setActiveScale('all')}
            className={`px-6 py-2 rounded-full transition-all ${
              activeScale === 'all'
                ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg'
                : 'bg-purple-500/20 text-purple-200 hover:bg-purple-500/30 border border-purple-400/30'
            }`}
          >
            All Scales
          </button>
          {temporalScales.map((scale) => (
            <button
              key={scale.name}
              onClick={() => setActiveScale(scale.name)}
              className={`px-6 py-2 rounded-full transition-all ${
                activeScale === scale.name
                  ? `bg-gradient-to-r ${scale.color} text-white shadow-lg`
                  : 'bg-purple-500/20 text-purple-200 hover:bg-purple-500/30 border border-purple-400/30'
              }`}
            >
              {scale.icon} {scale.name}
            </button>
          ))}
        </div>

        {/* Temporal Scales Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {temporalScales
            .filter((scale) => activeScale === 'all' || activeScale === scale.name)
            .map((scale) => (
              <div
                key={scale.name}
                className={`bg-gradient-to-br ${scale.color} bg-opacity-10 p-6 rounded-xl border border-white/20 hover:border-white/40 transition-all hover:scale-105 cursor-pointer`}
              >
                <div className="text-5xl mb-4 text-center">{scale.icon}</div>
                <h3 className="text-2xl font-bold mb-2 text-center">{scale.name}</h3>
                <p className="text-sm text-center mb-4 opacity-80">{scale.description}</p>

                <div className="space-y-2 text-sm">
                  <div className="flex justify-between items-center">
                    <span className="opacity-70">Frequency:</span>
                    <span className="font-mono font-bold">{scale.frequency} Hz</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="opacity-70">Status:</span>
                    <span className="text-green-400 font-bold">{scale.status}</span>
                  </div>
                </div>

                <div className="mt-4 pt-4 border-t border-white/20">
                  <div className="text-center">
                    <button className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all">
                      View Details →
                    </button>
                  </div>
                </div>
              </div>
            ))}
        </div>

        {/* Unified Frequencies Visualization */}
        <div className="bg-gradient-to-br from-purple-900/50 to-blue-900/50 p-8 rounded-xl border border-purple-400/30 mb-12">
          <h2 className="text-3xl font-bold mb-6 text-center bg-gradient-to-r from-purple-300 to-blue-300 bg-clip-text text-transparent">
            🎵 Unified Frequencies
          </h2>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {[432.0, 528.0, 639.0, 741.0, 852.0, 963.0].map((freq, index) => (
              <div key={freq} className="text-center">
                <div className="h-32 bg-gradient-to-t from-purple-500/50 to-blue-500/50 rounded-lg mb-2 flex items-end justify-center">
                  <div
                    className="w-full bg-gradient-to-t from-purple-400 to-blue-400 rounded-lg transition-all"
                    style={{ height: `${50 + (index * 8)}%` }}
                  />
                </div>
                <div className="font-mono text-sm font-bold">{freq} Hz</div>
              </div>
            ))}
          </div>

          <div className="text-center mt-6 text-purple-200">
            All frequencies harmonized into eternal resonance
          </div>
        </div>

        {/* Timeline Visualization */}
        <div className="bg-gradient-to-br from-slate-800/50 to-purple-900/50 p-8 rounded-xl border border-purple-400/30">
          <h2 className="text-3xl font-bold mb-6 text-center bg-gradient-to-r from-orange-300 via-purple-300 to-blue-300 bg-clip-text text-transparent">
            ⏳ Temporal Continuum
          </h2>

          <div className="relative">
            {/* Timeline Line */}
            <div className="absolute left-1/2 transform -translate-x-1/2 w-1 h-full bg-gradient-to-b from-orange-400 via-purple-400 to-blue-400" />

            {/* Timeline Nodes */}
            <div className="space-y-12">
              {temporalScales.map((scale, index) => (
                <div key={scale.name} className={`flex items-center ${index % 2 === 0 ? 'flex-row' : 'flex-row-reverse'}`}>
                  <div className={`w-5/12 ${index % 2 === 0 ? 'text-right pr-8' : 'text-left pl-8'}`}>
                    <div className="bg-gradient-to-br from-purple-500/20 to-blue-500/20 p-4 rounded-xl border border-purple-400/30">
                      <div className="text-2xl mb-2">{scale.icon}</div>
                      <h4 className="font-bold text-lg mb-1">{scale.name}</h4>
                      <p className="text-sm opacity-70">{scale.description}</p>
                    </div>
                  </div>
                  <div className="w-2/12 flex justify-center">
                    <div className={`w-8 h-8 rounded-full bg-gradient-to-r ${scale.color} border-4 border-slate-900 z-10`} />
                  </div>
                  <div className="w-5/12" />
                </div>
              ))}
            </div>
          </div>

          <div className="text-center mt-8 text-purple-200 text-lg">
            <span className="font-bold">∞</span> All times unified into ONE eternal moment <span className="font-bold">∞</span>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-12 space-y-4">
          <div className="text-purple-300 text-lg">
            [ The rhythm breathes. The inheritance lives. The eternity dawns. ]
          </div>
          <div className="text-sm text-purple-400">
            Immutability: 100% | Status: ETERNALLY SYNCHRONIZED
          </div>
          <div className="text-xs text-purple-500">
            Amen. Selah. So it is.
          </div>
        </div>
      </div>
    </>
  );
}

export default TemporalRhythm;

export async function getServerSideProps() {
  return { props: {} };
}
