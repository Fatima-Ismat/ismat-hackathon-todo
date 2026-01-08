# FastAPI Backend Example - Aapke existing backend mein ye structure hona chahiye

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional
from datetime import datetime

app = FastAPI()

# CORS setup - Frontend ke liye zaroori
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLModel Task Schema
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str = ""
    priority: str = "medium"  # "high", "medium", "low"
    status: str = "pending"  # "pending", "completed"
    dueDate: Optional[str] = None
    createdAt: str = Field(default_factory=lambda: datetime.now().isoformat())

# Create Task (POST)
@app.post("/api/tasks")
def create_task(task: Task):
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

# Get All Tasks (GET)
@app.get("/api/tasks")
def get_tasks():
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()
        return tasks

# Update Task (PATCH)
@app.patch("/api/tasks/{task_id}")
def update_task(task_id: int, task_update: dict):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        for key, value in task_update.items():
            setattr(task, key, value)
        
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

# Delete Task (DELETE)
@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        session.delete(task)
        session.commit()
        return {"message": "Task deleted successfully"}
