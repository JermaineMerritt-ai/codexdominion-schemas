// ===================================================================
// CODEX DOMINION 2.0 - CREATOR ENGINE SEED DATA
// Artifacts, Challenges, Submissions for testing
// ===================================================================

import { PrismaClient, ArtifactType, ArtifactStatus, SeasonName } from '@prisma/client';

const prisma = new PrismaClient();

async function seedCreatorEngine() {
  console.log('🎨 Seeding Creator Engine data...\n');

  // Get existing users for creator relationships
  const users = await prisma.user.findMany({
    take: 5,
    include: { roles: { include: { role: true } } },
  });

  if (users.length === 0) {
    console.error('❌ No users found. Run main seed first (npx ts-node prisma/seed.ts)');
    return;
  }

  console.log(`Found ${users.length} users for creator data`);

  // Get seasons for linking challenges
  const seasons = await prisma.season.findMany();
  const identitySeason = seasons.find((s) => s.name === SeasonName.IDENTITY);
  const masterySeason = seasons.find((s) => s.name === SeasonName.MASTERY);
  const creationSeason = seasons.find((s) => s.name === SeasonName.CREATION);

  // Get existing missions for linking artifacts
  const missions = await prisma.mission.findMany({ take: 3 });

  // ===================================================================
  // ARTIFACTS
  // ===================================================================

  console.log('\n📦 Creating artifacts...');

  const artifacts = [
    {
      creatorId: users[0].id,
      title: 'Automation for Youth Circle Check-ins',
      description: 'Zapier/Make workflow that sends reminders before each session.',
      artifactType: ArtifactType.AUTOMATION,
      fileUrl: 'https://zapier.com/app/editor/123456',
      missionId: missions[0]?.id,
      status: ArtifactStatus.PUBLISHED,
    },
    {
      creatorId: users[1].id,
      title: 'Budget Tracker Dashboard',
      description: 'Google Sheets automation with real-time expense tracking and alerts',
      artifactType: ArtifactType.AUTOMATION,
      fileUrl: 'https://docs.google.com/spreadsheets/d/abc123',
      missionId: missions[1]?.id,
      status: ArtifactStatus.PUBLISHED,
    },
    {
      creatorId: users[0].id,
      title: 'Community Event Flyer Design',
      description: 'Canva template for Youth Circle event promotions',
      artifactType: ArtifactType.DESIGN,
      fileUrl: 'https://canva.com/design/xyz789',
      status: ArtifactStatus.PUBLISHED,
    },
    {
      creatorId: users[2].id,
      title: 'My Journey: From Identity to Mastery',
      description: 'Personal essay reflecting on growth through the four seasons',
      artifactType: ArtifactType.WRITING,
      fileUrl: 'https://medium.com/@youth/my-journey',
      missionId: missions[2]?.id,
      status: ArtifactStatus.PUBLISHED,
    },
    {
      creatorId: users[1].id,
      title: 'Circle Session Intro Video',
      description: '2-minute welcome video explaining Youth Circle format',
      artifactType: ArtifactType.VIDEO,
      fileUrl: 'https://youtube.com/watch?v=abc123',
      status: ArtifactStatus.PUBLISHED,
    },
    {
      creatorId: users[2].id,
      title: 'Mission Tracker App Prototype',
      description: 'React Native app mockup for tracking youth missions',
      artifactType: ArtifactType.APP,
      fileUrl: 'https://github.com/youth/mission-tracker',
      status: ArtifactStatus.DRAFT,
    },
    {
      creatorId: users[2].id,
      title: 'Cultural Story: The Flame Keeper',
      description: 'Original story about the Dominion\'s founding values',
      artifactType: ArtifactType.WRITING,
      status: ArtifactStatus.PUBLISHED,
    },
    {
      creatorId: users[0].id,
      title: 'Seasonal Reset Ritual Guide',
      description: 'Step-by-step guide for leading quarterly reflection sessions',
      artifactType: ArtifactType.OTHER,
      fileUrl: 'https://docs.google.com/document/d/ritual123',
      status: ArtifactStatus.PUBLISHED,
    },
  ];

  const createdArtifacts: any[] = [];
  for (const artifact of artifacts) {
    const created = await prisma.artifact.create({ data: artifact });
    createdArtifacts.push(created);
    console.log(`  ✅ Created artifact: "${created.title}"`);
  }

  // ===================================================================
  // CREATOR CHALLENGES
  // ===================================================================

  console.log('\n🏆 Creating creator challenges...');

  const adminUser = users.find((u) =>
    u.roles.some((r) => r.role.name === 'ADMIN' || r.role.name === 'COUNCIL')
  ) || users[0];

  const challenges = [
    {
      title: 'Build Your First Automation',
      description:
        'Create an automation that solves a real problem in your community. Use any tool: Zapier, Make, Python, or other platforms.',
      seasonId: identitySeason?.id,
      deadline: new Date('2025-01-31T23:59:59Z'),
      createdBy: adminUser.id,
    },
    {
      title: 'Design Your Brand Identity',
      description:
        'Create a logo, color palette, and brand guide for a youth-led initiative in your community.',
      seasonId: masterySeason?.id,
      deadline: new Date('2025-02-28T23:59:59Z'),
      createdBy: adminUser.id,
    },
    {
      title: 'Share Your Story',
      description:
        'Write a 500+ word essay about your journey, your culture, or your vision for the future.',
      seasonId: creationSeason?.id,
      deadline: new Date('2025-03-31T23:59:59Z'),
      createdBy: adminUser.id,
    },
    {
      title: 'Create a Video Tutorial',
      description:
        'Record a 3-5 minute video teaching a skill, sharing knowledge, or showcasing your creativity.',
      seasonId: creationSeason?.id,
      deadline: null, // Evergreen challenge
      createdBy: adminUser.id,
    },
  ];

  const createdChallenges: any[] = [];
  for (const challenge of challenges) {
    const created = await prisma.creatorChallenge.create({ data: challenge });
    createdChallenges.push(created);
    console.log(`  ✅ Created challenge: "${created.title}"`);
  }

  // ===================================================================
  // CHALLENGE SUBMISSIONS
  // ===================================================================

  console.log('\n📤 Creating challenge submissions...');

  const submissions = [
    {
      challengeId: createdChallenges[0].id, // Build Your First Automation
      creatorId: createdArtifacts[0].creatorId,
      artifactId: createdArtifacts[0].id, // Circle Check-in Automation
    },
    {
      challengeId: createdChallenges[0].id, // Build Your First Automation
      creatorId: createdArtifacts[1].creatorId,
      artifactId: createdArtifacts[1].id, // Budget Tracker
    },
    {
      challengeId: createdChallenges[1].id, // Design Your Brand Identity
      creatorId: createdArtifacts[2].creatorId,
      artifactId: createdArtifacts[2].id, // Event Flyer Design
    },
    {
      challengeId: createdChallenges[2].id, // Share Your Story
      creatorId: createdArtifacts[3].creatorId,
      artifactId: createdArtifacts[3].id, // Personal Essay
    },
    {
      challengeId: createdChallenges[2].id, // Share Your Story
      creatorId: createdArtifacts[6].creatorId,
      artifactId: createdArtifacts[6].id, // Cultural Story
    },
    {
      challengeId: createdChallenges[3].id, // Video Tutorial
      creatorId: createdArtifacts[4].creatorId,
      artifactId: createdArtifacts[4].id, // Circle Session Video
    },
  ];

  for (const submission of submissions) {
    const created = await prisma.challengeSubmission.create({ data: submission });
    console.log(`  ✅ Submitted artifact to challenge`);
  }

  // ===================================================================
  // SUMMARY
  // ===================================================================

  console.log('\n✨ Creator Engine Seed Complete!\n');
  console.log(`📦 Artifacts Created: ${createdArtifacts.length}`);
  console.log(`🏆 Challenges Created: ${createdChallenges.length}`);
  console.log(`📤 Submissions Created: ${submissions.length}\n`);

  console.log('🔥 Ready to test Creator Engine endpoints!');
  console.log('   📚 Swagger docs: http://localhost:4000/api-docs');
  console.log('   🎨 Creator endpoints: /api/v1/creators/*\n');
}

async function main() {
  try {
    await seedCreatorEngine();
  } catch (error) {
    console.error('❌ Seed failed:', error);
    throw error;
  } finally {
    await prisma.$disconnect();
  }
}

main();
