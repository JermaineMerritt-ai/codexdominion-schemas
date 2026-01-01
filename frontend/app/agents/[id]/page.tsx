"use client";

import { useState } from "react";
import { sendChat } from "@/lib/api/chat";

export default function AgentChatPage({ params }: { params: { id: string } }) {
  const agentId = params.id;
  const [messages, setMessages] = useState<{ role: "user" | "agent"; text: string }[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [lastSavings, setLastSavings] = useState<any | null>(null);
  const [lastWorkflowId, setLastWorkflowId] = useState<string | null>(null);

  async function handleSendChat(mode: "chat" | "execute") {
    if (!input.trim()) return;
    setLoading(true);
    const userText = input.trim();
    setInput("");
    setMessages(prev => [...prev, { role: "user", text: userText }]);

    try {
      const context =
        mode === "execute"
          ? {
              calculator_inputs: {
                tasks_per_week: 200,
                time_per_task_minutes: 10,
                hourly_wage: 25,
                automation_percent: 0.7,
                error_rate: 0.1,
                cost_per_error: 15,
                value_per_accelerated_task: 0
              },
              workflow_inputs: {
                workflow_type: "customer_followup",
                description: userText
              }
            }
          : {};

      const res = await sendChat({
        agentId,
        message: userText,
        mode,
        context
      });

      if (res.savings) {
        setLastSavings(res.savings);
      }
      if (res.workflow_action) {
        setLastWorkflowId(res.workflow_action);
      }

      setMessages(prev => [...prev, { role: "agent", text: res.reply }]);
    } catch (err: any) {
      setMessages(prev => [
        ...prev,
        { role: "agent", text: "There was an error processing your request." }
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-4 max-w-3xl">
      <h1 className="text-2xl font-semibold">AI Agent Chat</h1>
      <div className="border border-slate-800 rounded-lg p-4 bg-slate-900 h-96 overflow-auto">
        {messages.length === 0 && (
          <div className="text-slate-500 text-sm">
            Start by asking this agent what you want to automate or understand.
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`mb-2 ${m.role === "user" ? "text-right" : "text-left"}`}>
            <div
              className={`inline-block px-3 py-2 rounded ${
                m.role === "user" ? "bg-blue-600" : "bg-slate-800"
              }`}
            >
              <span className="text-sm">{m.text}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          className="flex-1 px-3 py-2 rounded bg-slate-900 border border-slate-700 text-sm"
          placeholder="Describe what you want to automate or ask..."
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSendChat("chat");
            }
          }}
        />
        <button
          onClick={() => handleSendChat("chat")}
          disabled={loading}
          className="px-3 py-2 rounded bg-slate-700 hover:bg-slate-600 text-sm disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? "..." : "Chat"}
        </button>
        <button
          onClick={() => handleSendChat("execute")}
          disabled={loading}
          className="px-3 py-2 rounded bg-emerald-600 hover:bg-emerald-500 text-sm disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? "..." : "Execute Action"}
        </button>
      </div>

      {lastSavings && (
        <div className="border border-emerald-700 rounded-lg p-4 bg-slate-900">
          <div className="text-xs uppercase text-emerald-400 mb-2">Estimated Savings</div>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm">
            <Stat label="Weekly" value={`$${lastSavings.weekly_savings.toFixed(2)}`} />
            <Stat label="Monthly" value={`$${lastSavings.monthly_savings.toFixed(2)}`} />
            <Stat label="Yearly" value={`$${lastSavings.yearly_savings.toFixed(2)}`} />
            <Stat label="Hours/week saved" value={lastSavings.hours_saved_per_week.toFixed(2)} />
          </div>
          {lastWorkflowId && (
            <div className="mt-3 text-xs text-slate-400">
              Workflow created: <span className="font-mono">{lastWorkflowId}</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function Stat({ label, value }: { label: string; value: any }) {
  return (
    <div>
      <div className="text-slate-400 text-xs">{label}</div>
      <div className="font-semibold text-sm">{value}</div>
    </div>
  );
}
