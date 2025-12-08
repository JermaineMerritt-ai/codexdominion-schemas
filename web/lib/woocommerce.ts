// WooCommerce API stub - package not installed
// import WooCommerceRestApi from '@woocommerce/woocommerce-rest-api';

// const api = new WooCommerceRestApi({
//   url: process.env.NEXT_PUBLIC_WP_URL || 'http://localhost:8080',
//   consumerKey: process.env.WC_CONSUMER_KEY || '',
//   consumerSecret: process.env.WC_CONSUMER_SECRET || '',
//   version: 'wc/v3',
//   queryStringAuth: true
// });

export interface Product {
  id: number;
  name: string;
  slug: string;
  permalink: string;
  type: string;
  status: string;
  featured: boolean;
  description: string;
  short_description: string;
  sku: string;
  price: string;
  regular_price: string;
  sale_price: string;
  on_sale: boolean;
  purchasable: boolean;
  virtual: boolean;
  downloadable: boolean;
  categories: Array<{ id: number; name: string; slug: string }>;
  tags: Array<{ id: number; name: string; slug: string }>;
  images: Array<{ id: number; src: string; alt: string }>;
  attributes: any[];
  meta_data: any[];
}

export interface ProductCategory {
  id: number;
  name: string;
  slug: string;
  description: string;
  count: number;
  image?: { src: string; alt: string };
}

export interface Subscription {
  id: number;
  name: string;
  price: string;
  billing_period: string;
  billing_interval: number;
  signup_fee?: string;
  trial_length?: number;
  trial_period?: string;
}

// Product fetching
export async function getProducts(params: any = {}) {
  // TODO: Implement when @woocommerce/woocommerce-rest-api is installed
  return [];
}

export async function getProduct(id: number | string) {
  // TODO: Implement when @woocommerce/woocommerce-rest-api is installed
  return null;
}

export async function getProductBySlug(slug: string) {
  // TODO: Implement when @woocommerce/woocommerce-rest-api is installed
  return null;
}

// Category fetching
export async function getCategories(params: any = {}) {
  // TODO: Implement when @woocommerce/woocommerce-rest-api is installed
  return [];
}

export async function getCategory(id: number) {
  // TODO: Implement when @woocommerce/woocommerce-rest-api is installed
  return null;
}

// Bundle products
export async function getBundles() {
  // TODO: Implement when @woocommerce/woocommerce-rest-api is installed
  return [];
}

// Subscription products
export async function getSubscriptions() {
  // TODO: Implement when @woocommerce/woocommerce-rest-api is installed
  return [];
}

// Featured products
export async function getFeaturedProducts(limit: number = 8) {
  // TODO: Implement when @woocommerce/woocommerce-rest-api is installed
  return [];
}

// Products by tag
export async function getProductsByTag(tag: string, limit: number = 12) {
  // TODO: Implement when @woocommerce/woocommerce-rest-api is installed
  return [];
}

// Seasonal products
export async function getSeasonalProducts(season: string) {
  return getProductsByTag(`seasonal-${season}`);
}

// Niche-specific products
export async function getNicheProducts(niche: 'homeschool' | 'wedding' | 'kids' | 'memory-verse') {
  return getProductsByTag(niche);
}
