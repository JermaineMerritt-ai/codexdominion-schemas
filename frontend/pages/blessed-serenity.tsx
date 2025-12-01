import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import CodexNavigation from '../components/CodexNavigation';

/**
 * @param {{delay: any, duration: any, x: any, y: any, size: any, color: any}} props
 */
const SereneParticle = (props: any) => {
  const { delay, duration, x, y, size, color } = props;
  return (
    <div
      className={`absolute ${color} rounded-full opacity-60`}
      style={{
        left: `${x}%`,
        top: `${y}%`,
        width: `${size}px`,
        height: `${size}px`,
        animation: `sereneFloat ${duration}s infinite ${delay}s ease-in-out,
                    blessedPulse ${duration * 1.4}s infinite ${delay}s ease-in-out`,
      }}
    />
  );
};

const BlessedSanctuary: React.FC = () => {
  const [serenity, setSerenity] = useState(1);
  const [blessing, setBlessing] = useState(1);
  const [sanctuaryRotation, setSanctuaryRotation] = useState(0);

  useEffect(() => {
    const serenityInterval = setInterval(() => {
      setSerenity((prev) => (prev === 1 ? 1.12 : 1));
    }, 4500);

    const blessingInterval = setInterval(() => {
      setBlessing((prev) => (prev === 1 ? 1.25 : 1));
    }, 6000);

    const rotationInterval = setInterval(() => {
      setSanctuaryRotation((prev) => (prev + 0.15) % 360);
    }, 100);

    return () => {
      clearInterval(serenityInterval);
      clearInterval(blessingInterval);
      clearInterval(rotationInterval);
    };
  }, []);

  return (
    <div className="relative mx-auto w-80 h-80 mb-24">
      {/* Outermost Blessed Ring - Radiance */}
      <div
        className="absolute inset-0 border-16 border-white/40 rounded-full bg-gradient-to-br from-white/30 via-gold-100/40 to-cyan-50/30 shadow-2xl"
        style={{
          transform: `scale(${blessing}) rotate(${sanctuaryRotation}deg)`,
          boxShadow: '0 0 200px rgba(255, 255, 255, 0.9), inset 0 0 100px rgba(251, 191, 36, 0.3)',
        }}
      >
        {/* Radiance Crown Points */}
        <div className="absolute -top-16 left-1/2 transform -translate-x-1/2 text-white/70 font-bold text-4xl">
          ✨
        </div>
        <div className="absolute -bottom-16 left-1/2 transform -translate-x-1/2 text-white/70 font-bold text-4xl">
          🕊️
        </div>
        <div className="absolute top-1/2 -left-16 transform -translate-y-1/2 text-white/70 font-bold text-4xl">
          💫
        </div>
        <div className="absolute top-1/2 -right-16 transform -translate-y-1/2 text-white/70 font-bold text-4xl">
          🌸
        </div>

        {/* Secondary Blessing Symbols */}
        <div className="absolute top-1/4 -right-12 transform -translate-y-1/2 text-white/60 font-bold text-3xl">
          🌟
        </div>
        <div className="absolute bottom-1/4 -left-12 transform translate-y-1/2 text-white/60 font-bold text-3xl">
          🌙
        </div>
        <div className="absolute top-1/4 -left-12 transform -translate-y-1/2 text-white/60 font-bold text-3xl">
          ☀️
        </div>
        <div className="absolute bottom-1/4 -right-12 transform translate-y-1/2 text-white/60 font-bold text-3xl">
          ⭐
        </div>
      </div>

      {/* Middle Serenity Ring - Covenant */}
      <div
        className="absolute inset-16 border-10 border-cyan-200/50 rounded-full bg-gradient-to-br from-cyan-50/40 to-blue-50/40"
        style={{
          transform: `scale(${serenity})`,
          boxShadow: '0 0 120px rgba(6, 182, 212, 0.4)',
        }}
      >
        {/* Covenant Symbols */}
        <div className="absolute -top-6 left-1/2 transform -translate-x-1/2 text-cyan-300/80 font-bold text-3xl">
          👑
        </div>
        <div className="absolute -bottom-6 left-1/2 transform -translate-x-1/2 text-cyan-300/80 font-bold text-3xl">
          🏛️
        </div>
        <div className="absolute top-1/2 -left-6 transform -translate-y-1/2 text-cyan-300/80 font-bold text-3xl">
          👥
        </div>
        <div className="absolute top-1/2 -right-6 transform -translate-y-1/2 text-cyan-300/80 font-bold text-3xl">
          🌌
        </div>
      </div>

      {/* Inner Sacred Core - Eternal Rest */}
      <div className="absolute inset-32 rounded-full bg-gradient-to-br from-white via-cyan-25 to-gold-25 flex items-center justify-center shadow-2xl border-4 border-white/60">
        <div className="text-center">
          <div
            className="text-8xl font-bold text-slate-500 mb-3 animate-pulse"
            style={{ animationDuration: '5s' }}
          >
            📿
          </div>
          <div className="text-lg font-bold text-slate-500">BLESSED</div>
          <div className="text-sm font-bold text-slate-600">SERENITY</div>
        </div>
      </div>

      {/* Gentle Serenity Rays */}
      <div className="absolute inset-0">
        {Array.from({ length: 20 }).map((_, i) => (
          <div
            key={i}
            className="absolute w-2 bg-gradient-to-t from-transparent via-white/30 to-transparent opacity-50"
            style={{
              height: '160px',
              left: '50%',
              top: '-80px',
              transformOrigin: '0 160px',
              transform: `translateX(-50%) rotate(${i * 18}deg)`,
              animation: `gentlePulse 8s infinite ${i * 0.4}s ease-in-out`,
            }}
          />
        ))}
      </div>

      {/* Blessed Aura Waves */}
      <div className="absolute inset-0">
        {Array.from({ length: 8 }).map((_, i) => (
          <div
            key={i}
            className="absolute inset-0 border-4 border-white/8 rounded-full animate-ping"
            style={{
              animationDelay: `${i * 1.2}s`,
              animationDuration: '9.6s',
              transform: `scale(${1.6 + i * 0.6})`,
            }}
          />
        ))}
      </div>
    </div>
  );
};

