"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { suggestWorkflows, sendChat, type WorkflowSuggestion } from "@/lib/api/chat";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  suggestions?: WorkflowSuggestion[];
}

export default function ChatPage() {
  const searchParams = useSearchParams();
  const agentId = searchParams.get("agent") || "agent_jermaine_super_action";
  
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "How can I assist with your next move?",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [agent, setAgent] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [selectedWorkflow, setSelectedWorkflow] = useState<WorkflowSuggestion | null>(null);

  useEffect(() => {
    // Fetch agent details
    fetch(`http://localhost:5000/api/agents/${agentId}`)
      .then(res => res.json())
      .then(data => setAgent(data))
      .catch(err => console.error("Failed to load agent:", err));
  }, [agentId]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    const userInput = input;
    setInput("");
    setLoading(true);

    try {
      // First, get workflow suggestions using the API helper
      const suggestionData = await suggestWorkflows(userInput);
      const suggestions = suggestionData.suggestions || [];

      // If we have suggestions, show them to the user
      if (suggestions.length > 0) {
        const assistantMessage: Message = {
          role: "assistant",
          content: `I found ${suggestions.length} workflow${suggestions.length > 1 ? 's' : ''} that might help with your request. Select one to continue:`,
          timestamp: new Date(),
          suggestions: suggestions.slice(0, 3), // Show top 3
        };

        setMessages(prev => [...prev, assistantMessage]);
      } else {
        // Fallback to regular chat using the API helper
        const data = await sendChat(agentId, userInput, "chat");

        const assistantMessage: Message = {
          role: "assistant",
          content: data.reply || "I've processed your request.",
          timestamp: new Date(),
        };

        setMessages(prev => [...prev, assistantMessage]);
      }
    } catch (error) {
      console.error("Chat error:", error);
      const errorMessage: Message = {
        role: "assistant",
        content: "I'm currently experiencing connectivity issues. Please try again.",
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleWorkflowSelection = async (workflow: WorkflowSuggestion) => {
    setSelectedWorkflow(workflow);
    
    const userMessage: Message = {
      role: "user",
      content: `I'll use: ${workflow.name}`,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      // Get workflow details with required inputs using sendChat helper
      const data = await sendChat(
        agentId,
        `Setting up ${workflow.name}`,
        "confirm",
        { workflow_type: workflow.id }
      );

      const assistantMessage: Message = {
        role: "assistant",
        content: data.reply || `Great! To set up ${workflow.name}, I'll need some information. You can provide the inputs below.`,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);

      // For now, show a simple message about inputs
      // In a full implementation, you'd show a form here
      const inputsMessage: Message = {
        role: "assistant",
        content: `Required inputs: ${data.workflow_type?.required_inputs?.join(", ") || "No inputs required"}. (Input form coming soon!)`,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, inputsMessage]);
    } catch (error) {
      console.error("Workflow confirmation error:", error);
      const errorMessage: Message = {
        role: "assistant",
        content: "Error setting up workflow. Please try again.",
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const getIconEmoji = (icon?: string): string => {
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
  };

  if (!agent) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-slate-400">Loading agent...</div>
      </div>
    );
  }

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col max-w-4xl mx-auto">
      {/* Agent Header */}
      <div className="border-b border-slate-800 pb-4 mb-4">
        <div className="flex items-center gap-4">
          <div
            className="w-16 h-16 rounded-full flex items-center justify-center text-3xl flex-shrink-0"
            style={{ backgroundColor: agent.ui?.avatar_color || "#6366f1" }}
          >
            {getIconEmoji(agent.ui?.icon)}
          </div>
          <div>
            <h1 className="text-xl font-semibold">{agent.name}</h1>
            <p className="text-sm text-slate-400">{agent.role}</p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 mb-4">
        {messages.map((msg, idx) => (
          <div key={idx}>
            <div
              className={`flex gap-3 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              {msg.role === "assistant" && (
                <div
                  className="w-8 h-8 rounded-full flex items-center justify-center text-lg flex-shrink-0"
                  style={{ backgroundColor: agent.ui?.avatar_color || "#6366f1" }}
                >
                  {getIconEmoji(agent.ui?.icon)}
                </div>
              )}
              <div
                className={`max-w-[70%] rounded-lg px-4 py-2 ${
                  msg.role === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-slate-800 text-slate-100"
                }`}
              >
                <p className="text-sm">{msg.content}</p>
                <p className="text-xs opacity-60 mt-1">
                  {msg.timestamp.toLocaleTimeString()}
                </p>
              </div>
              {msg.role === "user" && (
                <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center text-lg flex-shrink-0">
                  👤
                </div>
              )}
            </div>

            {/* Workflow Suggestions */}
            {msg.role === "assistant" && msg.suggestions && msg.suggestions.length > 0 && (
              <div className="ml-11 mt-3 space-y-2">
                {msg.suggestions.map((suggestion) => (
                  <button
                    key={suggestion.id}
                    onClick={() => handleWorkflowSelection(suggestion)}
                    disabled={loading}
                    className="w-full text-left border border-slate-700 hover:border-blue-500 bg-slate-900 hover:bg-slate-800 rounded-lg p-3 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex-1">
                        <div className="font-semibold text-sm text-slate-100">
                          {suggestion.name}
                        </div>
                        <div className="text-xs text-slate-400 mt-1">
                          {suggestion.description}
                        </div>
                        <div className="flex gap-2 mt-2">
                          <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                            {suggestion.category}
                          </span>
                          <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                            {suggestion.domain}
                          </span>
                        </div>
                      </div>
                      <div className="text-blue-400 text-lg">→</div>
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="flex gap-3">
            <div
              className="w-8 h-8 rounded-full flex items-center justify-center text-lg"
              style={{ backgroundColor: agent.ui?.avatar_color || "#6366f1" }}
            >
              {getIconEmoji(agent.ui?.icon)}
            </div>
            <div className="bg-slate-800 rounded-lg px-4 py-2">
              <p className="text-sm text-slate-400">Thinking...</p>
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <div className="border-t border-slate-800 pt-4">
        <div className="flex flex-col gap-3">
          {/* Toolbar */}
          <div className="flex gap-2 px-2">
            <button
              title="Voice Mode"
              className="p-2 hover:bg-slate-800 rounded-lg transition-colors"
            >
              <svg className="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
            </button>
            <button
              title="Upload Files (Documents, Images, PDFs)"
              className="p-2 hover:bg-slate-800 rounded-lg transition-colors"
            >
              <svg className="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
              </svg>
            </button>
          </div>

          {/* Input Area */}
          <div className="flex gap-2">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              placeholder="Type your message... (Shift+Enter for new line)"
              disabled={loading}
              rows={3}
              className="flex-1 bg-slate-900 border border-slate-800 rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-slate-700 disabled:opacity-50 resize-none"
            />
            <button
              onClick={handleSend}
              disabled={loading || !input.trim()}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-colors self-end"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
