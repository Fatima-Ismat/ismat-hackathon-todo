import { type NextRequest, NextResponse } from "next/server"
import { getDb } from "@/lib/db"
import { getSession } from "@/lib/auth"

export async function PATCH(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const session = await getSession()
    if (!session) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    const { id } = await params
    const sql = getDb()

    const updatedTasks = await sql`
      UPDATE tasks 
      SET status = 'completed', updated_at = CURRENT_TIMESTAMP
      WHERE id = ${id} AND user_id = ${session.userId}
      RETURNING *
    `

    if (updatedTasks.length === 0) {
      return NextResponse.json({ error: "Task not found" }, { status: 404 })
    }

    return NextResponse.json(updatedTasks[0])
  } catch (error) {
    console.error("Complete task error:", error)
    return NextResponse.json({ error: "Failed to complete task" }, { status: 500 })
  }
}
