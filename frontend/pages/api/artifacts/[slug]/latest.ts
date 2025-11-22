import { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';

interface Pick {
  symbol: string;
  tier: string;
  target_weight: number;
  rationale: string;
  risk_factors: string[];
}

interface TierCounts {
  Alpha: number;
  Beta: number;
  Gamma: number;
  Delta: number;
}

// Mock data generator for development
function generateMockArtifact(slug: string) {
  const mockPicks = [
    {
      symbol: 'AAPL',
      tier: 'Alpha',
      target_weight: 0.15,
      rationale: 'Strong fundamentals with consistent revenue growth and robust ecosystem lock-in effects.',
      risk_factors: ['Regulatory pressure in key markets', 'Supply chain dependencies']
    },
    {
      symbol: 'GOOGL',
      tier: 'Alpha', 
      target_weight: 0.12,
      rationale: 'Dominant position in search and advertising with growing cloud business.',
      risk_factors: ['Antitrust regulations', 'Competition in cloud services']
    },
    {
      symbol: 'MSFT',
      tier: 'Beta',
      target_weight: 0.10,
      rationale: 'Leading cloud infrastructure and productivity software suite.',
      risk_factors: ['Market saturation', 'Cybersecurity threats']
    },
    {
      symbol: 'NVDA',
      tier: 'Beta',
      target_weight: 0.08,
      rationale: 'AI and data center growth driving semiconductor demand.',
      risk_factors: ['Cyclical semiconductor market', 'Geopolitical tensions']
    },
    {
      symbol: 'TSLA',
      tier: 'Gamma',
      target_weight: 0.05,
      rationale: 'Electric vehicle market leadership with energy storage expansion.',
      risk_factors: ['Execution risk on scaling', 'Increased competition', 'Regulatory changes']
    }
  ];

  return {
    title: `${slug.replace('-', ' ').toUpperCase()} Market Analysis`,
    capsule_slug: slug,
    generated_at: new Date().toISOString(),
    execution_id: `${slug}_${Date.now()}`,
    status: 'success',
    banner: `🎯 Strategic market positioning analysis for ${slug} capsule. Comprehensive tier-based allocation strategy designed for optimal risk-adjusted returns while maintaining sovereign operational independence.`,
    tier_counts: {
      Alpha: mockPicks.filter(p => p.tier === 'Alpha').length,
      Beta: mockPicks.filter(p => p.tier === 'Beta').length,
      Gamma: mockPicks.filter(p => p.tier === 'Gamma').length,
      Delta: mockPicks.filter(p => p.tier === 'Delta').length
    },
    picks: mockPicks,
    metadata: {
      archive_version: '1.0',
      archiver: 'local_fallback',
      timestamp: new Date().toISOString(),
      total_weight: mockPicks.reduce((sum, pick) => sum + pick.target_weight, 0)
    }
  };
}

async function loadArtifactFromArchive(slug: string) {
  try {
    // Path to archived snapshots
    const archivePath = path.join(process.cwd(), '..', 'archives', 'snapshots', slug);
    
    if (!fs.existsSync(archivePath)) {
      console.log(`No archive found for ${slug}, generating mock data`);
      return generateMockArtifact(slug);
    }

    // Find the most recent artifact file
    const years = fs.readdirSync(archivePath).filter(item => 
      fs.statSync(path.join(archivePath, item)).isDirectory()
    );
    
    if (years.length === 0) {
      return generateMockArtifact(slug);
    }

    // Get the latest year
    const latestYear = years.sort().pop();
    const yearPath = path.join(archivePath, latestYear!);
    
    const months = fs.readdirSync(yearPath).filter(item =>
      fs.statSync(path.join(yearPath, item)).isDirectory()
    );
    
    if (months.length === 0) {
      return generateMockArtifact(slug);
    }

    // Get the latest month
    const latestMonth = months.sort().pop();
    const monthPath = path.join(yearPath, latestMonth!);
    
    const days = fs.readdirSync(monthPath).filter(item =>
      fs.statSync(path.join(monthPath, item)).isDirectory()
    );
    
    if (days.length === 0) {
      return generateMockArtifact(slug);
    }

    // Get the latest day
    const latestDay = days.sort().pop();
    const dayPath = path.join(monthPath, latestDay!);
    
    const files = fs.readdirSync(dayPath).filter(file => file.endsWith('.json'));
    
    if (files.length === 0) {
      return generateMockArtifact(slug);
    }

    // Get the most recent file
    const latestFile = files.sort().pop();
    const filePath = path.join(dayPath, latestFile!);
    
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    const archiveData = JSON.parse(fileContent);
    
    // Transform archive data to match expected artifact format
    const artifact = {
      title: `${slug.replace('-', ' ').toUpperCase()} Execution Result`,
      capsule_slug: slug,
      generated_at: archiveData.metadata?.timestamp || new Date().toISOString(),
      execution_id: archiveData.data?.execution_id || `${slug}_archived`,
      status: 'success',
      banner: `📊 Archived execution data for ${slug} capsule. This represents a historical snapshot of system execution and performance metrics.`,
      tier_counts: {
        Alpha: 0,
        Beta: 0,
        Gamma: 0,
        Delta: 0
      },
      picks: [] as Pick[],
      metadata: archiveData.metadata || {},
      raw_data: archiveData.data
    };

    // If it's a signals-daily capsule with market data, create picks
    if (slug === 'signals-daily' && archiveData.data?.market_data) {
      const recommendations = archiveData.data.recommendations || [];
      const generatedPicks: Pick[] = recommendations.map((rec: string, index: number) => ({
        symbol: `SIGNAL_${index + 1}`,
        tier: ['Alpha', 'Beta', 'Gamma'][index % 3],
        target_weight: Math.random() * 0.1 + 0.05,
        rationale: rec,
        risk_factors: ['Market volatility', 'Execution risk']
      }));
      
      artifact.picks = generatedPicks;
      
      // Update tier counts
      artifact.tier_counts = {
        Alpha: generatedPicks.filter(p => p.tier === 'Alpha').length,
        Beta: generatedPicks.filter(p => p.tier === 'Beta').length,
        Gamma: generatedPicks.filter(p => p.tier === 'Gamma').length,
        Delta: generatedPicks.filter(p => p.tier === 'Delta').length
      };
    }

    return artifact;

  } catch (error) {
    console.error('Error loading artifact from archive:', error);
    return generateMockArtifact(slug);
  }
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { slug } = req.query;

  if (!slug || typeof slug !== 'string') {
    return res.status(400).json({ error: 'Invalid capsule slug' });
  }

  try {
    const artifact = await loadArtifactFromArchive(slug);
    
    res.status(200).json(artifact);
  } catch (error) {
    console.error('API error:', error);
    res.status(500).json({ 
      error: 'Failed to load artifact',
      message: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}