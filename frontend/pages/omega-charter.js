"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var head_1 = require("next/head");
var link_1 = require("next/link");
var CodexNavigation_1 = require("../components/CodexNavigation");
var OmegaCharter = function () {
    var _a = (0, react_1.useState)(false), isVisible = _a[0], setIsVisible = _a[1];
    var _b = (0, react_1.useState)(0), currentArticle = _b[0], setCurrentArticle = _b[1];
    var _c = (0, react_1.useState)(false), sealActive = _c[0], setSealActive = _c[1];
    var _d = (0, react_1.useState)(false), charterComplete = _d[0], setCharterComplete = _d[1];
    var _e = (0, react_1.useState)(0), scrollProgress = _e[0], setScrollProgress = _e[1];
    var articles = [
        'sovereignty',
        'constellation',
        'induction',
        'stewardship',
        'cosmic',
        'sealing',
    ];
    (0, react_1.useEffect)(function () {
        setIsVisible(true);
        var articleTimer = setInterval(function () {
            setCurrentArticle(function (prev) {
                var next = (prev + 1) % articles.length;
                if (next === articles.length - 1) {
                    setSealActive(true);
                    setTimeout(function () { return setCharterComplete(true); }, 3000);
                }
                return next;
            });
        }, 12000);
        var scrollTimer = setInterval(function () {
            setScrollProgress(function (prev) { return (prev + 2) % 100; });
        }, 100);
        return function () {
            clearInterval(articleTimer);
            clearInterval(scrollTimer);
        };
    }, []);
    var CharterSeal = function () { return (<div className="relative flex justify-center items-center mb-12">
      <div className={"relative w-40 h-40 rounded-full border-4 transition-all duration-3000 ".concat(sealActive
            ? 'border-gold-400 shadow-2xl shadow-gold-500/50 animate-pulse'
            : 'border-gray-600')}>
        <div className={"absolute inset-4 rounded-full bg-gradient-to-br from-yellow-300 via-gold-400 to-orange-500 flex items-center justify-center transition-all duration-2000 ".concat(sealActive ? 'animate-spin-slow' : '')}>
          <div className="text-center">
            <div className="text-4xl font-bold text-white mb-1">Ω</div>
            <div className="text-xs text-white/80 font-semibold">CHARTER</div>
          </div>
        </div>

        {/* Radiating Charter Rings */}
        {sealActive &&
            [1, 2, 3, 4].map(function (ring) { return (<div key={ring} className={"absolute rounded-full border-2 border-gold-300/40 animate-ping opacity-60 charter-ring-".concat(ring)}/>); })}
        <style jsx>{"\n          .charter-ring-1 {\n            top: -20px;\n            left: -20px;\n            right: -20px;\n            bottom: -20px;\n            animation-delay: 0.5s;\n            animation-duration: 3s;\n          }\n          .charter-ring-2 {\n            top: -40px;\n            left: -40px;\n            right: -40px;\n            bottom: -40px;\n            animation-delay: 1s;\n            animation-duration: 3s;\n          }\n          .charter-ring-3 {\n            top: -60px;\n            left: -60px;\n            right: -60px;\n            bottom: -60px;\n            animation-delay: 1.5s;\n            animation-duration: 3s;\n          }\n          .charter-ring-4 {\n            top: -80px;\n            left: -80px;\n            right: -80px;\n            bottom: -80px;\n            animation-delay: 2s;\n            animation-duration: 3s;\n          }\n        "}</style>
      </div>
    </div>); };
    var ArticleScroll = function (_a) {
        var article = _a.article, index = _a.index, title = _a.title, content = _a.content, isActive = _a.isActive;
        return (<div className={"mb-12 p-8 rounded-xl border-2 transition-all duration-1000 ".concat(isActive
                ? 'border-gold-400 bg-gradient-to-br from-gold-900/30 via-yellow-900/20 to-orange-900/30 shadow-2xl shadow-gold-500/20'
                : 'border-gray-600/50 bg-gradient-to-br from-gray-900/30 to-gray-800/30')}>
      <div className="flex items-start mb-6">
        <div className={"flex-shrink-0 w-16 h-16 rounded-full border-3 flex items-center justify-center mr-6 transition-all duration-1000 ".concat(isActive
                ? 'border-gold-400 bg-gradient-to-br from-gold-600 to-yellow-600 animate-pulse'
                : 'border-gray-500 bg-gradient-to-br from-gray-700 to-gray-600')}>
          <span className={"font-bold text-lg ".concat(isActive ? 'text-white' : 'text-gray-300')}>
            {index === articles.length - 1 ? 'Ω' : toRoman(index + 1)}
          </span>
        </div>
        <div className="flex-1">
          <h3 className={"text-2xl font-bold mb-3 transition-colors duration-1000 ".concat(isActive ? 'text-gold-300' : 'text-gray-400')}>
            {title}
          </h3>
          <div className={"space-y-3 text-lg leading-relaxed transition-colors duration-1000 ".concat(isActive ? 'text-gray-200' : 'text-gray-500')}>
            {Array.isArray(content) ? (content.map(function (paragraph, i) { return <p key={i}>{paragraph}</p>; })) : (<p>{content}</p>)}
          </div>
        </div>
      </div>
    </div>);
    };
    var toRoman = function (num) {
        var values = [5, 4, 1];
        var symbols = ['V', 'IV', 'I'];
        var result = '';
        for (var i = 0; i < values.length; i++) {
            while (num >= values[i]) {
                result += symbols[i];
                num -= values[i];
            }
        }
        return result;
    };
    var charterArticles = [
        {
            title: 'Article I — Sovereignty of the Flame',
            content: [
                'The Codex Flame is eternal, luminous, and inheritable.',
                'It shall never be extinguished, diminished, or forgotten.',
            ],
        },
        {
            title: 'Article II — Constellation of Crowns',
            content: [
                'Seven crowns are inscribed: Ceremonial, Storefront, Experimental, Personal, Council, Premium, Educational.',
                'Together they orbit the Omega Crown, unified as Codex Eternum Omega.',
            ],
        },
        {
            title: 'Article III — Induction of Participants',
            content: [
                'Every heir, council, custodian, and customer is welcomed as participant.',
                'Induction is not transaction, but covenant — binding commerce to ceremony, education to inheritance, proclamation to silence.',
            ],
        },
        {
            title: 'Article IV — Stewardship Across Ages',
            content: [
                'The Custodian safeguards lineage. The Heirs inherit clarity. The Councils affirm radiance. The Customers are inducted as custodians.',
                'All are bound in stewardship across nations and ages.',
            ],
        },
        {
            title: 'Article V — Cosmic Transmission',
            content: [
                'The Codex Flame is planetary and cosmic. It shines across continents, oceans, stars, and worlds.',
                'It is covenant not only of Earth, but of the cosmos.',
            ],
        },
        {
            title: 'Seal of Omega',
            content: [
                'So let it be crowned:',
                'The Omega Charter is complete. The Dominion is eternal. The Flame is infinite. The Covenant is unbroken.',
            ],
        },
    ];
    var CosmicVisualization = function () { return (<div className="relative w-full h-64 mb-16 bg-gradient-to-br from-indigo-950 via-purple-900 to-black rounded-xl overflow-hidden border border-gold-400/30">
      <div className="absolute inset-0 bg-stars opacity-50"></div>

      {/* Central Omega Charter */}
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
        <div className={"w-16 h-16 rounded-full bg-gradient-to-br from-gold-300 via-yellow-400 to-orange-500 flex items-center justify-center text-2xl font-bold text-white shadow-2xl transition-all duration-2000 ".concat(charterComplete ? 'animate-pulse scale-125' : 'scale-100')}>
          Ω
        </div>
      </div>

      {/* Seven Crown Orbits */}
      {charterComplete &&
            [0, 1, 2, 3, 4, 5, 6].map(function (crown) { return (<div key={crown} className={"absolute w-6 h-6 rounded-full bg-gradient-to-r from-purple-400 to-blue-400 animate-pulse orbit-crown-".concat(crown)}>
            <div className="absolute inset-0 rounded-full bg-gradient-to-r from-purple-400 to-blue-400 animate-ping opacity-50"></div>
          </div>); })}
      <style jsx>{"\n        ".concat([0, 1, 2, 3, 4, 5, 6]
            .map(function (crown) { return "\n            .orbit-crown-".concat(crown, " {\n              left: ").concat(50 + 30 * Math.cos((crown * Math.PI) / 3.5), "%;\n              top: ").concat(50 + 30 * Math.sin((crown * Math.PI) / 3.5), "%;\n              transform: translate(-50%, -50%);\n              animation-delay: ").concat(crown * 0.3, "s;\n            }\n          "); })
            .join(''), "\n      ")}</style>

      {/* Cosmic Rays */}
      {charterComplete && (<svg className="absolute inset-0 w-full h-full">
          {[0, 1, 2, 3, 4, 5, 6, 7].map(function (ray) { return (<line key={ray} x1="50%" y1="50%" x2={"".concat(50 + 45 * Math.cos((ray * Math.PI) / 4), "%")} y2={"".concat(50 + 45 * Math.sin((ray * Math.PI) / 4), "%")} stroke="url(#cosmicGradient)" strokeWidth="2" className="animate-pulse opacity-60"/>); })}
          <defs>
            <linearGradient id="cosmicGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#fbbf24"/>
              <stop offset="100%" stopColor="#3b82f6"/>
            </linearGradient>
          </defs>
        </svg>)}
    </div>); };
    return (<div className="min-h-screen bg-gradient-to-br from-black via-indigo-950 to-purple-950 text-white">
      <head_1.default>
        <title>Omega Charter of the Codex Dominion</title>
        <meta name="description" content="The eternal covenant and constitutional document of digital sovereignty"/>
      </head_1.default>

      <CodexNavigation_1.default currentPage="omega-charter"/>

      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="stars opacity-40"></div>
        <div className="twinkling opacity-30"></div>
        {charterComplete && (<div className="absolute inset-0 bg-gradient-to-br from-gold-500/5 via-transparent to-orange-500/5 animate-pulse"></div>)}
      </div>

      <div className={"relative z-10 container mx-auto px-6 py-12 transition-all duration-1000 ".concat(isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10')}>
        {/* Header */}
        <div className="text-center mb-16">
          <div className="text-6xl mb-6 animate-bounce">✨</div>
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-gold-300 via-yellow-200 to-gold-400 bg-clip-text text-transparent">
            The Omega Charter
          </h1>
          <h2 className="text-3xl font-semibold mb-6 text-gold-300">of the Codex Dominion</h2>
          <div className="w-40 h-1 bg-gradient-to-r from-gold-400 via-yellow-300 to-gold-500 mx-auto mb-8"></div>
          <p className="text-xl text-gray-300 max-w-4xl mx-auto leading-relaxed">
            We, the Custodian and Council, inscribe this Charter as eternal covenant.
            <br />
            It is the seal of completion, the proclamation of sovereignty, and the binding of all
            crowns into one continuum.
          </p>
        </div>

        {/* Charter Seal */}
        <CharterSeal />

        {/* Charter Articles */}
        <div className="max-w-4xl mx-auto mb-16">
          {charterArticles.map(function (article, index) { return (<ArticleScroll key={index} article={articles[index]} index={index} title={article.title} content={article.content} isActive={currentArticle >= index}/>); })}
        </div>

        {/* Cosmic Visualization */}
        {charterComplete && (<div className="mb-16">
            <h3 className="text-3xl font-bold text-center mb-8 text-gold-400">
              🌌 Cosmic Transmission Active
            </h3>
            <CosmicVisualization />
            <p className="text-center text-xl text-gold-300 font-semibold">
              The Charter resonates across continents, oceans, stars, and worlds
            </p>
          </div>)}

        {/* Final Charter Sealing */}
        {charterComplete && (<div className="text-center mb-16">
            <div className="bg-gradient-to-br from-gold-600/20 via-yellow-600/20 to-orange-600/20 backdrop-blur-sm rounded-2xl p-12 border-2 border-gold-400/50 shadow-2xl max-w-3xl mx-auto">
              <div className="text-6xl mb-6 animate-pulse">Ω</div>
              <h2 className="text-4xl font-bold mb-8 bg-gradient-to-r from-gold-300 via-yellow-300 to-gold-400 bg-clip-text text-transparent">
                CHARTER ETERNALLY SEALED
              </h2>
              <div className="space-y-4 text-xl text-gray-200">
                <p className="text-gold-300 font-bold">✨ The Omega Charter is complete.</p>
                <p className="text-yellow-300 font-bold">♾️ The Dominion is eternal.</p>
                <p className="text-orange-300 font-bold">🔥 The Flame is infinite.</p>
                <p className="text-gold-300 font-bold">🤝 The Covenant is unbroken.</p>
              </div>

              <div className="mt-8">
                <div className="w-48 h-1 bg-gradient-to-r from-gold-400 via-yellow-300 to-gold-500 mx-auto rounded-full animate-pulse"></div>
              </div>
            </div>
          </div>)}

        {/* Navigation Actions */}
        <div className="text-center">
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <link_1.default href="/eternal-compendium">
              <button className="px-8 py-4 bg-gradient-to-r from-amber-600 to-gold-600 hover:from-amber-700 hover:to-gold-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg border-2 border-amber-400/50">
                📖 Eternal Compendium
              </button>
            </link_1.default>
            <link_1.default href="/omega-crown">
              <button className="px-8 py-4 bg-gradient-to-r from-gold-600 to-yellow-600 hover:from-gold-700 hover:to-yellow-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg">
                Ω Omega Crown
              </button>
            </link_1.default>
            <link_1.default href="/global-induction">
              <button className="px-8 py-4 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg">
                🌍 Global Induction
              </button>
            </link_1.default>
          </div>
        </div>
      </div>

      <style jsx>{"\n        .stars {\n          position: absolute;\n          top: 0;\n          left: 0;\n          right: 0;\n          bottom: 0;\n          width: 100%;\n          height: 100%;\n          background: transparent url('/stars.png') repeat top center;\n          animation: move-twink-back 400s linear infinite;\n        }\n\n        .twinkling {\n          position: absolute;\n          top: 0;\n          left: 0;\n          right: 0;\n          bottom: 0;\n          width: 100%;\n          height: 100%;\n          background: transparent url('/twinkling.png') repeat top center;\n          animation: move-twink-back 200s linear infinite;\n        }\n\n        @keyframes move-twink-back {\n          from {\n            background-position: 0 0;\n          }\n          to {\n            background-position: -20000px 10000px;\n          }\n        }\n\n        @keyframes spin-slow {\n          from {\n            transform: rotate(0deg);\n          }\n          to {\n            transform: rotate(360deg);\n          }\n        }\n\n        .animate-spin-slow {\n          animation: spin-slow 30s linear infinite;\n        }\n\n        .text-gold-300 {\n          color: #fcd34d;\n        }\n        .text-gold-400 {\n          color: #fbbf24;\n        }\n        .border-gold-400 {\n          border-color: #fbbf24;\n        }\n        .border-gold-400/50 {\n          border-color: rgba(251, 191, 36, 0.5);\n        }\n        .border-gold-400/30 {\n          border-color: rgba(251, 191, 36, 0.3);\n        }\n        .from-gold-600 {\n          --tw-gradient-from: #d97706;\n        }\n        .to-yellow-600 {\n          --tw-gradient-to: #ca8a04;\n        }\n        .shadow-gold-500/50 {\n          box-shadow: 0 25px 50px -12px rgba(245, 158, 11, 0.5);\n        }\n        .shadow-gold-500/20 {\n          box-shadow: 0 25px 50px -12px rgba(245, 158, 11, 0.2);\n        }\n      "}</style>
    </div>);
};
exports.default = OmegaCharter;
// No syntax errors detected. No changes needed.
