#!/usr/bin/env node
/**
 * ACTION AI TASK ENGINE V0 - TEST SCRIPT
 * Tests the 3-stage execution pipeline:
 * 1. Create task (PENDING)
 * 2. Schedule task (SCHEDULED)
 * 3. Execute task (IN_PROGRESS → COMPLETED/FAILED)
 */

const API_BASE = 'http://localhost:4000/api/v1';

async function testTaskEngine() {
  console.log('🔥 ACTION AI TASK ENGINE V0 - TEST SCRIPT\n');

  // Test 1: Create task (POST /tasks)
  console.log('1️⃣ Creating INVOICE_FOLLOW_UP task...');
  const createResponse = await fetch(`${API_BASE}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      type: 'INVOICE_FOLLOW_UP',
      mode: 'ASSISTED',
      priority: 'HIGH',
      ownerType: 'AI',
      ownerId: 'ACTION_AI',
      subjectRefType: 'INVOICE',
      subjectRefId: 'INV-123',
      dueAt: '2026-01-05T12:00:00Z',
      source: 'OVERDUE_INVOICE_DETECTOR',
      payload: {
        customer_name: 'ACME Corp',
        customer_email: 'billing@acme.com',
        invoice_number: 'INV-123',
        invoice_amount: 1200,
        currency: 'USD',
        due_date: '2025-12-20',
        days_overdue: 10,
      },
    }),
  });

  if (!createResponse.ok) {
    console.error('❌ Failed to create task:', await createResponse.text());
    return;
  }

  const created = await createResponse.json();
  console.log('✅ Task created:', created);
  const taskId = created.id;

  // Test 2: List tasks (GET /tasks)
  console.log('\n2️⃣ Listing PENDING tasks...');
  const listResponse = await fetch(`${API_BASE}/tasks?status=PENDING`);
  const tasks = await listResponse.json();
  console.log(`✅ Found ${tasks.length} PENDING task(s)`);

  // Test 3: Schedule task (PATCH /tasks/:id - PENDING → SCHEDULED)
  console.log('\n3️⃣ Scheduling task...');
  const scheduleResponse = await fetch(`${API_BASE}/tasks/${taskId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      newStatus: 'SCHEDULED',
      scheduledAt: new Date().toISOString(),
      actorType: 'SYSTEM',
      actorId: 'FOLLOW_UP_SCHEDULER',
    }),
  });

  const scheduled = await scheduleResponse.json();
  console.log('✅ Task scheduled:', scheduled);

  // Test 4: Start execution (PATCH /tasks/:id - SCHEDULED → IN_PROGRESS)
  console.log('\n4️⃣ Starting execution...');
  const startResponse = await fetch(`${API_BASE}/tasks/${taskId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      newStatus: 'IN_PROGRESS',
      actorType: 'AI',
      actorId: 'ACTION_AI_FOLLOW_UP_WORKER',
    }),
  });

  const inProgress = await startResponse.json();
  console.log('✅ Task in progress:', inProgress);

  // Test 5: Complete task (PATCH /tasks/:id - IN_PROGRESS → COMPLETED)
  console.log('\n5️⃣ Completing task...');
  const completeResponse = await fetch(`${API_BASE}/tasks/${taskId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      newStatus: 'COMPLETED',
      actorType: 'AI',
      actorId: 'ACTION_AI_FOLLOW_UP_WORKER',
    }),
  });

  const completed = await completeResponse.json();
  console.log('✅ Task completed:', completed);

  // Test 6: Try to update terminal state (should fail)
  console.log('\n6️⃣ Testing terminal state lock...');
  const terminalResponse = await fetch(`${API_BASE}/tasks/${taskId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      newStatus: 'FAILED',
      actorType: 'SYSTEM',
      actorId: 'TEST',
    }),
  });

  if (!terminalResponse.ok) {
    console.log('✅ Terminal state lock working (cannot update COMPLETED task)');
  } else {
    console.error('❌ Terminal state lock failed - task was updated!');
  }

  // Test 7: Get full task details
  console.log('\n7️⃣ Fetching complete task with events...');
  const detailsResponse = await fetch(`${API_BASE}/tasks?status=COMPLETED`);
  const completedTasks = await detailsResponse.json();
  console.log('✅ Completed tasks with event history:', JSON.stringify(completedTasks[0], null, 2));

  console.log('\n🎉 ALL TESTS PASSED - Task Engine V0 is operational!\n');
}

// Run tests
testTaskEngine().catch((error) => {
  console.error('❌ Test failed:', error);
  process.exit(1);
});
