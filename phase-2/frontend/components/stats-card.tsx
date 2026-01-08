"use client"

import { Card } from "@/components/ui/card"
import { cn } from "@/lib/utils"
import type { ReactNode } from "react"

interface StatsCardProps {
  title: string
  value: number | string
  icon: ReactNode
  color: "indigo" | "emerald" | "amber" | "rose"
  delay: number
}

export function StatsCard({ title, value, icon, color, delay }: StatsCardProps) {
  const colorClasses = {
    indigo: "bg-indigo-500/10 text-indigo-600 dark:text-indigo-400",
    emerald: "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400",
    amber: "bg-amber-500/10 text-amber-600 dark:text-amber-400",
    rose: "bg-rose-500/10 text-rose-600 dark:text-rose-400",
  }

  return (
    <Card
      className="p-6 glass hover-lift animate-in bg-card text-card-foreground"
      style={{
        animationDelay: `${delay}ms`,
        animationFillMode: "backwards",
      }}
    >
      <div className="flex items-center justify-between mb-4">
        <div className={cn("p-3 rounded-lg", colorClasses[color])}>{icon}</div>
      </div>
      <div className="space-y-1">
        <p className="text-sm font-medium text-muted-foreground">{title}</p>
        <p className="text-3xl font-bold text-foreground">{value}</p>
      </div>
    </Card>
  )
}
