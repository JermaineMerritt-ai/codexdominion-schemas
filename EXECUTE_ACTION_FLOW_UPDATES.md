// EXECUTE-ACTION FLOW ENHANCEMENT FOR CHAT PAGE
// Add these updates to dashboard-app/app/dashboard/chat/page.tsx

// 1. UPDATE INTERFACE AT TOP (around line 6):
interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  workflowData?: any; // For execute-action flow metadata
}

interface ConversationState {
  workflow_id?: string;
  step?: number;
  collected_inputs?: Record<string, string>;
}

// 2. ADD CONVERSATION STATE (around line 24):
const [conversationState, setConversationState] = useState<ConversationState>({});

// 3. UPDATE GREETING MESSAGE (around line 17):
const [messages, setMessages] = useState<Message[]>([
  {
    role: "assistant",
    content: "Ready when you are. What action should I execute?",
    timestamp: new Date(),
  },
]);

// 4. ENHANCE handleSend FUNCTION (replace existing):
const handleSend = async () => {
  if (!input.trim()) return;

  const userMessage: Message = {
    role: "user",
    content: input,
    timestamp: new Date(),
  };

  setMessages(prev => [...prev, userMessage]);
  setInput("");
  setLoading(true);

  try {
    // Call Flask chat API with conversation state
    const response = await fetch("http://localhost:5000/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        agent_id: agentId,
        message: input,
        conversation_state: conversationState, // Include workflow state
      }),
    });

    const data = await response.json();

    // Check if this is an execute-action flow
    if (data.action_type === "input_gathering") {
      // Update conversation state for next turn
      setConversationState({
        workflow_id: data.workflow_id,
        step: data.current_step || 1,
        collected_inputs: data.collected_inputs || {},
      });
    } else if (data.action_type === "execution_ready") {
      // Show ROI and execution button
      setConversationState({
        workflow_id: data.workflow_id,
        step: data.current_step || 99,
        collected_inputs: data.collected_inputs || {},
      });
    }

    const assistantMessage: Message = {
      role: "assistant",
      content: data.response || "I've processed your request.",
      timestamp: new Date(),
      workflowData: data, // Store full workflow data for rendering
    };

    setMessages(prev => [...prev, assistantMessage]);

    // Handle automatic execution if user says "yes" to ready state
    if (data.ready_to_execute && input.toLowerCase().includes("yes")) {
      await handleExecuteWorkflow(data.workflow_id, data.collected_inputs);
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

// 5. ADD EXECUTION HANDLER:
const handleExecuteWorkflow = async (workflowId: string, inputs: Record<string, string>) => {
  try {
    setLoading(true);

    const response = await fetch("http://localhost:5000/api/workflow/execute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        agent_id: agentId,
        workflow_id: workflowId,
        inputs: inputs,
      }),
    });

    const data = await response.json();

    if (data.success) {
      const confirmationMessage: Message = {
        role: "assistant",
        content: `✅ **Workflow Deployed Successfully!**\n\n🆔 **ID:** ${data.workflow_id}\n📊 **Status:** ${data.status}\n\n**Next Steps:**\n${data.next_steps.map((step: string) => `• ${step}`).join("\n")}\n\n🔗 [View Dashboard](${data.dashboard_url})`,
        timestamp: new Date(),
        workflowData: data,
      };
      setMessages(prev => [...prev, confirmationMessage]);

      // Reset conversation state
      setConversationState({});
    }
  } catch (error) {
    console.error("Execution error:", error);
    const errorMessage: Message = {
      role: "assistant",
      content: "Workflow execution failed. Please try again.",
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, errorMessage]);
  } finally {
    setLoading(false);
  }
};

// 6. ADD ROI DISPLAY COMPONENT (insert before return statement):
const renderWorkflowData = (workflowData: any) => {
  if (!workflowData || !workflowData.roi_estimate) return null;

  const roi = workflowData.roi_estimate;

  return (
    <div className="mt-3 p-4 bg-slate-800 border border-slate-700 rounded-lg">
      <div className="text-sm font-semibold text-blue-400 mb-2">💰 ROI Breakdown</div>
      <div className="grid grid-cols-2 gap-3 text-xs">
        <div>
          <div className="text-slate-400">Time Saved/Week</div>
          <div className="text-white font-semibold">{roi.time_saved_per_week} hours</div>
        </div>
        <div>
          <div className="text-slate-400">Monthly Savings</div>
          <div className="text-green-400 font-semibold">${roi.monthly_savings.toFixed(2)}</div>
        </div>
        <div>
          <div className="text-slate-400">Annual Savings</div>
          <div className="text-green-400 font-semibold">${roi.annual_savings.toFixed(2)}</div>
        </div>
        <div>
          <div className="text-slate-400">Setup Time</div>
          <div className="text-white font-semibold">{roi.setup_time} min</div>
        </div>
      </div>

      {workflowData.ready_to_execute && (
        <button
          onClick={() => handleExecuteWorkflow(workflowData.workflow_id, workflowData.collected_inputs)}
          className="mt-3 w-full py-2 bg-green-600 hover:bg-green-700 text-white text-sm font-semibold rounded-lg"
        >
          ✅ Deploy Workflow
        </button>
      )}
    </div>
  );
};

// 7. UPDATE MESSAGE RENDERING (in the messages.map section):
// Find the existing message rendering code and add:
{message.workflowData && renderWorkflowData(message.workflowData)}
