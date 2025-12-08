'use client';

import { useEngineStatus } from '@/hooks/useEngineStatus';

interface EngineConfig {
  title: string;
  defaultStatus: 'green' | 'orange' | 'red';
  category: string;
}

const engineConfigs: EngineConfig[] = [
  // Core Business Engines
  { title: 'Distribution Engine', defaultStatus: 'green', category: 'Core' },
  { title: 'Marketing Engine', defaultStatus: 'green', category: 'Core' },
  { title: 'Commerce Engine', defaultStatus: 'orange', category: 'Core' },
  { title: 'Video Studio', defaultStatus: 'green', category: 'Core' },
  { title: 'Automations Engine', defaultStatus: 'red', category: 'Core' },
  { title: 'Avatars Engine', defaultStatus: 'green', category: 'Core' },

  // Operations Engines
  { title: 'Observability Engine', defaultStatus: 'green', category: 'Operations' },
  { title: 'Compliance Engine', defaultStatus: 'green', category: 'Operations' },
  { title: 'Profit Engine', defaultStatus: 'green', category: 'Operations' },

  // Content & Archive Engines
  { title: 'Replay Capsule Engine', defaultStatus: 'green', category: 'Content' },
  { title: 'Broadcast Grid Engine', defaultStatus: 'green', category: 'Content' },
  { title: 'Hymn Archive Engine', defaultStatus: 'green', category: 'Content' },

  // Creative Engines
  { title: 'Multi-Language Expansion Engine', defaultStatus: 'green', category: 'Creative' },
  { title: 'Character & World-Building Engine', defaultStatus: 'green', category: 'Creative' },
  { title: 'Music & Sound Engine', defaultStatus: 'green', category: 'Creative' },
  { title: 'Brand Identity Engine', defaultStatus: 'green', category: 'Creative' },

  // Intelligence Engines
  { title: 'RAG Intelligence Engine', defaultStatus: 'green', category: 'Intelligence' },
  { title: 'Axiom Intelligence Engine', defaultStatus: 'green', category: 'Intelligence' },
];

export function HealthGrid() {
  const { statuses, isConnected, error } = useEngineStatus();
  const categories = ['Core', 'Operations', 'Content', 'Creative', 'Intelligence'];

  // Map real-time statuses to display format
  const getEngineStatus = (title: string, defaultStatus: 'green' | 'orange' | 'red') => {
    const liveStatus = statuses[title];
    if (!liveStatus) return { status: defaultStatus, uptime: undefined };

    const statusMap: Record<string, 'green' | 'orange' | 'red'> = {
      operational: 'green',
      degraded: 'orange',
      down: 'red',
    };

    return {
      status: statusMap[liveStatus.status] || defaultStatus,
      uptime: liveStatus.uptime,
    };
  };

  return (
    <div className="space-y-6">
      {/* Connection Status Banner */}
      {!isConnected && error && (
        <div className="p-3 bg-red-900/30 border border-red-500 rounded-lg flex items-center space-x-2">
          <span className="text-red-400">⚠️</span>
          <span className="text-red-400 text-sm">{error}</span>
        </div>
      )}
      {isConnected && (
        <div className="p-3 bg-green-900/30 border border-green-500 rounded-lg flex items-center space-x-2">
          <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
          <span className="text-green-400 text-sm">Live status stream connected</span>
        </div>
      )}

      {/* Engine Categories */}
      {categories.map((category) => {
        const categoryEngines = engineConfigs.filter((e) => e.category === category);
        if (categoryEngines.length === 0) return null;

        return (
          <div key={category}>
            <h3 className="text-lg font-semibold text-[#FFD700] mb-3 flex items-center">
              <span className="mr-2">{getCategoryIcon(category)}</span>
              {category} Engines
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {categoryEngines.map((engine, idx) => {
                const { status, uptime } = getEngineStatus(engine.title, engine.defaultStatus);
                return (
                  <HealthTile
                    key={idx}
                    title={engine.title}
                    status={status}
                    uptime={uptime}
                  />
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
}

function HealthTile({
  title,
  status,
  uptime
}: {
  title: string;
  status: 'green' | 'orange' | 'red';
  uptime?: string;
}) {
  const colors = {
    green: { bg: 'bg-green-600', text: 'text-green-400', border: 'border-green-500', dot: 'bg-green-500' },
    orange: { bg: 'bg-orange-600', text: 'text-orange-400', border: 'border-orange-500', dot: 'bg-orange-500' },
    red: { bg: 'bg-red-600', text: 'text-red-400', border: 'border-red-500', dot: 'bg-red-500' },
  };

  const color = colors[status];

  return (
    <div
      className={`bg-[#1A1F3C] p-4 rounded-lg border ${color.border} flex flex-col justify-between hover:shadow-lg hover:scale-[1.02] transition-all cursor-pointer group`}
    >
      <div className="flex items-start justify-between mb-2">
        <span className="font-medium text-sm flex-1 group-hover:text-[#FFD700] transition-colors">
          {title}
        </span>
        <span className={`w-3 h-3 rounded-full ${color.dot} ${status === 'green' ? 'animate-pulse' : ''}`}></span>
      </div>
      <div className="flex items-center justify-between mt-2">
        <span className={`px-2 py-1 rounded-full text-xs font-bold ${color.bg} uppercase`}>
          {status}
        </span>
        {uptime && (
          <span className="text-xs text-gray-400">
            <span className={color.text}>{uptime}</span>
          </span>
        )}
      </div>
    </div>
  );
}

function getCategoryIcon(category: string): string {
  const icons: Record<string, string> = {
    Core: '⚙️',
    Operations: '📊',
    Content: '📚',
    Creative: '🎨',
    Intelligence: '🧠',
  };
  return icons[category] || '🔧';
}
