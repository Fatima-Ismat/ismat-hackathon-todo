# Phase 2 Backend - Hackathon Todo API

FastAPI backend with reusable intelligence, MCP integration, and JWT authentication.

## Features

- **Reusable Agents**: Task manager skill, auth subagent, notification subagent
- **MCP Server**: Model Context Protocol integration for AI chatbot (Phase 3)
- **JWT Authentication**: Secure token-based authentication
- **PostgreSQL Database**: SQLModel ORM with async support
- **API Documentation**: Auto-generated OpenAPI docs at `/docs`
- **CORS Enabled**: Cross-origin support for frontend integration

## Prerequisites

- Python 3.13+
- PostgreSQL 14+
- uv (Python package manager)

## Quick Start

### 1. Database Setup

Create PostgreSQL database:

```bash
# Using psql
createdb hackathon_todo

# Or using SQL
psql -U postgres
CREATE DATABASE hackathon_todo;
```

### 2. Environment Configuration

Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

Edit `.env`:
```env
DATABASE_URL="postgresql+asyncpg://postgres:yourpassword@localhost:5432/hackathon_todo"
JWT_SECRET="your-random-secret-key-here"
```

### 3. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### 4. Initialize Database

```bash
# Run migrations (creates tables)
python -c "from database import init_db; import asyncio; asyncio.run(init_db())"

# Or start the server (auto-creates tables)
uv run python main.py
```

### 5. Run Server

```bash
# Development mode with hot reload
uv run python main.py

# Or using uvicorn directly
uvicorn main:app --reload --port 8000
```

Server will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- MCP Tools: http://localhost:8000/api/mcp/tools

## Project Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── models.py               # SQLModel database models
├── database.py             # Database connection & adapter
├── config.py               # Configuration management
├── routes/                 # API route handlers
│   ├── auth.py            # Authentication endpoints
│   ├── tasks.py           # Task CRUD endpoints
│   └── notifications.py   # Notification endpoints
├── .env                   # Environment variables (create from .env.example)
└── pyproject.toml         # Python dependencies
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT tokens
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user info

### Tasks
- `POST /api/tasks` - Create task
- `GET /api/tasks` - List tasks (with filters)
- `GET /api/tasks/{id}` - Get task by ID
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task (soft delete)
- `POST /api/tasks/{id}/complete` - Mark task complete

### Notifications
- `GET /api/notifications` - List notifications
- `GET /api/notifications/unread-count` - Get unread count
- `PUT /api/notifications/{id}/read` - Mark as read
- `PUT /api/notifications/mark-all-read` - Mark all as read
- `DELETE /api/notifications/{id}` - Delete notification

### MCP (Model Context Protocol)
- `POST /api/mcp/call` - Execute MCP tool
- `GET /api/mcp/tools` - List available MCP tools

## Reusable Intelligence

### Task Manager Skill
Located in `../../agents/task-manager-skill/`

**Capabilities:**
- Create, list, update, complete, delete tasks
- Search and filter operations
- MCP tool wrappers for AI integration

**Reusability:** Designed for use in Phase 2-5 (Web, AI Chatbot, Mobile, Advanced)

### Auth Subagent
Located in `../../agents/auth-subagent/`

**Capabilities:**
- JWT token generation and validation
- Password hashing (bcrypt)
- User authentication
- Permission checking

**Reusability:** Used across all phases for secure authentication

### Notification Subagent
Located in `../../agents/notification-subagent/`

**Capabilities:**
- Multi-channel notifications (in-app, email, push)
- User preferences management
- Notification templates

**Reusability:** Extensible for Phase 3+ (AI alerts, mobile push)

## MCP Server Integration

The MCP server exposes task management tools for AI chatbot integration (Phase 3).

**Available Tools:**
1. `add_task` - Create new task
2. `list_tasks` - List tasks with filters
3. `complete_task` - Mark task complete
4. `delete_task` - Delete task
5. `update_task` - Update task properties
6. `search_tasks` - Search tasks by text

**Test MCP Tools:**

```bash
# List available tools
curl http://localhost:8000/api/mcp/tools

# Call a tool (requires JWT token)
curl -X POST http://localhost:8000/api/mcp/call \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "add_task",
    "parameters": {
      "title": "Test task from MCP",
      "priority": "high"
    }
  }'
```

## Database Schema

### Users Table
- `id` - Primary key
- `email` - Unique email
- `username` - Unique username
- `hashed_password` - Bcrypt hash
- `is_active` - Account status
- `created_at`, `updated_at` - Timestamps

### Tasks Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `title` - Task title
- `description` - Task description
- `status` - pending | in_progress | completed | cancelled
- `priority` - low | medium | high | urgent
- `due_date` - Optional due date
- `tags` - JSON array of tags
- `created_at`, `updated_at`, `completed_at` - Timestamps

### Notifications Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `message` - Notification message
- `notification_type` - Type of notification
- `read` - Read status
- `created_at`, `read_at` - Timestamps

## Authentication Flow

1. **Register**: `POST /api/auth/register`
   - Hash password with bcrypt
   - Store user in database
   - Return user info

2. **Login**: `POST /api/auth/login`
   - Verify email and password
   - Generate JWT access token (60 min)
   - Generate JWT refresh token (30 days)
   - Return both tokens

3. **Authenticated Requests**:
   - Include header: `Authorization: Bearer <access_token>`
   - Server validates JWT and extracts user_id
   - Request proceeds with authenticated user context

4. **Token Refresh**: `POST /api/auth/refresh`
   - Send refresh token
   - Receive new access token
   - Refresh token remains valid

## Development

### Run Tests

```bash
# Install test dependencies
uv add --dev pytest pytest-asyncio httpx

# Run tests
pytest
```

### Database Migrations (Alembic)

```bash
# Initialize alembic (if not done)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "migration message"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Code Quality

```bash
# Format code
black .

# Lint
ruff check .

# Type checking
mypy .
```

## Deployment

### Docker (Production)

```bash
# Build image
docker build -t hackathon-todo-backend .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql+asyncpg://..." \
  -e JWT_SECRET="..." \
  hackathon-todo-backend
```

### Environment Variables (Production)

**Required:**
- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET` - Strong random secret key

**Optional:**
- `SMTP_*` - Email notification configuration
- `PUSH_*` - Push notification configuration
- `CORS_ORIGINS` - Allowed frontend origins

## Troubleshooting

### Database Connection Error
```
Check DATABASE_URL format: postgresql+asyncpg://user:pass@host:port/dbname
Verify PostgreSQL is running: pg_isready
Check credentials and database exists
```

### JWT Token Invalid
```
Verify JWT_SECRET matches between restarts
Check token expiry time
Ensure Authorization header format: "Bearer <token>"
```

### MCP Tools Not Working
```
Verify MCP_ENABLED=true in .env
Check backend server is running
Test /api/mcp/tools endpoint
Ensure JWT token is valid
```

## Phase 3 Preparation

This backend is ready for Phase 3 AI chatbot integration:

1. **MCP Server**: Already exposed at `/api/mcp/call`
2. **Reusable Agents**: Task operations ready for AI consumption
3. **Authentication**: JWT tokens work for both web and AI clients
4. **Extensibility**: Add new MCP tools by extending MCPTaskTools class

## License

MIT - Reusable across all project phases
