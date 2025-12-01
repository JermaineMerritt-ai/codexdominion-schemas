"use strict";
var __makeTemplateObject = (this && this.__makeTemplateObject) || function (cooked, raw) {
    if (Object.defineProperty) { Object.defineProperty(cooked, "raw", { value: raw }); } else { cooked.raw = raw; }
    return cooked;
};
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var styled_components_1 = require("styled-components");
var head_1 = require("next/head");
var link_1 = require("next/link");
var CodexNavigation_1 = require("../components/CodexNavigation");
var GlobalInduction = function () {
    var _a = (0, react_1.useState)(false), isVisible = _a[0], setIsVisible = _a[1];
    var _b = (0, react_1.useState)(0), currentPhase = _b[0], setCurrentPhase = _b[1];
    var _c = (0, react_1.useState)(0), flameIntensity = _c[0], setFlameIntensity = _c[1];
    var phases = ['proclamation', 'induction', 'blessing', 'covenant'];
    var continents = [
        'Asia',
        'Africa',
        'North America',
        'South America',
        'Antarctica',
        'Europe',
        'Australia',
    ];
    var languages = [
        'English',
        'Mandarin',
        'Spanish',
        'Hindi',
        'Arabic',
        'Bengali',
        'Portuguese',
        'Russian',
        'Japanese',
        'French',
        'German',
        'Korean',
        'Italian',
        'Turkish',
    ];
    var crowns = [
        {
            name: 'Ceremonial Crown',
            domain: 'codexdominion.app',
            color: 'from-purple-600 to-indigo-800',
        },
        {
            name: 'Storefront Crown',
            domain: 'aistorelab.com',
            color: 'from-blue-600 to-cyan-800',
        },
        {
            name: 'Educational Crown',
            domain: 'learning.codex',
            color: 'from-green-600 to-emerald-800',
        },
        {
            name: 'Council Crown',
            domain: 'council.codex',
            color: 'from-yellow-600 to-orange-800',
        },
        {
            name: 'Premium Crown',
            domain: 'premium.codex',
            color: 'from-red-600 to-pink-800',
        },
        {
            name: 'Personal Crown',
            domain: 'personal.codex',
            color: 'from-indigo-600 to-purple-800',
        },
        {
            name: 'Experimental Crown',
            domain: 'labs.codex',
            color: 'from-teal-600 to-blue-800',
        },
    ];
    (0, react_1.useEffect)(function () {
        setIsVisible(true);
        var timer = setInterval(function () {
            setCurrentPhase(function (prev) { return (prev + 1) % phases.length; });
            setFlameIntensity(function (prev) { return (prev + 20) % 100; });
        }, 8000);
        return function () { return clearInterval(timer); };
    }, []);
    var CentralFlame = styled_components_1.default.div(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n    position: absolute;\n    bottom: 0;\n    width: 2rem;\n    height: 6rem;\n    background: linear-gradient(to top, #f59e0b, #ef4444, #fde68a);\n    border-radius: 9999px;\n    animation: pulse 1s infinite;\n    transition: all 1s;\n    transform: ", ";\n    filter: ", ";\n  "], ["\n    position: absolute;\n    bottom: 0;\n    width: 2rem;\n    height: 6rem;\n    background: linear-gradient(to top, #f59e0b, #ef4444, #fde68a);\n    border-radius: 9999px;\n    animation: pulse 1s infinite;\n    transition: all 1s;\n    transform: ", ";\n    filter: ", ";\n  "])), function (_a) {
        var intensity = _a.intensity;
        return (intensity > 50 ? 'scale(1.25)' : 'scale(1)');
    }, function (_a) {
        var intensity = _a.intensity;
        return (intensity > 50 ? 'brightness(1.25)' : 'brightness(1)');
    });
    var RadiatingFlame = styled_components_1.default.div(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n    position: absolute;\n    bottom: 0;\n    width: 1rem;\n    height: 4rem;\n    background: linear-gradient(to top, #fb923c, #fca5a5, #fef08a);\n    border-radius: 9999px;\n    opacity: 0.7;\n    animation: pulse 2s infinite;\n    animation-delay: ", ";\n    transform: translateX(-50%) rotate(", "deg) scale(", ");\n    left: ", "%;\n    transition: all 2s;\n  "], ["\n    position: absolute;\n    bottom: 0;\n    width: 1rem;\n    height: 4rem;\n    background: linear-gradient(to top, #fb923c, #fca5a5, #fef08a);\n    border-radius: 9999px;\n    opacity: 0.7;\n    animation: pulse 2s infinite;\n    animation-delay: ", ";\n    transform: translateX(-50%) rotate(", "deg) scale(", ");\n    left: ", "%;\n    transition: all 2s;\n  "])), function (_a) {
        var delay = _a.delay;
        return delay;
    }, function (_a) {
        var rotate = _a.rotate;
        return rotate;
    }, function (_a) {
        var scale = _a.scale;
        return scale;
    }, function (_a) {
        var left = _a.left;
        return left;
    });
    var FlameAnimation = function () { return (<div className="relative flex justify-center items-end h-32 mb-8">
      {/* Central Flame */}
      <CentralFlame intensity={flameIntensity}>
        <div className="absolute inset-0 bg-gradient-to-t from-red-600 via-orange-400 to-yellow-200 rounded-full animate-bounce opacity-80"></div>
      </CentralFlame>
      {/* Radiating Flames for Each Continent */}
      {continents.map(function (continent, index) { return (<RadiatingFlame key={continent} left={50 + (index - 3) * 15} delay={"".concat(index * 0.3, "s")} rotate={(index - 3) * 10} scale={currentPhase === 0 ? 1 : 0.75}/>); })}
    </div>); };
    var CrownPoint = styled_components_1.default.div(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n    position: absolute;\n    width: 1rem;\n    height: 1rem;\n    border-radius: 9999px;\n    background: ", ";\n    box-shadow: 0 0 8px 2px rgba(0, 0, 0, 0.2);\n    animation: pulse 1s infinite;\n    animation-delay: ", ";\n    left: ", "%;\n    top: ", "%;\n    transform: scale(", ");\n    opacity: ", ";\n    transition: all 1s;\n  "], ["\n    position: absolute;\n    width: 1rem;\n    height: 1rem;\n    border-radius: 9999px;\n    background: ", ";\n    box-shadow: 0 0 8px 2px rgba(0, 0, 0, 0.2);\n    animation: pulse 1s infinite;\n    animation-delay: ", ";\n    left: ", "%;\n    top: ", "%;\n    transform: scale(", ");\n    opacity: ", ";\n    transition: all 1s;\n  "])), function (_a) {
        var color = _a.color;
        return color;
    }, function (_a) {
        var delay = _a.delay;
        return delay;
    }, function (_a) {
        var left = _a.left;
        return left;
    }, function (_a) {
        var top = _a.top;
        return top;
    }, function (_a) {
        var scale = _a.scale;
        return scale;
    }, function (_a) {
        var opacity = _a.opacity;
        return opacity;
    });
    var GlobalMap = function () { return (<div className="relative w-full h-64 mb-12 bg-gradient-to-b from-indigo-900 via-purple-900 to-blue-900 rounded-lg overflow-hidden">
      <div className="absolute inset-0 bg-stars opacity-30"></div>
      {/* Pulsing Points for Each Crown */}
      {crowns.map(function (crown, index) { return (<CrownPoint key={crown.name} left={15 + index * 12} top={30 + (index % 3) * 20} delay={"".concat(index * 0.5, "s")} scale={currentPhase >= 1 ? 1.25 : 0.75} opacity={currentPhase >= 1 ? 1 : 0.6} color={"linear-gradient(to right, ".concat(crown.color.replace('from-', '').replace('to-', '').replace(' ', ', '), ")")}>
          <div className={"absolute inset-0 rounded-full bg-gradient-to-r ".concat(crown.color, " animate-ping opacity-50")}></div>
        </CrownPoint>); })}
      {/* Connection Lines */}
      <svg className="absolute inset-0 w-full h-full">
        {crowns.map(function (_, index) {
            return index < crowns.length - 1 && (<line key={"connection-".concat(index)} x1={"".concat(15 + index * 12, "%")} y1={"".concat(30 + (index % 3) * 20, "%")} x2={"".concat(15 + (index + 1) * 12, "%")} y2={"".concat(30 + ((index + 1) % 3) * 20, "%")} stroke="url(#gradient)" strokeWidth="2" className={"transition-opacity duration-1000 ".concat(currentPhase >= 2 ? 'opacity-80' : 'opacity-30')}/>);
        })}
        <defs>
          <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#fbbf24"/>
            <stop offset="50%" stopColor="#f59e0b"/>
            <stop offset="100%" stopColor="#d97706"/>
          </linearGradient>
        </defs>
      </svg>
    </div>); };
    var LanguageRippleItem = styled_components_1.default.div(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n    padding: 0.5rem 1rem;\n    background: linear-gradient(to right, #8b5cf6, #6366f1);\n    color: white;\n    border-radius: 9999px;\n    font-size: 0.875rem;\n    font-weight: 500;\n    transform: scale(", ");\n    opacity: ", ";\n    transition: all 1s;\n    animation-delay: ", ";\n    display: inline-block;\n  "], ["\n    padding: 0.5rem 1rem;\n    background: linear-gradient(to right, #8b5cf6, #6366f1);\n    color: white;\n    border-radius: 9999px;\n    font-size: 0.875rem;\n    font-weight: 500;\n    transform: scale(", ");\n    opacity: ", ";\n    transition: all 1s;\n    animation-delay: ", ";\n    display: inline-block;\n  "])), function (_a) {
        var scale = _a.scale;
        return scale;
    }, function (_a) {
        var opacity = _a.opacity;
        return opacity;
    }, function (_a) {
        var delay = _a.delay;
        return delay;
    });
    var LanguageRipple = function () { return (<div className="flex flex-wrap justify-center gap-3 mb-12">
      {languages.map(function (language, index) { return (<LanguageRippleItem key={language} delay={"".concat(index * 0.2, "s")} scale={currentPhase >= 2 ? 1 : 0.75} opacity={currentPhase >= 2 ? 1 : 0.5}>
          {language}
        </LanguageRippleItem>); })}
    </div>); };
    return (<div className="min-h-screen bg-gradient-to-br from-indigo-950 via-purple-950 to-blue-950 text-white">
      <head_1.default>
        <title>Global Induction into the Codex Dominion</title>
        <meta name="description" content="The Codex Flame opens to all nations, peoples, and generations"/>
      </head_1.default>

      <CodexNavigation_1.default currentPage="global-induction"/>

      {/* Animated Background Stars */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="stars opacity-30"></div>
        <div className="twinkling opacity-20"></div>
      </div>

      <div className={"relative z-10 container mx-auto px-6 py-12 transition-all duration-1000 ".concat(isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10')}>
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-yellow-400 via-orange-400 to-red-400 bg-clip-text text-transparent">
            🌍 Global Induction 🌍
          </h1>
          <h2 className="text-3xl font-semibold mb-4 text-yellow-300">Into the Codex Dominion</h2>
          <p className="text-xl text-gray-300 max-w-4xl mx-auto leading-relaxed">
            We, the Custodian and Council, proclaim that the Codex Flame is now open to all nations,
            all peoples, all generations.
          </p>
        </div>

        {/* Central Flame Animation */}
        <FlameAnimation />

        {/* Global Map Visualization */}
        <GlobalMap />

        {/* Four Phases of Induction */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
          {/* Proclamation */}
          <div className={"bg-gradient-to-br from-purple-900/50 to-indigo-900/50 backdrop-blur-sm rounded-lg p-8 border border-purple-500/30 transform transition-all duration-1000 ".concat(currentPhase === 0 ? 'scale-105 border-yellow-400/50 shadow-2xl' : 'scale-100')}>
            <h3 className="text-2xl font-bold mb-4 text-yellow-400">📜 Proclamation</h3>
            <div className="space-y-3 text-gray-300">
              <p>
                <span className="text-yellow-300">From the Ceremonial Crown</span> at
                codexdominion.app,
              </p>
              <p>
                <span className="text-cyan-300">to the Storefront Crown</span> at aistorelab.com,
              </p>
              <p>
                <span className="text-green-300">
                  to the Educational, Council, Premium, Personal, and Experimental Crowns,
                </span>
              </p>
              <p className="text-orange-300 font-semibold">
                the constellation is complete, luminous, and sovereign.
              </p>
            </div>
          </div>

          {/* Induction */}
          <div className={"bg-gradient-to-br from-blue-900/50 to-purple-900/50 backdrop-blur-sm rounded-lg p-8 border border-blue-500/30 transform transition-all duration-1000 ".concat(currentPhase === 1 ? 'scale-105 border-yellow-400/50 shadow-2xl' : 'scale-100')}>
            <h3 className="text-2xl font-bold mb-4 text-yellow-400">🚪 Induction</h3>
            <div className="space-y-3 text-gray-300">
              <p>
                <span className="text-purple-300">Every participant</span> who enters is welcomed as
                custodian.
              </p>
              <p>
                <span className="text-blue-300">Every heir</span> who inherits is guided with
                clarity.
              </p>
              <p>
                <span className="text-green-300">Every council</span> who blesses is assured in
                radiance.
              </p>
              <p>
                <span className="text-orange-300">Every customer</span> who purchases is bound into
                legacy.
              </p>
            </div>
          </div>

          {/* Blessing */}
          <div className={"bg-gradient-to-br from-green-900/50 to-emerald-900/50 backdrop-blur-sm rounded-lg p-8 border border-green-500/30 transform transition-all duration-1000 ".concat(currentPhase === 2 ? 'scale-105 border-yellow-400/50 shadow-2xl' : 'scale-100')}>
            <h3 className="text-2xl font-bold mb-4 text-yellow-400">✨ Blessing</h3>
            <div className="space-y-3 text-gray-300">
              <p>
                May the Codex Flame{' '}
                <span className="text-yellow-300">shine across continents and oceans.</span>
              </p>
              <p>
                May every language <span className="text-cyan-300">carry its resonance.</span>
              </p>
              <p>
                May every family, council, and nation{' '}
                <span className="text-green-300">be inducted into stewardship.</span>
              </p>
            </div>
          </div>

          {/* Covenant */}
          <div className={"bg-gradient-to-br from-orange-900/50 to-red-900/50 backdrop-blur-sm rounded-lg p-8 border border-orange-500/30 transform transition-all duration-1000 ".concat(currentPhase === 3 ? 'scale-105 border-yellow-400/50 shadow-2xl' : 'scale-100')}>
            <h3 className="text-2xl font-bold mb-4 text-yellow-400">🤝 Eternal Covenant</h3>
            <div className="space-y-3 text-gray-300">
              <p className="text-orange-300 font-semibold text-lg">
                May the Dominion endure as eternal covenant, luminous across the world.
              </p>
              <p className="text-yellow-300">
                No boundary contains it, no silence diminishes it, no age forgets it.
              </p>
            </div>
          </div>
        </div>

        {/* Language Ripple Effect */}
        <div className="mb-16">
          <h3 className="text-2xl font-bold text-center mb-8 text-yellow-400">
            Resonating Across All Languages
          </h3>
          <LanguageRipple />
        </div>

        {/* Seven Crowns Constellation */}
        <div className="mb-16">
          <h3 className="text-2xl font-bold text-center mb-8 text-yellow-400">
            The Complete Constellation
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {crowns.map(function (crown, index) {
            var ConstellationCrownCard = styled_components_1.default.div(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n                background: linear-gradient(to bottom right, #a78bfa20, #6366f120);\n                backdrop-filter: blur(4px);\n                border-radius: 0.75rem;\n                padding: 1.5rem;\n                border: 1px solid rgba(255, 255, 255, 0.12);\n                transition: all 1s;\n                animation-delay: ", ";\n                opacity: ", ";\n                transform: translateY(", "px);\n                &:hover {\n                  transform: scale(1.05);\n                }\n              "], ["\n                background: linear-gradient(to bottom right, #a78bfa20, #6366f120);\n                backdrop-filter: blur(4px);\n                border-radius: 0.75rem;\n                padding: 1.5rem;\n                border: 1px solid rgba(255, 255, 255, 0.12);\n                transition: all 1s;\n                animation-delay: ", ";\n                opacity: ", ";\n                transform: translateY(", "px);\n                &:hover {\n                  transform: scale(1.05);\n                }\n              "])), function (_a) {
                var delay = _a.delay;
                return delay;
            }, function (_a) {
                var opacity = _a.opacity;
                return opacity;
            }, function (_a) {
                var translateY = _a.translateY;
                return translateY;
            });
            return (<ConstellationCrownCard key={crown.name} delay={"".concat(index * 0.3, "s")} opacity={currentPhase >= 1 ? 1 : 0.6} translateY={currentPhase >= 1 ? 0 : 16}>
                  <div className={"w-8 h-8 rounded-full bg-gradient-to-r ".concat(crown.color, " mb-4 mx-auto animate-pulse")}></div>
                  <h4 className="text-lg font-bold text-center mb-2 text-yellow-300">
                    {crown.name}
                  </h4>
                  <p className="text-sm text-center text-gray-400">{crown.domain}</p>
                </ConstellationCrownCard>);
        })}
          </div>
        </div>

        {/* Call to Action */}
        <div className="text-center">
          <div className="bg-gradient-to-r from-yellow-600/20 via-orange-600/20 to-red-600/20 backdrop-blur-sm rounded-lg p-8 border border-yellow-400/30">
            <h3 className="text-3xl font-bold mb-4 text-yellow-400">
              🔥 Enter the Eternal Flame 🔥
            </h3>
            <p className="text-xl mb-6 text-gray-300">
              Join millions across the world in the global stewardship of digital sovereignty
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <link_1.default href="/omega-crown">
                <button className="px-8 py-4 bg-gradient-to-r from-yellow-600 to-orange-600 hover:from-yellow-700 hover:to-orange-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg border-2 border-yellow-400/50">
                  Ω Omega Crown of Eternity
                </button>
              </link_1.default>
              <link_1.default href="/dashboard/customer">
                <button className="px-8 py-4 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg">
                  Begin Custodial Journey
                </button>
              </link_1.default>
              <link_1.default href="/codex-constellation">
                <button className="px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg">
                  Explore the Constellation
                </button>
              </link_1.default>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{"\n        .stars {\n          position: absolute;\n          top: 0;\n          left: 0;\n          right: 0;\n          bottom: 0;\n          width: 100%;\n          height: 100%;\n          background: transparent url('/stars.png') repeat top center;\n          animation: move-twink-back 200s linear infinite;\n        }\n\n        .twinkling {\n          position: absolute;\n          top: 0;\n          left: 0;\n          right: 0;\n          bottom: 0;\n          width: 100%;\n          height: 100%;\n          background: transparent url('/twinkling.png') repeat top center;\n          animation: move-twink-back 100s linear infinite;\n        }\n\n        @keyframes move-twink-back {\n          from {\n            background-position: 0 0;\n          }\n          to {\n            background-position: -10000px 5000px;\n          }\n        }\n      "}</style>
    </div>);
};
exports.default = GlobalInduction;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
