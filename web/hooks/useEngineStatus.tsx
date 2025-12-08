'use client';

import { useEffect, useState } from 'react';

interface EngineStatusData {
  engine: string;
  status: 'operational' | 'degraded' | 'down';
  uptime?: string;
  lastUpdate?: string;
}

interface EngineStatuses {
  [key: string]: EngineStatusData;
}

export function useEngineStatus() {
  const [statuses, setStatuses] = useState<EngineStatuses>({});
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let evtSource: EventSource | null = null;

    try {
      evtSource = new EventSource('/api/engines/stream');

      evtSource.onopen = () => {
        setIsConnected(true);
        setError(null);
        console.log('🔥 Connected to engine status stream');
      };

      evtSource.onmessage = (e) => {
        try {
          const data: EngineStatusData = JSON.parse(e.data);
          setStatuses((prev) => ({
            ...prev,
            [data.engine]: {
              ...data,
              lastUpdate: new Date().toISOString(),
            },
          }));
        } catch (err) {
          console.error('Failed to parse engine status:', err);
        }
      };

      evtSource.onerror = (err) => {
        console.error('Engine status stream error:', err);
        setIsConnected(false);
        setError('Connection lost. Reconnecting...');
        evtSource?.close();
      };
    } catch (err) {
      console.error('Failed to create EventSource:', err);
      setError('Failed to connect to status stream');
    }

    return () => {
      if (evtSource) {
        evtSource.close();
        setIsConnected(false);
        console.log('🔌 Disconnected from engine status stream');
      }
    };
  }, []);

  return { statuses, isConnected, error };
}
