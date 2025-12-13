'use client';

import Link from 'next/link';
import { useState } from 'react';

interface FAQItem {
  question: string;
  answer: string;
  category: string;
}

function FAQPage() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const faqs: FAQItem[] = [
    {
      category: 'Products & Purchasing',
      question: 'What formats are the products available in?',
      answer: 'Most of our devotionals are available in PDF and ePub formats. Journals are printable PDFs (8.5x11 or 6x9). Bundles may include multiple formats including audio files (MP3). All formats are optimized for digital reading and printing.'
    },
    {
      category: 'Products & Purchasing',
      question: 'How do I access my purchase after buying?',
      answer: 'Immediately after completing your purchase, you\'ll receive a confirmation email with download links for all your products. You can download them as many times as you need. We recommend saving a copy to your device or cloud storage.'
    },
    {
      category: 'Products & Purchasing',
      question: 'Can I get physical printed copies?',
      answer: 'Some products like journals are available in physical format. Check the product page for "Physical Available" badge. Digital products can be self-printed at home or through a local print shop.'
    },
    {
      category: 'Products & Purchasing',
      question: 'Do you offer discounts or bundles?',
      answer: 'Yes! Our bundle packages offer significant savings (up to 40% off). We also run seasonal promotions and offer a 10% discount for newsletter subscribers on their first purchase.'
    },
    {
      category: 'Payment & Security',
      question: 'What payment methods do you accept?',
      answer: 'We accept all major credit cards (Visa, Mastercard, American Express, Discover) through Stripe, our secure payment processor. All transactions are encrypted and PCI-compliant.'
    },
    {
      category: 'Payment & Security',
      question: 'Is my payment information secure?',
      answer: 'Absolutely. We use Stripe for payment processing, which means your card information never touches our servers. Stripe is certified to PCI Service Provider Level 1, the highest level of payment security.'
    },
    {
      category: 'Refunds & Support',
      question: 'What is your refund policy?',
      answer: 'We offer a 30-day money-back guarantee. If you\'re not satisfied with your purchase for any reason, contact us within 30 days for a full refund. No questions asked.'
    },
    {
      category: 'Refunds & Support',
      question: 'What if I have technical issues downloading?',
      answer: 'Contact us at support@codexdominion.app and we\'ll help you immediately. Common issues are browser-related or email filtering. We typically respond within 24 hours.'
    },
    {
      category: 'Refunds & Support',
      question: 'Can I share my purchase with others?',
      answer: 'Our products are licensed for personal use. You may print copies for yourself or use them in your personal Bible study. For group use (church, ministry, business team), please contact us for group licensing options.'
    },
    {
      category: 'Usage & Licensing',
      question: 'Can I use these resources in my church or ministry?',
      answer: 'Yes! For small groups (under 10 people), you can use your personal copy. For larger groups or ministry-wide use, please contact us for bulk licensing. We offer discounted group rates.'
    },
    {
      category: 'Usage & Licensing',
      question: 'Do I get free updates?',
      answer: 'Yes! If we update a product you\'ve purchased (fixing typos, adding content, improving design), you\'ll receive the updated version for free via email.'
    },
    {
      category: 'Usage & Licensing',
      question: 'Can I print and bind the journals?',
      answer: 'Absolutely! Our journals are designed to be printed and bound. You can print at home, use an office printer, or take the PDF to a local print shop for professional binding.'
    },
    {
      category: 'Content & Topics',
      question: 'Are these resources theologically sound?',
      answer: 'Yes. All our content is rooted in historic Christian orthodoxy and biblical truth. We draw from multiple denominations but focus on core biblical principles that unite believers.'
    },
    {
      category: 'Content & Topics',
      question: 'Who are these products designed for?',
      answer: 'Our resources are designed for Christian entrepreneurs, business leaders, ministry workers, and anyone seeking to integrate faith with their professional life. They work for individuals, couples, and small groups.'
    },
    {
      category: 'Content & Topics',
      question: 'Do I need to be in business to use these?',
      answer: 'Not at all! While many resources have business applications, the spiritual principles apply to anyone seeking deeper faith, clarity, and purpose. The Daily Flame and gratitude journals work for all believers.'
    }
  ];

  const categories = ['All', 'Products & Purchasing', 'Payment & Security', 'Refunds & Support', 'Usage & Licensing', 'Content & Topics'];
  const [selectedCategory, setSelectedCategory] = useState('All');

  const filteredFAQs = selectedCategory === 'All'
    ? faqs
    : faqs.filter(faq => faq.category === selectedCategory);

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
            <Link href="/contact" className="text-purple-200 hover:text-gold-300 transition-colors">
              Contact
            </Link>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-6 py-16">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl font-bold mb-8 bg-gradient-to-r from-gold-300 via-yellow-300 to-gold-400 bg-clip-text text-transparent text-center">
            Frequently Asked Questions
          </h1>

          <p className="text-xl text-purple-200 text-center mb-12 max-w-2xl mx-auto">
            Find quick answers to common questions about our products, payments, and policies.
          </p>

          {/* Category Filter */}
          <div className="flex flex-wrap justify-center gap-3 mb-12">
            {categories.map(category => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-4 py-2 rounded-lg font-semibold transition-all duration-300 ${
                  selectedCategory === category
                    ? 'bg-gradient-to-r from-gold-500 to-amber-500 text-white'
                    : 'bg-gray-800/60 text-purple-200 hover:bg-gray-700/80 border border-purple-600/30'
                }`}
              >
                {category}
              </button>
            ))}
          </div>

          {/* FAQ Accordion */}
          <div className="space-y-4">
            {filteredFAQs.map((faq, index) => (
              <div
                key={index}
                className="bg-gradient-to-br from-gray-800/90 to-purple-900/80 rounded-xl border-2 border-purple-600/50 overflow-hidden"
              >
                <button
                  onClick={() => setOpenIndex(openIndex === index ? null : index)}
                  className="w-full px-6 py-4 text-left flex justify-between items-center hover:bg-purple-900/30 transition-colors"
                >
                  <div className="flex-1">
                    <span className="text-xs text-gold-400 uppercase font-bold block mb-1">
                      {faq.category}
                    </span>
                    <span className="text-lg font-bold text-white">
                      {faq.question}
                    </span>
                  </div>
                  <span className={`text-2xl text-gold-400 ml-4 transition-transform duration-300 ${openIndex === index ? 'rotate-180' : ''}`}>
                    ▼
                  </span>
                </button>

                {openIndex === index && (
                  <div className="px-6 py-4 border-t-2 border-purple-700/50 bg-gray-900/40">
                    <p className="text-purple-200 leading-relaxed">
                      {faq.answer}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Still Have Questions */}
          <div className="mt-16 bg-gradient-to-r from-gold-900/40 to-amber-900/40 rounded-3xl p-8 border-2 border-gold-500/50 text-center">
            <h2 className="text-3xl font-bold text-gold-300 mb-4">Still Have Questions?</h2>
            <p className="text-lg text-purple-200 mb-6">
              Can't find what you're looking for? We're here to help.
            </p>
            <Link href="/contact">
              <button className="px-8 py-4 bg-gradient-to-r from-gold-500 to-amber-500 hover:from-gold-600 hover:to-amber-600 rounded-xl font-bold text-lg transition-all duration-300 shadow-lg">
                Contact Support
              </button>
            </Link>
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

export default FAQPage;

export async function getServerSideProps() {
  return { props: {} };
}
