"use client"

import { useState } from "react"
import { Search, Flame, Zap, Droplet } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { cn } from "@/lib/utils"
import type { Task, FilterType, SortType } from "@/lib/types"
import { format } from "date-fns"

interface TaskListProps {
  tasks: Task[]
  selectedTask: Task | null
  onSelectTask: (task: Task) => void
  onToggleTask: (id: string) => void
  selectedTaskIds?: string[]
  onToggleSelection?: (id: string) => void
  bulkActionsEnabled?: boolean
}

export function TaskList({
  tasks,
  selectedTask,
  onSelectTask,
  onToggleTask,
  selectedTaskIds = [],
  onToggleSelection,
  bulkActionsEnabled = false,
}: TaskListProps) {
  const [searchQuery, setSearchQuery] = useState("")
  const [filter, setFilter] = useState<FilterType>("all")
  const [sortBy, setSortBy] = useState<SortType>("date")

  const getPriorityIcon = (priority: string) => {
    switch (priority) {
      case "high":
        return <Flame className="size-4 text-rose-500" />
      case "medium":
        return <Zap className="size-4 text-amber-500" />
      case "low":
        return <Droplet className="size-4 text-emerald-500" />
    }
  }

  const filteredTasks = tasks
    .filter((task) => {
      if (filter === "all") return true
      if (filter === "pending" || filter === "completed") return task.status === filter
      return task.priority === filter
    })
    .filter((task) => task.title.toLowerCase().includes(searchQuery.toLowerCase()))
    .sort((a, b) => {
      if (sortBy === "date") return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
      if (sortBy === "priority") {
        const priorityOrder = { high: 0, medium: 1, low: 2 }
        return priorityOrder[a.priority] - priorityOrder[b.priority]
      }
      return a.title.localeCompare(b.title)
    })

  return (
    <div className="flex flex-col h-full">
      {/* Search Bar */}
      <div className="p-3 sm:p-4 border-b border-border bg-card">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 size-4 text-muted-foreground" />
          <Input
            placeholder="Search tasks..."
            className="pl-10 text-sm sm:text-base"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>

      {/* Filters */}
      <div className="p-3 sm:p-4 border-b border-border bg-card space-y-3">
        <div className="flex flex-wrap gap-1.5 sm:gap-2">
          <Badge
            variant={filter === "all" ? "default" : "outline"}
            className="cursor-pointer text-xs sm:text-sm"
            onClick={() => setFilter("all")}
          >
            All
          </Badge>
          <Badge
            variant={filter === "pending" ? "default" : "outline"}
            className="cursor-pointer text-xs sm:text-sm"
            onClick={() => setFilter("pending")}
          >
            Pending
          </Badge>
          <Badge
            variant={filter === "completed" ? "default" : "outline"}
            className="cursor-pointer text-xs sm:text-sm"
            onClick={() => setFilter("completed")}
          >
            Completed
          </Badge>
          <Badge
            variant={filter === "high" ? "default" : "outline"}
            className="cursor-pointer text-xs sm:text-sm"
            onClick={() => setFilter("high")}
          >
            High
          </Badge>
          <Badge
            variant={filter === "medium" ? "default" : "outline"}
            className="cursor-pointer text-xs sm:text-sm"
            onClick={() => setFilter("medium")}
          >
            Medium
          </Badge>
          <Badge
            variant={filter === "low" ? "default" : "outline"}
            className="cursor-pointer text-xs sm:text-sm"
            onClick={() => setFilter("low")}
          >
            Low
          </Badge>
        </div>

        <Select value={sortBy} onValueChange={(value) => setSortBy(value as SortType)}>
          <SelectTrigger className="text-sm sm:text-base">
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="date">Date</SelectItem>
            <SelectItem value="priority">Priority</SelectItem>
            <SelectItem value="title">Title</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Task List */}
      <ScrollArea className="flex-1">
        <div className="p-2">
          {filteredTasks.length === 0 ? (
            <div className="text-center py-12 text-muted-foreground">
              <p className="text-sm sm:text-base">No tasks found</p>
            </div>
          ) : (
            <div className="space-y-2">
              {filteredTasks.map((task) => (
                <div
                  key={task.id}
                  onClick={() => onSelectTask(task)}
                  className={cn(
                    "p-3 sm:p-4 rounded-lg border border-border bg-card hover:bg-accent/50 cursor-pointer transition-colors",
                    selectedTask?.id === task.id && "bg-accent border-primary",
                    bulkActionsEnabled && selectedTaskIds.includes(task.id) && "ring-2 ring-primary",
                  )}
                >
                  <div className="flex items-start gap-2 sm:gap-3">
                    {bulkActionsEnabled && onToggleSelection ? (
                      <Checkbox
                        checked={selectedTaskIds.includes(task.id)}
                        onCheckedChange={() => onToggleSelection(task.id)}
                        onClick={(e) => e.stopPropagation()}
                        className="mt-0.5 sm:mt-1"
                      />
                    ) : (
                      <Checkbox
                        checked={task.status === "completed"}
                        onCheckedChange={() => onToggleTask(task.id)}
                        onClick={(e) => e.stopPropagation()}
                        className="mt-0.5 sm:mt-1"
                      />
                    )}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        {getPriorityIcon(task.priority)}
                        <h4
                          className={cn(
                            "font-medium text-xs sm:text-sm truncate",
                            task.status === "completed" && "line-through text-muted-foreground",
                          )}
                        >
                          {task.title}
                        </h4>
                      </div>
                      {task.dueDate && (
                        <p className="text-[10px] sm:text-xs text-muted-foreground">
                          Due: {format(new Date(task.dueDate), "MMM d, yyyy")}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </ScrollArea>
    </div>
  )
}
