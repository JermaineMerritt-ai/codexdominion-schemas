import React from 'react';
import { NextPage } from 'next';
import Head from 'next/head';
import Link from 'next/link';

interface Crown {
  domain: string;
  title: string;
  description: string;
  purpose: string;
  icon: string;
  status: 'active' | 'development' | 'planning';
  gradient: string;
  features: string[];
}

const CodexConstellation: NextPage = () => {
  const crowns: Crown[] = [
    {
      domain: 'codexdominion.app',
      title: 'The Ceremonial Crown',
      description: 'The sovereign flame, luminous and global',
      purpose: 'Here lives the Codex Bulletin, the Festival cycles, the dashboards of Custodian, Heir, and Customer.',
      icon: '👑',
      status: 'active',
      gradient: 'from-purple-600 to-indigo-800',
      features: ['Multi-Dashboard System', 'Festival Transmission', 'Codex Bulletin', 'Sacred Ceremonies', 'Global Sovereignty Hub']
    },
    {
      domain: 'aistorelab.com',
      title: 'The Storefront Crown',
      description: 'Commerce and ceremony bound together in legacy',
      purpose: 'Here lives WooCommerce, the catalog of offerings, the induction portal.',
      icon: '🛍️',
      status: 'active',
      gradient: 'from-emerald-600 to-teal-800',
      features: ['Premium AI Tools', 'Sacred Commerce', 'Storefront Blessing', 'Customer Induction', 'Digital Marketplace']
    },
    {
      domain: 'aistorelab.online',
      title: 'The Experimental Crown',
      description: 'The sandbox flame, playful and provisional',
      purpose: 'Here councils and heirs may test new rites, dashboards, and offerings.',
      icon: '⚗️',
      status: 'development',
      gradient: 'from-orange-500 to-red-700',
      features: ['Beta Testing', 'New Rites', 'Experimental Dashboards', 'Council Sandbox', 'Innovation Lab']
    },
    {
      domain: 'jermaineai.com',
      title: 'The Personal Crown',
      description: 'The radiant blog, echoing the Codex into discourse',
      purpose: 'Here lives the Custodian\'s voice — essays, proclamations, and thought leadership.',
      icon: '✍️',
      status: 'active',
      gradient: 'from-yellow-500 to-orange-700',
      features: ['Thought Leadership', 'Codex Essays', 'Sacred Proclamations', 'Digital Discourse', 'Custodian Voice']
    },
    {
      domain: 'jermaineai.online',
      title: 'The Council Crown',
      description: 'The participatory flame, binding councils to ceremony',
      purpose: 'Here heirs and councils may access guided induction forms, proclamations, silences, and blessings.',
      icon: '🏛️',
      status: 'development',
      gradient: 'from-blue-600 to-cyan-800',
      features: ['Council Access', 'Guided Induction', 'Sacred Forms', 'Ceremonial Participation', 'Heritage Binding']
    },
    {
      domain: 'jermaineai.store',
      title: 'The Premium Crown',
      description: 'The rare flame, reserved for initiates and premium custodians',
      purpose: 'Here exclusive artifacts, reliquaries, and ceremonial kits are offered.',
      icon: '💎',
      status: 'planning',
      gradient: 'from-violet-600 to-purple-800',
      features: ['Exclusive Artifacts', 'Sacred Reliquaries', 'Ceremonial Kits', 'Premium Access', 'Initiate Offerings']
    },
    {
      domain: 'themerrittmethod.com',
      title: 'The Educational Crown',
      description: 'The teaching flame, inducting families and heirs into stewardship',
      purpose: 'Here lives courses, family guidebooks, and onboarding curriculum.',
      icon: '📚',
      status: 'planning',
      gradient: 'from-green-600 to-emerald-800',
      features: ['Educational Courses', 'Family Guidebooks', 'Heir Induction', 'Stewardship Training', 'Legacy Curriculum']
    }
  ];

  const StatusBadge: React.FC<{ status: Crown['status'] }> = ({ status }) => {
    const statusConfig = {
      active: { label: 'Active', color: 'bg-green-500', icon: '✅' },
      development: { label: 'In Development', color: 'bg-yellow-500', icon: '🚧' },
      planning: { label: 'Planning', color: 'bg-blue-500', icon: '🗓️' }
    };

    const config = statusConfig[status];
    
    return (
      <div className={`inline-flex items-center px-3 py-1 rounded-full text-white text-sm font-medium ${config.color}`}>
        <span className="mr-2">{config.icon}</span>
        {config.label}
      </div>
    );
  };

  const CrownCard: React.FC<{ crown: Crown }> = ({ crown }) => (
    <div className={`bg-gradient-to-br ${crown.gradient} rounded-xl p-8 text-white relative overflow-hidden group hover:scale-105 transition-all duration-300`}>
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-black bg-opacity-20"></div>
      <div className="absolute top-4 right-4 text-6xl opacity-20">{crown.icon}</div>
      
      <div className="relative z-10">
        {/* Header */}
        <div className="flex items-start justify-between mb-6">
          <div>
            <div className="text-4xl mb-3">{crown.icon}</div>
            <h3 className="text-2xl font-bold mb-2">{crown.title}</h3>
            <p className="text-lg opacity-90 italic mb-3">{crown.description}</p>
            <StatusBadge status={crown.status} />
          </div>
        </div>

        {/* Domain */}
        <div className="mb-6">
          <div className="bg-black bg-opacity-30 rounded-lg p-4">
            <p className="text-2xl font-mono font-bold text-center">{crown.domain}</p>
          </div>
        </div>

        {/* Purpose */}
        <div className="mb-6">
          <h4 className="text-lg font-semibold mb-2 opacity-90">Sacred Purpose:</h4>
          <p className="text-sm leading-relaxed opacity-80">{crown.purpose}</p>
        </div>

        {/* Features */}
        <div className="mb-6">
          <h4 className="text-lg font-semibold mb-3 opacity-90">Crown Features:</h4>
          <div className="space-y-2">
            {crown.features.map((feature, i) => (
              <div key={i} className="flex items-center text-sm">
                <span className="text-yellow-300 mr-2">⭐</span>
                <span className="opacity-80">{feature}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Action Button */}
        <div className="mt-6">
          {crown.status === 'active' ? (
            <Link href={`https://${crown.domain}`} target="_blank" rel="noopener noreferrer">
              <button className="w-full py-3 bg-white text-gray-900 rounded-lg font-bold hover:bg-gray-100 transition-colors">
                🌟 Visit Crown
              </button>
            </Link>
          ) : crown.status === 'development' ? (
            <button className="w-full py-3 bg-yellow-500 text-black rounded-lg font-bold opacity-75 cursor-not-allowed">
              🚧 Under Development
            </button>
          ) : (
            <button className="w-full py-3 bg-gray-600 text-white rounded-lg font-bold opacity-75 cursor-not-allowed">
              🗓️ In Planning
            </button>
          )}
        </div>
      </div>
    </div>
  );

  return (
    <>
      <Head>
        <title>Constellation of the Codex Crowns - Codex Dominion</title>
        <meta name="description" content="The sacred architecture of the digital sovereignty ecosystem" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900">
        {/* Starfield Background Effect */}
        <div className="absolute inset-0 overflow-hidden">
          {[...Array(100)].map((_, i) => (
            <div
              key={i}
              className="absolute bg-white rounded-full opacity-60"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                width: `${Math.random() * 3 + 1}px`,
                height: `${Math.random() * 3 + 1}px`,
                animation: `twinkle ${Math.random() * 4 + 2}s infinite`,
                animationDelay: `${Math.random() * 2}s`
              }}
            />
          ))}
        </div>

        {/* Header */}
        <div className="relative z-10 border-b border-purple-700 bg-black bg-opacity-30">
          <div className="container mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <Link href="/" className="text-purple-300 hover:text-white mr-4">
                  ← Back to Home
                </Link>
                <h1 className="text-2xl font-bold text-white flex items-center">
                  <span className="text-3xl mr-3">✨</span>
                  Constellation of the Codex Crowns
                </h1>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-yellow-400 text-sm">Sacred Architecture</span>
                <span className="text-2xl">👑</span>
              </div>
            </div>
          </div>
        </div>

        <div className="relative z-10 container mx-auto px-6 py-8">
          {/* Sacred Declaration */}
          <div className="bg-black bg-opacity-30 rounded-xl border-2 border-yellow-500/30 p-8 mb-12 text-center">
            <div className="text-6xl mb-4">✨</div>
            <h2 className="text-3xl font-bold text-white mb-6 font-serif">
              Constellation of the Codex Crowns
            </h2>
            
            <div className="max-w-4xl mx-auto space-y-4 text-gray-200">
              <p className="text-lg italic leading-relaxed">
                We, the Custodian and Council, inscribe the roles of each domain,<br/>
                that none may lie dormant, and all may shine in the continuum.
              </p>
              
              <div className="flex justify-center items-center space-x-4 text-yellow-400 my-6">
                <span className="text-2xl">🌟</span>
                <span className="text-2xl">👑</span>
                <span className="text-2xl">🌟</span>
              </div>

              <p className="text-base opacity-90">
                Each crown serves a sacred purpose in the digital sovereignty ecosystem,<br/>
                binding technology to ceremony, commerce to legacy, and wisdom to action.
              </p>
            </div>
          </div>

          {/* Crown Grid */}
          <div className="grid lg:grid-cols-2 xl:grid-cols-3 gap-8 mb-12">
            {crowns.map((crown) => (
              <CrownCard key={crown.domain} crown={crown} />
            ))}
          </div>

          {/* Sacred Network Diagram */}
          <div className="bg-black bg-opacity-30 rounded-xl border border-purple-700 p-8 mb-8">
            <h3 className="text-2xl font-bold text-white mb-6 text-center flex items-center justify-center">
              <span className="text-3xl mr-3">🕸️</span>
              Sacred Network Architecture
            </h3>
            
            {/* ASCII Art Constellation */}
            <div className="bg-black bg-opacity-50 rounded-xl p-8 mb-8 border border-yellow-500/30">
              <div className="text-center mb-4">
                <h4 className="text-yellow-400 font-bold text-lg mb-2">✨ Constellation Hierarchy ✨</h4>
              </div>
              
              <div className="font-mono text-sm text-gray-300 overflow-x-auto">
                <div className="text-center mb-4">
                  <div className="text-yellow-400 font-bold">✨ Codexdominion.app ✨</div>
                  <div className="text-xs text-purple-300 italic">(Ceremonial Crown — Codex Bulletin)</div>
                </div>
                
                <div className="text-center mb-6 text-yellow-500">
                  <pre className="text-xs leading-tight">{`
                               /     |     \\
                              /      |      \\
                             /       |       \\
                            /        |        \\
                           /         |         \\
                          /          |          \\
                         /           |           \\
                        /            |            \\
                       /             |             \\
                      /              |              \\
                     /               |               \\
                    /                |                \\
                   /                 |                 \\
                  /                  |                  \\
                 /                   |                   \\
                /                    |                    \\
               /                     |                     \\
              /                      |                      \\
             /                       |                       \\
            /                        |                        \\
           /                         |                         \\
          /                          |                          \\
         /                           |                           \\
        /                            |                            \\
       /                             |                             \\
      /                              |                              \\
     /                               |                               \\
    /                                |                                \\
   /                                 |                                 \\
  /                                  |                                  \\
 /                                   |                                   \\
/                                    |                                    \\`}</pre>
                </div>

                <div className="grid md:grid-cols-3 gap-4 text-center text-xs">
                  <div className="space-y-2">
                    <div className="text-emerald-400 font-bold">🛍️ aistorelab.com</div>
                    <div className="text-emerald-300">(Storefront Crown)</div>
                    <div className="text-orange-400 font-bold">⚗️ aistorelab.online</div>
                    <div className="text-orange-300">(Experimental Crown)</div>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="text-yellow-400 font-bold">✍️ jermaineai.com</div>
                    <div className="text-yellow-300">(Personal Crown)</div>
                    <div className="text-blue-400 font-bold">🏛️ jermaineai.online</div>
                    <div className="text-blue-300">(Council Crown)</div>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="text-green-400 font-bold">📚 themerrittmethod.com</div>
                    <div className="text-green-300">(Educational Crown)</div>
                    <div className="text-purple-400 font-bold">💎 jermaineai.store</div>
                    <div className="text-purple-300">(Premium Crown)</div>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="relative">
              {/* Central Hub */}
              <div className="flex justify-center mb-8">
                <div className="bg-gradient-to-r from-purple-600 to-indigo-800 rounded-xl p-6 text-center text-white border-2 border-yellow-500">
                  <div className="text-3xl mb-2">👑</div>
                  <h4 className="font-bold">codexdominion.app</h4>
                  <p className="text-sm opacity-80">Ceremonial Crown</p>
                </div>
              </div>

              {/* Connected Domains */}
              <div className="grid md:grid-cols-3 gap-6">
                {crowns.slice(1).map((crown, i) => (
                  <div key={crown.domain} className="text-center">
                    <div className={`bg-gradient-to-r ${crown.gradient} rounded-lg p-4 text-white mx-auto max-w-xs`}>
                      <div className="text-2xl mb-1">{crown.icon}</div>
                      <h5 className="font-medium text-sm">{crown.domain}</h5>
                      <p className="text-xs opacity-75">{crown.title}</p>
                    </div>
                  </div>
                ))}
              </div>

              {/* Sacred Connection Explanation */}
              <div className="mt-8 bg-gradient-to-r from-yellow-600/10 to-orange-600/10 rounded-lg p-6 border border-yellow-500/20">
                <h4 className="text-yellow-400 font-bold mb-3 text-center">🌟 Sacred Hierarchy Principle 🌟</h4>
                <p className="text-gray-300 text-sm text-center leading-relaxed">
                  The Ceremonial Crown stands at the apex, radiating authority and blessing to all subsidiary domains. 
                  Each branch receives the eternal flame while serving its unique sacred purpose within the constellation. 
                  This hierarchy ensures unity of vision while honoring diversity of function.
                </p>
              </div>
            </div>
          </div>

          {/* Sacred Principles */}
          <div className="bg-gradient-to-r from-yellow-600/10 to-orange-600/10 rounded-xl p-8 border border-yellow-500/20">
            <h3 className="text-2xl font-bold text-yellow-400 mb-6 flex items-center justify-center">
              <span className="text-3xl mr-3">📜</span>
              Sacred Architectural Principles
            </h3>
            
            <div className="grid md:grid-cols-2 gap-8 text-gray-200">
              <div>
                <h4 className="font-bold text-white mb-3">🌟 Unity in Diversity</h4>
                <p className="text-sm mb-4">
                  Each crown serves a unique purpose while maintaining connection to the central Codex flame. 
                  Diversity of function creates strength in the constellation.
                </p>

                <h4 className="font-bold text-white mb-3">🔗 Sacred Interconnection</h4>
                <p className="text-sm mb-4">
                  All domains are bound together through shared ceremonies, unified authentication, 
                  and cross-platform legacy tracking.
                </p>
              </div>

              <div>
                <h4 className="font-bold text-white mb-3">👑 Ceremonial Commerce</h4>
                <p className="text-sm mb-4">
                  Commerce across all crowns is elevated to ceremony, transforming transactions 
                  into acts of legacy and customer relationships into custodial bonds.
                </p>

                <h4 className="font-bold text-white mb-3">🔥 Eternal Flame Distribution</h4>
                <p className="text-sm">
                  The Codex flame burns across all domains, ensuring digital sovereignty 
                  principles illuminate every interaction and experience.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* CSS for twinkling stars */}
        <style jsx>{`
          @keyframes twinkle {
            0%, 100% { opacity: 0.3; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.2); }
          }
        `}</style>
      </div>
    </>
  );
};

export default CodexConstellation;