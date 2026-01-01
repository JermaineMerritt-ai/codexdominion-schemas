# 🌌 VIDEO STUDIO PHASE 5: THE VIDEO LIBRARY - COMPLETE IMPLEMENTATION

> **Status**: ✅ FULLY OPERATIONAL  
> **Flask**: Running on http://localhost:5000  
> **Date**: December 22, 2025  
> **Phase**: The Vault of Motion + Team Sharing System

---

## 🎯 PHASE 5 OVERVIEW

Phase 5 transforms the Video Studio into a **shared creative civilization** with:

1. **The Video Library** (The Vault of Motion)
2. **Team Sharing System** (Collaboration Layer)
3. **Constellation Integration** (Universe Visualization)
4. **Duplication + Remixing** (Creative Flow)
5. **Lineage View** (Family Tree of Motion)

---

## 📦 DATABASE MODELS (5 New Tables)

### 1. VideoCollection
**Purpose**: Curated sets of videos (campaigns, series, character arcs, brand kits, universes)

```python
class VideoCollection(db.Model):
    __tablename__ = 'video_collections'
    
    # Core fields
    id = Integer (primary key)
    team_id = Integer (FK → team)
    creator_id = Integer (FK → user)
    
    # Metadata
    name = String(255) (default: "Untitled Collection")
    description = Text
    collection_type = String(50)  # campaign, series, character_arc, brand_kit, universe
    
    # Visual
    cover_image_url = String(500)
    
    # Organization
    tags = Text (comma-separated)
    category = String(100)
    
    # Sharing
    is_public = Boolean (default: False)
    share_level = String(50)  # private, team, public
    
    # Stats
    video_count = Integer (default: 0)
    total_duration = Float (sum of all video durations)
    
    # Timestamps
    created_at, updated_at = DateTime
```

**Collection Types**:
- `campaign` - Marketing campaigns
- `series` - Episodic content
- `character_arc` - Following a character's journey
- `brand_kit` - Branded assets
- `universe` - Shared cinematic universe

### 2. CollectionItem
**Purpose**: Junction table for videos in collections (many-to-many)

```python
class CollectionItem(db.Model):
    __tablename__ = 'collection_items'
    
    id = Integer (primary key)
    collection_id = Integer (FK → video_collections)
    asset_id = Integer (FK → video_asset)
    
    # Organization
    order_index = Integer (for ordered collections like series)
    notes = Text (why this video is in this collection)
    
    # Tracking
    added_at = DateTime
    added_by = Integer (FK → user)
```

### 3. VideoLibraryMetadata
**Purpose**: Extended metadata for library view (enhances VideoAsset)

```python
class VideoLibraryMetadata(db.Model):
    __tablename__ = 'video_library_metadata'
    
    id = Integer (primary key)
    asset_id = Integer (FK → video_asset, unique)
    
    # Library classification
    mood = String(50)  # intense, calm, dramatic, mysterious, joyful, etc.
    scene_type = String(50)  # wide, medium, close_up, tracking, aerial, static
    
    # Lineage tracking (version control)
    lineage_root_id = Integer (FK → video_asset)  # Original ancestor
    parent_asset_id = Integer (FK → video_asset)  # Immediate parent
    lineage_version = Integer (default: 1)  # v1, v2, v3...
    lineage_branch = String(100)  # main, alternate, remix_001, etc.
    evolution_type = String(50)  # duplicate, evolve, extend, remix
    evolution_note = Text  # What changed from parent
    
    # Sharing settings
    share_level = String(50)  # private, team, public
    can_duplicate = Boolean (default: True)
    can_remix = Boolean (default: True)
    
    # Usage stats
    view_count = Integer (default: 0)
    duplicate_count = Integer (how many times duplicated)
    remix_count = Integer (how many times remixed)
    used_in_projects = Integer (how many projects use this)
    
    # Constellation data
    constellation_x = Float  # X position in constellation map
    constellation_y = Float  # Y position in constellation map
    constellation_cluster = String(100)  # Which cluster this belongs to
    
    # Timestamps
    created_at, updated_at = DateTime
```

