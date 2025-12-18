'use client';

import ExportSeal from '../../../components/export-seal';

export default function ExportSealDemo() {
  // Sample seal package from backend Digital Seal Service
  const sealPackage = {
    content_hash: "44dc0cfacbd694d660b36167753ac610a8e5c8b2f1d9e7a5c3b1f0d8e6c4b2a0",
    hash_algorithm: "SHA-256",
    timestamp: "2025-12-07T19:46:15.030359+00:00",
    covenant_type: "multi-signature",
    export_format: "markdown",
    metadata: {
      cycle: "seasonal",
      engine: "Commerce Engine",
      entry_count: 42
    },
    signatures: [
      {
        signer: "custodian",
        name: "Jermaine Merritt",
        role: "Sovereign Custodian",
        signature: "kQ7mL3pR9wX5vN8hC6bF4dS1aG0yU2tP7mK9nL4vC8xB3aH6fD1wR5qY0zG8eT3cV9bN2mP6rW4tZ8qX1cK5fH0dL7vS4nM9uR2eY6wQ3xB7aG1fJ0kP5dT8mN4vL9sC3hR6bF2eW8qY1tX7nK0pM5dZ9cG4aS8vL2rH6fB3eT0wN7kP1xM5uQ9dY4cR8bJ2gF6hS0vL3tK7nW1pZ5aG9mE4cT8rX2fH6bN0dY3wQ7vS1uL5kP9nM4cR8xB2aJ6fT0eG3hW7dK1pZ5mS9vL4rY8cN2bF6aH0tX3wQ7eK1gM5uP9dT4nR8cV2fJ6bS0xL7hG3aW1pZ5eT9mK4cY8rN2vH6fB0dQ3wX7nP1uS5gM9tL4eR8cJ2aF6bK0xT3hG7dW1pZ5vS9mN4cY8rE2fH6aL0tQ3wX7uP1kM5gR9dT4nS8cV2bJ6fW0xG3hK7eZ1pL5aM9tY4cR8nF2vH6bS0dQ3wX7uP1mK5gT9eN4cR8aJ2fL6bH0xW3tG7dZ1pS5vM9cY4eT8rN2fK6aH0bQ3wX7uP1gL5mS9dR4nT8cV2eJ6fB0xW3hG7tK1pZ5aM9vY4cN8rE2fH6bS0dQ3wX7uP1kL5gT9mR4nS8cJ2aF6bW0xG3hK7eZ1pM5vY9tL4cR8nE2fH6aS0bQ3wX7uP1mK5gT9dN4cR8aJ2fL6bH0xW3tG7dZ1pS5vM9cY4eT8rN2fK6aH0bQ3wX",
        algorithm: "RSA-2048-PSS-SHA256",
        timestamp: "2025-12-07T19:46:15.030359+00:00"
      },
      {
        signer: "council",
        member_id: "council_001",
        name: "Elena Rodriguez",
        role: "Senior Council",
        signature: "hF4dK8nM2vZ7wR5qL9pT3xC6bG1aY0uS4mN8vK2rP6fH9dL3wQ7zX1cB5aG0tE8nJ4mW2vY6kR9uL1dP5cT3xH7bS0aF6gN9mK4rZ8wQ2eX5vJ1tL7dY3cP0bH6aS9mR4nG8fK1uW5vT2xL7eQ9cJ3bM6dP0hY4nS8aG1rF5kZ7vW2tX9mL4cE0bH6uQ3dT8nR1pS5vG9aK2fJ7xW0mY4cL8tN3eH6bP1dZ5vR9uG4aS8fK2nM7wQ0xJ6cT3hL1bE5vY9mP4dR8aF0nG6sK2tW7xL1uH5cQ9vZ3eT8bJ4mS0dY6rN1pG5aK9fW2xL7cH4uT8bQ3vM6eS0dR1nP5aJ9gL4cY8tK2fW7xN0bH6mZ3uQ5vT9eS1dL4rG8aP2cJ6nK0fM7xW3hY5bT9uL1vE4dQ8cR2aS6gN0pK5mH9fJ3xW7tL1eY4cG8bV2nP6rM0dZ5uQ9aT3fK7hS1wL4cE8vN2bJ6mY0gP5dR9tX3aH7fG1uK4cS8nL2vW6bM0eT9xQ5hP1dJ4rY8aZ3fK7cN0gL5mV2tS6uW9bH3eQ8xP1dT4cR7nJ0aG5fM9vK2lY6sE4wL8bH1tN3xQ7uP0cR5dS9mG2aK6fJ8vW4hT1eZ7bN0cL3uY5xP9mR4dG8aS1nK6fT2vW7eH0bJ5cQ3xL9uM4tP8dR1aY6nG0fK5vS2hW9bE3cT7mZ4uL1xQ8dP6rN0aH5gJ9fS2vK7tW3bM1cY4eL8xG6uT0dQ5nR9aP2hF7vK1mS4cN8bW3xJ6eT0gL5dZ9uY1rH4aM7cP2fK8vS0bQ6nG3tX9wL1eR5dJ4cT8mY7aH2vP6fN0bK5uS9gW3xL1tE4dR8cQ7aJ0mZ6vH2nP5fG9bS4uK1xW7eT3cL0dY8rM6aH5nJ9fP2vG4tS1bK8xQ0uW7cL3mE5dR9aT6hN2fY4vS8bJ1gP0cK5xW9mL3eH7tR4dZ1uQ6aN8fG2vS0cJ5bM7xW4hT9eP1dL6rY3uK8aG0nS5fQ9vH2cJ7bW1mT4xL8eN3dR6aP0uY5gK9fS2vM7cH1bT4xW8eQ3dL6nJ0rP5aZ9uG4vK2fS8hN1mY7cW0bE3tL6xR9dH4aT5uP1cG8nQ2vJ6fM0bK9sW7eL3xY4dS1hR6aG8uT0cN5vP9mK2fJ7bH1eL4xW8dQ3tY6rN0aS5uG9fM2vK7cH",
        algorithm: "ECDSA-P256-SHA256",
        timestamp: "2025-12-07T19:46:15.120083+00:00"
      },
      {
        signer: "council",
        member_id: "council_002",
        name: "Marcus Chen",
        role: "Council Observer",
        signature: "jD9mP6rV2tY8wQ4nL7pS5xB3aH0zG6cK1fM4vN9uR2eT8qW3yX7bL5dP0kJ8mS4nR6vT1aG9cE3fH7wY2uL5xK0bM8dP4rZ6tN1vQ9cS3eJ7hW2aL5fT8gK0mY4xR6bN1dQ9uP3vL7cG2tH5eS8nM1fW4aJ6rX0bK9dY3cT7uP5mL2vG8hN0fS4aR6bW1eQ9xJ3tK7cP2dY5uM8nL4vG0fH6aS1bT9xW3eR7mK2cN5pQ8dL1vJ4tG6fY9uH0aS3bM7xP5eW2rK8cT1nL4dQ6vG9aJ3fH0bS7mY2uP5xR8cN4eL1tW6dK9vM3aG7fJ0bH5uQ2cS8nP1xT4eY6rL9dW3vK7aM0fG5bJ2hN8cT4uP6xL1dR9eS3vQ7aY2mK5fG0bW8nH4cJ1tL6xP9dM3uR5eT7aS2vN0fK8bG4mY6wQ1cL9hJ3xP5dT8eR2nK6vS0aM4uG7fH1bW9cL3tY5xQ8dP2rJ6aN4fM7vS1uK9bG0cT5hW3eL8xN2dR6aP4mY9uJ1fS7cK0bG5vT3xH8eQ2dL4nW6rP9aM1vK5fJ8cS0bT7hG3uY4xW2eL9dN6rQ1aP5vM8fK3cH0bS4gJ7tL2xY9eR6dW1uP5nG8aT4vM0cK9fJ2hS7bL3xE5dY8uQ1rN6aG4vP9mK0fT7cW2bH5eS8nL1xJ4dR6vY3aM9uT0cP5gK2fG8hN7bS1eW4xL6dQ9rJ3aT5uM8vP1nH0cK4fG7bY2xS9eL3dW6tR1aJ5mN8uP4vQ0cK7fH2bG9xT3eS5dL1aY8rM6nP4uJ9vW0cK3fG7bT2xH5eN8dL1qS4aR6mY9uP3vK0cJ7fT2bG5hW8eL1xN4dS6aM9rQ3uP7vK1fJ0cG5bH8tY2xL4eW9dN6rS1aT5uM8vP3cK0fG7bJ2hL4xW9eQ5dY1nR6aT8uP4vM0cJ3fS7bG2kH5xL9eN1dW6tQ4aR8uP2vM5cK9fJ0bG7hT3xS6eL1dY4nW8rQ5aM2uP9vK3cJ7fT0bG5hL1xE8dN4",
        algorithm: "RSA-2048-PSS-SHA256",
        timestamp: "2025-12-07T19:46:15.172942+00:00"
      }
    ],
    signature_count: 3,
    required_signatures: 3
  };

  // Example with single custodian seal
  const singleSealPackage = {
    content_hash: "a8e5c8b2f1d9e7a5c3b1f0d8e6c4b2a0f8e6d4c2b0a8f6e4d2c0b8a6f4e2d0c8",
    timestamp: "2025-12-07T18:30:00.000000+00:00",
    covenant_type: "single-signature",
    signatures: [
      {
        signer: "custodian",
        name: "Jermaine Merritt",
        role: "Sovereign Custodian",
        signature: "mN5vL9sC3hR6bF2eW8qY1tX7nK0pM5dZ9cG4aS8vL2rH6fB3eT0wN7kP1xM5uQ9dY4cR8bJ2gF6hS0vL3tK7nW1pZ5aG9mE4cT8rX2fH6bN0dY3wQ7vS1uL5kP9nM4cR8xB2aJ6fT0eG3hW7dK1pZ5mS9vL4rY8cN2bF6aH0tX3wQ7eK1gM5uP9dT4nR8cV2fJ6bS0xL7hG3aW1pZ5eT9mK4cY8rN2vH6fB0dQ3wX7nP1uS5gM9tL4eR8cJ2aF6bK0xT3hG7dW1pZ5vS9mN4cY8rE2fH6aL0tQ3wX7uP1kM5gR9dT4nS8cV2bJ6fW0xG3hK7eZ1pL5aM9tY4cR8nF2vH6bS0dQ3wX7uP1mK5gT9eN4cR8aJ2fL6bH0xW3tG7dZ1pS5vM9cY4eT8rN2fK6aH0bQ3wX7uP1gL5mS9dR4nT8cV2eJ6fB0xW3hG7tK1pZ5aM9vY4cN8rE2fH6bS0dQ3wX7uP1kL5gT9mR4nS8cJ2aF6bW0xG3hK7eZ1pM5vY9tL4cR8nE2fH6aS0bQ3wX7uP1mK5gT9dN4cR8aJ2fL6bH0xW3tG7dZ1pS5vM9cY4eT8rN2fK6aH0bQ3wX",
        algorithm: "RSA-2048-PSS-SHA256",
        timestamp: "2025-12-07T18:30:00.000000+00:00"
      }
    ]
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0A0F29] via-[#1A1F3C] to-[#0A0F29] p-8">
      <div className="max-w-5xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-[#FFD700] mb-2">
            🔐 Export Seal Component Demo
          </h1>
          <p className="text-gray-400">
            Displaying cryptographic seals from the Digital Seal Service
          </p>
        </div>

        {/* Multi-Signature Covenant Example */}
        <section>
          <div className="mb-4">
            <h2 className="text-2xl font-bold text-white mb-2">
              Multi-Signature Covenant
            </h2>
            <p className="text-sm text-gray-400">
              Export sealed by Custodian + 2 Council members (3 total signatures)
            </p>
          </div>

          <ExportSeal
            seals={sealPackage.signatures}
            contentHash={sealPackage.content_hash}
            timestamp={sealPackage.timestamp}
            covenantType={sealPackage.covenant_type}
          />

          <div className="mt-4 p-4 bg-[#1A1F3C] rounded border border-[#FFD700]/30">
            <h3 className="text-sm font-bold text-[#FFD700] mb-2">Export Metadata:</h3>
            <pre className="text-xs text-gray-300 font-mono overflow-x-auto">
              {JSON.stringify(sealPackage.metadata, null, 2)}
            </pre>
          </div>
        </section>

        {/* Single Custodian Seal Example */}
        <section>
          <div className="mb-4">
            <h2 className="text-2xl font-bold text-white mb-2">
              Single Custodian Seal
            </h2>
            <p className="text-sm text-gray-400">
              Export sealed by Custodian only (standard export)
            </p>
          </div>

          <ExportSeal
            seals={singleSealPackage.signatures}
            contentHash={singleSealPackage.content_hash}
            timestamp={singleSealPackage.timestamp}
            covenantType={singleSealPackage.covenant_type}
          />
        </section>

        {/* Integration Instructions */}
        <section className="mt-12 p-6 bg-[#1A1F3C] rounded-lg border-2 border-[#FFD700]/50">
          <h2 className="text-xl font-bold text-[#FFD700] mb-4">
            📚 Integration Instructions
          </h2>

          <div className="space-y-4 text-sm text-gray-300">
            <div>
              <h3 className="font-bold text-white mb-2">1. Import Component</h3>
              <pre className="bg-[#0A0F29] p-3 rounded overflow-x-auto">
                <code className="text-green-400">
{`import ExportSeal from '@/components/export-seal';`}
                </code>
              </pre>
            </div>

            <div>
              <h3 className="font-bold text-white mb-2">2. Get Seal Package from Backend</h3>
              <pre className="bg-[#0A0F29] p-3 rounded overflow-x-auto">
                <code className="text-blue-400">
{`// After export generation
const response = await fetch('/api/annotations/export?format=markdown');
const sealPackage = response.headers.get('X-Seal-Package');`}
                </code>
              </pre>
            </div>

            <div>
              <h3 className="font-bold text-white mb-2">3. Display Seals</h3>
              <pre className="bg-[#0A0F29] p-3 rounded overflow-x-auto">
                <code className="text-purple-400">
{`<ExportSeal
  seals={sealPackage.signatures}
  contentHash={sealPackage.content_hash}
  timestamp={sealPackage.timestamp}
  covenantType={sealPackage.covenant_type}
/>`}
                </code>
              </pre>
            </div>

            <div>
              <h3 className="font-bold text-white mb-2">4. Use Cases</h3>
              <ul className="list-disc list-inside space-y-1 text-gray-400">
                <li>Display after export generation</li>
                <li>Show in export archive/history page</li>
                <li>Include in verification UI</li>
                <li>Embed in downloaded export files (as HTML)</li>
              </ul>
            </div>
          </div>
        </section>

        {/* API Information */}
        <section className="p-6 bg-[#1A1F3C] rounded-lg border border-[#FFD700]/30">
          <h2 className="text-xl font-bold text-[#FFD700] mb-4">
            🔗 Backend API Reference
          </h2>

          <div className="space-y-3 text-sm">
            <div className="flex items-start gap-3">
              <span className="px-2 py-1 bg-green-600 text-white rounded text-xs font-mono">GET</span>
              <div className="flex-1">
                <code className="text-gray-300 font-mono">
                  /api/annotations/export?format=markdown&include_council=true&council_members=council_001,council_002
                </code>
                <p className="text-gray-500 text-xs mt-1">
                  Generate export with multi-signature covenant
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <span className="px-2 py-1 bg-blue-600 text-white rounded text-xs font-mono">GET</span>
              <div className="flex-1">
                <code className="text-gray-300 font-mono">
                  /api/seal/council-seals
                </code>
                <p className="text-gray-500 text-xs mt-1">
                  List all registered council members
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <span className="px-2 py-1 bg-purple-600 text-white rounded text-xs font-mono">POST</span>
              <div className="flex-1">
                <code className="text-gray-300 font-mono">
                  /api/seal/verify
                </code>
                <p className="text-gray-500 text-xs mt-1">
                  Verify seal package authenticity
                </p>
              </div>
            </div>
          </div>

          <div className="mt-4 pt-4 border-t border-[#FFD700]/20">
            <p className="text-xs text-gray-400">
              <strong className="text-[#FFD700]">Backend Server:</strong> http://localhost:8000<br />
              <strong className="text-[#FFD700]">Documentation:</strong> http://localhost:8000/docs
            </p>
          </div>
        </section>
      </div>
    </div>
  );
}
