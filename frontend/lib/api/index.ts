/**
 * Chat API Module
 * 
 * Unified interface for AI agent chat and workflow execution
 */

export { sendChat, chatWithAgent, executeWorkflow } from "./chat";
export type { ChatResponse, ChatOptions } from "./chat";
export { useChat } from "./useChat";
export type { UseChatState, UseChatActions } from "./useChat";

// Export workflow API functions
export { 
  fetchWorkflowTypes, 
  fetchWorkflowMetrics,
  fetchWorkflowType,
  fetchWorkflows,
  fetchWorkflow
} from "./workflows";
export type { WorkflowType, WorkflowMetrics, WorkflowAction } from "./workflows";
