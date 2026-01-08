"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { TaskCard } from "./task-card"
import { ArrowLeft, Plus, Search } from "lucide-react"
import type { Task } from "@/lib/types"
import Link from "next/link"
import { Badge } from "@/components/ui/badge"

interface TaskListPanelProps {
  tasks: Task[]
  selectedTaskId: string | null
  onSelectTask: (taskId: string) => void
  onCreateTask: () => void
  onDeleteTask: (taskId: string) => void
  onDuplicateTask: (task: Task) => void
  onEditTask: (task: Task) => void
  onToggleComplete: (taskId: string) => void
}

type FilterType = "all" | "pending" | "completed" | "high"

export function TaskListPanel({
  tasks,
  selectedTaskId,
  onSelectTask,
  onCreateTask,
  onDeleteTask,
  onDuplicateTask,
  onEditTask,
  onToggleComplete,
}: TaskListPanelProps) {
  const [searchQuery, setSearchQuery] = useState("")
  const [filter, setFilter] = useState<FilterType>("all")

  const filteredTasks = tasks.filter((task) => {
    const matchesSearch = task.title.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesFilter =
      filter === "all" ||
      (filter === "pending" && task.status === "pending") ||
      (filter === "completed" && task.status === "completed") ||
      (filter === "high" && task.priority === "high")

    return matchesSearch && matchesFilter
  })

  const filterCounts = {
    all: tasks.length,
    pending: tasks.filter((t) => t.status === "pending").length,
    completed: tasks.filter((t) => t.status === "completed").length,
    high: tasks.filter((t) => t.priority === "high").length,
  }

  return (
    <div className="w-full lg:w-[400px] border-r border-border bg-card/50 backdrop-blur-sm flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-border space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link href="/">
              <Button variant="ghost" size="icon" className="h-9 w-9">
                <ArrowLeft className="h-5 w-5" />
              </Button>
            </Link>
            <h2 className="text-2xl font-bold">Tasks</h2>
          </div>
          <Button onClick={onCreateTask} size="sm" className="gap-2">
            <Plus className="h-4 w-4" />
            New
          </Button>
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search tasks..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-9"
          />
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-2">
          {(["all", "pending", "completed", "high"] as FilterType[]).map((filterType) => (
            <Button
              key={filterType}
              variant={filter === filterType ? "default" : "outline"}
              size="sm"
              onClick={() => setFilter(filterType)}
              className="gap-2"
            >
              {filterType.charAt(0).toUpperCase() + filterType.slice(1)}
              <Badge variant="secondary" className="ml-1 px-1.5 py-0 text-xs">
                {filterCounts[filterType]}
              </Badge>
            </Button>
          ))}
        </div>
      </div>

      {/* Task List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {filteredTasks.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center p-8">
            <div className="text-6xl mb-4">📋</div>
            <h3 className="text-lg font-semibold mb-2">No tasks found</h3>
            <p className="text-sm text-muted-foreground mb-4">Create a new task to get started</p>
            <Button onClick={onCreateTask} className="gap-2">
              <Plus className="h-4 w-4" />
              Create Task
            </Button>
          </div>
        ) : (
          filteredTasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              isSelected={task.id === selectedTaskId}
              onSelect={() => onSelectTask(task.id)}
              onDelete={() => onDeleteTask(task.id)}
              onDuplicate={() => onDuplicateTask(task)}
              onEdit={() => onEditTask(task)}
              onToggleComplete={() => onToggleComplete(task.id)}
            />
          ))
        )}
      </div>
    </div>
  )
}
