# Capsule Annotation System

## Overview

The **Capsule Annotation System** enables council members to add contextual notes, observations, and analysis to specific replay capsules during ceremonial reviews. This creates a rich historical archive that links engine status changes to business impact, recurring patterns, and correlational insights.

## Architecture

### Core Components

```
CapsuleAnnotationManager (lib/annotations/capsule-annotations.ts)
├── Storage: localStorage persistence
├── Auto-tagging: correlation, revenue-impact, performance, degraded-status, recovery, pattern-analysis
├── Search: Full-text search across notes, engines, authors, tags
└── Export/Import: JSON format for backup and sharing

AnnotationForm (components/annotation-form.tsx)
├── Input: Textarea for council observations
├── Context: Auto-captures capsuleId and engine from replay viewer
└── Submission: Creates annotation with timestamp and auto-tags

AnnotationTimeline (components/annotation-timeline.tsx)
├── Display: Chronological list of annotations
├── Filters: By capsule, engine, or tag
└── Actions: Delete, view metadata

CapsuleAnnotationPanel (components/capsule-annotation-panel.tsx)
├── Combined: AnnotationForm + AnnotationTimeline
└── Context: Scoped to current capsule in replay viewer

AnnotationsPage (app/annotations/page.tsx)
├── Dashboard: Full annotation archive with statistics
├── Search: Full-text search and multi-filter (engine + tag)
├── Export: Download JSON backup
└── Management: Clear all, delete individual
```

## Data Structure

### CapsuleAnnotation Interface

```typescript
interface CapsuleAnnotation {
  id: string;                    // Unique annotation ID (annotation_{timestamp}_{random})
  capsuleId: string;             // Reference to replay capsule
  engine: string;                // Engine name (Commerce Engine, Marketing Engine, etc.)
  note: string;                  // Council member's observation
  author: string;                // Council member name
  timestamp: string;             // ISO 8601 timestamp
  tags?: string[];               // Auto-extracted or manual tags
  metadata?: {
    originalStatus?: string;     // Capsule status at time of annotation
    relatedCapsules?: string[];  // IDs of related capsules
    impactMetrics?: Record<string, number>; // Quantitative impact data
  };
}
```

## Auto-Tagging System

### Tag Extraction Keywords

The system automatically extracts tags based on note content:

| Tag | Trigger Keywords | Purpose |
|-----|-----------------|---------|
| `correlation` | aligned, correlate, match | Links between events |
| `revenue-impact` | revenue, sales, income | Business impact |
| `performance` | performance, latency, speed | Technical metrics |
| `availability` | uptime, downtime, availability | System availability |
| `degraded-status` | degraded, failing, unstable | Problem identification |
| `recovery` | recovered, restored, fixed | Resolution tracking |
| `pattern-analysis` | pattern, trend, recurring | Pattern recognition |

### Example Annotations

```json
{
  "capsuleId": "12345",
  "engine": "Commerce Engine",
  "note": "Council reflection: revenue dip aligned with degraded status.",
  "tags": ["correlation", "revenue-impact", "degraded-status"]
}
```

**Auto-extracted tags:** `correlation` (aligned), `revenue-impact` (revenue), `degraded-status` (degraded)

## Integration with Replay System

### ReplayViewer Integration

The `CapsuleAnnotationPanel` is integrated into `ReplayViewer` component:

```tsx
{/* In replay-viewer.tsx */}
{!loading && !error && capsules.length > 0 && (
  <div className="mt-6">
    <CapsuleAnnotationPanel
      capsuleId={capsules[index].id}
      engine={capsules[index].engine}
    />
  </div>
)}
```

**Behavior:**
- Panel updates when user navigates between capsules
- Shows annotation form + timeline scoped to current capsule
- Annotations persist across replay sessions

## User Workflows

### 1. Council Member Reviews Replay

```
1. Navigate to replay viewer (/replay or integrated view)
2. Select capsule from timeline
3. Scroll to annotation panel
4. Type observation (e.g., "revenue dip aligned with degraded status")
5. Click "📋 Add Annotation"
6. Annotation appears in timeline with auto-tags
```

### 2. Search Historical Patterns

```
1. Navigate to /annotations dashboard
2. Use search bar: "revenue" or "degraded"
3. Filter by engine: "Commerce Engine"
4. Filter by tag: #revenue-impact or #degraded-status
5. View all matching annotations chronologically
6. Export JSON for external analysis
```

### 3. Correlation Analysis

```
1. View annotation for capsule with degraded status
2. Check metadata.impactMetrics (e.g., revenueDropPercent: 15.3)
3. Click related capsules to compare patterns
4. Add new annotation linking multiple events
5. Tag as #pattern-analysis for future reference
```

## API Reference

### CapsuleAnnotationManager Methods

#### `addAnnotation(data)`
```typescript
addAnnotation({
  capsuleId: string;
  engine: string;
  note: string;
  author?: string;
  tags?: string[];
  metadata?: {
    originalStatus?: string;
    relatedCapsules?: string[];
    impactMetrics?: Record<string, number>;
  };
}): CapsuleAnnotation
```

**Example:**
```typescript
const manager = getCapsuleAnnotationManager();
const annotation = manager.addAnnotation({
  capsuleId: '12345',
  engine: 'Commerce Engine',
  note: 'Revenue dip aligned with degraded status.',
  metadata: {
    originalStatus: 'degraded',
    impactMetrics: {
      revenueDropPercent: 15.3,
      orderProcessingDelay: 850
    }
  }
});
```

#### `getAnnotationsByCapsule(capsuleId)`
Retrieves all annotations for a specific capsule.

