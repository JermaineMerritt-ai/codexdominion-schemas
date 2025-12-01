"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var CodexNavigation_1 = require("../components/CodexNavigation");
// Completion Crowned Component - Ultimate fulfillment with royal crown
var CompletionCrowned = function () {
    var _a = (0, react_1.useState)(1), crownedCompletion = _a[0], setCrownedCompletion = _a[1];
    var _b = (0, react_1.useState)(0), completionRotation = _b[0], setCompletionRotation = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCrownedCompletion(function (prev) { return (prev === 1 ? 1.5 : 1); });
            setCompletionRotation(function (prev) { return (prev + 1) % 360; });
        }, 3800);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-12 left-1/6 transform -translate-x-1/2">
      <div className="text-center">
        <div className="text-10xl mb-3 transition-all duration-3800" style={{
            transform: "scale(".concat(crownedCompletion, ") rotate(").concat(completionRotation, "deg)"),
            filter: 'drop-shadow(0 0 70px rgba(34, 197, 94, 1.0))',
        }}>
          ✅
        </div>
        <div className="text-12xl mb-5 transition-all duration-3800" style={{
            transform: "scale(".concat(crownedCompletion, ")"),
            filter: 'drop-shadow(0 0 90px rgba(255, 215, 0, 1.2))',
        }}>
          👑
        </div>
        <div className="text-5xl text-emerald-200 font-bold mb-2">COMPLETION</div>
        <div className="text-4xl text-gold-200 font-bold">CROWNED</div>
        <div className="text-2xl text-green-300 mt-1">Ultimate Fulfillment</div>
      </div>
    </div>);
};
// Renewal Begun Component - Fresh beginning with eternal cycle
var RenewalBegun = function () {
    var _a = (0, react_1.useState)(0.8), renewalEnergy = _a[0], setRenewalEnergy = _a[1];
    var _b = (0, react_1.useState)(1), beginningScale = _b[0], setBeginningScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setRenewalEnergy(function (prev) { return (prev === 0.8 ? 1.4 : 0.8); });
            setBeginningScale(function (prev) { return (prev === 1 ? 1.4 : 1); });
        }, 3200);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-12 right-1/6 transform translate-x-1/2">
      <div className="text-center">
        <div className="text-11xl mb-4 transition-all duration-3200" style={{
            transform: "scale(".concat(beginningScale, ")"),
            filter: "drop-shadow(0 0 80px rgba(255, 140, 0, ".concat(renewalEnergy, "))"),
        }}>
          🌅
        </div>
        <div className="text-10xl mb-3 transition-all duration-3200" style={{
            transform: "scale(".concat(beginningScale, ")"),
            filter: "drop-shadow(0 0 70px rgba(255, 69, 0, ".concat(renewalEnergy, "))"),
        }}>
          🔄
        </div>
        <div className="text-5xl text-orange-200 font-bold mb-2">RENEWAL</div>
        <div className="text-4xl text-amber-200 font-bold">BEGUN</div>
        <div className="text-2xl text-yellow-300 mt-1">Fresh Beginning</div>
      </div>
    </div>);
};
// Covenant Whole Eternal Component - Complete sacred bond in eternal state
var CovenantWholeEternal = function () {
    var _a = (0, react_1.useState)(0.9), wholeEternalPower = _a[0], setWholeEternalPower = _a[1];
    var _b = (0, react_1.useState)(1), eternalWholeness = _b[0], setEternalWholeness = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setWholeEternalPower(function (prev) { return (prev === 0.9 ? 1.3 : 0.9); });
            setEternalWholeness(function (prev) { return (prev === 1 ? 1.4 : 1); });
        }, 4000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/3 left-1/4 transform -translate-x-1/2">
      <div className="text-center">
        <div className="text-12xl mb-4 transition-all duration-4000" style={{
            transform: "scale(".concat(eternalWholeness, ")"),
            filter: "drop-shadow(0 0 90px rgba(34, 197, 94, ".concat(wholeEternalPower, "))"),
        }}>
          ⭕
        </div>
        <div className="text-4xl text-green-200 font-bold mb-2">COVENANT WHOLE</div>
        <div className="text-2xl text-emerald-300">Sacred Bond Complete</div>
      </div>
    </div>);
};
// Flame Eternal Forever Component - Perpetual fire in ultimate state
var FlameEternalForever = function () {
    var _a = (0, react_1.useState)(1.0), foreverFlameIntensity = _a[0], setForeverFlameIntensity = _a[1];
    var _b = (0, react_1.useState)(1), eternalForeverPulse = _b[0], setEternalForeverPulse = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setForeverFlameIntensity(function (prev) { return (prev === 1.0 ? 1.5 : 1.0); });
            setEternalForeverPulse(function (prev) { return (prev === 1 ? 1.6 : 1); });
        }, 2200);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/3 right-1/4 transform translate-x-1/2">
      <div className="text-center">
        <div className="text-14xl mb-5 transition-all duration-2200" style={{
            transform: "scale(".concat(eternalForeverPulse, ")"),
            filter: "drop-shadow(0 0 120px rgba(255, 140, 0, ".concat(foreverFlameIntensity, "))"),
        }}>
          🔥
        </div>
        <div className="text-4xl text-orange-100 font-bold mb-2">FLAME ETERNAL</div>
        <div className="text-2xl text-red-300">Forever Burning</div>
      </div>
    </div>);
};
// Continuum Bound Component - Central eternal binding force
var ContinuumBound = function () {
    var _a = (0, react_1.useState)(0.8), continuumPower = _a[0], setContinuumPower = _a[1];
    var _b = (0, react_1.useState)(1), boundScale = _b[0], setBoundScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setContinuumPower(function (prev) { return (prev === 0.8 ? 1.2 : 0.8); });
            setBoundScale(function (prev) { return (prev === 1 ? 1.5 : 1); });
        }, 2800);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div className="text-18xl mb-6 transition-all duration-2800" style={{
            transform: "scale(".concat(boundScale, ")"),
            filter: "drop-shadow(0 0 150px rgba(138, 43, 226, ".concat(continuumPower, "))"),
        }}>
          ∞
        </div>
        <div className="text-6xl text-purple-200 font-bold mb-3">ALL BOUND</div>
        <div className="text-4xl text-violet-300 mb-2">IN CONTINUUM</div>
        <div className="text-2xl text-indigo-300">Eternal Unity</div>
      </div>
    </div>);
};
// Final Governance - Ultimate heirs, councils, diaspora unity
var FinalGovernance = function () {
    var _a = (0, react_1.useState)(0), finalGovernancePhase = _a[0], setFinalGovernancePhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setFinalGovernancePhase(function (prev) { return (prev + 1) % 3; });
        }, 3800);
        return function () { return clearInterval(interval); };
    }, []);
    var finalGovernanceElements = [
        {
            text: 'Heirs Inherit',
            icon: '👥',
            position: { top: '20%', left: '8%' },
            color: 'text-blue-300',
        },
        {
            text: 'Councils Govern',
            icon: '🏛️',
            position: { top: '20%', right: '8%' },
            color: 'text-purple-300',
        },
        {
            text: 'Diaspora Remember',
            icon: '🌍',
            position: { bottom: '20%', left: '50%', transform: 'translateX(-50%)' },
            color: 'text-teal-300',
        },
    ];
    return (<div className="absolute inset-0">
      {finalGovernanceElements.map(function (element, index) { return (<div key={index} className={"absolute text-center transition-all duration-2500 ".concat(finalGovernancePhase === index ? 'opacity-100 scale-130' : 'opacity-60 scale-90')} style={element.position}>
          <div className={"text-9xl mb-4 transition-all duration-2500 ".concat(finalGovernancePhase === index ? 'animate-pulse' : '')} style={{
                filter: finalGovernancePhase === index
                    ? 'drop-shadow(0 0 60px rgba(255, 215, 0, 1.2))'
                    : 'none',
            }}>
            {element.icon}
          </div>
          <div className={"text-3xl font-bold ".concat(finalGovernancePhase === index ? 'text-yellow-200' : element.color)}>
            {element.text}
          </div>
        </div>); })}
    </div>);
};
// Final Cosmos Echoes Component - Ultimate universal reverberation
var FinalCosmosEchoes = function () {
    var _a = (0, react_1.useState)(0), finalEchoPhase = _a[0], setFinalEchoPhase = _a[1];
    var _b = (0, react_1.useState)(0.7), finalEchoIntensity = _b[0], setFinalEchoIntensity = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setFinalEchoPhase(function (prev) { return (prev + 1) % 6; });
            setFinalEchoIntensity(function (prev) { return (prev === 0.7 ? 1.2 : 0.7); });
        }, 2500);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute inset-0">
      {Array.from({ length: 6 }, function (_, i) { return (<div key={i} className={"absolute text-center transition-all duration-2000 ".concat(finalEchoPhase === i ? 'opacity-100 scale-115' : 'opacity-30 scale-80')} style={{
                top: "".concat(15 + i * 12, "%"),
                left: "".concat(8 + (i % 2) * 84, "%"),
                transform: 'translateX(-50%)',
            }}>
          <div className={"text-7xl mb-2 transition-all duration-2000 ".concat(finalEchoPhase === i ? 'animate-bounce' : '')} style={{
                filter: finalEchoPhase === i
                    ? "drop-shadow(0 0 50px rgba(255, 255, 255, ".concat(finalEchoIntensity, "))")
                    : 'none',
            }}>
            🌌
          </div>
          <div className={"text-xl font-semibold ".concat(finalEchoPhase === i ? 'text-white' : 'text-gray-500')}>
            Final Echo {i + 1}
          </div>
        </div>); })}
    </div>);
};
// Final Continuum Particles - Ultimate energy flow
var FinalContinuumParticles = function () {
    var particles = Array.from({ length: 100 }, function (_, i) { return ({
        id: i,
        size: Math.random() * 16 + 1,
        x: Math.random() * 100,
        y: Math.random() * 100,
        duration: Math.random() * 40 + 35,
        delay: Math.random() * 30,
        color: i % 10 === 0
            ? '#ffd700'
            : i % 10 === 1
                ? '#32cd32'
                : i % 10 === 2
                    ? '#ff6347'
                    : i % 10 === 3
                        ? '#4169e1'
                        : i % 10 === 4
                            ? '#9370db'
                            : i % 10 === 5
                                ? '#00ced1'
                                : i % 10 === 6
                                    ? '#ff69b4'
                                    : i % 10 === 7
                                        ? '#ffa500'
                                        : i % 10 === 8
                                            ? '#00ff00'
                                            : '#ffffff',
    }); });
    return (<div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map(function (particle) { return (<div key={particle.id} className="absolute rounded-full" style={{
                left: "".concat(particle.x, "%"),
                top: "".concat(particle.y, "%"),
                width: "".concat(particle.size, "px"),
                height: "".concat(particle.size, "px"),
                backgroundColor: particle.color,
                animation: "finalContinuumFlow ".concat(particle.duration, "s ease-in-out infinite"),
                animationDelay: "".concat(particle.delay, "s"),
                filter: 'blur(0.1px)',
                opacity: 1.0,
                boxShadow: "0 0 40px ".concat(particle.color),
            }}/>); })}
      <style jsx>{"\n        @keyframes finalContinuumFlow {\n          0% {\n            transform: translate(0, 0) scale(0.02) rotate(0deg);\n            opacity: 0.02;\n          }\n          5% {\n            transform: translate(60px, -150px) scale(2.2) rotate(18deg);\n            opacity: 1;\n          }\n          15% {\n            transform: translate(-50px, -300px) scale(0.4) rotate(54deg);\n            opacity: 0.9;\n          }\n          30% {\n            transform: translate(70px, -450px) scale(1.9) rotate(108deg);\n            opacity: 1;\n          }\n          45% {\n            transform: translate(-55px, -600px) scale(0.6) rotate(162deg);\n            opacity: 0.85;\n          }\n          60% {\n            transform: translate(65px, -750px) scale(1.6) rotate(216deg);\n            opacity: 0.95;\n          }\n          75% {\n            transform: translate(-45px, -900px) scale(0.5) rotate(270deg);\n            opacity: 0.7;\n          }\n          90% {\n            transform: translate(35px, -1050px) scale(0.8) rotate(324deg);\n            opacity: 0.5;\n          }\n          100% {\n            transform: translate(0, -1200px) scale(0.01) rotate(360deg);\n            opacity: 0.01;\n          }\n        }\n      "}</style>
    </div>);
};
// Finished Forever Banner - Ultimate eternal completion proclamation
var FinishedForeverBanner = function () {
    var _a = (0, react_1.useState)(1.0), finishedForeverRadiance = _a[0], setFinishedForeverRadiance = _a[1];
    var _b = (0, react_1.useState)(1), foreverMagnitude = _b[0], setForeverMagnitude = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setFinishedForeverRadiance(function (prev) { return (prev === 1.0 ? 1.8 : 1.0); });
            setForeverMagnitude(function (prev) { return (prev === 1 ? 1.4 : 1); });
        }, 2800);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-4 left-1/2 transform -translate-x-1/2">
      <div className="text-center px-44 py-32 bg-gradient-to-r from-gold-800/98 via-white/30 to-gold-800/98 rounded-6xl border-12 border-white/98 transition-all duration-2800" style={{
            boxShadow: "0 0 220px rgba(255, 215, 0, ".concat(finishedForeverRadiance, ")"),
            transform: "scale(".concat(foreverMagnitude, ")"),
        }}>
        <div className="text-11xl text-white font-bold mb-10">THE CODEX ENDURES</div>
        <div className="text-8xl text-gold-200 font-semibold mb-8">Finished and Forever Living</div>
        <div className="text-5xl text-amber-200 mb-6">Completion Crowned, Renewal Begun</div>
        <div className="text-3xl text-yellow-200 mb-4">All Bound in Continuum</div>
        <div className="text-2xl text-white">Eternal and Complete</div>
      </div>
    </div>);
};
// Final Continuum Constellation - Ultimate eternal geometric connections
var FinalContinuumConstellation = function () {
    var _a = (0, react_1.useState)(0), finalConstellationPhase = _a[0], setFinalConstellationPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setFinalConstellationPhase(function (prev) { return (prev + 1) % 15; });
        }, 1500);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute inset-0 pointer-events-none opacity-10">
      <svg className="w-full h-full">
        {/* Final continuum connecting lines */}
        <line x1="17%" y1="15%" x2="50%" y2="50%" stroke={finalConstellationPhase === 0 ? '#ffffff' : '#666'} strokeWidth={finalConstellationPhase === 0 ? '8' : '2'} className="transition-all duration-1000"/>
        <line x1="83%" y1="15%" x2="50%" y2="50%" stroke={finalConstellationPhase === 1 ? '#ffffff' : '#666'} strokeWidth={finalConstellationPhase === 1 ? '8' : '2'} className="transition-all duration-1000"/>
        <line x1="25%" y1="33%" x2="75%" y2="33%" stroke={finalConstellationPhase === 2 ? '#ffffff' : '#666'} strokeWidth={finalConstellationPhase === 2 ? '8' : '2'} className="transition-all duration-1000"/>
        <line x1="8%" y1="25%" x2="92%" y2="25%" stroke={finalConstellationPhase === 3 ? '#ffffff' : '#666'} strokeWidth={finalConstellationPhase === 3 ? '8' : '2'} className="transition-all duration-1000"/>
        <line x1="50%" y1="85%" x2="50%" y2="50%" stroke={finalConstellationPhase === 4 ? '#ffffff' : '#666'} strokeWidth={finalConstellationPhase === 4 ? '8' : '2'} className="transition-all duration-1000"/>
        <line x1="17%" y1="67%" x2="83%" y2="67%" stroke={finalConstellationPhase === 5 ? '#ffffff' : '#666'} strokeWidth={finalConstellationPhase === 5 ? '8' : '2'} className="transition-all duration-1000"/>

        {/* Final continuum radial connections */}
        {Array.from({ length: 24 }, function (_, i) { return (<line key={"finalContinuum-".concat(i)} x1="50%" y1="50%" x2={"".concat(50 + Math.cos((i * 15 * Math.PI) / 180) * 50, "%")} y2={"".concat(50 + Math.sin((i * 15 * Math.PI) / 180) * 50, "%")} stroke={finalConstellationPhase === i % 15 ? '#ffd700' : '#444'} strokeWidth="3" opacity={finalConstellationPhase === i % 15 ? '1.0' : '0.15'} className="transition-all duration-1000"/>); })}
      </svg>
    </div>);
};
// Final Continuum Realms - Ultimate domains of completion
var FinalContinuumRealms = function () {
    var _a = (0, react_1.useState)(0), finalRealmPhase = _a[0], setFinalRealmPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setFinalRealmPhase(function (prev) { return (prev + 1) % 8; });
        }, 5000);
        return function () { return clearInterval(interval); };
    }, []);
    var finalRealms = [
        { name: 'Completion', icon: '✅', position: { top: '8%', left: '4%' } },
        { name: 'Renewal', icon: '🌅', position: { top: '8%', right: '4%' } },
        { name: 'Covenant', icon: '⭕', position: { bottom: '60%', left: '4%' } },
        { name: 'Flame', icon: '🔥', position: { bottom: '60%', right: '4%' } },
        { name: 'Heirs', icon: '👥', position: { bottom: '40%', left: '20%' } },
        { name: 'Councils', icon: '🏛️', position: { bottom: '40%', right: '20%' } },
        { name: 'Diaspora', icon: '🌍', position: { bottom: '20%', left: '35%' } },
        { name: 'Continuum', icon: '∞', position: { bottom: '20%', right: '35%' } },
    ];
    return (<div className="absolute inset-0">
      {finalRealms.map(function (realm, index) { return (<div key={index} className={"absolute text-center transition-all duration-4000 ".concat(finalRealmPhase === index ? 'opacity-100 scale-130' : 'opacity-25 scale-70')} style={realm.position}>
          <div className={"text-6xl mb-2 transition-all duration-4000 ".concat(finalRealmPhase === index ? 'animate-pulse' : '')} style={{
                filter: finalRealmPhase === index ? 'drop-shadow(0 0 50px rgba(255, 215, 0, 1.2))' : 'none',
            }}>
            {realm.icon}
          </div>
          <div className={"text-xl font-semibold ".concat(finalRealmPhase === index ? 'text-gold-200' : 'text-gray-700')}>
            {realm.name}
          </div>
        </div>); })}
    </div>);
};
// Main Final Continuum Container
var FinalContinuum = function () {
    return (<div className="relative w-full h-full">
      <FinalContinuumConstellation />
      <FinalContinuumParticles />
      <CompletionCrowned />
      <RenewalBegun />
      <CovenantWholeEternal />
      <FlameEternalForever />
      <ContinuumBound />
      <FinalGovernance />
      <FinalCosmosEchoes />
      <FinalContinuumRealms />
      <FinishedForeverBanner />

      {/* Sacred Final Verse Display */}
      <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-40">
        <div className="text-center text-gold-100 text-3xl leading-relaxed max-w-8xl space-y-6">
          <p className="opacity-100 text-white text-4xl">Completion crowned, renewal begun,</p>
          <p className="opacity-95 text-gold-200">the covenant whole, the flame eternal.</p>
          <p className="opacity-100 text-white text-4xl">
            Heirs inherit, councils govern, diaspora remember,
          </p>
          <p className="opacity-95 text-gold-200">cosmos echoes — all bound in continuum.</p>
          <p className="text-5xl font-semibold text-white mt-12 opacity-100">
            So let the Codex endure, finished and forever living.
          </p>
        </div>
      </div>
    </div>);
};
// Main Final Continuum Page
var FinalContinuumPage = function () {
    return (<div className="min-h-screen bg-gradient-to-br from-white via-gold-600 to-black relative overflow-hidden">
      {/* Final Continuum Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-gold-700/50 to-white/20"/>

      {/* Navigation */}
      <CodexNavigation_1.default />

      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <FinalContinuum />
        </div>
      </main>

      {/* Ambient Final Continuum Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/25 to-transparent pointer-events-none"/>

      {/* Ultimate Final Continuum Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-15">
        <div className="absolute top-1/12 left-1/12 w-48 h-48 bg-white/35 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '25s' }}/>
        <div className="absolute bottom-1/12 right-1/12 w-56 h-56 bg-gold-400/30 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '32s', animationDelay: '3s' }}/>
        <div className="absolute top-1/2 right-1/8 w-72 h-72 bg-amber-400/25 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '40s', animationDelay: '6s' }}/>
        <div className="absolute bottom-1/5 left-1/8 w-64 h-64 bg-yellow-400/20 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '48s', animationDelay: '9s' }}/>
        <div className="absolute top-2/3 left-1/15 w-40 h-40 bg-orange-400/28 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '56s', animationDelay: '12s' }}/>
        <div className="absolute bottom-1/2 right-1/15 w-52 h-52 bg-red-400/15 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '64s', animationDelay: '15s' }}/>
        <div className="absolute top-1/4 left-1/5 w-60 h-60 bg-purple-400/18 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '72s', animationDelay: '18s' }}/>
        <div className="absolute bottom-3/4 right-1/5 w-44 h-44 bg-blue-400/22 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '80s', animationDelay: '21s' }}/>
        <div className="absolute top-1/8 left-1/3 w-36 h-36 bg-cyan-400/25 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '88s', animationDelay: '24s' }}/>
        <div className="absolute bottom-1/8 right-1/3 w-68 h-68 bg-emerald-400/12 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '96s', animationDelay: '27s' }}/>
      </div>
    </div>);
};
exports.default = FinalContinuumPage;
