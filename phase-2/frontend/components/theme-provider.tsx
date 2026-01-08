"use client"

import { createContext, useContext, useEffect, useState, type ReactNode } from "react"

type Theme = "light" | "dark"

type ThemeProviderProps = {
  children: ReactNode
  attribute?: string
  defaultTheme?: Theme
  enableSystem?: boolean
  disableTransitionOnChange?: boolean
}

type ThemeProviderState = {
  theme: Theme
  setTheme: (theme: Theme) => void
  themes: Theme[]
}

const ThemeProviderContext = createContext<ThemeProviderState | undefined>(undefined)

export function ThemeProvider({ children, defaultTheme = "dark", attribute = "class", ...props }: ThemeProviderProps) {
  const [theme, setThemeState] = useState<Theme>(defaultTheme)

  useEffect(() => {
    const stored = localStorage.getItem("theme") as Theme | null
    if (stored && (stored === "light" || stored === "dark")) {
      setThemeState(stored)
      document.documentElement.classList.toggle("dark", stored === "dark")
    } else {
      document.documentElement.classList.toggle("dark", defaultTheme === "dark")
    }
  }, [defaultTheme])

  const setTheme = (newTheme: Theme) => {
    setThemeState(newTheme)
    localStorage.setItem("theme", newTheme)
    document.documentElement.classList.toggle("dark", newTheme === "dark")
  }

  return (
    <ThemeProviderContext.Provider value={{ theme, setTheme, themes: ["light", "dark"] }}>
      {children}
    </ThemeProviderContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeProviderContext)
  if (context === undefined) {
    throw new Error("useTheme must be used within a ThemeProvider")
  }
  return context
}
