import { Engine } from '../models';
import { fetchAPI } from './client';

export async function fetchEngines(): Promise<Engine[]> {
  return fetchAPI<Engine[]>('/api/direct/intelligence-core');
}

export async function fetchEngine(id: string): Promise<Engine> {
  return fetchAPI<Engine>(`/api/direct/intelligence-core/${id}`);
}

export async function fetchEngineConnections(engineId: string): Promise<string[]> {
  return fetchAPI<string[]>(`/api/mapping/engine-to-capsules/${engineId}`);
}
