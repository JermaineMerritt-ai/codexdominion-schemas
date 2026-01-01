# 🔱 The Dominion Exchange — MVP Implementation Specification

**Version**: 1.0.0  
**Status**: Ready for Implementation  
**Architecture**: CodexDominion 2.0 Integration  
**Estimated Timeline**: 4-6 weeks (MVP)

---

## 📐 Architecture Overview

The Dominion Exchange is a **NestJS module** within the existing CodexDominion backend, following the established patterns:

```
backend/src/
├── markets/                     # New Markets Module
│   ├── markets.module.ts
│   ├── markets.controller.ts
│   ├── markets.service.ts
│   ├── dto/
│   │   ├── heatmap.dto.ts
│   │   ├── screener.dto.ts
│   │   ├── earnings.dto.ts
│   │   └── risk.dto.ts
│   └── providers/
│       ├── alphavantage.provider.ts
│       ├── finnhub.provider.ts
│       └── cache.provider.ts
├── academy/                     # New Academy Module
│   ├── academy.module.ts
│   ├── academy.controller.ts
│   ├── academy.service.ts
│   └── dto/
│       ├── path.dto.ts
│       ├── lesson.dto.ts
│       └── progress.dto.ts
└── app.module.ts               # Import MarketsModule, AcademyModule
```

---

## 🗄️ Database Schema (Prisma Models)

### Phase 1: Core Models

```prisma
// ============================================
// MARKETS REALM
// ============================================

model Screener {
  id          String   @id @default(uuid())
  userId      String
  name        String
  description String?
  filters     Json     // { sector: 'tech', pe_min: 10, pe_max: 30 }
  isPublic    Boolean  @default(false)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  
  user        User     @relation(fields: [userId], references: [id])
  runs        ScreenerRun[]
  
  @@map("screeners")
}

model ScreenerRun {
  id          String   @id @default(uuid())
  screenerId  String
  results     Json     // Array of ticker results
  resultCount Int
  executedAt  DateTime @default(now())
  
  screener    Screener @relation(fields: [screenerId], references: [id])
  
  @@map("screener_runs")
}

model MarketWatchlist {
  id        String   @id @default(uuid())
  userId    String
  name      String
  tickers   String[] // ['AAPL', 'MSFT', 'TSLA']
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  user      User     @relation(fields: [userId], references: [id])
  
  @@map("market_watchlists")
}

model EarningsAlert {
  id          String   @id @default(uuid())
  userId      String
  ticker      String
  earningsDate DateTime
  alertSent   Boolean  @default(false)
  createdAt   DateTime @default(now())
  
  user        User     @relation(fields: [userId], references: [id])
  
  @@map("earnings_alerts")
}

model PortfolioAnalysis {
  id          String   @id @default(uuid())
  userId      String
  name        String
  positions   Json     // [{ ticker: 'AAPL', shares: 10, cost_basis: 150 }]
  riskMetrics Json     // { volatility, sharpe, beta, correlation_matrix }
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  
  user        User     @relation(fields: [userId], references: [id])
  
  @@map("portfolio_analyses")
}

// ============================================
// ACADEMY REALM (Wealth Curriculum)
// ============================================

model AcademyPath {
  id          String   @id @default(uuid())
  name        String   // 'Beginner', 'Intermediate', 'Advanced'
  level       AcademyLevel
  description String
  sequence    Int      // Display order
  createdAt   DateTime @default(now())
  
  lessons     AcademyLesson[]
  
  @@map("academy_paths")
}

model AcademyLesson {
  id          String   @id @default(uuid())
  pathId      String
  title       String
  content     String   @db.Text
  objectives  String[] // Learning objectives
  duration    Int      // Minutes
  sequence    Int      // Order in path
  quizId      String?
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  
  path        AcademyPath @relation(fields: [pathId], references: [id])
  quiz        AcademyQuiz? @relation(fields: [quizId], references: [id])
  progress    LessonProgress[]
  
  @@map("academy_lessons")
}

model AcademyQuiz {
  id          String   @id @default(uuid())
  title       String
  questions   Json     // [{ question, options: [], correct_index, explanation }]
  passingScore Int     @default(70)
  createdAt   DateTime @default(now())
  
  lessons     AcademyLesson[]
  attempts    QuizAttempt[]
  
  @@map("academy_quizzes")
}

model LessonProgress {
  userId      String
  lessonId    String
  completed   Boolean  @default(false)
  timeSpent   Int      @default(0) // Seconds
  lastAccessed DateTime @default(now())
  
  user        User          @relation(fields: [userId], references: [id])
  lesson      AcademyLesson @relation(fields: [lessonId], references: [id])
  
  @@id([userId, lessonId])
  @@map("lesson_progress")
}

model QuizAttempt {
  id          String   @id @default(uuid())
  userId      String
  quizId      String
  score       Int      // Percentage
  answers     Json     // User's answers
  passed      Boolean
  attemptedAt DateTime @default(now())
  
  user        User         @relation(fields: [userId], references: [id])
  quiz        AcademyQuiz  @relation(fields: [quizId], references: [id])
  
  @@map("quiz_attempts")
}

model MarketGlossary {
  id          String   @id @default(uuid())
  term        String   @unique
  definition  String   @db.Text
  category    String   // 'basics', 'technical', 'fundamental', 'risk'
  examples    String[]
  createdAt   DateTime @default(now())
  
  @@map("market_glossary")
}

// ============================================
// ENUMS
// ============================================

enum AcademyLevel {
  BEGINNER
  INTERMEDIATE
  ADVANCED
  MASTER
}
```

