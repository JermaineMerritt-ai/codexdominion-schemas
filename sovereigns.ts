export interface Sovereign {
  name: string;
  domain: string;
  responsibilities: string[];
}

export const sovereigns: Sovereign[] = [
  { name: "Voicekeeper", domain: "chatbot", responsibilities: ["customer support routing"] },
  { name: "System Flamekeeper", domain: "healing", responsibilities: ["error detection", "auto-fix"] },
  { name: "Archive Sovereign", domain: "compliance", responsibilities: ["record keeping", "audit logs"] },
  { name: "Commerce Sovereign", domain: "commerce", responsibilities: ["transaction processing", "order management"] },
  { name: "Observatory Sovereign", domain: "observatory", responsibilities: ["system monitoring", "metrics tracking"] },
];
