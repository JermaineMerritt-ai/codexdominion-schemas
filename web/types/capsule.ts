// types/capsule.ts
export type CapsuleRealm =
  | "foundation"
  | "economic"
  | "knowledge"
  | "community"
  | "automation"
  | "media"

export interface Capsule {
  id: string
  realm: CapsuleRealm
  realm_index: number
  capsule_index: number
  name: string
  description: string
  status: "planned" | "active" | "in_progress" | "deprecated"
  tags: string[]
  primary_systems: string[]
  primary_use_cases: string[]
  linked_modules: string[]
  lifecycle?: "alpha" | "beta" | "stable" | "mature" | "sunset"
  overlays?: {
    stewardship: boolean
    wellbeing: boolean
    planetary: boolean
    intergenerational: boolean
  }
  owner_role?: string
  owner_entity?: string
}
