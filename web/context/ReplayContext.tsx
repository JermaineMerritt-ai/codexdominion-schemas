'use client';

import { createContext, useContext, useState, ReactNode } from 'react';

interface ReplayCapsule {
  id: string;
  timestamp: string;
  engine: string;
  status: string;
  event?: string;
  metadata?: Record<string, any>;
}

interface ReplayContextType {
  index: number;
  setIndex: (index: number | ((prev: number) => number)) => void;
  capsules: ReplayCapsule[];
  setCapsules: (capsules: ReplayCapsule[]) => void;
  isPlaying: boolean;
  setIsPlaying: (playing: boolean) => void;
  mode: 'daily' | 'seasonal' | 'epochal' | 'millennial';
  setMode: (mode: 'daily' | 'seasonal' | 'epochal' | 'millennial') => void;
}

const ReplayContext = createContext<ReplayContextType | null>(null);

export function ReplayProvider({ children }: { children: ReactNode }) {
  const [index, setIndex] = useState(0);
  const [capsules, setCapsules] = useState<ReplayCapsule[]>([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const [mode, setMode] = useState<'daily' | 'seasonal' | 'epochal' | 'millennial'>('daily');

  return (
    <ReplayContext.Provider
      value={{
        index,
        setIndex,
        capsules,
        setCapsules,
        isPlaying,
        setIsPlaying,
        mode,
        setMode
      }}
    >
      {children}
    </ReplayContext.Provider>
  );
}

export function useReplay() {
  const context = useContext(ReplayContext);
  if (!context) {
    throw new Error('useReplay must be used within a ReplayProvider');
  }
  return context;
}
