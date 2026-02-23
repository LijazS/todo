from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Task Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── In-memory storage ──────────────────────────────────────────────
tasks = {}
next_id = 1

class Task(BaseModel):
    title: str
    description: str = ""
    completed: bool = False

# ── Routes ─────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def list_tasks():
    return list(tasks.values())

@app.post("/tasks")
def create_task(task: Task):
    global next_id
    new = {"id": next_id, **task.model_dump()}
    tasks[next_id] = new
    next_id += 1
    return new

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id] = {"id": task_id, **task.model_dump()}
    return tasks[task_id]

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    return {"message": "Deleted"}
