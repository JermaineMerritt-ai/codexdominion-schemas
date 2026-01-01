import { Capsule } from '../models';
import { fetchAPI } from './client';

export async function fetchCapsules(): Promise<Capsule[]> {
  return fetchAPI<Capsule[]>('/api/direct/capsules');
}

export async function fetchCapsule(id: string): Promise<Capsule> {
  return fetchAPI<Capsule>(`/api/direct/capsules/${id}`);
}

export async function fetchCapsulesByRealm(realm: string): Promise<Capsule[]> {
  return fetchAPI<Capsule[]>(`/api/capsules/realm/${realm}`);
}
