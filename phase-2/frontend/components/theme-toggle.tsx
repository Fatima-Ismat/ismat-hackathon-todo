"use client"

import { Moon, Sun } from "lucide-react"
import { useTheme } from "@/components/theme-provider"
import { Button } from "@/components/ui/button"
import { useEffect, useState } from "react"

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  const toggleTheme = () => {
    const newTheme = theme === "dark" ? "light" : "dark"
    setTheme(newTheme)
  }

  if (!mounted) {
    return (
      <Button
        variant="outline"
        size="icon"
        className="size-10 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border-slate-200 dark:border-slate-700"
      />
    )
  }

  return (
    <Button
      variant="outline"
      size="icon"
      className="size-10 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border-slate-200 dark:border-slate-700 hover:bg-white dark:hover:bg-slate-800 transition-all"
      onClick={toggleTheme}
    >
      {theme === "dark" ? <Sun className="size-5 text-amber-500" /> : <Moon className="size-5 text-indigo-600" />}
      <span className="sr-only">Toggle theme</span>
    </Button>
  )
}
