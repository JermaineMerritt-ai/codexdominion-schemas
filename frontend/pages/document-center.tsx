import React, { useState, useRef } from 'react';
import Head from 'next/head';

interface Document {
  id: string;
  name: string;
  type: string;
  size: string;
  uploadedAt: Date;
  tags: string[];
  category: string;
  aiProcessed: boolean;
  aiInsights?: string;
  thumbnail?: string;
}

interface Category {
  id: string;
  name: string;
  icon: string;
  count: number;
  color: string;
}

export default function DocumentCenter() {
  const [documents, setDocuments] = useState<Document[]>([
    {
      id: '1',
      name: 'Azure Architecture Diagram.pdf',
      type: 'pdf',
      size: '2.4 MB',
      uploadedAt: new Date('2025-12-10T09:00:00'),
      tags: ['Azure', 'Architecture', 'Cloud'],
      category: 'technical',
      aiProcessed: true,
      aiInsights: 'System architecture with 3-tier design, Azure services integration',
    },
    {
      id: '2',
      name: 'Product Roadmap Q1 2025.docx',
      type: 'docx',
      size: '156 KB',
      uploadedAt: new Date('2025-12-09T14:30:00'),
      tags: ['Planning', 'Roadmap', 'Strategy'],
      category: 'business',
      aiProcessed: true,
      aiInsights: 'Q1 priorities: AI integration, performance optimization, user growth',
    },
    {
      id: '3',
      name: 'API Documentation v2.0.md',
      type: 'md',
      size: '89 KB',
      uploadedAt: new Date('2025-12-08T16:45:00'),
      tags: ['Documentation', 'API', 'Development'],
      category: 'technical',
      aiProcessed: true,
      aiInsights: 'REST API endpoints, authentication, rate limits, code examples',
    },
    {
      id: '4',
      name: 'Brand Guidelines.pdf',
      type: 'pdf',
      size: '5.2 MB',
      uploadedAt: new Date('2025-12-07T11:20:00'),
      tags: ['Design', 'Brand', 'Marketing'],
      category: 'marketing',
      aiProcessed: true,
      aiInsights: 'Logo usage, color palette, typography, brand voice guidelines',
    },
  ]);

  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const categories: Category[] = [
    { id: 'all', name: 'All Documents', icon: '📁', count: documents.length, color: 'gray' },
    { id: 'technical', name: 'Technical', icon: '⚙️', count: documents.filter(d => d.category === 'technical').length, color: 'blue' },
    { id: 'business', name: 'Business', icon: '💼', count: documents.filter(d => d.category === 'business').length, color: 'green' },
    { id: 'marketing', name: 'Marketing', icon: '📢', count: documents.filter(d => d.category === 'marketing').length, color: 'purple' },
    { id: 'legal', name: 'Legal', icon: '⚖️', count: 0, color: 'red' },
    { id: 'personal', name: 'Personal', icon: '👤', count: 0, color: 'yellow' },
  ];

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  };

  const handleFiles = (files: FileList) => {
    // In production, upload files to Azure Blob Storage and process with AI
    Array.from(files).forEach((file) => {
      const newDoc: Document = {
        id: Date.now().toString(),
        name: file.name,
        type: file.name.split('.').pop() || 'file',
        size: `${(file.size / 1024 / 1024).toFixed(2)} MB`,
        uploadedAt: new Date(),
        tags: [],
        category: 'technical',
        aiProcessed: false,
      };
      setDocuments((prev) => [newDoc, ...prev]);
    });
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      handleFiles(e.target.files);
    }
  };

  const filteredDocuments = documents.filter((doc) => {
    const matchesCategory = selectedCategory === 'all' || doc.category === selectedCategory;
    const matchesSearch = doc.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         doc.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCategory && matchesSearch;
  });

  const getFileIcon = (type: string) => {
    const icons: { [key: string]: string } = {
      pdf: '📄',
      doc: '📝',
      docx: '📝',
      txt: '📃',
      md: '📋',
      xlsx: '📊',
      xls: '📊',
      pptx: '📊',
      ppt: '📊',
      jpg: '🖼️',
      jpeg: '🖼️',
      png: '🖼️',
      gif: '🖼️',
      mp4: '🎥',
      mp3: '🎵',
      zip: '📦',
    };
    return icons[type.toLowerCase()] || '📄';
  };

  return (
    <>
      <Head>
        <title>Document Center | CodexDominion</title>
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-indigo-900 to-gray-900 text-white">
        {/* Header */}
        <div className="bg-gray-800/50 backdrop-blur-lg border-b border-gray-700 p-6">
          <div className="max-w-7xl mx-auto">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h1 className="text-3xl font-bold mb-2">📁 Document Center</h1>
                <p className="text-gray-400">AI-powered document management and search</p>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`px-4 py-2 rounded-lg ${viewMode === 'grid' ? 'bg-indigo-600' : 'bg-gray-700 hover:bg-gray-600'}`}
                >
                  ⊞ Grid
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`px-4 py-2 rounded-lg ${viewMode === 'list' ? 'bg-indigo-600' : 'bg-gray-700 hover:bg-gray-600'}`}
                >
                  ☰ List
                </button>
              </div>
            </div>

            {/* Search and Stats */}
            <div className="flex items-center space-x-4">
              <div className="flex-1 relative">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search documents, tags, content..."
                  className="w-full px-4 py-3 pl-12 bg-gray-900/50 border border-gray-700 rounded-lg focus:border-indigo-500 focus:outline-none"
                />
                <span className="absolute left-4 top-3.5 text-xl">🔍</span>
              </div>
              <div className="flex space-x-4 bg-gray-900/50 px-6 py-3 rounded-lg border border-gray-700">
                <div className="text-center">
                  <div className="text-2xl font-bold text-indigo-400">{documents.length}</div>
                  <div className="text-xs text-gray-400">Total</div>
                </div>
                <div className="border-l border-gray-700" />
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-400">{documents.filter(d => d.aiProcessed).length}</div>
                  <div className="text-xs text-gray-400">Processed</div>
                </div>
                <div className="border-l border-gray-700" />
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-400">
                    {documents.reduce((sum, d) => sum + parseFloat(d.size), 0).toFixed(1)}
                  </div>
                  <div className="text-xs text-gray-400">MB</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="flex h-[calc(100vh-180px)]">
          {/* Sidebar */}
          <div className="w-64 bg-gray-800/50 backdrop-blur-lg border-r border-gray-700 p-4 overflow-y-auto">
            <h3 className="text-sm font-bold mb-3 text-gray-400">CATEGORIES</h3>
            <div className="space-y-2 mb-6">
              {categories.map((category) => (
                <div
                  key={category.id}
                  onClick={() => setSelectedCategory(category.id)}
                  className={`p-3 rounded-lg cursor-pointer flex items-center justify-between ${
                    selectedCategory === category.id
                      ? 'bg-indigo-600'
                      : 'hover:bg-gray-700/50'
                  }`}
                >
                  <div className="flex items-center space-x-2">
                    <span className="text-xl">{category.icon}</span>
                    <span className="font-medium">{category.name}</span>
                  </div>
                  {category.count > 0 && (
                    <span className="text-xs bg-white/20 px-2 py-1 rounded">
                      {category.count}
                    </span>
                  )}
                </div>
              ))}
            </div>

            <h3 className="text-sm font-bold mb-3 text-gray-400">QUICK FILTERS</h3>
            <div className="space-y-2 mb-6">
              <div className="px-3 py-2 rounded-lg hover:bg-gray-700/50 cursor-pointer text-sm">
                ⭐ Starred
              </div>
              <div className="px-3 py-2 rounded-lg hover:bg-gray-700/50 cursor-pointer text-sm">
                🕒 Recent
              </div>
              <div className="px-3 py-2 rounded-lg hover:bg-gray-700/50 cursor-pointer text-sm">
                🤖 AI Processed
              </div>
              <div className="px-3 py-2 rounded-lg hover:bg-gray-700/50 cursor-pointer text-sm">
                🔖 Tagged
              </div>
            </div>

            <div className="border-t border-gray-700 pt-4">
              <h3 className="text-sm font-bold mb-3 text-gray-400">AI INSIGHTS</h3>
              <div className="space-y-2">
                <div className="p-3 bg-gradient-to-br from-purple-600/20 to-pink-600/20 border border-purple-500/30 rounded-lg text-xs">
                  <div className="font-semibold mb-1">Auto-tagging active</div>
                  <div className="text-gray-400">AI analyzing new uploads</div>
                </div>
                <div className="p-3 bg-gradient-to-br from-blue-600/20 to-cyan-600/20 border border-blue-500/30 rounded-lg text-xs">
                  <div className="font-semibold mb-1">Search powered by AI</div>
                  <div className="text-gray-400">Semantic search enabled</div>
                </div>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="flex-1 overflow-y-auto p-6">
            <div className="max-w-7xl mx-auto">
              {/* Upload Area */}
              <div
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                className={`mb-6 border-2 border-dashed rounded-xl p-8 text-center transition-all ${
                  dragActive
                    ? 'border-indigo-500 bg-indigo-600/20'
                    : 'border-gray-700 bg-gray-800/30 hover:border-gray-600'
                }`}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  multiple
                  onChange={handleFileInput}
                  className="hidden"
                  accept=".pdf,.doc,.docx,.txt,.md,.xlsx,.xls,.pptx,.ppt,.jpg,.jpeg,.png,.gif,.mp4,.mp3,.zip"
                />
                <div className="text-6xl mb-4">☁️</div>
                <h3 className="text-xl font-bold mb-2">Drop files here or click to upload</h3>
                <p className="text-gray-400 mb-4">
                  Supports: PDF, DOC, DOCX, TXT, MD, XLS, XLSX, PPT, PPTX, Images, Videos
                </p>
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg font-semibold hover:opacity-90"
                >
                  📤 Select Files
                </button>
                <div className="mt-4 text-sm text-gray-500">
                  AI will automatically process, tag, and extract insights from your documents
                </div>
              </div>

              {/* Documents */}
              {viewMode === 'grid' ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                  {filteredDocuments.map((doc) => (
                    <div
                      key={doc.id}
                      className="bg-gray-800/50 backdrop-blur-lg border border-gray-700 rounded-xl p-4 hover:border-indigo-500 transition-all cursor-pointer"
                    >
                      <div className="flex items-start justify-between mb-3">
                        <span className="text-4xl">{getFileIcon(doc.type)}</span>
                        <div className="flex space-x-1">
                          {doc.aiProcessed && (
                            <span className="text-green-400" title="AI Processed">🤖</span>
                          )}
                          <span className="text-gray-400 hover:text-yellow-400 cursor-pointer">⭐</span>
                        </div>
                      </div>
                      <h3 className="font-bold mb-2 line-clamp-2">{doc.name}</h3>
                      <div className="text-xs text-gray-400 mb-3">
                        {doc.size} • {doc.uploadedAt.toLocaleDateString()}
                      </div>
                      {doc.aiInsights && (
                        <div className="text-xs text-gray-400 mb-3 p-2 bg-purple-600/10 rounded border border-purple-500/20">
                          💡 {doc.aiInsights}
                        </div>
                      )}
                      <div className="flex flex-wrap gap-1">
                        {doc.tags.map((tag) => (
                          <span
                            key={tag}
                            className="text-xs px-2 py-1 bg-indigo-600/30 rounded"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="space-y-2">
                  {filteredDocuments.map((doc) => (
                    <div
                      key={doc.id}
                      className="bg-gray-800/50 backdrop-blur-lg border border-gray-700 rounded-lg p-4 hover:border-indigo-500 transition-all cursor-pointer flex items-center space-x-4"
                    >
                      <span className="text-3xl">{getFileIcon(doc.type)}</span>
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          <h3 className="font-bold">{doc.name}</h3>
                          {doc.aiProcessed && (
                            <span className="text-green-400 text-sm" title="AI Processed">🤖</span>
                          )}
                        </div>
                        <div className="flex items-center space-x-4 text-sm text-gray-400">
                          <span>{doc.size}</span>
                          <span>•</span>
                          <span>{doc.uploadedAt.toLocaleDateString()}</span>
                          <span>•</span>
                          <div className="flex space-x-1">
                            {doc.tags.map((tag) => (
                              <span
                                key={tag}
                                className="px-2 py-0.5 bg-indigo-600/30 rounded text-xs"
                              >
                                {tag}
                              </span>
                            ))}
                          </div>
                        </div>
                        {doc.aiInsights && (
                          <div className="mt-2 text-xs text-gray-400 p-2 bg-purple-600/10 rounded border border-purple-500/20">
                            💡 {doc.aiInsights}
                          </div>
                        )}
                      </div>
                      <div className="flex space-x-2">
                        <button className="px-3 py-2 bg-gray-700 rounded hover:bg-gray-600">
                          👁️ View
                        </button>
                        <button className="px-3 py-2 bg-gray-700 rounded hover:bg-gray-600">
                          ⬇️ Download
                        </button>
                        <button className="px-3 py-2 bg-gray-700 rounded hover:bg-gray-600">
                          ⋯
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {filteredDocuments.length === 0 && (
                <div className="text-center py-12">
                  <div className="text-6xl mb-4">📂</div>
                  <h3 className="text-xl font-bold mb-2">No documents found</h3>
                  <p className="text-gray-400">Try adjusting your search or filters</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
