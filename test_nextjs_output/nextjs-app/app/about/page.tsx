import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'About',
  description: 'Testing',
  openGraph: {
    title: 'About',
    description: '',
    images: ['/og-image.png'],
  },
}

export default function AboutPage() {
  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-16 md:py-24">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-heading font-bold mb-6">
            Welcome to {page["title"]}
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 mb-8">
            About
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
      </section>
    </main>
  )
}
