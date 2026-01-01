import { PrismaClient, EventType, EventAttendanceStatus, RoleName } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('🎭 Seeding Events & Ceremonies Engine...\n');

  // Get admin user to create events
  const admin = await prisma.user.findFirst({
    where: { roles: { some: { role: { name: RoleName.ADMIN } } } },
  });

  if (!admin) {
    throw new Error('Admin user not found. Run main seed first.');
  }

  // Get regions
  const barbadosRegion = await prisma.region.findFirst({
    where: { name: 'Barbados' },
  });

  const jamaicaRegion = await prisma.region.findFirst({
    where: { name: 'Jamaica' },
  });

  if (!barbadosRegion || !jamaicaRegion) {
    console.warn('⚠️  Regions not found. Run seed-expansion first for better data.');
  }

  // Get ambassadors and youth for attendance
  const ambassador = await prisma.user.findFirst({
    where: { email: 'ambassador.bridgetown@codexdominion.app' },
  });

  const director = await prisma.user.findFirst({
    where: { email: 'director.barbados@codexdominion.app' },
  });

  // Get some youth users for attendance
  const youthUsers = await prisma.user.findMany({
    where: {
      roles: {
        some: {
          role: { name: RoleName.YOUTH },
        },
      },
    },
    take: 5,
  });

  console.log('🎭 Creating events...');

  // Event 1: Season Ceremony (Mastery)
  const seasonCeremony = await prisma.event.upsert({
    where: { id: 'season-ceremony-mastery-2025' },
    update: {},
    create: {
      id: 'season-ceremony-mastery-2025',
      title: 'Dawn Ceremony - Season of Mastery',
      description: 'A sacred gathering to honor the youth rising in mastery and leadership. This ceremony marks the transition into the Season of Mastery, where youth demonstrate their skills and prepare for their missions.',
      eventType: EventType.SEASON_CEREMONY,
      regionId: barbadosRegion?.id || null,
      scheduledAt: new Date('2025-03-21T18:00:00.000Z'), // March equinox
      createdBy: admin.id,
    },
  });
  console.log(`✅ Created: ${seasonCeremony.title}`);

  // Event 2: Ambassador Gathering
  const ambassadorEvent = await prisma.event.upsert({
    where: { id: 'ambassador-gathering-barbados-feb' },
    update: {},
    create: {
      id: 'ambassador-gathering-barbados-feb',
      title: 'Ambassador Gathering - Barbados',
      description: 'Monthly gathering for ambassadors to share insights, coordinate school outreach, and support circle captains. Includes workshop on leading cultural ceremonies.',
      eventType: EventType.AMBASSADOR_EVENT,
      regionId: barbadosRegion?.id || null,
      scheduledAt: new Date('2025-02-15T14:00:00.000Z'),
      createdBy: director?.id || admin.id,
    },
  });
  console.log(`✅ Created: ${ambassadorEvent.title}`);

  // Event 3: Youth Showcase
  const showcase = await prisma.event.upsert({
    where: { id: 'youth-showcase-jamaica-march' },
    update: {},
    create: {
      id: 'youth-showcase-jamaica-march',
      title: 'Creator Showcase - Jamaica',
      description: 'Youth and creators present their artifacts, missions, and cultural projects. Open to schools, families, and the diaspora community. Features music, storytelling, and digital creations.',
      eventType: EventType.SHOWCASE,
      regionId: jamaicaRegion?.id || null,
      scheduledAt: new Date('2025-03-08T16:00:00.000Z'),
      createdBy: admin.id,
    },
  });
  console.log(`✅ Created: ${showcase.title}`);

  // Event 4: Leadership Summit
  const summit = await prisma.event.upsert({
    where: { id: 'leadership-summit-2025' },
    update: {},
    create: {
      id: 'leadership-summit-2025',
      title: 'Caribbean Youth Leadership Summit',
      description: 'Annual gathering of youth captains, ambassadors, and regional directors from across the Caribbean. Three-day summit featuring workshops on circle leadership, cultural preservation, and digital sovereignty.',
      eventType: EventType.SUMMIT,
      regionId: null, // Multi-region event
      scheduledAt: new Date('2025-07-15T09:00:00.000Z'),
      createdBy: admin.id,
    },
  });
  console.log(`✅ Created: ${summit.title}`);

  // Event 5: Circle Ceremony (upcoming)
  const circleCeremony = await prisma.event.upsert({
    where: { id: 'circle-ceremony-harrison-jan' },
    update: {},
    create: {
      id: 'circle-ceremony-harrison-jan',
      title: 'Circle Opening Ceremony - Harrison College',
      description: 'Opening ceremony for new youth circle at Harrison College. Includes flame lighting ritual, youth oath, and first mission introduction.',
      eventType: EventType.CIRCLE_CEREMONY,
      regionId: barbadosRegion?.id || null,
      scheduledAt: new Date('2025-01-30T17:00:00.000Z'), // Past event for testing
      createdBy: ambassador?.id || admin.id,
    },
  });
  console.log(`✅ Created: ${circleCeremony.title}`);

  // Event 6: Community Launch
  const communityLaunch = await prisma.event.upsert({
    where: { id: 'community-launch-nyc-feb' },
    update: {},
    create: {
      id: 'community-launch-nyc-feb',
      title: 'Codex Dominion Launch - NYC Diaspora',
      description: 'Official launch event for NYC diaspora community. Open house introducing the Dominion, circle formation, and cultural celebration with Caribbean food and music.',
      eventType: EventType.COMMUNITY_EVENT,
      regionId: null, // NYC region if it exists
      scheduledAt: new Date('2025-02-22T18:30:00.000Z'),
      createdBy: admin.id,
    },
  });
  console.log(`✅ Created: ${communityLaunch.title}`);

  console.log('\n👥 Adding attendance records...');

  // Add attendance for past circle ceremony
  if (youthUsers.length > 0) {
    const attendancePromises = youthUsers.slice(0, 3).map((user, index) =>
      prisma.eventAttendance.upsert({
        where: {
          eventId_userId: {
            eventId: circleCeremony.id,
            userId: user.id,
          },
        },
        update: {},
        create: {
          eventId: circleCeremony.id,
          userId: user.id,
          status: index === 0 ? EventAttendanceStatus.PRESENT : EventAttendanceStatus.PRESENT,
          checkedInAt: new Date('2025-01-30T17:15:00.000Z'),
        },
      })
    );

    await Promise.all(attendancePromises);
    console.log(`✅ Added ${youthUsers.slice(0, 3).length} attendance records to circle ceremony`);
  }

  // Add registered attendance for upcoming season ceremony
  if (youthUsers.length > 3) {
    const registrations = youthUsers.slice(0, 4).map((user) =>
      prisma.eventAttendance.upsert({
        where: {
          eventId_userId: {
            eventId: seasonCeremony.id,
            userId: user.id,
          },
        },
        update: {},
        create: {
          eventId: seasonCeremony.id,
          userId: user.id,
          status: EventAttendanceStatus.REGISTERED,
          checkedInAt: null,
        },
      })
    );

    await Promise.all(registrations);
    console.log(`✅ Added ${youthUsers.slice(0, 4).length} registrations to season ceremony`);
  }

  console.log('\n🎭 Events Engine seed complete!');
  console.log(`   - 6 events created (ceremony, showcase, summit, community)`);
  console.log(`   - Attendance records added`);
  console.log(`   - Event types: SEASON_CEREMONY, AMBASSADOR_EVENT, SHOWCASE, SUMMIT, CIRCLE_CEREMONY, COMMUNITY_EVENT`);
}

main()
  .catch((e) => {
    console.error('❌ Error seeding events:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
