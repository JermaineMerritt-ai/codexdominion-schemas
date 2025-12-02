export interface Custodian {
  name: string;
  focus: "finance" | "security" | "innovation" | "community";
  responsibilities: string[];
}

export const custodians: Custodian[] = [
  { name: "Finance Custodian", focus: "finance", responsibilities: ["track money flows"] },
  { name: "Security Custodian", focus: "security", responsibilities: ["protect against cyber threats"] },
  { name: "Innovation Custodian", focus: "innovation", responsibilities: ["research new protocols"] },
  { name: "Community Custodian", focus: "community", responsibilities: ["engage councils and heirs"] },
];
