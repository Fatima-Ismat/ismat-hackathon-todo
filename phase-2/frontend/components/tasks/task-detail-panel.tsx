"use client"

import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent } from "@/components/ui/card"
import type { Task } from "@/lib/types"
import { Calendar, Clock, Edit, Tag, Trash2 } from "lucide-react"
import { format } from "date-fns"

interface TaskDetailPanelProps {
  task?: Task
  onUpdateTask: (taskId: string, updates: Partial<Task>) => void
  onDeleteTask: (taskId: string) => void
  onEditTask: (task: Task) => void
}

export function TaskDetailPanel({ task, onUpdateTask, onDeleteTask, onEditTask }: TaskDetailPanelProps) {
  if (!task) {
    return (
      <div className="flex-1 flex items-center justify-center bg-card/30 backdrop-blur-sm">
        <div className="text-center p-8">
          <div className="text-6xl mb-4">📝</div>
          <h3 className="text-xl font-semibold mb-2">No task selected</h3>
          <p className="text-muted-foreground">Select a task from the list to view details</p>
        </div>
      </div>
    )
  }

  const priorityColors = {
    high: "destructive",
    medium: "warning",
    low: "success",
  } as const

  return (
    <div className="flex-1 overflow-y-auto bg-card/30 backdrop-blur-sm p-6 lg:p-8">
      <div className="max-w-3xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <Badge variant={priorityColors[task.priority]}>{task.priority} priority</Badge>
              <Badge variant={task.status === "completed" ? "success" : "secondary"}>{task.status}</Badge>
            </div>
            <h1 className="text-3xl font-bold text-balance">{task.title}</h1>
          </div>

          <div className="flex gap-2">
            <Button variant="outline" size="icon" onClick={() => onEditTask(task)}>
              <Edit className="h-4 w-4" />
            </Button>
            <Button variant="outline" size="icon" onClick={() => onDeleteTask(task.id)}>
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Meta Information */}
        <Card className="glass border-2">
          <CardContent className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-primary/10 text-primary">
                  <Calendar className="h-5 w-5" />
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Due Date</p>
                  <p className="font-semibold">{format(new Date(task.dueDate), "PPP")}</p>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-accent/10 text-accent">
                  <Clock className="h-5 w-5" />
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Created</p>
                  <p className="font-semibold">{format(new Date(task.createdAt), "PPP")}</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Description */}
        <Card className="glass border-2">
          <CardContent className="p-6">
            <h2 className="text-lg font-semibold mb-3">Description</h2>
            <p className="text-muted-foreground leading-relaxed">{task.description || "No description provided."}</p>
          </CardContent>
        </Card>

        {/* Tags */}
        {task.tags && task.tags.length > 0 && (
          <Card className="glass border-2">
            <CardContent className="p-6">
              <div className="flex items-center gap-2 mb-3">
                <Tag className="h-5 w-5 text-muted-foreground" />
                <h2 className="text-lg font-semibold">Tags</h2>
              </div>
              <div className="flex flex-wrap gap-2">
                {task.tags.map((tag) => (
                  <Badge key={tag} variant="outline" className="text-sm px-3 py-1">
                    {tag}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Actions */}
        <Card className="glass border-2">
          <CardContent className="p-6">
            <h2 className="text-lg font-semibold mb-4">Actions</h2>
            <div className="flex flex-wrap gap-3">
              <Button
                variant={task.status === "completed" ? "outline" : "default"}
                onClick={() =>
                  onUpdateTask(task.id, {
                    status: task.status === "completed" ? "pending" : "completed",
                  })
                }
              >
                {task.status === "completed" ? "Mark as Pending" : "Mark as Complete"}
              </Button>
              <Button variant="outline" onClick={() => onEditTask(task)}>
                <Edit className="h-4 w-4 mr-2" />
                Edit Task
              </Button>
              <Button variant="destructive" onClick={() => onDeleteTask(task.id)}>
                <Trash2 className="h-4 w-4 mr-2" />
                Delete Task
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
