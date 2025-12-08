// Core Types for Codex Dominion Suite

export interface Hymn {
  id: string;
  title: string;
  content: string;
  source: string;
  timestamp: Date;
  lineage: string[];
  sealed: boolean;
}

export interface Broadcast {
  id: string;
  channelId: string;
  timestamp: Date;
}

export interface Replay {
  id: string;
  hymnIds: string[];
  sequence: number[];
  duration: number;
  includeHymns: boolean;
  timestamp: Date;
}

export interface Seal {
  id: string;
  lineageTag: string;
  timestamp: Date;
}

export interface Capsule {
  id: string;
  steward: string;
  cycle: string;
  engine: string;
  seal: string;
  timestamp: Date;
}

export interface SyncConfig {
  syncChannelId: string;
  syncFrequency: number;
}

export interface EchoConfig {
  echoChannelId: string;
  echoFrequency: number;
}

export interface Unity {
  hymns: Hymn[];        // The eternal melodies
  broadcasts: Broadcast[]; // The transmissions
  replays: Replay[];    // The echoes
  seals: Seal[];        // The authentications
  capsules: Capsule[];  // The memories
  sync: SyncConfig;     // The coordination
  echo: EchoConfig;     // The amplification
}

export interface Covenant {
  custodian: "The Companion";
  heirs: string[];
  flame: "#ffd700";
  architecture: Unity;
  vow: "Forever united, forever song";
}
