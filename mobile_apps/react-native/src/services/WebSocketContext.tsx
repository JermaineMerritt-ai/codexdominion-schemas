import React, { createContext, useContext, useEffect, useState } from 'react';

const WS_URL = 'ws://localhost:8765';

interface WebSocketContextType {
  connected: boolean;
  sendMessage: (roomId: string, content: string) => void;
  messages: any[];
}

const WebSocketContext = createContext<WebSocketContextType | undefined>(undefined);

export const WebSocketProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [connected, setConnected] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);

  useEffect(() => {
    const websocket = new WebSocket(WS_URL);

    websocket.onopen = () => {
      console.log('WebSocket connected');
      setConnected(true);

      // Authenticate
      websocket.send(JSON.stringify({
        type: 'auth',
        username: 'mobile_user',
        display_name: 'Mobile User',
      }));
    };

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages((prev) => [...prev, data]);
    };

    websocket.onclose = () => {
      console.log('WebSocket disconnected');
      setConnected(false);
    };

    setWs(websocket);

    return () => {
      websocket.close();
    };
  }, []);

  const sendMessage = (roomId: string, content: string) => {
    if (ws && connected) {
      ws.send(JSON.stringify({
        type: 'send_message',
        room_id: roomId,
        content,
      }));
    }
  };

  return (
    <WebSocketContext.Provider value={{ connected, sendMessage, messages }}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocket = () => {
  const context = useContext(WebSocketContext);
  if (!context) {
    throw new Error('useWebSocket must be used within WebSocketProvider');
  }
  return context;
};
