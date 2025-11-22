from pydantic import BaseModel
from datetime import datetime

class ToDoBase(BaseModel):
    title : str
    description: str | None = None
    completed : bool = False 

class ToDoCreate(ToDoBase):
    pass

class ToDoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None

class ToDoResponse(ToDoBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode: True

        