import { Capsule } from '@/types/capsule'

const API_BASE = process.env.NEXT_PUBLIC_API_URL

export async function fetchCapsules(): Promise<Capsule[]> {
  const res = await fetch(`${API_BASE}/api/capsules`, { cache: "no-store" })
  if (!res.ok) return []
  return res.json()
}
