"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = Home;
var link_1 = require("next/link");
function Home() {
    return (<div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-blue-900 flex items-center justify-center">
      <div className="text-center text-white max-w-2xl mx-auto p-8">
        <div className="text-8xl mb-6 animate-pulse">🔥</div>
        <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-gold-300 via-yellow-300 to-gold-400 bg-clip-text text-transparent">
          Codex Dominion
        </h1>
        <p className="text-xl text-purple-300 mb-8">
          Digital Sovereignty • Constitutional Framework • Eternal Covenant
        </p>

        {/* Source Charter - Supreme Governing Document */}
        <div className="mb-8">
          <link_1.default href="/codex-source-charter">
            <button className="px-8 py-6 bg-gradient-to-r from-gold-500 to-amber-500 hover:from-gold-600 hover:to-amber-600 rounded-xl font-bold text-xl transform hover:scale-105 transition-all duration-300 shadow-2xl border-2 border-gold-300 w-full max-w-md mx-auto block">
              ✨ Codex Source Charter
              <div className="text-sm font-normal text-gold-100 mt-1">
                Supreme Governing Covenant
              </div>
            </button>
          </link_1.default>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          <link_1.default href="/dashboard-selector">
            <button className="px-6 py-4 bg-gradient-to-r from-amber-600 to-gold-600 hover:from-amber-700 hover:to-gold-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg w-full">
              🏛️ Main Dashboard
            </button>
          </link_1.default>
          <link_1.default href="/alpha-omega-concord">
            <button className="px-6 py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg w-full">
              ∞ Alpha-Omega Concord
            </button>
          </link_1.default>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <link_1.default href="/eternal-compendium">
            <button className="px-4 py-3 bg-gradient-to-r from-amber-700 to-gold-700 hover:from-amber-800 hover:to-gold-800 rounded-lg font-semibold transform hover:scale-105 transition-all duration-300 shadow-lg w-full">
              📖 Eternal Compendium
            </button>
          </link_1.default>
          <link_1.default href="/omega-charter">
            <button className="px-4 py-3 bg-gradient-to-r from-gold-600 to-yellow-600 hover:from-gold-700 hover:to-yellow-700 rounded-lg font-semibold transform hover:scale-105 transition-all duration-300 shadow-lg w-full">
              📜 Omega Charter
            </button>
          </link_1.default>
          <link_1.default href="/omega-crown">
            <button className="px-4 py-3 bg-gradient-to-r from-yellow-600 to-orange-600 hover:from-yellow-700 hover:to-orange-700 rounded-lg font-semibold transform hover:scale-105 transition-all duration-300 shadow-lg w-full">
              Ω Omega Crown
            </button>
          </link_1.default>
        </div>

        <div className="mt-8 text-sm text-gray-400">
          <p>🌟 Complete Constellation System • Seven Sacred Domains • Constitutional Authority</p>
        </div>
      </div>
    </div>);
}
