from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, crud  # Absolute imports (no dot)
from database import SessionLocal, engine  # Absolute import (no dot)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

# create database table
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the directory where main.py is located
BASE_DIR = Path(__file__).resolve().parent

# Mount static files using absolute path
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# dependency to get db session for each object
def get_db():
    db = SessionLocal()
    try:
        yield db  # give the connection to the api function
    finally:
        db.close()

@app.get("/")
def home():
    return FileResponse(str(BASE_DIR / 'static' / 'index.html'))

# these is for creating 
@app.post("/todos/", response_model=schemas.ToDoResponse)
def create_todo(todo: schemas.ToDoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)

# to get all created 
@app.get("/todos/", response_model=list[schemas.ToDoResponse])
def get_all_todos(db: Session = Depends(get_db)):
    return crud.get_todos(db)

@app.get("/todos/{todo_id}", response_model=schemas.ToDoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=schemas.ToDoResponse)
def update_todo(todo_id: int, updated_data: schemas.ToDoUpdate, db: Session = Depends(get_db)):
    todo = crud.update_todo(db, todo_id, updated_data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    success = crud.delete_todo(db, todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="todo not found")
    return {"message": "Todo deleted successfully"}