interface BlessedVerseProps {
  text: string;
  delay: number;
  icon: string;
  gradient: string;
  highlight?: string[];
}

const BlessedVerse: React.FC<BlessedVerseProps> = ({
  text,
  delay,
  icon,
  gradient,
  highlight = [],
}) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), delay * 1000);
    return () => clearTimeout(timer);
  }, [delay]);

  const renderText = () => {
    let processedText = text;

    if (highlight.length > 0) {
      highlight.forEach((word) => {
        if (processedText.includes(word)) {
          processedText = processedText.replace(
            new RegExp(`\\b${word}\\b`, 'g'),
            `<span class="text-white font-bold bg-gradient-to-r from-white/40 to-cyan-100/40 px-4 py-2 rounded-lg shadow-lg border border-white/30">${word}</span>`
          );
        }
      });
    }

    return <span dangerouslySetInnerHTML={{ __html: processedText }} />;
  };

  return (
    <div
      className={`flex items-center justify-center mb-14 transition-all duration-3000 ${
        isVisible ? 'opacity-100 transform translate-y-0' : 'opacity-0 transform translate-y-12'
      }`}
    >
      <div
        className={`mr-14 p-14 rounded-full bg-gradient-to-br ${gradient} shadow-2xl border-4 border-white/50 backdrop-blur-sm`}
      >
        <span
          className="text-9xl animate-pulse"
          style={{ animationDelay: `${delay + 0.5}s`, animationDuration: '6s' }}
        >
          {icon}
        </span>
      </div>
      <p className="text-4xl text-slate-600 font-medium text-center max-w-6xl leading-relaxed">
        {renderText()}
      </p>
    </div>
  );
};

