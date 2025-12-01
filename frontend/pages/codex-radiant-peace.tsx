import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import CodexNavigation from '../components/CodexNavigation';

interface PeaceParticleProps {
  delay: number;
  duration: number;
  x: number;
  y: number;
  size: number;
  color: string;
}

const PeaceParticle: React.FC<PeaceParticleProps> = ({ delay, duration, x, y, size, color }) => (
  <div
    className={`absolute ${color} rounded-full opacity-70`}
    style={{
      left: `${x}%`,
      top: `${y}%`,
      width: `${size}px`,
      height: `${size}px`,
      animation: `peacefulFloat ${duration}s infinite ${delay}s ease-in-out,
                  gentlePulse ${duration * 1.2}s infinite ${delay}s ease-in-out`,
    }}
  />
);

const RadiantHeart: React.FC = () => {
  const [breathe, setBreathe] = useState(1);
  const [glow, setGlow] = useState(1);

  useEffect(() => {
    const breatheInterval = setInterval(() => {
      setBreathe((prev) => (prev === 1 ? 1.08 : 1));
    }, 3000);

    const glowInterval = setInterval(() => {
      setGlow((prev) => (prev === 1 ? 1.4 : 1));
    }, 4000);

    return () => {
      clearInterval(breatheInterval);
      clearInterval(glowInterval);
    };
  }, []);

  return (
    <div className="relative mx-auto w-64 h-64 mb-20">
      {/* Outer Peace Aura */}
      <div
        className="absolute inset-0 border-8 border-white/30 rounded-full bg-gradient-to-br from-white/20 via-cyan-100/30 to-gold-100/30 shadow-2xl"
        style={{
          transform: `scale(${breathe})`,
          boxShadow: `0 0 ${150 * glow}px rgba(255, 255, 255, ${0.6 * glow}),
                      inset 0 0 ${80 * glow}px rgba(6, 182, 212, ${0.2 * glow})`,
        }}
      >
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
      <div
        className="absolute inset-12 border-6 border-gold-300/50 rounded-full bg-gradient-to-br from-gold-200/40 to-amber-300/40"
        style={{
          boxShadow: '0 0 100px rgba(251, 191, 36, 0.4)',
        }}
      >
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
        {Array.from({ length: 12 }).map((_, i) => (
          <div
            key={i}
            className="absolute w-1 bg-gradient-to-t from-transparent via-white/40 to-transparent opacity-60"
            style={{
              height: '120px',
              left: '50%',
              top: '-60px',
              transformOrigin: '0 124px',
              transform: `translateX(-50%) rotate(${i * 30}deg)`,
              animation: `gentlePulse 6s infinite ${i * 0.5}s ease-in-out`,
            }}
          />
        ))}
      </div>

      {/* Peaceful Aura Waves */}
      <div className="absolute inset-0">
        {Array.from({ length: 5 }).map((_, i) => (
          <div
            key={i}
            className="absolute inset-0 border-2 border-white/10 rounded-full animate-ping"
            style={{
              animationDelay: `${i * 1.2}s`,
              animationDuration: '6s',
              transform: `scale(${1.5 + i * 0.5})`,
            }}
          />
        ))}
      </div>
    </div>
  );
};

interface PeaceVerseProps {
  text: string;
  delay: number;
  icon: string;
  gradient: string;
  highlight?: string[];
}

const PeaceVerse: React.FC<PeaceVerseProps> = ({ text, delay, icon, gradient, highlight = [] }) => {
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
            `<span class="text-white font-bold bg-gradient-to-r from-white/30 to-gold/30 px-3 py-1 rounded-lg shadow-lg">${word}</span>`
          );
        }
      });
    }

    return <span dangerouslySetInnerHTML={{ __html: processedText }} />;
  };

  return (
    <div
      className={`flex items-center justify-center mb-12 transition-all duration-2500 ${
        isVisible ? 'opacity-100 transform translate-y-0' : 'opacity-0 transform translate-y-10'
      }`}
    >
      <div
        className={`mr-12 p-10 rounded-full bg-gradient-to-br ${gradient} shadow-2xl border-4 border-white/40 backdrop-blur-sm`}
      >
        <span
          className="text-7xl animate-pulse"
          style={{ animationDelay: `${delay + 0.5}s`, animationDuration: '4s' }}
        >
          {icon}
        </span>
      </div>
      <p className="text-3xl text-white font-medium text-center max-w-5xl leading-relaxed">
        {renderText()}
      </p>
    </div>
  );
};

