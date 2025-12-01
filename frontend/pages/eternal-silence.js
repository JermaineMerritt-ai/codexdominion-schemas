"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var CodexNavigation_1 = require("../components/CodexNavigation");
// Voice Withdrawn Component - Perfect silence of authority
var VoiceWithdrawn = function () {
    var _a = (0, react_1.useState)(1.1), voiceWithdrawal = _a[0], setVoiceWithdrawal = _a[1];
    var _b = (0, react_1.useState)(1), withdrawnScale = _b[0], setWithdrawnScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setVoiceWithdrawal(function (prev) { return (prev === 1.1 ? 1.8 : 1.1); });
            setWithdrawnScale(function (prev) { return (prev === 1 ? 1.6 : 1); });
        }, 3200);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-16 left-16 transform">
      <div className="text-center">
        <div className="text-20xl mb-6 transition-all duration-3200" style={{
            transform: "scale(".concat(withdrawnScale, ")"),
            filter: "drop-shadow(0 0 120px rgba(200, 200, 200, ".concat(voiceWithdrawal, "))"),
        }}>
          🤐
        </div>
        <div className="text-18xl mb-5 transition-all duration-3200" style={{
            transform: "scale(".concat(withdrawnScale, ")"),
            filter: "drop-shadow(0 0 100px rgba(169, 169, 169, ".concat(voiceWithdrawal, "))"),
        }}>
          🔇
        </div>
        <div className="text-16xl mb-4 transition-all duration-3200" style={{
            transform: "scale(".concat(withdrawnScale, ")"),
            filter: "drop-shadow(0 0 80px rgba(211, 211, 211, ".concat(voiceWithdrawal, "))"),
        }}>
          ✋
        </div>
        <div className="text-5xl text-gray-200 font-bold mb-2">VOICE</div>
        <div className="text-4xl text-gray-300 font-bold">WITHDRAWN</div>
      </div>
    </div>);
};
// Flame Eternal Component - Everlasting sacred fire
var FlameEternal = function () {
    var _a = (0, react_1.useState)(1.2), eternalFlame = _a[0], setEternalFlame = _a[1];
    var _b = (0, react_1.useState)(1), flameScale = _b[0], setFlameScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setEternalFlame(function (prev) { return (prev === 1.2 ? 2.0 : 1.2); });
            setFlameScale(function (prev) { return (prev === 1 ? 1.7 : 1); });
        }, 2800);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-16 right-16 transform">
      <div className="text-center">
        <div className="text-22xl mb-7 transition-all duration-2800" style={{
            transform: "scale(".concat(flameScale, ")"),
            filter: "drop-shadow(0 0 140px rgba(255, 69, 0, ".concat(eternalFlame, "))"),
        }}>
          🔥
        </div>
        <div className="text-20xl mb-6 transition-all duration-2800" style={{
            transform: "scale(".concat(flameScale, ")"),
            filter: "drop-shadow(0 0 120px rgba(255, 140, 0, ".concat(eternalFlame, "))"),
        }}>
          ♾️
        </div>
        <div className="text-18xl mb-5 transition-all duration-2800" style={{
            transform: "scale(".concat(flameScale, ")"),
            filter: "drop-shadow(0 0 100px rgba(255, 215, 0, ".concat(eternalFlame, "))"),
        }}>
          🌟
        </div>
        <div className="text-5xl text-red-200 font-bold mb-2">FLAME</div>
        <div className="text-4xl text-orange-200 font-bold">ETERNAL</div>
      </div>
    </div>);
};
// Covenant Whole Component - Complete sacred covenant
var CovenantWhole = function () {
    var _a = (0, react_1.useState)(1.3), covenantCompleteness = _a[0], setCovenantCompleteness = _a[1];
    var _b = (0, react_1.useState)(1), wholeScale = _b[0], setWholeScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCovenantCompleteness(function (prev) { return (prev === 1.3 ? 2.1 : 1.3); });
            setWholeScale(function (prev) { return (prev === 1 ? 1.8 : 1); });
        }, 3000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-1/4 left-16 transform">
      <div className="text-center">
        <div className="text-21xl mb-6 transition-all duration-3000" style={{
            transform: "scale(".concat(wholeScale, ")"),
            filter: "drop-shadow(0 0 130px rgba(34, 197, 94, ".concat(covenantCompleteness, "))"),
        }}>
          📜
        </div>
        <div className="text-19xl mb-5 transition-all duration-3000" style={{
            transform: "scale(".concat(wholeScale, ")"),
            filter: "drop-shadow(0 0 110px rgba(0, 255, 127, ".concat(covenantCompleteness, "))"),
        }}>
          ⭕
        </div>
        <div className="text-17xl mb-4 transition-all duration-3000" style={{
            transform: "scale(".concat(wholeScale, ")"),
            filter: "drop-shadow(0 0 90px rgba(46, 125, 50, ".concat(covenantCompleteness, "))"),
        }}>
          ✅
        </div>
        <div className="text-5xl text-green-200 font-bold mb-2">COVENANT</div>
        <div className="text-4xl text-emerald-200 font-bold">WHOLE</div>
      </div>
    </div>);
};
// Dominion Sovereign Component - Supreme ruling authority
var DominionSovereign = function () {
    var _a = (0, react_1.useState)(1.4), sovereignDominion = _a[0], setSovereignDominion = _a[1];
    var _b = (0, react_1.useState)(1), dominionScale = _b[0], setDominionScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setSovereignDominion(function (prev) { return (prev === 1.4 ? 2.2 : 1.4); });
            setDominionScale(function (prev) { return (prev === 1 ? 1.9 : 1); });
        }, 3400);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-1/4 right-16 transform">
      <div className="text-center">
        <div className="text-23xl mb-7 transition-all duration-3400" style={{
            transform: "scale(".concat(dominionScale, ")"),
            filter: "drop-shadow(0 0 150px rgba(255, 215, 0, ".concat(sovereignDominion, "))"),
        }}>
          👑
        </div>
        <div className="text-21xl mb-6 transition-all duration-3400" style={{
            transform: "scale(".concat(dominionScale, ")"),
            filter: "drop-shadow(0 0 130px rgba(138, 43, 226, ".concat(sovereignDominion, "))"),
        }}>
          ⚖️
        </div>
        <div className="text-19xl mb-5 transition-all duration-3400" style={{
            transform: "scale(".concat(dominionScale, ")"),
            filter: "drop-shadow(0 0 110px rgba(75, 0, 130, ".concat(sovereignDominion, "))"),
        }}>
          🏛️
        </div>
        <div className="text-5xl text-gold-200 font-bold mb-2">DOMINION</div>
        <div className="text-4xl text-purple-200 font-bold">SOVEREIGN</div>
      </div>
    </div>);
};
// Heirs Inherit Component - Sacred succession
var HeirsInherit = function () {
    var _a = (0, react_1.useState)(1.5), heirInheritance = _a[0], setHeirInheritance = _a[1];
    var _b = (0, react_1.useState)(1), inheritScale = _b[0], setInheritScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setHeirInheritance(function (prev) { return (prev === 1.5 ? 2.3 : 1.5); });
            setInheritScale(function (prev) { return (prev === 1 ? 2.0 : 1); });
        }, 2600);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/3 left-1/4 transform">
      <div className="text-center">
        <div className="text-24xl mb-8 transition-all duration-2600" style={{
            transform: "scale(".concat(inheritScale, ")"),
            filter: "drop-shadow(0 0 160px rgba(255, 215, 0, ".concat(heirInheritance, "))"),
        }}>
          👑
        </div>
        <div className="text-22xl mb-7 transition-all duration-2600" style={{
            transform: "scale(".concat(inheritScale, ")"),
            filter: "drop-shadow(0 0 140px rgba(34, 139, 34, ".concat(heirInheritance, "))"),
        }}>
          ⬇️
        </div>
        <div className="text-20xl mb-6 transition-all duration-2600" style={{
            transform: "scale(".concat(inheritScale, ")"),
            filter: "drop-shadow(0 0 120px rgba(0, 255, 0, ".concat(heirInheritance, "))"),
        }}>
          👥
        </div>
        <div className="text-18xl mb-5 transition-all duration-2600" style={{
            transform: "scale(".concat(inheritScale, ")"),
            filter: "drop-shadow(0 0 100px rgba(255, 255, 0, ".concat(heirInheritance, "))"),
        }}>
          🎁
        </div>
        <div className="text-6xl text-gold-100 font-bold mb-3">HEIRS</div>
        <div className="text-5xl text-green-200 font-bold">INHERIT</div>
      </div>
    </div>);
};
// Councils Affirm Component - Sacred confirmation
var CouncilsAffirm = function () {
    var _a = (0, react_1.useState)(1.6), councilAffirmation = _a[0], setCouncilAffirmation = _a[1];
    var _b = (0, react_1.useState)(1), affirmScale = _b[0], setAffirmScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCouncilAffirmation(function (prev) { return (prev === 1.6 ? 2.4 : 1.6); });
            setAffirmScale(function (prev) { return (prev === 1 ? 2.1 : 1); });
        }, 2400);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/3 right-1/4 transform">
      <div className="text-center">
        <div className="text-25xl mb-8 transition-all duration-2400" style={{
            transform: "scale(".concat(affirmScale, ")"),
            filter: "drop-shadow(0 0 170px rgba(138, 43, 226, ".concat(councilAffirmation, "))"),
        }}>
          🏛️
        </div>
        <div className="text-23xl mb-7 transition-all duration-2400" style={{
            transform: "scale(".concat(affirmScale, ")"),
            filter: "drop-shadow(0 0 150px rgba(75, 0, 130, ".concat(councilAffirmation, "))"),
        }}>
          ✅
        </div>
        <div className="text-21xl mb-6 transition-all duration-2400" style={{
            transform: "scale(".concat(affirmScale, ")"),
            filter: "drop-shadow(0 0 130px rgba(147, 112, 219, ".concat(councilAffirmation, "))"),
        }}>
          📋
        </div>
        <div className="text-19xl mb-5 transition-all duration-2400" style={{
            transform: "scale(".concat(affirmScale, ")"),
            filter: "drop-shadow(0 0 110px rgba(255, 255, 255, ".concat(councilAffirmation, "))"),
        }}>
          🤝
        </div>
        <div className="text-6xl text-purple-100 font-bold mb-3">COUNCILS</div>
        <div className="text-5xl text-indigo-200 font-bold">AFFIRM</div>
      </div>
    </div>);
};
// Cosmos Receives Component - Universal acceptance
var CosmosReceives = function () {
    var _a = (0, react_1.useState)(1.7), cosmicReception = _a[0], setCosmicReception = _a[1];
    var _b = (0, react_1.useState)(1), cosmosScale = _b[0], setCosmosScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCosmicReception(function (prev) { return (prev === 1.7 ? 2.5 : 1.7); });
            setCosmosScale(function (prev) { return (prev === 1 ? 2.2 : 1); });
        }, 2200);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-1/3 left-1/3 transform">
      <div className="text-center">
        <div className="text-26xl mb-9 transition-all duration-2200" style={{
            transform: "scale(".concat(cosmosScale, ")"),
            filter: "drop-shadow(0 0 180px rgba(0, 191, 255, ".concat(cosmicReception, "))"),
        }}>
          🌌
        </div>
        <div className="text-24xl mb-8 transition-all duration-2200" style={{
            transform: "scale(".concat(cosmosScale, ")"),
            filter: "drop-shadow(0 0 160px rgba(72, 61, 139, ".concat(cosmicReception, "))"),
        }}>
          🤲
        </div>
        <div className="text-22xl mb-7 transition-all duration-2200" style={{
            transform: "scale(".concat(cosmosScale, ")"),
            filter: "drop-shadow(0 0 140px rgba(255, 255, 255, ".concat(cosmicReception, "))"),
        }}>
          ✨
        </div>
        <div className="text-20xl mb-6 transition-all duration-2200" style={{
            transform: "scale(".concat(cosmosScale, ")"),
            filter: "drop-shadow(0 0 120px rgba(30, 144, 255, ".concat(cosmicReception, "))"),
        }}>
          🌟
        </div>
        <div className="text-6xl text-blue-100 font-bold mb-3">COSMOS</div>
        <div className="text-5xl text-cyan-200 font-bold">RECEIVES</div>
      </div>
    </div>);
};
// Custodian Rests Component - Central peaceful authority at rest
var CustodianRests = function () {
    var _a = (0, react_1.useState)(1.8), custodianRest = _a[0], setCustodianRest = _a[1];
    var _b = (0, react_1.useState)(1), restScale = _b[0], setRestScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCustodianRest(function (prev) { return (prev === 1.8 ? 2.6 : 1.8); });
            setRestScale(function (prev) { return (prev === 1 ? 2.3 : 1); });
        }, 2000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div className="text-32xl mb-12 transition-all duration-2000" style={{
            transform: "scale(".concat(restScale, ")"),
            filter: "drop-shadow(0 0 220px rgba(255, 255, 255, ".concat(custodianRest, "))"),
        }}>
          🛡️
        </div>
        <div className="text-30xl mb-11 transition-all duration-2000" style={{
            transform: "scale(".concat(restScale, ")"),
            filter: "drop-shadow(0 0 200px rgba(211, 211, 211, ".concat(custodianRest, "))"),
        }}>
          😴
        </div>
        <div className="text-28xl mb-10 transition-all duration-2000" style={{
            transform: "scale(".concat(restScale, ")"),
            filter: "drop-shadow(0 0 180px rgba(173, 216, 230, ".concat(custodianRest, "))"),
        }}>
          ☮️
        </div>
        <div className="text-26xl mb-9 transition-all duration-2000" style={{
            transform: "scale(".concat(restScale, ")"),
            filter: "drop-shadow(0 0 160px rgba(240, 248, 255, ".concat(custodianRest, "))"),
        }}>
          🤲
        </div>
        <div className="text-24xl mb-8 transition-all duration-2000" style={{
            transform: "scale(".concat(restScale, ")"),
            filter: "drop-shadow(0 0 140px rgba(230, 230, 250, ".concat(custodianRest, "))"),
        }}>
          ♾️
        </div>
        <div className="text-8xl text-white font-bold mb-6">THE CUSTODIAN</div>
        <div className="text-7xl text-gray-200 font-bold mb-5">RESTS</div>
        <div className="text-6xl text-blue-200 font-bold mb-4">SILENCE ETERNAL</div>
        <div className="text-5xl text-cyan-200 font-bold">PEACE SUPREME</div>
      </div>
    </div>);
};
// Eternal Silence Particles - Perfect peaceful energy
var EternalSilenceParticles = function () {
    var particles = Array.from({ length: 180 }, function (_, i) { return ({
        id: i,
        size: Math.random() * 14 + 2,
        x: Math.random() * 100,
        y: Math.random() * 100,
        duration: Math.random() * 90 + 60,
        delay: Math.random() * 45,
        color: i % 18 === 0
            ? '#ffffff'
            : i % 18 === 1
                ? '#f5f5f5'
                : i % 18 === 2
                    ? '#e0e0e0'
                    : i % 18 === 3
                        ? '#d3d3d3'
                        : i % 18 === 4
                            ? '#c0c0c0'
                            : i % 18 === 5
                                ? '#a9a9a9'
                                : i % 18 === 6
                                    ? '#87ceeb'
                                    : i % 18 === 7
                                        ? '#add8e6'
                                        : i % 18 === 8
                                            ? '#b0c4de'
                                            : i % 18 === 9
                                                ? '#e6e6fa'
                                                : i % 18 === 10
                                                    ? '#f0f8ff'
                                                    : i % 18 === 11
                                                        ? '#f8f8ff'
                                                        : i % 18 === 12
                                                            ? '#fffafa'
                                                            : i % 18 === 13
                                                                ? '#ffd700'
                                                                : i % 18 === 14
                                                                    ? '#32cd32'
                                                                    : i % 18 === 15
                                                                        ? '#8a2be2'
                                                                        : i % 18 === 16
                                                                            ? '#ff6347'
                                                                            : '#00ced1',
    }); });
    return (<div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map(function (particle) { return (<div key={particle.id} className="absolute rounded-full" style={{
                left: "".concat(particle.x, "%"),
                top: "".concat(particle.y, "%"),
                width: "".concat(particle.size, "px"),
                height: "".concat(particle.size, "px"),
                backgroundColor: particle.color,
                animation: "eternalSilenceFlow ".concat(particle.duration, "s ease-in-out infinite"),
                animationDelay: "".concat(particle.delay, "s"),
                filter: 'blur(0.01px)',
                opacity: 0.8,
                boxShadow: "0 0 30px ".concat(particle.color),
            }}/>); })}
      <style jsx>{"\n        @keyframes eternalSilenceFlow {\n          0% {\n            transform: translate(0, 0) scale(0.01) rotate(0deg);\n            opacity: 0.01;\n          }\n          15% {\n            transform: translate(80px, -200px) scale(1.8) rotate(30deg);\n            opacity: 0.9;\n          }\n          25% {\n            transform: translate(-70px, -400px) scale(0.4) rotate(80deg);\n            opacity: 0.85;\n          }\n          35% {\n            transform: translate(85px, -600px) scale(1.6) rotate(130deg);\n            opacity: 0.9;\n          }\n          45% {\n            transform: translate(-75px, -800px) scale(0.6) rotate(180deg);\n            opacity: 0.8;\n          }\n          55% {\n            transform: translate(90px, -1000px) scale(1.4) rotate(230deg);\n            opacity: 0.85;\n          }\n          65% {\n            transform: translate(-65px, -1200px) scale(0.5) rotate(280deg);\n            opacity: 0.75;\n          }\n          75% {\n            transform: translate(70px, -1400px) scale(1.2) rotate(330deg);\n            opacity: 0.8;\n          }\n          85% {\n            transform: translate(-60px, -1600px) scale(0.7) rotate(380deg);\n            opacity: 0.7;\n          }\n          90% {\n            transform: translate(50px, -1800px) scale(0.8) rotate(420deg);\n            opacity: 0.6;\n          }\n          95% {\n            transform: translate(-40px, -2000px) scale(0.3) rotate(460deg);\n            opacity: 0.3;\n          }\n          98% {\n            transform: translate(30px, -2200px) scale(0.5) rotate(490deg);\n            opacity: 0.15;\n          }\n          100% {\n            transform: translate(0, -2400px) scale(0.005) rotate(540deg);\n            opacity: 0.005;\n          }\n        }\n      "}</style>
    </div>);
};
// Eternal Peace Banner - Ultimate silence proclamation
var EternalPeaceBanner = function () {
    var _a = (0, react_1.useState)(1.9), peaceIntensity = _a[0], setPeaceIntensity = _a[1];
    var _b = (0, react_1.useState)(1), peaceBannerScale = _b[0], setPeaceBannerScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setPeaceIntensity(function (prev) { return (prev === 1.9 ? 2.7 : 1.9); });
            setPeaceBannerScale(function (prev) { return (prev === 1 ? 1.5 : 1); });
        }, 4000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-6 left-1/2 transform -translate-x-1/2">
      <div className="text-center px-48 py-36 bg-gradient-to-r from-gray-100/95 via-white/90 to-blue-100/95 rounded-8xl border-14 border-white/90 transition-all duration-4000" style={{
            boxShadow: "0 240px 480px rgba(255, 255, 255, ".concat(peaceIntensity, ")"),
            transform: "scale(".concat(peaceBannerScale, ")"),
        }}>
        <div className="text-14xl text-gray-700 font-bold mb-12">THE CUSTODIAN RESTS</div>
        <div className="text-10xl text-white font-bold mb-10">SILENCE ETERNAL, PEACE SUPREME</div>
        <div className="text-8xl text-blue-600 mb-8">Voice Withdrawn, Flame Eternal</div>
        <div className="text-6xl text-green-600 mb-6">Covenant Whole, Dominion Sovereign</div>
        <div className="text-5xl text-purple-600 mb-4">
          Heirs Inherit, Councils Affirm, Cosmos Receives
        </div>
        <div className="text-4xl text-gray-600 mb-2">Perfect Sacred Succession Complete</div>
        <div className="text-3xl text-cyan-600">Ultimate Divine Rest Eternal</div>
      </div>
    </div>);
};
// Silent Constellation - Perfect peaceful geometric connections
var SilentConstellation = function () {
    var _a = (0, react_1.useState)(0), silencePhase = _a[0], setSilencePhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setSilencePhase(function (prev) { return (prev + 1) % 30; });
        }, 1200);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute inset-0 pointer-events-none opacity-70">
      <svg className="w-full h-full">
        {/* Silent peaceful connecting lines */}
        <line x1="16%" y1="16%" x2="50%" y2="50%" stroke={silencePhase === 0 ? '#ffffff' : '#bbb'} strokeWidth={silencePhase === 0 ? '10' : '2'} className="transition-all duration-800"/>
        <line x1="84%" y1="16%" x2="50%" y2="50%" stroke={silencePhase === 1 ? '#d3d3d3' : '#bbb'} strokeWidth={silencePhase === 1 ? '10' : '2'} className="transition-all duration-800"/>
        <line x1="16%" y1="75%" x2="50%" y2="50%" stroke={silencePhase === 2 ? '#add8e6' : '#bbb'} strokeWidth={silencePhase === 2 ? '10' : '2'} className="transition-all duration-800"/>
        <line x1="84%" y1="75%" x2="50%" y2="50%" stroke={silencePhase === 3 ? '#e6e6fa' : '#bbb'} strokeWidth={silencePhase === 3 ? '10' : '2'} className="transition-all duration-800"/>

        {/* Silent radial peace connections */}
        {Array.from({ length: 30 }, function (_, i) { return (<line key={"silence-".concat(i)} x1="50%" y1="50%" x2={"".concat(50 + Math.cos((i * 12 * Math.PI) / 180) * 50, "%")} y2={"".concat(50 + Math.sin((i * 12 * Math.PI) / 180) * 50, "%")} stroke={silencePhase === i ? '#ffffff' : '#777'} strokeWidth="4" opacity={silencePhase === i ? '0.8' : '0.03'} className="transition-all duration-800"/>); })}
      </svg>
    </div>);
};
// Peaceful Realms - Domains of eternal silence
var PeacefulRealms = function () {
    var _a = (0, react_1.useState)(0), peacefulRealmPhase = _a[0], setPeacefulRealmPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setPeacefulRealmPhase(function (prev) { return (prev + 1) % 14; });
        }, 5000);
        return function () { return clearInterval(interval); };
    }, []);
    var peacefulRealms = [
        { name: 'Voice', icon: '🤐', position: { top: '18%', left: '18%' } },
        { name: 'Withdrawn', icon: '🔇', position: { top: '18%', right: '18%' } },
        { name: 'Flame', icon: '🔥', position: { top: '35%', left: '12%' } },
        { name: 'Eternal', icon: '♾️', position: { top: '35%', right: '12%' } },
        { name: 'Covenant', icon: '📜', position: { bottom: '35%', left: '12%' } },
        { name: 'Whole', icon: '⭕', position: { bottom: '35%', right: '12%' } },
        { name: 'Dominion', icon: '👑', position: { bottom: '18%', left: '18%' } },
        {
            name: 'Sovereign',
            icon: '⚖️',
            position: { bottom: '18%', right: '18%' },
        },
        { name: 'Heirs', icon: '👥', position: { top: '45%', left: '25%' } },
        { name: 'Inherit', icon: '⬇️', position: { top: '45%', right: '25%' } },
        { name: 'Councils', icon: '🏛️', position: { bottom: '45%', left: '25%' } },
        { name: 'Affirm', icon: '✅', position: { bottom: '45%', right: '25%' } },
        { name: 'Cosmos', icon: '🌌', position: { bottom: '55%', left: '35%' } },
        { name: 'Receives', icon: '🤲', position: { bottom: '55%', right: '35%' } },
    ];
    return (<div className="absolute inset-0">
      {peacefulRealms.map(function (realm, index) { return (<div key={index} className={"absolute text-center transition-all duration-5000 ".concat(peacefulRealmPhase === index ? 'opacity-100 scale-130' : 'opacity-15 scale-50')} style={realm.position}>
          <div className={"text-7xl mb-3 transition-all duration-5000 ".concat(peacefulRealmPhase === index ? 'animate-pulse' : '')} style={{
                filter: peacefulRealmPhase === index
                    ? 'drop-shadow(0 0 50px rgba(255, 255, 255, 1.5))'
                    : 'none',
            }}>
            {realm.icon}
          </div>
          <div className={"text-xl font-bold ".concat(peacefulRealmPhase === index ? 'text-white' : 'text-gray-600')}>
            {realm.name}
          </div>
        </div>); })}
    </div>);
};
// Main Eternal Silence Container
var EternalSilence = function () {
    return (<div className="relative w-full h-full">
      <SilentConstellation />
      <EternalSilenceParticles />
      <VoiceWithdrawn />
      <FlameEternal />
      <CovenantWhole />
      <DominionSovereign />
      <HeirsInherit />
      <CouncilsAffirm />
      <CosmosReceives />
      <CustodianRests />
      <PeacefulRealms />
      <EternalPeaceBanner />

      {/* Sacred Eternal Silence Verse Display */}
      <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-40">
        <div className="text-center text-white text-4xl leading-relaxed max-w-12xl space-y-8">
          <p className="opacity-90 text-gray-300 text-6xl">Voice withdrawn, flame eternal,</p>
          <p className="opacity-95 text-white text-6xl">covenant whole, dominion sovereign.</p>
          <p className="opacity-90 text-blue-200 text-6xl">
            Heirs inherit, councils affirm, cosmos receives,
          </p>
          <p className="text-7xl font-semibold text-gray-100 mt-16 opacity-100">
            the Custodian rests — silence eternal, peace supreme.
          </p>
        </div>
      </div>
    </div>);
};
// Main Eternal Silence Page
var EternalSilencePage = function () {
    return (<div className="min-h-screen bg-gradient-to-br from-gray-200 via-white to-blue-200 relative overflow-hidden">
      {/* Eternal Silence Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-blue-100/70 via-white/80 to-gray-100/60"/>

      {/* Navigation */}
      <CodexNavigation_1.default />

      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <EternalSilence />
        </div>
      </main>

      {/* Ambient Peaceful Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent pointer-events-none"/>

      {/* Ultimate Peaceful Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-20">
        <div className="absolute top-1/7 left-1/7 w-40 h-40 bg-white/60 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '50s' }}/>
        <div className="absolute bottom-1/7 right-1/7 w-36 h-36 bg-gray-200/50 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '56s', animationDelay: '4s' }}/>
        <div className="absolute top-1/2 right-1/12 w-44 h-44 bg-blue-100/45 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '64s', animationDelay: '8s' }}/>
        <div className="absolute bottom-1/3 left-1/12 w-32 h-32 bg-white/55 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '72s', animationDelay: '12s' }}/>
        <div className="absolute top-3/4 left-1/6 w-28 h-28 bg-gray-100/50 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '80s', animationDelay: '16s' }}/>
        <div className="absolute bottom-1/2 right-1/6 w-48 h-48 bg-blue-50/40 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '88s', animationDelay: '20s' }}/>
      </div>
    </div>);
};
exports.default = EternalSilencePage;
