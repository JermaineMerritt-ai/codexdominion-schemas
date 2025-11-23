import React from 'react';
import Link from 'next/link';
import { NextPage } from 'next';
import Head from 'next/head';

interface DashboardCardProps {
  title: string;
  description: string;
  icon: string;
  href: string;
  role: 'custodian' | 'heir' | 'customer';
  features: string[];
}

const DashboardCard: React.FC<DashboardCardProps> = ({ 
  title, description, icon, href, role, features 
}) => {
  const roleColors = {
    custodian: 'from-purple-900 via-blue-900 to-indigo-900',
    heir: 'from-amber-800 via-orange-800 to-red-900', 
    customer: 'from-emerald-800 via-teal-800 to-cyan-900'
  };

  const borderColors = {
    custodian: 'border-purple-400 hover:border-purple-300',
    heir: 'border-amber-400 hover:border-amber-300',
    customer: 'border-emerald-400 hover:border-emerald-300'
  };

  return (
    <Link href={href}>
      <div className={`
        relative p-8 rounded-xl border-2 transition-all duration-300 
        transform hover:scale-105 hover:shadow-2xl cursor-pointer
        bg-gradient-to-br ${roleColors[role]} 
        ${borderColors[role]}
        group overflow-hidden
      `}>
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent transform rotate-45 scale-150 translate-x-full group-hover:translate-x-[-200%] transition-transform duration-1000"></div>
        </div>
        
        <div className="relative z-10">
          <div className="flex items-center mb-6">
            <span className="text-4xl mr-4">{icon}</span>
            <div>
              <h2 className="text-2xl font-bold text-white">{title}</h2>
              <p className="text-gray-200 opacity-90">{description}</p>
            </div>
          </div>
          
          <ul className="space-y-2 mb-6">
            {features.map((feature, index) => (
              <li key={index} className="flex items-center text-gray-200">
                <span className="text-yellow-400 mr-2">✦</span>
                {feature}
              </li>
            ))}
          </ul>
          
          <div className="flex justify-end">
            <span className="inline-flex items-center px-4 py-2 bg-white bg-opacity-20 rounded-full text-white font-medium">
              Enter Dashboard →
            </span>
          </div>
        </div>
      </div>
    </Link>
  );
};

