// Intelligence Core API Client
// Fetches intelligence engine data from the Flask backend

import { IntelligenceEngine } from "@/types/intelligenceCore"

const API_BASE = process.env.NEXT_PUBLIC_API_URL

export async function fetchIntelligenceCore(): Promise<IntelligenceEngine[]> {
  const res = await fetch(`${API_BASE}/api/intelligence-core`, { cache: "no-store" })
  if (!res.ok) return []
  return res.json()
}

export async function fetchActiveEngines(): Promise<IntelligenceEngine[]> {
  const res = await fetch(`${API_BASE}/api/intelligence-core/active`, { cache: "no-store" })
  if (!res.ok) return []
  return res.json()
}
