# Frontend-Backend Integration Guide

## Overview

This guide explains how to connect the Next.js frontend to the FastAPI backend for Phase 2.

---

## ✅ What's Already Configured

### Backend (FastAPI)
- **Running on:** http://localhost:8000
- **Database:** SQLite (`todo.db`) with auto-fallback
- **Authentication:** JWT with bcrypt hashing (fixed for direct bcrypt usage)
- **CORS:** Configured for `http://localhost:3000`

### Frontend (Next.js)
- **API Client:** Axios with JWT interceptors (`src/lib/api.ts`)
- **Auth Methods:** Login, Register, Refresh (`src/lib/api/auth.ts`)
- **Task Methods:** Full CRUD operations (`src/lib/api/tasks.ts`)
- **Components:** LoginForm, RegisterForm, TaskList, TaskForm
- **Environment:** `.env.local` with `NEXT_PUBLIC_API_URL=http://localhost:8000`

---

## 🔧 Recent Fixes Applied

### 1. Bcrypt Compatibility Issue (CRITICAL FIX)
**Problem:** Pass lib bcrypt compatibility error causing 500 errors on registration
**Solution:** Switched from passlib to direct bcrypt usage

**Files Modified:**
- `phase-2/backend/routes/auth.py` - Direct bcrypt implementation
- `phase-2/backend/routes/tasks.py` - Direct bcrypt implementation

**Changes:**
```python
# OLD (passlib - had compatibility issues)
from passlib.context import CryptContext
self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
return self.pwd_context.hash(password)

# NEW (direct bcrypt - works correctly)
import bcrypt
salt = bcrypt.gensalt(rounds=self.bcrypt_rounds)
hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
return hashed.decode('utf-8')
```

### 2. Database Auto-Fallback
- Automatically uses SQLite if PostgreSQL URL detected
- No manual environment override needed

---

## 🚀 How to Start Both Services

### Step 1: Start Backend (Terminal 1)
```bash
cd phase-2/backend

# IMPORTANT: Kill any existing backend process first!
# On Windows: taskkill /F /IM python.exe (if needed)
# On Linux/Mac: pkill -f "python main.py" (if needed)

# Start fresh server (loads fixed bcrypt code)
python main.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
Database initialized
CORS origins: ['http://localhost:3000']
JWT expiry: 60 minutes
```

### Step 2: Start Frontend (Terminal 2)
```bash
cd phase-2/frontend

# Install dependencies if needed
npm install

# Start development server
npm run dev
```

**Expected Output:**
```
  ▲ Next.js 16.1.1
  - Local:        http://localhost:3000
  - Ready in 2.5s
```

---

## 🧪 Testing the Integration

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```

**Expected:**
```json
{
  "status": "healthy",
  "phase": 2,
  "features": ["reusable-agents", "mcp-integration", "auth-jwt", "notifications"]
}
```

### Test 2: Register User (API)
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","username":"alice","password":"password123"}'
```

**Expected:**
```json
{
  "id": 1,
  "email": "alice@example.com",
  "username": "alice",
  "is_active": true,
  "created_at": "2026-01-01T..."
}
```

### Test 3: Login (API)
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"password123"}'
```

**Expected:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Test 4: Frontend Registration

1. Open http://localhost:3000/register
2. Fill in the form:
   - Email: `bob@example.com`
   - Username: `bob`
   - Password: `password123`
3. Click "Register"
4. Should redirect to login page with success message

### Test 5: Frontend Login

1. Open http://localhost:3000/login
2. Enter credentials from Test 4
3. Click "Login"
4. Should redirect to dashboard (`/`)

### Test 6: Create Task

1. After logging in, you should see the dashboard
2. In the "Create Task" form on the right:
   - Title: "Test Task"
   - Description: "This is a test"
   - Priority: Medium
3. Click "Create Task"
4. Task should appear in the list on the left

---

## 🔍 Troubleshooting

### Issue: 500 Error on Registration
**Cause:** Backend still using old passlib code (not restarted)
**Solution:**
```bash
# Kill backend process
# Windows: Ctrl+C in backend terminal
# Or: taskkill /F /IM python.exe

