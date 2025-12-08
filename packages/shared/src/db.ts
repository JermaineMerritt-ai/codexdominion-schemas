export const db = {
  prompts: table('prompts'),
  approvals: table('approvals'),
  finance_events: table('finance_events'),
  acts: table('acts'),
  seals: table('seals'),
  users: table('users'),
  roles: table('roles'),

  // mock helpers for example; replace with real ORM (Prisma/Drizzle)
};

function table(name: string) {
  return {
    insert: async (row: any) => ({ id: cryptoId(), ...row }),
    get: async (id: string) => ({ id, title: 'Example', status: 'in_review' }),
    update: async (id: string, patch: any) => ({ id, ...patch }),
    findBy: async (_: any) => null,
    groupBy: async (key: string) => ({ [key]: [] }),
    aggregate: async (_: any) => [],
    mrr: async () => ({ value: 0 })
  };
}
const cryptoId = () => Math.random().toString(36).slice(2);
