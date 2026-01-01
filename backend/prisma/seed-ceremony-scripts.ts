import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('\n🎭 Seeding Ceremony Scripts...\n');

  // Season Ceremony Script (Mastery Season)
  const seasonCeremony = await prisma.ceremonyScript.upsert({
    where: { eventId: 'season-ceremony-mastery-2025' },
    create: {
      eventId: 'season-ceremony-mastery-2025',
      sections: {
        rituals: [
          '🔥 Opening: Light the Flame of Mastery',
          '🌅 Dawn Invocation: "We rise as the sun rises"',
          '👥 Circle Formation: Youth form concentric circles by region',
          '📿 Unity Chain: Each youth holds hands, speaks their identity',
        ],
        readings: [
          '📖 Cultural Story: The Master Craftsman (Diaspora origin tale)',
          '📜 Season Reading: "Mastery is not perfection. It is practice, patience, and persistence."',
          '🌍 Diaspora Reflection: "Our ancestors mastered survival. We master sovereignty."',
        ],
        affirmations: [
          'I rise in mastery',
          'I honor my learning',
          'I refine my craft',
          'I build with excellence',
          'I grow through discipline',
        ],
        transitions: [
          '🎵 Dawn Ceremony Music: Traditional drumming',
          '🕯️ Candle Lighting: Each circle captain lights a candle',
          '🔔 Bell Ringing: Three rings to mark transition',
        ],
      },
    },
    update: {},
  });

  console.log('✓ Season Ceremony script created');

  // Launch Event Script (Barbados)
  const launchScript = await prisma.ceremonyScript.upsert({
    where: { eventId: 'barbados-launch-2025' },
    create: {
      eventId: 'barbados-launch-2025',
      sections: {
        rituals: [
          '🔥 Lighting the Dominion Flame',
          '🌴 Regional Acknowledgment: Honor Barbados land and ancestors',
          '👥 Youth Introduction: Each youth speaks their name and identity',
          '🤝 Unity Pledge: "I rise with my community"',
          '📯 Launch Declaration: Regional director announces mission',
        ],
        readings: [
          '📖 Origin Story: The First Flame (How Codex Dominion began)',
          '📜 Diaspora Reading: Caribbean Unity and Identity',
          '🎯 Mission Reveal: First regional mission announced',
        ],
        affirmations: [
          'I rise with my identity',
          'I honor my community',
          'I carry the flame',
          'I build with purpose',
          'I walk with unity',
        ],
        transitions: [
          '🎵 Opening Music: Caribbean rhythms',
          '🎉 Celebration: Dance and community gathering',
          '📸 Group Photo: All participants with Dominion banner',
        ],
      },
    },
    update: {},
  });

  console.log('✓ Barbados Launch script created');

  // Summit Script (Leadership)
  const summitScript = await prisma.ceremonyScript.upsert({
    where: { eventId: 'leadership-summit-2025' },
    create: {
      eventId: 'leadership-summit-2025',
      sections: {
        rituals: [
          '👑 Opening Council Circle',
          '🔥 Flame Passing: Each leader lights flame from central source',
          '📯 Leadership Charge: "I steward, I guide, I serve"',
          '🤝 Circle of Accountability: Leaders pledge to support one another',
        ],
        readings: [
          '📖 Leadership Story: The Servant Steward',
          '📜 Council Constitution Reading',
          '🎯 Strategic Vision: Year ahead goals',
        ],
        affirmations: [
          'I lead with humility',
          'I serve with clarity',
          'I steward with wisdom',
          'I guide with purpose',
          'I build for generations',
        ],
        transitions: [
          '🎵 Council March: Drums and horns',
          '🕯️ Candle Vigil: Silent reflection',
          '📜 Signature Ceremony: Leaders sign year commitment',
        ],
      },
    },
    update: {},
  });

  console.log('✓ Leadership Summit script created');

  // Showcase Script
  const showcaseScript = await prisma.ceremonyScript.upsert({
    where: { eventId: 'youth-showcase-jamaica-march' },
    create: {
      eventId: 'youth-showcase-jamaica-march',
      sections: {
        rituals: [
          '🎨 Gallery Walk: Artifacts displayed around circle',
          '👥 Creator Introductions: Each creator presents their work',
          '🎤 Testimony Time: 3-minute stories of creation process',
          '🏆 Community Recognition: Applause and affirmation',
        ],
        readings: [
          '📖 Creator Story: The Youth Who Built a Bridge',
          '📜 Innovation Reading: "We are builders, not consumers"',
        ],
        affirmations: [
          'I create with purpose',
          'I build with excellence',
          'I share with generosity',
          'I learn from feedback',
          'I grow through iteration',
        ],
        transitions: [
          '🎵 Showcase Music: Uplifting instrumental',
          '📸 Creator Photos: Each with their artifact',
          '🎉 Celebration: Refreshments and networking',
        ],
      },
    },
    update: {},
  });

  console.log('✓ Showcase script created');

  console.log('\n✅ Ceremony Scripts Seeded!\n');
  console.log('📋 Scripts Created:');
  console.log('  - Season Ceremony (Mastery) → season-ceremony-mastery-2025');
  console.log('  - Barbados Launch → barbados-launch-2025');
  console.log('  - Leadership Summit → leadership-summit-2025');
  console.log('  - Youth Showcase → youth-showcase-jamaica-march');
  console.log('\n🔥 Test with: GET /api/v1/events/:id/script');
}

main()
  .then(async () => {
    await prisma.$disconnect();
  })
  .catch(async (e) => {
    console.error('❌ Error:', e);
    await prisma.$disconnect();
    process.exit(1);
  });
