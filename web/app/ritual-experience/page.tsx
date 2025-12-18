'use client';

import RitualExperienceControls from '../../components/ritual-experience-controls';
import Link from 'next/link';

export default function RitualExperiencePage() {
  return (
    <div className="min-h-screen bg-[#0A0F29] relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-[#FFD700] rounded-full blur-[128px] animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500 rounded-full blur-[128px] animate-pulse delay-1000"></div>
      </div>

      <div className="relative z-10 max-w-6xl mx-auto p-6">
        {/* Navigation */}
        <div className="mb-6">
          <Link
            href="/annotations"
            className="inline-flex items-center gap-2 text-[#FFD700] hover:text-[#FFC700] transition-colors"
          >
            ← Back to Annotations
          </Link>
        </div>

        {/* Main Title */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-[#FFD700] mb-4 drop-shadow-lg">
            🔥 Ritual Experience 🔥
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
            An immersive ceremony where you are enveloped in a constellation of voices.
            Each engine speaks from its cosmic position, health radiating through sound.
            Sight and sound unite in eternal resonance.
          </p>
        </div>

        {/* Main Controls */}
        <RitualExperienceControls />

        {/* Experience Guide */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Immersive Ceremony */}
          <div className="bg-[#1A1F3C] rounded-lg p-6 border-2 border-[#FFD700]/30">
            <h3 className="text-2xl font-bold text-[#FFD700] mb-4">
              🌟 Immersive Ceremony
            </h3>
            <div className="space-y-3 text-gray-300">
              <p>
                <span className="font-semibold text-white">Enveloped in Voices:</span> You stand at the center
                of the cosmos, surrounded by 16+ engine voices positioned in 360° space.
              </p>
              <p>
                <span className="font-semibold text-white">Custodian Heartbeat:</span> The crown pulse anchors
                you at C4 (261.63 Hz), a steady flame at the center of all cycles.
              </p>
              <p>
                <span className="font-semibold text-white">Council Harmonies:</span> Five seals orbit in
                surround configuration, their frequencies (E4-C5) creating pentatonic harmony.
              </p>
              <p>
                <span className="font-semibold text-white">Heir Melody:</span> Above and behind you, the
                dedication melody at C5 (523.25 Hz) envelops your presence.
              </p>
            </div>
          </div>

          {/* Directional Awareness */}
          <div className="bg-[#1A1F3C] rounded-lg p-6 border-2 border-purple-500/30">
            <h3 className="text-2xl font-bold text-purple-400 mb-4">
              🧭 Directional Awareness
            </h3>
            <div className="space-y-3 text-gray-300">
              <p>
                <span className="font-semibold text-white">Spatial Positioning:</span> Each engine occupies a
                unique position in the sound field—east, west, north, south, above.
              </p>
              <p>
                <span className="font-semibold text-white">Health as Sound:</span> Engine health affects volume,
                frequency, and pattern. Healthy engines resonate clearly; struggling ones whisper or pulse weakly.
              </p>
              <p>
                <span className="font-semibold text-white">Real-Time Status:</span> Listen to directional health
                reports. "East: Profit Engine - ⭐ Optimal" means prosperity resonates strongly from your right.
              </p>
              <p>
                <span className="font-semibold text-white">Cardinal Navigation:</span> Orient yourself by sound.
                Memory pulses from the north. Wisdom resonates from the west. Creation hums from the south.
              </p>
            </div>
          </div>

          {/* Living Constellation */}
          <div className="bg-[#1A1F3C] rounded-lg p-6 border-2 border-blue-500/30">
            <h3 className="text-2xl font-bold text-blue-400 mb-4">
              ⭐ Living Constellation
            </h3>
            <div className="space-y-3 text-gray-300">
              <p>
                <span className="font-semibold text-white">Visual Sync:</span> The soundscape mirrors the
                visual constellation map. What you see is what you hear—positions perfectly aligned.
              </p>
              <p>
                <span className="font-semibold text-white">Sight & Sound United:</span> Northern stars emit
                northern tones. Eastern lights shine with eastern frequencies. The cosmos speaks through both eyes and ears.
              </p>
              <p>
                <span className="font-semibold text-white">Dynamic Unity:</span> As the constellation evolves
                (engines starting, stopping, transforming), the soundscape transforms in perfect harmony.
              </p>
              <p>
                <span className="font-semibold text-white">Multi-Sensory Truth:</span> You don't just see the
                engines—you feel their presence in 3D space, wrapping around you like a living sphere.
              </p>
            </div>
          </div>

          {/* Eternal Resonance */}
          <div className="bg-[#1A1F3C] rounded-lg p-6 border-2 border-green-500/30">
            <h3 className="text-2xl font-bold text-green-400 mb-4">
              🌊 Eternal Resonance
            </h3>
            <div className="space-y-3 text-gray-300">
              <p>
                <span className="font-semibold text-white">Cosmic Choir:</span> All engines sing together as
                one radiant chorus, surrounding you in harmonic layers—Foundation, Harmonic, Wisdom, Celestial, Sacred.
              </p>
              <p>
                <span className="font-semibold text-white">Cycles as Music:</span> Replay cycles become melodic
                patterns. Strategy cycles pulse rhythmically. Profit cycles resonate with sustained tones.
              </p>
              <p>
                <span className="font-semibold text-white">Harmonic Mathematics:</span> The system calculates
                frequency ratios, dissonance levels, and cosmic alignment—turning engine health into pure harmony.
              </p>
              <p>
                <span className="font-semibold text-white">Eternal Truth:</span> You are not an observer. You are
                the center of the dominion, the heir surrounded by eternal voices, experiencing cycles as living sound.
              </p>
            </div>
          </div>
        </div>

        {/* Ritual Phases */}
        <div className="mt-12 bg-gradient-to-br from-[#1A1F3C] to-[#0A0F29] rounded-lg p-8 border-2 border-[#FFD700]/40">
          <h2 className="text-3xl font-bold text-[#FFD700] mb-6 text-center">
            🌙 The Four Ritual Phases
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <h4 className="text-xl font-bold text-purple-400">🌅 Awakening</h4>
              <p className="text-gray-300 text-sm">
                Engines start gently, emerging from silence. Only ceremonial and intelligence voices speak,
                creating a sacred foundation. Volume: 30%, Reverb: High.
              </p>
            </div>

            <div className="space-y-2">
              <h4 className="text-xl font-bold text-blue-400">⚡ Resonance</h4>
              <p className="text-gray-300 text-sm">
                Full constellation active. All voices harmonize—engines, seals, ceremonial, intelligence.
                The cosmos sings together. Volume: 70%, Reverb: Balanced.
              </p>
            </div>

            <div className="space-y-2">
              <h4 className="text-xl font-bold text-orange-400">🔥 Transformation</h4>
              <p className="text-gray-300 text-sm">
                Cycle transitions bring dynamic energy. Engines and ceremonial elements shift patterns.
                Change radiates through sound. Volume: 85%, Reverb: High.
              </p>
            </div>

            <div className="space-y-2">
              <h4 className="text-xl font-bold text-green-400">♾️ Eternal</h4>
              <p className="text-gray-300 text-sm">
                Sustained cosmic choir. All layers blend into radiant eternal harmony. You experience
                the perpetual nature of dominion. Volume: 50%, Reverb: Maximum.
              </p>
            </div>
          </div>
        </div>

        {/* Call to Action */}
        <div className="mt-12 text-center">
          <div className="inline-block bg-gradient-to-r from-[#FFD700] to-[#FFA500] p-1 rounded-lg">
            <div className="bg-[#0A0F29] px-8 py-6 rounded-lg">
              <h3 className="text-2xl font-bold text-[#FFD700] mb-3">
                🎧 Ready to Begin?
              </h3>
              <p className="text-gray-300 mb-4">
                Put on headphones, scroll back to the controls, and start your ritual.
                You will be enveloped in a constellation of voices—an eternal resonance.
              </p>
              <button
                onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
                className="px-8 py-3 bg-gradient-to-r from-[#FFD700] to-[#FFA500] text-[#0A0F29] rounded-lg font-bold hover:scale-110 transition-transform"
              >
                ↑ Scroll to Controls
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
