import { PrismaClient } from '@prisma/client';
import * as bcrypt from 'bcrypt';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Starting database seed...');

  // First, create roles
  console.log('👑 Seeding roles...');
  const roles = await Promise.all([
    prisma.role.upsert({
      where: { name: 'YOUTH' },
      update: {},
      create: { name: 'YOUTH' },
    }),
    prisma.role.upsert({
      where: { name: 'YOUTH_CAPTAIN' },
      update: {},
      create: { name: 'YOUTH_CAPTAIN' },
    }),
    prisma.role.upsert({
      where: { name: 'AMBASSADOR' },
      update: {},
      create: { name: 'AMBASSADOR' },
    }),
    prisma.role.upsert({
      where: { name: 'CREATOR' },
      update: {},
      create: { name: 'CREATOR' },
    }),
    prisma.role.upsert({
      where: { name: 'EDUCATOR' },
      update: {},
      create: { name: 'EDUCATOR' },
    }),
    prisma.role.upsert({
      where: { name: 'REGIONAL_DIRECTOR' },
      update: {},
      create: { name: 'REGIONAL_DIRECTOR' },
    }),
    prisma.role.upsert({
      where: { name: 'COUNCIL' },
      update: {},
      create: { name: 'COUNCIL' },
    }),
    prisma.role.upsert({
      where: { name: 'ADMIN' },
      update: {},
      create: { name: 'ADMIN' },
    }),
  ]);
  console.log(`✅ Created ${roles.length} roles`);

  // Seed Seasons
  console.log('📅 Seeding seasons...');
  const seasons = await Promise.all([
    prisma.season.upsert({
      where: { name: 'IDENTITY' },
      update: {},
      create: {
        name: 'IDENTITY',
        startDate: new Date('2025-01-01'),
        endDate: new Date('2025-03-31'),
      },
    }),
    prisma.season.upsert({
      where: { name: 'MASTERY' },
      update: {},
      create: {
        name: 'MASTERY',
        startDate: new Date('2025-04-01'),
        endDate: new Date('2025-06-30'),
      },
    }),
    prisma.season.upsert({
      where: { name: 'CREATION' },
      update: {},
      create: {
        name: 'CREATION',
        startDate: new Date('2025-07-01'),
        endDate: new Date('2025-09-30'),
      },
    }),
    prisma.season.upsert({
      where: { name: 'LEADERSHIP' },
      update: {},
      create: {
        name: 'LEADERSHIP',
        startDate: new Date('2025-10-01'),
        endDate: new Date('2025-12-31'),
      },
    }),
  ]);
  console.log(`✅ Created ${seasons.length} seasons`);

  // Hash passwords
  const hashedPassword = await bcrypt.hash('password123', 10);
  
  // Seed Users
  console.log('👤 Seeding users...');
  
  // Admin user
  const adminUser = await prisma.user.upsert({
    where: { email: 'admin@codexdominion.com' },
    update: {},
    create: {
      email: 'admin@codexdominion.com',
      passwordHash: hashedPassword,
      firstName: 'Admin',
      lastName: 'User',
      status: 'ACTIVE',
      roles: {
        create: [
          { role: { connect: { name: 'ADMIN' } } },
        ],
      },
      profile: {
        create: {
          risePath: 'LEADERSHIP',
          bio: 'System administrator for Codex Dominion',
        },
      },
    },
  });
  console.log(`✅ Created admin user: ${adminUser.email}`);

  // Youth Captain
  const captainUser = await prisma.user.upsert({
    where: { email: 'captain@codexdominion.com' },
    update: {},
    create: {
      email: 'captain@codexdominion.com',
      passwordHash: hashedPassword,
      firstName: 'Captain',
      lastName: 'Leader',
      dateOfBirth: new Date('1995-06-15'),
      status: 'ACTIVE',
      roles: {
        create: [
          { role: { connect: { name: 'YOUTH_CAPTAIN' } } },
        ],
      },
      profile: {
        create: {
          risePath: 'LEADERSHIP',
          bio: 'Youth circle captain passionate about empowering the next generation',
        },
      },
    },
  });
  console.log(`✅ Created youth captain: ${captainUser.email}`);

  // Youth member
  const youthUser = await prisma.user.upsert({
    where: { email: 'youth@codexdominion.com' },
    update: {},
    create: {
      email: 'youth@codexdominion.com',
      passwordHash: hashedPassword,
      firstName: 'Young',
      lastName: 'Leader',
      dateOfBirth: new Date('2008-03-20'),
      status: 'ACTIVE',
      roles: {
        create: [
          { role: { connect: { name: 'YOUTH' } } },
        ],
      },
      profile: {
        create: {
          risePath: 'IDENTITY',
          bio: 'Youth member on identity journey',
        },
      },
    },
  });
  console.log(`✅ Created youth user: ${youthUser.email}`);

  // Seed Cultural Story
  console.log('📖 Seeding cultural story...');
  const story = await prisma.culturalStory.create({
    data: {
      title: 'The Story of the Flame',
      content: JSON.stringify({
        format: 'markdown',
        body: '## The Eternal Flame\n\nLong ago, our ancestors kept a flame burning that represented the continuity of our people. This flame symbolizes:\n- Continuity across generations\n- Hope in difficult times\n- Unity among all diaspora\n- The sovereign spirit of our nation\n\nToday, we carry that flame forward in a new form - through the Codex Dominion.',
      }),
      season: {
        connect: { name: 'IDENTITY' },
      },
      week: 1,
    },
  });
  console.log(`✅ Created cultural story: ${story.title}`);

  // Seed Mission
  console.log('🎯 Seeding mission...');
  const mission = await prisma.mission.create({
    data: {
      title: 'Discover Your Identity',
      description: 'Reflect on your cultural roots and write a personal story about what diaspora means to you.',
      season: {
        connect: { name: 'IDENTITY' },
      },
      month: 1,
      week: 1,
      type: 'GLOBAL',
    },
  });
  console.log(`✅ Created mission: ${mission.title}`);

  console.log('🔥 Seed completed successfully! The flame burns eternal!');
}

main()
  .catch((e) => {
    console.error('❌ Error seeding database:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
