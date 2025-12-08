'use client';

import { useEffect, useState, useRef } from 'react';
import { getUnifiedEventManager } from '@/lib/events/unified-event-manager';

interface ChatMessage {
  user: string;
  role: 'sovereign' | 'council' | 'heir' | 'observer' | 'custodian';
  message: string;
  timestamp: string;
}

interface BroadcastChatProps {
  userName?: string;
  userRole?: 'sovereign' | 'council' | 'heir' | 'observer' | 'custodian';
  wsUrl?: string;
}

export default function BroadcastChat({
  userName = 'Jermaine',
  userRole = 'custodian',
  wsUrl = 'wss://codexdominion.app/broadcast/chat',
}: BroadcastChatProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    connectWebSocket();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  useEffect(() => {
    // Auto-scroll to bottom when new messages arrive
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const connectWebSocket = () => {
    try {
      const ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        console.log('✅ Ceremonial chat connected');
        setIsConnected(true);
        setError(null);

        // Send join message
        ws.send(
          JSON.stringify({
            type: 'join',
            user: userName,
            role: userRole,
            timestamp: new Date().toISOString(),
          })
        );
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);

          if (data.type === 'message' || data.message) {
            setMessages((prev) => [
              ...prev,
              {
                user: data.user,
                role: data.role,
                message: data.message,
                timestamp: data.timestamp || new Date().toISOString(),
              },
            ]);
          } else if (data.type === 'history') {
            // Server sent message history
            setMessages(data.messages || []);
          }
        } catch (err) {
          console.error('Failed to parse chat message:', err);
        }
      };

      ws.onerror = (event) => {
        console.error('WebSocket error:', event);
        setError('Connection error');
        setIsConnected(false);
      };

      ws.onclose = () => {
        console.log('🔌 Ceremonial chat disconnected');
        setIsConnected(false);

        // Attempt reconnect after 3 seconds
        reconnectTimeoutRef.current = setTimeout(() => {
          console.log('🔄 Attempting to reconnect chat...');
          connectWebSocket();
        }, 3000);
      };

      wsRef.current = ws;
    } catch (err) {
      console.error('Failed to connect to chat:', err);
      setError('Failed to connect');
      setIsConnected(false);
    }
  };

  const sendMessage = () => {
    if (!input.trim() || !wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      return;
    }

    const message = {
      type: 'message',
      user: userName,
      role: userRole,
      message: input.trim(),
      timestamp: new Date().toISOString(),
    };

    try {
      wsRef.current.send(JSON.stringify(message));

      // Also log to unified event manager
      const eventManager = getUnifiedEventManager();
      eventManager.addEvent({
        type: 'chat',
        user: userName,
        role: userRole,
        content: input.trim(),
      });

      setInput('');
    } catch (err) {
      console.error('Failed to send message:', err);
      setError('Failed to send message');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const getRoleBadgeColor = (role: string) => {
    switch (role) {
      case 'sovereign':
        return 'bg-[#FFD700] text-black';
      case 'council':
        return 'bg-blue-600 text-white';
      case 'heir':
        return 'bg-purple-600 text-white';
      case 'custodian':
        return 'bg-green-600 text-white';
      case 'observer':
        return 'bg-gray-600 text-white';
      default:
        return 'bg-gray-500 text-white';
    }
  };

  const getRoleIcon = (role: string) => {
    switch (role) {
      case 'sovereign':
        return '👑';
      case 'council':
        return '🎓';
      case 'heir':
        return '🌟';
      case 'custodian':
        return '🔑';
      case 'observer':
        return '👁️';
      default:
        return '💬';
    }
  };

  return (
    <div className="bg-[#1A1F3C] p-4 rounded-lg border-2 border-[#FFD700] h-96 flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-xl font-bold text-[#FFD700] flex items-center gap-2">
          💬 Ceremonial Chat
        </h2>
        <div className="flex items-center gap-2">
          {isConnected ? (
            <span className="text-xs text-green-400 flex items-center gap-1">
              <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
              Connected
            </span>
          ) : (
            <span className="text-xs text-red-400 flex items-center gap-1">
              <span className="w-2 h-2 bg-red-400 rounded-full"></span>
              Disconnected
            </span>
          )}
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-900/30 border border-red-500 rounded p-2 mb-2 text-sm text-red-400">
          ⚠️ {error}
        </div>
      )}

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto space-y-3 mb-3 custom-scrollbar">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 py-8">
            <p className="text-2xl mb-2">💬</p>
            <p className="text-sm">No messages yet. Start the conversation!</p>
          </div>
        ) : (
          messages.map((m, idx) => (
            <div key={idx} className="bg-[#0A0F29] rounded p-3 border border-[#FFD700]/20">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-lg">{getRoleIcon(m.role)}</span>
                <span className="font-bold text-white">{m.user}</span>
                <span
                  className={`px-2 py-0.5 rounded text-xs font-medium ${getRoleBadgeColor(
                    m.role
                  )}`}
                >
                  {m.role}
                </span>
                <span className="text-xs text-gray-500 ml-auto">
                  {new Date(m.timestamp).toLocaleTimeString()}
                </span>
              </div>
              <p className="text-white text-sm leading-relaxed">{m.message}</p>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Add reflection..."
          disabled={!isConnected}
          className="flex-1 px-3 py-2 rounded bg-[#0A0F29] text-white border border-[#FFD700]/30 focus:border-[#FFD700] focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed"
        />
        <button
          onClick={sendMessage}
          disabled={!isConnected || !input.trim()}
          className="px-4 py-2 bg-[#FFD700] text-black rounded font-bold hover:bg-[#FFC700] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Send
        </button>
      </div>

      {/* Participant Info */}
      <div className="mt-2 text-xs text-gray-500 flex items-center gap-2">
        <span>Participating as:</span>
        <span className="font-bold text-[#FFD700]">
          {getRoleIcon(userRole)} {userName}
        </span>
      </div>

      <style>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: #0A0F29;
          border-radius: 3px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #FFD700;
          border-radius: 3px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #FFA500;
        }
      `}</style>
    </div>
  );
}
