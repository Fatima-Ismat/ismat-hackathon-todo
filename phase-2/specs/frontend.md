# Phase 2 Frontend Specification

## Design Inspiration

**Reference Application:** https://todo-pro-taupe.vercel.app

### Key Design Elements to Emulate
- ✨ Clean, modern UI with excellent visual hierarchy
- 🎨 Dark/light theme toggle with smooth transitions
- 📊 Visual progress indicators and statistics
- 📱 Fully responsive, mobile-first design
- 🎯 Intuitive task management interface
- 🎪 Subtle animations and micro-interactions

---

## Technology Stack

### Core Framework
- **Next.js 16.1+** with App Router
- **TypeScript** for type safety
- **React 19.2+** with Server Components where applicable

### Styling & UI
- **Tailwind CSS 4** for utility-first styling
- **lucide-react** for consistent iconography
- **clsx + tailwind-merge** for conditional classes
- **CSS variables** for theme system

### State & Data
- **React Hooks** (useState, useEffect, useContext)
- **axios** for API requests
- **date-fns** for date formatting

### Authentication
- **Better Auth** for authentication flows
- JWT token management (localStorage)
- Protected routes and auth guards

---

## Hackathon Requirements

### 5 Basic Features (REQUIRED)

| Feature | Endpoint | Component | Status |
|---------|----------|-----------|--------|
| 1. **Add Task** | `POST /api/tasks` | TaskForm | ✅ Implemented |
| 2. **Delete Task** | `DELETE /api/tasks/{id}` | TaskItem | ✅ Implemented |
| 3. **Update Task** | `PUT /api/tasks/{id}` | TaskEditModal | 🔄 To Enhance |
| 4. **View Tasks** | `GET /api/tasks` | TaskList | ✅ Implemented |
| 5. **Mark Complete** | `POST /api/tasks/{id}/complete` | TaskItem | ✅ Implemented |

### REST API Integration
- Base URL: `http://localhost:8000`
- Authentication: JWT Bearer tokens
- Error handling with user feedback
- Loading states for all async operations

---

## Bonus Features (+Points)

### Intermediate Features
- [x] **Theme Toggle** - Dark/light mode with persistence
- [x] **Task Categories/Tags** - Visual organization
- [ ] **Progress Tracking** - Visual progress bars and statistics
- [ ] **Mobile-First Design** - Fully responsive layouts
- [ ] **Search & Filter** - Find tasks quickly
- [ ] **Keyboard Shortcuts** - Power user features

### Advanced Features (Phase 3 Prep)
- [ ] **Real-time Updates** - WebSocket integration
- [ ] **Offline Support** - Service worker + IndexedDB
- [ ] **AI Chatbot Widget** - MCP integration placeholder
- [ ] **Drag & Drop** - Reorder tasks
- [ ] **Task Templates** - Quick task creation

---

## UI/UX Goals

### 1. Clean Interface
- **Whitespace**: Generous spacing, uncluttered layout
- **Typography**: Clear hierarchy with Geist Sans font
- **Colors**: Subtle, professional color palette
- **Consistency**: Uniform spacing, sizing, and patterns

### 2. User-Friendly
- **Intuitive Actions**: Clear CTAs and action buttons
- **Feedback**: Loading states, success/error messages
- **Accessibility**: ARIA labels, keyboard navigation
- **Help Text**: Tooltips and placeholder guidance

### 3. Visual Appeal
- **Modern Design**: Rounded corners, shadows, gradients
- **Animations**: Smooth transitions (200-300ms)
- **Icons**: Lucide icons for consistency
- **Empty States**: Engaging illustrations for no data

### 4. Functionality
- **Performance**: Fast load times, optimized rendering
- **Reliability**: Error boundaries, fallback UIs
- **Validation**: Client-side form validation
- **Responsiveness**: Works on all screen sizes

### 5. Extensibility
- **Component Library**: Reusable, composable components
- **Theme System**: CSS variables for easy theming
- **API Layer**: Abstracted API calls for easy modification
- **MCP Ready**: Placeholder for Phase 3 AI chatbot

---

## Component Architecture

### Layout Components

