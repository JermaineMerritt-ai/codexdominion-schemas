# USER ONBOARDING ENDPOINT
**CodexDominion Authentication System**  
**Version 1.1.0** | December 23, 2025

---

## 🎯 OVERVIEW

After successful registration, users complete onboarding by selecting their role type: **creator**, **youth**, or **both**. This determines their initial experience and recommended actions.

---

## 📡 ENDPOINT

### Complete User Onboarding

**Endpoint:** `POST /api/auth/onboarding`

**Request Body:**
```json
{
  "userId": "user_abc123",
  "role": "creator",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Field Requirements:**
- `userId`: Required, string (user ID from registration)
- `role`: Required, enum (`"creator"`, `"youth"`, or `"both"`)
- `token`: Required, string (JWT token from login/registration)

---

## ✅ SUCCESS RESPONSES

### Creator Onboarding (200)
```json
{
  "success": true,
  "message": "Welcome, Creator! 🎨 Start uploading your products and earning.",
  "user": {
    "id": "user_abc123",
    "name": "Marcus Thompson",
    "email": "marcus@example.com",
    "role": "viewer",
    "user_type": "creator",
    "onboarding_completed": true,
    "created_at": "2025-12-23T10:30:00.000000Z"
  },
  "next_steps": [
    {
      "title": "Upload Your First Product",
      "description": "Share your digital creations with the community",
      "url": "/upload",
      "icon": "📦"
    },
    {
      "title": "Set Up Your Profile",
      "description": "Tell the community about yourself",
      "url": "/profile/edit",
      "icon": "👤"
    },
    {
      "title": "Explore Marketplace",
      "description": "See what other creators are sharing",
      "url": "/marketplace",
      "icon": "🛍️"
    }
  ]
}
```

### Youth Onboarding (200)
```json
{
  "success": true,
  "message": "Welcome, Youth! 🔥 Start exploring challenges and rising up the leaderboard.",
  "user": {
    "id": "user_xyz789",
    "name": "Sarah Johnson",
    "email": "sarah@example.com",
    "role": "viewer",
    "user_type": "youth",
    "onboarding_completed": true,
    "created_at": "2025-12-23T11:00:00.000000Z"
  },
  "next_steps": [
    {
      "title": "View Challenges",
      "description": "Complete challenges to earn badges and climb the leaderboard",
      "url": "/challenges",
      "icon": "🏆"
    },
    {
      "title": "Check Leaderboard",
      "description": "See where you rank among the community",
      "url": "/leaderboard",
      "icon": "👑"
    },
    {
      "title": "Explore Products",
      "description": "Discover digital products from Caribbean creators",
      "url": "/marketplace",
      "icon": "🛍️"
    }
  ]
}
```

### Both Creator & Youth (200)
```json
{
  "success": true,
  "message": "Welcome! 👑 You're ready to create AND compete. Let's go!",
  "user": {
    "id": "user_def456",
    "name": "Alex Rodriguez",
    "email": "alex@example.com",
    "role": "viewer",
    "user_type": "both",
    "onboarding_completed": true,
    "created_at": "2025-12-23T11:30:00.000000Z"
  },
  "next_steps": [
    {
      "title": "Upload Your First Product",
      "description": "Share your digital creations",
      "url": "/upload",
      "icon": "📦"
    },
    {
      "title": "Complete Challenges",
      "description": "Earn badges and climb the leaderboard",
      "url": "/challenges",
      "icon": "🏆"
    },
    {
      "title": "Explore Community",
      "description": "Connect with creators and youth",
      "url": "/community",
      "icon": "🌎"
    }
  ]
}
```

---

## ❌ ERROR RESPONSES

### Missing User ID (400)
```json
{
  "success": false,
  "error": "User ID is required",
  "field": "userId"
}
```

### Missing Role (400)
```json
{
  "success": false,
  "error": "Role selection is required",
  "field": "role"
}
```

### Invalid Role Value (400)
```json
{
  "success": false,
  "error": "Role must be \"creator\", \"youth\", or \"both\"",
  "field": "role"
}
```

### Invalid Token (401)
```json
{
  "success": false,
  "error": "Invalid or expired token"
}
```

### User ID Mismatch (403)
```json
{
  "success": false,
  "error": "User ID does not match token"
}
```

### User Not Found (404)
```json
{
  "success": false,
  "error": "User not found"
}
```

---

## 🎨 FRONTEND INTEGRATION

### React/Next.js Example

```typescript
// services/onboarding.ts

interface OnboardingPayload {
  userId: string;
  role: 'creator' | 'youth' | 'both';
  token: string;
}

interface NextStep {
  title: string;
  description: string;
  url: string;
  icon: string;
}

interface OnboardingResponse {
  success: boolean;
  message: string;
  user: {
    id: string;
    name: string;
    email: string;
    role: string;
    user_type: string;
    onboarding_completed: boolean;
    created_at: string;
  };
  next_steps: NextStep[];
}

export const completeOnboarding = async (
  userId: string,
  role: 'creator' | 'youth' | 'both',
  token: string
): Promise<OnboardingResponse> => {
  const response = await fetch('/api/auth/onboarding', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ userId, role, token }),
  });

  const data = await response.json();

  if (!data.success) {
    throw new Error(data.error);
  }

  return data;
};
```

### Onboarding Component

```tsx
// components/OnboardingRoleSelection.tsx
import { useState } from 'react';
import { completeOnboarding } from '@/services/onboarding';

