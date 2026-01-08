"use client"

import type React from "react"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { useAuth } from "@/lib/hooks/use-auth"

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    console.log("[ProtectedRoute] Auth state - user:", user, "isLoading:", isLoading)
    if (!isLoading && !user) {
      console.log("[ProtectedRoute] No user, redirecting to /login")
      router.push("/login")
    }
  }, [user, isLoading, router])

  if (isLoading) {
    console.log("[ProtectedRoute] Still loading, showing spinner")
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    console.log("[ProtectedRoute] No user after loading, showing redirect message")
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Redirecting to login...</p>
        </div>
      </div>
    )
  }

  console.log("[ProtectedRoute] User authenticated, rendering children")
  return <>{children}</>
}
