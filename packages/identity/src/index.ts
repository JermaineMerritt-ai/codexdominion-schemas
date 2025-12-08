import { query } from './db';
import type { FastifyRequest } from 'fastify';

interface User {
  id: string;
  email: string;
  display_name: string;
  role_id: number;
  created_at: Date;
  updated_at: Date;
}

interface Role {
  id: number;
  name: string;
  description: string | null;
}

const db = {
  users: {
    async findBy({ email }: { email: string }) {
      const result = await query(
        `SELECT * FROM users WHERE email = $1`,
        [email]
      );
      return result.rows[0] as User | undefined;
    },

    async insert(data: { email: string; display_name: string; role_id: number }) {
      const result = await query(
        `INSERT INTO users (email, display_name, role_id)
         VALUES ($1, $2, $3)
         RETURNING *`,
        [data.email, data.display_name, data.role_id]
      );
      return result.rows[0] as User;
    }
  },

  roles: {
    async findBy({ name }: { name: string }) {
      const result = await query(
        `SELECT * FROM roles WHERE name = $1`,
        [name]
      );
      return result.rows[0] as Role;
    },

    async get(id: number) {
      const result = await query(
        `SELECT * FROM roles WHERE id = $1`,
        [id]
      );
      return result.rows[0] as Role;
    }
  }
};

export const identity = {
  async getOrCreateUser(email: string) {
    let u = await db.users.findBy({ email });
    if (!u) {
      const role = await db.roles.findBy({ name: 'steward' });
      u = await db.users.insert({ email, display_name: email.split('@')[0], role_id: role.id });
    }
    return { id: u.id, email: u.email, role: await db.roles.get(u.role_id) };
  },

  requireRole(...allowed: string[]) {
    return async (req: FastifyRequest) => {
      const user = await (req as any).jwtVerify();
      const ok = allowed.includes(user.role.name) || user.role.name === 'sovereign';
      if (!ok) throw new Error('unauthorized');
      (req as any).user = user;
    };
  }
};
