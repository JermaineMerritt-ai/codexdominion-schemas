import { useState, useEffect } from 'react';
import Head from 'next/head';

interface Product {
  id: string;
  name: string;
  price: number;
  description: string;
}

export default function CommerceHome() {
  const [products, setProducts] = useState<Product[]>([]);
  const [cart, setCart] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await fetch('/api/products');
      const data = await response.json();
      setProducts(data.products);
    } catch (error) {
      console.error('Failed to fetch products:', error);
    } finally {
      setLoading(false);
    }
  };

  const addToCart = (productId: string) => {
    setCart(prev => [...prev, productId]);
  };

  const checkout = async () => {
    try {
      const response = await fetch('/api/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ items: cart })
      });
      const data = await response.json();
      alert(`Checkout successful! Order ID: ${data.orderId}`);
      setCart([]);
    } catch (error) {
      console.error('Checkout failed:', error);
      alert('Checkout failed. Please try again.');
    }
  };

  return (
    <>
      <Head>
        <title>E-Commerce Platform - Codex Dominion</title>
      </Head>
      <div style={{
        minHeight: '100vh',
        backgroundColor: '#0f172a',
        color: '#f8fafc',
        fontFamily: 'system-ui, -apple-system, sans-serif'
      }}>
        <header style={{
          padding: '1rem 2rem',
          borderBottom: '1px solid #334155',
          backgroundColor: '#1e293b',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <div>
            <h1 style={{ margin: 0, fontSize: '1.5rem' }}>
              🛒 E-Commerce Platform
            </h1>
            <p style={{ margin: '0.25rem 0 0 0', color: '#94a3b8', fontSize: '0.875rem' }}>
              Sovereign Commerce Service
            </p>
          </div>
          <div style={{ fontSize: '1.25rem' }}>
            Cart: {cart.length} items
            {cart.length > 0 && (
              <button
                onClick={checkout}
                style={{
                  marginLeft: '1rem',
                  padding: '0.5rem 1rem',
                  backgroundColor: '#10b981',
                  color: 'white',
                  border: 'none',
                  borderRadius: '0.375rem',
                  cursor: 'pointer',
                  fontWeight: 600
                }}
              >
                Checkout
              </button>
            )}
          </div>
        </header>

        <main style={{ padding: '2rem' }}>
          {loading ? (
            <div style={{ textAlign: 'center', padding: '4rem', color: '#64748b' }}>
              Loading products...
            </div>
          ) : (
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
              gap: '1.5rem'
            }}>
              {products.map(product => (
                <div
                  key={product.id}
                  style={{
                    backgroundColor: '#1e293b',
                    padding: '1.5rem',
                    borderRadius: '0.5rem',
                    border: '1px solid #334155'
                  }}
                >
                  <h3 style={{ margin: '0 0 0.5rem 0' }}>{product.name}</h3>
                  <p style={{ color: '#94a3b8', margin: '0 0 1rem 0', fontSize: '0.875rem' }}>
                    {product.description}
                  </p>
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                  }}>
                    <span style={{ fontSize: '1.25rem', fontWeight: 600, color: '#10b981' }}>
                      ${product.price.toFixed(2)}
                    </span>
                    <button
                      onClick={() => addToCart(product.id)}
                      style={{
                        padding: '0.5rem 1rem',
                        backgroundColor: '#3b82f6',
                        color: 'white',
                        border: 'none',
                        borderRadius: '0.375rem',
                        cursor: 'pointer',
                        fontSize: '0.875rem',
                        fontWeight: 600
                      }}
                    >
                      Add to Cart
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </main>
      </div>
    </>
  );
}