### User Model Updates

```prisma
model User {
  // ... existing fields ...
  
  // Markets Relations
  screeners          Screener[]
  watchlists         MarketWatchlist[]
  earningsAlerts     EarningsAlert[]
  portfolioAnalyses  PortfolioAnalysis[]
  
  // Academy Relations
  lessonProgress     LessonProgress[]
  quizAttempts       QuizAttempt[]
}
```

---

## 🎯 MVP Feature 1: Market Heatmap

### Backend Implementation

**Controller**: `backend/src/markets/markets.controller.ts`

```typescript
import { Controller, Get, Query, UseGuards } from '@nestjs/common';
import { ApiTags, ApiBearerAuth, ApiQuery } from '@nestjs/swagger';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { MarketsService } from './markets.service';
import { HeatmapQueryDto } from './dto/heatmap.dto';

@ApiTags('markets')
@ApiBearerAuth()
@Controller('markets')
@UseGuards(JwtAuthGuard)
export class MarketsController {
  constructor(private readonly marketsService: MarketsService) {}

  @Get('heatmap')
  @ApiQuery({ name: 'timeframe', enum: ['1D', '1W', '1M', '3M', '1Y'], required: false })
  @ApiQuery({ name: 'index', enum: ['SP500', 'NASDAQ', 'DOW', 'ALL'], required: false })
  async getHeatmap(@Query() query: HeatmapQueryDto) {
    return this.marketsService.getHeatmap(query);
  }

  @Get('pulse')
  async getDominionPulse() {
    return this.marketsService.calculateDominionPulse();
  }
}
```

**Service**: `backend/src/markets/markets.service.ts`

```typescript
import { Injectable, Logger } from '@nestjs/common';
import { AlphaVantageProvider } from './providers/alphavantage.provider';
import { CacheProvider } from './providers/cache.provider';
import { HeatmapQueryDto } from './dto/heatmap.dto';

@Injectable()
export class MarketsService {
  private readonly logger = new Logger(MarketsService.name);

  constructor(
    private readonly alphaVantage: AlphaVantageProvider,
    private readonly cache: CacheProvider,
  ) {}

  async getHeatmap(query: HeatmapQueryDto) {
    const cacheKey = `heatmap:${query.timeframe}:${query.index}`;
    
    // Check cache (5 minutes)
    const cached = await this.cache.get(cacheKey);
    if (cached) return cached;

    // Fetch sector performance
    const sectors = await this.alphaVantage.getSectorPerformance();
    
    // Transform to heatmap format
    const heatmap = {
      sectors: sectors.map(sector => ({
        name: sector.name,
        performance: sector.performance,
        size: sector.marketCap,
        color: this.getColorForPerformance(sector.performance),
        fundamentals: {
          pe: sector.avgPE,
          volume: sector.totalVolume,
          advancers: sector.advancers,
          decliners: sector.decliners,
        },
      })),
      pulse: await this.calculateDominionPulse(),
      timestamp: new Date().toISOString(),
    };

    // Cache for 5 minutes
    await this.cache.set(cacheKey, heatmap, 300);

    return heatmap;
  }

  async calculateDominionPulse(): Promise<{
    score: number;
    sentiment: 'bullish' | 'neutral' | 'bearish';
    signals: string[];
  }> {
    // Proprietary "Dominion Pulse" calculation
    // Combines: VIX, advance/decline ratio, sector breadth, volume
    
    const vix = await this.alphaVantage.getVIX();
    const advanceDecline = await this.alphaVantage.getAdvanceDeclineRatio();
    const sectorBreadth = await this.alphaVantage.getSectorBreadth();
    
    const score = this.calculatePulseScore(vix, advanceDecline, sectorBreadth);
    
    return {
      score: Math.round(score),
      sentiment: score > 60 ? 'bullish' : score < 40 ? 'bearish' : 'neutral',
      signals: this.generatePulseSignals(score, vix, advanceDecline),
    };
  }

  private getColorForPerformance(performance: number): string {
    if (performance > 2) return '#00ff00';
    if (performance > 0) return '#90ff90';
    if (performance > -2) return '#ff9090';
    return '#ff0000';
  }

  private calculatePulseScore(vix: number, adRatio: number, breadth: number): number {
    // Weighted formula
    const vixScore = Math.max(0, 100 - vix * 5); // Lower VIX = higher score
    const adScore = Math.min(100, adRatio * 100); // Higher ratio = higher score
    const breadthScore = breadth; // Percentage of sectors advancing
    
    return (vixScore * 0.3 + adScore * 0.4 + breadthScore * 0.3);
  }

  private generatePulseSignals(score: number, vix: number, adRatio: number): string[] {
    const signals: string[] = [];
    
    if (vix < 15) signals.push('Low volatility environment');
    if (vix > 25) signals.push('Elevated risk levels');
    if (adRatio > 1.5) signals.push('Strong market breadth');
    if (adRatio < 0.7) signals.push('Weak market breadth');
    if (score > 70) signals.push('Market momentum accelerating');
    if (score < 30) signals.push('Defensive positioning advised');
    
    return signals;
  }
}
```

