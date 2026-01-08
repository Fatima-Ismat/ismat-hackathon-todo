"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Calendar } from "@/components/ui/calendar"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Separator } from "@/components/ui/separator"
import { Checkbox } from "@/components/ui/checkbox"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import { CalendarIcon, Flame, Zap, Droplet, Trash2, Copy, Share2, Plus, X, Edit2, Save } from "lucide-react"
import { format, isValid, parseISO } from "date-fns"
import { cn } from "@/lib/utils"
import type { Task, Subtask } from "@/lib/types"
import { useToast } from "@/hooks/use-toast"

interface TaskEditorProps {
  task: Task | null
  onUpdateTask: (id: string, updates: Partial<Task>) => void
  onDeleteTask: (id: string) => void
}

export function TaskEditor({ task, onUpdateTask, onDeleteTask }: TaskEditorProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [editedTask, setEditedTask] = useState<Task | null>(null)
  const [showDeleteDialog, setShowDeleteDialog] = useState(false)
  const [newTag, setNewTag] = useState("")
  const [newSubtask, setNewSubtask] = useState("")
  const [lastSaved, setLastSaved] = useState<Date | null>(null)
  const { toast } = useToast()

  if (task && !editedTask) {
    setEditedTask(task)
  }

  if (task && editedTask && task.id !== editedTask.id) {
    setEditedTask(task)
    setIsEditing(false)
  }

  const handleUpdate = (updates: Partial<Task>) => {
    if (isEditing && editedTask) {
      setEditedTask({ ...editedTask, ...updates })
    }
  }

  const handleSaveEdits = () => {
    if (editedTask) {
      onUpdateTask(editedTask.id, editedTask)
      setLastSaved(new Date())
      setIsEditing(false)
      toast({
        title: "Task updated",
        description: "Your changes have been saved",
      })
    }
  }

  const handleCancelEdit = () => {
    setEditedTask(task)
    setIsEditing(false)
  }

  const handleStartEdit = () => {
    setEditedTask(task)
    setIsEditing(true)
  }

  if (!task) {
    return (
      <div className="h-full flex items-center justify-center text-center p-8">
        <div>
          <p className="text-lg font-medium text-muted-foreground mb-2">No task selected</p>
          <p className="text-sm text-muted-foreground">Select a task from the list or create a new one</p>
        </div>
      </div>
    )
  }

  const displayTask = editedTask || task

  const safeFormatDate = (dateString: string | undefined, formatStr: string) => {
    if (!dateString) return null
    try {
      const date = typeof dateString === "string" ? parseISO(dateString) : new Date(dateString)
      return isValid(date) ? format(date, formatStr) : null
    } catch {
      return null
    }
  }

  const safeParseDateString = (dateString: string | undefined): Date | undefined => {
    if (!dateString) return undefined
    try {
      const date = typeof dateString === "string" ? parseISO(dateString) : new Date(dateString)
      return isValid(date) ? date : undefined
    } catch {
      return undefined
    }
  }

  const handleAddTag = () => {
    if (newTag.trim() && !displayTask.tags?.includes(newTag.trim())) {
      handleUpdate({ tags: [...(displayTask.tags || []), newTag.trim()] })
      setNewTag("")
    }
  }

  const handleRemoveTag = (tag: string) => {
    handleUpdate({ tags: displayTask.tags?.filter((t) => t !== tag) })
  }

  const handleAddSubtask = () => {
    if (newSubtask.trim()) {
      const subtask: Subtask = {
        id: crypto.randomUUID(),
        title: newSubtask.trim(),
        completed: false,
      }
      handleUpdate({ subtasks: [...(displayTask.subtasks || []), subtask] })
      setNewSubtask("")
    }
  }

  const handleToggleSubtask = (subtaskId: string) => {
    const updatedSubtasks = displayTask.subtasks?.map((st) =>
      st.id === subtaskId ? { ...st, completed: !st.completed } : st,
    )
    handleUpdate({ subtasks: updatedSubtasks })
  }

  const handleDuplicate = () => {
    toast({
      title: "Task duplicated",
      description: "A copy of this task has been created",
    })
  }

  const handleShare = () => {
    navigator.clipboard.writeText(task.title)
    toast({
      title: "Link copied",
      description: "Task link copied to clipboard",
    })
  }

  return (
    <div className="h-full flex flex-col">
      <div className="px-3 sm:px-6 py-2 sm:py-3 border-b border-border bg-card/50 flex items-center justify-between">
        <div className="text-xs sm:text-sm text-muted-foreground">
          {lastSaved && !isEditing && (
            <span className="flex items-center gap-1.5 sm:gap-2">
              <span className="size-1.5 sm:size-2 bg-green-500 rounded-full animate-pulse" />
              <span className="hidden sm:inline">Saved {format(lastSaved, "HH:mm:ss")}</span>
              <span className="sm:hidden">Saved</span>
            </span>
          )}
          {isEditing && <span className="flex items-center gap-1.5 sm:gap-2 text-amber-500">Editing</span>}
        </div>
        <div className="flex gap-1.5 sm:gap-2">
          {!isEditing ? (
            <Button size="sm" onClick={handleStartEdit} className="text-xs sm:text-sm">
              <Edit2 className="size-3 sm:size-4 sm:mr-2" />
              <span className="hidden sm:inline">Edit Task</span>
              <span className="sm:hidden">Edit</span>
            </Button>
          ) : (
            <>
              <Button
                size="sm"
                variant="outline"
                onClick={handleCancelEdit}
                className="text-xs sm:text-sm bg-transparent"
              >
                Cancel
              </Button>
              <Button size="sm" onClick={handleSaveEdits} className="text-xs sm:text-sm">
                <Save className="size-3 sm:size-4 sm:mr-2" />
                <span className="hidden sm:inline">Save</span>
                <span className="sm:hidden">✓</span>
              </Button>
            </>
          )}
        </div>
      </div>

      <ScrollArea className="flex-1">
        <div className="p-3 sm:p-6 space-y-4 sm:space-y-6 pb-16">
          {/* Title */}
          <div>
            <Input
              value={displayTask.title}
              onChange={(e) => handleUpdate({ title: e.target.value })}
              className="text-lg sm:text-2xl font-bold border-none px-0 focus-visible:ring-0"
              placeholder="Task title"
              disabled={!isEditing}
            />
          </div>

          {/* Priority Selector */}
          <div>
            <label className="text-xs sm:text-sm font-medium mb-2 block">Priority</label>
            <div className="flex gap-1.5 sm:gap-2">
              <Button
                variant={displayTask.priority === "high" ? "default" : "outline"}
                size="sm"
                onClick={() => handleUpdate({ priority: "high" })}
                disabled={!isEditing}
                className={cn("text-xs sm:text-sm", displayTask.priority === "high" && "bg-rose-500 hover:bg-rose-600")}
              >
                <Flame className="size-3 sm:size-4 sm:mr-2" />
                <span className="hidden sm:inline">High</span>
              </Button>
              <Button
                variant={displayTask.priority === "medium" ? "default" : "outline"}
                size="sm"
                onClick={() => handleUpdate({ priority: "medium" })}
                disabled={!isEditing}
                className={cn(
                  "text-xs sm:text-sm",
                  displayTask.priority === "medium" && "bg-amber-500 hover:bg-amber-600",
                )}
              >
                <Zap className="size-3 sm:size-4 sm:mr-2" />
                <span className="hidden sm:inline">Medium</span>
              </Button>
              <Button
                variant={displayTask.priority === "low" ? "default" : "outline"}
                size="sm"
                onClick={() => handleUpdate({ priority: "low" })}
                disabled={!isEditing}
                className={cn(
                  "text-xs sm:text-sm",
                  displayTask.priority === "low" && "bg-emerald-500 hover:bg-emerald-600",
                )}
              >
                <Droplet className="size-3 sm:size-4 sm:mr-2" />
                <span className="hidden sm:inline">Low</span>
              </Button>
            </div>
          </div>

          {/* Due Date */}
          <div>
            <label className="text-xs sm:text-sm font-medium mb-2 block">Due Date</label>
            <Popover>
              <PopoverTrigger asChild>
                <Button
                  variant="outline"
                  className="w-full justify-start text-left font-normal bg-transparent"
                  disabled={!isEditing}
                >
                  <CalendarIcon className="mr-2 size-4" />
                  {safeFormatDate(displayTask.dueDate, "PPP") || "Pick a date"}
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-auto p-0">
                <Calendar
                  mode="single"
                  selected={safeParseDateString(displayTask.dueDate)}
                  onSelect={(date) => handleUpdate({ dueDate: date?.toISOString() || "" })}
                  initialFocus
                />
              </PopoverContent>
            </Popover>
          </div>

          {/* Description */}
          <div className="mb-8">
            <label className="text-xs sm:text-sm font-medium mb-2 block">Description</label>
            <Textarea
              value={displayTask.description || ""}
              onChange={(e) => handleUpdate({ description: e.target.value })}
              placeholder="Add a description..."
              className="min-h-[120px] sm:min-h-[150px] text-sm sm:text-base resize-none mb-4"
              disabled={!isEditing}
            />
          </div>

          {/* Tags */}
          <div>
            <label className="text-xs sm:text-sm font-medium mb-2 block">Tags</label>
            <div className="flex flex-wrap gap-2 mb-2">
              {displayTask.tags?.map((tag) => (
                <Badge key={tag} variant="secondary" className="gap-1">
                  {tag}
                  {isEditing && <X className="size-3 cursor-pointer" onClick={() => handleRemoveTag(tag)} />}
                </Badge>
              ))}
            </div>
            {isEditing && (
              <div className="flex gap-2">
                <Input
                  value={newTag}
                  onChange={(e) => setNewTag(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleAddTag()}
                  placeholder="Add a tag..."
                />
                <Button size="sm" onClick={handleAddTag}>
                  <Plus className="size-4" />
                </Button>
              </div>
            )}
          </div>

          {/* Subtasks */}
          <div>
            <label className="text-xs sm:text-sm font-medium mb-2 block">Subtasks</label>
            <div className="space-y-2 mb-2">
              {displayTask.subtasks?.map((subtask) => (
                <div key={subtask.id} className="flex items-center gap-2">
                  <Checkbox
                    checked={subtask.completed}
                    onCheckedChange={() => handleToggleSubtask(subtask.id)}
                    disabled={!isEditing}
                  />
                  <span className={cn("text-sm", subtask.completed && "line-through text-muted-foreground")}>
                    {subtask.title}
                  </span>
                </div>
              ))}
            </div>
            {isEditing && (
              <div className="flex gap-2">
                <Input
                  value={newSubtask}
                  onChange={(e) => setNewSubtask(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleAddSubtask()}
                  placeholder="Add a subtask..."
                />
                <Button size="sm" onClick={handleAddSubtask}>
                  <Plus className="size-4" />
                </Button>
              </div>
            )}
          </div>

          <Separator />

          {/* Activity Log */}
          <div>
            <label className="text-xs sm:text-sm font-medium mb-2 block">Activity</label>
            <div className="text-xs sm:text-sm text-muted-foreground space-y-1">
              <p>Created: {safeFormatDate(displayTask.createdAt, "PPP") || "Unknown"}</p>
              <p>Status: {displayTask.status}</p>
            </div>
          </div>
        </div>
      </ScrollArea>

      {/* Action Buttons */}
      <div className="p-3 sm:p-4 border-t border-border bg-card">
        <div className="flex gap-1.5 sm:gap-2">
          <Button className="flex-1 bg-transparent text-xs sm:text-sm" variant="outline" onClick={handleDuplicate}>
            <Copy className="size-3 sm:size-4 sm:mr-2" />
            <span className="hidden sm:inline">Duplicate</span>
          </Button>
          <Button variant="outline" onClick={handleShare} className="text-xs sm:text-sm bg-transparent">
            <Share2 className="size-3 sm:size-4 sm:mr-2" />
            <span className="hidden sm:inline">Share</span>
          </Button>
          <Button variant="destructive" onClick={() => setShowDeleteDialog(true)} className="text-xs sm:text-sm">
            <Trash2 className="size-3 sm:size-4 sm:mr-2" />
            <span className="hidden sm:inline">Delete</span>
          </Button>
        </div>
      </div>

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Are you sure?</AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. This will permanently delete the task.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={() => {
                onDeleteTask(task.id)
                setShowDeleteDialog(false)
              }}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}
