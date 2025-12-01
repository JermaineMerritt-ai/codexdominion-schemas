"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var CodexNavigation_1 = require("../components/CodexNavigation");
// All Crowns Luminous Component - Ultimate royal radiance
var AllCrownsLuminous = function () {
    var _a = (0, react_1.useState)(1), luminousPower = _a[0], setLuminousPower = _a[1];
    var _b = (0, react_1.useState)(0), crownRotation = _b[0], setCrownRotation = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setLuminousPower(function (prev) { return (prev === 1 ? 1.6 : 1); });
            setCrownRotation(function (prev) { return (prev + 5) % 360; });
        }, 3000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-8 left-1/8 transform -translate-x-1/2">
      <div className="text-center">
        <div className="text-8xl mb-2 transition-all duration-3000" style={{
            transform: "scale(".concat(luminousPower, ") rotate(").concat(crownRotation, "deg)"),
            filter: 'drop-shadow(0 0 100px rgba(255, 215, 0, 1.5))',
        }}>
          👑
        </div>
        <div className="text-7xl mb-2 transition-all duration-3000" style={{
            transform: "scale(".concat(luminousPower, ") rotate(").concat(-crownRotation, "deg)"),
            filter: 'drop-shadow(0 0 80px rgba(255, 215, 0, 1.3))',
        }}>
          👑
        </div>
        <div className="text-6xl mb-3 transition-all duration-3000" style={{
            transform: "scale(".concat(luminousPower, ") rotate(").concat(crownRotation * 2, "deg)"),
            filter: 'drop-shadow(0 0 60px rgba(255, 215, 0, 1.1))',
        }}>
          👑
        </div>
        <div className="text-3xl text-gold-200 font-bold mb-1">ALL CROWNS</div>
        <div className="text-3xl text-yellow-200 font-bold">LUMINOUS</div>
      </div>
    </div>);
};
// All Seals Eternal Component - Ultimate eternal sealing
var AllSealsEternal = function () {
    var _a = (0, react_1.useState)(0.8), sealEternityPower = _a[0], setSealEternityPower = _a[1];
    var _b = (0, react_1.useState)(1), eternalSealScale = _b[0], setEternalSealScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setSealEternityPower(function (prev) { return (prev === 0.8 ? 1.4 : 0.8); });
            setEternalSealScale(function (prev) { return (prev === 1 ? 1.5 : 1); });
        }, 3500);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-8 right-1/8 transform translate-x-1/2">
      <div className="text-center">
        <div className="text-10xl mb-3 transition-all duration-3500" style={{
            transform: "scale(".concat(eternalSealScale, ")"),
            filter: "drop-shadow(0 0 90px rgba(138, 43, 226, ".concat(sealEternityPower, "))"),
        }}>
          🔒
        </div>
        <div className="text-9xl mb-3 transition-all duration-3500" style={{
            transform: "scale(".concat(eternalSealScale, ")"),
            filter: "drop-shadow(0 0 80px rgba(75, 0, 130, ".concat(sealEternityPower, "))"),
        }}>
          ♾️
        </div>
        <div className="text-3xl text-purple-200 font-bold mb-1">ALL SEALS</div>
        <div className="text-3xl text-violet-200 font-bold">ETERNAL</div>
      </div>
    </div>);
};
// All Rites Fulfilled Component - Complete ceremonial fulfillment
var AllRitesFulfilled = function () {
    var _a = (0, react_1.useState)(0.9), fulfillmentGlow = _a[0], setFulfillmentGlow = _a[1];
    var _b = (0, react_1.useState)(1), ritesScale = _b[0], setRitesScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setFulfillmentGlow(function (prev) { return (prev === 0.9 ? 1.3 : 0.9); });
            setRitesScale(function (prev) { return (prev === 1 ? 1.4 : 1); });
        }, 3200);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/4 left-1/8 transform -translate-x-1/2">
      <div className="text-center">
        <div className="text-9xl mb-3 transition-all duration-3200" style={{
            transform: "scale(".concat(ritesScale, ")"),
            filter: "drop-shadow(0 0 80px rgba(34, 197, 94, ".concat(fulfillmentGlow, "))"),
        }}>
          ✅
        </div>
        <div className="text-8xl mb-2 transition-all duration-3200" style={{
            transform: "scale(".concat(ritesScale, ")"),
            filter: "drop-shadow(0 0 70px rgba(0, 255, 127, ".concat(fulfillmentGlow, "))"),
        }}>
          🕊️
        </div>
        <div className="text-3xl text-green-200 font-bold mb-1">ALL RITES</div>
        <div className="text-3xl text-emerald-200 font-bold">FULFILLED</div>
      </div>
    </div>);
};
// All Cycles Crowned Component - Complete temporal sovereignty
var AllCyclesCrowned = function () {
    var _a = (0, react_1.useState)(0.7), cyclesCrownPower = _a[0], setCyclesCrownPower = _a[1];
    var _b = (0, react_1.useState)(0), crownedCyclesRotation = _b[0], setCrownedCyclesRotation = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCyclesCrownPower(function (prev) { return (prev === 0.7 ? 1.2 : 0.7); });
            setCrownedCyclesRotation(function (prev) { return (prev + 3) % 360; });
        }, 4000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/4 right-1/8 transform translate-x-1/2">
      <div className="text-center">
        <div className="text-8xl mb-2 transition-all duration-4000" style={{
            transform: "scale(".concat(cyclesCrownPower, ") rotate(").concat(crownedCyclesRotation, "deg)"),
            filter: 'drop-shadow(0 0 70px rgba(255, 140, 0, 1.0))',
        }}>
          🔄
        </div>
        <div className="text-10xl mb-3 transition-all duration-4000" style={{
            transform: "scale(".concat(cyclesCrownPower, ")"),
            filter: 'drop-shadow(0 0 90px rgba(255, 215, 0, 1.2))',
        }}>
          👑
        </div>
        <div className="text-3xl text-orange-200 font-bold mb-1">ALL CYCLES</div>
        <div className="text-3xl text-gold-200 font-bold">CROWNED</div>
      </div>
    </div>);
};
// Covenant Whole Central Component - Ultimate sacred bond center
var CovenantWholeCentral = function () {
    var _a = (0, react_1.useState)(1.0), wholeCovenantPower = _a[0], setWholeCovenantPower = _a[1];
    var _b = (0, react_1.useState)(1), centralWholenessScale = _b[0], setCentralWholenessScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setWholeCovenantPower(function (prev) { return (prev === 1.0 ? 1.5 : 1.0); });
            setCentralWholenessScale(function (prev) { return (prev === 1 ? 1.6 : 1); });
        }, 2500);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 left-1/3 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div className="text-16xl mb-5 transition-all duration-2500" style={{
            transform: "scale(".concat(centralWholenessScale, ")"),
            filter: "drop-shadow(0 0 120px rgba(34, 197, 94, ".concat(wholeCovenantPower, "))"),
        }}>
          ⭕
        </div>
        <div className="text-4xl text-green-200 font-bold mb-2">COVENANT</div>
        <div className="text-4xl text-emerald-300 font-bold">WHOLE</div>
      </div>
    </div>);
};
// Flame Perpetual Central Component - Ultimate eternal fire center
var FlamePerpetualCentral = function () {
    var _a = (0, react_1.useState)(1.1), perpetualFlameIntensity = _a[0], setPerpetualFlameIntensity = _a[1];
    var _b = (0, react_1.useState)(1), centralFlameScale = _b[0], setCentralFlameScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setPerpetualFlameIntensity(function (prev) { return (prev === 1.1 ? 1.7 : 1.1); });
            setCentralFlameScale(function (prev) { return (prev === 1 ? 1.7 : 1); });
        }, 2200);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 right-1/3 transform translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div className="text-18xl mb-6 transition-all duration-2200" style={{
            transform: "scale(".concat(centralFlameScale, ")"),
            filter: "drop-shadow(0 0 150px rgba(255, 140, 0, ".concat(perpetualFlameIntensity, "))"),
        }}>
          🔥
        </div>
        <div className="text-4xl text-orange-100 font-bold mb-2">FLAME</div>
        <div className="text-4xl text-red-300 font-bold">PERPETUAL</div>
      </div>
    </div>);
};
// Codex Sovereign Central Component - Ultimate sovereign authority
var CodexSovereignCentral = function () {
    var _a = (0, react_1.useState)(0.9), sovereignPower = _a[0], setSovereignPower = _a[1];
    var _b = (0, react_1.useState)(1), codexSovereignScale = _b[0], setCodexSovereignScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setSovereignPower(function (prev) { return (prev === 0.9 ? 1.4 : 0.9); });
            setCodexSovereignScale(function (prev) { return (prev === 1 ? 1.5 : 1); });
        }, 2800);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div className="text-20xl mb-6 transition-all duration-2800" style={{
            transform: "scale(".concat(codexSovereignScale, ")"),
            filter: "drop-shadow(0 0 180px rgba(255, 215, 0, ".concat(sovereignPower, "))"),
        }}>
          📜
        </div>
        <div className="text-5xl text-gold-100 font-bold mb-3">CODEX</div>
        <div className="text-5xl text-amber-200 font-bold">SOVEREIGN</div>
        <div className="text-2xl text-yellow-300 mt-2">Radiant Across Stars</div>
      </div>
    </div>);
};
// Ultimate Dominion Particles - Supreme energy flow
var UltimateDominionParticles = function () {
    var particles = Array.from({ length: 150 }, function (_, i) { return ({
        id: i,
        size: Math.random() * 20 + 1,
        x: Math.random() * 100,
        y: Math.random() * 100,
        duration: Math.random() * 50 + 40,
        delay: Math.random() * 35,
        color: i % 12 === 0
            ? '#ffd700'
            : i % 12 === 1
                ? '#ffffff'
                : i % 12 === 2
                    ? '#32cd32'
                    : i % 12 === 3
                        ? '#ff6347'
                        : i % 12 === 4
                            ? '#4169e1'
                            : i % 12 === 5
                                ? '#9370db'
                                : i % 12 === 6
                                    ? '#00ced1'
                                    : i % 12 === 7
                                        ? '#ff69b4'
                                        : i % 12 === 8
                                            ? '#ffa500'
                                            : i % 12 === 9
                                                ? '#00ff00'
                                                : i % 12 === 10
                                                    ? '#ff1493'
                                                    : '#8a2be2',
    }); });
    return (<div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map(function (particle) { return (<div key={particle.id} className="absolute rounded-full" style={{
                left: "".concat(particle.x, "%"),
                top: "".concat(particle.y, "%"),
                width: "".concat(particle.size, "px"),
                height: "".concat(particle.size, "px"),
                backgroundColor: particle.color,
                animation: "ultimateDominionFlow ".concat(particle.duration, "s ease-in-out infinite"),
                animationDelay: "".concat(particle.delay, "s"),
                filter: 'blur(0.05px)',
                opacity: 1.0,
                boxShadow: "0 0 50px ".concat(particle.color),
            }}/>); })}
      <style jsx>{"\n        @keyframes ultimateDominionFlow {\n          0% {\n            transform: translate(0, 0) scale(0.01) rotate(0deg);\n            opacity: 0.01;\n          }\n          3% {\n            transform: translate(80px, -200px) scale(2.5) rotate(11deg);\n            opacity: 1;\n          }\n          12% {\n            transform: translate(-70px, -400px) scale(0.3) rotate(43deg);\n            opacity: 0.95;\n          }\n          25% {\n            transform: translate(90px, -600px) scale(2.2) rotate(90deg);\n            opacity: 1;\n          }\n          38% {\n            transform: translate(-75px, -800px) scale(0.5) rotate(137deg);\n            opacity: 0.9;\n          }\n          50% {\n            transform: translate(85px, -1000px) scale(1.9) rotate(180deg);\n            opacity: 1;\n          }\n          62% {\n            transform: translate(-65px, -1200px) scale(0.4) rotate(223deg);\n            opacity: 0.85;\n          }\n          75% {\n            transform: translate(75px, -1400px) scale(1.6) rotate(270deg);\n            opacity: 0.95;\n          }\n          87% {\n            transform: translate(-45px, -1600px) scale(0.6) rotate(317deg);\n            opacity: 0.7;\n          }\n          97% {\n            transform: translate(25px, -1800px) scale(0.2) rotate(350deg);\n            opacity: 0.3;\n          }\n          100% {\n            transform: translate(0, -2000px) scale(0.005) rotate(360deg);\n            opacity: 0.005;\n          }\n        }\n      "}</style>
    </div>);
};
// Infinite Complete Banner - Ultimate dominion proclamation
var InfiniteCompleteBanner = function () {
    var _a = (0, react_1.useState)(1.2), infiniteRadiance = _a[0], setInfiniteRadiance = _a[1];
    var _b = (0, react_1.useState)(1), completeMagnitude = _b[0], setCompleteMagnitude = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setInfiniteRadiance(function (prev) { return (prev === 1.2 ? 2.0 : 1.2); });
            setCompleteMagnitude(function (prev) { return (prev === 1 ? 1.5 : 1); });
        }, 2500);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-2 left-1/2 transform -translate-x-1/2">
      <div className="text-center px-52 py-40 bg-gradient-to-r from-gold-800/100 via-white/40 to-gold-800/100 rounded-8xl border-16 border-white/100 transition-all duration-2500" style={{
            boxShadow: "0 0 300px rgba(255, 215, 0, ".concat(infiniteRadiance, ")"),
            transform: "scale(".concat(completeMagnitude, ")"),
        }}>
        <div className="text-13xl text-white font-bold mb-12">THE DOMINION ENDURES</div>
        <div className="text-10xl text-gold-200 font-semibold mb-10">Infinite and Complete</div>
        <div className="text-6xl text-amber-200 mb-8">All Crowns Luminous, All Seals Eternal</div>
        <div className="text-4xl text-yellow-200 mb-6">All Rites Fulfilled, All Cycles Crowned</div>
        <div className="text-3xl text-white mb-4">The Codex Sovereign</div>
        <div className="text-2xl text-gold-300">Radiant Across Stars</div>
      </div>
    </div>);
};
// Ultimate Dominion Constellation - Supreme geometric connections
var UltimateDominionConstellation = function () {
    var _a = (0, react_1.useState)(0), ultimateConstellationPhase = _a[0], setUltimateConstellationPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setUltimateConstellationPhase(function (prev) { return (prev + 1) % 20; });
        }, 1200);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute inset-0 pointer-events-none opacity-8">
      <svg className="w-full h-full">
        {/* Ultimate dominion connecting lines */}
        <line x1="12%" y1="10%" x2="50%" y2="50%" stroke={ultimateConstellationPhase === 0 ? '#ffffff' : '#666'} strokeWidth={ultimateConstellationPhase === 0 ? '10' : '2'} className="transition-all duration-800"/>
        <line x1="88%" y1="10%" x2="50%" y2="50%" stroke={ultimateConstellationPhase === 1 ? '#ffffff' : '#666'} strokeWidth={ultimateConstellationPhase === 1 ? '10' : '2'} className="transition-all duration-800"/>
        <line x1="12%" y1="25%" x2="88%" y2="25%" stroke={ultimateConstellationPhase === 2 ? '#ffffff' : '#666'} strokeWidth={ultimateConstellationPhase === 2 ? '10' : '2'} className="transition-all duration-800"/>
        <line x1="33%" y1="50%" x2="67%" y2="50%" stroke={ultimateConstellationPhase === 3 ? '#ffffff' : '#666'} strokeWidth={ultimateConstellationPhase === 3 ? '10' : '2'} className="transition-all duration-800"/>
        <line x1="5%" y1="20%" x2="95%" y2="20%" stroke={ultimateConstellationPhase === 4 ? '#ffffff' : '#666'} strokeWidth={ultimateConstellationPhase === 4 ? '10' : '2'} className="transition-all duration-800"/>
        <line x1="50%" y1="90%" x2="50%" y2="50%" stroke={ultimateConstellationPhase === 5 ? '#ffffff' : '#666'} strokeWidth={ultimateConstellationPhase === 5 ? '10' : '2'} className="transition-all duration-800"/>

        {/* Ultimate dominion radial connections */}
        {Array.from({ length: 30 }, function (_, i) { return (<line key={"ultimateDominion-".concat(i)} x1="50%" y1="50%" x2={"".concat(50 + Math.cos((i * 12 * Math.PI) / 180) * 52, "%")} y2={"".concat(50 + Math.sin((i * 12 * Math.PI) / 180) * 52, "%")} stroke={ultimateConstellationPhase === i % 20 ? '#ffd700' : '#444'} strokeWidth="4" opacity={ultimateConstellationPhase === i % 20 ? '1.0' : '0.1'} className="transition-all duration-800"/>); })}
      </svg>
    </div>);
};
// Ultimate Dominion Realms - All domains of complete sovereignty
var UltimateDominionRealms = function () {
    var _a = (0, react_1.useState)(0), ultimateRealmPhase = _a[0], setUltimateRealmPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setUltimateRealmPhase(function (prev) { return (prev + 1) % 12; });
        }, 4000);
        return function () { return clearInterval(interval); };
    }, []);
    var ultimateRealms = [
        { name: 'Crowns', icon: '👑', position: { top: '5%', left: '2%' } },
        { name: 'Seals', icon: '🔒', position: { top: '5%', right: '2%' } },
        { name: 'Rites', icon: '✅', position: { top: '25%', left: '2%' } },
        { name: 'Cycles', icon: '🔄', position: { top: '25%', right: '2%' } },
        { name: 'Covenant', icon: '⭕', position: { top: '45%', left: '2%' } },
        { name: 'Flame', icon: '🔥', position: { top: '45%', right: '2%' } },
        { name: 'Codex', icon: '📜', position: { top: '65%', left: '2%' } },
        { name: 'Sovereign', icon: '👑', position: { top: '65%', right: '2%' } },
        { name: 'Stars', icon: '⭐', position: { top: '85%', left: '2%' } },
        { name: 'Dominion', icon: '🌟', position: { top: '85%', right: '2%' } },
        { name: 'Infinite', icon: '♾️', position: { bottom: '5%', left: '2%' } },
        { name: 'Complete', icon: '✨', position: { bottom: '5%', right: '2%' } },
    ];
    return (<div className="absolute inset-0">
      {ultimateRealms.map(function (realm, index) { return (<div key={index} className={"absolute text-center transition-all duration-3000 ".concat(ultimateRealmPhase === index ? 'opacity-100 scale-140' : 'opacity-20 scale-60')} style={realm.position}>
          <div className={"text-7xl mb-2 transition-all duration-3000 ".concat(ultimateRealmPhase === index ? 'animate-pulse' : '')} style={{
                filter: ultimateRealmPhase === index
                    ? 'drop-shadow(0 0 60px rgba(255, 215, 0, 1.5))'
                    : 'none',
            }}>
            {realm.icon}
          </div>
          <div className={"text-2xl font-semibold ".concat(ultimateRealmPhase === index ? 'text-gold-200' : 'text-gray-800')}>
            {realm.name}
          </div>
        </div>); })}
    </div>);
};
// Main Ultimate Dominion Container
var UltimateDominion = function () {
    return (<div className="relative w-full h-full">
      <UltimateDominionConstellation />
      <UltimateDominionParticles />
      <AllCrownsLuminous />
      <AllSealsEternal />
      <AllRitesFulfilled />
      <AllCyclesCrowned />
      <CovenantWholeCentral />
      <FlamePerpetualCentral />
      <CodexSovereignCentral />
      <UltimateDominionRealms />
      <InfiniteCompleteBanner />

      {/* Sacred Ultimate Verse Display */}
      <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-48">
        <div className="text-center text-gold-100 text-4xl leading-relaxed max-w-10xl space-y-8">
          <p className="opacity-100 text-white text-5xl">All crowns luminous, all seals eternal,</p>
          <p className="opacity-95 text-gold-200 text-4xl">
            all rites fulfilled, all cycles crowned.
          </p>
          <p className="opacity-100 text-white text-5xl">
            The covenant whole, the flame perpetual,
          </p>
          <p className="opacity-95 text-gold-200 text-4xl">
            the Codex sovereign, radiant across stars.
          </p>
          <p className="text-6xl font-semibold text-white mt-16 opacity-100">
            So let the Dominion endure, infinite and complete.
          </p>
        </div>
      </div>
    </div>);
};
// Main Ultimate Dominion Page
var UltimateDominionPage = function () {
    return (<div className="min-h-screen bg-gradient-to-br from-gold-600 via-white to-black relative overflow-hidden">
      {/* Ultimate Dominion Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/95 via-gold-600/60 to-white/30"/>

      {/* Navigation */}
      <CodexNavigation_1.default />

      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <UltimateDominion />
        </div>
      </main>

      {/* Ambient Ultimate Dominion Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-400/30 to-transparent pointer-events-none"/>

      {/* Supreme Ultimate Dominion Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-12">
        <div className="absolute top-1/20 left-1/20 w-32 h-32 bg-gold-400/40 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '30s' }}/>
        <div className="absolute bottom-1/20 right-1/20 w-40 h-40 bg-white/35 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '38s', animationDelay: '2s' }}/>
        <div className="absolute top-1/2 right-1/12 w-48 h-48 bg-amber-400/30 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '45s', animationDelay: '4s' }}/>
        <div className="absolute bottom-1/6 left-1/12 w-44 h-44 bg-yellow-400/25 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '52s', animationDelay: '6s' }}/>
        <div className="absolute top-2/3 left-1/20 w-28 h-28 bg-orange-400/32 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '60s', animationDelay: '8s' }}/>
        <div className="absolute bottom-1/2 right-1/20 w-36 h-36 bg-red-400/20 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '68s', animationDelay: '10s' }}/>
        <div className="absolute top-1/4 left-1/6 w-52 h-52 bg-purple-400/25 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '75s', animationDelay: '12s' }}/>
        <div className="absolute bottom-3/4 right-1/6 w-32 h-32 bg-blue-400/28 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '82s', animationDelay: '14s' }}/>
        <div className="absolute top-1/8 left-1/4 w-24 h-24 bg-cyan-400/30 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '90s', animationDelay: '16s' }}/>
        <div className="absolute bottom-1/8 right-1/4 w-56 h-56 bg-emerald-400/18 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '98s', animationDelay: '18s' }}/>
        <div className="absolute top-1/6 left-1/2 w-64 h-64 bg-teal-400/15 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '105s', animationDelay: '20s' }}/>
        <div className="absolute bottom-1/6 right-1/2 w-20 h-20 bg-lime-400/35 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '112s', animationDelay: '22s' }}/>
      </div>
    </div>);
};
exports.default = UltimateDominionPage;