**DTO**: `backend/src/markets/dto/heatmap.dto.ts`

```typescript
import { IsEnum, IsOptional } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class HeatmapQueryDto {
  @ApiProperty({ enum: ['1D', '1W', '1M', '3M', '1Y'], default: '1D' })
  @IsEnum(['1D', '1W', '1M', '3M', '1Y'])
  @IsOptional()
  timeframe?: '1D' | '1W' | '1M' | '3M' | '1Y' = '1D';

  @ApiProperty({ enum: ['SP500', 'NASDAQ', 'DOW', 'ALL'], default: 'ALL' })
  @IsEnum(['SP500', 'NASDAQ', 'DOW', 'ALL'])
  @IsOptional()
  index?: 'SP500' | 'NASDAQ' | 'DOW' | 'ALL' = 'ALL';
}
```

### Frontend Component

**Component**: `frontend/src/components/markets/MarketHeatmap.tsx`

```tsx
'use client';

import { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Treemap, ResponsiveContainer } from 'recharts';

interface HeatmapSector {
  name: string;
  performance: number;
  size: number;
  color: string;
  fundamentals: {
    pe: number;
    volume: number;
    advancers: number;
    decliners: number;
  };
}

interface HeatmapData {
  sectors: HeatmapSector[];
  pulse: {
    score: number;
    sentiment: 'bullish' | 'neutral' | 'bearish';
    signals: string[];
  };
  timestamp: string;
}

export function MarketHeatmap() {
  const [timeframe, setTimeframe] = useState<'1D' | '1W' | '1M' | '3M' | '1Y'>('1D');

  const { data, isLoading } = useQuery<HeatmapData>({
    queryKey: ['heatmap', timeframe],
    queryFn: async () => {
      const response = await fetch(
        `/api/v1/markets/heatmap?timeframe=${timeframe}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      return response.json();
    },
    refetchInterval: 60000, // Refresh every minute
  });

  if (isLoading) return <div className="animate-pulse">Loading terrain...</div>;

  return (
    <div className="market-heatmap">
      {/* Dominion Pulse Indicator */}
      <div className="pulse-indicator">
        <h3>Dominion Pulse</h3>
        <div className={`pulse-score pulse-${data.pulse.sentiment}`}>
          {data.pulse.score}
        </div>
        <div className="pulse-signals">
          {data.pulse.signals.map((signal, i) => (
            <span key={i} className="signal-badge">{signal}</span>
          ))}
        </div>
      </div>

      {/* Timeframe Selector */}
      <div className="timeframe-selector">
        {['1D', '1W', '1M', '3M', '1Y'].map(tf => (
          <button
            key={tf}
            onClick={() => setTimeframe(tf as any)}
            className={timeframe === tf ? 'active' : ''}
          >
            {tf}
          </button>
        ))}
      </div>

      {/* Heatmap Visualization */}
      <ResponsiveContainer width="100%" height={600}>
        <Treemap
          data={data.sectors}
          dataKey="size"
          aspectRatio={4 / 3}
          stroke="#fff"
          fill="#8884d8"
        >
          {data.sectors.map((sector, index) => (
            <Cell key={index} fill={sector.color} />
          ))}
        </Treemap>
      </ResponsiveContainer>

      {/* Hover Card Details */}
      <div className="sector-details">
        {/* Show fundamentals on hover */}
      </div>
    </div>
  );
}
```

---

## 🎯 MVP Feature 2: Screener Pro

### Backend Implementation

**Endpoints**:
- `POST /markets/screeners` - Create screener
- `GET /markets/screeners` - List user's screeners
- `GET /markets/screeners/:id` - Get screener details
- `PUT /markets/screeners/:id` - Update screener
- `DELETE /markets/screeners/:id` - Delete screener
- `POST /markets/screeners/:id/run` - Execute screener
- `GET /markets/screeners/:id/runs` - Get past runs

**Service**: `backend/src/markets/screener.service.ts`

```typescript
import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateScreenerDto, RunScreenerDto } from './dto/screener.dto';

@Injectable()
export class ScreenerService {
  constructor(
    private readonly prisma: PrismaService,
    private readonly alphaVantage: AlphaVantageProvider,
  ) {}

  async createScreener(userId: string, dto: CreateScreenerDto) {
    return this.prisma.screener.create({
      data: {
        userId,
        name: dto.name,
        description: dto.description,
        filters: dto.filters,
        isPublic: dto.isPublic ?? false,
      },
    });
  }

  async runScreener(screenerId: string) {
    const screener = await this.prisma.screener.findUnique({
      where: { id: screenerId },
    });

    if (!screener) throw new Error('Screener not found');

    // Execute filters against market data
    const results = await this.executeFilters(screener.filters);

    // Save run results
    const run = await this.prisma.screenerRun.create({
      data: {
        screenerId,
        results,
        resultCount: results.length,
      },
    });

    return { run, results };
  }