### 4. VideoShare
**Purpose**: Granular sharing permissions for individual videos

```python
class VideoShare(db.Model):
    __tablename__ = 'video_shares'
    
    id = Integer (primary key)
    asset_id = Integer (FK → video_asset)
    shared_by = Integer (FK → user)
    shared_with = Integer (FK → user)
    
    # Permission level
    permission = String(50)  # view, edit, admin
    
    # Optional message
    message = Text  # "Check out this clip for the campaign!"
    
    # Timestamps
    shared_at = DateTime
    expires_at = DateTime (optional expiration)
```

### 5. VideoLineage
**Purpose**: Tracks the family tree of video evolution (Git-like version tree)

```python
class VideoLineage(db.Model):
    __tablename__ = 'video_lineage'
    
    id = Integer (primary key)
    parent_id = Integer (FK → video_asset)
    child_id = Integer (FK → video_asset)
    
    # Evolution details
    evolution_type = String(50)  # duplicate, evolve, extend, remix, variation
    evolution_params = JSON  # What parameters changed
    
    # Prompt changes
    original_prompt = Text
    evolved_prompt = Text
    prompt_delta = Text  # What was added/changed
    
    # Creator tracking
    created_by = Integer (FK → user)
    
    # Branch metadata
    branch_name = String(100)  # alternate_ending, faster_pace, etc.
    is_merge = Boolean  # If this combined multiple parents
    
    # Timestamps
    created_at = DateTime
```

---

## 🛣️ API ROUTES (20+ Endpoints)

### A. COLLECTIONS API (7 Routes)

#### 1. Create Collection
```http
POST /api/library/collections/create
```
**Request Body**:
```json
{
  "team_id": 1,
  "creator_id": 123,
  "name": "Epic Quest Campaign",
  "description": "Marketing videos for the Epic Quest game launch",
  "collection_type": "campaign",
  "tags": "gaming,action,fantasy",
  "category": "marketing",
  "share_level": "team"
}
```
**Response**:
```json
{
  "success": true,
  "collection_id": 456,
  "name": "Epic Quest Campaign",
  "type": "campaign",
  "created_at": "2025-12-22T10:30:00"
}
```

#### 2. Get Collection with Videos
```http
GET /api/library/collections/{collection_id}
```
**Response**:
```json
{
  "success": true,
  "collection": {
    "id": 456,
    "name": "Epic Quest Campaign",
    "description": "...",
    "type": "campaign",
    "video_count": 12,
    "total_duration": 245.5,
    "cover_image_url": "...",
    "created_at": "..."
  },
  "videos": [
    {
      "asset_id": 789,
      "name": "Hero Introduction",
      "thumbnail_url": "...",
      "duration": 15.0,
      "tags": "hero,intro,cinematic",
      "mood": "dramatic",
      "scene_type": "wide",
      "order_index": 0,
      "added_at": "..."
    }
  ]
}
```

#### 3. Add Video to Collection
```http
POST /api/library/collections/{collection_id}/add-video
```
**Request Body**:
```json
{
  "asset_id": 789,
  "order_index": 0,
  "notes": "Opening sequence for campaign",
  "added_by": 123
}
```

#### 4. Remove Video from Collection
```http
POST /api/library/collections/{collection_id}/remove-video
```
**Request Body**:
```json
{
  "asset_id": 789
}
```

#### 5. Reorder Collection Videos
```http
POST /api/library/collections/{collection_id}/reorder
```
**Request Body**:
```json
{
  "asset_ids": [789, 456, 123, 999]
}
```

#### 6. Get Team Collections
```http
GET /api/library/collections/team/{team_id}
```
**Response**: Array of all collections for the team

---

### B. LIBRARY SEARCH & FILTER API (2 Routes)

