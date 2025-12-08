import Fastify from 'fastify';
import cors from '@fastify/cors';
import jwt from '@fastify/jwt';
import { config } from 'dotenv';
import { workflow } from './modules/workflow';
import { ledger } from './modules/ledger';
import { finance } from './modules/finance';
import { broadcast } from './modules/broadcast';
import { identity } from './modules/identity';

// Load environment variables
config();

const app = Fastify({ logger: true });

app.register(cors, { origin: true });
app.register(jwt, { secret: process.env.JWT_SECRET || 'change-me-in-production' });

// Auth
app.post('/auth/login', async (req, reply) => {
  const { email } = req.body as { email: string };
  const user = await identity.getOrCreateUser(email);
  const token = app.jwt.sign({ sub: user.id, role: user.role });
  reply.send({ token, user });
});

// Prompts
app.post('/prompts', {
  preValidation: [identity.requireRole('steward', 'council', 'sovereign')]
}, async (req, reply) => {
  const prompt = await workflow.createPrompt(req.body as any);
  reply.send(prompt);
});

app.get('/prompts/:id', async (req, reply) => {
  const { id } = req.params as { id: string };
  const prompt = await workflow.getPrompt(id);
  reply.send(prompt);
});

app.post('/prompts/:id/execute', {
  preValidation: [identity.requireRole('sovereign', 'council')]
}, async (req, reply) => {
  const { id } = req.params as { id: string };
  const result = await workflow.executePrompt(id);
  reply.send(result);
});

app.post('/prompts/:id/approve', {
  preValidation: [identity.requireRole('sovereign', 'council')]
}, async (req, reply) => {
  const { id } = req.params as { id: string };
  const res = await workflow.approvePrompt(id, (req as any).user);
  reply.send(res);
});

// Broadcast Capsule
app.post('/broadcast/dispatch', {
  preValidation: [identity.requireRole('sovereign', 'council')]
}, async (req, reply) => {
  const res = await broadcast.dispatchCapsule(req.body as any);
  reply.send(res);
});

// Finance telemetry
app.get('/finance/summary', {
  preValidation: [identity.requireRole('finance', 'sovereign')]
}, async (_req, reply) => {
  const summary = await finance.summary();
  reply.send(summary);
});

// Ledger
app.post('/ledger/acts', {
  preValidation: [identity.requireRole('steward', 'council', 'sovereign')]
}, async (req, reply) => {
  const act = await ledger.createAct(req.body as any);
  reply.send(act);
});

app.post('/ledger/acts/:id/seal', {
  preValidation: [identity.requireRole('sovereign', 'council')]
}, async (req, reply) => {
  const { id } = req.params as { id: string };
  const userId = ((req as any).user as any).sub;
  const seal = await ledger.sealAct(id, userId);
  reply.send(seal);
});

// Health check
app.get('/health', async (_req, reply) => {
  reply.send({ status: 'ok', timestamp: new Date().toISOString() });
});

const start = async () => {
  try {
    const port = parseInt(process.env.API_PORT || '4000', 10);
    await app.listen({ port, host: '0.0.0.0' });
    console.log(`🚀 API server running on http://localhost:${port}`);
  } catch (err) {
    app.log.error(err);
    process.exit(1);
  }
};

start();