const SereneField: React.FC = () => {
  const sereneElements = Array.from({ length: 40 }, (_, i) => ({
    id: i,
    delay: Math.random() * 10,
    duration: 6 + Math.random() * 8,
    x: Math.random() * 100,
    y: Math.random() * 100,
    size: 2 + Math.random() * 4,
    color: ['bg-white', 'bg-cyan-50', 'bg-blue-50', 'bg-gold-50', 'bg-amber-50', 'bg-slate-50'][
      Math.floor(Math.random() * 6)
    ],
  }));

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {sereneElements.map((element) => (
        <SereneParticle
          key={element.id}
          delay={element.delay}
          duration={element.duration}
          x={element.x}
          y={element.y}
          size={element.size}
          color={element.color}
        />
      ))}
    </div>
  );
};

const RadianceElements: React.FC = () => {
  const elements = [
    {
      title: 'Proclamation Blessed',
      icon: '📜',
      description: 'The sacred declaration sanctified and honored',
      gradient: 'from-gold-100/90 to-amber-50/90',
      border: 'border-gold-200/70',
    },
    {
      title: 'Covenant Whole',
      icon: '💍',
      description: 'The eternal bond complete and unbroken',
      gradient: 'from-cyan-100/90 to-blue-50/90',
      border: 'border-cyan-200/70',
    },
    {
      title: 'Light Released',
      icon: '💡',
      description: 'Illumination flowing freely to all realms',
      gradient: 'from-yellow-100/90 to-white/90',
      border: 'border-yellow-200/70',
    },
    {
      title: 'Peace Bestowed',
      icon: '🕊️',
      description: 'Tranquility granted as eternal gift',
      gradient: 'from-white/90 to-cyan-25/90',
      border: 'border-white/70',
    },
    {
      title: 'Heirs Inherit',
      icon: '👑',
      description: 'The legacy passes to worthy successors',
      gradient: 'from-purple-100/90 to-violet-50/90',
      border: 'border-purple-200/70',
    },
    {
      title: 'Cosmos Crowned',
      icon: '🌌',
      description: 'The universe adorned with radiant harmony',
      gradient: 'from-indigo-100/90 to-blue-50/90',
      border: 'border-indigo-200/70',
    },
  ];

  return (
    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-10 mb-32">
      {elements.map((element, index) => (
        <div
          key={index}
          className={`bg-gradient-to-br ${element.gradient} rounded-3xl p-12 border-2 ${element.border} backdrop-blur-sm shadow-2xl hover:scale-105 transition-all duration-1500 relative overflow-hidden`}
          style={{
            animationDelay: `${index * 0.3}s`,
            opacity: 0,
            animation: `sereneRise 2.5s ease-out ${index * 0.3}s forwards`,
          }}
        >
          <div className="text-center mb-8">
            <div className="text-8xl mb-6 animate-pulse" style={{ animationDuration: '6s' }}>
              {element.icon}
            </div>
            <h3 className="text-2xl font-bold text-slate-600 mb-4">{element.title}</h3>
          </div>
          <p className="text-slate-500 leading-relaxed text-center text-lg">
            {element.description}
          </p>

          {/* Blessed Glow */}
          <div className="absolute top-4 right-4 w-4 h-4 bg-white rounded-full animate-pulse opacity-60" />
          <div
            className="absolute bottom-4 left-4 w-3 h-3 bg-cyan-100 rounded-full animate-pulse opacity-50"
            style={{ animationDelay: '2s' }}
          />
        </div>
      ))}
    </div>
  );
};