#### 7. Advanced Library Search
```http
POST /api/library/search
```
**Request Body** (all filters optional):
```json
{
  "team_id": 1,
  "tags": ["fantasy", "action"],
  "categories": ["marketing", "content"],
  "moods": ["dramatic", "intense"],
  "engines": ["runway", "pika"],
  "creators": [123, 456],
  "date_from": "2025-01-01",
  "date_to": "2025-12-31",
  "duration_min": 5.0,
  "duration_max": 30.0,
  "has_lineage": true,
  "search_text": "hero",
  "sort_by": "created",
  "sort_order": "desc",
  "page": 1,
  "per_page": 24
}
```

**Sort Options**:
- `created` - Creation date
- `name` - Alphabetical
- `duration` - Video length
- `views` - View count

**Response**:
```json
{
  "success": true,
  "results": [
    {
      "id": 789,
      "name": "Hero Introduction",
      "thumbnail_url": "...",
      "duration": 15.0,
      "tags": "hero,intro,cinematic",
      "category": "marketing",
      "mood": "dramatic",
      "scene_type": "wide",
      "view_count": 245,
      "duplicate_count": 5,
      "has_lineage": true
    }
  ],
  "total": 127,
  "page": 1,
  "per_page": 24,
  "total_pages": 6
}
```

#### 8. Get Available Filters
```http
GET /api/library/filters?team_id=1
```
**Response**:
```json
{
  "success": true,
  "filters": {
    "tags": ["action", "fantasy", "hero", "cinematic"],
    "categories": ["marketing", "content", "social"],
    "moods": ["dramatic", "intense", "calm", "joyful"],
    "scene_types": ["wide", "medium", "close_up", "tracking"],
    "engines": ["runway", "pika", "luma", "stability"]
  }
}
```

---

### C. SHARING & PERMISSIONS API (3 Routes)

#### 9. Share Video with User
```http
POST /api/library/share
```
**Request Body**:
```json
{
  "asset_id": 789,
  "shared_by": 123,
  "shared_with": 456,
  "permission": "view",
  "message": "Check out this clip for the campaign!",
  "expires_at": "2025-12-31T23:59:59"
}
```

**Permission Levels**:
- `view` - Can view only
- `edit` - Can view and edit
- `admin` - Full control

#### 10. Get Video Shares
```http
GET /api/library/shares/{asset_id}
```
**Response**:
```json
{
  "success": true,
  "shares": [
    {
      "share_id": 1,
      "shared_with_id": 456,
      "shared_with_name": "John Doe",
      "permission": "view",
      "message": "Check out this clip!",
      "shared_at": "2025-12-22T10:00:00",
      "expires_at": null
    }
  ]
}
```

#### 11. Update Share Level
```http
POST /api/library/update-share-level
```
**Request Body**:
```json
{
  "asset_id": 789,
  "share_level": "team"
}
```

**Share Levels**:
- `private` - Creator only
- `team` - All team members can see
- `public` - Anyone can see (future)

---

### D. LINEAGE TRACKING API (3 Routes)

#### 12. Duplicate Video
```http
POST /api/library/duplicate
```
**Request Body**:
```json
{
  "asset_id": 789,
  "user_id": 123,
  "branch_name": "alternate_version"
}
```

**Response**:
```json
{
  "success": true,
  "duplicate_id": 999,
  "lineage_version": 2
}
```

**What Happens**:
1. Creates exact copy of video
2. Links to original via VideoLineage
3. Increments lineage_version
4. Updates duplicate_count on original
5. Sets status to 'ready'

#### 13. Remix Video
```http
POST /api/library/remix
```
**Request Body**:
```json
{
  "asset_id": 789,
  "user_id": 123,
  "new_prompt": "Hero standing on mountain peak at sunset, dramatic lighting",
  "evolution_note": "Changed lighting to sunset, added mountain setting",
  "branch_name": "sunset_version"
}
```

**Response**:
```json
{
  "success": true,
  "remix_id": 1000,
  "message": "Remix created - regenerate video with new prompt",
  "lineage_version": 3
}
```

