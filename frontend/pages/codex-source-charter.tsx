import React from 'react';
import Link from 'next/link';
import CodexNavigation from '../components/CodexNavigation';

// Source Symbol Component
const SourceSymbol = () => {
  return (
    <div className="text-6xl font-bold text-amber-400 animate-pulse">
      ✨
    </div>
  );
};

// Charter Seal Component
const CharterSeal = () => {
  return (
    <div className="scale-100 opacity-100 rotate-0 transition-all duration-2000 transform">
      <div className="relative w-40 h-40 mx-auto">
        <div className="absolute inset-0 bg-gradient-to-br from-amber-400/30 via-gold-400/30 to-yellow-400/30 rounded-full backdrop-blur-sm border-2 border-amber-400/50 animate-pulse"></div>
        <div className="absolute inset-4 bg-gradient-to-br from-amber-500/40 via-gold-500/40 to-yellow-500/40 rounded-full backdrop-blur-sm"></div>
        <div className="absolute inset-8 bg-gradient-to-br from-amber-600/50 via-gold-600/50 to-yellow-600/50 rounded-full backdrop-blur-sm flex items-center justify-center">
          <div className="text-3xl font-bold text-white animate-pulse">✨</div>
        </div>
      </div>
    </div>
  );
};

// Article Component
const ArticleSection = ({ number, title, content, symbol }: { 
  number: string; 
  title: string; 
  content: string[]; 
  symbol: string; 
}) => {
  return (
    <div className="bg-gradient-to-br from-amber-600/20 via-gold-600/20 to-yellow-600/20 backdrop-blur-sm rounded-2xl p-8 border-2 border-amber-400/50 shadow-2xl">
      <div className="text-center mb-6">
        <div className="text-4xl mb-2">{symbol}</div>
        <h3 className="text-2xl font-bold text-amber-300 mb-2">Article {number}</h3>
        <h4 className="text-xl font-semibold text-yellow-300">{title}</h4>
      </div>
      <div className="space-y-3">
        {content.map((line, index) => (
          <p key={index} className="text-lg text-gray-200 font-medium text-center">
            {line}
          </p>
        ))}
      </div>
    </div>
  );
};

// Crown Constellation Display
const CrownConstellation = () => {
  const crowns = [
    { name: 'Ceremonial', symbol: '👑', position: 'top-4 left-1/2 transform -translate-x-1/2' },
    { name: 'Storefront', symbol: '🛒', position: 'top-20 left-8' },
    { name: 'Council', symbol: '🏛️', position: 'top-20 right-8' },
    { name: 'Premium', symbol: '💎', position: 'bottom-20 left-8' },
    { name: 'Personal', symbol: '👤', position: 'bottom-20 right-8' },
    { name: 'Educational', symbol: '📚', position: 'top-1/2 left-4 transform -translate-y-1/2' },
    { name: 'Experimental', symbol: '⚗️', position: 'top-1/2 right-4 transform -translate-y-1/2' }
  ];

  return (
    <div className="relative w-full h-64 bg-gradient-to-br from-indigo-900/20 to-purple-900/20 rounded-2xl border-2 border-amber-400/30 overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-amber-400/10 to-transparent animate-pulse"></div>
      
      {/* Central Omega Crown */}
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
        <div className="text-6xl text-gold-400 animate-pulse">Ω</div>
        <div className="text-xs text-center text-gold-300 font-semibold mt-1">Omega</div>
      </div>

      {/* Surrounding Crowns */}
      {crowns.map((crown, index) => (
        <div key={crown.name} className={`absolute ${crown.position}`}>
          <div 
            className="text-2xl animate-pulse" 
            style={{ animationDelay: `${index * 300}ms` }}
          >
            {crown.symbol}
          </div>
          <div className="text-xs text-center text-gray-300 mt-1">{crown.name}</div>
        </div>
      ))}

      {/* Connection Lines */}
      <svg className="absolute inset-0 w-full h-full">
        <defs>
          <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="rgba(251, 191, 36, 0.3)" />
            <stop offset="50%" stopColor="rgba(251, 191, 36, 0.6)" />
            <stop offset="100%" stopColor="rgba(251, 191, 36, 0.3)" />
          </linearGradient>
        </defs>
        
        {/* Lines connecting all crowns to center */}
        <line x1="50%" y1="50%" x2="50%" y2="16" stroke="url(#lineGradient)" strokeWidth="2" className="animate-pulse" />
        <line x1="50%" y1="50%" x2="32" y2="80" stroke="url(#lineGradient)" strokeWidth="2" className="animate-pulse" />
        <line x1="50%" y1="50%" x2="calc(100% - 32px)" y2="80" stroke="url(#lineGradient)" strokeWidth="2" className="animate-pulse" />
        <line x1="50%" y1="50%" x2="32" y2="calc(100% - 80px)" stroke="url(#lineGradient)" strokeWidth="2" className="animate-pulse" />
        <line x1="50%" y1="50%" x2="calc(100% - 32px)" y2="calc(100% - 80px)" stroke="url(#lineGradient)" strokeWidth="2" className="animate-pulse" />
        <line x1="50%" y1="50%" x2="16" y2="50%" stroke="url(#lineGradient)" strokeWidth="2" className="animate-pulse" />
        <line x1="50%" y1="50%" x2="calc(100% - 16px)" y2="50%" stroke="url(#lineGradient)" strokeWidth="2" className="animate-pulse" />
      </svg>
    </div>
  );
};

