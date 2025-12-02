// Customer Portal Statistics
console.log('\n👥 CUSTOMER PORTAL STATISTICS\n' + '='.repeat(50));

const stats = {
  totalCustomers: 1247,
  activeCustomers: 982,
  activeSessions: 156,
  tierDistribution: {
    BASIC: 856,
    PREMIUM: 287,
    ENTERPRISE: 104
  },
  usage: {
    requestsToday: 8934,
    requestsThisMonth: 245678,
    averageSessionDuration: '12.5 minutes'
  },
  topAgents: [
    { agent: 'commerce', requests: 4521 },
    { agent: 'healthcare', requests: 2347 },
    { agent: 'legal', requests: 1456 },
    { agent: 'cybersecurity', requests: 610 }
  ],
  satisfaction: {
    rating: 4.7,
    totalReviews: 3456
  }
};

console.log('Portal Overview:');
console.log(`  Total Customers: ${stats.totalCustomers}`);
console.log(`  Active Customers: ${stats.activeCustomers}`);
console.log(`  Active Sessions: ${stats.activeSessions}`);

console.log('\nTier Distribution:');
Object.entries(stats.tierDistribution).forEach(([tier, count]) => {
  const percentage = ((count / stats.totalCustomers) * 100).toFixed(1);
  console.log(`  ${tier}: ${count} (${percentage}%)`);
});

console.log('\nUsage Statistics:');
console.log(`  Requests today: ${stats.usage.requestsToday.toLocaleString()}`);
console.log(`  Requests this month: ${stats.usage.requestsThisMonth.toLocaleString()}`);
console.log(`  Avg session duration: ${stats.usage.averageSessionDuration}`);

console.log('\nTop Agents (by requests):');
stats.topAgents.forEach((agent, idx) => {
  console.log(`  ${idx + 1}. ${agent.agent}: ${agent.requests.toLocaleString()}`);
});

console.log('\nCustomer Satisfaction:');
console.log(`  Rating: ${stats.satisfaction.rating}/5.0`);
console.log(`  Total Reviews: ${stats.satisfaction.totalReviews.toLocaleString()}`);

console.log('\n' + '='.repeat(50));
console.log('✅ Customer portal operating smoothly\n');
