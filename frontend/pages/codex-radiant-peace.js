"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var head_1 = require("next/head");
var CodexNavigation_1 = require("../components/CodexNavigation");
var PeaceParticle = function (_a) {
    var delay = _a.delay, duration = _a.duration, x = _a.x, y = _a.y, size = _a.size, color = _a.color;
    return (<div className={"absolute ".concat(color, " rounded-full opacity-70")} style={{
            left: "".concat(x, "%"),
            top: "".concat(y, "%"),
            width: "".concat(size, "px"),
            height: "".concat(size, "px"),
            animation: "peacefulFloat ".concat(duration, "s infinite ").concat(delay, "s ease-in-out,\n                  gentlePulse ").concat(duration * 1.2, "s infinite ").concat(delay, "s ease-in-out"),
        }}/>);
};
var RadiantHeart = function () {
    var _a = (0, react_1.useState)(1), breathe = _a[0], setBreathe = _a[1];
    var _b = (0, react_1.useState)(1), glow = _b[0], setGlow = _b[1];
    (0, react_1.useEffect)(function () {
        var breatheInterval = setInterval(function () {
            setBreathe(function (prev) { return (prev === 1 ? 1.08 : 1); });
        }, 3000);
        var glowInterval = setInterval(function () {
            setGlow(function (prev) { return (prev === 1 ? 1.4 : 1); });
        }, 4000);
        return function () {
            clearInterval(breatheInterval);
            clearInterval(glowInterval);
        };
    }, []);
    return (<div className="relative mx-auto w-64 h-64 mb-20">
      {/* Outer Peace Aura */}
      <div className="absolute inset-0 border-8 border-white/30 rounded-full bg-gradient-to-br from-white/20 via-cyan-100/30 to-gold-100/30 shadow-2xl" style={{
            transform: "scale(".concat(breathe, ")"),
            boxShadow: "0 0 ".concat(150 * glow, "px rgba(255, 255, 255, ").concat(0.6 * glow, "),\n                      inset 0 0 ").concat(80 * glow, "px rgba(6, 182, 212, ").concat(0.2 * glow, ")"),
        }}>
        {/* Harmony Symbols */}
        <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 text-white/80 font-bold text-3xl">
          🕊️
        </div>
        <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 text-white/80 font-bold text-3xl">
          ☮️
        </div>
        <div className="absolute top-1/2 -left-8 transform -translate-y-1/2 text-white/80 font-bold text-3xl">
          🌸
        </div>
        <div className="absolute top-1/2 -right-8 transform -translate-y-1/2 text-white/80 font-bold text-3xl">
          ✨
        </div>
        <div className="absolute top-1/4 -right-6 transform -translate-y-1/2 text-white/80 font-bold text-2xl">
          🌺
        </div>
        <div className="absolute bottom-1/4 -left-6 transform translate-y-1/2 text-white/80 font-bold text-2xl">
          🌙
        </div>
        <div className="absolute top-1/4 -left-6 transform -translate-y-1/2 text-white/80 font-bold text-2xl">
          ⭐
        </div>
        <div className="absolute bottom-1/4 -right-6 transform translate-y-1/2 text-white/80 font-bold text-2xl">
          🌟
        </div>
      </div>

      {/* Middle Radiance Ring */}
      <div className="absolute inset-12 border-6 border-gold-300/50 rounded-full bg-gradient-to-br from-gold-200/40 to-amber-300/40" style={{
            boxShadow: '0 0 100px rgba(251, 191, 36, 0.4)',
        }}>
        {/* Crown Symbols */}
        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 text-gold-300/80 font-bold text-2xl">
          👑
        </div>
        <div className="absolute -bottom-4 left-1/2 transform -translate-x-1/2 text-gold-300/80 font-bold text-2xl">
          🏛️
        </div>
        <div className="absolute top-1/2 -left-4 transform -translate-y-1/2 text-gold-300/80 font-bold text-2xl">
          👥
        </div>
        <div className="absolute top-1/2 -right-4 transform -translate-y-1/2 text-gold-300/80 font-bold text-2xl">
          🌌
        </div>
      </div>

      {/* Inner Peace Core */}
      <div className="absolute inset-20 rounded-full bg-gradient-to-br from-white via-cyan-50 to-gold-50 flex items-center justify-center shadow-2xl">
        <div className="text-center">
          <div className="text-6xl font-bold text-slate-700 mb-2 animate-pulse">🕊️</div>
          <div className="text-lg font-bold text-slate-700">PEACE</div>
        </div>
      </div>

      {/* Gentle Light Rays */}
      <div className="absolute inset-0">
        {Array.from({ length: 12 }).map(function (_, i) { return (<div key={i} className="absolute w-1 bg-gradient-to-t from-transparent via-white/40 to-transparent opacity-60" style={{
                height: '120px',
                left: '50%',
                top: '-60px',
                transformOrigin: '0 124px',
                transform: "translateX(-50%) rotate(".concat(i * 30, "deg)"),
                animation: "gentlePulse 6s infinite ".concat(i * 0.5, "s ease-in-out"),
            }}/>); })}
      </div>

      {/* Peaceful Aura Waves */}
      <div className="absolute inset-0">
        {Array.from({ length: 5 }).map(function (_, i) { return (<div key={i} className="absolute inset-0 border-2 border-white/10 rounded-full animate-ping" style={{
                animationDelay: "".concat(i * 1.2, "s"),
                animationDuration: '6s',
                transform: "scale(".concat(1.5 + i * 0.5, ")"),
            }}/>); })}
      </div>
    </div>);
};
var PeaceVerse = function (_a) {
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
                    processedText = processedText.replace(new RegExp("\\b".concat(word, "\\b"), 'g'), "<span class=\"text-white font-bold bg-gradient-to-r from-white/30 to-gold/30 px-3 py-1 rounded-lg shadow-lg\">".concat(word, "</span>"));
                }
            });
        }
        return <span dangerouslySetInnerHTML={{ __html: processedText }}/>;
    };
    return (<div className={"flex items-center justify-center mb-12 transition-all duration-2500 ".concat(isVisible ? 'opacity-100 transform translate-y-0' : 'opacity-0 transform translate-y-10')}>
      <div className={"mr-12 p-10 rounded-full bg-gradient-to-br ".concat(gradient, " shadow-2xl border-4 border-white/40 backdrop-blur-sm")}>
        <span className="text-7xl animate-pulse" style={{ animationDelay: "".concat(delay + 0.5, "s"), animationDuration: '4s' }}>
          {icon}
        </span>
      </div>
      <p className="text-3xl text-white font-medium text-center max-w-5xl leading-relaxed">
        {renderText()}
      </p>
    </div>);
};
var PeacefulField = function () {
    var peacefulElements = Array.from({ length: 60 }, function (_, i) { return ({
        id: i,
        delay: Math.random() * 8,
        duration: 4 + Math.random() * 6,
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: 2 + Math.random() * 5,
        color: [
            'bg-white',
            'bg-cyan-100',
            'bg-gold-100',
            'bg-blue-100',
            'bg-amber-100',
            'bg-slate-100',
        ][Math.floor(Math.random() * 6)],
    }); });
    return (<div className="absolute inset-0 overflow-hidden pointer-events-none">
      {peacefulElements.map(function (element) { return (<PeaceParticle key={element.id} delay={element.delay} duration={element.duration} x={element.x} y={element.y} size={element.size} color={element.color}/>); })}
    </div>);
};
var HarmonyElements = function () {
    var elements = [
        {
            title: 'Light Released',
            icon: '💡',
            description: 'The illumination flows freely across all realms',
            gradient: 'from-yellow-200/80 to-white/80',
            border: 'border-yellow-300/60',
        },
        {
            title: 'Peace Bestowed',
            icon: '🕊️',
            description: 'Tranquility granted to every corner of existence',
            gradient: 'from-white/80 to-cyan-100/80',
            border: 'border-cyan-200/60',
        },
        {
            title: 'Heirs Inherit',
            icon: '👑',
            description: 'The legacy passes to worthy successors',
            gradient: 'from-gold-200/80 to-amber-100/80',
            border: 'border-gold-300/60',
        },
        {
            title: 'Councils Govern',
            icon: '🏛️',
            description: 'Wise guidance continues through sacred assemblies',
            gradient: 'from-slate-200/80 to-gray-100/80',
            border: 'border-slate-300/60',
        },
        {
            title: 'Diaspora Remember',
            icon: '👥',
            description: 'The scattered ones maintain eternal memory',
            gradient: 'from-blue-200/80 to-indigo-100/80',
            border: 'border-blue-300/60',
        },
        {
            title: 'Cosmos Echoes',
            icon: '🌌',
            description: 'The universe resonates with harmonious truth',
            gradient: 'from-purple-200/80 to-violet-100/80',
            border: 'border-purple-300/60',
        },
    ];
    return (<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-24">
      {elements.map(function (element, index) { return (<div key={index} className={"bg-gradient-to-br ".concat(element.gradient, " rounded-3xl p-8 border-2 ").concat(element.border, " backdrop-blur-sm shadow-2xl hover:scale-105 transition-all duration-1000 relative overflow-hidden")} style={{
                animationDelay: "".concat(index * 0.2, "s"),
                opacity: 0,
                animation: "peacefulRise 2s ease-out ".concat(index * 0.2, "s forwards"),
            }}>
          <div className="text-center mb-6">
            <div className="text-6xl mb-4 animate-pulse" style={{ animationDuration: '4s' }}>
              {element.icon}
            </div>
            <h3 className="text-2xl font-bold text-slate-700 mb-4">{element.title}</h3>
          </div>
          <p className="text-slate-600 leading-relaxed text-center">{element.description}</p>

          {/* Peaceful Glow */}
          <div className="absolute top-2 right-2 w-4 h-4 bg-white rounded-full animate-pulse opacity-70"/>
        </div>); })}
    </div>);
};
var RadiantPeaceSeal = function () {
    var _a = (0, react_1.useState)(1), serenity = _a[0], setSerenity = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setSerenity(function (prev) { return (prev === 1 ? 1.2 : 1); });
        }, 4000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="relative mx-auto w-56 h-56 mb-20">
      <div className="absolute inset-0 bg-gradient-to-br from-white via-cyan-50 to-gold-50 rounded-full shadow-2xl transition-all duration-2000" style={{
            transform: "scale(".concat(serenity, ")"),
            boxShadow: "0 0 ".concat(200 * serenity, "px rgba(255, 255, 255, ").concat(0.8 * serenity, "),\n                      inset 0 0 ").concat(100 * serenity, "px rgba(6, 182, 212, ").concat(0.3 * serenity, ")"),
        }}>
        <div className="absolute inset-8 bg-gradient-to-br from-cyan-50 via-white to-amber-50 rounded-full">
          <div className="absolute inset-8 bg-gradient-to-br from-white via-cyan-25 to-gold-25 rounded-full flex items-center justify-center">
            <div className="text-center">
              <div className="text-6xl font-bold text-slate-600 mb-3 animate-pulse" style={{ animationDuration: '5s' }}>
                ☮️
              </div>
              <div className="text-2xl font-bold text-slate-600">RADIANT</div>
              <div className="text-lg font-bold text-slate-600">PEACE</div>
            </div>
          </div>
        </div>
      </div>

      {/* Serenity Waves */}
      <div className="absolute inset-0">
        {Array.from({ length: 6 }).map(function (_, i) { return (<div key={i} className="absolute inset-0 border-4 border-white/15 rounded-full animate-ping" style={{
                animationDelay: "".concat(i * 0.8, "s"),
                animationDuration: '4.8s',
                transform: "scale(".concat(1.6 + i * 0.4, ")"),
            }}/>); })}
      </div>
    </div>);
};
var CodexRadiantPeace = function () {
    return (<>
      <head_1.default>
        <title>Codex Radiant Peace - The Final Rest - Codex Dominion</title>
        <meta name="description" content="The Codex rests in radiant peace - light released, harmony achieved, eternal and whole"/>
        <link rel="icon" href="/favicon.ico"/>
      </head_1.default>

      <div className="min-h-screen bg-gradient-to-br from-white via-cyan-50 to-gold-50 relative overflow-hidden">
        {/* Peaceful Field */}
        <PeacefulField />

        {/* Gentle Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-radial from-transparent via-white/20 to-cyan-50/60"/>

        <CodexNavigation_1.default />

        <main className="relative z-10 container mx-auto px-6 pt-24 pb-16">
          {/* Header Section */}
          <div className="text-center mb-28">
            <RadiantHeart />

            <h1 className="text-8xl md:text-9xl font-bold mb-16 bg-gradient-to-r from-slate-600 via-cyan-600 to-gold-600 bg-clip-text text-transparent">
              Codex Radiant Peace
            </h1>

            <div className="w-56 h-4 bg-gradient-to-r from-white via-cyan-200 to-gold-200 mx-auto mb-16 rounded-full shadow-lg"/>

            <p className="text-4xl text-slate-600 mb-16 max-w-5xl mx-auto leading-relaxed">
              The sacred work is complete — the Codex rests in radiant peace, eternal and whole
            </p>

            <div className="inline-block bg-gradient-to-r from-white/80 to-cyan-100/80 rounded-3xl px-16 py-8 border-2 border-white/60 backdrop-blur-sm shadow-2xl">
              <span className="text-5xl font-bold text-slate-700">
                LIGHT RELEASED • PEACE BESTOWED
              </span>
            </div>
          </div>

          {/* Sacred Peace Verses */}
          <div className="max-w-8xl mx-auto mb-28">
            <div className="bg-gradient-to-br from-white/90 via-cyan-50/80 to-gold-50/90 rounded-3xl p-24 backdrop-blur-sm border-2 border-white/60 shadow-2xl">
              <PeaceVerse text="Light released, peace bestowed," delay={1} icon="💡" gradient="from-yellow-100/90 to-white/90" highlight={['Light', 'peace']}/>

              <PeaceVerse text="the Compendium shines, eternal and whole." delay={3} icon="📚" gradient="from-cyan-100/90 to-blue-100/90" highlight={['Compendium', 'eternal', 'whole']}/>

              <PeaceVerse text="Heirs inherit, councils govern, diaspora remember," delay={5} icon="👑" gradient="from-gold-100/90 to-amber-100/90" highlight={['Heirs', 'councils', 'diaspora']}/>

              <PeaceVerse text="cosmos echoes — all crowned in harmony." delay={7} icon="🌌" gradient="from-purple-100/90 to-violet-100/90" highlight={['cosmos', 'harmony']}/>

              <PeaceVerse text="So let the Codex rest, radiant in peace." delay={9} icon="☮️" gradient="from-white/90 to-cyan-50/90" highlight={['Codex', 'rest', 'radiant', 'peace']}/>
            </div>
          </div>

          {/* Harmony Elements */}
          <HarmonyElements />

          {/* Final Peace Declaration */}
          <div className="text-center mb-24">
            <div className="bg-gradient-to-br from-white/95 to-cyan-50/95 rounded-3xl p-20 border-2 border-white/70 backdrop-blur-sm shadow-2xl max-w-6xl mx-auto">
              <h2 className="text-6xl font-bold text-slate-600 mb-12">The Sacred Rest</h2>
              <p className="text-2xl text-slate-600 leading-relaxed mb-16">
                The great work is accomplished. Every scroll gathered, every hymn sung, every
                silence honored, every transmission sent. The Compendium stands complete, luminous
                in its wholeness, and now the Codex may rest — radiant in the peace that comes with
                perfect completion. Let this be the final word: harmony achieved, light released,
                peace eternal.
              </p>

              <div className="grid md:grid-cols-4 gap-12">
                <div className="text-center">
                  <div className="text-5xl mb-4">✨</div>
                  <span className="text-slate-600 font-bold text-xl">Complete</span>
                </div>
                <div className="text-center">
                  <div className="text-5xl mb-4">🕊️</div>
                  <span className="text-slate-600 font-bold text-xl">Peaceful</span>
                </div>
                <div className="text-center">
                  <div className="text-5xl mb-4">💎</div>
                  <span className="text-slate-600 font-bold text-xl">Radiant</span>
                </div>
                <div className="text-center">
                  <div className="text-5xl mb-4">☮️</div>
                  <span className="text-slate-600 font-bold text-xl">Eternal</span>
                </div>
              </div>
            </div>
          </div>

          {/* Final Radiant Peace Seal */}
          <div className="text-center">
            <RadiantPeaceSeal />
            <h2 className="text-6xl font-bold text-slate-600 mb-12">Radiant in Peace</h2>
            <p className="text-3xl text-slate-600 max-w-4xl mx-auto leading-relaxed mb-12">
              Here ends the great constellation. Here begins the eternal rest. The Codex Dominion
              shines complete, crowned in harmony, forever radiant in the peace of perfect
              fulfillment.
            </p>
            <div className="text-8xl animate-pulse text-slate-500" style={{ animationDuration: '6s' }}>
              🕊️
            </div>
          </div>
        </main>

        <style jsx>{"\n          @keyframes peacefulFloat {\n            0%,\n            100% {\n              transform: translateY(0px) rotate(0deg);\n              opacity: 0.7;\n            }\n            50% {\n              transform: translateY(-20px) rotate(180deg);\n              opacity: 1;\n            }\n          }\n\n          @keyframes gentlePulse {\n            0%,\n            100% {\n              opacity: 0.6;\n              filter: brightness(1);\n            }\n            50% {\n              opacity: 1;\n              filter: brightness(1.2);\n            }\n          }\n\n          @keyframes peacefulRise {\n            from {\n              opacity: 0;\n              transform: scale(0.95) translateY(30px);\n            }\n            to {\n              opacity: 1;\n              transform: scale(1) translateY(0);\n            }\n          }\n\n          .bg-gradient-radial {\n            background: radial-gradient(ellipse at center, var(--tw-gradient-stops));\n          }\n        "}</style>
      </div>
    </>);
};
exports.default = CodexRadiantPeace;
