import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import CodexNavigation from '../components/CodexNavigation';

interface Engine {
  id: string;
  name: string;
  cycle: string;
  activeTasks: number;
  pendingDispatches: number;
  performance: number;
  status: 'optimal' | 'warning' | 'critical';
  icon: string;
  trend: 'up' | 'down' | 'stable';
}

interface Avatar {
  id: string;
  name: string;
  domain: string;
  currentTask: string;
  activeConversations: number;
  performance: number;
  status: 'active' | 'idle' | 'processing';
  icon: string;
}

interface AIInsight {
  id: string;
  type: 'opportunity' | 'risk' | 'optimization' | 'idea';
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  timestamp: Date;
}

const SovereignDashboard = () => {
  const [cycleHealth, setCycleHealth] = useState(94);
  const [activeRituals, setActiveRituals] = useState(7);
  const [creatorImpact, setCreatorImpact] = useState(87);
  const [systemAlerts, setSystemAlerts] = useState(2);

  // API Base URL - uses Azure backend
  const apiBase = process.env.NEXT_PUBLIC_API_URL || "http://codex-backend.eastus.azurecontainer.io:8001";

  // Chat and AI Interaction States
  const [showAIChat, setShowAIChat] = useState(false);
  const [chatMessages, setChatMessages] = useState<{role: string, content: string}[]>([]);
  const [chatInput, setChatInput] = useState('');
  const [showUploadPanel, setShowUploadPanel] = useState(false);
  const [showMonetization, setShowMonetization] = useState(false);
  const [isLoadingChat, setIsLoadingChat] = useState(false);

  // Send message to AI backend
  const sendChatMessage = async () => {
    if (!chatInput.trim()) return;

    const userMessage = chatInput;
    setChatMessages([...chatMessages, {role: 'user', content: userMessage}]);
    setChatInput('');
    setIsLoadingChat(true);

    try {
      const response = await fetch(`${apiBase}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
      });

      const data = await response.json();
      setChatMessages(prev => [...prev, {
        role: 'assistant',
        content: data.response
      }]);
    } catch (error) {
      console.error('Chat error:', error);
      setChatMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Connection error. Please ensure the backend is running.'
      }]);
    } finally {
      setIsLoadingChat(false);
    }
  };

  // Handle file upload
  const handleFileUpload = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${apiBase}/api/upload`, {
        method: 'POST',
        body: formData
      });

      const data = await response.json();
      alert(`File uploaded successfully!\nFile ID: ${data.file_id}\nSize: ${data.size} bytes`);
      setShowUploadPanel(false);
    } catch (error) {
      console.error('Upload error:', error);
      alert('Upload failed. Please try again.');
    }
  };

  // Check backend health on mount
  useEffect(() => {
    fetch(`${apiBase}/health`)
      .then(res => res.json())
      .then(data => {
        console.log("Backend status:", data);
        console.log(`✅ Connected to Azure backend: ${apiBase}`);
      })
      .catch(err => {
        console.error("❌ Backend connection failed:", err);
        console.log(`Backend URL: ${apiBase}`);
      });
  }, [apiBase]);

  // Sixteen Engines Status - All Operational Systems
  const engines: Engine[] = [
    { id: '1', name: 'Distribution Engine', cycle: 'Dawn Cycle', activeTasks: 12, pendingDispatches: 5, performance: 96, status: 'optimal', icon: '📡', trend: 'up' },
    { id: '2', name: 'Marketing Engine', cycle: 'Growth Cycle', activeTasks: 18, pendingDispatches: 8, performance: 89, status: 'optimal', icon: '📊', trend: 'up' },
    { id: '3', name: 'Commerce Engine', cycle: 'Revenue Cycle', activeTasks: 24, pendingDispatches: 12, performance: 92, status: 'optimal', icon: '💰', trend: 'stable' },
    { id: '4', name: 'Observability Engine', cycle: 'Monitor Cycle', activeTasks: 31, pendingDispatches: 3, performance: 98, status: 'optimal', icon: '🔭', trend: 'up' },
    { id: '5', name: 'Avatar Studio', cycle: 'Creation Cycle', activeTasks: 15, pendingDispatches: 9, performance: 85, status: 'warning', icon: '👤', trend: 'down' },
    { id: '6', name: 'Niche Engine', cycle: 'Discovery Cycle', activeTasks: 9, pendingDispatches: 4, performance: 91, status: 'optimal', icon: '🎯', trend: 'up' },
    { id: '7', name: 'Compliance Engine', cycle: 'Guardian Cycle', activeTasks: 6, pendingDispatches: 2, performance: 99, status: 'optimal', icon: '✅', trend: 'stable' },
    { id: '8', name: 'Content Engine', cycle: 'Creative Cycle', activeTasks: 21, pendingDispatches: 11, performance: 88, status: 'optimal', icon: '✍️', trend: 'up' },
    { id: '9', name: 'Analytics Engine', cycle: 'Insight Cycle', activeTasks: 28, pendingDispatches: 7, performance: 94, status: 'optimal', icon: '📈', trend: 'up' },
    { id: '10', name: 'Automation Engine', cycle: 'Flow Cycle', activeTasks: 34, pendingDispatches: 15, performance: 91, status: 'optimal', icon: '⚡', trend: 'stable' },
    { id: '11', name: 'Communication Engine', cycle: 'Connection Cycle', activeTasks: 19, pendingDispatches: 6, performance: 93, status: 'optimal', icon: '📬', trend: 'up' },
    { id: '12', name: 'Intelligence Engine', cycle: 'Wisdom Cycle', activeTasks: 16, pendingDispatches: 4, performance: 97, status: 'optimal', icon: '🧠', trend: 'up' },
    { id: '13', name: 'Integration Engine', cycle: 'Unity Cycle', activeTasks: 22, pendingDispatches: 9, performance: 86, status: 'warning', icon: '🔗', trend: 'stable' },
    { id: '14', name: 'Security Engine', cycle: 'Shield Cycle', activeTasks: 11, pendingDispatches: 2, performance: 99, status: 'optimal', icon: '🛡️', trend: 'up' },
    { id: '15', name: 'Innovation Engine', cycle: 'Future Cycle', activeTasks: 13, pendingDispatches: 8, performance: 82, status: 'warning', icon: '💡', trend: 'down' },
    { id: '16', name: 'Sovereignty Engine', cycle: 'Eternal Cycle', activeTasks: 7, pendingDispatches: 1, performance: 100, status: 'optimal', icon: '👑', trend: 'up' },
  ];

  // 28 Sovereign Avatars (showing first 12)
  const avatars: Avatar[] = [
    { id: '1', name: 'Claude Sonnet', domain: 'Strategic Intelligence', currentTask: 'Revenue Analysis', activeConversations: 3, performance: 98, status: 'active', icon: '🧠' },
    { id: '2', name: 'GitHub Copilot', domain: 'Code Generation', currentTask: 'API Development', activeConversations: 5, performance: 95, status: 'active', icon: '💻' },
    { id: '3', name: 'Jermaine Action AI', domain: 'Command Execution', currentTask: 'System Orchestration', activeConversations: 8, performance: 97, status: 'active', icon: '⚡' },
    { id: '4', name: 'Marketing Maven', domain: 'Campaign Strategy', currentTask: 'Content Calendar', activeConversations: 4, performance: 91, status: 'active', icon: '📱' },
    { id: '5', name: 'Commerce Sage', domain: 'Sales Optimization', currentTask: 'Product Analysis', activeConversations: 6, performance: 93, status: 'active', icon: '🛍️' },
    { id: '6', name: 'Content Creator', domain: 'Creative Production', currentTask: 'Video Script', activeConversations: 2, performance: 88, status: 'processing', icon: '🎬' },
    { id: '7', name: 'Data Oracle', domain: 'Analytics & Insights', currentTask: 'Trend Prediction', activeConversations: 7, performance: 96, status: 'active', icon: '📊' },
    { id: '8', name: 'Customer Guardian', domain: 'Support & Relations', currentTask: 'Ticket Resolution', activeConversations: 12, performance: 94, status: 'active', icon: '💬' },
    { id: '9', name: 'SEO Sentinel', domain: 'Search Optimization', currentTask: 'Keyword Research', activeConversations: 3, performance: 90, status: 'active', icon: '🔍' },
    { id: '10', name: 'Social Conductor', domain: 'Platform Management', currentTask: 'Post Scheduling', activeConversations: 9, performance: 92, status: 'active', icon: '📲' },
    { id: '11', name: 'Email Architect', domain: 'Campaign Design', currentTask: 'Newsletter Build', activeConversations: 4, performance: 89, status: 'active', icon: '📧' },
    { id: '12', name: 'Compliance Keeper', domain: 'Regulatory Guardian', currentTask: 'Policy Review', activeConversations: 1, performance: 99, status: 'idle', icon: '⚖️' },
  ];

  // AI Insights Feed
  const insights: AIInsight[] = [
    { id: '1', type: 'opportunity', title: 'TikTok Revenue Surge', description: 'Short-form content performing 340% above average. Recommend doubling production.', priority: 'high', timestamp: new Date() },
    { id: '2', type: 'optimization', title: 'Automation Efficiency', description: 'Workflow consolidation could save 8 hours/week. Merge distribution pipelines.', priority: 'medium', timestamp: new Date() },
    { id: '3', type: 'risk', title: 'Server Load Alert', description: 'Commerce engine approaching capacity during peak hours. Scale recommended.', priority: 'high', timestamp: new Date() },
    { id: '4', type: 'idea', title: 'Caribbean Market Expansion', description: 'AI detected untapped demand in 3 Caribbean niches. Launch pilot campaign.', priority: 'medium', timestamp: new Date() },
  ];

  // Revenue Streams
  const revenueStreams = [
    { name: 'YouTube', revenue: 12500, trend: '+18%', icon: '📺', color: 'text-red-400' },
    { name: 'TikTok', revenue: 8300, trend: '+340%', icon: '🎵', color: 'text-pink-400' },
    { name: 'Affiliate', revenue: 15200, trend: '+12%', icon: '🔗', color: 'text-blue-400' },
    { name: 'WooCommerce', revenue: 22100, trend: '+8%', icon: '🛍️', color: 'text-green-400' },
    { name: 'Memberships', revenue: 18500, trend: '+22%', icon: '⭐', color: 'text-yellow-400' },
  ];

  const totalRevenue = revenueStreams.reduce((sum, stream) => sum + stream.revenue, 0);

  // All 50+ dashboards organized by category
  const allDashboards = [
    // Core Management
    { id: 'custodian', name: 'Custodian Dashboard', path: '/dashboard/custodian', icon: '👑', category: 'Core' },
    { id: 'heir', name: 'Heir Dashboard', path: '/dashboard/heir', icon: '🏺', category: 'Core' },
    { id: 'customer', name: 'Customer Dashboard', path: '/dashboard/customer', icon: '🌟', category: 'Core' },
    { id: 'council', name: 'Council Dashboard', path: '/apps/dashboard/pages/council', icon: '⚖️', category: 'Core' },
    { id: 'finance', name: 'Finance Dashboard', path: '/apps/dashboard/pages/finance', icon: '💰', category: 'Core' },

    // Revenue & Commerce
    { id: 'revenue', name: 'Revenue Crown', path: '/monetization', icon: '💎', category: 'Revenue' },
    { id: 'affiliate', name: 'Affiliate Command', path: '/affiliate-dashboard', icon: '🔗', category: 'Revenue' },
    { id: 'commerce', name: 'Commerce Hub', path: '/apps/commerce/pages/index', icon: '🛒', category: 'Revenue' },
    { id: 'woocommerce', name: 'WooCommerce Sync', path: '/woocommerce-dashboard', icon: '🛍️', category: 'Revenue' },

    // Social Media
    { id: 'youtube', name: 'YouTube Charts', path: '/youtube-analytics', icon: '📺', category: 'Social' },
    { id: 'tiktok', name: 'TikTok Earnings', path: '/tiktok-analytics', icon: '🎵', category: 'Social' },
    { id: 'threads', name: 'Threads Engagement', path: '/threads-analytics', icon: '🧵', category: 'Social' },
    { id: 'whatsapp', name: 'WhatsApp Business', path: '/whatsapp-analytics', icon: '💬', category: 'Social' },
    { id: 'pinterest', name: 'Pinterest Capsule', path: '/pinterest-analytics', icon: '📌', category: 'Social' },
    { id: 'buffer', name: 'Buffer Integration', path: '/buffer-dashboard', icon: '📤', category: 'Social' },

    // Communication
    { id: 'email', name: 'Email Dashboard', path: '/apps/dashboard/pages/email', icon: '📧', category: 'Communication' },
    { id: 'broadcast', name: 'Broadcast Center', path: '/apps/dashboard/pages/broadcast', icon: '📡', category: 'Communication' },
    { id: 'dawn', name: 'Dawn Dispatch', path: '/dawn-dispatch', icon: '🌅', category: 'Communication' },

    // AI & Automation Tools
    { id: 'copilot', name: 'Copilot AI', path: '/apps/dashboard/pages/copilot', icon: '🤖', category: 'AI Tools' },
    { id: 'action-ai', name: 'Jermaine Super Action AI', path: '/ai-command', icon: '⚡', category: 'AI Tools' },
    { id: 'avatar', name: 'Avatar System', path: '/avatar-dashboard', icon: '👤', category: 'AI Tools' },
    { id: 'video-studio', name: 'AI Video Studio', path: '/ai-video-studio', icon: '🎬', category: 'AI Tools' },
    { id: 'automation', name: 'Automation Studio (N8N Killer)', path: '/automation-studio', icon: '🔄', category: 'AI Tools' },
    { id: 'research', name: 'Research Studio (NotebookLLM)', path: '/research-studio', icon: '🔬', category: 'AI Tools' },
    { id: 'creative', name: 'Creative Studio (Nano Banana)', path: '/creative-studio', icon: '🎨', category: 'AI Tools' },
    { id: 'website-builder', name: 'Website Builder (Lovable)', path: '/website-builder', icon: '🚀', category: 'AI Tools' },
    { id: 'ebook', name: 'eBook Generator (Designrr)', path: '/ebook-manager', icon: '📚', category: 'AI Tools' },

    // Content & Knowledge
    { id: 'capsules', name: 'Capsules Archive', path: '/capsules', icon: '💊', category: 'Content' },
    { id: 'signals', name: 'Signals Dashboard', path: '/signals-enhanced', icon: '📊', category: 'Content' },
    { id: 'ebook', name: 'eBook Generator', path: '/ebook-manager', icon: '📚', category: 'Content' },
    { id: 'bulletin', name: 'Codex Bulletin', path: '/bulletin', icon: '📰', category: 'Content' },

    // Operations
    { id: 'observatory', name: 'Observatory', path: '/apps/observatory/pages/index', icon: '🔭', category: 'Operations' },
    { id: 'compliance', name: 'Compliance', path: '/apps/compliance/pages/index', icon: '✅', category: 'Operations' },
    { id: 'continuum', name: 'Continuum Flow', path: '/apps/dashboard/pages/continuum', icon: '♾️', category: 'Operations' },
    { id: 'approvals', name: 'Approvals', path: '/apps/dashboard/pages/approvals', icon: '✍️', category: 'Operations' },

    // Ceremonial
    { id: 'flame', name: 'Flame Eternal', path: '/flame-eternal', icon: '🔥', category: 'Ceremonial' },
    { id: 'stillness', name: 'Eternal Stillness', path: '/eternal-stillness', icon: '🌑', category: 'Ceremonial' },
    { id: 'covenant', name: 'Living Covenant', path: '/living-covenant', icon: '📜', category: 'Ceremonial' },
    { id: 'peace', name: 'Radiant Peace', path: '/codex-radiant-peace', icon: '🕊️', category: 'Ceremonial' },
    { id: 'proclamation', name: 'Eternal Proclamation', path: '/eternal-proclamation', icon: '📯', category: 'Ceremonial' },
    { id: 'serenity', name: 'Blessed Serenity', path: '/blessed-serenity', icon: '🌸', category: 'Ceremonial' },
    { id: 'silence', name: 'Eternal Silence', path: '/eternal-silence', icon: '🤫', category: 'Ceremonial' },
    { id: 'light', name: 'Eternal Light Peace', path: '/eternal-light-peace', icon: '✨', category: 'Ceremonial' },

    // Advanced
    { id: 'zenith', name: 'Day Zenith', path: '/day-zenith', icon: '☀️', category: 'Advanced' },
    { id: 'endurance', name: 'Night Endurance', path: '/night-endurance', icon: '🌙', category: 'Advanced' },
    { id: 'balance', name: 'Balance Renewal', path: '/balance-renewal', icon: '⚖️', category: 'Advanced' },
    { id: 'harvest', name: 'Harvest Serenity', path: '/harvest-serenity', icon: '🌾', category: 'Advanced' },
    { id: 'millennial', name: 'Millennial Sovereignty', path: '/millennial-sovereignty', icon: '🏛️', category: 'Advanced' },
    { id: 'transcendence', name: 'Eternal Transcendence', path: '/eternal-transcendence', icon: '🌌', category: 'Advanced' },
    { id: 'cosmic', name: 'Cosmic Sovereignty', path: '/cosmic-sovereignty', icon: '🌠', category: 'Advanced' },
    { id: 'perpetual', name: 'Perpetual Sovereignty', path: '/perpetual-sovereignty', icon: '⭕', category: 'Advanced' },
    { id: 'continuum-final', name: 'Final Continuum', path: '/final-continuum', icon: '🔄', category: 'Advanced' },
    { id: 'dominion', name: 'Ultimate Dominion', path: '/ultimate-dominion', icon: '👑', category: 'Advanced' },
    { id: 'inheritance', name: 'Sovereign Inheritance', path: '/sovereign-inheritance', icon: '🏺', category: 'Advanced' },
    { id: 'succession', name: 'Sovereign Succession', path: '/sovereign-succession', icon: '👥', category: 'Advanced' },
    { id: 'unity', name: 'Unity Continuum', path: '/unity-continuum', icon: '🤝', category: 'Advanced' },
    { id: 'supreme', name: 'Supreme Ultimate', path: '/supreme-ultimate', icon: '💫', category: 'Advanced' },
    { id: 'infinite', name: 'Infinite Serenity', path: '/infinite-serenity', icon: '∞', category: 'Advanced' },
  ];

  // Group dashboards by category
  const dashboardsByCategory = allDashboards.reduce((acc, dashboard) => {
    if (!acc[dashboard.category]) {
      acc[dashboard.category] = [];
    }
    acc[dashboard.category].push(dashboard);
    return acc;
  }, {} as Record<string, typeof allDashboards>);

  return (
    <>
      <Head>
        <title>👑 Sovereign Command Center - Codex Dominion</title>
        <meta name="description" content="Executive mythic command center for planetary operations" />
      </Head>

      <CodexNavigation />

      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 text-white p-4">
        <div className="max-w-[2400px] mx-auto">

          {/* 🜂 1. THE THRONE ROW - Sovereign KPIs */}
          <div className="mb-6">
            <div className="bg-gradient-to-r from-gold-600/20 via-yellow-600/20 to-gold-600/20 backdrop-blur-xl rounded-2xl p-6 border-2 border-gold-500/30">
              <h2 className="text-2xl font-bold mb-4 flex items-center gap-3">
                <span>👑</span>
                <span className="bg-gradient-to-r from-gold-400 to-yellow-400 bg-clip-text text-transparent">
                  THE THRONE ROW - Dominion Vitals
                </span>
              </h2>

              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                <div className="bg-white/5 p-4 rounded-xl border border-white/10">
                  <div className="text-xs text-gray-400 mb-1">Cycle Health</div>
                  <div className="text-3xl font-bold text-green-400">{cycleHealth}%</div>
                  <div className="text-xs text-green-400 mt-1">↑ Optimal</div>
                </div>

                <div className="bg-white/5 p-4 rounded-xl border border-white/10">
                  <div className="text-xs text-gray-400 mb-1">Active Rituals</div>
                  <div className="text-3xl font-bold text-blue-400">{activeRituals}</div>
                  <div className="text-xs text-blue-400 mt-1">Today</div>
                </div>

                <div className="bg-white/5 p-4 rounded-xl border border-white/10">
                  <div className="text-xs text-gray-400 mb-1">Total Revenue</div>
                  <div className="text-2xl font-bold text-green-400">${(totalRevenue/1000).toFixed(1)}K</div>
                  <div className="text-xs text-green-400 mt-1">↑ +15%</div>
                </div>

                <div className="bg-white/5 p-4 rounded-xl border border-white/10">
                  <div className="text-xs text-gray-400 mb-1">Creator Impact</div>
                  <div className="text-3xl font-bold text-purple-400">{creatorImpact}</div>
                  <div className="text-xs text-purple-400 mt-1">Global Score</div>
                </div>

                <div className="bg-white/5 p-4 rounded-xl border border-white/10">
                  <div className="text-xs text-gray-400 mb-1">Engines Status</div>
                  <div className="text-3xl font-bold text-cyan-400">16/16</div>
                  <div className="text-xs text-cyan-400 mt-1">↑ Active</div>
                </div>

                <div className="bg-white/5 p-4 rounded-xl border border-white/10">
                  <div className="text-xs text-gray-400 mb-1">System Alerts</div>
                  <div className="text-3xl font-bold text-yellow-400">{systemAlerts}</div>
                  <div className="text-xs text-yellow-400 mt-1">⚠ Review</div>
                </div>
              </div>
            </div>
          </div>

          {/* Main Content Grid */}
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">

            {/* Left Column */}
            <div className="xl:col-span-2 space-y-6">

              {/* 🜁 2. THE ENGINES GRID */}
              <div className="bg-white/5 backdrop-blur-xl rounded-2xl p-6 border border-white/10">
                <h2 className="text-2xl font-bold mb-4 flex items-center gap-3">
                  <span>⚙️</span>
                  <span>THE ENGINES GRID - Sixteen Living Systems</span>
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {engines.map((engine) => (
                    <div key={engine.id} className={`p-5 rounded-xl border-2 transition-all hover:scale-105 cursor-pointer ${
                      engine.status === 'optimal' ? 'bg-green-600/10 border-green-500/30' :
                      engine.status === 'warning' ? 'bg-yellow-600/10 border-yellow-500/30' :
                      'bg-red-600/10 border-red-500/30'
                    }`}>
                      <div className="flex justify-between items-start mb-3">
                        <span className="text-3xl">{engine.icon}</span>
                        <span className={`text-2xl ${
                          engine.trend === 'up' ? 'text-green-400' :
                          engine.trend === 'down' ? 'text-red-400' : 'text-gray-400'
                        }`}>
                          {engine.trend === 'up' ? '↗' : engine.trend === 'down' ? '↘' : '→'}
                        </span>
                      </div>
                      <h3 className="font-bold text-sm mb-2">{engine.name}</h3>
                      <div className="text-xs text-gray-400 mb-3">{engine.cycle}</div>
                      <div className="space-y-1 text-xs">
                        <div className="flex justify-between">
                          <span className="text-gray-400">Tasks:</span>
                          <span className="font-semibold">{engine.activeTasks}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Pending:</span>
                          <span className="font-semibold">{engine.pendingDispatches}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Performance:</span>
                          <span className="font-semibold text-green-400">{engine.performance}%</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* 🜄 3. THE OBSERVATORY */}
              <div className="bg-white/5 backdrop-blur-xl rounded-2xl p-6 border border-white/10">
                <h2 className="text-2xl font-bold mb-4 flex items-center gap-3">
                  <span>🔭</span>
                  <span>THE OBSERVATORY - Real-Time Monitoring</span>
                </h2>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  <div className="bg-white/5 p-4 rounded-xl">
                    <div className="text-xs text-gray-400 mb-1">CPU Load</div>
                    <div className="text-2xl font-bold text-cyan-400">23%</div>
                    <div className="h-2 bg-gray-700 rounded-full mt-2 overflow-hidden">
                      <div className="h-full bg-cyan-400 rounded-full w-[23%]"></div>
                    </div>
                  </div>
                  <div className="bg-white/5 p-4 rounded-xl">
                    <div className="text-xs text-gray-400 mb-1">Memory</div>
                    <div className="text-2xl font-bold text-green-400">47%</div>
                    <div className="h-2 bg-gray-700 rounded-full mt-2 overflow-hidden">
                      <div className="h-full bg-green-400 rounded-full w-[47%]"></div>
                    </div>
                  </div>
                  <div className="bg-white/5 p-4 rounded-xl">
                    <div className="text-xs text-gray-400 mb-1">Uptime</div>
                    <div className="text-2xl font-bold text-purple-400">99.9%</div>
                    <div className="text-xs text-green-400 mt-1">↑ 24d 7h</div>
                  </div>
                  <div className="bg-white/5 p-4 rounded-xl">
                    <div className="text-xs text-gray-400 mb-1">Latency</div>
                    <div className="text-2xl font-bold text-blue-400">18ms</div>
                    <div className="text-xs text-green-400 mt-1">↓ Optimal</div>
                  </div>
                </div>

                <div className="bg-white/5 p-4 rounded-xl">
                  <div className="text-sm font-semibold mb-3">System Health Timeline (24h)</div>
                  <div className="h-16 bg-gray-800/50 rounded-lg p-2 flex items-end gap-1">
                    {Array.from({ length: 24 }).map((_, i) => (
                      <div key={i} className="flex-1 bg-green-500 rounded-t" style={{ height: `${Math.random() * 80 + 20}%` }}></div>
                    ))}
                  </div>
                </div>
              </div>

              {/* 🜃 4. THE COMMERCE CONSTELLATION */}
              <div className="bg-white/5 backdrop-blur-xl rounded-2xl p-6 border border-white/10">
                <h2 className="text-2xl font-bold mb-4 flex items-center gap-3">
                  <span>💰</span>
                  <span>THE COMMERCE CONSTELLATION</span>
                </h2>

                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                  {revenueStreams.map((stream, idx) => (
                    <div key={idx} className="bg-white/5 p-4 rounded-xl hover:bg-white/10 transition-all">
                      <div className="text-3xl mb-2">{stream.icon}</div>
                      <div className="text-xs text-gray-400 mb-1">{stream.name}</div>
                      <div className={`text-xl font-bold ${stream.color}`}>${stream.revenue.toLocaleString()}</div>
                      <div className="text-xs text-green-400 mt-1">{stream.trend}</div>
                    </div>
                  ))}
                </div>

                <div className="mt-4 bg-gradient-to-r from-green-600/20 to-emerald-600/20 p-4 rounded-xl border border-green-500/30">
                  <div className="flex justify-between items-center">
                    <div>
                      <div className="text-sm text-gray-400">Total Monthly Revenue</div>
                      <div className="text-3xl font-bold text-green-400">${totalRevenue.toLocaleString()}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm text-gray-400">Caribbean Impact</div>
                      <div className="text-2xl font-bold text-yellow-400">32%</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Right Column */}
            <div className="space-y-6">

              {/* 🜁 5. THE CREATOR SPHERE */}
              <div className="bg-white/5 backdrop-blur-xl rounded-2xl p-6 border border-white/10">
                <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                  <span>🎨</span>
                  <span>CREATOR SPHERE</span>
                </h2>

                <div className="space-y-3">
                  <div className="bg-white/5 p-3 rounded-lg">
                    <div className="flex justify-between items-center">
                      <span className="text-sm">📺 YouTube Pipeline</span>
                      <span className="text-xs text-green-400">Active</span>
                    </div>
                    <div className="text-xs text-gray-400 mt-1">5 cartoons in production</div>
                  </div>
                  <div className="bg-white/5 p-3 rounded-lg">
                    <div className="flex justify-between items-center">
                      <span className="text-sm">📚 Books → Cartoons</span>
                      <span className="text-xs text-yellow-400">Converting</span>
                    </div>
                    <div className="text-xs text-gray-400 mt-1">3 stories ready</div>
                  </div>
                  <div className="bg-white/5 p-3 rounded-lg">
                    <div className="flex justify-between items-center">
                      <span className="text-sm">📤 Daily Dispatches</span>
                      <span className="text-xs text-blue-400">Scheduled</span>
                    </div>
                    <div className="text-xs text-gray-400 mt-1">12 posts queued</div>
                  </div>
                </div>
              </div>

              {/* 🜂 6. THE AVATAR COUNCIL */}
              <div className="bg-white/5 backdrop-blur-xl rounded-2xl p-6 border border-white/10">
                <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                  <span>👥</span>
                  <span>AVATAR COUNCIL (28)</span>
                </h2>

                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {avatars.map((avatar) => (
                    <div key={avatar.id} className="bg-white/5 p-3 rounded-lg hover:bg-white/10 transition-all cursor-pointer">
                      <div className="flex items-start gap-3">
                        <span className="text-2xl">{avatar.icon}</span>
                        <div className="flex-1 min-w-0">
                          <div className="flex justify-between items-start">
                            <h3 className="text-sm font-bold truncate">{avatar.name}</h3>
                            <span className={`px-2 py-0.5 rounded-full text-xs ${
                              avatar.status === 'active' ? 'bg-green-600' :
                              avatar.status === 'processing' ? 'bg-yellow-600' : 'bg-gray-600'
                            }`}>
                              {avatar.status}
                            </span>
                          </div>
                          <div className="text-xs text-gray-400 truncate">{avatar.domain}</div>
                          <div className="text-xs text-gray-500 truncate mt-1">{avatar.currentTask}</div>
                          <div className="flex gap-3 mt-1 text-xs">
                            <span className="text-blue-400">💬 {avatar.activeConversations}</span>
                            <span className="text-green-400">⚡ {avatar.performance}%</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* 🜁 9. THE COUNCIL FEED */}
              <div className="bg-white/5 backdrop-blur-xl rounded-2xl p-6 border border-white/10">
                <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                  <span>🧠</span>
                  <span>AI INSIGHTS</span>
                </h2>

                <div className="space-y-3">
                  {insights.map((insight) => (
                    <div key={insight.id} className={`p-3 rounded-lg border-l-4 ${
                      insight.type === 'opportunity' ? 'bg-green-600/10 border-green-500' :
                      insight.type === 'risk' ? 'bg-red-600/10 border-red-500' :
                      insight.type === 'optimization' ? 'bg-blue-600/10 border-blue-500' :
                      'bg-purple-600/10 border-purple-500'
                    }`}>
                      <div className="flex justify-between items-start mb-1">
                        <span className="text-sm font-bold">{insight.title}</span>
                        <span className={`px-2 py-0.5 rounded-full text-xs ${
                          insight.priority === 'high' ? 'bg-red-600' :
                          insight.priority === 'medium' ? 'bg-yellow-600' : 'bg-gray-600'
                        }`}>
                          {insight.priority}
                        </span>
                      </div>
                      <p className="text-xs text-gray-300">{insight.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* 🜂 10. THE SOVEREIGN COMMAND BAR */}
          <div className="fixed bottom-0 left-0 right-0 bg-gradient-to-r from-slate-950 via-purple-950 to-slate-950 backdrop-blur-xl border-t-2 border-gold-500/30 p-4 z-50">
            <div className="max-w-[2400px] mx-auto flex justify-center gap-3 flex-wrap">
              <button className="bg-gradient-to-r from-blue-600 to-cyan-600 px-6 py-3 rounded-xl font-semibold hover:scale-105 transition-transform">
                📤 Dispatch
              </button>
              <button className="bg-gradient-to-r from-purple-600 to-pink-600 px-6 py-3 rounded-xl font-semibold hover:scale-105 transition-transform">
                📦 Archive
              </button>
              <button className="bg-gradient-to-r from-green-600 to-emerald-600 px-6 py-3 rounded-xl font-semibold hover:scale-105 transition-transform">
                ⚙️ Activate Engine
              </button>
              <button className="bg-gradient-to-r from-orange-600 to-red-600 px-6 py-3 rounded-xl font-semibold hover:scale-105 transition-transform">
                ✨ Generate Artifact
              </button>
              <Link href="/avatar-dashboard">
                <button className="bg-gradient-to-r from-indigo-600 to-purple-600 px-6 py-3 rounded-xl font-semibold hover:scale-105 transition-transform">
                  👥 Avatar Council
                </button>
              </Link>
              <button className="bg-gradient-to-r from-gold-600 to-yellow-600 px-6 py-3 rounded-xl font-semibold hover:scale-105 transition-transform text-black">
                🜂 Run Ceremony
              </button>
              <Link href="/dashboard-selector">
                <button className="bg-gradient-to-r from-cyan-600 to-blue-600 px-6 py-3 rounded-xl font-semibold hover:scale-105 transition-transform">
                  📊 All Dashboards
                </button>
              </Link>
            </div>
          </div>

          {/* Spacer for fixed command bar */}
          <div className="h-24"></div>
        </div>
      </div>

      {/* 🤖 AI CHAT INTERFACE - Jermaine Super Action AI */}
      {showAIChat && (
        <div className="fixed bottom-24 right-6 w-96 h-[600px] bg-gradient-to-br from-slate-900 to-purple-900 rounded-2xl shadow-2xl border-2 border-purple-500/50 flex flex-col z-50">
          <div className="bg-gradient-to-r from-purple-600 to-pink-600 p-4 rounded-t-2xl flex justify-between items-center">
            <div className="flex items-center gap-2">
              <span className="text-2xl">⚡</span>
              <div>
                <h3 className="font-bold">Jermaine Super Action AI</h3>
                <p className="text-xs opacity-80">Copilot-Instruction Ready</p>
              </div>
            </div>
            <button onClick={() => setShowAIChat(false)} className="text-white hover:bg-white/20 rounded-lg p-2">✕</button>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {chatMessages.length === 0 ? (
              <div className="text-center text-gray-400 mt-20">
                <p className="text-4xl mb-4">🤖</p>
                <p className="text-sm">Start chatting with Jermaine Super Action AI</p>
                <p className="text-xs mt-2">Upload Copilot-Instruction.md or describe what you want built</p>
              </div>
            ) : (
              chatMessages.map((msg, idx) => (
                <div key={idx} className={`p-3 rounded-lg ${msg.role === 'user' ? 'bg-blue-600 ml-8' : 'bg-gray-700 mr-8'}`}>
                  <div className="text-xs opacity-70 mb-1">{msg.role === 'user' ? 'You' : 'Jermaine AI'}</div>
                  <div className="text-sm">{msg.content}</div>
                </div>
              ))
            )}
          </div>

          <div className="p-4 border-t border-gray-700">
            <div className="flex gap-2 mb-2">
              <button onClick={() => setShowUploadPanel(true)} className="px-3 py-1 bg-purple-600 rounded-lg text-xs hover:bg-purple-700">
                📎 Upload Doc
              </button>
              <button className="px-3 py-1 bg-blue-600 rounded-lg text-xs hover:bg-blue-700">
                📧 Email
              </button>
              <Link href="/ai-video-studio">
                <button className="px-3 py-1 bg-pink-600 rounded-lg text-xs hover:bg-pink-700">
                  🎬 Video Studio
                </button>
              </Link>
            </div>
            <div className="flex gap-2">
              <input
                type="text"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && chatInput.trim()) {
                    sendChatMessage();
                  }
                }}
                placeholder="Type your instruction or prompt..."
                className="flex-1 bg-gray-800 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
                disabled={isLoadingChat}
              />
              <button
                onClick={sendChatMessage}
                disabled={isLoadingChat}
                className="bg-gradient-to-r from-purple-600 to-pink-600 px-4 py-2 rounded-lg font-semibold hover:scale-105 disabled:opacity-50"
              >
                {isLoadingChat ? '...' : 'Send'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 📎 UPLOAD PANEL */}
      {showUploadPanel && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-gradient-to-br from-slate-900 to-purple-900 rounded-2xl p-6 w-[500px] border-2 border-purple-500/50">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold">📎 Upload Document</h3>
              <button onClick={() => setShowUploadPanel(false)} className="text-white hover:bg-white/20 rounded-lg p-2">✕</button>
            </div>
            <div className="border-2 border-dashed border-purple-500/50 rounded-xl p-8 text-center hover:border-purple-500 transition-all cursor-pointer">
              <p className="text-4xl mb-4">📄</p>
              <p className="text-sm text-gray-300 mb-2">Drop files here or click to browse</p>
              <p className="text-xs text-gray-500">Supports: PDF, DOCX, TXT, MD, Copilot-Instruction.md</p>
              <input
                type="file"
                className="hidden"
                id="file-upload"
                accept=".pdf,.doc,.docx,.txt,.md"
                onChange={(e) => {
                  if (e.target.files && e.target.files[0]) {
                    handleFileUpload(e.target.files[0]);
                  }
                }}
              />
              <label htmlFor="file-upload" className="cursor-pointer block">
                <span className="mt-4 inline-block bg-purple-600 px-6 py-2 rounded-lg hover:bg-purple-700">
                  Choose File
                </span>
              </label>
            </div>
            <div className="mt-4 space-y-2">
              <button className="w-full bg-purple-600 py-2 rounded-lg hover:bg-purple-700">
                📋 Copilot-Instruction.md Template
              </button>
              <button className="w-full bg-blue-600 py-2 rounded-lg hover:bg-blue-700">
                📧 Email Attachment
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 💰 MONETIZATION PANEL */}
      {showMonetization && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 overflow-y-auto">
          <div className="bg-gradient-to-br from-slate-900 to-emerald-900 rounded-2xl p-6 w-[900px] max-h-[80vh] overflow-y-auto border-2 border-emerald-500/50 m-4">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-2xl font-bold flex items-center gap-2">
                <span>💰</span>
                <span>Monetization Command Center</span>
              </h3>
              <button onClick={() => setShowMonetization(false)} className="text-white hover:bg-white/20 rounded-lg p-2">✕</button>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="bg-white/5 p-4 rounded-xl">
                <h4 className="font-bold mb-3 flex items-center gap-2">
                  <span>🛍️</span>
                  <span>Stores</span>
                </h4>
                <div className="space-y-2">
                  <button className="w-full bg-green-600 py-2 px-3 rounded-lg text-left hover:bg-green-700 text-sm">
                    WooCommerce Integration
                  </button>
                  <button className="w-full bg-blue-600 py-2 px-3 rounded-lg text-left hover:bg-blue-700 text-sm">
                    Shopify Connect
                  </button>
                  <button className="w-full bg-purple-600 py-2 px-3 rounded-lg text-left hover:bg-purple-700 text-sm">
                    Etsy Sync
                  </button>
                </div>
              </div>

              <div className="bg-white/5 p-4 rounded-xl">
                <h4 className="font-bold mb-3 flex items-center gap-2">
                  <span>📺</span>
                  <span>Channels</span>
                </h4>
                <div className="space-y-2">
                  <button className="w-full bg-red-600 py-2 px-3 rounded-lg text-left hover:bg-red-700 text-sm">
                    YouTube Revenue
                  </button>
                  <button className="w-full bg-pink-600 py-2 px-3 rounded-lg text-left hover:bg-pink-700 text-sm">
                    TikTok Creator Fund
                  </button>
                  <button className="w-full bg-blue-600 py-2 px-3 rounded-lg text-left hover:bg-blue-700 text-sm">
                    Twitch Earnings
                  </button>
                </div>
              </div>

              <div className="bg-white/5 p-4 rounded-xl">
                <h4 className="font-bold mb-3 flex items-center gap-2">
                  <span>🌐</span>
                  <span>Websites</span>
                </h4>
                <div className="space-y-2">
                  <button className="w-full bg-indigo-600 py-2 px-3 rounded-lg text-left hover:bg-indigo-700 text-sm">
                    WordPress Ads
                  </button>
                  <button className="w-full bg-cyan-600 py-2 px-3 rounded-lg text-left hover:bg-cyan-700 text-sm">
                    Affiliate Links
                  </button>
                  <button className="w-full bg-yellow-600 py-2 px-3 rounded-lg text-left hover:bg-yellow-700 text-sm">
                    Membership Sites
                  </button>
                </div>
              </div>

              <div className="bg-white/5 p-4 rounded-xl">
                <h4 className="font-bold mb-3 flex items-center gap-2">
                  <span>📱</span>
                  <span>Apps</span>
                </h4>
                <div className="space-y-2">
                  <button className="w-full bg-green-600 py-2 px-3 rounded-lg text-left hover:bg-green-700 text-sm">
                    App Store Revenue
                  </button>
                  <button className="w-full bg-blue-600 py-2 px-3 rounded-lg text-left hover:bg-blue-700 text-sm">
                    Google Play Earnings
                  </button>
                  <button className="w-full bg-purple-600 py-2 px-3 rounded-lg text-left hover:bg-purple-700 text-sm">
                    In-App Purchases
                  </button>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-r from-green-600/20 to-emerald-600/20 p-6 rounded-xl border border-green-500/30">
              <div className="text-center mb-4">
                <div className="text-sm text-gray-300">Total Revenue This Month</div>
                <div className="text-5xl font-bold text-green-400">${totalRevenue.toLocaleString()}</div>
              </div>
              <div className="grid grid-cols-4 gap-4 text-center">
                <div>
                  <div className="text-xs text-gray-400">Stores</div>
                  <div className="text-xl font-bold text-blue-400">$22.1K</div>
                </div>
                <div>
                  <div className="text-xs text-gray-400">Channels</div>
                  <div className="text-xl font-bold text-red-400">$20.8K</div>
                </div>
                <div>
                  <div className="text-xs text-gray-400">Websites</div>
                  <div className="text-xl font-bold text-cyan-400">$15.2K</div>
                </div>
                <div>
                  <div className="text-xs text-gray-400">Apps</div>
                  <div className="text-xl font-bold text-purple-400">$18.5K</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 🎬 FLOATING ACTION BUTTONS */}
      <div className="fixed right-6 bottom-32 flex flex-col gap-3 z-40">
        <button
          onClick={() => setShowAIChat(!showAIChat)}
          className="bg-gradient-to-r from-purple-600 to-pink-600 p-4 rounded-full shadow-2xl hover:scale-110 transition-transform"
          title="Chat with Jermaine Super Action AI"
        >
          <span className="text-2xl">⚡</span>
        </button>
        <button
          onClick={() => setShowMonetization(!showMonetization)}
          className="bg-gradient-to-r from-green-600 to-emerald-600 p-4 rounded-full shadow-2xl hover:scale-110 transition-transform"
          title="Monetization Center"
        >
          <span className="text-2xl">💰</span>
        </button>
        <Link href="/ai-video-studio">
          <button
            className="bg-gradient-to-r from-red-600 to-pink-600 p-4 rounded-full shadow-2xl hover:scale-110 transition-transform"
            title="AI Video Studio"
          >
            <span className="text-2xl">🎬</span>
          </button>
        </Link>
        <Link href="/avatar-dashboard">
          <button
            className="bg-gradient-to-r from-blue-600 to-cyan-600 p-4 rounded-full shadow-2xl hover:scale-110 transition-transform"
            title="Avatar Council"
          >
            <span className="text-2xl">👥</span>
          </button>
        </Link>
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

export default SovereignDashboard;
