# AUTHENTICATION API DOCUMENTATION
**CodexDominion Design System**  
**Version 1.0.0** | December 23, 2025

---

## 🔐 OVERVIEW

Complete authentication system for CodexDominion platform with user registration, login, JWT token authentication, and role-based access control.

**Base URL:** `http://localhost:5000/api/auth`  
**Production URL:** `https://codexdominion.app/api/auth`

---

## 🚀 API ENDPOINTS

### 1. Register New User

**Endpoint:** `POST /api/auth/register`

**Request Body:**
```json
{
  "name": "Marcus Thompson",
  "email": "marcus@example.com",
  "password": "SecurePass123",
  "country": "Jamaica"
}
```

**Field Requirements:**
- `name`: Required, 2-100 characters
- `email`: Required, valid email format
- `password`: Required, minimum 8 characters, must contain letters and numbers
- `country`: Optional, user's country

**Success Response (201):**
```json
{
  "success": true,
  "message": "Account created successfully! 🎉",
  "user": {
    "id": "user_abc123",
    "name": "Marcus Thompson",
    "email": "marcus@example.com",
    "role": "viewer",
    "created_at": "2025-12-23T10:30:00.000000Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses:**

**400 - Validation Error:**
```json
{
  "success": false,
  "error": "Password must be at least 8 characters",
  "field": "password"
}
```

**409 - Email Already Exists:**
```json
{
  "success": false,
  "error": "This email is already in use. Try signing in?",
  "field": "email"
}
```

---

### 2. Login User

**Endpoint:** `POST /api/auth/login`

**Request Body:**
```json
{
  "email": "marcus@example.com",
  "password": "SecurePass123"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Welcome back! 👑",
  "user": {
    "id": "user_abc123",
    "name": "Marcus Thompson",
    "email": "marcus@example.com",
    "role": "viewer",
    "last_login": "2025-12-23T10:45:00.000000Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses:**

**401 - Invalid Credentials:**
```json
{
  "success": false,
  "error": "Invalid email or password"
}
```

**403 - Inactive Account:**
```json
{
  "success": false,
  "error": "Account is inactive. Contact support."
}
```

---

### 3. Verify Token

**Endpoint:** `GET /api/auth/verify`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Success Response (200):**
```json
{
  "success": true,
  "user": {
    "id": "user_abc123",
    "email": "marcus@example.com",
    "role": "viewer"
  }
}
```

**Error Response (401):**
```json
{
  "success": false,
  "error": "Invalid or expired token"
}
```

---

### 4. Get User Profile

**Endpoint:** `GET /api/auth/profile`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Success Response (200):**
```json
{
  "success": true,
  "user": {
    "id": "user_abc123",
    "name": "Marcus Thompson",
    "email": "marcus@example.com",
    "role": "viewer",
    "created_at": "2025-12-23T10:30:00.000000Z",
    "last_login": "2025-12-23T10:45:00.000000Z"
  }
}
```

**Error Response (401):**
```json
{
  "success": false,
  "error": "No token provided"
}
```

---

### 5. Logout User

**Endpoint:** `POST /api/auth/logout`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

**Note:** Since we use JWT tokens (stateless), logout is handled client-side by discarding the token. This endpoint exists for consistency and future server-side logout logic.

---

### 6. Request Password Reset

**Endpoint:** `POST /api/auth/reset-password-request`

**Request Body:**
```json
{
  "email": "marcus@example.com"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "If that email exists, we've sent reset instructions."
}
```

**Note:** Always returns success to prevent email enumeration attacks.

---

## 🔑 JWT TOKEN

### Token Structure

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.payload.signature
```

### Token Payload

```json
{
  "user_id": "user_abc123",
  "email": "marcus@example.com",
  "role": "viewer",
  "exp": 1703510400,
  "iat": 1703424000
}
```

### Token Expiration

- **Default:** 24 hours
- **Refresh:** Client should handle token refresh or re-login

### Using Token in Requests

**Header Format:**
```
Authorization: Bearer <your-token-here>
```

**Example:**
```bash
curl -H "Authorization: Bearer eyJhbGc..." http://localhost:5000/api/auth/profile
```

---

## 👥 USER ROLES

| Role | Permissions | Description |
|------|-------------|-------------|
| **viewer** | Read-only access | Default role for new users |
| **council_operator** | Vote on workflows | Council members with voting rights |
| **admin** | Full system access | System administrators |
| **owner** | Tenant owner | Tenant owner with full tenant access |
| **collaborator** | Tenant collaborator | Collaborator with limited tenant access |
| **tenant_viewer** | Tenant read-only | Read-only access to tenant data |

---

## 🔒 SECURITY FEATURES

### Password Requirements

- Minimum 8 characters
- Must contain letters AND numbers
- Stored as bcrypt hash (never plain text)

### JWT Security

- **Algorithm:** HS256 (HMAC SHA-256)
- **Secret Key:** Configurable via `JWT_SECRET` environment variable
- **Expiration:** 24 hours (configurable)
- **Claims:** user_id, email, role, exp, iat

### Rate Limiting

**Recommended (not yet implemented):**
- Login: 5 attempts per 15 minutes per IP
- Registration: 3 attempts per hour per IP
- Password Reset: 3 attempts per hour per email

---

## 📊 ERROR CODES

| Code | Meaning | Common Causes |
|------|---------|---------------|
| 400 | Bad Request | Missing/invalid fields, validation errors |
| 401 | Unauthorized | Invalid credentials, expired token |
| 403 | Forbidden | Inactive account, insufficient permissions |
| 409 | Conflict | Email already exists |
| 500 | Server Error | Database error, unexpected exception |

---

## 🧪 TESTING

### Test Registration

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "TestPass123"
  }'
```

### Test Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123"
  }'
```

### Test Verify Token

```bash
curl -X GET http://localhost:5000/api/auth/verify \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Test Get Profile

```bash
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 🎨 FRONTEND INTEGRATION

### React/Next.js Example

```typescript
// Register new user
const register = async (name: string, email: string, password: string) => {
  const response = await fetch('http://localhost:5000/api/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, password })
  });
  
  const data = await response.json();
  
  if (data.success) {
    // Store token
    localStorage.setItem('token', data.token);
    // Redirect to dashboard
    window.location.href = '/dashboard';
  } else {
    // Show error
    alert(data.error);
  }
};