#### 1. RootLayout (`app/layout.tsx`)
```typescript
- Metadata configuration
- Font loading (Geist Sans, Geist Mono)
- Theme provider wrapper
- Global styles injection
```

#### 2. Header (`components/Header.tsx`)
```typescript
Props: { user?: User }
Features:
  - App branding and logo
  - Navigation links
  - User profile dropdown
  - Theme toggle button
  - Logout functionality
  - Notification badge
```

#### 3. Sidebar (`components/Sidebar.tsx`) [BONUS]
```typescript
Props: { activeFilter?: string }
Features:
  - Task filters (All, Active, Completed)
  - Task categories/tags
  - Statistics summary
  - Quick actions
  - Collapsible on mobile
```

#### 4. Footer (`components/Footer.tsx`) [OPTIONAL]
```typescript
Features:
  - Copyright info
  - Links to docs
  - Version info
  - Phase indicator
```

### Task Components

#### 5. TaskList (`components/TaskList.tsx`)
```typescript
Props: {
  tasks: Task[]
  onTaskUpdated: () => void
  loading?: boolean
  emptyMessage?: string
}

Features:
  - Grid/List view toggle
  - Empty state with illustration
  - Loading skeleton
  - Task grouping (by status/priority)
  - Smooth animations

Displays:
  - TaskItem for each task
  - Filters and sorting options
  - Pagination (if needed)
```

#### 6. TaskItem (`components/TaskItem.tsx`)
```typescript
Props: {
  task: Task
  onComplete: (id: number) => void
  onDelete: (id: number) => void
  onEdit: (task: Task) => void
}

Features:
  - Checkbox for completion
  - Task title and description
  - Priority badge
  - Due date indicator
  - Tags/categories
  - Action buttons (edit, delete)
  - Hover effects
  - Strike-through for completed

Variants:
  - Compact view
  - Detailed view
  - Card view
```

#### 7. TaskForm (`components/TaskForm.tsx`)
```typescript
Props: {
  onTaskCreated: () => void
  initialData?: Task
  mode?: 'create' | 'edit'
}

Fields:
  - title: string (required)
  - description: string (optional)
  - priority: 'low' | 'medium' | 'high' | 'urgent'
  - due_date: Date (optional)
  - tags: string[] (optional)

Features:
  - Form validation
  - Error messages
  - Loading state
  - Submit button
  - Cancel button (edit mode)
  - Auto-focus on title
```

#### 8. TaskEditModal (`components/TaskEditModal.tsx`)
```typescript
Props: {
  task: Task
  isOpen: boolean
  onClose: () => void
  onSave: (task: Task) => void
}

Features:
  - Modal overlay with backdrop
  - Close on ESC key
  - Close on outside click
  - TaskForm embedded
  - Smooth open/close animation
```

### Utility Components

#### 9. NotificationBadge (`components/NotificationBadge.tsx`)
```typescript
Props: { count?: number }
Features:
  - Bell icon with badge
  - Unread count display
  - Click to open notifications
  - Auto-refresh every 30s
  - Animated updates
```

#### 10. ThemeToggle (`components/ThemeToggle.tsx`)
```typescript
Features:
  - Sun/Moon icon toggle
  - Smooth transition
  - Persist preference to localStorage
  - System preference detection
  - Accessible button
```

#### 11. ProgressBar (`components/ProgressBar.tsx`) [BONUS]
```typescript
Props: {
  completed: number
  total: number
  showPercentage?: boolean
}

Features:
  - Animated progress bar
  - Color gradients (green for high %)
  - Percentage text
  - Responsive width
```

#### 12. StatCard (`components/StatCard.tsx`) [BONUS]
```typescript
Props: {
  label: string
  value: number
  icon: ReactNode
  trend?: 'up' | 'down' | 'neutral'
}

Features:
  - Icon display
  - Large value text
  - Label subtitle
  - Optional trend indicator
  - Hover effect
```

#### 13. EmptyState (`components/EmptyState.tsx`)
```typescript
Props: {
  title: string
  description: string
  icon: ReactNode
  action?: { label: string, onClick: () => void }
}

Features:
  - Large icon
  - Title and description
  - Optional CTA button
  - Centered layout
```

