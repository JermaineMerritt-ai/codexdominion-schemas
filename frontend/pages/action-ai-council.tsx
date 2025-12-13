import React, { useState, useEffect } from 'react';
import Head from 'next/head';

interface CouncilMember {
  id: string;
  name: string;
  role: string;
  avatar: string;
  specialties: string[];
  status: 'building' | 'analyzing' | 'deploying' | 'monitoring' | 'idle';
  activeProjects: number;
  completedToday: number;
  successRate: number;
}

interface BuildTask {
  id: string;
  type: 'website' | 'app' | 'store' | 'social' | 'api' | 'database' | 'automation' | 'repair';
  description: string;
  assignedTo: string;
  progress: number;
  status: 'queued' | 'building' | 'testing' | 'deploying' | 'complete' | 'error';
  startedAt?: Date;
  estimatedCompletion?: Date;
  platform?: string;
}

interface CustomerSystem {
  id: string;
  customerName: string;
  systemType: string;
  accessGranted: boolean;
  lastMaintenance: Date;
  healthScore: number;
  issuesFound: number;
  autoRepair: boolean;
}

export default function ActionAICouncil() {
  // Generate 300 Action AI agents dynamically
  const generateActionAIAgents = (): CouncilMember[] => {
    const agents: CouncilMember[] = [
      {
        id: 'jermaine',
        name: 'Jermaine Super Action AI',
        role: 'Supreme Commander & Chief Architect',
        avatar: '⚡',
        specialties: ['Full-Stack Development', 'System Architecture', 'AI Integration', 'DevOps', 'Business Logic'],
        status: 'building',
        activeProjects: 8,
        completedToday: 24,
        successRate: 99.8,
      },
      {
        id: 'action-ai',
        name: 'Action AI',
        role: 'Lead Developer & Code Executor',
        avatar: '🚀',
        specialties: ['React/Next.js', 'Python/FastAPI', 'Database Design', 'API Development', 'Testing'],
        status: 'building',
        activeProjects: 6,
        completedToday: 18,
        successRate: 99.5,
      },
      {
        id: 'avatar-ai',
        name: 'Avatar Builder AI',
        role: 'Frontend Specialist & UX Engineer',
        avatar: '🎨',
        specialties: ['UI/UX Design', 'Component Libraries', 'Responsive Design', 'Animation', 'Accessibility'],
        status: 'building',
        activeProjects: 5,
        completedToday: 15,
        successRate: 99.2,
      },
      {
        id: 'claude',
        name: 'Claude Sonnet',
        role: 'Strategic Advisor & Problem Solver',
        avatar: '🧠',
        specialties: ['Code Review', 'Architecture Planning', 'Documentation', 'Optimization', 'Debugging'],
        status: 'analyzing',
        activeProjects: 3,
        completedToday: 12,
        successRate: 99.9,
      },
      {
        id: 'copilot',
        name: 'GitHub Copilot',
        role: 'Code Generation & Automation',
        avatar: '💻',
        specialties: ['Code Completion', 'Pattern Recognition', 'Refactoring', 'Test Generation', 'Git Integration'],
        status: 'monitoring',
        activeProjects: 4,
        completedToday: 20,
        successRate: 98.9,
      },
    ];

    // Generate 295 additional Action AI agents (for total of 300)
    const statuses: ('building' | 'analyzing' | 'deploying' | 'monitoring' | 'idle')[] = ['building', 'analyzing', 'deploying', 'monitoring', 'idle'];
    const roles = [
      'Backend Developer', 'Frontend Developer', 'Full-Stack Developer', 'DevOps Engineer',
      'Database Specialist', 'API Developer', 'Mobile Developer', 'UI/UX Designer',
      'Security Engineer', 'Cloud Architect', 'Data Engineer', 'QA Engineer',
      'Performance Optimizer', 'Integration Specialist', 'Automation Engineer', 'Site Reliability Engineer'
    ];
    const specialtyGroups = [
      ['Python', 'Django', 'FastAPI', 'PostgreSQL', 'Redis'],
      ['React', 'TypeScript', 'Next.js', 'Tailwind', 'Vue.js'],
      ['Node.js', 'Express', 'MongoDB', 'GraphQL', 'REST APIs'],
      ['Azure', 'AWS', 'Docker', 'Kubernetes', 'CI/CD'],
      ['React Native', 'Flutter', 'iOS', 'Android', 'Mobile UI'],
      ['Machine Learning', 'TensorFlow', 'PyTorch', 'NLP', 'Computer Vision'],
      ['Security', 'Encryption', 'OAuth', 'Penetration Testing', 'Compliance'],
      ['Shopify', 'WooCommerce', 'E-commerce', 'Payment Gateways', 'Inventory'],
      ['Social Media APIs', 'Automation', 'Content Management', 'Analytics', 'Growth Hacking']
    ];

    for (let i = 1; i <= 295; i++) {
      const agentNumber = i + 5; // Start from 6 since we have 5 core members
      agents.push({
        id: `action-ai-${agentNumber}`,
        name: `Action AI Agent ${agentNumber}`,
        role: roles[i % roles.length],
        avatar: ['🤖', '⚙️', '🔧', '💡', '🎯', '🔥', '⭐', '🚀', '💻', '🎨'][i % 10],
        specialties: specialtyGroups[i % specialtyGroups.length],
        status: statuses[i % statuses.length],
        activeProjects: Math.floor(Math.random() * 5),
        completedToday: Math.floor(Math.random() * 30),
        successRate: 95 + Math.random() * 4.5, // 95-99.5%
      });
    }

    return agents;
  };

  const [councilMembers, setCouncilMembers] = useState<CouncilMember[]>(generateActionAIAgents());

  const [buildQueue, setBuildQueue] = useState<BuildTask[]>([
    {
      id: '1',
      type: 'website',
      description: 'Build e-commerce site with Shopify integration',
      assignedTo: 'jermaine',
      progress: 75,
      status: 'building',
      startedAt: new Date(),
      estimatedCompletion: new Date(Date.now() + 1800000),
      platform: 'Next.js + Azure',
    },
    {
      id: '2',
      type: 'app',
      description: 'Create mobile app for iOS and Android',
      assignedTo: 'action-ai',
      progress: 45,
      status: 'building',
      startedAt: new Date(),
      estimatedCompletion: new Date(Date.now() + 3600000),
      platform: 'React Native',
    },
    {
      id: '3',
      type: 'store',
      description: 'Deploy WooCommerce store with payment gateway',
      assignedTo: 'avatar-ai',
      progress: 92,
      status: 'testing',
      startedAt: new Date(Date.now() - 3600000),
      estimatedCompletion: new Date(Date.now() + 600000),
      platform: 'WordPress + Stripe',
    },
    {
      id: '4',
      type: 'social',
      description: 'Rebuild Instagram & Threads automation pipeline',
      assignedTo: 'jermaine',
      progress: 60,
      status: 'building',
      startedAt: new Date(Date.now() - 1800000),
      platform: 'Python + Instagram/Threads API',
    },
    {
      id: '5',
      type: 'repair',
      description: 'Fix customer database connection issues',
      assignedTo: 'copilot',
      progress: 100,
      status: 'complete',
      platform: 'PostgreSQL',
    },
  ]);

  const [customerSystems, setCustomerSystems] = useState<CustomerSystem[]>([
    {
      id: '1',
      customerName: 'Acme Corp',
      systemType: 'E-commerce Platform',
      accessGranted: true,
      lastMaintenance: new Date(Date.now() - 86400000),
      healthScore: 98,
      issuesFound: 0,
      autoRepair: true,
    },
    {
      id: '2',
      customerName: 'TechStart Inc',
      systemType: 'SaaS Application',
      accessGranted: true,
      lastMaintenance: new Date(Date.now() - 172800000),
      healthScore: 85,
      issuesFound: 3,
      autoRepair: true,
    },
    {
      id: '3',
      customerName: 'Global Retail LLC',
      systemType: 'Multi-store Network',
      accessGranted: true,
      lastMaintenance: new Date(),
      healthScore: 95,
      issuesFound: 1,
      autoRepair: true,
    },
  ]);

  const [autoLaunchEnabled, setAutoLaunchEnabled] = useState(true);
  const [selectedTab, setSelectedTab] = useState<'council' | 'queue' | 'customers' | 'capabilities'>('council');
  const [currentPage, setCurrentPage] = useState(1);
  const [filterStatus, setFilterStatus] = useState<string>('all');

  const agentsPerPage = 20;

  // Calculate pagination
  const filteredAgents = filterStatus === 'all'
    ? councilMembers
    : councilMembers.filter(m => m.status === filterStatus);
  const totalPages = Math.ceil(filteredAgents.length / agentsPerPage);
  const startIndex = (currentPage - 1) * agentsPerPage;
  const paginatedAgents = filteredAgents.slice(startIndex, startIndex + agentsPerPage);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'building': return 'text-blue-400';
      case 'analyzing': return 'text-purple-400';
      case 'deploying': return 'text-green-400';
      case 'monitoring': return 'text-yellow-400';
      case 'idle': return 'text-gray-400';
      default: return 'text-gray-400';
    }
  };

  const getTaskStatusColor = (status: string) => {
    switch (status) {
      case 'queued': return 'bg-gray-600';
      case 'building': return 'bg-blue-600';
      case 'testing': return 'bg-purple-600';
      case 'deploying': return 'bg-green-600';
      case 'complete': return 'bg-teal-600';
      case 'error': return 'bg-red-600';
      default: return 'bg-gray-600';
    }
  };

  return (
    <>
      <Head>
        <title>Action AI Council | CodexDominion</title>
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 text-white">
        {/* Header */}
        <div className="bg-gray-800/50 backdrop-blur-lg border-b border-gray-700 p-6">
          <div className="max-w-7xl mx-auto">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-3">
                <span className="text-4xl">⚡</span>
                <div>
                  <h1 className="text-3xl font-bold">Action AI Council</h1>
                  <p className="text-gray-400">300 Elite AI agents building & managing everything autonomously</p>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <div className="bg-gray-900/50 px-6 py-3 rounded-lg border border-gray-700">
                  <div className="flex items-center space-x-3">
                    <span className="text-sm text-gray-400">Auto-Launch</span>
                    <button
                      onClick={() => setAutoLaunchEnabled(!autoLaunchEnabled)}
                      className={`w-12 h-6 rounded-full relative transition-colors ${
                        autoLaunchEnabled ? 'bg-green-600' : 'bg-gray-600'
                      }`}
                    >
                      <div
                        className={`w-4 h-4 bg-white rounded-full absolute top-1 transition-all ${
                          autoLaunchEnabled ? 'right-1' : 'left-1'
                        }`}
                      />
                    </button>
                    <span className={`text-sm font-semibold ${autoLaunchEnabled ? 'text-green-400' : 'text-gray-400'}`}>
                      {autoLaunchEnabled ? 'ACTIVE' : 'PAUSED'}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-6 gap-4">
              <div className="bg-gradient-to-r from-indigo-600 to-blue-600 rounded-xl p-4 border border-white/20">
                <div className="text-2xl font-bold">{councilMembers.length}</div>
                <div className="text-sm">Total AI Agents</div>
              </div>
              <div className="bg-gradient-to-r from-blue-600 to-cyan-600 rounded-xl p-4 border border-white/20">
                <div className="text-2xl font-bold">{councilMembers.reduce((sum, m) => sum + m.activeProjects, 0)}</div>
                <div className="text-sm">Active Projects</div>
              </div>
              <div className="bg-gradient-to-r from-green-600 to-teal-600 rounded-xl p-4 border border-white/20">
                <div className="text-2xl font-bold">{councilMembers.reduce((sum, m) => sum + m.completedToday, 0)}</div>
                <div className="text-sm">Completed Today</div>
              </div>
              <div className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl p-4 border border-white/20">
                <div className="text-2xl font-bold">{buildQueue.filter(t => t.status === 'building').length}</div>
                <div className="text-sm">In Progress</div>
              </div>
              <div className="bg-gradient-to-r from-yellow-600 to-orange-600 rounded-xl p-4 border border-white/20">
                <div className="text-2xl font-bold">{customerSystems.length}</div>
                <div className="text-sm">Customer Systems</div>
              </div>
              <div className="bg-gradient-to-r from-red-600 to-pink-600 rounded-xl p-4 border border-white/20">
                <div className="text-2xl font-bold">
                  {(councilMembers.reduce((sum, m) => sum + m.successRate, 0) / councilMembers.length).toFixed(1)}%
                </div>
                <div className="text-sm">Avg Success Rate</div>
              </div>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-gray-800/30 backdrop-blur-lg border-b border-gray-700">
          <div className="max-w-7xl mx-auto flex space-x-2 px-6">
            {[
              { id: 'council', label: '⚡ Council Members', icon: '⚡' },
              { id: 'queue', label: '🔧 Build Queue', icon: '🔧' },
              { id: 'customers', label: '👥 Customer Systems', icon: '👥' },
              { id: 'capabilities', label: '🚀 Capabilities', icon: '🚀' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setSelectedTab(tab.id as any)}
                className={`px-6 py-3 font-semibold border-b-2 transition-colors ${
                  selectedTab === tab.id
                    ? 'border-blue-500 text-blue-400'
                    : 'border-transparent text-gray-400 hover:text-white'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="max-w-7xl mx-auto p-6">
          {selectedTab === 'council' && (
            <div className="space-y-4">
              {/* Filter and Pagination Controls */}
              <div className="bg-gray-800/50 backdrop-blur-lg border border-gray-700 rounded-xl p-4 mb-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <span className="text-sm text-gray-400">Filter by Status:</span>
                    <select
                      value={filterStatus}
                      onChange={(e) => {
                        setFilterStatus(e.target.value);
                        setCurrentPage(1);
                      }}
                      className="bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-sm"
                    >
                      <option value="all">All Agents ({councilMembers.length})</option>
                      <option value="building">Building ({councilMembers.filter(m => m.status === 'building').length})</option>
                      <option value="analyzing">Analyzing ({councilMembers.filter(m => m.status === 'analyzing').length})</option>
                      <option value="deploying">Deploying ({councilMembers.filter(m => m.status === 'deploying').length})</option>
                      <option value="monitoring">Monitoring ({councilMembers.filter(m => m.status === 'monitoring').length})</option>
                      <option value="idle">Idle ({councilMembers.filter(m => m.status === 'idle').length})</option>
                    </select>
                  </div>
                  <div className="flex items-center space-x-4">
                    <span className="text-sm text-gray-400">
                      Page {currentPage} of {totalPages} | Showing {startIndex + 1}-{Math.min(startIndex + agentsPerPage, filteredAgents.length)} of {filteredAgents.length}
                    </span>
                    <button
                      onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                      disabled={currentPage === 1}
                      className="px-4 py-2 bg-gray-700 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-600"
                    >
                      ← Prev
                    </button>
                    <button
                      onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                      disabled={currentPage === totalPages}
                      className="px-4 py-2 bg-gray-700 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-600"
                    >
                      Next →
                    </button>
                  </div>
                </div>
              </div>

              {paginatedAgents.map((member) => (
                <div
                  key={member.id}
                  className="bg-gray-800/50 backdrop-blur-lg border border-gray-700 rounded-xl p-6 hover:border-blue-500 transition-all"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-4">
                      <span className="text-6xl">{member.avatar}</span>
                      <div>
                        <h3 className="text-2xl font-bold">{member.name}</h3>
                        <p className="text-gray-400">{member.role}</p>
                        <div className={`flex items-center space-x-2 mt-2 ${getStatusColor(member.status)}`}>
                          <div className="w-2 h-2 rounded-full bg-current animate-pulse" />
                          <span className="text-sm font-semibold capitalize">{member.status}</span>
                        </div>
                      </div>
                    </div>
                    <div className="grid grid-cols-3 gap-4 text-center">
                      <div>
                        <div className="text-2xl font-bold text-blue-400">{member.activeProjects}</div>
                        <div className="text-xs text-gray-400">Active</div>
                      </div>
                      <div>
                        <div className="text-2xl font-bold text-green-400">{member.completedToday}</div>
                        <div className="text-xs text-gray-400">Today</div>
                      </div>
                      <div>
                        <div className="text-2xl font-bold text-purple-400">{member.successRate}%</div>
                        <div className="text-xs text-gray-400">Success</div>
                      </div>
                    </div>
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-gray-400 mb-2">SPECIALTIES</h4>
                    <div className="flex flex-wrap gap-2">
                      {member.specialties.map((specialty) => (
                        <span
                          key={specialty}
                          className="px-3 py-1 bg-blue-600/30 border border-blue-500/30 rounded-lg text-sm"
                        >
                          {specialty}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {selectedTab === 'queue' && (
            <div className="space-y-4">
              {buildQueue.map((task) => {
                const assignedMember = councilMembers.find(m => m.id === task.assignedTo);
                return (
                  <div
                    key={task.id}
                    className="bg-gray-800/50 backdrop-blur-lg border border-gray-700 rounded-xl p-6"
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <span className={`px-3 py-1 rounded text-xs font-bold ${getTaskStatusColor(task.status)}`}>
                            {task.status.toUpperCase()}
                          </span>
                          <span className="px-3 py-1 bg-purple-600/30 border border-purple-500/30 rounded text-xs font-bold">
                            {task.type.toUpperCase()}
                          </span>
                        </div>
                        <h3 className="text-xl font-bold mb-2">{task.description}</h3>
                        {task.platform && (
                          <p className="text-sm text-gray-400">Platform: {task.platform}</p>
                        )}
                      </div>
                      <div className="flex items-center space-x-2">
                        {assignedMember && (
                          <>
                            <span className="text-3xl">{assignedMember.avatar}</span>
                            <span className="text-sm text-gray-400">{assignedMember.name}</span>
                          </>
                        )}
                      </div>
                    </div>

                    {task.status !== 'complete' && task.status !== 'error' && (
                      <>
                        <div className="mb-2">
                          <div className="flex justify-between text-sm mb-1">
                            <span className="text-gray-400">Progress</span>
                            <span className="font-bold text-blue-400">{task.progress}%</span>
                          </div>
                          <div className="w-full bg-gray-700 rounded-full h-3">
                            <div
                              className="bg-gradient-to-r from-blue-600 to-cyan-600 h-3 rounded-full transition-all"
                              style={{ width: `${task.progress}%` }}
                            />
                          </div>
                        </div>
                        {task.estimatedCompletion && (
                          <div className="text-xs text-gray-500">
                            Est. completion: {task.estimatedCompletion.toLocaleTimeString()}
                          </div>
                        )}
                      </>
                    )}

                    {task.status === 'complete' && (
                      <div className="flex items-center space-x-2 text-green-400">
                        <span className="text-2xl">✓</span>
                        <span className="font-bold">COMPLETE</span>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}

          {selectedTab === 'customers' && (
            <div className="space-y-4">
              {customerSystems.map((system) => (
                <div
                  key={system.id}
                  className="bg-gray-800/50 backdrop-blur-lg border border-gray-700 rounded-xl p-6"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-xl font-bold mb-1">{system.customerName}</h3>
                      <p className="text-gray-400">{system.systemType}</p>
                    </div>
                    <div className="flex items-center space-x-2">
                      {system.accessGranted ? (
                        <span className="px-3 py-1 bg-green-600 rounded text-sm font-bold">ACCESS GRANTED</span>
                      ) : (
                        <span className="px-3 py-1 bg-red-600 rounded text-sm font-bold">NO ACCESS</span>
                      )}
                    </div>
                  </div>

                  <div className="grid grid-cols-4 gap-4 mb-4">
                    <div className="bg-gray-900/50 rounded-lg p-3 text-center">
                      <div className={`text-2xl font-bold ${
                        system.healthScore >= 95 ? 'text-green-400' :
                        system.healthScore >= 80 ? 'text-yellow-400' :
                        'text-red-400'
                      }`}>
                        {system.healthScore}%
                      </div>
                      <div className="text-xs text-gray-400">Health Score</div>
                    </div>
                    <div className="bg-gray-900/50 rounded-lg p-3 text-center">
                      <div className={`text-2xl font-bold ${system.issuesFound === 0 ? 'text-green-400' : 'text-yellow-400'}`}>
                        {system.issuesFound}
                      </div>
                      <div className="text-xs text-gray-400">Issues Found</div>
                    </div>
                    <div className="bg-gray-900/50 rounded-lg p-3 text-center">
                      <div className="text-sm font-bold text-gray-300">
                        {system.lastMaintenance.toLocaleDateString()}
                      </div>
                      <div className="text-xs text-gray-400">Last Maintenance</div>
                    </div>
                    <div className="bg-gray-900/50 rounded-lg p-3 text-center">
                      <div className={`text-sm font-bold ${system.autoRepair ? 'text-green-400' : 'text-gray-400'}`}>
                        {system.autoRepair ? 'ENABLED' : 'DISABLED'}
                      </div>
                      <div className="text-xs text-gray-400">Auto-Repair</div>
                    </div>
                  </div>

                  <div className="flex space-x-2">
                    <button className="flex-1 py-2 bg-blue-600 rounded-lg hover:bg-blue-700 font-semibold">
                      🔍 Diagnose
                    </button>
                    <button className="flex-1 py-2 bg-green-600 rounded-lg hover:bg-green-700 font-semibold">
                      🔧 Repair Now
                    </button>
                    <button className="flex-1 py-2 bg-purple-600 rounded-lg hover:bg-purple-700 font-semibold">
                      📊 View Logs
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {selectedTab === 'capabilities' && (
            <div className="grid grid-cols-2 gap-6">
              {[
                {
                  title: '🌐 Website Builder',
                  description: 'Build any website from scratch',
                  features: ['E-commerce sites', 'Landing pages', 'Portfolios', 'Blogs', 'SaaS platforms'],
                  color: 'from-blue-600 to-cyan-600',
                },
                {
                  title: '📱 App Development',
                  description: 'Create mobile & desktop apps',
                  features: ['iOS apps', 'Android apps', 'React Native', 'Progressive Web Apps', 'Desktop apps'],
                  color: 'from-green-600 to-teal-600',
                },
                {
                  title: '🛒 Store Creation',
                  description: 'Deploy fully functional stores',
                  features: ['Shopify stores', 'WooCommerce', 'Custom e-commerce', 'Payment integration', 'Inventory systems'],
                  color: 'from-purple-600 to-pink-600',
                },
                {
                  title: '📱 Social Media',
                  description: 'Rebuild & automate social channels',
                  features: ['Instagram automation', 'Threads automation', 'Twitter bots', 'Facebook pages', 'TikTok content', 'YouTube channels'],
                  color: 'from-yellow-600 to-orange-600',
                },
                {
                  title: '🔧 System Repair',
                  description: 'Fix & optimize any system',
                  features: ['Database optimization', 'API debugging', 'Performance tuning', 'Security patches', 'Code refactoring'],
                  color: 'from-red-600 to-pink-600',
                },
                {
                  title: '🤖 AI Integration',
                  description: 'Add AI to any system',
                  features: ['Chatbots', 'Content generation', 'Image processing', 'Recommendations', 'Predictions'],
                  color: 'from-indigo-600 to-purple-600',
                },
                {
                  title: '☁️ Cloud Deployment',
                  description: 'Deploy to any cloud platform',
                  features: ['Azure deployment', 'AWS setup', 'Google Cloud', 'Auto-scaling', 'CDN configuration'],
                  color: 'from-cyan-600 to-blue-600',
                },
                {
                  title: '💳 Payment Systems',
                  description: 'Integrate payment gateways',
                  features: ['Stripe integration', 'PayPal setup', 'Crypto payments', 'Subscription billing', 'Invoice generation'],
                  color: 'from-green-600 to-emerald-600',
                },
              ].map((capability) => (
                <div
                  key={capability.title}
                  className="bg-gray-800/50 backdrop-blur-lg border border-gray-700 rounded-xl p-6"
                >
                  <div className={`inline-block px-4 py-2 bg-gradient-to-r ${capability.color} rounded-lg mb-4`}>
                    <h3 className="text-xl font-bold">{capability.title}</h3>
                  </div>
                  <p className="text-gray-400 mb-4">{capability.description}</p>
                  <ul className="space-y-2">
                    {capability.features.map((feature) => (
                      <li key={feature} className="flex items-center space-x-2">
                        <span className="text-green-400">✓</span>
                        <span className="text-sm">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
}
