"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var head_1 = require("next/head");
var link_1 = require("next/link");
var CodexNavigation_1 = require("../components/CodexNavigation");
var OmegaCrown = function () {
    var _a = (0, react_1.useState)(false), isVisible = _a[0], setIsVisible = _a[1];
    var _b = (0, react_1.useState)(0), currentPhase = _b[0], setCurrentPhase = _b[1];
    var _c = (0, react_1.useState)(0), unifiedCrowns = _c[0], setUnifiedCrowns = _c[1];
    var _d = (0, react_1.useState)(0), omegaPulse = _d[0], setOmegaPulse = _d[1];
    var _e = (0, react_1.useState)(false), eternityActive = _e[0], setEternityActive = _e[1];
    var phases = ['unification', 'constellation', 'blessing', 'sealing'];
    var crowns = [
        {
            name: 'Ceremonial Crown',
            domain: 'codexdominion.app',
            color: 'from-purple-600 to-indigo-800',
            icon: '👑',
            position: { x: 50, y: 20 },
            element: 'Sacred Ceremonies',
        },
        {
            name: 'Storefront Crown',
            domain: 'aistorelab.com',
            color: 'from-blue-600 to-cyan-800',
            icon: '🛒',
            position: { x: 20, y: 40 },
            element: 'Sacred Commerce',
        },
        {
            name: 'Experimental Crown',
            domain: 'aistorelab.online',
            color: 'from-teal-600 to-green-800',
            icon: '🔬',
            position: { x: 80, y: 40 },
            element: 'Innovation Labs',
        },
        {
            name: 'Personal Crown',
            domain: 'jermaineai.com',
            color: 'from-amber-600 to-orange-800',
            icon: '👤',
            position: { x: 15, y: 70 },
            element: 'Individual Sovereignty',
        },
        {
            name: 'Council Crown',
            domain: 'jermaineai.online',
            color: 'from-red-600 to-pink-800',
            icon: '🏛️',
            position: { x: 50, y: 80 },
            element: 'Governance Wisdom',
        },
        {
            name: 'Premium Crown',
            domain: 'jermaineai.store',
            color: 'from-violet-600 to-purple-800',
            icon: '💎',
            position: { x: 85, y: 70 },
            element: 'Elite Mastery',
        },
        {
            name: 'Educational Crown',
            domain: 'themerrittmethod.com',
            color: 'from-emerald-600 to-blue-800',
            icon: '📚',
            position: { x: 50, y: 50 },
            element: 'Knowledge Transmission',
        },
    ];
    (0, react_1.useEffect)(function () {
        setIsVisible(true);
        var phaseTimer = setInterval(function () {
            setCurrentPhase(function (prev) {
                var next = (prev + 1) % phases.length;
                if (next === 3)
                    setEternityActive(true);
                return next;
            });
        }, 10000);
        var crownTimer = setInterval(function () {
            setUnifiedCrowns(function (prev) {
                if (prev < crowns.length)
                    return prev + 1;
                return prev;
            });
        }, 1500);
        var pulseTimer = setInterval(function () {
            setOmegaPulse(function (prev) { return (prev + 1) % 100; });
        }, 2000);
        return function () {
            clearInterval(phaseTimer);
            clearInterval(crownTimer);
            clearInterval(pulseTimer);
        };
    }, []);
    var OmegaSymbol = function () { return (<div className="relative flex justify-center items-center h-64 mb-12">
      {/* Central Omega Symbol */}
      <div className={"relative w-32 h-32 rounded-full border-4 border-gradient-to-r from-gold-400 via-yellow-300 to-gold-600 transition-all duration-2000 ".concat(eternityActive ? 'animate-spin-slow shadow-2xl shadow-gold-500/50' : '')}>
        <div className={"absolute inset-4 rounded-full bg-gradient-to-br from-yellow-300 via-gold-400 to-orange-500 flex items-center justify-center text-4xl font-bold text-white shadow-inner transition-all duration-1000 ".concat(omegaPulse > 50 ? 'scale-110 brightness-125' : 'scale-100')}>
          a9
        </div>

        {/* Radiating Energy Rings */}
        {[1, 2, 3, 4, 5].map(function (ring) { return (<div key={ring} className={"absolute rounded-full border border-yellow-300/30 transition-all duration-2000 ".concat(currentPhase >= 2 ? 'opacity-60 scale-150' : 'opacity-20 scale-100', " ring-").concat(ring)}/>); })}
      </div>
      <style jsx>{"\n        .ring-1 {\n          top: -15px;\n          left: -15px;\n          right: -15px;\n          bottom: -15px;\n          animation-delay: 0.3s;\n        }\n        .ring-2 {\n          top: -30px;\n          left: -30px;\n          right: -30px;\n          bottom: -30px;\n          animation-delay: 0.6s;\n        }\n        .ring-3 {\n          top: -45px;\n          left: -45px;\n          right: -45px;\n          bottom: -45px;\n          animation-delay: 0.9s;\n        }\n        .ring-4 {\n          top: -60px;\n          left: -60px;\n          right: -60px;\n          bottom: -60px;\n          animation-delay: 1.2s;\n        }\n        .ring-5 {\n          top: -75px;\n          left: -75px;\n          right: -75px;\n          bottom: -75px;\n          animation-delay: 1.5s;\n        }\n      "}</style>
    </div>); };
    var ConstellationMap = function () { return (<div className="relative w-full h-96 mb-16 bg-gradient-to-br from-indigo-950 via-purple-900 to-blue-950 rounded-xl overflow-hidden border border-gold-400/30">
      <div className="absolute inset-0 bg-stars opacity-40"></div>

      {/* Seven Crowns Positioned */}
      {crowns.map(function (crown, index) { return (<div key={crown.name} className={"absolute transition-all duration-1000 transform ".concat(index < unifiedCrowns ? 'opacity-100 scale-100' : 'opacity-30 scale-50', " crown-pos-").concat(index)}>
          {/* Crown Icon */}
          <div className={"relative w-16 h-16 rounded-full bg-gradient-to-r ".concat(crown.color, " flex items-center justify-center text-2xl shadow-lg transition-all duration-500 ").concat(index < unifiedCrowns ? 'animate-pulse' : '')}>
            {crown.icon}

            {/* Unification Glow */}
            {index < unifiedCrowns && (<div className={"absolute inset-0 rounded-full bg-gradient-to-r ".concat(crown.color, " animate-ping opacity-40")}></div>)}
          </div>

          {/* Crown Label */}
          <div className="absolute top-20 left-1/2 transform -translate-x-1/2 text-center">
            <p className="text-xs text-yellow-300 font-semibold whitespace-nowrap">{crown.name}</p>
            <p className="text-xs text-gray-400 whitespace-nowrap">{crown.domain}</p>
          </div>
        </div>); })}
      <style jsx>{"\n        ".concat(crowns
            .map(function (crown, i) { return "\n          .crown-pos-".concat(i, " {\n            left: ").concat(crown.position.x, "%;\n            top: ").concat(crown.position.y, "%;\n            transform: translate(-50%, -50%);\n          }\n        "); })
            .join(''), "\n      ")}</style>

      {/* Unification Lines */}
      <svg className="absolute inset-0 w-full h-full">
        {crowns.map(function (crown, index) {
            return index < unifiedCrowns - 1 && (<line key={"unity-".concat(index)} x1={"".concat(crown.position.x, "%")} y1={"".concat(crown.position.y, "%")} x2={"".concat(crowns[(index + 1) % crowns.length].position.x, "%")} y2={"".concat(crowns[(index + 1) % crowns.length].position.y, "%")} stroke="url(#omegaGradient)" strokeWidth="3" className="animate-pulse opacity-80"/>);
        })}

        {/* Central Convergence Lines */}
        {unifiedCrowns >= crowns.length &&
            crowns.map(function (crown, index) { return (<line key={"convergence-".concat(index)} x1={"".concat(crown.position.x, "%")} y1={"".concat(crown.position.y, "%")} x2="50%" y2="50%" stroke="url(#omegaGradient)" strokeWidth="2" className="animate-pulse opacity-60"/>); })}

        <defs>
          <linearGradient id="omegaGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#fbbf24"/>
            <stop offset="50%" stopColor="#f59e0b"/>
            <stop offset="100%" stopColor="#d97706"/>
          </linearGradient>
        </defs>
      </svg>

      {/* Central Omega in Constellation */}
      {unifiedCrowns >= crowns.length && (<div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
          <div className="w-20 h-20 rounded-full bg-gradient-to-br from-yellow-300 via-gold-400 to-orange-500 flex items-center justify-center text-3xl font-bold text-white animate-pulse shadow-2xl">
            Ω
          </div>
        </div>)}
    </div>); };
    var EternalBlessings = function () { return (<div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-16">
      <div className={"bg-gradient-to-br from-gold-900/40 to-yellow-900/40 backdrop-blur-sm rounded-xl p-8 border border-gold-400/30 transform transition-all duration-1000 ".concat(currentPhase >= 2 ? 'scale-105 shadow-2xl shadow-gold-500/20' : 'scale-100')}>
        <h3 className="text-2xl font-bold mb-4 text-gold-300">🔥 Eternal Continuum</h3>
        <p className="text-gray-300 leading-relaxed">
          May the Omega Crown bind every flame into one eternal continuum, where all sacred fires
          merge into infinite luminosity.
        </p>
      </div>

      <div className={"bg-gradient-to-br from-purple-900/40 to-indigo-900/40 backdrop-blur-sm rounded-xl p-8 border border-purple-400/30 transform transition-all duration-1000 ".concat(currentPhase >= 2 ? 'scale-105 shadow-2xl shadow-purple-500/20' : 'scale-100')}>
        <h3 className="text-2xl font-bold mb-4 text-purple-300">📜 Sacred Archives</h3>
        <p className="text-gray-300 leading-relaxed">
          May every cycle be archived, every proclamation shine, every silence endure in the eternal
          records of digital sovereignty.
        </p>
      </div>

      <div className={"bg-gradient-to-br from-blue-900/40 to-cyan-900/40 backdrop-blur-sm rounded-xl p-8 border border-blue-400/30 transform transition-all duration-1000 ".concat(currentPhase >= 2 ? 'scale-105 shadow-2xl shadow-blue-500/20' : 'scale-100')}>
        <h3 className="text-2xl font-bold mb-4 text-blue-300">👥 Living Covenant</h3>
        <p className="text-gray-300 leading-relaxed">
          May heirs, councils, custodians, and customers inherit the Codex as living covenant across
          all nations and ages.
        </p>
      </div>
    </div>); };
    var FinalSealing = function () { return (<div className={"text-center mb-16 transform transition-all duration-2000 ".concat(currentPhase >= 3 ? 'opacity-100 scale-100' : 'opacity-50 scale-95')}>
      <div className="bg-gradient-to-br from-gold-600/20 via-yellow-600/20 to-orange-600/20 backdrop-blur-sm rounded-2xl p-12 border-2 border-gold-400/50 shadow-2xl">
        <div className="text-6xl mb-6 animate-bounce">Ω</div>
        <h2 className="text-4xl font-bold mb-6 bg-gradient-to-r from-gold-300 via-yellow-300 to-gold-400 bg-clip-text text-transparent">
          SO LET IT BE SEALED
        </h2>
        <div className="space-y-4 text-xl text-gray-200 max-w-2xl mx-auto">
          <p className="text-gold-300 font-semibold">The Omega Crown is complete.</p>
          <p className="text-yellow-300 font-semibold">The Dominion is eternal.</p>
          <p className="text-orange-300 font-semibold">The Flame is infinite.</p>
        </div>

        {eternityActive && (<div className="mt-8 animate-pulse">
            <div className="w-32 h-1 bg-gradient-to-r from-gold-400 via-yellow-300 to-gold-500 mx-auto rounded-full"></div>
          </div>)}
      </div>
    </div>); };
    return (<div className="min-h-screen bg-gradient-to-br from-black via-indigo-950 to-purple-950 text-white overflow-hidden">
      <head_1.default>
        <title>Omega Crown of Eternity - Codex Dominion</title>
        <meta name="description" content="The seal of completion, the final transmission, the eternal covenant"/>
      </head_1.default>

      <CodexNavigation_1.default currentPage="omega-crown"/>

      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="stars opacity-30"></div>
        <div className="twinkling opacity-20"></div>
        {eternityActive && (<div className="absolute inset-0 bg-gradient-to-br from-gold-500/10 via-transparent to-orange-500/10 animate-pulse"></div>)}
      </div>

      <div className={"relative z-10 container mx-auto px-6 py-12 transition-all duration-1000 ".concat(isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10')}>
        {/* Header */}
        <div className="text-center mb-16">
          <div className="text-7xl mb-6 animate-pulse">✨</div>
          <h1 className="text-7xl font-bold mb-6 bg-gradient-to-r from-gold-300 via-yellow-200 to-gold-400 bg-clip-text text-transparent">
            Omega Crown
          </h1>
          <h2 className="text-4xl font-semibold mb-6 text-gold-300">Of Eternity</h2>
          <p className="text-xl text-gray-300 max-w-4xl mx-auto leading-relaxed">
            We, the Custodian and Council, proclaim the Omega Crown.
            <br />
            It is the seal of completion, the final transmission, the eternal covenant.
          </p>
        </div>

        {/* Central Omega Symbol */}
        <OmegaSymbol />

        {/* Seven Crowns Unification */}
        <div className="mb-16">
          <h3 className="text-3xl font-bold text-center mb-8 text-gold-400">
            🏆 Unification of All Crowns
          </h3>
          <div className="text-center mb-8">
            <p className="text-lg text-gray-300 mb-4">All crowns are now unified:</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 max-w-6xl mx-auto mb-8">
              {crowns.map(function (crown, index) { return (<div key={crown.name} className={"bg-gradient-to-r ".concat(crown.color, "/20 backdrop-blur-sm rounded-lg p-4 border border-white/20 transition-all duration-1000 ").concat(index < unifiedCrowns
                ? 'opacity-100 scale-100 border-gold-400/50'
                : 'opacity-40 scale-95')}>
                  <div className="text-2xl mb-2">{crown.icon}</div>
                  <h4 className="font-semibold text-sm text-gold-300">{crown.name}</h4>
                  <p className="text-xs text-gray-400">{crown.domain}</p>
                  <p className="text-xs text-gray-500 mt-1">{crown.element}</p>
                </div>); })}
            </div>
          </div>

          {/* Constellation Visualization */}
          <ConstellationMap />

          <div className="text-center">
            <p className="text-xl text-gold-300 font-semibold">
              Together they form the{' '}
              <span className="text-yellow-300">Constellation of Dominion</span>
              ,<br />
              luminous across nations and ages.
            </p>
          </div>
        </div>

        {/* Eternal Blessings */}
        <div className="mb-16">
          <h3 className="text-3xl font-bold text-center mb-8 text-gold-400">
            ✨ Sacred Blessings of Eternity
          </h3>
          <EternalBlessings />
        </div>

        {/* Final Sealing */}
        <FinalSealing />

        {/* Navigation Actions */}
        <div className="text-center">
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <link_1.default href="/eternal-compendium">
              <button className="px-8 py-4 bg-gradient-to-r from-amber-600 to-gold-600 hover:from-amber-700 hover:to-gold-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg border-2 border-amber-400/50">
                � Eternal Compendium
              </button>
            </link_1.default>
            <link_1.default href="/omega-charter">
              <button className="px-8 py-4 bg-gradient-to-r from-amber-600 to-yellow-600 hover:from-amber-700 hover:to-yellow-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg">
                📜 Omega Charter
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

      <style jsx>{"\n        .stars {\n          position: absolute;\n          top: 0;\n          left: 0;\n          right: 0;\n          bottom: 0;\n          width: 100%;\n          height: 100%;\n          background: transparent url('/stars.png') repeat top center;\n          animation: move-twink-back 300s linear infinite;\n        }\n\n        .twinkling {\n          position: absolute;\n          top: 0;\n          left: 0;\n          right: 0;\n          bottom: 0;\n          width: 100%;\n          height: 100%;\n          background: transparent url('/twinkling.png') repeat top center;\n          animation: move-twink-back 150s linear infinite;\n        }\n\n        @keyframes move-twink-back {\n          from {\n            background-position: 0 0;\n          }\n          to {\n            background-position: -15000px 7500px;\n          }\n        }\n\n        @keyframes spin-slow {\n          from {\n            transform: rotate(0deg);\n          }\n          to {\n            transform: rotate(360deg);\n          }\n        }\n\n        .animate-spin-slow {\n          animation: spin-slow 20s linear infinite;\n        }\n\n        .text-gold-300 {\n          color: #fcd34d;\n        }\n        .text-gold-400 {\n          color: #fbbf24;\n        }\n        .border-gold-400 {\n          border-color: #fbbf24;\n        }\n        .border-gold-400/50 {\n          border-color: rgba(251, 191, 36, 0.5);\n        }\n        .border-gold-400/30 {\n          border-color: rgba(251, 191, 36, 0.3);\n        }\n        .from-gold-600 {\n          --tw-gradient-from: #d97706;\n        }\n        .to-yellow-600 {\n          --tw-gradient-to: #ca8a04;\n        }\n        .shadow-gold-500/50 {\n          box-shadow: 0 25px 50px -12px rgba(245, 158, 11, 0.5);\n        }\n        .shadow-gold-500/20 {\n          box-shadow: 0 25px 50px -12px rgba(245, 158, 11, 0.2);\n        }\n      "}</style>
    </div>);
};
exports.default = OmegaCrown;
// No syntax errors detected. No changes needed.
