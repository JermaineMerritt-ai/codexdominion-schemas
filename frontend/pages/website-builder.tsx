import React, { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import CodexNavigation from '../components/CodexNavigation';

const WebsiteBuilder = () => {
  const [activeTab, setActiveTab] = useState('builder');

  const projectTemplates = [
    { id: 1, name: 'Landing Page', icon: '🎯', tech: 'React + Tailwind', difficulty: 'Easy' },
    { id: 2, name: 'E-commerce Store', icon: '🛍️', tech: 'Next.js + Stripe', difficulty: 'Medium' },
    { id: 3, name: 'Portfolio', icon: '💼', tech: 'React + Framer', difficulty: 'Easy' },
    { id: 4, name: 'SaaS Dashboard', icon: '📊', tech: 'Next.js + Charts', difficulty: 'Advanced' },
    { id: 5, name: 'Blog Platform', icon: '📝', tech: 'Next.js + MDX', difficulty: 'Medium' },
    { id: 6, name: 'Social Network', icon: '👥', tech: 'Next.js + Supabase', difficulty: 'Advanced' },
    { id: 7, name: 'Mobile App', icon: '📱', tech: 'React Native', difficulty: 'Advanced' },
    { id: 8, name: 'Admin Panel', icon: '⚙️', tech: 'React + Dashboard', difficulty: 'Medium' },
  ];

  const techStacks = [
    { name: 'React', icon: '⚛️', description: 'Component-based UI library', color: 'from-blue-600 to-cyan-600' },
    { name: 'Next.js', icon: '▲', description: 'Full-stack React framework', color: 'from-slate-700 to-slate-900' },
    { name: 'Vue.js', icon: '💚', description: 'Progressive framework', color: 'from-green-600 to-emerald-600' },
    { name: 'FastAPI', icon: '⚡', description: 'Python high-performance API', color: 'from-teal-600 to-cyan-600' },
    { name: 'Flutter', icon: '📱', description: 'Cross-platform mobile', color: 'from-blue-500 to-indigo-600' },
    { name: 'Tailwind CSS', icon: '🎨', description: 'Utility-first CSS', color: 'from-cyan-600 to-blue-600' },
  ];

  const features = [
    { name: 'AI Code Generation', description: 'Natural language to production code', icon: '🤖' },
    { name: 'Real-time Preview', description: 'See changes instantly', icon: '👁️' },
    { name: 'One-Click Deploy', description: 'Deploy to Vercel, Netlify, AWS', icon: '🚀' },
    { name: 'Database Integration', description: 'Auto-configure DB schemas', icon: '💾' },
    { name: 'Authentication', description: 'Built-in auth with OAuth', icon: '🔐' },
    { name: 'Responsive Design', description: 'Mobile-first automatically', icon: '📱' },
    { name: 'SEO Optimized', description: 'Meta tags, sitemaps, SSR', icon: '📊' },
    { name: 'Dark Mode', description: 'Automatic theme switching', icon: '🌙' },
  ];

  return (
    <>
      <Head>
        <title>AI Website Builder - Lovable Inspired</title>
        <meta name="description" content="Build full-stack applications with AI" />
      </Head>

      <CodexNavigation />

      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white p-8">
        <div className="max-w-[1800px] mx-auto">

          {/* Header */}
          <div className="text-center mb-10">
            <h1 className="text-5xl font-bold mb-3 bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
              🚀 AI Website Builder
            </h1>
            <p className="text-xl text-gray-300">
              Build Full-Stack Apps with AI • Lovable-Inspired • Deploy in Minutes
            </p>
            <div className="flex justify-center gap-4 mt-4 flex-wrap">
              <span className="px-4 py-2 bg-purple-600/30 rounded-full text-sm">🤖 AI-Powered</span>
              <span className="px-4 py-2 bg-pink-600/30 rounded-full text-sm">⚡ Lightning Fast</span>
              <span className="px-4 py-2 bg-blue-600/30 rounded-full text-sm">🎨 Beautiful Design</span>
            </div>
          </div>

          {/* Tab Navigation */}
          <div className="flex justify-center gap-4 mb-8 flex-wrap">
            {['builder', 'templates', 'tech-stack', 'features'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-6 py-3 rounded-xl font-semibold transition-all ${
                  activeTab === tab
                    ? 'bg-gradient-to-r from-purple-600 to-pink-600 shadow-2xl scale-110'
                    : 'bg-white/10 hover:bg-white/20'
                }`}
              >
                {tab === 'builder' && '🛠️ AI Builder'}
                {tab === 'templates' && '📋 Templates'}
                {tab === 'tech-stack' && '💻 Tech Stack'}
                {tab === 'features' && '✨ Features'}
              </button>
            ))}
          </div>

          {/* Content */}
          <div className="bg-white/5 backdrop-blur-xl rounded-3xl p-8 border border-white/10">

            {/* Builder Tab */}
            {activeTab === 'builder' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">🛠️ Build Your Application</h2>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  <div className="space-y-6">
                    <div className="bg-white/10 p-6 rounded-xl">
                      <h3 className="text-xl font-bold mb-4">Project Configuration</h3>

                      <div className="space-y-4">
                        <div>
                          <label className="block text-sm font-semibold mb-2">Project Name</label>
                          <input
                            type="text"
                            placeholder="my-awesome-app"
                            aria-label="Project Name"
                            className="w-full bg-black/30 border border-white/20 rounded-lg px-4 py-3 focus:outline-none focus:border-purple-400"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-semibold mb-2">Project Type</label>
                          <select className="w-full bg-black/30 border border-white/20 rounded-lg px-4 py-3" aria-label="Project Type">
                            <option>React Application</option>
                            <option>Next.js Full-Stack App</option>
                            <option>Vue.js Application</option>
                            <option>FastAPI Backend</option>
                            <option>Flutter Mobile App</option>
                            <option>Analytics Dashboard</option>
                          </select>
                        </div>

                        <div>
                          <label className="block text-sm font-semibold mb-2">Features</label>
                          <div className="space-y-2">
                            <label className="flex items-center gap-2">
                              <input type="checkbox" defaultChecked className="rounded" aria-label="Authentication (OAuth, JWT)" />
                              <span className="text-sm">Authentication (OAuth, JWT)</span>
                            </label>
                            <label className="flex items-center gap-2">
                              <input type="checkbox" defaultChecked className="rounded" aria-label="Database (PostgreSQL, MongoDB)" />
                              <span className="text-sm">Database (PostgreSQL, MongoDB)</span>
                            </label>
                            <label className="flex items-center gap-2">
                              <input type="checkbox" defaultChecked className="rounded" aria-label="API Integration" />
                              <span className="text-sm">API Integration</span>
                            </label>
                            <label className="flex items-center gap-2">
                              <input type="checkbox" className="rounded" aria-label="Real-time Updates (WebSockets)" />
                              <span className="text-sm">Real-time Updates (WebSockets)</span>
                            </label>
                            <label className="flex items-center gap-2">
                              <input type="checkbox" className="rounded" aria-label="Dark Mode" />
                              <span className="text-sm">Dark Mode</span>
                            </label>
                            <label className="flex items-center gap-2">
                              <input type="checkbox" className="rounded" aria-label="Payment Integration (Stripe)" />
                              <span className="text-sm">Payment Integration (Stripe)</span>
                            </label>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-6">
                    <div className="bg-white/10 p-6 rounded-xl">
                      <h3 className="text-xl font-bold mb-4">Describe Your App (AI)</h3>
                      <textarea
                        placeholder="Describe your application in natural language... AI will generate the complete codebase, including frontend, backend, database schema, and deployment configuration.

Example: 'Create a social media dashboard with user authentication, post creation, comments, likes, and a feed showing recent posts from followed users. Include dark mode and mobile responsive design.'"
                        className="w-full h-64 bg-black/30 border border-white/20 rounded-lg px-4 py-3 focus:outline-none focus:border-purple-400 font-mono text-sm"
                      />
                    </div>

                    <div className="bg-white/10 p-6 rounded-xl">
                      <h3 className="text-xl font-bold mb-4">AI Intelligence Level</h3>
                      <div className="space-y-3">
                        <div className="flex justify-between items-center">
                          <span>Code Quality</span>
                          <input type="range" min="0" max="100" defaultValue="90" className="w-40" aria-label="Code Quality" />
                          <span className="text-purple-400 font-bold">90%</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span>Optimization</span>
                          <input type="range" min="0" max="100" defaultValue="85" className="w-40" aria-label="Optimization" />
                          <span className="text-blue-400 font-bold">85%</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span>Security</span>
                          <input type="range" min="0" max="100" defaultValue="95" className="w-40" aria-label="Security" />
                          <span className="text-green-400 font-bold">95%</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="mt-8 flex gap-4">
                  <button className="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 py-4 rounded-xl font-bold text-lg hover:scale-105 transition-transform">
                    🚀 Generate Application
                  </button>
                  <button className="px-8 bg-white/10 hover:bg-white/20 py-4 rounded-xl font-semibold">
                    💾 Save Configuration
                  </button>
                </div>
              </div>
            )}

            {/* Templates Tab */}
            {activeTab === 'templates' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">📋 Project Templates</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {projectTemplates.map((template) => (
                    <div key={template.id} className="bg-white/10 p-6 rounded-xl hover:bg-white/15 transition-all cursor-pointer">
                      <div className="text-5xl mb-4 text-center">{template.icon}</div>
                      <h3 className="text-lg font-bold mb-2 text-center">{template.name}</h3>
                      <p className="text-sm text-gray-400 text-center mb-1">{template.tech}</p>
                      <div className="text-center mb-4">
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          template.difficulty === 'Easy' ? 'bg-green-600' :
                          template.difficulty === 'Medium' ? 'bg-yellow-600' : 'bg-red-600'
                        }`}>
                          {template.difficulty}
                        </span>
                      </div>
                      <button className="w-full bg-purple-600 hover:bg-purple-700 py-2 rounded-lg font-semibold">
                        Use Template
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Tech Stack Tab */}
            {activeTab === 'tech-stack' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">💻 Supported Technologies</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {techStacks.map((tech, idx) => (
                    <div key={idx} className={`bg-gradient-to-br ${tech.color} p-6 rounded-xl hover:scale-105 transition-transform`}>
                      <div className="text-5xl mb-4">{tech.icon}</div>
                      <h3 className="text-xl font-bold mb-2">{tech.name}</h3>
                      <p className="text-sm opacity-90">{tech.description}</p>
                      <button className="w-full mt-4 bg-white/20 hover:bg-white/30 py-2 rounded-lg font-semibold">
                        Select
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Features Tab */}
            {activeTab === 'features' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">✨ Platform Features</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {features.map((feature, idx) => (
                    <div key={idx} className="bg-white/10 p-6 rounded-xl hover:bg-white/15 transition-all">
                      <div className="text-5xl mb-4">{feature.icon}</div>
                      <h3 className="text-lg font-bold mb-2">{feature.name}</h3>
                      <p className="text-sm text-gray-400">{feature.description}</p>
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

export default WebsiteBuilder;
