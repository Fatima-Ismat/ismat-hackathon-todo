import { type NextRequest, NextResponse } from "next/server"
import { createSession } from "@/lib/auth"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export async function POST(request: NextRequest) {
  try {
    // DEVELOPMENT MODE: Comment out for now
    // if (process.env.NODE_ENV === 'development') {
    //   console.log("Development mode: Mock signup successful")
    //   
    //   const { email, name } = await request.json().catch(() => ({ email: "dev@test.com", name: "Developer" }))
    //   
    //   return NextResponse.json({
    //     user: {
    //       id: "dev-user-" + Date.now(),
    //       email: email || "dev@test.com",
    //       name: name || email?.split("@")[0] || "Developer"
    //     },
    //     token: "dev-token-" + Date.now(),
    //     message: "Development mode: Mock authentication"
    //   }, { status: 201 })
    // }

    // PRODUCTION MODE: Original code with backend call
    const { email, password, name } = await request.json()

    if (!email || !password) {
      return NextResponse.json({ error: "Email and password are required" }, { status: 400 })
    }

    // DEBUG LOG
    console.log("Signup attempt for:", email, "Name:", name)

    // Call backend API - backend expects 'username' and 'full_name' fields
    const response = await fetch(`${API_URL}/api/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
        password,
        username: name || email.split("@")[0] || "user_" + Date.now(),
        full_name: name || email.split("@")[0] || "User",  // ADDED THIS LINE
      }),
    })

    const data = await response.json()

    if (!response.ok) {
      return NextResponse.json({ error: data.detail || "Failed to create user" }, { status: response.status })
    }

    // Backend returns user data, now we need to login to get tokens
    const loginResponse = await fetch(`${API_URL}/api/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    })

    const loginData = await loginResponse.json()

    if (!loginResponse.ok) {
      return NextResponse.json({ error: "User created but login failed" }, { status: 500 })
    }

    // Extract user info from token payload
    const payload = JSON.parse(atob(loginData.access_token.split(".")[1]))

    await createSession(payload.sub, payload.email, loginData.access_token)

    // Return tokens so frontend can store them in localStorage
    return NextResponse.json(
      {
        user: {
          id: data.id,
          email: data.email,
          name: data.username,
        },
        accessToken: loginData.access_token,
        refreshToken: loginData.refresh_token,
      },
      { status: 201 },
    )
  } catch (error) {
    console.error("Signup error:", error)
    
    // Even in error, return success in development mode - commented out
    // if (process.env.NODE_ENV === 'development') {
    //   return NextResponse.json({
    //     user: {
    //       id: "dev-error-user",
    //       email: "error@example.com",
    //       name: "Error User"
    //     },
    //     token: "dev-error-token",
    //     message: "Development mode: Error fallback"
    //   }, { status: 200 })
    // }
    
    return NextResponse.json({ error: "Failed to create user" }, { status: 500 })
  }
}