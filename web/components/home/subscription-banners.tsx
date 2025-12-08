import Link from 'next/link';
import { getSubscriptions } from '@/lib/woocommerce';

export async function SubscriptionBanners() {
  const subscriptions = await getSubscriptions();

  const banners = [
    {
      id: 'kids-monthly',
      title: 'Kids Bible Monthly Club',
      price: '$9.99/month',
      description: 'New coloring books, activity packs, and exclusive printables every month',
      benefits: ['20+ new pages monthly', 'Early access to episodes', 'Exclusive member-only designs'],
      cta: 'Start Free Trial',
      href: '/subscriptions/kids-bible-monthly',
      color: 'from-yellow-400 to-orange-500',
      icon: '🎨'
    },
    {
      id: 'homeschool-monthly',
      title: 'Homeschool Master Pack',
      price: '$19.99/month',
      description: 'Complete lesson plans, curriculum guides, and printable resources',
      benefits: ['50+ pages of curriculum', 'Video lesson guides', 'Teacher community access'],
      cta: 'Join Now',
      href: '/subscriptions/homeschool-monthly',
      color: 'from-green-400 to-emerald-600',
      icon: '📚'
    },
    {
      id: 'wedding-monthly',
      title: 'Wedding Planning Monthly',
      price: '$14.99/month',
      description: 'Faith-centered planning guides, checklists, and templates',
      benefits: ['Monthly planning milestones', 'Vendor checklists', 'Budget trackers'],
      cta: 'Start Planning',
      href: '/subscriptions/wedding-planning-monthly',
      color: 'from-pink-400 to-rose-600',
      icon: '💒'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {banners.map((banner) => (
        <div
          key={banner.id}
          className={`relative overflow-hidden rounded-2xl bg-gradient-to-br ${banner.color} p-8 text-white shadow-xl hover:shadow-2xl transition-shadow`}
        >
          {/* Icon */}
          <div className="text-6xl mb-4">{banner.icon}</div>

          {/* Content */}
          <div className="space-y-4">
            <div>
              <h3 className="text-2xl font-bold mb-2">{banner.title}</h3>
              <p className="text-3xl font-bold mb-2">{banner.price}</p>
              <p className="text-white/90">{banner.description}</p>
            </div>

            {/* Benefits */}
            <ul className="space-y-2">
              {banner.benefits.map((benefit, idx) => (
                <li key={idx} className="flex items-start">
                  <svg
                    className="w-5 h-5 mr-2 flex-shrink-0 mt-0.5"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fillRule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clipRule="evenodd"
                    />
                  </svg>
                  <span className="text-sm">{benefit}</span>
                </li>
              ))}
            </ul>

            {/* CTA */}
            <Link
              href={banner.href}
              className="block w-full bg-white text-gray-900 text-center font-bold py-3 px-6 rounded-lg hover:bg-gray-100 transition-colors"
            >
              {banner.cta}
            </Link>

            {/* Trial note */}
            {banner.id === 'kids-monthly' && (
              <p className="text-xs text-white/75 text-center">
                7-day free trial • Cancel anytime
              </p>
            )}
          </div>

          {/* Background decoration */}
          <div className="absolute -right-8 -bottom-8 opacity-10">
            <div className="text-9xl">{banner.icon}</div>
          </div>
        </div>
      ))}
    </div>
  );
}
