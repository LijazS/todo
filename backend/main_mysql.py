from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# ── DATABASE CONFIG ────────────────────────────────────────────────

DATABASE_URL = "mysql+mysqlconnector://username:password@localhost:3306/taskdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ── MODEL ──────────────────────────────────────────────────────────

class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), default="")
    completed = Column(Boolean, default=False)

# Create tables
Base.metadata.create_all(bind=engine)

# ── Pydantic Schemas ───────────────────────────────────────────────

class Task(BaseModel):
    title: str
    description: str = ""
    completed: bool = False

class TaskResponse(Task):
    id: int

    class Config:
        from_attributes = True  # For Pydantic v2

# ── APP SETUP ──────────────────────────────────────────────────────

app = FastAPI(title="Task Manager API (MySQL)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Dependency ─────────────────────────────────────────────────────

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ── Routes ─────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(TaskDB).all()


@app.post("/tasks", response_model=TaskResponse)
def create_task(task: Task, db: Session = Depends(get_db)):
    new_task = TaskDB(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: Task, db: Session = Depends(get_db)):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task.model_dump().items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()

    return {"message": "Deleted"}