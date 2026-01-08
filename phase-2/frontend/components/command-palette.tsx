"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command"
import { Home, ListTodo, Plus, Sun, Moon } from "lucide-react"
import { useTheme } from "next-themes"

interface CommandPaletteProps {
  onNewTask?: () => void
}

export function CommandPalette({ onNewTask }: CommandPaletteProps) {
  const [open, setOpen] = useState(false)
  const router = useRouter()
  const { setTheme } = useTheme()

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault()
        setOpen((open) => !open)
      }
    }
    document.addEventListener("keydown", down)
    return () => document.removeEventListener("keydown", down)
  }, [])

  return (
    <CommandDialog open={open} onOpenChange={setOpen}>
      <CommandInput placeholder="Type a command or search..." />
      <CommandList>
        <CommandEmpty>No results found.</CommandEmpty>
        <CommandGroup heading="Navigation">
          <CommandItem
            onSelect={() => {
              router.push("/")
              setOpen(false)
            }}
          >
            <Home className="mr-2 size-4" />
            Dashboard
          </CommandItem>
          <CommandItem
            onSelect={() => {
              router.push("/tasks")
              setOpen(false)
            }}
          >
            <ListTodo className="mr-2 size-4" />
            Tasks
          </CommandItem>
        </CommandGroup>
        <CommandGroup heading="Actions">
          <CommandItem
            onSelect={() => {
              onNewTask?.()
              setOpen(false)
            }}
          >
            <Plus className="mr-2 size-4" />
            New Task
          </CommandItem>
        </CommandGroup>
        <CommandGroup heading="Theme">
          <CommandItem
            onSelect={() => {
              setTheme("light")
              setOpen(false)
            }}
          >
            <Sun className="mr-2 size-4" />
            Light Mode
          </CommandItem>
          <CommandItem
            onSelect={() => {
              setTheme("dark")
              setOpen(false)
            }}
          >
            <Moon className="mr-2 size-4" />
            Dark Mode
          </CommandItem>
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  )
}
