"use client"

import { useState } from "react"
import { TaskListPanel } from "./task-list-panel"
import { TaskDetailPanel } from "./task-detail-panel"
import { TaskFormModal } from "./task-form-modal"
import type { Task } from "@/lib/types"

const mockTasks: Task[] = [
  {
    id: "1",
    title: "Complete project proposal",
    description: "Write a comprehensive proposal for the new client project including timeline and budget",
    priority: "high",
    status: "pending",
    dueDate: new Date(Date.now() + 2 * 60 * 60 * 1000).toISOString(),
    tags: ["urgent", "client"],
    createdAt: new Date().toISOString(),
  },
  {
    id: "2",
    title: "Review design mockups",
    description: "Check the latest UI/UX designs and provide feedback to the design team",
    priority: "medium",
    status: "pending",
    dueDate: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
    tags: ["design", "review"],
    createdAt: new Date().toISOString(),
  },
  {
    id: "3",
    title: "Update documentation",
    description: "Add new API endpoints to the developer documentation",
    priority: "low",
    status: "completed",
    dueDate: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString(),
    tags: ["docs"],
    createdAt: new Date().toISOString(),
  },
]

export function TaskManager() {
  const [tasks, setTasks] = useState<Task[]>(mockTasks)
  const [selectedTaskId, setSelectedTaskId] = useState<string | null>(tasks[0]?.id || null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingTask, setEditingTask] = useState<Task | undefined>(undefined)

  const selectedTask = tasks.find((task) => task.id === selectedTaskId)

  const handleCreateTask = (taskData: Omit<Task, "id" | "createdAt">) => {
    const newTask: Task = {
      ...taskData,
      id: Date.now().toString(),
      createdAt: new Date().toISOString(),
    }
    setTasks([newTask, ...tasks])
    setSelectedTaskId(newTask.id)
    setIsModalOpen(false)
  }

  const handleUpdateTask = (taskId: string, updates: Partial<Task>) => {
    setTasks(tasks.map((task) => (task.id === taskId ? { ...task, ...updates } : task)))
  }

  const handleDeleteTask = (taskId: string) => {
    setTasks(tasks.filter((task) => task.id !== taskId))
    if (selectedTaskId === taskId) {
      setSelectedTaskId(tasks.find((t) => t.id !== taskId)?.id || null)
    }
  }

  const handleDuplicateTask = (task: Task) => {
    const duplicatedTask: Task = {
      ...task,
      id: Date.now().toString(),
      title: `${task.title} (Copy)`,
      createdAt: new Date().toISOString(),
    }
    setTasks([duplicatedTask, ...tasks])
    setSelectedTaskId(duplicatedTask.id)
  }

  const handleOpenEditModal = (task: Task) => {
    setEditingTask(task)
    setIsModalOpen(true)
  }

  const handleEditTask = (taskData: Omit<Task, "id" | "createdAt">) => {
    if (editingTask) {
      handleUpdateTask(editingTask.id, taskData)
      setIsModalOpen(false)
      setEditingTask(undefined)
    }
  }

  const handleCloseModal = () => {
    setIsModalOpen(false)
    setEditingTask(undefined)
  }

  return (
    <>
      <div className="h-screen flex flex-col lg:flex-row">
        <TaskListPanel
          tasks={tasks}
          selectedTaskId={selectedTaskId}
          onSelectTask={setSelectedTaskId}
          onCreateTask={() => setIsModalOpen(true)}
          onDeleteTask={handleDeleteTask}
          onDuplicateTask={handleDuplicateTask}
          onEditTask={handleOpenEditModal}
          onToggleComplete={(taskId) => {
            const task = tasks.find((t) => t.id === taskId)
            if (task) {
              handleUpdateTask(taskId, {
                status: task.status === "completed" ? "pending" : "completed",
              })
            }
          }}
        />
        <TaskDetailPanel
          task={selectedTask}
          onUpdateTask={handleUpdateTask}
          onDeleteTask={handleDeleteTask}
          onEditTask={handleOpenEditModal}
        />
      </div>

      <TaskFormModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onSubmit={editingTask ? handleEditTask : handleCreateTask}
        editingTask={editingTask}
      />
    </>
  )
}
