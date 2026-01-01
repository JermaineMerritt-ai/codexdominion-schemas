"use client";

import { useEffect, useState, useRef } from "react";
import { useParams } from "next/navigation";
import { suggestWorkflows, sendChat, WorkflowSuggestion } from "@/lib/api/chat";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:5000";

interface Agent {
  id: string;
  name: string;
  role: string;
  personality: string;
  reputation: {
    score: number;
    total_savings: number;
    workflows_executed: number;
    approval_rate: number;
  };
  ui: {
    color: string;
    icon: string;
    emoji: string;
  };
}

interface Message {
  role: "user" | "agent";
  text: string;
}

export default function AgentChatPage() {
  const params = useParams();
  const agentId = params.id as string;

  const [agent, setAgent] = useState<Agent | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [userText, setUserText] = useState("");
  const [workflowSuggestions, setWorkflowSuggestions] = useState<WorkflowSuggestion[]>([]);
  const [lastSavings, setLastSavings] = useState<any | null>(null);
  const [lastWorkflowId, setLastWorkflowId] = useState<string | null>(null);
  const [workflowStatus, setWorkflowStatus] = useState<any | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Fetch agent info on mount
  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${API_BASE}/api/agents/${agentId}`);
        if (!res.ok) throw new Error("Failed to fetch agent");
        const data = await res.json();
        setAgent(data);
        setMessages([
          {
            role: "agent",
            text: `Hi! I'm ${data.name}. Tell me what you'd like to automate—invoices, follow-ups, order processing, or anything else.`,
          },
        ]);
      } catch (err) {
        console.error(err);
      }
    })();
  }, [agentId]);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Poll workflow status if we have a workflow ID
  useEffect(() => {
    if (!lastWorkflowId) return;
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${API_BASE}/api/workflows/${lastWorkflowId}`);
        if (res.ok) {
          const wf = await res.json();
          setWorkflowStatus(wf);
        }
      } catch (err) {
        console.error("Error polling workflow:", err);
      }
    }, 5000);
    return () => clearInterval(interval);
  }, [lastWorkflowId]);

  // Send user message
  async function handleSend() {
    if (!userText.trim()) return;
    const msg = userText.trim();
    setUserText("");
    setMessages((prev) => [...prev, { role: "user", text: msg }]);

    try {
      // Try to get workflow suggestions first
      const suggestionRes = await suggestWorkflows(msg);
      if (suggestionRes.suggestions && suggestionRes.suggestions.length > 0) {
        setWorkflowSuggestions(suggestionRes.suggestions);
        setMessages((prev) => [
          ...prev,
          {
            role: "agent",
            text: "I found some workflow options that match your request. Click one to see estimated savings.",
          },
        ]);
      } else {
        // No suggestions → just chat
        const res = await sendChat(agentId, msg, "chat");
        setMessages((prev) => [...prev, { role: "agent", text: res.reply || "I understand. How can I help?" }]);
      }
    } catch (err: any) {
      console.error(err);
      setMessages((prev) => [...prev, { role: "agent", text: "Sorry, I encountered an error." }]);
    }
  }

  // User clicks a workflow suggestion
  async function handleWorkflowClick(wf: WorkflowSuggestion) {
    setMessages((prev) => [
      ...prev,
      { role: "agent", text: `Great choice! Let me calculate savings for "${wf.name}"...` },
    ]);

    try {
      // Calculate savings (dummy inputs for demo)
      const calcRes = await fetch(`${API_BASE}/api/calculators/savings`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tasks_per_week: 200,
          time_per_task_minutes: 10,
          hourly_wage: 25,
          automation_percent: 0.7,
          error_rate: 0.1,
          cost_per_error: 15,
          value_per_accelerated_task: 0,
        }),
      });
      const savingsData = await calcRes.json();
      setLastSavings(savingsData);

      setMessages((prev) => [
        ...prev,
        {
          role: "agent",
          text: `📊 This workflow could save $${savingsData.weekly_savings.toLocaleString()}/week, or $${savingsData.yearly_savings.toLocaleString()}/year.\n\nReady to create it? Click "Execute Workflow" below.`,
        },
      ]);

      // Store selected workflow for execution
      setWorkflowSuggestions([wf]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [...prev, { role: "agent", text: "Error calculating savings." }]);
    }
  }

  // Execute workflow (mode = execute)
  async function handleExecuteWorkflow(workflowTypeId: string) {
    setMessages((prev) => [...prev, { role: "agent", text: "⚙️ Creating your workflow..." }]);

    try {
      const res = await sendChat(agentId, `Execute workflow: ${workflowTypeId}`, "execute", {
        workflow_type: workflowTypeId,
        calculator_inputs: {
          tasks_per_week: 200,
          time_per_task_minutes: 10,
          hourly_wage: 25,
          automation_percent: 0.7,
        },
      });

      // Check if workflow created
      if (res.workflow_action) {
        const wfId = typeof res.workflow_action === 'string' 
          ? res.workflow_action 
          : res.workflow_action.id;
        setLastWorkflowId(wfId);
        
        // Check if needs council review
        const needsReview = lastSavings && lastSavings.weekly_savings >= 1000;
        
        setMessages((prev) => [
          ...prev,
          {
            role: "agent",
            text: needsReview
              ? `✅ Workflow Created!\n\nWorkflow ID: ${wfId}\n\nThis workflow requires council review (savings ≥ $1,000/week). Status: Pending approval.`
              : `✅ Workflow Active!\n\nWorkflow ID: ${wfId}\n\nYour automation is now running.`,
          },
        ]);
      } else {
        setMessages((prev) => [
          ...prev,
          { role: "agent", text: res.reply || "Workflow created successfully." },
        ]);
      }
    } catch (err) {
      console.error(err);
      setMessages((prev) => [...prev, { role: "agent", text: "Error creating workflow." }]);
    }
  }

  if (!agent) {
    return (
      <div className="flex items-center justify-center h-screen bg-slate-900">
        <div className="text-slate-400">Loading agent...</div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <div className="flex-shrink-0 border-b border-slate-700 bg-slate-900/80 backdrop-blur">
        <div className="p-4 flex items-center gap-4">
          {/* eslint-disable-next-line react/no-unknown-property */}
          <div
            className="w-14 h-14 rounded-full flex items-center justify-center text-2xl font-bold border-2 border-white shadow-lg"
            style={{
              background: `linear-gradient(135deg, ${agent.ui.color}, ${agent.ui.color}dd)`,
            }}
          >
            {agent.ui.emoji || agent.name.charAt(0)}
          </div>
          <div className="flex-1">
            <h1 className="text-lg font-semibold text-white">{agent.name}</h1>
            <p className="text-sm text-slate-400">{agent.role}</p>
          </div>
          <div className="text-right">
            <div className="text-xs text-slate-500">Reputation</div>
            <div className="text-sm font-semibold text-white">
              {(agent.reputation.score * 100).toFixed(0)}%
            </div>
          </div>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-2xl rounded-lg p-4 ${
                msg.role === "user" ? "bg-blue-600 text-white" : "bg-slate-800 text-slate-100"
              }`}
            >
              <div className="whitespace-pre-wrap text-sm">{msg.text}</div>
            </div>
          </div>
        ))}

        {/* Workflow Suggestions Panel */}
        {workflowSuggestions.length > 0 && (
          <div className="space-y-2">
            {workflowSuggestions.map((wf) => (
              <button
                key={wf.id}
                onClick={() => handleWorkflowClick(wf)}
                className="w-full text-left p-3 rounded-lg bg-slate-700 hover:bg-slate-600 transition-colors border border-slate-600"
              >
                <div className="font-medium text-sm text-white">{wf.name}</div>
                <div className="text-xs text-slate-400 mt-1">{wf.description}</div>
              </button>
            ))}
          </div>
        )}

        {/* Savings Display */}
        {lastSavings && (
          <div className="mt-4 rounded-lg bg-gradient-to-br from-emerald-900/40 to-green-900/40 border border-emerald-700/50 p-4">
            <div className="text-xs font-semibold text-emerald-300 uppercase mb-3">💰 Estimated Savings</div>
            <div className="grid grid-cols-3 gap-4 text-center">
              <Stat label="Weekly" value={`$${lastSavings.weekly_savings.toLocaleString()}`} />
              <Stat label="Monthly" value={`$${lastSavings.monthly_savings.toLocaleString()}`} />
              <Stat label="Annual" value={`$${lastSavings.yearly_savings.toLocaleString()}`} />
            </div>
            <div className="mt-3 text-xs text-slate-300 text-center">
              ⏱️ Time saved: {lastSavings.hours_saved_per_week.toFixed(1)} hours/week
            </div>

            {/* Execute button (only if we have a selected workflow) */}
            {workflowSuggestions.length === 1 && !lastWorkflowId && (
              <button
                onClick={() => handleExecuteWorkflow(workflowSuggestions[0].id)}
                className="mt-4 w-full py-2 px-4 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-medium text-sm transition-colors"
              >
                ✓ Execute Workflow
              </button>
            )}
          </div>
        )}

        {/* Workflow Status */}
        {lastWorkflowId && (
          <div className="mt-4 bg-slate-800 border border-slate-700 rounded-lg p-4 space-y-2">
            <div className="flex items-center justify-between text-xs">
              <span className="text-slate-400">Workflow ID:</span>
              <span className="font-mono text-slate-300">{lastWorkflowId}</span>
            </div>

            {workflowStatus && (
              <>
                <div className="flex items-center gap-2 text-xs">
                  <span className="text-slate-400">Status:</span>
                  <StatusPill label="Status" value={workflowStatus.status || "pending"} />
                </div>

                {workflowStatus.decision && (
                  <div className="flex items-center gap-2 text-xs">
                    <span className="text-slate-400">Council:</span>
                    <StatusPill label="Council" value={workflowStatus.decision} />
                  </div>
                )}
              </>
            )}
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="flex-shrink-0 border-t border-slate-700 bg-slate-900/80 backdrop-blur">
        <div className="p-4 flex gap-3">
          <textarea
            value={userText}
            onChange={(e) => setUserText(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            placeholder="Describe what you'd like to automate..."
            rows={2}
            className="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />
          <button
            onClick={handleSend}
            disabled={!userText.trim()}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:text-slate-500 text-white rounded-lg font-medium transition-colors"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

// Helper components
function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="text-xs text-slate-400">{label}</div>
      <div className="text-lg font-bold text-emerald-300">{value}</div>
    </div>
  );
}

function StatusPill({ label, value }: { label: string; value: string }) {
  const colors: Record<string, string> = {
    pending: "bg-yellow-900/40 text-yellow-300 border-yellow-700/50",
    approved: "bg-emerald-900/40 text-emerald-300 border-emerald-700/50",
    denied: "bg-rose-900/40 text-rose-300 border-rose-700/50",
    running: "bg-blue-900/40 text-blue-300 border-blue-700/50",
    completed: "bg-emerald-900/40 text-emerald-300 border-emerald-700/50",
    failed: "bg-rose-900/40 text-rose-300 border-rose-700/50",
  };

  const colorClass = colors[value.toLowerCase()] || "bg-slate-700 text-slate-300";

  return (
    <span className={`px-2 py-1 rounded-full text-xs border ${colorClass}`}>
      {value}
    </span>
  );
}