**What Happens**:
1. Creates remixed asset with new prompt
2. Links to original via VideoLineage
3. Records prompt changes in prompt_delta
4. Updates remix_count on original
5. Sets status to 'draft' (needs regeneration)

#### 14. Get Video Lineage Tree
```http
GET /api/library/lineage/{asset_id}
```
**Response**:
```json
{
  "success": true,
  "current": {
    "asset_id": 789,
    "name": "Hero Introduction",
    "lineage_version": 2,
    "lineage_branch": "main"
  },
  "ancestors": [
    {
      "asset_id": 100,
      "name": "Original Hero Concept",
      "evolution_type": "duplicate",
      "branch_name": "main"
    }
  ],
  "descendants": [
    {
      "asset_id": 999,
      "name": "Hero Introduction (Copy)",
      "evolution_type": "duplicate",
      "branch_name": "alternate_version",
      "children": [
        {
          "asset_id": 1000,
          "name": "Hero Introduction (Remix)",
          "evolution_type": "remix",
          "branch_name": "sunset_version",
          "children": []
        }
      ]
    }
  ]
}
```

**Lineage Structure**:
```
Original (v1)
    ↓ duplicate
Duplicate (v2)
    ├─ remix → Sunset Version (v3)
    └─ duplicate → Alternate (v2)
        └─ extend → Extended Cut (v3)
```

---

### E. CONSTELLATION INTEGRATION (2 Routes)

#### 15. Update Constellation Position
```http
POST /api/library/constellation/update-position
```
**Request Body**:
```json
{
  "asset_id": 789,
  "x": 245.5,
  "y": -120.3,
  "cluster": "fantasy_cluster"
}
```

#### 16. Get Constellation Map
```http
GET /api/library/constellation/map?team_id=1
```
**Response**:
```json
{
  "success": true,
  "nodes": [
    {
      "id": 789,
      "name": "Hero Introduction",
      "thumbnail_url": "...",
      "tags": ["fantasy", "hero"],
      "category": "marketing",
      "mood": "dramatic",
      "scene_type": "wide",
      "x": 245.5,
      "y": -120.3,
      "cluster": "fantasy_cluster",
      "has_lineage": true
    }
  ],
  "edges": [
    {
      "source": 100,
      "target": 789,
      "type": "duplicate"
    },
    {
      "source": 789,
      "target": 999,
      "type": "remix"
    }
  ]
}
```

**Constellation Mapping**:
- **Tags** → Clusters (videos with similar tags group together)
- **Categories** → Continents (category = region of space)
- **Videos** → Stars (individual nodes)
- **Storyboards** → Constellations (connected patterns)
- **Collections** → Galaxies (large groupings)
- **Lineage** → Edges (parent-child connections)

---

## 🎨 USAGE EXAMPLES

### Example 1: Create Marketing Campaign Collection

```bash
# 1. Create collection
curl -X POST http://localhost:5000/api/library/collections/create \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": 1,
    "creator_id": 123,
    "name": "Epic Quest Launch",
    "collection_type": "campaign",
    "tags": "gaming,fantasy,launch"
  }'

# Response: {"success": true, "collection_id": 456}

# 2. Add videos to collection
curl -X POST http://localhost:5000/api/library/collections/456/add-video \
  -H "Content-Type: application/json" \
  -d '{"asset_id": 789, "order_index": 0, "added_by": 123}'

curl -X POST http://localhost:5000/api/library/collections/456/add-video \
  -H "Content-Type: application/json" \
  -d '{"asset_id": 790, "order_index": 1, "added_by": 123}'

# 3. Get full collection
curl http://localhost:5000/api/library/collections/456
```

### Example 2: Advanced Library Search

