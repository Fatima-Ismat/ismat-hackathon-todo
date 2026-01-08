import { type NextRequest, NextResponse } from "next/server"
import { createSession } from "@/lib/auth"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export async function POST(request: NextRequest) {
  try {
    // DEVELOPMENT MODE: Comment out for now to test actual backend
    // if (process.env.NODE_ENV === 'development') {
    //   console.log("Development mode: Mock login successful")
    //   
    //   const { email } = await request.json().catch(() => ({ email: "dev@test.com" }))
    //   
    //   return NextResponse.json({
    //     user: {
    //       id: "dev-user-" + Date.now(),
    //       email: email || "dev@test.com",
    //       name: "Developer"
    //     },
    //     token: "dev-token-" + Date.now(),
    //     message: "Development mode: Mock authentication"
    //   })
    // }

    // PRODUCTION MODE: Original code
    const { email, password } = await request.json()

    if (!email || !password) {
      return NextResponse.json({ error: "Email and password are required" }, { status: 400 })
    }

    // DEBUG LOG
    console.log("Signin attempt for:", email, "API_URL:", API_URL)

    const response = await fetch(`${API_URL}/api/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    })

    const data = await response.json()

    if (!response.ok) {
      return NextResponse.json({ error: data.detail || "Invalid credentials" }, { status: response.status })
    }

    // Extract user info from token payload
    const payload = JSON.parse(atob(data.access_token.split(".")[1]))

    await createSession(payload.sub, payload.email, data.access_token)

    // Return tokens so frontend can store them in localStorage
    return NextResponse.json({
      user: {
        id: payload.sub,
        email: payload.email,
        name: payload.username || payload.email.split("@")[0],
      },
      accessToken: data.access_token,
      refreshToken: data.refresh_token,
    })
  } catch (error) {
    console.error("Signin error:", error)
    
    // Development mode fallback - commented out
    // if (process.env.NODE_ENV === 'development') {
    //   return NextResponse.json({
    //     user: {
    //       id: "dev-error-user",
    //       email: "error@example.com",
    //       name: "Error User"
    //     },
    //     token: "dev-error-token"
    //   })
    // }
    
    return NextResponse.json({ error: "Failed to sign in" }, { status: 500 })
  }
}