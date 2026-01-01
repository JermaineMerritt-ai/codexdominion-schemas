/**
 * React Hook for Chat API
 * 
 * Provides easy-to-use interface for chat and workflow execution
 */

import { useState, useCallback } from "react";
import { sendChat, ChatResponse, ChatOptions } from "./chat";

export interface UseChatState {
  loading: boolean;
  error: string | null;
  response: ChatResponse | null;
}

export interface UseChatActions {
  sendMessage: (options: ChatOptions) => Promise<ChatResponse>;
  chat: (agentId: string, message: string) => Promise<ChatResponse>;
  execute: (
    agentId: string,
    message: string,
    context: ChatOptions["context"]
  ) => Promise<ChatResponse>;
  reset: () => void;
}

/**
 * Hook for interacting with the unified chat API
 * 
 * @example
 * ```tsx
 * function ChatComponent() {
 *   const { loading, error, response, chat, execute } = useChat();
 * 
 *   const handleChat = async () => {
 *     const res = await chat("agent_jermaine_super_action", "Hello!");
 *     console.log(res.reply);
 *   };
 * 
 *   const handleExecute = async () => {
 *     const res = await execute(
 *       "agent_jermaine_super_action",
 *       "Create automation",
 *       {
 *         calculator_inputs: {
 *           tasks_per_week: 200,
 *           time_per_task_minutes: 10,
 *           hourly_wage: 25,
 *           automation_percent: 0.7
 *         }
 *       }
 *     );
 *     console.log(res.savings?.yearly_savings);
 *     console.log(res.workflow_action);
 *   };
 * 
 *   return (
 *     <div>
 *       <button onClick={handleChat} disabled={loading}>
 *         Chat
 *       </button>
 *       <button onClick={handleExecute} disabled={loading}>
 *         Execute Workflow
 *       </button>
 *       {loading && <p>Loading...</p>}
 *       {error && <p>Error: {error}</p>}
 *       {response && <p>Reply: {response.reply}</p>}
 *     </div>
 *   );
 * }
 * ```
 */
export function useChat(): UseChatState & UseChatActions {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [response, setResponse] = useState<ChatResponse | null>(null);

  const sendMessage = useCallback(async (options: ChatOptions) => {
    setLoading(true);
    setError(null);

    try {
      const res = await sendChat(options);
      setResponse(res);
      return res;
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : "Unknown error";
      setError(errorMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const chat = useCallback(
    async (agentId: string, message: string) => {
      return sendMessage({ agentId, message, mode: "chat" });
    },
    [sendMessage]
  );

  const execute = useCallback(
    async (
      agentId: string,
      message: string,
      context: ChatOptions["context"]
    ) => {
      return sendMessage({ agentId, message, mode: "execute", context });
    },
    [sendMessage]
  );

  const reset = useCallback(() => {
    setLoading(false);
    setError(null);
    setResponse(null);
  }, []);

  return {
    loading,
    error,
    response,
    sendMessage,
    chat,
    execute,
    reset
  };
}
