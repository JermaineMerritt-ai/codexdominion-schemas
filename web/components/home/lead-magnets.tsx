'use client';

import { useState } from 'react';

const leadMagnets = [
  {
    id: 'christmas-coloring',
    title: 'Free Christmas Story Coloring Pack',
    description: '10 beautiful coloring pages from our animated Christmas episode',
    image: '/images/lead-magnets/christmas-coloring.jpg',
    downloadUrl: '/api/download/christmas-coloring',
    tag: 'seasonal-christmas',
    icon: '🎨'
  },
  {
    id: 'homeschool-checklist',
    title: 'Weekly Homeschool Planning Checklist',
    description: 'Organize your homeschool week with our free printable planner',
    image: '/images/lead-magnets/homeschool-checklist.jpg',
    downloadUrl: '/api/download/homeschool-checklist',
    tag: 'homeschool',
    icon: '✅'
  },
  {
    id: 'wedding-timeline',
    title: 'Christian Wedding Timeline Template',
    description: '12-month planning timeline with scripture-based milestones',
    image: '/images/lead-magnets/wedding-timeline.jpg',
    downloadUrl: '/api/download/wedding-timeline',
    tag: 'wedding',
    icon: '📅'
  },
  {
    id: 'memory-verse-cards',
    title: 'Printable Memory Verse Cards (10 Pack)',
    description: 'Beautiful cards featuring popular Bible verses for kids',
    image: '/images/lead-magnets/memory-verse-cards.jpg',
    downloadUrl: '/api/download/memory-verse-cards',
    tag: 'memory-verse',
    icon: '📖'
  }
];

export function LeadMagnets() {
  const [email, setEmail] = useState('');
  const [selectedMagnet, setSelectedMagnet] = useState<string | null>(null);
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

  const handleDownload = async (magnetId: string) => {
    if (!email) {
      alert('Please enter your email address');
      return;
    }

    setSelectedMagnet(magnetId);
    setStatus('loading');

    try {
      // Track lead magnet download event
      if (typeof window !== 'undefined' && (window as any).gtag) {
        (window as any).gtag('event', 'download_lead_magnet', {
          event_category: 'engagement',
          event_label: magnetId,
          value: email
        });
      }

      const response = await fetch('/api/lead-magnet', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, magnetId })
      });

      if (response.ok) {
        const data = await response.json();
        // Trigger download
        window.location.href = data.downloadUrl;
        setStatus('success');
        setTimeout(() => {
          setStatus('idle');
          setEmail('');
        }, 3000);
      } else {
        setStatus('error');
      }
    } catch (error) {
      console.error('Download error:', error);
      setStatus('error');
    }
  };

  return (
    <div className="space-y-8">
      {/* Email input */}
      <div className="max-w-md mx-auto">
        <label htmlFor="email" className="block text-sm font-medium mb-2">
          Enter your email to download free resources:
        </label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="your@email.com"
          className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        {status === 'success' && (
          <p className="text-green-600 text-sm mt-2">✓ Download started! Check your email for more resources.</p>
        )}
        {status === 'error' && (
          <p className="text-red-600 text-sm mt-2">Error downloading. Please try again.</p>
        )}
      </div>

      {/* Lead magnets grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {leadMagnets.map((magnet) => (
          <div
            key={magnet.id}
            className="bg-white rounded-xl shadow-md overflow-hidden border-2 border-gray-200 hover:border-blue-400 transition-all hover:scale-[1.02]"
          >
            <div className="p-6">
              <div className="text-5xl mb-4">{magnet.icon}</div>
              <h3 className="font-bold text-lg mb-2">{magnet.title}</h3>
              <p className="text-gray-600 text-sm mb-4">{magnet.description}</p>

              <button
                onClick={() => handleDownload(magnet.id)}
                disabled={!email || (status === 'loading' && selectedMagnet === magnet.id)}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
              >
                {status === 'loading' && selectedMagnet === magnet.id
                  ? 'Downloading...'
                  : 'Download Free'}
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Value prop */}
      <p className="text-center text-sm text-gray-500 max-w-2xl mx-auto">
        📧 Join 10,000+ faith-centered families receiving weekly printables, homeschool tips, and exclusive offers
      </p>
    </div>
  );
}
