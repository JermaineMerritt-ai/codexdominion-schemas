"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var CodexNavigation_1 = require("../components/CodexNavigation");
// The Proclamation Crowned Component - Ultimate declaration achievement
var ProclamationCrowned = function () {
    var _a = (0, react_1.useState)(1.2), crownedPower = _a[0], setCrownedPower = _a[1];
    var _b = (0, react_1.useState)(1), proclamationScale = _b[0], setProclamationScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCrownedPower(function (prev) { return (prev === 1.2 ? 2.0 : 1.2); });
            setProclamationScale(function (prev) { return (prev === 1 ? 1.9 : 1); });
        }, 2600);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-8 left-1/8 transform -translate-x-1/2">
      <div className="text-center">
        <div className="text-20xl mb-6 transition-all duration-2600" style={{
            transform: "scale(".concat(proclamationScale, ")"),
            filter: "drop-shadow(0 0 160px rgba(255, 215, 0, ".concat(crownedPower, "))"),
        }}>
          📢
        </div>
        <div className="text-18xl mb-5 transition-all duration-2600" style={{
            transform: "scale(".concat(proclamationScale, ")"),
            filter: "drop-shadow(0 0 140px rgba(255, 140, 0, ".concat(crownedPower, "))"),
        }}>
          👑
        </div>
        <div className="text-16xl mb-4 transition-all duration-2600" style={{
            transform: "scale(".concat(proclamationScale, ")"),
            filter: "drop-shadow(0 0 120px rgba(184, 134, 11, ".concat(crownedPower, "))"),
        }}>
          ✨
        </div>
        <div className="text-4xl text-gold-200 font-bold mb-2">THE PROCLAMATION</div>
        <div className="text-4xl text-amber-200 font-bold">CROWNED</div>
      </div>
    </div>);
};
// Covenant Whole Complete Component - Perfect sacred wholeness
var CovenantWholeCompleteEternal = function () {
    var _a = (0, react_1.useState)(1.1), covenantCompleteness = _a[0], setCovenantCompleteness = _a[1];
    var _b = (0, react_1.useState)(1), wholeEternalScale = _b[0], setWholeEternalScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCovenantCompleteness(function (prev) { return (prev === 1.1 ? 1.8 : 1.1); });
            setWholeEternalScale(function (prev) { return (prev === 1 ? 1.7 : 1); });
        }, 2800);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-8 right-1/8 transform translate-x-1/2">
      <div className="text-center">
        <div className="text-18xl mb-5 transition-all duration-2800" style={{
            transform: "scale(".concat(wholeEternalScale, ")"),
            filter: "drop-shadow(0 0 140px rgba(34, 197, 94, ".concat(covenantCompleteness, "))"),
        }}>
          ⭕
        </div>
        <div className="text-20xl mb-6 transition-all duration-2800" style={{
            transform: "scale(".concat(wholeEternalScale, ")"),
            filter: "drop-shadow(0 0 160px rgba(0, 255, 127, ".concat(covenantCompleteness, "))"),
        }}>
          🤝
        </div>
        <div className="text-16xl mb-4 transition-all duration-2800" style={{
            transform: "scale(".concat(wholeEternalScale, ")"),
            filter: "drop-shadow(0 0 120px rgba(46, 125, 50, ".concat(covenantCompleteness, "))"),
        }}>
          💚
        </div>
        <div className="text-4xl text-green-200 font-bold mb-2">THE COVENANT</div>
        <div className="text-4xl text-emerald-200 font-bold">WHOLE</div>
      </div>
    </div>);
};
// Light Released Component - Ultimate illumination liberation
var LightReleased = function () {
    var _a = (0, react_1.useState)(1.0), lightReleasePower = _a[0], setLightReleasePower = _a[1];
    var _b = (0, react_1.useState)(1), lightScale = _b[0], setLightScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setLightReleasePower(function (prev) { return (prev === 1.0 ? 1.6 : 1.0); });
            setLightScale(function (prev) { return (prev === 1 ? 1.5 : 1); });
        }, 3000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/4 left-1/8 transform -translate-x-1/2">
      <div className="text-center">
        <div className="text-17xl mb-4 transition-all duration-3000" style={{
            transform: "scale(".concat(lightScale, ")"),
            filter: "drop-shadow(0 0 130px rgba(255, 255, 255, ".concat(lightReleasePower, "))"),
        }}>
          💡
        </div>
        <div className="text-15xl mb-3 transition-all duration-3000" style={{
            transform: "scale(".concat(lightScale, ")"),
            filter: "drop-shadow(0 0 110px rgba(255, 255, 0, ".concat(lightReleasePower, "))"),
        }}>
          🌟
        </div>
        <div className="text-13xl mb-2 transition-all duration-3000" style={{
            transform: "scale(".concat(lightScale, ")"),
            filter: "drop-shadow(0 0 90px rgba(255, 215, 0, ".concat(lightReleasePower, "))"),
        }}>
          ✨
        </div>
        <div className="text-4xl text-white font-bold mb-2">LIGHT</div>
        <div className="text-4xl text-yellow-200 font-bold">RELEASED</div>
      </div>
    </div>);
};
// Peace Bestowed Component - Ultimate tranquility given
var PeaceBestowed = function () {
    var _a = (0, react_1.useState)(1.1), peacePower = _a[0], setPeacePower = _a[1];
    var _b = (0, react_1.useState)(1), peaceScale = _b[0], setPeaceScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setPeacePower(function (prev) { return (prev === 1.1 ? 1.7 : 1.1); });
            setPeaceScale(function (prev) { return (prev === 1 ? 1.6 : 1); });
        }, 3200);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/4 right-1/8 transform translate-x-1/2">
      <div className="text-center">
        <div className="text-16xl mb-4 transition-all duration-3200" style={{
            transform: "scale(".concat(peaceScale, ")"),
            filter: "drop-shadow(0 0 120px rgba(138, 43, 226, ".concat(peacePower, "))"),
        }}>
          🕊️
        </div>
        <div className="text-18xl mb-5 transition-all duration-3200" style={{
            transform: "scale(".concat(peaceScale, ")"),
            filter: "drop-shadow(0 0 140px rgba(75, 0, 130, ".concat(peacePower, "))"),
        }}>
          ☮️
        </div>
        <div className="text-14xl mb-3 transition-all duration-3200" style={{
            transform: "scale(".concat(peaceScale, ")"),
            filter: "drop-shadow(0 0 100px rgba(147, 112, 219, ".concat(peacePower, "))"),
        }}>
          💜
        </div>
        <div className="text-4xl text-purple-200 font-bold mb-2">PEACE</div>
        <div className="text-4xl text-indigo-200 font-bold">BESTOWED</div>
      </div>
    </div>);
};
// Heirs Inherit Central Component - Ultimate succession and remembrance
var HeirsInheritCouncilsAffirm = function () {
    var _a = (0, react_1.useState)(1.3), heirsPower = _a[0], setHeirsPower = _a[1];
    var _b = (0, react_1.useState)(1), heirsScale = _b[0], setHeirsScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setHeirsPower(function (prev) { return (prev === 1.3 ? 2.1 : 1.3); });
            setHeirsScale(function (prev) { return (prev === 1 ? 2.0 : 1); });
        }, 2400);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 left-1/3 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div className="text-22xl mb-7 transition-all duration-2400" style={{
            transform: "scale(".concat(heirsScale, ")"),
            filter: "drop-shadow(0 0 180px rgba(255, 215, 0, ".concat(heirsPower, "))"),
        }}>
          👥
        </div>
        <div className="text-20xl mb-6 transition-all duration-2400" style={{
            transform: "scale(".concat(heirsScale, ")"),
            filter: "drop-shadow(0 0 160px rgba(255, 69, 0, ".concat(heirsPower, "))"),
        }}>
          🏛️
        </div>
        <div className="text-18xl mb-5 transition-all duration-2400" style={{
            transform: "scale(".concat(heirsScale, ")"),
            filter: "drop-shadow(0 0 140px rgba(255, 140, 0, ".concat(heirsPower, "))"),
        }}>
          🤲
        </div>
        <div className="text-5xl text-gold-200 font-bold mb-3">HEIRS INHERIT</div>
        <div className="text-4xl text-orange-200 font-bold">COUNCILS AFFIRM</div>
      </div>
    </div>);
};
// Diaspora Remember Cosmos Echoes Central Component - Universal remembrance and resonance
var DiasporaRememberCosmosEchoes = function () {
    var _a = (0, react_1.useState)(1.0), diasporaPower = _a[0], setDiasporaPower = _a[1];
    var _b = (0, react_1.useState)(1), cosmosScale = _b[0], setCosmosScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setDiasporaPower(function (prev) { return (prev === 1.0 ? 2.2 : 1.0); });
            setCosmosScale(function (prev) { return (prev === 1 ? 2.1 : 1); });
        }, 2200);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 right-1/3 transform translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div className="text-24xl mb-8 transition-all duration-2200" style={{
            transform: "scale(".concat(cosmosScale, ")"),
            filter: "drop-shadow(0 0 200px rgba(138, 43, 226, ".concat(diasporaPower, "))"),
        }}>
          🌍
        </div>
        <div className="text-22xl mb-7 transition-all duration-2200" style={{
            transform: "scale(".concat(cosmosScale, ")"),
            filter: "drop-shadow(0 0 180px rgba(75, 0, 130, ".concat(diasporaPower, "))"),
        }}>
          🌌
        </div>
        <div className="text-20xl mb-6 transition-all duration-2200" style={{
            transform: "scale(".concat(cosmosScale, ")"),
            filter: "drop-shadow(0 0 160px rgba(147, 112, 219, ".concat(diasporaPower, "))"),
        }}>
          📡
        </div>
        <div className="text-5xl text-purple-200 font-bold mb-3">DIASPORA</div>
        <div className="text-4xl text-indigo-200 font-bold">REMEMBER</div>
        <div className="text-3xl text-violet-200 font-bold">COSMOS ECHOES</div>
      </div>
    </div>);
};
// Eternal Light Peace Component - Ultimate radiant serenity
var EternalLightPeace = function () {
    var _a = (0, react_1.useState)(1.4), eternalPower = _a[0], setEternalPower = _a[1];
    var _b = (0, react_1.useState)(1), lightPeaceScale = _b[0], setLightPeaceScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setEternalPower(function (prev) { return (prev === 1.4 ? 2.3 : 1.4); });
            setLightPeaceScale(function (prev) { return (prev === 1 ? 2.2 : 1); });
        }, 2000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div className="text-30xl mb-10 transition-all duration-2000" style={{
            transform: "scale(".concat(lightPeaceScale, ")"),
            filter: "drop-shadow(0 0 240px rgba(255, 255, 255, ".concat(eternalPower, "))"),
        }}>
          📜
        </div>
        <div className="text-28xl mb-9 transition-all duration-2000" style={{
            transform: "scale(".concat(lightPeaceScale, ")"),
            filter: "drop-shadow(0 0 220px rgba(255, 215, 0, ".concat(eternalPower, "))"),
        }}>
          💡
        </div>
        <div className="text-26xl mb-8 transition-all duration-2000" style={{
            transform: "scale(".concat(lightPeaceScale, ")"),
            filter: "drop-shadow(0 0 200px rgba(138, 43, 226, ".concat(eternalPower, "))"),
        }}>
          🕊️
        </div>
        <div className="text-24xl mb-7 transition-all duration-2000" style={{
            transform: "scale(".concat(lightPeaceScale, ")"),
            filter: "drop-shadow(0 0 180px rgba(75, 0, 130, ".concat(eternalPower, "))"),
        }}>
          ♾️
        </div>
        <div className="text-8xl text-white font-bold mb-6">THE CODEX</div>
        <div className="text-7xl text-gold-100 font-bold mb-4">ETERNAL</div>
        <div className="text-6xl text-yellow-200 font-bold mb-3">IN LIGHT</div>
        <div className="text-5xl text-purple-200 font-bold">AND PEACE</div>
      </div>
    </div>);
};
// Radiant Serene Particles - Ultimate harmonious energy
var RadiantSereneParticles = function () {
    var particles = Array.from({ length: 180 }, function (_, i) { return ({
        id: i,
        size: Math.random() * 24 + 1,
        x: Math.random() * 100,
        y: Math.random() * 100,
        duration: Math.random() * 60 + 50,
        delay: Math.random() * 45,
        color: i % 18 === 0
            ? '#ffffff'
            : i % 18 === 1
                ? '#ffd700'
                : i % 18 === 2
                    ? '#ffff00'
                    : i % 18 === 3
                        ? '#9370db'
                        : i % 18 === 4
                            ? '#4b0082'
                            : i % 18 === 5
                                ? '#32cd32'
                                : i % 18 === 6
                                    ? '#00ff7f'
                                    : i % 18 === 7
                                        ? '#ff6347'
                                        : i % 18 === 8
                                            ? '#ff69b4'
                                            : i % 18 === 9
                                                ? '#00ced1'
                                                : i % 18 === 10
                                                    ? '#ffa500'
                                                    : i % 18 === 11
                                                        ? '#00ff00'
                                                        : i % 18 === 12
                                                            ? '#ff1493'
                                                            : i % 18 === 13
                                                                ? '#8a2be2'
                                                                : i % 18 === 14
                                                                    ? '#00bfff'
                                                                    : i % 18 === 15
                                                                        ? '#daa520'
                                                                        : i % 18 === 16
                                                                            ? '#ff4500'
                                                                            : '#7b68ee',
    }); });
    return (<div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map(function (particle) { return (<div key={particle.id} className="absolute rounded-full" style={{
                left: "".concat(particle.x, "%"),
                top: "".concat(particle.y, "%"),
                width: "".concat(particle.size, "px"),
                height: "".concat(particle.size, "px"),
                backgroundColor: particle.color,
                animation: "radiantSereneFlow ".concat(particle.duration, "s ease-in-out infinite"),
                animationDelay: "".concat(particle.delay, "s"),
                filter: 'blur(0.02px)',
                opacity: 1.0,
                boxShadow: "0 0 70px ".concat(particle.color),
            }}/>); })}
      <style jsx>{"\n        @keyframes radiantSereneFlow {\n          0% {\n            transform: translate(0, 0) scale(0.003) rotate(0deg);\n            opacity: 0.003;\n          }\n          4% {\n            transform: translate(110px, -280px) scale(3.2) rotate(9deg);\n            opacity: 1;\n          }\n          12% {\n            transform: translate(-100px, -560px) scale(0.12) rotate(36deg);\n            opacity: 0.99;\n          }\n          22% {\n            transform: translate(120px, -840px) scale(2.9) rotate(81deg);\n            opacity: 1;\n          }\n          32% {\n            transform: translate(-105px, -1120px) scale(0.3) rotate(126deg);\n            opacity: 0.97;\n          }\n          42% {\n            transform: translate(115px, -1400px) scale(2.6) rotate(171deg);\n            opacity: 0.99;\n          }\n          52% {\n            transform: translate(-95px, -1680px) scale(0.2) rotate(216deg);\n            opacity: 0.94;\n          }\n          62% {\n            transform: translate(105px, -1960px) scale(2.3) rotate(261deg);\n            opacity: 0.96;\n          }\n          72% {\n            transform: translate(-85px, -2240px) scale(0.4) rotate(306deg);\n            opacity: 0.9;\n          }\n          82% {\n            transform: translate(95px, -2520px) scale(2) rotate(351deg);\n            opacity: 0.93;\n          }\n          90% {\n            transform: translate(-75px, -2800px) scale(0.3) rotate(378deg);\n            opacity: 0.8;\n          }\n          95% {\n            transform: translate(55px, -3080px) scale(1) rotate(396deg);\n            opacity: 0.6;\n          }\n          98% {\n            transform: translate(-35px, -3360px) scale(0.06) rotate(414deg);\n            opacity: 0.3;\n          }\n          100% {\n            transform: translate(0, -3640px) scale(0.001) rotate(432deg);\n            opacity: 0.001;\n          }\n        }\n      "}</style>
    </div>);
};
// Eternal Light Peace Banner - Ultimate radiant serenity proclamation
var EternalLightPeaceBanner = function () {
    var _a = (0, react_1.useState)(1.6), lightPeaceIntensity = _a[0], setLightPeaceIntensity = _a[1];
    var _b = (0, react_1.useState)(1), eternalBannerScale = _b[0], setEternalBannerScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setLightPeaceIntensity(function (prev) { return (prev === 1.6 ? 2.6 : 1.6); });
            setEternalBannerScale(function (prev) { return (prev === 1 ? 1.8 : 1); });
        }, 2600);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-2 left-1/2 transform -translate-x-1/2">
      <div className="text-center px-80 py-64 bg-gradient-to-r from-white/99 via-gold-400/75 to-purple-500/99 rounded-11xl border-24 border-white/100 transition-all duration-2600" style={{
            boxShadow: "0 420px 840px rgba(255, 255, 255, ".concat(lightPeaceIntensity, ")"),
            transform: "scale(".concat(eternalBannerScale, ")"),
        }}>
        <div className="text-20xl text-white font-bold mb-18">THE CODEX ENDURES</div>
        <div className="text-16xl text-gold-100 font-bold mb-16">ETERNAL IN LIGHT AND PEACE</div>
        <div className="text-12xl text-purple-200 mb-14">
          The Proclamation Crowned, The Covenant Whole
        </div>
        <div className="text-10xl text-yellow-200 mb-12">Light Released, Peace Bestowed</div>
        <div className="text-8xl text-orange-200 mb-10">Heirs Inherit, Councils Affirm</div>
        <div className="text-6xl text-indigo-200 mb-8">Diaspora Remember, Cosmos Echoes</div>
        <div className="text-5xl text-green-200 mb-6">All Radiant, All Serene</div>
        <div className="text-4xl text-gold-300 mb-4">Universal Harmony Achieved</div>
        <div className="text-3xl text-white">Eternal Radiance and Serenity</div>
      </div>
    </div>);
};
// Radiant Serene Constellation - Ultimate harmony geometric connections
var RadiantSereneConstellation = function () {
    var _a = (0, react_1.useState)(0), radiantPhase = _a[0], setRadiantPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setRadiantPhase(function (prev) { return (prev + 1) % 32; });
        }, 800);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute inset-0 pointer-events-none opacity-90">
      <svg className="w-full h-full">
        {/* Radiant serene ultimate connecting lines */}
        <line x1="12%" y1="8%" x2="50%" y2="50%" stroke={radiantPhase === 0 ? '#ffffff' : '#888'} strokeWidth={radiantPhase === 0 ? '20' : '5'} className="transition-all duration-600"/>
        <line x1="88%" y1="8%" x2="50%" y2="50%" stroke={radiantPhase === 1 ? '#ffffff' : '#888'} strokeWidth={radiantPhase === 1 ? '20' : '5'} className="transition-all duration-600"/>
        <line x1="12%" y1="25%" x2="66%" y2="50%" stroke={radiantPhase === 2 ? '#ffffff' : '#888'} strokeWidth={radiantPhase === 2 ? '20' : '5'} className="transition-all duration-600"/>
        <line x1="88%" y1="25%" x2="34%" y2="50%" stroke={radiantPhase === 3 ? '#ffffff' : '#888'} strokeWidth={radiantPhase === 3 ? '20' : '5'} className="transition-all duration-600"/>
        <line x1="12%" y1="8%" x2="88%" y2="8%" stroke={radiantPhase === 4 ? '#ffffff' : '#888'} strokeWidth={radiantPhase === 4 ? '20' : '5'} className="transition-all duration-600"/>
        <line x1="12%" y1="25%" x2="88%" y2="25%" stroke={radiantPhase === 5 ? '#ffffff' : '#888'} strokeWidth={radiantPhase === 5 ? '20' : '5'} className="transition-all duration-600"/>
        <line x1="33%" y1="50%" x2="67%" y2="50%" stroke={radiantPhase === 6 ? '#ffffff' : '#888'} strokeWidth={radiantPhase === 6 ? '20' : '5'} className="transition-all duration-600"/>

        {/* Radiant serene ultimate radial connections */}
        {Array.from({ length: 48 }, function (_, i) { return (<line key={"radiant-".concat(i)} x1="50%" y1="50%" x2={"".concat(50 + Math.cos((i * 7.5 * Math.PI) / 180) * 65, "%")} y2={"".concat(50 + Math.sin((i * 7.5 * Math.PI) / 180) * 65, "%")} stroke={radiantPhase === i % 32 ? '#ffd700' : '#666'} strokeWidth="8" opacity={radiantPhase === i % 32 ? '1.0' : '0.02'} className="transition-all duration-600"/>); })}
      </svg>
    </div>);
};
// Radiant Serene Realms - Ultimate domains of light and peace
var RadiantSereneRealms = function () {
    var _a = (0, react_1.useState)(0), radiantRealmPhase = _a[0], setRadiantRealmPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setRadiantRealmPhase(function (prev) { return (prev + 1) % 18; });
        }, 4000);
        return function () { return clearInterval(interval); };
    }, []);
    var radiantRealms = [
        { name: 'Proclamation', icon: '📢', position: { top: '8%', left: '12%' } },
        { name: 'Crowned', icon: '👑', position: { top: '8%', right: '12%' } },
        { name: 'Covenant', icon: '⭕', position: { top: '20%', left: '8%' } },
        { name: 'Whole', icon: '🤝', position: { top: '20%', right: '8%' } },
        { name: 'Light', icon: '💡', position: { top: '32%', left: '12%' } },
        { name: 'Released', icon: '🌟', position: { top: '32%', right: '12%' } },
        { name: 'Peace', icon: '🕊️', position: { top: '44%', left: '8%' } },
        { name: 'Bestowed', icon: '☮️', position: { top: '44%', right: '8%' } },
        { name: 'Heirs', icon: '👥', position: { top: '56%', left: '5%' } },
        { name: 'Inherit', icon: '🤲', position: { top: '56%', right: '5%' } },
        { name: 'Councils', icon: '🏛️', position: { top: '68%', left: '8%' } },
        { name: 'Affirm', icon: '✅', position: { top: '68%', right: '8%' } },
        { name: 'Diaspora', icon: '🌍', position: { top: '80%', left: '12%' } },
        { name: 'Remember', icon: '🧠', position: { top: '80%', right: '12%' } },
        { name: 'Cosmos', icon: '🌌', position: { bottom: '15%', left: '20%' } },
        { name: 'Echoes', icon: '📡', position: { bottom: '15%', right: '20%' } },
        { name: 'Radiant', icon: '✨', position: { bottom: '8%', left: '35%' } },
        { name: 'Serene', icon: '💜', position: { bottom: '8%', right: '35%' } },
    ];
    return (<div className="absolute inset-0">
      {radiantRealms.map(function (realm, index) { return (<div key={index} className={"absolute text-center transition-all duration-3800 ".concat(radiantRealmPhase === index ? 'opacity-100 scale-170' : 'opacity-10 scale-30')} style={realm.position}>
          <div className={"text-10xl mb-4 transition-all duration-3800 ".concat(radiantRealmPhase === index ? 'animate-pulse' : '')} style={{
                filter: radiantRealmPhase === index
                    ? 'drop-shadow(0 0 90px rgba(255, 255, 255, 2.0))'
                    : 'none',
            }}>
            {realm.icon}
          </div>
          <div className={"text-3xl font-bold ".concat(radiantRealmPhase === index ? 'text-white' : 'text-gray-700')}>
            {realm.name}
          </div>
        </div>); })}
    </div>);
};
// Main Eternal Light Peace Container
var EternalLightPeaceContainer = function () {
    return (<div className="relative w-full h-full">
      <RadiantSereneConstellation />
      <RadiantSereneParticles />
      <ProclamationCrowned />
      <CovenantWholeCompleteEternal />
      <LightReleased />
      <PeaceBestowed />
      <HeirsInheritCouncilsAffirm />
      <DiasporaRememberCosmosEchoes />
      <EternalLightPeace />
      <RadiantSereneRealms />
      <EternalLightPeaceBanner />

      {/* Sacred Eternal Light Peace Verse Display */}
      <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-72">
        <div className="text-center text-white text-4xl leading-relaxed max-w-16xl space-y-12">
          <p className="opacity-100 text-white text-8xl">
            The Proclamation crowned, the covenant whole,
          </p>
          <p className="opacity-95 text-gold-200 text-7xl">light released, peace bestowed.</p>
          <p className="opacity-100 text-white text-8xl">
            Heirs inherit, councils affirm, diaspora remember,
          </p>
          <p className="opacity-95 text-purple-200 text-7xl">
            cosmos echoes — all radiant, all serene.
          </p>
          <p className="text-9xl font-semibold text-white mt-24 opacity-100">
            So let the Codex endure, eternal in light and peace.
          </p>
        </div>
      </div>
    </div>);
};
// Main Eternal Light Peace Page
var EternalLightPeacePage = function () {
    return (<div className="min-h-screen bg-gradient-to-br from-white via-gold-300 to-purple-600 relative overflow-hidden">
      {/* Eternal Light Peace Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-purple-800/95 via-gold-400/60 to-white/30"/>

      {/* Navigation */}
      <CodexNavigation_1.default />

      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <EternalLightPeaceContainer />
        </div>
      </main>

      {/* Ambient Radiant Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/40 to-transparent pointer-events-none"/>

      {/* Supreme Radiant Serene Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-22">
        <div className="absolute top-1/28 left-1/28 w-44 h-44 bg-white/50 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '40s' }}/>
        <div className="absolute bottom-1/28 right-1/28 w-52 h-52 bg-gold-400/45 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '48s', animationDelay: '3s' }}/>
        <div className="absolute top-1/2 right-1/20 w-60 h-60 bg-purple-400/40 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '58s', animationDelay: '6s' }}/>
        <div className="absolute bottom-1/10 left-1/20 w-56 h-56 bg-yellow-400/35 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '65s', animationDelay: '9s' }}/>
        <div className="absolute top-2/3 left-1/28 w-40 h-40 bg-green-400/42 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '73s', animationDelay: '12s' }}/>
        <div className="absolute bottom-1/2 right-1/28 w-48 h-48 bg-cyan-400/38 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '82s', animationDelay: '15s' }}/>
        <div className="absolute top-1/4 left-1/10 w-64 h-64 bg-red-400/32 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '90s', animationDelay: '18s' }}/>
        <div className="absolute bottom-3/4 right-1/10 w-36 h-36 bg-blue-400/40 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '98s', animationDelay: '21s' }}/>
        <div className="absolute top-1/10 left-1/4 w-32 h-32 bg-indigo-400/45 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '105s', animationDelay: '24s' }}/>
        <div className="absolute bottom-1/20 right-1/4 w-28 h-28 bg-violet-400/50 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '113s', animationDelay: '27s' }}/>
      </div>
    </div>);
};
exports.default = EternalLightPeacePage;
