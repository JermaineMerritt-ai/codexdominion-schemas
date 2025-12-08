import React, { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import CodexNavigation from '../components/CodexNavigation';

interface WorkflowNode {
  id: string;
  type: string;
  name: string;
  icon: string;
}

interface Workflow {
  id: string;
  name: string;
  nodes: number;
  status: 'active' | 'paused' | 'draft';
  executions: number;
}

const AutomationStudio = () => {
  const [activeTab, setActiveTab] = useState('workflows');
  const [workflows, setWorkflows] = useState<Workflow[]>([
    { id: '1', name: 'Social Media Cross-Post', nodes: 8, status: 'active', executions: 1523 },
    { id: '2', name: 'Email to Task Automation', nodes: 5, status: 'active', executions: 892 },
    { id: '3', name: 'Revenue Alert System', nodes: 12, status: 'active', executions: 2341 },
    { id: '4', name: 'Content Distribution Pipeline', nodes: 15, status: 'paused', executions: 456 },
  ]);

  const integrationCategories = [
    {
      name: 'Social Media',
      count: 50,
      icon: '📱',
      platforms: ['YouTube', 'TikTok', 'Instagram', 'LinkedIn', 'Twitter', 'Facebook', 'Discord', 'Telegram', 'WhatsApp', 'Snapchat', 'Pinterest', 'Reddit', 'Twitch', 'Threads', 'BlueSky']
    },
    {
      name: 'Cloud Services',
      count: 200,
      icon: '☁️',
      platforms: ['AWS', 'Azure', 'Google Cloud', 'Cloudflare', 'Heroku', 'DigitalOcean', 'Vercel', 'Netlify']
    },
    {
      name: 'Communication',
      count: 40,
      icon: '💬',
      platforms: ['Gmail', 'Outlook', 'Slack', 'Teams', 'Zoom', 'Discord', 'Telegram', 'WhatsApp Business']
    },
    {
      name: 'E-commerce',
      count: 35,
      icon: '🛍️',
      platforms: ['Shopify', 'WooCommerce', 'Stripe', 'PayPal', 'Square', 'Amazon', 'Etsy', 'eBay']
    },
    {
      name: 'Productivity',
      count: 60,
      icon: '⚡',
      platforms: ['Notion', 'Airtable', 'Google Sheets', 'Excel', 'Trello', 'Asana', 'Monday.com', 'ClickUp']
    },
    {
      name: 'Marketing',
      count: 45,
      icon: '📊',
      platforms: ['Google Analytics', 'HubSpot', 'Mailchimp', 'ConvertKit', 'ActiveCampaign', 'Buffer', 'Hootsuite']
    },
    {
      name: 'AI Services',
      count: 30,
      icon: '🤖',
      platforms: ['OpenAI', 'Anthropic', 'Google AI', 'Hugging Face', 'Stability AI', 'Runway', 'ElevenLabs']
    },
    {
      name: 'Development',
      count: 40,
      icon: '💻',
      platforms: ['GitHub', 'GitLab', 'Bitbucket', 'Docker', 'Kubernetes', 'Jenkins', 'CircleCI', 'Vercel']
    },
  ];

  const triggerNodes: WorkflowNode[] = [
    { id: 't1', type: 'trigger', name: 'Webhook', icon: '🔗' },
    { id: 't2', type: 'trigger', name: 'Schedule', icon: '⏰' },
    { id: 't3', type: 'trigger', name: 'Email Received', icon: '📧' },
    { id: 't4', type: 'trigger', name: 'File Upload', icon: '📁' },
    { id: 't5', type: 'trigger', name: 'Database Change', icon: '💾' },
    { id: 't6', type: 'trigger', name: 'API Call', icon: '🌐' },
    { id: 't7', type: 'trigger', name: 'Form Submit', icon: '📝' },
    { id: 't8', type: 'trigger', name: 'Payment Received', icon: '💰' },
  ];

  const actionNodes: WorkflowNode[] = [
    { id: 'a1', type: 'action', name: 'Send Email', icon: '✉️' },
    { id: 'a2', type: 'action', name: 'Create Task', icon: '✅' },
    { id: 'a3', type: 'action', name: 'Post to Social', icon: '📱' },
    { id: 'a4', type: 'action', name: 'Update Database', icon: '💾' },
    { id: 'a5', type: 'action', name: 'Generate AI Content', icon: '🤖' },
    { id: 'a6', type: 'action', name: 'Send SMS', icon: '💬' },
    { id: 'a7', type: 'action', name: 'Create Document', icon: '📄' },
    { id: 'a8', type: 'action', name: 'Call API', icon: '🌐' },
  ];

  const logicNodes: WorkflowNode[] = [
    { id: 'l1', type: 'logic', name: 'If/Else', icon: '🔀' },
    { id: 'l2', type: 'logic', name: 'Loop', icon: '🔄' },
    { id: 'l3', type: 'logic', name: 'Filter', icon: '🔍' },
    { id: 'l4', type: 'logic', name: 'Merge Data', icon: '🔗' },
    { id: 'l5', type: 'logic', name: 'Split', icon: '✂️' },
    { id: 'l6', type: 'logic', name: 'Wait', icon: '⏸️' },
    { id: 'l7', type: 'logic', name: 'Transform', icon: '⚙️' },
    { id: 'l8', type: 'logic', name: 'AI Decision', icon: '🧠' },
  ];

  const workflowTemplates = [
    { id: 1, name: 'Social Media Scheduler', nodes: 6, icon: '📱', category: 'Marketing' },
    { id: 2, name: 'Lead Generation Pipeline', nodes: 10, icon: '🎯', category: 'Sales' },
    { id: 3, name: 'Customer Onboarding', nodes: 8, icon: '👋', category: 'CRM' },
    { id: 4, name: 'Invoice Processing', nodes: 7, icon: '💰', category: 'Finance' },
    { id: 5, name: 'Content Distribution', nodes: 12, icon: '📤', category: 'Marketing' },
    { id: 6, name: 'Support Ticket Routing', nodes: 9, icon: '🎫', category: 'Support' },
    { id: 7, name: 'Data Sync & Backup', nodes: 5, icon: '🔄', category: 'Operations' },
    { id: 8, name: 'AI Content Generator', nodes: 11, icon: '🤖', category: 'Content' },
  ];

  return (
    <>
      <Head>
        <title>Codex Automation Studio - N8N Destroyer</title>
        <meta name="description" content="500+ integrations, quantum automation workflows" />
      </Head>

      <CodexNavigation />

      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white p-8">
        <div className="max-w-[1800px] mx-auto">

          {/* Header */}
          <div className="text-center mb-10">
            <h1 className="text-5xl font-bold mb-3 bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
              ⚡ Codex Automation Studio
            </h1>
            <p className="text-xl text-gray-300">
              Quantum Workflow Engine • 500+ Integrations • Consciousness-Level Intelligence
            </p>
            <div className="flex justify-center gap-4 mt-4 flex-wrap">
              <span className="px-4 py-2 bg-red-600/30 rounded-full text-sm">🔥 N8N Destroyer</span>
              <span className="px-4 py-2 bg-orange-600/30 rounded-full text-sm">⚡ Zapier Killer</span>
              <span className="px-4 py-2 bg-blue-600/30 rounded-full text-sm">🚀 Make Obliterator</span>
              <span className="px-4 py-2 bg-purple-600/30 rounded-full text-sm">♾️ 500% Faster</span>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-white/10 p-6 rounded-xl text-center">
              <div className="text-4xl font-bold text-cyan-400">500+</div>
              <div className="text-sm text-gray-400 mt-1">Integrations</div>
            </div>
            <div className="bg-white/10 p-6 rounded-xl text-center">
              <div className="text-4xl font-bold text-green-400">5,212</div>
              <div className="text-sm text-gray-400 mt-1">Active Workflows</div>
            </div>
            <div className="bg-white/10 p-6 rounded-xl text-center">
              <div className="text-4xl font-bold text-purple-400">98.7%</div>
              <div className="text-sm text-gray-400 mt-1">Success Rate</div>
            </div>
            <div className="bg-white/10 p-6 rounded-xl text-center">
              <div className="text-4xl font-bold text-yellow-400">500%</div>
              <div className="text-sm text-gray-400 mt-1">Faster than N8N</div>
            </div>
          </div>

          {/* Tab Navigation */}
          <div className="flex justify-center gap-4 mb-8 flex-wrap">
            {['workflows', 'integrations', 'builder', 'templates'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-6 py-3 rounded-xl font-semibold transition-all ${
                  activeTab === tab
                    ? 'bg-gradient-to-r from-cyan-600 to-blue-600 shadow-2xl scale-110'
                    : 'bg-white/10 hover:bg-white/20'
                }`}
              >
                {tab === 'workflows' && '🔄 My Workflows'}
                {tab === 'integrations' && '🔌 Integrations'}
                {tab === 'builder' && '🛠️ Workflow Builder'}
                {tab === 'templates' && '📋 Templates'}
              </button>
            ))}
          </div>

          {/* Content */}
          <div className="bg-white/5 backdrop-blur-xl rounded-3xl p-8 border border-white/10">

            {/* Workflows Tab */}
            {activeTab === 'workflows' && (
              <div>
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-3xl font-bold">🔄 My Workflows</h2>
                  <button className="bg-gradient-to-r from-cyan-600 to-blue-600 px-6 py-3 rounded-xl font-semibold hover:scale-105 transition-transform">
                    + New Workflow
                  </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {workflows.map((workflow) => (
                    <div key={workflow.id} className="bg-white/10 p-6 rounded-xl hover:bg-white/15 transition-all">
                      <div className="flex justify-between items-start mb-4">
                        <div>
                          <h3 className="text-xl font-bold mb-2">{workflow.name}</h3>
                          <p className="text-sm text-gray-400">{workflow.nodes} nodes</p>
                        </div>
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          workflow.status === 'active' ? 'bg-green-600' :
                          workflow.status === 'paused' ? 'bg-yellow-600' : 'bg-gray-600'
                        }`}>
                          {workflow.status.toUpperCase()}
                        </span>
                      </div>
                      <div className="text-2xl font-bold text-cyan-400 mb-4">
                        {workflow.executions.toLocaleString()} executions
                      </div>
                      <div className="flex gap-2">
                        <button className="flex-1 bg-blue-600 hover:bg-blue-700 py-2 rounded-lg text-sm font-semibold">
                          Edit
                        </button>
                        <button className="flex-1 bg-purple-600 hover:bg-purple-700 py-2 rounded-lg text-sm font-semibold">
                          View Logs
                        </button>
                        <button className="px-4 bg-gray-600 hover:bg-gray-700 py-2 rounded-lg text-sm font-semibold">
                          ⋮
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Integrations Tab */}
            {activeTab === 'integrations' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">🔌 500+ Available Integrations</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {integrationCategories.map((category, idx) => (
                    <div key={idx} className="bg-white/10 p-6 rounded-xl hover:border-cyan-400 border-2 border-transparent transition-all">
                      <div className="text-5xl mb-4">{category.icon}</div>
                      <h3 className="text-xl font-bold mb-2">{category.name}</h3>
                      <p className="text-3xl font-bold text-cyan-400 mb-4">{category.count}</p>
                      <div className="space-y-1 mb-4">
                        {category.platforms.slice(0, 5).map((platform, pidx) => (
                          <p key={pidx} className="text-xs text-gray-400">• {platform}</p>
                        ))}
                        {category.platforms.length > 5 && (
                          <p className="text-xs text-gray-400 font-semibold">+ {category.platforms.length - 5} more</p>
                        )}
                      </div>
                      <button className="w-full bg-cyan-600 hover:bg-cyan-700 py-2 rounded-lg font-semibold">
                        Browse
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Builder Tab */}
            {activeTab === 'builder' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">🛠️ Visual Workflow Builder</h2>

                <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                  <div className="lg:col-span-1 space-y-4">
                    <div className="bg-white/10 p-4 rounded-xl">
                      <h3 className="font-bold mb-3">🎯 Triggers</h3>
                      <div className="space-y-2">
                        {triggerNodes.map((node) => (
                          <div key={node.id} className="bg-green-600/20 p-3 rounded-lg cursor-pointer hover:bg-green-600/30 transition-all">
                            <span className="mr-2">{node.icon}</span>
                            <span className="text-sm">{node.name}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="bg-white/10 p-4 rounded-xl">
                      <h3 className="font-bold mb-3">⚡ Actions</h3>
                      <div className="space-y-2">
                        {actionNodes.slice(0, 4).map((node) => (
                          <div key={node.id} className="bg-blue-600/20 p-3 rounded-lg cursor-pointer hover:bg-blue-600/30 transition-all">
                            <span className="mr-2">{node.icon}</span>
                            <span className="text-sm">{node.name}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="bg-white/10 p-4 rounded-xl">
                      <h3 className="font-bold mb-3">🧠 Logic</h3>
                      <div className="space-y-2">
                        {logicNodes.slice(0, 4).map((node) => (
                          <div key={node.id} className="bg-purple-600/20 p-3 rounded-lg cursor-pointer hover:bg-purple-600/30 transition-all">
                            <span className="mr-2">{node.icon}</span>
                            <span className="text-sm">{node.name}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div className="lg:col-span-3 bg-white/10 rounded-xl p-8 min-h-[600px] relative">
                    <div className="text-center text-gray-400 mt-40">
                      <div className="text-6xl mb-4">🎨</div>
                      <p className="text-xl mb-2">Visual Workflow Canvas</p>
                      <p className="text-sm mb-6">Drag nodes from the left to build your automation</p>
                      <button className="bg-gradient-to-r from-cyan-600 to-blue-600 px-8 py-3 rounded-xl font-semibold hover:scale-105 transition-transform">
                        Start Building
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Templates Tab */}
            {activeTab === 'templates' && (
              <div>
                <h2 className="text-3xl font-bold mb-6">📋 Workflow Templates</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {workflowTemplates.map((template) => (
                    <div key={template.id} className="bg-white/10 p-5 rounded-xl hover:bg-white/15 transition-all cursor-pointer">
                      <div className="text-4xl mb-3 text-center">{template.icon}</div>
                      <h3 className="font-bold mb-2 text-center">{template.name}</h3>
                      <p className="text-xs text-gray-400 text-center mb-1">{template.nodes} nodes</p>
                      <p className="text-xs text-gray-400 text-center mb-3">{template.category}</p>
                      <button className="w-full bg-cyan-600 hover:bg-cyan-700 py-2 rounded-lg text-sm font-semibold">
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

export default AutomationStudio;
