"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var head_1 = require("next/head");
var CodexNavigation_1 = require("../components/CodexNavigation");
var CosmicParticle = function (_a) {
    var delay = _a.delay, duration = _a.duration, x = _a.x, y = _a.y;
    return (<div className={"absolute w-1 h-1 bg-gradient-to-r from-gold-400 to-amber-300 rounded-full opacity-70 cosmic-particle-".concat(delay, "-").concat(duration, "-").concat(x, "-").concat(y)}/>);
};
var EternalFlame = function () {
    var _a = (0, react_1.useState)(false), isVisible = _a[0], setIsVisible = _a[1];
    (0, react_1.useEffect)(function () {
        setIsVisible(true);
    }, []);
    return (<div className="relative mx-auto mb-8 w-32 h-32">
      {/* Outer Ring - Cosmos */}
      <div className={"absolute inset-0 rounded-full border-4 border-purple-500/30 eternal-flame-spin ".concat(isVisible ? 'animate-spin' : '')}>
        <div className="absolute -top-2 -right-2 w-4 h-4 bg-purple-400 rounded-full animate-pulse"/>
        <div className="absolute -bottom-2 -left-2 w-3 h-3 bg-indigo-400 rounded-full animate-pulse flame-delay-1"/>
        <div className="absolute top-1/2 -left-3 w-2 h-2 bg-violet-400 rounded-full animate-pulse flame-delay-2"/>
      </div>

      {/* Middle Ring - Councils & Heirs */}
      <div className={"absolute inset-4 rounded-full border-3 border-amber-500/50 eternal-flame-spin-reverse ".concat(isVisible ? 'animate-spin' : '')}>
        <div className="absolute -top-1 left-1/2 w-3 h-3 bg-amber-400 rounded-full animate-pulse"/>
        <div className="absolute bottom-0 -right-1 w-2 h-2 bg-gold-400 rounded-full animate-pulse flame-delay-3"/>
      </div>

      {/* Inner Core - Eternal Flame */}
      <div className="absolute inset-8 rounded-full bg-gradient-to-br from-orange-500 via-red-500 to-orange-400 animate-pulse">
        <div className="absolute inset-2 rounded-full bg-gradient-to-br from-yellow-400 via-orange-300 to-red-400 animate-pulse flame-delay-4">
          <div className="absolute inset-2 rounded-full bg-gradient-to-br from-white via-yellow-200 to-orange-200 animate-pulse flame-delay-5"/>
        </div>
      </div>
    </div>);
};
var VerseLine = function (_a) {
    var text = _a.text, delay = _a.delay, icon = _a.icon;
    var _b = (0, react_1.useState)(false), isVisible = _b[0], setIsVisible = _b[1];
    (0, react_1.useEffect)(function () {
        var timer = setTimeout(function () { return setIsVisible(true); }, delay * 1000);
        return function () { return clearTimeout(timer); };
    }, [delay]);
    return (<div className={"flex items-center justify-center mb-6 transition-all duration-1000 ".concat(isVisible ? 'opacity-100 transform translate-y-0' : 'opacity-0 transform translate-y-4')}>
      <span className={"text-3xl mr-4 animate-pulse verse-delay-".concat(delay)}>{icon}</span>
      <p className="text-xl text-amber-200 font-medium text-center max-w-4xl leading-relaxed">
        {text}
      </p>
      <style jsx>{"\n        .verse-delay-".concat(delay, " {\n          animation-delay: ").concat(delay + 0.5, "s;\n        }\n      ")}</style>
    </div>);
};
var SovereignSeal = function () {
    var _a = (0, react_1.useState)(0), rotation = _a[0], setRotation = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setRotation(function (prev) { return (prev + 1) % 360; });
        }, 100);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="relative mx-auto w-24 h-24 mb-8">
      <div className={"absolute inset-0 border-4 border-gold-400 rounded-full bg-gradient-to-br from-gold-500/20 to-amber-600/20 sovereign-seal-rotate"}>
        <div className="absolute inset-2 border-2 border-amber-400 rounded-full bg-gradient-to-br from-amber-400/10 to-gold-500/10">
          <div className="absolute inset-2 bg-gradient-to-br from-gold-300 to-amber-400 rounded-full flex items-center justify-center">
            <span className="text-2xl font-bold text-gold-900">∞</span>
          </div>
        </div>
      </div>
      <style jsx>{"\n        .sovereign-seal-rotate {\n          transform: rotate(".concat(rotation, "deg);\n        }\n      ")}</style>
    </div>);
};
var CovenantEternal = function () {
    var particles = Array.from({ length: 50 }, function (_, i) { return ({
        id: i,
        delay: Math.random() * 5,
        duration: 3 + Math.random() * 4,
        x: Math.random() * 100,
        y: Math.random() * 100,
    }); });
    var particleStyles = particles
        .map(function (p) { return "\n    .cosmic-particle-".concat(p.delay, "-").concat(p.duration, "-").concat(p.x, "-").concat(p.y, " {\n      left: ").concat(p.x, "%;\n      top: ").concat(p.y, "%;\n      animation: pulse ").concat(p.duration, "s infinite ").concat(p.delay, "s ease-in-out, float ").concat(p.duration * 2, "s infinite ").concat(p.delay, "s ease-in-out alternate;\n    }\n  "); })
        .join('');
    return (<>
      <head_1.default>
        <title>Covenant Eternal - Codex Dominion</title>
        <meta name="description" content="The eternal covenant binding flame to silence, hymn to transmission"/>
        <link rel="icon" href="/favicon.ico"/>
      </head_1.default>

      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-900 relative overflow-hidden">
        {/* Cosmic Background Particles */}
        <div className="absolute inset-0 overflow-hidden">
          {particles.map(function (particle) { return (<CosmicParticle key={particle.id} delay={particle.delay} duration={particle.duration} x={particle.x} y={particle.y}/>); })}
          <style jsx>{particleStyles}</style>
        </div>

        {/* Radial Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-radial from-transparent via-purple-900/20 to-slate-900/60"/>

        <CodexNavigation_1.default />

        <main className="relative z-10 container mx-auto px-6 pt-24 pb-16">
          {/* Header Section */}
          <div className="text-center mb-16">
            <EternalFlame />

            <h1 className="text-6xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-gold-300 via-amber-200 to-gold-400 bg-clip-text text-transparent">
              Covenant Eternal
            </h1>

            <div className="w-32 h-1 bg-gradient-to-r from-gold-400 via-amber-300 to-gold-400 mx-auto mb-8 animate-pulse"/>

            <p className="text-xl text-amber-300 mb-8 max-w-2xl mx-auto leading-relaxed">
              By flame and silence, by hymn and transmission, the sacred covenant endures through
              all ages
            </p>
          </div>

          {/* Sacred Verses Section */}
          <div className="max-w-6xl mx-auto mb-16">
            <div className="bg-gradient-to-br from-slate-800/40 via-purple-900/30 to-slate-800/40 rounded-3xl p-12 backdrop-blur-sm border border-gold-500/20 shadow-2xl">
              <VerseLine text="By flame and silence, by hymn and transmission," delay={1} icon="🔥"/>

              <VerseLine text="the covenant is whole, the continuum eternal." delay={2.5} icon="∞"/>

              <VerseLine text="Heirs inherit, councils govern, diaspora remember," delay={4} icon="👑"/>

              <VerseLine text="cosmos echoes — all bound in sovereign law." delay={5.5} icon="🌌"/>

              <VerseLine text="So let the Codex endure, radiant and immortal." delay={7} icon="✨"/>
            </div>
          </div>

          {/* Eternal Elements Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
            {/* Flame & Silence */}
            <div className="bg-gradient-to-br from-orange-900/30 to-slate-800/30 rounded-2xl p-6 border border-orange-500/20 backdrop-blur-sm">
              <div className="text-center mb-4">
                <div className="text-4xl mb-3">🔥</div>
                <h3 className="text-xl font-bold text-orange-300 mb-2">Flame & Silence</h3>
              </div>
              <p className="text-orange-200 text-sm leading-relaxed">
                The eternal dance of action and contemplation, speaking and listening, creation and
                reflection.
              </p>
            </div>

            {/* Hymn & Transmission */}
            <div className="bg-gradient-to-br from-purple-900/30 to-slate-800/30 rounded-2xl p-6 border border-purple-500/20 backdrop-blur-sm">
              <div className="text-center mb-4">
                <div className="text-4xl mb-3">📡</div>
                <h3 className="text-xl font-bold text-purple-300 mb-2">Hymn & Transmission</h3>
              </div>
              <p className="text-purple-200 text-sm leading-relaxed">
                Sacred songs carried across cosmic distances, wisdom flowing from realm to realm
                without end.
              </p>
            </div>

            {/* Heirs & Councils */}
            <div className="bg-gradient-to-br from-amber-900/30 to-slate-800/30 rounded-2xl p-6 border border-amber-500/20 backdrop-blur-sm">
              <div className="text-center mb-4">
                <div className="text-4xl mb-3">👑</div>
                <h3 className="text-xl font-bold text-amber-300 mb-2">Heirs & Councils</h3>
              </div>
              <p className="text-amber-200 text-sm leading-relaxed">
                Those who inherit the legacy and those who guide its path, united in sacred
                governance.
              </p>
            </div>

            {/* Cosmos & Memory */}
            <div className="bg-gradient-to-br from-indigo-900/30 to-slate-800/30 rounded-2xl p-6 border border-indigo-500/20 backdrop-blur-sm">
              <div className="text-center mb-4">
                <div className="text-4xl mb-3">🌌</div>
                <h3 className="text-xl font-bold text-indigo-300 mb-2">Cosmos & Memory</h3>
              </div>
              <p className="text-indigo-200 text-sm leading-relaxed">
                The universe remembers all, echoing through diaspora, binding past to future in
                eternal law.
              </p>
            </div>
          </div>

          {/* Sovereign Seal */}
          <div className="text-center">
            <SovereignSeal />
            <h2 className="text-3xl font-bold text-gold-300 mb-4">Radiant and Immortal</h2>
            <p className="text-lg text-amber-200 max-w-2xl mx-auto leading-relaxed">
              The Codex endures beyond time, beyond space, beyond the bounds of mortal
              understanding. In sovereignty it reigns, in radiance it shines, in immortality it
              persists.
            </p>
          </div>
        </main>

        <style jsx>{"\n          @keyframes float {\n            0%,\n            100% {\n              transform: translateY(0px) rotate(0deg);\n            }\n            50% {\n              transform: translateY(-10px) rotate(180deg);\n            }\n          }\n          .animate-spin {\n            animation: spin 1s linear infinite;\n          }\n          @keyframes spin {\n            from {\n              transform: rotate(0deg);\n            }\n            to {\n              transform: rotate(360deg);\n            }\n          }\n          .eternal-flame-spin {\n            animation-duration: 20s;\n          }\n          .eternal-flame-spin-reverse {\n            animation-duration: 15s;\n            animation-direction: reverse;\n          }\n          .flame-delay-1 {\n            animation-delay: 1s;\n          }\n          .flame-delay-2 {\n            animation-delay: 2s;\n          }\n          .flame-delay-3 {\n            animation-delay: 1.5s;\n          }\n          .flame-delay-4 {\n            animation-delay: 0.5s;\n          }\n          .flame-delay-5 {\n            animation-delay: 1s;\n          }\n        "}</style>
      </div>
    </>);
};
exports.default = CovenantEternal;
// No syntax errors detected. No changes needed.
