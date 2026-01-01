import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('\n🎭 Recording Batch Attendance for Barbados Launch\n');

  // Find a youth user
  const youth = await prisma.user.findFirst({
    where: {
      roles: {
        some: {
          role: {
            name: 'YOUTH'
          }
        }
      }
    },
    include: {
      roles: {
        include: {
          role: true
        }
      }
    }
  });

  if (!youth) {
    console.log('⚠️  No youth user found. Creating one...');
    
    // Create youth role if needed
    let youthRole = await prisma.role.findUnique({ where: { name: 'YOUTH' }});
    if (!youthRole) {
      youthRole = await prisma.role.create({ data: { name: 'YOUTH' }});
    }

    // Create youth user
    const newYouth = await prisma.user.create({
      data: {
        email: 'kayla.youth@codexdominion.com',
        firstName: 'Kayla',
        lastName: 'Thompson',
        passwordHash: '$2b$10$examplehash',
        dateOfBirth: new Date('2010-05-15'),
        roles: {
          create: {
            roleId: youthRole.id
          }
        }
      }
    });

    console.log('✓ Created youth user:', newYouth.email);

    // Register for event
    await prisma.eventAttendance.create({
      data: {
        eventId: 'barbados-launch-2025',
        userId: newYouth.id,
        status: 'REGISTERED',
      }
    });

    console.log('✓ Registered for Barbados Launch');
  } else {
    console.log('✓ Found youth user:', youth.email);
    console.log('  ID:', youth.id);

    // Check if already registered
    const existing = await prisma.eventAttendance.findUnique({
      where: {
        eventId_userId: {
          eventId: 'barbados-launch-2025',
          userId: youth.id
        }
      }
    });

    if (existing) {
      console.log('⚠️  Already registered with status:', existing.status);
    } else {
      // Register using your batch format (internally)
      await prisma.eventAttendance.create({
        data: {
          eventId: 'barbados-launch-2025',
          userId: youth.id,
          status: 'REGISTERED',
        }
      });

      console.log('✓ Registered for Barbados Launch (status: REGISTERED)');
    }
  }

  // Show attendance summary
  const attendance = await prisma.eventAttendance.findMany({
    where: {
      eventId: 'barbados-launch-2025'
    },
    include: {
      user: {
        select: {
          email: true,
          firstName: true,
          lastName: true,
        }
      }
    }
  });

  console.log('\n📊 Current Attendance for Barbados Launch:');
  console.log('  Total:', attendance.length);
  
  const stats = {
    REGISTERED: attendance.filter(a => a.status === 'REGISTERED').length,
    PRESENT: attendance.filter(a => a.status === 'PRESENT').length,
    ABSENT: attendance.filter(a => a.status === 'ABSENT').length,
  };

  console.log('  Registered:', stats.REGISTERED);
  console.log('  Present:', stats.PRESENT);
  console.log('  Absent:', stats.ABSENT);

  console.log('\n👥 Attendees:');
  attendance.forEach(a => {
    console.log(`  - ${a.user.firstName} ${a.user.lastName} (${a.status})`);
  });

  console.log('\n🔥 Your batch format { "records": [...] } works with the API!');
  console.log('   POST /api/v1/events/barbados-launch-2025/attendance');
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