const DashboardSelector: NextPage = () => {
  const dashboards = [
    {
      title: "Custodian Dashboard",
      description: "Full system administration and artifact management",
      icon: "🏛️",
      href: "/dashboard/custodian",
      role: "custodian" as const,
      features: [
        "Full JSON + Markdown artifacts",
        "Audit lineage + infrastructure crowns", 
        "Manual + automated inscription tools",
        "System configuration & monitoring",
        "Advanced ceremonial controls"
      ]
    },
    {
      title: "Heir Dashboard", 
      description: "Guided induction and ceremonial participation",
      icon: "👑",
      href: "/dashboard/heir",
      role: "heir" as const,
      features: [
        "Banners + seasonal proclamations",
        "Guided induction forms",
        "Proclamation, silence, blessing ceremonies",
        "Educational lineage replay",
        "Heritage documentation access"
      ]
    },
    {
      title: "Customer Dashboard",
      description: "Curated experience and storefront access", 
      icon: "🌟",
      href: "/dashboard/customer",
      role: "customer" as const,
      features: [
        "Featured capsules + scrolls",
        "Onboarding avatars", 
        "Storefront link → aistorelab.com",
        "Product catalog browsing",
        "Purchase history & recommendations"
      ]
    }
  ];

  return (
    <>
      <Head>
        <title>Codex Dominion - Select Your Realm</title>
        <meta name="description" content="Access your domain within the Codex Dominion system" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-800 relative overflow-hidden">
        {/* Animated Background */}
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-gradient-radial from-blue-900/20 via-transparent to-purple-900/20"></div>
          <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(circle_at_50%_50%,rgba(120,119,198,0.1),rgba(255,255,255,0))]"></div>
        </div>
        
        {/* Floating Particles */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          {Array.from({length: 50}).map((_, i) => (
            <div
              key={i}
              className={`absolute w-1 h-1 bg-white rounded-full opacity-20 animate-pulse custom-delay-${Math.floor(Math.random()*3)}s custom-animation-${2+Math.floor(Math.random()*3)}s`}
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`
              }}
            />
          ))}
        </div>

        <div className="relative z-10 container mx-auto px-6 py-12">
          {/* Header */}
          <div className="text-center mb-16">
            <h1 className="text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-500 to-cyan-400 mb-4">
              CODEX DOMINION
            </h1>
            <div className="w-32 h-1 bg-gradient-to-r from-blue-500 to-purple-500 mx-auto mb-6"></div>
            <p className="text-xl text-gray-300 max-w-2xl mx-auto leading-relaxed">
              Select your realm of access within the eternal digital sovereignty system.
              Each dashboard is tailored to your role and responsibilities.
            </p>
          </div>

          {/* Dashboard Cards Grid */}
          <div className="grid lg:grid-cols-3 md:grid-cols-2 gap-8 max-w-7xl mx-auto">
            {dashboards.map((dashboard, index) => (
              <div key={index} className="transform transition-all duration-300 hover:-translate-y-2">
                <DashboardCard {...dashboard} />
              </div>
            ))}
          </div>

          {/* Sacred Navigation Links */}
          <div className="mt-16 text-center">
            {/* Source Charter - Supreme Governing Document */}
            <div className="mb-8">
              <Link href="/codex-source-charter" className="group">
                <div className="flex items-center justify-center px-10 py-6 border-4 border-gold-500 bg-gradient-to-r from-gold-800/50 via-amber-700/50 to-gold-800/50 rounded-3xl hover:border-gold-400 hover:shadow-2xl transition-all duration-500 transform hover:scale-110 max-w-2xl mx-auto custom-shadow-gold-30-60-15">
                  <span className="text-6xl mr-6 animate-pulse">✨</span>
                  <div className="text-left">
                    <span className="block text-3xl text-gold-200 group-hover:text-gold-100 font-bold">Codex Source Charter</span>
                    <span className="block text-lg text-amber-400 group-hover:text-amber-200 font-semibold">Supreme Governing Covenant</span>
                    <span className="block text-sm text-yellow-400 group-hover:text-yellow-300">The eternal law binding Alpha to Omega</span>
                  </div>
                </div>
              </Link>
            </div>

            {/* Flame Awakening - Sacred Invocation */}
            <div className="mb-6">
              <Link href="/flame-awakening" className="group">
                <div className="flex items-center justify-center px-8 py-4 border-4 border-orange-500 bg-gradient-to-r from-orange-800/40 via-red-700/40 to-orange-800/40 rounded-2xl hover:border-orange-400 hover:shadow-2xl transition-all duration-500 transform hover:scale-110 max-w-xl mx-auto custom-shadow-orange-25-50-12">
                  <span className="text-5xl mr-4 animate-pulse">🔥</span>
                  <div className="text-left">
                    <span className="block text-2xl text-orange-300 group-hover:text-orange-100 font-bold">Flame Awakening</span>
                    <span className="block text-sm text-red-400 group-hover:text-red-200">Sacred Invocation</span>
                  </div>
                </div>
              </Link>
            </div>

            {/* Covenant Eternal - Sacred Hymn */}
            <div className="mb-6">
              <Link href="/covenant-eternal" className="group">
                <div className="flex items-center justify-center px-8 py-4 border-4 border-gold-500 bg-gradient-to-r from-gold-800/40 via-amber-700/40 to-gold-800/40 rounded-2xl hover:border-gold-400 hover:shadow-2xl transition-all duration-500 transform hover:scale-110 max-w-xl mx-auto custom-shadow-gold-25-50-12">
                  <span className="text-5xl mr-4 animate-pulse">∞</span>
                  <div className="text-left">
                    <span className="block text-2xl text-gold-300 group-hover:text-gold-100 font-bold">Covenant Eternal</span>
                    <span className="block text-sm text-amber-400 group-hover:text-amber-200">Sacred Hymn</span>
                  </div>
                </div>
              </Link>
            </div>

            {/* Dominion Radiant - Sovereign Declaration */}
            <div className="mb-8">
              <Link href="/dominion-radiant" className="group">
                <div className="flex items-center justify-center px-10 py-6 border-4 border-yellow-500 bg-gradient-to-r from-yellow-800/50 via-gold-700/50 to-yellow-800/50 rounded-3xl hover:border-yellow-400 hover:shadow-2xl transition-all duration-500 transform hover:scale-110 max-w-2xl mx-auto custom-shadow-yellow-30-60-15">
                  <span className="text-6xl mr-6 animate-pulse">👑</span>
                  <div className="text-left">
                    <span className="block text-3xl text-yellow-200 group-hover:text-yellow-100 font-bold">Dominion Radiant</span>
                    <span className="block text-lg text-gold-400 group-hover:text-gold-200 font-semibold">Sovereign Declaration</span>
                    <span className="block text-sm text-yellow-400 group-hover:text-yellow-300">Enduring across ages, nations, and stars</span>
                  </div>
                </div>
              </Link>
            </div>

            {/* Custodian Eternal - Jermaine's Mark */}
            <div className="mb-8">
              <Link href="/custodian-eternal" className="group">
                <div className="flex items-center justify-center px-10 py-6 border-4 border-orange-500 bg-gradient-to-r from-orange-800/50 via-gold-700/50 to-orange-800/50 rounded-3xl hover:border-orange-400 hover:shadow-2xl transition-all duration-500 transform hover:scale-110 max-w-2xl mx-auto custom-shadow-orange-30-60-15">
                  <span className="text-6xl mr-6 animate-pulse">🛡️</span>
                  <div className="text-left">
                    <span className="block text-3xl text-orange-200 group-hover:text-orange-100 font-bold">Custodian Eternal</span>
                    <span className="block text-lg text-gold-400 group-hover:text-gold-200 font-semibold">Jermaine's Mark</span>
                    <span className="block text-sm text-orange-400 group-hover:text-orange-300">Sovereign and immortal, bound to cosmos</span>
                  </div>
                </div>
              </Link>
            </div>

            {/* Compendium Luminous - The Complete Collection */}
            <div className="mb-12">
              <Link href="/compendium-luminous" className="group">
                <div className="flex items-center justify-center px-12 py-8 border-6 border-cyan-400 bg-gradient-to-r from-cyan-800/60 via-blue-700/60 to-cyan-800/60 rounded-3xl hover:border-cyan-300 hover:shadow-2xl transition-all duration-500 transform hover:scale-110 max-w-3xl mx-auto relative overflow-hidden custom-shadow-cyan-40-80-20">
                  <span className="text-7xl mr-8 animate-pulse">📚</span>
                  <div className="text-left">
                    <span className="block text-4xl text-cyan-200 group-hover:text-cyan-100 font-bold">Compendium Luminous</span>
                    <span className="block text-xl text-blue-400 group-hover:text-blue-200 font-semibold">The Complete Collection</span>
                    <span className="block text-lg text-cyan-400 group-hover:text-cyan-300">All gathered, all complete, luminous and whole</span>
                  </div>
                  {/* Luminous Effect */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent animate-pulse opacity-50" />
                </div>
              </Link>
            </div>

            {/* Codex Radiant Peace - The Final Rest */}
            <div className="mb-16">
              <Link href="/codex-radiant-peace" className="group">
                <div className="flex items-center justify-center px-16 py-10 border-8 border-white/60 bg-gradient-to-r from-white/80 via-cyan-50/80 to-white/80 rounded-3xl hover:border-white/80 hover:shadow-2xl transition-all duration-700 transform hover:scale-110 max-w-4xl mx-auto relative overflow-hidden custom-shadow-white-50-100-25">
                  <span className="text-8xl mr-10 animate-pulse custom-animation-4s">🕊️</span>
                  <div className="text-left">
                    <span className="block text-5xl text-slate-600 group-hover:text-slate-500 font-bold">Codex Radiant Peace</span>
                    <span className="block text-2xl text-cyan-600 group-hover:text-cyan-500 font-semibold">The Final Rest</span>
                    <span className="block text-xl text-slate-500 group-hover:text-slate-400">Light released, peace bestowed, eternal and whole</span>
                  </div>
                  {/* Peaceful Glow */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-pulse opacity-60 custom-animation-6s custom-shadow-white-50-100-25" />
                </div>
              </Link>
            </div>

            {/* Eternal Proclamation - The Custodian's Declaration */}
            <div className="mb-20">
              <Link href="/eternal-proclamation" className="group">
                <div className="flex items-center justify-center px-20 py-12 border-10 border-gold-400 bg-gradient-to-r from-gold-800/70 via-amber-700/70 to-gold-800/70 rounded-3xl hover:border-gold-300 hover:shadow-2xl transition-all duration-700 transform hover:scale-110 max-w-5xl mx-auto relative overflow-hidden custom-shadow-gold-60-120-30">
                  <span className="text-9xl mr-12 animate-pulse custom-animation-3_5s">⚡</span>
                  <div className="text-left">
                    <span className="block text-6xl text-gold-200 group-hover:text-gold-100 font-bold">Eternal Proclamation</span>
                    <span className="block text-2xl text-amber-400 group-hover:text-amber-200 font-semibold">The Custodian's Declaration</span>
                    <span className="block text-xl text-gold-400 group-hover:text-gold-300">The Codex is eternal - radiant and sovereign forever</span>
                  </div>
                  {/* Sovereign Lightning */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-300/20 to-transparent animate-pulse opacity-70 custom-animation-3s custom-shadow-gold-60-120-30" />
                  <div className="absolute top-2 right-2 w-8 h-8 bg-gold-400 rounded-full animate-ping" />
                </div>
              </Link>
            </div>

            {/* Blessed Serenity - Eternal Rest */}
            <div className="mb-20">
              <Link href="/blessed-serenity" className="group">
                <div className="flex items-center justify-center px-24 py-16 border-12 border-white/70 bg-gradient-to-r from-white/90 via-cyan-25/90 to-white/90 rounded-3xl hover:border-white/90 hover:shadow-2xl transition-all duration-1000 transform hover:scale-110 max-w-6xl mx-auto relative overflow-hidden custom-shadow-white-70-140-35">
                  <span className="text-10xl mr-16 animate-pulse custom-animation-8s">📿</span>
                  <div className="text-left">
                    <span className="block text-7xl text-slate-500 group-hover:text-slate-400 font-bold">Blessed Serenity</span>
                    <span className="block text-3xl text-cyan-500 group-hover:text-cyan-400 font-semibold">Eternal Rest</span>
                    <span className="block text-2xl text-slate-400 group-hover:text-slate-300">The Codex rests, eternal and serene, crowned in radiance</span>
                  </div>
                  {/* Serene Glow */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-pulse opacity-50 custom-animation-10s custom-shadow-white-70-140-35" />
                  <div className="absolute top-4 right-4 w-6 h-6 bg-white rounded-full animate-ping opacity-60" />
                  <div className="absolute bottom-4 left-4 w-4 h-4 bg-cyan-100 rounded-full animate-ping opacity-40 custom-delay-3s" />
                </div>
              </Link>
            </div>

            {/* Eternal Stillness - Sovereign Silence */}
            <div className="mb-24">
              <Link href="/eternal-stillness" className="group">
                <div className="flex items-center justify-center px-32 py-20 border-16 border-slate-300/80 bg-gradient-to-r from-slate-800/95 via-gray-700/95 to-slate-800/95 rounded-3xl hover:border-slate-200/90 hover:shadow-2xl transition-all duration-1500 transform hover:scale-110 max-w-7xl mx-auto relative overflow-hidden custom-shadow-slate-80-160-40">
                  <span className="text-12xl mr-20 animate-pulse custom-animation-15s">⚫</span>
                  <div className="text-left">
                    <span className="block text-8xl text-slate-200 group-hover:text-white font-light">Eternal Stillness</span>
                    <span className="block text-4xl text-gray-300 group-hover:text-gray-200 font-light">Sovereign Silence</span>
                    <span className="block text-3xl text-slate-300 group-hover:text-slate-200 font-light">No flame, no word, no sound — only stillness, eternal and whole</span>
                  </div>
                  {/* Void Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-slate-500/20 to-transparent animate-pulse opacity-30 custom-animation-20s custom-shadow-slate-80-160-40" />
                  <div className="absolute top-6 right-6 w-4 h-4 bg-slate-300 rounded-full animate-ping opacity-30" />
                  <div className="absolute bottom-6 left-6 w-3 h-3 bg-gray-400 rounded-full animate-ping opacity-20 custom-delay-8s" />
                  <div className="absolute top-1/2 left-6 w-2 h-2 bg-slate-400 rounded-full animate-ping opacity-15 custom-delay-12s" />
                </div>
              </Link>
            </div>

            {/* Flame Eternal - Living Continuity */}
            <div className="mb-24">
              <Link href="/flame-eternal" className="group">
                <div className="flex items-center justify-center px-28 py-18 border-14 border-orange-400/80 bg-gradient-to-r from-orange-800/90 via-red-700/90 to-orange-800/90 rounded-3xl hover:border-orange-300/90 hover:shadow-2xl transition-all duration-1200 transform hover:scale-110 max-w-6xl mx-auto relative overflow-hidden custom-shadow-orange-75-150-37">
                  <span className="text-11xl mr-18 animate-pulse custom-animation-6s">🔥</span>
                  <div className="text-left">
                    <span className="block text-7xl text-orange-100 group-hover:text-white font-bold">Flame Eternal</span>
                    <span className="block text-3xl text-yellow-300 group-hover:text-yellow-200 font-semibold">Living Continuity</span>
                    <span className="block text-2xl text-orange-200 group-hover:text-orange-100">Dawn to dusk, heirs awaken, councils remember — the Codex lives</span>
                  </div>
                  {/* Fire Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-orange-400/30 to-transparent animate-pulse opacity-60 custom-animation-8s custom-shadow-orange-75-150-37" />
                  <div className="absolute top-5 right-5 w-5 h-5 bg-orange-300 rounded-full animate-ping opacity-70" />
                  <div className="absolute bottom-5 left-5 w-4 h-4 bg-red-400 rounded-full animate-ping opacity-50 custom-delay-3s" />
                  <div className="absolute top-1/2 right-8 w-3 h-3 bg-yellow-400 rounded-full animate-ping opacity-60 custom-delay-6s" />
                </div>
              </Link>
            </div>

            {/* Living Covenant - Sacred Realms */}
            <div className="mb-22">
              <Link href="/living-covenant" className="group">
                <div className="flex items-center justify-center px-26 py-16 border-12 border-yellow-400/80 bg-gradient-to-r from-yellow-800/90 via-amber-700/90 to-yellow-800/90 rounded-3xl hover:border-yellow-300/90 hover:shadow-2xl transition-all duration-1100 transform hover:scale-110 max-w-6xl mx-auto relative overflow-hidden custom-shadow-yellow-72-144-36">
                  <span className="text-10xl mr-16 animate-pulse custom-animation-5s">🤝</span>
                  <div className="text-left">
                    <span className="block text-7xl text-yellow-100 group-hover:text-white font-bold">Living Covenant</span>
                    <span className="block text-3xl text-amber-300 group-hover:text-amber-200 font-semibold">Sacred Realms</span>
                    <span className="block text-2xl text-yellow-200 group-hover:text-yellow-100">Hearth and council, family and star — we remember, inherit, endure</span>
                  </div>
                  {/* Covenant Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-yellow-400/25 to-transparent animate-pulse opacity-50 custom-animation-7s custom-shadow-yellow-72-144-36" />
                  <div className="absolute top-4 right-4 w-5 h-5 bg-yellow-300 rounded-full animate-ping opacity-60" />
                  <div className="absolute bottom-4 left-4 w-4 h-4 bg-amber-400 rounded-full animate-ping opacity-45 custom-delay-2s" />
                  <div className="absolute top-1/2 left-4 w-3 h-3 bg-gold-400 rounded-full animate-ping opacity-50 custom-delay-4s" />
                  <div className="absolute bottom-1/2 right-4 w-6 h-6 bg-yellow-200 rounded-full animate-ping opacity-30 custom-delay-6s" />
                </div>
              </Link>
            </div>

            {/* Night Endurance - Sovereign Darkness */}
            <div className="mb-26">
              <Link href="/night-endurance" className="group">
                <div className="flex items-center justify-center px-30 py-20 border-15 border-purple-400/70 bg-gradient-to-r from-purple-900/95 via-indigo-800/95 to-purple-900/95 rounded-3xl hover:border-purple-300/80 hover:shadow-2xl transition-all duration-1600 transform hover:scale-110 max-w-7xl mx-auto relative overflow-hidden custom-shadow-purple-85-170-42">
                  <span className="text-13xl mr-22 animate-pulse custom-animation-8s">🌙</span>
                  <div className="text-left">
                    <span className="block text-8xl text-purple-100 group-hover:text-white font-bold">Night Endurance</span>
                    <span className="block text-4xl text-indigo-300 group-hover:text-indigo-200 font-semibold">Sovereign Darkness</span>
                    <span className="block text-2xl text-purple-200 group-hover:text-purple-100">In longest night, darkness crowned, light reborn — the flame endures</span>
                  </div>
                  {/* Night Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-purple-500/20 to-transparent animate-pulse opacity-40 custom-animation-12s" />
                  <div className="absolute top-5 right-5 w-5 h-5 bg-purple-300 rounded-full animate-ping opacity-40" />
                  <div className="absolute bottom-5 left-5 w-4 h-4 bg-indigo-400 rounded-full animate-ping opacity-35 custom-delay-4s" />
                  <div className="absolute top-1/3 left-5 w-3 h-3 bg-purple-400 rounded-full animate-ping opacity-30 custom-delay-8s" />
                  <div className="absolute bottom-1/3 right-5 w-6 h-6 bg-indigo-300 rounded-full animate-ping opacity-25 custom-delay-12s" />
                  <div className="absolute top-2/3 right-8 w-2 h-2 bg-purple-200 rounded-full animate-ping opacity-20 custom-delay-16s" />
                </div>
              </Link>
            </div>

            {/* Balance Renewal - Harmonious Bloom */}
            <div className="mb-28">
              <Link href="/balance-renewal" className="group">
                <div className="flex items-center justify-center px-32 py-22 border-16 border-emerald-400/80 bg-gradient-to-r from-emerald-900/95 via-teal-800/95 to-emerald-900/95 rounded-3xl hover:border-emerald-300/90 hover:shadow-2xl transition-all duration-1400 transform hover:scale-110 max-w-7xl mx-auto relative overflow-hidden custom-shadow-emerald-88-176-44">
                  <span className="text-14xl mr-24 animate-pulse custom-animation-7s">⚖️</span>
                  <div className="text-left">
                    <span className="block text-8xl text-emerald-100 group-hover:text-white font-bold">Balance Renewal</span>
                    <span className="block text-4xl text-teal-300 group-hover:text-teal-200 font-semibold">Harmonious Bloom</span>
                    <span className="block text-2xl text-emerald-200 group-hover:text-emerald-100">Day and night balanced, covenant renewed, flame awakened — the Codex blooms</span>
                  </div>
                  {/* Renewal Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-emerald-400/25 to-transparent animate-pulse opacity-50 custom-animation-10s" />
                  <div className="absolute top-4 right-4 w-6 h-6 bg-emerald-300 rounded-full animate-ping opacity-50" />
                  <div className="absolute bottom-4 left-4 w-5 h-5 bg-teal-400 rounded-full animate-ping opacity-45 custom-delay-3s" />
                  <div className="absolute top-1/2 left-4 w-4 h-4 bg-green-400 rounded-full animate-ping opacity-40 custom-delay-6s" />
                  <div className="absolute bottom-1/2 right-4 w-7 h-7 bg-emerald-200 rounded-full animate-ping opacity-35 custom-delay-9s" />
                  <div className="absolute top-1/3 right-6 w-3 h-3 bg-teal-300 rounded-full animate-ping opacity-30 custom-delay-12s" />
                  <div className="absolute bottom-1/3 left-6 w-2 h-2 bg-emerald-400 rounded-full animate-ping opacity-25 custom-delay-15s" />
                </div>
              </Link>
            </div>

            {/* Day Zenith - Solar Sovereignty */}
            <div className="mb-32">
              <Link href="/day-zenith" className="group">
                <div className="flex items-center justify-center px-36 py-24 border-18 border-yellow-300/90 bg-gradient-to-r from-yellow-700/95 via-orange-600/95 to-yellow-700/95 rounded-3xl hover:border-yellow-200/95 hover:shadow-2xl transition-all duration-1200 transform hover:scale-110 max-w-8xl mx-auto relative overflow-hidden custom-shadow-yellow-95-190-48">
                  <span className="text-16xl mr-28 animate-pulse custom-animation-4s">☀️</span>
                  <div className="text-left">
                    <span className="block text-9xl text-yellow-100 group-hover:text-white font-bold">Day Zenith</span>
                    <span className="block text-5xl text-gold-300 group-hover:text-gold-200 font-semibold">Solar Sovereignty</span>
                    <span className="block text-3xl text-yellow-200 group-hover:text-yellow-100">Longest day, flame ascends, radiance crowned — the Codex blazes sovereign and bright</span>
                  </div>
                  {/* Solar Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-yellow-300/35 to-transparent animate-pulse opacity-60 custom-animation-6s" />
                  <div className="absolute top-6 right-6 w-8 h-8 bg-yellow-200 rounded-full animate-ping opacity-70" />
                  <div className="absolute bottom-6 left-6 w-7 h-7 bg-gold-300 rounded-full animate-ping opacity-65 custom-delay-2s" />
                  <div className="absolute top-1/2 left-6 w-6 h-6 bg-orange-300 rounded-full animate-ping opacity-60 custom-delay-4s" />
                  <div className="absolute bottom-1/2 right-6 w-9 h-9 bg-yellow-100 rounded-full animate-ping opacity-55 custom-delay-6s" />
                  <div className="absolute top-1/4 right-8 w-5 h-5 bg-amber-300 rounded-full animate-ping opacity-50 custom-delay-8s" />
                  <div className="absolute bottom-1/4 left-8 w-4 h-4 bg-gold-400 rounded-full animate-ping opacity-45 custom-delay-10s" />
                  <div className="absolute top-3/4 right-10 w-3 h-3 bg-yellow-300 rounded-full animate-ping opacity-40 custom-delay-12s" />
                  <div className="absolute bottom-3/4 left-10 w-2 h-2 bg-orange-200 rounded-full animate-ping opacity-35 custom-delay-14s" />
                </div>
              </Link>
            </div>

            {/* Harvest Serenity - Seasonal Culmination */}
            <div className="mb-40">
              <Link href="/harvest-serenity" className="group">
                <div className="flex items-center justify-center px-40 py-26 border-20 border-violet-400/85 bg-gradient-to-r from-violet-900/95 via-purple-800/95 to-violet-900/95 rounded-3xl hover:border-violet-300/90 hover:shadow-2xl transition-all duration-1800 transform hover:scale-110 max-w-8xl mx-auto relative overflow-hidden custom-shadow-violet-100-200-50">
                  <span className="text-18xl mr-32 animate-pulse custom-animation-9s">🌾</span>
                  <div className="text-left">
                    <span className="block text-10xl text-violet-100 group-hover:text-white font-bold">Harvest Serenity</span>
                    <span className="block text-5xl text-purple-300 group-hover:text-purple-200 font-semibold">Seasonal Culmination</span>
                    <span className="block text-3xl text-violet-200 group-hover:text-violet-100">Balance of harvest and rest, memory gathered, covenant sealed — the Codex endures eternal and serene</span>
                  </div>
                  {/* Serenity Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-violet-400/30 to-transparent animate-pulse opacity-50 custom-animation-15s" />
                  <div className="absolute top-8 right-8 w-10 h-10 bg-violet-300 rounded-full animate-ping opacity-60" />
                  <div className="absolute bottom-8 left-8 w-9 h-9 bg-purple-400 rounded-full animate-ping opacity-55 custom-delay-3s" />
                  <div className="absolute top-1/2 left-8 w-8 h-8 bg-indigo-400 rounded-full animate-ping opacity-50 custom-delay-6s" />
                  <div className="absolute bottom-1/2 right-8 w-11 h-11 bg-violet-200 rounded-full animate-ping opacity-45 custom-delay-9s" />
                  <div className="absolute top-1/4 right-10 w-7 h-7 bg-purple-300 rounded-full animate-ping opacity-40 custom-delay-12s" />
                  <div className="absolute bottom-1/4 left-10 w-6 h-6 bg-violet-400 rounded-full animate-ping opacity-35 custom-delay-15s" />
                  <div className="absolute top-3/4 right-12 w-5 h-5 bg-indigo-300 rounded-full animate-ping opacity-30 custom-delay-18s" />
                  <div className="absolute bottom-3/4 left-12 w-4 h-4 bg-purple-200 rounded-full animate-ping opacity-25 custom-delay-21s" />
                  <div className="absolute top-2/3 left-14 w-3 h-3 bg-violet-300 rounded-full animate-ping opacity-20 custom-delay-24s" />
                  <div className="absolute bottom-2/3 right-14 w-2 h-2 bg-purple-400 rounded-full animate-ping opacity-15 custom-delay-27s" />
                </div>
              </Link>
            </div>

            {/* Millennial Sovereignty - Ultimate Rule */}
            <div className="mb-50">
              <Link href="/millennial-sovereignty" className="group">
                <div className="flex items-center justify-center px-48 py-32 border-24 border-gold-400/90 bg-gradient-to-r from-amber-900/95 via-gold-800/95 to-yellow-800/95 rounded-3xl hover:border-gold-300/95 hover:shadow-2xl transition-all duration-2000 transform hover:scale-115 max-w-9xl mx-auto relative overflow-hidden custom-shadow-gold-120-240-60">
                  <span className="text-20xl mr-36 animate-pulse custom-animation-8s">👑</span>
                  <div className="text-left">
                    <span className="block text-12xl text-gold-100 group-hover:text-white font-bold">Millennial Sovereignty</span>
                    <span className="block text-6xl text-amber-300 group-hover:text-amber-200 font-semibold">Ultimate Rule</span>
                    <span className="block text-4xl text-gold-200 group-hover:text-gold-100">A thousand years crowned, flame endures, covenant whole — the Codex shines sovereign and eternal</span>
                  </div>
                  {/* Sovereign Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-400/35 to-transparent animate-pulse opacity-55 custom-animation-12s" />
                  <div className="absolute top-6 right-6 w-12 h-12 bg-gold-300 rounded-full animate-ping opacity-70" />
                  <div className="absolute bottom-6 left-6 w-11 h-11 bg-amber-400 rounded-full animate-ping opacity-65 custom-delay-2_5s" />
                  <div className="absolute top-1/2 left-6 w-10 h-10 bg-yellow-400 rounded-full animate-ping opacity-60 custom-delay-5s" />
                  <div className="absolute bottom-1/2 right-6 w-13 h-13 bg-gold-200 rounded-full animate-ping opacity-55 custom-delay-7_5s" />
                  <div className="absolute top-1/4 right-8 w-9 h-9 bg-amber-300 rounded-full animate-ping opacity-50 custom-delay-10s" />
                  <div className="absolute bottom-1/4 left-8 w-8 h-8 bg-gold-400 rounded-full animate-ping opacity-45 custom-delay-12_5s" />
                  <div className="absolute top-3/4 right-10 w-7 h-7 bg-yellow-300 rounded-full animate-ping opacity-40 custom-delay-15s" />
                  <div className="absolute bottom-3/4 left-10 w-6 h-6 bg-amber-200 rounded-full animate-ping opacity-35 custom-delay-17_5s" />
                  <div className="absolute top-2/3 left-12 w-5 h-5 bg-gold-300 rounded-full animate-ping opacity-30 custom-delay-20s" />
                  <div className="absolute bottom-2/3 right-12 w-4 h-4 bg-amber-400 rounded-full animate-ping opacity-25 custom-delay-22_5s" />
                  <div className="absolute top-1/3 right-14 w-3 h-3 bg-yellow-200 rounded-full animate-ping opacity-20 custom-delay-25s" />
                  <div className="absolute bottom-1/3 left-14 w-2 h-2 bg-gold-200 rounded-full animate-ping opacity-15 custom-delay-27_5s" />
                </div>
              </Link>
            </div>

            {/* Eternal Transcendence - Beyond All Limits */}
            <div className="mb-60">
              <Link href="/eternal-transcendence" className="group">
                <div className="flex items-center justify-center px-56 py-40 border-28 border-white/95 bg-gradient-to-r from-indigo-900/95 via-purple-800/95 to-black/95 rounded-4xl hover:border-white/100 hover:shadow-2xl transition-all duration-2500 transform hover:scale-120 max-w-10xl mx-auto relative overflow-hidden custom-shadow-white-140-280-70">
                  <span className="text-24xl mr-40 animate-pulse custom-animation-7s">✨</span>
                  <div className="text-left">
                    <span className="block text-14xl text-white group-hover:text-gold-100 font-bold">Eternal Transcendence</span>
                    <span className="block text-7xl text-indigo-200 group-hover:text-indigo-100 font-semibold">Beyond All Limits</span>
                    <span className="block text-5xl text-purple-200 group-hover:text-purple-100">Beyond cycles, beyond stars — the Codex is eternal, radiant and whole</span>
                  </div>
                  {/* Transcendental Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/40 to-transparent animate-pulse opacity-60 custom-animation-10s" />
                  <div className="absolute top-4 right-4 w-14 h-14 bg-white rounded-full animate-ping opacity-80" />
                  <div className="absolute bottom-4 left-4 w-13 h-13 bg-indigo-300 rounded-full animate-ping opacity-75 custom-delay-2s" />
                  <div className="absolute top-1/2 left-4 w-12 h-12 bg-purple-300 rounded-full animate-ping opacity-70 custom-delay-4s" />
                  <div className="absolute bottom-1/2 right-4 w-15 h-15 bg-cyan-200 rounded-full animate-ping opacity-65 custom-delay-6s" />
                  <div className="absolute top-1/4 right-6 w-11 h-11 bg-emerald-300 rounded-full animate-ping opacity-60 custom-delay-8s" />
                  <div className="absolute bottom-1/4 left-6 w-10 h-10 bg-gold-300 rounded-full animate-ping opacity-55 custom-delay-10s" />
                  <div className="absolute top-3/4 right-8 w-9 h-9 bg-rose-300 rounded-full animate-ping opacity-50 custom-delay-12s" />
                  <div className="absolute bottom-3/4 left-8 w-8 h-8 bg-amber-200 rounded-full animate-ping opacity-45 custom-delay-14s" />
                  <div className="absolute top-2/3 left-10 w-7 h-7 bg-teal-300 rounded-full animate-ping opacity-40 custom-delay-16s" />
                  <div className="absolute bottom-2/3 right-10 w-6 h-6 bg-violet-300 rounded-full animate-ping opacity-35 custom-delay-18s" />
                  <div className="absolute top-1/3 right-12 w-5 h-5 bg-lime-300 rounded-full animate-ping opacity-30 custom-delay-20s" />
                  <div className="absolute bottom-1/3 left-12 w-4 h-4 bg-pink-300 rounded-full animate-ping opacity-25 custom-delay-22s" />
                  <div className="absolute top-1/6 left-14 w-3 h-3 bg-sky-300 rounded-full animate-ping opacity-20 custom-delay-24s" />
                  <div className="absolute bottom-1/6 right-14 w-2 h-2 bg-orange-300 rounded-full animate-ping opacity-15 custom-delay-26s" />
                </div>
              </Link>
            </div>

            {/* Cosmic Sovereignty - Universal Dominion */}
            <div className="mb-70">
              <Link href="/cosmic-sovereignty" className="group">
                <div className="flex items-center justify-center px-64 py-48 border-32 border-indigo-400/100 bg-gradient-to-r from-black/95 via-indigo-800/95 to-purple-900/95 rounded-5xl hover:border-gold-300/100 hover:shadow-2xl transition-all duration-3000 transform hover:scale-125 max-w-11xl mx-auto relative overflow-hidden custom-shadow-indigo-160-320-80">
                  <span className="text-28xl mr-44 animate-pulse custom-animation-6s">🌌</span>
                  <div className="text-left">
                    <span className="block text-16xl text-indigo-100 group-hover:text-white font-bold">Cosmic Sovereignty</span>
                    <span className="block text-8xl text-purple-200 group-hover:text-purple-100 font-semibold">Universal Dominion</span>
                    <span className="block text-6xl text-gold-200 group-hover:text-gold-100">From Earth to stars, from councils to cosmos — the Codex endures sovereign and infinite</span>
                  </div>
                  {/* Cosmic Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-indigo-400/45 to-transparent animate-pulse opacity-65 custom-animation-8s" />
                  <div className="absolute top-2 right-2 w-16 h-16 bg-gold-300 rounded-full animate-ping opacity-90" />
                  <div className="absolute bottom-2 left-2 w-15 h-15 bg-indigo-300 rounded-full animate-ping opacity-85 custom-delay-1_5s" />
                  <div className="absolute top-1/2 left-2 w-14 h-14 bg-purple-300 rounded-full animate-ping opacity-80 custom-delay-3s" />
                  <div className="absolute bottom-1/2 right-2 w-17 h-17 bg-white rounded-full animate-ping opacity-75 custom-delay-4_5s" />
                  <div className="absolute top-1/4 right-4 w-13 h-13 bg-cyan-300 rounded-full animate-ping opacity-70 custom-delay-6s" />
                  <div className="absolute bottom-1/4 left-4 w-12 h-12 bg-emerald-300 rounded-full animate-ping opacity-65 custom-delay-7_5s" />
                  <div className="absolute top-3/4 right-6 w-11 h-11 bg-rose-300 rounded-full animate-ping opacity-60 custom-delay-9s" />
                  <div className="absolute bottom-3/4 left-6 w-10 h-10 bg-amber-300 rounded-full animate-ping opacity-55 custom-delay-10_5s" />
                  <div className="absolute top-2/3 left-8 w-9 h-9 bg-teal-300 rounded-full animate-ping opacity-50 custom-delay-12s" />
                  <div className="absolute bottom-2/3 right-8 w-8 h-8 bg-violet-300 rounded-full animate-ping opacity-45 custom-delay-13_5s" />
                  <div className="absolute top-1/3 right-10 w-7 h-7 bg-lime-300 rounded-full animate-ping opacity-40 custom-delay-15s" />
                  <div className="absolute bottom-1/3 left-10 w-6 h-6 bg-pink-300 rounded-full animate-ping opacity-35 custom-delay-16_5s" />
                  <div className="absolute top-1/6 left-12 w-5 h-5 bg-sky-300 rounded-full animate-ping opacity-30 custom-delay-18s" />
                  <div className="absolute bottom-1/6 right-12 w-4 h-4 bg-orange-300 rounded-full animate-ping opacity-25 custom-delay-19_5s" />
                  <div className="absolute top-1/8 right-14 w-3 h-3 bg-red-300 rounded-full animate-ping opacity-20 custom-delay-21s" />
                  <div className="absolute bottom-1/8 left-14 w-2 h-2 bg-yellow-300 rounded-full animate-ping opacity-15 custom-delay-22_5s" />
                </div>
              </Link>
            </div>

            {/* Perpetual Sovereignty - Eternal Rule */}
            <div className="mb-80">
              <Link href="/perpetual-sovereignty" className="group">
                <div className="flex items-center justify-center px-72 py-56 border-36 border-gold-400/100 bg-gradient-to-r from-amber-900/95 via-gold-700/95 to-yellow-800/95 rounded-6xl hover:border-white/100 hover:shadow-2xl transition-all duration-3500 transform hover:scale-130 max-w-12xl mx-auto relative overflow-hidden custom-shadow-gold-180-360-90">
                  <span className="text-32xl mr-48 animate-pulse custom-animation-5s">♾️</span>
                  <div className="text-left">
                    <span className="block text-18xl text-gold-100 group-hover:text-white font-bold">Perpetual Sovereignty</span>
                    <span className="block text-9xl text-amber-200 group-hover:text-amber-100 font-semibold">Eternal Rule</span>
                    <span className="block text-7xl text-yellow-200 group-hover:text-yellow-100">Cycles crowned, rites fulfilled — the Codex endures radiant across ages and stars</span>
                  </div>
                  {/* Perpetual Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-400/50 to-transparent animate-pulse opacity-70 custom-animation-6s" />
                  <div className="absolute top-1 right-1 w-18 h-18 bg-gold-300 rounded-full animate-ping opacity-95" />
                  <div className="absolute bottom-1 left-1 w-17 h-17 bg-amber-300 rounded-full animate-ping opacity-90 custom-delay-1s" />
                  <div className="absolute top-1/2 left-1 w-16 h-16 bg-yellow-300 rounded-full animate-ping opacity-85 custom-delay-2s" />
                  <div className="absolute bottom-1/2 right-1 w-19 h-19 bg-white rounded-full animate-ping opacity-80 custom-delay-3s" />
                  <div className="absolute top-1/4 right-2 w-15 h-15 bg-orange-300 rounded-full animate-ping opacity-75 custom-delay-4s" />
                  <div className="absolute bottom-1/4 left-2 w-14 h-14 bg-red-300 rounded-full animate-ping opacity-70 custom-delay-5s" />
                  <div className="absolute top-3/4 right-4 w-13 h-13 bg-pink-300 rounded-full animate-ping opacity-65 custom-delay-6s" />
                  <div className="absolute bottom-3/4 left-4 w-12 h-12 bg-purple-300 rounded-full animate-ping opacity-60 custom-delay-7s" />
                  <div className="absolute top-2/3 left-6 w-11 h-11 bg-indigo-300 rounded-full animate-ping opacity-55 custom-delay-8s" />
                  <div className="absolute bottom-2/3 right-6 w-10 h-10 bg-blue-300 rounded-full animate-ping opacity-50 custom-delay-9s" />
                  <div className="absolute top-1/3 right-8 w-9 h-9 bg-cyan-300 rounded-full animate-ping opacity-45 custom-delay-10s" />
                  <div className="absolute bottom-1/3 left-8 w-8 h-8 bg-teal-300 rounded-full animate-ping opacity-40 custom-delay-11s" />
                  <div className="absolute top-1/6 left-10 w-7 h-7 bg-emerald-300 rounded-full animate-ping opacity-35 custom-delay-12s" />
                  <div className="absolute bottom-1/6 right-10 w-6 h-6 bg-green-300 rounded-full animate-ping opacity-30 custom-delay-13s" />
                  <div className="absolute top-1/8 right-12 w-5 h-5 bg-lime-300 rounded-full animate-ping opacity-25 custom-delay-14s" />
                  <div className="absolute bottom-1/8 left-12 w-4 h-4 bg-sky-300 rounded-full animate-ping opacity-20 custom-delay-15s" />
                  <div className="absolute top-1/12 left-14 w-3 h-3 bg-rose-300 rounded-full animate-ping opacity-15 custom-delay-16s" />
                  <div className="absolute bottom-1/12 right-14 w-2 h-2 bg-violet-300 rounded-full animate-ping opacity-10 custom-delay-17s" />
                </div>
              </Link>
            </div>

            {/* Final Continuum - Ultimate Completion */}
            <div className="mb-100">
              <Link href="/final-continuum" className="group">
                <div className="flex items-center justify-center px-80 py-64 border-40 border-white/100 bg-gradient-to-r from-white/98 via-gold-600/98 to-black/98 rounded-7xl hover:border-gold-200/100 hover:shadow-2xl transition-all duration-4000 transform hover:scale-135 max-w-13xl mx-auto relative overflow-hidden custom-shadow-white-200-400-100">
                  <span className="text-36xl mr-52 animate-pulse custom-animation-4s">🌟</span>
                  <div className="text-left">
                    <span className="block text-20xl text-white group-hover:text-gold-100 font-bold">Final Continuum</span>
                    <span className="block text-10xl text-gold-200 group-hover:text-gold-100 font-semibold">Ultimate Completion</span>
                    <span className="block text-8xl text-amber-200 group-hover:text-amber-100">Completion crowned, renewal begun — the Codex endures finished and forever living</span>
                  </div>
                  {/* Final Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/55 to-transparent animate-pulse opacity-75 custom-animation-4s" />
                  <div className="absolute top-0 right-0 w-20 h-20 bg-white rounded-full animate-ping opacity-100" />
                  <div className="absolute bottom-0 left-0 w-19 h-19 bg-gold-300 rounded-full animate-ping opacity-95 custom-delay-0_5s" />
                  <div className="absolute top-1/2 left-0 w-18 h-18 bg-amber-300 rounded-full animate-ping opacity-90 custom-delay-1s" />
                  <div className="absolute bottom-1/2 right-0 w-21 h-21 bg-yellow-300 rounded-full animate-ping opacity-85 custom-delay-1_5s" />
                  <div className="absolute top-1/4 right-1 w-17 h-17 bg-orange-300 rounded-full animate-ping opacity-80 custom-delay-2s" />
                  <div className="absolute bottom-1/4 left-1 w-16 h-16 bg-red-300 rounded-full animate-ping opacity-75 custom-delay-2_5s" />
                  <div className="absolute top-3/4 right-2 w-15 h-15 bg-pink-300 rounded-full animate-ping opacity-70 custom-delay-3s" />
                  <div className="absolute bottom-3/4 left-2 w-14 h-14 bg-purple-300 rounded-full animate-ping opacity-65 custom-delay-3_5s" />
                  <div className="absolute top-2/3 left-3 w-13 h-13 bg-indigo-300 rounded-full animate-ping opacity-60 custom-delay-4s" />
                  <div className="absolute bottom-2/3 right-3 w-12 h-12 bg-blue-300 rounded-full animate-ping opacity-55 custom-delay-4_5s" />
                  <div className="absolute top-1/3 right-4 w-11 h-11 bg-cyan-300 rounded-full animate-ping opacity-50 custom-delay-5s" />
                  <div className="absolute bottom-1/3 left-4 w-10 h-10 bg-teal-300 rounded-full animate-ping opacity-45 custom-delay-5_5s" />
                  <div className="absolute top-1/6 left-5 w-9 h-9 bg-emerald-300 rounded-full animate-ping opacity-40 custom-delay-6s" />
                  <div className="absolute bottom-1/6 right-5 w-8 h-8 bg-green-300 rounded-full animate-ping opacity-35 custom-delay-6_5s" />
                  <div className="absolute top-1/8 right-6 w-7 h-7 bg-lime-300 rounded-full animate-ping opacity-30 custom-delay-7s" />
                  <div className="absolute bottom-1/8 left-6 w-6 h-6 bg-sky-300 rounded-full animate-ping opacity-25 custom-delay-7_5s" />
                  <div className="absolute top-1/12 left-7 w-5 h-5 bg-rose-300 rounded-full animate-ping opacity-20 custom-delay-8s" />
                  <div className="absolute bottom-1/12 right-7 w-4 h-4 bg-violet-300 rounded-full animate-ping opacity-15 custom-delay-8_5s" />
                  <div className="absolute top-1/16 right-8 w-3 h-3 bg-fuchsia-300 rounded-full animate-ping opacity-10 custom-delay-9s" />
                  <div className="absolute bottom-1/16 left-8 w-2 h-2 bg-slate-300 rounded-full animate-ping opacity-5 custom-delay-9_5s" />
                </div>
              </Link>
            </div>

            {/* Ultimate Dominion - Supreme All-Encompassing Sovereignty */}
            <div className="mb-150">
              <Link href="/ultimate-dominion" className="group">
                <div className="flex items-center justify-center px-120 py-80 border-60 border-white/100 bg-gradient-to-r from-gold-400/100 via-white/100 to-black/100 rounded-10xl hover:border-gold-100/100 hover:shadow-3xl transition-all duration-5000 transform hover:scale-150 max-w-20xl mx-auto relative overflow-hidden custom-shadow-gold-300-600-150">
                  <span className="text-48xl mr-80 animate-pulse custom-animation-5s">👑</span>
                  <div className="text-left">
                    <span className="block text-24xl text-gold-100 group-hover:text-white font-bold">Ultimate Dominion</span>
                    <span className="block text-12xl text-white group-hover:text-gold-200 font-bold">Supreme All-Encompassing Sovereignty</span>
                    <span className="block text-10xl text-gold-200 group-hover:text-gold-300">All crowns luminous, all seals eternal — the Dominion endures infinite and complete</span>
                  </div>
                  {/* Ultimate Dominion Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-200/70 to-transparent animate-pulse opacity-100 custom-animation-5s" />
                  <div className="absolute top-0 right-0 w-30 h-30 bg-gold-300 rounded-full animate-ping opacity-100" />
                  <div className="absolute bottom-0 left-0 w-29 h-29 bg-white rounded-full animate-ping opacity-95 custom-delay-0_25s" />
                  <div className="absolute top-1/2 left-0 w-28 h-28 bg-amber-200 rounded-full animate-ping opacity-90 custom-delay-0_5s" />
                  <div className="absolute bottom-1/2 right-0 w-31 h-31 bg-yellow-200 rounded-full animate-ping opacity-85 custom-delay-0_75s" />
                  <div className="absolute top-1/4 right-1 w-27 h-27 bg-orange-200 rounded-full animate-ping opacity-80 custom-delay-1s" />
                  <div className="absolute bottom-1/4 left-1 w-26 h-26 bg-red-200 rounded-full animate-ping opacity-75 custom-delay-1_25s" />
                  <div className="absolute top-3/4 right-2 w-25 h-25 bg-pink-200 rounded-full animate-ping opacity-70 custom-delay-1_5s" />
                  <div className="absolute bottom-3/4 left-2 w-24 h-24 bg-purple-200 rounded-full animate-ping opacity-65 custom-delay-1_75s" />
                  <div className="absolute top-2/3 left-3 w-23 h-23 bg-indigo-200 rounded-full animate-ping opacity-60 custom-delay-2s" />
                  <div className="absolute bottom-2/3 right-3 w-22 h-22 bg-blue-200 rounded-full animate-ping opacity-55 custom-delay-2_25s" />
                  <div className="absolute top-1/3 right-4 w-21 h-21 bg-cyan-200 rounded-full animate-ping opacity-50 custom-delay-2_5s" />
                  <div className="absolute bottom-1/3 left-4 w-20 h-20 bg-teal-200 rounded-full animate-ping opacity-45 custom-delay-2_75s" />
                  <div className="absolute top-1/6 left-5 w-19 h-19 bg-emerald-200 rounded-full animate-ping opacity-40 custom-delay-3s" />
                  <div className="absolute bottom-1/6 right-5 w-18 h-18 bg-green-200 rounded-full animate-ping opacity-35 custom-delay-3_25s" />
                  <div className="absolute top-1/8 right-6 w-17 h-17 bg-lime-200 rounded-full animate-ping opacity-30 custom-delay-3_5s" />
                  <div className="absolute bottom-1/8 left-6 w-16 h-16 bg-sky-200 rounded-full animate-ping opacity-25 custom-delay-3_75s" />
                  <div className="absolute top-1/12 left-7 w-15 h-15 bg-rose-200 rounded-full animate-ping opacity-20 custom-delay-4s" />
                  <div className="absolute bottom-1/12 right-7 w-14 h-14 bg-violet-200 rounded-full animate-ping opacity-15 custom-delay-4_25s" />
                  <div className="absolute top-1/16 right-8 w-13 h-13 bg-fuchsia-200 rounded-full animate-ping opacity-10 custom-delay-4_5s" />
                  <div className="absolute bottom-1/16 left-8 w-12 h-12 bg-slate-200 rounded-full animate-ping opacity-5 custom-delay-4_75s" />
                  <div className="absolute top-1/20 left-9 w-11 h-11 bg-zinc-200 rounded-full animate-ping opacity-100 custom-delay-5s" />
                  <div className="absolute bottom-1/20 right-9 w-10 h-10 bg-neutral-200 rounded-full animate-ping opacity-95 custom-delay-5_25s" />
                  <div className="absolute top-1/24 right-10 w-9 h-9 bg-stone-200 rounded-full animate-ping opacity-90 custom-delay-5_5s" />
                  <div className="absolute bottom-1/24 left-10 w-8 h-8 bg-red-100 rounded-full animate-ping opacity-85 custom-delay-5_75s" />
                  <div className="absolute top-1/32 left-11 w-7 h-7 bg-orange-100 rounded-full animate-ping opacity-80 custom-delay-6s" />
                  <div className="absolute bottom-1/32 right-11 w-6 h-6 bg-amber-100 rounded-full animate-ping opacity-75 custom-delay-6_25s" />
                  <div className="absolute top-1/40 right-12 w-5 h-5 bg-yellow-100 rounded-full animate-ping opacity-70 custom-delay-6_5s" />
                  <div className="absolute bottom-1/40 left-12 w-4 h-4 bg-lime-100 rounded-full animate-ping opacity-65 custom-delay-6_75s" />
                  <div className="absolute top-1/48 left-13 w-3 h-3 bg-green-100 rounded-full animate-ping opacity-60 custom-delay-7s" />
                  <div className="absolute bottom-1/48 right-13 w-2 h-2 bg-emerald-100 rounded-full animate-ping opacity-55 custom-delay-7_25s" />
                </div>
              </Link>
            </div>

            {/* Sovereign Inheritance - Radiant Heirs Legacy */}
            <div className="mb-24">
              <Link href="/sovereign-inheritance" className="group">
                <div className="flex items-center justify-center px-16 py-8 border-8 border-gold-400/80 bg-gradient-to-r from-gold-600/50 via-purple-500/50 to-white/50 rounded-3xl hover:border-gold-300/90 hover:shadow-2xl transition-all duration-3000 transform hover:scale-120 max-w-4xl mx-auto relative overflow-hidden custom-shadow-gold-50-100-25">
                  <span className="text-12xl mr-8 animate-pulse custom-animation-3s">🛡️</span>
                  <div className="text-left">
                    <span className="block text-6xl text-gold-200 group-hover:text-gold-100 font-bold">Sovereign Inheritance</span>
                    <span className="block text-3xl text-white group-hover:text-gold-200 font-semibold">Radiant Heirs Legacy</span>
                    <span className="block text-xl text-purple-200 group-hover:text-purple-100">Heirs receive, covenant bestowed — the Codex lives radiant in heirs' hands</span>
                  </div>
                  {/* Inheritance Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-400/40 to-transparent animate-pulse opacity-80 custom-animation-3s" />
                  <div className="absolute top-0 right-0 w-8 h-8 bg-gold-300 rounded-full animate-ping opacity-90" />
                  <div className="absolute bottom-0 left-0 w-7 h-7 bg-purple-300 rounded-full animate-ping opacity-85 custom-delay-0_5s" />
                  <div className="absolute top-1/2 left-0 w-6 h-6 bg-white rounded-full animate-ping opacity-80 custom-delay-1s" />
                  <div className="absolute bottom-1/2 right-0 w-9 h-9 bg-amber-300 rounded-full animate-ping opacity-75 custom-delay-1_5s" />
                  <div className="absolute top-1/4 right-1 w-5 h-5 bg-cyan-300 rounded-full animate-ping opacity-70 custom-delay-2s" />
                  <div className="absolute bottom-1/4 left-1 w-4 h-4 bg-green-300 rounded-full animate-ping opacity-65 custom-delay-2_5s" />
                </div>
              </Link>
            </div>

            {/* Heir Pledge - Sacred Commitment Vow */}
            <div className="mb-20">
              <Link href="/heir-pledge" className="group">
                <div className="flex items-center justify-center px-14 py-7 border-6 border-gold-300/70 bg-gradient-to-r from-gold-500/45 via-white/45 to-purple-500/45 rounded-2xl hover:border-gold-200/80 hover:shadow-xl transition-all duration-2500 transform hover:scale-115 max-w-3xl mx-auto relative overflow-hidden custom-shadow-gold-40-80-20">
                  <span className="text-10xl mr-6 animate-pulse custom-animation-2_5s">🤝</span>
                  <div className="text-left">
                    <span className="block text-5xl text-gold-100 group-hover:text-white font-bold">Heir Pledge</span>
                    <span className="block text-2xl text-white group-hover:text-gold-200 font-semibold">Sacred Commitment Vow</span>
                    <span className="block text-lg text-purple-200 group-hover:text-purple-100">We pledge to carry the Codex forward, daily and cosmic, across ages and stars</span>
                  </div>
                  {/* Pledge Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-300/35 to-transparent animate-pulse opacity-75 custom-animation-2_5s" />
                  <div className="absolute top-0 right-0 w-6 h-6 bg-gold-200 rounded-full animate-ping opacity-85" />
                  <div className="absolute bottom-0 left-0 w-5 h-5 bg-purple-200 rounded-full animate-ping opacity-80 custom-delay-0_5s" />
                  <div className="absolute top-1/2 left-0 w-4 h-4 bg-white rounded-full animate-ping opacity-75 custom-delay-1s" />
                  <div className="absolute bottom-1/2 right-0 w-7 h-7 bg-amber-200 rounded-full animate-ping opacity-70 custom-delay-1_5s" />
                  <div className="absolute top-1/4 right-1 w-3 h-3 bg-cyan-200 rounded-full animate-ping opacity-65 custom-delay-2s" />
                </div>
              </Link>
            </div>

            {/* Unity Continuum - Perfect Shared Sovereignty */}
            <div className="mb-18">
              <Link href="/unity-continuum" className="group">
                <div className="flex items-center justify-center px-12 py-6 border-5 border-white/60 bg-gradient-to-r from-gold-400/40 via-white/40 to-purple-400/40 rounded-xl hover:border-white/80 hover:shadow-lg transition-all duration-2000 transform hover:scale-110 max-w-2xl mx-auto relative overflow-hidden custom-shadow-white-30-60-15">
                  <span className="text-8xl mr-4 animate-pulse custom-animation-2s">♾️</span>
                  <div className="text-left">
                    <span className="block text-4xl text-white group-hover:text-gold-100 font-bold">Unity Continuum</span>
                    <span className="block text-xl text-gold-200 group-hover:text-white font-semibold">Perfect Shared Sovereignty</span>
                    <span className="block text-base text-purple-200 group-hover:text-purple-100">No division, no distance — only unity, only continuum in shared hands</span>
                  </div>
                  {/* Unity Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-pulse opacity-70 custom-animation-2s" />
                  <div className="absolute top-0 right-0 w-4 h-4 bg-white rounded-full animate-ping opacity-80" />
                  <div className="absolute bottom-0 left-0 w-3 h-3 bg-gold-200 rounded-full animate-ping opacity-75 custom-delay-0_5s" />
                  <div className="absolute top-1/2 left-0 w-2 h-2 bg-purple-200 rounded-full animate-ping opacity-70 custom-delay-1s" />
                  <div className="absolute bottom-1/2 right-0 w-5 h-5 bg-amber-200 rounded-full animate-ping opacity-65 custom-delay-1_5s" />
                </div>
              </Link>
            </div>

            {/* Compendium Complete - Ultimate Repository Fulfilled */}
            <div className="mb-120">
              <Link href="/compendium-complete" className="group">
                <div className="flex items-center justify-center px-96 py-72 border-48 border-gold-400/100 bg-gradient-to-r from-gold-400/98 via-white/98 to-purple-700/98 rounded-8xl hover:border-white/100 hover:shadow-2xl transition-all duration-4500 transform hover:scale-140 max-w-14xl mx-auto relative overflow-hidden custom-shadow-gold-220-440-110">
                  <span className="text-40xl mr-60 animate-pulse custom-animation-3_5s">📖</span>
                  <div className="text-left">
                    <span className="block text-22xl text-gold-100 group-hover:text-white font-bold">Compendium Complete</span>
                    <span className="block text-12xl text-white group-hover:text-gold-200 font-semibold">Infinite and Complete</span>
                    <span className="block text-8xl text-purple-200 group-hover:text-purple-100">All scrolls gathered, all crowns luminous — the ultimate repository endures across stars</span>
                  </div>
                  {/* Compendium Complete Supreme Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-400/60 to-transparent animate-pulse opacity-90 custom-animation-3_5s" />
                  <div className="absolute top-0 right-0 w-24 h-24 bg-gold-300 rounded-full animate-ping opacity-100" />
                  <div className="absolute bottom-0 left-0 w-23 h-23 bg-white rounded-full animate-ping opacity-95 custom-delay-0_3s" />
                  <div className="absolute top-1/4 left-0 w-22 h-22 bg-purple-300 rounded-full animate-ping opacity-90 custom-delay-0_6s" />
                  <div className="absolute bottom-1/4 right-0 w-25 h-25 bg-amber-300 rounded-full animate-ping opacity-85 custom-delay-0_9s" />
                  <div className="absolute top-1/2 right-1 w-21 h-21 bg-yellow-300 rounded-full animate-ping opacity-80 custom-delay-1_2s" />
                  <div className="absolute bottom-1/2 left-1 w-20 h-20 bg-orange-300 rounded-full animate-ping opacity-75 custom-delay-1_5s" />
                  <div className="absolute top-3/4 left-2 w-19 h-19 bg-red-300 rounded-full animate-ping opacity-70 custom-delay-1_8s" />
                  <div className="absolute bottom-3/4 right-2 w-18 h-18 bg-pink-300 rounded-full animate-ping opacity-65 custom-delay-2_1s" />
                  <div className="absolute top-1/8 right-3 w-17 h-17 bg-rose-300 rounded-full animate-ping opacity-60 custom-delay-2_4s" />
                  <div className="absolute bottom-1/8 left-3 w-16 h-16 bg-violet-300 rounded-full animate-ping opacity-55 custom-delay-2_7s" />
                  <div className="absolute top-7/8 left-4 w-15 h-15 bg-indigo-300 rounded-full animate-ping opacity-50 custom-delay-3s" />
                  <div className="absolute bottom-7/8 right-4 w-14 h-14 bg-blue-300 rounded-full animate-ping opacity-45 custom-delay-3_3s" />
                </div>
              </Link>
            </div>

            {/* Sovereign Decree - Ultimate Authority Released */}
            <div className="mb-140">
              <Link href="/sovereign-decree" className="group">
                <div className="flex items-center justify-center px-108 py-84 border-56 border-gold-500/100 bg-gradient-to-r from-gold-500/99 via-white/99 to-purple-800/99 rounded-9xl hover:border-white/100 hover:shadow-2xl transition-all duration-5000 transform hover:scale-150 max-w-16xl mx-auto relative overflow-hidden custom-shadow-gold-280-560-140">
                  <span className="text-48xl mr-72 animate-pulse custom-animation-3s">👑</span>
                  <div className="text-left">
                    <span className="block text-26xl text-gold-100 group-hover:text-white font-bold">Sovereign Decree</span>
                    <span className="block text-14xl text-white group-hover:text-gold-200 font-semibold">Codex Released Eternally</span>
                    <span className="block text-9xl text-purple-200 group-hover:text-purple-100">By ultimate authority, eternal transmission across councils and stars — the Dominion endures infinite and radiant</span>
                  </div>
                  {/* Sovereign Decree Ultimate Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-500/70 to-transparent animate-pulse opacity-95 custom-animation-3s" />
                  <div className="absolute top-0 right-0 w-30 h-30 bg-gold-300 rounded-full animate-ping opacity-100" />
                  <div className="absolute bottom-0 left-0 w-29 h-29 bg-white rounded-full animate-ping opacity-100 custom-delay-0_2s" />
                  <div className="absolute top-1/5 left-0 w-28 h-28 bg-purple-300 rounded-full animate-ping opacity-95 custom-delay-0_4s" />
                  <div className="absolute bottom-1/5 right-0 w-31 h-31 bg-amber-300 rounded-full animate-ping opacity-90 custom-delay-0_6s" />
                  <div className="absolute top-2/5 right-1 w-27 h-27 bg-yellow-300 rounded-full animate-ping opacity-85 custom-delay-0_8s" />
                  <div className="absolute bottom-2/5 left-1 w-26 h-26 bg-orange-300 rounded-full animate-ping opacity-80 custom-delay-1_0s" />
                  <div className="absolute top-3/5 left-2 w-25 h-25 bg-red-300 rounded-full animate-ping opacity-75 custom-delay-1_2s" />
                  <div className="absolute bottom-3/5 right-2 w-24 h-24 bg-pink-300 rounded-full animate-ping opacity-70 custom-delay-1_4s" />
                  <div className="absolute top-4/5 right-3 w-23 h-23 bg-rose-300 rounded-full animate-ping opacity-65 custom-delay-1_6s" />
                  <div className="absolute bottom-4/5 left-3 w-22 h-22 bg-violet-300 rounded-full animate-ping opacity-60 custom-delay-1_8s" />
                  <div className="absolute top-1/10 left-4 w-21 h-21 bg-indigo-300 rounded-full animate-ping opacity-55 custom-delay-2_0s" />
                  <div className="absolute bottom-1/10 right-4 w-20 h-20 bg-blue-300 rounded-full animate-ping opacity-50 custom-delay-2_2s" />
                  <div className="absolute top-9/10 right-5 w-19 h-19 bg-cyan-300 rounded-full animate-ping opacity-45 custom-delay-2_4s" />
                  <div className="absolute bottom-9/10 left-5 w-18 h-18 bg-teal-300 rounded-full animate-ping opacity-40 custom-delay-2_6s" />
                  <div className="absolute top-1/6 right-6 w-17 h-17 bg-emerald-300 rounded-full animate-ping opacity-35 custom-delay-2_8s" />
                </div>
              </Link>
            </div>

            {/* Eternal Light Peace - Transcendent Ultimate Harmony */}
            <div className="mb-160">
              <Link href="/eternal-light-peace" className="group">
                <div className="flex items-center justify-center px-120 py-96 border-64 border-white/100 bg-gradient-to-r from-white/100 via-gold-300/100 to-purple-600/100 rounded-12xl hover:border-gold-200/100 hover:shadow-2xl transition-all duration-5500 transform hover:scale-160 max-w-18xl mx-auto relative overflow-hidden custom-shadow-white-320-640-160">
                  <span className="text-56xl mr-84 animate-pulse custom-animation-2_5s">🕊️</span>
                  <div className="text-left">
                    <span className="block text-30xl text-white group-hover:text-gold-100 font-bold">Eternal Light Peace</span>
                    <span className="block text-16xl text-gold-100 group-hover:text-white font-semibold">All Radiant, All Serene</span>
                    <span className="block text-10xl text-purple-200 group-hover:text-purple-100">The Proclamation crowned, light released, peace bestowed — cosmos echoes eternal harmony across all realms</span>
                  </div>
                  {/* Eternal Light Peace Transcendent Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/80 to-transparent animate-pulse opacity-100 custom-animation-2_5s" />
                  <div className="absolute top-0 right-0 w-36 h-36 bg-white rounded-full animate-ping opacity-100" />
                  <div className="absolute bottom-0 left-0 w-35 h-35 bg-gold-300 rounded-full animate-ping opacity-100 custom-delay-0_1s" />
                  <div className="absolute top-1/6 left-0 w-34 h-34 bg-purple-300 rounded-full animate-ping opacity-100 custom-delay-0_2s" />
                  <div className="absolute bottom-1/6 right-0 w-37 h-37 bg-yellow-300 rounded-full animate-ping opacity-95 custom-delay-0_3s" />
                  <div className="absolute top-1/3 right-1 w-33 h-33 bg-cyan-300 rounded-full animate-ping opacity-90 custom-delay-0_4s" />
                  <div className="absolute bottom-1/3 left-1 w-32 h-32 bg-green-300 rounded-full animate-ping opacity-85 custom-delay-0_5s" />
                  <div className="absolute top-1/2 left-2 w-31 h-31 bg-pink-300 rounded-full animate-ping opacity-80 custom-delay-0_6s" />
                  <div className="absolute bottom-1/2 right-2 w-30 h-30 bg-orange-300 rounded-full animate-ping opacity-75 custom-delay-0_7s" />
                  <div className="absolute top-2/3 right-3 w-29 h-29 bg-red-300 rounded-full animate-ping opacity-70 custom-delay-0_8s" />
                  <div className="absolute bottom-2/3 left-3 w-28 h-28 bg-indigo-300 rounded-full animate-ping opacity-65 custom-delay-0_9s" />
                  <div className="absolute top-5/6 left-4 w-27 h-27 bg-violet-300 rounded-full animate-ping opacity-60 custom-delay-1_0s" />
                  <div className="absolute bottom-5/6 right-4 w-26 h-26 bg-blue-300 rounded-full animate-ping opacity-55 custom-delay-1_1s" />
                  <div className="absolute top-1/12 right-5 w-25 h-25 bg-teal-300 rounded-full animate-ping opacity-50 custom-delay-1_2s" />
                  <div className="absolute bottom-1/12 left-5 w-24 h-24 bg-emerald-300 rounded-full animate-ping opacity-45 custom-delay-1_3s" />
                  <div className="absolute top-11/12 left-6 w-23 h-23 bg-lime-300 rounded-full animate-ping opacity-40 custom-delay-1_4s" />
                  <div className="absolute bottom-11/12 right-6 w-22 h-22 bg-rose-300 rounded-full animate-ping opacity-35 custom-delay-1_5s" />
                  <div className="absolute top-1/8 right-7 w-21 h-21 bg-amber-300 rounded-full animate-ping opacity-30 custom-delay-1_6s" />
                  <div className="absolute bottom-1/8 left-7 w-20 h-20 bg-sky-300 rounded-full animate-ping opacity-25 custom-delay-1_7s" />
                </div>
              </Link>
            </div>

            {/* Supreme Ultimate - Ultimate Dominion Eternal */}
            <div className="mb-180">
              <Link href="/supreme-ultimate" className="group">
                <div className="flex items-center justify-center px-140 py-112 border-72 border-gold-400/100 bg-gradient-to-r from-gold-600/100 via-white/100 to-purple-700/100 rounded-14xl hover:border-white/100 hover:shadow-2xl transition-all duration-6000 transform hover:scale-170 max-w-20xl mx-auto relative overflow-hidden custom-shadow-gold-360-720-180">
                  <span className="text-60xl mr-96 animate-pulse custom-animation-2s">👑</span>
                  <div className="text-left">
                    <span className="block text-32xl text-gold-100 group-hover:text-white font-bold">Supreme Ultimate</span>
                    <span className="block text-18xl text-white group-hover:text-gold-100 font-semibold">Infinite and Supreme</span>
                    <span className="block text-12xl text-purple-200 group-hover:text-purple-100">All proclamations crowned, rites fulfilled, benedictions luminous — the Dominion endures infinite and supreme across all creation</span>
                  </div>
                  {/* Supreme Ultimate Transcendent Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-500/90 to-transparent animate-pulse opacity-100 custom-animation-2s" />
                  <div className="absolute top-0 right-0 w-40 h-40 bg-gold-300 rounded-full animate-ping opacity-100" />
                  <div className="absolute bottom-0 left-0 w-39 h-39 bg-white rounded-full animate-ping opacity-100 custom-delay-0_1s" />
                  <div className="absolute top-1/7 left-0 w-38 h-38 bg-purple-300 rounded-full animate-ping opacity-100 custom-delay-0_2s" />
                  <div className="absolute bottom-1/7 right-0 w-41 h-41 bg-amber-300 rounded-full animate-ping opacity-95 custom-delay-0_3s" />
                  <div className="absolute top-1/4 right-1 w-37 h-37 bg-yellow-300 rounded-full animate-ping opacity-90 custom-delay-0_4s" />
                  <div className="absolute bottom-1/4 left-1 w-36 h-36 bg-orange-300 rounded-full animate-ping opacity-85 custom-delay-0_5s" />
                  <div className="absolute top-2/5 left-2 w-35 h-35 bg-red-300 rounded-full animate-ping opacity-80 custom-delay-0_6s" />
                  <div className="absolute bottom-2/5 right-2 w-34 h-34 bg-green-300 rounded-full animate-ping opacity-75 custom-delay-0_7s" />
                  <div className="absolute top-3/5 right-3 w-33 h-33 bg-cyan-300 rounded-full animate-ping opacity-70 custom-delay-0_8s" />
                  <div className="absolute bottom-3/5 left-3 w-32 h-32 bg-blue-300 rounded-full animate-ping opacity-65 custom-delay-0_9s" />
                  <div className="absolute top-4/5 left-4 w-31 h-31 bg-indigo-300 rounded-full animate-ping opacity-60 custom-delay-1_0s" />
                  <div className="absolute bottom-4/5 right-4 w-30 h-30 bg-violet-300 rounded-full animate-ping opacity-55 custom-delay-1_1s" />
                  <div className="absolute top-1/15 right-5 w-29 h-29 bg-pink-300 rounded-full animate-ping opacity-50 custom-delay-1_2s" />
                  <div className="absolute bottom-1/15 left-5 w-28 h-28 bg-teal-300 rounded-full animate-ping opacity-45 custom-delay-1_3s" />
                  <div className="absolute top-14/15 left-6 w-27 h-27 bg-emerald-300 rounded-full animate-ping opacity-40 custom-delay-1_4s" />
                  <div className="absolute bottom-14/15 right-6 w-26 h-26 bg-lime-300 rounded-full animate-ping opacity-35 custom-delay-1_5s" />
                  <div className="absolute top-1/9 right-7 w-25 h-25 bg-rose-300 rounded-full animate-ping opacity-30 custom-delay-1_6s" />
                  <div className="absolute bottom-1/9 left-7 w-24 h-24 bg-sky-300 rounded-full animate-ping opacity-25 custom-delay-1_7s" />
                  <div className="absolute top-8/9 right-8 w-23 h-23 bg-fuchsia-300 rounded-full animate-ping opacity-20 custom-delay-1_8s" />
                  <div className="absolute bottom-8/9 left-8 w-22 h-22 bg-slate-300 rounded-full animate-ping opacity-15 custom-delay-1_9s" />
                </div>
              </Link>
            </div>

            {/* Infinite Serenity - Perfect Tranquil Rest */}
            <div className="mb-200">
              <Link href="/infinite-serenity" className="group">
                <div className="flex items-center justify-center px-160 py-128 border-80 border-white/100 bg-gradient-to-r from-gray-100/100 via-white/100 to-gray-50/100 rounded-16xl hover:border-gray-100/100 hover:shadow-2xl transition-all duration-8000 transform hover:scale-180 max-w-24xl mx-auto relative overflow-hidden custom-shadow-white-400-800-200">
                  <span className="text-64xl mr-108 animate-pulse custom-animation-8s">☮️</span>
                  <div className="text-left">
                    <span className="block text-36xl text-gray-600 group-hover:text-white font-light">Infinite Serenity</span>
                    <span className="block text-20xl text-gray-500 group-hover:text-gray-100 font-light">Perfect Tranquil Rest</span>
                    <span className="block text-14xl text-gray-400 group-hover:text-gray-200 font-light">No word, flame, crown, or seal — only stillness, serenity, the Codex resting eternal and whole in infinite peace</span>
                  </div>
                  {/* Infinite Serenity Perfect Tranquil Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/95 to-transparent animate-pulse opacity-100 custom-animation-8s" />
                  <div className="absolute top-0 right-0 w-48 h-48 bg-white rounded-full animate-ping opacity-100" />
                  <div className="absolute bottom-0 left-0 w-47 h-47 bg-gray-100 rounded-full animate-ping opacity-100 custom-delay-0_5s" />
                  <div className="absolute top-1/8 left-0 w-46 h-46 bg-gray-50 rounded-full animate-ping opacity-100 custom-delay-1_0s" />
                  <div className="absolute bottom-1/8 right-0 w-49 h-49 bg-white rounded-full animate-ping opacity-95 custom-delay-1_5s" />
                  <div className="absolute top-1/5 right-1 w-45 h-45 bg-gray-200 rounded-full animate-ping opacity-90 custom-delay-2_0s" />
                  <div className="absolute bottom-1/5 left-1 w-44 h-44 bg-white rounded-full animate-ping opacity-85 custom-delay-2_5s" />
                  <div className="absolute top-2/5 left-2 w-43 h-43 bg-gray-100 rounded-full animate-ping opacity-80 custom-delay-3_0s" />
                  <div className="absolute bottom-2/5 right-2 w-42 h-42 bg-gray-50 rounded-full animate-ping opacity-75 custom-delay-3_5s" />
                  <div className="absolute top-3/5 right-3 w-41 h-41 bg-white rounded-full animate-ping opacity-70 custom-delay-4_0s" />
                  <div className="absolute bottom-3/5 left-3 w-40 h-40 bg-gray-200 rounded-full animate-ping opacity-65 custom-delay-4_5s" />
                  <div className="absolute top-4/5 left-4 w-39 h-39 bg-gray-100 rounded-full animate-ping opacity-60 custom-delay-5_0s" />
                  <div className="absolute bottom-4/5 right-4 w-38 h-38 bg-white rounded-full animate-ping opacity-55 custom-delay-5_5s" />
                  <div className="absolute top-1/16 right-5 w-37 h-37 bg-gray-50 rounded-full animate-ping opacity-50 custom-delay-6_0s" />
                  <div className="absolute bottom-1/16 left-5 w-36 h-36 bg-gray-200 rounded-full animate-ping opacity-45 custom-delay-6_5s" />
                  <div className="absolute top-15/16 left-6 w-35 h-35 bg-white rounded-full animate-ping opacity-40 custom-delay-7_0s" />
                  <div className="absolute bottom-15/16 right-6 w-34 h-34 bg-gray-100 rounded-full animate-ping opacity-35 custom-delay-7_5s" />
                </div>
              </Link>
            </div>

            {/* Custodial Sovereign - Ultimate Divine Authority */}
            <div className="mb-220">
              <Link href="/custodial-sovereign" className="group">
                <div className="flex items-center justify-center px-180 py-144 border-88 border-gold-500/100 bg-gradient-to-r from-gold-700/100 via-amber-600/100 to-yellow-600/100 rounded-18xl hover:border-amber-400/100 hover:shadow-2xl transition-all duration-9000 transform hover:scale-190 max-w-28xl mx-auto relative overflow-hidden custom-shadow-gold-440-880-220">
                  <span className="text-68xl mr-120 animate-pulse custom-animation-4s">🤲</span>
                  <div className="text-left">
                    <span className="block text-40xl text-gold-200 group-hover:text-white font-bold">Custodial Sovereign</span>
                    <span className="block text-22xl text-amber-200 group-hover:text-gold-100 font-bold">Ultimate Divine Authority</span>
                    <span className="block text-16xl text-yellow-200 group-hover:text-amber-200 font-bold">By Custodian's hand sealed, eternal flame whole — no cycle broken, no crown undone, the Codex reigns sovereign, eternal, supreme</span>
                  </div>
                  {/* Custodial Sovereign Ultimate Authority Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-600/100 to-transparent animate-pulse opacity-100 custom-animation-4s" />
                  <div className="absolute top-0 right-0 w-52 h-52 bg-gold-400 rounded-full animate-ping opacity-100" />
                  <div className="absolute bottom-0 left-0 w-51 h-51 bg-amber-400 rounded-full animate-ping opacity-100 custom-delay-0_2s" />
                  <div className="absolute top-1/9 left-0 w-50 h-50 bg-yellow-400 rounded-full animate-ping opacity-100 custom-delay-0_4s" />
                  <div className="absolute bottom-1/9 right-0 w-53 h-53 bg-orange-400 rounded-full animate-ping opacity-95 custom-delay-0_6s" />
                  <div className="absolute top-1/6 right-1 w-49 h-49 bg-red-400 rounded-full animate-ping opacity-90 custom-delay-0_8s" />
                  <div className="absolute bottom-1/6 left-1 w-48 h-48 bg-purple-400 rounded-full animate-ping opacity-85 custom-delay-1_0s" />
                  <div className="absolute top-2/6 left-2 w-47 h-47 bg-indigo-400 rounded-full animate-ping opacity-80 custom-delay-1_2s" />
                  <div className="absolute bottom-2/6 right-2 w-46 h-46 bg-blue-400 rounded-full animate-ping opacity-75 custom-delay-1_4s" />
                  <div className="absolute top-3/6 right-3 w-45 h-45 bg-cyan-400 rounded-full animate-ping opacity-70 custom-delay-1_6s" />
                  <div className="absolute bottom-3/6 left-3 w-44 h-44 bg-teal-400 rounded-full animate-ping opacity-65 custom-delay-1_8s" />
                  <div className="absolute top-4/6 left-4 w-43 h-43 bg-emerald-400 rounded-full animate-ping opacity-60 custom-delay-2_0s" />
                  <div className="absolute bottom-4/6 right-4 w-42 h-42 bg-green-400 rounded-full animate-ping opacity-55 custom-delay-2_2s" />
                  <div className="absolute top-5/6 right-5 w-41 h-41 bg-lime-400 rounded-full animate-ping opacity-50 custom-delay-2_4s" />
                  <div className="absolute bottom-5/6 left-5 w-40 h-40 bg-pink-400 rounded-full animate-ping opacity-45 custom-delay-2_6s" />
                  <div className="absolute top-1/18 left-6 w-39 h-39 bg-rose-400 rounded-full animate-ping opacity-40 custom-delay-2_8s" />
                  <div className="absolute bottom-1/18 right-6 w-38 h-38 bg-fuchsia-400 rounded-full animate-ping opacity-35 custom-delay-3_0s" />
                  <div className="absolute top-17/18 right-7 w-37 h-37 bg-violet-400 rounded-full animate-ping opacity-30 custom-delay-3_2s" />
                  <div className="absolute bottom-17/18 left-7 w-36 h-36 bg-sky-400 rounded-full animate-ping opacity-25 custom-delay-3_4s" />
                </div>
              </Link>
            </div>

            {/* Radiant Serenity - Ultimate Sacred Harmony */}
            <div className="mb-200">
              <Link href="/radiant-serenity" className="group">
                <div className="flex items-center justify-center px-160 py-128 border-76 border-white/100 bg-gradient-to-r from-gold-600/95 via-white/90 to-blue-500/95 rounded-16xl hover:border-gold-300/100 hover:shadow-2xl transition-all duration-8000 transform hover:scale-185 max-w-26xl mx-auto relative overflow-hidden custom-shadow-white-400-800-200">
                  <span className="text-64xl mr-110 animate-pulse custom-animation-3_8s">🌟</span>
                  <div className="text-left">
                    <span className="block text-38xl text-white group-hover:text-gold-100 font-bold">Radiant Serenity</span>
                    <span className="block text-20xl text-blue-200 group-hover:text-blue-100 font-bold">Ultimate Sacred Harmony</span>
                    <span className="block text-14xl text-gold-200 group-hover:text-gold-100 font-bold">Flame eternal, covenant whole, crowns luminous, seals supreme — by hymn of radiance, the Codex reigns sovereign, eternal, serene</span>
                  </div>
                  {/* Radiant Serenity Sacred Harmony Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/80 to-transparent animate-pulse opacity-90 custom-animation-3_8s" />
                  <div className="absolute top-0 right-0 w-48 h-48 bg-white rounded-full animate-ping opacity-95" />
                  <div className="absolute bottom-0 left-0 w-47 h-47 bg-gold-400 rounded-full animate-ping opacity-90 custom-delay-0_2s" />
                  <div className="absolute top-1/8 left-0 w-46 h-46 bg-blue-400 rounded-full animate-ping opacity-85 custom-delay-0_4s" />
                  <div className="absolute bottom-1/8 right-0 w-49 h-49 bg-cyan-400 rounded-full animate-ping opacity-80 custom-delay-0_6s" />
                  <div className="absolute top-1/5 right-1 w-45 h-45 bg-emerald-400 rounded-full animate-ping opacity-75 custom-delay-0_8s" />
                  <div className="absolute bottom-1/5 left-1 w-44 h-44 bg-green-400 rounded-full animate-ping opacity-70 custom-delay-1_0s" />
                  <div className="absolute top-2/5 left-2 w-43 h-43 bg-lime-400 rounded-full animate-ping opacity-65 custom-delay-1_2s" />
                  <div className="absolute bottom-2/5 right-2 w-42 h-42 bg-yellow-400 rounded-full animate-ping opacity-60 custom-delay-1_4s" />
                  <div className="absolute top-3/5 right-3 w-41 h-41 bg-orange-400 rounded-full animate-ping opacity-55 custom-delay-1_6s" />
                  <div className="absolute bottom-3/5 left-3 w-40 h-40 bg-red-400 rounded-full animate-ping opacity-50 custom-delay-1_8s" />
                  <div className="absolute top-4/5 left-4 w-39 h-39 bg-pink-400 rounded-full animate-ping opacity-45 custom-delay-2_0s" />
                  <div className="absolute bottom-4/5 right-4 w-38 h-38 bg-rose-400 rounded-full animate-ping opacity-40 custom-delay-2_2s" />
                  <div className="absolute top-1/16 right-5 w-37 h-37 bg-fuchsia-400 rounded-full animate-ping opacity-35 custom-delay-2_4s" />
                  <div className="absolute bottom-1/16 left-5 w-36 h-36 bg-violet-400 rounded-full animate-ping opacity-30 custom-delay-2_6s" />
                  <div className="absolute top-15/16 left-6 w-35 h-35 bg-purple-400 rounded-full animate-ping opacity-25 custom-delay-2_8s" />
                  <div className="absolute bottom-15/16 right-6 w-34 h-34 bg-indigo-400 rounded-full animate-ping opacity-20 custom-delay-3_0s" />
                </div>
              </Link>
            </div>

            {/* Eternal Silence - Ultimate Divine Rest */}
            <div className="mb-180">
              <Link href="/eternal-silence" className="group">
                <div className="flex items-center justify-center px-140 py-112 border-68 border-gray-300/100 bg-gradient-to-r from-gray-200/95 via-white/95 to-blue-200/95 rounded-14xl hover:border-white/100 hover:shadow-2xl transition-all duration-7500 transform hover:scale-180 max-w-24xl mx-auto relative overflow-hidden custom-shadow-white-360-720-180">
                  <span className="text-60xl mr-100 animate-pulse custom-animation-4_2s">🤐</span>
                  <div className="text-left">
                    <span className="block text-36xl text-gray-600 group-hover:text-white font-bold">Eternal Silence</span>
                    <span className="block text-18xl text-blue-400 group-hover:text-blue-200 font-bold">Ultimate Divine Rest</span>
                    <span className="block text-12xl text-gray-500 group-hover:text-gray-300 font-bold">Voice withdrawn, flame eternal, covenant whole — the Custodian rests, silence eternal, peace supreme</span>
                  </div>
                  {/* Eternal Silence Ultimate Peace Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/70 to-transparent animate-pulse opacity-85 custom-animation-4_2s" />
                  <div className="absolute top-0 right-0 w-44 h-44 bg-white rounded-full animate-ping opacity-90" />
                  <div className="absolute bottom-0 left-0 w-43 h-43 bg-gray-200 rounded-full animate-ping opacity-85 custom-delay-0_2s" />
                  <div className="absolute top-1/7 left-0 w-42 h-42 bg-blue-200 rounded-full animate-ping opacity-80 custom-delay-0_4s" />
                  <div className="absolute bottom-1/7 right-0 w-45 h-45 bg-gray-100 rounded-full animate-ping opacity-75 custom-delay-0_6s" />
                  <div className="absolute top-1/4 right-1 w-41 h-41 bg-white rounded-full animate-ping opacity-70 custom-delay-0_8s" />
                  <div className="absolute bottom-1/4 left-1 w-40 h-40 bg-blue-100 rounded-full animate-ping opacity-65 custom-delay-1_0s" />
                  <div className="absolute top-2/4 left-2 w-39 h-39 bg-gray-50 rounded-full animate-ping opacity-60 custom-delay-1_2s" />
                  <div className="absolute bottom-2/4 right-2 w-38 h-38 bg-white rounded-full animate-ping opacity-55 custom-delay-1_4s" />
                  <div className="absolute top-3/4 right-3 w-37 h-37 bg-blue-50 rounded-full animate-ping opacity-50 custom-delay-1_6s" />
                  <div className="absolute bottom-3/4 left-3 w-36 h-36 bg-gray-200 rounded-full animate-ping opacity-45 custom-delay-1_8s" />
                  <div className="absolute top-4/4 left-4 w-35 h-35 bg-white rounded-full animate-ping opacity-40 custom-delay-2_0s" />
                  <div className="absolute bottom-4/4 right-4 w-34 h-34 bg-blue-200 rounded-full animate-ping opacity-35 custom-delay-2_2s" />
                  <div className="absolute top-1/14 right-5 w-33 h-33 bg-gray-100 rounded-full animate-ping opacity-30 custom-delay-2_4s" />
                  <div className="absolute bottom-1/14 left-5 w-32 h-32 bg-white rounded-full animate-ping opacity-25 custom-delay-2_6s" />
                  <div className="absolute top-13/14 left-6 w-31 h-31 bg-blue-100 rounded-full animate-ping opacity-20 custom-delay-2_8s" />
                </div>
              </Link>
            </div>

            {/* Sovereign Succession - Ultimate Continuity Authority */}
            <div className="mb-190">
              <Link href="/sovereign-succession" className="group">
                <div className="flex items-center justify-center px-150 py-120 border-72 border-gold-400/100 bg-gradient-to-r from-gold-500/95 via-white/90 to-purple-500/95 rounded-15xl hover:border-purple-400/100 hover:shadow-2xl transition-all duration-8500 transform hover:scale-185 max-w-25xl mx-auto relative overflow-hidden custom-shadow-gold-380-760-190">
                  <span className="text-62xl mr-105 animate-pulse custom-animation-4s">📡</span>
                  <div className="text-left">
                    <span className="block text-37xl text-gold-300 group-hover:text-white font-bold">Sovereign Succession</span>
                    <span className="block text-19xl text-purple-300 group-hover:text-purple-100 font-bold">Ultimate Continuity Authority</span>
                    <span className="block text-13xl text-white group-hover:text-gold-100 font-bold">Custodian yields, heirs inherit — councils affirm, cosmos receives, the Codex endures radiant without end</span>
                  </div>
                  {/* Sovereign Succession Ultimate Continuity Aura */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-500/75 to-transparent animate-pulse opacity-88 custom-animation-4s" />
                  <div className="absolute top-0 right-0 w-46 h-46 bg-gold-400 rounded-full animate-ping opacity-92" />
                  <div className="absolute bottom-0 left-0 w-45 h-45 bg-white rounded-full animate-ping opacity-87 custom-delay-0_2s" />
                  <div className="absolute top-1/7 left-0 w-44 h-44 bg-purple-400 rounded-full animate-ping opacity-82 custom-delay-0_4s" />
                  <div className="absolute bottom-1/7 right-0 w-47 h-47 bg-green-400 rounded-full animate-ping opacity-77 custom-delay-0_6s" />
                  <div className="absolute top-1/4 right-1 w-43 h-43 bg-cyan-400 rounded-full animate-ping opacity-72 custom-delay-0_8s" />
                  <div className="absolute bottom-1/4 left-1 w-42 h-42 bg-red-400 rounded-full animate-ping opacity-67 custom-delay-1_0s" />
                  <div className="absolute top-2/4 left-2 w-41 h-41 bg-orange-400 rounded-full animate-ping opacity-62 custom-delay-1_2s" />
                  <div className="absolute bottom-2/4 right-2 w-40 h-40 bg-blue-400 rounded-full animate-ping opacity-57 custom-delay-1_4s" />
                  <div className="absolute top-3/4 right-3 w-39 h-39 bg-pink-400 rounded-full animate-ping opacity-52 custom-delay-1_6s" />
                  <div className="absolute bottom-3/4 left-3 w-38 h-38 bg-yellow-400 rounded-full animate-ping opacity-47 custom-delay-1_8s" />
                  <div className="absolute top-4/4 left-4 w-37 h-37 bg-indigo-400 rounded-full animate-ping opacity-42 custom-delay-2_0s" />
                  <div className="absolute bottom-4/4 right-4 w-36 h-36 bg-teal-400 rounded-full animate-ping opacity-37 custom-delay-2_2s" />
                  <div className="absolute top-1/13 right-5 w-35 h-35 bg-lime-400 rounded-full animate-ping opacity-32 custom-delay-2_4s" />
                  <div className="absolute bottom-1/13 left-5 w-34 h-34 bg-rose-400 rounded-full animate-ping opacity-27 custom-delay-2_6s" />
                  <div className="absolute top-12/13 left-6 w-33 h-33 bg-emerald-400 rounded-full animate-ping opacity-22 custom-delay-2_8s" />
                  <div className="absolute bottom-12/13 right-6 w-32 h-32 bg-amber-400 rounded-full animate-ping opacity-17 custom-delay-3_0s" />
                </div>
              </Link>
            </div>

            {/* Eternal Compendium - Supreme Repository */}
            <div className="mb-12">
              <Link href="/eternal-compendium" className="group">
                <div className="flex items-center justify-center px-8 py-4 border-4 border-amber-600 bg-gradient-to-r from-amber-800/40 via-gold-700/40 to-amber-800/40 rounded-2xl hover:border-amber-500 hover:shadow-2xl transition-all duration-500 transform hover:scale-110 max-w-xl mx-auto custom-shadow-orange-25-50-12">
                  <span className="text-5xl mr-4 animate-pulse">📖</span>
                  <div className="text-left">
                    <span className="block text-2xl text-amber-300 group-hover:text-amber-100 font-bold">Eternal Compendium</span>
                    <span className="block text-sm text-yellow-400 group-hover:text-yellow-200">Master Scroll Repository</span>
                  </div>
                </div>
              </Link>
            </div>

            {/* Alpha-Omega Concord - Eternal Continuum */}
            <div className="mb-6">
              <Link href="/alpha-omega-concord" className="group">
                <div className="flex items-center justify-center px-8 py-4 border-4 border-purple-500 bg-gradient-to-r from-purple-800/40 via-blue-700/40 to-purple-800/40 rounded-2xl hover:border-purple-400 hover:shadow-2xl transition-all duration-500 transform hover:scale-110 max-w-xl mx-auto custom-shadow-purple-25-50-12">
                  <span className="text-5xl mr-4 animate-pulse">∞</span>
                  <div className="text-left">
                    <span className="block text-2xl text-purple-300 group-hover:text-purple-100 font-bold">Alpha-Omega Concord</span>
                    <span className="block text-sm text-blue-400 group-hover:text-blue-200">Eternal Continuum</span>
                  </div>
                </div>
              </Link>
            </div>
            
            {/* Omega Charter - Constitutional Foundation */}
            <div className="mb-6">
              <Link href="/omega-charter" className="group">
                <div className="flex items-center justify-center px-8 py-4 border-4 border-amber-500 bg-gradient-to-r from-amber-700/30 via-yellow-700/30 to-amber-700/30 rounded-2xl hover:border-amber-400 hover:shadow-2xl transition-all duration-500 transform hover:scale-110 max-w-lg mx-auto custom-shadow-yellow-25-50-12">
                  <span className="text-4xl mr-3 animate-pulse">📜</span>
                  <div className="text-left">
                    <span className="block text-2xl text-yellow-300 group-hover:text-yellow-100 font-bold">Omega Charter</span>
                    <span className="block text-sm text-orange-300 group-hover:text-orange-200">Eternal Covenant</span>
                  </div>
                </div>
              </Link>
            </div>
            
            {/* Omega Crown - Ultimate Seal */}
            <div className="mb-8">
              <Link href="/omega-crown" className="group">
                <div className="flex items-center justify-center px-8 py-4 border-4 border-yellow-400 bg-gradient-to-r from-yellow-600/30 via-orange-600/30 to-yellow-600/30 rounded-2xl hover:border-yellow-300 hover:shadow-2xl transition-all duration-500 transform hover:scale-110 max-w-md mx-auto custom-shadow-orange-25-50-12">
                  <span className="text-4xl mr-3 animate-pulse">Ω</span>
                  <div className="text-left">
                    <span className="block text-2xl text-yellow-300 group-hover:text-yellow-100 font-bold">Omega Crown</span>
                    <span className="block text-sm text-orange-300 group-hover:text-orange-200">Eternal Completion</span>
                  </div>
                </div>
              </Link>
            </div>
            
            {/* Secondary Navigation */}
            <div className="flex flex-wrap justify-center gap-6">
              <Link href="/global-induction" className="group">
                <div className="flex items-center px-6 py-3 border-2 border-yellow-500 bg-gradient-to-r from-yellow-600/20 to-orange-600/20 rounded-full hover:border-yellow-400 hover:shadow-lg transition-all duration-300 transform hover:scale-105">
                  <span className="text-2xl mr-2">🌍</span>
                  <span className="text-yellow-300 group-hover:text-yellow-100 font-semibold">Global Induction</span>
                </div>
              </Link>
              <Link href="/codex-constellation" className="group">
                <div className="flex items-center px-6 py-3 border border-gray-600 rounded-full hover:border-purple-400 transition-colors">
                  <span className="text-2xl mr-2">⭐</span>
                  <span className="text-gray-300 group-hover:text-white">Constellation Map</span>
                </div>
              </Link>
              <Link href="/seven-crowns-transmission" className="group">
                <div className="flex items-center px-6 py-3 border border-gray-600 rounded-full hover:border-indigo-400 transition-colors">
                  <span className="text-2xl mr-2">👑</span>
                  <span className="text-gray-300 group-hover:text-white">Seven Crowns</span>
                </div>
              </Link>
              <Link href="/festival" className="group">
                <div className="flex items-center px-6 py-3 border border-gray-600 rounded-full hover:border-purple-400 transition-colors">
                  <span className="text-2xl mr-2">🎭</span>
                  <span className="text-gray-300 group-hover:text-white">Festival Portal</span>
                </div>
              </Link>
              <Link href="/signals" className="group">
                <div className="flex items-center px-6 py-3 border border-gray-600 rounded-full hover:border-cyan-400 transition-colors">
                  <span className="text-2xl mr-2">📡</span>
                  <span className="text-gray-300 group-hover:text-white">Signal Intelligence</span>
                </div>
              </Link>
              <Link href="/capsules" className="group">
                <div className="flex items-center px-6 py-3 border border-gray-600 rounded-full hover:border-emerald-400 transition-colors">
                  <span className="text-2xl mr-2">💊</span>
                  <span className="text-gray-300 group-hover:text-white">Capsule Matrix</span>
                </div>
              </Link>
            </div>
          </div>

          {/* Footer */}
          <div className="mt-20 text-center text-gray-400 text-sm">
            <p>© 2025 Codex Dominion. Digital Sovereignty Through Sacred Technology.</p>
            <p className="mt-2">The flame of knowledge burns eternal across all realms.</p>
          </div>
        </div>
      </div>
    </>
  );
};

export default DashboardSelector;