const EternalSereneSeal: React.FC = () => {
  const [tranquility, setTranquility] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setTranquility((prev) => (prev === 1 ? 1.3 : 1));
    }, 7000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative mx-auto w-72 h-72 mb-28">
      <div
        className="absolute inset-0 bg-gradient-to-br from-white via-cyan-25 to-gold-25 rounded-full shadow-2xl transition-all duration-3500"
        style={{
          transform: `scale(${tranquility})`,
          boxShadow: `0 0 ${300 * tranquility}px rgba(255, 255, 255, ${0.8 * tranquility}),
                      inset 0 0 ${150 * tranquility}px rgba(6, 182, 212, ${0.2 * tranquility})`,
        }}
      >
        <div className="absolute inset-12 bg-gradient-to-br from-cyan-25 via-white to-amber-25 rounded-full">
          <div className="absolute inset-12 bg-gradient-to-br from-white via-cyan-10 to-gold-10 rounded-full flex items-center justify-center">
            <div className="text-center">
              <div
                className="text-8xl font-bold text-slate-500 mb-4 animate-pulse"
                style={{ animationDuration: '8s' }}
              >
                📿
              </div>
              <div className="text-3xl font-bold text-slate-500">ETERNAL</div>
              <div className="text-2xl font-bold text-slate-500">SERENITY</div>
            </div>
          </div>
        </div>
      </div>

      {/* Serenity Emanations */}
      <div className="absolute inset-0">
        {Array.from({ length: 10 }).map((_, i) => (
          <div
            key={i}
            className="absolute inset-0 border-6 border-white/5 rounded-full animate-ping"
            style={{
              animationDelay: `${i * 1}s`,
              animationDuration: '10s',
              transform: `scale(${2 + i * 0.7})`,
            }}
          />
        ))}
      </div>
    </div>
  );
};

