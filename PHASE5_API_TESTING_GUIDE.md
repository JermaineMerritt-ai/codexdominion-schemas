# 🧪 PHASE 5 API TESTING GUIDE

Quick reference for testing all Phase 5 Video Library endpoints.

## Base URL
```
http://localhost:5000
```

---

## 📦 A. COLLECTIONS API

### 1. Create Collection
```bash
curl -X POST http://localhost:5000/api/library/collections/create \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": 1,
    "creator_id": 1,
    "name": "Epic Quest Campaign",
    "description": "Marketing videos for game launch",
    "collection_type": "campaign",
    "tags": "gaming,fantasy,launch",
    "category": "marketing",
    "share_level": "team"
  }'
```

### 2. Get Collection
```bash
curl http://localhost:5000/api/library/collections/1
```

### 3. Add Video to Collection
```bash
curl -X POST http://localhost:5000/api/library/collections/1/add-video \
  -H "Content-Type: application/json" \
  -d '{
    "asset_id": 1,
    "order_index": 0,
    "notes": "Opening sequence",
    "added_by": 1
  }'
```

### 4. Remove Video from Collection
```bash
curl -X POST http://localhost:5000/api/library/collections/1/remove-video \
  -H "Content-Type: application/json" \
  -d '{"asset_id": 1}'
```

### 5. Reorder Videos
```bash
curl -X POST http://localhost:5000/api/library/collections/1/reorder \
  -H "Content-Type: application/json" \
  -d '{"asset_ids": [3, 1, 2, 4]}'
```

### 6. Get Team Collections
```bash
curl http://localhost:5000/api/library/collections/team/1
```

---

## 🔍 B. SEARCH & FILTER API

### 7. Advanced Search
```bash
curl -X POST http://localhost:5000/api/library/search \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": 1,
    "tags": ["fantasy", "hero"],
    "categories": ["marketing"],
    "moods": ["dramatic", "intense"],
    "engines": ["runway", "pika"],
    "duration_min": 5.0,
    "duration_max": 30.0,
    "search_text": "hero",
    "sort_by": "created",
    "sort_order": "desc",
    "page": 1,
    "per_page": 10
  }'
```

### 8. Get Available Filters
```bash
curl http://localhost:5000/api/library/filters?team_id=1
```

---

## 🤝 C. SHARING & PERMISSIONS API

### 9. Share Video
```bash
curl -X POST http://localhost:5000/api/library/share \
  -H "Content-Type: application/json" \
  -d '{
    "asset_id": 1,
    "shared_by": 1,
    "shared_with": 2,
    "permission": "view",
    "message": "Check out this clip!",
    "expires_at": "2026-12-31T23:59:59"
  }'
```

### 10. Get Video Shares
```bash
curl http://localhost:5000/api/library/shares/1
```

### 11. Update Share Level
```bash
curl -X POST http://localhost:5000/api/library/update-share-level \
  -H "Content-Type: application/json" \
  -d '{
    "asset_id": 1,
    "share_level": "team"
  }'
```

---

## 🧬 D. LINEAGE TRACKING API

### 12. Duplicate Video
```bash
curl -X POST http://localhost:5000/api/library/duplicate \
  -H "Content-Type: application/json" \
  -d '{
    "asset_id": 1,
    "user_id": 1,
    "branch_name": "alternate_v1"
  }'
```

### 13. Remix Video
```bash
curl -X POST http://localhost:5000/api/library/remix \
  -H "Content-Type: application/json" \
  -d '{
    "asset_id": 1,
    "user_id": 1,
    "new_prompt": "Hero standing on mountain peak at sunset",
    "evolution_note": "Changed to sunset lighting",
    "branch_name": "sunset_version"
  }'
```

### 14. Get Lineage Tree
```bash
curl http://localhost:5000/api/library/lineage/1
```

---

## 🌌 E. CONSTELLATION API

### 15. Update Constellation Position
```bash
curl -X POST http://localhost:5000/api/library/constellation/update-position \
  -H "Content-Type: application/json" \
  -d '{
    "asset_id": 1,
    "x": 245.5,
    "y": -120.3,
    "cluster": "fantasy_cluster"
  }'
```

