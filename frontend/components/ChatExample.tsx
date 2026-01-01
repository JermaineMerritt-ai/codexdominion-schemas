/**
 * Example Chat Component
 * 
 * Demonstrates usage of the unified chat API with both modes
 */

"use client";

import { useState } from "react";
import { useChat } from "@/lib/api/useChat";

export default function ChatExample() {
  const { loading, error, response, chat, execute } = useChat();
  const [message, setMessage] = useState("");
  const [tasksPerWeek, setTasksPerWeek] = useState(200);
  const [timePerTask, setTimePerTask] = useState(10);
  const [hourlyWage, setHourlyWage] = useState(25);
  const [automationPercent, setAutomationPercent] = useState(0.7);

  const AGENT_ID = "agent_jermaine_super_action";

  const handleChat = async () => {
    if (!message.trim()) return;
    await chat(AGENT_ID, message);
    setMessage("");
  };

  const handleExecute = async () => {
    await execute(AGENT_ID, message || "Create automation workflow", {
      calculator_inputs: {
        tasks_per_week: tasksPerWeek,
        time_per_task_minutes: timePerTask,
        hourly_wage: hourlyWage,
        automation_percent: automationPercent,
        error_rate: 0.1,
        cost_per_error: 15,
        value_per_accelerated_task: 0
      },
      workflow_inputs: {
        workflow_name: "Customer Followup Automation",
        target_platform: "Email",
        frequency: "Daily"
      }
    });
    setMessage("");
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold">Chat API Example</h1>

      {/* Input Section */}
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">
            Message
          </label>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message..."
            className="w-full p-3 border rounded-lg"
            rows={3}
            disabled={loading}
          />
        </div>

        {/* Calculator Inputs */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">
              Tasks per Week
            </label>
            <input
              type="number"
              value={tasksPerWeek}
              onChange={(e) => setTasksPerWeek(Number(e.target.value))}
              className="w-full p-2 border rounded"
              disabled={loading}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">
              Time per Task (min)
            </label>
            <input
              type="number"
              value={timePerTask}
              onChange={(e) => setTimePerTask(Number(e.target.value))}
              className="w-full p-2 border rounded"
              disabled={loading}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">
              Hourly Wage ($)
            </label>
            <input
              type="number"
              value={hourlyWage}
              onChange={(e) => setHourlyWage(Number(e.target.value))}
              className="w-full p-2 border rounded"
              disabled={loading}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">
              Automation % (0.0-1.0)
            </label>
            <input
              type="number"
              step="0.1"
              value={automationPercent}
              onChange={(e) => setAutomationPercent(Number(e.target.value))}
              className="w-full p-2 border rounded"
              disabled={loading}
            />
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-4">
          <button
            onClick={handleChat}
            disabled={loading || !message.trim()}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg 
                     hover:bg-blue-700 disabled:bg-gray-400 
                     disabled:cursor-not-allowed transition"
          >
            💬 Chat Mode
          </button>
          <button
            onClick={handleExecute}
            disabled={loading}
            className="px-6 py-3 bg-green-600 text-white rounded-lg 
                     hover:bg-green-700 disabled:bg-gray-400 
                     disabled:cursor-not-allowed transition"
          >
            🚀 Execute Mode (Create Workflow)
          </button>
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <p className="text-blue-700">⏳ Processing...</p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-700 font-medium">❌ Error</p>
          <p className="text-red-600 text-sm mt-1">{error}</p>
        </div>
      )}

      {/* Response Display */}
      {response && (
        <div className="space-y-4">
          {/* Agent Info */}
          <div className="p-4 bg-gray-50 border rounded-lg">
            <h3 className="font-semibold text-lg mb-2">
              {response.agent_name || "AI Agent"}
            </h3>
            <p className="text-sm text-gray-600">
              Mode: <span className="font-medium">{response.mode}</span>
            </p>
          </div>

          {/* Reply */}
          <div className="p-4 bg-white border rounded-lg">
            <h4 className="font-medium mb-2">Reply:</h4>
            <p className="text-gray-700">{response.reply}</p>
          </div>

          {/* Workflow Info (Execute Mode) */}
          {response.workflow_action && (
            <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
              <h4 className="font-medium mb-2 text-green-800">
                ✅ Workflow Created
              </h4>
              <p className="text-sm text-green-700 mb-2">
                ID: <code className="bg-green-100 px-2 py-1 rounded">
                  {response.workflow_action}
                </code>
              </p>
            </div>
          )}

          {/* Savings Breakdown (Execute Mode) */}
          {response.savings && (
            <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <h4 className="font-medium mb-3 text-yellow-800">
                💰 ROI Savings
              </h4>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <p className="text-gray-600">Weekly</p>
                  <p className="font-semibold text-lg">
                    ${response.savings.weekly_savings.toLocaleString()}
                  </p>
                </div>
                <div>
                  <p className="text-gray-600">Monthly</p>
                  <p className="font-semibold text-lg">
                    ${response.savings.monthly_savings.toLocaleString()}
                  </p>
                </div>
                <div>
                  <p className="text-gray-600">Yearly</p>
                  <p className="font-semibold text-lg text-green-600">
                    ${response.savings.yearly_savings.toLocaleString()}
                  </p>
                </div>
                <div>
                  <p className="text-gray-600">Hours Saved/Week</p>
                  <p className="font-semibold text-lg">
                    {response.savings.hours_saved_per_week.toFixed(2)}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* API Documentation */}
      <div className="mt-8 p-4 bg-gray-100 rounded-lg">
        <h3 className="font-semibold mb-2">📚 API Info</h3>
        <p className="text-sm text-gray-600">
          Endpoint: <code className="bg-white px-2 py-1 rounded">
            POST /api/chat
          </code>
        </p>
        <p className="text-sm text-gray-600 mt-1">
          Modes: chat (conversational) | execute (workflow + ROI)
        </p>
      </div>
    </div>
  );
}
