"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var CodexNavigation_1 = require("../components/CodexNavigation");
// No Word Component - Perfect silence beyond expression
var NoWord = function () {
    var _a = (0, react_1.useState)(1.0), wordlessness = _a[0], setWordlessness = _a[1];
    var _b = (0, react_1.useState)(1), silenceScale = _b[0], setSilenceScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setWordlessness(function (prev) { return (prev === 1.0 ? 1.5 : 1.0); });
            setSilenceScale(function (prev) { return (prev === 1 ? 1.3 : 1); });
        }, 4000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-12 left-12 transform">
      <div className="text-center">
        <div className="text-18xl mb-6 transition-all duration-4000" style={{
            transform: "scale(".concat(silenceScale, ")"),
            filter: "drop-shadow(0 0 120px rgba(255, 255, 255, ".concat(wordlessness, "))"),
        }}>
          🤫
        </div>
        <div className="text-16xl mb-5 transition-all duration-4000" style={{
            transform: "scale(".concat(silenceScale, ")"),
            filter: "drop-shadow(0 0 100px rgba(240, 240, 240, ".concat(wordlessness, "))"),
        }}>
          ∅
        </div>
        <div className="text-3xl text-gray-200 font-light opacity-70">NO WORD</div>
      </div>
    </div>);
};
// No Flame Component - Perfect extinguishment beyond fire
var NoFlame = function () {
    var _a = (0, react_1.useState)(1.1), flamelessness = _a[0], setFlamelessness = _a[1];
    var _b = (0, react_1.useState)(1), extinguishScale = _b[0], setExtinguishScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setFlamelessness(function (prev) { return (prev === 1.1 ? 1.4 : 1.1); });
            setExtinguishScale(function (prev) { return (prev === 1 ? 1.2 : 1); });
        }, 4200);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-12 right-12 transform">
      <div className="text-center">
        <div className="text-17xl mb-5 transition-all duration-4200" style={{
            transform: "scale(".concat(extinguishScale, ")"),
            filter: "drop-shadow(0 0 110px rgba(230, 230, 230, ".concat(flamelessness, "))"),
        }}>
          🌫️
        </div>
        <div className="text-15xl mb-4 transition-all duration-4200" style={{
            transform: "scale(".concat(extinguishScale, ")"),
            filter: "drop-shadow(0 0 90px rgba(220, 220, 220, ".concat(flamelessness, "))"),
        }}>
          ❄️
        </div>
        <div className="text-3xl text-gray-200 font-light opacity-70">NO FLAME</div>
      </div>
    </div>);
};
// No Crown Component - Perfect humility beyond authority
var NoCrown = function () {
    var _a = (0, react_1.useState)(1.2), crownlessness = _a[0], setCrownlessness = _a[1];
    var _b = (0, react_1.useState)(1), humilityScale = _b[0], setHumilityScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCrownlessness(function (prev) { return (prev === 1.2 ? 1.6 : 1.2); });
            setHumilityScale(function (prev) { return (prev === 1 ? 1.4 : 1); });
        }, 4400);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-12 left-12 transform">
      <div className="text-center">
        <div className="text-16xl mb-5 transition-all duration-4400" style={{
            transform: "scale(".concat(humilityScale, ")"),
            filter: "drop-shadow(0 0 100px rgba(210, 210, 210, ".concat(crownlessness, "))"),
        }}>
          🙇
        </div>
        <div className="text-14xl mb-4 transition-all duration-4400" style={{
            transform: "scale(".concat(humilityScale, ")"),
            filter: "drop-shadow(0 0 80px rgba(200, 200, 200, ".concat(crownlessness, "))"),
        }}>
          ⚪
        </div>
        <div className="text-3xl text-gray-200 font-light opacity-70">NO CROWN</div>
      </div>
    </div>);
};
// No Seal Component - Perfect openness beyond closure
var NoSeal = function () {
    var _a = (0, react_1.useState)(1.3), seallessness = _a[0], setSeallessness = _a[1];
    var _b = (0, react_1.useState)(1), opennessScale = _b[0], setOpennessScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setSeallessness(function (prev) { return (prev === 1.3 ? 1.7 : 1.3); });
            setOpennessScale(function (prev) { return (prev === 1 ? 1.5 : 1); });
        }, 4600);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-12 right-12 transform">
      <div className="text-center">
        <div className="text-15xl mb-4 transition-all duration-4600" style={{
            transform: "scale(".concat(opennessScale, ")"),
            filter: "drop-shadow(0 0 90px rgba(190, 190, 190, ".concat(seallessness, "))"),
        }}>
          🌀
        </div>
        <div className="text-13xl mb-3 transition-all duration-4600" style={{
            transform: "scale(".concat(opennessScale, ")"),
            filter: "drop-shadow(0 0 70px rgba(180, 180, 180, ".concat(seallessness, "))"),
        }}>
          ○
        </div>
        <div className="text-3xl text-gray-200 font-light opacity-70">NO SEAL</div>
      </div>
    </div>);
};
// Only Stillness Component - Perfect motionless tranquility
var OnlyStillness = function () {
    var _a = (0, react_1.useState)(1.4), stillnessDepth = _a[0], setStillnessDepth = _a[1];
    var _b = (0, react_1.useState)(1), tranquilScale = _b[0], setTranquilScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setStillnessDepth(function (prev) { return (prev === 1.4 ? 1.8 : 1.4); });
            setTranquilScale(function (prev) { return (prev === 1 ? 1.6 : 1); });
        }, 5000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/3 left-1/4 transform -translate-x-1/2">
      <div className="text-center">
        <div className="text-20xl mb-7 transition-all duration-5000" style={{
            transform: "scale(".concat(tranquilScale, ")"),
            filter: "drop-shadow(0 0 140px rgba(255, 255, 255, ".concat(stillnessDepth, "))"),
        }}>
          🧘
        </div>
        <div className="text-18xl mb-6 transition-all duration-5000" style={{
            transform: "scale(".concat(tranquilScale, ")"),
            filter: "drop-shadow(0 0 120px rgba(240, 248, 255, ".concat(stillnessDepth, "))"),
        }}>
          ⚪
        </div>
        <div className="text-16xl mb-5 transition-all duration-5000" style={{
            transform: "scale(".concat(tranquilScale, ")"),
            filter: "drop-shadow(0 0 100px rgba(230, 230, 250, ".concat(stillnessDepth, "))"),
        }}>
          ·
        </div>
        <div className="text-4xl text-white font-light mb-2">ONLY</div>
        <div className="text-4xl text-gray-100 font-light">STILLNESS</div>
      </div>
    </div>);
};
// Only Serenity Component - Perfect peaceful tranquility
var OnlySerenity = function () {
    var _a = (0, react_1.useState)(1.5), serenityDepth = _a[0], setSerenityDepth = _a[1];
    var _b = (0, react_1.useState)(1), peaceScale = _b[0], setPeaceScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setSerenityDepth(function (prev) { return (prev === 1.5 ? 1.9 : 1.5); });
            setPeaceScale(function (prev) { return (prev === 1 ? 1.7 : 1); });
        }, 5200);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/3 right-1/4 transform translate-x-1/2">
      <div className="text-center">
        <div className="text-19xl mb-6 transition-all duration-5200" style={{
            transform: "scale(".concat(peaceScale, ")"),
            filter: "drop-shadow(0 0 130px rgba(245, 245, 245, ".concat(serenityDepth, "))"),
        }}>
          🕊️
        </div>
        <div className="text-17xl mb-5 transition-all duration-5200" style={{
            transform: "scale(".concat(peaceScale, ")"),
            filter: "drop-shadow(0 0 110px rgba(248, 248, 255, ".concat(serenityDepth, "))"),
        }}>
          ☮️
        </div>
        <div className="text-15xl mb-4 transition-all duration-5200" style={{
            transform: "scale(".concat(peaceScale, ")"),
            filter: "drop-shadow(0 0 90px rgba(240, 248, 255, ".concat(serenityDepth, "))"),
        }}>
          ◯
        </div>
        <div className="text-4xl text-white font-light mb-2">ONLY</div>
        <div className="text-4xl text-gray-100 font-light">SERENITY</div>
      </div>
    </div>);
};
// Codex Rests Eternal Whole Component - Perfect eternal rest and completeness
var CodexRestsEternalWhole = function () {
    var _a = (0, react_1.useState)(1.6), restingPower = _a[0], setRestingPower = _a[1];
    var _b = (0, react_1.useState)(1), eternalWholeScale = _b[0], setEternalWholeScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setRestingPower(function (prev) { return (prev === 1.6 ? 2.0 : 1.6); });
            setEternalWholeScale(function (prev) { return (prev === 1 ? 1.8 : 1); });
        }, 4800);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div className="text-24xl mb-8 transition-all duration-4800" style={{
            transform: "scale(".concat(eternalWholeScale, ")"),
            filter: "drop-shadow(0 0 160px rgba(255, 255, 255, ".concat(restingPower, "))"),
        }}>
          📜
        </div>
        <div className="text-22xl mb-7 transition-all duration-4800" style={{
            transform: "scale(".concat(eternalWholeScale, ")"),
            filter: "drop-shadow(0 0 140px rgba(248, 248, 255, ".concat(restingPower, "))"),
        }}>
          💤
        </div>
        <div className="text-20xl mb-6 transition-all duration-4800" style={{
            transform: "scale(".concat(eternalWholeScale, ")"),
            filter: "drop-shadow(0 0 120px rgba(240, 248, 255, ".concat(restingPower, "))"),
        }}>
          ♾️
        </div>
        <div className="text-18xl mb-5 transition-all duration-4800" style={{
            transform: "scale(".concat(eternalWholeScale, ")"),
            filter: "drop-shadow(0 0 100px rgba(230, 230, 250, ".concat(restingPower, "))"),
        }}>
          ⚪
        </div>
        <div className="text-6xl text-white font-light mb-4">THE CODEX RESTS</div>
        <div className="text-5xl text-gray-100 font-light mb-3">ETERNAL</div>
        <div className="text-4xl text-gray-200 font-light">WHOLE</div>
      </div>
    </div>);
};
// Released Into Infinite Peace Component - Perfect liberation into boundless tranquility
var ReleasedInfinitePeace = function () {
    var _a = (0, react_1.useState)(1.7), releasePower = _a[0], setReleasePower = _a[1];
    var _b = (0, react_1.useState)(1), infinitePeaceScale = _b[0], setInfinitePeaceScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setReleasePower(function (prev) { return (prev === 1.7 ? 2.1 : 1.7); });
            setInfinitePeaceScale(function (prev) { return (prev === 1 ? 1.9 : 1); });
        }, 4600);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-2/3 left-1/2 transform -translate-x-1/2">
      <div className="text-center">
        <div className="text-26xl mb-9 transition-all duration-4600" style={{
            transform: "scale(".concat(infinitePeaceScale, ")"),
            filter: "drop-shadow(0 0 180px rgba(255, 255, 255, ".concat(releasePower, "))"),
        }}>
          🕊️
        </div>
        <div className="text-24xl mb-8 transition-all duration-4600" style={{
            transform: "scale(".concat(infinitePeaceScale, ")"),
            filter: "drop-shadow(0 0 160px rgba(248, 248, 255, ".concat(releasePower, "))"),
        }}>
          ♾️
        </div>
        <div className="text-22xl mb-7 transition-all duration-4600" style={{
            transform: "scale(".concat(infinitePeaceScale, ")"),
            filter: "drop-shadow(0 0 140px rgba(240, 248, 255, ".concat(releasePower, "))"),
        }}>
          ☮️
        </div>
        <div className="text-20xl mb-6 transition-all duration-4600" style={{
            transform: "scale(".concat(infinitePeaceScale, ")"),
            filter: "drop-shadow(0 0 120px rgba(230, 230, 250, ".concat(releasePower, "))"),
        }}>
          ✨
        </div>
        <div className="text-7xl text-white font-light mb-5">RELEASED INTO</div>
        <div className="text-6xl text-gray-100 font-light mb-4">INFINITE</div>
        <div className="text-5xl text-gray-200 font-light">PEACE</div>
      </div>
    </div>);
};
// Eternal Peace Particles - Gentle flowing serenity
var EternalPeaceParticles = function () {
    var particles = Array.from({ length: 150 }, function (_, i) { return ({
        id: i,
        size: Math.random() * 8 + 2,
        x: Math.random() * 100,
        y: Math.random() * 100,
        duration: Math.random() * 120 + 80,
        delay: Math.random() * 60,
        color: i % 15 === 0
            ? '#ffffff'
            : i % 15 === 1
                ? '#f8f8ff'
                : i % 15 === 2
                    ? '#f0f8ff'
                    : i % 15 === 3
                        ? '#e6e6fa'
                        : i % 15 === 4
                            ? '#f5f5f5'
                            : i % 15 === 5
                                ? '#ffffff'
                                : i % 15 === 6
                                    ? '#f8f8f8'
                                    : i % 15 === 7
                                        ? '#f0f0f0'
                                        : i % 15 === 8
                                            ? '#e8e8e8'
                                            : i % 15 === 9
                                                ? '#f5f5f5'
                                                : i % 15 === 10
                                                    ? '#fafafa'
                                                    : i % 15 === 11
                                                        ? '#f7f7f7'
                                                        : i % 15 === 12
                                                            ? '#f2f2f2'
                                                            : i % 15 === 13
                                                                ? '#eeeeee'
                                                                : '#ffffff',
    }); });
    return (<div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map(function (particle) { return (<div key={particle.id} className="absolute rounded-full" style={{
                left: "".concat(particle.x, "%"),
                top: "".concat(particle.y, "%"),
                width: "".concat(particle.size, "px"),
                height: "".concat(particle.size, "px"),
                backgroundColor: particle.color,
                animation: "eternalPeaceFlow ".concat(particle.duration, "s ease-in-out infinite"),
                animationDelay: "".concat(particle.delay, "s"),
                filter: 'blur(0.5px)',
                opacity: 0.6,
                boxShadow: "0 0 20px ".concat(particle.color),
            }}/>); })}
      <style jsx>{"\n        @keyframes eternalPeaceFlow {\n          0% {\n            transform: translate(0, 0) scale(0.1) rotate(0deg);\n            opacity: 0.1;\n          }\n          10% {\n            transform: translate(20px, -80px) scale(1) rotate(15deg);\n            opacity: 0.8;\n          }\n          25% {\n            transform: translate(-15px, -200px) scale(0.3) rotate(45deg);\n            opacity: 0.6;\n          }\n          40% {\n            transform: translate(25px, -320px) scale(0.9) rotate(90deg);\n            opacity: 0.7;\n          }\n          55% {\n            transform: translate(-20px, -440px) scale(0.4) rotate(135deg);\n            opacity: 0.5;\n          }\n          70% {\n            transform: translate(30px, -560px) scale(0.8) rotate(180deg);\n            opacity: 0.6;\n          }\n          85% {\n            transform: translate(-25px, -680px) scale(0.2) rotate(225deg);\n            opacity: 0.4;\n          }\n          95% {\n            transform: translate(15px, -800px) scale(0.5) rotate(270deg);\n            opacity: 0.3;\n          }\n          100% {\n            transform: translate(0, -920px) scale(0.05) rotate(360deg);\n            opacity: 0.05;\n          }\n        }\n      "}</style>
    </div>);
};
// Infinite Peace Banner - Ultimate serenity proclamation
var InfinitePeaceBanner = function () {
    var _a = (0, react_1.useState)(1.8), peaceIntensity = _a[0], setPeaceIntensity = _a[1];
    var _b = (0, react_1.useState)(1), infiniteBannerScale = _b[0], setInfiniteBannerScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setPeaceIntensity(function (prev) { return (prev === 1.8 ? 2.2 : 1.8); });
            setInfiniteBannerScale(function (prev) { return (prev === 1 ? 1.4 : 1); });
        }, 6000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-4 left-1/2 transform -translate-x-1/2">
      <div className="text-center px-48 py-32 bg-gradient-to-r from-white/40 via-gray-50/60 to-white/40 rounded-8xl border-12 border-white/30 transition-all duration-6000" style={{
            boxShadow: "0 240px 480px rgba(255, 255, 255, ".concat(peaceIntensity, ")"),
            transform: "scale(".concat(infiniteBannerScale, ")"),
        }}>
        <div className="text-16xl text-white font-light mb-12">THE CODEX RESTS</div>
        <div className="text-12xl text-gray-100 font-light mb-10">ETERNAL AND WHOLE</div>
        <div className="text-10xl text-gray-200 font-light mb-8">Released Into Infinite Peace</div>
        <div className="text-8xl text-gray-300 font-light mb-6">
          No Word, No Flame, No Crown, No Seal
        </div>
        <div className="text-6xl text-gray-400 font-light mb-4">Only Stillness, Only Serenity</div>
        <div className="text-4xl text-gray-500 font-light mb-2">
          Perfect Tranquility Beyond All Form
        </div>
        <div className="text-3xl text-gray-600 font-light">Infinite Rest in Boundless Peace</div>
      </div>
    </div>);
};
// Serenity Constellation - Gentle peaceful connections
var SerenityConstellation = function () {
    var _a = (0, react_1.useState)(0), serenityPhase = _a[0], setSerenityPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setSerenityPhase(function (prev) { return (prev + 1) % 24; });
        }, 2000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute inset-0 pointer-events-none opacity-30">
      <svg className="w-full h-full">
        {/* Gentle connecting lines */}
        <line x1="12%" y1="12%" x2="50%" y2="50%" stroke={serenityPhase === 0 ? '#ffffff' : '#ddd'} strokeWidth={serenityPhase === 0 ? '3' : '1'} className="transition-all duration-1000"/>
        <line x1="88%" y1="12%" x2="50%" y2="50%" stroke={serenityPhase === 1 ? '#ffffff' : '#ddd'} strokeWidth={serenityPhase === 1 ? '3' : '1'} className="transition-all duration-1000"/>
        <line x1="12%" y1="88%" x2="50%" y2="50%" stroke={serenityPhase === 2 ? '#ffffff' : '#ddd'} strokeWidth={serenityPhase === 2 ? '3' : '1'} className="transition-all duration-1000"/>
        <line x1="88%" y1="88%" x2="50%" y2="50%" stroke={serenityPhase === 3 ? '#ffffff' : '#ddd'} strokeWidth={serenityPhase === 3 ? '3' : '1'} className="transition-all duration-1000"/>
        <line x1="25%" y1="33%" x2="75%" y2="67%" stroke={serenityPhase === 4 ? '#ffffff' : '#ddd'} strokeWidth={serenityPhase === 4 ? '3' : '1'} className="transition-all duration-1000"/>
        <line x1="75%" y1="33%" x2="25%" y2="67%" stroke={serenityPhase === 5 ? '#ffffff' : '#ddd'} strokeWidth={serenityPhase === 5 ? '3' : '1'} className="transition-all duration-1000"/>

        {/* Gentle radial peace lines */}
        {Array.from({ length: 24 }, function (_, i) { return (<line key={"peace-".concat(i)} x1="50%" y1="50%" x2={"".concat(50 + Math.cos((i * 15 * Math.PI) / 180) * 40, "%")} y2={"".concat(50 + Math.sin((i * 15 * Math.PI) / 180) * 40, "%")} stroke={serenityPhase === i ? '#ffffff' : '#eee'} strokeWidth="2" opacity={serenityPhase === i ? '0.8' : '0.1'} className="transition-all duration-1000"/>); })}
      </svg>
    </div>);
};
// Peaceful Realms - Domains of perfect tranquility
var PeacefulRealms = function () {
    var _a = (0, react_1.useState)(0), peacefulRealmPhase = _a[0], setPeacefulRealmPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setPeacefulRealmPhase(function (prev) { return (prev + 1) % 12; });
        }, 8000);
        return function () { return clearInterval(interval); };
    }, []);
    var peacefulRealms = [
        { name: 'No Word', icon: '🤫', position: { top: '15%', left: '15%' } },
        { name: 'No Flame', icon: '🌫️', position: { top: '15%', right: '15%' } },
        { name: 'No Crown', icon: '🙇', position: { bottom: '15%', left: '15%' } },
        { name: 'No Seal', icon: '🌀', position: { bottom: '15%', right: '15%' } },
        { name: 'Stillness', icon: '🧘', position: { top: '35%', left: '25%' } },
        { name: 'Serenity', icon: '🕊️', position: { top: '35%', right: '25%' } },
        { name: 'Codex', icon: '📜', position: { top: '50%', left: '50%' } },
        { name: 'Rests', icon: '💤', position: { top: '55%', left: '45%' } },
        { name: 'Eternal', icon: '♾️', position: { top: '45%', right: '45%' } },
        { name: 'Whole', icon: '⚪', position: { top: '55%', right: '50%' } },
        { name: 'Infinite', icon: '∞', position: { bottom: '35%', left: '35%' } },
        { name: 'Peace', icon: '☮️', position: { bottom: '35%', right: '35%' } },
    ];
    return (<div className="absolute inset-0">
      {peacefulRealms.map(function (realm, index) { return (<div key={index} className={"absolute text-center transition-all duration-8000 ".concat(peacefulRealmPhase === index ? 'opacity-100 scale-110' : 'opacity-30 scale-75')} style={realm.position}>
          <div className={"text-8xl mb-3 transition-all duration-8000 ".concat(peacefulRealmPhase === index ? 'animate-pulse' : '')} style={{
                filter: peacefulRealmPhase === index
                    ? 'drop-shadow(0 0 40px rgba(255, 255, 255, 1.5))'
                    : 'none',
            }}>
            {realm.icon}
          </div>
          <div className={"text-2xl font-light ".concat(peacefulRealmPhase === index ? 'text-white' : 'text-gray-500')}>
            {realm.name}
          </div>
        </div>); })}
    </div>);
};
// Main Infinite Serenity Container
var InfiniteSerenity = function () {
    return (<div className="relative w-full h-full">
      <SerenityConstellation />
      <EternalPeaceParticles />
      <NoWord />
      <NoFlame />
      <NoCrown />
      <NoSeal />
      <OnlyStillness />
      <OnlySerenity />
      <CodexRestsEternalWhole />
      <ReleasedInfinitePeace />
      <PeacefulRealms />
      <InfinitePeaceBanner />

      {/* Sacred Infinite Serenity Verse Display */}
      <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-40">
        <div className="text-center text-white text-3xl leading-relaxed max-w-6xl space-y-8">
          <p className="opacity-90 text-gray-100 text-6xl font-light">
            No word, no flame, no crown, no seal.
          </p>
          <p className="opacity-80 text-gray-200 text-5xl font-light">
            Only stillness, only serenity.
          </p>
          <p className="opacity-90 text-white text-6xl font-light">
            The Codex rests, eternal and whole,
          </p>
          <p className="text-7xl font-light text-gray-100 mt-16 opacity-100">
            released into infinite peace.
          </p>
        </div>
      </div>
    </div>);
};
// Main Infinite Serenity Page
var InfiniteSerenityPage = function () {
    return (<div className="min-h-screen bg-gradient-to-br from-gray-100 via-white to-gray-50 relative overflow-hidden">
      {/* Infinite Serenity Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-gray-200/80 via-white/90 to-gray-100/70"/>

      {/* Navigation */}
      <CodexNavigation_1.default />

      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <InfiniteSerenity />
        </div>
      </main>

      {/* Ambient Serenity Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent pointer-events-none"/>

      {/* Peaceful Light Orbs */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-15">
        <div className="absolute top-1/6 left-1/6 w-32 h-32 bg-white/30 rounded-full filter blur-2xl animate-pulse" style={{ animationDuration: '12s' }}/>
        <div className="absolute bottom-1/6 right-1/6 w-36 h-36 bg-gray-200/25 rounded-full filter blur-2xl animate-pulse" style={{ animationDuration: '14s', animationDelay: '2s' }}/>
        <div className="absolute top-1/2 right-1/8 w-28 h-28 bg-white/35 rounded-full filter blur-2xl animate-pulse" style={{ animationDuration: '16s', animationDelay: '4s' }}/>
        <div className="absolute bottom-1/3 left-1/8 w-40 h-40 bg-gray-100/20 rounded-full filter blur-2xl animate-pulse" style={{ animationDuration: '18s', animationDelay: '6s' }}/>
        <div className="absolute top-3/4 left-1/3 w-24 h-24 bg-white/40 rounded-full filter blur-2xl animate-pulse" style={{ animationDuration: '20s', animationDelay: '8s' }}/>
        <div className="absolute bottom-1/2 right-1/3 w-44 h-44 bg-gray-50/25 rounded-full filter blur-2xl animate-pulse" style={{ animationDuration: '22s', animationDelay: '10s' }}/>
      </div>
    </div>);
};
exports.default = InfiniteSerenityPage;
