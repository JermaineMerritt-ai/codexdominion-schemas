import React, { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import CodexNavigation from '../components/CodexNavigation';

const CreativeStudio = () => {
  const [activeTab, setActiveTab] = useState('dashboard');

  const contentTypes = [
    { id: 1, name: 'Social Media Posts', platform: 'Instagram/TikTok/LinkedIn', icon: '📱', color: 'from-pink-600 to-purple-600' },
    { id: 2, name: 'Marketing Copy', platform: 'Ads & Campaigns', icon: '💼', color: 'from-blue-600 to-cyan-600' },
    { id: 3, name: 'Video Scripts', platform: 'YouTube/TikTok', icon: '🎬', color: 'from-red-600 to-orange-600' },
    { id: 4, name: 'Blog Articles', platform: 'Website/Medium', icon: '📝', color: 'from-green-600 to-emerald-600' },
    { id: 5, name: 'Email Campaigns', platform: 'Newsletter/Marketing', icon: '📧', color: 'from-indigo-600 to-purple-600' },
    { id: 6, name: 'Visual Content', platform: 'Images/Graphics/Designs', icon: '🎨', color: 'from-yellow-600 to-orange-600' },
    { id: 7, name: 'Storyboards', platform: 'Video/Animation Planning', icon: '🎭', color: 'from-purple-600 to-pink-600' },
    { id: 8, name: 'Product Descriptions', platform: 'E-commerce', icon: '🛍️', color: 'from-teal-600 to-cyan-600' },
  ];

  const platforms = [
    { name: 'Instagram', icon: '📷', optimizations: ['Reels', 'Stories', 'Posts', 'Carousels'] },
    { name: 'TikTok', icon: '🎵', optimizations: ['Short Videos', 'Trends', 'Challenges'] },
    { name: 'YouTube', icon: '📺', optimizations: ['Long-form', 'Shorts', 'Titles', 'Descriptions'] },
    { name: 'LinkedIn', icon: '💼', optimizations: ['Professional Posts', 'Articles', 'Carousels'] },
    { name: 'Twitter/X', icon: '🐦', optimizations: ['Threads', 'Tweets', 'Viral Content'] },
    { name: 'Facebook', icon: '👥', optimizations: ['Posts', 'Stories', 'Ads', 'Groups'] },
  ];

  const aiEnhancements = [
    { name: 'Viral Optimization', description: 'AI analyzes trends to maximize engagement', icon: '🚀' },
    { name: 'Psychology-Based Persuasion', description: 'Conversion-focused content creation', icon: '🧠' },
    { name: 'Multi-Platform Adaptation', description: 'One prompt, optimized for all platforms', icon: '🔄' },
    { name: 'Brand Voice Consistency', description: 'Maintains your unique tone across all content', icon: '🎯' },
    { name: 'SEO Optimization', description: 'Built-in keyword and ranking optimization', icon: '📊' },
    { name: 'A/B Testing Suggestions', description: 'AI generates variations for testing', icon: '🔬' },
  ];

  return (
    <>
      <Head>
        <title>Creative Content Studio - Nano Banana Destroyer</title>
        <meta name="description" content="Reality-defying creative content generation" />
      </Head>

      <CodexNavigation />

      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-orange-900 to-slate-900 text-white p-8">
        <div className="max-w-[1800px] mx-auto">

          {/* Header */}
          <div className="text-center mb-10">
            <h1 className="text-5xl font-bold mb-3 bg-gradient-to-r from-orange-400 via-yellow-400 to-pink-400 bg-clip-text text-transparent">
              🎨 Creative Content Studio
            </h1>
            <p className="text-xl text-gray-300">
              AI-Powered Creative Generation • Viral Optimization • Nano Banana Atomizer
            </p>
            <div className="flex justify-center gap-4 mt-4 flex-wrap">
              <span className="px-4 py-2 bg-red-600/30 rounded-full text-sm">🍌 Nano Banana Destroyed</span>
              <span className="px-4 py-2 bg-orange-600/30 rounded-full text-sm">⚡ 5000% Faster</span>
              <span className="px-4 py-2 bg-yellow-600/30 rounded-full text-sm">✨ Reality-Defying Creativity</span>
            </div>
          </div>

          {/* Tab Navigation */}
          <div className="flex justify-center gap-4 mb-8 flex-wrap">
            {['dashboard', 'create', 'platforms', 'templates'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-6 py-3 rounded-xl font-semibold transition-all ${
                  activeTab === tab
                    ? 'bg-gradient-to-r from-orange-600 to-pink-600 shadow-2xl scale-110'
                    : 'bg-white/10 hover:bg-white/20'
                }`}
              >
                {tab === 'dashboard' && '🎯 Dashboard'}
                {tab === 'create' && '✨ Create Content'}
                {tab === 'platforms' && '📱 Platforms'}
                {tab === 'templates' && '📋 Templates'}
              </button>
            ))}
          </div>

          {/* Content */}
          <div className="bg-white/5 backdrop-blur-xl rounded-3xl p-8 border border-white/10">

            {/* Dashboard Tab */}
            {activeTab === 'dashboard' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">🎯 Content Generation Dashboard</h2>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                  {contentTypes.map((type) => (
                    <div key={type.id} className={`bg-gradient-to-br ${type.color} p-6 rounded-xl hover:scale-105 transition-transform cursor-pointer`}>
                      <div className="text-5xl mb-3">{type.icon}</div>
                      <h3 className="text-lg font-bold mb-2">{type.name}</h3>
                      <p className="text-sm opacity-90">{type.platform}</p>
                    </div>
                  ))}
                </div>

                <div className="bg-white/10 p-6 rounded-xl">
                  <h3 className="text-2xl font-bold mb-4">🚀 AI Enhancements</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {aiEnhancements.map((enhancement, idx) => (
                      <div key={idx} className="bg-white/10 p-4 rounded-lg">
                        <div className="flex items-start gap-3">
                          <span className="text-3xl">{enhancement.icon}</span>
                          <div>
                            <h4 className="font-bold mb-1">{enhancement.name}</h4>
                            <p className="text-sm text-gray-400">{enhancement.description}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Create Tab */}
            {activeTab === 'create' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">✨ Create AI-Powered Content</h2>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  <div className="space-y-6">
                    <div className="bg-white/10 p-6 rounded-xl">
                      <h3 className="text-xl font-bold mb-4">Content Type</h3>
                      <select className="w-full bg-black/30 border border-white/20 rounded-lg px-4 py-3 mb-4" aria-label="Content Type">
                        <option>Social Media Post</option>
                        <option>Video Script</option>
                        <option>Blog Article</option>
                        <option>Marketing Copy</option>
                        <option>Email Campaign</option>
                        <option>Product Description</option>
                      </select>

                      <h3 className="text-xl font-bold mb-4 mt-6">Target Platform</h3>
                      <div className="grid grid-cols-3 gap-2 mb-4">
                        {platforms.map((platform, idx) => (
                          <button key={idx} className="bg-white/10 hover:bg-white/20 p-3 rounded-lg text-sm">
                            {platform.icon} {platform.name}
                          </button>
                        ))}
                      </div>

                      <h3 className="text-xl font-bold mb-4 mt-6">Tone & Style</h3>
                      <select className="w-full bg-black/30 border border-white/20 rounded-lg px-4 py-3" aria-label="Tone & Style">
                        <option>Professional</option>
                        <option>Casual & Friendly</option>
                        <option>Bold & Energetic</option>
                        <option>Educational</option>
                        <option>Inspirational</option>
                        <option>Humorous</option>
                      </select>
                    </div>
                  </div>

                  <div className="space-y-6">
                    <div className="bg-white/10 p-6 rounded-xl">
                      <h3 className="text-xl font-bold mb-4">Your Prompt</h3>
                      <textarea
                        placeholder="Describe what you want to create... AI will generate viral-optimized content based on your description."
                        className="w-full h-40 bg-black/30 border border-white/20 rounded-lg px-4 py-3 focus:outline-none focus:border-orange-400"
                      />

                      <h3 className="text-xl font-bold mb-4 mt-6">AI Options</h3>
                      <div className="space-y-2">
                        <label className="flex items-center gap-2">
                          <input type="checkbox" defaultChecked className="rounded" />
                          <span className="text-sm">Viral Optimization</span>
                        </label>
                        <label className="flex items-center gap-2">
                          <input type="checkbox" defaultChecked className="rounded" />
                          <span className="text-sm">SEO Enhancement</span>
                        </label>
                        <label className="flex items-center gap-2">
                          <input type="checkbox" defaultChecked className="rounded" />
                          <span className="text-sm">Generate Variations</span>
                        </label>
                        <label className="flex items-center gap-2">
                          <input type="checkbox" className="rounded" />
                          <span className="text-sm">Include Hashtags</span>
                        </label>
                        <label className="flex items-center gap-2">
                          <input type="checkbox" className="rounded" />
                          <span className="text-sm">Create Visual Mockup</span>
                        </label>
                      </div>

                      <button className="w-full mt-6 bg-gradient-to-r from-orange-600 to-pink-600 py-4 rounded-xl font-bold text-lg hover:scale-105 transition-transform">
                        ✨ Generate Content
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Platforms Tab */}
            {activeTab === 'platforms' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">📱 Supported Platforms</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {platforms.map((platform, idx) => (
                    <div key={idx} className="bg-white/10 p-6 rounded-xl hover:bg-white/15 transition-all">
                      <div className="text-5xl mb-4">{platform.icon}</div>
                      <h3 className="text-xl font-bold mb-3">{platform.name}</h3>
                      <div className="space-y-1">
                        {platform.optimizations.map((opt, oidx) => (
                          <p key={oidx} className="text-sm text-gray-400">✓ {opt}</p>
                        ))}
                      </div>
                      <button className="w-full mt-4 bg-orange-600 hover:bg-orange-700 py-2 rounded-lg font-semibold">
                        Create for {platform.name}
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Templates Tab */}
            {activeTab === 'templates' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">📋 Content Templates</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {contentTypes.map((type) => (
                    <div key={type.id} className="bg-white/10 p-5 rounded-xl hover:bg-white/15 transition-all cursor-pointer">
                      <div className="text-4xl mb-3 text-center">{type.icon}</div>
                      <h3 className="font-bold mb-2 text-center text-sm">{type.name}</h3>
                      <p className="text-xs text-gray-400 text-center mb-3">{type.platform}</p>
                      <button className="w-full bg-orange-600 hover:bg-orange-700 py-2 rounded-lg text-sm font-semibold">
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

export default CreativeStudio;