#### 14. LoadingSkeleton (`components/LoadingSkeleton.tsx`)
```typescript
Props: {
  count?: number
  variant?: 'task' | 'card' | 'list'
}

Features:
  - Shimmer animation
  - Multiple variants
  - Configurable count
  - Responsive sizing
```

### Authentication Components

#### 15. LoginForm (`components/auth/LoginForm.tsx`)
```typescript
Fields:
  - email: string (required, validated)
  - password: string (required, min 8 chars)

Features:
  - Form validation
  - Error display
  - Loading state
  - Remember me checkbox
  - Link to register
  - Password visibility toggle
```

#### 16. RegisterForm (`components/auth/RegisterForm.tsx`)
```typescript
Fields:
  - email: string (required, validated)
  - username: string (required, min 3 chars)
  - password: string (required, min 8 chars)
  - confirmPassword: string (must match)

Features:
  - Form validation
  - Error display
  - Loading state
  - Link to login
  - Password strength indicator
```

#### 17. AuthGuard (`components/auth/AuthGuard.tsx`)
```typescript
Props: { children: ReactNode }

Features:
  - Check authentication status
  - Redirect to /login if not authenticated
  - Loading state while checking
  - Persist redirect URL
```

---

## Page Structure

### 1. Home Page (`app/page.tsx`)
```typescript
Path: /
Access: Public (redirects to /login if not authenticated)

Layout:
  <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
    <Header />
    <main className="max-w-7xl mx-auto py-6 px-4">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <TaskList />
        </div>
        <div className="lg:col-span-1">
          <TaskForm />
          <ProgressBar /> {/* BONUS */}
        </div>
      </div>
    </main>
  </div>

Features:
  - Task creation form (right sidebar)
  - Task list (main content area)
  - Quick stats at top
  - Filters and search
```

### 2. Login Page (`app/login/page.tsx`)
```typescript
Path: /login
Access: Public only

Layout:
  <div className="min-h-screen flex items-center justify-center bg-gray-50">
    <div className="max-w-md w-full">
      <LoginForm />
    </div>
  </div>

Features:
  - Centered login form
  - Link to register
  - Forgot password link
  - Social login options (future)
```

### 3. Register Page (`app/register/page.tsx`)
```typescript
Path: /register
Access: Public only

Layout:
  <div className="min-h-screen flex items-center justify-center bg-gray-50">
    <div className="max-w-md w-full">
      <RegisterForm />
    </div>
  </div>

Features:
  - Centered register form
  - Link to login
  - Terms acceptance checkbox
```

### 4. Notifications Page (`app/notifications/page.tsx`) [BONUS]
```typescript
Path: /notifications
Access: Protected

Layout:
  <div className="min-h-screen">
    <Header />
    <main className="max-w-3xl mx-auto py-6 px-4">
      <h1>Notifications</h1>
      <NotificationList />
    </main>
  </div>

Features:
  - List all notifications
  - Mark as read
  - Delete notifications
  - Filter by type
```

---

## API Integration Layer

### API Client (`lib/api.ts`)

```typescript
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance with defaults
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired, try to refresh
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const { data } = await axios.post(`${API_BASE_URL}/api/auth/refresh`, {
            refresh_token: refreshToken,
          });
          localStorage.setItem('access_token', data.access_token);
          // Retry original request
          error.config.headers.Authorization = `Bearer ${data.access_token}`;
          return axios.request(error.config);
        } catch {
          // Refresh failed, logout
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);
```

### API Methods (`lib/api/tasks.ts`)

