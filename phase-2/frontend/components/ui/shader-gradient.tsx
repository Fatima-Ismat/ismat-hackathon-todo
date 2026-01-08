"use client"

import { useEffect, useRef } from "react"
import { useTheme } from "@/components/theme-provider"
import { cn } from "@/lib/utils"

interface ShaderGradientProps {
  className?: string
  animate?: boolean
  intensity?: "low" | "medium" | "high"
}

export function ShaderGradient({ className, animate = true, intensity = "medium" }: ShaderGradientProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const themeContext = useTheme()
  const theme = themeContext ? themeContext.theme : "dark"

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext("2d")
    if (!ctx) return

    const resizeCanvas = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }
    resizeCanvas()
    window.addEventListener("resize", resizeCanvas)

    let animationId: number
    let time = 0

    const intensityMap = {
      low: 0.3,
      medium: 0.6,
      high: 1,
    }

    const isDark = theme === "dark"

    const render = () => {
      if (!animate) {
        const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height)
        if (isDark) {
          gradient.addColorStop(0, "rgba(79, 70, 229, 0.15)")
          gradient.addColorStop(0.5, "rgba(8, 145, 178, 0.1)")
          gradient.addColorStop(1, "rgba(16, 185, 129, 0.15)")
        } else {
          gradient.addColorStop(0, "rgba(99, 102, 241, 0.25)")
          gradient.addColorStop(0.5, "rgba(8, 145, 178, 0.15)")
          gradient.addColorStop(1, "rgba(16, 185, 129, 0.25)")
        }
        ctx.fillStyle = gradient
        ctx.fillRect(0, 0, canvas.width, canvas.height)
        return
      }

      time += 0.001 * intensityMap[intensity]

      ctx.fillStyle = isDark ? "rgba(2, 6, 23, 0.05)" : "rgba(255, 255, 255, 0.05)"
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      // Create multiple animated gradients for depth
      for (let i = 0; i < 3; i++) {
        const offset = (i * Math.PI * 2) / 3
        const gradient = ctx.createRadialGradient(
          canvas.width / 2 + Math.sin(time + offset) * canvas.width * 0.3,
          canvas.height / 2 + Math.cos(time + offset) * canvas.height * 0.3,
          0,
          canvas.width / 2 + Math.sin(time + offset) * canvas.width * 0.3,
          canvas.height / 2 + Math.cos(time + offset) * canvas.height * 0.3,
          canvas.width * 0.6,
        )

        if (isDark) {
          if (i === 0) {
            gradient.addColorStop(0, "rgba(79, 70, 229, 0.2)")
            gradient.addColorStop(0.5, "rgba(79, 70, 229, 0.08)")
            gradient.addColorStop(1, "rgba(79, 70, 229, 0)")
          } else if (i === 1) {
            gradient.addColorStop(0, "rgba(8, 145, 178, 0.18)")
            gradient.addColorStop(0.5, "rgba(8, 145, 178, 0.06)")
            gradient.addColorStop(1, "rgba(8, 145, 178, 0)")
          } else {
            gradient.addColorStop(0, "rgba(16, 185, 129, 0.18)")
            gradient.addColorStop(0.5, "rgba(16, 185, 129, 0.06)")
            gradient.addColorStop(1, "rgba(16, 185, 129, 0)")
          }
        } else {
          if (i === 0) {
            gradient.addColorStop(0, "rgba(99, 102, 241, 0.35)")
            gradient.addColorStop(0.5, "rgba(99, 102, 241, 0.15)")
            gradient.addColorStop(1, "rgba(99, 102, 241, 0)")
          } else if (i === 1) {
            gradient.addColorStop(0, "rgba(8, 145, 178, 0.3)")
            gradient.addColorStop(0.5, "rgba(8, 145, 178, 0.12)")
            gradient.addColorStop(1, "rgba(8, 145, 178, 0)")
          } else {
            gradient.addColorStop(0, "rgba(16, 185, 129, 0.3)")
            gradient.addColorStop(0.5, "rgba(16, 185, 129, 0.12)")
            gradient.addColorStop(1, "rgba(16, 185, 129, 0)")
          }
        }

        ctx.fillStyle = gradient
        ctx.fillRect(0, 0, canvas.width, canvas.height)
      }

      animationId = requestAnimationFrame(render)
    }

    render()

    return () => {
      cancelAnimationFrame(animationId)
      window.removeEventListener("resize", resizeCanvas)
    }
  }, [animate, intensity, theme])

  return (
    <canvas
      ref={canvasRef}
      className={cn("fixed inset-0 pointer-events-none", className)}
      style={{
        zIndex: 0,
      }}
    />
  )
}