interface Props {
  userId: string;
  token: string;
  onComplete: () => void;
}

export default function OnboardingRoleSelection({ userId, token, onComplete }: Props) {
  const [selectedRole, setSelectedRole] = useState<'creator' | 'youth' | 'both' | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    if (!selectedRole) {
      setError('Please select a role');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const result = await completeOnboarding(userId, selectedRole, token);
      
      // Show success message
      alert(result.message);
      
      // Redirect or show next steps
      onComplete();
      
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="onboarding-container">
      <h1>Welcome to CodexDominion! 👑</h1>
      <p>Tell us about yourself to get started</p>

      {error && <div className="error">{error}</div>}

      <div className="role-options">
        <button
          className={`role-card ${selectedRole === 'creator' ? 'selected' : ''}`}
          onClick={() => setSelectedRole('creator')}
        >
          <span className="icon">🎨</span>
          <h3>Creator</h3>
          <p>Upload and sell your digital products</p>
        </button>

        <button
          className={`role-card ${selectedRole === 'youth' ? 'selected' : ''}`}
          onClick={() => setSelectedRole('youth')}
        >
          <span className="icon">🔥</span>
          <h3>Youth</h3>
          <p>Complete challenges and climb the leaderboard</p>
        </button>

        <button
          className={`role-card ${selectedRole === 'both' ? 'selected' : ''}`}
          onClick={() => setSelectedRole('both')}
        >
          <span className="icon">👑</span>
          <h3>Both</h3>
          <p>Create products AND compete in challenges</p>
        </button>
      </div>

      <button
        className="btn-primary"
        onClick={handleSubmit}
        disabled={!selectedRole || loading}
      >
        {loading ? 'Starting your journey...' : 'Continue 🚀'}
      </button>
    </div>
  );
}
```

---

## 🔄 COMPLETE USER FLOW

### 1. Registration
```
POST /api/auth/register
→ Returns: user object + JWT token
```

### 2. Onboarding
```
POST /api/auth/onboarding
→ User selects role (creator/youth/both)
→ Returns: updated user + next_steps
```

### 3. Dashboard
```
User is redirected to dashboard
Next steps are displayed based on role
```

---

## 📊 USER TYPES & NEXT STEPS

### Creator Role
**Next Steps:**
1. 📦 Upload Your First Product
2. 👤 Set Up Your Profile
3. 🛍️ Explore Marketplace

**Primary Features:**
- Product upload
- Sales tracking
- Earnings dashboard
- Share links

### Youth Role
**Next Steps:**
1. 🏆 View Challenges
2. 👑 Check Leaderboard
3. 🛍️ Explore Products

**Primary Features:**
- Challenge completion
- Leaderboard ranking
- Badge collection
- Community interaction

### Both (Creator + Youth)
**Next Steps:**
1. 📦 Upload Your First Product
2. 🏆 Complete Challenges
3. 🌎 Explore Community

**Primary Features:**
- All creator features
- All youth features
- Enhanced profile
- Dual dashboard view

---

## 🧪 TESTING

### Test Onboarding

```bash
# First, register and get token
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"TestPass123"}'

# Save the token and user_id from response

# Complete onboarding as creator
curl -X POST http://localhost:5000/api/auth/onboarding \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user_abc123",
    "role": "creator",
    "token": "YOUR_TOKEN_HERE"
  }'
```

### Test Script

```bash
python test_auth_api.py
```

**Expected Result:**
- Test 8: ✅ Onboarding successful!

---

## 💾 DATABASE CHANGES

### User Model Updates

**Added Fields:**
```python
user_type = Column(String, nullable=True)  # 'creator', 'youth', or 'both'
onboarding_completed = Column(Boolean, default=False)
```

**Migration Required:**
```sql
ALTER TABLE users ADD COLUMN user_type VARCHAR(20);
ALTER TABLE users ADD COLUMN onboarding_completed BOOLEAN DEFAULT FALSE;
```

---

## ✅ IMPLEMENTATION CHECKLIST

- [x] Add `user_type` field to User model
- [x] Add `onboarding_completed` field to User model
- [x] Create onboarding endpoint
- [x] Validate role values (creator/youth/both)
- [x] Verify JWT token in onboarding
- [x] Return role-specific next steps
- [x] Add test for onboarding endpoint
- [x] Update documentation

---

## 🚀 NEXT FEATURES

### Phase 1 (Complete)
✅ User registration  
✅ JWT authentication  
✅ Role selection onboarding  

### Phase 2 (TODO)
- [ ] Profile completion flow
- [ ] Guided tours per role type
- [ ] Initial preferences setup
- [ ] Welcome email based on role

### Phase 3 (TODO)
- [ ] Role upgrade (youth → creator)
- [ ] Achievement system integration
- [ ] Personalized dashboard per role
- [ ] Community recommendations

---

**Status:** 🟢 Production Ready  
**Version:** 1.1.0  
**Last Updated:** December 23, 2025  
**Endpoint:** `POST /api/auth/onboarding`

🔥 **Your Journey. Your Role. Your Sovereignty.** 👑