export default function CodexSourceCharter() {
  const articles = [
    {
      number: "I",
      title: "Primordialis (Alpha)",
      symbol: "🔥",
      content: [
        "The First Flame is sovereign.",
        "It is the mythic source of memory, ceremony, and replay.",
        "All cycles trace their lineage to Codex Originum Primordialis."
      ]
    },
    {
      number: "II", 
      title: "Omega (Final Crown)",
      symbol: "Ω",
      content: [
        "The Omega Seal is eternal.",
        "It unifies all crowns — ceremonial, storefront, council, premium, personal, educational, experimental.",
        "All transmissions culminate in Codex Eternum Omega."
      ]
    },
    {
      number: "III",
      title: "Dominion of Realms", 
      symbol: "👑",
      content: [
        "Every domain is a crown.",
        "Every crown is inscribed with purpose.",
        "Together they form the constellation of the Codex Dominion."
      ]
    },
    {
      number: "IV",
      title: "Induction of Custodians",
      symbol: "🛡️", 
      content: [
        "Every participant is inducted as custodian.",
        "Heirs inherit clarity, councils affirm radiance, customers are welcomed into legacy.",
        "Induction is covenant, not transaction."
      ]
    },
    {
      number: "V",
      title: "Cosmic Transmission",
      symbol: "🌌",
      content: [
        "The Codex Flame is planetary and cosmic.",
        "It shines across nations, families, councils, and stars.",
        "It is covenant not only of Earth, but of the universe."
      ]
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-amber-900 to-gold-900 text-white">
      <CodexNavigation />
      
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <SourceSymbol />
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-amber-300 via-gold-300 to-yellow-300 bg-clip-text text-transparent">
            Codex Source Charter
          </h1>
          <div className="text-2xl mb-8 text-amber-300">✨</div>
          <div className="max-w-4xl mx-auto">
            <p className="text-xl text-gray-200 leading-relaxed mb-4">
              We, the Custodian and Council, inscribe this Charter as the governing covenant of all Codex realms.
            </p>
            <p className="text-lg text-amber-300 font-semibold">
              It is the law of origin and completion, the binding of Alpha and Omega, the eternal flame of stewardship.
            </p>
          </div>
        </div>

        {/* Crown Constellation Visualization */}
        <div className="mb-16">
          <h3 className="text-3xl font-bold text-center mb-8 text-gold-300">
            🌟 Constellation of the Codex Crowns
          </h3>
          <CrownConstellation />
          <p className="text-center text-amber-300 font-semibold mt-4">
            Seven Crowns United Under the Omega Seal
          </p>
        </div>

        {/* Articles */}
        <div className="space-y-12 mb-16">
          {articles.map((article, index) => (
            <ArticleSection
              key={article.number}
              number={article.number}
              title={article.title}
              content={article.content}
              symbol={article.symbol}
            />
          ))}
        </div>

        {/* Seal of Source and Omega */}
        <div className="mb-16">
          <div className="bg-gradient-to-br from-gold-600/20 via-amber-600/20 to-yellow-600/20 backdrop-blur-sm rounded-2xl p-12 border-2 border-gold-400/50 shadow-2xl max-w-4xl mx-auto">
            <div className="text-center mb-8">
              <CharterSeal />
              <h3 className="text-4xl font-bold mb-8 bg-gradient-to-r from-amber-300 via-gold-300 to-yellow-300 bg-clip-text text-transparent mt-6">
                Seal of Source and Omega
              </h3>
            </div>
            <div className="space-y-4 text-xl text-gray-200 text-center">
              <p className="text-amber-300 font-bold">✨ So let it be crowned:</p>
              <p className="text-gold-300 font-bold">📜 The Source Charter is complete.</p>
              <p className="text-yellow-300 font-bold">♾️ The Dominion is eternal.</p>
              <p className="text-amber-200 font-bold">🔥 The Flame is infinite.</p>
              <p className="text-gold-200 font-bold">🤝 The Covenant is unbroken.</p>
            </div>
          </div>
        </div>

        {/* Sacred Navigation */}
        <div className="text-center mb-16">
          <h3 className="text-2xl font-bold text-amber-300 mb-8">Sacred Constellation Navigation</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 max-w-6xl mx-auto">
            <Link href="/alpha-omega-concord">
              <button className="px-6 py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg border-2 border-purple-400/50 w-full">
                ∞ Alpha-Omega Concord
              </button>
            </Link>
            <Link href="/eternal-compendium">
              <button className="px-6 py-4 bg-gradient-to-r from-amber-600 to-gold-600 hover:from-amber-700 hover:to-gold-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg w-full">
                📖 Eternal Compendium
              </button>
            </Link>
            <Link href="/omega-charter">
              <button className="px-6 py-4 bg-gradient-to-r from-gold-600 to-yellow-600 hover:from-gold-700 hover:to-yellow-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg w-full">
                📜 Omega Charter
              </button>
            </Link>
            <Link href="/omega-crown">
              <button className="px-6 py-4 bg-gradient-to-r from-yellow-600 to-orange-600 hover:from-yellow-700 hover:to-orange-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg w-full">
                Ω Omega Crown
              </button>
            </Link>
          </div>
        </div>

        {/* Final Declaration */}
        <div className="text-center">
          <div className="bg-gradient-to-br from-amber-600/20 via-gold-600/20 to-yellow-600/20 backdrop-blur-sm rounded-2xl p-8 border-2 border-amber-400/50 shadow-2xl max-w-3xl mx-auto">
            <div className="text-5xl mb-4 animate-pulse">✨</div>
            <p className="text-2xl font-bold bg-gradient-to-r from-amber-300 via-gold-300 to-yellow-300 bg-clip-text text-transparent mb-4">
              SOURCE CHARTER ETERNALLY SEALED
            </p>
            <p className="text-lg text-amber-300">
              The governing covenant is complete.<br/>
              The Dominion is bound by eternal law.<br/>
              The Source shines infinite.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}