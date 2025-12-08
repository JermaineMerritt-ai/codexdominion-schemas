import Link from 'next/link';
import Image from 'next/image';

const niches = [
  {
    id: 'kids',
    title: 'Kids Bible Stories',
    description: 'Coloring books, activity packs, and animated story companions',
    image: '/images/niches/kids.jpg',
    href: '/shop/kids-bible-stories',
    tags: ['episode-christmas', 'episode-noah', 'coloring', 'activity'],
    color: 'bg-yellow-100',
    icon: '🎨'
  },
  {
    id: 'homeschool',
    title: 'Homeschool Resources',
    description: 'Curriculum, lesson plans, activity packs, and printables',
    image: '/images/niches/homeschool.jpg',
    href: '/shop/homeschool',
    tags: ['homeschool', 'activity', 'memory-verse'],
    color: 'bg-green-100',
    icon: '📚'
  },
  {
    id: 'wedding',
    title: 'Christian Weddings',
    description: 'Faith-centered planners, checklists, invitations, and decor',
    image: '/images/niches/wedding.jpg',
    href: '/shop/wedding',
    tags: ['wedding'],
    color: 'bg-pink-100',
    icon: '💒'
  },
  {
    id: 'memory-verse',
    title: 'Scripture Art & Decor',
    description: 'Memory verse cards, wall art, and printable decor',
    image: '/images/niches/memory-verse.jpg',
    href: '/shop/memory-verses',
    tags: ['memory-verse', 'home-decor'],
    color: 'bg-purple-100',
    icon: '✝️'
  },
  {
    id: 'seasonal',
    title: 'Seasonal Collections',
    description: 'Christmas, Easter, Thanksgiving, and holiday resources',
    image: '/images/niches/seasonal.jpg',
    href: '/shop/seasonal',
    tags: ['seasonal-christmas', 'seasonal'],
    color: 'bg-red-100',
    icon: '🎄'
  },
  {
    id: 'digital',
    title: 'Digital Downloads',
    description: 'Instant access printables and templates',
    image: '/images/niches/digital.jpg',
    href: '/shop/digital-downloads',
    tags: ['digital'],
    color: 'bg-blue-100',
    icon: '⚡'
  }
];

export function NichesGrid() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {niches.map((niche) => (
        <Link
          key={niche.id}
          href={niche.href}
          className="group relative overflow-hidden rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
        >
          <div className={`${niche.color} p-8 h-full flex flex-col justify-between min-h-[280px]`}>
            {/* Icon */}
            <div className="text-6xl mb-4">{niche.icon}</div>

            {/* Content */}
            <div>
              <h3 className="text-2xl font-bold mb-2 group-hover:text-blue-600 transition-colors">
                {niche.title}
              </h3>
              <p className="text-gray-700 mb-4">{niche.description}</p>

              {/* Tags */}
              <div className="flex flex-wrap gap-2 mb-4">
                {niche.tags.slice(0, 2).map((tag) => (
                  <span
                    key={tag}
                    className="text-xs bg-white/50 px-2 py-1 rounded-full"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>

            {/* CTA */}
            <div className="flex items-center text-blue-600 font-semibold group-hover:translate-x-2 transition-transform">
              Shop Now
              <svg
                className="w-5 h-5 ml-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 5l7 7-7 7"
                />
              </svg>
            </div>
          </div>

          {/* Hover overlay */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
        </Link>
      ))}
    </div>
  );
}
