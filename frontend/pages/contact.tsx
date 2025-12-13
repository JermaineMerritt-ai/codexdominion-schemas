'use client';

import Link from 'next/link';
import { useState } from 'react';

function ContactPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Integrate with email service or backend API
    console.log('Form submitted:', formData);
    setSubmitted(true);
    setTimeout(() => {
      setSubmitted(false);
      setFormData({ name: '', email: '', subject: '', message: '' });
    }, 5000);
  };

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
            <Link href="/about" className="text-purple-200 hover:text-gold-300 transition-colors">
              About
            </Link>
            <Link href="/contact" className="text-gold-300 font-bold">
              Contact
            </Link>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-6 py-16">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl font-bold mb-8 bg-gradient-to-r from-gold-300 via-yellow-300 to-gold-400 bg-clip-text text-transparent text-center">
            Get In Touch
          </h1>

          <p className="text-xl text-purple-200 text-center mb-12 max-w-2xl mx-auto">
            Have questions about our products? Need support? Want to share your testimony?
            We'd love to hear from you.
          </p>

          <div className="grid md:grid-cols-2 gap-8 mb-12">
            {/* Contact Info */}
            <div className="space-y-6">
              <div className="bg-gradient-to-br from-gray-800/90 to-purple-900/80 rounded-2xl p-6 border-2 border-purple-600/50">
                <h3 className="text-2xl font-bold text-gold-300 mb-6">Contact Information</h3>

                <div className="space-y-4">
                  <div className="flex items-start">
                    <span className="text-3xl mr-4">📧</span>
                    <div>
                      <p className="text-white font-bold">Email</p>
                      <a href="mailto:support@codexdominion.app" className="text-purple-300 hover:text-gold-300">
                        support@codexdominion.app
                      </a>
                    </div>
                  </div>

                  <div className="flex items-start">
                    <span className="text-3xl mr-4">💬</span>
                    <div>
                      <p className="text-white font-bold">Response Time</p>
                      <p className="text-purple-300">Within 24 hours</p>
                    </div>
                  </div>

                  <div className="flex items-start">
                    <span className="text-3xl mr-4">🌐</span>
                    <div>
                      <p className="text-white font-bold">Social Media</p>
                      <div className="space-y-1">
                        <a href="https://instagram.com/codexdominion" target="_blank" rel="noopener noreferrer" className="block text-purple-300 hover:text-gold-300">
                          Instagram
                        </a>
                        <a href="https://facebook.com/codexdominion" target="_blank" rel="noopener noreferrer" className="block text-purple-300 hover:text-gold-300">
                          Facebook
                        </a>
                        <a href="https://tiktok.com/@codexdominion" target="_blank" rel="noopener noreferrer" className="block text-purple-300 hover:text-gold-300">
                          TikTok
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-gradient-to-br from-gray-800/90 to-purple-900/80 rounded-2xl p-6 border-2 border-purple-600/50">
                <h3 className="text-xl font-bold text-gold-300 mb-4">Common Questions</h3>
                <p className="text-purple-200 mb-3">
                  Before reaching out, check our <Link href="/faq" className="text-gold-400 hover:underline">FAQ page</Link> for
                  quick answers to common questions about products, downloads, and refunds.
                </p>
              </div>
            </div>

            {/* Contact Form */}
            <div className="bg-gradient-to-br from-gray-800/90 to-purple-900/80 rounded-2xl p-6 md:p-8 border-2 border-purple-600/50">
              {submitted ? (
                <div className="text-center py-12">
                  <div className="text-6xl mb-4">✓</div>
                  <h3 className="text-2xl font-bold text-gold-300 mb-2">Message Sent!</h3>
                  <p className="text-purple-200">
                    Thank you for contacting us. We'll respond within 24 hours.
                  </p>
                </div>
              ) : (
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <label className="block text-white font-bold mb-2">Name *</label>
                    <input
                      type="text"
                      required
                      value={formData.name}
                      onChange={(e) => setFormData({...formData, name: e.target.value})}
                      className="w-full px-4 py-3 rounded-lg text-gray-900 font-semibold focus:outline-none focus:ring-4 focus:ring-gold-400"
                      placeholder="Your name"
                    />
                  </div>

                  <div>
                    <label className="block text-white font-bold mb-2">Email *</label>
                    <input
                      type="email"
                      required
                      value={formData.email}
                      onChange={(e) => setFormData({...formData, email: e.target.value})}
                      className="w-full px-4 py-3 rounded-lg text-gray-900 font-semibold focus:outline-none focus:ring-4 focus:ring-gold-400"
                      placeholder="your.email@example.com"
                    />
                  </div>

                  <div>
                    <label className="block text-white font-bold mb-2">Subject *</label>
                    <select
                      required
                      value={formData.subject}
                      onChange={(e) => setFormData({...formData, subject: e.target.value})}
                      className="w-full px-4 py-3 rounded-lg text-gray-900 font-semibold focus:outline-none focus:ring-4 focus:ring-gold-400"
                    >
                      <option value="">Select a subject</option>
                      <option value="product-question">Product Question</option>
                      <option value="technical-support">Technical Support</option>
                      <option value="billing-refund">Billing & Refunds</option>
                      <option value="partnership">Partnership Inquiry</option>
                      <option value="testimony">Share Testimony</option>
                      <option value="other">Other</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-white font-bold mb-2">Message *</label>
                    <textarea
                      required
                      value={formData.message}
                      onChange={(e) => setFormData({...formData, message: e.target.value})}
                      rows={6}
                      className="w-full px-4 py-3 rounded-lg text-gray-900 font-semibold focus:outline-none focus:ring-4 focus:ring-gold-400 resize-none"
                      placeholder="How can we help you?"
                    />
                  </div>

                  <button
                    type="submit"
                    className="w-full py-4 bg-gradient-to-r from-gold-500 to-amber-500 hover:from-gold-600 hover:to-amber-600 rounded-xl font-bold text-lg transition-all duration-300 shadow-lg"
                  >
                    Send Message
                  </button>
                </form>
              )}
            </div>
          </div>
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

export default ContactPage;

export async function getServerSideProps() {
  return { props: {} };
}