// Login user
const login = async (email: string, password: string) => {
  const response = await fetch('http://localhost:5000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  
  const data = await response.json();
  
  if (data.success) {
    localStorage.setItem('token', data.token);
    window.location.href = '/dashboard';
  } else {
    alert(data.error);
  }
};

// Get user profile
const getProfile = async () => {
  const token = localStorage.getItem('token');
  
  const response = await fetch('http://localhost:5000/api/auth/profile', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  const data = await response.json();
  
  if (data.success) {
    return data.user;
  } else {
    // Token expired, redirect to login
    window.location.href = '/login';
  }
};

// Logout
const logout = () => {
  localStorage.removeItem('token');
  window.location.href = '/';
};
```

---

## 🔐 ENVIRONMENT VARIABLES

**Required:**

```env
# JWT Secret Key (change in production!)
JWT_SECRET=your-super-secret-key-here-2025

# Database URL
DATABASE_URL=postgresql://user:password@localhost:5432/codex

# Flask Secret Key
SECRET_KEY=your-flask-secret-key-here
```

**Optional:**

```env
# JWT Expiration (hours)
JWT_EXPIRATION_HOURS=24

# Enable debug mode
FLASK_DEBUG=True
```

---

## ✅ IMPLEMENTATION CHECKLIST

- [x] User registration endpoint
- [x] Login endpoint
- [x] Token verification endpoint
- [x] Get profile endpoint
- [x] Logout endpoint
- [x] Password reset request endpoint
- [x] Email validation
- [x] Password strength validation
- [x] JWT token generation
- [x] JWT token verification
- [x] Password hashing (bcrypt)
- [x] Role-based access control
- [ ] Rate limiting (TODO)
- [ ] Email verification (TODO)
- [ ] Password reset flow (TODO)
- [ ] Refresh token logic (TODO)

---

## 🚀 NEXT STEPS

### Phase 1 (Complete)
✅ Basic registration and login  
✅ JWT token authentication  
✅ User profile endpoint  

### Phase 2 (TODO)
- [ ] Email verification workflow
- [ ] Complete password reset flow
- [ ] Refresh token logic
- [ ] Rate limiting middleware

### Phase 3 (TODO)
- [ ] OAuth integration (Google, Facebook)
- [ ] Two-factor authentication (2FA)
- [ ] Session management
- [ ] User management dashboard

---

**Status:** 🟢 Production Ready (Phase 1)  
**Version:** 1.0.0  
**Last Updated:** December 23, 2025  
**API File:** `auth_api.py`

🔥 **Secure. Scalable. Sovereign.** 👑
