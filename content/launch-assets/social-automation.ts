/**
 * Social Media Automation Configuration
 * Manages content scheduling, templates, and UTM tracking
 */

export interface SocialPost {
  id: string;
  platform: 'instagram' | 'facebook' | 'pinterest' | 'youtube' | 'tiktok';
  type: 'post' | 'story' | 'reel' | 'short' | 'pin' | 'video';
  content: string;
  media: string[];
  scheduledDate: Date;
  tags: string[];
  utm: {
    source: string;
    medium: string;
    campaign: string;
    content?: string;
  };
}

export interface ContentTemplate {
  id: string;
  category: 'kids' | 'homeschool' | 'wedding' | 'seasonal' | 'verse' | 'testimonial';
  caption: string;
  hashtags: string[];
  cta: string;
  variables: string[];
}

// Content templates (plug-and-play)
export const contentTemplates: ContentTemplate[] = [
  {
    id: 'kids-coloring-pack',
    category: 'kids',
    caption: '🎨 New {episodeName} coloring pack just dropped! {pageCount} beautiful pages your kids will love. Perfect for Sunday school, rainy days, or quiet time. ✝️\n\nFree sample pages in bio! 👆',
    hashtags: ['#ChristianColoring', '#BibleStories', '#KidsActivities', '#FaithBasedParenting', '#SundaySchool', '#ChristianKids', '#ColoringBooks', '#BiblicalArt'],
    cta: 'Download free sample → Link in bio',
    variables: ['episodeName', 'pageCount']
  },
  {
    id: 'homeschool-tip',
    category: 'homeschool',
    caption: '📚 Homeschool tip: {tipContent}\n\nWant more? Our {planName} includes weekly lesson plans, printables, and video guides. Making faith-centered homeschooling easier! 🙏',
    hashtags: ['#Homeschool', '#ChristianHomeschool', '#HomeschoolMom', '#FaithBasedEducation', '#HomeschoolCurriculum', '#BiblicalEducation', '#HomeschoolLife', '#ChristianEducation'],
    cta: 'Get the full curriculum → {link}',
    variables: ['tipContent', 'planName', 'link']
  },
  {
    id: 'wedding-checklist',
    category: 'wedding',
    caption: '💒 Planning a Christian wedding? Our faith-centered planner includes:\n\n✅ {feature1}\n✅ {feature2}\n✅ {feature3}\n✅ Scripture for every milestone\n\nMake your big day glorify God! 💍',
    hashtags: ['#ChristianWedding', '#FaithBasedWedding', '#WeddingPlanning', '#ChristianBride', '#WeddingChecklist', '#BiblicalMarriage', '#ChristianMarriage', '#WeddingPlanner'],
    cta: 'Download the planner → {link}',
    variables: ['feature1', 'feature2', 'feature3', 'link']
  },
  {
    id: 'seasonal-christmas',
    category: 'seasonal',
    caption: '🎄 Christmas is coming! Our {productName} makes the perfect:\n\n🎁 Stocking stuffer\n📚 Homeschool activity\n⛪ Sunday school resource\n🎨 Family activity night\n\nShop the Christmas collection now! ❄️',
    hashtags: ['#ChristmasActivities', '#ChristianChristmas', '#AdventActivities', '#ChristmasColoring', '#HolidayPrintables', '#ChristmasCrafts', '#FaithfulChristmas', '#BiblicalChristmas'],
    cta: 'Shop Christmas deals → {link}',
    variables: ['productName', 'link']
  },
  {
    id: 'memory-verse-challenge',
    category: 'verse',
    caption: '📖 This week\'s memory verse:\n\n"{verseText}"\n- {verseRef}\n\nDownload our free printable cards to help your family memorize Scripture together! 🙏',
    hashtags: ['#MemoryVerse', '#ScriptureMemorization', '#BibleVerse', '#FaithFamily', '#ChristianLiving', '#DailyScripture', '#BibleStudy', '#ChristianParenting'],
    cta: 'Get free verse cards → Link in bio',
    variables: ['verseText', 'verseRef']
  },
  {
    id: 'testimonial',
    category: 'testimonial',
    caption: '💝 "{testimonialText}"\n\n- {customerName}\n\nWe\'re so blessed to serve families like yours! Thank you for sharing your journey with us. 🙏',
    hashtags: ['#CustomerLove', '#FaithFamily', '#ChristianCommunity', '#Testimony', '#Blessed', '#FaithfulParenting', '#ChristianLife', '#GodsGoodness'],
    cta: 'Join our community → {link}',
    variables: ['testimonialText', 'customerName', 'link']
  }
];

