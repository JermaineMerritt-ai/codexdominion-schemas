import React, { useState } from 'react';
import Head from 'next/head';

interface Project {
  id: string;
  name: string;
  type: 'video' | 'graphic' | 'animation' | 'audio';
  status: 'queued' | 'generating' | 'completed' | 'failed';
  progress: number;
  thumbnail?: string;
  createdAt: Date;
}

interface AIModel {
  id: string;
  name: string;
  type: string;
  icon: string;
  status: 'active' | 'busy' | 'offline';
}

export default function AIGraphicVideoStudio() {
  const [activeTab, setActiveTab] = useState<'video' | 'graphic' | 'animation' | 'audio' | 'models'>('video');
  const [projects, setProjects] = useState<Project[]>([
    { id: '1', name: 'Product Demo Video', type: 'video', status: 'completed', progress: 100, createdAt: new Date() },
    { id: '2', name: 'Social Media Banner', type: 'graphic', status: 'generating', progress: 65, createdAt: new Date() },
    { id: '3', name: 'Logo Animation', type: 'animation', status: 'queued', progress: 0, createdAt: new Date() },
  ]);

  const aiModels: AIModel[] = [
    { id: '1', name: 'RunwayML Gen-3', type: 'Video Generation', icon: '🎬', status: 'active' },
    { id: '2', name: 'DALL-E 3', type: 'Image Generation', icon: '🖼️', status: 'active' },
    { id: '3', name: 'Midjourney', type: 'Artistic Design', icon: '🎨', status: 'active' },
    { id: '4', name: 'Stable Diffusion XL', type: 'Image Synthesis', icon: '🌟', status: 'active' },
    { id: '5', name: 'Pika Labs', type: 'Text-to-Video', icon: '📹', status: 'busy' },
    { id: '6', name: 'ElevenLabs', type: 'Voice Synthesis', icon: '🎙️', status: 'active' },
    { id: '7', name: 'GPT-4 Vision', type: 'Visual Analysis', icon: '👁️', status: 'active' },
    { id: '8', name: 'Adobe Firefly', type: 'Creative Suite', icon: '🔥', status: 'active' },
  ];

  const videoFormats = ['4K UHD (3840x2160)', 'Full HD (1920x1080)', 'HD (1280x720)', 'Social Square (1080x1080)', 'Social Story (1080x1920)'];
  const graphicFormats = ['Social Post (1080x1080)', 'Banner (1200x628)', 'Thumbnail (1280x720)', 'Logo (512x512)', 'eBook Cover (1600x2560)'];
  const animationStyles = ['Motion Graphics', 'Kinetic Typography', 'Character Animation', 'Particle Effects', 'Transition Effects'];

  return (
    <>
      <Head>
        <title>AI Graphic & Video Studio | CodexDominion</title>
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white p-6">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-5xl font-bold mb-2 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            🎨 AI Graphic & Video Studio
          </h1>
          <p className="text-gray-300 text-lg">Professional content creation powered by cutting-edge AI</p>
        </div>

        {/* Stats Bar */}
        <div className="grid grid-cols-4 gap-4 mb-8">
          <div className="bg-gray-800/50 backdrop-blur-lg rounded-xl p-4 border border-purple-500/30">
            <div className="text-3xl mb-2">🎬</div>
            <div className="text-2xl font-bold">24</div>
            <div className="text-sm text-gray-400">Videos Generated</div>
          </div>
          <div className="bg-gray-800/50 backdrop-blur-lg rounded-xl p-4 border border-pink-500/30">
            <div className="text-3xl mb-2">🖼️</div>
            <div className="text-2xl font-bold">156</div>
            <div className="text-sm text-gray-400">Graphics Created</div>
          </div>
          <div className="bg-gray-800/50 backdrop-blur-lg rounded-xl p-4 border border-blue-500/30">
            <div className="text-3xl mb-2">⚡</div>
            <div className="text-2xl font-bold">3</div>
            <div className="text-sm text-gray-400">Active Projects</div>
          </div>
          <div className="bg-gray-800/50 backdrop-blur-lg rounded-xl p-4 border border-green-500/30">
            <div className="text-3xl mb-2">🤖</div>
            <div className="text-2xl font-bold">8</div>
            <div className="text-sm text-gray-400">AI Models Active</div>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex space-x-2 mb-6">
          {['video', 'graphic', 'animation', 'audio', 'models'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab as any)}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                activeTab === tab
                  ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white'
                  : 'bg-gray-800/50 text-gray-400 hover:text-white hover:bg-gray-700/50'
              }`}
            >
              {tab === 'video' && '🎬 Video Generation'}
              {tab === 'graphic' && '🖼️ Graphic Design'}
              {tab === 'animation' && '✨ Animation Studio'}
              {tab === 'audio' && '🎵 Audio Generation'}
              {tab === 'models' && '🤖 AI Models'}
            </button>
          ))}
        </div>

        {/* Video Generation Tab */}
        {activeTab === 'video' && (
          <div className="grid grid-cols-3 gap-6">
            {/* Creation Panel */}
            <div className="col-span-2 bg-gray-800/50 backdrop-blur-lg rounded-xl p-6 border border-purple-500/30">
              <h2 className="text-2xl font-bold mb-4">🎬 Generate New Video</h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold mb-2">Project Name</label>
                  <input
                    type="text"
                    placeholder="My Amazing Video"
                    className="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg focus:border-purple-500 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-2">Video Script / Description</label>
                  <textarea
                    rows={4}
                    placeholder="Describe the video you want to create... Be specific about scenes, actions, style, and mood."
                    className="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg focus:border-purple-500 focus:outline-none resize-none"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold mb-2">Resolution</label>
                    <select className="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg focus:border-purple-500 focus:outline-none">
                      {videoFormats.map((format) => (
                        <option key={format}>{format}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold mb-2">Duration</label>
                    <select className="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg focus:border-purple-500 focus:outline-none">
                      <option>15 seconds</option>
                      <option>30 seconds</option>
                      <option>60 seconds</option>
                      <option>2 minutes</option>
                      <option>5 minutes</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-2">AI Model</label>
                  <div className="grid grid-cols-3 gap-2">
                    <button className="px-4 py-2 bg-purple-600 border-2 border-purple-400 rounded-lg font-semibold">RunwayML</button>
                    <button className="px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg hover:border-purple-500">Pika Labs</button>
                    <button className="px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg hover:border-purple-500">Stable Video</button>
                  </div>
                </div>

                <button className="w-full py-4 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg font-bold text-lg hover:opacity-90 transition-opacity">
                  🎬 Generate Video
                </button>
              </div>
            </div>

            {/* Recent Projects */}
            <div className="bg-gray-800/50 backdrop-blur-lg rounded-xl p-6 border border-purple-500/30">
              <h3 className="text-xl font-bold mb-4">📂 Recent Projects</h3>
              <div className="space-y-3">
                {projects.filter(p => p.type === 'video').map((project) => (
                  <div key={project.id} className="bg-gray-900/50 rounded-lg p-3 border border-gray-700">
                    <div className="flex justify-between items-start mb-2">
                      <div className="font-semibold text-sm">{project.name}</div>
                      <div className={`text-xs px-2 py-1 rounded ${
                        project.status === 'completed' ? 'bg-green-500/20 text-green-400' :
                        project.status === 'generating' ? 'bg-yellow-500/20 text-yellow-400' :
                        'bg-gray-500/20 text-gray-400'
                      }`}>
                        {project.status}
                      </div>
                    </div>
                    {project.status === 'generating' && (
                      <div className="w-full bg-gray-800 rounded-full h-2 overflow-hidden">
                        <div
                          className="bg-gradient-to-r from-purple-600 to-pink-600 h-full transition-all duration-300"
                          style={{ width: `${project.progress}%` }}
                        />
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Graphic Design Tab */}
        {activeTab === 'graphic' && (
          <div className="grid grid-cols-3 gap-6">
            {/* Creation Panel */}
            <div className="col-span-2 bg-gray-800/50 backdrop-blur-lg rounded-xl p-6 border border-pink-500/30">
              <h2 className="text-2xl font-bold mb-4">🖼️ Generate Graphics & Designs</h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold mb-2">Design Name</label>
                  <input
                    type="text"
                    placeholder="My Design Project"
                    className="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg focus:border-pink-500 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-2">Design Prompt</label>
                  <textarea
                    rows={4}
                    placeholder="Describe your design vision... Include colors, style, mood, and specific elements you want."
                    className="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg focus:border-pink-500 focus:outline-none resize-none"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold mb-2">Format</label>
                    <select className="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg focus:border-pink-500 focus:outline-none">
                      {graphicFormats.map((format) => (
                        <option key={format}>{format}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold mb-2">Style</label>
                    <select className="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg focus:border-pink-500 focus:outline-none">
                      <option>Photorealistic</option>
                      <option>Artistic/Painting</option>
                      <option>Minimalist</option>
                      <option>3D Rendered</option>
                      <option>Cartoon/Illustration</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-2">AI Model</label>
                  <div className="grid grid-cols-3 gap-2">
                    <button className="px-4 py-2 bg-pink-600 border-2 border-pink-400 rounded-lg font-semibold">DALL-E 3</button>
                    <button className="px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg hover:border-pink-500">Midjourney</button>
                    <button className="px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg hover:border-pink-500">Firefly</button>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-2">Variations to Generate</label>
                  <input
                    type="range"
                    min="1"
                    max="8"
                    defaultValue="4"
                    className="w-full"
                  />
                  <div className="text-sm text-gray-400 text-center">4 variations</div>
                </div>

                <button className="w-full py-4 bg-gradient-to-r from-pink-600 to-purple-600 rounded-lg font-bold text-lg hover:opacity-90 transition-opacity">
                  🖼️ Generate Design
                </button>
              </div>
            </div>

            {/* Templates Gallery */}
            <div className="bg-gray-800/50 backdrop-blur-lg rounded-xl p-6 border border-pink-500/30">
              <h3 className="text-xl font-bold mb-4">🎨 Quick Templates</h3>
              <div className="space-y-3">
                <button className="w-full p-3 bg-gradient-to-r from-pink-600/20 to-purple-600/20 border border-pink-500/30 rounded-lg text-left hover:border-pink-500 transition-colors">
                  <div className="font-semibold">Social Media Post</div>
                  <div className="text-xs text-gray-400">1080x1080</div>
                </button>
                <button className="w-full p-3 bg-gradient-to-r from-purple-600/20 to-blue-600/20 border border-purple-500/30 rounded-lg text-left hover:border-purple-500 transition-colors">
                  <div className="font-semibold">YouTube Thumbnail</div>
                  <div className="text-xs text-gray-400">1280x720</div>
                </button>
                <button className="w-full p-3 bg-gradient-to-r from-blue-600/20 to-green-600/20 border border-blue-500/30 rounded-lg text-left hover:border-blue-500 transition-colors">
                  <div className="font-semibold">Blog Banner</div>
                  <div className="text-xs text-gray-400">1200x628</div>
                </button>
                <button className="w-full p-3 bg-gradient-to-r from-green-600/20 to-yellow-600/20 border border-green-500/30 rounded-lg text-left hover:border-green-500 transition-colors">
                  <div className="font-semibold">Logo Design</div>
                  <div className="text-xs text-gray-400">512x512</div>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Audio Generation Tab */}
        {activeTab === 'audio' && (
          <div className="grid grid-cols-3 gap-6">
            {/* Creation Panel */}
            <div className="col-span-2 bg-gray-800/50 backdrop-blur-lg rounded-xl p-6 border border-green-500/30">
              <h2 className="text-2xl font-bold mb-4">🎵 Generate Audio & Voice</h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold mb-2">Audio Project Name</label>
                  <input
                    type="text"
                    placeholder="My Audio Track"
                    className="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg focus:border-green-500 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-2">Audio Type</label>
                  <div className="grid grid-cols-3 gap-2">
                    <button className="px-4 py-2 bg-green-600 border-2 border-green-400 rounded-lg font-semibold">Voice/Narration</button>
                    <button className="px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg hover:border-green-500">Music/Soundtrack</button>
                    <button className="px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg hover:border-green-500">Sound Effects</button>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-2">Script / Text to Speech</label>
                  <textarea
                    rows={4}
                    placeholder="Enter the text you want to convert to speech, or describe the music/sound you want to generate..."
                    className="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg focus:border-green-500 focus:outline-none resize-none"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold mb-2">Voice/Style</label>
                    <select className="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg focus:border-green-500 focus:outline-none">
                      <option>Professional Male</option>
                      <option>Professional Female</option>
                      <option>Warm & Friendly</option>
                      <option>Energetic & Upbeat</option>
                      <option>Calm & Soothing</option>
                      <option>Dramatic & Powerful</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold mb-2">Duration</label>
                    <select className="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg focus:border-green-500 focus:outline-none">
                      <option>30 seconds</option>
                      <option>1 minute</option>
                      <option>2 minutes</option>
                      <option>5 minutes</option>
                      <option>10 minutes</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-2">AI Model</label>
                  <div className="grid grid-cols-3 gap-2">
                    <button className="px-4 py-2 bg-green-600 border-2 border-green-400 rounded-lg font-semibold">ElevenLabs</button>
                    <button className="px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg hover:border-green-500">Murf.ai</button>
                    <button className="px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg hover:border-green-500">Suno AI</button>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-2">Audio Quality</label>
                  <div className="flex gap-2">
                    <button className="flex-1 px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg hover:border-green-500">Standard</button>
                    <button className="flex-1 px-4 py-2 bg-green-600 border-2 border-green-400 rounded-lg font-semibold">High Quality</button>
                    <button className="flex-1 px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg hover:border-green-500">Studio</button>
                  </div>
                </div>

                <button className="w-full py-4 bg-gradient-to-r from-green-600 to-blue-600 rounded-lg font-bold text-lg hover:opacity-90 transition-opacity">
                  🎵 Generate Audio
                </button>
              </div>
            </div>

            {/* Recent Audio Projects */}
            <div className="bg-gray-800/50 backdrop-blur-lg rounded-xl p-6 border border-green-500/30">
              <h3 className="text-xl font-bold mb-4">🎙️ Recent Audio</h3>
              <div className="space-y-3">
                <div className="bg-gray-900/50 rounded-lg p-3 border border-gray-700">
                  <div className="flex justify-between items-start mb-2">
                    <div className="font-semibold text-sm">Product Demo Voiceover</div>
                    <div className="text-xs px-2 py-1 rounded bg-green-500/20 text-green-400">completed</div>
                  </div>
                  <div className="text-xs text-gray-400">ElevenLabs • 2:30</div>
                </div>
                <div className="bg-gray-900/50 rounded-lg p-3 border border-gray-700">
                  <div className="flex justify-between items-start mb-2">
                    <div className="font-semibold text-sm">Background Music Track</div>
                    <div className="text-xs px-2 py-1 rounded bg-yellow-500/20 text-yellow-400">generating</div>
                  </div>
                  <div className="w-full bg-gray-800 rounded-full h-2 overflow-hidden mt-2">
                    <div className="bg-gradient-to-r from-green-600 to-blue-600 h-full" style={{ width: '45%' }} />
                  </div>
                </div>
              </div>

              <div className="mt-6 p-4 bg-green-500/10 border border-green-500/30 rounded-lg">
                <h4 className="font-semibold mb-2">🎧 Audio Features</h4>
                <ul className="text-xs text-gray-400 space-y-1">
                  <li>• Text-to-Speech with 50+ voices</li>
                  <li>• AI Music Generation</li>
                  <li>• Sound Effects Library</li>
                  <li>• Multi-language Support</li>
                  <li>• Voice Cloning</li>
                  <li>• Audio Enhancement</li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* Animation Studio Tab */}
        {activeTab === 'animation' && (
          <div className="bg-gray-800/50 backdrop-blur-lg rounded-xl p-6 border border-blue-500/30">
            <h2 className="text-2xl font-bold mb-6">✨ Animation Studio</h2>

            <div className="grid grid-cols-2 gap-6">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold mb-2">Animation Type</label>
                  <div className="grid grid-cols-2 gap-2">
                    {animationStyles.map((style) => (
                      <button
                        key={style}
                        className="px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg hover:border-blue-500 transition-colors text-sm"
                      >
                        {style}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-2">Duration</label>
                  <input
                    type="number"
                    placeholder="5"
                    className="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg focus:border-blue-500 focus:outline-none"
                  />
                  <div className="text-xs text-gray-400 mt-1">seconds</div>
                </div>

                <button className="w-full py-4 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg font-bold text-lg hover:opacity-90 transition-opacity">
                  ✨ Create Animation
                </button>
              </div>

              <div className="bg-gray-900/50 rounded-lg p-6 border border-gray-700">
                <h3 className="font-semibold mb-3">🎬 Preview Window</h3>
                <div className="aspect-video bg-gray-800 rounded-lg flex items-center justify-center border-2 border-dashed border-gray-600">
                  <div className="text-center text-gray-500">
                    <div className="text-4xl mb-2">🎥</div>
                    <div>Animation preview will appear here</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* AI Models Tab */}
        {activeTab === 'models' && (
          <div className="bg-gray-800/50 backdrop-blur-lg rounded-xl p-6 border border-green-500/30">
            <h2 className="text-2xl font-bold mb-6">🤖 AI Models Dashboard</h2>

            <div className="grid grid-cols-4 gap-4">
              {aiModels.map((model) => (
                <div
                  key={model.id}
                  className="bg-gray-900/50 rounded-lg p-4 border border-gray-700 hover:border-green-500 transition-colors"
                >
                  <div className="text-4xl mb-3">{model.icon}</div>
                  <div className="font-bold mb-1">{model.name}</div>
                  <div className="text-xs text-gray-400 mb-3">{model.type}</div>
                  <div className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${
                    model.status === 'active' ? 'bg-green-500/20 text-green-400' :
                    model.status === 'busy' ? 'bg-yellow-500/20 text-yellow-400' :
                    'bg-gray-500/20 text-gray-400'
                  }`}>
                    {model.status === 'active' ? '● Active' :
                     model.status === 'busy' ? '● Busy' :
                     '● Offline'}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </>
  );
}