  private async executeFilters(filters: any): Promise<any[]> {
    // Get universe of stocks
    let universe = await this.alphaVantage.getStockUniverse();

    // Apply filters
    if (filters.sector) {
      universe = universe.filter(s => s.sector === filters.sector);
    }

    if (filters.pe_min !== undefined) {
      universe = universe.filter(s => s.pe >= filters.pe_min);
    }

    if (filters.pe_max !== undefined) {
      universe = universe.filter(s => s.pe <= filters.pe_max);
    }

    if (filters.market_cap_min) {
      universe = universe.filter(s => s.marketCap >= filters.market_cap_min);
    }

    if (filters.dividend_yield_min) {
      universe = universe.filter(s => s.dividendYield >= filters.dividend_yield_min);
    }

    // Add more filter logic...

    return universe.map(stock => ({
      ticker: stock.ticker,
      name: stock.name,
      sector: stock.sector,
      price: stock.price,
      pe: stock.pe,
      marketCap: stock.marketCap,
      dividendYield: stock.dividendYield,
    }));
  }
}
```

**DTO**: `backend/src/markets/dto/screener.dto.ts`

```typescript
export class CreateScreenerDto {
  name: string;
  description?: string;
  filters: {
    sector?: string;
    pe_min?: number;
    pe_max?: number;
    market_cap_min?: number;
    market_cap_max?: number;
    dividend_yield_min?: number;
    volume_min?: number;
    price_min?: number;
    price_max?: number;
    // Custom filters...
  };
  isPublic?: boolean;
}
```

### Creator Engine Integration

**Artifact Submission**: Youth can submit screeners as artifacts

```typescript
// backend/src/creators/artifacts.service.ts
async submitScreenerArtifact(userId: string, screenerId: string, challengeId: string) {
  const screener = await this.prisma.screener.findUnique({
    where: { id: screenerId },
    include: { runs: { take: 1, orderBy: { executedAt: 'desc' } } },
  });

  return this.prisma.artifact.create({
    data: {
      userId,
      challengeId,
      type: 'AUTOMATION',
      title: screener.name,
      description: `Custom market screener: ${screener.description}`,
      contentUrl: `/screeners/${screenerId}`,
      metadata: {
        screener_id: screenerId,
        filters: screener.filters,
        last_run: screener.runs[0],
      },
      status: 'SUBMITTED',
    },
  });
}
```

---

## 🎯 MVP Feature 3: Earnings Calendar

### Backend Implementation

```typescript
// backend/src/markets/earnings.service.ts
@Injectable()
export class EarningsService {
  async getEarningsCalendar(from: Date, to: Date) {
    const cached = await this.cache.get(`earnings:${from}:${to}`);
    if (cached) return cached;

    const earnings = await this.finnhub.getEarningsCalendar(from, to);

    const enriched = await Promise.all(
      earnings.map(async (event) => {
        const historical = await this.getHistoricalReaction(event.ticker);
        return {
          ...event,
          historical_reaction: historical,
          volatility_forecast: this.forecastVolatility(historical),
        };
      })
    );

    await this.cache.set(`earnings:${from}:${to}`, enriched, 3600);
    return enriched;
  }

  private async getHistoricalReaction(ticker: string) {
    // Fetch last 4 earnings and price reaction
    const history = await this.prisma.$queryRaw`
      SELECT 
        earnings_date,
        eps_estimate,
        eps_actual,
        revenue_estimate,
        revenue_actual,
        price_change_1d,
        price_change_5d
      FROM earnings_history
      WHERE ticker = ${ticker}
      ORDER BY earnings_date DESC
      LIMIT 4
    `;

    return {
      avg_1d_reaction: this.average(history.map(h => h.price_change_1d)),
      avg_5d_reaction: this.average(history.map(h => h.price_change_5d)),
      beat_rate: history.filter(h => h.eps_actual > h.eps_estimate).length / history.length,
    };
  }
}
```

### Frontend Component

```tsx
// frontend/src/components/markets/EarningsCalendar.tsx
export function EarningsCalendar() {
  const [view, setView] = useState<'calendar' | 'list'>('calendar');
  const [dateRange, setDateRange] = useState({ from: new Date(), to: addDays(new Date(), 30) });

  const { data } = useQuery({
    queryKey: ['earnings', dateRange],
    queryFn: () => fetchEarnings(dateRange),
  });

  return (
    <div className="earnings-calendar">
      <div className="view-toggle">
        <button onClick={() => setView('calendar')}>Calendar View</button>
        <button onClick={() => setView('list')}>List View</button>
      </div>

      {view === 'calendar' ? (
        <Calendar events={data} />
      ) : (
        <EarningsList events={data} />
      )}
    </div>
  );
}

function EarningsCard({ event }) {
  return (
    <div className="earnings-card">
      <h3>{event.ticker} - {event.company_name}</h3>
      <div className="earnings-details">
        <div>EPS Estimate: ${event.eps_estimate}</div>
        <div>Revenue Estimate: ${event.revenue_estimate}B</div>
        <div className="historical">
          <span>Historical 1D Reaction: {event.historical_reaction.avg_1d_reaction}%</span>
          <span>Beat Rate: {event.historical_reaction.beat_rate * 100}%</span>
        </div>
        <div className="volatility-forecast">
          Expected Volatility: {event.volatility_forecast}%
        </div>
      </div>
    </div>
  );
}
```

---

## 🎯 MVP Feature 4: Risk Management Arsenal

### Backend Implementation

```typescript
// backend/src/markets/risk.service.ts
@Injectable()
export class RiskService {
  async calculatePositionSize(dto: PositionSizeDto) {
    const { account_value, risk_per_trade, entry_price, stop_loss } = dto;

    const risk_amount = account_value * (risk_per_trade / 100);
    const risk_per_share = Math.abs(entry_price - stop_loss);
    const shares = Math.floor(risk_amount / risk_per_share);
    const position_value = shares * entry_price;
    const position_pct = (position_value / account_value) * 100;

    return {
      shares,
      position_value,
      position_pct,
      risk_amount,
      risk_per_share,
      max_loss: shares * risk_per_share,
    };
  }

