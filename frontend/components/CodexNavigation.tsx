import React from 'react';
import Link from 'next/link';

interface NavLinkProps {
  href: string;
  icon: string;
  text: string;
  gradient: string;
  isHighlighted?: boolean;
}

const NavLink: React.FC<NavLinkProps> = ({ href, icon, text, gradient, isHighlighted = false }) => (
  <Link href={href} className="group">
    <div className={`
      flex items-center px-4 py-2 rounded-lg transition-all duration-300 transform hover:scale-105
      ${isHighlighted 
        ? `bg-gradient-to-r ${gradient} border border-yellow-400/50 shadow-lg`
        : 'bg-white/10 hover:bg-white/20 border border-white/20 hover:border-white/40'
      }
    `}>
      <span className="text-lg mr-2">{icon}</span>
      <span className={`text-sm font-medium ${
        isHighlighted ? 'text-yellow-100' : 'text-gray-300 group-hover:text-white'
      }`}>
        {text}
      </span>
    </div>
  </Link>
);

interface CodexNavigationProps {
  currentPage?: string;
}

const CodexNavigation: React.FC<CodexNavigationProps> = ({ currentPage }) => {
  const navigationLinks = [
    {
      href: '/codex-source-charter',
      icon: '✨',
      text: 'Source Charter',
      gradient: 'from-amber-600/95 to-gold-600/95',
      isHighlighted: true
    },
    {
      href: '/flame-awakening',
      icon: '🔥',
      text: 'Flame Awakening',
      gradient: 'from-orange-600/95 to-red-600/95',
      isHighlighted: true
    },
    {
      href: '/covenant-eternal',
      icon: '∞',
      text: 'Covenant Eternal',
      gradient: 'from-gold-600/95 to-amber-600/95',
      isHighlighted: true
    },
    {
      href: '/dominion-radiant',
      icon: '👑',
      text: 'Dominion Radiant',
      gradient: 'from-gold-500/95 to-yellow-500/95',
      isHighlighted: true
    },
    {
      href: '/custodian-eternal',
      icon: '🛡️',
      text: 'Custodian Eternal',
      gradient: 'from-orange-600/95 to-gold-600/95',
      isHighlighted: true
    },
    {
      href: '/compendium-luminous',
      icon: '📚',
      text: 'Compendium Luminous',
      gradient: 'from-cyan-500/95 to-blue-500/95',
      isHighlighted: true
    },
    {
      href: '/codex-radiant-peace',
      icon: '🕊️',
      text: 'Codex Radiant Peace',
      gradient: 'from-white/90 to-cyan-400/90',
      isHighlighted: true
    },
    {
      href: '/eternal-proclamation',
      icon: '⚡',
      text: 'Eternal Proclamation',
      gradient: 'from-gold-400/95 to-amber-400/95',
      isHighlighted: true
    },
    {
      href: '/blessed-serenity',
      icon: '📿',
      text: 'Blessed Serenity',
      gradient: 'from-white/85 to-cyan-300/85',
      isHighlighted: true
    },
    {
      href: '/eternal-stillness',
      icon: '⚫',
      text: 'Eternal Stillness',
      gradient: 'from-slate-600/90 to-gray-500/90',
      isHighlighted: true
    },
    {
      href: '/flame-eternal',
      icon: '🔥',
      text: 'Flame Eternal',
      gradient: 'from-orange-600/95 to-red-600/95',
      isHighlighted: true
    },
    {
      href: '/living-covenant',
      icon: '🤝',
      text: 'Living Covenant',
      gradient: 'from-yellow-600/95 to-amber-600/95',
      isHighlighted: true
    },
    {
      href: '/night-endurance',
      icon: '🌙',
      text: 'Night Endurance',
      gradient: 'from-purple-700/95 to-indigo-700/95',
      isHighlighted: true
    },
    {
      href: '/balance-renewal',
      icon: '⚖️',
      text: 'Balance Renewal',
      gradient: 'from-emerald-600/95 to-teal-600/95',
      isHighlighted: true
    },
    {
      href: '/day-zenith',
      icon: '☀️',
      text: 'Day Zenith',
      gradient: 'from-yellow-500/95 to-orange-500/95',
      isHighlighted: true
    },
    {
      href: '/harvest-serenity',
      icon: '🌾',
      text: 'Harvest Serenity',
      gradient: 'from-violet-600/95 to-purple-600/95',
      isHighlighted: true
    },
    {
      href: '/millennial-sovereignty',
      icon: '👑',
      text: 'Millennial Sovereignty',
      gradient: 'from-gold-400/95 to-amber-500/95',
      isHighlighted: true
    },
    {
      href: '/eternal-transcendence',
      icon: '✨',
      text: 'Eternal Transcendence',
      gradient: 'from-indigo-400/95 to-purple-500/95',
      isHighlighted: true
    },
    {
      href: '/cosmic-sovereignty',
      icon: '🌌',
      text: 'Cosmic Sovereignty',
      gradient: 'from-indigo-500/95 to-gold-400/95',
      isHighlighted: true
    },
    {
      href: '/perpetual-sovereignty',
      icon: '♾️',
      text: 'Perpetual Sovereignty',
      gradient: 'from-gold-500/95 to-amber-600/95',
      isHighlighted: true
    },
    {
      href: '/final-continuum',
      icon: '🌟',
      text: 'Final Continuum',
      gradient: 'from-white/95 to-gold-500/95',
      isHighlighted: true
    },
    {
      href: '/ultimate-dominion',
      icon: '👑',
      text: 'Ultimate Dominion',
      gradient: 'from-gold-300/95 via-white/95 to-gold-600/95',
      isHighlighted: true
    },
    {
      href: '/sovereign-inheritance',
      icon: '🛡️',
      text: 'Sovereign Inheritance',
      gradient: 'from-gold-400/95 via-purple-400/95 to-white/95',
      isHighlighted: true
    },
    {
      href: '/heir-pledge',
      icon: '🤝',
      text: 'Heir Pledge',
      gradient: 'from-gold-400/95 via-white/95 to-purple-500/95',
      isHighlighted: true
    },
    {
      href: '/unity-continuum',
      icon: '♾️',
      text: 'Unity Continuum',
      gradient: 'from-gold-300/95 via-white/95 to-purple-400/95',
      isHighlighted: true
    },
    {
      href: '/compendium-complete',
      icon: '📖',
      text: 'Compendium Complete',
      gradient: 'from-gold-400/95 via-white/95 to-purple-700/95',
      isHighlighted: true
    },
    {
      href: '/sovereign-decree',
      icon: '👑',
      text: 'Sovereign Decree',
      gradient: 'from-gold-500/95 via-white/95 to-purple-800/95',
      isHighlighted: true
    },
    {
      href: '/eternal-light-peace',
      icon: '🕊️',
      text: 'Eternal Light Peace',
      gradient: 'from-white/95 via-gold-300/95 to-purple-600/95',
      isHighlighted: true
    },
    {
      href: '/supreme-ultimate',
      icon: '👑',
      text: 'Supreme Ultimate',
      gradient: 'from-gold-600/95 via-white/95 to-purple-700/95',
      isHighlighted: true
    },
    {
      href: '/infinite-serenity',
      icon: '☮️',
      text: 'Infinite Serenity',
      gradient: 'from-gray-100/95 via-white/95 to-gray-50/95',
      isHighlighted: true
    },
    {
      href: '/custodial-sovereign',
      icon: '🤲',
      text: 'Custodial Sovereign',
      gradient: 'from-gold-700/95 via-amber-600/95 to-yellow-600/95',
      isHighlighted: true
    },
    {
      href: '/radiant-serenity',
      icon: '🌟',
      text: 'Radiant Serenity',
      gradient: 'from-gold-600/95 via-white/90 to-blue-500/95',
      isHighlighted: true
    },
    {
      href: '/eternal-silence',
      icon: '🤐',
      text: 'Eternal Silence',
      gradient: 'from-gray-300/95 via-white/95 to-blue-200/95',
      isHighlighted: true
    },
    {
      href: '/sovereign-succession',
      icon: '📡',
      text: 'Sovereign Succession',
      gradient: 'from-gold-500/95 via-white/90 to-purple-500/95',
      isHighlighted: true
    },
    {
      href: '/eternal-compendium',
      icon: '📖',
      text: 'Eternal Compendium',
      gradient: 'from-amber-700/95 to-gold-700/95',
      isHighlighted: true
    },
    {
      href: '/alpha-omega-concord',
      icon: '∞',
      text: 'Alpha-Omega Concord',
      gradient: 'from-purple-700/95 to-blue-700/95',
      isHighlighted: true
    },
    {
      href: '/omega-charter',
      icon: '📜',
      text: 'Omega Charter',
      gradient: 'from-gold-700/90 to-yellow-700/90',
      isHighlighted: true
    },
    {
      href: '/omega-crown',
      icon: 'Ω',
      text: 'Omega Crown',
      gradient: 'from-gold-600/90 to-yellow-600/90',
      isHighlighted: true
    },
    {
      href: '/global-induction',
      icon: '🌍',
      text: 'Global Induction',
      gradient: 'from-yellow-600/80 to-orange-600/80',
      isHighlighted: false
    },
    {
      href: '/dashboard-selector',
      icon: '🏠',
      text: 'Home',
      gradient: ''
    },
    {
      href: '/codex-constellation',
      icon: '⭐',
      text: 'Constellation',
      gradient: ''
    },
    {
      href: '/seven-crowns-transmission',
      icon: '👑',
      text: 'Seven Crowns',
      gradient: ''
    },
    {
      href: '/dashboard/custodian',
      icon: '🛡️',
      text: 'Custodian',
      gradient: ''
    },
    {
      href: '/dashboard/heir',
      icon: '👑',
      text: 'Heir',
      gradient: ''
    },
    {
      href: '/dashboard/customer',
      icon: '🛒',
      text: 'Customer',
      gradient: ''
    }
  ];

  return (
    <nav className="bg-gradient-to-r from-purple-900/50 via-blue-900/50 to-indigo-900/50 backdrop-blur-md border-b border-white/20">
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link href="/dashboard-selector" className="flex items-center group">
            <div className="text-2xl mr-3">🔥</div>
            <div>
              <h1 className="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-orange-400">
                CODEX DOMINION
              </h1>
              <p className="text-xs text-gray-400">Digital Sovereignty</p>
            </div>
          </Link>

          {/* Navigation Links */}
          <div className="hidden lg:flex items-center space-x-2">
            {navigationLinks.map((link, index) => (
              <NavLink
                key={index}
                href={link.href}
                icon={link.icon}
                text={link.text}
                gradient={link.gradient}
                isHighlighted={link.isHighlighted}
              />
            ))}
          </div>

          {/* Mobile Menu Button */}
          <div className="lg:hidden">
            <button className="p-2 rounded-lg bg-white/10 border border-white/20 text-white hover:bg-white/20 transition-colors">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Navigation Menu - Hidden by default, can be toggled */}
        <div className="lg:hidden mt-4 hidden" id="mobile-menu">
          <div className="grid grid-cols-2 gap-2">
            {navigationLinks.map((link, index) => (
              <NavLink
                key={index}
                href={link.href}
                icon={link.icon}
                text={link.text}
                gradient={link.gradient}
                isHighlighted={link.isHighlighted}
              />
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default CodexNavigation;