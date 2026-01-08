"use client"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import type { Task } from "@/lib/types"
import { Calendar, Copy, MoreVertical, Pencil, Trash2 } from "lucide-react"
import { formatDistanceToNow } from "date-fns"

interface TaskCardProps {
  task: Task
  isSelected: boolean
  onSelect: () => void
  onDelete: () => void
  onDuplicate: () => void
  onEdit: () => void
  onToggleComplete: () => void
}

export function TaskCard({
  task,
  isSelected,
  onSelect,
  onDelete,
  onDuplicate,
  onEdit,
  onToggleComplete,
}: TaskCardProps) {
  const priorityColors = {
    high: "destructive",
    medium: "warning",
    low: "success",
  } as const

  const isOverdue = new Date(task.dueDate) < new Date() && task.status !== "completed"
  const timeUntilDue = formatDistanceToNow(new Date(task.dueDate), { addSuffix: true })

  return (
    <div
      onClick={onSelect}
      className={`p-4 rounded-lg border-2 transition-all duration-200 cursor-pointer hover:shadow-md ${
        isSelected ? "border-primary bg-primary/5 shadow-sm" : "border-border bg-card"
      }`}
    >
      <div className="flex items-start gap-3">
        <Checkbox
          checked={task.status === "completed"}
          onCheckedChange={onToggleComplete}
          onClick={(e) => e.stopPropagation()}
          className="mt-1"
        />

        <div className="flex-1 min-w-0">
          <h4
            className={`font-semibold text-sm mb-2 ${task.status === "completed" ? "line-through text-muted-foreground" : ""}`}
          >
            {task.title}
          </h4>

          <div className="flex flex-wrap items-center gap-2">
            <Badge variant={priorityColors[task.priority]} className="text-xs">
              {task.priority}
            </Badge>

            {task.tags?.map((tag) => (
              <Badge key={tag} variant="outline" className="text-xs">
                {tag}
              </Badge>
            ))}

            <div
              className={`flex items-center gap-1 text-xs ${isOverdue ? "text-destructive" : "text-muted-foreground"}`}
            >
              <Calendar className="h-3 w-3" />
              <span>{timeUntilDue}</span>
            </div>
          </div>
        </div>

        <DropdownMenu>
          <DropdownMenuTrigger asChild onClick={(e) => e.stopPropagation()}>
            <Button variant="ghost" size="icon" className="h-8 w-8">
              <MoreVertical className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={onEdit}>
              <Pencil className="h-4 w-4 mr-2" />
              Edit
            </DropdownMenuItem>
            <DropdownMenuItem onClick={onDuplicate}>
              <Copy className="h-4 w-4 mr-2" />
              Duplicate
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={onDelete} className="text-destructive">
              <Trash2 className="h-4 w-4 mr-2" />
              Delete
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>
  )
}