  async analyzePortfolio(userId: string, positions: Position[]) {
    // Calculate portfolio metrics
    const weights = this.calculateWeights(positions);
    const returns = await this.getHistoricalReturns(positions);
    
    const metrics = {
      total_value: this.sum(positions.map(p => p.value)),
      volatility: this.calculateVolatility(returns),
      sharpe_ratio: this.calculateSharpeRatio(returns),
      beta: await this.calculateBeta(positions),
      correlation_matrix: this.calculateCorrelationMatrix(returns),
      var_95: this.calculateVaR(returns, 0.95),
      max_drawdown: this.calculateMaxDrawdown(returns),
    };

    // Save analysis
    await this.prisma.portfolioAnalysis.create({
      data: {
        userId,
        name: `Analysis ${new Date().toISOString()}`,
        positions,
        riskMetrics: metrics,
      },
    });

    return metrics;
  }

  async runScenario(positions: Position[], scenarios: Scenario[]) {
    return scenarios.map(scenario => {
      const newPrices = positions.map(p => ({
        ticker: p.ticker,
        current: p.price,
        scenario: p.price * (1 + scenario.change_pct / 100),
      }));

      const scenario_value = newPrices.reduce((sum, p) => sum + p.scenario * p.shares, 0);
      const current_value = positions.reduce((sum, p) => sum + p.value, 0);
      const change = ((scenario_value - current_value) / current_value) * 100;

      return {
        scenario: scenario.name,
        current_value,
        scenario_value,
        change_pct: change,
        change_dollar: scenario_value - current_value,
      };
    });
  }
}
```

### Frontend Component

```tsx
// frontend/src/components/markets/RiskArsenal.tsx
export function RiskArsenal() {
  const [activeTab, setActiveTab] = useState<'position' | 'portfolio' | 'scenario'>('position');

  return (
    <div className="risk-arsenal">
      <div className="arsenal-tabs">
        <button onClick={() => setActiveTab('position')}>Position Sizing</button>
        <button onClick={() => setActiveTab('portfolio')}>Portfolio Risk</button>
        <button onClick={() => setActiveTab('scenario')}>Scenario Simulator</button>
      </div>

      {activeTab === 'position' && <PositionSizeCalculator />}
      {activeTab === 'portfolio' && <PortfolioAnalyzer />}
      {activeTab === 'scenario' && <ScenarioSimulator />}
    </div>
  );
}

function PositionSizeCalculator() {
  const [inputs, setInputs] = useState({
    account_value: 10000,
    risk_per_trade: 1,
    entry_price: 100,
    stop_loss: 95,
  });

  const { data } = useQuery({
    queryKey: ['position-size', inputs],
    queryFn: () => calculatePositionSize(inputs),
  });

  return (
    <div className="position-calculator">
      <h3>🛡️ Position Sizing Calculator</h3>
      <div className="calculator-inputs">
        <label>
          Account Value: 
          <input type="number" value={inputs.account_value} onChange={...} />
        </label>
        <label>
          Risk Per Trade (%): 
          <input type="number" value={inputs.risk_per_trade} onChange={...} />
        </label>
        <label>
          Entry Price: 
          <input type="number" value={inputs.entry_price} onChange={...} />
        </label>
        <label>
          Stop Loss: 
          <input type="number" value={inputs.stop_loss} onChange={...} />
        </label>
      </div>

      {data && (
        <div className="calculator-results">
          <div className="result-card">
            <h4>Recommended Position</h4>
            <div className="result-value">{data.shares} shares</div>
            <div className="result-detail">${data.position_value.toFixed(2)}</div>
            <div className="result-detail">{data.position_pct.toFixed(1)}% of account</div>
          </div>
          <div className="result-card danger">
            <h4>Maximum Loss</h4>
            <div className="result-value">${data.max_loss.toFixed(2)}</div>
            <div className="result-detail">{inputs.risk_per_trade}% of account</div>
          </div>
        </div>
      )}
    </div>
  );
}
```

---

## 🎯 MVP Feature 5: Education Academy

### Backend Implementation

```typescript
// backend/src/academy/academy.service.ts
@Injectable()
export class AcademyService {
  async getPaths(level?: AcademyLevel) {
    return this.prisma.academyPath.findMany({
      where: level ? { level } : {},
      include: {
        lessons: {
          select: {
            id: true,
            title: true,
            duration: true,
            sequence: true,
          },
          orderBy: { sequence: 'asc' },
        },
      },
      orderBy: { sequence: 'asc' },
    });
  }

  async getLesson(lessonId: string, userId: string) {
    const lesson = await this.prisma.academyLesson.findUnique({
      where: { id: lessonId },
      include: {
        path: true,
        quiz: true,
      },
    });

    const progress = await this.prisma.lessonProgress.findUnique({
      where: {
        userId_lessonId: { userId, lessonId },
      },
    });

    return { lesson, progress };
  }

