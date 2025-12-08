import { query } from '../db';
import { FastifyRequest, FastifyReply } from 'fastify';

interface User {
  id: string;
  email: string;
  display_name: string;
  role: string;
  role_id: number;
}

export const identity = {
  async getOrCreateUser(email: string): Promise<User> {
    // Try to find existing user
    const existingUser = await query(
      `SELECT u.id, u.email, u.display_name, r.name as role, u.role_id
       FROM users u
       JOIN roles r ON u.role_id = r.id
       WHERE u.email = $1`,
      [email]
    );

    if (existingUser.rows.length > 0) {
      return existingUser.rows[0];
    }

    // Create new user with guest role
    const newUser = await query(
      `INSERT INTO users (email, display_name, role_id)
       VALUES ($1, $2, (SELECT id FROM roles WHERE name = 'guest'))
       RETURNING id, email, display_name, role_id`,
      [email, email.split('@')[0]]
    );

    const user = newUser.rows[0];
    user.role = 'guest';
    return user;
  },

  requireRole(...allowedRoles: string[]) {
    return async (request: FastifyRequest, reply: FastifyReply) => {
      try {
        await request.jwtVerify();
        const payload = request.user as any;

        // Get user role from database
        const result = await query(
          `SELECT r.name as role
           FROM users u
           JOIN roles r ON u.role_id = r.id
           WHERE u.id = $1`,
          [payload.sub]
        );

        if (result.rows.length === 0) {
          return reply.code(401).send({ error: 'User not found' });
        }

        const userRole = result.rows[0].role;

        if (!allowedRoles.includes(userRole)) {
          return reply.code(403).send({ error: 'Insufficient permissions' });
        }

        // Attach user info to request
        (request as any).user = { ...payload, role: userRole };
      } catch (err) {
        return reply.code(401).send({ error: 'Invalid token' });
      }
    };
  }
};
