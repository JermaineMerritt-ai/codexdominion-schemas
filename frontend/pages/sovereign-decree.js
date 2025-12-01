"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var CodexNavigation_1 = require("../components/CodexNavigation");
// The Compendium Crowned Component - Ultimate repository achievement
var CompendiumCrowned = function () {
    var _a = (0, react_1.useState)(1.1), crownedPower = _a[0], setCrownedPower = _a[1];
    var _b = (0, react_1.useState)(1), compendiumScale = _b[0], setCompendiumScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCrownedPower(function (prev) { return (prev === 1.1 ? 1.9 : 1.1); });
            setCompendiumScale(function (prev) { return (prev === 1 ? 1.8 : 1); });
        }, 2800);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-8 left-1/8 transform -translate-x-1/2">
      <div className="text-center">
        <div className="text-18xl mb-5 transition-all duration-2800" style={{
            transform: "scale(".concat(compendiumScale, ")"),
            filter: "drop-shadow(0 0 140px rgba(255, 215, 0, ".concat(crownedPower, "))"),
        }}>
          📖
        </div>
        <div className="text-16xl mb-4 transition-all duration-2800" style={{
            transform: "scale(".concat(compendiumScale, ")"),
            filter: "drop-shadow(0 0 120px rgba(255, 140, 0, ".concat(crownedPower, "))"),
        }}>
          👑
        </div>
        <div className="text-14xl mb-3 transition-all duration-2800" style={{
            transform: "scale(".concat(compendiumScale, ")"),
            filter: "drop-shadow(0 0 100px rgba(184, 134, 11, ".concat(crownedPower, "))"),
        }}>
          ✨
        </div>
        <div className="text-4xl text-gold-200 font-bold mb-2">THE COMPENDIUM</div>
        <div className="text-4xl text-amber-200 font-bold">CROWNED</div>
      </div>
    </div>);
};
// Covenant Whole Complete Component - Perfect sacred bond
var CovenantWholeComplete = function () {
    var _a = (0, react_1.useState)(1.0), covenantWholeness = _a[0], setCovenantWholeness = _a[1];
    var _b = (0, react_1.useState)(1), wholeScale = _b[0], setWholeScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCovenantWholeness(function (prev) { return (prev === 1.0 ? 1.7 : 1.0); });
            setWholeScale(function (prev) { return (prev === 1 ? 1.6 : 1); });
        }, 3000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-8 right-1/8 transform translate-x-1/2">
      <div className="text-center">
        <div className="text-16xl mb-4 transition-all duration-3000" style={{
            transform: "scale(".concat(wholeScale, ")"),
            filter: "drop-shadow(0 0 120px rgba(34, 197, 94, ".concat(covenantWholeness, "))"),
        }}>
          ⭕
        </div>
        <div className="text-18xl mb-5 transition-all duration-3000" style={{
            transform: "scale(".concat(wholeScale, ")"),
            filter: "drop-shadow(0 0 140px rgba(0, 255, 127, ".concat(covenantWholeness, "))"),
        }}>
          🤝
        </div>
        <div className="text-14xl mb-3 transition-all duration-3000" style={{
            transform: "scale(".concat(wholeScale, ")"),
            filter: "drop-shadow(0 0 100px rgba(46, 125, 50, ".concat(covenantWholeness, "))"),
        }}>
          💚
        </div>
        <div className="text-4xl text-green-200 font-bold mb-2">THE COVENANT</div>
        <div className="text-4xl text-emerald-200 font-bold">WHOLE</div>
      </div>
    </div>);
};
// All Scrolls Gathered Fulfilled Component - Complete manuscript achievement
var AllScrollsGatheredFulfilled = function () {
    var _a = (0, react_1.useState)(0.9), scrollsGathering = _a[0], setScrollsGathering = _a[1];
    var _b = (0, react_1.useState)(1), gatheredScale = _b[0], setGatheredScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setScrollsGathering(function (prev) { return (prev === 0.9 ? 1.6 : 0.9); });
            setGatheredScale(function (prev) { return (prev === 1 ? 1.5 : 1); });
        }, 3200);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/4 left-1/8 transform -translate-x-1/2">
      <div className="text-center">
        <div className="text-15xl mb-3 transition-all duration-3200" style={{
            transform: "scale(".concat(gatheredScale, ")"),
            filter: "drop-shadow(0 0 110px rgba(139, 69, 19, ".concat(scrollsGathering, "))"),
        }}>
          📜
        </div>
        <div className="text-13xl mb-2 transition-all duration-3200" style={{
            transform: "scale(".concat(gatheredScale, ")"),
            filter: "drop-shadow(0 0 90px rgba(160, 82, 45, ".concat(scrollsGathering, "))"),
        }}>
          📋
        </div>
        <div className="text-11xl mb-1 transition-all duration-3200" style={{
            transform: "scale(".concat(gatheredScale, ")"),
            filter: "drop-shadow(0 0 70px rgba(205, 133, 63, ".concat(scrollsGathering, "))"),
        }}>
          📃
        </div>
        <div className="text-4xl text-amber-200 font-bold mb-2">ALL SCROLLS</div>
        <div className="text-4xl text-yellow-200 font-bold">GATHERED</div>
      </div>
    </div>);
};
// All Rites Fulfilled Supreme Component - Complete ceremonial perfection
var AllRitesFulfilledSupreme = function () {
    var _a = (0, react_1.useState)(1.1), ritesCompletion = _a[0], setRitesCompletion = _a[1];
    var _b = (0, react_1.useState)(1), fulfilledScale = _b[0], setFulfilledScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setRitesCompletion(function (prev) { return (prev === 1.1 ? 1.8 : 1.1); });
            setFulfilledScale(function (prev) { return (prev === 1 ? 1.7 : 1); });
        }, 2600);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/4 right-1/8 transform translate-x-1/2">
      <div className="text-center">
        <div className="text-17xl mb-4 transition-all duration-2600" style={{
            transform: "scale(".concat(fulfilledScale, ")"),
            filter: "drop-shadow(0 0 130px rgba(34, 197, 94, ".concat(ritesCompletion, "))"),
        }}>
          ✅
        </div>
        <div className="text-15xl mb-3 transition-all duration-2600" style={{
            transform: "scale(".concat(fulfilledScale, ")"),
            filter: "drop-shadow(0 0 110px rgba(76, 175, 80, ".concat(ritesCompletion, "))"),
        }}>
          🕊️
        </div>
        <div className="text-13xl mb-2 transition-all duration-2600" style={{
            transform: "scale(".concat(fulfilledScale, ")"),
            filter: "drop-shadow(0 0 90px rgba(129, 199, 132, ".concat(ritesCompletion, "))"),
        }}>
          ⚡
        </div>
        <div className="text-4xl text-green-200 font-bold mb-2">ALL RITES</div>
        <div className="text-4xl text-lime-200 font-bold">FULFILLED</div>
      </div>
    </div>);
};
// Sovereign Decree Central Component - Ultimate authority declaration
var SovereignDecreeCentral = function () {
    var _a = (0, react_1.useState)(1.2), decreePower = _a[0], setDecreePower = _a[1];
    var _b = (0, react_1.useState)(1), sovereignScale = _b[0], setSovereignScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setDecreePower(function (prev) { return (prev === 1.2 ? 2.0 : 1.2); });
            setSovereignScale(function (prev) { return (prev === 1 ? 1.9 : 1); });
        }, 2200);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 left-1/3 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div className="text-20xl mb-6 transition-all duration-2200" style={{
            transform: "scale(".concat(sovereignScale, ")"),
            filter: "drop-shadow(0 0 160px rgba(255, 215, 0, ".concat(decreePower, "))"),
        }}>
          👑
        </div>
        <div className="text-18xl mb-5 transition-all duration-2200" style={{
            transform: "scale(".concat(sovereignScale, ")"),
            filter: "drop-shadow(0 0 140px rgba(255, 69, 0, ".concat(decreePower, "))"),
        }}>
          📜
        </div>
        <div className="text-16xl mb-4 transition-all duration-2200" style={{
            transform: "scale(".concat(sovereignScale, ")"),
            filter: "drop-shadow(0 0 120px rgba(255, 140, 0, ".concat(decreePower, "))"),
        }}>
          ⚖️
        </div>
        <div className="text-5xl text-gold-200 font-bold mb-3">SOVEREIGN DECREE</div>
        <div className="text-4xl text-orange-200 font-bold">CODEX RELEASED</div>
      </div>
    </div>);
};
// Eternal Transmission Central Component - Cosmic distribution across councils and stars
var EternalTransmissionCentral = function () {
    var _a = (0, react_1.useState)(1.0), transmissionPower = _a[0], setTransmissionPower = _a[1];
    var _b = (0, react_1.useState)(1), eternalScale = _b[0], setEternalScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setTransmissionPower(function (prev) { return (prev === 1.0 ? 2.1 : 1.0); });
            setEternalScale(function (prev) { return (prev === 1 ? 2.0 : 1); });
        }, 2000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 right-1/3 transform translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div className="text-22xl mb-7 transition-all duration-2000" style={{
            transform: "scale(".concat(eternalScale, ")"),
            filter: "drop-shadow(0 0 180px rgba(138, 43, 226, ".concat(transmissionPower, "))"),
        }}>
          📡
        </div>
        <div className="text-20xl mb-6 transition-all duration-2000" style={{
            transform: "scale(".concat(eternalScale, ")"),
            filter: "drop-shadow(0 0 160px rgba(75, 0, 130, ".concat(transmissionPower, "))"),
        }}>
          🌌
        </div>
        <div className="text-18xl mb-5 transition-all duration-2000" style={{
            transform: "scale(".concat(eternalScale, ")"),
            filter: "drop-shadow(0 0 140px rgba(147, 112, 219, ".concat(transmissionPower, "))"),
        }}>
          ⭐
        </div>
        <div className="text-5xl text-purple-200 font-bold mb-3">ETERNAL</div>
        <div className="text-4xl text-indigo-200 font-bold">TRANSMISSION</div>
      </div>
    </div>);
};
// Dominion Infinite Radiant Component - Ultimate endurance proclamation
var DominionInfiniteRadiant = function () {
    var _a = (0, react_1.useState)(1.3), dominionPower = _a[0], setDominionPower = _a[1];
    var _b = (0, react_1.useState)(1), infiniteRadiantScale = _b[0], setInfiniteRadiantScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setDominionPower(function (prev) { return (prev === 1.3 ? 2.2 : 1.3); });
            setInfiniteRadiantScale(function (prev) { return (prev === 1 ? 2.1 : 1); });
        }, 1800);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div className="text-28xl mb-8 transition-all duration-1800" style={{
            transform: "scale(".concat(infiniteRadiantScale, ")"),
            filter: "drop-shadow(0 0 220px rgba(255, 215, 0, ".concat(dominionPower, "))"),
        }}>
          👑
        </div>
        <div className="text-26xl mb-7 transition-all duration-1800" style={{
            transform: "scale(".concat(infiniteRadiantScale, ")"),
            filter: "drop-shadow(0 0 200px rgba(255, 255, 255, ".concat(dominionPower, "))"),
        }}>
          ♾️
        </div>
        <div className="text-24xl mb-6 transition-all duration-1800" style={{
            transform: "scale(".concat(infiniteRadiantScale, ")"),
            filter: "drop-shadow(0 0 180px rgba(255, 140, 0, ".concat(dominionPower, "))"),
        }}>
          ✨
        </div>
        <div className="text-7xl text-gold-100 font-bold mb-5">THE DOMINION</div>
        <div className="text-6xl text-white font-bold mb-3">INFINITE</div>
        <div className="text-5xl text-amber-200 font-bold">RADIANT</div>
      </div>
    </div>);
};
// Sovereign Release Particles - Ultimate liberation energy
var SovereignReleaseParticles = function () {
    var particles = Array.from({ length: 160 }, function (_, i) { return ({
        id: i,
        size: Math.random() * 22 + 1,
        x: Math.random() * 100,
        y: Math.random() * 100,
        duration: Math.random() * 55 + 45,
        delay: Math.random() * 40,
        color: i % 16 === 0
            ? '#ffd700'
            : i % 16 === 1
                ? '#ffffff'
                : i % 16 === 2
                    ? '#32cd32'
                    : i % 16 === 3
                        ? '#ff6347'
                        : i % 16 === 4
                            ? '#4169e1'
                            : i % 16 === 5
                                ? '#9370db'
                                : i % 16 === 6
                                    ? '#00ced1'
                                    : i % 16 === 7
                                        ? '#ff69b4'
                                        : i % 16 === 8
                                            ? '#ffa500'
                                            : i % 16 === 9
                                                ? '#00ff00'
                                                : i % 16 === 10
                                                    ? '#ff1493'
                                                    : i % 16 === 11
                                                        ? '#8a2be2'
                                                        : i % 16 === 12
                                                            ? '#00bfff'
                                                            : i % 16 === 13
                                                                ? '#daa520'
                                                                : i % 16 === 14
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
                animation: "sovereignReleaseFlow ".concat(particle.duration, "s ease-in-out infinite"),
                animationDelay: "".concat(particle.delay, "s"),
                filter: 'blur(0.03px)',
                opacity: 1.0,
                boxShadow: "0 0 60px ".concat(particle.color),
            }}/>); })}
      <style jsx>{"\n        @keyframes sovereignReleaseFlow {\n          0% {\n            transform: translate(0, 0) scale(0.004) rotate(0deg);\n            opacity: 0.004;\n          }\n          3% {\n            transform: translate(100px, -250px) scale(3) rotate(8deg);\n            opacity: 1;\n          }\n          10% {\n            transform: translate(-90px, -500px) scale(0.15) rotate(32deg);\n            opacity: 0.98;\n          }\n          20% {\n            transform: translate(110px, -750px) scale(2.7) rotate(72deg);\n            opacity: 1;\n          }\n          30% {\n            transform: translate(-95px, -1000px) scale(0.35) rotate(112deg);\n            opacity: 0.95;\n          }\n          40% {\n            transform: translate(105px, -1250px) scale(2.4) rotate(152deg);\n            opacity: 0.98;\n          }\n          50% {\n            transform: translate(-85px, -1500px) scale(0.25) rotate(192deg);\n            opacity: 0.9;\n          }\n          60% {\n            transform: translate(95px, -1750px) scale(2.1) rotate(232deg);\n            opacity: 0.93;\n          }\n          70% {\n            transform: translate(-75px, -2000px) scale(0.45) rotate(272deg);\n            opacity: 0.85;\n          }\n          80% {\n            transform: translate(85px, -2250px) scale(1.8) rotate(312deg);\n            opacity: 0.88;\n          }\n          88% {\n            transform: translate(-65px, -2500px) scale(0.35) rotate(342deg);\n            opacity: 0.75;\n          }\n          94% {\n            transform: translate(45px, -2750px) scale(0.9) rotate(356deg);\n            opacity: 0.55;\n          }\n          97% {\n            transform: translate(-25px, -3000px) scale(0.08) rotate(368deg);\n            opacity: 0.25;\n          }\n          100% {\n            transform: translate(0, -3250px) scale(0.001) rotate(380deg);\n            opacity: 0.001;\n          }\n        }\n      "}</style>
    </div>);
};
// Infinite Radiant Banner - Ultimate dominion proclamation
var InfiniteRadiantBanner = function () {
    var _a = (0, react_1.useState)(1.5), radiantIntensity = _a[0], setRadiantIntensity = _a[1];
    var _b = (0, react_1.useState)(1), infiniteBannerScale = _b[0], setInfiniteBannerScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setRadiantIntensity(function (prev) { return (prev === 1.5 ? 2.4 : 1.5); });
            setInfiniteBannerScale(function (prev) { return (prev === 1 ? 1.7 : 1); });
        }, 2400);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-2 left-1/2 transform -translate-x-1/2">
      <div className="text-center px-72 py-56 bg-gradient-to-r from-gold-500/98 via-white/70 to-purple-600/98 rounded-10xl border-20 border-gold-200/100 transition-all duration-2400" style={{
            boxShadow: "0 380px 760px rgba(255, 215, 0, ".concat(radiantIntensity, ")"),
            transform: "scale(".concat(infiniteBannerScale, ")"),
        }}>
        <div className="text-18xl text-gold-100 font-bold mb-16">THE DOMINION ENDURES</div>
        <div className="text-14xl text-white font-bold mb-14">INFINITE AND RADIANT</div>
        <div className="text-10xl text-purple-200 mb-12">
          The Compendium Crowned, The Covenant Whole
        </div>
        <div className="text-8xl text-green-200 mb-10">
          All Scrolls Gathered, All Rites Fulfilled
        </div>
        <div className="text-6xl text-orange-200 mb-8">
          By Sovereign Decree, the Codex is Released
        </div>
        <div className="text-5xl text-indigo-200 mb-6">
          Eternal Transmission Across Councils and Stars
        </div>
        <div className="text-4xl text-gold-300 mb-4">The Ultimate Authority Endures Forever</div>
        <div className="text-3xl text-white">Infinite Radiance Across All Realms</div>
      </div>
    </div>);
};
// Sovereign Constellation - Ultimate decree geometric connections
var SovereignConstellation = function () {
    var _a = (0, react_1.useState)(0), sovereignPhase = _a[0], setSovereignPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setSovereignPhase(function (prev) { return (prev + 1) % 28; });
        }, 900);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute inset-0 pointer-events-none opacity-85">
      <svg className="w-full h-full">
        {/* Sovereign ultimate connecting lines */}
        <line x1="12%" y1="8%" x2="50%" y2="50%" stroke={sovereignPhase === 0 ? '#ffffff' : '#777'} strokeWidth={sovereignPhase === 0 ? '18' : '4'} className="transition-all duration-700"/>
        <line x1="88%" y1="8%" x2="50%" y2="50%" stroke={sovereignPhase === 1 ? '#ffffff' : '#777'} strokeWidth={sovereignPhase === 1 ? '18' : '4'} className="transition-all duration-700"/>
        <line x1="12%" y1="25%" x2="66%" y2="50%" stroke={sovereignPhase === 2 ? '#ffffff' : '#777'} strokeWidth={sovereignPhase === 2 ? '18' : '4'} className="transition-all duration-700"/>
        <line x1="88%" y1="25%" x2="34%" y2="50%" stroke={sovereignPhase === 3 ? '#ffffff' : '#777'} strokeWidth={sovereignPhase === 3 ? '18' : '4'} className="transition-all duration-700"/>
        <line x1="12%" y1="8%" x2="88%" y2="8%" stroke={sovereignPhase === 4 ? '#ffffff' : '#777'} strokeWidth={sovereignPhase === 4 ? '18' : '4'} className="transition-all duration-700"/>
        <line x1="12%" y1="25%" x2="88%" y2="25%" stroke={sovereignPhase === 5 ? '#ffffff' : '#777'} strokeWidth={sovereignPhase === 5 ? '18' : '4'} className="transition-all duration-700"/>
        <line x1="33%" y1="50%" x2="67%" y2="50%" stroke={sovereignPhase === 6 ? '#ffffff' : '#777'} strokeWidth={sovereignPhase === 6 ? '18' : '4'} className="transition-all duration-700"/>

        {/* Sovereign ultimate radial connections */}
        {Array.from({ length: 42 }, function (_, i) { return (<line key={"sovereign-".concat(i)} x1="50%" y1="50%" x2={"".concat(50 + Math.cos((i * 8.571 * Math.PI) / 180) * 60, "%")} y2={"".concat(50 + Math.sin((i * 8.571 * Math.PI) / 180) * 60, "%")} stroke={sovereignPhase === i % 28 ? '#ffd700' : '#555'} strokeWidth="7" opacity={sovereignPhase === i % 28 ? '1.0' : '0.03'} className="transition-all duration-700"/>); })}
      </svg>
    </div>);
};
// Sovereign Realms - Ultimate domains of decree and transmission
var SovereignRealms = function () {
    var _a = (0, react_1.useState)(0), sovereignRealmPhase = _a[0], setSovereignRealmPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setSovereignRealmPhase(function (prev) { return (prev + 1) % 16; });
        }, 3800);
        return function () { return clearInterval(interval); };
    }, []);
    var sovereignRealms = [
        { name: 'Compendium', icon: '📖', position: { top: '8%', left: '12%' } },
        { name: 'Crowned', icon: '👑', position: { top: '8%', right: '12%' } },
        { name: 'Covenant', icon: '⭕', position: { top: '25%', left: '12%' } },
        { name: 'Whole', icon: '🤝', position: { top: '25%', right: '12%' } },
        { name: 'Scrolls', icon: '📜', position: { top: '40%', left: '8%' } },
        { name: 'Gathered', icon: '📋', position: { top: '40%', right: '8%' } },
        { name: 'Rites', icon: '✅', position: { top: '55%', left: '8%' } },
        { name: 'Fulfilled', icon: '🕊️', position: { top: '55%', right: '8%' } },
        { name: 'Sovereign', icon: '⚖️', position: { top: '70%', left: '5%' } },
        { name: 'Decree', icon: '📜', position: { top: '70%', right: '5%' } },
        { name: 'Codex', icon: '📚', position: { top: '85%', left: '10%' } },
        { name: 'Released', icon: '🚀', position: { top: '85%', right: '10%' } },
        { name: 'Eternal', icon: '♾️', position: { bottom: '15%', left: '25%' } },
        {
            name: 'Transmission',
            icon: '📡',
            position: { bottom: '15%', right: '25%' },
        },
        { name: 'Councils', icon: '🏛️', position: { bottom: '8%', left: '35%' } },
        { name: 'Stars', icon: '⭐', position: { bottom: '8%', right: '35%' } },
    ];
    return (<div className="absolute inset-0">
      {sovereignRealms.map(function (realm, index) { return (<div key={index} className={"absolute text-center transition-all duration-3500 ".concat(sovereignRealmPhase === index ? 'opacity-100 scale-160' : 'opacity-12 scale-40')} style={realm.position}>
          <div className={"text-9xl mb-4 transition-all duration-3500 ".concat(sovereignRealmPhase === index ? 'animate-pulse' : '')} style={{
                filter: sovereignRealmPhase === index
                    ? 'drop-shadow(0 0 80px rgba(255, 215, 0, 1.8))'
                    : 'none',
            }}>
            {realm.icon}
          </div>
          <div className={"text-3xl font-bold ".concat(sovereignRealmPhase === index ? 'text-gold-200' : 'text-gray-800')}>
            {realm.name}
          </div>
        </div>); })}
    </div>);
};
// Main Sovereign Decree Container
var SovereignDecree = function () {
    return (<div className="relative w-full h-full">
      <SovereignConstellation />
      <SovereignReleaseParticles />
      <CompendiumCrowned />
      <CovenantWholeComplete />
      <AllScrollsGatheredFulfilled />
      <AllRitesFulfilledSupreme />
      <SovereignDecreeCentral />
      <EternalTransmissionCentral />
      <DominionInfiniteRadiant />
      <SovereignRealms />
      <InfiniteRadiantBanner />

      {/* Sacred Sovereign Decree Verse Display */}
      <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-60">
        <div className="text-center text-gold-100 text-4xl leading-relaxed max-w-14xl space-y-10">
          <p className="opacity-100 text-white text-7xl">
            The Compendium crowned, the covenant whole,
          </p>
          <p className="opacity-95 text-gold-200 text-6xl">
            all scrolls gathered, all rites fulfilled.
          </p>
          <p className="opacity-100 text-white text-7xl">
            By sovereign decree, the Codex is released,
          </p>
          <p className="opacity-95 text-purple-200 text-6xl">
            eternal transmission across councils and stars.
          </p>
          <p className="text-8xl font-semibold text-white mt-20 opacity-100">
            So let the Dominion endure, infinite and radiant.
          </p>
        </div>
      </div>
    </div>);
};
// Main Sovereign Decree Page
var SovereignDecreePage = function () {
    return (<div className="min-h-screen bg-gradient-to-br from-gold-500 via-white to-purple-800 relative overflow-hidden">
      {/* Sovereign Decree Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-purple-900/98 via-gold-500/55 to-white/25"/>

      {/* Navigation */}
      <CodexNavigation_1.default />

      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <SovereignDecree />
        </div>
      </main>

      {/* Ambient Sovereign Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-400/35 to-transparent pointer-events-none"/>

      {/* Supreme Sovereign Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-20">
        <div className="absolute top-1/24 left-1/24 w-40 h-40 bg-gold-400/45 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '38s' }}/>
        <div className="absolute bottom-1/24 right-1/24 w-48 h-48 bg-white/40 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '45s', animationDelay: '3s' }}/>
        <div className="absolute top-1/2 right-1/15 w-56 h-56 bg-purple-400/35 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '55s', animationDelay: '6s' }}/>
        <div className="absolute bottom-1/8 left-1/15 w-52 h-52 bg-amber-400/30 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '62s', animationDelay: '9s' }}/>
        <div className="absolute top-2/3 left-1/24 w-36 h-36 bg-green-400/38 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '70s', animationDelay: '12s' }}/>
        <div className="absolute bottom-1/2 right-1/24 w-44 h-44 bg-cyan-400/33 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '78s', animationDelay: '15s' }}/>
        <div className="absolute top-1/4 left-1/8 w-60 h-60 bg-red-400/28 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '85s', animationDelay: '18s' }}/>
        <div className="absolute bottom-3/4 right-1/8 w-32 h-32 bg-blue-400/35 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '92s', animationDelay: '21s' }}/>
        <div className="absolute top-1/8 left-1/3 w-28 h-28 bg-indigo-400/40 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '100s', animationDelay: '24s' }}/>
      </div>
    </div>);
};
exports.default = SovereignDecreePage;
