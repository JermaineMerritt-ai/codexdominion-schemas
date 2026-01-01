/**
 * Daily Intelligence Job Orchestrator
 * 
 * Master function that runs all domain intelligence evaluations.
 * Called by IntelligenceSchedulerService at 6 AM daily.
 * 
 * Execution order:
 * 1. Circle Intelligence (C1-C7)
 * 2. Youth Intelligence (Y1-Y7)
 * 3. Mission Intelligence (M1-M7)
 * 4. Curriculum Intelligence (CU1-CU7)
 * 5. Culture Intelligence (CUL1-CUL7)
 * 6. Creator Intelligence (CR1-CR7)
 * 7. Expansion Intelligence (E1-E7)
 */

import { PrismaClient } from '@prisma/client';
import { runCircleIntelligence } from '../evaluators/circle-evaluators';
import { runYouthIntelligence } from '../evaluators/youth-evaluators';
import { runMissionIntelligence } from '../evaluators/mission-evaluators';
import { runCurriculumIntelligence } from '../evaluators/curriculum-evaluators';
import { runCultureIntelligence } from '../evaluators/culture-evaluators';
import { runCreatorIntelligence } from '../evaluators/creator-evaluators';
import { runExpansionIntelligence } from '../evaluators/expansion-evaluators';

/**
 * Run all domain intelligence evaluations and persist insights
 * 
 * @param prisma - Prisma client instance
 * @returns Object with counts of insights generated per domain
 */
export async function runDailyIntelligenceJob(prisma: PrismaClient) {
  console.log('[Intelligence] Starting daily intelligence job...');
  const startTime = Date.now();

  // Track insights generated per domain
  const results = {
    circles: 0,
    youth: 0,
    missions: 0,
    curriculum: 0,
    culture: 0,
    creators: 0,
    expansion: 0,
    total: 0,
  };

  try {
    // 1. Circle Intelligence (C1-C7)
    console.log('[Intelligence] Running Circle Intelligence...');
    const circleInsights = await runCircleIntelligence(prisma);
    results.circles = circleInsights.length;
    console.log(`[Intelligence] Generated ${results.circles} circle insights`);

    // 2. Youth Intelligence (Y1-Y7)
    console.log('[Intelligence] Running Youth Intelligence...');
    const youthInsights = await runYouthIntelligence(prisma);
    results.youth = youthInsights.length;
    console.log(`[Intelligence] Generated ${results.youth} youth insights`);

    // 3. Mission Intelligence (M1-M7)
    console.log('[Intelligence] Running Mission Intelligence...');
    const missionInsights = await runMissionIntelligence(prisma);
    results.missions = missionInsights.length;
    console.log(`[Intelligence] Generated ${results.missions} mission insights`);

    // 4. Curriculum Intelligence (CU1-CU7)
    console.log('[Intelligence] Running Curriculum Intelligence...');
    const curriculumInsights = await runCurriculumIntelligence(prisma);
    results.curriculum = curriculumInsights.length;
    console.log(`[Intelligence] Generated ${results.curriculum} curriculum insights`);

    // 5. Culture Intelligence (CUL1-CUL7)
    console.log('[Intelligence] Running Culture Intelligence...');
    const cultureInsights = await runCultureIntelligence(prisma);
    results.culture = cultureInsights.length;
    console.log(`[Intelligence] Generated ${results.culture} culture insights`);

    // 6. Creator Intelligence (CR1-CR7)
    console.log('[Intelligence] Running Creator Intelligence...');
    const creatorInsights = await runCreatorIntelligence(prisma);
    results.creators = creatorInsights.length;
    console.log(`[Intelligence] Generated ${results.creators} creator insights`);

    // 7. Expansion Intelligence (E1-E7)
    console.log('[Intelligence] Running Expansion Intelligence...');
    const expansionInsights = await runExpansionIntelligence(prisma);
    results.expansion = expansionInsights.length;
    console.log(`[Intelligence] Generated ${results.expansion} expansion insights`);

    // Calculate total
    results.total = 
      results.circles +
      results.youth +
      results.missions +
      results.curriculum +
      results.culture +
      results.creators +
      results.expansion;

    const duration = Date.now() - startTime;
    console.log(
      `[Intelligence] Daily job complete: ${results.total} insights generated in ${duration}ms`
    );

    return results;
  } catch (error) {
    console.error('[Intelligence] Daily job failed:', error);
    throw error;
  }
}
