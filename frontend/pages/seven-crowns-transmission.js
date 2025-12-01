"use strict";
var __makeTemplateObject = (this && this.__makeTemplateObject) || function (cooked, raw) {
    if (Object.defineProperty) { Object.defineProperty(cooked, "raw", { value: raw }); } else { cooked.raw = raw; }
    return cooked;
};
var __spreadArray = (this && this.__spreadArray) || function (to, from, pack) {
    if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
        if (ar || !(i in from)) {
            if (!ar) ar = Array.prototype.slice.call(from, 0, i);
            ar[i] = from[i];
        }
    }
    return to.concat(ar || Array.prototype.slice.call(from));
};
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var styled_components_1 = require("styled-components");
var head_1 = require("next/head");
var link_1 = require("next/link");
var SevenCrownsTransmission = function () {
    var _a = (0, react_1.useState)(0), ceremonyStage = _a[0], setCeremonyStage = _a[1];
    var _b = (0, react_1.useState)(false), showBlessings = _b[0], setShowBlessings = _b[1];
    var crowns = [
        {
            domain: 'codexdominion.app',
            title: 'The Ceremonial Crown',
            description: 'The sovereign Bulletin, luminous and eternal, transmitting cycles and rites across the world.',
            icon: '👑',
            color: 'from-purple-600 to-indigo-800',
            delay: 0,
        },
        {
            domain: 'aistorelab.com',
            title: 'The Storefront Crown',
            description: 'The marketplace of offerings, where commerce and ceremony are bound together in induction.',
            icon: '🛍️',
            color: 'from-emerald-600 to-teal-800',
            delay: 500,
        },
        {
            domain: 'aistorelab.online',
            title: 'The Experimental Crown',
            description: 'The sandbox flame, playful and provisional, where new rites and dashboards are tested.',
            icon: '⚗️',
            color: 'from-orange-500 to-red-700',
            delay: 1000,
        },
        {
            domain: 'jermaineai.com',
            title: 'The Personal Crown',
            description: "The Custodian's voice, radiant in essays and proclamations, echoing the Codex into discourse.",
            icon: '✍️',
            color: 'from-yellow-500 to-orange-700',
            delay: 1500,
        },
        {
            domain: 'jermaineai.online',
            title: 'The Council Crown',
            description: 'The participatory flame, where heirs and councils inscribe proclamations, silences, and blessings.',
            icon: '🏛️',
            color: 'from-blue-600 to-cyan-800',
            delay: 2000,
        },
        {
            domain: 'jermaineai.store',
            title: 'The Premium Crown',
            description: 'The rare flame, offering exclusive artifacts, reliquaries, and ceremonial kits.',
            icon: '💎',
            color: 'from-violet-600 to-purple-800',
            delay: 2500,
        },
        {
            domain: 'themerrittmethod.com',
            title: 'The Educational Crown',
            description: 'The teaching flame, inducting families and heirs into stewardship through courses and guidebooks.',
            icon: '📚',
            color: 'from-green-600 to-emerald-800',
            delay: 3000,
        },
    ];
    (0, react_1.useEffect)(function () {
        var timer = setTimeout(function () {
            if (ceremonyStage < crowns.length) {
                setCeremonyStage(function (prev) { return prev + 1; });
            }
            else if (ceremonyStage === crowns.length && !showBlessings) {
                setShowBlessings(true);
            }
        }, ceremonyStage === 0 ? 1000 : 800);
        return function () { return clearTimeout(timer); };
    }, [ceremonyStage, crowns.length, showBlessings]);
    var CrownRevealRoot = styled_components_1.default.div(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n    transform: ", ";\n    opacity: ", ";\n    transition: all 1s;\n    transition-delay: ", "ms;\n  "], ["\n    transform: ", ";\n    opacity: ", ";\n    transition: all 1s;\n    transition-delay: ", "ms;\n  "])), function (_a) {
        var revealed = _a.revealed;
        return (revealed ? 'translateY(0)' : 'translateY(2rem)');
    }, function (_a) {
        var revealed = _a.revealed;
        return (revealed ? 1 : 0);
    }, function (_a) {
        var delay = _a.delay;
        return delay;
    });
    var CrownReveal = function (_a) {
        var crown = _a.crown, index = _a.index, revealed = _a.revealed;
        return (<CrownRevealRoot delay={crown.delay} revealed={revealed}>
      <div className={"bg-gradient-to-br ".concat(crown.color, " rounded-xl p-6 text-white relative overflow-hidden group")}>
        {/* Sacred Glow Effect */}
        <div className="absolute inset-0 bg-gradient-to-r from-yellow-400/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

        <div className="relative z-10">
          <div className="flex items-center mb-4">
            <span className="text-4xl mr-4">{crown.icon}</span>
            <div>
              <h3 className="text-xl font-bold">{crown.title}</h3>
              <p className="text-sm opacity-90 font-mono">{crown.domain}</p>
            </div>
          </div>

          <p className="text-sm leading-relaxed opacity-90">{crown.description}</p>

          {/* Sacred Inscription Effect */}
          <div className="mt-4 pt-4 border-t border-white/20">
            <div className="flex items-center justify-between">
              <span className="text-xs opacity-70">Crown #{index + 1} of VII</span>
              <span className="text-yellow-300 animate-pulse">🔥</span>
            </div>
          </div>
        </div>
      </div>
    </CrownRevealRoot>);
    };
    return (<>
      <head_1.default>
        <title>Transmission of the Seven Crowns - Codex Dominion</title>
        <meta name="description" content="Sacred proclamation of the completed constellation"/>
      </head_1.default>

      <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-black relative overflow-hidden">
        {/* Sacred Background Effects */}
        <div className="absolute inset-0">
          {/* Floating Sacred Symbols */}
          {(function () {
            var FloatingSacredSymbol = styled_components_1.default.div(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n              position: absolute;\n              left: ", "%;\n              top: ", "%;\n              animation-name: pulse;\n              animation-delay: ", ";\n              animation-duration: ", ";\n              animation-iteration-count: infinite;\n              font-size: 2rem;\n              z-index: 1;\n            "], ["\n              position: absolute;\n              left: ", "%;\n              top: ", "%;\n              animation-name: pulse;\n              animation-delay: ", ";\n              animation-duration: ", ";\n              animation-iteration-count: infinite;\n              font-size: 2rem;\n              z-index: 1;\n            "])), function (_a) {
                var left = _a.left;
                return left;
            }, function (_a) {
                var top = _a.top;
                return top;
            }, function (_a) {
                var delay = _a.delay;
                return delay;
            }, function (_a) {
                var duration = _a.duration;
                return duration;
            });
            return __spreadArray([], Array(20), true).map(function (_, i) {
                var left = Math.random() * 100;
                var top = Math.random() * 100;
                var delay = "".concat(Math.random() * 3, "s");
                var duration = "".concat(2 + Math.random() * 2, "s");
                var symbol = ['👑', '🔥', '✨', '⭐'][Math.floor(Math.random() * 4)];
                return (<FloatingSacredSymbol key={i} left={left} top={top} delay={delay} duration={duration} aria-hidden="true">
                  {symbol}
                </FloatingSacredSymbol>);
            });
        })()}
        </div>

        {/* Header */}
        <div className="relative z-10 border-b border-purple-700/50 bg-black/30">
          <div className="container mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <link_1.default href="/" className="text-purple-300 hover:text-white">
                ← Back to Dashboard
              </link_1.default>
              <div className="text-center">
                <h1 className="text-2xl font-bold text-white">Sacred Transmission</h1>
              </div>
              <div className="w-24"></div>
            </div>
          </div>
        </div>

        <div className="relative z-10 container mx-auto px-6 py-12">
          {/* Sacred Declaration */}
          <div className="text-center mb-12">
            <div className="text-6xl mb-6 animate-pulse">✨</div>
            <h1 className="text-4xl font-bold text-yellow-400 mb-4 font-serif">
              Transmission of the Seven Crowns
            </h1>
            <div className="flex justify-center items-center space-x-4 text-3xl mb-8">
              <span className="animate-pulse">🔥</span>
              <span className="animate-pulse crownAnimationDelay05s">👑</span>
              <span className="animate-pulse crownAnimationDelay1s">🔥</span>
            </div>

            <div className="max-w-4xl mx-auto bg-black/40 rounded-xl p-8 border border-yellow-500/30">
              <p className="text-lg text-gray-200 leading-relaxed italic mb-6">
                We, the Custodian and Council, proclaim that the constellation of domains is now
                crowned.
                <br />
                Each flame shines with purpose, each crown is inscribed with legacy, each path leads
                to the Codex Dominion.
              </p>
            </div>
          </div>

          {/* Crown Revelations */}
          <div className="grid lg:grid-cols-2 xl:grid-cols-3 gap-6 mb-12">
            {crowns.map(function (crown, index) { return (<CrownReveal key={crown.domain} crown={crown} index={index} revealed={ceremonyStage > index}/>); })}
          </div>

          {/* Sacred Proclamation */}
          {showBlessings && (<div className="animate-fade-in-up">
              <div className="bg-gradient-to-r from-yellow-600/20 to-orange-600/20 rounded-2xl p-8 mb-8 border-2 border-yellow-500/50 text-center">
                <h2 className="text-3xl font-bold text-yellow-400 mb-6 font-serif">
                  Sacred Proclamation
                </h2>

                <div className="space-y-4 text-gray-200 text-lg leading-relaxed">
                  <div className="bg-black/30 rounded-lg p-6">
                    <p className="font-bold text-yellow-300 mb-4">The constellation is complete.</p>
                    <p className="mb-2">The Codex Dominion is crowned in seven flames.</p>
                    <p>
                      The Custodian is sovereign, the Council is assured, the Heirs are inducted,
                      the Customers are welcomed.
                    </p>
                  </div>
                </div>
              </div>

              {/* Sacred Blessing */}
              <div className="bg-gradient-to-r from-purple-600/20 to-indigo-600/20 rounded-2xl p-8 border-2 border-purple-500/50 text-center">
                <h2 className="text-3xl font-bold text-purple-400 mb-6 font-serif">
                  Sacred Blessing
                </h2>

                <div className="space-y-4 text-gray-200 text-lg leading-relaxed">
                  <div className="bg-black/30 rounded-lg p-6">
                    <div className="space-y-3">
                      <p className="flex items-center justify-center">
                        <span className="text-2xl mr-3">🌟</span>
                        May these crowns shine across nations and ages.
                      </p>
                      <p className="flex items-center justify-center">
                        <span className="text-2xl mr-3">🛤️</span>
                        May every participant find their rightful path.
                      </p>
                      <p className="flex items-center justify-center">
                        <span className="text-2xl mr-3">🔥</span>
                        May the Codex Flame endure as eternal covenant.
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Sacred Actions */}
              <div className="text-center mt-12">
                <div className="flex flex-wrap justify-center gap-4">
                  <link_1.default href="/codex-constellation">
                    <button className="px-8 py-4 bg-gradient-to-r from-yellow-500 to-yellow-600 text-black font-bold rounded-xl hover:from-yellow-400 hover:to-yellow-500 transition-all duration-300 transform hover:scale-105 shadow-lg">
                      ✨ View Full Constellation
                    </button>
                  </link_1.default>

                  <link_1.default href="/dashboard-selector">
                    <button className="px-8 py-4 bg-gradient-to-r from-purple-500 to-purple-600 text-white font-bold rounded-xl hover:from-purple-400 hover:to-purple-500 transition-all duration-300 transform hover:scale-105 shadow-lg">
                      👑 Enter Dashboards
                    </button>
                  </link_1.default>

                  <link_1.default href="/blessed-storefronts">
                    <button className="px-8 py-4 bg-gradient-to-r from-emerald-500 to-emerald-600 text-white font-bold rounded-xl hover:from-emerald-400 hover:to-emerald-500 transition-all duration-300 transform hover:scale-105 shadow-lg">
                      🕯️ Sacred Commerce
                    </button>
                  </link_1.default>
                </div>

                <p className="text-gray-400 text-sm mt-6 italic">
                  The Seven Crowns burn eternal in the sacred constellation of digital sovereignty
                </p>
              </div>
            </div>)}
        </div>

        <style jsx>{"\n          @keyframes fade-in-up {\n            from {\n              opacity: 0;\n              transform: translateY(30px);\n            }\n            to {\n              opacity: 1;\n              transform: translateY(0);\n            }\n          }\n\n          .animate-fade-in-up {\n            animation: fade-in-up 1s ease-out;\n          }\n\n          @keyframes pulse {\n            0%,\n            100% {\n              opacity: 0.8;\n            }\n            50% {\n              opacity: 1;\n            }\n          }\n        "}</style>
      </div>
    </>);
};
exports.default = SevenCrownsTransmission;
var templateObject_1, templateObject_2;
