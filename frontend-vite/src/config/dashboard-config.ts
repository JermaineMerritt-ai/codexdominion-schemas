// CodexDominion - Dashboard Configuration
// Maps studio tiles to routes and metadata
// Integrates with frontend/config/studio-config.json

import type { LucideIcon } from 'lucide-react';

/**
 * Studio tile definition for dashboard
 */
export interface StudioTile {
  id: string;
  name: string;
  description: string;
  icon: string;          // Emoji or icon component name
  route: string;         // Frontend route (e.g., '/studio/audio')
  legacyRoute?: string;  // Optional legacy route for backwards compatibility
  color: string;         // Tailwind gradient class
  status: 'active' | 'beta' | 'coming-soon';
  category: StudioCategory;
  features: string[];
  actions?: TileAction[];
  recentItems?: string[];
}

/**
 * Studio category for grouping
 */
export type StudioCategory =
  | 'creative'      // Audio, Video, Publishing
  | 'productivity'  // Notebook, Automation
  | 'development'   // Builder, Intelligence
  | 'governance';   // Sacred systems (if needed)

/**
 * Quick action on a tile
 */
export interface TileAction {
  label: string;
  route: string;
  icon?: string;
}

/**
 * Intelligence engine category
 */
export interface IntelligenceCategory {
  name: string;
  icon: string;
  engines: string[];
  count: number;
  color: string;
}

/**
 * AI Assistant configuration
 */
export interface AIAssistant {
  name: string;
  provider: string;
  roles: string[];
  description: string;
  icon: string;
}

/**
 * Complete dashboard configuration
 */
export interface DashboardConfig {
  systemName: string;
  version: string;
  studios: StudioTile[];
  intelligenceEngines: {
    total: number;
    categories: IntelligenceCategory[];
  };
  aiAssistants: AIAssistant[];
}

/**
 * Main dashboard configuration
 */
