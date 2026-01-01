/**
 * Complete Execute Example
 * 
 * Full working example of execute mode with all parameters
 */

"use client";

import { useChat } from "@/lib/api";

export default function ExecuteExample() {
  const { execute, loading, error, response } = useChat();

  const handleExecute = async () => {
    const result = await execute(
      "agent_jermaine_super_action",
      "Create a customer followup automation workflow",
      {
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
          workflow_name: "Customer Followup Automation",
          target_platform: "Email",
          frequency: "Daily",
          description: "Automated email followups for new customers"
        }
      }
    );

    console.log("Workflow Created:", result.workflow_action);
    console.log("Yearly Savings:", result.savings?.yearly_savings);
  };

  return (
    <div className="p-6">
      <button
        onClick={handleExecute}
        disabled={loading}
        className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
      >
        {loading ? "Creating..." : "Create Workflow"}
      </button>

      {error && <p className="text-red-600 mt-2">Error: {error}</p>}

      {response && (
        <div className="mt-4 space-y-4">
          <div className="p-4 bg-white border rounded">
            <p className="font-medium">{response.reply}</p>
          </div>

          {response.workflow_action && (
            <div className="p-4 bg-green-50 border border-green-200 rounded">
              <p className="text-sm text-green-600">Workflow ID:</p>
              <code className="text-xs">{response.workflow_action}</code>
            </div>
          )}

          {response.savings && (
            <div className="p-4 bg-yellow-50 border border-yellow-200 rounded">
              <h3 className="font-semibold mb-2">💰 ROI Savings</h3>
              <div className="space-y-1 text-sm">
                <p>Weekly: ${response.savings.weekly_savings.toFixed(2)}</p>
                <p>Monthly: ${response.savings.monthly_savings.toFixed(2)}</p>
                <p className="font-bold text-green-600">
                  Yearly: ${response.savings.yearly_savings.toFixed(2)}
                </p>
                <p>Hours Saved/Week: {response.savings.hours_saved_per_week.toFixed(2)}</p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ============================================================
// ALTERNATIVE: Direct API call without hook
// ============================================================

import { sendChat } from "@/lib/api";

async function executeWithoutHook() {
  const response = await sendChat({
    agentId: "agent_jermaine_super_action",
    message: "Create customer followup automation",
    mode: "execute",
    context: {
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
        workflow_name: "Customer Followup Automation",
        target_platform: "Email",
        frequency: "Daily"
      }
    }
  });

  return response;
}

// ============================================================
// USAGE EXAMPLES
// ============================================================

// Example 1: Button click handler
export function QuickExecuteButton() {
  const { execute, loading } = useChat();

  return (
    <button
      onClick={() =>
        execute("agent_jermaine_super_action", "Create automation", {
          calculator_inputs: {
            tasks_per_week: 200,
            time_per_task_minutes: 10,
            hourly_wage: 25,
            automation_percent: 0.7,
            error_rate: 0.1,
            cost_per_error: 15,
            value_per_accelerated_task: 0
          }
        })
      }
      disabled={loading}
    >
      Execute
    </button>
  );
}

// Example 2: Form submission
export function WorkflowForm() {
  const { execute, loading, response } = useChat();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);

    await execute(
      "agent_jermaine_super_action",
      "Create workflow based on form inputs",
      {
        calculator_inputs: {
          tasks_per_week: Number(formData.get("tasks_per_week")),
          time_per_task_minutes: Number(formData.get("time_per_task")),
          hourly_wage: Number(formData.get("hourly_wage")),
          automation_percent: Number(formData.get("automation_percent")) / 100,
          error_rate: 0.1,
          cost_per_error: 15,
          value_per_accelerated_task: 0
        },
        workflow_inputs: {
          workflow_name: formData.get("workflow_name"),
          target_platform: formData.get("platform"),
          frequency: formData.get("frequency")
        }
      }
    );
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="workflow_name" placeholder="Workflow Name" required />
      <input name="tasks_per_week" type="number" placeholder="Tasks/Week" required />
      <input name="time_per_task" type="number" placeholder="Minutes/Task" required />
      <input name="hourly_wage" type="number" placeholder="Hourly Wage ($)" required />
      <input name="automation_percent" type="number" placeholder="Automation %" required />
      <input name="platform" placeholder="Platform" required />
      <input name="frequency" placeholder="Frequency" required />
      <button type="submit" disabled={loading}>
        {loading ? "Creating..." : "Create Workflow"}
      </button>
      {response && <p>Created: {response.workflow_action}</p>}
    </form>
  );
}

// Example 3: Async function with error handling
export async function createWorkflowAsync() {
  try {
    const response = await sendChat({
      agentId: "agent_jermaine_super_action",
      message: "Create customer followup automation",
      mode: "execute",
      context: {
        calculator_inputs: {
          tasks_per_week: 200,
          time_per_task_minutes: 10,
          hourly_wage: 25,
          automation_percent: 0.7,
          error_rate: 0.1,
          cost_per_error: 15,
          value_per_accelerated_task: 0
        }
      }
    });

    if (response.workflow_action) {
      console.log("✅ Workflow created:", response.workflow_action);
      console.log("💰 Yearly savings:", response.savings?.yearly_savings);
      return response.workflow_action;
    }
  } catch (error) {
    console.error("❌ Failed to create workflow:", error);
    throw error;
  }
}
