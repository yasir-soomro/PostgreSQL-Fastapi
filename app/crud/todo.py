from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.todo_model import Todo
from app.schemas.todo import TodoCreate


def create_todo(db: Session, payload: TodoCreate) -> Todo:
    db_todo = Todo(
        title=payload.title,
        description=payload.description,
        completed=payload.completed,
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def list_todos(db: Session, skip: int = 0, limit: int = 20) -> list[Todo]:
    stmt = (
        select(Todo)
        .order_by(Todo.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(db.scalars(stmt))
