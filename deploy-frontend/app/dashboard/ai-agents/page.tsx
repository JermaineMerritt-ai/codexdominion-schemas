import { fetchAgents } from "@/lib/api";
import Link from "next/link";

export default async function AIAgentsPage() {
  const data = await fetchAgents();
  const agents = data.agents || [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">AI Agents</h1>
        <p className="text-sm text-slate-400 mt-1">
          Sovereign orchestrators, execution specialists, and strategic advisors
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {agents.map((agent: any) => (
          <Link
            key={agent.id}
            href={`/dashboard/ai-agents/${agent.id}`}
            className="group"
          >
            <div className="border border-slate-800 rounded-lg p-6 bg-slate-900 hover:border-slate-700 transition-colors">
              <div className="flex items-start gap-4">
                <div
                  className="w-12 h-12 rounded-full flex items-center justify-center text-2xl"
                  style={{ backgroundColor: agent.ui?.avatar_color || "#6366f1" }}
                >
                  {getIconEmoji(agent.ui?.icon)}
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-slate-50 group-hover:text-white transition-colors">
                    {agent.name}
                  </h3>
                  <p className="text-xs text-slate-400 mt-1 line-clamp-2">
                    {agent.role || agent.description}
                  </p>
                  {agent.mode && (
                    <div className="mt-2">
                      <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                        {agent.mode}
                      </span>
                    </div>
                  )}
                </div>
              </div>
              <div className="mt-4 text-sm text-slate-500 group-hover:text-slate-400 transition-colors">
                Open Chat →
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

function getIconEmoji(icon?: string): string {
  const iconMap: Record<string, string> = {
    crown: "👑",
    bolt: "⚡",
    brain: "🧠",
    target: "🎯",
    chat: "💬",
    user: "👤",
    gavel: "⚖️",
    code: "💻",
  };
  return iconMap[icon || ""] || "🤖";
}
