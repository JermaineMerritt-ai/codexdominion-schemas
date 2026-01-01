import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('\n🎭 Creating Barbados Launch Event...\n');

  // Find Barbados region
  const barbados = await prisma.region.findFirst({
    where: { 
      OR: [
        { name: { contains: 'Barbados', mode: 'insensitive' }},
        { id: 'barbados' }
      ]
    }
  });

  if (!barbados) {
    console.log('⚠️  Barbados region not found, creating one...');
    // Create Barbados region if it doesn't exist
    const newBarbados = await prisma.region.create({
      data: {
        id: 'barbados',
        name: 'Barbados',
        country: 'Barbados',
        timezone: 'America/Barbados',
      }
    });
    console.log('✓ Created Barbados region:', newBarbados.id);
  }

  // Find an admin user to be the creator
  const admin = await prisma.user.findFirst({
    where: {
      roles: {
        some: {
          role: {
            name: 'ADMIN'
          }
        }
      }
    }
  });

  if (!admin) {
    console.log('❌ No admin user found! Run main seed script first.');
    return;
  }

  // Check if event already exists
  const existing = await prisma.event.findFirst({
    where: {
      title: 'CodexDominion Barbados Launch'
    }
  });

  if (existing) {
    console.log('⚠️  Event already exists:', existing.id);
    console.log('   Title:', existing.title);
    console.log('   Scheduled:', existing.scheduledAt);
    return;
  }

  // Create the Barbados Launch event
  const event = await prisma.event.create({
    data: {
      id: 'barbados-launch-2025',
      title: 'CodexDominion Barbados Launch',
      description: 'Unity ceremony + mission kickoff',
      eventType: 'LAUNCH',
      regionId: barbados?.id || 'barbados',
      scheduledAt: new Date('2025-03-01T16:00:00Z'),
      createdBy: admin.id,
    }
  });

  // Fetch full details for display
  const fullEvent = await prisma.event.findUnique({
    where: { id: event.id },
    include: {
      region: true,
      creator: {
        select: {
          email: true,
          firstName: true,
          lastName: true,
        }
      }
    }
  });

  console.log('✅ Barbados Launch Event Created!\n');
  console.log('Event Details:');
  console.log('  ID:', fullEvent?.id);
  console.log('  Title:', fullEvent?.title);
  console.log('  Type:', fullEvent?.eventType);
  console.log('  Region:', fullEvent?.region?.name);
  console.log('  Scheduled:', fullEvent?.scheduledAt.toLocaleString());
  console.log('  Created by:', fullEvent?.creator?.email);
  console.log('\n🔥 Access at: GET /api/v1/events/' + event.id);
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