  async markLessonComplete(userId: string, lessonId: string, timeSpent: number) {
    await this.prisma.lessonProgress.upsert({
      where: {
        userId_lessonId: { userId, lessonId },
      },
      create: {
        userId,
        lessonId,
        completed: true,
        timeSpent,
      },
      update: {
        completed: true,
        timeSpent: { increment: timeSpent },
        lastAccessed: new Date(),
      },
    });

    // Check if path completed
    const lesson = await this.prisma.academyLesson.findUnique({
      where: { id: lessonId },
      include: { path: { include: { lessons: true } } },
    });

    const pathProgress = await this.prisma.lessonProgress.count({
      where: {
        userId,
        lessonId: { in: lesson.path.lessons.map(l => l.id) },
        completed: true,
      },
    });

    if (pathProgress === lesson.path.lessons.length) {
      // Path completed! Trigger Intelligence Engine signal
      await this.intelligenceService.emit({
        type: 'opportunity',
        domain: 'academy',
        ruleId: 'A1',
        message: `Youth completed ${lesson.path.name} path!`,
        severity: 'high',
        audience: ['youth', 'director'],
        metadata: { userId, pathId: lesson.pathId },
      });
    }
  }

  async submitQuiz(userId: string, quizId: string, answers: any[]) {
    const quiz = await this.prisma.academyQuiz.findUnique({
      where: { id: quizId },
    });

    const questions = quiz.questions as any[];
    let correct = 0;

    questions.forEach((q, i) => {
      if (q.correct_index === answers[i]) {
        correct++;
      }
    });

    const score = Math.round((correct / questions.length) * 100);
    const passed = score >= quiz.passingScore;

    await this.prisma.quizAttempt.create({
      data: {
        userId,
        quizId,
        score,
        answers,
        passed,
      },
    });

    return { score, passed, correct, total: questions.length };
  }

  async getUserProgress(userId: string) {
    const paths = await this.prisma.academyPath.findMany({
      include: {
        lessons: {
          include: {
            progress: {
              where: { userId },
            },
          },
        },
      },
    });

    return paths.map(path => {
      const total = path.lessons.length;
      const completed = path.lessons.filter(l => l.progress[0]?.completed).length;
      
      return {
        path: path.name,
        level: path.level,
        progress: (completed / total) * 100,
        completed,
        total,
      };
    });
  }
}
```

### Curriculum Integration

**Seasonal Mapping**: Academy paths become Curriculum modules

```typescript
// backend/src/curriculum/curriculum-academy.service.ts
@Injectable()
export class CurriculumAcademyService {
  async createWealthSeason() {
    // Create "Wealth & Markets" season in Curriculum Engine
    const modules = [
      {
        title: 'Foundation (Beginner)',
        weeks: [
          { title: 'What is Money?', academy_path: 'BEGINNER' },
          { title: 'The Market Terrain', academy_path: 'BEGINNER' },
          { title: 'Risk Before Reward', academy_path: 'BEGINNER' },
        ],
      },
      {
        title: 'Strategy (Intermediate)',
        weeks: [
          { title: 'Technical Analysis', academy_path: 'INTERMEDIATE' },
          { title: 'Fundamental Analysis', academy_path: 'INTERMEDIATE' },
          { title: 'Portfolio Construction', academy_path: 'INTERMEDIATE' },
        ],
      },
      {
        title: 'Mastery (Advanced)',
        weeks: [
          { title: 'Options & Derivatives', academy_path: 'ADVANCED' },
          { title: 'Macro Strategy', academy_path: 'ADVANCED' },
          { title: 'Wealth Architecture', academy_path: 'ADVANCED' },
        ],
      },
    ];

    return modules;
  }
}
```

---

## 🧠 Intelligence Engine Integration

### New Intelligence Rules for Markets Domain

```typescript
// backend/src/intelligence/rules/markets-rules.ts

export async function evaluateAcademyPathCompletion(
  context: IntelligenceRuleContext
): Promise<IntelligenceItem[]> {
  const results: IntelligenceItem[] = [];

  // Find youth who completed a path in last 7 days
  const completions = await context.prisma.$queryRaw`
    SELECT 
      u.id as user_id,
      u."firstName",
      u."lastName",
      ap.name as path_name,
      COUNT(lp.id) as lessons_completed,
      (SELECT COUNT(*) FROM academy_lessons WHERE "pathId" = ap.id) as total_lessons
    FROM users u
    JOIN lesson_progress lp ON lp."userId" = u.id
    JOIN academy_lessons al ON al.id = lp."lessonId"
    JOIN academy_paths ap ON ap.id = al."pathId"
    WHERE lp.completed = true
      AND lp."lastAccessed" >= NOW() - INTERVAL '7 days'
    GROUP BY u.id, u."firstName", u."lastName", ap.id, ap.name
    HAVING COUNT(lp.id) = (SELECT COUNT(*) FROM academy_lessons WHERE "pathId" = ap.id)
  `;

  completions.forEach((completion: any) => {
    results.push(
      createItem('MK1', {
        type: 'opportunity',
        domain: 'markets',
        message: `${completion.firstName} ${completion.lastName} completed ${completion.path_name} path!`,
        severity: 'high',
        audience: ['youth', 'captain', 'director'],
        metadata: {
          user_id: completion.user_id,
          path_name: completion.path_name,
          lessons_completed: completion.lessons_completed,
        },
      })
    );
  });

  return results;
}

