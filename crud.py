from sqlalchemy.orm import Session
import models,schemas

def get_todos(db :Session):
    return db.query(models.Todo).all()

def get_todo(db:Session,todo_id:int):
    return db.query(models.Todo).filter(models.Todo.id==todo_id).first()

def create_todo(db:Session, todo:schemas.ToDoCreate ):
    db_todo=models.Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db:Session,todo_id:int,updated_data:schemas.ToDoUpdate):
    db_todo=get_todo(db,todo_id)
    if not db_todo:
        return None

    if updated_data.title is not None:
        db_todo.title = updated_data.title
    if updated_data.description is not None:
        db_todo.description = updated_data.description
    if updated_data.completed is not None:
        db_todo.completed = updated_data.completed

    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db:Session,todo_id:int):
    db_todo=get_todo(db,todo_id)
    if not db_todo:
        return None
    
    db.delete(db_todo)
    db.commit()
    return True

 