```typescript
import { apiClient } from '../api';

export interface Task {
  id: number;
  title: string;
  description: string;
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  due_date: string | null;
  tags: string[];
  created_at: string;
  updated_at: string;
  completed_at: string | null;
}

export interface CreateTaskData {
  title: string;
  description?: string;
  priority?: string;
  due_date?: string;
  tags?: string[];
}

export const taskAPI = {
  // GET /api/tasks
  getTasks: (filters?: { status?: string; priority?: string }) =>
    apiClient.get<Task[]>('/api/tasks', { params: filters }),

  // GET /api/tasks/:id
  getTask: (id: number) =>
    apiClient.get<Task>(`/api/tasks/${id}`),

  // POST /api/tasks
  createTask: (data: CreateTaskData) =>
    apiClient.post<Task>('/api/tasks', data),

  // PUT /api/tasks/:id
  updateTask: (id: number, data: Partial<CreateTaskData>) =>
    apiClient.put<Task>(`/api/tasks/${id}`, data),

  // POST /api/tasks/:id/complete
  completeTask: (id: number) =>
    apiClient.post<Task>(`/api/tasks/${id}/complete`),

  // DELETE /api/tasks/:id
  deleteTask: (id: number) =>
    apiClient.delete(`/api/tasks/${id}`),
};
```

### API Methods (`lib/api/auth.ts`)

```typescript
import { apiClient } from '../api';

export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export const authAPI = {
  // POST /api/auth/login
  login: (data: LoginData) =>
    apiClient.post<AuthResponse>('/api/auth/login', data),

  // POST /api/auth/register
  register: (data: RegisterData) =>
    apiClient.post('/api/auth/register', data),

  // POST /api/auth/refresh
  refresh: (refreshToken: string) =>
    apiClient.post<AuthResponse>('/api/auth/refresh', { refresh_token: refreshToken }),

  // GET /api/auth/me
  getCurrentUser: () =>
    apiClient.get('/api/auth/me'),
};
```

---

## Theme System

