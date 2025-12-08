import React, { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import CodexNavigation from '../components/CodexNavigation';

interface VideoProject {
  id: string;
  title: string;
  type: string;
  status: 'draft' | 'rendering' | 'complete';
  duration: string;
  thumbnail: string;
}

const AIVideoStudio = () => {
  const [activeTab, setActiveTab] = useState('create');
  const [projects, setProjects] = useState<VideoProject[]>([
    { id: '1', title: 'Product Demo Video', type: 'Marketing', status: 'complete', duration: '2:30', thumbnail: '🎬' },
    { id: '2', title: 'Social Media Reel', type: 'TikTok', status: 'rendering', duration: '0:45', thumbnail: '📱' },
    { id: '3', title: 'YouTube Tutorial', type: 'Education', status: 'draft', duration: '10:00', thumbnail: '🎓' },
  ]);

  const aiModels = [
    { name: 'Runway Gen-3', icon: '🎭', speed: 'Ultra Fast', quality: 'Cinematic' },
    { name: 'Pika Labs 1.5', icon: '🎨', speed: 'Fast', quality: 'High Quality' },
    { name: 'Stable Video', icon: '🎪', speed: 'Medium', quality: 'Consistent' },
    { name: 'Luma Dream', icon: '✨', speed: 'Fast', quality: 'Dreamlike' },
    { name: 'Kling AI', icon: '🌟', speed: 'Very Fast', quality: 'Realistic' },
    { name: 'MiniMax Hailuo', icon: '⚡', speed: 'Ultra Fast', quality: 'Professional' },
  ];

  const renderEngines = [
    { name: 'Blender 4.0+', icon: '🔷', capabilities: 'AI Add-ons, 3D Rendering' },
    { name: 'Unreal Engine 5', icon: '🎮', capabilities: 'MetaHuman, Real-time' },
    { name: 'Unity 2023', icon: '🎯', capabilities: 'AI Timeline, Effects' },
    { name: 'DaVinci Resolve', icon: '🎞️', capabilities: 'AI Color Grading' },
    { name: 'After Effects', icon: '🎬', capabilities: 'AI Motion Graphics' },
    { name: 'OBS Studio', icon: '📹', capabilities: 'AI Scene Detection' },
  ];

  const videoTemplates = [
    { id: 1, name: 'Social Media Reel', duration: '15-60s', platform: 'TikTok/Reels', icon: '📱' },
    { id: 2, name: 'Product Demo', duration: '1-3min', platform: 'YouTube', icon: '🛍️' },
    { id: 3, name: 'Explainer Video', duration: '2-5min', platform: 'Website', icon: '💡' },
    { id: 4, name: 'Tutorial', duration: '5-15min', platform: 'YouTube', icon: '🎓' },
    { id: 5, name: 'Testimonial', duration: '30-90s', platform: 'Multi-platform', icon: '⭐' },
    { id: 6, name: 'Ad Campaign', duration: '15-30s', platform: 'Social Ads', icon: '📺' },
    { id: 7, name: 'Documentary', duration: '10-30min', platform: 'YouTube', icon: '📽️' },
    { id: 8, name: 'Presentation', duration: '5-20min', platform: 'Business', icon: '💼' },
  ];

  return (
    <>
      <Head>
        <title>AI Video Studio Omega - Codex Dominion</title>
        <meta name="description" content="Professional AI-powered video production studio" />
      </Head>

      <CodexNavigation />

      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900 text-white p-8">
        <div className="max-w-[1800px] mx-auto">

          {/* Header */}
          <div className="text-center mb-10">
            <h1 className="text-5xl font-bold mb-3 bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
              🎬 AI Video Studio Omega
            </h1>
            <p className="text-xl text-gray-300">
              Professional Video Production • AI-Powered • Multi-Engine Rendering
            </p>
            <div className="flex justify-center gap-4 mt-4 flex-wrap">
              <span className="px-4 py-2 bg-purple-600/30 rounded-full text-sm">✨ GenSpark Compatible</span>
              <span className="px-4 py-2 bg-pink-600/30 rounded-full text-sm">🎨 Designrr Integration</span>
              <span className="px-4 py-2 bg-blue-600/30 rounded-full text-sm">🤖 AI-Enhanced</span>
            </div>
          </div>

          {/* Tab Navigation */}
          <div className="flex justify-center gap-4 mb-8 flex-wrap">
            {['create', 'projects', 'ai-models', 'render', 'templates'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-6 py-3 rounded-xl font-semibold transition-all ${
                  activeTab === tab
                    ? 'bg-gradient-to-r from-purple-600 to-pink-600 shadow-2xl scale-110'
                    : 'bg-white/10 hover:bg-white/20'
                }`}
              >
                {tab === 'create' && '🎥 Create Video'}
                {tab === 'projects' && '📂 My Projects'}
                {tab === 'ai-models' && '🤖 AI Models'}
                {tab === 'render' && '⚙️ Render Engines'}
                {tab === 'templates' && '📋 Templates'}
              </button>
            ))}
          </div>

          {/* Content */}
          <div className="bg-white/5 backdrop-blur-xl rounded-3xl p-8 border border-white/10">

            {/* Create Video Tab */}
            {activeTab === 'create' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">🎥 Create New Video</h2>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  <div className="bg-white/10 p-6 rounded-xl">
                    <h3 className="text-xl font-bold mb-4">Project Details</h3>
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-semibold mb-2">Project Name</label>
                        <input
                          type="text"
                          placeholder="My Awesome Video"
                          className="w-full bg-black/30 border border-white/20 rounded-lg px-4 py-3 focus:outline-none focus:border-purple-400"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-semibold mb-2">Video Type</label>
                        <select className="w-full bg-black/30 border border-white/20 rounded-lg px-4 py-3 focus:outline-none focus:border-purple-400" aria-label="Video Type">
                          <option>Social Media Reel</option>
                          <option>Product Demo</option>
                          <option>Tutorial</option>
                          <option>Explainer</option>
                          <option>Ad Campaign</option>
                          <option>Documentary</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-semibold mb-2">Platform</label>
                        <select className="w-full bg-black/30 border border-white/20 rounded-lg px-4 py-3 focus:outline-none focus:border-purple-400" aria-label="Platform">
                          <option>YouTube</option>
                          <option>TikTok</option>
                          <option>Instagram Reels</option>
                          <option>LinkedIn</option>
                          <option>Website</option>
                          <option>Multi-platform</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-semibold mb-2">Duration</label>
                        <input
                          type="text"
                          placeholder="2:30"
                          className="w-full bg-black/30 border border-white/20 rounded-lg px-4 py-3 focus:outline-none focus:border-purple-400"
                        />
                      </div>
                    </div>
                  </div>

                  <div className="bg-white/10 p-6 rounded-xl">
                    <h3 className="text-xl font-bold mb-4">AI Configuration</h3>
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-semibold mb-2">AI Model</label>
                        <select className="w-full bg-black/30 border border-white/20 rounded-lg px-4 py-3 focus:outline-none focus:border-purple-400" aria-label="AI Model">
                          {aiModels.map((model, idx) => (
                            <option key={idx}>{model.icon} {model.name}</option>
                          ))}
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-semibold mb-2">Render Engine</label>
                        <select className="w-full bg-black/30 border border-white/20 rounded-lg px-4 py-3 focus:outline-none focus:border-purple-400" aria-label="Render Engine">
                          {renderEngines.map((engine, idx) => (
                            <option key={idx}>{engine.icon} {engine.name}</option>
                          ))}
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-semibold mb-2">Style Preset</label>
                        <select className="w-full bg-black/30 border border-white/20 rounded-lg px-4 py-3 focus:outline-none focus:border-purple-400" aria-label="Style Preset">
                          <option>🎨 Cinematic</option>
                          <option>🌟 Modern & Clean</option>
                          <option>🔥 Bold & Energetic</option>
                          <option>💼 Professional</option>
                          <option>✨ Dreamlike</option>
                          <option>🎭 Artistic</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-semibold mb-2">Voice Synthesis</label>
                        <select className="w-full bg-black/30 border border-white/20 rounded-lg px-4 py-3 focus:outline-none focus:border-purple-400" aria-label="Voice Synthesis">
                          <option>Natural Male Voice</option>
                          <option>Natural Female Voice</option>
                          <option>Narrator Voice</option>
                          <option>Energetic Voice</option>
                          <option>No Voice</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="mt-6 bg-white/10 p-6 rounded-xl">
                  <h3 className="text-xl font-bold mb-4">Script / Prompt</h3>
                  <textarea
                    placeholder="Describe your video or paste your script here. AI will generate the perfect video based on your description..."
                    className="w-full h-40 bg-black/30 border border-white/20 rounded-lg px-4 py-3 focus:outline-none focus:border-purple-400 font-mono"
                  />
                </div>

                <div className="mt-6 flex gap-4">
                  <button className="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 py-4 rounded-xl font-bold text-lg hover:scale-105 transition-transform">
                    🎬 Generate Video
                  </button>
                  <button className="px-8 bg-white/10 hover:bg-white/20 py-4 rounded-xl font-semibold transition-all">
                    💾 Save Draft
                  </button>
                </div>
              </div>
            )}

            {/* Projects Tab */}
            {activeTab === 'projects' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">📂 My Video Projects</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {projects.map((project) => (
                    <div key={project.id} className="bg-white/10 p-6 rounded-xl hover:bg-white/15 transition-all">
                      <div className="text-6xl mb-4 text-center">{project.thumbnail}</div>
                      <h3 className="text-xl font-bold mb-2">{project.title}</h3>
                      <div className="space-y-2 text-sm">
                        <p className="text-gray-400">Type: {project.type}</p>
                        <p className="text-gray-400">Duration: {project.duration}</p>
                        <div className="flex items-center gap-2">
                          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                            project.status === 'complete' ? 'bg-green-600' :
                            project.status === 'rendering' ? 'bg-yellow-600' : 'bg-gray-600'
                          }`}>
                            {project.status.toUpperCase()}
                          </span>
                        </div>
                      </div>
                      <div className="mt-4 flex gap-2">
                        <button className="flex-1 bg-purple-600 hover:bg-purple-700 py-2 rounded-lg text-sm font-semibold">
                          Edit
                        </button>
                        <button className="flex-1 bg-blue-600 hover:bg-blue-700 py-2 rounded-lg text-sm font-semibold">
                          Export
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* AI Models Tab */}
            {activeTab === 'ai-models' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">🤖 AI Video Generation Models</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {aiModels.map((model, idx) => (
                    <div key={idx} className="bg-white/10 p-6 rounded-xl hover:border-purple-400 border-2 border-transparent transition-all">
                      <div className="text-5xl mb-4">{model.icon}</div>
                      <h3 className="text-xl font-bold mb-3">{model.name}</h3>
                      <div className="space-y-2 text-sm">
                        <p className="text-gray-300">Speed: <span className="text-green-400 font-semibold">{model.speed}</span></p>
                        <p className="text-gray-300">Quality: <span className="text-blue-400 font-semibold">{model.quality}</span></p>
                      </div>
                      <button className="w-full mt-4 bg-gradient-to-r from-purple-600 to-pink-600 py-2 rounded-lg font-semibold hover:scale-105 transition-transform">
                        Use Model
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Render Engines Tab */}
            {activeTab === 'render' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">⚙️ Professional Render Engines</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {renderEngines.map((engine, idx) => (
                    <div key={idx} className="bg-white/10 p-6 rounded-xl hover:border-blue-400 border-2 border-transparent transition-all">
                      <div className="text-5xl mb-4">{engine.icon}</div>
                      <h3 className="text-xl font-bold mb-3">{engine.name}</h3>
                      <p className="text-sm text-gray-300 mb-4">{engine.capabilities}</p>
                      <button className="w-full bg-blue-600 hover:bg-blue-700 py-2 rounded-lg font-semibold transition-all">
                        Configure Engine
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Templates Tab */}
            {activeTab === 'templates' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">📋 Video Templates</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {videoTemplates.map((template) => (
                    <div key={template.id} className="bg-white/10 p-5 rounded-xl hover:bg-white/15 transition-all cursor-pointer">
                      <div className="text-4xl mb-3 text-center">{template.icon}</div>
                      <h3 className="font-bold mb-2 text-center">{template.name}</h3>
                      <p className="text-xs text-gray-400 text-center mb-1">{template.duration}</p>
                      <p className="text-xs text-gray-400 text-center mb-3">{template.platform}</p>
                      <button className="w-full bg-purple-600 hover:bg-purple-700 py-2 rounded-lg text-sm font-semibold">
                        Use Template
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <style jsx>{`
        .bg-clip-text {
          -webkit-background-clip: text;
          background-clip: text;
        }
      `}</style>
    </>
  );
};

export default AIVideoStudio;
