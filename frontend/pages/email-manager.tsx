import React, { useState } from 'react';
import Head from 'next/head';

interface Email {
  id: string;
  from: string;
  subject: string;
  preview: string;
  timestamp: Date;
  read: boolean;
  starred: boolean;
  category: 'primary' | 'social' | 'promotions' | 'spam';
  priority: 'high' | 'medium' | 'low';
  labels: string[];
}

interface Folder {
  id: string;
  name: string;
  icon: string;
  count: number;
  color: string;
}

export default function EmailManager() {
  const [selectedFolder, setSelectedFolder] = useState('inbox');
  const [selectedEmail, setSelectedEmail] = useState<string | null>(null);
  const [composeOpen, setComposeOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const folders: Folder[] = [
    { id: 'inbox', name: 'Inbox', icon: '📥', count: 24, color: 'blue' },
    { id: 'starred', name: 'Starred', icon: '⭐', count: 8, color: 'yellow' },
    { id: 'sent', name: 'Sent', icon: '📤', count: 142, color: 'green' },
    { id: 'drafts', name: 'Drafts', icon: '📝', count: 5, color: 'orange' },
    { id: 'archive', name: 'Archive', icon: '📦', count: 358, color: 'gray' },
    { id: 'spam', name: 'Spam', icon: '🚫', count: 12, color: 'red' },
    { id: 'trash', name: 'Trash', icon: '🗑️', count: 7, color: 'red' },
  ];

  const emails: Email[] = [
    {
      id: '1',
      from: 'team@azure.com',
      subject: 'Azure Credits Available - $200 Free',
      preview: 'Your Azure subscription now includes $200 in free credits for the next 30 days...',
      timestamp: new Date('2025-12-10T09:30:00'),
      read: false,
      starred: true,
      category: 'primary',
      priority: 'high',
      labels: ['Azure', 'Cloud'],
    },
    {
      id: '2',
      from: 'github@notifications.com',
      subject: 'New PR: Performance Optimization',
      preview: 'JermaineMerritt-ai opened a pull request in codex-dominion...',
      timestamp: new Date('2025-12-10T08:15:00'),
      read: false,
      starred: false,
      category: 'primary',
      priority: 'high',
      labels: ['GitHub', 'Development'],
    },
    {
      id: '3',
      from: 'anthropic@updates.com',
      subject: 'Claude 4.0 - Now Available',
      preview: 'We are excited to announce Claude 4.0 with enhanced reasoning capabilities...',
      timestamp: new Date('2025-12-09T16:45:00'),
      read: true,
      starred: true,
      category: 'primary',
      priority: 'medium',
      labels: ['AI', 'Updates'],
    },
    {
      id: '4',
      from: 'stripe@billing.com',
      subject: 'Payment Received - $49.00',
      preview: 'Your payment of $49.00 has been successfully processed for Codex Dominion subscription...',
      timestamp: new Date('2025-12-09T14:20:00'),
      read: true,
      starred: false,
      category: 'primary',
      priority: 'medium',
      labels: ['Billing'],
    },
    {
      id: '5',
      from: 'linkedin@notifications.com',
      subject: 'Your post got 142 likes',
      preview: 'Your recent post about AI development is getting great engagement...',
      timestamp: new Date('2025-12-09T11:30:00'),
      read: true,
      starred: false,
      category: 'social',
      priority: 'low',
      labels: ['Social'],
    },
  ];

  const templates = [
    { id: '1', name: 'Meeting Request', icon: '📅', category: 'Professional' },
    { id: '2', name: 'Follow-up', icon: '🔄', category: 'Professional' },
    { id: '3', name: 'Thank You', icon: '🙏', category: 'Professional' },
    { id: '4', name: 'Introduction', icon: '👋', category: 'Networking' },
    { id: '5', name: 'Sales Pitch', icon: '💼', category: 'Business' },
    { id: '6', name: 'Support Response', icon: '💬', category: 'Support' },
  ];

  const automationRules = [
    { id: '1', name: 'Auto-label Azure emails', active: true, triggers: 3 },
    { id: '2', name: 'Forward urgent to phone', active: true, triggers: 1 },
    { id: '3', name: 'Archive social after 7 days', active: true, triggers: 24 },
    { id: '4', name: 'Auto-reply when away', active: false, triggers: 0 },
  ];

  const selectedEmailData = emails.find(e => e.id === selectedEmail);

  return (
    <>
      <Head>
        <title>Email Manager | CodexDominion</title>
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 text-white">
        <div className="flex h-screen">
          {/* Sidebar */}
          <div className="w-64 bg-gray-800/50 backdrop-blur-lg border-r border-gray-700 p-4 overflow-y-auto">
            <div className="mb-6">
              <button
                onClick={() => setComposeOpen(true)}
                className="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-lg font-semibold hover:opacity-90 flex items-center justify-center space-x-2"
              >
                <span>✉️</span>
                <span>Compose</span>
              </button>
            </div>

            <div className="space-y-2 mb-6">
              {folders.map((folder) => (
                <div
                  key={folder.id}
                  onClick={() => setSelectedFolder(folder.id)}
                  className={`p-3 rounded-lg cursor-pointer flex items-center justify-between ${
                    selectedFolder === folder.id
                      ? 'bg-blue-600'
                      : 'hover:bg-gray-700/50'
                  }`}
                >
                  <div className="flex items-center space-x-2">
                    <span className="text-xl">{folder.icon}</span>
                    <span className="font-medium">{folder.name}</span>
                  </div>
                  {folder.count > 0 && (
                    <span className="text-xs bg-white/20 px-2 py-1 rounded">
                      {folder.count}
                    </span>
                  )}
                </div>
              ))}
            </div>

            <div className="border-t border-gray-700 pt-4">
              <h3 className="text-sm font-bold mb-3 text-gray-400">LABELS</h3>
              <div className="space-y-2">
                {['Azure', 'Development', 'AI', 'Billing', 'Social'].map((label) => (
                  <div
                    key={label}
                    className="px-3 py-2 rounded-lg hover:bg-gray-700/50 cursor-pointer text-sm flex items-center space-x-2"
                  >
                    <div className="w-3 h-3 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full" />
                    <span>{label}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="border-t border-gray-700 mt-4 pt-4">
              <h3 className="text-sm font-bold mb-3 text-gray-400">AUTOMATION</h3>
              <div className="space-y-2">
                {automationRules.slice(0, 2).map((rule) => (
                  <div
                    key={rule.id}
                    className="px-3 py-2 bg-gray-900/50 rounded-lg text-xs"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-semibold">{rule.name}</span>
                      <div className={`w-2 h-2 rounded-full ${rule.active ? 'bg-green-500' : 'bg-gray-500'}`} />
                    </div>
                    <span className="text-gray-400">{rule.triggers} triggers</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Email List */}
          <div className="w-96 bg-gray-800/30 backdrop-blur-lg border-r border-gray-700 overflow-y-auto">
            <div className="p-4 border-b border-gray-700">
              <div className="relative">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search emails..."
                  className="w-full px-4 py-2 pl-10 bg-gray-900/50 border border-gray-700 rounded-lg focus:border-blue-500 focus:outline-none"
                />
                <span className="absolute left-3 top-2.5">🔍</span>
              </div>
              <div className="flex space-x-2 mt-3">
                <button className="px-3 py-1 bg-gray-700 rounded text-xs hover:bg-gray-600">
                  All
                </button>
                <button className="px-3 py-1 bg-gray-700 rounded text-xs hover:bg-gray-600">
                  Unread
                </button>
                <button className="px-3 py-1 bg-gray-700 rounded text-xs hover:bg-gray-600">
                  Starred
                </button>
              </div>
            </div>

            <div className="divide-y divide-gray-700">
              {emails.map((email) => (
                <div
                  key={email.id}
                  onClick={() => setSelectedEmail(email.id)}
                  className={`p-4 cursor-pointer hover:bg-gray-700/30 ${
                    selectedEmail === email.id ? 'bg-gray-700/50' : ''
                  } ${!email.read ? 'border-l-4 border-blue-500' : ''}`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-1">
                        <span className="font-semibold text-sm">{email.from}</span>
                        {email.priority === 'high' && (
                          <span className="text-xs bg-red-600 px-2 py-0.5 rounded">HIGH</span>
                        )}
                      </div>
                      <div className="font-bold mb-1">{email.subject}</div>
                      <p className="text-sm text-gray-400 line-clamp-2">{email.preview}</p>
                    </div>
                    <div className="ml-2">
                      {email.starred && <span className="text-yellow-400">⭐</span>}
                    </div>
                  </div>
                  <div className="flex items-center justify-between text-xs text-gray-500">
                    <span>{email.timestamp.toLocaleTimeString()}</span>
                    <div className="flex space-x-1">
                      {email.labels.slice(0, 2).map((label) => (
                        <span
                          key={label}
                          className="px-2 py-0.5 bg-purple-600/30 rounded"
                        >
                          {label}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Email Content / Compose */}
          <div className="flex-1 flex flex-col">
            {composeOpen ? (
              /* Compose View */
              <div className="flex-1 flex flex-col">
                <div className="bg-gray-800/50 backdrop-blur-lg border-b border-gray-700 p-4 flex items-center justify-between">
                  <h2 className="text-xl font-bold">✉️ New Message</h2>
                  <button
                    onClick={() => setComposeOpen(false)}
                    className="px-4 py-2 bg-gray-700 rounded-lg hover:bg-gray-600"
                  >
                    ✕ Close
                  </button>
                </div>

                <div className="flex-1 p-6 overflow-y-auto">
                  <div className="max-w-4xl mx-auto space-y-4">
                    <div>
                      <label className="block text-sm font-semibold mb-2">To</label>
                      <input
                        type="email"
                        placeholder="recipient@example.com"
                        className="w-full px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg focus:border-blue-500 focus:outline-none"
                      />
                    </div>

                    <div className="flex space-x-4">
                      <div className="flex-1">
                        <label className="block text-sm font-semibold mb-2">CC</label>
                        <input
                          type="email"
                          placeholder="Optional"
                          className="w-full px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg focus:border-blue-500 focus:outline-none"
                        />
                      </div>
                      <div className="flex-1">
                        <label className="block text-sm font-semibold mb-2">BCC</label>
                        <input
                          type="email"
                          placeholder="Optional"
                          className="w-full px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg focus:border-blue-500 focus:outline-none"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-semibold mb-2">Subject</label>
                      <input
                        type="text"
                        placeholder="Email subject"
                        className="w-full px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg focus:border-blue-500 focus:outline-none"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-semibold mb-2">AI Templates</label>
                      <div className="flex space-x-2 overflow-x-auto pb-2">
                        {templates.map((template) => (
                          <button
                            key={template.id}
                            className="px-4 py-2 bg-gradient-to-r from-purple-600/30 to-pink-600/30 border border-purple-500/30 rounded-lg text-sm whitespace-nowrap hover:from-purple-600/50 hover:to-pink-600/50"
                          >
                            {template.icon} {template.name}
                          </button>
                        ))}
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-semibold mb-2">Message</label>
                      <textarea
                        placeholder="Write your message here... (AI will help with grammar and tone)"
                        className="w-full h-64 px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg focus:border-blue-500 focus:outline-none resize-none"
                      />
                    </div>

                    <div className="flex items-center space-x-2">
                      <button className="px-4 py-2 bg-gray-700 rounded-lg hover:bg-gray-600">
                        📎 Attach Files
                      </button>
                      <button className="px-4 py-2 bg-gray-700 rounded-lg hover:bg-gray-600">
                        🎨 Format
                      </button>
                      <button className="px-4 py-2 bg-gray-700 rounded-lg hover:bg-gray-600">
                        😊 Emoji
                      </button>
                      <button className="px-4 py-2 bg-purple-600 rounded-lg hover:bg-purple-700">
                        ✨ AI Enhance
                      </button>
                    </div>

                    <div className="flex justify-end space-x-2 pt-4">
                      <button className="px-6 py-2 bg-gray-700 rounded-lg hover:bg-gray-600">
                        💾 Save Draft
                      </button>
                      <button className="px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-lg font-semibold hover:opacity-90">
                        ➤ Send Email
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ) : selectedEmailData ? (
              /* Email View */
              <div className="flex-1 flex flex-col">
                <div className="bg-gray-800/50 backdrop-blur-lg border-b border-gray-700 p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => setSelectedEmail(null)}
                        className="px-3 py-2 bg-gray-700 rounded-lg hover:bg-gray-600"
                      >
                        ← Back
                      </button>
                      <button className="px-3 py-2 bg-gray-700 rounded-lg hover:bg-gray-600">
                        🗑️
                      </button>
                      <button className="px-3 py-2 bg-gray-700 rounded-lg hover:bg-gray-600">
                        📦
                      </button>
                      <button className="px-3 py-2 bg-gray-700 rounded-lg hover:bg-gray-600">
                        ⚠️ Spam
                      </button>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-yellow-400 text-xl cursor-pointer">
                        {selectedEmailData.starred ? '⭐' : '☆'}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex-1 overflow-y-auto p-6">
                  <div className="max-w-4xl mx-auto">
                    <h1 className="text-3xl font-bold mb-4">{selectedEmailData.subject}</h1>

                    <div className="bg-gray-800/50 backdrop-blur-lg border border-gray-700 rounded-xl p-6 mb-6">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-3">
                          <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-full flex items-center justify-center font-bold text-lg">
                            {selectedEmailData.from.charAt(0).toUpperCase()}
                          </div>
                          <div>
                            <div className="font-bold">{selectedEmailData.from}</div>
                            <div className="text-sm text-gray-400">to me</div>
                          </div>
                        </div>
                        <div className="text-sm text-gray-400">
                          {selectedEmailData.timestamp.toLocaleString()}
                        </div>
                      </div>

                      <div className="prose prose-invert max-w-none">
                        <p className="text-gray-300 leading-relaxed">
                          {selectedEmailData.preview}
                        </p>
                        <p className="text-gray-300 leading-relaxed mt-4">
                          This is a sample email content. In production, this would display the full email body with proper formatting, images, and attachments.
                        </p>
                        <p className="text-gray-300 leading-relaxed mt-4">
                          The AI system can analyze this email for sentiment, priority, suggested responses, and automatic categorization.
                        </p>
                      </div>
                    </div>

                    <div className="flex space-x-2">
                      <button className="flex-1 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-lg font-semibold hover:opacity-90">
                        ↩️ Reply
                      </button>
                      <button className="flex-1 py-3 bg-gray-700 rounded-lg font-semibold hover:bg-gray-600">
                        ↪️ Forward
                      </button>
                      <button className="px-6 py-3 bg-purple-600 rounded-lg font-semibold hover:bg-purple-700">
                        ✨ AI Reply
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              /* No Selection */
              <div className="flex-1 flex items-center justify-center">
                <div className="text-center">
                  <div className="text-6xl mb-4">📧</div>
                  <h2 className="text-2xl font-bold mb-2">Select an email</h2>
                  <p className="text-gray-400">Choose an email from the list to view its contents</p>
                </div>
              </div>
            )}
          </div>

          {/* Right Sidebar - AI Assistant */}
          <div className="w-80 bg-gray-800/50 backdrop-blur-lg border-l border-gray-700 p-4 overflow-y-auto">
            <h3 className="text-xl font-bold mb-4">🤖 AI Assistant</h3>

            <div className="space-y-4">
              <div className="bg-gradient-to-br from-purple-600/20 to-pink-600/20 border border-purple-500/30 rounded-xl p-4">
                <h4 className="font-bold mb-2">📊 Analytics</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Today</span>
                    <span className="font-semibold">12 emails</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Unread</span>
                    <span className="text-blue-400 font-semibold">24</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Avg Response</span>
                    <span className="text-green-400 font-semibold">2.4h</span>
                  </div>
                </div>
              </div>

              <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-4">
                <h4 className="font-bold mb-3">⚡ Quick Actions</h4>
                <div className="space-y-2">
                  <button className="w-full py-2 px-3 bg-blue-600 rounded-lg text-sm hover:bg-blue-700">
                    Mark all as read
                  </button>
                  <button className="w-full py-2 px-3 bg-purple-600 rounded-lg text-sm hover:bg-purple-700">
                    AI Categorize
                  </button>
                  <button className="w-full py-2 px-3 bg-green-600 rounded-lg text-sm hover:bg-green-700">
                    Bulk Forward
                  </button>
                </div>
              </div>

              <div className="bg-gray-900/50 border border-gray-700 rounded-xl p-4">
                <h4 className="font-bold mb-3">🔧 Automation Rules</h4>
                <div className="space-y-3">
                  {automationRules.map((rule) => (
                    <div key={rule.id} className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="text-sm font-semibold">{rule.name}</div>
                        <div className="text-xs text-gray-400">{rule.triggers} triggers</div>
                      </div>
                      <div className={`w-10 h-6 rounded-full ${rule.active ? 'bg-green-600' : 'bg-gray-600'} relative cursor-pointer`}>
                        <div className={`w-4 h-4 bg-white rounded-full absolute top-1 transition-all ${rule.active ? 'right-1' : 'left-1'}`} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-gradient-to-br from-blue-600/20 to-cyan-600/20 border border-blue-500/30 rounded-xl p-4">
                <h4 className="font-bold mb-2">💡 AI Suggestions</h4>
                <div className="space-y-2 text-sm">
                  <div className="p-2 bg-white/5 rounded">
                    3 emails need follow-up
                  </div>
                  <div className="p-2 bg-white/5 rounded">
                    Archive old newsletters (24)
                  </div>
                  <div className="p-2 bg-white/5 rounded">
                    Create rule for Azure emails
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
