import Link from 'next/link';

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-blue-900">
      {/* Navigation */}
      <nav className="container mx-auto px-6 py-4 border-b-2 border-purple-800/50">
        <div className="flex justify-between items-center">
          <Link href="/" className="flex items-center space-x-2">
            <span className="text-3xl">🔥</span>
            <span className="text-2xl font-bold text-gold-300">Codex Dominion</span>
          </Link>
          <div className="flex space-x-6">
            <Link href="/products" className="text-purple-200 hover:text-gold-300 transition-colors">
              Shop
            </Link>
            <Link href="/about" className="text-gold-300 font-bold">
              About
            </Link>
            <Link href="/contact" className="text-purple-200 hover:text-gold-300 transition-colors">
              Contact
            </Link>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-6 py-16 max-w-4xl">
        <h1 className="text-5xl font-bold mb-8 bg-gradient-to-r from-gold-300 via-yellow-300 to-gold-400 bg-clip-text text-transparent text-center">
          About Codex Dominion
        </h1>

        <div className="bg-gradient-to-br from-gray-800/90 to-purple-900/80 rounded-3xl p-8 md:p-12 border-2 border-purple-600/50 mb-12">
          <div className="text-6xl text-center mb-6">🔥</div>

          <h2 className="text-3xl font-bold text-gold-300 mb-4">Our Mission</h2>
          <p className="text-lg text-purple-200 mb-6 leading-relaxed">
            At Codex Dominion, we believe that faith and business aren't separate—they're two sides of the same calling.
            We empower Christian entrepreneurs, ministry leaders, and believers to build kingdom-driven enterprises with
            integrity, wisdom, and divine guidance.
          </p>

          <p className="text-lg text-purple-200 mb-6 leading-relaxed">
            Our premium devotionals, journals, and resources combine biblical principles with practical business strategies,
            helping you grow spiritually while building sustainable, purpose-driven ventures.
          </p>

          <h2 className="text-3xl font-bold text-gold-300 mb-4 mt-8">Our Story</h2>
          <p className="text-lg text-purple-200 mb-6 leading-relaxed">
            Codex Dominion was born from a simple question: "How can I honor God while building a successful business?"
            After years of navigating the tension between worldly success and spiritual integrity, our founder realized
            that faith-driven entrepreneurship isn't about compromise—it's about alignment.
          </p>

          <p className="text-lg text-purple-200 mb-6 leading-relaxed">
            We've poured biblical wisdom, real-world experience, and prayer into every resource we create. Each devotional,
            journal, and course is designed to help you discern God's will for your business, lead with compassion, and
            build legacy ventures that glorify His name.
          </p>

          <h2 className="text-3xl font-bold text-gold-300 mb-4 mt-8">Our Values</h2>
          <div className="grid md:grid-cols-2 gap-6 mt-6">
            <div className="bg-gray-900/60 rounded-xl p-6 border-2 border-gold-500/30">
              <div className="text-4xl mb-3">📖</div>
              <h3 className="text-xl font-bold text-white mb-2">Scripture-Centered</h3>
              <p className="text-purple-200">Every resource is rooted in biblical truth and theological soundness.</p>
            </div>
            <div className="bg-gray-900/60 rounded-xl p-6 border-2 border-gold-500/30">
              <div className="text-4xl mb-3">🤝</div>
              <h3 className="text-xl font-bold text-white mb-2">Integrity First</h3>
              <p className="text-purple-200">We practice what we preach—honesty, transparency, and ethical business.</p>
            </div>
            <div className="bg-gray-900/60 rounded-xl p-6 border-2 border-gold-500/30">
              <div className="text-4xl mb-3">💡</div>
              <h3 className="text-xl font-bold text-white mb-2">Practical Wisdom</h3>
              <p className="text-purple-200">Faith meets action with actionable strategies and real-world application.</p>
            </div>
            <div className="bg-gray-900/60 rounded-xl p-6 border-2 border-gold-500/30">
              <div className="text-4xl mb-3">🌍</div>
              <h3 className="text-xl font-bold text-white mb-2">Kingdom Impact</h3>
              <p className="text-purple-200">Business as ministry—profit with purpose and eternal significance.</p>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center bg-gradient-to-r from-gold-900/40 to-amber-900/40 rounded-3xl p-8 border-2 border-gold-500/50">
          <h2 className="text-3xl font-bold text-gold-300 mb-4">Ready to Build Your Faith-Driven Empire?</h2>
          <p className="text-lg text-purple-200 mb-6">
            Explore our resources and start your journey today.
          </p>
          <Link href="/products">
            <button className="px-8 py-4 bg-gradient-to-r from-gold-500 to-amber-500 hover:from-gold-600 hover:to-amber-600 rounded-xl font-bold text-lg transition-all duration-300 shadow-lg">
              Shop Products
            </button>
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="container mx-auto px-6 py-12 border-t-2 border-purple-800/50 mt-16">
        <div className="text-center text-purple-300 text-sm">
          <p>© 2024 Codex Dominion. All rights reserved.</p>
          <p className="mt-2">🔥 Empowering Faith-Driven Entrepreneurs</p>
        </div>
      </footer>
    </div>
  );
}
