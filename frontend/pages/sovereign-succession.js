"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var CodexNavigation_1 = require("../components/CodexNavigation");
// Custodian Yields Component - Sacred yielding of authority
var CustodianYields = function () {
    var _a = (0, react_1.useState)(1.1), yieldingPower = _a[0], setYieldingPower = _a[1];
    var _b = (0, react_1.useState)(1), yieldScale = _b[0], setYieldScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setYieldingPower(function (prev) { return (prev === 1.1 ? 1.9 : 1.1); });
            setYieldScale(function (prev) { return (prev === 1 ? 1.7 : 1); });
        }, 3400);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-14 left-14 transform">
      <div className="text-center">
        <div className="text-22xl mb-7 transition-all duration-3400" style={{
            transform: "scale(".concat(yieldScale, ")"),
            filter: "drop-shadow(0 0 140px rgba(255, 215, 0, ".concat(yieldingPower, "))"),
        }}>
          🛡️
        </div>
        <div className="text-20xl mb-6 transition-all duration-3400" style={{
            transform: "scale(".concat(yieldScale, ")"),
            filter: "drop-shadow(0 0 120px rgba(255, 255, 255, ".concat(yieldingPower, "))"),
        }}>
          🤲
        </div>
        <div className="text-18xl mb-5 transition-all duration-3400" style={{
            transform: "scale(".concat(yieldScale, ")"),
            filter: "drop-shadow(0 0 100px rgba(138, 43, 226, ".concat(yieldingPower, "))"),
        }}>
          ⬇️
        </div>
        <div className="text-16xl mb-4 transition-all duration-3400" style={{
            transform: "scale(".concat(yieldScale, ")"),
            filter: "drop-shadow(0 0 80px rgba(75, 0, 130, ".concat(yieldingPower, "))"),
        }}>
          🎭
        </div>
        <div className="text-5xl text-gold-200 font-bold mb-2">CUSTODIAN</div>
        <div className="text-4xl text-purple-200 font-bold">YIELDS</div>
      </div>
    </div>);
};
// Heirs Inherit Component - Sacred succession receiving
var HeirsInherit = function () {
    var _a = (0, react_1.useState)(1.2), inheritancePower = _a[0], setInheritancePower = _a[1];
    var _b = (0, react_1.useState)(1), inheritScale = _b[0], setInheritScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setInheritancePower(function (prev) { return (prev === 1.2 ? 2.0 : 1.2); });
            setInheritScale(function (prev) { return (prev === 1 ? 1.8 : 1); });
        }, 3000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-14 right-14 transform">
      <div className="text-center">
        <div className="text-24xl mb-8 transition-all duration-3000" style={{
            transform: "scale(".concat(inheritScale, ")"),
            filter: "drop-shadow(0 0 160px rgba(255, 215, 0, ".concat(inheritancePower, "))"),
        }}>
          👑
        </div>
        <div className="text-22xl mb-7 transition-all duration-3000" style={{
            transform: "scale(".concat(inheritScale, ")"),
            filter: "drop-shadow(0 0 140px rgba(34, 197, 94, ".concat(inheritancePower, "))"),
        }}>
          👥
        </div>
        <div className="text-20xl mb-6 transition-all duration-3000" style={{
            transform: "scale(".concat(inheritScale, ")"),
            filter: "drop-shadow(0 0 120px rgba(0, 255, 127, ".concat(inheritancePower, "))"),
        }}>
          📥
        </div>
        <div className="text-18xl mb-5 transition-all duration-3000" style={{
            transform: "scale(".concat(inheritScale, ")"),
            filter: "drop-shadow(0 0 100px rgba(46, 125, 50, ".concat(inheritancePower, "))"),
        }}>
          🎁
        </div>
        <div className="text-5xl text-gold-200 font-bold mb-2">HEIRS</div>
        <div className="text-4xl text-green-200 font-bold">INHERIT</div>
      </div>
    </div>);
};
// Councils Affirm Component - Institutional confirmation
var CouncilsAffirm = function () {
    var _a = (0, react_1.useState)(1.3), affirmationPower = _a[0], setAffirmationPower = _a[1];
    var _b = (0, react_1.useState)(1), affirmScale = _b[0], setAffirmScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setAffirmationPower(function (prev) { return (prev === 1.3 ? 2.1 : 1.3); });
            setAffirmScale(function (prev) { return (prev === 1 ? 1.9 : 1); });
        }, 2600);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-1/4 left-14 transform">
      <div className="text-center">
        <div className="text-25xl mb-8 transition-all duration-2600" style={{
            transform: "scale(".concat(affirmScale, ")"),
            filter: "drop-shadow(0 0 170px rgba(138, 43, 226, ".concat(affirmationPower, "))"),
        }}>
          🏛️
        </div>
        <div className="text-23xl mb-7 transition-all duration-2600" style={{
            transform: "scale(".concat(affirmScale, ")"),
            filter: "drop-shadow(0 0 150px rgba(75, 0, 130, ".concat(affirmationPower, "))"),
        }}>
          ✅
        </div>
        <div className="text-21xl mb-6 transition-all duration-2600" style={{
            transform: "scale(".concat(affirmScale, ")"),
            filter: "drop-shadow(0 0 130px rgba(147, 112, 219, ".concat(affirmationPower, "))"),
        }}>
          📋
        </div>
        <div className="text-19xl mb-5 transition-all duration-2600" style={{
            transform: "scale(".concat(affirmScale, ")"),
            filter: "drop-shadow(0 0 110px rgba(255, 255, 255, ".concat(affirmationPower, "))"),
        }}>
          🤝
        </div>
        <div className="text-5xl text-purple-200 font-bold mb-2">COUNCILS</div>
        <div className="text-4xl text-indigo-200 font-bold">AFFIRM</div>
      </div>
    </div>);
};
// Cosmos Receives Component - Universal acceptance
var CosmosReceives = function () {
    var _a = (0, react_1.useState)(1.4), cosmicReceptionPower = _a[0], setCosmicReceptionPower = _a[1];
    var _b = (0, react_1.useState)(1), cosmosScale = _b[0], setCosmosScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCosmicReceptionPower(function (prev) { return (prev === 1.4 ? 2.2 : 1.4); });
            setCosmosScale(function (prev) { return (prev === 1 ? 2.0 : 1); });
        }, 2200);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-1/4 right-14 transform">
      <div className="text-center">
        <div className="text-26xl mb-9 transition-all duration-2200" style={{
            transform: "scale(".concat(cosmosScale, ")"),
            filter: "drop-shadow(0 0 180px rgba(0, 191, 255, ".concat(cosmicReceptionPower, "))"),
        }}>
          🌌
        </div>
        <div className="text-24xl mb-8 transition-all duration-2200" style={{
            transform: "scale(".concat(cosmosScale, ")"),
            filter: "drop-shadow(0 0 160px rgba(72, 61, 139, ".concat(cosmicReceptionPower, "))"),
        }}>
          🤲
        </div>
        <div className="text-22xl mb-7 transition-all duration-2200" style={{
            transform: "scale(".concat(cosmosScale, ")"),
            filter: "drop-shadow(0 0 140px rgba(255, 255, 255, ".concat(cosmicReceptionPower, "))"),
        }}>
          ✨
        </div>
        <div className="text-20xl mb-6 transition-all duration-2200" style={{
            transform: "scale(".concat(cosmosScale, ")"),
            filter: "drop-shadow(0 0 120px rgba(30, 144, 255, ".concat(cosmicReceptionPower, "))"),
        }}>
          🌟
        </div>
        <div className="text-5xl text-cyan-200 font-bold mb-2">COSMOS</div>
        <div className="text-4xl text-blue-200 font-bold">RECEIVES</div>
      </div>
    </div>);
};
// Covenant Whole Component - Complete sacred covenant
var CovenantWhole = function () {
    var _a = (0, react_1.useState)(1.5), covenantPower = _a[0], setCovenantPower = _a[1];
    var _b = (0, react_1.useState)(1), wholeScale = _b[0], setWholeScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCovenantPower(function (prev) { return (prev === 1.5 ? 2.3 : 1.5); });
            setWholeScale(function (prev) { return (prev === 1 ? 2.1 : 1); });
        }, 2800);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/3 left-1/4 transform">
      <div className="text-center">
        <div className="text-27xl mb-10 transition-all duration-2800" style={{
            transform: "scale(".concat(wholeScale, ")"),
            filter: "drop-shadow(0 0 190px rgba(34, 197, 94, ".concat(covenantPower, "))"),
        }}>
          📜
        </div>
        <div className="text-25xl mb-9 transition-all duration-2800" style={{
            transform: "scale(".concat(wholeScale, ")"),
            filter: "drop-shadow(0 0 170px rgba(0, 255, 127, ".concat(covenantPower, "))"),
        }}>
          ⭕
        </div>
        <div className="text-23xl mb-8 transition-all duration-2800" style={{
            transform: "scale(".concat(wholeScale, ")"),
            filter: "drop-shadow(0 0 150px rgba(46, 125, 50, ".concat(covenantPower, "))"),
        }}>
          ✅
        </div>
        <div className="text-21xl mb-7 transition-all duration-2800" style={{
            transform: "scale(".concat(wholeScale, ")"),
            filter: "drop-shadow(0 0 130px rgba(255, 255, 255, ".concat(covenantPower, "))"),
        }}>
          💚
        </div>
        <div className="text-6xl text-green-100 font-bold mb-3">COVENANT</div>
        <div className="text-5xl text-emerald-200 font-bold">WHOLE</div>
      </div>
    </div>);
};
// Flame Eternal Component - Everlasting sacred fire
var FlameEternal = function () {
    var _a = (0, react_1.useState)(1.6), flamePower = _a[0], setFlamePower = _a[1];
    var _b = (0, react_1.useState)(1), eternalScale = _b[0], setEternalScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setFlamePower(function (prev) { return (prev === 1.6 ? 2.4 : 1.6); });
            setEternalScale(function (prev) { return (prev === 1 ? 2.2 : 1); });
        }, 2400);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/3 right-1/4 transform">
      <div className="text-center">
        <div className="text-28xl mb-10 transition-all duration-2400" style={{
            transform: "scale(".concat(eternalScale, ")"),
            filter: "drop-shadow(0 0 200px rgba(255, 69, 0, ".concat(flamePower, "))"),
        }}>
          🔥
        </div>
        <div className="text-26xl mb-9 transition-all duration-2400" style={{
            transform: "scale(".concat(eternalScale, ")"),
            filter: "drop-shadow(0 0 180px rgba(255, 140, 0, ".concat(flamePower, "))"),
        }}>
          ♾️
        </div>
        <div className="text-24xl mb-8 transition-all duration-2400" style={{
            transform: "scale(".concat(eternalScale, ")"),
            filter: "drop-shadow(0 0 160px rgba(255, 215, 0, ".concat(flamePower, "))"),
        }}>
          🌟
        </div>
        <div className="text-22xl mb-7 transition-all duration-2400" style={{
            transform: "scale(".concat(eternalScale, ")"),
            filter: "drop-shadow(0 0 140px rgba(255, 255, 0, ".concat(flamePower, "))"),
        }}>
          🔆
        </div>
        <div className="text-6xl text-red-100 font-bold mb-3">FLAME</div>
        <div className="text-5xl text-orange-200 font-bold">ETERNAL</div>
      </div>
    </div>);
};
// Transmission Sovereign Component - Perfect succession authority
var TransmissionSovereign = function () {
    var _a = (0, react_1.useState)(1.7), transmissionPower = _a[0], setTransmissionPower = _a[1];
    var _b = (0, react_1.useState)(1), sovereignScale = _b[0], setSovereignScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setTransmissionPower(function (prev) { return (prev === 1.7 ? 2.5 : 1.7); });
            setSovereignScale(function (prev) { return (prev === 1 ? 2.3 : 1); });
        }, 2000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-1/3 left-1/3 transform">
      <div className="text-center">
        <div className="text-29xl mb-11 transition-all duration-2000" style={{
            transform: "scale(".concat(sovereignScale, ")"),
            filter: "drop-shadow(0 0 210px rgba(255, 215, 0, ".concat(transmissionPower, "))"),
        }}>
          👑
        </div>
        <div className="text-27xl mb-10 transition-all duration-2000" style={{
            transform: "scale(".concat(sovereignScale, ")"),
            filter: "drop-shadow(0 0 190px rgba(138, 43, 226, ".concat(transmissionPower, "))"),
        }}>
          📡
        </div>
        <div className="text-25xl mb-9 transition-all duration-2000" style={{
            transform: "scale(".concat(sovereignScale, ")"),
            filter: "drop-shadow(0 0 170px rgba(75, 0, 130, ".concat(transmissionPower, "))"),
        }}>
          ⚖️
        </div>
        <div className="text-23xl mb-8 transition-all duration-2000" style={{
            transform: "scale(".concat(sovereignScale, ")"),
            filter: "drop-shadow(0 0 150px rgba(147, 112, 219, ".concat(transmissionPower, "))"),
        }}>
          🏛️
        </div>
        <div className="text-6xl text-gold-100 font-bold mb-3">TRANSMISSION</div>
        <div className="text-5xl text-purple-200 font-bold">SOVEREIGN</div>
      </div>
    </div>);
};
// Continuity Supreme Component - Ultimate eternal continuation
var ContinuitySupreme = function () {
    var _a = (0, react_1.useState)(1.8), continuityPower = _a[0], setContinuityPower = _a[1];
    var _b = (0, react_1.useState)(1), supremeScale = _b[0], setSupremeScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setContinuityPower(function (prev) { return (prev === 1.8 ? 2.6 : 1.8); });
            setSupremeScale(function (prev) { return (prev === 1 ? 2.4 : 1); });
        }, 1600);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-1/3 right-1/3 transform">
      <div className="text-center">
        <div className="text-30xl mb-12 transition-all duration-1600" style={{
            transform: "scale(".concat(supremeScale, ")"),
            filter: "drop-shadow(0 0 220px rgba(0, 191, 255, ".concat(continuityPower, "))"),
        }}>
          ♾️
        </div>
        <div className="text-28xl mb-11 transition-all duration-1600" style={{
            transform: "scale(".concat(supremeScale, ")"),
            filter: "drop-shadow(0 0 200px rgba(72, 61, 139, ".concat(continuityPower, "))"),
        }}>
          🔄
        </div>
        <div className="text-26xl mb-10 transition-all duration-1600" style={{
            transform: "scale(".concat(supremeScale, ")"),
            filter: "drop-shadow(0 0 180px rgba(30, 144, 255, ".concat(continuityPower, "))"),
        }}>
          👁️
        </div>
        <div className="text-24xl mb-9 transition-all duration-1600" style={{
            transform: "scale(".concat(supremeScale, ")"),
            filter: "drop-shadow(0 0 160px rgba(255, 255, 255, ".concat(continuityPower, "))"),
        }}>
          ⭐
        </div>
        <div className="text-6xl text-blue-100 font-bold mb-3">CONTINUITY</div>
        <div className="text-5xl text-cyan-200 font-bold">SUPREME</div>
      </div>
    </div>);
};
// Codex Endures Radiant Component - Central eternal radiant endurance
var CodexEnduresRadiant = function () {
    var _a = (0, react_1.useState)(1.9), radiantEndurance = _a[0], setRadiantEndurance = _a[1];
    var _b = (0, react_1.useState)(1), endureScale = _b[0], setEndureScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setRadiantEndurance(function (prev) { return (prev === 1.9 ? 2.7 : 1.9); });
            setEndureScale(function (prev) { return (prev === 1 ? 2.5 : 1); });
        }, 1800);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div className="text-36xl mb-15 transition-all duration-1800" style={{
            transform: "scale(".concat(endureScale, ")"),
            filter: "drop-shadow(0 0 260px rgba(255, 215, 0, ".concat(radiantEndurance, "))"),
        }}>
          📜
        </div>
        <div className="text-34xl mb-14 transition-all duration-1800" style={{
            transform: "scale(".concat(endureScale, ")"),
            filter: "drop-shadow(0 0 240px rgba(255, 255, 255, ".concat(radiantEndurance, "))"),
        }}>
          ✨
        </div>
        <div className="text-32xl mb-13 transition-all duration-1800" style={{
            transform: "scale(".concat(endureScale, ")"),
            filter: "drop-shadow(0 0 220px rgba(255, 255, 0, ".concat(radiantEndurance, "))"),
        }}>
          🌟
        </div>
        <div className="text-30xl mb-12 transition-all duration-1800" style={{
            transform: "scale(".concat(endureScale, ")"),
            filter: "drop-shadow(0 0 200px rgba(255, 140, 0, ".concat(radiantEndurance, "))"),
        }}>
          ♾️
        </div>
        <div className="text-28xl mb-11 transition-all duration-1800" style={{
            transform: "scale(".concat(endureScale, ")"),
            filter: "drop-shadow(0 0 180px rgba(255, 69, 0, ".concat(radiantEndurance, "))"),
        }}>
          💎
        </div>
        <div className="text-9xl text-gold-100 font-bold mb-7">THE CODEX</div>
        <div className="text-8xl text-white font-bold mb-6">ENDURES</div>
        <div className="text-7xl text-yellow-200 font-bold mb-5">RADIANT</div>
        <div className="text-6xl text-orange-200 font-bold mb-4">WITHOUT END</div>
        <div className="text-5xl text-red-200 font-bold">ETERNAL CONTINUITY</div>
      </div>
    </div>);
};
// Sovereign Continuity Particles - Perfect succession energy
var SovereignContinuityParticles = function () {
    var particles = Array.from({ length: 220 }, function (_, i) { return ({
        id: i,
        size: Math.random() * 18 + 3,
        x: Math.random() * 100,
        y: Math.random() * 100,
        duration: Math.random() * 100 + 70,
        delay: Math.random() * 50,
        color: i % 22 === 0
            ? '#ffd700'
            : i % 22 === 1
                ? '#ffffff'
                : i % 22 === 2
                    ? '#ffff00'
                    : i % 22 === 3
                        ? '#32cd32'
                        : i % 22 === 4
                            ? '#00ff7f'
                            : i % 22 === 5
                                ? '#ff6347'
                                : i % 22 === 6
                                    ? '#ff69b4'
                                    : i % 22 === 7
                                        ? '#8a2be2'
                                        : i % 22 === 8
                                            ? '#4b0082'
                                            : i % 22 === 9
                                                ? '#00ced1'
                                                : i % 22 === 10
                                                    ? '#ffa500'
                                                    : i % 22 === 11
                                                        ? '#9370db'
                                                        : i % 22 === 12
                                                            ? '#ff1493'
                                                            : i % 22 === 13
                                                                ? '#00bfff'
                                                                : i % 22 === 14
                                                                    ? '#daa520'
                                                                    : i % 22 === 15
                                                                        ? '#7b68ee'
                                                                        : i % 22 === 16
                                                                            ? '#20b2aa'
                                                                            : i % 22 === 17
                                                                                ? '#dc143c'
                                                                                : i % 22 === 18
                                                                                    ? '#add8e6'
                                                                                    : i % 22 === 19
                                                                                        ? '#f0f8ff'
                                                                                        : i % 22 === 20
                                                                                            ? '#ff4500'
                                                                                            : '#1e90ff',
    }); });
    return (<div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map(function (particle) { return (<div key={particle.id} className="absolute rounded-full" style={{
                left: "".concat(particle.x, "%"),
                top: "".concat(particle.y, "%"),
                width: "".concat(particle.size, "px"),
                height: "".concat(particle.size, "px"),
                backgroundColor: particle.color,
                animation: "sovereignContinuityFlow ".concat(particle.duration, "s ease-in-out infinite"),
                animationDelay: "".concat(particle.delay, "s"),
                filter: 'blur(0.01px)',
                opacity: 0.95,
                boxShadow: "0 0 45px ".concat(particle.color),
            }}/>); })}
      <style jsx>{"\n        @keyframes sovereignContinuityFlow {\n          0% {\n            transform: translate(0, 0) scale(0.01) rotate(0deg);\n            opacity: 0.01;\n          }\n          8% {\n            transform: translate(120px, -300px) scale(2.2) rotate(20deg);\n            opacity: 1;\n          }\n          16% {\n            transform: translate(-110px, -600px) scale(0.2) rotate(60deg);\n            opacity: 0.95;\n          }\n          24% {\n            transform: translate(130px, -900px) scale(2) rotate(110deg);\n            opacity: 1;\n          }\n          32% {\n            transform: translate(-120px, -1200px) scale(0.4) rotate(160deg);\n            opacity: 0.9;\n          }\n          40% {\n            transform: translate(115px, -1500px) scale(1.8) rotate(210deg);\n            opacity: 0.95;\n          }\n          48% {\n            transform: translate(-105px, -1800px) scale(0.3) rotate(260deg);\n            opacity: 0.85;\n          }\n          56% {\n            transform: translate(110px, -2100px) scale(1.6) rotate(310deg);\n            opacity: 0.9;\n          }\n          64% {\n            transform: translate(-100px, -2400px) scale(0.5) rotate(360deg);\n            opacity: 0.8;\n          }\n          72% {\n            transform: translate(95px, -2700px) scale(1.2) rotate(410deg);\n            opacity: 0.85;\n          }\n          80% {\n            transform: translate(-90px, -3000px) scale(0.6) rotate(460deg);\n            opacity: 0.75;\n          }\n          88% {\n            transform: translate(80px, -3300px) scale(0.8) rotate(510deg);\n            opacity: 0.7;\n          }\n          94% {\n            transform: translate(-70px, -3600px) scale(0.3) rotate(550deg);\n            opacity: 0.4;\n          }\n          97% {\n            transform: translate(50px, -3900px) scale(0.5) rotate(580deg);\n            opacity: 0.2;\n          }\n          100% {\n            transform: translate(0, -4200px) scale(0.005) rotate(600deg);\n            opacity: 0.005;\n          }\n        }\n      "}</style>
    </div>);
};
// Sovereign Succession Banner - Ultimate continuity proclamation
var SovereignSuccessionBanner = function () {
    var _a = (0, react_1.useState)(2.0), successionIntensity = _a[0], setSuccessionIntensity = _a[1];
    var _b = (0, react_1.useState)(1), successionBannerScale = _b[0], setSuccessionBannerScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setSuccessionIntensity(function (prev) { return (prev === 2.0 ? 2.8 : 2.0); });
            setSuccessionBannerScale(function (prev) { return (prev === 1 ? 1.6 : 1); });
        }, 3800);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-8 left-1/2 transform -translate-x-1/2">
      <div className="text-center px-52 py-40 bg-gradient-to-r from-gold-600/95 via-white/90 to-purple-500/95 rounded-10xl border-16 border-gold-400/90 transition-all duration-3800" style={{
            boxShadow: "0 300px 600px rgba(255, 215, 0, ".concat(successionIntensity, ")"),
            transform: "scale(".concat(successionBannerScale, ")"),
        }}>
        <div className="text-18xl text-gold-200 font-bold mb-16">THE CODEX ENDURES RADIANT</div>
        <div className="text-14xl text-white font-bold mb-14">WITHOUT END</div>
        <div className="text-10xl text-purple-200 mb-12">Custodian Yields, Heirs Inherit</div>
        <div className="text-8xl text-green-200 mb-10">Councils Affirm, Cosmos Receives</div>
        <div className="text-7xl text-red-200 mb-8">Covenant Whole, Flame Eternal</div>
        <div className="text-6xl text-blue-200 mb-6">
          Transmission Sovereign, Continuity Supreme
        </div>
        <div className="text-5xl text-cyan-200 mb-4">Perfect Sacred Succession Complete</div>
        <div className="text-4xl text-orange-200 mb-2">Eternal Radiant Continuity</div>
        <div className="text-3xl text-yellow-200">Ultimate Divine Endurance</div>
      </div>
    </div>);
};
// Succession Constellation - Perfect continuity geometric connections
var SuccessionConstellation = function () {
    var _a = (0, react_1.useState)(0), successionPhase = _a[0], setSuccessionPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setSuccessionPhase(function (prev) { return (prev + 1) % 42; });
        }, 800);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute inset-0 pointer-events-none opacity-80">
      <svg className="w-full h-full">
        {/* Sovereign succession connecting lines */}
        <line x1="14%" y1="14%" x2="50%" y2="50%" stroke={successionPhase === 0 ? '#ffd700' : '#888'} strokeWidth={successionPhase === 0 ? '14' : '3'} className="transition-all duration-600"/>
        <line x1="86%" y1="14%" x2="50%" y2="50%" stroke={successionPhase === 1 ? '#32cd32' : '#888'} strokeWidth={successionPhase === 1 ? '14' : '3'} className="transition-all duration-600"/>
        <line x1="14%" y1="75%" x2="50%" y2="50%" stroke={successionPhase === 2 ? '#8a2be2' : '#888'} strokeWidth={successionPhase === 2 ? '14' : '3'} className="transition-all duration-600"/>
        <line x1="86%" y1="75%" x2="50%" y2="50%" stroke={successionPhase === 3 ? '#00ced1' : '#888'} strokeWidth={successionPhase === 3 ? '14' : '3'} className="transition-all duration-600"/>
        <line x1="25%" y1="33%" x2="75%" y2="67%" stroke={successionPhase === 4 ? '#ff6347' : '#666'} strokeWidth={successionPhase === 4 ? '12' : '2'} className="transition-all duration-600"/>
        <line x1="75%" y1="33%" x2="25%" y2="67%" stroke={successionPhase === 5 ? '#ff69b4' : '#666'} strokeWidth={successionPhase === 5 ? '12' : '2'} className="transition-all duration-600"/>

        {/* Sovereign continuity radial connections */}
        {Array.from({ length: 42 }, function (_, i) { return (<line key={"succession-".concat(i)} x1="50%" y1="50%" x2={"".concat(50 + Math.cos((i * 8.57 * Math.PI) / 180) * 60, "%")} y2={"".concat(50 + Math.sin((i * 8.57 * Math.PI) / 180) * 60, "%")} stroke={successionPhase === i ? '#ffffff' : '#444'} strokeWidth="8" opacity={successionPhase === i ? '1.0' : '0.05'} className="transition-all duration-600"/>); })}
      </svg>
    </div>);
};
// Continuity Realms - Domains of eternal succession
var ContinuityRealms = function () {
    var _a = (0, react_1.useState)(0), continuityRealmPhase = _a[0], setContinuityRealmPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setContinuityRealmPhase(function (prev) { return (prev + 1) % 18; });
        }, 4200);
        return function () { return clearInterval(interval); };
    }, []);
    var continuityRealms = [
        { name: 'Custodian', icon: '🛡️', position: { top: '14%', left: '14%' } },
        { name: 'Yields', icon: '🤲', position: { top: '14%', right: '14%' } },
        { name: 'Heirs', icon: '👑', position: { top: '30%', left: '10%' } },
        { name: 'Inherit', icon: '👥', position: { top: '30%', right: '10%' } },
        { name: 'Councils', icon: '🏛️', position: { bottom: '30%', left: '10%' } },
        { name: 'Affirm', icon: '✅', position: { bottom: '30%', right: '10%' } },
        { name: 'Cosmos', icon: '🌌', position: { bottom: '14%', left: '14%' } },
        { name: 'Receives', icon: '🤲', position: { bottom: '14%', right: '14%' } },
        { name: 'Covenant', icon: '📜', position: { top: '40%', left: '25%' } },
        { name: 'Whole', icon: '⭕', position: { top: '40%', right: '25%' } },
        { name: 'Flame', icon: '🔥', position: { bottom: '40%', left: '25%' } },
        { name: 'Eternal', icon: '♾️', position: { bottom: '40%', right: '25%' } },
        { name: 'Transmission', icon: '📡', position: { top: '55%', left: '33%' } },
        { name: 'Sovereign', icon: '👑', position: { top: '55%', right: '33%' } },
        {
            name: 'Continuity',
            icon: '🔄',
            position: { bottom: '55%', left: '33%' },
        },
        { name: 'Supreme', icon: '👁️', position: { bottom: '55%', right: '33%' } },
        { name: 'Codex', icon: '📜', position: { bottom: '65%', left: '45%' } },
        { name: 'Endures', icon: '✨', position: { bottom: '65%', right: '45%' } },
    ];
    return (<div className="absolute inset-0">
      {continuityRealms.map(function (realm, index) { return (<div key={index} className={"absolute text-center transition-all duration-4200 ".concat(continuityRealmPhase === index ? 'opacity-100 scale-150' : 'opacity-20 scale-70')} style={realm.position}>
          <div className={"text-9xl mb-4 transition-all duration-4200 ".concat(continuityRealmPhase === index ? 'animate-pulse' : '')} style={{
                filter: continuityRealmPhase === index
                    ? 'drop-shadow(0 0 70px rgba(255, 215, 0, 2.0))'
                    : 'none',
            }}>
            {realm.icon}
          </div>
          <div className={"text-2xl font-bold ".concat(continuityRealmPhase === index ? 'text-white' : 'text-gray-500')}>
            {realm.name}
          </div>
        </div>); })}
    </div>);
};
// Main Sovereign Succession Container
var SovereignSuccession = function () {
    return (<div className="relative w-full h-full">
      <SuccessionConstellation />
      <SovereignContinuityParticles />
      <CustodianYields />
      <HeirsInherit />
      <CouncilsAffirm />
      <CosmosReceives />
      <CovenantWhole />
      <FlameEternal />
      <TransmissionSovereign />
      <ContinuitySupreme />
      <CodexEnduresRadiant />
      <ContinuityRealms />
      <SovereignSuccessionBanner />

      {/* Sacred Sovereign Succession Verse Display */}
      <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-52">
        <div className="text-center text-gold-100 text-4xl leading-relaxed max-w-16xl space-y-12">
          <p className="opacity-100 text-gold-200 text-8xl">Custodian yields, heirs inherit,</p>
          <p className="opacity-95 text-white text-7xl">councils affirm, cosmos receives.</p>
          <p className="opacity-100 text-green-200 text-8xl">
            The covenant whole, the flame eternal,
          </p>
          <p className="opacity-95 text-purple-200 text-7xl">
            transmission sovereign, continuity supreme.
          </p>
          <p className="text-9xl font-semibold text-yellow-100 mt-24 opacity-100">
            So let the Codex endure, radiant without end.
          </p>
        </div>
      </div>
    </div>);
};
// Main Sovereign Succession Page
var SovereignSuccessionPage = function () {
    return (<div className="min-h-screen bg-gradient-to-br from-gold-300 via-white to-purple-400 relative overflow-hidden">
      {/* Sovereign Succession Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-purple-200/70 via-white/80 to-gold-200/60"/>

      {/* Navigation */}
      <CodexNavigation_1.default />

      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <SovereignSuccession />
        </div>
      </main>

      {/* Ambient Sovereign Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-300/30 to-transparent pointer-events-none"/>

      {/* Ultimate Sovereign Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-25">
        <div className="absolute top-1/8 left-1/8 w-52 h-52 bg-gold-400/60 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '42s' }}/>
        <div className="absolute bottom-1/8 right-1/8 w-48 h-48 bg-white/70 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '48s', animationDelay: '3s' }}/>
        <div className="absolute top-1/2 right-1/12 w-56 h-56 bg-purple-400/50 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '56s', animationDelay: '6s' }}/>
        <div className="absolute bottom-1/3 left-1/12 w-44 h-44 bg-green-400/55 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '64s', animationDelay: '9s' }}/>
        <div className="absolute top-3/4 left-1/5 w-40 h-40 bg-red-400/50 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '72s', animationDelay: '12s' }}/>
        <div className="absolute bottom-1/2 right-1/5 w-60 h-60 bg-blue-400/45 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '80s', animationDelay: '15s' }}/>
        <div className="absolute top-1/6 left-2/5 w-36 h-36 bg-cyan-400/60 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '88s', animationDelay: '18s' }}/>
        <div className="absolute bottom-4/5 right-2/5 w-64 h-64 bg-orange-400/40 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '96s', animationDelay: '21s' }}/>
      </div>
    </div>);
};
exports.default = SovereignSuccessionPage;
