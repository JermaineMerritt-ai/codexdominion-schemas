'use client';

import { Card, CardHeader, CardBody, Badge, Icon } from "@/components/ui";
import { formatCurrency } from "@/lib/design-system";

interface RecommendationCardProps {
  recommendation: {
    id: string;
    title: string;
    description: string;
    impact_level: "high" | "medium" | "low";
    confidence_score: number;
    estimated_weekly_savings?: number;
    estimated_monthly_savings?: number;
    automation_complexity?: string;
    expires_at?: string;
    status: string;
  };
}

export function RecommendationCard({ recommendation }: RecommendationCardProps) {
  const impactColors = {
    high: "text-sovereign-crimson border-sovereign-crimson/30 bg-sovereign-crimson/5",
    medium: "text-sovereign-gold border-sovereign-gold/30 bg-sovereign-gold/5",
    low: "text-sovereign-blue border-sovereign-blue/30 bg-sovereign-blue/5",
  };

  const handleDismiss = () => {
    // TODO: Call API to dismiss recommendation
    console.log('Dismiss recommendation:', recommendation.id);
  };

  const impactIcons = {
    high: "fire" as const,
    medium: "activity" as const,
    low: "info" as const,
  };

  const getExpirationStatus = () => {
    if (!recommendation.expires_at) return null;
    
    const expiresAt = new Date(recommendation.expires_at);
    const now = new Date();
    const hoursUntilExpiry = (expiresAt.getTime() - now.getTime()) / (1000 * 60 * 60);
    
    if (hoursUntilExpiry < 0) return { text: "Expired", variant: "crimson" as const };
    if (hoursUntilExpiry < 24) return { text: `${Math.round(hoursUntilExpiry)}h left`, variant: "gold" as const };
    if (hoursUntilExpiry < 72) return { text: `${Math.round(hoursUntilExpiry / 24)}d left`, variant: "blue" as const };
    return null;
  };

  const expirationStatus = getExpirationStatus();

  return (
    <Card className="hover:ring-2 hover:ring-sovereign-gold/30 transition-all">
      <CardHeader>
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-start gap-3 flex-1">
            <div className={`p-2 rounded-lg ${impactColors[recommendation.impact_level]}`}>
              <Icon 
                name={impactIcons[recommendation.impact_level]} 
                size={20} 
                className={impactColors[recommendation.impact_level].split(" ")[0]} 
              />
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="text-base font-semibold text-white mb-1">
                {recommendation.title}
              </h3>
              <div className="flex flex-wrap items-center gap-2 text-xs">
                <Badge variant={recommendation.impact_level === "high" ? "crimson" : recommendation.impact_level === "medium" ? "gold" : "blue"}>
                  {recommendation.impact_level.toUpperCase()} IMPACT
                </Badge>
                <span className="text-slate-400">
                  {recommendation.confidence_score}% confidence
                </span>
                {expirationStatus && (
                  <Badge variant={expirationStatus.variant}>
                    <Icon name="clock" size={10} className="inline mr-1" />
                    {expirationStatus.text}
                  </Badge>
                )}
              </div>
            </div>
          </div>
        </div>
      </CardHeader>
      
      <CardBody>
        <p className="text-sm text-slate-300 mb-4">
          {recommendation.description}
        </p>

        {/* Impact Estimates */}
        {(recommendation.estimated_weekly_savings || recommendation.estimated_monthly_savings) && (
          <div className="grid grid-cols-2 gap-3 mb-4 p-3 rounded-lg bg-sovereign-slate/30 border border-sovereign-slate">
            {recommendation.estimated_weekly_savings && (
              <div>
                <div className="text-xs text-slate-400 mb-1">Weekly Savings</div>
                <div className="text-base font-semibold text-sovereign-gold">
                  {formatCurrency(recommendation.estimated_weekly_savings)}
                </div>
              </div>
            )}
            {recommendation.estimated_monthly_savings && (
              <div>
                <div className="text-xs text-slate-400 mb-1">Monthly Savings</div>
                <div className="text-base font-semibold text-sovereign-gold">
                  {formatCurrency(recommendation.estimated_monthly_savings)}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Complexity Indicator */}
        {recommendation.automation_complexity && (
          <div className="mb-4 flex items-center gap-2 text-xs text-slate-400">
            <Icon name="settings" size={12} />
            <span>Automation complexity: {recommendation.automation_complexity}</span>
          </div>
        )}

        {/* Confidence Meter */}
        <div className="mb-4">
          <div className="flex items-center justify-between text-xs mb-1">
            <span className="text-slate-400">Confidence Score</span>
            <span className="text-white font-semibold">{recommendation.confidence_score}%</span>
          </div>
          <div className="h-2 bg-sovereign-slate rounded-full overflow-hidden">
            <div 
              className={`h-full rounded-full transition-all ${
                recommendation.confidence_score >= 80 
                  ? "bg-sovereign-emerald" 
                  : recommendation.confidence_score >= 60 
                  ? "bg-sovereign-gold" 
                  : "bg-sovereign-blue"
              }`}
              style={{ width: `${Math.min(100, Math.max(0, recommendation.confidence_score))}%` }}
            />
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-2">
          <a
            href={`/dashboard/advisor/recommendations/${recommendation.id}`}
            className="flex-1 px-4 py-2 rounded-lg bg-sovereign-gold hover:bg-sovereign-gold/80 text-sovereign-obsidian font-semibold text-sm transition-colors flex items-center justify-center gap-2"
          >
            <Icon name="eye" size={14} />
            Review Draft
          </a>
          <button
            onClick={handleDismiss}
            className="px-4 py-2 rounded-lg border border-sovereign-slate hover:bg-sovereign-slate/30 text-slate-300 text-sm transition-colors flex items-center justify-center gap-2"
          >
            <Icon name="xCircle" size={14} />
            Dismiss
          </button>
        </div>
      </CardBody>
    </Card>
  );
}
