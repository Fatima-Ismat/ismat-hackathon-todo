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
    const updates = await request.json()
    const sql = getDb()

    // Build dynamic update query
    const updateFields: string[] = []
    const values: any[] = []
    let paramIndex = 1

    if (updates.title !== undefined) {
      updateFields.push(`title = $${paramIndex}`)
      values.push(updates.title)
      paramIndex++
    }
    if (updates.description !== undefined) {
      updateFields.push(`description = $${paramIndex}`)
      values.push(updates.description)
      paramIndex++
    }
    if (updates.status !== undefined) {
      updateFields.push(`status = $${paramIndex}`)
      values.push(updates.status)
      paramIndex++
    }
    if (updates.priority !== undefined) {
      updateFields.push(`priority = $${paramIndex}`)
      values.push(updates.priority)
      paramIndex++
    }
    if (updates.dueDate !== undefined) {
      updateFields.push(`due_date = $${paramIndex}`)
      values.push(updates.dueDate)
      paramIndex++
    }

    if (updateFields.length === 0) {
      return NextResponse.json({ error: "No fields to update" }, { status: 400 })
    }

    updateFields.push(`updated_at = CURRENT_TIMESTAMP`)

    const updatedTasks = await sql`
      UPDATE tasks 
      SET title = ${updates.title !== undefined ? updates.title : sql`title`},
          description = ${updates.description !== undefined ? updates.description : sql`description`},
          status = ${updates.status !== undefined ? updates.status : sql`status`},
          priority = ${updates.priority !== undefined ? updates.priority : sql`priority`},
          due_date = ${updates.dueDate !== undefined ? updates.dueDate : sql`due_date`},
          updated_at = CURRENT_TIMESTAMP
      WHERE id = ${id} AND user_id = ${session.userId}
      RETURNING *
    `

    if (updatedTasks.length === 0) {
      return NextResponse.json({ error: "Task not found" }, { status: 404 })
    }

    return NextResponse.json(updatedTasks[0])
  } catch (error) {
    console.error("Update task error:", error)
    return NextResponse.json({ error: "Failed to update task" }, { status: 500 })
  }
}

export async function DELETE(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  try {
    const session = await getSession()
    if (!session) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    const { id } = await params
    const sql = getDb()

    const deletedTasks = await sql`
      DELETE FROM tasks 
      WHERE id = ${id} AND user_id = ${session.userId}
      RETURNING id
    `

    if (deletedTasks.length === 0) {
      return NextResponse.json({ error: "Task not found" }, { status: 404 })
    }

    return NextResponse.json({ success: true })
  } catch (error) {
    console.error("Delete task error:", error)
    return NextResponse.json({ error: "Failed to delete task" }, { status: 500 })
  }
}