export const dashboardConfig: DashboardConfig = {
  systemName: 'CodexDominion Top-Tier Studio',
  version: '2.0.0',

  studios: [
    {
      id: 'audio',
      name: 'Audio Studio',
      description: 'Professional audio creation, editing, and mastering with AI',
      icon: '🎵',
      route: '/studio/audio',
      legacyRoute: '/ai-audio-studio',
      color: 'from-purple-600 to-pink-600',
      status: 'active',
      category: 'creative',
      features: ['Voice Synthesis', 'Audio Mastering', 'Sound Effects', 'Podcast Pipeline'],
      actions: [
        { label: 'Record', route: '/studio/audio?mode=record', icon: '🎙️' },
        { label: 'Upload', route: '/studio/audio?mode=upload', icon: '⬆️' },
        { label: 'Enhance', route: '/studio/audio?mode=enhance', icon: '✨' },
        { label: 'Voice Gen', route: '/studio/audio?mode=generate', icon: '🗣️' }
      ],
      recentItems: ['Morning Devotional EP12', 'Podcast Intro v3', 'Hymn Recording 2024-12-10']
    },
    {
      id: 'video',
      name: 'Video Studio',
      description: 'Video production, graphics, and animation platform',
      icon: '🎬',
      route: '/studio/video',
      legacyRoute: '/ai-graphic-video-studio',
      color: 'from-blue-600 to-cyan-600',
      status: 'active',
      category: 'creative',
      features: ['Video Editing', 'Motion Graphics', 'Audio-to-Video', 'Templates'],
      actions: [
        { label: 'New from Audio', route: '/studio/video?source=audio', icon: '🎵' },
        { label: 'Templates', route: '/studio/video?view=templates', icon: '📋' },
        { label: 'Recent Renders', route: '/studio/video?view=recent', icon: '📊' }
      ],
      recentItems: ['Sermon Highlight Reel', 'Social Clip - Faith', 'Lyric Video Draft']
    },
    {
      id: 'automation',
      name: 'Automation Studio',
      description: 'Workflow automation and integration platform',
      icon: '⚙️',
      route: '/studio/automation',
      legacyRoute: '/automation-studio',
      color: 'from-green-600 to-emerald-600',
      status: 'active',
      category: 'productivity',
      features: ['Visual Workflows', 'Trigger Catalog', 'Execution History', 'Templates'],
      actions: [
        { label: 'Workflow Builder', route: '/studio/automation?view=builder', icon: '🔨' },
        { label: 'Triggers', route: '/studio/automation?view=triggers', icon: '⚡' },
        { label: 'Library', route: '/studio/automation?view=library', icon: '📚' },
        { label: 'History', route: '/studio/automation?view=history', icon: '📜' }
      ],
      recentItems: ['Podcast Publisher', 'YouTube Uploader', 'Ebook Generator']
    },
    {
      id: 'notebook',
      name: 'Notebook Studio',
      description: 'Interactive research, analysis, and documentation environment',
      icon: '📓',
      route: '/studio/notebook',
      legacyRoute: '/notebook-studio',
      color: 'from-amber-600 to-yellow-600',
      status: 'active',
      category: 'productivity',
      features: ['Rich Text Editor', 'AI Summarize', 'Link Assets', 'Version Control'],
      actions: [
        { label: 'All Notebooks', route: '/studio/notebook?view=all', icon: '📚' },
        { label: 'AI Helpers', route: '/studio/notebook?view=ai', icon: '🤖' },
        { label: 'Link Assets', route: '/studio/notebook?view=links', icon: '🔗' }
      ],
      recentItems: ['Sermon Notes - Faith', 'Podcast Script EP13', 'Study Guide Draft']
    },
    {
      id: 'publishing',
      name: 'Publishing Studio',
      description: 'Content transformation and distribution platform',
      icon: '📚',
      route: '/studio/publishing',
      legacyRoute: '/creative-studio',
      color: 'from-rose-600 to-pink-600',
      status: 'active',
      category: 'creative',
      features: ['eBook Generation', 'Study Guides', 'Landing Pages', 'Templates'],
      actions: [
        { label: 'From Transcript', route: '/studio/publishing?source=transcript', icon: '📝' },
        { label: 'Study Guide', route: '/studio/publishing?type=study-guide', icon: '📖' },
        { label: 'Landing Copy', route: '/studio/publishing?type=landing', icon: '🌐' }
      ],
      recentItems: ['Devotional eBook v2', 'Prayer Journal PDF', 'Faith Bundle Landing']
    },
    {
      id: 'builder',
      name: 'App & Site Builder',
      description: 'Professional website and application development platform',
      icon: '🏗️',
      route: '/studio/builder',
      legacyRoute: '/website-builder',
      color: 'from-cyan-600 to-blue-600',
      status: 'active',
      category: 'development',
      features: ['Visual Builder', 'Templates', 'Deploy', 'Mobile Apps'],
      actions: [
        { label: 'New App/Site', route: '/studio/builder?action=new', icon: '➕' },
        { label: 'Templates', route: '/studio/builder?view=templates', icon: '📋' },
        { label: 'Deploy', route: '/studio/builder?action=deploy', icon: '🚀' }
      ],
      recentItems: ['Daily Devo App', 'Kids Story Player', 'Prayer Timer']
    },
    {
      id: 'intelligence',
      name: 'Intelligence Counsel',
      description: 'AI-powered strategic guidance with Claude + Copilot + 48 Intelligence Engines',
      icon: '🧠',
      route: '/studio/intelligence',
      legacyRoute: '/action-ai-council',
      color: 'from-indigo-600 to-purple-600',
      status: 'active',
      category: 'development',
      features: ['Architecture (Claude)', 'Code Gen (Copilot)', '48 AI Engines', 'Strategic Guidance'],
      actions: [
        { label: 'Ask Claude', route: '/studio/intelligence?mode=claude', icon: '🤖' },
        { label: 'Copilot Gen', route: '/studio/intelligence?mode=copilot', icon: '💻' },
        { label: '48 Engines', route: '/studio/intelligence?view=engines', icon: '🧠' }
      ],
      recentItems: ['Architecture Planning', 'Code Refactor', 'Strategic Analysis']
    }
  ],

  intelligenceEngines: {
    total: 48,
    categories: [
      {
        name: 'Creative Intelligence',
        icon: '🎨',
        engines: ['Audio Synthesis', 'Video Generation', 'Graphic Design', 'Content Creation', 'Voice Synthesis', 'Music Composition'],
        count: 6,
        color: 'from-purple-900/50 to-pink-900/50'
      },
      {
        name: 'Analytical Intelligence',
        icon: '📊',
        engines: ['Data Analysis', 'Pattern Recognition', 'Trend Forecasting', 'Performance Analytics', 'Market Research', 'Sentiment Analysis'],
        count: 6,
        color: 'from-blue-900/50 to-cyan-900/50'
      },
      {
        name: 'Strategic Intelligence',
        icon: '🎯',
        engines: ['Decision Support', 'Risk Assessment', 'Strategic Planning', 'Competitive Analysis', 'Resource Optimization', 'Goal Alignment'],
        count: 6,
        color: 'from-green-900/50 to-emerald-900/50'
      },
      {
        name: 'Operational Intelligence',
        icon: '⚙️',
        engines: ['Workflow Automation', 'Process Optimization', 'Task Management', 'Resource Allocation', 'Quality Control', 'System Monitoring'],
        count: 6,
        color: 'from-amber-900/50 to-yellow-900/50'
      },
      {
        name: 'Communication Intelligence',
        icon: '💬',
        engines: ['Natural Language Processing', 'Translation', 'Summarization', 'Communication Optimization', 'Audience Analysis', 'Message Crafting'],
        count: 6,
        color: 'from-rose-900/50 to-pink-900/50'
      },
      {
        name: 'Research Intelligence',
        icon: '🔬',
        engines: ['Information Retrieval', 'Knowledge Synthesis', 'Fact Checking', 'Citation Management', 'Literature Review', 'Research Planning'],
        count: 6,
        color: 'from-indigo-900/50 to-purple-900/50'
      },
      {
        name: 'Technical Intelligence',
        icon: '💻',
        engines: ['Code Generation', 'System Architecture', 'Security Analysis', 'Performance Tuning', 'Error Detection', 'Technology Assessment'],
        count: 6,
        color: 'from-cyan-900/50 to-blue-900/50'
      },
      {
        name: 'Business Intelligence',
        icon: '💼',
        engines: ['Revenue Optimization', 'Customer Insights', 'Market Analysis', 'Financial Planning', 'Growth Strategy', 'Competitive Intelligence'],
        count: 6,
        color: 'from-emerald-900/50 to-green-900/50'
      }
    ]
  },

  aiAssistants: [
    {
      name: 'Claude',
      provider: 'Anthropic',
      roles: ['architecture', 'specifications', 'flow-design'],
      description: 'Strategic architecture and design guidance',
      icon: '🤖'
    },
    {
      name: 'Copilot',
      provider: 'GitHub',
      roles: ['code-completion', 'tests', 'refactoring'],
      description: 'Code generation and development assistance',
      icon: '💻'
    }
  ]
};

/**
 * Get studio by ID
 */
export const getStudio = (id: string): StudioTile | undefined => {
  return dashboardConfig.studios.find(studio => studio.id === id);
};

/**
 * Get studios by category
 */
export const getStudiosByCategory = (category: StudioCategory): StudioTile[] => {
  return dashboardConfig.studios.filter(studio => studio.category === category);
};

/**
 * Get active studios only
 */
export const getActiveStudios = (): StudioTile[] => {
  return dashboardConfig.studios.filter(studio => studio.status === 'active');
};

/**
 * Get studio route mapping (for backwards compatibility)
 */
export const getStudioRouteMap = (): Record<string, string> => {
  return dashboardConfig.studios.reduce((acc, studio) => {
    if (studio.legacyRoute) {
      acc[studio.legacyRoute] = studio.route;
    }
    return acc;
  }, {} as Record<string, string>);
};
