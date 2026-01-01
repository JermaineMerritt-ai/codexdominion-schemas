# AI Advisor - Quick Start Guide

**Status**: Backend Complete ✅ | Ready for Frontend Integration

---

## 🚀 5-Minute Setup

### 1. Run Database Migration
```bash
# Create advisor_recommendations table
python -c "from models import Base; from db import engine; Base.metadata.create_all(bind=engine)"
```

### 2. Seed Sample Data
```bash
python seed_advisor_recommendations.py
# Creates 6 sample recommendations
```

### 3. Test System
```bash
python test_advisor_system.py
# Runs full test suite (signal collection, intelligence, storage, lifecycle, learning)
```

### 4. Start Flask
```bash
python flask_dashboard.py
# Should see: "✓ AI Advisor API registered"
```

### 5. Test API
```bash
# Generate fresh recommendations
curl -X POST http://localhost:5000/api/advisor/recommendations/refresh \
  -H "Content-Type: application/json" \
  -d '{"tenant_id":"tenant_codexdominion","days":30}'

# List pending recommendations
curl "http://localhost:5000/api/advisor/recommendations?tenant_id=tenant_codexdominion&status=pending"
```

---

## 📋 Core Concepts

### Signals (40+ metrics)
```python
from advisor_signals import collect_tenant_signals

signals = collect_tenant_signals('tenant_codexdominion', days=30)
# Returns: store_signals, workflow_signals, marketing_signals, customer_signals, automation_signals
```

### Intelligence (10+ scenarios)
```python
from advisor_intelligence import generate_recommendations

recommendations = generate_recommendations('tenant_codexdominion', signals)
# Returns: Prioritized list of recommendation dicts
```

### Lifecycle (5 states)
```
pending → accepted/dismissed → completed
                    ↓
              expired (if expires_at passes)
```

### Learning Loop
```
Accept → Track Impact → Measure Accuracy → Improve Confidence
```

---

## 🌐 API Cheat Sheet

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/advisor/recommendations` | GET | List recommendations |
| `/api/advisor/recommendations/:id` | GET | Get details |
| `/api/advisor/recommendations/:id/accept` | POST | Accept recommendation |
| `/api/advisor/recommendations/:id/dismiss` | POST | Dismiss recommendation |
| `/api/advisor/recommendations/refresh` | POST | Generate new recommendations |
| `/api/advisor/recommendations/stats` | GET | Performance metrics |
| `/api/advisor/health` | GET | Health check |

---

## 🎯 Common Tasks

### Generate Recommendations
```python
# Manual generation
from advisor_signals import collect_tenant_signals
from advisor_intelligence import generate_recommendations

signals = collect_tenant_signals('tenant_codexdominion', days=30)
recs = generate_recommendations('tenant_codexdominion', signals)
```

### Accept Recommendation
```bash
curl -X POST http://localhost:5000/api/advisor/recommendations/:id/accept \
  -H "Content-Type: application/json" \
  -d '{"feedback":"Great suggestion!"}'
```

### Dismiss Recommendation
```bash
curl -X POST http://localhost:5000/api/advisor/recommendations/:id/dismiss \
  -H "Content-Type: application/json" \
  -d '{"reason":"Not relevant right now"}'
```

### Track Impact
```python
from db import SessionLocal
from models import AdvisorRecommendation, RecommendationStatus