export async function evaluateScreenerCreativity(
  context: IntelligenceRuleContext
): Promise<IntelligenceItem[]> {
  const results: IntelligenceItem[] = [];

  // Find screeners with unique filter combinations
  const screeners = await context.prisma.screener.findMany({
    where: {
      createdAt: { gte: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000) },
    },
    include: {
      user: { select: { firstName: true, lastName: true } },
      runs: { take: 1, orderBy: { executedAt: 'desc' } },
    },
  });

  screeners.forEach((screener) => {
    const filterCount = Object.keys(screener.filters as any).length;
    
    if (filterCount >= 5) {
      results.push(
        createItem('MK2', {
          type: 'recommendation',
          domain: 'markets',
          message: `${screener.user.firstName} created advanced screener: ${screener.name}`,
          severity: 'medium',
          audience: ['captain', 'creator'],
          metadata: {
            screener_id: screener.id,
            filter_count: filterCount,
            result_count: screener.runs[0]?.resultCount,
          },
        })
      );
    }
  });

  return results;
}

export async function evaluateRiskAwareness(
  context: IntelligenceRuleContext
): Promise<IntelligenceItem[]> {
  const results: IntelligenceItem[] = [];

  // Find youth who completed Risk Management lessons but haven't used tools
  const youthWithRisk = await context.prisma.$queryRaw`
    SELECT 
      u.id,
      u."firstName",
      u."lastName",
      COUNT(lp.id) as risk_lessons_completed
    FROM users u
    JOIN lesson_progress lp ON lp."userId" = u.id
    JOIN academy_lessons al ON al.id = lp."lessonId"
    WHERE al.title ILIKE '%risk%'
      AND lp.completed = true
      AND NOT EXISTS (
        SELECT 1 FROM portfolio_analyses pa WHERE pa."userId" = u.id
      )
    GROUP BY u.id, u."firstName", u."lastName"
    HAVING COUNT(lp.id) >= 2
  `;

  youthWithRisk.forEach((youth: any) => {
    results.push(
      createItem('MK3', {
        type: 'recommendation',
        domain: 'markets',
        message: `Encourage ${youth.firstName} to use Risk Arsenal tools`,
        severity: 'medium',
        audience: ['captain'],
        metadata: {
          user_id: youth.id,
          risk_lessons_completed: youth.risk_lessons_completed,
          suggestion: 'Assign portfolio analysis challenge',
        },
      })
    );
  });

  return results;
}
```

**Add to Rule Registry**:

```typescript
// backend/src/intelligence/rules/rule-definitions.ts

export const IntelligenceRules: IntelligenceRuleDefinition[] = [
  // ... existing rules (Y2, C1-C7, M3) ...

  // MARKETS DOMAIN (MK*)
  {
    id: 'MK1',
    name: 'Academy Path Completion',
    description: 'Recognize youth who complete learning paths',
    domain: 'markets',
    evaluator: evaluateAcademyPathCompletion,
  },
  {
    id: 'MK2',
    name: 'Screener Creativity Signal',
    description: 'Highlight advanced screener creation',
    domain: 'markets',
    evaluator: evaluateScreenerCreativity,
  },
  {
    id: 'MK3',
    name: 'Risk Awareness Gap',
    description: 'Recommend tool usage after lesson completion',
    domain: 'markets',
    evaluator: evaluateRiskAwareness,
  },
];
```

---

## 📊 Analytics Dashboard Integration

### New Analytics Endpoints

```typescript
// backend/src/analytics/markets-analytics.service.ts
@Injectable()
export class MarketsAnalyticsService {
  async getMarketsOverview(regionId?: string) {
    return {
      academy: {
        total_learners: await this.countActiveLearners(regionId),
        paths_completed: await this.countCompletedPaths(regionId),
        avg_quiz_score: await this.getAvgQuizScore(regionId),
        active_lessons: await this.countActiveLessons(regionId),
      },
      tools: {
        screeners_created: await this.countScreeners(regionId),
        portfolio_analyses: await this.countAnalyses(regionId),
        watchlists_active: await this.countWatchlists(regionId),
      },
      engagement: {
        daily_active_users: await this.getDailyActiveUsers(regionId),
        avg_session_duration: await this.getAvgSessionDuration(regionId),
        feature_usage: await this.getFeatureUsage(regionId),
      },
      creators: {
        screener_artifacts: await this.countScreenerArtifacts(regionId),
        strategy_submissions: await this.countStrategySubmissions(regionId),
      },
    };
  }

