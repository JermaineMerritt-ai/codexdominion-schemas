// TypeScript interfaces for Codex Dominion data models

export interface Capsule {
  id: string;
  name: string;
  description: string;
  realm: string;
  status: 'active' | 'inactive' | 'development';
  modules: Module[];
  engines: string[];
  metadata?: {
    created?: string;
    updated?: string;
    version?: string;
  };
}

export interface Module {
  name: string;
  type: string;
  status: 'enabled' | 'disabled';
  description?: string;
}

export interface Engine {
  id: string;
  name: string;
  description: string;
  status: 'operational' | 'degraded' | 'offline';
  capabilities: string[];
  connected_capsules: string[];
  metrics?: EngineMetrics;
}

export interface EngineMetrics {
  uptime: string;
  requests: string;
  avg_latency: string;
  cache_hits: string;
  status: 'optimal' | 'good' | 'degraded';
}

export interface Realm {
  id: string;
  name: string;
  icon: string;
  capsule_count: number;
}

export interface Industry {
  id: string;
  name: string;
  icon: string;
  color: string;
  description: string;
  key_markets: string[];
  capsules: string[];
  revenue_potential: string;
  maturity: string;
  mvp_status: string;
  mvp_progress: number;
  capsule_dependencies: string[];
  engine_dependencies: string[];
  features_ready: number;
  features_total: number;
  api_health: string;
  platform_features?: PlatformFeature[];
}

export interface PlatformFeature {
  name: string;
  icon: string;
  status: string;
}

export interface HeatmapItem {
  industry: string;
  readiness: number;
  capsules: number;
  status: 'excellent' | 'good' | 'fair' | 'needs-attention';
}

export interface EngineLog {
  time: string;
  engine: string;
  action: string;
  status: 'success' | 'warning' | 'error';
}

export interface PlatformMetrics {
  uptime: string;
  response_time: string;
  requests_per_min: string;
  active_users: string;
  cpu_usage: string;
  memory_usage: string;
}

export interface Pipeline {
  name: string;
  status: 'operational' | 'degraded' | 'failed';
  last_run: string;
  throughput: string;
}

export interface ApiCall {
  endpoint: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  calls: string;
  avg_response: string;
  status: 'healthy' | 'warning' | 'error';
}

export interface ErrorLog {
  time: string;
  level: 'info' | 'warning' | 'error';
  source: string;
  message: string;
  resolved: boolean;
}

export interface CapsuleLoadEvent {
  time: string;
  capsule: string;
  action: string;
  load_time: string;
  status: 'success' | 'warning' | 'error';
}
