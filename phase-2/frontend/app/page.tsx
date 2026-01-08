"use client"

import { Button } from "@/components/ui/button"
import { StatsCard } from "@/components/stats-card"
import { ThemeToggle } from "@/components/theme-toggle"
import { CheckCircle2, Circle, ListTodo, TrendingUp, LogOut } from "lucide-react"
import Link from "next/link"
import { ShaderGradient } from "@/components/ui/shader-gradient"
import { ProtectedRoute } from "@/components/protected-route"
import { useAuth } from "@/lib/hooks/use-auth"
import { useTasksAPI } from "@/lib/hooks/use-tasks-api"

function DashboardContent() {
  const { user, logout } = useAuth()
  const { tasks } = useTasksAPI()

  // DEBUG: Log authentication state
  console.log('[Dashboard] Render - user:', user)
  console.log('[Dashboard] Render - logout function exists:', typeof logout === 'function')

  const totalTasks = tasks.length
  const completedTasks = tasks.filter((t) => t.status === "completed").length
  const pendingTasks = totalTasks - completedTasks
  const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0

  return (
    <div className="min-h-screen bg-background transition-colors duration-300 relative">
      <ShaderGradient animate intensity="medium" />

      <div className="absolute top-4 right-4 z-50 flex items-center gap-2 sm:top-6 sm:right-6 md:top-8 md:right-8">
        {user && (
          <div className="hidden sm:flex items-center gap-2 bg-card/80 backdrop-blur-sm border border-border rounded-lg px-3 py-1.5">
            <span className="text-sm text-muted-foreground">Welcome,</span>
            <span className="text-sm font-medium">{user.name}</span>
          </div>
        )}
        <Button
          variant="outline"
          size="icon"
          onClick={() => {
            console.log('[Dashboard] Logout button clicked!')
            logout()
          }}
          className="size-10 bg-transparent"
          data-testid="logout-button"
        >
          <LogOut className="size-4" />
          <span className="sr-only">Sign Out</span>
        </Button>
        <ThemeToggle />
      </div>

      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 lg:py-16 relative z-10">
        <div className="max-w-4xl mx-auto">
          {/* Welcome Header */}
          <div className="text-center mb-8 sm:mb-12 animate-in">
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-foreground mb-3 sm:mb-4">
              Welcome to <span className="text-primary">TaskFlow Pro</span>
            </h1>
            <p className="text-base sm:text-lg text-muted-foreground">Your professional task management dashboard</p>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 mb-8 sm:mb-12">
            <StatsCard
              title="Total Tasks"
              value={totalTasks}
              icon={<ListTodo className="size-5 sm:size-6" />}
              color="indigo"
              delay={0}
            />
            <StatsCard
              title="Completed"
              value={completedTasks}
              icon={<CheckCircle2 className="size-5 sm:size-6" />}
              color="emerald"
              delay={100}
            />
            <StatsCard
              title="Pending"
              value={pendingTasks}
              icon={<Circle className="size-5 sm:size-6" />}
              color="amber"
              delay={200}
            />
            <StatsCard
              title="Completion Rate"
              value={`${completionRate}%`}
              icon={<TrendingUp className="size-5 sm:size-6" />}
              color="rose"
              delay={300}
            />
          </div>

          <div className="text-center">
            <Button
              size="lg"
              className="bg-primary hover:bg-primary/90 text-primary-foreground px-6 sm:px-8 py-4 sm:py-6 text-base sm:text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200 w-full sm:w-auto"
              asChild
            >
              <Link href="/tasks">Go to Tasks</Link>
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <DashboardContent />
    </ProtectedRoute>
  )
}