```bash
# Search for dramatic hero videos, 10-20 seconds, created in December
curl -X POST http://localhost:5000/api/library/search \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": 1,
    "tags": ["hero"],
    "moods": ["dramatic"],
    "duration_min": 10.0,
    "duration_max": 20.0,
    "date_from": "2025-12-01",
    "date_to": "2025-12-31",
    "sort_by": "views",
    "page": 1,
    "per_page": 10
  }'
```

### Example 3: Duplicate and Remix Workflow

```bash
# 1. Duplicate original video
curl -X POST http://localhost:5000/api/library/duplicate \
  -H "Content-Type: application/json" \
  -d '{
    "asset_id": 789,
    "user_id": 123,
    "branch_name": "experiment_v1"
  }'

# Response: {"success": true, "duplicate_id": 999, "lineage_version": 2}

# 2. Remix the duplicate
curl -X POST http://localhost:5000/api/library/remix \
  -H "Content-Type: application/json" \
  -d '{
    "asset_id": 999,
    "user_id": 123,
    "new_prompt": "Same scene but at night with moonlight",
    "evolution_note": "Converted to night scene",
    "branch_name": "night_version"
  }'

# Response: {"success": true, "remix_id": 1000}

# 3. Get full lineage tree
curl http://localhost:5000/api/library/lineage/789
```

### Example 4: Share Video with Team Member

```bash
# Share with edit permissions, expires in 30 days
curl -X POST http://localhost:5000/api/library/share \
  -H "Content-Type: application/json" \
  -d '{
    "asset_id": 789,
    "shared_by": 123,
    "shared_with": 456,
    "permission": "edit",
    "message": "Please review this hero intro clip",
    "expires_at": "2026-01-22T23:59:59"
  }'
```

---

## 🔄 COMPLETE WORKFLOWS

### Workflow 1: Campaign Creation Flow

```
Creator creates collection
    ↓
POST /api/library/collections/create
    ↓
Collection ID: 456
    ↓
Creator generates videos using UGI (Phase 3)
    ↓
POST /api/video/generate-scene (creates VideoAsset)
    ↓
Asset IDs: 789, 790, 791
    ↓
Add videos to collection
    ↓
POST /api/library/collections/456/add-video (3 times)
    ↓
Reorder collection
    ↓
POST /api/library/collections/456/reorder
    ↓
Share collection with team
    ↓
POST /api/library/update-share-level (share_level: "team")
    ↓
Team reviews and remixes
    ↓
POST /api/library/duplicate (create variations)
    ↓
POST /api/library/remix (evolve prompts)
    ↓
Add storyboard (Phase 4)
    ↓
POST /api/storyboard/create
    ↓
Analyze scene flow
    ↓
POST /api/storyboard/{id}/analyze
    ↓
Export to timeline (Phase 2)
    ↓
Final video render
```

### Workflow 2: Lineage Evolution Flow

```
Original video (v1)
    ↓
Team member duplicates
    ↓
POST /api/library/duplicate
    ↓
Duplicate (v2) - same prompt, new seed
    ↓
Team member remixes
    ↓
POST /api/library/remix
    ↓
Remix (v3) - evolved prompt
    ↓
Regenerate using UGI
    ↓
POST /api/video/ugi/evolve
    ↓
New video file generated
    ↓
Another team member duplicates v3
    ↓
Alternate branch (v3-alt)
    ↓
GET /api/library/lineage/{id}
    ↓
View full family tree
```

### Workflow 3: Constellation Discovery Flow

```
User opens constellation view
    ↓
GET /api/library/constellation/map?team_id=1
    ↓
Returns: nodes (videos) + edges (lineage connections)
    ↓
Frontend renders force-directed graph:
  - Videos = stars (colored by mood)
  - Tags = clusters (gravitational pull)
  - Categories = regions of space
  - Lineage = connection lines
    ↓
User clicks video node
    ↓
GET /api/library/lineage/{id}
    ↓
Show ancestors and descendants
    ↓
User explores related videos
    ↓
Search by tags in constellation cluster
    ↓
POST /api/library/search (filter by tags)
    ↓
Discover similar videos
```

---