// Posting schedule configuration
export const postingSchedule = {
  instagram: {
    posts: 5, // per week
    stories: 10, // per week
    reels: 2, // per week
    bestTimes: ['9:00 AM', '12:00 PM', '7:00 PM']
  },
  facebook: {
    posts: 5,
    stories: 10,
    reels: 2,
    bestTimes: ['9:00 AM', '1:00 PM', '8:00 PM']
  },
  pinterest: {
    pins: 20, // per week
    boards: ['Coloring Books', 'Activity Packs', 'Homeschool', 'Wedding Printables', 'Verse Decor'],
    bestTimes: ['8:00 PM', '9:00 PM', '10:00 PM'] // Evening pins perform best
  },
  youtube: {
    shorts: 2, // per week
    longForm: 1, // per week
    bestTimes: ['2:00 PM', '5:00 PM']
  },
  tiktok: {
    shorts: 2, // per week
    bestTimes: ['7:00 AM', '12:00 PM', '9:00 PM']
  }
};

// UTM tracking builder
export function buildUTM(params: {
  source: string;
  medium: string;
  campaign: string;
  content?: string;
  term?: string;
}): string {
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://codexdominion.app';
  const utmParams = new URLSearchParams({
    utm_source: params.source,
    utm_medium: params.medium,
    utm_campaign: params.campaign,
    ...(params.content && { utm_content: params.content }),
    ...(params.term && { utm_term: params.term })
  });

  return `${baseUrl}?${utmParams.toString()}`;
}

// Generate social post with UTM tracking
export function generateSocialPost(
  template: ContentTemplate,
  variables: Record<string, string>,
  platform: string,
  campaignName: string
): SocialPost {
  // Replace variables in caption
  let caption = template.caption;
  Object.entries(variables).forEach(([key, value]) => {
    caption = caption.replace(new RegExp(`{${key}}`, 'g'), value);
  });

  // Build UTM link
  const utmLink = buildUTM({
    source: platform,
    medium: 'social',
    campaign: campaignName,
    content: template.id
  });

  // Replace {link} with UTM link
  caption = caption.replace(/{link}/g, utmLink);

  // Add hashtags
  const fullCaption = `${caption}\n\n${template.hashtags.join(' ')}`;

  return {
    id: `${platform}_${template.id}_${Date.now()}`,
    platform: platform as any,
    type: 'post',
    content: fullCaption,
    media: [],
    scheduledDate: new Date(),
    tags: template.hashtags,
    utm: {
      source: platform,
      medium: 'social',
      campaign: campaignName,
      content: template.id
    }
  };
}

// Lead magnet sequence (automated email after download)
export const leadMagnetSequence = {
  welcome: {
    subject: '🎉 Your free {magnetName} is ready!',
    body: 'Thanks for downloading! Here\'s your link + 3 bonus printables...',
    sendAfter: 0 // immediately
  },
  productDrop: {
    subject: '📦 New {niche} products you\'ll love',
    body: 'We just launched {productName}. As a subscriber, you get 20% off...',
    sendAfter: 3 // 3 days
  },
  seasonalPromo: {
    subject: '🎄 Christmas sale: 40% off everything',
    body: 'Limited time! Stock up on activities, planners, and printables...',
    sendAfter: 7 // 7 days
  }
};

// Pinterest SEO titles (optimized for search)
export const pinterestTitles = {
  coloring: '{episodeName} Bible Coloring Pages for Kids | Free Printable Christian Activity',
  homeschool: '{subject} Homeschool Curriculum | Christian Lesson Plans & Printables',
  wedding: 'Christian Wedding Planning Checklist | Faith-Based Wedding Planner Template',
  verse: '{verseTopic} Bible Verse Cards | Free Printable Scripture Memory',
  seasonal: '{season} Christian Activities for Kids | Faith-Based Holiday Printables'
};
