from fastapi import FastAPI

from app.core.settings import get_settings
from app.routes.todo import router as todo_router

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.include_router(todo_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
