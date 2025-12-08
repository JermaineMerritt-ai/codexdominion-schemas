import React, { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import CodexNavigation from '../components/CodexNavigation';

interface EbookProject {
  id: string;
  title: string;
  author: string;
  pages: number;
  status: 'draft' | 'designing' | 'complete';
  format: string[];
  thumbnail: string;
}

const EbookManager = () => {
  const [activeTab, setActiveTab] = useState('projects');
  const [projects, setProjects] = useState<EbookProject[]>([
    { id: '1', title: 'Codex Dominion Complete Guide', author: 'Jermaine Merritt', pages: 156, status: 'complete', format: ['PDF', 'EPUB'], thumbnail: '📘' },
    { id: '2', title: 'AI Automation Mastery', author: 'Codex Council', pages: 89, status: 'designing', format: ['PDF'], thumbnail: '🤖' },
    { id: '3', title: 'Revenue Growth Strategies', author: 'Jermaine Merritt', pages: 0, status: 'draft', format: [], thumbnail: '💰' },
  ]);

  const templates = [
    { id: 1, name: 'Professional Report', pages: '20-50', style: 'Corporate', icon: '📊', color: 'from-blue-600 to-cyan-600' },
    { id: 2, name: 'eBook Novel', pages: '100-300', style: 'Literary', icon: '📖', color: 'from-purple-600 to-pink-600' },
    { id: 3, name: 'How-To Guide', pages: '30-80', style: 'Educational', icon: '📚', color: 'from-green-600 to-emerald-600' },
    { id: 4, name: 'Magazine Layout', pages: '40-100', style: 'Modern', icon: '📰', color: 'from-orange-600 to-red-600' },
    { id: 5, name: 'Portfolio Book', pages: '20-60', style: 'Visual', icon: '🎨', color: 'from-pink-600 to-purple-600' },
    { id: 6, name: 'Technical Manual', pages: '50-200', style: 'Technical', icon: '⚙️', color: 'from-slate-600 to-gray-700' },
    { id: 7, name: 'Course Workbook', pages: '40-120', style: 'Educational', icon: '📝', color: 'from-indigo-600 to-blue-600' },
    { id: 8, name: 'Recipe Book', pages: '30-100', style: 'Lifestyle', icon: '🍳', color: 'from-yellow-600 to-orange-600' },
  ];

  const designStyles = [
    { name: 'Modern & Clean', description: 'Minimalist design with plenty of white space', icon: '✨' },
    { name: 'Bold & Colorful', description: 'Eye-catching colors and dynamic layouts', icon: '🎨' },
    { name: 'Professional', description: 'Corporate style with elegant typography', icon: '💼' },
    { name: 'Academic', description: 'Traditional scholarly formatting', icon: '🎓' },
    { name: 'Creative', description: 'Artistic layouts with unique elements', icon: '🌈' },
    { name: 'Technical', description: 'Code-friendly with diagrams support', icon: '💻' },
  ];

  const exportFormats = [
    { format: 'PDF', description: 'Universal format for all devices', icon: '📄', quality: 'High' },
    { format: 'EPUB', description: 'Reflowable eBook for e-readers', icon: '📱', quality: 'Optimized' },
    { format: 'MOBI', description: 'Amazon Kindle format', icon: '📚', quality: 'Kindle' },
    { format: 'HTML', description: 'Web-based interactive book', icon: '🌐', quality: 'Interactive' },
    { format: 'DOCX', description: 'Microsoft Word editable', icon: '📝', quality: 'Editable' },
    { format: 'Print Ready', description: 'High-resolution print PDF', icon: '🖨️', quality: '300 DPI' },
  ];

  return (
    <>
      <Head>
        <title>eBook Manager - Designrr Quality</title>
        <meta name="description" content="Professional eBook creation and publishing" />
      </Head>

      <CodexNavigation />

      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900 text-white p-8">
        <div className="max-w-[1800px] mx-auto">

          {/* Header */}
          <div className="text-center mb-10">
            <h1 className="text-5xl font-bold mb-3 bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent">
              📚 eBook Manager
            </h1>
            <p className="text-xl text-gray-300">
              Professional eBook Creation • AI-Powered Design • Designrr Quality
            </p>
            <div className="flex justify-center gap-4 mt-4 flex-wrap">
              <span className="px-4 py-2 bg-blue-600/30 rounded-full text-sm">✨ Designrr-Level Quality</span>
              <span className="px-4 py-2 bg-indigo-600/30 rounded-full text-sm">🎨 Auto-Design</span>
              <span className="px-4 py-2 bg-purple-600/30 rounded-full text-sm">📱 Multi-Format</span>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-white/10 p-6 rounded-xl text-center">
              <div className="text-4xl font-bold text-blue-400">{projects.length}</div>
              <div className="text-sm text-gray-400 mt-1">eBook Projects</div>
            </div>
            <div className="bg-white/10 p-6 rounded-xl text-center">
              <div className="text-4xl font-bold text-indigo-400">
                {projects.reduce((sum, p) => sum + p.pages, 0)}
              </div>
              <div className="text-sm text-gray-400 mt-1">Total Pages</div>
            </div>
            <div className="bg-white/10 p-6 rounded-xl text-center">
              <div className="text-4xl font-bold text-purple-400">{templates.length}</div>
              <div className="text-sm text-gray-400 mt-1">Templates</div>
            </div>
            <div className="bg-white/10 p-6 rounded-xl text-center">
              <div className="text-4xl font-bold text-pink-400">{exportFormats.length}</div>
              <div className="text-sm text-gray-400 mt-1">Export Formats</div>
            </div>
          </div>

          {/* Tab Navigation */}
          <div className="flex justify-center gap-4 mb-8 flex-wrap">
            {['projects', 'create', 'templates', 'design', 'export'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-6 py-3 rounded-xl font-semibold transition-all ${
                  activeTab === tab
                    ? 'bg-gradient-to-r from-blue-600 to-indigo-600 shadow-2xl scale-110'
                    : 'bg-white/10 hover:bg-white/20'
                }`}
              >
                {tab === 'projects' && '📚 My Projects'}
                {tab === 'create' && '✨ Create eBook'}
                {tab === 'templates' && '📋 Templates'}
                {tab === 'design' && '🎨 Design Styles'}
                {tab === 'export' && '📤 Export & Publish'}
              </button>
            ))}
          </div>

          {/* Content */}
          <div className="bg-white/5 backdrop-blur-xl rounded-3xl p-8 border border-white/10">

            {/* Projects Tab */}
            {activeTab === 'projects' && (
              <div>
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-3xl font-bold">📚 My eBook Projects</h2>
                  <button className="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-3 rounded-xl font-semibold hover:scale-105 transition-transform">
                    + New Project
                  </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {projects.map((project) => (
                    <div key={project.id} className="bg-white/10 p-6 rounded-xl hover:bg-white/15 transition-all">
                      <div className="text-6xl mb-4 text-center">{project.thumbnail}</div>
                      <h3 className="text-xl font-bold mb-2">{project.title}</h3>
                      <p className="text-sm text-gray-400 mb-3">By {project.author}</p>
                      <div className="space-y-2 mb-4">
                        <p className="text-sm text-gray-400">📄 {project.pages} pages</p>
                        <div className="flex gap-2">
                          {project.format.map((fmt, idx) => (
                            <span key={idx} className="px-2 py-1 bg-blue-600/30 rounded text-xs">{fmt}</span>
                          ))}
                        </div>
                        <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${
                          project.status === 'complete' ? 'bg-green-600' :
                          project.status === 'designing' ? 'bg-yellow-600' : 'bg-gray-600'
                        }`}>
                          {project.status.toUpperCase()}
                        </span>
                      </div>
                      <div className="flex gap-2">
                        <button className="flex-1 bg-blue-600 hover:bg-blue-700 py-2 rounded-lg text-sm font-semibold">
                          Edit
                        </button>
                        <button className="flex-1 bg-purple-600 hover:bg-purple-700 py-2 rounded-lg text-sm font-semibold">
                          Export
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Create Tab */}
            {activeTab === 'create' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">✨ Create New eBook</h2>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  <div className="space-y-6">
                    <div className="bg-white/10 p-6 rounded-xl">
                      <h3 className="text-xl font-bold mb-4">Book Information</h3>

                      <div className="space-y-4">
                        <div>
                          <label className="block text-sm font-semibold mb-2">Book Title</label>
                          <input
                            type="text"
                            placeholder="My Awesome eBook"
                            className="w-full bg-black/30 border border-white/20 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-400"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-semibold mb-2">Author Name</label>
                          <input
                            type="text"
                            placeholder="Your Name"
                            className="w-full bg-black/30 border border-white/20 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-400"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-semibold mb-2">Category</label>
                          <select className="w-full bg-black/30 border border-white/20 rounded-lg px-4 py-3" aria-label="Category">
                            <option>Business & Finance</option>
                            <option>Technology</option>
                            <option>Self-Help</option>
                            <option>Education</option>
                            <option>Fiction</option>
                            <option>Non-Fiction</option>
                            <option>How-To Guide</option>
                            <option>Technical Manual</option>
                          </select>
                        </div>

                        <div>
                          <label className="block text-sm font-semibold mb-2">Design Template</label>
                          <select className="w-full bg-black/30 border border-white/20 rounded-lg px-4 py-3" aria-label="Design Template">
                            {templates.map((template) => (
                              <option key={template.id}>{template.icon} {template.name}</option>
                            ))}
                          </select>
                        </div>

                        <div>
                          <label className="block text-sm font-semibold mb-2">Design Style</label>
                          <select className="w-full bg-black/30 border border-white/20 rounded-lg px-4 py-3" aria-label="Design Style">
                            {designStyles.map((style, idx) => (
                              <option key={idx}>{style.icon} {style.name}</option>
                            ))}
                          </select>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-6">
                    <div className="bg-white/10 p-6 rounded-xl">
                      <h3 className="text-xl font-bold mb-4">Content Source</h3>

                      <div className="space-y-4">
                        <div className="bg-white/10 p-6 rounded-xl border-2 border-dashed border-white/30 text-center">
                          <div className="text-5xl mb-3">📁</div>
                          <p className="font-semibold mb-2">Upload Content Files</p>
                          <p className="text-sm text-gray-400 mb-4">DOCX, PDF, TXT, MD, HTML</p>
                          <button className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-lg font-semibold">
                            Choose Files
                          </button>
                        </div>

                        <div className="text-center text-gray-400">— OR —</div>

                        <div className="bg-white/10 p-6 rounded-xl">
                          <h4 className="font-bold mb-3">AI Content Generation</h4>
                          <textarea
                            placeholder="Describe your book content... AI will generate chapters, sections, and content based on your description."
                            className="w-full h-32 bg-black/30 border border-white/20 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-400"
                          />
                        </div>

                        <div className="bg-white/10 p-6 rounded-xl">
                          <h4 className="font-bold mb-3">Import from Web</h4>
                          <input
                            type="url"
                            placeholder="Enter URL to import content"
                            className="w-full bg-black/30 border border-white/20 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-400"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="mt-8 flex gap-4">
                  <button className="flex-1 bg-gradient-to-r from-blue-600 to-indigo-600 py-4 rounded-xl font-bold text-lg hover:scale-105 transition-transform">
                    ✨ Generate eBook
                  </button>
                  <button className="px-8 bg-white/10 hover:bg-white/20 py-4 rounded-xl font-semibold">
                    💾 Save Draft
                  </button>
                </div>
              </div>
            )}

            {/* Templates Tab */}
            {activeTab === 'templates' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">📋 eBook Templates</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {templates.map((template) => (
                    <div key={template.id} className={`bg-gradient-to-br ${template.color} p-6 rounded-xl hover:scale-105 transition-transform cursor-pointer`}>
                      <div className="text-5xl mb-4 text-center">{template.icon}</div>
                      <h3 className="text-lg font-bold mb-2 text-center">{template.name}</h3>
                      <p className="text-sm opacity-90 text-center mb-1">{template.pages} pages</p>
                      <p className="text-sm opacity-90 text-center mb-4">{template.style} style</p>
                      <button className="w-full bg-white/20 hover:bg-white/30 py-2 rounded-lg font-semibold">
                        Use Template
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Design Tab */}
            {activeTab === 'design' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">🎨 Design Styles</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {designStyles.map((style, idx) => (
                    <div key={idx} className="bg-white/10 p-6 rounded-xl hover:bg-white/15 transition-all">
                      <div className="text-5xl mb-4">{style.icon}</div>
                      <h3 className="text-xl font-bold mb-2">{style.name}</h3>
                      <p className="text-sm text-gray-400 mb-4">{style.description}</p>
                      <button className="w-full bg-blue-600 hover:bg-blue-700 py-2 rounded-lg font-semibold">
                        Apply Style
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Export Tab */}
            {activeTab === 'export' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">📤 Export & Publish</h2>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                  {exportFormats.map((fmt, idx) => (
                    <div key={idx} className="bg-white/10 p-6 rounded-xl hover:bg-white/15 transition-all">
                      <div className="text-5xl mb-4">{fmt.icon}</div>
                      <h3 className="text-xl font-bold mb-2">{fmt.format}</h3>
                      <p className="text-sm text-gray-400 mb-2">{fmt.description}</p>
                      <p className="text-xs text-gray-500 mb-4">Quality: {fmt.quality}</p>
                      <button className="w-full bg-indigo-600 hover:bg-indigo-700 py-2 rounded-lg font-semibold">
                        Export {fmt.format}
                      </button>
                    </div>
                  ))}
                </div>

                <div className="bg-gradient-to-br from-blue-600/20 to-indigo-600/20 p-8 rounded-xl border border-blue-500/30">
                  <h3 className="text-2xl font-bold mb-4">🚀 Publishing Options</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <button className="bg-white/10 hover:bg-white/20 p-4 rounded-lg">
                      <div className="text-3xl mb-2">📚</div>
                      <p className="font-semibold">Amazon KDP</p>
                      <p className="text-xs text-gray-400">Publish to Kindle</p>
                    </button>
                    <button className="bg-white/10 hover:bg-white/20 p-4 rounded-lg">
                      <div className="text-3xl mb-2">📱</div>
                      <p className="font-semibold">Apple Books</p>
                      <p className="text-xs text-gray-400">iOS Distribution</p>
                    </button>
                    <button className="bg-white/10 hover:bg-white/20 p-4 rounded-lg">
                      <div className="text-3xl mb-2">🌐</div>
                      <p className="font-semibold">Direct Download</p>
                      <p className="text-xs text-gray-400">Host on your site</p>
                    </button>
                  </div>
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

export default EbookManager;
