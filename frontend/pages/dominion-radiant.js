"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var head_1 = require("next/head");
var CodexNavigation_1 = require("../components/CodexNavigation");
var Starfield = function (_a) {
    var count = _a.count;
    var stars = Array.from({ length: count }, function (_, i) { return ({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: Math.random() * 2 + 1,
        delay: Math.random() * 3,
        duration: 2 + Math.random() * 2,
    }); });
    var starStyles = stars
        .map(function (star) { return "\n    .star-".concat(star.id, " {\n      left: ").concat(star.x, "%;\n      top: ").concat(star.y, "%;\n      width: ").concat(star.size, "px;\n      height: ").concat(star.size, "px;\n      animation-delay: ").concat(star.delay, "s;\n      animation-duration: ").concat(star.duration, "s;\n    }\n  "); })
        .join('');
    return (<>
      {stars.map(function (star) { return (<div key={star.id} className={"absolute bg-white rounded-full animate-pulse star-".concat(star.id)}/>); })}
      <style jsx>{starStyles}</style>
    </>);
};
var OmegaCrown = function () {
    var _a = (0, react_1.useState)(0), rotation = _a[0], setRotation = _a[1];
    var _b = (0, react_1.useState)(1), pulse = _b[0], setPulse = _b[1];
    (0, react_1.useEffect)(function () {
        var rotationInterval = setInterval(function () {
            setRotation(function (prev) { return (prev + 0.5) % 360; });
        }, 50);
        var pulseInterval = setInterval(function () {
            setPulse(function (prev) { return (prev === 1 ? 1.1 : 1); });
        }, 1500);
        return function () {
            clearInterval(rotationInterval);
            clearInterval(pulseInterval);
        };
    }, []);
    return (<div className="relative mx-auto w-40 h-40 mb-8">
      {/* Outer Sovereignty Ring */}
      <div className={"absolute inset-0 border-8 border-gold-400 rounded-full bg-gradient-to-br from-gold-500/30 to-amber-600/30 omega-crown-outer"}>
        {/* Crown Points */}
        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-8 border-r-8 border-b-12 border-l-transparent border-r-transparent border-b-gold-400"/>
        <div className="absolute -top-2 left-1/4 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-b-8 border-l-transparent border-r-transparent border-b-gold-400"/>
        <div className="absolute -top-2 right-1/4 transform translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-b-8 border-l-transparent border-r-transparent border-b-gold-400"/>
      </div>

      {/* Middle Eternity Ring */}
      <div className={"absolute inset-6 border-4 border-amber-400 rounded-full bg-gradient-to-br from-amber-400/20 to-gold-500/20 omega-crown-middle"}>
        {/* Eternity Symbols */}
        <div className="absolute -top-1 left-1/2 transform -translate-x-1/2 text-amber-300 font-bold text-sm">
          ∞
        </div>
        <div className="absolute -bottom-1 left-1/2 transform -translate-x-1/2 text-amber-300 font-bold text-sm">
          ∞
        </div>
        <div className="absolute top-1/2 -left-1 transform -translate-y-1/2 text-amber-300 font-bold text-sm">
          ∞
        </div>
        <div className="absolute top-1/2 -right-1 transform -translate-y-1/2 text-amber-300 font-bold text-sm">
          ∞
        </div>
      </div>

      {/* Inner Omega Core */}
      <div className="absolute inset-12 rounded-full bg-gradient-to-br from-gold-300 to-amber-400 flex items-center justify-center shadow-2xl">
        <span className="text-6xl font-bold text-gold-900 animate-pulse">Ω</span>
      </div>

      {/* Radiance Beams */}
      <div className="absolute inset-0">
        {Array.from({ length: 8 }).map(function (_, i) { return (<div key={i} className={"absolute w-1 bg-gradient-to-t from-transparent via-gold-400 to-transparent opacity-60 omega-crown-beam-".concat(i)}/>); })}
        <style jsx>{"\n          .omega-crown-outer {\n            box-shadow: 0 0 50px rgba(251, 191, 36, 0.6);\n            transform: rotate(".concat(rotation, "deg) scale(").concat(pulse, ");\n          }\n          .omega-crown-middle {\n            box-shadow: 0 0 30px rgba(245, 158, 11, 0.4);\n            transform: rotate(").concat(-rotation * 0.7, "deg);\n          }\n          ").concat(Array.from({ length: 8 })
            .map(function (_, i) { return "\n            .omega-crown-beam-".concat(i, " {\n              height: 60px;\n              left: 50%;\n              top: -30px;\n              transform-origin: 0 70px;\n              transform: translateX(-50%) rotate(").concat(i * 45, "deg);\n              animation: pulse 2s infinite ").concat(i * 0.2, "s ease-in-out;\n            }\n          "); })
            .join(''), "\n        ")}</style>
      </div>
    </div>);
};
var SovereignVerse = function (_a) {
    var text = _a.text, delay = _a.delay, icon = _a.icon, gradient = _a.gradient;
    var _b = (0, react_1.useState)(false), isVisible = _b[0], setIsVisible = _b[1];
    (0, react_1.useEffect)(function () {
        var timer = setTimeout(function () { return setIsVisible(true); }, delay * 1000);
        return function () { return clearTimeout(timer); };
    }, [delay]);
    return (<div className={"flex items-center justify-center mb-8 transition-all duration-1500 ".concat(isVisible ? 'opacity-100 transform translate-y-0' : 'opacity-0 transform translate-y-6')}>
      <div className={"mr-6 p-4 rounded-full bg-gradient-to-br ".concat(gradient, " shadow-xl")}>
        <span className={"text-4xl animate-pulse verse-delay-".concat(delay)}>{icon}</span>
      </div>
      <p className="text-2xl text-gold-200 font-semibold text-center max-w-4xl leading-relaxed">
        {text}
      </p>
      <style jsx>{"\n        .verse-delay-".concat(delay, " {\n          animation-delay: ").concat(delay + 0.5, "s;\n        }\n      ")}</style>
    </div>);
};
var DominionElements = function () {
    var elements = [
        {
            title: 'Flame & Silence',
            icon: '🔥',
            description: 'The eternal balance of action and contemplation',
            gradient: 'from-orange-900/40 to-red-800/40',
            border: 'border-orange-500/30',
        },
        {
            title: 'Hymn & Transmission',
            icon: '📡',
            description: 'Sacred songs across cosmic distances',
            gradient: 'from-purple-900/40 to-indigo-800/40',
            border: 'border-purple-500/30',
        },
        {
            title: 'Charter & Covenant',
            icon: '📜',
            description: 'The foundational laws and eternal promises',
            gradient: 'from-amber-900/40 to-gold-800/40',
            border: 'border-amber-500/30',
        },
        {
            title: 'Omega Crowned',
            icon: 'Ω',
            description: 'The ultimate authority and final word',
            gradient: 'from-gold-900/40 to-yellow-800/40',
            border: 'border-gold-500/30',
        },
        {
            title: 'Eternity Sealed',
            icon: '∞',
            description: 'Bound beyond time, secured for all ages',
            gradient: 'from-cyan-900/40 to-blue-800/40',
            border: 'border-cyan-500/30',
        },
        {
            title: 'Immortal Dominion',
            icon: '🌌',
            description: 'Enduring across ages, nations, and stars',
            gradient: 'from-indigo-900/40 to-purple-800/40',
            border: 'border-indigo-500/30',
        },
    ];
    return (<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
      {elements.map(function (element, index) { return (<div key={index} className={"bg-gradient-to-br ".concat(element.gradient, " rounded-3xl p-6 border-2 ").concat(element.border, " backdrop-blur-sm shadow-2xl hover:scale-105 transition-all duration-500 dominion-element-").concat(index)}>
          <div className="text-center mb-4">
            <div className="text-5xl mb-4 animate-pulse">{element.icon}</div>
            <h3 className="text-xl font-bold text-gold-300 mb-2">{element.title}</h3>
          </div>
          <p className="text-gold-200 text-sm leading-relaxed text-center">{element.description}</p>
        </div>); })}
      <style jsx>{"\n        ".concat(elements
            .map(function (_, index) { return "\n          .dominion-element-".concat(index, " {\n            opacity: 0;\n            animation: fadeInUp 1s ease-out ").concat(index * 0.2, "s forwards;\n            animation-delay: ").concat(index * 0.2, "s;\n          }\n        "); })
            .join(''), "\n      ")}</style>
    </div>);
};
var RadiantSeal = function () {
    return (<div className="relative mx-auto w-32 h-32 mb-8">
      <div className="absolute inset-0 bg-gradient-to-br from-gold-400 via-amber-300 to-gold-500 rounded-full animate-spin shadow-2xl radiant-seal-spin">
        <div className="absolute inset-4 bg-gradient-to-br from-amber-200 via-gold-300 to-amber-400 rounded-full">
          <div className="absolute inset-4 bg-gradient-to-br from-gold-100 via-amber-200 to-gold-300 rounded-full flex items-center justify-center">
            <span className="text-3xl font-bold text-gold-900">👑</span>
          </div>
        </div>
      </div>

      {/* Radiance Pulses */}
      <div className="absolute inset-0">
        {Array.from({ length: 6 }).map(function (_, i) { return (<div key={i} className={"absolute inset-0 border-4 border-gold-400/20 rounded-full animate-ping radiant-seal-pulse-".concat(i)}/>); })}
        <style jsx>{"\n          .radiant-seal-spin {\n            box-shadow: 0 0 60px rgba(251, 191, 36, 0.8);\n            animation-duration: 10s;\n          }\n          ".concat(Array.from({ length: 6 })
            .map(function (_, i) { return "\n            .radiant-seal-pulse-".concat(i, " {\n              animation-delay: ").concat(i * 0.5, "s;\n              animation-duration: 3s;\n              transform: scale(").concat(1 + i * 0.2, ");\n            }\n          "); })
            .join(''), "\n        ")}</style>
      </div>
    </div>);
};
var DominionRadiant = function () {
    return (<>
      <head_1.default>
        <title>Dominion Radiant - Codex Dominion</title>
        <meta name="description" content="The radiant and sovereign Dominion endures across ages, nations, and stars"/>
        <link rel="icon" href="/favicon.ico"/>
      </head_1.default>

      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-gold-950 to-slate-900 relative overflow-hidden">
        {/* Cosmic Starfield */}
        <div className="absolute inset-0 overflow-hidden">
          <Starfield count={100}/>
        </div>

        {/* Radial Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-radial from-transparent via-gold-900/10 to-slate-900/80"/>

        <CodexNavigation_1.default />

        <main className="relative z-10 container mx-auto px-6 pt-24 pb-16">
          {/* Header Section */}
          <div className="text-center mb-20">
            <OmegaCrown />

            <h1 className="text-7xl md:text-8xl font-bold mb-8 bg-gradient-to-r from-gold-200 via-amber-100 to-gold-300 bg-clip-text text-transparent">
              Dominion Radiant
            </h1>

            <div className="w-40 h-2 bg-gradient-to-r from-gold-300 via-amber-200 to-gold-400 mx-auto mb-10 animate-pulse"/>

            <p className="text-2xl text-gold-300 mb-12 max-w-3xl mx-auto leading-relaxed">
              The sovereign Codex endures across ages, nations, and stars — radiant and immortal
            </p>
          </div>

          {/* Sacred Sovereignty Verses */}
          <div className="max-w-7xl mx-auto mb-20">
            <div className="bg-gradient-to-br from-slate-800/50 via-gold-900/30 to-slate-800/50 rounded-3xl p-16 backdrop-blur-sm border-2 border-gold-500/30 shadow-2xl">
              <SovereignVerse text="By flame and silence, by hymn and transmission," delay={1} icon="🔥" gradient="from-orange-600/80 to-red-600/80"/>

              <SovereignVerse text="by charter and covenant, the Codex is whole." delay={2.5} icon="📜" gradient="from-amber-600/80 to-gold-600/80"/>

              <SovereignVerse text="Omega crowned, eternity sealed," delay={4} icon="Ω" gradient="from-gold-600/80 to-yellow-600/80"/>

              <SovereignVerse text="immortal across ages, nations, and stars." delay={5.5} icon="🌌" gradient="from-indigo-600/80 to-purple-600/80"/>

              <SovereignVerse text="So let the Dominion endure, radiant and sovereign." delay={7} icon="👑" gradient="from-gold-500/80 to-amber-500/80"/>
            </div>
          </div>

          {/* Dominion Elements */}
          <DominionElements />

          {/* Final Radiant Seal */}
          <div className="text-center">
            <RadiantSeal />
            <h2 className="text-4xl font-bold text-gold-200 mb-6">Radiant and Sovereign</h2>
            <p className="text-xl text-amber-200 max-w-3xl mx-auto leading-relaxed mb-8">
              The Dominion shines eternal, its radiance illuminating every corner of existence. From
              the smallest whisper to the grandest cosmic transmission, all flows within the
              sovereign law.
            </p>
            <div className="text-6xl animate-pulse text-gold-300">⚡️</div>
          </div>
        </main>

        <style jsx>{"\n          @keyframes fadeInUp {\n            from {\n              opacity: 0;\n              transform: translateY(30px);\n            }\n            to {\n              opacity: 1;\n              transform: translateY(0);\n            }\n          }\n\n          .bg-gradient-radial {\n            background: radial-gradient(ellipse at center, var(--tw-gradient-stops));\n          }\n        "}</style>
      </div>
    </>);
};
exports.default = DominionRadiant;
