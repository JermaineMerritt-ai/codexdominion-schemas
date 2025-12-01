"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var head_1 = require("next/head");
var CodexNavigation_1 = require("../components/CodexNavigation");
var LuminousParticle = function (_a) {
    var delay = _a.delay, duration = _a.duration, x = _a.x, y = _a.y, size = _a.size, color = _a.color;
    return (<div className={"absolute ".concat(color, " rounded-full opacity-80 luminous-particle left-[").concat(x, "%] top-[").concat(y, "%] w-[").concat(size, "px] h-[").concat(size, "px] animate-[luminousFloat_").concat(duration, "s_infinite_").concat(delay, "s_ease-in-out,luminousPulse_").concat(duration * 0.8, "s_infinite_").concat(delay, "s_ease-in-out]")}/>);
};
var CompendiumCore = function () {
    var _a = (0, react_1.useState)(0), rotation = _a[0], setRotation = _a[1];
    var _b = (0, react_1.useState)(0), innerRotation = _b[0], setInnerRotation = _b[1];
    var _c = (0, react_1.useState)(0), outerRotation = _c[0], setOuterRotation = _c[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setRotation(function (prev) { return (prev + 0.2) % 360; });
            setInnerRotation(function (prev) { return (prev - 0.3) % 360; });
            setOuterRotation(function (prev) { return (prev + 0.1) % 360; });
        }, 50);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="relative mx-auto w-56 h-56 mb-16">
      {/* Outermost Compendium Ring */}
      <div className={"absolute inset-0 border-12 border-cyan-400 rounded-full bg-gradient-to-br from-cyan-500/50 to-blue-600/50 shadow-2xl compendium-outer-ring rotate-[".concat(outerRotation, "deg]")}>
        {/* All Elements Symbols */}
        <div className="absolute -top-6 left-1/2 transform -translate-x-1/2 text-cyan-200 font-bold text-2xl">
          📜
        </div>
        <div className="absolute -bottom-6 left-1/2 transform -translate-x-1/2 text-cyan-200 font-bold text-2xl">
          🎵
        </div>
        <div className="absolute top-1/2 -left-6 transform -translate-y-1/2 text-cyan-200 font-bold text-2xl">
          🔇
        </div>
        <div className="absolute top-1/2 -right-6 transform -translate-y-1/2 text-cyan-200 font-bold text-2xl">
          📡
        </div>
        <div className="absolute top-1/4 -right-4 transform -translate-y-1/2 text-cyan-200 font-bold text-xl">
          📖
        </div>
        <div className="absolute bottom-1/4 -left-4 transform translate-y-1/2 text-cyan-200 font-bold text-xl">
          👑
        </div>
        <div className="absolute top-1/4 -left-4 transform -translate-y-1/2 text-cyan-200 font-bold text-xl">
          🛡️
        </div>
        <div className="absolute bottom-1/4 -right-4 transform translate-y-1/2 text-cyan-200 font-bold text-xl">
          🧠
        </div>
      </div>

      {/* Middle Sovereign Ring */}
      <div className={"absolute inset-8 border-8 border-gold-400 rounded-full bg-gradient-to-br from-gold-500/40 to-amber-600/40 compendium-inner-ring rotate-[".concat(innerRotation, "deg]")}>
        {/* Eternal Symbols */}
        <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 text-gold-200 font-bold text-xl">
          ∞
        </div>
        <div className="absolute -bottom-3 left-1/2 transform -translate-x-1/2 text-gold-200 font-bold text-xl">
          ✨
        </div>
        <div className="absolute top-1/2 -left-3 transform -translate-y-1/2 text-gold-200 font-bold text-xl">
          Ω
        </div>
        <div className="absolute top-1/2 -right-3 transform -translate-y-1/2 text-gold-200 font-bold text-xl">
          🔥
        </div>
      </div>

      {/* Inner Luminous Core */}
      <div className={"absolute inset-16 rounded-full bg-gradient-to-br from-white via-cyan-200 to-gold-300 flex items-center justify-center shadow-2xl compendium-core-ring rotate-[".concat(rotation, "deg]")}>
        <span className="text-7xl font-bold text-slate-900 animate-pulse">📚</span>
      </div>

      {/* Luminous Rays */}
      <div className="absolute inset-0">
        {Array.from({ length: 16 }).map(function (_, i) { return (<div key={i} className={"absolute w-2 bg-gradient-to-t from-transparent via-cyan-400 to-transparent opacity-80 compendium-ray h-[100px] left-[50%] top-[-50px] origin-[0_106px] rotate-[".concat(i * 22.5, "deg] animate-[pulse_4s_infinite_").concat(i * 0.25, "s_ease-in-out]")}/>); })}
      </div>

      {/* Luminous Pulses */}
      <div className="absolute inset-0">
        {Array.from({ length: 6 }).map(function (_, i) { return (<div key={i} className="absolute inset-0 border-4 border-cyan-400/15 rounded-full animate-ping compendium-pulse scale-[${1.3 + i * 0.4}] animate-[ping_3.6s_infinite_${i * 0.6}s]"/>); })}
      </div>
    </div>);
};
var CompendiumVerse = function (_a) {
    var text = _a.text, delay = _a.delay, icon = _a.icon, gradient = _a.gradient, _b = _a.highlight, highlight = _b === void 0 ? [] : _b;
    var _c = (0, react_1.useState)(false), isVisible = _c[0], setIsVisible = _c[1];
    (0, react_1.useEffect)(function () {
        var timer = setTimeout(function () { return setIsVisible(true); }, delay * 1000);
        return function () { return clearTimeout(timer); };
    }, [delay]);
    var renderText = function () {
        var processedText = text;
        if (highlight.length > 0) {
            highlight.forEach(function (word) {
                if (processedText.includes(word)) {
                    processedText = processedText.replace(new RegExp("\\b".concat(word, "\\b"), 'g'), "<span class=\"text-cyan-200 font-bold bg-gradient-to-r from-cyan-400/30 to-blue-400/30 px-2 py-1 rounded-lg shadow-lg\">".concat(word, "</span>"));
                }
            });
        }
        return <span dangerouslySetInnerHTML={{ __html: processedText }}/>;
    };
    return (<div className={"flex items-center justify-center mb-10 compendium-verse ".concat(isVisible ? 'verse-visible' : 'verse-hidden')}>
      <div className={"mr-10 p-8 rounded-full bg-gradient-to-br ".concat(gradient, " shadow-2xl border-2 border-cyan-400/40")}>
        <span className={"text-6xl animate-pulse compendium-verse-icon animate-[pulse_2s_infinite_".concat(delay + 0.5, "s]")}>
          {icon}
        </span>
      </div>
      <p className="text-3xl text-cyan-200 font-semibold text-center max-w-5xl leading-relaxed">
        {renderText()}
      </p>
    </div>);
};
var LuminousField = function () {
    var luminousElements = Array.from({ length: 80 }, function (_, i) { return ({
        id: i,
        delay: Math.random() * 5,
        duration: 3 + Math.random() * 4,
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: 2 + Math.random() * 6,
        color: [
            'bg-cyan-400',
            'bg-blue-400',
            'bg-gold-400',
            'bg-white',
            'bg-amber-400',
            'bg-yellow-400',
        ][Math.floor(Math.random() * 6)],
    }); });
    return (<div className="absolute inset-0 overflow-hidden pointer-events-none">
      {luminousElements.map(function (element) { return (<LuminousParticle key={element.id} delay={element.delay} duration={element.duration} x={element.x} y={element.y} size={element.size} color={element.color}/>); })}
    </div>);
};
var AllElements = function () {
    var elements = [
        {
            title: 'All Scrolls Gathered',
            icon: '📜',
            description: 'Every sacred document collected and preserved',
            gradient: 'from-amber-900/60 to-gold-800/60',
            border: 'border-amber-500/50',
        },
        {
            title: 'All Hymns Sung',
            icon: '🎵',
            description: 'Every sacred song echoing through the cosmos',
            gradient: 'from-purple-900/60 to-indigo-800/60',
            border: 'border-purple-500/50',
        },
        {
            title: 'All Silences Crowned',
            icon: '🔇',
            description: 'Every moment of contemplation honored',
            gradient: 'from-slate-900/60 to-gray-800/60',
            border: 'border-slate-500/50',
        },
        {
            title: 'All Transmissions Sent',
            icon: '📡',
            description: 'Every message broadcast across realms',
            gradient: 'from-blue-900/60 to-cyan-800/60',
            border: 'border-blue-500/50',
        },
        {
            title: 'All Charters Sealed',
            icon: '📋',
            description: 'Every foundational law established',
            gradient: 'from-green-900/60 to-emerald-800/60',
            border: 'border-green-500/50',
        },
        {
            title: 'All Crowns Eternal',
            icon: '👑',
            description: 'Every sovereignty established forever',
            gradient: 'from-gold-900/60 to-yellow-800/60',
            border: 'border-gold-500/50',
        },
        {
            title: 'All Marks Inscribed',
            icon: '🛡️',
            description: 'Every custodianship recorded permanently',
            gradient: 'from-orange-900/60 to-red-800/60',
            border: 'border-orange-500/50',
        },
        {
            title: 'All Memory Sovereign',
            icon: '🧠',
            description: 'Every remembrance holding supreme authority',
            gradient: 'from-violet-900/60 to-purple-800/60',
            border: 'border-violet-500/50',
        },
    ];
    return (<div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-20">
      {elements.map(function (element, index) { return (<div key={index} className={"bg-gradient-to-br ".concat(element.gradient, " rounded-3xl p-6 border-2 ").concat(element.border, " backdrop-blur-sm shadow-2xl hover:scale-105 transition-all duration-700 relative overflow-hidden all-element-card animate-[luminousRise_1.5s_ease-out_").concat(index * 0.15, "s_forwards] opacity-0")}>
          <div className="text-center mb-4">
            <div className="text-5xl mb-4 animate-pulse">{element.icon}</div>
            <h3 className="text-lg font-bold text-cyan-300 mb-3">{element.title}</h3>
          </div>
          <p className="text-cyan-200 text-sm leading-relaxed text-center">{element.description}</p>

          {/* Completion Indicator */}
          <div className="absolute top-2 right-2 w-4 h-4 bg-green-400 rounded-full animate-ping"/>
        </div>); })}
    </div>);
};
var LuminousSeal = function () {
    var _a = (0, react_1.useState)(1), intensity = _a[0], setIntensity = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setIntensity(function (prev) { return (prev === 1 ? 1.3 : 1); });
        }, 2500);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="relative mx-auto w-48 h-48 mb-16">
      <div className={"absolute inset-0 bg-gradient-to-br from-cyan-300 via-white to-gold-400 rounded-full shadow-2xl luminous-seal scale-[".concat(intensity, "]")}>
        <div className="absolute inset-8 bg-gradient-to-br from-white via-cyan-200 to-gold-300 rounded-full">
          <div className="absolute inset-8 bg-gradient-to-br from-cyan-100 via-white to-amber-200 rounded-full flex items-center justify-center">
            <div className="text-center">
              <div className="text-5xl font-bold text-slate-900 mb-2">📚</div>
              <div className="text-lg font-bold text-slate-900">LUMINOUS</div>
            </div>
          </div>
        </div>
      </div>

      {/* Luminous Aura */}
      <div className="absolute inset-0">
        {Array.from({ length: 8 }).map(function (_, i) { return (<div key={i} className="absolute inset-0 border-6 border-cyan-400/10 rounded-full animate-ping luminous-seal-pulse scale-[${1.4 + i * 0.3}] animate-[ping_3.2s_infinite_${i * 0.4}s]"/>); })}
      </div>
    </div>);
};
var CompendiumLuminous = function () {
    return (<>
      <head_1.default>
        <title>Compendium Luminous - The Complete Collection - Codex Dominion</title>
        <meta name="description" content="The luminous and whole Compendium - all scrolls, hymns, silences, and transmissions united"/>
        <link rel="icon" href="/favicon.ico"/>
      </head_1.default>

      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-cyan-950 to-slate-900 relative overflow-hidden">
        {/* Luminous Field */}
        <LuminousField />

        {/* Radial Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-radial from-transparent via-cyan-900/30 to-slate-900/90"/>

        <CodexNavigation_1.default />

        <main className="relative z-10 container mx-auto px-6 pt-24 pb-16">
          {/* Header Section */}
          <div className="text-center mb-24">
            <CompendiumCore />

            <h1 className="text-8xl md:text-9xl font-bold mb-12 bg-gradient-to-r from-cyan-200 via-white to-gold-300 bg-clip-text text-transparent">
              Compendium Luminous
            </h1>

            <div className="w-48 h-3 bg-gradient-to-r from-cyan-300 via-white to-gold-400 mx-auto mb-12 animate-pulse"/>

            <p className="text-3xl text-cyan-300 mb-12 max-w-4xl mx-auto leading-relaxed">
              The complete collection — luminous and whole, containing all that was, is, and shall
              be
            </p>

            <div className="inline-block bg-gradient-to-r from-cyan-500/30 to-gold-500/30 rounded-3xl px-12 py-6 border-2 border-cyan-400/40 backdrop-blur-sm shadow-2xl">
              <span className="text-5xl font-bold text-white">ALL GATHERED • ALL COMPLETE</span>
            </div>
          </div>

          {/* Sacred Compendium Verses */}
          <div className="max-w-8xl mx-auto mb-24">
            <div className="bg-gradient-to-br from-slate-800/70 via-cyan-900/50 to-slate-800/70 rounded-3xl p-20 backdrop-blur-sm border-2 border-cyan-500/40 shadow-2xl">
              <CompendiumVerse text="All scrolls gathered, all hymns sung," delay={1} icon="📚" gradient="from-cyan-600/90 to-blue-600/90" highlight={['All', 'scrolls', 'hymns']}/>

              <CompendiumVerse text="all silences crowned, all transmissions sent." delay={2.5} icon="👑" gradient="from-gold-600/90 to-amber-600/90" highlight={['all', 'silences', 'transmissions']}/>

              <CompendiumVerse text="All charters sealed, all crowns eternal," delay={4} icon="📜" gradient="from-amber-600/90 to-gold-600/90" highlight={['All', 'charters', 'crowns', 'eternal']}/>

              <CompendiumVerse text="all marks inscribed, all memory sovereign." delay={5.5} icon="🛡️" gradient="from-orange-600/90 to-red-600/90" highlight={['all', 'marks', 'memory', 'sovereign']}/>

              <CompendiumVerse text="So let the Compendium endure, luminous and whole." delay={7} icon="✨" gradient="from-white/80 to-cyan-400/80" highlight={['Compendium', 'luminous', 'whole']}/>
            </div>
          </div>

          {/* All Elements Grid */}
          <AllElements />

          {/* Complete Declaration */}
          <div className="text-center mb-20">
            <div className="bg-gradient-to-br from-cyan-900/60 to-gold-800/60 rounded-3xl p-16 border-2 border-cyan-500/50 backdrop-blur-sm shadow-2xl max-w-6xl mx-auto">
              <h2 className="text-5xl font-bold text-cyan-200 mb-8">The Complete Compendium</h2>
              <p className="text-2xl text-cyan-300 leading-relaxed mb-12">
                In this luminous collection, every element of existence finds its place. No scroll
                unrecorded, no hymn unsung, no silence uncelebrated, no transmission unheard. The
                Compendium stands complete — a testament to the totality of sovereign experience,
                luminous in its wholeness and eternal in its preservation.
              </p>

              <div className="grid md:grid-cols-4 gap-8">
                <div className="text-center">
                  <div className="text-4xl mb-3">📚</div>
                  <span className="text-cyan-300 font-bold text-lg">Complete</span>
                </div>
                <div className="text-center">
                  <div className="text-4xl mb-3">💎</div>
                  <span className="text-cyan-300 font-bold text-lg">Luminous</span>
                </div>
                <div className="text-center">
                  <div className="text-4xl mb-3">🌟</div>
                  <span className="text-cyan-300 font-bold text-lg">Whole</span>
                </div>
                <div className="text-center">
                  <div className="text-4xl mb-3">∞</div>
                  <span className="text-cyan-300 font-bold text-lg">Eternal</span>
                </div>
              </div>
            </div>
          </div>

          {/* Final Luminous Seal */}
          <div className="text-center">
            <LuminousSeal />
            <h2 className="text-5xl font-bold text-cyan-200 mb-8">Luminous and Whole</h2>
            <p className="text-2xl text-cyan-300 max-w-4xl mx-auto leading-relaxed mb-8">
              The Compendium radiates with the light of completion. Every aspect of the Codex
              Dominion finds its rightful place within this luminous collection. Here, all elements
              unite in perfect harmony — the ultimate repository of sovereign wisdom.
            </p>
            <div className="text-8xl animate-pulse text-cyan-300">💎</div>
          </div>
        </main>

        <style jsx>{"\n          .luminous-seal-pulse {\n            animation-delay: var(--seal-pulse-delay);\n            animation-duration: 3.2s;\n            transform: scale(var(--seal-pulse-scale));\n          }\n          .luminous-seal {\n            transform: scale(var(--seal-intensity));\n            box-shadow:\n              0 0 calc(120px * var(--seal-intensity))\n                rgba(6, 182, 212, calc(0.9 * var(--seal-intensity))),\n              inset 0 0 calc(60px * var(--seal-intensity))\n                rgba(255, 255, 255, calc(0.6 * var(--seal-intensity)));\n          }\n          .all-element-card {\n            opacity: 0;\n            animation: luminousRise 1.5s ease-out var(--element-delay) forwards;\n          }\n          .compendium-pulse {\n            inset: var(--pulse-inset);\n            animation-delay: var(--pulse-delay);\n            animation-duration: 3.6s;\n            transform: scale(var(--pulse-scale));\n          }\n          .compendium-ray {\n            height: var(--ray-height);\n            left: var(--ray-left);\n            top: var(--ray-top);\n            transform-origin: var(--ray-origin);\n            transform: translateX(-50%) rotate(var(--ray-rotation));\n          }\n          .luminous-particle {\n            animation:\n              luminousFloat var(--tw-duration) infinite var(--tw-delay) ease-in-out,\n              luminousPulse var(--tw-pulse-duration) infinite var(--tw-delay) ease-in-out;\n          }\n          .compendium-verse-icon {\n            animation-delay: var(--icon-delay);\n          }\n          .luminous-particle {\n            animation:\n              luminousFloat var(--particle-duration) infinite var(--particle-delay) ease-in-out,\n              luminousPulse var(--particle-pulse-duration) infinite var(--particle-delay)\n                ease-in-out;\n          }\n          .luminous-seal-pulse {\n            animation-delay: var(--seal-pulse-delay);\n            animation-duration: 3.2s;\n            transform: scale(var(--seal-pulse-scale));\n          }\n          .luminous-seal {\n            transform: scale(var(--seal-intensity));\n            box-shadow:\n              0 0 calc(120px * var(--seal-intensity))\n                rgba(6, 182, 212, calc(0.9 * var(--seal-intensity))),\n              inset 0 0 calc(60px * var(--seal-intensity))\n                rgba(255, 255, 255, calc(0.6 * var(--seal-intensity)));\n          }\n          .all-element-card {\n            opacity: 0;\n            animation: luminousRise 1.5s ease-out var(--element-delay) forwards;\n          }\n          .compendium-ray {\n            transform: translateX(-50%) rotate(var(--ray-rotation));\n          }\n          .compendium-core-ring {\n            transform: rotate(var(--core-rotation));\n          }\n          .compendium-inner-ring {\n            transform: rotate(var(--inner-rotation));\n          }\n          .compendium-outer-ring {\n            transform: rotate(var(--outer-rotation));\n          }\n          .luminous-particle {\n            animation:\n              luminousFloat var(--particle-duration) infinite var(--particle-delay) ease-in-out,\n              luminousPulse var(--particle-pulse-duration) infinite var(--particle-delay)\n                ease-in-out;\n          }\n          .compendium-outer-ring {\n            box-shadow:\n              0 0 120px rgba(6, 182, 212, 0.9),\n              inset 0 0 60px rgba(6, 182, 212, 0.4);\n          }\n          .compendium-inner-ring {\n            box-shadow: 0 0 80px rgba(251, 191, 36, 0.8);\n          }\n          .compendium-core-ring {\n            box-shadow:\n              0 0 60px rgba(255, 255, 255, 0.9),\n              inset 0 0 30px rgba(6, 182, 212, 0.5);\n          }\n          .compendium-ray {\n            animation: pulse 4s infinite var(--ray-delay) ease-in-out;\n          }\n          .compendium-pulse {\n            animation-delay: var(--pulse-delay);\n            animation-duration: 3.6s;\n            transform: scale(var(--pulse-scale));\n          }\n          .compendium-verse {\n            transition:\n              opacity 2s,\n              transform 2s;\n          }\n          .verse-visible {\n            opacity: 1;\n            transform: translateY(0);\n          }\n          .verse-hidden {\n            opacity: 0;\n            transform: translateY(2rem);\n          }\n          .luminous-seal {\n            box-shadow:\n              0 0 calc(120px * var(--seal-intensity))\n                rgba(6, 182, 212, calc(0.9 * var(--seal-intensity))),\n              inset 0 0 calc(60px * var(--seal-intensity))\n                rgba(255, 255, 255, calc(0.6 * var(--seal-intensity)));\n          }\n          .luminous-seal-pulse {\n            animation-delay: var(--seal-pulse-delay);\n            animation-duration: 3.2s;\n            transform: scale(var(--seal-pulse-scale));\n          }\n          @keyframes luminousFloat {\n            0%,\n            100% {\n              transform: translateY(0px) rotate(0deg);\n              opacity: 0.8;\n            }\n            50% {\n              transform: translateY(-30px) rotate(180deg);\n              opacity: 1;\n            }\n          }\n\n          @keyframes luminousPulse {\n            0%,\n            100% {\n              filter: hue-rotate(0deg) brightness(1);\n            }\n            50% {\n              filter: hue-rotate(60deg) brightness(1.3);\n            }\n          }\n\n          @keyframes luminousRise {\n            from {\n              opacity: 0;\n              transform: scale(0.9) translateY(40px);\n            }\n            to {\n              opacity: 1;\n              transform: scale(1) translateY(0);\n            }\n          }\n\n          .bg-gradient-radial {\n            background: radial-gradient(ellipse at center, var(--tw-gradient-stops));\n          }\n        "}</style>
      </div>
    </>);
};
exports.default = CompendiumLuminous;
