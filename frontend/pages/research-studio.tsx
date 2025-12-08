import React, { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import CodexNavigation from '../components/CodexNavigation';

interface Document {
  id: string;
  title: string;
  type: string;
  pages: number;
  status: 'analyzing' | 'ready' | 'processing';
}

interface ResearchProject {
  id: string;
  name: string;
  documents: number;
  insights: number;
  status: 'active' | 'archived';
}

const ResearchStudio = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [documents, setDocuments] = useState<Document[]>([
    { id: '1', title: 'Market Research Report 2024', type: 'PDF', pages: 45, status: 'ready' },
    { id: '2', title: 'Product Specifications', type: 'DOCX', pages: 28, status: 'ready' },
    { id: '3', title: 'Financial Analysis Q4', type: 'XLSX', pages: 12, status: 'analyzing' },
  ]);

  const [projects, setProjects] = useState<ResearchProject[]>([
    { id: '1', name: 'Competitive Analysis', documents: 15, insights: 127, status: 'active' },
    { id: '2', name: 'Customer Research', documents: 23, insights: 198, status: 'active' },
    { id: '3', name: 'Industry Trends 2024', documents: 31, insights: 245, status: 'active' },
  ]);

  const supportedFormats = [
    { category: 'Documents', formats: ['PDF', 'DOCX', 'TXT', 'MD', 'RTF', 'ODT', 'EPUB'], icon: '📄' },
    { category: 'Presentations', formats: ['PPTX', 'KEY', 'ODP', 'PDF'], icon: '📊' },
    { category: 'Spreadsheets', formats: ['XLSX', 'CSV', 'ODS', 'Google Sheets'], icon: '📈' },
    { category: 'Multimedia', formats: ['MP4', 'MP3', 'WAV', 'PNG', 'JPG'], icon: '🎬' },
    { category: 'Code', formats: ['PY', 'JS', 'TS', 'HTML', 'CSS', 'JSON'], icon: '💻' },
    { category: 'Research', formats: ['Scientific Papers', 'Patents', 'Legal Docs'], icon: '🔬' },
    { category: 'Web', formats: ['Web Pages', 'Articles', 'Blogs'], icon: '🌐' },
    { category: 'Real-time', formats: ['Live Conversations', 'Meetings'], icon: '🎙️' },
  ];

  const aiCapabilities = [
    { name: 'Quantum Document Analysis', description: 'Deep understanding beyond surface text', icon: '🔮' },
    { name: 'Cross-Document Intelligence', description: 'Connect insights across unlimited documents', icon: '🔗' },
    { name: 'Multimedia Consciousness', description: 'Process video, audio, images with AI', icon: '🎭' },
    { name: 'Predictive Research', description: 'Anticipate research directions', icon: '🎯' },
    { name: 'Interactive Generation', description: 'Create videos, presentations, reports', icon: '✨' },
    { name: 'Real-time Collaboration', description: 'Team research with shared AI', icon: '👥' },
  ];

  return (
    <>
      <Head>
        <title>AI Research Studio - NotebookLLM Destroyer</title>
        <meta name="description" content="Consciousness-level research and analysis platform" />
      </Head>

      <CodexNavigation />

      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-green-900 to-slate-900 text-white p-8">
        <div className="max-w-[1800px] mx-auto">

          {/* Header */}
          <div className="text-center mb-10">
            <h1 className="text-5xl font-bold mb-3 bg-gradient-to-r from-green-400 via-emerald-400 to-teal-400 bg-clip-text text-transparent">
              🔬 AI Research Studio
            </h1>
            <p className="text-xl text-gray-300">
              Quantum Research & Analysis • Multimedia Intelligence • NotebookLLM Destroyer
            </p>
            <div className="flex justify-center gap-4 mt-4 flex-wrap">
              <span className="px-4 py-2 bg-red-600/30 rounded-full text-sm">💥 NotebookLLM Obliterator</span>
              <span className="px-4 py-2 bg-green-600/30 rounded-full text-sm">🧠 Consciousness-Level AI</span>
              <span className="px-4 py-2 bg-blue-600/30 rounded-full text-sm">📊 Multimedia Analysis</span>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-white/10 p-6 rounded-xl text-center">
              <div className="text-4xl font-bold text-green-400">{documents.length}</div>
              <div className="text-sm text-gray-400 mt-1">Documents Analyzed</div>
            </div>
            <div className="bg-white/10 p-6 rounded-xl text-center">
              <div className="text-4xl font-bold text-emerald-400">{projects.length}</div>
              <div className="text-sm text-gray-400 mt-1">Research Projects</div>
            </div>
            <div className="bg-white/10 p-6 rounded-xl text-center">
              <div className="text-4xl font-bold text-teal-400">570</div>
              <div className="text-sm text-gray-400 mt-1">AI Insights Generated</div>
            </div>
            <div className="bg-white/10 p-6 rounded-xl text-center">
              <div className="text-4xl font-bold text-cyan-400">∞</div>
              <div className="text-sm text-gray-400 mt-1">Analysis Depth</div>
            </div>
          </div>

          {/* Tab Navigation */}
          <div className="flex justify-center gap-4 mb-8 flex-wrap">
            {['dashboard', 'upload', 'projects', 'formats', 'capabilities'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-6 py-3 rounded-xl font-semibold transition-all ${
                  activeTab === tab
                    ? 'bg-gradient-to-r from-green-600 to-emerald-600 shadow-2xl scale-110'
                    : 'bg-white/10 hover:bg-white/20'
                }`}
              >
                {tab === 'dashboard' && '📊 Dashboard'}
                {tab === 'upload' && '📤 Upload & Analyze'}
                {tab === 'projects' && '📁 Projects'}
                {tab === 'formats' && '📋 Supported Formats'}
                {tab === 'capabilities' && '🚀 AI Capabilities'}
              </button>
            ))}
          </div>

          {/* Content */}
          <div className="bg-white/5 backdrop-blur-xl rounded-3xl p-8 border border-white/10">

            {/* Dashboard Tab */}
            {activeTab === 'dashboard' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">📊 Research Dashboard</h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                  <div className="bg-gradient-to-br from-green-600/20 to-emerald-600/20 p-6 rounded-xl border border-green-500/30">
                    <h3 className="text-xl font-bold mb-4">Recent Documents</h3>
                    <div className="space-y-3">
                      {documents.map((doc) => (
                        <div key={doc.id} className="bg-white/10 p-4 rounded-lg">
                          <div className="flex justify-between items-start">
                            <div>
                              <h4 className="font-bold">{doc.title}</h4>
                              <p className="text-sm text-gray-400">{doc.type} • {doc.pages} pages</p>
                            </div>
                            <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                              doc.status === 'ready' ? 'bg-green-600' :
                              doc.status === 'analyzing' ? 'bg-yellow-600' : 'bg-blue-600'
                            }`}>
                              {doc.status}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="bg-gradient-to-br from-emerald-600/20 to-teal-600/20 p-6 rounded-xl border border-emerald-500/30">
                    <h3 className="text-xl font-bold mb-4">AI Insights</h3>
                    <div className="space-y-3">
                      <div className="bg-white/10 p-4 rounded-lg">
                        <div className="flex items-start gap-3">
                          <span className="text-2xl">💡</span>
                          <div>
                            <p className="font-semibold">Market trend identified</p>
                            <p className="text-sm text-gray-400">AI detected 3 emerging patterns in market data</p>
                          </div>
                        </div>
                      </div>
                      <div className="bg-white/10 p-4 rounded-lg">
                        <div className="flex items-start gap-3">
                          <span className="text-2xl">🎯</span>
                          <div>
                            <p className="font-semibold">Cross-document connection</p>
                            <p className="text-sm text-gray-400">5 related insights found across projects</p>
                          </div>
                        </div>
                      </div>
                      <div className="bg-white/10 p-4 rounded-lg">
                        <div className="flex items-start gap-3">
                          <span className="text-2xl">🔮</span>
                          <div>
                            <p className="font-semibold">Predictive suggestion</p>
                            <p className="text-sm text-gray-400">AI recommends 4 new research directions</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-white/10 p-6 rounded-xl">
                  <h3 className="text-xl font-bold mb-4">Quick Actions</h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <button className="bg-green-600 hover:bg-green-700 py-4 rounded-xl font-semibold transition-all">
                      📤 Upload Document
                    </button>
                    <button className="bg-emerald-600 hover:bg-emerald-700 py-4 rounded-xl font-semibold transition-all">
                      📊 New Project
                    </button>
                    <button className="bg-teal-600 hover:bg-teal-700 py-4 rounded-xl font-semibold transition-all">
                      🤖 Ask AI
                    </button>
                    <button className="bg-cyan-600 hover:bg-cyan-700 py-4 rounded-xl font-semibold transition-all">
                      📈 Generate Report
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Upload Tab */}
            {activeTab === 'upload' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">📤 Upload & Analyze Documents</h2>

                <div className="bg-white/10 p-12 rounded-xl border-2 border-dashed border-white/30 mb-6 text-center">
                  <div className="text-6xl mb-4">📁</div>
                  <p className="text-2xl font-semibold mb-2">Drop files here or click to upload</p>
                  <p className="text-gray-400 mb-6">Supports: PDF, DOCX, XLSX, PPTX, Images, Videos, Audio, Code, and more</p>
                  <button className="bg-gradient-to-r from-green-600 to-emerald-600 px-8 py-3 rounded-xl font-semibold hover:scale-105 transition-transform">
                    Choose Files
                  </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="bg-white/10 p-6 rounded-xl">
                    <h3 className="text-lg font-bold mb-3">🎯 Analysis Options</h3>
                    <div className="space-y-2">
                      <label className="flex items-center gap-2">
                        <input type="checkbox" defaultChecked className="rounded" />
                        <span className="text-sm">Deep Content Analysis</span>
                      </label>
                      <label className="flex items-center gap-2">
                        <input type="checkbox" defaultChecked className="rounded" />
                        <span className="text-sm">Extract Key Insights</span>
                      </label>
                      <label className="flex items-center gap-2">
                        <input type="checkbox" defaultChecked className="rounded" />
                        <span className="text-sm">Cross-Reference Existing</span>
                      </label>
                      <label className="flex items-center gap-2">
                        <input type="checkbox" className="rounded" />
                        <span className="text-sm">Generate Summary</span>
                      </label>
                      <label className="flex items-center gap-2">
                        <input type="checkbox" className="rounded" />
                        <span className="text-sm">Create Presentation</span>
                      </label>
                    </div>
                  </div>

                  <div className="bg-white/10 p-6 rounded-xl">
                    <h3 className="text-lg font-bold mb-3">🤖 AI Enhancement</h3>
                    <div className="space-y-2">
                      <label className="flex items-center gap-2">
                        <input type="checkbox" defaultChecked className="rounded" />
                        <span className="text-sm">Quantum Analysis</span>
                      </label>
                      <label className="flex items-center gap-2">
                        <input type="checkbox" defaultChecked className="rounded" />
                        <span className="text-sm">Predictive Insights</span>
                      </label>
                      <label className="flex items-center gap-2">
                        <input type="checkbox" className="rounded" />
                        <span className="text-sm">Multimedia Processing</span>
                      </label>
                      <label className="flex items-center gap-2">
                        <input type="checkbox" className="rounded" />
                        <span className="text-sm">Real-time Monitoring</span>
                      </label>
                    </div>
                  </div>

                  <div className="bg-white/10 p-6 rounded-xl">
                    <h3 className="text-lg font-bold mb-3">📊 Output Format</h3>
                    <select className="w-full bg-black/30 border border-white/20 rounded-lg px-4 py-2 mb-3" aria-label="Output Format">
                      <option>Interactive Dashboard</option>
                      <option>PDF Report</option>
                      <option>PowerPoint Presentation</option>
                      <option>Video Summary</option>
                      <option>Audio Briefing</option>
                    </select>
                    <button className="w-full bg-green-600 hover:bg-green-700 py-2 rounded-lg font-semibold">
                      Start Analysis
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Projects Tab */}
            {activeTab === 'projects' && (
              <div>
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-3xl font-bold">📁 Research Projects</h2>
                  <button className="bg-gradient-to-r from-green-600 to-emerald-600 px-6 py-3 rounded-xl font-semibold hover:scale-105 transition-transform">
                    + New Project
                  </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {projects.map((project) => (
                    <div key={project.id} className="bg-white/10 p-6 rounded-xl hover:bg-white/15 transition-all">
                      <h3 className="text-xl font-bold mb-3">{project.name}</h3>
                      <div className="space-y-2 mb-4">
                        <p className="text-sm text-gray-400">📄 {project.documents} documents</p>
                        <p className="text-sm text-gray-400">💡 {project.insights} AI insights</p>
                        <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${
                          project.status === 'active' ? 'bg-green-600' : 'bg-gray-600'
                        }`}>
                          {project.status.toUpperCase()}
                        </span>
                      </div>
                      <div className="flex gap-2">
                        <button className="flex-1 bg-green-600 hover:bg-green-700 py-2 rounded-lg text-sm font-semibold">
                          Open
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

            {/* Formats Tab */}
            {activeTab === 'formats' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">📋 Supported File Formats</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {supportedFormats.map((category, idx) => (
                    <div key={idx} className="bg-white/10 p-6 rounded-xl">
                      <div className="text-4xl mb-3">{category.icon}</div>
                      <h3 className="text-lg font-bold mb-3">{category.category}</h3>
                      <div className="space-y-1">
                        {category.formats.map((format, fidx) => (
                          <p key={fidx} className="text-sm text-gray-400">✓ {format}</p>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Capabilities Tab */}
            {activeTab === 'capabilities' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">🚀 AI Capabilities</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {aiCapabilities.map((capability, idx) => (
                    <div key={idx} className="bg-gradient-to-br from-green-600/20 to-emerald-600/20 p-6 rounded-xl border border-green-500/30">
                      <div className="text-5xl mb-4">{capability.icon}</div>
                      <h3 className="text-xl font-bold mb-2">{capability.name}</h3>
                      <p className="text-sm text-gray-300">{capability.description}</p>
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

export default ResearchStudio;