#### `getAnnotationsByEngine(engine)`
Retrieves all annotations for a specific engine.

#### `getAnnotationsByTag(tag)`
Retrieves all annotations with a specific tag.

#### `searchAnnotations(query)`
Full-text search across notes, engines, authors, and tags.

#### `getStatistics()`
Returns aggregate statistics:
```typescript
{
  total: number;
  byEngine: Record<string, number>;
  byAuthor: Record<string, number>;
  topTags: Record<string, number>;
}
```

#### `exportToJSON()` / `importFromJSON(json)`
Export/import annotations in JSON format.

## Sample Data

The system seeds 4 sample annotations on first load (see `web/data/sample-capsule-annotations.json`):

1. **Commerce Engine** - Revenue correlation with degraded status
2. **Commerce Engine** - Performance degradation during holiday campaign
3. **Marketing Engine** - Recovery after database optimization
4. **Video Studio** - Performance improvement from Q4 caching strategy

## UI Components

### Annotations Dashboard (/annotations)

**Features:**
- Statistics grid: Total, engines monitored, contributors, unique tags
- Search bar: Full-text search
- Engine filter: Buttons for each engine with annotation count
- Tag filter: Top 8 tags with count
- Annotation cards: Author, timestamp, engine, capsule ID, note, tags, metadata
- Actions: Export JSON, Clear All, Delete individual

**Layout:**
```
┌─────────────────────────────────────────────┐
│ 📋 Capsule Annotations      [📥 Export] [🗑️]│
├─────────────────────────────────────────────┤
│ [Total: 4] [Engines: 3] [Contributors: 2]   │
├─────────────────────────────────────────────┤
│ 🔍 Search: [________________]               │
│ ⚙️ Engine: [All] [Commerce] [Marketing]...  │
│ 🏷️ Tags: [All] [#correlation] [#revenue]... │
├─────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────┐ │
│ │ 👤 Council Member  Dec 7, 2025 6:25 AM │ │
│ │ Commerce Engine • 12345                 │ │
│ │ Revenue dip aligned with degraded...   │ │
│ │ #correlation #revenue-impact           │ │
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

## Storage & Persistence

### localStorage Schema

```javascript
// Key: capsule_annotations
{
  "annotations": [
    {
      "id": "annotation_1733615500000_xyz789abc",
      "capsuleId": "12345",
      "engine": "Commerce Engine",
      "note": "Revenue dip aligned with degraded status.",
      "author": "Council Member",
      "timestamp": "2025-12-07T06:25:00Z",
      "tags": ["correlation", "revenue-impact", "degraded-status"],
      "metadata": {
        "originalStatus": "degraded",
        "impactMetrics": {
          "revenueDropPercent": 15.3
        }
      }
    }
  ]
}
```

## Security & Best Practices

### Data Validation
- Notes are trimmed and validated before storage
- CapsuleId and engine are required fields
- Timestamps use ISO 8601 format
- Metadata is optional and schema-free

### Performance
- Annotations loaded on mount and cached in React state
- Auto-refresh every 10 seconds in dashboard
- LocalStorage sync after each mutation
- Search uses client-side filtering (no backend required)

### Privacy
- Author names stored as-is (no PII validation)
- All data stored locally in browser localStorage
- Export function allows data portability
- No server-side persistence (100% client-side)

## Future Enhancements

### Phase 1: Advanced Analytics
- [ ] Correlation heatmap (engine × tag matrix)
- [ ] Time-series graph of annotations per engine
- [ ] Impact metrics aggregation dashboard
- [ ] Related capsule visualization (graph view)

### Phase 2: Collaboration
- [ ] WebSocket sync for multi-user annotations
- [ ] Reply threads on annotations
- [ ] @mention notifications for other council members
- [ ] Annotation voting/upvoting system

### Phase 3: AI Insights
- [ ] GPT-4 pattern analysis on annotation clusters
- [ ] Auto-suggest related capsules based on content
- [ ] Sentiment analysis of council observations
- [ ] Predictive alerts based on historical patterns

### Phase 4: Integration
- [ ] Export to PostgreSQL for long-term storage
- [ ] Slack/Discord notifications for critical annotations
- [ ] Grafana dashboard with annotation overlays
- [ ] API endpoint for external tools (Jupyter, BI tools)

## Testing Checklist

- [x] Create annotation from replay viewer
- [x] Verify auto-tagging for keywords (revenue, degraded, correlation)
- [x] Search annotations by text query
- [x] Filter by engine (Commerce Engine, Marketing Engine)
- [x] Filter by tag (#correlation, #revenue-impact)
- [x] Delete annotation and verify localStorage update
- [x] Export annotations to JSON file
- [x] Import sample annotations on first load
- [ ] Test annotation with metadata (impactMetrics)
- [ ] Test multi-capsule correlation via relatedCapsules
- [ ] Verify persistence across browser sessions
- [ ] Test with 100+ annotations (performance)

## Navigation

**Quick Links:**
- Dashboard: `/annotations` - Full annotation archive
- Replay Viewer: Contains `CapsuleAnnotationPanel` for current capsule
- Home: `/` - Link to "📋 Capsule Annotations" in Quick Actions

## Support

For questions about the annotation system:
1. Check this documentation first
2. Review sample data in `web/data/sample-capsule-annotations.json`
3. Inspect `CapsuleAnnotationManager` source code
4. Test with seed data using `useSeedAnnotations` hook

---

**Status:** ✅ Complete and ready for production testing

**Last Updated:** December 7, 2025