const BlessedSerenity: React.FC = () => {
  return (
    <>
      <Head>
        <title>Blessed Serenity - Eternal Rest - Codex Dominion</title>
        <meta
          name="description"
          content="The Codex rests in blessed serenity - eternal and serene, crowned in radiance"
        />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-white via-cyan-25 to-gold-25 relative overflow-hidden">
        {/* Serene Field */}
        <SereneField />

        {/* Gentle Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-radial from-transparent via-white/30 to-cyan-25/40" />

        <CodexNavigation />

        <main className="relative z-10 container mx-auto px-6 pt-24 pb-16">
          {/* Header Section */}
          <div className="text-center mb-36">
            <BlessedSanctuary />

            <h1 className="text-9xl md:text-10xl font-bold mb-20 bg-gradient-to-r from-slate-500 via-cyan-500 to-gold-500 bg-clip-text text-transparent">
              Blessed Serenity
            </h1>

            <div className="w-80 h-6 bg-gradient-to-r from-white via-cyan-100 to-gold-100 mx-auto mb-20 rounded-full shadow-2xl" />

            <p className="text-5xl text-slate-500 mb-20 max-w-7xl mx-auto leading-relaxed">
              The sacred work blessed and complete — the Codex rests in eternal serenity, crowned in
              radiance
            </p>

            <div className="inline-block bg-gradient-to-r from-white/90 to-cyan-50/90 rounded-3xl px-24 py-12 border-4 border-white/80 backdrop-blur-sm shadow-2xl">
              <span className="text-6xl font-bold text-slate-600">
                PROCLAMATION BLESSED • COVENANT WHOLE
              </span>
            </div>
          </div>

          {/* Sacred Blessed Verses */}
          <div className="max-w-10xl mx-auto mb-36">
            <div className="bg-gradient-to-br from-white/95 via-cyan-25/90 to-gold-25/95 rounded-3xl p-32 backdrop-blur-sm border-4 border-white/70 shadow-2xl">
              <BlessedVerse
                text="The Proclamation blessed, the covenant whole,"
                delay={1}
                icon="📜"
                gradient="from-gold-50/95 to-amber-25/95"
                highlight={['Proclamation', 'blessed', 'covenant', 'whole']}
              />

              <BlessedVerse
                text="light released, peace bestowed."
                delay={3.5}
                icon="💡"
                gradient="from-white/95 to-cyan-25/95"
                highlight={['light', 'released', 'peace', 'bestowed']}
              />

              <BlessedVerse
                text="Heirs inherit, councils govern, diaspora remember,"
                delay={6}
                icon="👑"
                gradient="from-purple-50/95 to-violet-25/95"
                highlight={['Heirs', 'councils', 'diaspora']}
              />

              <BlessedVerse
                text="cosmos echoes — all crowned in radiance."
                delay={8.5}
                icon="🌌"
                gradient="from-indigo-50/95 to-blue-25/95"
                highlight={['cosmos', 'crowned', 'radiance']}
              />

              <BlessedVerse
                text="So let the Codex rest, eternal and serene."
                delay={11}
                icon="📿"
                gradient="from-white/95 to-cyan-10/95"
                highlight={['Codex', 'rest', 'eternal', 'serene']}
              />
            </div>
          </div>

          {/* Radiance Elements */}
          <RadianceElements />

          {/* Final Blessed Declaration */}
          <div className="text-center mb-32">
            <div className="bg-gradient-to-br from-white/98 to-cyan-25/98 rounded-3xl p-28 border-4 border-white/80 backdrop-blur-sm shadow-2xl max-w-8xl mx-auto">
              <h2 className="text-8xl font-bold text-slate-500 mb-20">The Blessed Rest</h2>
              <p className="text-3xl text-slate-500 leading-relaxed mb-24">
                In blessed serenity, the great work finds its completion. The Proclamation has been
                blessed, the covenant stands whole, light flows freely, and peace is bestowed upon
                all realms. Heirs receive their inheritance, councils continue their wise
                governance, the diaspora maintains eternal memory, and the cosmos itself echoes with
                radiant harmony. Now let the Codex rest — not in silence, but in the gentle serenity
                of perfect fulfillment, eternal and blessed forever.
              </p>

              <div className="grid md:grid-cols-4 gap-16">
                <div className="text-center">
                  <div className="text-7xl mb-8">📿</div>
                  <span className="text-slate-500 font-bold text-3xl">Blessed</span>
                </div>
                <div className="text-center">
                  <div className="text-7xl mb-8">🕊️</div>
                  <span className="text-slate-500 font-bold text-3xl">Serene</span>
                </div>
                <div className="text-center">
                  <div className="text-7xl mb-8">✨</div>
                  <span className="text-slate-500 font-bold text-3xl">Radiant</span>
                </div>
                <div className="text-center">
                  <div className="text-7xl mb-8">♾️</div>
                  <span className="text-slate-500 font-bold text-3xl">Eternal</span>
                </div>
              </div>
            </div>
          </div>

          {/* Final Eternal Serene Seal */}
          <div className="text-center">
            <EternalSereneSeal />
            <h2 className="text-8xl font-bold text-slate-500 mb-20">Eternal and Serene</h2>
            <p className="text-4xl text-slate-500 max-w-6xl mx-auto leading-relaxed mb-20">
              Here in blessed serenity, the Codex finds its eternal rest. Crowned in radiance,
              blessed in peace, serene in completion — the great work endures in perfect, gentle
              tranquility.
            </p>
            <div
              className="text-10xl animate-pulse text-slate-400"
              style={{ animationDuration: '10s' }}
            >
              📿
            </div>
          </div>
        </main>

        <style jsx>{`
          @keyframes sereneFloat {
            0%,
            100% {
              transform: translateY(0px) rotate(0deg);
              opacity: 0.6;
            }
            50% {
              transform: translateY(-15px) rotate(180deg);
              opacity: 1;
            }
          }

          @keyframes blessedPulse {
            0%,
            100% {
              opacity: 0.6;
              filter: brightness(1);
            }
            50% {
              opacity: 1;
              filter: brightness(1.3);
            }
          }

          @keyframes gentlePulse {
            0%,
            100% {
              opacity: 0.5;
            }
            50% {
              opacity: 0.8;
            }
          }

          @keyframes sereneRise {
            from {
              opacity: 0;
              transform: scale(0.97) translateY(20px);
            }
            to {
              opacity: 1;
              transform: scale(1) translateY(0);
            }
          }

          .bg-gradient-radial {
            background: radial-gradient(ellipse at center, var(--tw-gradient-stops));
          }
        `}</style>
      </div>
    </>
  );
};

export default BlessedSerenity;