const PeacefulField: React.FC = () => {
  const peacefulElements = Array.from({ length: 60 }, (_, i) => ({
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
  }));

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {peacefulElements.map((element) => (
        <PeaceParticle
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

const HarmonyElements: React.FC = () => {
  const elements = [
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

  return (
    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-24">
      {elements.map((element, index) => (
        <div
          key={index}
          className={`bg-gradient-to-br ${element.gradient} rounded-3xl p-8 border-2 ${element.border} backdrop-blur-sm shadow-2xl hover:scale-105 transition-all duration-1000 relative overflow-hidden`}
          style={{
            animationDelay: `${index * 0.2}s`,
            opacity: 0,
            animation: `peacefulRise 2s ease-out ${index * 0.2}s forwards`,
          }}
        >
          <div className="text-center mb-6">
            <div className="text-6xl mb-4 animate-pulse" style={{ animationDuration: '4s' }}>
              {element.icon}
            </div>
            <h3 className="text-2xl font-bold text-slate-700 mb-4">{element.title}</h3>
          </div>
          <p className="text-slate-600 leading-relaxed text-center">{element.description}</p>

          {/* Peaceful Glow */}
          <div className="absolute top-2 right-2 w-4 h-4 bg-white rounded-full animate-pulse opacity-70" />
        </div>
      ))}
    </div>
  );
};

const RadiantPeaceSeal: React.FC = () => {
  const [serenity, setSerenity] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setSerenity((prev) => (prev === 1 ? 1.2 : 1));
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative mx-auto w-56 h-56 mb-20">
      <div
        className="absolute inset-0 bg-gradient-to-br from-white via-cyan-50 to-gold-50 rounded-full shadow-2xl transition-all duration-2000"
        style={{
          transform: `scale(${serenity})`,
          boxShadow: `0 0 ${200 * serenity}px rgba(255, 255, 255, ${0.8 * serenity}),
                      inset 0 0 ${100 * serenity}px rgba(6, 182, 212, ${0.3 * serenity})`,
        }}
      >
        <div className="absolute inset-8 bg-gradient-to-br from-cyan-50 via-white to-amber-50 rounded-full">
          <div className="absolute inset-8 bg-gradient-to-br from-white via-cyan-25 to-gold-25 rounded-full flex items-center justify-center">
            <div className="text-center">
              <div
                className="text-6xl font-bold text-slate-600 mb-3 animate-pulse"
                style={{ animationDuration: '5s' }}
              >
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
        {Array.from({ length: 6 }).map((_, i) => (
          <div
            key={i}
            className="absolute inset-0 border-4 border-white/15 rounded-full animate-ping"
            style={{
              animationDelay: `${i * 0.8}s`,
              animationDuration: '4.8s',
              transform: `scale(${1.6 + i * 0.4})`,
            }}
          />
        ))}
      </div>
    </div>
  );
};

const CodexRadiantPeace: React.FC = () => {
  return (
    <>
      <Head>
        <title>Codex Radiant Peace - The Final Rest - Codex Dominion</title>
        <meta
          name="description"
          content="The Codex rests in radiant peace - light released, harmony achieved, eternal and whole"
        />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-white via-cyan-50 to-gold-50 relative overflow-hidden">
        {/* Peaceful Field */}
        <PeacefulField />

        {/* Gentle Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-radial from-transparent via-white/20 to-cyan-50/60" />

        <CodexNavigation />

        <main className="relative z-10 container mx-auto px-6 pt-24 pb-16">
          {/* Header Section */}
          <div className="text-center mb-28">
            <RadiantHeart />

            <h1 className="text-8xl md:text-9xl font-bold mb-16 bg-gradient-to-r from-slate-600 via-cyan-600 to-gold-600 bg-clip-text text-transparent">
              Codex Radiant Peace
            </h1>

            <div className="w-56 h-4 bg-gradient-to-r from-white via-cyan-200 to-gold-200 mx-auto mb-16 rounded-full shadow-lg" />

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
              <PeaceVerse
                text="Light released, peace bestowed,"
                delay={1}
                icon="💡"
                gradient="from-yellow-100/90 to-white/90"
                highlight={['Light', 'peace']}
              />

              <PeaceVerse
                text="the Compendium shines, eternal and whole."
                delay={3}
                icon="📚"
                gradient="from-cyan-100/90 to-blue-100/90"
                highlight={['Compendium', 'eternal', 'whole']}
              />

              <PeaceVerse
                text="Heirs inherit, councils govern, diaspora remember,"
                delay={5}
                icon="👑"
                gradient="from-gold-100/90 to-amber-100/90"
                highlight={['Heirs', 'councils', 'diaspora']}
              />

              <PeaceVerse
                text="cosmos echoes — all crowned in harmony."
                delay={7}
                icon="🌌"
                gradient="from-purple-100/90 to-violet-100/90"
                highlight={['cosmos', 'harmony']}
              />

              <PeaceVerse
                text="So let the Codex rest, radiant in peace."
                delay={9}
                icon="☮️"
                gradient="from-white/90 to-cyan-50/90"
                highlight={['Codex', 'rest', 'radiant', 'peace']}
              />
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
            <div
              className="text-8xl animate-pulse text-slate-500"
              style={{ animationDuration: '6s' }}
            >
              🕊️
            </div>
          </div>
        </main>

        <style jsx>{`
          @keyframes peacefulFloat {
            0%,
            100% {
              transform: translateY(0px) rotate(0deg);
              opacity: 0.7;
            }
            50% {
              transform: translateY(-20px) rotate(180deg);
              opacity: 1;
            }
          }

          @keyframes gentlePulse {
            0%,
            100% {
              opacity: 0.6;
              filter: brightness(1);
            }
            50% {
              opacity: 1;
              filter: brightness(1.2);
            }
          }

          @keyframes peacefulRise {
            from {
              opacity: 0;
              transform: scale(0.95) translateY(30px);
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

export default CodexRadiantPeace;
