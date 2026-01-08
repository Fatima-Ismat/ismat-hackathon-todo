import { NextResponse } from "next/server"
import { getSession } from "@/lib/auth"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export async function GET() {
  try {
    // Get session from cookies (stored during login)
    const session = await getSession()

    console.log("[/api/auth/me] Session data:", session ? 'Found' : 'Not found')

    if (!session) {
      console.log("[/api/auth/me] No session, returning 401")
      return NextResponse.json({ error: "Not authenticated" }, { status: 401 })
    }

    console.log("[/api/auth/me] Returning user:", { id: session.userId, email: session.email })

    // Return session data (already validated during login)
    return NextResponse.json({
      user: {
        id: session.userId,
        email: session.email,
        name: session.email.split('@')[0], // Extract name from email
      },
    })
  } catch (error) {
    console.error("[/api/auth/me] Error:", error)
    return NextResponse.json({ error: "Failed to get user" }, { status: 500 })
  }
}