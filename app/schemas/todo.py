from pydantic import BaseModel, ConfigDict


class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False


class TodoOut(TodoCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
