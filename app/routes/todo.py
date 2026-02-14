import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.todo import create_todo as create_todo_record
from app.crud.todo import list_todos
from app.schemas.todo import TodoCreate, TodoOut

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)) -> TodoOut:
    try:
        return create_todo_record(db, todo)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Failed to create todo")
        raise HTTPException(status_code=500, detail="Failed to create todo")


@router.get("/", response_model=list[TodoOut])
def get_todos(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[TodoOut]:
    return list_todos(db=db, skip=skip, limit=limit)
