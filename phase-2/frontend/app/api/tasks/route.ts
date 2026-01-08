import { type NextRequest, NextResponse } from "next/server"
import { getDb } from "@/lib/db"
import { getSession } from "@/lib/auth"

export async function GET() {
  try {
    const session = await getSession()
    if (!session) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    const sql = getDb()
    const tasks = await sql`
      SELECT * FROM tasks 
      WHERE user_id = ${session.userId}
      ORDER BY created_at DESC
    `

    return NextResponse.json(tasks)
  } catch (error) {
    console.error("Get tasks error:", error)
    return NextResponse.json({ error: "Failed to fetch tasks" }, { status: 500 })
  }
}

export async function POST(request: NextRequest) {
  try {
    const session = await getSession()
    if (!session) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    const body = await request.json()
    const { title, description, priority, dueDate, status } = body

    if (!title) {
      return NextResponse.json({ error: "Title is required" }, { status: 400 })
    }

    const sql = getDb()
    const newTasks = await sql`
      INSERT INTO tasks (user_id, title, description, priority, due_date, status)
      VALUES (
        ${session.userId}, 
        ${title}, 
        ${description || null}, 
        ${priority || "medium"}, 
        ${dueDate || null}, 
        ${status || "pending"}
      )
      RETURNING *
    `

    return NextResponse.json(newTasks[0], { status: 201 })
  } catch (error) {
    console.error("Create task error:", error)
    return NextResponse.json({ error: "Failed to create task" }, { status: 500 })
  }
}
