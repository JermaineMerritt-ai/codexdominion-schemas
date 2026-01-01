import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Testing',
  description: 'Testing',
  openGraph: {
    title: 'Home',
    description: '',
    images: ['/og-image.png'],
  },
}

export default function HomePage() {
  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-16 md:py-24">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-heading font-bold mb-6">
            Welcome to Demo Site
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 mb-8">
            Testing
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="btn-primary">
              Get Started
            </button>
            <button className="px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
              Learn More
            </button>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
          <div className="card">
            <h3 className="text-xl font-heading font-bold mb-2">Expert Solutions</h3>
            <p className="text-gray-600">Leverage our industry-leading expertise to achieve your goals faster and more efficiently.</p>
          </div>
          <div className="card">
            <h3 className="text-xl font-heading font-bold mb-2">Dedicated Support</h3>
            <p className="text-gray-600">Our team is available 24/7 to ensure your success and answer any questions.</p>
          </div>
          <div className="card">
            <h3 className="text-xl font-heading font-bold mb-2">Proven Results</h3>
            <p className="text-gray-600">Join thousands of satisfied clients who have transformed their operations with our platform.</p>
          </div>
        </div>
      </section>
    </main>
  )
}
