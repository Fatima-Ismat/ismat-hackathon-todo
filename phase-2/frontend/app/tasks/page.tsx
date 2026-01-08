"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { TaskList } from "@/components/task-list"
import { TaskEditor } from "@/components/task-editor"
import { CommandPalette } from "@/components/command-palette"
import { ThemeToggle } from "@/components/theme-toggle"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Calendar } from "@/components/ui/calendar"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Plus, Home, CalendarIcon, Flame, Zap, Droplet } from "lucide-react"
import { useRouter } from "next/navigation"
import { useTasksAPI } from "@/lib/hooks/use-tasks-api"
import type { Task } from "@/lib/types"
import { format } from "date-fns"
import { cn } from "@/lib/utils"
import { useToast } from "@/hooks/use-toast"
import { Badge } from "@/components/ui/badge"
import { ShaderGradient } from "@/components/ui/shader-gradient"
import { ProtectedRoute } from "@/components/protected-route"
import { useAuth } from "@/lib/hooks/use-auth"
import { LogOut } from "lucide-react"

function TasksContent() {
  const router = useRouter()
  const { user, logout } = useAuth()
  const { tasks, addTask, updateTask, deleteTask, toggleTask, isLoading } = useTasksAPI()
  const [selectedTask, setSelectedTask] = useState<Task | null>(null)

  // DEBUG: Log authentication state
  console.log('[Tasks] Render - user:', user)
  console.log('[Tasks] Render - logout function exists:', typeof logout === 'function')
  const [showNewTaskModal, setShowNewTaskModal] = useState(false)
  const [bulkActionsEnabled, setBulkActionsEnabled] = useState(false)
  const [selectedTaskIds, setSelectedTaskIds] = useState<string[]>([])
  const [showMobileEditor, setShowMobileEditor] = useState(false)
  const [newTask, setNewTask] = useState<{
    title: string
    description: string
    priority: "high" | "medium" | "low"
    dueDate: string
  }>({
    title: "",
    description: "",
    priority: "medium",
    dueDate: "",
  })
  const { toast } = useToast()

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "n" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault()
        setShowNewTaskModal(true)
      }
      if (e.key === "Delete" && selectedTaskIds.length > 0 && bulkActionsEnabled) {
        e.preventDefault()
        handleBulkDelete()
      }
    }
    document.addEventListener("keydown", handleKeyDown)
    return () => document.removeEventListener("keydown", handleKeyDown)
  }, [selectedTaskIds, bulkActionsEnabled])

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading tasks...</p>
        </div>
      </div>
    )
  }

  const handleCreateTask = () => {
    if (!newTask.title.trim()) {
      toast({
        title: "Error",
        description: "Please enter a task title",
        variant: "destructive",
      })
      return
    }

    addTask({
      ...newTask,
      status: "pending",
    })

    setNewTask({
      title: "",
      description: "",
      priority: "medium",
      dueDate: "",
    })
    setShowNewTaskModal(false)
    toast({
      title: "Success",
      description: "Task created successfully",
    })
  }

  const handleUpdateTask = (id: string, updates: Partial<Task>) => {
    updateTask(id, updates)
    if (selectedTask?.id === id) {
      setSelectedTask({ ...selectedTask, ...updates })
    }
  }

  const handleDeleteTask = (id: string) => {
    deleteTask(id)
    if (selectedTask?.id === id) {
      setSelectedTask(null)
      setShowMobileEditor(false)
    }
    toast({
      title: "Task deleted",
      description: "The task has been removed",
    })
  }

  const handleToggleTask = (id: string) => {
    const task = tasks.find((t) => t.id === id)
    if (task) {
      const newStatus = task.status === "completed" ? "pending" : "completed"
      toggleTask(id)
      if (selectedTask?.id === id) {
        setSelectedTask({ ...selectedTask, status: newStatus })
      }
    }
  }

  const handleToggleSelection = (id: string) => {
    setSelectedTaskIds((prev) => (prev.includes(id) ? prev.filter((taskId) => taskId !== id) : [...prev, id]))
  }

  const handleBulkDelete = () => {
    selectedTaskIds.forEach((id) => deleteTask(id))
    setSelectedTaskIds([])
    toast({
      title: "Tasks deleted",
      description: `${selectedTaskIds.length} task(s) removed`,
    })
  }

  const handleBulkComplete = () => {
    selectedTaskIds.forEach((id) => {
      const task = tasks.find((t) => t.id === id)
      if (task && task.status === "pending") {
        toggleTask(id)
      }
    })
    setSelectedTaskIds([])
    toast({
      title: "Tasks completed",
      description: `${selectedTaskIds.length} task(s) marked as complete`,
    })
  }

  const handleSelectAll = () => {
    if (selectedTaskIds.length === tasks.length) {
      setSelectedTaskIds([])
    } else {
      setSelectedTaskIds(tasks.map((t) => t.id))
    }
  }

  const handleSelectTaskMobile = (task: Task) => {
    setSelectedTask(task)
    setShowMobileEditor(true)
  }

  return (
    <div className="min-h-screen bg-background relative">
      <ShaderGradient animate intensity="medium" />

      <CommandPalette onNewTask={() => setShowNewTaskModal(true)} />

      {/* Header */}
      <div className="border-b border-border bg-card/50 backdrop-blur-sm relative z-10">
        <div className="container mx-auto px-3 sm:px-4 py-3 sm:py-4">
          <div className="flex flex-wrap items-center justify-between gap-2 sm:gap-4">
            <div className="flex items-center gap-2 sm:gap-4">
              <Button variant="ghost" size="icon" onClick={() => router.push("/")}>
                <Home className="size-4 sm:size-5" />
              </Button>
              <h1 className="text-xl sm:text-2xl font-bold">Tasks</h1>
              <Badge variant="secondary" className="text-xs sm:text-sm">
                {tasks.length} total
              </Badge>
            </div>
            <div className="flex items-center gap-1.5 sm:gap-2">
              {user && (
                <div className="hidden sm:flex items-center gap-2 text-xs text-muted-foreground mr-2">{user.name}</div>
              )}
              <Button
                variant={bulkActionsEnabled ? "default" : "outline"}
                size="sm"
                onClick={() => {
                  setBulkActionsEnabled(!bulkActionsEnabled)
                  setSelectedTaskIds([])
                }}
                className="text-xs sm:text-sm"
              >
                {bulkActionsEnabled ? "Done" : "Select"}
              </Button>
              <Button onClick={() => setShowNewTaskModal(true)} size="sm" className="text-xs sm:text-sm">
                <Plus className="size-3 sm:size-4 sm:mr-2" />
                <span className="hidden sm:inline">New Task</span>
              </Button>
              <Button
                variant="outline"
                size="icon"
                onClick={() => {
                  console.log('[Tasks] Logout button clicked!')
                  logout()
                }}
                className="size-9 bg-transparent"
                data-testid="logout-button"
              >
                <LogOut className="size-4" />
                <span className="sr-only">Sign Out</span>
              </Button>
              <ThemeToggle />
            </div>
          </div>
        </div>
        {bulkActionsEnabled && (
          <div className="container mx-auto px-3 sm:px-4 pb-3 sm:pb-4">
            <div className="flex flex-wrap items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleSelectAll}
                className="text-xs sm:text-sm bg-transparent"
              >
                {selectedTaskIds.length === tasks.length ? "Deselect All" : "Select All"}
              </Button>
              {selectedTaskIds.length > 0 && (
                <>
                  <Badge className="text-xs sm:text-sm">{selectedTaskIds.length} selected</Badge>
                  <Button variant="default" size="sm" onClick={handleBulkComplete} className="text-xs sm:text-sm">
                    Complete
                  </Button>
                  <Button variant="destructive" size="sm" onClick={handleBulkDelete} className="text-xs sm:text-sm">
                    Delete
                  </Button>
                </>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Main Content - Split Screen */}
      <div className="container mx-auto p-2 sm:p-4 h-[calc(100vh-80px)] sm:h-[calc(100vh-90px)] relative z-10">
        <div className="flex flex-col lg:flex-row gap-2 sm:gap-4 h-full">
          {/* Left Sidebar - Full width on mobile, 40% on desktop */}
          <div
            className={cn(
              "w-full lg:w-2/5 bg-card rounded-lg border border-border shadow-lg overflow-hidden",
              showMobileEditor && "hidden lg:block",
            )}
          >
            <TaskList
              tasks={tasks}
              selectedTask={selectedTask}
              onSelectTask={handleSelectTaskMobile}
              onToggleTask={handleToggleTask}
              selectedTaskIds={selectedTaskIds}
              onToggleSelection={handleToggleSelection}
              bulkActionsEnabled={bulkActionsEnabled}
            />
          </div>

          {/* Main Content - Full width on mobile when shown, 60% on desktop */}
          <div
            className={cn(
              "flex-1 bg-card rounded-lg border border-border shadow-lg overflow-hidden",
              !showMobileEditor && "hidden lg:block",
            )}
          >
            <div className="lg:hidden border-b border-border bg-card/50 p-2">
              <Button variant="ghost" size="sm" onClick={() => setShowMobileEditor(false)}>
                ← Back to List
              </Button>
            </div>
            <TaskEditor task={selectedTask} onUpdateTask={handleUpdateTask} onDeleteTask={handleDeleteTask} />
          </div>
        </div>
      </div>

      {/* New Task Modal */}
      <Dialog open={showNewTaskModal} onOpenChange={setShowNewTaskModal}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Create New Task</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div>
              <Label htmlFor="title">Title</Label>
              <Input
                id="title"
                value={newTask.title}
                onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
                placeholder="Enter task title..."
              />
            </div>
            <div>
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                value={newTask.description}
                onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                placeholder="Enter task description..."
              />
            </div>
            <div>
              <Label>Priority</Label>
              <div className="flex gap-2 mt-2">
                <Button
                  type="button"
                  variant={newTask.priority === "high" ? "default" : "outline"}
                  size="sm"
                  onClick={() => setNewTask({ ...newTask, priority: "high" })}
                  className={cn(newTask.priority === "high" && "bg-rose-500 hover:bg-rose-600")}
                >
                  <Flame className="size-4 mr-2" />
                  High
                </Button>
                <Button
                  type="button"
                  variant={newTask.priority === "medium" ? "default" : "outline"}
                  size="sm"
                  onClick={() => setNewTask({ ...newTask, priority: "medium" })}
                  className={cn(newTask.priority === "medium" && "bg-amber-500 hover:bg-amber-600")}
                >
                  <Zap className="size-4 mr-2" />
                  Medium
                </Button>
                <Button
                  type="button"
                  variant={newTask.priority === "low" ? "default" : "outline"}
                  size="sm"
                  onClick={() => setNewTask({ ...newTask, priority: "low" })}
                  className={cn(newTask.priority === "low" && "bg-emerald-500 hover:bg-emerald-600")}
                >
                  <Droplet className="size-4 mr-2" />
                  Low
                </Button>
              </div>
            </div>
            <div>
              <Label>Due Date</Label>
              <Popover>
                <PopoverTrigger asChild>
                  <Button variant="outline" className="w-full justify-start text-left font-normal mt-2 bg-transparent">
                    <CalendarIcon className="mr-2 size-4" />
                    {newTask.dueDate ? format(new Date(newTask.dueDate), "PPP") : "Pick a date"}
                  </Button>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0">
                  <Calendar
                    mode="single"
                    selected={newTask.dueDate ? new Date(newTask.dueDate) : undefined}
                    onSelect={(date) => setNewTask({ ...newTask, dueDate: date?.toISOString() || "" })}
                    initialFocus
                  />
                </PopoverContent>
              </Popover>
            </div>
          </div>
          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={() => setShowNewTaskModal(false)}>
              Cancel
            </Button>
            <Button onClick={handleCreateTask}>Create Task</Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}

export default function TasksPage() {
  return (
    <ProtectedRoute>
      <TasksContent />
    </ProtectedRoute>
  )
}