session = SessionLocal()
rec = session.query(AdvisorRecommendation).filter_by(id='rec_123').first()
rec.actual_impact = {'revenue': '+25%', 'measured_at': datetime.utcnow().isoformat()}
rec.status = RecommendationStatus.COMPLETED
rec.completed_at = datetime.utcnow()
session.commit()
```

### Get Performance Stats
```bash
curl "http://localhost:5000/api/advisor/recommendations/stats?tenant_id=tenant_codexdominion&days=30"
```

---

## 🐛 Troubleshooting

### No Recommendations Generated
- **Check**: Do you have workflows/products/marketing campaigns in database?
- **Fix**: Seed test data or ensure tenant has activity
- **Test**: `python test_advisor_system.py`

### Signal Collection Fails
- **Check**: Database connection
- **Fix**: Verify PostgreSQL is running, check `db.py` connection string
- **Test**: `python -c "from db import SessionLocal; SessionLocal().execute('SELECT 1')"`

### API Returns 404
- **Check**: Flask registration
- **Fix**: Restart Flask: `python flask_dashboard.py`
- **Verify**: Look for "✓ AI Advisor API registered" in output

### Recommendations Not Prioritized Correctly
- **Check**: Confidence scores and impact levels
- **Fix**: Adjust weights in `advisor_intelligence.py` `prioritize_recommendations()`
- **Test**: Generate recommendations and inspect scores

---

## 📚 File Reference

| File | Purpose | Lines |
|------|---------|-------|
| `models.py` (lines 1839-1934) | AdvisorRecommendation model + enums | 100 |
| `advisor_signals.py` | Signal collection (5 categories, 40+ metrics) | 350 |
| `advisor_intelligence.py` | Intelligence engine (4 detection methods) | 400 |
| `advisor_api.py` | REST API (6 endpoints) | 370 |
| `flask_dashboard.py` (lines 11414-11422) | API registration | 12 |
| `seed_advisor_recommendations.py` | Sample data generator | 200 |
| `test_advisor_system.py` | Full test suite | 450 |

---

## 🎨 Frontend Integration (Next Steps)

### 1. Create Recommendation Card Component
```tsx
// components/RecommendationCard.tsx
interface Props {
  recommendation: AdvisorRecommendation;
  onAccept: () => void;
  onDismiss: () => void;
}

export function RecommendationCard({ recommendation, onAccept, onDismiss }: Props) {
  return (
    <div className="recommendation-card">
      <h3>{recommendation.title}</h3>
      <p>{recommendation.description}</p>
      <div className="impact">
        <Badge>{recommendation.impact_level}</Badge>
        <span>{recommendation.confidence_score}% confidence</span>
      </div>
      <div className="actions">
        <Button onClick={onAccept}>Review Draft</Button>
        <Button variant="ghost" onClick={onDismiss}>Dismiss</Button>
      </div>
    </div>
  );
}
```

### 2. Add to Portal Dashboard
```tsx
// app/dashboard/page.tsx
import { useRecommendations } from '@/hooks/useRecommendations';

export default function DashboardPage() {
  const { recommendations, acceptRecommendation, dismissRecommendation } = useRecommendations();
  
  return (
    <div className="dashboard">
      <Section title="AI Advisor Recommendations">
        {recommendations.map(rec => (
          <RecommendationCard
            key={rec.id}
            recommendation={rec}
            onAccept={() => acceptRecommendation(rec.id)}
            onDismiss={() => dismissRecommendation(rec.id)}
          />
        ))}
      </Section>
    </div>
  );
}
```

### 3. Implement Review Draft Flow
```typescript
async function handleReviewDraft(recommendationId: string) {
  // 1. Accept recommendation
  const { recommendation, pre_filled_data } = await fetch(
    `/api/advisor/recommendations/${recommendationId}/accept`,
    { method: 'POST' }
  ).then(r => r.json());
  
  // 2. Open workflow editor with pre-filled data
  router.push({
    pathname: '/workflows/draft',
    query: {
      template: recommendation.workflow_template_id,
      data: JSON.stringify(pre_filled_data)
    }
  });
}
```

---

## 🎯 Success Metrics

Target performance after frontend integration:

- **Acceptance Rate**: 40-60%
- **Time to Act**: < 2 minutes from recommendation to draft
- **Impact Accuracy**: 80-90% within ±10% of estimate
- **User Satisfaction**: "Feels like a partner, not a nag"

---

## 🔥 The Strategic Brain Awakens! 👑

**Next**: Build recommendation cards UI and integrate with draft workflow system.

See full documentation: [AI_ADVISOR_DOCUMENTATION.md](./AI_ADVISOR_DOCUMENTATION.md)