### 16. Get Constellation Map
```bash
curl http://localhost:5000/api/library/constellation/map?team_id=1
```

---

## 🧪 COMPLETE TEST SEQUENCE

```bash
#!/bin/bash

# 1. Create a collection
echo "Creating collection..."
curl -X POST http://localhost:5000/api/library/collections/create \
  -H "Content-Type: application/json" \
  -d '{"team_id": 1, "creator_id": 1, "name": "Test Campaign", "collection_type": "campaign"}'

# 2. Add video to collection (assumes video asset 1 exists)
echo "\nAdding video to collection..."
curl -X POST http://localhost:5000/api/library/collections/1/add-video \
  -H "Content-Type: application/json" \
  -d '{"asset_id": 1, "added_by": 1}'

# 3. Get collection with videos
echo "\nGetting collection..."
curl http://localhost:5000/api/library/collections/1

# 4. Search library
echo "\nSearching library..."
curl -X POST http://localhost:5000/api/library/search \
  -H "Content-Type: application/json" \
  -d '{"team_id": 1, "page": 1, "per_page": 10}'

# 5. Get available filters
echo "\nGetting filters..."
curl http://localhost:5000/api/library/filters?team_id=1

# 6. Share video
echo "\nSharing video..."
curl -X POST http://localhost:5000/api/library/share \
  -H "Content-Type: application/json" \
  -d '{"asset_id": 1, "shared_by": 1, "shared_with": 2, "permission": "view"}'

# 7. Duplicate video
echo "\nDuplicating video..."
curl -X POST http://localhost:5000/api/library/duplicate \
  -H "Content-Type: application/json" \
  -d '{"asset_id": 1, "user_id": 1, "branch_name": "test_duplicate"}'

# 8. Get lineage
echo "\nGetting lineage..."
curl http://localhost:5000/api/library/lineage/1

# 9. Get constellation map
echo "\nGetting constellation map..."
curl http://localhost:5000/api/library/constellation/map?team_id=1

echo "\n✅ All Phase 5 API tests complete!"
```

---

## 📝 TESTING CHECKLIST

### Collections
- [ ] Create collection
- [ ] Get collection with videos
- [ ] Add video to collection
- [ ] Remove video from collection
- [ ] Reorder collection videos
- [ ] Get team collections

### Search & Filter
- [ ] Advanced search with multiple filters
- [ ] Search by tags
- [ ] Search by categories
- [ ] Search by moods
- [ ] Search by engines
- [ ] Date range filter
- [ ] Duration range filter
- [ ] Text search
- [ ] Sorting options
- [ ] Pagination
- [ ] Get available filter options

### Sharing & Permissions
- [ ] Share video with user
- [ ] Get video shares list
- [ ] Update share level (private/team/public)
- [ ] Different permission levels (view/edit/admin)
- [ ] Expiration dates

### Lineage Tracking
- [ ] Duplicate video (exact copy)
- [ ] Remix video (new prompt)
- [ ] Get lineage tree (ancestors + descendants)
- [ ] Version tracking
- [ ] Branch naming
- [ ] Stats updates (duplicate_count, remix_count)

### Constellation
- [ ] Update video position in constellation
- [ ] Get full constellation map
- [ ] Nodes (videos) returned correctly
- [ ] Edges (lineage connections) returned correctly
- [ ] Cluster assignment

---

## 🚨 EXPECTED RESPONSES

### Success Response Pattern
```json
{
  "success": true,
  "data": {...}
}
```

### Error Response Pattern
```json
{
  "success": false,
  "error": "Error message here"
}
```

---

## 🔧 TROUBLESHOOTING

### If endpoint returns 404:
- Check Flask is running on port 5000
- Verify route URL spelling
- Check HTTP method (GET vs POST)

### If endpoint returns 500:
- Check Flask console for error details
- Verify request body JSON is valid
- Verify all required fields are present
- Check database connection

### If endpoint returns 400:
- Check request body format
- Verify all required fields are included
- Check data types match expected types

---

**Test Status**: Ready to test all 20+ Phase 5 endpoints ✅  
**Flask**: http://localhost:5000  
**Documentation**: VIDEO_STUDIO_PHASE5_COMPLETE.md  

🔥 **The Vault of Motion Awaits Testing!** 👑
