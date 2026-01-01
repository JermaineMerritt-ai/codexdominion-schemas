import { PrismaClient, OutreachType, RoleName } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('🌍 Seeding Expansion Engine (Regions, Schools, Outreach)...\n');

  // Get admin and create ambassadors/regional directors
  const admin = await prisma.user.findFirst({
    where: { roles: { some: { role: { name: RoleName.ADMIN } } } },
  });

  if (!admin) {
    throw new Error('Admin user not found. Run main seed first.');
  }

  // Get or create Ambassador role
  const ambassadorRole = await prisma.role.upsert({
    where: { name: RoleName.AMBASSADOR },
    update: {},
    create: { name: RoleName.AMBASSADOR },
  });

  const regionalDirectorRole = await prisma.role.upsert({
    where: { name: RoleName.REGIONAL_DIRECTOR },
    update: {},
    create: { name: RoleName.REGIONAL_DIRECTOR },
  });

  // Create Regional Directors
  const barbadosDirector = await prisma.user.upsert({
    where: { email: 'director.barbados@codexdominion.app' },
    update: {},
    create: {
      email: 'director.barbados@codexdominion.app',
      passwordHash: '$2b$10$dummyHashForSeeding',
      firstName: 'Marcus',
      lastName: 'Thompson',
      dateOfBirth: new Date('1980-03-15'),
      roles: {
        create: { roleId: regionalDirectorRole.id },
      },
    },
  });

  const jamaicaDirector = await prisma.user.upsert({
    where: { email: 'director.jamaica@codexdominion.app' },
    update: {},
    create: {
      email: 'director.jamaica@codexdominion.app',
      passwordHash: '$2b$10$dummyHashForSeeding',
      firstName: 'Keisha',
      lastName: 'Brown',
      dateOfBirth: new Date('1985-07-22'),
      roles: {
        create: { roleId: regionalDirectorRole.id },
      },
    },
  });

  // Create Ambassadors
  const ambassador1 = await prisma.user.upsert({
    where: { email: 'ambassador.bridgetown@codexdominion.app' },
    update: {},
    create: {
      email: 'ambassador.bridgetown@codexdominion.app',
      passwordHash: '$2b$10$dummyHashForSeeding',
      firstName: 'Sarah',
      lastName: 'Williams',
      dateOfBirth: new Date('1995-05-10'),
      roles: {
        create: { roleId: ambassadorRole.id },
      },
    },
  });

  const ambassador2 = await prisma.user.upsert({
    where: { email: 'ambassador.kingston@codexdominion.app' },
    update: {},
    create: {
      email: 'ambassador.kingston@codexdominion.app',
      passwordHash: '$2b$10$dummyHashForSeeding',
      firstName: 'Dwayne',
      lastName: 'Campbell',
      dateOfBirth: new Date('1992-11-18'),
      roles: {
        create: { roleId: ambassadorRole.id },
      },
    },
  });

  console.log('✅ Created Regional Directors and Ambassadors\n');

  // Create Regions
  const barbadosRegion = await prisma.region.upsert({
    where: { id: 'barbados-region-001' },
    update: {},
    create: {
      id: 'barbados-region-001',
      name: 'Barbados',
      country: 'Barbados',
      timezone: 'America/Barbados',
      directorId: barbadosDirector.id,
    },
  });

  const jamaicaRegion = await prisma.region.upsert({
    where: { id: 'jamaica-region-001' },
    update: {},
    create: {
      id: 'jamaica-region-001',
      name: 'Jamaica',
      country: 'Jamaica',
      timezone: 'America/Jamaica',
      directorId: jamaicaDirector.id,
    },
  });

  const nycDiasporaRegion = await prisma.region.upsert({
    where: { id: 'nyc-diaspora-001' },
    update: {},
    create: {
      id: 'nyc-diaspora-001',
      name: 'NYC Diaspora',
      country: 'United States',
      timezone: 'America/New_York',
      directorId: null,
    },
  });

  console.log('✅ Created 3 Regions (Barbados, Jamaica, NYC Diaspora)\n');

  // Create Schools
  const harrisonCollege = await prisma.school.create({
    data: {
      regionId: barbadosRegion.id,
      name: 'Harrison College',
      address: 'Crumpton St, Bridgetown, Barbados',
      contactPerson: 'Principal Jennifer Clarke',
    },
  });

  const queenCollege = await prisma.school.create({
    data: {
      regionId: barbadosRegion.id,
      name: 'Queen\'s College',
      address: 'Husbands, St. James, Barbados',
      contactPerson: 'Principal Robert Armstrong',
    },
  });

  const wolmersSchool = await prisma.school.create({
    data: {
      regionId: jamaicaRegion.id,
      name: 'Wolmer\'s Boys\' School',
      address: 'Heroes Circle, Kingston, Jamaica',
      contactPerson: 'Principal Michael Edwards',
    },
  });

  const camperdownSchool = await prisma.school.create({
    data: {
      regionId: jamaicaRegion.id,
      name: 'Camperdown High School',
      address: 'Mannings Hill Rd, Kingston, Jamaica',
      contactPerson: 'Principal Grace Johnson',
    },
  });

  const brooklynYouth = await prisma.school.create({
    data: {
      regionId: nycDiasporaRegion.id,
      name: 'Brooklyn Caribbean Youth Center',
      address: '1234 Flatbush Ave, Brooklyn, NY',
      contactPerson: 'Director Trevor Morgan',
    },
  });

  console.log('✅ Created 5 Schools across 3 regions\n');

  // Create Outreach Records
  await prisma.ambassadorOutreach.createMany({
    data: [
      {
        ambassadorId: ambassador1.id,
        regionId: barbadosRegion.id,
        schoolId: harrisonCollege.id,
        type: OutreachType.VISIT,
        notes: 'Initial visit - met with principal and 3 teachers. Discussed Youth Circle integration.',
        date: new Date('2025-01-10'),
      },
      {
        ambassadorId: ambassador1.id,
        regionId: barbadosRegion.id,
        schoolId: harrisonCollege.id,
        type: OutreachType.MEETING,
        notes: 'Follow-up meeting with teachers. Scheduled pilot Youth Circle for February.',
        date: new Date('2025-01-17'),
      },
      {
        ambassadorId: ambassador1.id,
        regionId: barbadosRegion.id,
        schoolId: queenCollege.id,
        type: OutreachType.VISIT,
        notes: 'First contact with Queen\'s College. Principal very interested in homeschool curriculum.',
        date: new Date('2025-01-12'),
      },
      {
        ambassadorId: ambassador2.id,
        regionId: jamaicaRegion.id,
        schoolId: wolmersSchool.id,
        type: OutreachType.EVENT,
        notes: 'Hosted info session for 40 students. Demonstrated Mission Engine and Creator Dashboard.',
        date: new Date('2025-01-15'),
      },
      {
        ambassadorId: ambassador2.id,
        regionId: jamaicaRegion.id,
        schoolId: camperdownSchool.id,
        type: OutreachType.VISIT,
        notes: 'Exploratory visit. Principal requested proposal for school-wide Youth Circle program.',
        date: new Date('2025-01-20'),
      },
      {
        ambassadorId: ambassador2.id,
        regionId: jamaicaRegion.id,
        schoolId: null, // Community event, not school-specific
        type: OutreachType.EVENT,
        notes: 'Community youth gathering in Kingston - 60 attendees, 12 new sign-ups.',
        date: new Date('2025-01-25'),
      },
    ],
  });

  console.log('✅ Created 6 Outreach Records\n');

  console.log('🔥 EXPANSION ENGINE SEEDED SUCCESSFULLY!\n');
  console.log('Summary:');
  console.log('  - 3 Regions (Barbados, Jamaica, NYC Diaspora)');
  console.log('  - 2 Regional Directors');
  console.log('  - 2 Ambassadors');
  console.log('  - 5 Schools');
  console.log('  - 6 Outreach Records');
  console.log('\nRegional Directors:');
  console.log(`  - ${barbadosDirector.firstName} ${barbadosDirector.lastName} (Barbados)`);
  console.log(`  - ${jamaicaDirector.firstName} ${jamaicaDirector.lastName} (Jamaica)`);
  console.log('\nAmbassadors:');
  console.log(`  - ${ambassador1.firstName} ${ambassador1.lastName} (Bridgetown)`);
  console.log(`  - ${ambassador2.firstName} ${ambassador2.lastName} (Kingston)`);
}

main()
  .catch((e) => {
    console.error('❌ Seeding failed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
