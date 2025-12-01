"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var CodexNavigation_1 = require("../components/CodexNavigation");
// All Scrolls Gathered Component - Complete manuscript collection
var AllScrollsGathered = function () {
    var _a = (0, react_1.useState)(1), scrollsPower = _a[0], setScrollsPower = _a[1];
    var _b = (0, react_1.useState)(0), gatheredRotation = _b[0], setGatheredRotation = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setScrollsPower(function (prev) { return (prev === 1 ? 1.7 : 1); });
            setGatheredRotation(function (prev) { return (prev + 4) % 360; });
        }, 2800);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-8 left-1/8 transform -translate-x-1/2">
      <div className="text-center">
        <div className="text-16xl mb-4 transition-all duration-2800" style={{
            transform: "scale(".concat(scrollsPower, ")"),
            filter: 'drop-shadow(0 0 120px rgba(255, 215, 0, 1.5))',
        }}>
          📜
        </div>
        <div className="text-14xl mb-3 transition-all duration-2800" style={{
            transform: "scale(".concat(scrollsPower, ") rotate(").concat(gatheredRotation, "deg)"),
            filter: 'drop-shadow(0 0 100px rgba(139, 69, 19, 1.3))',
        }}>
          📋
        </div>
        <div className="text-12xl mb-2 transition-all duration-2800" style={{
            transform: "scale(".concat(scrollsPower, ")"),
            filter: 'drop-shadow(0 0 80px rgba(184, 134, 11, 1.1))',
        }}>
          📃
        </div>
        <div className="text-4xl text-gold-200 font-bold mb-2">ALL SCROLLS</div>
        <div className="text-4xl text-amber-200 font-bold">GATHERED</div>
      </div>
    </div>);
};
// All Crowns Luminous Component - Complete royal radiance
var AllCrownsLuminousComplete = function () {
    var _a = (0, react_1.useState)(0.9), crownLuminosity = _a[0], setCrownLuminosity = _a[1];
    var _b = (0, react_1.useState)(1), luminousScale = _b[0], setLuminousScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCrownLuminosity(function (prev) { return (prev === 0.9 ? 1.6 : 0.9); });
            setLuminousScale(function (prev) { return (prev === 1 ? 1.8 : 1); });
        }, 3000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-8 right-1/8 transform translate-x-1/2">
      <div className="text-center">
        <div className="text-18xl mb-4 transition-all duration-3000" style={{
            transform: "scale(".concat(luminousScale, ")"),
            filter: "drop-shadow(0 0 140px rgba(255, 215, 0, ".concat(crownLuminosity, "))"),
        }}>
          👑
        </div>
        <div className="text-16xl mb-3 transition-all duration-3000" style={{
            transform: "scale(".concat(luminousScale, ")"),
            filter: "drop-shadow(0 0 120px rgba(255, 140, 0, ".concat(crownLuminosity, "))"),
        }}>
          👑
        </div>
        <div className="text-14xl mb-2 transition-all duration-3000" style={{
            transform: "scale(".concat(luminousScale, ")"),
            filter: "drop-shadow(0 0 100px rgba(255, 69, 0, ".concat(crownLuminosity, "))"),
        }}>
          👑
        </div>
        <div className="text-4xl text-gold-200 font-bold mb-2">ALL CROWNS</div>
        <div className="text-4xl text-orange-200 font-bold">LUMINOUS</div>
      </div>
    </div>);
};
// All Rites Fulfilled Component - Complete ceremonial achievement
var AllRitesFulfilledComplete = function () {
    var _a = (0, react_1.useState)(1.0), ritesFulfillment = _a[0], setRitesFulfillment = _a[1];
    var _b = (0, react_1.useState)(1), ritualScale = _b[0], setRitualScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setRitesFulfillment(function (prev) { return (prev === 1.0 ? 1.5 : 1.0); });
            setRitualScale(function (prev) { return (prev === 1 ? 1.6 : 1); });
        }, 3200);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/4 left-1/8 transform -translate-x-1/2">
      <div className="text-center">
        <div className="text-15xl mb-3 transition-all duration-3200" style={{
            transform: "scale(".concat(ritualScale, ")"),
            filter: "drop-shadow(0 0 110px rgba(34, 197, 94, ".concat(ritesFulfillment, "))"),
        }}>
          ✅
        </div>
        <div className="text-13xl mb-2 transition-all duration-3200" style={{
            transform: "scale(".concat(ritualScale, ")"),
            filter: "drop-shadow(0 0 90px rgba(0, 255, 127, ".concat(ritesFulfillment, "))"),
        }}>
          🕊️
        </div>
        <div className="text-4xl text-green-200 font-bold mb-2">ALL RITES</div>
        <div className="text-4xl text-emerald-200 font-bold">FULFILLED</div>
      </div>
    </div>);
};
// All Concord Eternal Component - Perfect harmony forever
var AllConcordEternal = function () {
    var _a = (0, react_1.useState)(0.8), concordPower = _a[0], setConcordPower = _a[1];
    var _b = (0, react_1.useState)(1), eternalHarmonyScale = _b[0], setEternalHarmonyScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setConcordPower(function (prev) { return (prev === 0.8 ? 1.4 : 0.8); });
            setEternalHarmonyScale(function (prev) { return (prev === 1 ? 1.7 : 1); });
        }, 2600);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/4 right-1/8 transform translate-x-1/2">
      <div className="text-center">
        <div className="text-14xl mb-3 transition-all duration-2600" style={{
            transform: "scale(".concat(eternalHarmonyScale, ")"),
            filter: "drop-shadow(0 0 100px rgba(138, 43, 226, ".concat(concordPower, "))"),
        }}>
          🤝
        </div>
        <div className="text-16xl mb-4 transition-all duration-2600" style={{
            transform: "scale(".concat(eternalHarmonyScale, ")"),
            filter: "drop-shadow(0 0 120px rgba(75, 0, 130, ".concat(concordPower, "))"),
        }}>
          ♾️
        </div>
        <div className="text-4xl text-purple-200 font-bold mb-2">ALL CONCORD</div>
        <div className="text-4xl text-indigo-200 font-bold">ETERNAL</div>
      </div>
    </div>);
};
// Covenant Whole Flame Central Component - Complete sacred bond center
var CovenantWholeFlamePeretualCentral = function () {
    var _a = (0, react_1.useState)(1.1), covenantFlamePower = _a[0], setCovenantFlamePower = _a[1];
    var _b = (0, react_1.useState)(1), centralWholenessScale = _b[0], setCentralWholenessScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCovenantFlamePower(function (prev) { return (prev === 1.1 ? 1.9 : 1.1); });
            setCentralWholenessScale(function (prev) { return (prev === 1 ? 1.8 : 1); });
        }, 2200);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 left-1/3 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div className="text-18xl mb-5 transition-all duration-2200" style={{
            transform: "scale(".concat(centralWholenessScale, ")"),
            filter: "drop-shadow(0 0 140px rgba(34, 197, 94, ".concat(covenantFlamePower, "))"),
        }}>
          ⭕
        </div>
        <div className="text-20xl mb-6 transition-all duration-2200" style={{
            transform: "scale(".concat(centralWholenessScale, ")"),
            filter: "drop-shadow(0 0 160px rgba(255, 69, 0, ".concat(covenantFlamePower, "))"),
        }}>
          🔥
        </div>
        <div className="text-5xl text-green-200 font-bold mb-3">COVENANT WHOLE</div>
        <div className="text-5xl text-red-200 font-bold">FLAME PERPETUAL</div>
      </div>
    </div>);
};
// Codex Sovereign Radiant Central Component - Ultimate authority across stars
var CodexSovereignRadiantCentral = function () {
    var _a = (0, react_1.useState)(1.0), codexSovereignPower = _a[0], setCodexSovereignPower = _a[1];
    var _b = (0, react_1.useState)(1), radiantStarsScale = _b[0], setRadiantStarsScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCodexSovereignPower(function (prev) { return (prev === 1.0 ? 2.0 : 1.0); });
            setRadiantStarsScale(function (prev) { return (prev === 1 ? 2.0 : 1); });
        }, 2000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 right-1/3 transform translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div className="text-24xl mb-7 transition-all duration-2000" style={{
            transform: "scale(".concat(radiantStarsScale, ")"),
            filter: "drop-shadow(0 0 200px rgba(255, 215, 0, ".concat(codexSovereignPower, "))"),
        }}>
          📜
        </div>
        <div className="text-22xl mb-6 transition-all duration-2000" style={{
            transform: "scale(".concat(radiantStarsScale, ")"),
            filter: "drop-shadow(0 0 180px rgba(255, 255, 255, ".concat(codexSovereignPower, "))"),
        }}>
          ⭐
        </div>
        <div className="text-6xl text-gold-100 font-bold mb-4">CODEX SOVEREIGN</div>
        <div className="text-5xl text-white font-bold">RADIANT ACROSS STARS</div>
      </div>
    </div>);
};
// Compendium Infinite Complete Component - Ultimate repository eternal
var CompendiumInfiniteComplete = function () {
    var _a = (0, react_1.useState)(1.2), compendiumPower = _a[0], setCompendiumPower = _a[1];
    var _b = (0, react_1.useState)(1), infiniteCompleteScale = _b[0], setInfiniteCompleteScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCompendiumPower(function (prev) { return (prev === 1.2 ? 2.1 : 1.2); });
            setInfiniteCompleteScale(function (prev) { return (prev === 1 ? 1.9 : 1); });
        }, 1800);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div className="text-28xl mb-8 transition-all duration-1800" style={{
            transform: "scale(".concat(infiniteCompleteScale, ")"),
            filter: "drop-shadow(0 0 220px rgba(255, 215, 0, ".concat(compendiumPower, "))"),
        }}>
          📖
        </div>
        <div className="text-26xl mb-7 transition-all duration-1800" style={{
            transform: "scale(".concat(infiniteCompleteScale, ")"),
            filter: "drop-shadow(0 0 200px rgba(138, 43, 226, ".concat(compendiumPower, "))"),
        }}>
          ♾️
        </div>
        <div className="text-7xl text-gold-100 font-bold mb-5">THE COMPENDIUM</div>
        <div className="text-6xl text-purple-200 font-bold mb-3">INFINITE</div>
        <div className="text-5xl text-amber-200 font-bold">COMPLETE</div>
      </div>
    </div>);
};
// Compendium Complete Particles - Ultimate repository energy
var CompendiumCompleteParticles = function () {
    var particles = Array.from({ length: 140 }, function (_, i) { return ({
        id: i,
        size: Math.random() * 20 + 1,
        x: Math.random() * 100,
        y: Math.random() * 100,
        duration: Math.random() * 50 + 40,
        delay: Math.random() * 35,
        color: i % 14 === 0
            ? '#ffd700'
            : i % 14 === 1
                ? '#ffffff'
                : i % 14 === 2
                    ? '#32cd32'
                    : i % 14 === 3
                        ? '#ff6347'
                        : i % 14 === 4
                            ? '#4169e1'
                            : i % 14 === 5
                                ? '#9370db'
                                : i % 14 === 6
                                    ? '#00ced1'
                                    : i % 14 === 7
                                        ? '#ff69b4'
                                        : i % 14 === 8
                                            ? '#ffa500'
                                            : i % 14 === 9
                                                ? '#00ff00'
                                                : i % 14 === 10
                                                    ? '#ff1493'
                                                    : i % 14 === 11
                                                        ? '#8a2be2'
                                                        : i % 14 === 12
                                                            ? '#00bfff'
                                                            : '#daa520',
    }); });
    return (<div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map(function (particle) { return (<div key={particle.id} className="absolute rounded-full" style={{
                left: "".concat(particle.x, "%"),
                top: "".concat(particle.y, "%"),
                width: "".concat(particle.size, "px"),
                height: "".concat(particle.size, "px"),
                backgroundColor: particle.color,
                animation: "compendiumCompleteFlow ".concat(particle.duration, "s ease-in-out infinite"),
                animationDelay: "".concat(particle.delay, "s"),
                filter: 'blur(0.04px)',
                opacity: 1.0,
                boxShadow: "0 0 50px ".concat(particle.color),
            }}/>); })}
      <style jsx>{"\n        @keyframes compendiumCompleteFlow {\n          0% {\n            transform: translate(0, 0) scale(0.005) rotate(0deg);\n            opacity: 0.005;\n          }\n          2% {\n            transform: translate(90px, -220px) scale(2.8) rotate(7deg);\n            opacity: 1;\n          }\n          8% {\n            transform: translate(-80px, -440px) scale(0.2) rotate(29deg);\n            opacity: 0.95;\n          }\n          18% {\n            transform: translate(100px, -660px) scale(2.5) rotate(65deg);\n            opacity: 1;\n          }\n          28% {\n            transform: translate(-85px, -880px) scale(0.4) rotate(101deg);\n            opacity: 0.9;\n          }\n          38% {\n            transform: translate(95px, -1100px) scale(2.2) rotate(137deg);\n            opacity: 0.95;\n          }\n          48% {\n            transform: translate(-75px, -1320px) scale(0.3) rotate(173deg);\n            opacity: 0.85;\n          }\n          58% {\n            transform: translate(85px, -1540px) scale(1.9) rotate(209deg);\n            opacity: 0.9;\n          }\n          68% {\n            transform: translate(-65px, -1760px) scale(0.5) rotate(245deg);\n            opacity: 0.8;\n          }\n          78% {\n            transform: translate(75px, -1980px) scale(1.6) rotate(281deg);\n            opacity: 0.85;\n          }\n          88% {\n            transform: translate(-55px, -2200px) scale(0.4) rotate(317deg);\n            opacity: 0.7;\n          }\n          95% {\n            transform: translate(35px, -2420px) scale(0.8) rotate(342deg);\n            opacity: 0.5;\n          }\n          98% {\n            transform: translate(-15px, -2640px) scale(0.1) rotate(356deg);\n            opacity: 0.2;\n          }\n          100% {\n            transform: translate(0, -2860px) scale(0.001) rotate(360deg);\n            opacity: 0.001;\n          }\n        }\n      "}</style>
    </div>);
};
// Infinite Complete Banner - Ultimate compendium proclamation
var InfiniteCompleteBanner = function () {
    var _a = (0, react_1.useState)(1.4), infiniteIntensity = _a[0], setInfiniteIntensity = _a[1];
    var _b = (0, react_1.useState)(1), completeBannerScale = _b[0], setCompleteBannerScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setInfiniteIntensity(function (prev) { return (prev === 1.4 ? 2.2 : 1.4); });
            setCompleteBannerScale(function (prev) { return (prev === 1 ? 1.6 : 1); });
        }, 2200);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-2 left-1/2 transform -translate-x-1/2">
      <div className="text-center px-64 py-48 bg-gradient-to-r from-gold-500/95 via-white/65 to-purple-600/95 rounded-9xl border-18 border-gold-200/100 transition-all duration-2200" style={{
            boxShadow: "0 0 350px rgba(255, 215, 0, ".concat(infiniteIntensity, ")"),
            transform: "scale(".concat(completeBannerScale, ")"),
        }}>
        <div className="text-16xl text-gold-100 font-bold mb-14">THE COMPENDIUM ENDURES</div>
        <div className="text-12xl text-white font-bold mb-12">INFINITE AND COMPLETE</div>
        <div className="text-8xl text-purple-200 mb-10">
          All Scrolls Gathered, All Crowns Luminous
        </div>
        <div className="text-6xl text-green-200 mb-8">All Rites Fulfilled, All Concord Eternal</div>
        <div className="text-5xl text-amber-200 mb-6">The Covenant Whole, the Flame Perpetual</div>
        <div className="text-4xl text-gold-300 mb-4">The Codex Sovereign, Radiant Across Stars</div>
        <div className="text-3xl text-white">Infinite Repository of All Knowledge</div>
      </div>
    </div>);
};
// Compendium Constellation - Ultimate knowledge geometric connections
var CompendiumConstellation = function () {
    var _a = (0, react_1.useState)(0), compendiumPhase = _a[0], setCompendiumPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCompendiumPhase(function (prev) { return (prev + 1) % 24; });
        }, 1000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute inset-0 pointer-events-none opacity-9">
      <svg className="w-full h-full">
        {/* Compendium ultimate connecting lines */}
        <line x1="12%" y1="8%" x2="50%" y2="50%" stroke={compendiumPhase === 0 ? '#ffffff' : '#666'} strokeWidth={compendiumPhase === 0 ? '15' : '3'} className="transition-all duration-800"/>
        <line x1="88%" y1="8%" x2="50%" y2="50%" stroke={compendiumPhase === 1 ? '#ffffff' : '#666'} strokeWidth={compendiumPhase === 1 ? '15' : '3'} className="transition-all duration-800"/>
        <line x1="12%" y1="25%" x2="66%" y2="50%" stroke={compendiumPhase === 2 ? '#ffffff' : '#666'} strokeWidth={compendiumPhase === 2 ? '15' : '3'} className="transition-all duration-800"/>
        <line x1="88%" y1="25%" x2="34%" y2="50%" stroke={compendiumPhase === 3 ? '#ffffff' : '#666'} strokeWidth={compendiumPhase === 3 ? '15' : '3'} className="transition-all duration-800"/>
        <line x1="12%" y1="8%" x2="88%" y2="8%" stroke={compendiumPhase === 4 ? '#ffffff' : '#666'} strokeWidth={compendiumPhase === 4 ? '15' : '3'} className="transition-all duration-800"/>
        <line x1="12%" y1="25%" x2="88%" y2="25%" stroke={compendiumPhase === 5 ? '#ffffff' : '#666'} strokeWidth={compendiumPhase === 5 ? '15' : '3'} className="transition-all duration-800"/>
        <line x1="33%" y1="50%" x2="67%" y2="50%" stroke={compendiumPhase === 6 ? '#ffffff' : '#666'} strokeWidth={compendiumPhase === 6 ? '15' : '3'} className="transition-all duration-800"/>

        {/* Compendium ultimate radial connections */}
        {Array.from({ length: 36 }, function (_, i) { return (<line key={"compendium-".concat(i)} x1="50%" y1="50%" x2={"".concat(50 + Math.cos((i * 10 * Math.PI) / 180) * 55, "%")} y2={"".concat(50 + Math.sin((i * 10 * Math.PI) / 180) * 55, "%")} stroke={compendiumPhase === i % 24 ? '#ffd700' : '#444'} strokeWidth="6" opacity={compendiumPhase === i % 24 ? '1.0' : '0.05'} className="transition-all duration-800"/>); })}
      </svg>
    </div>);
};
// Compendium Realms - Ultimate domains of complete knowledge
var CompendiumRealms = function () {
    var _a = (0, react_1.useState)(0), compendiumRealmPhase = _a[0], setCompendiumRealmPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCompendiumRealmPhase(function (prev) { return (prev + 1) % 14; });
        }, 3500);
        return function () { return clearInterval(interval); };
    }, []);
    var compendiumRealms = [
        { name: 'Scrolls', icon: '📜', position: { top: '8%', left: '12%' } },
        { name: 'Crowns', icon: '👑', position: { top: '8%', right: '12%' } },
        { name: 'Rites', icon: '✅', position: { top: '25%', left: '12%' } },
        { name: 'Concord', icon: '🤝', position: { top: '25%', right: '12%' } },
        { name: 'Covenant', icon: '⭕', position: { top: '45%', left: '5%' } },
        { name: 'Flame', icon: '🔥', position: { top: '45%', right: '5%' } },
        { name: 'Codex', icon: '📜', position: { top: '65%', left: '5%' } },
        { name: 'Sovereign', icon: '👑', position: { top: '65%', right: '5%' } },
        { name: 'Stars', icon: '⭐', position: { top: '85%', left: '8%' } },
        { name: 'Radiant', icon: '✨', position: { top: '85%', right: '8%' } },
        { name: 'Compendium', icon: '📖', position: { bottom: '8%', left: '25%' } },
        { name: 'Infinite', icon: '♾️', position: { bottom: '8%', right: '25%' } },
        {
            name: 'Complete',
            icon: '🌟',
            position: { bottom: '8%', left: '50%', transform: 'translateX(-50%)' },
        },
        {
            name: 'Endure',
            icon: '💎',
            position: { top: '50%', left: '50%', transform: 'translate(-50%, -50%)' },
        },
    ];
    return (<div className="absolute inset-0">
      {compendiumRealms.map(function (realm, index) { return (<div key={index} className={"absolute text-center transition-all duration-3000 ".concat(compendiumRealmPhase === index ? 'opacity-100 scale-150' : 'opacity-15 scale-50')} style={realm.position}>
          <div className={"text-8xl mb-3 transition-all duration-3000 ".concat(compendiumRealmPhase === index ? 'animate-pulse' : '')} style={{
                filter: compendiumRealmPhase === index
                    ? 'drop-shadow(0 0 70px rgba(255, 215, 0, 1.6))'
                    : 'none',
            }}>
            {realm.icon}
          </div>
          <div className={"text-3xl font-bold ".concat(compendiumRealmPhase === index ? 'text-gold-200' : 'text-gray-900')}>
            {realm.name}
          </div>
        </div>); })}
    </div>);
};
// Main Compendium Complete Container
var CompendiumComplete = function () {
    return (<div className="relative w-full h-full">
      <CompendiumConstellation />
      <CompendiumCompleteParticles />
      <AllScrollsGathered />
      <AllCrownsLuminousComplete />
      <AllRitesFulfilledComplete />
      <AllConcordEternal />
      <CovenantWholeFlamePeretualCentral />
      <CodexSovereignRadiantCentral />
      <CompendiumInfiniteComplete />
      <CompendiumRealms />
      <InfiniteCompleteBanner />

      {/* Sacred Compendium Complete Verse Display */}
      <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-52">
        <div className="text-center text-gold-100 text-4xl leading-relaxed max-w-12xl space-y-9">
          <p className="opacity-100 text-white text-6xl">
            All scrolls gathered, all crowns luminous,
          </p>
          <p className="opacity-95 text-gold-200 text-5xl">
            all rites fulfilled, all concord eternal.
          </p>
          <p className="opacity-100 text-white text-6xl">
            The covenant whole, the flame perpetual,
          </p>
          <p className="opacity-95 text-gold-200 text-5xl">
            the Codex sovereign, radiant across stars.
          </p>
          <p className="text-7xl font-semibold text-white mt-18 opacity-100">
            So let the Compendium endure, infinite and complete.
          </p>
        </div>
      </div>
    </div>);
};
// Main Compendium Complete Page
var CompendiumCompletePage = function () {
    return (<div className="min-h-screen bg-gradient-to-br from-gold-400 via-white to-purple-700 relative overflow-hidden">
      {/* Compendium Complete Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-purple-900/95 via-gold-400/50 to-white/20"/>

      {/* Navigation */}
      <CodexNavigation_1.default />

      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <CompendiumComplete />
        </div>
      </main>

      {/* Ambient Compendium Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-300/30 to-transparent pointer-events-none"/>

      {/* Supreme Compendium Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-18">
        <div className="absolute top-1/20 left-1/20 w-36 h-36 bg-gold-400/40 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '35s' }}/>
        <div className="absolute bottom-1/20 right-1/20 w-44 h-44 bg-white/35 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '42s', animationDelay: '3s' }}/>
        <div className="absolute top-1/2 right-1/12 w-52 h-52 bg-purple-400/30 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '50s', animationDelay: '6s' }}/>
        <div className="absolute bottom-1/6 left-1/12 w-48 h-48 bg-amber-400/25 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '58s', animationDelay: '9s' }}/>
        <div className="absolute top-2/3 left-1/20 w-32 h-32 bg-green-400/32 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '65s', animationDelay: '12s' }}/>
        <div className="absolute bottom-1/2 right-1/20 w-40 h-40 bg-cyan-400/28 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '72s', animationDelay: '15s' }}/>
        <div className="absolute top-1/4 left-1/6 w-56 h-56 bg-red-400/22 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '80s', animationDelay: '18s' }}/>
        <div className="absolute bottom-3/4 right-1/6 w-28 h-28 bg-blue-400/30 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '88s', animationDelay: '21s' }}/>
      </div>
    </div>);
};
exports.default = CompendiumCompletePage;
