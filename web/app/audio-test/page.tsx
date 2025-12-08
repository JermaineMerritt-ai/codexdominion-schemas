'use client';

import { useState } from 'react';

export default function AudioTestPage() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [audioContext, setAudioContext] = useState<AudioContext | null>(null);
  const [oscillator, setOscillator] = useState<OscillatorNode | null>(null);

  const startBasicTest = () => {
    // Your example code (updated to modern API)
    const audioCtx = new AudioContext();
    const source = audioCtx.createOscillator();
    const panner = audioCtx.createPanner();

    // Modern API: Use positionX/Y/Z instead of setPosition()
    panner.positionX.value = 1;
    panner.positionY.value = 0;
    panner.positionZ.value = -1;

    // Set panner model for 3D audio
    panner.panningModel = 'HRTF';
    panner.distanceModel = 'inverse';

    source.connect(panner).connect(audioCtx.destination);
    source.start();

    setAudioContext(audioCtx);
    setOscillator(source);
    setIsPlaying(true);

    console.log('🎵 Basic Web Audio API test started');
    console.log('Position: x=1, y=0, z=-1 (right and in front)');
  };

  const stopBasicTest = () => {
    if (oscillator) {
      oscillator.stop();
      oscillator.disconnect();
    }
    if (audioContext) {
      audioContext.close();
    }
    setIsPlaying(false);
    setOscillator(null);
    setAudioContext(null);

    console.log('🔇 Audio stopped');
  };

  return (
    <div className="min-h-screen bg-[#0A0F29] p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-[#FFD700] mb-6">
          🎵 Web Audio API Test
        </h1>

        {/* Basic Test */}
        <div className="bg-[#1A1F3C] rounded-lg p-6 border-2 border-[#FFD700]/30 mb-6">
          <h2 className="text-xl font-bold text-white mb-4">
            Basic Spatial Audio Test
          </h2>

          <div className="bg-[#0A0F29] rounded p-4 mb-4">
            <pre className="text-sm text-gray-300 overflow-x-auto">
{`const audioCtx = new AudioContext()
const source = audioCtx.createOscillator()
const panner = audioCtx.createPanner()

// Modern API (instead of deprecated setPosition)
panner.positionX.value = 1
panner.positionY.value = 0
panner.positionZ.value = -1

panner.panningModel = 'HRTF'
panner.distanceModel = 'inverse'

source.connect(panner).connect(audioCtx.destination)
source.start()`}
            </pre>
          </div>

          <div className="flex gap-3">
            <button
              onClick={startBasicTest}
              disabled={isPlaying}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                isPlaying
                  ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                  : 'bg-[#FFD700] text-[#0A0F29] hover:bg-[#FFC700] hover:scale-105'
              }`}
            >
              ▶️ Start Test
            </button>
            <button
              onClick={stopBasicTest}
              disabled={!isPlaying}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                !isPlaying
                  ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                  : 'bg-red-600 text-white hover:bg-red-700 hover:scale-105'
              }`}
            >
              ⏹️ Stop Test
            </button>
          </div>

          {isPlaying && (
            <div className="mt-4 p-3 bg-green-900/30 text-green-400 rounded border border-green-500/50">
              🎧 Playing sine wave at 440 Hz positioned at (1, 0, -1) - should sound from your right
            </div>
          )}
        </div>

        {/* Explanation */}
        <div className="bg-[#1A1F3C] rounded-lg p-6 border-2 border-purple-500/30">
          <h2 className="text-xl font-bold text-purple-400 mb-4">
            📚 Understanding Spatial Audio
          </h2>

          <div className="space-y-4 text-gray-300">
            <div>
              <h3 className="font-bold text-white mb-2">🎯 Position Coordinates:</h3>
              <ul className="list-disc list-inside space-y-1 text-sm">
                <li><span className="text-[#FFD700]">X-axis:</span> Left (-) to Right (+)</li>
                <li><span className="text-[#FFD700]">Y-axis:</span> Down (-) to Up (+)</li>
                <li><span className="text-[#FFD700]">Z-axis:</span> Behind (-) to Front (+)</li>
                <li><span className="text-purple-400">Position (1, 0, -1):</span> To the right and slightly in front</li>
              </ul>
            </div>

            <div>
              <h3 className="font-bold text-white mb-2">🔊 Panning Models:</h3>
              <ul className="list-disc list-inside space-y-1 text-sm">
                <li><span className="text-[#FFD700]">HRTF:</span> Head-Related Transfer Function - realistic 3D audio using ear shape</li>
                <li><span className="text-gray-400]">equalpower:</span> Simple stereo panning (less realistic)</li>
              </ul>
            </div>

            <div>
              <h3 className="font-bold text-white mb-2">📏 Distance Models:</h3>
              <ul className="list-disc list-inside space-y-1 text-sm">
                <li><span className="text-[#FFD700]">inverse:</span> Volume decreases as 1/distance (natural falloff)</li>
                <li><span className="text-gray-400]">linear:</span> Volume decreases linearly</li>
                <li><span className="text-gray-400]">exponential:</span> Rapid volume decrease</li>
              </ul>
            </div>

            <div className="bg-[#0A0F29] rounded p-4 mt-4">
              <h3 className="font-bold text-[#FFD700] mb-2">⚠️ API Updates:</h3>
              <p className="text-sm">
                The <code className="text-red-400">setPosition(x, y, z)</code> method is deprecated.
                Use modern AudioParam properties instead:
              </p>
              <pre className="text-xs text-green-400 mt-2 bg-black/30 p-2 rounded">
{`// ❌ Deprecated
panner.setPosition(1, 0, -1)

// ✅ Modern API
panner.positionX.value = 1
panner.positionY.value = 0
panner.positionZ.value = -1`}
              </pre>
            </div>
          </div>
        </div>

        {/* Link to Full Experience */}
        <div className="mt-6 text-center">
          <a
            href="/annotations"
            className="inline-block px-8 py-4 bg-gradient-to-r from-[#FFD700] to-[#FFA500] text-[#0A0F29] rounded-lg font-bold text-lg hover:scale-105 transition-transform"
          >
            🎵 Try Full Spatial Audio Experience →
          </a>
          <p className="text-gray-400 text-sm mt-2">
            Experience 23+ audio sources in 360° immersive soundscape
          </p>
        </div>
      </div>
    </div>
  );
}