  async getLearningProgress(userId: string) {
    const paths = await this.prisma.academyPath.findMany({
      include: {
        lessons: {
          include: {
            progress: { where: { userId } },
          },
        },
      },
    });

    return {
      overall_completion: this.calculateOverallCompletion(paths),
      path_breakdown: paths.map(p => ({
        name: p.name,
        level: p.level,
        progress: this.calculatePathProgress(p),
        time_spent: this.sumTimeSpent(p.lessons),
      })),
      quiz_performance: await this.getQuizPerformance(userId),
      next_recommended_lesson: await this.getNextLesson(userId),
    };
  }
}
```

---

## 🚀 Implementation Roadmap

### Phase 1: Foundation (Week 1-2)

**Backend Setup**:
- [ ] Create Prisma migrations for Markets & Academy models
- [ ] Set up MarketsModule with basic structure
- [ ] Set up AcademyModule with basic structure
- [ ] Configure AlphaVantage/Finnhub API providers
- [ ] Implement caching layer

**Frontend Setup**:
- [ ] Create `/markets` route structure
- [ ] Create `/academy` route structure
- [ ] Set up React Query for data fetching
- [ ] Design Markets layout component

### Phase 2: Feature Implementation (Week 2-4)

**Week 2: Heatmap & Screener**
- [ ] Implement Market Heatmap backend
- [ ] Implement Market Heatmap frontend
- [ ] Implement Screener CRUD endpoints
- [ ] Implement Screener execution logic
- [ ] Build Screener UI with drag-drop filters

**Week 3: Earnings & Risk**
- [ ] Implement Earnings Calendar backend
- [ ] Implement Earnings Calendar frontend
- [ ] Implement Risk calculators backend
- [ ] Build Risk Arsenal UI
- [ ] Integrate scenario simulator

**Week 4: Academy**
- [ ] Seed Academy paths and lessons
- [ ] Implement lesson progress tracking
- [ ] Build Academy UI (paths, lessons, quizzes)
- [ ] Implement quiz submission and grading

### Phase 3: Integration (Week 5)

**Creator Engine**:
- [ ] Enable screener artifact submissions
- [ ] Create Markets challenges
- [ ] Integrate artifact evaluation

**Curriculum Engine**:
- [ ] Map Academy paths to Curriculum
- [ ] Create "Wealth Season" missions
- [ ] Link lessons to Youth Circle curriculum

**Intelligence Engine**:
- [ ] Implement MK1-MK3 rules
- [ ] Add Markets domain to intelligence endpoints
- [ ] Test intelligence signals

### Phase 4: Analytics & Polish (Week 6)

**Analytics Dashboard**:
- [ ] Build Markets analytics views
- [ ] Director dashboard for Academy progress
- [ ] Creator dashboard for Markets artifacts

**Polish**:
- [ ] UI/UX refinement
- [ ] Performance optimization
- [ ] Error handling improvements
- [ ] Documentation completion

---

## 📦 API Endpoints Summary

### Markets Endpoints

```
GET    /api/v1/markets/heatmap
GET    /api/v1/markets/pulse
GET    /api/v1/markets/earnings
POST   /api/v1/markets/screeners
GET    /api/v1/markets/screeners
GET    /api/v1/markets/screeners/:id
PUT    /api/v1/markets/screeners/:id
DELETE /api/v1/markets/screeners/:id
POST   /api/v1/markets/screeners/:id/run
GET    /api/v1/markets/screeners/:id/runs
POST   /api/v1/markets/watchlists
GET    /api/v1/markets/watchlists
POST   /api/v1/markets/risk/position-size
POST   /api/v1/markets/risk/portfolio-analysis
POST   /api/v1/markets/risk/scenario
```

### Academy Endpoints

```
GET    /api/v1/academy/paths
GET    /api/v1/academy/paths/:id
GET    /api/v1/academy/lessons/:id
POST   /api/v1/academy/lessons/:id/complete
GET    /api/v1/academy/progress
POST   /api/v1/academy/quizzes/:id/submit
GET    /api/v1/academy/quizzes/:id/attempts
GET    /api/v1/academy/glossary
```

### Analytics Endpoints

```
GET    /api/v1/analytics/markets/overview
GET    /api/v1/analytics/markets/learning-progress/:userId
GET    /api/v1/analytics/markets/tool-usage
GET    /api/v1/analytics/markets/creator-activity
```

---

## 🔐 Security & Performance

### Rate Limiting

```typescript
// backend/src/markets/markets.module.ts
@Module({
  imports: [
    ThrottlerModule.forRoot({
      ttl: 60,
      limit: 100, // 100 requests per minute
    }),
  ],
  // ...
})
```

### Caching Strategy

- **Heatmap**: 5 minutes
- **Earnings Calendar**: 1 hour
- **Stock universe**: 15 minutes
- **Market data**: 1 minute
- **User screeners**: No cache (always fresh)

### Data Sources

**Primary**: AlphaVantage (free tier: 5 requests/minute)  
**Secondary**: Finnhub (free tier: 60 requests/minute)  
**Backup**: TwelveData or Polygon

---

## 🎯 Success Metrics

### User Engagement
- Daily active users in Markets realm
- Lesson completion rate
- Quiz pass rate
- Time spent in Academy

### Creator Activity
- Screeners created per week
- Artifact submissions
- Portfolio analyses run

### Intelligence Signals
- MK1-MK3 rule trigger rate
- Opportunity identification accuracy
- Recommendation effectiveness

### Business Metrics
- Youth progression through paths
- Director engagement with analytics
- Creator artifact quality scores

---

## 🔥 The Flame Burns Sovereign and Eternal! 👑

This MVP transforms the mythic Wealth & Markets Realm into a buildable, shippable product that:

✅ **Integrates seamlessly** with CodexDominion 2.0  
✅ **Empowers youth** with financial literacy  
✅ **Enables creators** to build and submit artifacts  
✅ **Provides directors** with actionable intelligence  
✅ **Establishes foundation** for future expansion  

**Ready to build? Start with Phase 1: Database schema and module setup!**
