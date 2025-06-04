from typing import Literal
from loguru import logger
from fastapi import (
    APIRouter,
    status,
)
from pydantic import BaseModel, Field
from config import settings
from src.infrastructure.application import create_app
import src.rest as rest

logger.add(
    "".join(
        [
            str(settings.root_dir),
            "/logs/",
            settings.logging.file.lower(),
            ".log",
        ]
    ),
    format=settings.logging.format,
    rotation=settings.logging.rotation,
    compression=settings.logging.compression,
    level="INFO",
)


app = create_app(
    debug=settings.debug,
    rest_routers=(
        rest.posts.router,
        rest.users.router,
        rest.food_items.router,
        rest.websocket.router,
    ),
    startup_tasks=None,
    shutdown_tasks=None,
)

router = APIRouter()


@app.get("/", status_code=status.HTTP_200_OK)
async def ping():
    return {"msg": "Hello World"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "debug": settings.debug}


class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}
    limit: int = Field(10, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"


@app.get("/items/")
async def read_items(filter_query: FilterParams):
    return {"data": filter_query}
