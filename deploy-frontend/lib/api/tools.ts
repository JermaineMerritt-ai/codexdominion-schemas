/**
 * Tools API
 */

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:5000";

export interface Tool {
  id: string;
  name: string;
  description: string;
  category?: string;
  capabilities?: string[];
  status?: string;
  version?: string;
}

export async function fetchTools(): Promise<Tool[]> {
  const res = await fetch(`${API_BASE}/api/tools`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch tools: ${res.status}`);
  }

  const data = await res.json();
  return data.tools || [];
}

export async function fetchToolById(id: string): Promise<Tool | null> {
  const res = await fetch(`${API_BASE}/api/tools/${id}`, {
    cache: "no-store",
  });

  if (!res.ok) {
    return null;
  }

  return res.json();
}