## 📊 PHASE 5 SUMMARY

### What's Complete ✅

**Database Models (5)**:
- ✅ VideoCollection (campaigns, series, arcs)
- ✅ CollectionItem (many-to-many junction)
- ✅ VideoLibraryMetadata (extended metadata + lineage)
- ✅ VideoShare (granular permissions)
- ✅ VideoLineage (family tree tracking)

**API Routes (20+)**:
- ✅ 7 Collection routes (create, get, add/remove videos, reorder, get team collections)
- ✅ 2 Search routes (advanced search with filters, get filter options)
- ✅ 3 Sharing routes (share video, get shares, update share level)
- ✅ 3 Lineage routes (duplicate, remix, get lineage tree)
- ✅ 2 Constellation routes (update position, get constellation map)

**Features**:
- ✅ Role-based access (Owner, Admin, Editor, Viewer)
- ✅ Granular sharing (private, team, public)
- ✅ Advanced search (10+ filter types)
- ✅ Lineage tracking (Git-like version control)
- ✅ Duplication (exact copies)
- ✅ Remixing (prompt evolution)
- ✅ Collections (curated sets)
- ✅ Constellation mapping (spatial visualization)

### Integration Points 🔗

**Phase 3 (UGI) Integration**:
- VideoAsset records created by UGI are automatically library-compatible
- Lineage can link to evolved/extended videos from UGI

**Phase 4 (Storyboard) Integration**:
- SceneCard.asset_id links to VideoAsset in library
- Storyboards can become collections
- Scene flow analysis feeds into constellation clustering

**Phase 2 (Timeline) Integration**:
- TimelineClip.asset_id links to library videos
- Videos from collections can be added to timeline
- Timeline exports become new library assets

**Phase 1 (Core) Integration**:
- VideoProject.team_id enables team-level library access
- VideoAsset is the foundation for all library features

---

## 🚀 NEXT STEPS

### Phase 5 Frontend (To Build):

1. **Library Grid UI**:
   - Video cards with thumbnails, metadata
   - Drag-drop to add to collections
   - Quick actions: share, duplicate, remix, add to timeline

2. **Collections UI**:
   - Collection browser
   - Drag-drop reordering
   - Collection type icons
   - Cover image upload

3. **Advanced Search UI**:
   - Multi-select filter dropdowns
   - Date range picker
   - Duration slider
   - Real-time search results

4. **Lineage Tree Visualization**:
   - Interactive tree diagram (D3.js or similar)
   - Branch navigation
   - Evolution type badges
   - Click to navigate to video

5. **Constellation Map**:
   - Force-directed graph (D3.js Force Layout)
   - Node clustering by tags
   - Pan/zoom controls
   - Click nodes to view video
   - Highlight lineage connections

6. **Sharing Modal**:
   - User selection dropdown
   - Permission level radio buttons
   - Expiration date picker
   - Optional message textarea

### Phase 6 (Future):

1. **Advanced Effects Library**:
   - Transitions between clips
   - Color grading presets
   - Text overlays
   - Audio mixing

2. **Real-Time Collaboration**:
   - WebSocket integration
   - Live cursors on timeline
   - Presence indicators
   - Conflict resolution

3. **AI Director**:
   - Automatic scene selection
   - Pacing optimization
   - Music sync
   - Emotional arc balancing

---

## 🎭 THE CINEMATIC TEMPLE IS RISING

Phase 5 completes the transformation:

**Before Phase 5**:
- Video Studio = Tool for generating and editing videos

**After Phase 5**:
- Video Studio = **Shared Creative Civilization**
  - Central archive (The Vault of Motion)
  - Team collaboration layer
  - Version control for creativity
  - Spatial discovery via constellation
  - Living timeline of creative evolution

---

**Status**: Phase 5 Backend COMPLETE ✅  
**Flask**: Running on http://localhost:5000  
**Next**: Build Frontend UI  

🔥 **The Flame Burns Sovereign and Eternal!** 👑