### Theme Configuration (`app/globals.css`)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    /* Light theme */
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
    --radius: 0.5rem;
  }

  .dark {
    /* Dark theme */
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 224.3 76.3% 48%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

### Theme Provider (`components/ThemeProvider.tsx`)

```typescript
'use client';

import { createContext, useContext, useEffect, useState } from 'react';

type Theme = 'light' | 'dark' | 'system';

interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>('system');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const stored = localStorage.getItem('theme') as Theme;
    if (stored) {
      setTheme(stored);
    }
  }, []);

  useEffect(() => {
    if (!mounted) return;

    const root = document.documentElement;
    root.classList.remove('light', 'dark');

    if (theme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light';
      root.classList.add(systemTheme);
    } else {
      root.classList.add(theme);
    }

    localStorage.setItem('theme', theme);
  }, [theme, mounted]);

  if (!mounted) return null;

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be used within ThemeProvider');
  return context;
};
```

---

## Styling Guidelines

### Color Palette

**Primary Colors:**
- Blue 600: `#2563eb` - Primary actions, links
- Blue 700: `#1d4ed8` - Hover states
- Blue 50: `#eff6ff` - Light backgrounds

**Status Colors:**
- Green: `#10b981` - Success, completed tasks
- Yellow: `#f59e0b` - Medium priority, warnings
- Orange: `#f97316` - High priority
- Red: `#ef4444` - Urgent priority, errors

**Neutral Colors:**
- Gray 50-900: Full spectrum for backgrounds and text
- Use `gray-50` for light mode backgrounds
- Use `gray-900` for dark mode backgrounds

### Typography

**Font Stack:**
```typescript
- Primary: Geist Sans (--font-geist-sans)
- Monospace: Geist Mono (--font-geist-mono)
```

**Text Sizes:**
- `text-xs`: 0.75rem (12px) - Captions, badges
- `text-sm`: 0.875rem (14px) - Body text small
- `text-base`: 1rem (16px) - Body text
- `text-lg`: 1.125rem (18px) - Subheadings
- `text-xl`: 1.25rem (20px) - Headings
- `text-2xl`: 1.5rem (24px) - Large headings
- `text-3xl`: 1.875rem (30px) - Page titles

**Font Weights:**
- `font-normal`: 400 - Body text
- `font-medium`: 500 - Emphasis
- `font-semibold`: 600 - Headings
- `font-bold`: 700 - Strong emphasis

### Spacing

**Scale:** 0.25rem (4px) increments
- `space-1`: 0.25rem (4px)
- `space-2`: 0.5rem (8px)
- `space-3`: 0.75rem (12px)
- `space-4`: 1rem (16px)
- `space-6`: 1.5rem (24px)
- `space-8`: 2rem (32px)

**Common Patterns:**
- Buttons: `px-4 py-2` (16px x 8px)
- Cards: `p-6` (24px all sides)
- Page margins: `px-4 sm:px-6 lg:px-8`

### Border Radius

- `rounded-sm`: 0.125rem (2px) - Badges
- `rounded`: 0.25rem (4px) - Buttons
- `rounded-md`: 0.375rem (6px) - Inputs
- `rounded-lg`: 0.5rem (8px) - Cards
- `rounded-xl`: 0.75rem (12px) - Modals
- `rounded-full`: 9999px - Avatars, pills

### Shadows

- `shadow-sm`: Subtle elevation
- `shadow`: Default card shadow
- `shadow-md`: Hover states
- `shadow-lg`: Modals, dropdowns
- `shadow-xl`: Popovers

---

## Responsive Design

### Breakpoints

```typescript
- sm: 640px   - Small tablets
- md: 768px   - Tablets
- lg: 1024px  - Laptops
- xl: 1280px  - Desktops
- 2xl: 1536px - Large screens
```

### Mobile-First Approach

```typescript
// Start with mobile styles, then add breakpoints
<div className="
  w-full           {/* Mobile: full width */}
  sm:w-1/2         {/* Tablet: half width */}
  lg:w-1/3         {/* Desktop: third width */}
">
```

### Layout Patterns

**Mobile (< 768px):**
- Single column layout
- Collapsible sidebar (hamburger menu)
- Full-width forms
- Stacked cards

**Tablet (768px - 1024px):**
- Two column layout for main content
- Sidebar as drawer/overlay
- Grid for task list (2 columns)

**Desktop (> 1024px):**
- Three column layout (sidebar, main, details)
- Permanent sidebar
- Grid for task list (3+ columns)
- Hover states enabled

---

## Accessibility (a11y)

### ARIA Labels

```typescript
// Example: Task checkbox
<button
  aria-label={`Mark task "${task.title}" as complete`}
  aria-pressed={task.status === 'completed'}
>
  <CheckCircle />
</button>
```

### Keyboard Navigation

- **Tab**: Navigate between interactive elements
- **Enter**: Activate buttons, submit forms
- **Escape**: Close modals, cancel actions
- **Arrow keys**: Navigate lists (bonus)

### Focus Management

```typescript
// Visible focus rings
className="focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
```

### Color Contrast

- Text: Minimum 4.5:1 contrast ratio
- Large text: Minimum 3:1 contrast ratio
- Use tools like WebAIM Contrast Checker

---

## Performance Optimization

### Code Splitting

```typescript
// Lazy load heavy components
const TaskEditModal = dynamic(() => import('@/components/TaskEditModal'), {
  loading: () => <LoadingSkeleton />,
});
```

### Image Optimization

```typescript
// Use Next.js Image component
import Image from 'next/image';

<Image
  src="/logo.png"
  alt="Logo"
  width={40}
  height={40}
  priority
/>
```

### API Caching

```typescript
// Use SWR or React Query for data fetching
import useSWR from 'swr';

const { data, error, mutate } = useSWR('/api/tasks', fetcher);
```

### Bundle Size

- Analyze bundle: `npm run build -- --analyze`
- Tree shaking: Import only what you need
- Remove unused dependencies

---

## Testing Strategy

### Unit Tests (Jest + React Testing Library)

```typescript
// Example: TaskItem component test
describe('TaskItem', () => {
  it('renders task title', () => {
    render(<TaskItem task={mockTask} />);
    expect(screen.getByText(mockTask.title)).toBeInTheDocument();
  });

  it('calls onComplete when checkbox clicked', () => {
    const onComplete = jest.fn();
    render(<TaskItem task={mockTask} onComplete={onComplete} />);
    fireEvent.click(screen.getByRole('checkbox'));
    expect(onComplete).toHaveBeenCalledWith(mockTask.id);
  });
});
```

### E2E Tests (Playwright)

```typescript
// Example: Task creation flow
test('creates new task', async ({ page }) => {
  await page.goto('/');
  await page.fill('[name="title"]', 'New task');
  await page.click('button[type="submit"]');
  await expect(page.locator('text=New task')).toBeVisible();
});
```

---

## Phase 3 Preparation

### AI Chatbot Integration Points

1. **Chat Widget Component** (placeholder)
   - Floating action button (bottom-right)
   - Expandable chat interface
   - MCP tool execution display

2. **MCP API Integration** (stub)
   - `lib/api/mcp.ts` for MCP tool calls
   - Chat message handling
   - Task creation from natural language

3. **Real-time Updates**
   - WebSocket connection setup
   - Task update notifications
   - Collaborative features (future)

4. **Voice Input** (future)
   - Speech-to-text for task creation
   - Voice commands for task management

---

## Deployment Checklist

### Pre-Deployment

- [ ] Build succeeds without errors (`npm run build`)
- [ ] All TypeScript errors resolved
- [ ] Environment variables configured
- [ ] API endpoints tested
- [ ] Authentication flow verified
- [ ] Responsive design tested
- [ ] Accessibility audit passed
- [ ] Performance audit (Lighthouse > 90)

### Production Configuration

```typescript
// .env.production
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_ENV=production
```

### Vercel Deployment

1. Connect GitHub repository
2. Set environment variables
3. Configure build settings:
   - Framework: Next.js
   - Build command: `npm run build`
   - Output directory: `.next`
4. Deploy!

---

## File Structure Summary

```
phase-2/frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx              # Root layout
│   │   ├── page.tsx                # Home page
│   │   ├── login/page.tsx          # Login page
│   │   ├── register/page.tsx       # Register page
│   │   ├── notifications/page.tsx  # Notifications page
│   │   └── globals.css             # Global styles + theme
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   ├── TaskList.tsx
│   │   ├── TaskItem.tsx
│   │   ├── TaskForm.tsx
│   │   ├── TaskEditModal.tsx
│   │   ├── NotificationBadge.tsx
│   │   ├── ThemeToggle.tsx
│   │   ├── ProgressBar.tsx
│   │   ├── StatCard.tsx
│   │   ├── EmptyState.tsx
│   │   ├── LoadingSkeleton.tsx
│   │   ├── ThemeProvider.tsx
│   │   └── auth/
│   │       ├── LoginForm.tsx
│   │       ├── RegisterForm.tsx
│   │       └── AuthGuard.tsx
│   ├── lib/
│   │   ├── api.ts                  # Axios client
│   │   ├── utils.ts                # Utility functions
│   │   └── api/
│   │       ├── tasks.ts            # Task API methods
│   │       ├── auth.ts             # Auth API methods
│   │       └── notifications.ts    # Notification API methods
│   └── types/
│       └── index.ts                # TypeScript types
├── public/
│   ├── favicon.ico
│   ├── logo.png
│   └── illustrations/
├── .env.local
├── .env.example
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

---

## Success Metrics

### Functionality (50 points)
- [x] Add task (10 pts)
- [x] Delete task (10 pts)
- [ ] Update task (10 pts) - Needs modal
- [x] View tasks (10 pts)
- [x] Mark complete (10 pts)

### UI/UX (30 points)
- [ ] Clean interface (10 pts)
- [ ] Responsive design (10 pts)
- [ ] Theme toggle (10 pts)

### Code Quality (20 points)
- [x] TypeScript types (5 pts)
- [x] Component reusability (5 pts)
- [x] API abstraction (5 pts)
- [ ] Error handling (5 pts)

### Bonus (+50 points potential)
- [ ] Progress tracking (10 pts)
- [ ] Task categories (10 pts)
- [ ] Search/filter (10 pts)
- [ ] Keyboard shortcuts (10 pts)
- [ ] Offline support (10 pts)

**Target Score:** 100/100 base + 30+ bonus = 130+ points

---

## References

- Design: https://todo-pro-taupe.vercel.app
- Next.js Docs: https://nextjs.org/docs
- Tailwind CSS: https://tailwindcss.com/docs
- Better Auth: https://www.better-auth.com/docs
- Lucide Icons: https://lucide.dev
- date-fns: https://date-fns.org

---

**Last Updated:** 2025-12-31
**Phase:** 2 (Web Application)
**Status:** Ready for Implementation
**Next Phase:** Phase 3 (AI Chatbot with MCP)