# Restart backend
cd phase-2/backend
python main.py
```

### Issue: CORS Error
**Symptom:** Browser console shows "CORS policy" error
**Check:**
```bash
# Verify backend CORS setting
python -c "from config import settings; print('CORS:', settings.CORS_ORIGINS)"
```

**Expected:** `['http://localhost:3000']`

**Fix if needed:** Update `phase-2/backend/.env`:
```env
CORS_ORIGINS=http://localhost:3000
```

### Issue: Connection Refused
**Symptom:** `ECONNREFUSED` error in frontend
**Check:**
1. Backend running on port 8000?
   ```bash
   curl http://localhost:8000/health
   ```
2. Frontend `.env.local` has correct URL?
   ```bash
   cat phase-2/frontend/.env.local | grep API_URL
   ```

### Issue: Tokens Not Working
**Symptom:** 401 Unauthorized on protected endpoints
**Debug:**
```bash
# Test login and capture token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"password123"}' \
  | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# Test protected endpoint
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/auth/me
```

### Issue: Database Not Found
**Symptom:** `no such table` errors
**Solution:**
```bash
cd phase-2/backend

# Delete old database
rm todo.db

# Restart server (will recreate tables)
python main.py
```

---

## 📋 API Endpoints Reference

### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Create new user | No |
| POST | `/api/auth/login` | Login and get tokens | No |
| POST | `/api/auth/refresh` | Refresh access token | No |
| GET | `/api/auth/me` | Get current user | Yes |

### Tasks
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/tasks` | Create task | Yes |
| GET | `/api/tasks` | List tasks | Yes |
| GET | `/api/tasks/{id}` | Get specific task | Yes |
| PUT | `/api/tasks/{id}` | Update task | Yes |
| DELETE | `/api/tasks/{id}` | Delete task (soft) | Yes |
| POST | `/api/tasks/{id}/complete` | Mark completed | Yes |

### Notifications
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/notifications` | List notifications | Yes |
| PUT | `/api/notifications/{id}/read` | Mark as read | Yes |

---

## 🎯 Complete User Flow Test

### End-to-End Test Script
```bash
#!/bin/bash

echo "1. Testing health..."
curl -s http://localhost:8000/health | python -m json.tool

echo "\n2. Registering user..."
curl -s -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"test","password":"password123"}' \
  | python -m json.tool

echo "\n3. Logging in..."
RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}')
TOKEN=$(echo $RESPONSE | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

echo "Token: ${TOKEN:0:50}..."

echo "\n4. Creating task..."
curl -s -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Test Task","description":"Integration test","priority":"high"}' \
  | python -m json.tool

echo "\n5. Listing tasks..."
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/tasks \
  | python -m json.tool

echo "\nTest complete!"
```

Save as `test-integration.sh` and run:
```bash
chmod +x test-integration.sh
./test-integration.sh
```

---

## 📊 Architecture Diagram

```
┌──────────────────┐         ┌──────────────────┐
│                  │         │                  │
│  Next.js         │         │  FastAPI         │
│  Frontend        │◄────────┤  Backend         │
│  :3000           │  HTTP   │  :8000           │
│                  │         │                  │
└────────┬─────────┘         └────────┬─────────┘
         │                            │
         │                            │
    ┌────▼─────┐                 ┌────▼─────┐
    │ Browser  │                 │ SQLite   │
    │ Storage  │                 │ Database │
    │ (Tokens) │                 │ todo.db  │
    └──────────┘                 └──────────┘
```

---

## ✅ Success Criteria

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Health endpoint returns `{"status":"healthy"}`
- [ ] Can register new user via API
- [ ] Can register new user via frontend
- [ ] Can login via API and receive JWT tokens
- [ ] Can login via frontend and redirect to dashboard
- [ ] Can create tasks via frontend
- [ ] Tasks persist in database
- [ ] Logout clears tokens and redirects to login

---

## 🎓 Next Steps

After successful integration:

1. ✅ Test all CRUD operations for tasks
2. ✅ Test token refresh flow
3. ✅ Test notifications (if implemented)
4. 📝 Add error handling improvements
5. 📝 Add loading states
6. 📝 Add form validation
7. 🚀 Phase 3: Add AI agent integration

---

**Last Updated:** 2026-01-01
**Phase:** 2 (Full-Stack Integration)
**Status:** Ready for Testing (Backend restart required for bcrypt fix)
