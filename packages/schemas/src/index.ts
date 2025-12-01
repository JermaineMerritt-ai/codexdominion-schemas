/**
 * @codex-dominion/schemas - Custodian Schemas Library
 * Centralized data schemas and validation for the entire system
 */

import { z } from 'zod';

// User Schema
export const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1),
  role: z.enum(['admin', 'user', 'agent']),
  createdAt: z.date(),
  updatedAt: z.date()
});

export type User = z.infer<typeof UserSchema>;

// Product Schema
export const ProductSchema = z.object({
  id: z.string(),
  name: z.string().min(1),
  description: z.string(),
  price: z.number().positive(),
  category: z.string(),
  inStock: z.boolean(),
  createdAt: z.date()
});

export type Product = z.infer<typeof ProductSchema>;

// Order Schema
export const OrderSchema = z.object({
  id: z.string().uuid(),
  userId: z.string().uuid(),
  items: z.array(z.object({
    productId: z.string(),
    quantity: z.number().int().positive(),
    price: z.number().positive()
  })),
  total: z.number().positive(),
  status: z.enum(['pending', 'processing', 'completed', 'cancelled']),
  createdAt: z.date()
});

export type Order = z.infer<typeof OrderSchema>;

// Payment Schema
export const PaymentSchema = z.object({
  id: z.string().uuid(),
  orderId: z.string().uuid(),
  amount: z.number().positive(),
  method: z.enum(['credit_card', 'debit_card', 'paypal', 'crypto']),
  status: z.enum(['pending', 'completed', 'failed']),
  processedAt: z.date().optional()
});

export type Payment = z.infer<typeof PaymentSchema>;

// Config Schema
export const ConfigSchema = z.object({
  appName: z.string(),
  environment: z.enum(['development', 'staging', 'production']),
  apiUrl: z.string().url(),
  features: z.record(z.boolean()),
  limits: z.object({
    maxFileSize: z.number(),
    rateLimit: z.number(),
    maxConnections: z.number()
  })
});

export type Config = z.infer<typeof ConfigSchema>;

// Validator functions
export function validateUser(data: unknown): { valid: boolean; data?: User; error?: string } {
  try {
    const user = UserSchema.parse(data);
    return { valid: true, data: user };
  } catch (error) {
    return { valid: false, error: (error as Error).message };
  }
}

export function validateProduct(data: unknown): { valid: boolean; data?: Product; error?: string } {
  try {
    const product = ProductSchema.parse(data);
    return { valid: true, data: product };
  } catch (error) {
    return { valid: false, error: (error as Error).message };
  }
}

export function validateOrder(data: unknown): { valid: boolean; data?: Order; error?: string } {
  try {
    const order = OrderSchema.parse(data);
    return { valid: true, data: order };
  } catch (error) {
    return { valid: false, error: (error as Error).message };
  }
}

export function validatePayment(data: unknown): { valid: boolean; data?: Payment; error?: string } {
  try {
    const payment = PaymentSchema.parse(data);
    return { valid: true, data: payment };
  } catch (error) {
    return { valid: false, error: (error as Error).message };
  }
}

export function validateConfig(data: unknown): { valid: boolean; data?: Config; error?: string } {
  try {
    const config = ConfigSchema.parse(data);
    return { valid: true, data: config };
  } catch (error) {
    return { valid: false, error: (error as Error).message };
  }
}
